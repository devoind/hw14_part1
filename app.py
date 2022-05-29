from flask import Flask, jsonify
from utils import *

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False


@app.route('/movie/<title>')
def get_by_title(title):
    """
    Вьюшка для маршрута /movie/<title>

    :param title: получает данные про фильм
    :return: возвращает данные про фильм
    """
    return movies_by_title(title)


@app.route('/movie/<int:year1>/to/<int:year2>')
def get_by_year_to_year(year1, year2):
    """
    Вьюшка для маршрута /movie/year/to/year, которая выводит список словарей

    :return: возвращает список словарей
    """
    return jsonify(movies_by_to_years(year1, year2))


@app.route('/rating/<category>')
def get_by_rating(category):
    """
    Вьюшка, которая обрабатывает несколько маршрутов в соответствии с определенными группами

    :param category: получает категорию
    :return: возвращает список словарей в соответствии с категорией
    """
    return jsonify(movies_by_rating(category))


@app.route('/genre/<genre>')
def get_by_genre(genre):
    """
    Вьюшка /genre/<genre>, которая возвращает 10 самых свежих фильмов в формате json

    :param genre: получает жанр
    :return: возвращает 10 самых свежих фильмов в формате json
    """
    return jsonify(movies_by_genre(genre))


if __name__ == "__main__":
    app.run(debug=True)
