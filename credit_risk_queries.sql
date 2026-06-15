-- ============================================================
-- CREDIT RISK ANALYSIS — SQL QUERIES
-- Project: AI-Powered Credit Risk & Collections Strategy
-- Author: Venkata Ganesh Kumar Nethuluri
-- Email: ganeshkumarnethuluri@gmail.com
-- ============================================================
-- Import cs-training.csv as table: credit_risk
-- ============================================================

-- ── QUERY 1: Overall Delinquency Rate ───────────────────────
SELECT
    SeriousDlqin2yrs AS Delinquent,
    COUNT(*) AS total_customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM credit_risk
GROUP BY SeriousDlqin2yrs;

-- ── QUERY 2: Delinquency by Age Group ───────────────────────
SELECT
    CASE
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age BETWEEN 46 AND 55 THEN '46-55'
        WHEN age BETWEEN 56 AND 65 THEN '56-65'
        ELSE '65+'
    END AS age_group,
    COUNT(*) AS total,
    SUM(SeriousDlqin2yrs) AS delinquent,
    ROUND(SUM(SeriousDlqin2yrs) * 100.0 / COUNT(*), 2) AS delinquency_rate_pct
FROM credit_risk
GROUP BY age_group
ORDER BY delinquency_rate_pct DESC;

-- ── QUERY 3: Delinquency by Debt Ratio Tier ─────────────────
SELECT
    CASE
        WHEN DebtRatio < 0.20 THEN 'Low (<20%)'
        WHEN DebtRatio < 0.40 THEN 'Medium (20-40%)'
        WHEN DebtRatio < 0.60 THEN 'High (40-60%)'
        ELSE 'Very High (>60%)'
    END AS debt_tier,
    COUNT(*) AS total_customers,
    SUM(SeriousDlqin2yrs) AS delinquent,
    ROUND(SUM(SeriousDlqin2yrs) * 100.0 / COUNT(*), 2) AS delinquency_rate_pct
FROM credit_risk
GROUP BY debt_tier
ORDER BY delinquency_rate_pct DESC;

-- ── QUERY 4: Customers with Past Due History ─────────────────
SELECT
    CASE
        WHEN (NumberOfTime30_59DaysPastDueNotWorse +
              NumberOfTime60_89DaysPastDueNotWorse +
              NumberOfTimes90DaysLate) = 0 THEN 'No Past Due'
        WHEN (NumberOfTime30_59DaysPastDueNotWorse +
              NumberOfTime60_89DaysPastDueNotWorse +
              NumberOfTimes90DaysLate) BETWEEN 1 AND 2 THEN '1-2 incidents'
        ELSE '3+ incidents'
    END AS past_due_category,
    COUNT(*) AS total_customers,
    ROUND(SUM(SeriousDlqin2yrs) * 100.0 / COUNT(*), 2) AS delinquency_rate_pct
FROM credit_risk
GROUP BY past_due_category
ORDER BY delinquency_rate_pct DESC;

-- ── QUERY 5: High Income vs Low Income Delinquency ──────────
SELECT
    CASE
        WHEN MonthlyIncome < 3000  THEN 'Low Income (<$3K)'
        WHEN MonthlyIncome < 6000  THEN 'Mid Income ($3K-$6K)'
        WHEN MonthlyIncome < 10000 THEN 'High Income ($6K-$10K)'
        ELSE 'Very High (>$10K)'
    END AS income_band,
    COUNT(*) AS total_customers,
    ROUND(SUM(SeriousDlqin2yrs) * 100.0 / COUNT(*), 2) AS delinquency_rate_pct,
    ROUND(AVG(MonthlyIncome), 0) AS avg_monthly_income
FROM credit_risk
WHERE MonthlyIncome IS NOT NULL
GROUP BY income_band
ORDER BY delinquency_rate_pct DESC;

-- ── QUERY 6: High Risk Customers for Collections ────────────
-- Customers who are NOT yet delinquent but show risk signals
SELECT
    age,
    MonthlyIncome,
    DebtRatio,
    RevolvingUtilizationOfUnsecuredLines,
    NumberOfTimes90DaysLate,
    (NumberOfTime30_59DaysPastDueNotWorse +
     NumberOfTime60_89DaysPastDueNotWorse +
     NumberOfTimes90DaysLate) AS total_past_due_incidents
FROM credit_risk
WHERE SeriousDlqin2yrs = 0          -- Not yet defaulted
  AND DebtRatio > 0.40               -- High debt burden
  AND RevolvingUtilizationOfUnsecuredLines > 0.70  -- High utilization
  AND (NumberOfTime30_59DaysPastDueNotWorse +
       NumberOfTime60_89DaysPastDueNotWorse) > 0    -- Has late history
ORDER BY DebtRatio DESC
LIMIT 25;

-- ── QUERY 7: Average Financial Profile by Delinquency ────────
SELECT
    SeriousDlqin2yrs AS Is_Delinquent,
    ROUND(AVG(age), 1)                              AS avg_age,
    ROUND(AVG(MonthlyIncome), 0)                    AS avg_monthly_income,
    ROUND(AVG(DebtRatio), 3)                        AS avg_debt_ratio,
    ROUND(AVG(RevolvingUtilizationOfUnsecuredLines), 3) AS avg_utilization,
    ROUND(AVG(NumberOfOpenCreditLinesAndLoans), 1)  AS avg_open_lines,
    ROUND(AVG(NumberRealEstateLoansOrLines), 1)     AS avg_real_estate_loans
FROM credit_risk
GROUP BY SeriousDlqin2yrs;

-- ── QUERY 8: Utilization Rate Risk Analysis ──────────────────
SELECT
    CASE
        WHEN RevolvingUtilizationOfUnsecuredLines < 0.30 THEN 'Low (<30%)'
        WHEN RevolvingUtilizationOfUnsecuredLines < 0.60 THEN 'Medium (30-60%)'
        WHEN RevolvingUtilizationOfUnsecuredLines < 0.90 THEN 'High (60-90%)'
        ELSE 'Very High (>90%)'
    END AS utilization_band,
    COUNT(*) AS total_customers,
    ROUND(SUM(SeriousDlqin2yrs) * 100.0 / COUNT(*), 2) AS delinquency_rate_pct
FROM credit_risk
GROUP BY utilization_band
ORDER BY delinquency_rate_pct DESC;

-- ── QUERY 9: Collections Priority List ───────────────────────
-- Customers most likely to default (for immediate collections action)
SELECT
    age,
    ROUND(DebtRatio, 2)                                     AS debt_ratio,
    ROUND(RevolvingUtilizationOfUnsecuredLines, 2)          AS credit_utilization,
    NumberOfTimes90DaysLate                                  AS times_90_days_late,
    MonthlyIncome,
    (NumberOfTime30_59DaysPastDueNotWorse +
     NumberOfTime60_89DaysPastDueNotWorse +
     NumberOfTimes90DaysLate)                                AS total_incidents,
    'HIGH PRIORITY'                                          AS collections_action
FROM credit_risk
WHERE SeriousDlqin2yrs = 1
ORDER BY NumberOfTimes90DaysLate DESC,
         DebtRatio DESC
LIMIT 30;

-- ── QUERY 10: Summary Statistics ────────────────────────────
SELECT 'Total Borrowers'      AS metric,
       COUNT(*)               AS value FROM credit_risk
UNION ALL
SELECT 'Total Delinquent',
       SUM(SeriousDlqin2yrs) FROM credit_risk
UNION ALL
SELECT 'Delinquency Rate %',
       ROUND(SUM(SeriousDlqin2yrs) * 100.0 / COUNT(*), 2) FROM credit_risk
UNION ALL
SELECT 'Avg Monthly Income',
       ROUND(AVG(MonthlyIncome), 0) FROM credit_risk WHERE MonthlyIncome IS NOT NULL
UNION ALL
SELECT 'Avg Debt Ratio',
       ROUND(AVG(DebtRatio) * 100, 1) FROM credit_risk;
