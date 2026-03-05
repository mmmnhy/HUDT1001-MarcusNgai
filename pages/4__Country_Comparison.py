import streamlit as st
import pandas as pd
import wbgapi as wb

st.set_page_config(page_title="Country Comparison", page_icon="📈", layout="wide")

st.title("📈 Country Comparison")
st.markdown("Compare multiple indicators across different countries side by side.")

# Sidebar
st.sidebar.header("Settings")

# Multiple indicator selection
indicators = {
    "Population": "SP.POP.TOTL",
    "GDP (current US$)": "NY.GDP.MKTP.CD",
    "GDP per capita": "NY.GDP.PCAP.CD",
    "Life expectancy": "SP.DYN.LE00.IN",
    "Literacy rate (%)": "SE.ADT.LITR.ZS",
    "CO2 emissions (metric tons per capita)": "EN.ATM.CO2E.PC",
    "Internet users (% of population)": "IT.NET.USER.ZS",
    "Urban population (% of total)": "SP.URB.TOTL.IN.ZS"
}

selected_indicators = st.sidebar.multiselect(
    "Select Indicators (up to 4)", 
    list(indicators.keys()),
    default=["Population", "GDP per capita", "Life expectancy"]
)

countries_input = st.sidebar.text_input("Country Codes (comma-separated)", "USA,CHN,IND,JPN,DEU")
year = st.sidebar.slider("Year", 1960, 2023, 2022)

# Fetch and display data
if st.sidebar.button("Compare", type="primary") and selected_indicators:
    try:
        with st.spinner("Fetching comparison data..."):
            countries = [c.strip() for c in countries_input.split(",")]
            
            # Create comparison dataframe
            comparison_data = {}
            
            for indicator_name in selected_indicators:
                indicator_code = indicators[indicator_name]
                try:
                    data = wb.data.DataFrame(indicator_code, countries, time=year)
                    comparison_data[indicator_name] = data[f'YR{year}']
                except:
                    st.warning(f"⚠️ Could not fetch data for {indicator_name}")
            
            if comparison_data:
                df = pd.DataFrame(comparison_data)
                
                st.success("✅ Comparison data loaded!")
                
                # Display comparison table
                st.subheader(f"📊 Country Comparison - Year {year}")
                st.dataframe(df.style.format("{:.2f}"), use_container_width=True)
                
                # Create visualizations for each indicator
                st.subheader("📈 Visual Comparisons")
                
                cols = st.columns(2)
                for idx, indicator_name in enumerate(selected_indicators):
                    with cols[idx % 2]:
                        st.markdown(f"**{indicator_name}**")
                        chart_data = df[indicator_name].sort_values(ascending=False)
                        st.bar_chart(chart_data)
                
                # Ranking
                st.subheader("🏆 Rankings")
                ranking_cols = st.columns(len(selected_indicators))
                
                for idx, indicator_name in enumerate(selected_indicators):
                    with ranking_cols[idx]:
                        st.markdown(f"**{indicator_name}**")
                        ranked = df[indicator_name].sort_values(ascending=False)
                        for rank, (country, value) in enumerate(ranked.items(), 1):
                            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
                            st.write(f"{medal} {country}: {value:.2f}")
                
                # Download option
                st.subheader("📥 Export Data")
                csv = df.to_csv()
                st.download_button(
                    label="Download Comparison as CSV",
                    data=csv,
                    file_name=f"country_comparison_{year}.csv",
                    mime="text/csv"
                )
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Make sure your country codes are valid.")

elif st.sidebar.button("Compare", type="primary"):
    st.warning("⚠️ Please select at least one indicator.")

# Information
st.sidebar.markdown("---")
st.sidebar.info("""
**How to use:**

1. Select up to 4 indicators
2. Enter country codes (comma-separated)
3. Choose a year
4. Click 'Compare'

**Example Country Codes:**
USA, CHN, IND, JPN, DEU, GBR, FRA, BRA, CAN, AUS
""")
