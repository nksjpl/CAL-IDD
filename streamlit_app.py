import streamlit as st
import json
import geopandas as gpd
import pandas as pd
import altair as alt
import folium
from streamlit_folium import folium_static

# Load the data
try:
    with open('idb_2001-2023.json') as f:
        data = json.load(f)
    counties_gdf = gpd.read_file('california-counties.geojson')
except FileNotFoundError:
    st.error("Make sure 'idb_2001-2023.json' and 'california-counties.geojson' are in the same directory as your Streamlit app.")
    st.stop()

# Convert data to pandas DataFrame
df = pd.DataFrame(data)

# Convert the 'timestamp' column to datetime objects
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract year
df['year'] = df['timestamp'].dt.year

# Streamlit App
st.title('California Births Dashboard (2001-2023)')

st.write("""
This dashboard visualizes California birth data from 2001 to 2023.
Explore the total number of births per year and the distribution across counties.
""")

# Sidebar filters
st.sidebar.header('Filters')
selected_year = st.sidebar.slider('Select Year', int(df['year'].min()), int(df['year'].max()), int(df['year'].min()))

# Filter data by selected year
df_filtered = df[df['year'] == selected_year].copy()

# Ensure county names in data match GeoJSON
df_filtered['county'] = df_filtered['county'].str.replace(' County', '')

# Aggregate births by county for the selected year
births_by_county = df_filtered.groupby('county')['births'].sum().reset_index()

# Merge county data with GeoDataFrame
counties_merged = counties_gdf.merge(births_by_county, left_on='name', right_on='county', how='left')

# Handle counties with no data (fill NaN with 0 births)
counties_merged['births'] = counties_merged['births'].fillna(0)

# Data Visualization

# 1. Time Series of Total Births
st.header('Total Births Over Time')
total_births_yearly = df.groupby('year')['births'].sum().reset_index()

chart_total_births = alt.Chart(total_births_yearly).mark_line(point=True).encode(
    x=alt.X('year:O', title='Year'),
    y=alt.Y('births', title='Total Births'),
    tooltip=['year', 'births']
).properties(
    title='Total Births in California by Year'
).interactive()
st.altair_chart(chart_total_births, use_container_width=True)

# 2. Map of Births by County for the selected year
st.header(f'Births by County in {selected_year}')

# Create a Folium map
m = folium.Map(location=[37, -120], zoom_start=5)

# Add a choropleth layer
folium.Choropleth(
    geo_data=counties_merged,
    name='choropleth',
    data=counties_merged,
    columns=['name', 'births'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f'Total Births in {selected_year}',
).add_to(m)

# Add tooltips
folium.features.GeoJson(
    counties_merged,
    tooltip=folium.features.GeoJsonTooltip(fields=['name', 'births'],
                                          aliases=['County:', 'Births:'])
).add_to(m)

# Display the map
folium_static(m)

# Optional: Display raw data for the selected year
if st.checkbox(f'Show raw data for {selected_year}'):
    st.subheader(f'Raw Data for {selected_year}')
    st.dataframe(df_filtered)
