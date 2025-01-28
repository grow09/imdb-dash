import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import datetime
from app import app, movie_data



@app.callback(
    Output('world-map', 'figure'),
    [Input('date-range-slider', 'value'),
     Input('genre-filter', 'value'),
     Input('type-filter', 'value'),
     Input('rating-toggle', 'value')]
)

def update_world_map(year_range, selected_genres, selected_type,rating_type):
    # Filter by selected years
    filtered_data = movie_data[(movie_data['year_x'] >= year_range[0]) & (movie_data['year_x'] <= year_range[1])]
    
    # Explode genres into separate rows
    filtered_data = filtered_data.explode('genre')
    
    # Filter by selected genres
    if selected_genres:
        filtered_data = filtered_data[
            filtered_data['genre'].apply(
                lambda genres: any(genre in genres for genre in selected_genres)
            )
        ]
    
    # Filter by selected types
    if selected_type and selected_type != 'All':
        filtered_data = filtered_data[filtered_data['titleType'] == selected_type]


    # Handle rating calculation based on toggle
    if rating_type == 'average':
        # Calculate average rating by country
        country_rating = filtered_data.groupby('country_name')['averageRating'].mean().reset_index()
        top_title = filtered_data.loc[
            filtered_data.groupby('country_name')['averageRating'].idxmax()
        ].groupby('country_name')['originalTitle'].first().reset_index()    
    
    elif rating_type == 'top':
        # Find top rating by country (maximum rating)
        country_rating = filtered_data.groupby('country_name')['averageRating'].max().reset_index()
        top_title = filtered_data.loc[
            filtered_data.groupby('country_name')['averageRating'].idxmax()
        ].groupby('country_name')['originalTitle'].first().reset_index()



    # Build map
    world_map = go.Figure(data=[go.Choropleth(
        locations=country_rating['country_name'],  # Country names may not match ISO-3 codes used in the map
        locationmode='country names',
        z=country_rating['averageRating'],
        text=country_rating['country_name'],  # Use only country names for hover
        colorscale='Sunset',
        autocolorscale=False,
        reversescale=False,
        marker=go.choropleth.Marker(
            line=dict(
                color='darkgray',
                width=1
            )
        ),
        colorbar=go.choropleth.ColorBar(
            title=''  # Removed title as full rating is in text
        ),
        customdata=top_title['originalTitle'],
        hovertemplate='<b>%{text}</b><br>Avg Rating: %{z:.2f}<br>Top Title: %{customdata}<extra></extra>'
    )])

    world_map.update_layout(
        title='Average Rating by Country',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        height=800,
        margin=dict(l=0, r=0, t=100, b=0)
    )

    return world_map



