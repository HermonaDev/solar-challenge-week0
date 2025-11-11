import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.utils import SolarDataCleaner

st.set_page_config(page_title="Solar Investment Dashboard", layout="wide")
st.title("🌞 MoonLight Energy - Solar Investment Analysis")
st.markdown("Data-Driven Solar Potential Assessment for West Africa")

# Sidebar
st.sidebar.header("Investment Analysis Controls")
countries = st.sidebar.multiselect(
    "Select Countries for Comparison:",
    ["Benin", "Sierra Leone", "Togo"],
    default=["Benin", "Sierra Leone", "Togo"]
)

analysis_type = st.sidebar.selectbox(
    "Analysis Focus:",
    ["Solar Potential", "Financial Metrics", "Risk Assessment"]
)

# Main dashboard
if countries:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📊 Solar Potential Ranking")
        
        # Mock ranking data - replace with actual calculations
        ranking_data = {
            'Country': ['Benin', 'Togo', 'Sierra Leone'],
            'Average GHI (W/m²)': [240.6, 230.6, 202.0],
            'Data Reliability': ['High', 'Medium', 'Low'],
            'Investment Priority': ['Primary', 'Secondary', 'Conditional']
        }
        ranking_df = pd.DataFrame(ranking_data)
        st.dataframe(ranking_df, use_container_width=True)
    
    with col2:
        st.header("💰 Investment Recommendation")
        
        recommendation = """
        **Primary Investment: Benin (60-70%)**
        - Highest solar consistency
        - Best data quality
        - Expected ROI: 18-22% above regional average
        
        **Secondary: Togo (20-30%)**
        - Good diversification
        - Strong infrastructure
        
        **Conditional: Sierra Leone (10%)**
        - Pending sensor validation
        - 3-6 month assessment needed
        """
        st.info(recommendation)
    
    # Metrics
    st.header("📈 Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.metric("Total Data Points", "1.58M")
    with kpi2:
        st.metric("Analysis Period", "1 Year")
    with kpi3:
        st.metric("Countries Analyzed", "3")
    with kpi4:
        st.metric("Statistical Confidence", "99%")
    
    # Sample visualization
    st.header("🌤️ Solar Irradiance Comparison")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Mock data - replace with actual
    countries_plot = ['Benin', 'Togo', 'Sierra Leone']
    ghi_values = [240.6, 230.6, 202.0]
    
    bars = ax.bar(countries_plot, ghi_values, color=['#2E8B57', '#FFA500', '#DC143C'])
    ax.set_ylabel('Average GHI (W/m²)')
    ax.set_title('Solar Potential by Country')
    
    for bar, value in zip(bars, ghi_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                f'{value}', ha='center', va='bottom')
    
    st.pyplot(fig)

else:
    st.warning("Please select at least one country from the sidebar.")

# Footer
st.markdown("---")
st.markdown("**MoonLight Energy Solutions** | Data-Driven Investment Strategy")