# 🏢 Hire-to-Retire (H2R) — Employee Lifecycle in SAP HR

> A complete end-to-end documentation and reference project for the **Hire-to-Retire** business process implemented on **SAP HCM (Human Capital Management)**.

![SAP HCM](https://img.shields.io/badge/SAP-HCM-blue?style=for-the-badge&logo=sap)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge)
![Phase](https://img.shields.io/badge/Phases-7-orange?style=for-the-badge)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Project Structure](#-project-structure)
- [H2R Lifecycle Phases](#-h2r-lifecycle-phases)
- [SAP Modules Covered](#-sap-modules-covered)
- [Phase-by-Phase Documentation](#-phase-by-phase-documentation)
- [Key SAP Transaction Codes](#-key-sap-transaction-codes)
- [Integration Map](#-integration-map)
- [Scripts & Automation](#-scripts--automation)
- [How to Use This Repository](#-how-to-use-this-repository)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

The **Hire-to-Retire (H2R)** process represents the complete journey of an employee within an organization — from the moment a vacancy is identified through recruitment, onboarding, day-to-day employment, and finally to separation or retirement.

This repository provides:

- ✅ Step-by-step process documentation for each H2R phase
- ✅ SAP HCM transaction code reference tables
- ✅ Infotype mapping for Personnel Administration
- ✅ Payroll processing workflow and statutory compliance guides
- ✅ Python automation scripts for HR data operations
- ✅ SQL queries for HR reporting
- ✅ Process flow diagrams (Mermaid-based)
- ✅ Configuration templates and checklists

---

## 📁 Project Structure

```
hire-to-retire/
│
├── README.md                          # This file
├── LICENSE
│
├── docs/
│   ├── 01_workforce_planning.md       # Phase 1: OM & Recruitment
│   ├── 02_hiring_onboarding.md        # Phase 2: PA, Infotypes, Hiring
│   ├── 03_time_management.md          # Phase 3: TM, Leave, Attendance
│   ├── 04_payroll_processing.md       # Phase 4: Payroll, Statutory
│   ├── 05_ess_mss.md                  # Phase 5: Self-Service Portals
│   ├── 06_talent_management.md        # Phase 6: Performance, LSO
│   ├── 07_separation.md              # Phase 7: Off-boarding, F&F
│   ├── infotype_reference.md          # Complete Infotype catalog
│   ├── tcode_reference.md             # All SAP T-Codes used
│   ├── integration_points.md          # Module integration map
│   └── roles_authorizations.md        # RBAC and structural auth
│
├── diagrams/
│   ├── h2r_overview_flowchart.md      # Main lifecycle flowchart (Mermaid)
│   ├── payroll_cycle.md               # Payroll cycle diagram
│   ├── om_hierarchy.md                # Org Management hierarchy
│   └── integration_diagram.md         # System integration map
│
├── scripts/
│   ├── python/
│   │   ├── employee_data_validator.py # Validate HR master data
│   │   ├── payroll_calculator.py      # Basic payroll computation
│   │   ├── leave_balance_tracker.py   # Leave quota tracker
│   │   └── headcount_report.py        # Headcount analytics
│   └── sql/
│       ├── employee_master_queries.sql # PA/OM data queries
│       ├── payroll_reports.sql         # Payroll result queries
│       ├── time_management_queries.sql # Time data queries
│       └── headcount_analytics.sql     # HR analytics queries
│
├── templates/
│   ├── offer_letter_template.md       # Offer letter template
│   ├── relieving_letter_template.md   # Relieving letter template
│   ├── exit_interview_form.md         # Exit interview checklist
│   ├── onboarding_checklist.md        # New joiner checklist
│   └── payslip_template.md            # Payslip format reference
│
└── config/
    ├── wage_types_reference.json      # SAP wage type catalog
    ├── infotype_fields.json           # Infotype field definitions
    └── statutory_rates.json           # PF, ESI, TDS rates (India)
```

---

## 🔄 H2R Lifecycle Phases

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Phase 1    │───▶│  Phase 2    │───▶│  Phase 3    │───▶│  Phase 4    │
│  Workforce  │    │  Hiring &   │    │    Time     │    │   Payroll   │
│  Planning   │    │ Onboarding  │    │ Management  │    │ Processing  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                  │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐            │
│  Phase 7    │◀───│  Phase 6    │◀───│  Phase 5    │◀───────────┘
│ Separation  │    │   Talent    │    │  ESS / MSS  │
│  / Retire   │    │ Management  │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

| Phase | Name | SAP Module | Key T-Codes |
|-------|------|-----------|-------------|
| 1 | Workforce Planning & Recruitment | OM, REC | PPOME, PP01, PB20 |
| 2 | Hiring & Onboarding | PA | PA40, PA30, PA20 |
| 3 | Time Management | TM | PA61, PT60, CAT2 |
| 4 | Payroll Processing | PY | PA03, PC00_M40_CALC |
| 5 | ESS / MSS | Portal | Fiori / NetWeaver |
| 6 | Talent Management | PM, LSO | PHAP_ADMIN, LSO_PVCT |
| 7 | Separation / Retire | PA | PA40, PC00_M40_GRTY |

---

## 📦 SAP Modules Covered

| Module | Full Name | Function |
|--------|-----------|----------|
| **OM** | Organisational Management | Org structure, positions, jobs |
| **PA** | Personnel Administration | Employee master data, infotypes |
| **TM** | Time Management | Attendance, leave, overtime |
| **PY** | Payroll | Gross/net pay, statutory deductions |
| **ESS** | Employee Self-Service | Employee portal transactions |
| **MSS** | Manager Self-Service | Manager portal transactions |
| **LSO** | Learning Solution | Training & development |
| **ECM** | Enterprise Compensation Mgmt | Salary revisions, bonuses |
| **BN** | Benefits | Medical, insurance enrollment |
| **REC** | Recruitment | Applicant management |

---

## 📖 Phase-by-Phase Documentation

Detailed step-by-step guides for each phase are available in the `docs/` folder:

- 📄 [Phase 1 — Workforce Planning](docs/01_workforce_planning.md)
- 📄 [Phase 2 — Hiring & Onboarding](docs/02_hiring_onboarding.md)
- 📄 [Phase 3 — Time Management](docs/03_time_management.md)
- 📄 [Phase 4 — Payroll Processing](docs/04_payroll_processing.md)
- 📄 [Phase 5 — ESS / MSS](docs/05_ess_mss.md)
- 📄 [Phase 6 — Talent Management](docs/06_talent_management.md)
- 📄 [Phase 7 — Separation](docs/07_separation.md)

---

## 💻 Key SAP Transaction Codes

| T-Code | Description | Module |
|--------|-------------|--------|
| `PPOME` | Maintain Org Structure | OM |
| `PP01` | Maintain Objects | OM |
| `PA40` | Personnel Actions (Hire/Transfer/Leave/Retire) | PA |
| `PA30` | Maintain HR Master Data | PA |
| `PA20` | Display HR Master Data | PA |
| `PA03` | Payroll Control Record | PY |
| `PA61` | Maintain Time Data | TM |
| `PT60` | Run Time Evaluation | TM |
| `CAT2` | CATS — Record Working Time | TM |
| `PTARQ` | Process Absence Quotas | TM |
| `PC00_M40_CALC` | Run Payroll (India) | PY |
| `PC_PAYRESULT` | Display Payroll Results | PY |
| `PC00_M40_CEDT` | Print Payslips | PY |
| `PC00_M40_CDTB` | Create Bank Transfer File | PY |
| `PC00_M40_CIPE` | Post Payroll to FI/CO | PY |
| `PHAP_ADMIN` | Appraisal Administration | PM |
| `LSO_PVCT` | Course Catalogue | LSO |
| `LSO_PVGS` | Schedule Training Events | LSO |
| `SU01` | User Maintenance | Basis |
| `PB20` | Maintain Applicant Master | REC |

> 📄 Full reference: [docs/tcode_reference.md](docs/tcode_reference.md)

---

## 🔗 Integration Map

```
         ┌──────────────────────────────────────────────────┐
         │              SAP HCM Core                        │
         │  OM ──▶ PA ──▶ TM ──▶ PY ──▶ ESS/MSS            │
         └──────────────────────┬───────────────────────────┘
                                │
              ┌─────────────────┼──────────────────┐
              ▼                 ▼                  ▼
         SAP FI             SAP CO           SuccessFactors
       (GL Posting)    (Cost Allocation)   (Talent/Cloud)
```

---

## 🛠 Scripts & Automation

### Python Scripts
```bash
# Validate employee master data completeness
python scripts/python/employee_data_validator.py --file employees.csv

# Calculate payroll (demo mode)
python scripts/python/payroll_calculator.py --employee E001 --month 2025-01

# Check leave balances
python scripts/python/leave_balance_tracker.py --department HR

# Generate headcount report
python scripts/python/headcount_report.py --org-unit 50000001
```

### SQL Queries
```sql
-- Run employee master data report
-- See scripts/sql/employee_master_queries.sql

-- Run payroll reconciliation
-- See scripts/sql/payroll_reports.sql
```

---

## 🚀 How to Use This Repository

### For Students / Learners
1. Start with [docs/02_hiring_onboarding.md](docs/02_hiring_onboarding.md) for the core PA infotypes
2. Review the [T-Code Reference](docs/tcode_reference.md) to memorize key transactions
3. Study [docs/04_payroll_processing.md](docs/04_payroll_processing.md) for payroll cycle mastery
4. Use the diagrams in `diagrams/` folder to visualize process flows

### For SAP Consultants / Implementers
1. Use `config/wage_types_reference.json` for wage type configuration reference
2. Use `config/statutory_rates.json` for Indian statutory compliance rates
3. Reference `docs/integration_points.md` for cross-module integration design
4. Use `scripts/sql/` for report queries in custom HR reporting

### For Project Reports / Academics
1. The full PDF project report is available at the root of this repository
2. Each `docs/` file corresponds to a chapter in the project report
3. `diagrams/` folder contains Mermaid-based process flow diagrams (render in GitHub)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/add-new-phase-docs`
3. Commit your changes: `git commit -m "Add: Succession planning documentation"`
4. Push to the branch: `git push origin feature/add-new-phase-docs`
5. Open a Pull Request

### Areas for Contribution
- [ ] Add SuccessFactors integration documentation
- [ ] Add SAP S/4HANA HCM updates
- [ ] Add more country-specific payroll guides (US, UK, Germany)
- [ ] Add test data sets for demo environments
- [ ] Add Fiori app reference for ESS/MSS

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**SAP HCM H2R Project**
- Domain: SAP Human Capital Management
- Scenario: Hire-to-Retire End-to-End
- Version: 1.0.0
- Year: 2025

---

> ⚠️ **Disclaimer:** This project is created for academic and training purposes. All SAP transaction codes, configurations, and processes referenced are based on standard SAP HCM documentation and best practices.
