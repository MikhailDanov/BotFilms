from loader import bot
from utils.set_bot_commands import set_bot_commands
import handlers
from states.filters import add_custom_filters


if __name__ == '__main__':
    add_custom_filters()

    bot.message_handler(func=handlers)

    set_bot_commands(bot)
    bot.infinity_polling()
