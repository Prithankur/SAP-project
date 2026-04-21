"""
Leave Balance Tracker — SAP HCM H2R Project
=============================================
Simulates SAP HCM Time Management (TM) leave quota tracking.
Tracks leave entitlements, applications, approvals, and balances.

Corresponds to SAP infotypes:
  IT 2006 — Absence Quotas (entitlements)
  IT 2001 — Absences (actual leave taken)
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional


# ── Leave Types (mapped to SAP Absence Types) ─────────────────────────────────

LEAVE_TYPES = {
    "CL": {"name": "Casual Leave",          "annual_quota": 12, "carry_forward": False, "encashable": False},
    "SL": {"name": "Sick Leave",             "annual_quota": 12, "carry_forward": True,  "max_carry": 30, "encashable": False},
    "EL": {"name": "Earned / Privilege Leave","annual_quota": 18, "carry_forward": True,  "max_carry": 45, "encashable": True},
    "ML": {"name": "Maternity Leave",        "annual_quota": 182, "carry_forward": False, "encashable": False},
    "PL": {"name": "Paternity Leave",        "annual_quota": 15, "carry_forward": False,  "encashable": False},
    "CO": {"name": "Compensatory Off",       "annual_quota": 0,  "carry_forward": True,  "max_carry": 12, "encashable": False},
    "LWP": {"name": "Leave Without Pay",     "annual_quota": 999,"carry_forward": False, "encashable": False},
}


# ── Data Classes ──────────────────────────────────────────────────────────────

@dataclass
class LeaveApplication:
    app_id: str
    employee_id: str
    leave_type: str
    from_date: date
    to_date: date
    reason: str
    status: str = "PENDING"   # PENDING / APPROVED / REJECTED / CANCELLED
    applied_on: date = field(default_factory=date.today)
    days: int = 0

    def __post_init__(self):
        self.days = (self.to_date - self.from_date).days + 1


@dataclass
class LeaveBalance:
    employee_id: str
    leave_type: str
    opening_balance: float = 0
    annual_credit: float = 0
    comp_off_earned: float = 0
    leaves_taken: float = 0
    leaves_pending: float = 0
    leaves_lapsed: float = 0
    closing_balance: float = 0

    def recalculate(self):
        self.closing_balance = (
            self.opening_balance
            + self.annual_credit
            + self.comp_off_earned
            - self.leaves_taken
            - self.leaves_pending
            - self.leaves_lapsed
        )
        return self


class LeaveTracker:
    """
    Simulates SAP TM leave quota management.
    Maps to PT60 (Time Evaluation) and IT2006 (Absence Quota).
    """

    def __init__(self):
        self.employees: dict[str, dict] = {}
        self.applications: list[LeaveApplication] = []
        self._next_app_id = 1

    def add_employee(self, emp_id: str, name: str, joining_date: date):
        """Register an employee — simulates PA40 hiring action."""
        self.employees[emp_id] = {
            "name": name,
            "joining_date": joining_date,
            "balances": {}
        }
        # Initialize leave balances (simulates PT_QTA10 — Generate Quotas)
        self._initialize_quotas(emp_id, joining_date)

    def _initialize_quotas(self, emp_id: str, joining_date: date):
        """Generate leave quotas for the employee (IT 2006)."""
        today = date.today()
        months_in_year = 12
        months_worked = min(months_in_year, (today - joining_date).days // 30 + 1)
        proration = months_worked / months_in_year

        for code, meta in LEAVE_TYPES.items():
            quota = meta["annual_quota"]
            # Pro-rate for new joiners
            prorated = round(quota * proration, 1) if joining_date.year == today.year else float(quota)

            self.employees[emp_id]["balances"][code] = LeaveBalance(
                employee_id   = emp_id,
                leave_type    = code,
                opening_balance = 0,
                annual_credit   = prorated,
            )
            self.employees[emp_id]["balances"][code].recalculate()

    def apply_leave(
        self,
        emp_id: str,
        leave_type: str,
        from_date: date,
        to_date: date,
        reason: str
    ) -> LeaveApplication:
        """
        Employee applies for leave.
        Simulates ESS leave application → SAP IT 2001 creation (pending).
        """
        if emp_id not in self.employees:
            raise ValueError(f"Employee {emp_id} not found")
        if leave_type not in LEAVE_TYPES:
            raise ValueError(f"Leave type '{leave_type}' not recognized")

        balance = self.employees[emp_id]["balances"].get(leave_type)
        app_id = f"LA{self._next_app_id:04d}"
        self._next_app_id += 1

        app = LeaveApplication(
            app_id=app_id,
            employee_id=emp_id,
            leave_type=leave_type,
            from_date=from_date,
            to_date=to_date,
            reason=reason,
        )

        # Check balance
        if leave_type != "LWP" and balance:
            available = balance.closing_balance
            if app.days > available:
                print(f"  ⚠️  Warning: {app.days} days requested but only {available:.1f} available for {leave_type}. Application will be created but may be rejected.")

        # Mark as pending (deducted from "leaves_pending")
        if balance:
            balance.leaves_pending += app.days
            balance.recalculate()

        self.applications.append(app)
        print(f"  ✅ Leave Application {app_id} submitted | {LEAVE_TYPES[leave_type]['name']} | {from_date} to {to_date} ({app.days} days)")
        return app

    def approve_leave(self, app_id: str) -> bool:
        """
        Manager approves leave. Simulates PTARQ approval action.
        Converts pending → taken (deducts from IT 2006 quota).
        """
        for app in self.applications:
            if app.app_id == app_id and app.status == "PENDING":
                app.status = "APPROVED"
                balance = self.employees[app.employee_id]["balances"].get(app.leave_type)
                if balance:
                    balance.leaves_pending -= app.days
                    balance.leaves_taken   += app.days
                    balance.recalculate()
                print(f"  ✅ Leave {app_id} APPROVED | {app.employee_id} | {app.days} days of {app.leave_type}")
                return True
        print(f"  ❌ Application {app_id} not found or already processed")
        return False

    def reject_leave(self, app_id: str, reason: str = "Not approved") -> bool:
        """Manager rejects — reverses the pending deduction."""
        for app in self.applications:
            if app.app_id == app_id and app.status == "PENDING":
                app.status = "REJECTED"
                balance = self.employees[app.employee_id]["balances"].get(app.leave_type)
                if balance:
                    balance.leaves_pending -= app.days
                    balance.recalculate()
                print(f"  ❌ Leave {app_id} REJECTED | Reason: {reason}")
                return True
        return False

    def credit_comp_off(self, emp_id: str, days: float, reason: str = "Overtime worked"):
        """Credit compensatory off — simulates IT 2007 quota accrual."""
        if emp_id in self.employees:
            balance = self.employees[emp_id]["balances"].get("CO")
            if balance:
                balance.comp_off_earned += days
                balance.recalculate()
                print(f"  ✅ Comp-Off credited: {days} day(s) to {emp_id} | {reason}")

    def print_balance_report(self, emp_id: str):
        """Print leave balance report — simulates PT_BAL00."""
        emp = self.employees.get(emp_id)
        if not emp:
            print(f"Employee {emp_id} not found")
            return

        print(f"\n{'═'*70}")
        print(f"  LEAVE BALANCE REPORT — SAP HCM Time Management")
        print(f"  Employee: {emp['name']} ({emp_id})")
        print(f"  Report Date: {date.today()}")
        print(f"{'═'*70}")
        print(f"  {'Leave Type':<25} {'Annual':>8} {'Taken':>8} {'Pending':>9} {'Balance':>9}")
        print(f"  {'─'*65}")

        for code, meta in LEAVE_TYPES.items():
            bal = emp["balances"].get(code)
            if bal and (bal.annual_credit > 0 or bal.comp_off_earned > 0 or bal.leaves_taken > 0):
                total_credit = bal.annual_credit + bal.comp_off_earned
                print(f"  {meta['name']:<25} {total_credit:>8.1f} {bal.leaves_taken:>8.1f} {bal.leaves_pending:>9.1f} {bal.closing_balance:>9.1f}")

        print(f"  {'─'*65}")
        print(f"  (Balance = Annual Credit - Taken - Pending)\n")

    def print_application_history(self, emp_id: str):
        """Print leave application history — simulates S_AHR_61016049."""
        apps = [a for a in self.applications if a.employee_id == emp_id]
        if not apps:
            print(f"  No applications found for {emp_id}")
            return

        emp_name = self.employees.get(emp_id, {}).get("name", emp_id)
        print(f"\n  Leave Applications — {emp_name} ({emp_id})")
        print(f"  {'─'*65}")
        print(f"  {'App ID':<10} {'Type':<6} {'From':<12} {'To':<12} {'Days':>5} {'Status':<12}")
        print(f"  {'─'*65}")
        for a in apps:
            lt = LEAVE_TYPES.get(a.leave_type, {}).get("name", a.leave_type)[:20]
            print(f"  {a.app_id:<10} {a.leave_type:<6} {str(a.from_date):<12} {str(a.to_date):<12} {a.days:>5} {a.status:<12}")
        print()


# ── Demo ──────────────────────────────────────────────────────────────────────

def run_demo():
    print("\n" + "="*70)
    print("  SAP HCM Leave Balance Tracker — H2R Project Demo")
    print("="*70)

    tracker = LeaveTracker()

    # Add employees (PA40 — Hire)
    tracker.add_employee("E001", "Priya Sharma",  date(2024, 1, 15))
    tracker.add_employee("E002", "Rahul Mehta",   date(2025, 3, 1))

    print("\n  [Step 1] Leave Quotas Generated (PT_QTA10)")

    # Apply leaves (ESS / PA61)
    print("\n  [Step 2] Employees Apply for Leave")
    app1 = tracker.apply_leave("E001", "EL",  date(2025, 2, 10), date(2025, 2, 14), "Annual family trip")
    app2 = tracker.apply_leave("E001", "CL",  date(2025, 3, 5),  date(2025, 3, 6),  "Personal work")
    app3 = tracker.apply_leave("E002", "SL",  date(2025, 3, 10), date(2025, 3, 12), "Medical — fever")
    app4 = tracker.apply_leave("E001", "EL",  date(2025, 6, 2),  date(2025, 6, 13), "Annual leave") # Might exceed

    # Manager approvals (PTARQ / MSS)
    print("\n  [Step 3] Manager Approves / Rejects (PTARQ)")
    tracker.approve_leave(app1.app_id)
    tracker.approve_leave(app2.app_id)
    tracker.reject_leave(app3.app_id, "Team understaffed — please reschedule")
    tracker.approve_leave(app4.app_id)

    # Comp-off credit
    print("\n  [Step 4] Comp-Off Credited (Weekend OT)")
    tracker.credit_comp_off("E001", 2, "Worked weekend 01-02 Feb 2025")
    tracker.credit_comp_off("E002", 1, "Worked Sunday 09 Mar 2025")

    # Balance reports
    print("\n  [Step 5] Leave Balance Reports (PT_BAL00)")
    tracker.print_balance_report("E001")
    tracker.print_balance_report("E002")

    # Application history
    print("  [Step 6] Application History")
    tracker.print_application_history("E001")
    tracker.print_application_history("E002")


if __name__ == "__main__":
    run_demo()
  
