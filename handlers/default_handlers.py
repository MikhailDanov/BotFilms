from telebot.types import Message

from loader import bot
from config_data.config import ALL_COMMANDS
from handlers.keyboards.keyboards import commands_button, help_button


@bot.message_handler(regexp=r"[Пп]ривет[!]?")
@bot.message_handler(commands=["start", "привет", "hello", "hello-world"])
def greeting(message: Message) -> None:
    """
    Handler function to processing the start command and regexp with greetings.
    :param message: message from user
    :return: None
    """
    bot.send_message(message.chat.id, f"Привет, {message.from_user.full_name}!\nЯ бот, созданный для ведения личного "
                                      f"рейтинга просмотренных фильмов.\n\n<b>Чтобы просмотреть доступные команды, "
                                      f"введите команду</b> /help", reply_markup=help_button())


@bot.message_handler(commands=['help'])
def available_commands(message: Message) -> None:
    """
    Handler function to processing the help command. Output the all available commands.
    :param message: message from user
    :return: None
    """
    commands = '\n'.join([f"/{full_command[0]} - {full_command[1]}" for full_command in ALL_COMMANDS])
    bot.send_message(message.chat.id, f"<b>Доступные команды:</b>\n{commands}", reply_markup=commands_button())


@bot.message_handler(commands=['about'])
def info_about(message: Message) -> None:
    """
    Handler function for processing the about command. Output the info about the bot
    :param message: message from user
    :return: None
    """
    bot.send_message(message.chat.id, "Данный бот предоставляет возможность ведения своего личного кино-рейтинга.\n\n"
                                      "<b>Возможности:</b>\n1. Добавить фильм в свою подборку и установить свой "
                                      "рейтинг,\n2. Вывести фильмы из личной подборки по рейтингу: лучшие, худшие и "
                                      "в определенном диапазоне рейтинга\n3. Вывести историю последних 10 просмотренных"
                                      " фильмов.", reply_markup=commands_button())


@bot.message_handler()
def unknown_command(message: Message) -> None:
    """
    Handler for all messages that are not in the list of available commands
    :param message: some message from user
    :return: None
    """
    bot.send_message(message.from_user.id,
                     "На такое я не смогу ответить, выберите одну из доступных команд, чтобы продолжить",
                     reply_markup=commands_button())
