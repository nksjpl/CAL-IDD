# streamlit_host_dashboard.py
# A Streamlit app that inlines JSON and GeoJSON data with regex-based replacement for robust embedding

import re
import json
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Utility to load local files
def load_file(file_name: str) -> str:
    return (Path(__file__).parent / file_name).read_text(encoding="utf-8")

# Inline JSON data by replacing fetch calls using regex
def inline_data(html: str, filename: str) -> str:
    raw = load_file(filename)
    try:
        compact = json.dumps(json.loads(raw))
    except Exception as e:
        st.error(f"Failed to load or parse {filename}: {e}")
        return html
    # Replace any fetch('filename') call
    pattern = rf"await fetch\(['\"]{filename}['\"]\)"
    replacement = f"await (async ()=> {{ return {{ ok: true, json: async ()=> {compact} }} }})()"
    return re.sub(pattern, replacement, html)

# Main application
def main():
    st.set_page_config(
        page_title="California Infectious Disease Dashboard",
        layout="wide"
    )
    st.title("California Infectious Disease Dashboard")

    # Load raw dashboard HTML
    html_content = load_file("index.html")

    # Inline JSON and GeoJSON data
    html_content = inline_data(html_content, "idb_2001-2023.json")
    html_content = inline_data(html_content, "california-counties.geojson")

    # Render the dashboard
    components.html(
        html_content,
        height=900,
        scrolling=True
    )

    # Source downloads
    st.markdown("### Source Files:")
    files = ["index.html", "idb_2001-2023.json", "california-counties.geojson"]
    for f in files:
        st.markdown(f"- [{f}]({f})")

if __name__ == "__main__":
    main()
