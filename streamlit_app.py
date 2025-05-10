# streamlit_host_dashboard.py
# A simple Streamlit app to host and display the provided HTML dashboard

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Function to load a local file relative to this script
def load_file(file_name: str) -> str:
    base_path = Path(__file__).parent
    file_path = base_path / file_name
    return file_path.read_text(encoding="utf-8")

# Main application entry point
def main():
    # Configure page settings
    st.set_page_config(
        page_title="California Infectious Disease Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Title
    st.title("California Infectious Disease Dashboard")

    # Load and render the HTML file
    html_content = load_file("index.html")
    components.html(
        html_content,
        height=800,
        scrolling=True
    )

    # Provide download links for source files
    st.markdown("### Download source files:")
    st.markdown("- [Dashboard HTML](index.html)")
    st.markdown("- [Data (2001-2023)](idb_2001-2023.json)")
    st.markdown("- [GeoJSON Counties](california-counties.geojson)")

if __name__ == "__main__":
    main()
