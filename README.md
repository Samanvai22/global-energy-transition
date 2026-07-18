# ⚡ Powering the Future

## A Global Analysis of the Transition from Fossil Fuels to Renewable Energy

This data visualization project explores how electricity systems around the
world are transitioning from fossil fuels such as coal, oil, and natural gas
towards renewable energy sources such as solar, wind, and hydropower.

The project combines exploratory data analysis, ten analytical questions,
interactive Plotly visualizations, and a Streamlit dashboard.

---

## 🌍 Project Overview

The global energy transition is progressing, but countries are moving at very
different speeds.

This project investigates:

- Global renewable and fossil-fuel electricity trends
- Renewable adoption across major economies
- Countries with the strongest renewable growth
- Renewable electricity and carbon intensity
- GDP per person and renewable adoption
- Electricity-mix differences between Germany and India
- Growth of solar, wind, hydropower, and nuclear electricity
- Electricity expansion alongside fossil-fuel reduction
- Coal and natural-gas dependence across major economies
- Countries with clean large-scale electricity systems

---

## 📊 Interactive Dashboard

The Streamlit dashboard allows users to:

- Select multiple countries
- Change the analysis year range
- Select a comparison year
- Compare renewable and fossil electricity shares
- Explore carbon intensity
- View leading renewable electricity systems
- Inspect filtered data

The public dashboard link will be added after deployment.

---

## 🔍 Main Findings

- Global renewable electricity increased from approximately 19.1% in 1990
  to 33.8% in 2025.
- Germany recorded strong renewable growth, reaching approximately 59.1%
  renewable electricity in 2025.
- Renewable electricity share and carbon intensity showed a strong negative
  relationship in 2024.
- GDP per person alone did not explain renewable electricity adoption.
- Solar was the fastest-growing global electricity source between 2000 and
  2025.
- Several countries increased electricity generation per person while
  reducing fossil-fuel dependence.
- Norway had the lowest carbon intensity among electricity systems generating
  at least 50 TWh in 2024.

---

## 🗂️ Project Structure

```text
global-energy-transition/
│
├── data/
│   ├── owid-energy-data.csv
│   └── clean_energy_data.csv
│
├── dashboard/
│   └── app.py
│
├── notebook/
│   ├── global_energy_analysis.ipynb
│   └── global_energy_analysis_report.html
│
├── presentation/
│
├── images/
│
├── .gitignore
├── README.md
└── requirements.txt