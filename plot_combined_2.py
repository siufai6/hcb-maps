import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Load the GeoJSON file
# Replace 'your_geojson_file.geojson' with the actual path to your file
with open('./lsoa 2021/LSOA_2021_EW_BSC_V4.geojson', 'r') as f:
    lsoa_geojson = json.load(f)

# 2. Load the CSV data
# Replace 'your_data_file.csv' with the actual path to your CSV file
# Make sure your CSV has a column with LSOA codes (e.g., 'LSOA11CD')
# and a column with the data you want to plot (e.g., 'Value').
df = pd.read_csv('./combined_lsoa_data_cleaned_2.csv')

# Ensure LSOA11CD is a string
df['LSOA21CD'] = df['LSOA21CD'].astype(str)

# 3. Create a dictionary mapping LSOA codes to names
lsoa_name_mapping = {
    feature['properties']['LSOA21CD']: feature['properties']['LSOA21NM']
    for feature in lsoa_geojson['features']
}

# 4. Add LSOA names to the DataFrame
df['LSOA_Name'] = df['LSOA21CD'].map(lsoa_name_mapping)
df['LSOA_Name'] = df['LSOA_Name'].fillna('Name Not Available')

# 5. Define the measures you want to display
measures = ['dpi_normalized', 'Pct of population speaks no or little English normalized', 'Pct umemp or econo inactive normalized','Pct household deprivation normalized','score']  # Replace with your actual column names

# 6. Create the figure with subplots (if needed)
fig = go.Figure()

# 7. Add Choropleth traces for each measure
for measure in measures:
    
    fig.add_trace(go.Choropleth(
        geojson=lsoa_geojson,
        locations=df['LSOA21CD'],
        z=df[measure],  # Use the current measure for the color
        featureidkey='properties.LSOA21CD',
        colorscale="Viridis",
        visible=False,  # Initially hide all traces
        hovertemplate='<b>%{properties.LSOA21NM}</b><br>' +  # LSOA Name
                      f'{measure}: %{{z}}<extra></extra>',  # Measure Value
        name=measure  # Name for the legend/menu
    ))

# Make the first trace visible by default
fig.data[0].visible = True

# 8. Update layout for mapbox
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=6,
    mapbox_center={"lat": 53, "lon": -1},
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

# 9. Create the dropdown menu
fig.update_layout(
    updatemenus=[
        {
            'buttons': [
                {
                    'label': measure,
                    'method': 'update',
                    'args': [
                        {'visible': [m == measure for m in measures]}
                    ]
                } for measure in measures
            ],
            'direction': 'down',
            'pad': {'r': 10, 't': 10},
            'showactive': True,
            'x': 0.1,
            'xanchor': 'left',
            'y': 1.1,
            'yanchor': 'top'
        },
    ]
)

# Add title
fig.update_layout(
    title_text='LSOA Measures',
    title_x=0.5
)

#fig.show()

fig.write_html("lsoa_map.html")