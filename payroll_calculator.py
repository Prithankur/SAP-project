"""
Payroll Calculator — SAP HCM H2R Project
=========================================
Simulates the SAP HCM India payroll computation for demonstration purposes.
Computes gross pay, statutory deductions, TDS, and net pay.

Usage:
    python payroll_calculator.py
    python payroll_calculator.py --basic 50000 --hra 20000 --name "Priya Sharma"
"""

import argparse
from dataclasses import dataclass, field
from typing import Optional


# ── Statutory Rates (India — FY 2024-25) ─────────────────────────────────────

PF_EMPLOYEE_RATE    = 0.12       # 12% of PF wages
PF_EMPLOYER_EPF     = 0.0367     # 3.67% to EPF
PF_EMPLOYER_EPS     = 0.0833     # 8.33% to EPS (Pension)
PF_WAGE_CAP         = 15000      # PF computed on max ₹15,000 if wages > cap
EDLI_RATE           = 0.005      # 0.5% EDLI
PF_ADMIN_CHARGE     = 0.005      # 0.5% admin charge

ESI_EMPLOYEE_RATE   = 0.0075     # 0.75%
ESI_EMPLOYER_RATE   = 0.0325     # 3.25%
ESI_ELIGIBILITY_CAP = 21000      # ESI not applicable if gross > ₹21,000

# Professional Tax (Maharashtra)
PT_SLABS = [
    (7500,  0),
    (10000, 175),
    (float("inf"), 200),
]

# Standard deduction (FY 2024-25)
STANDARD_DEDUCTION = 50000

# Basic income tax slabs (New Regime FY 2024-25)
TAX_SLABS_NEW = [
    (300000,   0.00),
    (600000,   0.05),
    (900000,   0.10),
    (1200000,  0.15),
    (1500000,  0.20),
    (float("inf"), 0.30),
]

REBATE_87A_LIMIT    = 700000     # Rebate u/s 87A if taxable income ≤ ₹7L
REBATE_87A_AMOUNT   = 25000
SURCHARGE_THRESHOLD = 5000000    # 10% surcharge above ₹50L
HEALTH_EDU_CESS     = 0.04       # 4% HEC on tax


# ── Data Classes ─────────────────────────────────────────────────────────────

@dataclass
class EmployeePayInput:
    """Input data for payroll computation."""
    employee_id: str = "E001"
    name: str = "Employee"
    month: str = "2025-01"

    # Earnings (Monthly)
    basic: float = 30000
    hra: float = 15000
    conveyance: float = 1600
    medical_allowance: float = 1250
    special_allowance: float = 5000
    lta: float = 0
    bonus: float = 0

    # Deductions (Monthly override)
    loan_emi: float = 0
    other_deductions: float = 0

    # Tax-saving declarations (Annual)
    sec_80c: float = 150000     # PF, LIC, ELSS, etc.
    sec_80d: float = 25000      # Health insurance
    hra_exemption: float = 0    # HRA tax exemption claimed

    # Status
    pf_applicable: bool = True
    esi_applicable: Optional[bool] = None  # Auto-detect if None
    pt_state: str = "MH"        # Maharashtra by default
    tax_regime: str = "NEW"     # OLD or NEW


@dataclass
class PayslipResult:
    """Computed payslip for one month."""
    employee_id: str = ""
    name: str = ""
    month: str = ""

    # Earnings
    basic: float = 0
    hra: float = 0
    conveyance: float = 0
    medical_allowance: float = 0
    special_allowance: float = 0
    lta: float = 0
    bonus: float = 0
    gross_salary: float = 0

    # Statutory deductions
    pf_employee: float = 0
    esi_employee: float = 0
    professional_tax: float = 0
    income_tax_monthly: float = 0

    # Other deductions
    loan_emi: float = 0
    other_deductions: float = 0
    total_deductions: float = 0

    # Employer contributions (cost to company)
    pf_employer: float = 0
    esi_employer: float = 0
    ctc_monthly: float = 0

    net_pay: float = 0

    # Annual figures
    annual_gross: float = 0
    annual_tax: float = 0


# ── Calculation Functions ─────────────────────────────────────────────────────

def compute_pf(basic: float) -> tuple[float, float]:
    """Returns (employee_pf, employer_pf_total)"""
    pf_wages = min(basic, PF_WAGE_CAP)
    employee_pf = round(pf_wages * PF_EMPLOYEE_RATE, 2)
    employer_pf = round(pf_wages * (PF_EMPLOYER_EPF + PF_EMPLOYER_EPS + EDLI_RATE + PF_ADMIN_CHARGE), 2)
    return employee_pf, employer_pf


def compute_esi(gross: float) -> tuple[float, float]:
    """Returns (employee_esi, employer_esi). Zero if gross > cap."""
    if gross > ESI_ELIGIBILITY_CAP:
        return 0.0, 0.0
    return round(gross * ESI_EMPLOYEE_RATE, 2), round(gross * ESI_EMPLOYER_RATE, 2)


def compute_professional_tax(gross: float, state: str = "MH") -> float:
    """Compute professional tax based on state slabs."""
    if state != "MH":
        # Simplified — only Maharashtra implemented here
        return 200.0 if gross > 15000 else 0.0
    for limit, amount in PT_SLABS:
        if gross <= limit:
            return float(amount)
    return 200.0


def compute_income_tax_annual(annual_taxable: float, regime: str = "NEW") -> float:
    """Compute annual income tax using new or old regime slabs."""
    tax = 0.0
    prev_limit = 0

    for limit, rate in TAX_SLABS_NEW:
        if annual_taxable <= prev_limit:
            break
        taxable_in_slab = min(annual_taxable, limit) - prev_limit
        tax += taxable_in_slab * rate
        prev_limit = limit

    # Rebate u/s 87A
    if annual_taxable <= REBATE_87A_LIMIT:
        tax = max(0, tax - REBATE_87A_AMOUNT)

    # Health & Education Cess
    tax = round(tax * (1 + HEALTH_EDU_CESS), 2)
    return tax


def calculate_payslip(inp: EmployeePayInput) -> PayslipResult:
    """Main payroll computation function."""
    r = PayslipResult(
        employee_id=inp.employee_id,
        name=inp.name,
        month=inp.month,
    )

    # ── Gross Salary ──────────────────────────────────────────────────────
    r.basic             = inp.basic
    r.hra               = inp.hra
    r.conveyance        = inp.conveyance
    r.medical_allowance = inp.medical_allowance
    r.special_allowance = inp.special_allowance
    r.lta               = inp.lta
    r.bonus             = inp.bonus
    r.gross_salary      = sum([r.basic, r.hra, r.conveyance,
                               r.medical_allowance, r.special_allowance,
                               r.lta, r.bonus])

    # ── PF ────────────────────────────────────────────────────────────────
    if inp.pf_applicable:
        r.pf_employee, r.pf_employer = compute_pf(inp.basic)
    else:
        r.pf_employee, r.pf_employer = 0, 0

    # ── ESI ───────────────────────────────────────────────────────────────
    esi_check = inp.esi_applicable if inp.esi_applicable is not None else (r.gross_salary <= ESI_ELIGIBILITY_CAP)
    if esi_check:
        r.esi_employee, r.esi_employer = compute_esi(r.gross_salary)
    else:
        r.esi_employee, r.esi_employer = 0, 0

    # ── Professional Tax ──────────────────────────────────────────────────
    r.professional_tax = compute_professional_tax(r.gross_salary, inp.pt_state)

    # ── Income Tax (TDS) ─────────────────────────────────────────────────
    r.annual_gross = r.gross_salary * 12
    annual_pf_deduction = r.pf_employee * 12  # PF is in 80C
    annual_taxable = max(0, r.annual_gross - STANDARD_DEDUCTION)

    r.annual_tax = compute_income_tax_annual(annual_taxable, inp.tax_regime)
    r.income_tax_monthly = round(r.annual_tax / 12, 2)

    # ── Other Deductions ──────────────────────────────────────────────────
    r.loan_emi        = inp.loan_emi
    r.other_deductions = inp.other_deductions

    # ── Total Deductions ─────────────────────────────────────────────────
    r.total_deductions = sum([
        r.pf_employee, r.esi_employee, r.professional_tax,
        r.income_tax_monthly, r.loan_emi, r.other_deductions
    ])

    # ── Net Pay ───────────────────────────────────────────────────────────
    r.net_pay = round(r.gross_salary - r.total_deductions, 2)

    # ── CTC ───────────────────────────────────────────────────────────────
    r.ctc_monthly = round(r.gross_salary + r.pf_employer + r.esi_employer, 2)

    return r


# ── Display ───────────────────────────────────────────────────────────────────

def print_payslip(r: PayslipResult):
    """Print a formatted payslip to console."""
    sep = "─" * 55

    print(f"\n{'═'*55}")
    print(f"  SALARY SLIP — {r.month}")
    print(f"  {r.name} (ID: {r.employee_id})")
    print(f"{'═'*55}")

    print(f"\n  {'EARNINGS':30s} {'AMOUNT (₹)':>15s}")
    print(f"  {sep}")
    print(f"  {'Basic Pay':30s} {r.basic:>15,.2f}")
    print(f"  {'House Rent Allowance (HRA)':30s} {r.hra:>15,.2f}")
    print(f"  {'Conveyance Allowance':30s} {r.conveyance:>15,.2f}")
    print(f"  {'Medical Allowance':30s} {r.medical_allowance:>15,.2f}")
    print(f"  {'Special Allowance':30s} {r.special_allowance:>15,.2f}")
    if r.lta:
        print(f"  {'LTA':30s} {r.lta:>15,.2f}")
    if r.bonus:
        print(f"  {'Bonus / Variable Pay':30s} {r.bonus:>15,.2f}")
    print(f"  {sep}")
    print(f"  {'GROSS SALARY':30s} {r.gross_salary:>15,.2f}")

    print(f"\n  {'DEDUCTIONS':30s} {'AMOUNT (₹)':>15s}")
    print(f"  {sep}")
    print(f"  {'Provident Fund (Employee)':30s} {r.pf_employee:>15,.2f}")
    if r.esi_employee:
        print(f"  {'ESI (Employee)':30s} {r.esi_employee:>15,.2f}")
    if r.professional_tax:
        print(f"  {'Professional Tax':30s} {r.professional_tax:>15,.2f}")
    if r.income_tax_monthly:
        print(f"  {'Income Tax / TDS':30s} {r.income_tax_monthly:>15,.2f}")
    if r.loan_emi:
        print(f"  {'Loan EMI Recovery':30s} {r.loan_emi:>15,.2f}")
    if r.other_deductions:
        print(f"  {'Other Deductions':30s} {r.other_deductions:>15,.2f}")
    print(f"  {sep}")
    print(f"  {'TOTAL DEDUCTIONS':30s} {r.total_deductions:>15,.2f}")

    print(f"\n  {'═'*53}")
    print(f"  {'NET PAY (Take Home)':30s} {r.net_pay:>15,.2f}")
    print(f"  {'═'*53}")

    print(f"\n  EMPLOYER CONTRIBUTIONS (not in payslip, part of CTC)")
    print(f"  {sep}")
    print(f"  {'PF Employer (EPF + EPS + EDLI)':30s} {r.pf_employer:>15,.2f}")
    if r.esi_employer:
        print(f"  {'ESI Employer':30s} {r.esi_employer:>15,.2f}")
    print(f"  {sep}")
    print(f"  {'MONTHLY CTC':30s} {r.ctc_monthly:>15,.2f}")
    print(f"  {'ANNUAL CTC':30s} {r.ctc_monthly * 12:>15,.2f}")
    print(f"\n  Annual Gross  : ₹{r.annual_gross:,.2f}")
    print(f"  Annual Tax    : ₹{r.annual_tax:,.2f}")
    print(f"\n{'═'*55}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SAP HCM India Payroll Calculator")
    parser.add_argument("--id",       default="E001",              help="Employee ID")
    parser.add_argument("--name",     default="Sample Employee",   help="Employee name")
    parser.add_argument("--month",    default="2025-01",           help="Payroll month (YYYY-MM)")
    parser.add_argument("--basic",    type=float, default=30000,   help="Basic pay")
    parser.add_argument("--hra",      type=float, default=15000,   help="HRA")
    parser.add_argument("--special",  type=float, default=5000,    help="Special allowance")
    parser.add_argument("--convey",   type=float, default=1600,    help="Conveyance allowance")
    parser.add_argument("--medical",  type=float, default=1250,    help="Medical allowance")
    parser.add_argument("--bonus",    type=float, default=0,       help="Bonus / variable pay")
    parser.add_argument("--loan",     type=float, default=0,       help="Loan EMI recovery")
    parser.add_argument("--regime",   default="NEW",               help="Tax regime: NEW or OLD")
    args = parser.parse_args()

    inp = EmployeePayInput(
        employee_id     = args.id,
        name            = args.name,
        month           = args.month,
        basic           = args.basic,
        hra             = args.hra,
        special_allowance = args.special,
        conveyance      = args.convey,
        medical_allowance = args.medical,
        bonus           = args.bonus,
        loan_emi        = args.loan,
        tax_regime      = args.regime.upper(),
    )

    result = calculate_payslip(inp)
    print_payslip(result)

    # Demo — run with 3 sample employees
    if len(sys.argv) == 1:
        demos = [
            EmployeePayInput("E002", "Rahul Mehta",  "2025-01", basic=22000, hra=8800,  special_allowance=3000),
            EmployeePayInput("E003", "Ananya Iyer",  "2025-01", basic=60000, hra=24000, special_allowance=10000, loan_emi=5000),
        ]
        for d in demos:
            print_payslip(calculate_payslip(d))


import sys
if __name__ == "__main__":
    main()
  
