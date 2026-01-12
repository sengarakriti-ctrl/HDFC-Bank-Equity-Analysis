import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# 1. LOAD DATA
df = pd.read_csv('hdfc_final_data.csv')

# --- CLEANING STEP ---
df.columns = df.columns.str.strip().str.lower()
nii_col = 'net_interest_income'
npa_col = 'gross_npa_pct'
casa_col = 'casa_ratio'
stock_col = 'avg_stock_price'

cols_to_fix = [nii_col, npa_col, casa_col, stock_col]
for col in cols_to_fix:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- CHART 1: FINANCIAL CORRELATION HEATMAP ---
plt.figure(figsize=(10, 8))
corr_data = df[cols_to_fix].dropna()
sns.heatmap(corr_data.corr(), annot=True, cmap='RdYlGn', fmt=".2f")
plt.title('HDFC Bank: Financial Correlation Heatmap')
plt.savefig('1_Correlation_Heatmap.png', bbox_inches='tight')
plt.close()

# --- CHART 2: PROFIT (NII) DISTRIBUTION ---
plt.figure(figsize=(10, 6))
sns.histplot(df[nii_col].dropna(), kde=True, color='blue')
plt.title('HDFC Bank: Profit (NII) Distribution')
plt.xlabel('Net Interest Income')
plt.savefig('2_Profit_Distribution.png', bbox_inches='tight')
plt.close()

# --- CHART 3: ASSET QUALITY VS PROFITABILITY ---
plt.figure(figsize=(10, 6))
sns.scatterplot(x=npa_col, y=nii_col, data=df, s=200, color='red')
plt.title('Asset Quality (NPA %) vs Profitability (NII)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('3_NPA_vs_Profit_Scatter.png', bbox_inches='tight')
plt.close()

# --- CHART 4: BANKING MARKET SHARE ---
plt.figure(figsize=(8, 8))
banks = ['HDFC', 'ICICI', 'SBI', 'Axis', 'Others']
shares = [20, 18, 25, 12, 25]
plt.pie(shares, labels=banks, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis'))
plt.title('Banking Industry Market Share Benchmarking')
plt.savefig('4_Market_Share_Pie.png', bbox_inches='tight')
plt.close()

# --- CHART 5: RANDOM FOREST DRIVERS ---
plt.figure(figsize=(10, 6))
df_model = df[[casa_col, npa_col, stock_col]].dropna()
if not df_model.empty:
    X = df_model[[casa_col, npa_col]]
    y = df_model[stock_col]
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)

    importance_df = pd.DataFrame({
        'Driver': ['CASA Ratio', 'Gross NPA %'],
        'Importance': rf.feature_importances_
    }).sort_values(by='Importance', ascending=True)

    plt.barh(importance_df['Driver'], importance_df['Importance'], color='teal')
    plt.title('Predictive Analysis: Key Stock Price Drivers')
    plt.xlabel('Importance Score')
    plt.savefig('5_Stock_Price_Drivers.png', bbox_inches='tight')
plt.close()
plt.show()

print("Success! All 5 charts have been saved as individual PNG files in your folder.")