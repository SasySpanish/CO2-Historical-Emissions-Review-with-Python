# Analysis Scripts

This folder contains all the Python scripts used for the core analyses in the project.  
Each script is self-contained, well-commented, and designed to run independently after installing the dependencies listed in `requirements.txt`.

### Script Overview

| Script                  | Main Purpose                                                                                  | Primary Output                                              | Main Input Data Files                                      |
|-------------------------|-----------------------------------------------------------------------------------------------|-------------------------------------------------------------|------------------------------------------------------------|
| `fuel.py`               | Computes and visualizes cumulative CO₂ emissions by source (1850–2024)                        | Stacked area chart + console print of percentages & totals  | `co2-by-source.csv`                                        |
| `tcre.py`               | Linear regression between cumulative CO₂ emissions and global temperature anomaly (TCRE)      | Scatter plot with temporal colorbar + TCRE value & R²       | `annual-co2-emissions-per-country.csv`, `temperature-anomaly.csv` |
| `climate_debt.py`       | Calculates historical climate debt per country (1850–2023) relative to per-capita fair share | Pie chart + bar chart of climate debt + top emitters table  | `annual-co2-emissions-per-country.csv`, `population.csv`   |
| `emissions_country.py`  | Extended economic-emissions decoupling analysis (total GDP vs absolute emissions)             | Scatter plot with detailed 2023 legend                      | `annual-co2-emissions-per-country.csv`, `population.csv`, `gdp-per-capita-maddison.csv` |
| `less_emissions.py`     | Focused decoupling analysis with carbon intensity (Europe + major economies)                  | Decoupling scatter + table of intensity & % reduction       | `annual-co2-emissions-per-country.csv`, `population.csv`, `gdp-per-capita-maddison.csv` |
| `trajectory.py`         | Projects national pathways to +1.5°C with climate justice criteria (2025–2050)                | Table of required annual reductions + visualization         | `annual-co2-emissions-per-country.csv`, `population.csv`   |
| `stat_descrittive.py`   | Multi-trend descriptive overview post-1950 (by source, total GHG, per capita, temperature)    | Multi-panel line plots with final value annotations         | All main CSV files (co2-by-source, total-ghg-emissions, co2-per-capita, temperature-anomaly, etc.) |

### Usage Notes

All scripts:
- expect input CSV files to be located in `data/raw/` (or adjust paths accordingly)
- display figures on screen via `.show()` (you can easily add `plt.savefig()` to export)
- do not modify original input files
- were developed with Pandas ≥2.0, NumPy, Matplotlib, Seaborn, and (only in `tcre.py`) SciPy

### Minimum Requirements (requirements.txt)

```text
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
scipy>=1.10    # required only for tcre.py
