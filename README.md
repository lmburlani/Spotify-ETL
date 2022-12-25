# Spotify ETL
Este projeto é um pipeline que baixa os dados do Spotify de quais músicas foram ouvidas pelo usuário nas últimas 24 horas e armazena esses dados em um banco de dados SQLite. Esse pipeline é executado diariamente, permitindo ao usuário ter um histórico das músicas ouvidas ao longo do tempo.

Para utilizar esse projeto, é necessário ter uma conta no Spotify e obter as credenciais de autenticação necessárias para acessar a API do Spotify. Além disso, é preciso ter instalado em sua máquina as seguintes bibliotecas Python:

    spotipy
    sqlite3
    schedule (para agendar a execução diária do pipeline)

O projeto consiste em dois arquivos principais:

    O arquivo "spotify_pipeline.py" contém o código do pipeline em si. Ele se conecta à API do Spotify, baixa os dados de músicas ouvidas nas últimas 24 horas e armazena esses dados em um banco de dados SQLite.

    O arquivo "schedule.py" é responsável por agendar a execução do pipeline de forma diária. Ele importa o código do arquivo "spotify_pipeline.py" e usa a biblioteca schedule para agendar a execução desse código a cada 24 horas.

Para iniciar o pipeline, basta executar o arquivo "schedule.py". Isso fará com que o pipeline seja executado todos os dias às 00h00 (horário de sua máquina). O banco de dados SQLite será criado automaticamente e os dados de músicas ouvidas serão armazenados nele a cada execução do pipeline.

Espero que esse projeto seja útil para você! Qualquer dúvida ou sugestão, não hesite em entrar em contato.

API usada: https://developer.spotify.com/console/get-recently-played/
