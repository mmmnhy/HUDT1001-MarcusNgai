import streamlit as st
import pandas as pd
import wbgapi as wb

st.set_page_config(page_title="Economic Indicators", page_icon="💰", layout="wide")

st.title("💰 Economic Indicators")
st.markdown("Analyze GDP, economic growth, and other financial indicators.")

# Sidebar
st.sidebar.header("Settings")

indicators = {
    "GDP (current US$)": "NY.GDP.MKTP.CD",
    "GDP per capita": "NY.GDP.PCAP.CD",
    "GDP growth (annual %)": "NY.GDP.MKTP.KD.ZG",
    "Inflation, consumer prices (annual %)": "FP.CPI.TOTL.ZG",
    "Unemployment (% of total labor force)": "SL.UEM.TOTL.ZS"
}

selected_indicator = st.sidebar.selectbox("Select Indicator", list(indicators.keys()))
indicator_code = indicators[selected_indicator]

country_input = st.sidebar.text_input("Country Codes (comma-separated)", "USA,CHN,JPN,DEU,GBR")
year_range = st.sidebar.slider("Year Range", 1960, 2023, (2010, 2023))

# Fetch data
if st.sidebar.button("Load Data", type="primary"):
    try:
        with st.spinner(f"Fetching {selected_indicator} data..."):
            countries = [c.strip() for c in country_input.split(",")]
            data = wb.data.DataFrame(indicator_code, countries, 
                                    time=range(year_range[0], year_range[1] + 1))
            
            st.success("✅ Data loaded successfully!")
            
            # Metrics for latest year
            st.subheader(f"📊 {selected_indicator} (Latest Year)")
            cols = st.columns(min(len(countries), 5))
            latest_year = data.columns[-1]
            
            for idx, country in enumerate(countries):
                with cols[idx % 5]:
                    value = data.loc[country, latest_year]
                    if "GDP" in selected_indicator and "growth" not in selected_indicator:
                        if value >= 1e12:
                            display_value = f"${value/1e12:.2f}T"
                        elif value >= 1e9:
                            display_value = f"${value/1e9:.1f}B"
                        else:
                            display_value = f"${value/1e6:.0f}M"
                    else:
                        display_value = f"{value:.2f}%"
                    st.metric(country, display_value)
            
            # Visualization
            st.subheader("📈 Trends Over Time")
            st.line_chart(data.T)
            
            # Comparison
            st.subheader("📊 Country Comparison (Latest Year)")
            latest_data = data[latest_year].sort_values(ascending=False)
            st.bar_chart(latest_data)
            
            # Data table
            st.subheader("📋 Raw Data")
            st.dataframe(data, use_container_width=True)
            
            # Download button
            csv = data.to_csv()
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{selected_indicator.replace(' ', '_')}_data.csv",
                mime="text/csv"
            )
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Please check your country codes and try again.")

# Information
st.sidebar.markdown("---")
st.sidebar.info("""
**Economic Indicators:**

- **GDP**: Total economic output
- **GDP per capita**: Economic output per person
- **GDP growth**: Annual growth rate
- **Inflation**: Price increase rate
- **Unemployment**: Jobless rate

**Top Economies by GDP:**
- USA, CHN, JPN, DEU, IND, GBR, FRA
""")
