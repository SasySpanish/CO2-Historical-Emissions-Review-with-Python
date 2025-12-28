import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Ricarica i due dataset chiave (se non già in memoria)
co2_country = pd.read_csv("annual-co2-emissions-per-country.csv")
temp = pd.read_csv("temperature-anomaly.csv")

# 1. CO₂ globale annuale (tonnellate → GtCO₂)
co2_global = co2_country.groupby('Year')['Annual CO₂ emissions'].sum().reset_index()
co2_global = co2_global[co2_global['Year'] >= 1850]

# Conversione in GtCO₂
co2_global['GtCO2'] = co2_global['Annual CO₂ emissions'] / 1e9

# 2. Emissioni cumulative
co2_global['Cumulative_GtCO2'] = co2_global['GtCO2'].cumsum()

# 3. Anomalia termica globale (World)
temp_world = temp[temp['Entity'] == 'World'].copy()
temp_world = temp_world[['Year', 'Global average temperature anomaly relative to 1861-1890']].dropna()
temp_world = temp_world.rename(columns={'Global average temperature anomaly relative to 1861-1890': 'Temp_anomaly'})

# 4. Merge su anno comune (dal 1850)
df = pd.merge(co2_global[['Year', 'GtCO2', 'Cumulative_GtCO2']], 
              temp_world, on='Year', how='inner')

# 5. Regressione lineare: ΔT = TCRE × Cumulative CO₂ + intercept
slope, intercept, r_value, p_value, std_err = stats.linregress(df['Cumulative_GtCO2'], df['Temp_anomaly'])

# TCRE in °C per GtCO₂
TCRE = slope
r2 = r_value**2

print(f"TCRE (Transient Climate Response to cumulative Emissions): {TCRE:.6f} °C per GtCO₂")
print(f"Coefficiente di determinazione R²: {r2:.4f}")
print(f"Ultime emissioni cumulative (1850–2024): {df['Cumulative_GtCO2'].iloc[-1]:.0f} GtCO₂")
print(f"Anomalia 2024: {df['Temp_anomaly'].iloc[-1]:.3f} °C")
print(f"Carbon budget rimanente per +0.5°C (1.5°C totali): {(1500 - df['Temp_anomaly'].iloc[-1]*1000) / (TCRE*1000):.0f} GtCO₂")

# 6. Grafico
plt.figure(figsize=(14, 8))
plt.scatter(df['Cumulative_GtCO2'], df['Temp_anomaly'], 
            c=df['Year'], cmap='inferno', s=60, edgecolors='white', linewidth=0.5, alpha=0.9)
plt.colorbar(label='Anno')

# Linea di regressione
x_fit = np.array([df['Cumulative_GtCO2'].min(), df['Cumulative_GtCO2'].max()])
y_fit = intercept + slope * x_fit
plt.plot(x_fit, y_fit, color='red', linewidth=3, 
         label=f'TCRE = {TCRE:.5f} °C/GtCO₂\nR² = {r2:.4f}')

plt.title('Relazione lineare tra Emissioni Cumulative di CO₂ e Riscaldamento Globale\n(1850–2024 | Dati: Global Carbon Project + HadCRUT5)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Emissioni cumulative di CO₂ (GtCO₂ dal 1850)', fontsize=13)
plt.ylabel('Anomalia termica globale (°C vs 1861–1890)', fontsize=13)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

# Annotazioni chiave
plt.annotate(f'2024: {df["Cumulative_GtCO2"].iloc[-1]:.0f} GtCO₂ → +{df["Temp_anomaly"].iloc[-1]:.2f}°C',
             xy=(df['Cumulative_GtCO2'].iloc[-1], df['Temp_anomaly'].iloc[-1]),
             xytext=(20, -30), textcoords='offset points',
             fontsize=12, fontweight='bold', color='darkred',
             arrowprops=dict(arrowstyle='->', color='darkred', lw=2))

plt.tight_layout()
plt.show()