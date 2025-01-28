from dash import Dash
import dash_bootstrap_components as dbc
from data_processing import merge_movie_data


# Initialize Dash app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

movie_data = merge_movie_data()

server = app.server  # Required for deployment
