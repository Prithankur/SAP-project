# Phase 1 — Workforce Planning & Recruitment

## Overview

Workforce Planning is the strategic foundation of the Hire-to-Retire process. HR managers and business leaders identify staffing needs, define positions, and initiate recruitment requisitions within SAP Organisational Management (OM) and the Recruitment module.

---

## 1.1 Organisational Management (OM) Setup

Before any hiring can occur, the organisational structure must be configured in SAP OM. This includes creating organisational units, jobs, positions, and defining reporting relationships.

### Object Types in SAP OM

| Object Type | Code | Description |
|-------------|------|-------------|
| Organisational Unit | O | Department, division, team |
| Job | C | Generic role descriptor (e.g., "Software Engineer") |
| Position | S | Specific post in the org (e.g., "Senior Dev - Team A") |
| Person | P | Individual employee linked to a position |
| Cost Centre | K | Financial cost allocation unit |

### Step-by-Step: OM Configuration

| Step | Activity | T-Code | Output |
|------|----------|--------|--------|
| 1 | Create Organisational Unit | `PPOCE` / `PP01` | Org Unit object |
| 2 | Define Job (generic role) | `PP01` (Type: C) | Job object |
| 3 | Create Position (specific post) | `PP01` (Type: S) | Position object |
| 4 | Assign Position to Org Unit | `PPOME` | Org chart updated |
| 5 | Define Reporting Relationships | `PPOME` | Hierarchy established |
| 6 | Maintain Vacancy for Position | `PP01` / `PPOME` | Position marked vacant |
| 7 | Assign Cost Centre to Position | `PPOME` — Account Assignment | Cost centre linked |
| 8 | Display Org Chart | `PPOSA` | Org hierarchy visual |

### Key Transaction Codes — OM

```
PPOME   → Maintain Org Structure (primary tool)
PP01    → Maintain Objects (Org Unit, Job, Position)
PPOCE   → Create Organisational Unit
PPOSA   → Display Org Structure
PO13    → Maintain Position
PO10    → Maintain Organisational Unit
S_AHR_61016533 → Org Structure Report
```

---

## 1.2 Manpower Planning

Before raising a recruitment requisition, the following activities are performed:

1. **Headcount Planning** — HR and Finance agree on approved headcount for the financial year
2. **Skills Gap Analysis** — Identify skill requirements not met by the current workforce
3. **Budget Approval** — Finance approves CTC budget for new hires
4. **Role Definition** — JD (Job Description) created and approved by the hiring manager
5. **Requisition Raised** — HR Requisition submitted via `PB10` or manual process

---

## 1.3 Recruitment Process

SAP Recruitment (or E-Recruiting) is used to manage job postings, applicant tracking, and selection.

### Applicant Object Types

| Object | Description |
|--------|-------------|
| Applicant | Person applying for the job |
| Vacancy | Open position requiring a hire |
| Advertisement | Job posting on internal/external board |

### Step-by-Step: Recruitment

| Step | Activity | T-Code | Output |
|------|----------|--------|--------|
| 1 | Raise Manpower Requisition | `PB10` / `PBAW` | Requisition document |
| 2 | Post Job Advertisement | E-Recruiting / Portal | Job published |
| 3 | Receive Applications | `PB20` — Applicant Master | Applicant records |
| 4 | Initial Screening | `PB30` — Applicant Actions | Shortlist |
| 5 | Schedule Interviews | `PBAH` / Calendar | Interview schedule |
| 6 | Conduct Interviews | Manual / Portal | Interview feedback |
| 7 | Reference Check | Manual | Reference verified |
| 8 | Select Candidate | `PB40` — Applicant Transfer | Offer initiated |
| 9 | Generate Offer Letter | HR Letter Tools / SmartForms | Signed offer |
| 10 | Candidate Accepts Offer | Manual — DOJ confirmed | Joining date fixed |

### Key Transaction Codes — Recruitment

```
PB10    → Create Recruitment Requisition
PB20    → Maintain Applicant Master
PB30    → Applicant Actions (screen, reject, invite)
PB40    → Transfer Applicant to Employee
PBAH    → Maintain Applicant (Short)
PBAW    → Recruitment Requisition Overview
S_PH9_46000172 → Applicant Statistics Report
```

---

## 1.4 Applicant Status Flow

```
Application Received
        ↓
    Screening
        ↓
   Shortlisted ──→ Rejected
        ↓
   Interview 1
        ↓
   Interview 2
        ↓
    Selected ──→ Rejected
        ↓
  Offer Extended
        ↓
  Offer Accepted ──→ Offer Declined
        ↓
   Joining Date Confirmed
        ↓
   Transfer to Employee (PA40)
```

---

## 1.5 Position Vacancy Management

- When a position is **vacant**, it appears in recruitment reports and can be advertised
- Once a hire is made using `PA40`, the position is automatically linked to the new employee
- Vacancy flag is cleared in Org Management when position is filled
- The `PPOME` transaction provides a real-time view of filled vs. vacant positions

---

## Checklist — Phase 1 Completion

- [ ] Org Unit created and approved in PPOME
- [ ] Job and Position objects configured
- [ ] Reporting relationships established
- [ ] Cost centre assigned to position
- [ ] Manpower requisition approved
- [ ] Job description signed off by hiring manager
- [ ] Candidate selected and offer accepted
- [ ] Joining date confirmed
- [ ] Ready to initiate PA40 hiring action

---

*Next Phase: [Phase 2 — Hiring & Onboarding](02_hiring_onboarding.md)*
