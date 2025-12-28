import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Stile grafico coerente
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# 1. Caricamento di tutti i dataset
co2_source = pd.read_csv("co2-by-source.csv")
co2_fuel = pd.read_csv("co2-emissions-by-fuel-line.csv")
ghg_total = pd.read_csv("total-ghg-emissions.csv")
co2_per_capita = pd.read_csv("co2-emissions-per-capita.csv")
co2_by_region = pd.read_csv("annual-co-emissions-by-region.csv")
co2_by_country = pd.read_csv("annual-co2-emissions-per-country.csv")
temperature = pd.read_csv("temperature-anomaly.csv")

# Lista per iterare
datasets = {
    "CO₂ per fonte/settore": co2_source,
    "CO₂ per combustibile": co2_fuel,
    "GHG totali (incl. LULUCF)": ghg_total,
    "CO₂ per capita": co2_per_capita,
    "CO₂ per regione": co2_by_region,
    "CO₂ per paese": co2_by_country,
    "Anomalia termica globale": temperature
}

# 2. Funzione per estrarre e preparare serie globale (quando esiste)
def get_global(df, value_col):
    if 'Entity' in df.columns:
        global_df = df[df['Entity'].isin(['World', 'OWID_WRL'])].copy()
        if global_df.empty:
            # fallback: somma tutti i paesi per anno
            global_df = df.groupby('Year')[value_col].sum().reset_index()
            global_df['Entity'] = 'World (sum)'
        return global_df
    return df

# 3. Analisi e un grafico per dataset
fig, axes = plt.subplots(4, 2, figsize=(16, 20))
axes = axes.flatten()
i = 0

for name, df in datasets.items():
    print(f"\n{'='*60}")
    print(f"{name.upper()}")
    print(f"{'='*60}")
    
    # Statistiche di base
    numeric_cols = df.select_dtypes(include='number').columns
    print(df[numeric_cols].describe())
    
    # Preparazione serie da plottare
    if name == "Anomalia termica globale":
        world_temp = temperature[temperature['Entity'] == 'World'].copy()
        col_to_plot = 'Global average temperature anomaly relative to 1861-1890'
        plot_df = world_temp[['Year', col_to_plot]].dropna()
        title = "Anomalia termica globale (°C vs 1861-1890)"
        ylabel = "Anomalia (°C)"
        scale = 1  # no scaling for temp
    elif name == "CO₂ per capita":
        # media globale ponderata non possibile senza popolazione → prendi World se c'è, altrimenti Cina come esempio grande emettitore
        if 'World' in df['Entity'].values:
            plot_df = df[df['Entity'] == 'World'][['Year', 'Annual CO₂ emissions (per capita)']].dropna()
        else:
            plot_df = df[df['Entity'] == 'China'][['Year', 'Annual CO₂ emissions (per capita)']].dropna()
        col_to_plot = 'Annual CO₂ emissions (per capita)'
        title = "CO₂ per capita – Cina (t/anno)"
        ylabel = "t CO₂/capita"
        scale = 1  # no scaling for per capita
    else:
        # Tutti gli altri: cerchiamo serie globale
        value_col = [c for c in df.columns if 'emission' in c.lower() or 'anomaly' in c.lower()][0]
        global_data = get_global(df, value_col)
        if 'World' in global_data['Entity'].values:
            plot_df = global_data[global_data['Entity'].isin(['World', 'OWID_WRL', 'World (sum)'])][['Year', value_col]].dropna()
        else:
            # fallback somma globale
            plot_df = global_data.groupby('Year')[value_col].sum().reset_index()
        col_to_plot = value_col
        title = name
        ylabel = "tonnellate CO₂" if "CO₂" in value_col else "tonnellate CO₂e"
        scale = 1e6
    
    # Conversione in milioni per leggibilità (dove ha senso)
    unit = "Mt" if scale == 1e6 else ylabel
    plot_df = plot_df[plot_df['Year'] >= 1950].copy()  # focus post-1950
    
    ax = axes[i]
    ax.plot(plot_df['Year'], plot_df[col_to_plot] / scale, linewidth=2.5, color=sns.color_palette()[i % len(sns.color_palette())])
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Anno')
    ax.set_ylabel(ylabel.replace("tonnellate", unit))
    ax.grid(True, alpha=0.3)
    
    # Annotazione ultimo valore
    last_year = plot_df['Year'].iloc[-1]
    last_val = plot_df[col_to_plot].iloc[-1] / scale
    ax.annotate(f'{last_val:.1f} {unit}',
                xy=(last_year, last_val),
                xytext=(5, 5), textcoords='offset points',
                fontsize=11, fontweight='bold',
                color='darkred')
    
    i += 1

# Rimuovi asse vuoto
fig.delaxes(axes[-1])
plt.tight_layout()
plt.show()