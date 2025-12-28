import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === CARICAMENTO DATI LOCALI (testati sui tuoi file) ===
co2 = pd.read_csv("annual-co2-emissions-per-country.csv")
pop = pd.read_csv("population.csv")           # colonna: Population (historical)
gdp = pd.read_csv("gdp-per-capita-maddison.csv")  # colonna: GDP per capita

# Rinominiamo le colonne corrette
pop = pop.rename(columns={'Population (historical)': 'Population'})
gdp = gdp.rename(columns={'GDP per capita': 'GDP_per_capita_2011USD'})

# Entità da analizzare (World escluso come richiesto)
entities = ['European Union (27)', 
            'Japan', 'Germany', 'United Kingdom', 'France', 'Italy']

# CO₂
df = co2[co2['Entity'].isin(entities)].copy()
df = df.rename(columns={'Annual CO₂ emissions': 'CO2_t'})

# Merge popolazione e GDP
df = df.merge(pop[['Entity', 'Year', 'Population']], on=['Entity', 'Year'], how='left')
df = df.merge(gdp[['Entity', 'Year', 'GDP_per_capita_2011USD']], on=['Entity', 'Year'], how='left')

# Calcoli
df['GDP_billion_USD'] = df['GDP_per_capita_2011USD'] * df['Population'] / 1e9
df['CO2_Gt'] = df['CO2_t'] / 1e9
df['Carbon_Intensity'] = df['CO2_t'] / (df['GDP_billion_USD'] * 1e9) * 1000  # kg CO₂/$1000

# Filtro 1990–2023 + pulizia
df = df[(df['Year'] >= 1990) & (df['Year'] <= 2023)].dropna(subset=['GDP_billion_USD', 'CO2_Gt']).copy()

# === GRAFICO DECOUPLING + ETICHETTE CON VALORI 2023 ===
plt.figure(figsize=(17, 10))
colors = sns.color_palette("tab10", len(entities))

for i, entity in enumerate(entities):
    sub = df[df['Entity'] == entity].sort_values('Year')
    if len(sub) < 5: 
        print(f"→ {entity}: dati insufficienti")
        continue
    
    plt.plot(sub['GDP_billion_USD'], sub['CO2_Gt'],
             linewidth=4, color=colors[i], marker='o', markersize=6, alpha=0.9)

    # Punto finale con etichetta VALORI 2023
    last = sub.iloc[-1]
    plt.scatter(last['GDP_billion_USD'], last['CO2_Gt'], 
                s=200, color=colors[i], edgecolors='black', zorder=5)

    label_text = (f"{entity}\n"
                  f"{last['CO2_Gt']:.2f} Gt CO₂\n"
                  f"{last['GDP_billion_USD']:,.0f} B$\n"
                  f"{last['Carbon_Intensity']:.0f} kg/$1000")

    plt.annotate(label_text,
                 xy=(last['GDP_billion_USD'], last['CO2_Gt']),
                 xytext=(12, 12), textcoords='offset points',
                 fontsize=11, fontweight='bold', color=colors[i],
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.95, edgecolor=colors[i], linewidth=1.5))

plt.title('Decoupling Economico-Emissivo (1990–2023)\n'
          'Valori 2023: Emissioni, PIL e Intensità Carbonica per paese/blocco',
          fontsize=20, fontweight='bold', pad=30)
plt.xlabel('PIL totale (miliardi USD 2011)', fontsize=14)
plt.ylabel('Emissioni annuali CO₂ (Gt)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# === TABELLA COMPLETA CON TUTTI I VALORI 2023 ===
print("\nDECOUPLING 2023 – VALORI ASSOLUTI E INTENSITÀ")
print("="*100)
results = []
for entity in entities:
    sub = df[df['Entity'] == entity]
    if len(sub) == 0: continue
    last = sub.sort_values('Year').iloc[-1]
    first = sub.sort_values('Year').iloc[0]
    reduction = round((1 - last['Carbon_Intensity']/first['Carbon_Intensity'])*100, 1) if first['Carbon_Intensity'] > 0 else 0
    
    results.append({
        'Paese/Blocco': entity,
        'CO₂ 2023 (Gt)': f"{last['CO2_Gt']:.2f}",
        'PIL 2023 (miliardi $)': f"{last['GDP_billion_USD']:,.0f}",
        'Intensità 2023 (kg CO₂/$1000)': f"{last['Carbon_Intensity']:.0f}",
        'Riduzione intensità 1990→2023': f"{reduction}%",
    })

print(pd.DataFrame(results).to_string(index=False))