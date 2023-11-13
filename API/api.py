import requests
import json

from typing import Optional, List
from requests import ConnectTimeout
from config_data.config import headers
from unicodedata import normalize


url = "https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword"


def movie_info(movie_name: str) -> Optional[List[dict]]:
    """
    The function for request to API server.
    Returns information about founded films, list of dictionaries.
    :param movie_name: title
    :return: list of dictionaries with film info
    """
    response = _search_movies(movie_name)
    if response:
        result = _info_processing(response, movie_name)
        return result
    return None


def _search_movies(movie_name: str) -> Optional[List[dict]]:
    """
    Request to API server. Returns json info about films or None.
    :param movie_name: title
    :return: list of dictionaries with full movie information
    """
    try:
        request = requests.get(url, headers=headers, params={"keyword": movie_name, "page": 1}, timeout=10)

        if request.status_code == requests.codes.ok:
            result = json.loads(request.text)
            return result.get("films", None)
        return None

    except ConnectTimeout:
        return None


def _info_processing(info: List[dict], title: str) -> List[dict]:
    """
    Information handler for filtering only the necessary information.
    :param info: full information about founded films
    :param title: movie name
    :return: filtered information, lisf of dictionaries
    """
    required_info = list()
    for film in info:
        data = {
            "kp_id": film.get('filmId', '-'),
            "title": film.get("nameRu", film.get("nameEn", None)),
            "year": film.get('year'.split('-')[0]),
            "genres": ', '.join([genre.get('genre', '-') for genre in film.get('genres', '-')]),
            "poster": film.get('posterUrl', '-'),
            "description": normalize("NFKC", film.get('description', '-'))
        }
        if data["title"] == title:
            return [data]
        required_info.append(data)
        if len(required_info) == 5:
            break

    return required_info
