"""
Employee Data Validator — SAP HCM H2R Project
=============================================
Validates employee master data completeness for SAP HCM onboarding.
Simulates the data checks performed before IT infotypes are maintained.

Usage:
    python employee_data_validator.py
    python employee_data_validator.py --file employees.csv
"""

import csv
import json
import re
import sys
import argparse
from datetime import datetime, date
from typing import Optional


# ── Required fields per infotype (simplified model) ──────────────────────────

REQUIRED_FIELDS = {
    "IT0001": ["company_code", "personnel_area", "employee_group", "employee_subgroup", "position"],
    "IT0002": ["first_name", "last_name", "date_of_birth", "gender", "nationality"],
    "IT0006": ["address_line1", "city", "state", "pin_code", "country"],
    "IT0007": ["work_schedule_rule"],
    "IT0008": ["pay_scale_type", "pay_scale_area", "pay_grade", "basic_pay"],
    "IT0009": ["bank_name", "account_number", "ifsc_code", "account_type"],
    "IT0077": ["pan_number"],
    "IT0587": ["uan_number"],
}

VALID_EMPLOYEE_GROUPS = ["1", "2", "3"]  # 1=Active, 2=Retiree, 3=External
VALID_EMPLOYEE_SUBGROUPS = ["01", "02", "03", "04"]  # 01=Monthly, 02=Daily, etc.
VALID_GENDERS = ["M", "F", "O"]
VALID_ACCOUNT_TYPES = ["S", "C"]  # S=Savings, C=Current
VALID_COUNTRIES = ["IN", "US", "GB", "DE", "SG", "AE"]


# ── Validation Functions ──────────────────────────────────────────────────────

def validate_pan(pan: str) -> bool:
    """Validate Indian PAN number format: AAAAA1234A"""
    if not pan:
        return False
    pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
    return bool(re.match(pattern, pan.upper()))


def validate_ifsc(ifsc: str) -> bool:
    """Validate Indian IFSC code format: ABCD0123456"""
    if not ifsc:
        return False
    pattern = r"^[A-Z]{4}0[A-Z0-9]{6}$"
    return bool(re.match(pattern, ifsc.upper()))


def validate_uan(uan: str) -> bool:
    """Validate UAN (Universal Account Number) — 12-digit numeric"""
    if not uan:
        return False
    return uan.isdigit() and len(uan) == 12


def validate_pin(pin: str) -> bool:
    """Validate Indian PIN code — 6-digit numeric"""
    if not pin:
        return False
    return pin.isdigit() and len(pin) == 6


def validate_account_number(acc: str) -> bool:
    """Validate bank account number — 9 to 18 digits"""
    if not acc:
        return False
    return acc.isdigit() and 9 <= len(acc) <= 18


def validate_date(date_str: str, fmt: str = "%d-%m-%Y") -> bool:
    """Validate date format and logical correctness"""
    try:
        d = datetime.strptime(date_str, fmt).date()
        # Ensure DOB is not in future and employee is at least 18
        if fmt == "%d-%m-%Y":
            age = (date.today() - d).days / 365.25
            return 18 <= age <= 65
        return True
    except (ValueError, TypeError):
        return False


def validate_basic_pay(pay_str: str) -> bool:
    """Validate basic pay — must be positive numeric"""
    try:
        pay = float(str(pay_str).replace(",", ""))
        return pay > 0
    except (ValueError, TypeError):
        return False


def validate_employee(emp: dict) -> dict:
    """
    Run all validations on a single employee record.
    Returns a dict with 'errors', 'warnings', and 'score'.
    """
    errors = []
    warnings = []

    # ── IT 0001 — Org Assignment ──────────────────────────────────────────
    if not emp.get("company_code"):
        errors.append("[IT0001] Company Code is missing")
    if not emp.get("personnel_area"):
        errors.append("[IT0001] Personnel Area is missing")
    if emp.get("employee_group") not in VALID_EMPLOYEE_GROUPS:
        errors.append(f"[IT0001] Employee Group '{emp.get('employee_group')}' is invalid. Must be: {VALID_EMPLOYEE_GROUPS}")
    if emp.get("employee_subgroup") not in VALID_EMPLOYEE_SUBGROUPS:
        errors.append(f"[IT0001] Employee Subgroup '{emp.get('employee_subgroup')}' is invalid")
    if not emp.get("position"):
        errors.append("[IT0001] Position is missing — must link to OM position")

    # ── IT 0002 — Personal Data ───────────────────────────────────────────
    if not emp.get("first_name", "").strip():
        errors.append("[IT0002] First Name is missing")
    if not emp.get("last_name", "").strip():
        errors.append("[IT0002] Last Name is missing")
    if emp.get("date_of_birth"):
        if not validate_date(emp["date_of_birth"]):
            errors.append(f"[IT0002] Date of Birth '{emp['date_of_birth']}' is invalid or age is outside 18–65 range")
    else:
        errors.append("[IT0002] Date of Birth is missing")
    if emp.get("gender", "").upper() not in VALID_GENDERS:
        errors.append(f"[IT0002] Gender '{emp.get('gender')}' is invalid. Must be: M, F, or O")

    # ── IT 0006 — Address ─────────────────────────────────────────────────
    if not emp.get("address_line1", "").strip():
        errors.append("[IT0006] Address Line 1 is missing")
    if not emp.get("city", "").strip():
        errors.append("[IT0006] City is missing")
    if emp.get("pin_code"):
        if not validate_pin(str(emp["pin_code"])):
            errors.append(f"[IT0006] PIN Code '{emp['pin_code']}' is invalid — must be 6 digits")
    else:
        warnings.append("[IT0006] PIN Code not provided")

    # ── IT 0008 — Basic Pay ───────────────────────────────────────────────
    if emp.get("basic_pay"):
        if not validate_basic_pay(emp["basic_pay"]):
            errors.append(f"[IT0008] Basic Pay '{emp['basic_pay']}' is invalid — must be positive number")
        elif float(str(emp["basic_pay"]).replace(",", "")) < 15000:
            warnings.append("[IT0008] Basic Pay is below ₹15,000 — verify against statutory minimum wage")
    else:
        errors.append("[IT0008] Basic Pay is missing")

    # ── IT 0009 — Bank Details ────────────────────────────────────────────
    if emp.get("ifsc_code"):
        if not validate_ifsc(str(emp["ifsc_code"])):
            errors.append(f"[IT0009] IFSC Code '{emp['ifsc_code']}' is invalid format (expected: ABCD0123456)")
    else:
        errors.append("[IT0009] IFSC Code is missing")

    if emp.get("account_number"):
        if not validate_account_number(str(emp["account_number"])):
            errors.append(f"[IT0009] Account Number '{emp['account_number']}' appears invalid (9–18 digits expected)")
    else:
        errors.append("[IT0009] Bank Account Number is missing")

    if emp.get("account_type", "").upper() not in VALID_ACCOUNT_TYPES:
        warnings.append(f"[IT0009] Account Type '{emp.get('account_type')}' not specified or invalid. Should be S (Savings) or C (Current)")

    # ── IT 0077 — PAN (India) ─────────────────────────────────────────────
    if emp.get("pan_number"):
        if not validate_pan(str(emp["pan_number"])):
            errors.append(f"[IT0077] PAN Number '{emp['pan_number']}' is invalid format (expected: AAAAA1234A)")
    else:
        errors.append("[IT0077] PAN Number is missing — required for TDS computation")

    # ── IT 0587 — UAN / PF ────────────────────────────────────────────────
    if emp.get("uan_number"):
        if not validate_uan(str(emp["uan_number"])):
            errors.append(f"[IT0587] UAN '{emp['uan_number']}' is invalid — must be 12 digits")
    else:
        warnings.append("[IT0587] UAN not provided — required for PF contribution")

    # ── Calculate score ───────────────────────────────────────────────────
    total_checks = 20
    failed = len(errors)
    score = max(0, round(((total_checks - failed) / total_checks) * 100, 1))
    status = "✅ READY" if not errors else ("⚠️  INCOMPLETE" if len(errors) <= 3 else "❌ BLOCKED")

    return {
        "employee_id": emp.get("employee_id", "UNKNOWN"),
        "name": f"{emp.get('first_name', '')} {emp.get('last_name', '')}".strip() or "Unknown",
        "status": status,
        "score": score,
        "errors": errors,
        "warnings": warnings,
    }


# ── Sample Data ───────────────────────────────────────────────────────────────

SAMPLE_EMPLOYEES = [
    {
        "employee_id": "E001",
        "first_name": "Priya",
        "last_name": "Sharma",
        "date_of_birth": "15-06-1992",
        "gender": "F",
        "nationality": "IN",
        "company_code": "1000",
        "personnel_area": "1100",
        "employee_group": "1",
        "employee_subgroup": "01",
        "position": "50000567",
        "address_line1": "12, MG Road",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pin_code": "400001",
        "country": "IN",
        "work_schedule_rule": "GNST",
        "pay_scale_type": "S1",
        "pay_scale_area": "01",
        "pay_grade": "G3",
        "basic_pay": "45000",
        "bank_name": "HDFC Bank",
        "account_number": "12345678901",
        "ifsc_code": "HDFC0001234",
        "account_type": "S",
        "pan_number": "ABCDE1234F",
        "uan_number": "100123456789",
    },
    {
        "employee_id": "E002",
        "first_name": "Rahul",
        "last_name": "Mehta",
        "date_of_birth": "03-11-1988",
        "gender": "M",
        "nationality": "IN",
        "company_code": "1000",
        "personnel_area": "1100",
        "employee_group": "1",
        "employee_subgroup": "01",
        "position": "",          # Missing position
        "address_line1": "45 Park Street",
        "city": "Pune",
        "state": "Maharashtra",
        "pin_code": "41100X",    # Invalid PIN
        "country": "IN",
        "work_schedule_rule": "GNST",
        "pay_scale_type": "S1",
        "pay_scale_area": "01",
        "pay_grade": "G2",
        "basic_pay": "32000",
        "bank_name": "SBI",
        "account_number": "98765432101",
        "ifsc_code": "SBIN0001234",
        "account_type": "S",
        "pan_number": "XYZAB9876G",  # Invalid PAN
        "uan_number": "",            # Missing UAN
    },
    {
        "employee_id": "E003",
        "first_name": "Ananya",
        "last_name": "Iyer",
        "date_of_birth": "22-03-1995",
        "gender": "F",
        "nationality": "IN",
        "company_code": "",          # Missing company code
        "personnel_area": "",        # Missing
        "employee_group": "9",       # Invalid
        "employee_subgroup": "01",
        "position": "50000891",
        "address_line1": "",         # Missing address
        "city": "Bengaluru",
        "state": "Karnataka",
        "pin_code": "560001",
        "country": "IN",
        "work_schedule_rule": "",
        "pay_scale_type": "S1",
        "pay_scale_area": "01",
        "pay_grade": "G4",
        "basic_pay": "0",            # Invalid pay
        "bank_name": "ICICI",
        "account_number": "123",     # Too short
        "ifsc_code": "ICIC0000567",
        "account_type": "S",
        "pan_number": "PQRST5678H",
        "uan_number": "100987654321",
    },
]


# ── Report Generation ─────────────────────────────────────────────────────────

def print_report(results: list):
    """Print a formatted validation report to console."""
    print("\n" + "=" * 70)
    print("   SAP HCM — EMPLOYEE DATA VALIDATION REPORT")
    print("   H2R (Hire-to-Retire) Onboarding Readiness Check")
    print("=" * 70)
    print(f"   Run Date : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    print(f"   Records  : {len(results)}")
    print("=" * 70)

    ready = sum(1 for r in results if "READY" in r["status"])
    blocked = sum(1 for r in results if "BLOCKED" in r["status"])
    incomplete = len(results) - ready - blocked

    print(f"\n  Summary: ✅ Ready: {ready}  ⚠️  Incomplete: {incomplete}  ❌ Blocked: {blocked}")
    print()

    for r in results:
        print(f"  {'─' * 60}")
        print(f"  Employee ID : {r['employee_id']}")
        print(f"  Name        : {r['name']}")
        print(f"  Status      : {r['status']}")
        print(f"  Data Score  : {r['score']}%")

        if r["errors"]:
            print(f"\n  ❌ Errors ({len(r['errors'])}):")
            for e in r["errors"]:
                print(f"     • {e}")

        if r["warnings"]:
            print(f"\n  ⚠️  Warnings ({len(r['warnings'])}):")
            for w in r["warnings"]:
                print(f"     • {w}")

        if not r["errors"] and not r["warnings"]:
            print("  ✅ All validations passed — ready for SAP PA40 action")

        print()

    print("=" * 70)
    print("  END OF REPORT")
    print("=" * 70 + "\n")


def load_from_csv(filepath: str) -> list:
    """Load employee data from a CSV file."""
    employees = []
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                employees.append(dict(row))
        print(f"  Loaded {len(employees)} employee records from {filepath}")
    except FileNotFoundError:
        print(f"  Error: File '{filepath}' not found. Using sample data instead.")
        employees = SAMPLE_EMPLOYEES
    return employees


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="SAP HCM Employee Data Validator — H2R Project"
    )
    parser.add_argument("--file", type=str, help="Path to CSV file with employee data")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    # Load data
    if args.file:
        employees = load_from_csv(args.file)
    else:
        print("  Using sample employee data (3 records)...")
        employees = SAMPLE_EMPLOYEES

    # Validate
    results = [validate_employee(emp) for emp in employees]

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results)

    # Exit code based on errors
    has_blocked = any("BLOCKED" in r["status"] for r in results)
    sys.exit(1 if has_blocked else 0)


if __name__ == "__main__":
    main()
