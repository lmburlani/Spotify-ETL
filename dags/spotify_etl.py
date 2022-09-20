import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3


DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "" # seu usuário do Spotify 
TOKEN = "" # Spotify API token

# Link para gerar tokein:  https://developer.spotify.com/console/get-recently-played/

def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Verifica se o dataframe está vazio
    if df.empty:
        print("Nenhuma música baixada. Encerrando execução")
        return False 

    # Verificação da key primária
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("A verificação da key primária foi violada")

    # Verificação de dados nulos
    if df.isnull().values.any():
        raise Exception("Valores nulos encontrados")

    # Verifique se as  datas/horas são da data de ontem
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception("Pelo menos uma das músicas devolvidas não tem data/hora de ontem")

    return True

if __name__ == "__main__":

    # Extração
 
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
    
    # Converte hora para Unix timestamp em milissegundos
      
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Baixe todas as músicas que você ouviu "depois de ontem"     
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extraindo apenas os bits de dados relevantes do JSON     
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        
    # Prepare um dicionário para transformá-lo em um DataFrame abaixo       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    
    # Validação
    if check_if_valid_data(song_df):
        print("Data valid, proceed to Load stage")

    # Carregamento

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")
