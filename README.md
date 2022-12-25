# Spotify ETL

Este script é uma implementação de um pipeline de extração, transformação e carregamento (ETL, do inglês Extract, Transform, Load) para a plataforma de streaming de música Spotify. Ele permite ao usuário baixar os dados de músicas ouvidas pelo usuário nas últimas 24 horas e armazená-los em um banco de dados SQLite para análise posterior.

Para utilizar esse script, é necessário ter uma conta no Spotify e obter as credenciais de autenticação necessárias para acessar a API do Spotify. Além disso, é preciso ter instalado em sua máquina as bibliotecas Python sqlalchemy, pandas, requests e sqlite3.

O script é dividido em três partes principais: extração, transformação e carregamento. A extração consiste em baixar os dados de músicas ouvidas pelo usuário nas últimas 24 horas através da API do Spotify. A transformação consiste em limpar e validar esses dados, garantindo que estão no formato correto e prontos para serem armazenados no banco de dados. O carregamento consiste em armazenar esses dados limpos e validados em uma tabela do banco de dados SQLite.

API usada: https://developer.spotify.com/console/get-recently-played/
