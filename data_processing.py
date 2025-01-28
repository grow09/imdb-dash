import pandas as pd
import pycountry
import time

def merge_movie_data():
    """Prepare datasets for analytics base."""
    start_time = time.time()

    # Load and filter title basics

    columns_to_load = ["tconst","originalTitle","titleType","startYear","runtimeMinutes","genres"]
    title_basics = pd.read_csv('assets/title.basics.csv', usecols=columns_to_load, engine='pyarrow')

    # Filter the DataFrame based on the `titleType` column
    title_basics_filtered = title_basics.query('titleType in ["movie", "tvSeries"]')

    print(f"time to load title basics: {time.time() - start_time:.2f} s")

    # Load and process IMDb movies
    imdb_movies = pd.read_csv('assets/imdb_movies.csv', usecols=['orig_title', 'overview', 'budget_x', 'revenue', 'country', 'genre', 'date_x'])
    imdb_movies['year_x'] = pd.to_datetime(imdb_movies['date_x'], errors='coerce').dt.year.astype(str)


    # Merge IMDb movies with filtered title basics
    merged_data = pd.merge(
        imdb_movies, title_basics_filtered,
        left_on=['orig_title', 'year_x'],
        right_on=['originalTitle', 'startYear'],
        how='left'
    )

    # Load title ratings and merge with existing data
    title_ratings = pd.read_csv('assets/title.ratings.csv')
    merged_data = pd.merge(
        merged_data, title_ratings,
        on='tconst',
        how='left'
    )

    # Remove duplicates based on 'tconst'
    merged_data = merged_data.drop_duplicates(subset='tconst')

    merged_data['year_x'] = pd.to_numeric(merged_data['year_x'], errors='coerce')

    # Example: Convert ISO-2 column to ISO-3
    merged_data['country_name'] = merged_data['country'].apply(iso2_to_country_name)

    # Drop rows where conversion failed (invalid ISO-2 codes)
    merged_data = merged_data.dropna(subset=['country_name'])
    merged_data = merged_data.dropna(subset=['titleType'])
    merged_data = merged_data.dropna(subset=['averageRating'])


    # Clean the genre column by splitting comma-separated genres and trimming whitespace
    merged_data['genre'] = merged_data['genre'].apply(
        lambda x: [genre.strip() for genre in x.split(',')] if isinstance(x, str) else (x if isinstance(x, list) else [])
    )

    # Drop rows with empty genres, if necessary
    merged_data = merged_data[merged_data['genre'].apply(lambda x: isinstance(x, list) and len(x) > 0)]

    print(f"time to run all: {time.time() - start_time:.2f} s")

    return merged_data


def iso2_to_country_name(iso2_code):
    try:
        return pycountry.countries.get(alpha_2=iso2_code).name
    except AttributeError:
        return None


if __name__ == "__main__":
    merged_data = merge_movie_data()

