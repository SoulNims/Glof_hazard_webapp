# 🌊 Himalayan Glacial Lake Outburst Flood (GLOF) Hazard Map

An interactive **web-based hazard visualization tool** that maps over **2,600 Himalayan glacial lakes** with machine learning–predicted GLOF (Glacial Lake Outburst Flood) probabilities.  

Built using **Streamlit** and **Folium**, this app allows users to explore regional lake-level risks, visualize spatial patterns, and view individual lake attributes derived from satellite and model data.

---

## 🧠 Background

Glacial Lake Outburst Floods (GLOFs) are among the most catastrophic cryospheric hazards in the Himalayas, capable of releasing millions of cubic meters of water in hours.  
This research project combines **remote sensing**, **machine learning**, and **imputation-based feature reconstruction (MICE)** to forecast the relative hazard of glacial lakes across Nepal, Tibet, and adjacent regions.

---

## 🗺️ App Features

- **Interactive Map Viewer:**  
  Explore lakes colored by hazard probability — from green (low risk) to dark red (high risk).
- **Base Map Options:**  
  Switch between satellite, terrain, and light map tiles using the sidebar.
- **Clustered Lake Display:**  
  Smart clustering for smooth performance when viewing large datasets.
- **Lake Information Popups:**  
  Click any lake marker to view detailed attributes including:
  - Area (ha)
  - Elevation (m)
  - Glacier proximity
  - Expansion rates (5-year & 10-year)
  - Glacier contact type
  - Predicted Hazard Probability (0–1)
- **Model Integration:**  
  Probabilities generated using a tuned **Logistic Regression classifier** trained on imputed and balanced datasets.

---

## 🧩 Dataset Overview

The app visualizes data from `hazard_probabilities.csv`, containing 2,652 glacial lakes with the following attributes:

| Column | Description |
|---------|--------------|
| `Latitude`, `Longitude` | Lake coordinates |
| `Lake_area_calculated_ha` | Lake area in hectares |
| `Elevation_m` | Mean lake elevation (m) |
| `Lake_type_simplified` | Simplified lake classification (ice-contact, moraine-dammed, supraglacial, etc.) |
| `glacier_area_ha` | Source glacier area (ha) |
| `slope_glac_to_lake` | Down-glacier slope (°) |
| `nearest_glacier_dist_m` | Distance to nearest glacier (m) |
| `5y_expansion_rate`, `10y_expansion_rate` | Historical expansion rates |
| `GLOF` | Observed flood label (1 = GLOF event, 0 = none) |
| `Hazard_Prob` | ML-predicted GLOF probability (0–1) |

---

## ⚙️ Technologies Used

- **Python 3.10+**
- **Streamlit** – Web app framework  
- **Folium / Branca** – Interactive map rendering  
- **scikit-learn** – Logistic Regression model  
- **miceforest** – MICE-based imputation of missing data  
- **pandas / numpy** – Data wrangling and analysis  

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/nima-sherpa/GLOF_Hazard_Map_App.git
cd GLOF_Hazard_Map_App

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py

