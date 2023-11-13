from telebot.custom_filters import StateFilter, SimpleCustomFilter
from loader import bot


class CorrectRangeNumber(SimpleCustomFilter):
    """Class-filter for checking the correctness number of user input"""
    key = "is_correct_num"

    def __init__(self):
        super().__init__()

    def check(self, message):
        if not message.text.isdigit():
            return False
        return 1 <= int(message.text) <= 10


class IsCustomState(SimpleCustomFilter):
    """Class-filter for checking the user's state"""
    key = "is_custom_state"

    def __init__(self):
        super().__init__()

    def check(self, message):
        try:
            if bot.get_state(message.from_user.id).startswith("CustomStates"):
                return True
            return False
        except AttributeError:
            return False


def add_custom_filters():
    """Adding the filters to bot"""
    bot.add_custom_filter(CorrectRangeNumber())
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(IsCustomState())
