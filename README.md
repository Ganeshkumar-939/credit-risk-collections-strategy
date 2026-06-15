# 🏦 AI-Powered Credit Risk & Collections Strategy

**Tools:** Python | Machine Learning | Power BI | SQL | Excel  
**Domain:** Banking | FinTech | Risk Analytics  
**Level:** Major Portfolio Project — Entry Level Data / Business Analyst  
**Author:** Venkata Ganesh Kumar Nethuluri  
**Email:** ganeshkumarnethuluri@gmail.com  
**GitHub:** https://github.com/Ganeshkumar-939

> 💡 **Inspired by:** TATA GenAI Powered Data Analytics Job Simulation (Forage, Dec 2025)  
> This project is a real-world implementation of the simulation tasks I completed.

---

## 🎯 Project Objective

Build an end-to-end AI-driven system to:
1. **Identify** customers at risk of loan delinquency
2. **Predict** delinquency using Machine Learning
3. **Design** a smart collections strategy based on AI risk tiers
4. **Deliver** a business report with data-backed recommendations

---

## ❓ Business Problem

A financial institution has thousands of active loan accounts. The collections team has limited resources and needs to know:
- **Who** is likely to default in the next 90 days?
- **How risky** is each customer? (High / Medium / Low)
- **Which** customers to prioritize for collections outreach?
- **What** is the estimated revenue at risk?

---

## 📁 Project Structure

```
credit-risk-collections-strategy/
│
├── README.md                                ← You are here
│
├── data/
│   └── credit_data.csv                      ← Dataset (Kaggle)
│
├── notebooks/
│   ├── 01_EDA_risk_profiling.py             ← Exploratory analysis
│   ├── 02_delinquency_prediction.py         ← ML model building
│   └── 03_collections_strategy.py           ← AI collections tiers
│
├── sql/
│   └── credit_risk_queries.sql              ← SQL risk analysis
│
├── reports/
│   └── business_report.md                   ← Final business report
│
├── dashboard/
│   └── risk_dashboard.png                   ← Dashboard screenshot
│
└── images/
    ├── risk_distribution.png
    ├── delinquency_by_age.png
    ├── feature_importance.png
    ├── roc_curve.png
    └── collections_tiers.png
```

---

## 🔬 Project Workflow

```
Raw Data → EDA & Risk Profiling → Feature Engineering
    → ML Model Training → Risk Score Prediction
        → Collections Strategy Tiers → Business Report
```

---

## 🤖 Machine Learning Results

| Model | Accuracy | AUC-ROC | Precision | Recall |
|---|---|---|---|---|
| Logistic Regression | 93.1% | 0.856 | 0.71 | 0.63 |
| Random Forest | 93.8% | 0.868 | 0.74 | 0.68 |
| **Gradient Boosting** | **94.2%** | **0.874** | **0.76** | **0.70** |

**Best Model:** Gradient Boosting Classifier  
**Key Metric Used:** AUC-ROC (best for imbalanced credit data)

---

## 🎯 AI-Driven Collections Strategy Tiers

| Risk Tier | Risk Score | Action | Priority |
|---|---|---|---|
| 🔴 HIGH RISK | > 0.70 | Immediate call + legal notice | 1st |
| 🟡 MEDIUM RISK | 0.40 – 0.70 | SMS + email reminder campaign | 2nd |
| 🟢 LOW RISK | < 0.40 | Automated email only | 3rd |

---

## 📊 Key Findings

| Finding | Detail |
|---|---|
| Overall Delinquency Rate | 6.68% of borrowers |
| Highest Risk Age Group | 18–30 years old |
| Debt Ratio Impact | Debt ratio > 40% → 3x delinquency risk |
| Revenue at Risk | ~$2.1M across high-risk tier |
| Collections Efficiency | AI tier targeting saves 47% of team effort |

---

## 💡 Business Recommendations

1. **High-risk tier (score > 0.70):** Immediate personal outreach within 48 hours
2. **Restructuring offers** for medium-risk customers with good payment history
3. **AI early warning system** — flag customers 60 days before expected default
4. **Debt counseling program** for customers with debt ratio > 50%
5. **Reject or reduce limits** for applicants aged 20–25 with no credit history

---

## 📊 Dashboard Preview

> Risk dashboard showing customer distribution across tiers, delinquency trends, and collections action plan.

![Risk Dashboard](dashboard/risk_dashboard.png)

---

## 📂 Dataset

- **Dataset:** Give Me Some Credit — Loan Delinquency  
- **Source:** [Kaggle](https://www.kaggle.com/c/GiveMeSomeCredit)  
- **Rows:** 150,000 borrowers | **Target:** SeriousDlqin2yrs

---

## 🚀 How to Run

```bash
# 1. Clone repo
git clone https://github.com/Ganeshkumar-939/credit-risk-collections-strategy

# 2. Open Google Colab (free)
# https://colab.research.google.com

# 3. Upload notebooks one by one:
#    01_EDA_risk_profiling.py
#    02_delinquency_prediction.py
#    03_collections_strategy.py

# 4. Upload credit_data.csv when prompted

# 5. Run all cells
```

---

## 📜 Certifications Used in This Project

| Skill | Certificate |
|---|---|
| EDA & Risk Profiling | TATA GenAI Powered Data Analytics (Forage) |
| AI Delinquency Prediction | TATA GenAI Powered Data Analytics (Forage) |
| Business Report Writing | Deloitte Data Analytics Simulation (Forage) |
| SQL Analysis | SQL Analytics & BI on Databricks |
| Dashboard Design | Cisco Data Analytics Essentials |

---

## 🏆 What Makes This Project Stand Out

- ✅ Real financial domain (banks & NBFCs actively hire for this)
- ✅ End-to-end pipeline (raw data → business action)
- ✅ 3 ML models compared with metrics
- ✅ Actionable 3-tier collections strategy
- ✅ Professional business report included
- ✅ Mirrors real TATA/Deloitte job simulation tasks

---

*This project demonstrates my ability to take raw financial data, apply machine learning, and translate results into a business collections strategy — a core skill for Data Analyst and Business Analyst roles in banking and FinTech.*
