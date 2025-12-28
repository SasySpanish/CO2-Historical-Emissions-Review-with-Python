# Datasets from Our World in Data

This folder contains the raw CSV files downloaded from Our World in Data (OWID) between November and December 2025.  
All datasets are used as the primary source for the analysis of territorial CO₂ and GHG emissions, historical trends, climate impacts, and policy-relevant indicators (cumulative responsibility, decoupling, carbon inequality, 1.5°C compatible pathways).

### Key Characteristics
- **Territorial basis**: Emissions are attributed to the country of production (not consumption-based, except where explicitly noted).
- **Exclusions**: Land-use change (LULUCF) is excluded unless stated otherwise; bunker fuels (international aviation & shipping) are excluded from national totals.
- **Main sources**: Global Carbon Project (GCP), HadCRUT5 (Met Office), Jones et al. (national contributions), Maddison Project Database.
- **License**: All OWID datasets are licensed under CC BY 4.0. Always cite OWID + original producer.

### File Inventory

| File name                                      | Description                                                                 | Primary Source                          | Time coverage     | Main unit                           | Key use in the project                                            |
|------------------------------------------------|-----------------------------------------------------------------------------|-----------------------------------------|-------------------|-------------------------------------|-------------------------------------------------------------------|
| annual-co2-emissions-per-country.csv           | Annual total CO₂ emissions by country (territorial, excl. LULUCF)           | Global Carbon Project                   | 1750–2024         | tonnes CO₂                          | Core dataset for per-country, per-capita, cumulative, regional aggregates |
| co2-by-source.csv                              | Breakdown of CO₂ emissions by source/fuel (coal, oil, gas, cement, flaring, other industry) | Global Carbon Project                   | 1750–2024         | tonnes CO₂                          | Historical fuel-level responsibility (coal ≈45% of cumulative emissions) |
| co2-emissions-by-fuel-line.csv                 | Alternative format of fuel breakdown (very similar to co2-by-source)        | Global Carbon Project                   | 1750–2024         | tonnes CO₂                          | Stacked area charts and cross-validation                          |
| total-ghg-emissions.csv                        | Total greenhouse gas emissions including LULUCF (CO₂eq 100-year GWP)       | Jones et al. (National contributions)   | 1850–2023         | tonnes CO₂ equivalents              | Broader GHG context, including agriculture, forestry, methane     |
| co2-emissions-per-capita.csv                   | CO₂ emissions per capita by country                                         | Global Carbon Project                   | 1750–2024         | tonnes CO₂ per person               | Carbon inequality, historical per-capita debt/credit              |
| annual-co-emissions-by-region.csv              | Aggregated CO₂ emissions by world region/macro-area                         | Global Carbon Project                   | 1750–2024         | tonnes CO₂                          | North–South comparisons, regional responsibility                 |
| temperature-anomaly.csv                        | Global and hemispheric temperature anomalies (HadCRUT5, baseline 1861–1890) | Met Office Hadley Centre – HadCRUT5     | 1850–2025         | °C anomaly                          | Empirical validation of TCRE (≈0.00045 °C per GtCO₂ cumulative)   |
| gdp-per-capita-maddison.csv                    | Historical GDP per capita (Maddison Project Database, constant 2011 USD)   | Maddison Project Database               | 1–2023 (varies)   | 2011 international $ per person     | Economic decoupling, carbon intensity (kgCO₂ per $1000 GDP)       |

### Additional Notes
- **Data processing** in the project includes:
  - Conversion to GtCO₂ / MtCO₂
  - Cumulative sums from 1850
  - Per-capita and intensity calculations
  - Merges on `Entity` + `Year`
  - NaN removal + focus on post-1990 for recent trends
- **Consumption-based alternative** — For trade-adjusted emissions, download the separate OWID dataset: https://ourworldindata.org/consumption-based-co2
- **Updates** — Files downloaded Nov–Dec 2025. Always check OWID for newer releases.
- **Citation** — When using:  
  Our World in Data (2025) – with major processing by [your name/repo]. Original sources: Global Carbon Project, HadCRUT5, Jones et al., Maddison Project.

Last updated: December 28, 2025
