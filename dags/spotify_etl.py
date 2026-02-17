"""Spotify ETL pipeline.

This module extracts recently played tracks from the Spotify Web API,
transforms the response into a tabular structure, validates the dataset,
and loads it into a local SQLite database.
"""

from __future__ import annotations

import datetime as dt
import os
import sqlite3
from typing import Any, Dict, List

import pandas as pd
import requests
import sqlalchemy

DATABASE_LOCATION = os.getenv("DATABASE_LOCATION", "sqlite:///my_played_tracks.sqlite")
SPOTIFY_TOKEN = os.getenv("SPOTIFY_TOKEN", "")
RECENTLY_PLAYED_ENDPOINT = "https://api.spotify.com/v1/me/player/recently-played"
TABLE_NAME = "my_played_tracks"


def build_auth_headers(token: str) -> Dict[str, str]:
    """Build standard headers required by Spotify Web API requests."""
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }


def get_yesterday_unix_ms(now: dt.datetime | None = None) -> int:
    """Return yesterday's timestamp in Unix milliseconds for Spotify filtering."""
    reference = now or dt.datetime.now()
    yesterday = reference - dt.timedelta(days=1)
    return int(yesterday.timestamp()) * 1000


def extract_recently_played(token: str, after_timestamp_ms: int) -> Dict[str, Any]:
    """Extract listening history from Spotify after the provided timestamp."""
    response = requests.get(
        f"{RECENTLY_PLAYED_ENDPOINT}?after={after_timestamp_ms}",
        headers=build_auth_headers(token),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def transform_to_dataframe(payload: Dict[str, Any]) -> pd.DataFrame:
    """Transform Spotify JSON payload into a normalized Pandas DataFrame."""
    records: List[Dict[str, str]] = []

    # Each item represents one played track event.
    for item in payload.get("items", []):
        records.append(
            {
                "song_name": item["track"]["name"],
                "artist_name": item["track"]["album"]["artists"][0]["name"],
                "played_at": item["played_at"],
                "timestamp": item["played_at"][0:10],
            }
        )

    return pd.DataFrame(records, columns=["song_name", "artist_name", "played_at", "timestamp"])


def validate_recent_tracks(df: pd.DataFrame, now: dt.datetime | None = None) -> bool:
    """Validate expected quality constraints before loading data."""
    # Pipeline can exit gracefully when there is no new data in the interval.
    if df.empty:
        print("No songs downloaded. Pipeline finished with no new data.")
        return False

    # `played_at` is the unique event key and cannot contain duplicates.
    if not pd.Series(df["played_at"]).is_unique:
        raise ValueError("Primary key validation failed: duplicate played_at values found.")

    # Prevent null data from entering the analytical table.
    if df.isnull().values.any():
        raise ValueError("Null values found in extracted data.")

    # Guarantee rows refer to yesterday's window only.
    reference = now or dt.datetime.now()
    yesterday = (reference - dt.timedelta(days=1)).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    for timestamp in df["timestamp"].tolist():
        if dt.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
            raise ValueError("At least one returned song is not from yesterday's date.")

    return True


def ensure_database_table(database_file: str, table_name: str = TABLE_NAME) -> None:
    """Create destination table if it does not exist."""
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name}(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()


def load_to_sqlite(df: pd.DataFrame, database_location: str = DATABASE_LOCATION, table_name: str = TABLE_NAME) -> None:
    """Load validated dataframe into SQLite using SQLAlchemy."""
    database_file = database_location.replace("sqlite:///", "")
    ensure_database_table(database_file, table_name)

    engine = sqlalchemy.create_engine(database_location)
    try:
        df.to_sql(table_name, engine, index=False, if_exists="append")
        print("Rows inserted successfully.")
    except Exception:
        print("Rows already exist in the database.")


def run_spotify_etl() -> None:
    """Run extract, transform, validate and load stages end-to-end."""
    token = SPOTIFY_TOKEN
    if not token:
        raise ValueError(
            "SPOTIFY_TOKEN is not set. Export a valid token with scope "
            "`user-read-recently-played` before running the pipeline."
        )

    # Extract stage.
    after_timestamp_ms = get_yesterday_unix_ms()
    payload = extract_recently_played(token=token, after_timestamp_ms=after_timestamp_ms)

    # Transform stage.
    tracks_df = transform_to_dataframe(payload)

    # Validation stage.
    if validate_recent_tracks(tracks_df):
        print("Data validated. Starting load stage.")

    # Load stage.
    load_to_sqlite(tracks_df)


if __name__ == "__main__":
    run_spotify_etl()
