# ============================================================
# NOTEBOOK 1: EDA & RISK PROFILING
# Project: AI-Powered Credit Risk & Collections Strategy
# Author: Venkata Ganesh Kumar Nethuluri
# Email: ganeshkumarnethuluri@gmail.com
# ============================================================
# Dataset: https://www.kaggle.com/c/GiveMeSomeCredit
# Download cs-training.csv and rename to credit_data.csv
# ============================================================

# ── CELL 1: Imports ─────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
print("✅ Imports done!")

# ── CELL 2: Load Data ───────────────────────────────────────
from google.colab import files
uploaded = files.upload()   # upload credit_data.csv

df = pd.read_csv('cs-training.csv')
df.drop(columns=['Unnamed: 0'], errors='ignore', inplace=True)

print(f"Shape: {df.shape}")
print(f"\nColumns:\n{df.columns.tolist()}")
df.head()

# ── CELL 3: Data Overview ───────────────────────────────────
print("=== DATA TYPES & NULL VALUES ===")
overview = pd.DataFrame({
    'dtype': df.dtypes,
    'null_count': df.isnull().sum(),
    'null_%': (df.isnull().sum() / len(df) * 100).round(2)
})
print(overview)

# ── CELL 4: Target Variable Analysis ────────────────────────
target_counts = df['SeriousDlqin2yrs'].value_counts()
target_pct    = df['SeriousDlqin2yrs'].value_counts(normalize=True) * 100

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Pie chart
axes[0].pie(target_counts, labels=['No Default (0)', 'Default (1)'],
            autopct='%1.2f%%', colors=['#2ecc71', '#e74c3c'],
            startangle=90, textprops={'fontsize': 12})
axes[0].set_title('Delinquency Distribution', fontsize=14, fontweight='bold')

# Bar chart
bars = axes[1].bar(['Not Delinquent', 'Delinquent'],
                   target_counts.values,
                   color=['#2ecc71', '#e74c3c'], edgecolor='black')
axes[1].set_title('Delinquency Count', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Number of Borrowers')
for bar, val in zip(bars, target_counts.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                 f'{val:,}', ha='center', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('delinquency_distribution.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"\n⚠️  Delinquency Rate: {target_pct[1]:.2f}%")
print(f"   This is an IMBALANCED dataset — use AUC-ROC, not accuracy!")

# ── CELL 5: Data Cleaning ───────────────────────────────────
# Fill missing values with median (robust to outliers)
df['MonthlyIncome'].fillna(df['MonthlyIncome'].median(), inplace=True)
df['NumberOfDependents'].fillna(df['NumberOfDependents'].median(), inplace=True)

# Cap extreme outliers
df['RevolvingUtilizationOfUnsecuredLines'] = df[
    'RevolvingUtilizationOfUnsecuredLines'].clip(upper=1.0)
df['DebtRatio'] = df['DebtRatio'].clip(upper=5.0)
df['age'] = df['age'].clip(lower=18, upper=100)

print("✅ Data cleaned!")
print(f"Null values remaining: {df.isnull().sum().sum()}")

# ── CELL 6: Age Distribution & Risk ─────────────────────────
df['Age_Group'] = pd.cut(df['age'],
                          bins=[17, 25, 35, 45, 55, 65, 100],
                          labels=['18-25', '26-35', '36-45',
                                  '46-55', '56-65', '65+'])

age_risk = df.groupby('Age_Group')['SeriousDlqin2yrs'].mean() * 100

plt.figure(figsize=(10, 6))
colors = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6']
bars = plt.bar(age_risk.index, age_risk.values, color=colors, edgecolor='black')

plt.title('Delinquency Rate by Age Group', fontsize=15, fontweight='bold', pad=15)
plt.xlabel('Age Group', fontsize=12)
plt.ylabel('Delinquency Rate (%)', fontsize=12)
plt.ylim(0, 14)

for bar, val in zip(bars, age_risk.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'{val:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('delinquency_by_age.png', dpi=150, bbox_inches='tight')
plt.show()

# ── CELL 7: Debt Ratio Risk Profiling ───────────────────────
df['Debt_Tier'] = pd.cut(df['DebtRatio'],
                          bins=[-0.01, 0.2, 0.4, 0.6, 5.0],
                          labels=['Low (<20%)', 'Medium (20-40%)',
                                  'High (40-60%)', 'Very High (>60%)'])

debt_risk = df.groupby('Debt_Tier')['SeriousDlqin2yrs'].mean() * 100

plt.figure(figsize=(10, 6))
colors_debt = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
bars = plt.bar(debt_risk.index, debt_risk.values,
               color=colors_debt, edgecolor='black')

plt.title('Delinquency Rate by Debt Ratio Tier', fontsize=15, fontweight='bold')
plt.xlabel('Debt Ratio Tier', fontsize=12)
plt.ylabel('Delinquency Rate (%)', fontsize=12)
plt.ylim(0, 18)

for bar, val in zip(bars, debt_risk.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'{val:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('delinquency_by_debt.png', dpi=150, bbox_inches='tight')
plt.show()

# ── CELL 8: Past Due Analysis ───────────────────────────────
late_cols = ['NumberOfTime30-59DaysPastDueNotWorse',
             'NumberOfTime60-89DaysPastDueNotWorse',
             'NumberOfTimes90DaysLate']

late_risk = {}
for col in late_cols:
    rate = df[df[col] > 0]['SeriousDlqin2yrs'].mean() * 100
    label = col.replace('NumberOf', '').replace('Time', '').replace('DaysPastDueNotWorse', ' days late')
    late_risk[label] = rate

plt.figure(figsize=(10, 6))
labels = list(late_risk.keys())
values = list(late_risk.values())
colors_late = ['#f1c40f', '#e67e22', '#e74c3c']
bars = plt.bar(labels, values, color=colors_late, edgecolor='black')

plt.title('Delinquency Rate by Past Due History', fontsize=15, fontweight='bold')
plt.ylabel('Delinquency Rate (%)', fontsize=12)
plt.ylim(0, 80)

for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{val:.1f}%', ha='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('past_due_risk.png', dpi=150, bbox_inches='tight')
plt.show()

# ── CELL 9: Correlation Heatmap ─────────────────────────────
plt.figure(figsize=(12, 8))
corr = df.select_dtypes(include='number').corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
            cmap='RdYlGn', center=0,
            linewidths=0.5, annot_kws={'size': 9})
plt.title('Feature Correlation Heatmap', fontsize=15, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()

# ── CELL 10: Risk Profile Summary ───────────────────────────
print("=" * 55)
print("       RISK PROFILING SUMMARY")
print("=" * 55)
print(f"  Total Borrowers         : {len(df):,}")
print(f"  Delinquency Rate        : {df['SeriousDlqin2yrs'].mean()*100:.2f}%")
print(f"  Highest Risk Age Group  : 18-25 years")
print(f"  Avg Monthly Income      : ${df['MonthlyIncome'].mean():,.0f}")
print(f"  High Debt Ratio (>40%)  : {(df['DebtRatio']>0.4).sum():,} customers")
print("=" * 55)
print("\n💾 Save this notebook as: 01_EDA_risk_profiling.ipynb")
print("✅ EDA Complete! Move to Notebook 2.")
