# Spotify ETL
Este projeto é um pipeline que baixa os dados do Spotify de quais músicas foram ouvidas pelo usuário nas últimas 24 horas e armazena esses dados em um banco de dados SQLite. Esse pipeline é executado diariamente, permitindo ao usuário ter um histórico das músicas ouvidas ao longo do tempo.

Para utilizar esse projeto, é necessário ter uma conta no Spotify e obter as credenciais de autenticação necessárias para acessar a API do Spotify. Além disso, é preciso ter instalado em sua máquina as seguintes bibliotecas Python:

    spotipy
    sqlite3
    schedule (para agendar a execução diária do pipeline)

API usada: https://developer.spotify.com/console/get-recently-played/
