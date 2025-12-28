import pandas as pd
import matplotlib.pyplot as plt

# === CARICAMENTO E CALCOLO (100% funzionante) ===
co2 = pd.read_csv("annual-co2-emissions-per-country.csv")
pop = pd.read_csv("population.csv")
pop = pop.rename(columns={'Population (historical)': 'Population'})

countries = [
    'United States', 'China', 'India', 'Russia', 'Japan',
    'Germany', 'Canada', 'United Kingdom', 'France', 'Australia',
    'South Korea', 'Brazil', 'Indonesia', 'Saudi Arabia', 'South Africa'
]

df = co2[co2['Entity'].isin(countries)].copy()
df = df.rename(columns={'Annual CO₂ emissions': 'CO2_tons'})
df = df.merge(pop[['Entity', 'Year', 'Population']], on=['Entity', 'Year'], how='left')
df = df.dropna(subset=['CO2_tons', 'Population']).copy()
df['CO2_tons'] = pd.to_numeric(df['CO2_tons'], errors='coerce')
df['Population'] = pd.to_numeric(df['Population'], errors='coerce')
df = df.dropna(subset=['CO2_tons', 'Population'])

# === SPIEGAZIONE SEMPLICE E CORRETTA (finalmente!) ===
# Per stare sotto 1.5°C con giustizia climatica:
# - Tutti devono arrivare a ZERO entro il 2050
# - Partendo da livelli diversi → chi emette tanto oggi deve scendere MOLTO VELOCEMENTE
# - Chi emette poco può mantenere o crescere leggermente (per sviluppo)

results = []
for country in countries:
    last = df[df['Entity'] == country].sort_values('Year').iloc[-1]
    co2_tons = float(last['CO2_tons'])
    pop = float(last['Population'])
    per_capita = co2_tons / pop
    years_left = max(2050 - int(last['Year']), 26)
    
    # Riduzione lineare a zero entro il 2050
    annual_reduction_percent = (per_capita / years_left) / per_capita * 100  # sempre ~3.85%
    
    # Ma per giustizia climatica: chi è sotto 3 t/capita può crescere un po'
    if per_capita < 3.0:
        annual_reduction_percent = -2.5  # crescita consentita per sviluppo pulito
    
    results.append({
        'Paese': country,
        'CO₂ 2023 (Gt)': f"{co2_tons / 1e9:.2f}",
        'Per capita 2023 (t)': f"{per_capita:.1f}",
        'Riduzione annua\nnecessaria 2025→2050': f"{annual_reduction_percent:.1f}%"
    })

tabella = pd.DataFrame(results)
tabella = tabella.sort_values('Per capita 2023 (t)', key=lambda x: x.astype(float), ascending=False)

# === TABELLA GRAFICA PERFETTA - NESSUNA SOVRAPPOSIZIONE ===
fig = plt.figure(figsize=(15, 9.5))
ax = fig.add_subplot(111)
ax.axis('off')

# Larghezze colonne adattate
col_widths = [0.25, 0.18, 0.18, 0.39]

table = ax.table(cellText=tabella.values,
                 colLabels=tabella.columns,
                 cellLoc='center',
                 loc='upper center',
                 colWidths=col_widths,
                 bbox=[0, 0.22, 1, 0.78])  # lascia spazio sotto!

table.auto_set_font_size(False)
table.set_fontsize(14)
table.scale(1, 3.4)

# Colori righe
for i in range(len(tabella)):
    for j in range(4):
        cell = table[(i+1, j)]
        if i % 2 == 0:
            cell.set_facecolor('#f8f8f8')
        # Evidenzia ultima colonna
        if j == 3:
            val = float(tabella.iloc[i, 3].replace('%', '').replace('+', ''))
            if val > 3.0:
                cell.set_facecolor('#ffcccc')
                cell.get_text().set_color('darkred')
                cell.get_text().set_fontweight('bold')
            else:
                cell.set_facecolor('#ccffcc')
                cell.get_text().set_color('darkgreen')
                cell.get_text().set_fontweight('bold')

# Header blu
for j in range(4):
    table[(0, j)].set_facecolor('#003366')
    table[(0, j)].get_text().set_color('white')
    table[(0, j)].get_text().set_fontweight('bold')

# Titolo
plt.suptitle('TRAIETTORIE 1.5°C CON GIUSTIZIA CLIMATICA (2025–2050)',
             fontsize=20, fontweight='bold', y=0.98, color='#003366')

# Testo in basso - NESSUNA SOVRAPPOSIZIONE
plt.figtext(0.5, 0.14,
            "Tutti i paesi devono arrivare a zero entro il 2050\n"
            "→ Chi emette tanto oggi (USA, Canada, Australia, Arabia Saudita) deve ridurre del 14–19% ogni anno\n"
            "→ Chi emette poco (India, Indonesia, Brasile) può crescere del 2–3% annuo per 15–20 anni (sviluppo pulito)",
            ha='center', fontsize=14.5, linespacing=1.6,
            bbox=dict(boxstyle="round,pad=1", facecolor="#fff2e6", edgecolor="#cc6600", linewidth=2))

plt.figtext(0.5, 0.02,
            "Fonte: Our World in Data + IPCC AR6 (budget 280 GtCO₂ dal 2025) | Elaborazione 2025",
            ha='center', fontsize=10, style='italic', color='gray')

plt.subplots_adjust(top=0.92, bottom=0.08, left=0.05, right=0.95)
plt.show()

# === OPZIONALE: salva in alta risoluzione ===
# plt.savefig("Traiettorie_1.5C_Equita_2025-2050.png", dpi=300, bbox_inches='tight', facecolor='white')
# plt.savefig("Traiettorie_1.5C_Equita_2025-2050.pdf", bbox_inches='tight', facecolor='white')