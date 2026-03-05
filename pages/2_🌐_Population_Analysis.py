import streamlit as st
import pandas as pd
import wbgapi as wb

st.set_page_config(page_title="Population Analysis", page_icon="🌐", layout="wide")

st.title("🌐 Population Analysis")
st.markdown("Explore global population trends and demographics.")

# Predefined country groups
country_groups = {
    "G7 Countries": ["USA", "CAN", "GBR", "FRA", "DEU", "ITA", "JPN"],
    "BRICS": ["BRA", "RUS", "IND", "CHN", "ZAF"],
    "Most Populous": ["CHN", "IND", "USA", "IDN", "PAK", "BRA", "NGA"],
    "Europe": ["DEU", "FRA", "GBR", "ITA", "ESP", "POL", "ROU"],
    "Asia": ["CHN", "IND", "IDN", "PAK", "BGD", "JPN", "PHL"]
}

# Sidebar
st.sidebar.header("Settings")
selected_group = st.sidebar.selectbox("Select Country Group", list(country_groups.keys()))
countries = country_groups[selected_group]

year_range = st.sidebar.slider("Year Range", 1960, 2023, (2000, 2023))

# Fetch population data
if st.sidebar.button("Load Data", type="primary"):
    try:
        with st.spinner("Fetching population data..."):
            # Total population
            pop_data = wb.data.DataFrame('SP.POP.TOTL', countries, 
                                         time=range(year_range[0], year_range[1] + 1))
            
            st.success("✅ Data loaded successfully!")
            
            # Display metrics for latest year
            st.subheader("📊 Current Population (Latest Available)")
            cols = st.columns(min(len(countries), 4))
            latest_year = pop_data.columns[-1]
            
            for idx, country in enumerate(countries):
                with cols[idx % 4]:
                    pop = pop_data.loc[country, latest_year]
                    st.metric(country, f"{pop/1e6:.1f}M" if pop < 1e9 else f"{pop/1e9:.2f}B")
            
            # Line chart
            st.subheader("📈 Population Trends Over Time")
            st.line_chart(pop_data.T)
            
            # Data table
            st.subheader("📋 Raw Data")
            st.dataframe(pop_data, use_container_width=True)
            
            # Growth rate analysis
            st.subheader("📊 Population Growth Rate")
            growth_rate = ((pop_data[pop_data.columns[-1]] - pop_data[pop_data.columns[0]]) / 
                          pop_data[pop_data.columns[0]] * 100)
            growth_df = pd.DataFrame({
                'Country': growth_rate.index,
                'Growth Rate (%)': growth_rate.values
            }).sort_values('Growth Rate (%)', ascending=False)
            
            st.bar_chart(growth_df.set_index('Country'))
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Information
st.sidebar.markdown("---")
st.sidebar.info("""
**About Population Data:**

This page shows total population trends for selected country groups. 
The data is sourced from the World Bank's World Development Indicators.

**Data Source:** World Bank - SP.POP.TOTL
""")
