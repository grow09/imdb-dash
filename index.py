from dash import dcc, html
from dash.dependencies import Input, Output
from app import app  # Import the app instance from app.py
import os

from pages.map.layout import layout as map_layout
import pages.map.callbacks

from pages.home.layout import layout as home_layout
import pages.home.callbacks

from pages.analytics.layout import layout as analytics_layout
import pages.analytics.callbacks

import dash_bootstrap_components as dbc

pages_dir = 'pages'
pages = sorted([name for name in os.listdir(pages_dir) if os.path.isdir(os.path.join(pages_dir, name)) and name != 'home'])

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink("Home", href="/", className="text-light", style={'fontSize': '1.2rem', 'marginRight': '1.5rem'})),
                                *[dbc.NavItem(dbc.NavLink(name.capitalize(), href=f"/{name}/", className="text-light", style={'fontSize': '1.2rem', 'marginRight': '1.5rem'})) for name in pages],
                            ],
                            className='ml-auto',
                            navbar=True
                        ),
                        className="col"
                    ),
                    dbc.Col(
                        dbc.NavbarBrand("IMDB Ratings", href="/"),
                        className="col-auto"
                    ),
                ],
                align="center",
                className="w-100"
            ),
        ],
        fluid=True,
        className="p-3"
    ),
    color="dark",
    dark=True,
    sticky="top",
    expand="md"
)

# Define the layout with dynamic URL routing
app.layout = html.Div([
    navbar,
    html.Div(style={"height": "25px"}),
    dcc.Location(id='url', refresh=False),  # Tracks the URL
    html.Div(id='page-content')  
])

# Callback to update the page content based on the URL
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home_layout
    elif pathname == '/map/':
        return map_layout
    elif pathname == '/analytics/':
        return analytics_layout
    else:
        return html.H1("404: Page not found", style={"textAlign": "center"})  # Handle unknown paths

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

