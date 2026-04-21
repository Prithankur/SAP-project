-- ============================================================
-- SAP HCM HR Master Data SQL Queries
-- H2R (Hire-to-Retire) Project Reference
-- ============================================================
-- NOTE: These queries reference the SAP database table structure.
-- In production SAP, data is accessed via SE16/SE16N or ABAP reports.
-- Use these as reference for custom HR reporting or SAP BW/BEx queries.
-- ============================================================

-- ── SAP HCM Key Tables Reference ─────────────────────────────────────────────
-- PA0000  → IT0000 — Actions
-- PA0001  → IT0001 — Organisational Assignment
-- PA0002  → IT0002 — Personal Data
-- PA0006  → IT0006 — Addresses
-- PA0007  → IT0007 — Planned Working Time
-- PA0008  → IT0008 — Basic Pay
-- PA0009  → IT0009 — Bank Details
-- HRP1000 → OM Objects (Org Units, Positions, Jobs)
-- HRP1001 → OM Relationships
-- T77S0   → SAP HR System Parameters
-- ─────────────────────────────────────────────────────────────────────────────


-- ============================================================
-- QUERY 1: Active Employees — Full Master Data View
-- Equivalent to S_AHR_61016380 (Headcount Report)
-- ============================================================
SELECT
    pa0001.pernr           AS employee_id,
    pa0002.nachn           AS last_name,
    pa0002.vorna           AS first_name,
    pa0002.gbdat           AS date_of_birth,
    pa0002.gesch           AS gender,
    pa0001.plans           AS position,
    pa0001.stell           AS job,
    pa0001.orgeh           AS org_unit,
    pa0001.kostl           AS cost_centre,
    pa0001.bukrs           AS company_code,
    pa0001.persk           AS employee_subgroup,
    pa0001.persg           AS employee_group,
    pa0001.btrtl           AS personnel_subarea,
    pa0001.werks           AS personnel_area,
    pa0000.massn           AS last_action_type,
    pa0000.begda           AS hire_date,
    pa0007.schkz           AS work_schedule_rule,
    pa0008.trfgr           AS pay_grade,
    pa0008.bet01           AS basic_pay_amount
FROM pa0001
INNER JOIN pa0002 ON pa0001.pernr = pa0002.pernr
    AND pa0002.begda <= CURRENT_DATE AND pa0002.endda >= CURRENT_DATE
INNER JOIN pa0000 ON pa0001.pernr = pa0000.pernr
    AND pa0000.begda = (
        SELECT MAX(pa0000b.begda) FROM pa0000 pa0000b
        WHERE pa0000b.pernr = pa0000.pernr
        AND pa0000b.begda <= CURRENT_DATE
    )
LEFT JOIN pa0007 ON pa0001.pernr = pa0007.pernr
    AND pa0007.begda <= CURRENT_DATE AND pa0007.endda >= CURRENT_DATE
LEFT JOIN pa0008 ON pa0001.pernr = pa0008.pernr
    AND pa0008.begda <= CURRENT_DATE AND pa0008.endda >= CURRENT_DATE
WHERE
    pa0001.begda <= CURRENT_DATE
    AND pa0001.endda >= CURRENT_DATE
    AND pa0000.massn NOT IN ('Z1', 'Z2')   -- Exclude resigned/retired action types
ORDER BY pa0001.orgeh, pa0001.pernr;


-- ============================================================
-- QUERY 2: New Hires in Last 30 Days
-- Equivalent to S_AHR_61016362
-- ============================================================
SELECT
    pa0000.pernr           AS employee_id,
    pa0002.nachn           AS last_name,
    pa0002.vorna           AS first_name,
    pa0000.begda           AS hire_date,
    pa0001.orgeh           AS org_unit,
    pa0001.plans           AS position,
    pa0001.bukrs           AS company_code
FROM pa0000
INNER JOIN pa0001 ON pa0000.pernr = pa0001.pernr
    AND pa0001.begda <= CURRENT_DATE AND pa0001.endda >= CURRENT_DATE
INNER JOIN pa0002 ON pa0000.pernr = pa0002.pernr
    AND pa0002.begda <= CURRENT_DATE AND pa0002.endda >= CURRENT_DATE
WHERE
    pa0000.massn = '01'                            -- Action type: Hiring
    AND pa0000.begda >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY pa0000.begda DESC;


-- ============================================================
-- QUERY 3: Headcount by Department and Gender
-- ============================================================
SELECT
    o.stext                AS org_unit_name,
    pa0002.gesch           AS gender,
    COUNT(DISTINCT pa0001.pernr) AS headcount
FROM pa0001
INNER JOIN pa0002 ON pa0001.pernr = pa0002.pernr
    AND pa0002.begda <= CURRENT_DATE AND pa0002.endda >= CURRENT_DATE
INNER JOIN hrp1000 o ON pa0001.orgeh = o.objid
    AND o.otype = 'O'
    AND o.begda <= CURRENT_DATE AND o.endda >= CURRENT_DATE
WHERE
    pa0001.begda <= CURRENT_DATE
    AND pa0001.endda >= CURRENT_DATE
GROUP BY o.stext, pa0002.gesch
ORDER BY o.stext, pa0002.gesch;


-- ============================================================
-- QUERY 4: Employees Approaching Retirement (Next 12 Months)
-- ============================================================
SELECT
    pa0001.pernr           AS employee_id,
    pa0002.nachn           AS last_name,
    pa0002.vorna           AS first_name,
    pa0002.gbdat           AS date_of_birth,
    -- Superannuation age = 60 years
    (pa0002.gbdat + INTERVAL '60 years')  AS expected_retirement_date,
    pa0001.orgeh           AS org_unit,
    pa0001.plans           AS position,
    pa0001.kostl           AS cost_centre,
    DATEDIFF('year', pa0002.gbdat, CURRENT_DATE) AS current_age
FROM pa0001
INNER JOIN pa0002 ON pa0001.pernr = pa0002.pernr
    AND pa0002.begda <= CURRENT_DATE AND pa0002.endda >= CURRENT_DATE
WHERE
    pa0001.begda <= CURRENT_DATE
    AND pa0001.endda >= CURRENT_DATE
    AND (pa0002.gbdat + INTERVAL '60 years')
        BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '12 months'
ORDER BY pa0002.gbdat;


-- ============================================================
-- QUERY 5: Salary Range by Grade and Department
-- ============================================================
SELECT
    o.stext                AS org_unit_name,
    pa0008.trfgr           AS pay_grade,
    COUNT(pa0008.pernr)    AS headcount,
    MIN(pa0008.bet01)      AS min_basic,
    MAX(pa0008.bet01)      AS max_basic,
    ROUND(AVG(pa0008.bet01), 0) AS avg_basic,
    SUM(pa0008.bet01)      AS total_monthly_basic
FROM pa0008
INNER JOIN pa0001 ON pa0008.pernr = pa0001.pernr
    AND pa0001.begda <= CURRENT_DATE AND pa0001.endda >= CURRENT_DATE
INNER JOIN hrp1000 o ON pa0001.orgeh = o.objid
    AND o.otype = 'O'
    AND o.begda <= CURRENT_DATE AND o.endda >= CURRENT_DATE
WHERE
    pa0008.begda <= CURRENT_DATE
    AND pa0008.endda >= CURRENT_DATE
GROUP BY o.stext, pa0008.trfgr
ORDER BY o.stext, pa0008.trfgr;


-- ============================================================
-- QUERY 6: Leavers / Resigned Employees — Last 6 Months
-- Equivalent to Attrition Report
-- ============================================================
SELECT
    pa0000.pernr           AS employee_id,
    pa0002.nachn           AS last_name,
    pa0002.vorna           AS first_name,
    pa0000.begda           AS leaving_date,
    pa0000.massn           AS action_type,
    pa0000.massg           AS action_reason,
    pa0001.orgeh           AS last_org_unit,
    pa0001.plans           AS last_position,
    pa0001.bukrs           AS company_code,
    -- Tenure at leaving
    DATEDIFF('year',
        (SELECT MIN(pa0000b.begda) FROM pa0000 pa0000b
         WHERE pa0000b.pernr = pa0000.pernr AND pa0000b.massn = '01'),
        pa0000.begda
    ) AS tenure_years
FROM pa0000
INNER JOIN pa0001 ON pa0000.pernr = pa0001.pernr
    AND pa0001.begda = (
        SELECT MAX(pa0001b.begda) FROM pa0001 pa0001b
        WHERE pa0001b.pernr = pa0001.pernr
    )
INNER JOIN pa0002 ON pa0000.pernr = pa0002.pernr
    AND pa0002.begda = (
        SELECT MAX(pa0002b.begda) FROM pa0002 pa0002b
        WHERE pa0002b.pernr = pa0002.pernr
    )
WHERE
    pa0000.massn IN ('Z1', 'Z2', 'Z3', 'U1')     -- Leaving action types
    AND pa0000.begda >= CURRENT_DATE - INTERVAL '6 months'
ORDER BY pa0000.begda DESC;


-- ============================================================
-- QUERY 7: Employees Without Bank Details (IT0009 Missing)
-- Pre-payroll validation query
-- ============================================================
SELECT
    pa0001.pernr           AS employee_id,
    pa0002.nachn           AS last_name,
    pa0002.vorna           AS first_name,
    pa0001.orgeh           AS org_unit,
    pa0001.werks           AS personnel_area,
    pa0001.btrtl           AS personnel_subarea
FROM pa0001
INNER JOIN pa0002 ON pa0001.pernr = pa0002.pernr
    AND pa0002.begda <= CURRENT_DATE AND pa0002.endda >= CURRENT_DATE
WHERE
    pa0001.begda <= CURRENT_DATE
    AND pa0001.endda >= CURRENT_DATE
    AND pa0001.pernr NOT IN (
        SELECT DISTINCT pernr FROM pa0009
        WHERE begda <= CURRENT_DATE AND endda >= CURRENT_DATE
        AND zlsch = 'T'                             -- T = Bank Transfer
    )
ORDER BY pa0001.orgeh, pa0001.pernr;


-- ============================================================
-- QUERY 8: Org Structure with Position Vacancies
-- ============================================================
SELECT
    o.stext                AS org_unit_name,
    o.objid                AS org_unit_id,
    p.stext                AS position_name,
    p.objid                AS position_id,
    CASE WHEN pa.pernr IS NOT NULL THEN 'FILLED' ELSE 'VACANT' END AS status,
    pa.pernr               AS employee_id,
    pa2.nachn              AS holder_last_name,
    pa2.vorna              AS holder_first_name
FROM hrp1000 o
INNER JOIN hrp1001 rel ON o.objid = rel.sobid
    AND rel.otype = 'O' AND rel.rsign = 'A' AND rel.relat = '003'  -- O has positions S
    AND rel.begda <= CURRENT_DATE AND rel.endda >= CURRENT_DATE
INNER JOIN hrp1000 p ON rel.objid = p.objid AND p.otype = 'S'
    AND p.begda <= CURRENT_DATE AND p.endda >= CURRENT_DATE
LEFT JOIN pa0001 pa ON p.objid = pa.plans
    AND pa.begda <= CURRENT_DATE AND pa.endda >= CURRENT_DATE
LEFT JOIN pa0002 pa2 ON pa.pernr = pa2.pernr
    AND pa2.begda <= CURRENT_DATE AND pa2.endda >= CURRENT_DATE
WHERE
    o.otype = 'O'
    AND o.begda <= CURRENT_DATE AND o.endda >= CURRENT_DATE
ORDER BY o.stext, status DESC, p.stext;
