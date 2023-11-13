from telebot.types import Message, CallbackQuery
from states.states import CustomStates
from loader import bot
from database.database_process import *
from handlers.keyboards.keyboards import digit_buttons, cancel_button, add_button, commands_button
from API.api import movie_info


@bot.message_handler(commands=["cancel"], is_custom_state=True)
@bot.message_handler(regexp=r"[Оо]тмена", is_custom_state=True)
def cancel_state(message: Message) -> None:
    """
    Handler function, cancels the action selected by the user.
    :param message: user's message (/cancel command or regexp "[Оо]тмена")
    :return: None
    """
    bot.send_message(message.from_user.id, "Хорошо, в другой раз. Чтобы продолжить, "
                                           "введите одну из доступных команд", reply_markup=commands_button())
    bot.delete_state(message.from_user.id)


@bot.message_handler(commands=["add"])
def add(message: Message) -> None:
    """
    Handler function, to add a new film to personal list
    :param message: user's message (/add command)
    :return: None
    """
    bot.set_state(message.from_user.id, CustomStates.add_film)
    bot.send_message(message.from_user.id, "Напишите название фильма", reply_markup=cancel_button())


@bot.message_handler(content_types=["text"], state=CustomStates.add_film)
def find_films_by_request(message: Message) -> None:
    """
    Handler function, related to the add function. Accepts the name of the movie as message.
    In var result records data about movies received from the movie_info function, or None, if films not found.
    A button for adding a movie is displayed under the movie information section (contains a unique id as callback)
    :param message: movie name
    :return: None
    """
    result = movie_info(message.text)

    with bot.retrieve_data(message.from_user.id) as data:
        data["films"] = result

    if not result:
        bot.send_message(message.from_user.id, "К сожалению мне не удалось найти фильм по вашему запросу. Возможно в "
                                               "названии ошибка. Попробуйте снова", reply_markup=cancel_button())
        return
    elif len(result) == 1:
        bot.send_message(message.from_user.id, "Кажется, нашел то, что вы искали")
    else:
        bot.send_message(message.from_user.id, "Нашлось несколько вариантов по вашему запросу. Если среди них есть "
                                               "нужный, нажмите на кнопку 'Добавить' под фильмом")
    for film in result:
        bot.send_photo(message.from_user.id, film["poster"])
        bot.send_message(message.from_user.id, f"<b>Название:</b> {film['title']}, {film['year']}\n"
                                               f"<b>Жанр(ы):</b> {film['genres']}\n"
                                               f"<b>Описание:</b> {film['description']}",
                         reply_markup=add_button(film["kp_id"]))


@bot.callback_query_handler(func=lambda call: True)
def get_rating(call: CallbackQuery) -> None:
    """
    The callback function of adding the new film to personal list. Tracks clicks on the Add button under the movie.
    :param call: film id
    :return: None
    """
    with bot.retrieve_data(call.from_user.id) as data:
        for film in data["films"]:
            if str(film["kp_id"]) == call.data:
                data["film_info"] = film

    bot.set_state(call.from_user.id, CustomStates.rating)
    bot.send_message(call.from_user.id, "Введите рейтинг", reply_markup=digit_buttons())


@bot.message_handler(state=CustomStates.rating, is_correct_num=True)
def adding_film_process(message: Message) -> None:
    """
    Movie adding process. Calls new_rating_entry function with film info, user info and film rating as parameters
    :param message: rating
    :return: None
    """
    user_info = {
        "user_id": message.from_user.id,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
    }
    with bot.retrieve_data(message.from_user.id) as data:
        new_rating_entry(film_rating=int(message.text), film_info=data["film_info"], user_info=user_info)
    bot.send_message(message.from_user.id, "Фильм добавлен. Чтобы продолжить, введите одну из доступных команд",
                     reply_markup=commands_button())
    bot.delete_state(message.from_user.id)


@bot.message_handler(commands=["high", "low"])
def high_rating_command(message: Message) -> None:
    """
    Handler function for displaying the movies from the personal list with the highest or lowest rating.
    Prompts the user to select the number of movies to output from 1 to 10
    :param message: commands /high or /low
    :return: None
    """
    bot.set_state(message.from_user.id, CustomStates.quantity, message.chat.id)
    with bot.retrieve_data(message.from_user.id) as data:
        data["func"] = output_low_high_or_history_rating_films
        data["command"] = message.text

    bot.send_message(message.from_user.id, "Сколько фильмов нужно вывести?", reply_markup=digit_buttons())


@bot.message_handler(state=CustomStates.quantity, is_correct_num=True)
def low_high_and_custom_commands_processing(message: Message) -> None:
    """
    Handler function for /low, /high and /custom commands.
    Accepts a number from 1 to 10 as the limit for the output of movies
    :param message: number from 1 to 10
    :return: None
    """
    with bot.retrieve_data(message.from_user.id) as data:
        if data["command"] == "/high":
            callback_database_request(data["func"], message.from_user.id, PR.rating.desc, int(message.text))
        elif data["command"] == "/low":
            callback_database_request(data["func"], message.from_user.id, PR.rating.asc, int(message.text))
        elif data["command"] == "/custom":
            callback_database_request(data["func"], message.from_user.id, data["low_limit"],
                                      data["high_limit"], int(message.text))
    bot.delete_state(message.from_user.id)


@bot.message_handler(commands=["history"])
def history_command(message: Message) -> None:
    """
    Handler function to display the 10 most recently added movies
    :param message: command /history
    :return: None
    """
    callback_database_request(output_low_high_or_history_rating_films, message.from_user.id, PR.id.desc)


@bot.message_handler(commands=["custom"])
def custom_rating_command(message: Message) -> None:
    """
    Handler function to display the added movies in a certain rating range
    :param message: command /custom
    :return: None
    """
    bot.set_state(message.from_user.id, CustomStates.low_rating, message.chat.id)
    bot.send_message(message.from_user.id, "Напишите нижний порог диапазона для поиска", reply_markup=digit_buttons())


@bot.message_handler(state=CustomStates.low_rating, is_correct_num=True)
def custom_input_high_limit(message: Message) -> None:
    """
    The second step of the Custom command, entering the lower rating value, records to the user's data
    :param message: number, low rating limit
    :return: None
    """
    with bot.retrieve_data(message.from_user.id) as data:
        data["low_limit"] = int(message.text)
        data["command"] = "/custom"
        data["func"] = output_custom_rating_films
    bot.set_state(message.from_user.id, CustomStates.high_rating, message.chat.id)
    bot.send_message(message.from_user.id, "Теперь напишите верхний порог")


@bot.message_handler(state=CustomStates.high_rating, is_correct_num=True)
def custom_input_low_limit(message: Message) -> None:
    """
    The third step of the Custom command, entering the higher rating value, records to the user's data
    :param message: number, high rating limit
    :return: None
    """
    bot.set_state(message.from_user.id, CustomStates.quantity)

    with bot.retrieve_data(message.from_user.id) as data:
        data["high_limit"] = int(message.text)

    bot.send_message(message.from_user.id, "Введите количество фильмов")


@bot.message_handler(is_custom_state=True, is_correct_num=False)
def wrong_limit(message: Message) -> None:
    """
    Checking input from the user. Is called if the text is not a number or is in the wrong range.
    :param message: user's input
    :return: None
    """
    bot.send_message(message.from_user.id, "Нужно число от 1 до 10, иначе я не смогу помочь.\n\n"
                                           "Если хотите отменить выбранное действие, нажмите <b>Отмена</b>")


def callback_database_request(func: Callable, user_id: int, *args) -> None:
    """
    Callback function. Called at the end of commands to output movies.
    :param func: function for processing the required information
    :param user_id: id
    :param args: some arguments for the function
    :return: None
    """
    response = func(user_id, *args)

    if not response:
        bot.send_message(user_id, "К сожалению я не нашел ни одного фильма...", reply_markup=commands_button())
    else:
        bot.send_message(user_id, "<b>Вот записи, который я нашел:</b>\n", reply_markup=commands_button())
        for film in response:
            bot.send_photo(user_id, film["poster"])
            bot.send_message(user_id, f"<b>Название:</b> {film['title']},\n"
                                      f"<b>Рейтинг:</b> {film['rating']}\n"
                                      f"<b>Жанр(ы):</b> {film['genres']}\n"
                                      f"<b>Описание:</b> {film['description']}",
                             reply_markup=commands_button())
