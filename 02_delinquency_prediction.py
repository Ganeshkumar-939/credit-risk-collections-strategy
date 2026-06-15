# ============================================================
# NOTEBOOK 2: DELINQUENCY PREDICTION WITH AI
# Project: AI-Powered Credit Risk & Collections Strategy
# Author: Venkata Ganesh Kumar Nethuluri
# Email: ganeshkumarnethuluri@gmail.com
# ============================================================
# Run AFTER Notebook 01_EDA_risk_profiling.py
# ============================================================

# ── CELL 1: Imports ─────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, ConfusionMatrixDisplay,
                             roc_auc_score, roc_curve)
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')
print("✅ Imports done!")

# If SMOTE not installed, run:
# !pip install imbalanced-learn -q

# ── CELL 2: Load & Prepare Data ─────────────────────────────
from google.colab import files
uploaded = files.upload()   # upload credit_data.csv

df = pd.read_csv('cs-training.csv')
df.drop(columns=['Unnamed: 0'], errors='ignore', inplace=True)

# Cleaning (same as notebook 1)
df['MonthlyIncome'].fillna(df['MonthlyIncome'].median(), inplace=True)
df['NumberOfDependents'].fillna(df['NumberOfDependents'].median(), inplace=True)
df['RevolvingUtilizationOfUnsecuredLines'] = df[
    'RevolvingUtilizationOfUnsecuredLines'].clip(upper=1.0)
df['DebtRatio'] = df['DebtRatio'].clip(upper=5.0)
df['age'] = df['age'].clip(lower=18, upper=100)

print("✅ Data loaded and cleaned!")

# ── CELL 3: Feature Engineering ─────────────────────────────
# Create new meaningful features
df['Total_Past_Due'] = (
    df['NumberOfTime30-59DaysPastDueNotWorse'] +
    df['NumberOfTime60-89DaysPastDueNotWorse'] +
    df['NumberOfTimes90DaysLate']
)
df['Income_Per_Dependent'] = df['MonthlyIncome'] / (df['NumberOfDependents'] + 1)
df['Has_Past_Due'] = (df['Total_Past_Due'] > 0).astype(int)
df['High_Utilization'] = (df['RevolvingUtilizationOfUnsecuredLines'] > 0.7).astype(int)

print("✅ Feature engineering complete!")
print(f"New features added: Total_Past_Due, Income_Per_Dependent, Has_Past_Due, High_Utilization")

# ── CELL 4: Define Features & Target ────────────────────────
feature_cols = [
    'RevolvingUtilizationOfUnsecuredLines',
    'age',
    'NumberOfTime30-59DaysPastDueNotWorse',
    'DebtRatio',
    'MonthlyIncome',
    'NumberOfOpenCreditLinesAndLoans',
    'NumberOfTimes90DaysLate',
    'NumberRealEstateLoansOrLines',
    'NumberOfTime60-89DaysPastDueNotWorse',
    'NumberOfDependents',
    'Total_Past_Due',
    'Income_Per_Dependent',
    'Has_Past_Due',
    'High_Utilization'
]

X = df[feature_cols]
y = df['SeriousDlqin2yrs']

print(f"\nFeatures: {X.shape[1]}")
print(f"Target distribution:\n{y.value_counts()}")

# ── CELL 5: Handle Class Imbalance with SMOTE ───────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nBefore SMOTE - Training set:")
print(f"  Majority (0): {(y_train==0).sum():,}")
print(f"  Minority (1): {(y_train==1).sum():,}")

sm = SMOTE(random_state=42)
X_train_res, y_train_res = sm.fit_resample(X_train, y_train)

print(f"\nAfter SMOTE - Balanced Training set:")
print(f"  Class 0: {(y_train_res==0).sum():,}")
print(f"  Class 1: {(y_train_res==1).sum():,}")

# Scale features
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train_res)
X_test_sc  = scaler.transform(X_test)

# ── CELL 6: Train 3 Models ───────────────────────────────────
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest':       RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'Gradient Boosting':   GradientBoostingClassifier(n_estimators=100, random_state=42)
}

results = {}
print("Training models... (this may take 1-2 minutes)\n")

for name, model in models.items():
    if name == 'Logistic Regression':
        model.fit(X_train_sc, y_train_res)
        y_pred = model.predict(X_test_sc)
        y_prob = model.predict_proba(X_test_sc)[:, 1]
    else:
        model.fit(X_train_res, y_train_res)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    results[name] = {'model': model, 'pred': y_pred, 'prob': y_prob,
                     'acc': acc, 'auc': auc}
    print(f"✅ {name}: Accuracy={acc*100:.2f}%  AUC-ROC={auc:.4f}")

# ── CELL 7: Model Comparison Chart ──────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

model_names = list(results.keys())
accuracies  = [results[m]['acc']*100 for m in model_names]
aucs        = [results[m]['auc'] for m in model_names]
colors      = ['#3498db', '#2ecc71', '#e74c3c']

# Accuracy
bars = axes[0].bar(model_names, accuracies, color=colors, edgecolor='black')
axes[0].set_title('Model Accuracy Comparison', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Accuracy (%)')
axes[0].set_ylim(85, 100)
for bar, val in zip(bars, accuracies):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 f'{val:.2f}%', ha='center', fontsize=11, fontweight='bold')

# AUC-ROC
bars2 = axes[1].bar(model_names, aucs, color=colors, edgecolor='black')
axes[1].set_title('AUC-ROC Score Comparison', fontsize=13, fontweight='bold')
axes[1].set_ylabel('AUC-ROC Score')
axes[1].set_ylim(0.7, 1.0)
for bar, val in zip(bars2, aucs):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
                 f'{val:.4f}', ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

# ── CELL 8: ROC Curve ───────────────────────────────────────
plt.figure(figsize=(10, 7))
for name, color in zip(results.keys(), colors):
    fpr, tpr, _ = roc_curve(y_test, results[name]['prob'])
    auc = results[name]['auc']
    plt.plot(fpr, tpr, color=color, linewidth=2.5,
             label=f'{name} (AUC = {auc:.4f})')

plt.plot([0, 1], [0, 1], 'k--', linewidth=1.5, label='Random Classifier')
plt.title('ROC Curve — All Models', fontsize=15, fontweight='bold', pad=15)
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.legend(loc='lower right', fontsize=11)
plt.tight_layout()
plt.savefig('roc_curve.png', dpi=150, bbox_inches='tight')
plt.show()

# ── CELL 9: Confusion Matrix (Best Model = Gradient Boosting)
best_model = 'Gradient Boosting'
cm = confusion_matrix(y_test, results[best_model]['pred'])
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                              display_labels=['No Default', 'Default'])

fig, ax = plt.subplots(figsize=(8, 6))
disp.plot(ax=ax, colorbar=False, cmap='Blues')
ax.set_title(f'Confusion Matrix — {best_model}\nAUC-ROC: {results[best_model]["auc"]:.4f}',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.show()

print(f"\n📋 {best_model} Classification Report:")
print(classification_report(y_test, results[best_model]['pred'],
                            target_names=['No Default', 'Default']))

# ── CELL 10: Feature Importance ─────────────────────────────
gb_model   = results['Gradient Boosting']['model']
feat_imp   = pd.Series(gb_model.feature_importances_, index=feature_cols)
feat_imp   = feat_imp.sort_values(ascending=False)

plt.figure(figsize=(10, 7))
colors_feat = ['#e74c3c' if i < 5 else '#3498db' for i in range(len(feat_imp))]
plt.barh(feat_imp.index[::-1], feat_imp.values[::-1],
         color=colors_feat[::-1], edgecolor='black')
plt.title('Feature Importance — Gradient Boosting\n(Red = Top 5 Most Important)',
          fontsize=13, fontweight='bold')
plt.xlabel('Importance Score', fontsize=12)
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
plt.show()

# ── CELL 11: Model Summary ───────────────────────────────────
print("=" * 55)
print("      ML MODEL RESULTS SUMMARY")
print("=" * 55)
for name in results:
    print(f"  {name:<25} Acc={results[name]['acc']*100:.2f}%  AUC={results[name]['auc']:.4f}")
print("=" * 55)
print(f"\n🏆 Best Model: Gradient Boosting (AUC={results['Gradient Boosting']['auc']:.4f})")
print("\n✅ Notebook 2 Complete! Move to Notebook 3.")

# Save predictions for notebook 3
X_test_df = X_test.copy()
X_test_df['risk_score']  = results['Gradient Boosting']['prob']
X_test_df['actual']      = y_test.values
X_test_df['predicted']   = results['Gradient Boosting']['pred']
X_test_df.to_csv('predictions.csv', index=False)
print("💾 Predictions saved to predictions.csv")
