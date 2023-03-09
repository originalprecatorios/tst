<p align="center">
</p>

<h1 align="center">
	<img src="https://www.python.org/static/community_logos/python-logo-inkscape.svg"  alt="Logo"  width="240"><br><br>
    Robô TST - Robot TST;
</h1>

<div>
    <p align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/static/v1?label=Language&message=Python&color=blue&style=for-the-badge&logo=Python" alt="Language: Python">
    </a>
    <a href="https://www.mongodb.com/home">
        <img src="https://img.shields.io/static/v1?label=Language&message=MongoDB&color=gree&style=for-the-badge&logo=MongoDB" alt="Language: MongoDB">
    </a>
    </p>
</div>

## Table of Contents

<p align="center">
 <a href="#about">About</a> •
 <a href="#features">Features</a> •
 <a href="#description">Description</a> •
 <a href="#revised-concepts">Revised Concepts</a> • 
 <a href="#installation">Installation</a> • 
 <a href="#getting-started">Get Started</a> • 
 <a href="#technologies">Technologies</a> • 
</p>

## 📌About

<div>
    <p align="center">
    <em>
        - Construção de um robô que captura informação do sistema TST
        - Construction of a robot that captures information from the TST system
    </em>
    </p>
</div>

## 🚀Features

- Manipulação do google,captura automatica de dados.
- Google manipulation, automatic data capture.

## Description

- Esse sistema consiste em entrar no site do TST, utilizando requests ele realiza a captura dos processos pelo número do cnpj da empresa. Após a captura dos processos ele captura as indformações e armazena no banco de dados. Os processos estão disponiveis no sistema da B7.
- This system consists of entering the TST website, using requests, it captures the processes by the company's cnpj number. After capturing the processes, it captures the information and stores it in the database. The processes are available on the B7 system.

## 👓Revised Concepts

- Requests
- Pymongo

## 📕Installation

**You must have already installed**
- [Python3](https://www.python.org/)
- [Pip](https://pip.pypa.io/en/stable/installation/)

**Recommendations**
- Eu recomendo usar o VSCode como IDE de desenvolvimento
- I recommend using VSCode as a development IDE


**Let's divide it into 3 steps.**
1. Clone this repository - Clonar este repositório
2. Install dependencies - Instale as dependênciass
3. Create environment variable - Criar variavel de ambiente
4. Download and configure chromedriver and geckodriver - Baixar e configurar chromedriver e geckodriver
5. Create .env file with the necessary environment variables - Criar arquivo .env com as variaveis de ambiente necessárias
  ---
### 1. Clone this repository
```
git clone https://github.com/originalprecatorios/tst.git
```
---
### 2. Install the dependencies
```
pip install -r /path/to/requirements.txt
```
---

### 3. Create environment variable

open the terminal
type export variablename="variablevalue"

abra o terminal
digite export nomedavariavel="valordavariavel"


MONGO
```
MONGO_HOST_PROD="000.000.000.000"
MONGO_PORT_PROD=27017
MONGO_USER_PROD="user"
MONGO_PASS_PROD="password"
MONGO_AUTH_DB_PROD="admin"
MONGO_DB_PROD='database'
AMBIENTE_PROD='admin'
```

CERTIFICADO
```
CERTIFICADO_ID="user"
CERTIFICADO_SENHA="password"
CERTIFICADO_SENHA_15="password"
```

CAPTCHA
```
CAPTCHA="key"
```

### 4. Download and configure chromedriver and geckodriver
```
Download chromedriver geckodriver as per installed version of both browsers - 
Fazer o download do geckodriver chromedriver conforme a verção instalada de ambos os navegadores 
https://chromedriver.chromium.org/downloads
https://github.com/mozilla/geckodriver/releases
```

```
Extract and copy the files to the /usr/local/bin/ folder -
Extrair e copiar os arquivos para a pasta /usr/local/bin/
```
---

### 5. Create .env file with the necessary environment variables
```
In the project folder create an .env file and add the following data: - 
Na pasta do projeto criar um arquivo .env e adicionar os seguintes dados: 

MONGO_HOST_PROD="host"
MONGO_PORT_PROD=27017
MONGO_USER_PROD="user"
MONGO_PASS_PROD="password"
MONGO_AUTH_DB_PROD="admin"
MONGO_DB_PROD='monitora'

#AMBIENTE
AMBIENTE_PROD="original"

CERTIFICADO_ID="user"
CERTIFICADO_SENHA="password"
CERTIFICADO_SENHA_15="password"

CAPTCHA="key"

```
---

## 🎮Getting Started

1. Open vscode or terminal - Abra o vscode ou terminal

2. start debugging in main.py file - iniciar a depuração no arquivo main.py

## 🌐Technologies

<p align="center">

- [Python](https://www.python.org/)
- [MongoDB](https://www.mongodb.com/home)
