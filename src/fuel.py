import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Caricamento e preparazione (come prima)
df = pd.read_csv("co2-by-source.csv")

fuel_cols = {
    'Coal': 'Annual CO₂ emissions from coal',
    'Oil': 'Annual CO₂ emissions from oil',
    'Gas': 'Annual CO₂ emissions from gas',
    'Cement': 'Annual CO₂ emissions from cement',
    'Flaring': 'Annual CO₂ emissions from flaring',
    'Other industry': 'Annual CO₂ emissions from other industry'
}

# Globale annuale
global_annual = df.groupby('Year')[list(fuel_cols.values())].sum().reset_index()

# Convertiamo in GtCO₂
for fuel, col in fuel_cols.items():
    global_annual[fuel + '_Gt'] = global_annual[col] / 1e9

# Cumulative
cum_cols = [c for c in global_annual.columns if '_Gt' in c]
for col in cum_cols:
    global_annual[col] = global_annual[col.replace('_Gt', '') + '_Gt'].cumsum()

global_annual['Cumulative_Total_Gt'] = global_annual[cum_cols].sum(axis=1)

# Calcolo percentuali cumulative finali
latest = global_annual.iloc[-1]
total_2024 = latest['Cumulative_Total_Gt']

percentuali = {}
for fuel in fuel_cols.keys():
    gt = latest[fuel + '_Gt']
    perc = (gt / total_2024) * 100
    percentuali[fuel] = (gt, perc)

# === GRAFICO CON PERCENTUALI NELLA LEGENDA ===
plt.figure(figsize=(16, 9))

years = global_annual['Year']
fuels = list(fuel_cols.keys())
colors = sns.color_palette("dark", len(fuels))

# Stacked area
plt.stackplot(years,
              [global_annual[f + '_Gt'] for f in fuels],
              labels=[f"{f} – {percentuali[f][1]:.1f}% ({percentuali[f][0]:.0f} Gt)"
                      for f in fuels],
              colors=colors,
              alpha=0.92)

# Linea totale cumulativa
plt.plot(years, global_annual['Cumulative_Total_Gt'],
         color='black', linewidth=3.5, label=f'Totale → {total_2024:.0f} GtCO₂')

plt.title('Emissioni Cumulative di CO₂ per Fonte (1850–2024)\n'
          'Responsabilità storica del riscaldamento globale',
          fontsize=18, fontweight='bold', pad=25)

plt.xlabel('Anno', fontsize=14)
plt.ylabel('Emissioni cumulative (GtCO₂)', fontsize=14)

# Legenda con percentuali e Gt
plt.legend(loc='upper left', fontsize=11.5, frameon=True, fancybox=True, shadow=True,
           title='Fonte → % e GtCO₂ cumulative (1850–2024)', title_fontsize=12)

# Annotazione finale
last_year = years.iloc[-1]
plt.annotate(f'2024: {total_2024:.0f} GtCO₂ totali',
             xy=(last_year, total_2024), xytext=(-90, -35),
             textcoords='offset points', fontsize=14, fontweight='bold', color='darkred',
             arrowprops=dict(arrowstyle='->', color='darkred', lw=2.5),
             bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.8))

plt.grid(True, alpha=0.3)
plt.xlim(1850, 2024)
plt.tight_layout()
plt.show()

# Stampa pulita a console
print("RESPONSABILITÀ CUMULATIVA 1850–2024")
print("-" * 50)
for fuel, (gt, perc) in percentuali.items():
    print(f"{fuel:15}: {gt:6.0f} GtCO₂ → {perc:5.1f}%")
print(f"{'Totale':15}: {total_2024:.0f} GtCO₂ → 100.0%")
