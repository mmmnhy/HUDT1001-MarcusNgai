import streamlit as st

st.set_page_config(
    page_title="World Bank Data Explorer",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 World Bank Data Explorer")
st.markdown("""
Welcome to the World Bank Data Explorer! This app allows you to explore and visualize 
World Bank data using the `wbgapi` library.

### Features:
- 📊 **Custom Data Explorer**: Fetch and visualize custom indicators
- 🌐 **Population Analysis**: Explore global population trends
- 💰 **Economic Indicators**: Analyze GDP and economic data
- 📈 **Country Comparison**: Compare multiple countries side by side

### Getting Started:
Select a page from the sidebar to begin exploring!
""")

st.sidebar.success("Select a page above.")

# Quick stats section
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**📚 Data Sources**\n\nWorld Bank Open Data")

with col2:
    st.info("**🌎 Countries**\n\n200+ Countries Available")

with col3:
    st.info("**📊 Indicators**\n\n1000+ Data Series")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit and wbgapi by Marcus Ngai*")
