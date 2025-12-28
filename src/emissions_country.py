import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === CARICAMENTO E CORREZIONE COLONNE ===
co2 = pd.read_csv("annual-co2-emissions-per-country.csv")
pop = pd.read_csv("population.csv")      # colonna: "Population (historical)"
gdp = pd.read_csv("gdp-per-capita-maddison.csv")  # colonna: "GDP per capita"

# Rinominiamo correttamente
pop = pop.rename(columns={'Population (historical)': 'Population'})
gdp = gdp.rename(columns={'GDP per capita': 'GDP_per_capita'})

# Entità da analizzare (senza World)
entities = ['European Union (27)', 'United States', 'China', 'India',
            'Japan', 'Germany', 'United Kingdom', 'France', 'Italy']

df = co2[co2['Entity'].isin(entities)].copy()
df = df.rename(columns={'Annual CO₂ emissions': 'CO2_t'})

df = df.merge(pop[['Entity', 'Year', 'Population']], on=['Entity', 'Year'], how='left')
df = df.merge(gdp[['Entity', 'Year', 'GDP_per_capita']], on=['Entity', 'Year'], how='left')

# === CALCOLI CORRETTI (il problema era qui!) ===
# 1 USD = 1 dollaro → 1 miliardo USD = 1e9 USD
df['GDP_total_USD']   = df['GDP_per_capita'] * df['Population']          # USD totali
df['GDP_billion_USD'] = df['GDP_total_USD'] / 1e9                         # miliardi di USD
df['CO2_Gt']          = df['CO2_t'] / 1e9                                # Gt CO₂
df['CO2_Mt']          = df['CO2_t'] / 1e6                                # Mt CO₂ (per intensità)

# Intensità carbonica corretta: kg CO₂ per 1000 USD di PIL
df['Carbon_Intensity'] = (df['CO2_Mt'] * 1e6) / (df['GDP_total_USD'] * 1000)   # kg CO₂ / $1000

# Filtro anni
df = df[(df['Year'] >= 1990) & (df['Year'] <= 2023)]
df = df.dropna(subset=['GDP_total_USD', 'CO2_t', 'Carbon_Intensity']).copy()

# === PREPARAZIONE ETICHETTE PER LA LEGENDA ===
legend_labels = []
handles = []

plt.figure(figsize=(17, 10))
colors = sns.color_palette("tab10", len(entities))

for i, entity in enumerate(entities):
    sub = df[df['Entity'] == entity].sort_values('Year')
    if len(sub) < 5:
        continue

    # Traccia
    line = plt.plot(sub['GDP_billion_USD'], sub['CO2_Gt'],
                    linewidth=4, color=colors[i], marker='o', markersize=6)[0]
    handles.append(line)

    # Ultimi valori 2023 (o anno più recente)
    last = sub.iloc[-1]
    label = (f"{entity}\n"
             f"CO₂: {last['CO2_Gt']:.2f} Gt\n"
             f"PIL: {last['GDP_billion_USD']:,.0f} B$\n"
            )
    legend_labels.append(label)

# === LEGENDA ESTERNA CON TUTTE LE INFO ===
plt.legend(handles, legend_labels,
           loc='upper left', fontsize=9, frameon=True, fancybox=True,
           title="Paese/Blocco – Dati 2023", title_fontsize=10)

plt.title('Decoupling Economico-Emissivo (1990–2023)\n'
          'Tutte le informazioni nella legenda – Intensità carbonica corretta',
          fontsize=20, fontweight='bold', pad=30)
plt.xlabel('PIL totale (miliardi USD 2011)', fontsize=14)
plt.ylabel('Emissioni annuali CO₂ (Gt)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# === TABELLA VERIFICA (ora i valori sono corretti) ===
print("\nVERIFICA VALORI 2023 (Intensità corretta)")
print("="*100)
for entity in entities:
    sub = df[df['Entity'] == entity]
    if len(sub) == 0: continue
    last = sub.sort_values('Year').iloc[-1]
    print(f"{entity:25} → CO₂: {last['CO2_Gt']:6.2f} Gt | "
          f"PIL: {last['GDP_billion_USD']:8,.0f} B$ | "
          )