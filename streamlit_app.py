# streamlit_host_dashboard.py
# A Streamlit app that inlines JSON and GeoJSON data to avoid fetch path issues

import json
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Utility to load local files
def load_file(file_name: str) -> str:
    return (Path(__file__).parent / file_name).read_text(encoding="utf-8")

# Main application
def main():
    # Configure page
    st.set_page_config(
        page_title="California Infectious Disease Dashboard",
        layout="wide"
    )
    st.title("California Infectious Disease Dashboard")

    base_path = Path(__file__).parent
    # Load HTML template
    html_content = load_file("index.html")

    # Load and compact JSON and GeoJSON data
    raw_data = load_file("idb_2001-2023.json")
    raw_geo = load_file("california-counties.geojson")
    compact_data = json.dumps(json.loads(raw_data))
    compact_geo = json.dumps(json.loads(raw_geo))

    # Inject inline data in place of fetch calls
    html_content = html_content.replace(
        "const response = await fetch('idb_2001-2023.json');",
        f"const response = {{ ok: true, json: async () => {compact_data} }};"
    )
    html_content = html_content.replace(
        "const response = await fetch('california-counties.geojson');",
        f"const response = {{ ok: true, json: async () => {compact_geo} }};"
    )

    # Render the dashboard
    components.html(
        html_content,
        height=800,
        scrolling=True
    )

    # Provide download links
    st.markdown("### Download source files:")
    st.markdown("- [Dashboard HTML](index.html)")
    st.markdown("- [Data (2001-2023)](idb_2001-2023.json)")
    st.markdown("- [GeoJSON Counties](california-counties.geojson)")

if __name__ == "__main__":
    main()
