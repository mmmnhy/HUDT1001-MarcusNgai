import streamlit as st
import pandas as pd
import wbgapi as wb

st.set_page_config(page_title="Custom Data Explorer", page_icon="📊", layout="wide")

st.title("📊 Custom Data Explorer")
st.markdown("Fetch any World Bank indicator for your selected countries and time period.")

# Sidebar for user input
st.sidebar.header("Settings")
indicator = st.sidebar.text_input("Indicator Code", "SP.POP.TOTL", 
                                   help="Enter a World Bank indicator code (e.g., SP.POP.TOTL)")
country_codes = st.sidebar.text_input("Country Codes (comma-separated)", "USA,CHN,IND",
                                      help="Enter country ISO3 codes separated by commas")
start_year = st.sidebar.number_input("Start Year", min_value=1960, max_value=2025, value=2018)
end_year = st.sidebar.number_input("End Year", min_value=1960, max_value=2025, value=2023)

# Fetch data button
if st.sidebar.button("Fetch Data", type="primary"):
    try:
        with st.spinner("Fetching data from World Bank..."):
            countries = [c.strip() for c in country_codes.split(",")]
            data = wb.data.DataFrame(indicator, countries, time=range(start_year, end_year + 1))
            
            st.success("✅ Data fetched successfully!")
            
            # Display data
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📋 Data Table")
                st.dataframe(data, use_container_width=True)
            
            with col2:
                st.subheader("📈 Line Chart")
                st.line_chart(data.T)
            
            # Additional visualization
            st.subheader("📊 Bar Chart (Latest Year)")
            latest_year = data.columns[-1]
            st.bar_chart(data[latest_year])
            
    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        st.info("💡 Make sure the indicator code and country codes are valid.")

# Information section
st.sidebar.markdown("---")
st.sidebar.info("""
**Common Indicators:**
- `SP.POP.TOTL`: Population, total
- `NY.GDP.MKTP.CD`: GDP (current US$)
- `SP.DYN.LE00.IN`: Life expectancy at birth
- `SE.ADT.LITR.ZS`: Literacy rate
- `EN.ATM.CO2E.PC`: CO2 emissions per capita

**Common Country Codes:**
- USA, CHN, IND, GBR, JPN, DEU, FRA, BRA, RUS, CAN
""")

st.sidebar.markdown("[🔍 Search for more indicators](https://data.worldbank.org/indicator)")
