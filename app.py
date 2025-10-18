# ===================================================
# app.py — Interactive GLOF Hazard Map with Map Selector
# ===================================================
import streamlit as st
import folium
from branca.colormap import LinearColormap
import pandas as pd
from streamlit_folium import st_folium

# ---------------------------------------------------
# 1. Page setup
# ---------------------------------------------------
st.set_page_config(page_title="Himalayan GLOF Hazard Map", layout="wide")
st.title("🌊 Himalayan Glacial Lake Outburst Flood (GLOF) Hazard Map")
st.markdown("Explore glacial lakes across the Himalayas with predicted hazard probabilities from the ML model.")

# ---------------------------------------------------
# 2. Load dataset
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("hazard_probabilities.csv")

hazard_df = load_data()

# ---------------------------------------------------
# 3. Sidebar map selector
# ---------------------------------------------------
st.sidebar.header("🗺️ Map Settings")

base_maps = {
    "OpenStreetMap": "OpenStreetMap",
    "CartoDB Positron": "CartoDB.Positron",
    "CartoDB Dark Matter": "CartoDB.DarkMatter",
    "Stamen Terrain": "Stamen.Terrain",
    "Stamen Toner": "Stamen.Toner",
    "Stamen Watercolor": "Stamen.Watercolor",
    "Esri Satellite": "Esri.WorldImagery",
    "Esri NatGeo": "Esri.NatGeoWorldMap",
    "OpenTopoMap": "OpenTopoMap",
    "NASAGIBS Night Lights": "NASAGIBS.ViirsEarthAtNight2012"
}

selected_map = st.sidebar.selectbox(
    "Choose Base Map Style:",
    options=list(base_maps.keys()),
    index=1
)

zoom_level = st.sidebar.slider("Zoom Level", 5, 12, 7)

# ---------------------------------------------------
# 4. Create base map dynamically
# ---------------------------------------------------
hazard_map = folium.Map(
    location=[28.2, 87.0],  # Center near Makalu-Barun / eastern Nepal
    zoom_start=zoom_level,
    tiles=selected_map,
    attr="© OpenStreetMap contributors"
)

# ---------------------------------------------------
# 5. Create continuous color scale
# ---------------------------------------------------
colormap = LinearColormap(
    ['green', 'yellow', 'orange', 'red', 'darkred'],
    vmin=0, vmax=1,
    caption='Hazard Probability'
)
colormap.add_to(hazard_map)

# ---------------------------------------------------
# 6. Plot each lake
# ---------------------------------------------------
area_col = "Lake_area_calculated_ha"

for _, row in hazard_df.iterrows():
    prob = row["Hazard_Prob"]
    area = row.get(area_col, 0.5)
    color = colormap(prob)
    radius = max(2, min(area / 30, 10))

    popup_html = f"""
    <b>Lake Information</b><br>
    <b>Latitude:</b> {row.get('Latitude', float('nan')):.4f}<br>
    <b>Longitude:</b> {row.get('Longitude', float('nan')):.4f}<br>
    <b>Lake Area (ha):</b> {row.get('Lake_area_calculated_ha', 0):.2f}<br>
    <b>Elevation (m):</b> {row.get('Elevation_m', 0):.0f}<br>
    <b>Lake Type:</b> {row.get('Lake_type_simplified', 'N/A')}<br>
    <b>Supraglacial:</b> {row.get('is_supraglacial', 'N/A')}<br>
    <b>Glacier Area (ha):</b> {row.get('glacier_area_ha', 0):.2f}<br>
    <b>Slope glac→lake (°):</b> {row.get('slope_glac_to_lake', 0):.2f}<br>
    <b>Glacier Contact:</b> {row.get('glacier_contact', 'N/A')}<br>
    <b>Glacier Touch Count:</b> {row.get('glacier_touch_count', 0)}<br>
    <b>Nearest Glacier Dist (m):</b> {row.get('nearest_glacier_dist_m', 0):.0f}<br>
    <b>Glacier Elev (m):</b> {row.get('glacier_elev_m', 0):.0f}<br>
    <b>5-yr Expansion Rate:</b> {row.get('5y_expansion_rate', 0):.3f}<br>
    <b>10-yr Expansion Rate:</b> {row.get('10y_expansion_rate', 0):.3f}<br>
    <b>Observed GLOF:</b> {row.get('GLOF', 'N/A')}<br>
    <b><font color='{color}'>Hazard Probability:</font></b> {prob:.2f}
    """

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=radius,
        color=None,
        fill=True,
        fill_color=color,
        fill_opacity=0.85,
        popup=folium.Popup(popup_html, max_width=350)
    ).add_to(hazard_map)

# ---------------------------------------------------
# 7. Add layer control + display map
# ---------------------------------------------------
folium.LayerControl().add_to(hazard_map)
st_folium(hazard_map, width=1300, height=750)
