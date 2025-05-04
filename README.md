# ❄️ Road Icing Risk Prediction and Heat Cable Prioritization in Gwangjin-gu

This project aims to predict road icing risks in Gwangjin-gu (Seoul, South Korea) using weather, road structure, and accident data, and to prioritize road segments for heat cable installations to improve winter road safety.

## 📍 Background

In winter, icy roads can lead to serious traffic accidents. To prevent this, local governments often install heat cables or place salt boxes on high-risk road segments.  
This project was conducted as part of a public data competition hosted by **Gwangjin-gu District Office**, and focuses on:

- Identifying road segments with high icing risk
- Prioritizing heat cable installations based on data-driven insights

## 🧩 Data Sources

We collected and processed multiple datasets, including:

| Category         | Description                                                |
|------------------|------------------------------------------------------------|
| **Weather Data** | Daily temperature, precipitation, and humidity records     |
| **Road Structure** | Slope (%), number of lanes, road width, and elevation data |
| **Accident Data** | Road accidents involving freezing over the past 5 years   |
| **Infrastructure** | Existing heat cable installations, salt box locations     |

All data were filtered to include only roads within the **Gwangjin-gu** area.

## 🛠️ Preprocessing

- Calculated road center coordinates from shapefiles
- Computed slope using elevation and coordinate data
- Merged road data with accident and weather information
- Filtered and cleaned data to remove inconsistencies

## 🤖 Model Development

We used a classification model to predict the probability of icing incidents on each road segment.  
After testing several models (Logistic Regression, Random Forest, XGBoost), **Random Forest** was chosen for its balance of accuracy and interpretability.

### Features Used:
- Average winter temperature
- Road slope (%)
- Precipitation level
- Number of freezing-related accidents
- Nearby infrastructure (heat cables, salt boxes)

### Performance Metrics:
- Accuracy, Precision, Recall
- ROC AUC Score
- SHAP value interpretation for model explainability

## 📊 SHAP-Based Interpretation

To explain the model's predictions and improve trustworthiness, we applied **SHAP (SHapley Additive exPlanations)** to identify key contributing features per road segment.

- Road slope and temperature were the most influential factors
- Local explanations helped in selecting priority areas

## 🗺️ Visualization

Using `folium` and `geopandas`, we visualized the results:

- Heatmaps of high-risk road segments
- Map overlays of existing vs. recommended heat cable locations
- SHAP-based feature influence layers

## 🧩 Policy Recommendation

Based on the model and visualization:

- We proposed a **priority installation map** for heat cables
- Suggested optimized placement of salt boxes
- Offered risk grading (High / Medium / Low) for each segment

## 📌 Technologies Used

- **Python (pandas, scikit-learn, geopandas, folium, SHAP)**
- **Jupyter Notebook**
- **QGIS** for road shapefile processing
- **Public APIs** for weather and coordinate data

