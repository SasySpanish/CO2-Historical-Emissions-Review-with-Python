import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === CARICAMENTO DATI ===
co2 = pd.read_csv("annual-co2-emissions-per-country.csv")
pop = pd.read_csv("population.csv")
pop = pop.rename(columns={'Population (historical)': 'Population'})

# Solo paesi singoli (no World, no European Union)
entities = [
    'United States', 'China', 'Russia', 'India', 'Japan',
    'Germany', 'Canada', 'United Kingdom', 'France', 'Australia',
    'South Korea', 'Brazil', 'Indonesia', 'Italy', 'Saudi Arabia',
    'Mexico', 'South Africa', 'Turkey', 'Iran', 'Poland'
]

df = co2[co2['Entity'].isin(entities)].copy()
df = df.rename(columns={'Annual CO₂ emissions': 'CO2_tons'})
df = df.merge(pop[['Entity', 'Year', 'Population']], on=['Entity', 'Year'], how='left')

# === EMISSIONI CUMULATIVE 1850–2023 ===
cumulative = df[df['Year'] <= 2023].groupby('Entity')['CO2_tons'].sum().reset_index()
cumulative['CO2_cumulative_Gt'] = cumulative['CO2_tons'] / 1e9
cumulative = cumulative.sort_values('CO2_cumulative_Gt', ascending=False)

# Popolazione 2023
pop_2023 = df[df['Year'] == 2023][['Entity', 'Population']].dropna()
cumulative = cumulative.merge(pop_2023, on='Entity', how='left')

# Debito climatico
world_cum_tons = co2[co2['Entity'] == 'World']['Annual CO₂ emissions'].sum()
world_pop_2023 = pop[pop['Entity'] == 'World'].sort_values('Year').iloc[-1]['Population']
world_per_capita_cum = world_cum_tons / world_pop_2023

cumulative['Cum_per_capita_tons'] = cumulative['CO2_tons'] / cumulative['Population']
cumulative['Climate_Debt_Gt'] = ((cumulative['Cum_per_capita_tons'] - world_per_capita_cum) * cumulative['Population']) / 1e9

# === GRAFICO FINALE CON COLORI PERSONALIZZATI ===
plt.figure(figsize=(21, 10))

# --- 1. GRAFICO A TORTA con colori belli e distinti ---
top10 = cumulative.head(10).copy()
others_sum = cumulative.iloc[10:]['CO2_cumulative_Gt'].sum()
others = pd.DataFrame([{'Entity': 'Tutti gli altri paesi', 'CO2_cumulative_Gt': others_sum}])
pie_data = pd.concat([top10[['Entity', 'CO2_cumulative_Gt']], others], ignore_index=True)

# COLORI PERSONALIZZATI (professionali, accessibili, belli in stampa)
custom_colors = [
    '#d62728',  # rosso UK/USA
    '#1f77b4',  # blu Cina
    '#ff7f0e',  # arancione Russia
    '#2ca02c',  # verde India
    '#9467bd',  # viola Giappone
    '#8c564b',  # marrone Germania
    '#e377c2',  # rosa Canada
    '#7f7f7f',  # grigio UK
    '#bcbd22',  # giallo-verde Francia
    '#17becf',  # ciano Australia
    '#888888'   # grigio chiaro per "altri"
]

plt.subplot(1, 2, 1)
wedges, texts, autotexts = plt.pie(
    pie_data['CO2_cumulative_Gt'],
    labels=pie_data['Entity'],
    autopct=lambda pct: f'{pct:.1f}%' if pct >= 4 else '',
    startangle=90,
    colors=custom_colors,
    textprops={'fontsize': 12, 'fontweight': 'bold'},
    wedgeprops={'linewidth': 1.5, 'edgecolor': 'white'}
)

# Evidenzia USA e Cina
wedges[0].set_edgecolor('black')
wedges[0].set_linewidth(3)
wedges[1].set_edgecolor('black')
wedges[1].set_linewidth(3)

plt.title('Chi ha emesso di più nella storia della CO₂?\nEmissioni cumulative 1850–2023 (solo paesi)\nTotale mondiale ≈ 2.600 GtCO₂',
          fontsize=17, fontweight='bold', pad=30, color='darkblue')

# --- 2. BARRE DEBITO CLIMATICO (stesso stile) ---
plt.subplot(1, 2, 2)
debt = cumulative[cumulative['Climate_Debt_Gt'] > 5].copy()
debt = debt.sort_values('Climate_Debt_Gt', ascending=False).head(12)

bars = sns.barplot(
    data=debt,
    y='Entity',
    x='Climate_Debt_Gt',
    palette="Reds_r",
    edgecolor='black'
)

plt.title('Debito Climatico Storico\nGtCO₂ oltre la quota equa per capita (1850–2023)',
          fontsize=17, fontweight='bold', pad=30, color='darkred')
plt.xlabel('GtCO₂ di debito climatico', fontsize=13)
plt.ylabel('')

for i, bar in enumerate(bars.patches):
    width = bar.get_width()
    plt.text(width + 6, bar.get_y() + bar.get_height()/2,
             f'{width:.0f} Gt', va='center', fontweight='bold', fontsize=12, color='darkred')

plt.tight_layout()
plt.show()

# === TABELLA TOP 10 ===
print("\nTOP 10 PAESI PER EMISSIONI CUMULATIVE (1850–2023)")
print("="*80)
top10_table = cumulative.head(10)[['Entity', 'CO2_cumulative_Gt']].round(1)
top10_table = top10_table.rename(columns={'Entity': 'Paese', 'CO2_cumulative_Gt': 'GtCO₂'})
print(top10_table.to_string(index=False))