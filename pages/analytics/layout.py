import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import datetime
from app import movie_data

all_genres = sorted(set(sum(movie_data['genre'], [])))

layout = html.Div([
    html.Div([
        # RangeSlider Container
        html.Div([
            html.Div([
                dcc.RangeSlider(
                    id='date-range-slider',
                    min=int(movie_data['year_x'].min()),
                    max=int(movie_data['year_x'].max()),
                    value=[int(movie_data['year_x'].min()), int(movie_data['year_x'].max())],
                    marks={
                        int(movie_data['year_x'].min()): str(movie_data['year_x'].min()),
                        int(movie_data['year_x'].max()): str(movie_data['year_x'].max())
                    },
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ], className="col-5"),
            html.Div([
                dcc.Dropdown(
                    id='genre-filter',
                    options=[{'label': genre, 'value': genre} for genre in all_genres],
                    value=[],
                    multi=True,
                    placeholder='Select genres',
                    style={"width": "100%"}
                )
            ], className="col-2"),
            html.Div([
                dcc.Dropdown(
                    id='type-filter',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': title_type, 'value': title_type} for title_type in sorted(movie_data['titleType'].unique())],
                    value='All',
                    multi=False,
                    placeholder='Select type',
                    style={"width": "100%"}
                )
            ], className="col-2"),
        ], className="row"),
        html.Div(style={"height": "20px"}),
    ]),
    html.Div([
            html.Div(
                dcc.Graph(id='rating-over-year', figure={}),  # Leave figure empty for dynamic updates
                style={"flex": "2"}
            )
        ], className="d-flex", style={"gap": "10px"})
])
