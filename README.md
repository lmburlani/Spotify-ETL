# Spotify ETL

A compact ETL project that collects your recently played Spotify tracks (last 24 hours), validates data quality, and stores the result in a local SQLite database.

## Project Goal

This repository is useful when you want a simple but production-minded data pipeline example with:

- clear ETL stage separation (extract, transform, validate, load)
- reusable Python functions instead of one large script
- optional orchestration through Apache Airflow

## Repository Structure

- `dags/spotify_etl.py`: ETL business logic and reusable functions.
- `dags/spotify_dag.py`: Airflow DAG that schedules `run_spotify_etl` daily.
- `main.py`: local command-line entrypoint to run the pipeline without Airflow.
- `requirements.txt`: Python dependencies.

## ETL Flow

### 1) Extract

The pipeline calls Spotify's endpoint:

`GET https://api.spotify.com/v1/me/player/recently-played?after=<timestamp_ms>`

`after` is generated as "current time minus 24h" in Unix milliseconds.

### 2) Transform

The JSON response is normalized into a DataFrame with these columns:

- `song_name`
- `artist_name`
- `played_at` (ISO datetime from Spotify)
- `timestamp` (date portion used for quality checks)

### 3) Validate

Before loading, the pipeline enforces:

- dataset is not empty (otherwise it exits gracefully)
- `played_at` values are unique (primary key behavior)
- no null values in any column
- all rows belong to yesterday's date window

### 4) Load

Validated records are appended into SQLite table `my_played_tracks`.

If the table does not exist, it is created automatically with `played_at` as primary key.

## Spotify API Credentials Setup

### Required scope

Your token must include:

- `user-read-recently-played`

### Create and export token

1. Generate a token in the Spotify Web API console for the required scope.
2. Export it in your terminal:

```bash
export SPOTIFY_TOKEN="your_spotify_token_here"
```

Optional: customize database location (defaults to `sqlite:///my_played_tracks.sqlite`):

```bash
export DATABASE_LOCATION="sqlite:///my_played_tracks.sqlite"
```

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

After execution, the SQLite database file is created in the project root (unless `DATABASE_LOCATION` is changed).

## Run with Airflow

When using Airflow, place this repository (or at least the files inside `dags/`) in your Airflow DAGs folder.

The DAG id is `spotify_dag` and it runs once per day.

## Notes

- Do not commit real Spotify tokens.
- Spotify tokens can expire; regenerate as needed.
- If no songs were played in the selected window, the pipeline finishes without inserting rows.
