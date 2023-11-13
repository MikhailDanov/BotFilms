from telebot.types import BotCommand
from config_data.config import ALL_COMMANDS


def set_bot_commands(bot):
    """Setting up a menu with all commands in the chatbot"""
    bot.set_my_commands(
        [BotCommand(*i) for i in ALL_COMMANDS]
    )
