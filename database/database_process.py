from typing import List, Callable

from database.models import User, Film, PersonalRating as PR


def _add_to_users_table(user_info: dict) -> None:
    """
    Creating the new row in the table. If the user is in the table, the function terminates
    :param user_info: dictionary with information about user
    :return: None
    """
    User.get_or_create(
        user_id=user_info["user_id"],
        first_name=user_info["first_name"],
        last_name=user_info["last_name"],
    )


def _add_to_films_table(film_info: dict) -> None:
    """
    Creating the new row in the table. If the film is in the table, the function terminates
    :param film_info: dictionary with information about film
    :return: None
    """
    Film.get_or_create(
        kp_id=film_info["kp_id"],
        title=film_info["title"],
        year=film_info["year"],
        genres=film_info["genres"],
        poster=film_info["poster"],
        description=film_info["description"],
    )


def _add_to_personal_rating(film_id: int, user_id: int, rating: int) -> None:
    """
    Creating the new row in the table. If the record is in the table, the function terminates
    :param film_id: film id
    :param user_id: user id
    :param rating: personal rating from 1 to 10
    :return: None
    """
    PR.get_or_create(
        film_id=film_id,
        user_id=user_id,
    )

    PR.update(
        rating=rating,
    ).where(PR.film_id == film_id, PR.user_id == user_id).execute()


def new_rating_entry(film_rating: int, film_info: dict, user_info: dict) -> None:
    """
    A function for creating a new record in tables. Adding a user, movie, rating.
    If the records are already present in the tables, only the rating in the Personal rating table is updated.
    :param film_rating: personal rating number
    :param film_info: dictionary with film information
    :param user_info: dictionary with user information
    :return: None
    """
    _add_to_users_table(user_info)
    _add_to_films_table(film_info)
    _add_to_personal_rating(film_id=Film.select().where(Film.title == film_info["title"]).get(),
                            user_id=user_info["user_id"], rating=film_rating)


def _to_full_info(films_dict: List[dict]) -> List[dict]:
    """
    Extracting full movie information from the table
    :param films_dict: film id and rating
    :return: list of the full information about the movies
    """
    result_list = []
    for film in films_dict:
        full_info = Film.select().where(Film.id == film["film_id"]).dicts()
        for row in full_info:
            row["rating"] = film["rating"]
            result_list.append(row)
    return result_list


def output_low_high_or_history_rating_films(user_id: int, sort_method: Callable, limit: int = 10) -> List[dict]:
    """
    Output of the added movies from the Personal rating table.
    Filters - with the highest rating, the lowest rating and history of the last 10 added films.
    :param user_id: user id
    :param sort_method: peewee sql method for sorting
    :param limit: limit on the number of movies to output
    :return: list of information about films in tables
    """
    films_dict = PR.select(PR.film_id, PR.rating).order_by(sort_method()).limit(limit).\
        where(PR.user_id == user_id).dicts()
    return _to_full_info([row for row in films_dict])


def output_custom_rating_films(user_id: int, lower: int, higher: int, limit: int) -> List[dict]:
    """
    Output of the added movies from the Personal rating table with a rating in a certain range.
    :param user_id: user id
    :param lower: lower level of the search range
    :param higher: higher level of the search range
    :param limit: limit on the number of movies to output
    :return: list of information about films in tables
    """
    lower, higher = min(lower, higher), max(lower, higher)
    films_dicts = PR.select(PR.film_id, PR.rating).where(PR.user_id == user_id, PR.rating.between(lower, higher)).\
        limit(limit).order_by(PR.rating.desc()).dicts()

    return _to_full_info([row for row in films_dicts])
