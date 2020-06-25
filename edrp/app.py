import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

load_dotenv()

earthquakes = pd.read_csv('edrp/data/clean_dataset.csv', header=0)
px.set_mapbox_access_token(os.getenv('MAPBOX_ACCESS_TOKEN'))

# Defaults are the center of the contiguous US
default_latitude = 39.8283
default_longitude = -98.5795

# Generate the default map
scattermap = px.scatter_mapbox(
    center={ 'lat': default_latitude, 'lon': default_longitude },
    color=earthquakes.magnitude,
    data_frame=earthquakes,
    height=750, 
    lat=earthquakes.latitude, 
    lon=earthquakes.longitude,
    # Setting the size & opacity like this allows the larger earthquakes to stand out on the map
    opacity=earthquakes.magnitude / 10,
    size=earthquakes.magnitude ** 5,
    size_max=25,
    zoom=3)

stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/flatly/bootstrap.min.css']
app = dash.Dash(__name__, external_stylesheets=stylesheets)
app.layout = html.Div(children=[
    html.H1(children='Earthquake Damage Risk Predictor'),

    html.Form(children=[
        dcc.Input(
            id='input_latitude',
            persistence_type='session',
            placeholder=default_latitude,
            type='number'
        ),
        dcc.Input(
            id='input_longitude',
            persistence_type='session',
            placeholder=default_longitude,
            type='number'
        ),
        html.Button(
            children='Submit',
            id='submit_location',
            # Setting the button's type to 'button' prevents the page from being reloaded when it is pressed
            type='button'
        )
    ]),

    dcc.Graph(
        id='local_scattermap',
        figure=scattermap
    )
])

@app.callback(Output('local_scattermap', 'figure'), [Input('submit_location', 'n_clicks')], [State('input_latitude', 'value'), State('input_longitude', 'value')])
def update_map_target(n_clicks, latitude, longitude):
    # This callback will fire when the page loads. We don't want to update the map until the button is actually clicked
    if n_clicks is not None:
        scattermap.update_layout(mapbox_center={ 'lat': latitude, 'lon': longitude }, mapbox_zoom=6)
    return scattermap

if __name__ == '__main__':
    app.run_server(debug=True)