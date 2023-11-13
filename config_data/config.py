import os
from dotenv import find_dotenv, load_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены, отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
headers = {
    "X-API-KEY": os.getenv("X_API_KEY"),
}


DEFAULT_COMMANDS = (
    ("help", "Справка"),
    ("about", "Информация о боте"),
)

CUSTOM_COMMANDS = (
    ("add", "Добавить новый фильм в свою подборку"),
    ("high", "Вывести фильмы из личного списка с самым высоким рейтингом"),
    ("low", "Вывести фильмы из личного списка с самым низким рейтингом"),
    ("custom", "Вывести фильмы в выбранном диапазоне рейтинга"),
    ("history", "История последних 10 просмотренных фильмов"),
)

ALL_COMMANDS = CUSTOM_COMMANDS + DEFAULT_COMMANDS

DB_PATH = "database/database.db"
