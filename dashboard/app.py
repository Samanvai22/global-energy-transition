from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Global Energy Transition",
    page_icon="⚡",
    layout="wide"
)


# ---------------------------------------------------------
# DATA LOCATION
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "clean_energy_data.csv"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)

    data["year"] = pd.to_numeric(
        data["year"],
        errors="coerce"
    )

    return data


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        f"The dataset was not found at: {DATA_PATH}"
    )
    st.stop()

except Exception as error:
    st.error("The dataset could not be loaded.")
    st.exception(error)
    st.stop()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("⚡ Powering the Future")

st.subheader(
    "A Global Analysis of the Transition from "
    "Fossil Fuels to Renewable Energy"
)

st.markdown(
    """
    Explore how electricity systems are changing across countries.
    Use the filters to compare renewable energy, fossil fuels and
    carbon intensity over time.
    """
)

st.divider()


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
country_options = sorted(
    df["country"]
    .dropna()
    .unique()
    .tolist()
)

default_countries = [
    country
    for country in [
        "Germany",
        "India",
        "China",
        "United States"
    ]
    if country in country_options
]

available_years = sorted(
    df["year"]
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)

minimum_year = min(available_years)
maximum_year = max(available_years)

default_snapshot_year = (
    2024
    if 2024 in available_years
    else maximum_year
)

with st.sidebar:

    st.header("Dashboard filters")

    selected_countries = st.multiselect(
        label="Select countries",
        options=country_options,
        default=default_countries
    )

    selected_year_range = st.slider(
        label="Select year range",
        min_value=minimum_year,
        max_value=maximum_year,
        value=(1990, maximum_year),
        step=1
    )

    snapshot_year = st.select_slider(
        label="Select comparison year",
        options=available_years,
        value=default_snapshot_year
    )

    st.caption(
        "Change these filters to update the dashboard."
    )


if not selected_countries:
    st.warning(
        "Please select at least one country from the sidebar."
    )
    st.stop()


# ---------------------------------------------------------
# FILTERED DATA
# ---------------------------------------------------------
filtered_df = df[
    (
        df["country"].isin(selected_countries)
    )
    &
    (
        df["year"].between(
            selected_year_range[0],
            selected_year_range[1]
        )
    )
].copy()


snapshot_selected = df[
    (
        df["country"].isin(selected_countries)
    )
    &
    (
        df["year"] == snapshot_year
    )
].copy()


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
st.subheader(f"Overview for {snapshot_year}")

average_renewable = (
    snapshot_selected["renewables_share_elec"].mean()
)

average_fossil = (
    snapshot_selected["fossil_share_elec"].mean()
)

average_carbon = (
    snapshot_selected["carbon_intensity_elec"].mean()
)


def percentage_value(value):
    if pd.isna(value):
        return "N/A"

    return f"{value:.1f}%"


def carbon_value(value):
    if pd.isna(value):
        return "N/A"

    return f"{value:.1f} gCO₂e/kWh"


kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    label="Selected countries",
    value=len(selected_countries)
)

kpi2.metric(
    label="Average renewable share",
    value=percentage_value(average_renewable)
)

kpi3.metric(
    label="Average fossil share",
    value=percentage_value(average_fossil)
)

kpi4.metric(
    label="Average carbon intensity",
    value=carbon_value(average_carbon)
)

st.divider()


# ---------------------------------------------------------
# GRAPH 1: RENEWABLE TREND
# ---------------------------------------------------------
st.subheader(
    "Renewable electricity adoption over time"
)

renewable_trend = filtered_df.dropna(
    subset=["renewables_share_elec"]
)

if renewable_trend.empty:

    st.warning(
        "No renewable electricity data is available "
        "for the selected filters."
    )

else:

    fig1 = px.line(
        renewable_trend,
        x="year",
        y="renewables_share_elec",
        color="country",
        title=(
            "Countries followed different renewable "
            "electricity pathways"
        ),
        labels={
            "year": "Year",
            "renewables_share_elec":
                "Renewable electricity share (%)",
            "country": "Country"
        }
    )

    fig1.update_layout(
        template="plotly_white",
        title_x=0.02,
        height=500,
        hovermode="x unified",
        legend_title_text=""
    )

    fig1.update_xaxes(
        gridcolor="#E5E7EB"
    )

    fig1.update_yaxes(
        gridcolor="#E5E7EB",
        rangemode="tozero"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

st.info(
    """
    **How to read this chart:** A rising line means that a country
    is generating a larger share of its electricity from renewable
    sources.
    """
)


# ---------------------------------------------------------
# GRAPH 2: ELECTRICITY MIX
# ---------------------------------------------------------
st.subheader(
    f"Electricity mix comparison in {snapshot_year}"
)

mix_data = snapshot_selected.dropna(
    subset=[
        "renewables_share_elec",
        "fossil_share_elec"
    ]
).copy()

if mix_data.empty:

    st.warning(
        "No electricity-mix data is available "
        "for the selected year."
    )

else:

    mix_data["Renewable energy"] = (
        mix_data["renewables_share_elec"]
        .fillna(0)
    )

    mix_data["Fossil fuels"] = (
        mix_data["fossil_share_elec"]
        .fillna(0)
    )

    mix_data["Nuclear energy"] = (
        (
            mix_data["nuclear_electricity"]
            /
            mix_data["electricity_generation"]
        )
        *
        100
    ).fillna(0)

    mix_data["Other sources"] = (
        100
        -
        mix_data[
            [
                "Renewable energy",
                "Fossil fuels",
                "Nuclear energy"
            ]
        ].sum(axis=1)
    ).clip(lower=0)

    mix_long = mix_data.melt(
        id_vars=["country"],
        value_vars=[
            "Renewable energy",
            "Fossil fuels",
            "Nuclear energy",
            "Other sources"
        ],
        var_name="Energy source",
        value_name="Electricity share"
    )

    fig2 = px.bar(
        mix_long,
        x="country",
        y="Electricity share",
        color="Energy source",
        title=(
            f"Electricity systems remain very different "
            f"across countries in {snapshot_year}"
        ),
        labels={
            "country": "Country",
            "Electricity share":
                "Share of electricity generation (%)"
        },
        color_discrete_map={
            "Renewable energy": "#009E73",
            "Fossil fuels": "#D55E00",
            "Nuclear energy": "#0072B2",
            "Other sources": "#999999"
        }
    )

    fig2.update_layout(
        template="plotly_white",
        title_x=0.02,
        height=500,
        barmode="stack",
        legend_title_text=""
    )

    fig2.update_yaxes(
        range=[0, 100],
        gridcolor="#E5E7EB"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# ---------------------------------------------------------
# GRAPH 3: RENEWABLES VS CARBON INTENSITY
# ---------------------------------------------------------
st.subheader(
    f"Renewable electricity and carbon intensity in {snapshot_year}"
)

scatter_data = df[
    (
        df["year"] == snapshot_year
    )
    &
    (
        df["population"] >= 1_000_000
    )
].dropna(
    subset=[
        "renewables_share_elec",
        "carbon_intensity_elec",
        "population"
    ]
).copy()

if scatter_data.empty:

    st.warning(
        "No carbon-intensity data is available "
        "for the selected year."
    )

else:

    fig3 = px.scatter(
        scatter_data,
        x="renewables_share_elec",
        y="carbon_intensity_elec",
        size="population",
        color="renewables_share_elec",
        hover_name="country",
        size_max=45,
        color_continuous_scale="Viridis",
        title=(
            "Higher renewable electricity shares are generally "
            "linked to lower carbon intensity"
        ),
        labels={
            "renewables_share_elec":
                "Renewable electricity share (%)",
            "carbon_intensity_elec":
                "Carbon intensity (gCO₂e/kWh)",
            "population": "Population"
        }
    )

    fig3.update_layout(
        template="plotly_white",
        title_x=0.02,
        height=550
    )

    fig3.update_xaxes(
        gridcolor="#E5E7EB"
    )

    fig3.update_yaxes(
        gridcolor="#E5E7EB"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# ---------------------------------------------------------
# GRAPH 4: TOP RENEWABLE COUNTRIES
# ---------------------------------------------------------
st.subheader(
    f"Leading renewable electricity systems in {snapshot_year}"
)

top_renewable = df[
    (
        df["year"] == snapshot_year
    )
    &
    (
        df["population"] >= 1_000_000
    )
].dropna(
    subset=["renewables_share_elec"]
).nlargest(
    10,
    "renewables_share_elec"
).sort_values(
    "renewables_share_elec",
    ascending=True
)

if top_renewable.empty:

    st.warning(
        "No renewable ranking data is available "
        "for the selected year."
    )

else:

    fig4 = px.bar(
        top_renewable,
        x="renewables_share_elec",
        y="country",
        orientation="h",
        text="renewables_share_elec",
        title=(
            f"Several countries generated almost all "
            f"their electricity from renewables in {snapshot_year}"
        ),
        labels={
            "renewables_share_elec":
                "Renewable electricity share (%)",
            "country": ""
        }
    )

    fig4.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False
    )

    fig4.update_layout(
        template="plotly_white",
        title_x=0.02,
        height=550,
        margin=dict(
            l=120,
            r=80,
            t=100,
            b=60
        )
    )

    fig4.update_xaxes(
        range=[0, 105],
        gridcolor="#E5E7EB"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )


# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------
with st.expander(
    "View filtered dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "Dataset source: Our World in Data Energy Dataset"
)