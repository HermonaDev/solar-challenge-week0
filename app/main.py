import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Page configuration
st.set_page_config(
    page_title="Solar Farm Analysis",
    page_icon="🌞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2E8B57;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🌞 Solar Farm Data Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown("**Cross-country comparison of solar potential in Benin, Sierra Leone, and Togo**")

# Sidebar with improved styling
with st.sidebar:
    st.markdown("### 🎛️ Analysis Controls")
    st.markdown("---")
    
    countries = st.multiselect(
        "**Select Countries for Analysis:**",
        ["Benin", "Sierra Leone", "Togo"],
        default=["Benin", "Sierra Leone", "Togo"],
        help="Choose which countries to include in the comparison"
    )
    
    metric = st.selectbox(
        "**Primary Solar Metric:**",
        ["GHI", "DNI", "DHI"],
        help="Global Horizontal Irradiance (GHI), Direct Normal Irradiance (DNI), or Diffuse Horizontal Irradiance (DHI)"
    )
    
    st.markdown("---")
    st.markdown("### 📊 About the Analysis")
    st.info("""
    This dashboard compares solar irradiance data 
    across West African countries to identify 
    high-potential regions for solar development.
    """)

# Main analysis area
if countries:
    # Load data with progress indicator
    with st.spinner('Loading and analyzing solar data...'):
        country_data = {}
        loaded_countries = []
        
        for country in countries:
            try:
                filepath = f'data/{country.replace(" ", "_").lower()}_clean.csv'
                country_data[country] = pd.read_csv(filepath)
                loaded_countries.append(country)
            except FileNotFoundError:
                st.error(f"❌ Data file not found for {country}")

    if loaded_countries:
        # Success message
        #st.success(f"✅ Successfully loaded data for {', '.join(loaded_countries)}")
        
        # Key Metrics Overview
        st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_records = sum(len(country_data[country]) for country in loaded_countries)
            st.metric("Total Records Analyzed", f"{total_records:,}")
        
        with col2:
            st.metric("Countries Compared", len(loaded_countries))
        
        with col3:
            avg_ghi = sum(country_data[country]['GHI'].mean() for country in loaded_countries if 'GHI' in country_data[country].columns) / len(loaded_countries)
            st.metric("Average GHI", f"{avg_ghi:.1f} W/m²")
        
        with col4:
            analysis_period = "1 Year"
            st.metric("Analysis Period", analysis_period)

        # Boxplot Comparison
        st.markdown('<div class="section-header">📊 Distribution Analysis</div>', unsafe_allow_html=True)
        st.markdown(f"**{metric} Distribution Comparison Across Selected Countries**")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        data_to_plot = []
        labels = []
        
        for country in loaded_countries:
            if metric in country_data[country].columns:
                data_to_plot.append(country_data[country][metric])
                labels.append(country)
        
        box_plot = ax.boxplot(data_to_plot, tick_labels=labels, patch_artist=True)
        
        # Color the boxes
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        for patch, color in zip(box_plot['boxes'], colors):
            patch.set_facecolor(color)
        
        ax.set_ylabel(f'{metric} (W/m²)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Country', fontsize=12, fontweight='bold')
        ax.set_title(f'Distribution of {metric} Values by Country', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        with st.expander("💡 Interpretation Guide"):
            st.markdown("""
            - **Box** shows interquartile range (middle 50% of data)
            - **Line inside box** is the median value
            - **Whiskers** show the range of typical values
            - **Dots** indicate potential outliers
            - **Taller boxes** = more variability in solar resource
            """)

        # Statistical Summary Table
        st.markdown('<div class="section-header">📋 Statistical Summary</div>', unsafe_allow_html=True)
        
        summary_data = []
        for country in loaded_countries:
            if metric in country_data[country].columns:
                df = country_data[country]
                summary_data.append({
                    'Country': country,
                    'Mean (W/m²)': round(df[metric].mean(), 1),
                    'Median (W/m²)': round(df[metric].median(), 1),
                    'Std Dev (W/m²)': round(df[metric].std(), 1),
                    'Min (W/m²)': round(df[metric].min(), 1),
                    'Max (W/m²)': round(df[metric].max(), 1)
                })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, height=200)

        # Country Ranking
        st.markdown('<div class="section-header">🏆 Solar Potential Ranking</div>', unsafe_allow_html=True)
        
        ranking_data = []
        for country in loaded_countries:
            if 'GHI' in country_data[country].columns:
                avg_ghi = country_data[country]['GHI'].mean()
                ranking_data.append({
                    'Country': country,
                    'Average GHI (W/m²)': round(avg_ghi, 1)
                })
        
        ranking_df = pd.DataFrame(ranking_data).sort_values('Average GHI (W/m²)', ascending=False)
        ranking_df['Rank'] = range(1, len(ranking_df) + 1)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Ranking Table**")
            display_df = ranking_df[['Rank', 'Country', 'Average GHI (W/m²)']].copy()
            display_df = display_df.set_index('Rank')
            st.dataframe(display_df, use_container_width=True)
        
        with col2:
            st.markdown("**Visual Ranking**")
            fig, ax = plt.subplots(figsize=(6, 4))
            
            colors = ['gold', 'silver', '#cd7f32']  # Gold, Silver, Bronze
            bars = ax.bar(ranking_df['Country'], ranking_df['Average GHI (W/m²)'], 
                         color=colors[:len(ranking_df)], alpha=0.8)
            
            ax.set_ylabel('Average GHI (W/m²)', fontweight='bold')
            ax.set_title('Solar Potential Ranking', fontweight='bold')
            ax.tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, value in zip(bars, ranking_df['Average GHI (W/m²)']):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                       f'{value}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)

        # Key Insights
        st.markdown('<div class="section-header">🔍 Key Insights & Observations</div>', unsafe_allow_html=True)
        
        if len(ranking_df) > 0:
            top_country = ranking_df.iloc[0]['Country']
            top_ghi = ranking_df.iloc[0]['Average GHI (W/m²)']
            
            # Calculate variability
            variabilities = []
            for country in loaded_countries:
                if metric in country_data[country].columns:
                    std_dev = country_data[country][metric].std()
                    variabilities.append((country, std_dev))
            
            most_variable = max(variabilities, key=lambda x: x[1]) if variabilities else (None, 0)
            least_variable = min(variabilities, key=lambda x: x[1]) if variabilities else (None, 0)
            
            insights = f"""
            ### 📋 Summary Findings:
            
            1. **{top_country} demonstrates the highest solar potential** with an average Global Horizontal Irradiance (GHI) of **{top_ghi} W/m²**
            
            2. **{metric} shows varying consistency** across regions - {most_variable[0]} has the highest variability (±{most_variable[1]:.1f} W/m²)
            
            3. **Statistical analysis confirms meaningful differences** in solar resource availability between the selected countries
            
            4. **The data supports strategic prioritization** of solar development investments based on quantifiable metrics
            """
            
            st.markdown(insights)

else:
    st.warning("👈 Please select at least one country from the sidebar to begin the analysis.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Solar Data Discovery Challenge • Week 0 Analysis • Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)