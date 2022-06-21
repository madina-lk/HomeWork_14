from classes.netflixDAO import DbNetflix
from config import DB_PATH
from flask import Blueprint, jsonify

netflix_blueprint = Blueprint('netflix_blueprint', __name__)            # Объявление блупринта
bd_connect = DbNetflix(DB_PATH)                                         # Задаем пути


@netflix_blueprint.route('/')
def main_page():
    """Метод для главной страницы вьюшки (не несет никакой смысловой нагрузки)"""
    return "Это главная страница!"


@netflix_blueprint.route('/movie/<title>')
def movie_page_by_title(title):
    """Метод для вьюшки получения списка фильмов по названию"""

    result = bd_connect.get_movie_by_title(title)
    return jsonify(result)


@netflix_blueprint.route('/movie/year/to/year/')
def movie_page_by_years():
    """Метод для вьюшки получения списка фильмов по временному промежутку"""

    result = bd_connect.get_movie_by_year(2020, 2022)
    return jsonify(result)


@netflix_blueprint.route('/genre/<genre>')
def movie_page_by_genre(genre):
    """Метод для вьюшки получения списка фильмов по жанру"""

    result = bd_connect.get_movie_by_genre(genre)
    return jsonify(result)


@netflix_blueprint.route('/rating/')
def movie_page_by_rating():
    """Метод для вьюшки получения списка фильмов всем возрастным группам"""
    result = bd_connect.get_movie_by_rating(bd_connect.rating_formation())
    return jsonify(result)


@netflix_blueprint.route('/rating/children/')
def movie_page_by_children_rating():
    """"""
    result = bd_connect.get_movie_by_rating("G")
    return jsonify(result)


@netflix_blueprint.route('/rating/family')
def movie_page_by_family_rating():
    """"""
    result = bd_connect.get_movie_by_rating(('G', 'PG', 'PG-13'))
    return jsonify(result)


@netflix_blueprint.route('/rating/adult')
def movie_page_by_adult_rating():
    """"""
    result = bd_connect.get_movie_by_rating(('R', 'NC-17'))
    return jsonify(result)

