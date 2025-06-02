import pandas as pd
import folium
from folium.plugins import HeatMap

file_path = 'C:/Users/Pracheer/Desktop/Earthquake Prediction/earthquake_dataset.csv'
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    raise FileNotFoundError(f"The file at {file_path} was not found. Please check the path.")


required_columns = ['latitude', 'longitude', 'magnitudo', 'place', 'date']
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise KeyError(f"Missing required column(s): {', '.join(missing_columns)}")


significant_quakes = data[data['magnitudo'] >= 5.0].nlargest(100, 'magnitudo')


quake_map = folium.Map(
    location=[20, 0],
    zoom_start=2,
    tiles='OpenStreetMap'  
)


heat_data = significant_quakes[['latitude', 'longitude', 'magnitudo']].values.tolist()

# Add heatmap layer
HeatMap(heat_data, radius=10).add_to(quake_map)


for _, quake in significant_quakes.iterrows():
    popup_info = (
        f"<b>Location:</b> {quake['place']}<br>"
        f"<b>Date:</b> {quake['date']}<br>"
        f"<b>Magnitude:</b> {quake['magnitudo']}"
    )
    folium.Marker(
        location=[quake['latitude'], quake['longitude']],
        popup=folium.Popup(popup_info, max_width=250),
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(quake_map)


output_path = "earthquake_risk_map.html"
try:
    quake_map.save(output_path)
    print(f"Map saved as {output_path}")
except Exception as e:
    raise RuntimeError(f"An error occurred while saving the map: {e}")
