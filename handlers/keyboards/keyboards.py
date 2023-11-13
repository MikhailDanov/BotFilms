from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,\
    ReplyKeyboardMarkup, KeyboardButton

from config_data.config import ALL_COMMANDS


def commands_button():
    """
    Reply keyboard with all available commands.
    :return: ReplyKeyboardMarkup object
    """
    keyboard = ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    buttons = []

    for command in ALL_COMMANDS:
        buttons.append("/" + command[0])
    keyboard.add(*buttons)

    return keyboard


def digit_buttons():
    """
    Reply keyboard with digits from 1 to 10 and cancel button.
    :return: ReplyKeyboardMarkup object
    """
    keyboard = ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
    buttons = []

    for num in range(10):
        buttons.append(KeyboardButton(f"{num + 1}"))
    buttons.append(KeyboardButton("Отмена"))
    keyboard.add(*buttons)

    return keyboard


def cancel_button():
    """
    Reply keyboard with cancel button.
    :return: ReplyKeyboardMarkup object
    """
    return ReplyKeyboardMarkup(row_width=5, resize_keyboard=True).add(KeyboardButton("Отмена"))


def help_button():
    """
    Reply keyboard with help command button.
    :return: ReplyKeyboardMarkup object
    """
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("/help"))


def add_button(callback_data: str):
    """
    Reply keyboard with add command button.
    :return: ReplyKeyboardMarkup object
    """
    return InlineKeyboardMarkup().add(InlineKeyboardButton("Добавить", callback_data=callback_data))
