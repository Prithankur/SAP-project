# SAP HCM Transaction Code (T-Code) Reference

## Complete T-Code Catalog — H2R Lifecycle

---

## Organisational Management (OM)

| T-Code | Description | Usage |
|--------|-------------|-------|
| `PPOME` | Maintain Org Structure | Create/edit org hierarchy, assign positions |
| `PPOSA` | Display Org Structure | Read-only org chart view |
| `PPOCE` | Create Organisational Unit | Initial org unit creation |
| `PP01` | Maintain Objects | Create/edit OM objects (O, C, S, P, K) |
| `PO10` | Maintain Organisational Unit | Direct org unit maintenance |
| `PO13` | Maintain Position | Direct position maintenance |
| `PO03` | Maintain Job | Direct job maintenance |
| `PPSC` | Display Structure | Alternative org chart display |

---

## Personnel Administration (PA)

| T-Code | Description | Usage |
|--------|-------------|-------|
| `PA40` | Personnel Actions | Hire, transfer, change, leave, retire |
| `PA30` | Maintain HR Master Data | Create/change infotypes |
| `PA20` | Display HR Master Data | Read-only infotype view |
| `PA10` | Personnel File | View all infotypes for employee |
| `PA70` | Fast Entry | Bulk infotype entry (multiple employees) |
| `PA71` | Fast Entry Time | Bulk time infotype entry |
| `PRMD` | Display Employee Data | Manager's view of employee data |

---

## Time Management (TM)

| T-Code | Description | Usage |
|--------|-------------|-------|
| `PA61` | Maintain Time Data | Enter IT2001 (absence), IT2002 (attendance) etc. |
| `PA62` | List Entry — Time | Multiple employee time entry |
| `PA63` | Maintain Time Infotypes | Alternative to PA61 |
| `PT60` | Time Evaluation | Run RPTIME00 time evaluation program |
| `PT66` | Display TIP | Time Identification Pair results |
| `PT_BAL00` | Time Balances | Display quota balances |
| `PT_QTA10` | Generate Absence Quotas | Batch generate leave quotas |
| `PTMW` | Time Manager Workplace | Comprehensive time admin tool |
| `PTARQ` | Process Absence Quotas | Approve/process leave requests |
| `CAT2` | CATS — Enter Time | Cross-application time sheet entry |
| `CAT3` | CATS — Display Time | View entered time sheets |
| `CAT5` | CATS — Approve Time | Manager approves time sheets |
| `PT61` | Shift Planning | Plan shifts for org units |

---

## Payroll (PY)

| T-Code | Description | Usage |
|--------|-------------|-------|
| `PA03` | Payroll Control Record | Set payroll period status |
| `PC00_M40_CALC` | Run Payroll (India) | Execute payroll computation |
| `PC_PAYRESULT` | Display Payroll Results | View payroll cluster data |
| `PC00_M40_CEDT` | Print Payslips | Generate/print payslips |
| `PC00_M40_CDTB` | Bank Transfer File | Create EFT/NEFT bank file |
| `PC00_M40_CIPE` | Post to FI/CO | Post payroll to accounting |
| `PC00_M40_EPF` | PF Statement | Monthly PF report / ECR |
| `PC00_M40_ESI` | ESI Statement | Monthly ESI report |
| `PC00_M40_F24` | Form 24Q | Quarterly TDS return |
| `PC00_M40_F16` | Form 16 | Annual TDS certificate |
| `PC00_M40_GRTY` | Gratuity Report | Calculate/report gratuity |
| `PC00_M40_LWF` | Labour Welfare Fund | LWF monthly report |
| `PC00_M40_PRTX` | Professional Tax | State professional tax report |
| `S_AHR_61015987` | Payroll Journal | Wage type reporter / payroll journal |

---

## Recruitment (REC)

| T-Code | Description | Usage |
|--------|-------------|-------|
| `PB10` | Create Requisition | Raise manpower requisition |
| `PB20` | Maintain Applicant | Create/edit applicant master |
| `PB30` | Applicant Actions | Screen, invite, reject applicants |
| `PB40` | Transfer Applicant | Convert applicant to employee |
| `PBAH` | Short Applicant Maintenance | Quick applicant data entry |
| `PBAW` | Requisition Overview | View open recruitment requisitions |

---

## Performance Management (PM)

| T-Code | Description | Usage |
|--------|-------------|-------|
| `PHAP_CATALOG` | Appraisal Catalogue | Create/maintain appraisal templates |
| `PHAP_CREATE_PA` | Create Appraisal | Initiate appraisal document |
| `PHAP_ADMIN` | Administer Appraisals | Process appraisals (HR admin) |
| `PHAP_SEARCH` | Search Appraisals | Find appraisal documents |
| `PECM_START_PROCESS_BSP` | Start ECM Process | Launch compensation review cycle |

---

## Learning Solution (LSO)

| T-Code | Description | Usage |
|--------|-------------|-------|
| `LSO_PVCT` | Course Catalogue | Maintain course types |
| `LSO_PVGS` | Schedule Events | Create course instances/dates |
| `LSO_PVBN` | Book Participant | Enrol employee in course |
| `LSO_PVAT` | Record Attendance | Mark attendance post-training |
| `LSO_RHXKURS` | Course Catalogue Report | View full training catalogue |
| `OOST` | Business Event Types | Alternative to LSO_PVCT |

---

## Standard HR Reports

| T-Code | Description |
|--------|-------------|
| `S_AHR_61016362` | New Hire Report |
| `S_AHR_61016380` | Headcount Report |
| `S_AHR_61016383` | Joiners and Leavers |
| `S_AHR_61016049` | Attendance / Absence Report |
| `S_AHR_61016353` | Absence Statistics |
| `S_PH9_46000172` | Applicant Statistics |
| `S_PH9_46000166` | Attrition Report |
| `S_AHR_61015987` | Payroll Journal |
| `S_AHR_61016858` | Salary Statement Report |

---

## System / Basis T-Codes

| T-Code | Description | Usage |
|--------|-------------|-------|
| `SU01` | User Maintenance | Create/change/lock SAP user accounts |
| `SU01D` | Display User | View user account details |
| `SUIM` | User Information System | User/role/authorization reporting |
| `PFCG` | Role Maintenance | Create and maintain authorization roles |
| `SM37` | Job Monitoring | Monitor background jobs |
| `SM36` | Schedule Background Job | Schedule payroll / reports as jobs |

---

## Quick Reference Card

```
NEW HIRE:        PA40 → PA30 → PPOME → SU01
PAYROLL:         PA03 → PC00_M40_CALC → PC_PAYRESULT → PC00_M40_CEDT → PC00_M40_CIPE → PA03 (Exit)
LEAVE:           PA61 (IT2001) → PT60 → PT_BAL00
APPRAISAL:       PHAP_CATALOG → PHAP_CREATE_PA → PHAP_ADMIN
SEPARATION:      PA40 (Leaving) → PC00_M40_CALC → PC00_M40_GRTY → SU01 (Lock)
```
