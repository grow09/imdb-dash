import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import datetime
import os

pages_dir = 'pages'
pages = sorted([name for name in os.listdir(pages_dir) if os.path.isdir(os.path.join(pages_dir, name)) and name != 'home'])
print(pages)


layout = html.Div([
    html.Div(style={'height': '50px'}),
    html.Div([
        html.A([
            html.Div([
                html.H3(name.capitalize(), className="card-header", style={'text-align': 'center', 'font-weight': 'bold'}),
                html.Img(src=f"assets/{name}_preview.png", className="card-img-top")
            ], className="card mx-auto", style={'width': '25rem', 'margin': '10px'})
        ], href=f"/{name}/") for name in pages
    ], className="d-flex justify-content-around")
])


