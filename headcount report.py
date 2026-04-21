"""
Headcount Report Generator — SAP HCM H2R Project
=================================================
Generates HR headcount analytics from employee master data.
Simulates SAP standard reports: S_AHR_61016380 and custom HR dashboards.

Usage:
    python headcount_report.py
    python headcount_report.py --org-unit "IT Department"
    python headcount_report.py --format json
"""

import argparse
import json
from collections import defaultdict
from datetime import date, datetime
from typing import Optional


# ── Sample Employee Dataset (simulates SAP PA/OM data) ───────────────────────

EMPLOYEES = [
    {"id": "E001", "name": "Priya Sharma",       "dept": "IT Department",    "designation": "Senior Developer",      "grade": "G4", "gender": "F", "doj": "2022-03-15", "status": "Active",    "location": "Mumbai",    "basic": 55000},
    {"id": "E002", "name": "Rahul Mehta",         "dept": "IT Department",    "designation": "Business Analyst",       "grade": "G3", "gender": "M", "doj": "2023-06-01", "status": "Active",    "location": "Pune",      "basic": 40000},
    {"id": "E003", "name": "Ananya Iyer",          "dept": "HR Department",    "designation": "HR Business Partner",    "grade": "G3", "gender": "F", "doj": "2021-11-20", "status": "Active",    "location": "Bengaluru", "basic": 42000},
    {"id": "E004", "name": "Vikram Singh",         "dept": "Finance",          "designation": "Finance Manager",        "grade": "G5", "gender": "M", "doj": "2019-01-10", "status": "Active",    "location": "Mumbai",    "basic": 75000},
    {"id": "E005", "name": "Sneha Reddy",          "dept": "Supply Chain",     "designation": "Operations Lead",        "grade": "G4", "gender": "F", "doj": "2020-08-01", "status": "Active",    "location": "Hyderabad", "basic": 52000},
    {"id": "E006", "name": "Arjun Nair",           "dept": "IT Department",    "designation": "DevOps Engineer",        "grade": "G3", "gender": "M", "doj": "2024-01-15", "status": "Active",    "location": "Bengaluru", "basic": 45000},
    {"id": "E007", "name": "Pooja Verma",          "dept": "HR Department",    "designation": "Payroll Executive",      "grade": "G2", "gender": "F", "doj": "2022-09-05", "status": "Active",    "location": "Mumbai",    "basic": 28000},
    {"id": "E008", "name": "Sanjay Kumar",         "dept": "Finance",          "designation": "Accountant",             "grade": "G2", "gender": "M", "doj": "2023-03-20", "status": "Active",    "location": "Delhi",     "basic": 30000},
    {"id": "E009", "name": "Kavya Krishnan",       "dept": "Marketing",        "designation": "Brand Manager",          "grade": "G4", "gender": "F", "doj": "2021-05-10", "status": "Active",    "location": "Mumbai",    "basic": 58000},
    {"id": "E010", "name": "Deepak Joshi",         "dept": "IT Department",    "designation": "Project Manager",        "grade": "G5", "gender": "M", "doj": "2018-07-01", "status": "Active",    "location": "Pune",      "basic": 80000},
    {"id": "E011", "name": "Meera Pillai",         "dept": "Supply Chain",     "designation": "Supply Planner",         "grade": "G3", "gender": "F", "doj": "2023-10-01", "status": "Active",    "location": "Chennai",   "basic": 35000},
    {"id": "E012", "name": "Rohan Desai",          "dept": "Marketing",        "designation": "Digital Marketing Lead", "grade": "G3", "gender": "M", "doj": "2022-04-18", "status": "Active",    "location": "Mumbai",    "basic": 38000},
    {"id": "E013", "name": "Divya Patel",          "dept": "HR Department",    "designation": "Recruitment Specialist", "grade": "G2", "gender": "F", "doj": "2024-02-01", "status": "Active",    "location": "Ahmedabad", "basic": 26000},
    {"id": "E014", "name": "Aditya Bhatt",         "dept": "Finance",          "designation": "Sr. Financial Analyst",  "grade": "G4", "gender": "M", "doj": "2020-12-01", "status": "Active",    "location": "Mumbai",    "basic": 60000},
    {"id": "E015", "name": "Nisha Thomas",         "dept": "IT Department",    "designation": "QA Engineer",            "grade": "G3", "gender": "F", "doj": "2021-08-15", "status": "Active",    "location": "Kochi",     "basic": 40000},
    {"id": "E016", "name": "Gaurav Mishra",        "dept": "Supply Chain",     "designation": "Logistics Manager",      "grade": "G5", "gender": "M", "doj": "2017-03-20", "status": "Resigned",  "location": "Delhi",     "basic": 70000},
    {"id": "E017", "name": "Sunita Rao",           "dept": "HR Department",    "designation": "HRBP Manager",           "grade": "G5", "gender": "F", "doj": "2016-06-10", "status": "Retired",   "location": "Bengaluru", "basic": 90000},
    {"id": "E018", "name": "Manish Agarwal",       "dept": "Marketing",        "designation": "Marketing Head",         "grade": "G6", "gender": "M", "doj": "2015-01-01", "status": "Active",    "location": "Mumbai",    "basic": 120000},
    {"id": "E019", "name": "Preethi Subramaniam",  "dept": "Finance",          "designation": "CFO",                    "grade": "G7", "gender": "F", "doj": "2014-04-01", "status": "Active",    "location": "Mumbai",    "basic": 200000},
    {"id": "E020", "name": "Kartik Menon",         "dept": "IT Department",    "designation": "CTO",                    "grade": "G7", "gender": "M", "doj": "2013-09-01", "status": "Active",    "location": "Mumbai",    "basic": 250000},
]


# ── Report Functions ──────────────────────────────────────────────────────────

def get_years_of_service(doj_str: str) -> float:
    doj = datetime.strptime(doj_str, "%Y-%m-%d").date()
    return round((date.today() - doj).days / 365.25, 1)


def headcount_by_department(employees: list) -> dict:
    """Headcount grouped by department."""
    result = defaultdict(int)
    for e in employees:
        result[e["dept"]] += 1
    return dict(sorted(result.items(), key=lambda x: -x[1]))


def headcount_by_status(employees: list) -> dict:
    """Headcount grouped by employment status."""
    result = defaultdict(int)
    for e in employees:
        result[e["status"]] += 1
    return dict(result)


def headcount_by_gender(employees: list) -> dict:
    """Headcount grouped by gender."""
    result = defaultdict(int)
    for e in employees:
        result["Male" if e["gender"] == "M" else "Female"] += 1
    return dict(result)


def headcount_by_location(employees: list) -> dict:
    """Headcount grouped by location."""
    result = defaultdict(int)
    for e in employees:
        result[e["location"]] += 1
    return dict(sorted(result.items(), key=lambda x: -x[1]))


def headcount_by_grade(employees: list) -> dict:
    """Headcount grouped by pay grade."""
    result = defaultdict(int)
    for e in employees:
        result[e["grade"]] += 1
    return dict(sorted(result.items()))


def attrition_report(employees: list) -> dict:
    """Compute attrition statistics."""
    total = len(employees)
    leavers = [e for e in employees if e["status"] in ("Resigned", "Retired")]
    active = [e for e in employees if e["status"] == "Active"]
    rate = round(len(leavers) / total * 100, 1) if total else 0
    return {
        "total_employees": total,
        "active": len(active),
        "leavers": len(leavers),
        "attrition_rate_pct": rate,
        "leaver_details": [{"id": e["id"], "name": e["name"], "dept": e["dept"], "status": e["status"]} for e in leavers],
    }


def salary_analytics(employees: list) -> dict:
    """Basic salary analytics."""
    active = [e for e in employees if e["status"] == "Active"]
    salaries = [e["basic"] for e in active]
    if not salaries:
        return {}
    by_dept = defaultdict(list)
    for e in active:
        by_dept[e["dept"]].append(e["basic"])
    return {
        "total_monthly_basic": sum(salaries),
        "avg_basic": round(sum(salaries) / len(salaries)),
        "min_basic": min(salaries),
        "max_basic": max(salaries),
        "by_department": {
            dept: {"avg": round(sum(pays)/len(pays)), "headcount": len(pays), "total": sum(pays)}
            for dept, pays in sorted(by_dept.items())
        },
    }


def tenure_analysis(employees: list) -> dict:
    """Analyse years of service bands."""
    bands = {"0-1 yr": 0, "1-3 yrs": 0, "3-5 yrs": 0, "5-10 yrs": 0, "10+ yrs": 0}
    for e in employees:
        yos = get_years_of_service(e["doj"])
        if yos < 1:       bands["0-1 yr"] += 1
        elif yos < 3:     bands["1-3 yrs"] += 1
        elif yos < 5:     bands["3-5 yrs"] += 1
        elif yos < 10:    bands["5-10 yrs"] += 1
        else:             bands["10+ yrs"] += 1
    return bands


# ── Print Functions ───────────────────────────────────────────────────────────

def bar(val: int, total: int, width: int = 25) -> str:
    filled = int(val / total * width)
    return "█" * filled + "░" * (width - filled)


def print_headcount_report(employees: list, filter_dept: Optional[str] = None):
    if filter_dept:
        employees = [e for e in employees if filter_dept.lower() in e["dept"].lower()]

    total = len(employees)
    active = [e for e in employees if e["status"] == "Active"]

    print("\n" + "="*70)
    print("  SAP HCM — HEADCOUNT ANALYTICS REPORT")
    print(f"  Equivalent to: S_AHR_61016380 | Date: {date.today()}")
    print("="*70)
    print(f"  Total Employees : {total}")
    print(f"  Active          : {len(active)}")
    print(f"  Inactive        : {total - len(active)}")

    # By Department
    print(f"\n  ── Headcount by Department ──────────────────────────────")
    by_dept = headcount_by_department(active)
    for dept, count in by_dept.items():
        pct = round(count / len(active) * 100)
        print(f"  {dept:<30} {count:>3}  {bar(count, len(active))} {pct}%")

    # By Location
    print(f"\n  ── Headcount by Location ───────────────────────────────")
    by_loc = headcount_by_location(active)
    for loc, count in by_loc.items():
        pct = round(count / len(active) * 100)
        print(f"  {loc:<30} {count:>3}  {bar(count, len(active))} {pct}%")

    # By Gender
    print(f"\n  ── Gender Diversity ────────────────────────────────────")
    by_gender = headcount_by_gender(active)
    for g, count in by_gender.items():
        pct = round(count / len(active) * 100)
        print(f"  {g:<30} {count:>3}  {bar(count, len(active))} {pct}%")

    # By Grade
    print(f"\n  ── Headcount by Pay Grade ──────────────────────────────")
    by_grade = headcount_by_grade(active)
    for grade, count in by_grade.items():
        print(f"  {grade:<30} {count:>3}  {bar(count, len(active))}")

    # Tenure
    print(f"\n  ── Tenure Analysis ─────────────────────────────────────")
    tenure = tenure_analysis(active)
    for band, count in tenure.items():
        print(f"  {band:<30} {count:>3}  {bar(count, len(active) or 1)}")

    # Attrition
    print(f"\n  ── Attrition Report ────────────────────────────────────")
    attr = attrition_report(employees)
    print(f"  Attrition Rate  : {attr['attrition_rate_pct']}%")
    for leaver in attr["leaver_details"]:
        print(f"  → {leaver['name']:<30} {leaver['dept']:<20} ({leaver['status']})")

    # Salary
    print(f"\n  ── Salary Analytics (Basic Pay — ₹/month) ──────────────")
    sal = salary_analytics(active)
    print(f"  Total Monthly Basic Payroll : ₹{sal['total_monthly_basic']:>12,.0f}")
    print(f"  Average Basic               : ₹{sal['avg_basic']:>12,.0f}")
    print(f"  Minimum Basic               : ₹{sal['min_basic']:>12,.0f}")
    print(f"  Maximum Basic               : ₹{sal['max_basic']:>12,.0f}")
    print(f"\n  {'Department':<30} {'Count':>6} {'Avg Basic':>12} {'Total':>14}")
    print(f"  {'─'*65}")
    for dept, d in sal["by_department"].items():
        print(f"  {dept:<30} {d['headcount']:>6} {d['avg']:>12,.0f} {d['total']:>14,.0f}")

    print(f"\n{'═'*70}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SAP HCM Headcount Report")
    parser.add_argument("--org-unit", type=str, help="Filter by department name")
    parser.add_argument("--format",   type=str, default="text", choices=["text", "json"])
    args = parser.parse_args()

    if args.format == "json":
        active = [e for e in EMPLOYEES if e["status"] == "Active"]
        output = {
            "report_date": str(date.today()),
            "total": len(EMPLOYEES),
            "active": len(active),
            "by_department": headcount_by_department(active),
            "by_location": headcount_by_location(active),
            "by_gender": headcount_by_gender(active),
            "by_grade": headcount_by_grade(active),
            "tenure": tenure_analysis(active),
            "attrition": attrition_report(EMPLOYEES),
            "salary_analytics": salary_analytics(active),
        }
        print(json.dumps(output, indent=2))
    else:
        print_headcount_report(EMPLOYEES, filter_dept=args.org_unit)


if __name__ == "__main__":
    main()
