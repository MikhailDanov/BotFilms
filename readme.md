# <center>Personal Rating Bot</center>

---

## Description

---

Telegram bot for conducting your personal movie rating. Allows you to search by the name of the movie, 
add it and set the rating, as well as display information about the added movies. This bot is based on the 
API of the Russian service - Kinopoisk. Also, all commands are output in the bot in Russian. If desired, 
you can adapt it to English - you will only have to change the API and translate commands into English 
(Google translator to help), and add .env file for API-KEY and BOT-TOKEN.

---

## How to use

---

1. Install dependencies in your virtual environment
    ```
    pip install -r requirements.txt
    ```
2. Add a file.env to the root of the project, add an API key and a bot token to it
    ```
    BOT_TOKEN = "YourBotToken"
    X_API_KEY = "YourApiKey"
    ```
3. Launch the bot via a file main.py or directly through the terminal
    ```
    python main.py
    /
    python3 main.py
    ```
4. Start using

---

## Available commands

---

### Default commands:
    - /about - full information about the bot;
    - /help - help on bot commands;

### Film rating commands:
    - /add - add the nem film to your own selection;
    - /low - output of films with a minimum rating from your own selection (up to 10 films);
    - /high - output of films with a maximum rating from your own selection (also, up to 10 films);
    - /custom - entry with a custom range rating (up to 10 films);
    - /history — output from the history of user requests (the last 10 views).

---

## Database

---

All information about users and movies is stored in the database/database.db. To add new columns to the database table, 
you need to initially change the models in models.py, and fix adding information to database_process.py

---

## Links

[API from this project](https://kinopoiskapiunofficial.tech/profile)

