from telebot.handler_backends import State, StatesGroup


class CustomStates(StatesGroup):
    """Custom states for correct processing of commands from the user"""
    low_rating = State()
    high_rating = State()
    quantity = State()
    add_film = State()
    rating = State()
