import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import datetime
from app import app, movie_data



@app.callback(
    Output('rating-over-year', 'figure'),
    [Input('date-range-slider', 'value'),
     Input('genre-filter', 'value'),
     Input('type-filter', 'value')
     ]
)

def update_world_map(year_range, selected_genres, selected_type):
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

    # Sort data by year
    filtered_data = filtered_data.sort_values(by='year_x')

    # Calculate average rating by year
    rating_over_year = filtered_data.groupby('year_x')['averageRating'].mean().reset_index()

    # Timeline plot
    rating_over_years = go.Figure()

    # Add line trace for "Time to Open"
    rating_over_years.add_trace(go.Scatter(
        x=rating_over_year['year_x'],
        y=rating_over_year['averageRating'],
        mode='lines+markers',  # Add markers for each data point
        name='Time to open lootbox',
        line=dict(
            color='#6AB187',  # Line color
            width=3,  # Line width
            dash='solid'  # Solid line style
        ),
        marker=dict(
            color='#6AB187',  # Marker color
            size=5,  # Marker size
            line=dict(
                color='white',  # Marker border color
                width=1  # Marker border width
            )
        )
    ))

    # Update layout with refined styling and removed empty space
    rating_over_years.update_layout(
        title='Time from Activation to Opening Lootbox',
        title_x=0.5,  # Center the title
        title_font=dict(size=18, color='rgb(34, 34, 34)', family='Arial'),  # Title font style
        xaxis_title='Year',  # X-axis title updated to reflect "Year"
        yaxis_title='Average rating',
        xaxis=dict(
            tickmode='array',  # Custom ticks
            tickvals=list(range(rating_over_year['year_x'].min(), rating_over_year['year_x'].max()+1))[::2],  # Display all years
            tickangle=-45,  # Rotate tick labels for better readability
            ticks='',  # Move ticks outside the axis
            tickwidth=2,
            ticklen=8
        ),
        yaxis=dict(
            gridcolor='rgba(204, 204, 204, 0.5)',  # Lighter grid lines
            zeroline=False,  # Remove zero line
            showline=True,  # Show axis line
            showgrid=True  # Show grid lines
        ),
        plot_bgcolor='rgb(245, 245, 245)',  # Light gray background
        paper_bgcolor='white',  # White background for the paper
        hovermode='closest',  # Display closest hover info
        margin=dict(l=20, r=20, t=40, b=40),  # Reduced margins to eliminate empty space
        height=500  # Increased height for better readability
    )


    return rating_over_years



