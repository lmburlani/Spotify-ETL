# Spotify ETL
Baixa suas tracks recentes do Spotify (últimas 24h) e salva em SQLite.

## Quick start
1. `export SPOTIFY_TOKEN="SEU_TOKEN"`
2. `pip install -r requirements.txt`
3. `python spotify_etl.py`

DB gerado: `my_played_tracks.sqlite` (tabela `my_played_tracks`)

Obs: token precisa do scope `user-read-recently-played`. Não comite tokens.
