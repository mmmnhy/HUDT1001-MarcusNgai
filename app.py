import streamlit as st
import pandas as pd
import wbgapi as wb

st.title("World Bank Data Explorer")
st.write("Explore World Bank data using the wbgapi library")

# Sidebar for user input
st.sidebar.header("Settings")
indicator = st.sidebar.text_input("Indicator Code", "SP.POP.TOTL")
country_codes = st.sidebar.text_input("Country Codes (comma-separated)", "USA,CHN,IND")
start_year = st.sidebar.number_input("Start Year", min_value=2000, max_value=2025, value=2018)
end_year = st.sidebar.number_input("End Year", min_value=2000, max_value=2025, value=2023)

# Fetch data button
if st.sidebar.button("Fetch Data"):
    try:
        with st.spinner("Fetching data from World Bank..."):
            countries = [c.strip() for c in country_codes.split(",")]
            data = wb.data.DataFrame(indicator, countries, time=range(start_year, end_year + 1))
            
            st.success("Data fetched successfully!")
            st.subheader("Data Preview")
            st.dataframe(data)
            
            st.subheader("Data Visualization")
            st.line_chart(data.T)
            
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        st.info("Make sure the indicator code and country codes are valid.")

# Information section
st.sidebar.markdown("---")
st.sidebar.info("""
**Common Indicators:**
- SP.POP.TOTL: Population
- NY.GDP.MKTP.CD: GDP
- SP.DYN.LE00.IN: Life Expectancy

**Common Country Codes:**
- USA, CHN, IND, GBR, JPN
""")
