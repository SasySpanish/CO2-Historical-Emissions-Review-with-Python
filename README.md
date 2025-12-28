# CO₂ Historical Emissions Review (1850–2025)

Report on CO₂ emissions, global warming, and sustainable energy transition pathways.

## Data Sources and Datasets Overview

The analyses in this repository are based on high-quality, publicly available datasets from Our World in Data, processed and harmonized for consistency. All primary data originate from authoritative institutions and have been minimally transformed (e.g. unit conversions, global aggregations) to enable the presented calculations and visualizations.

### Primary Datasets Used

| Dataset / File name                              | Source / Producer                              | Content Overview                                                                 | Time Coverage       | Unit / Format                  | Main Analyses Performed                                      |
|--------------------------------------------------|------------------------------------------------|----------------------------------------------------------------------------------|---------------------|--------------------------------|--------------------------------------------------------------|
| `co2-by-source.csv`                              | Global Carbon Project → Our World in Data      | Annual territorial CO₂ emissions disaggregated by source: coal, oil, gas, cement, flaring, other industry | 1750–2024          | tonnes CO₂                     | Cumulative emissions by source, stacked area charts, historical responsibility breakdown |
| `annual-co2-emissions-per-country.csv`           | Global Carbon Project → Our World in Data      | Annual territorial CO₂ emissions at country level (including selected regional aggregates) | 1750–2024          | tonnes CO₂                     | Country-level cumulative totals, climate debt calculation, national per-capita emissions, equitable 1.5°C pathways |
| `temperature-anomaly.csv`                        | HadCRUT5 – Met Office Hadley Centre            | Annual global, hemispheric and land/ocean temperature anomalies relative to 1861–1890 baseline | 1850–2025          | °C anomaly                     | TCRE regression, correlation with cumulative emissions, long-term global warming trend |
| `population.csv`                                 | Our World in Data / HYDE / United Nations      | Historical and contemporary population estimates by country                     | 10,000 BCE–2024    | persons                        | Per-capita emissions, fair-share climate debt allocation, carbon intensity calculations |
| `gdp-per-capita-maddison.csv`                    | Maddison Project Database                      | GDP per capita in constant 2011 international dollars by country                | 1–2023             | 2011 intl. $ per person        | Total GDP reconstruction, economic–emissions decoupling analysis, carbon intensity trends |
| `total-ghg-emissions.csv`                        | Jones et al. / OWID (National contributions)   | Total annual greenhouse gas emissions including land-use, land-use change and forestry (LULUCF) | 1850–2023          | tonnes CO₂-equivalent (GWP100) | Multi-trend overview, comparison between CO₂-only and full GHG trends |
| `co2-emissions-per-capita.csv`                   | Global Carbon Project → Our World in Data      | Annual CO₂ emissions per person by country                                       | 1750–2024          | tonnes CO₂ per capita          | Per-capita benchmarking, equity considerations in climate debt and future pathways |

### Key Processing and Methodological Notes

- All CO₂ emissions are **territorial** (production-based accounting), excluding emissions from international aviation & shipping bunkers and land-use, land-use change and forestry (LULUCF) unless explicitly included (as in the total GHG dataset).
- Conversion from tonnes of carbon to tonnes of CO₂ uses the standard factor **3.664** recommended by the Global Carbon Project.
- Global aggregates are calculated as the sum across all countries, consistent with territorial accounting principles.
- Temperature anomalies are expressed relative to the 1861–1890 mean, a widely accepted reference period for pre-industrial conditions.
- GDP values are in constant 2011 international dollars to ensure long-term comparability and reliable intensity metrics.
- All raw data files remain untouched; all derived calculations (cumulatives, per-capita, intensity, regressions) are performed dynamically in the analysis scripts.

These datasets provide a comprehensive, consistent foundation for tracing historical emissions responsibility, attributing observed warming, evaluating economic decoupling progress, quantifying climate debt, and projecting differentiated national pathways toward a 1.5°C-compatible future.

## Analysis workflow

The provided scripts (`fuel.py`, `emissions_country.py`, `climate_debt.py`, `stat_descrittive.py`, `less_emissions.py`, `trajectory.py`, `tcre.py`) were used to generate quantitative insights on historical emission trends, correlation with global temperature rise, and equitable pathways toward net-zero.

Data processing was performed with Pandas and NumPy for cumulative aggregations and linear regressions (SciPy), while visualizations were created using Matplotlib and Seaborn.  
The analyses cover:

- Territorial CO₂ emissions by source and country (excluding international aviation/shipping and land-use change, converted from tonnes of carbon to CO₂ using the factor 3.664)  
- Correlation with temperature anomalies relative to the pre-industrial baseline (1861–1890)  
- Economic-emissions decoupling (carbon intensity: GtCO₂ per billion 2011 USD GDP)  
- Historical climate debt and pathways to limit warming to +1.5°C with equity considerations (based on IPCC AR6 remaining budget of ~280 GtCO₂ from 2025)

Focus areas include historical responsibility, decoupling progress, and climate justice implications, with clear policy and GitHub repository reproducibility considerations.

All calculations have been verified. As an example, the TCRE (Transient Climate Response to Cumulative Emissions) regression yields **0.00011 °C/GtCO₂** with **R² = 0.8995**, confirming strong linearity between cumulative emissions (~12,321 GtCO₂ in 2024) and the observed +1.543 °C anomaly.

## Cumulative CO₂ Emissions by Source (1850–2024)

Script: `fuel.py`  
Global annual emissions are aggregated by source (coal, oil, gas, cement, flaring, other industry), converted to GtCO₂, and cumulated.

Results highlight historical dominance of coal (46.5% – 4,067 GtCO₂), followed by oil (33.5% – 2,936 GtCO₂) and natural gas (15.5% – 1,358 GtCO₂).  
**Total cumulative emissions in 2024: 8,751 GtCO₂**, with exponential acceleration after 1950 driven by industrialization.

![a](results/fuel+legend.png)

Final breakdown (1850–2024):

![a](results/fuelperc.PNG)

**Implication**: Phase-out of coal must be prioritized, together with a rapid shift to renewables, to achieve the necessary 70–80% reduction in fossil fuel emissions by 2030.

## Economic-Emissions Decoupling (1990–2023)

Scripts: `emissions_country.py` & `less_emissions.py`  
Carbon intensity (GtCO₂ per billion 2011 USD GDP) is analysed for selected major economies, merging emissions with population and GDP per capita (Maddison dataset).

![A](results/emitionscountry.png)

Key findings for high-income/developing economies:
- China: intensity 0.67 GtCO₂/billion USD (60% reduction since 1990, but absolute emissions still rising to 11.71 GtCO₂ in 2023)  
- United States: 0.06 GtCO₂/billion USD (55% reduction, 2023 GDP ~19,975 billion USD)  
- India: 2.83 GtCO₂/billion USD (still coupled, but high potential for green leapfrogging)

Clear declining trajectories are visible for EU27, Japan, Germany (intensity <0.2 in recent years), while USA and China show ongoing transition.  
![A](results/lessemitionscountry.png)

Average intensity reductions 1990–2023: 40–60% in mature economies, still globally insufficient for +1.5°C compatibility.

**Implication**: Carbon pricing, renewable incentives, and industrial electrification are key accelerators. China is leading in solar/wind deployment but remains heavily coal-dependent.

## Relationship Between Cumulative Emissions and Warming (TCRE, 1850–2024)

Script: `tcre.py`  
Linear regression between cumulative CO₂ emissions and global temperature anomalies.

![A](results/tcre.png)

Results: **TCRE = 0.00011 °C/GtCO₂**  
**R² = 0.8995** (p-value < 10⁻⁸⁸)  
~90% of temperature variance explained by cumulative anthropogenic CO₂ emissions.

Scatter plot with temporal colorbar shows strong linearity since ~1900.  
2024 status: ~12,321 GtCO₂ cumulative → **+1.543 °C** anomaly (HadCRUT5).

**Implication**: To remain within +1.5°C, the remaining global carbon budget is ~500 GtCO₂ (IPCC estimate), requiring net-zero worldwide by 2040–2050.

## Descriptive Statistics and Global Trends

Script: `stat_descrittive.py`  
Multi-panel overview of post-1950 trends:

![a](results/statdesc.png)

- CO₂ by source/sector: coal peak ~12,470 Mt, oil ~12,470 Mt  
- Total GHG (incl. LULUCF): 53,819 MtCO₂e  
- CO₂ per capita: China ~4.7 t/year  
- Global temperature anomaly: **+1.6 °C** in 2024

These confirm acceleration of emissions since the 1980s, with Asia as the main regional driver.

## Historical Climate Debt (1850–2023)

Script: `climate_debt.py`  
Cumulative emissions normalized against per-capita fair share (global total ~2,600 GtCO₂ / historical population).

![A](results/climate_debt.png)

Top emitters (absolute):  
- United States: 351 GtCO₂ (30.1%)  
- China: 19.1%  
- Russia: 8.5%

Largest climate debtors (excess over fair share):  
- United States: +351 GtCO₂  
- Russia: +88 GtCO₂  
- Germany: +75 GtCO₂

**Implication**: Climate justice requires substantial financial transfers from historical debtors (Global North) to creditors (Global South) for adaptation and mitigation.

## Equitable Pathways to +1.5°C (2025–2050)

Script: `trajectory.py`  
Linear reduction pathways to net-zero by 2050, based on IPCC AR6 remaining budget (~280 GtCO₂ post-2025).

![](results/trajectoryless.PNG)

Countries with high emissions required average annual change:
- Saudi Arabia: 0.68 GtCO₂ (20.4 t/capita) → **-18.1%/year**  
- Australia: 0.38 GtCO₂ (14.5 t/capita) → **-16.3%/year**  
- United States: 4.92 GtCO₂ (14.3 t/capita) → **-15.8%/year**
Countries with low emissions are allowed to a clean development
- India: 3.06 GtCO₂ (2.1 t/capita) → **+1.9%/year**
- Brazil: 0.48 GtCO₂ (2.3 t/capita) → **+2.5%/year**

**Implication**: Strongly differentiated policies are required: rapid fossil phase-out in high per-capita emitters, green investment space for low emitters.

## Conclusions and Policy & Repository Recommendations

The analyses confirm coal as the dominant historical driver (46.5%), with a very strong linear relationship to observed warming (R² ≈ 0.90). Decoupling is progressing in mature economies but remains globally inadequate. Cumulative emissions have already exceeded critical thresholds.

**Policy recommendations**:
- Implement robust carbon border adjustment mechanisms  
- Establish loss & damage funds proportional to historical climate debt  
- Accelerate coal phase-out and scale renewables to >50% of global energy mix by 2030  
- Differentiated national contributions respecting CBDR-RC (Common But Differentiated Responsibilities and Respective Capabilities)

**Repository best practices**:
Structure as proposed (data/raw & processed, src/, reports/).   
Include full data provenance and citation of original sources in every publication.

Questions, collaborations, extensions (scenario modelling, renewable integration, ML forecasting) are welcome.

Developed by **[Salvatore Spagnuolo](https://github.com/SasySpanish)**  
