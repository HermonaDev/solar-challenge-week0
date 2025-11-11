# app/main.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Solar Farm Analysis", layout="wide")
st.title("🌞 Cross-Country Solar Farm Analysis")
st.markdown("Compare solar potential across Benin, Sierra Leone, and Togo")

# Sidebar for country selection
st.sidebar.header("Dashboard Controls")
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    ["Benin", "Sierra Leone", "Togo"],
    default=["Benin", "Sierra Leone", "Togo"]
)

# Load data function
@st.cache_data
def load_country_data(country_name):
    try:
        return pd.read_csv(f'data/{country_name.lower().replace(" ", "_")}_clean.csv')
    except FileNotFoundError:
        st.error(f"Data file for {country_name} not found.")
        return None

if selected_countries:
    st.header("Solar Irradiance Comparison")
    
    # Placeholder for visualizations
    st.info("Dashboard under development - Add visualizations here")
    
    # Display basic stats
    col1, col2, col3 = st.columns(3)
    
    for i, country in enumerate(selected_countries):
        df = load_country_data(country)
        if df is not None:
            with [col1, col2,  col3][i]:
                st.metric(
                    label=f"Avg GHI - {country}",
                    value=f"{df['GHI'].mean():.1f} W/m²"
                )
    # Boxplot comparison
st.header("Solar Metric Distributions")
metric = st.selectbox("Select Metric:", ["GHI", "DNI", "DHI"])

if len(selected_countries) > 0:
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data_to_plot = []
    labels = []
    for country in selected_countries:
        df = load_country_data(country)
        if df is not None:
            data_to_plot.append(df[metric])
            labels.append(country)
    
    ax.boxplot(data_to_plot, labels=labels)
    ax.set_ylabel(f'{metric} (W/m²)')
    ax.set_title(f'{metric} Distribution by Country')
    st.pyplot(fig)

# Country ranking table
st.header("Country Ranking by Solar Potential")
ranking_data = []
for country in selected_countries:
    df = load_country_data(country)
    if df is not None:
        ranking_data.append({
            'Country': country,
            'Avg GHI (W/m²)': f"{df['GHI'].mean():.1f}",
            'Avg DNI (W/m²)': f"{df['DNI'].mean():.1f}", 
            'Avg DHI (W/m²)': f"{df['DHI'].mean():.1f}"
        })

if ranking_data:
    ranking_df = pd.DataFrame(ranking_data)
    ranking_df = ranking_df.sort_values('Avg GHI (W/m²)', ascending=False)
    st.dataframe(ranking_df, use_container_width=True)
else:
    st.warning("Please select at least one country from the sidebar.")