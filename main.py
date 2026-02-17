"""Command-line entrypoint for the Spotify ETL pipeline."""

from dags.spotify_etl import run_spotify_etl


if __name__ == "__main__":
    run_spotify_etl()
