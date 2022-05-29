import sqlite3
from collections import Counter


class DbConnect:
    def __init__(self, path):
        """
        Функция создания экземпляра класса

        :param path: возвращает объект
        """
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        """
        Функция удаления и отключение базы данных

        :return: ничего не возвращает
        """
        self.cur.close()
        self.con.close()


def execute_query(query):
    """
    Функция создания объекта запроса к БД

    :param query: принимает поля объекта
    :return: возвращает объект запроса
    """
    with sqlite3.connect('netflix.db') as con:
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
    return result


def movies_by_title(title):
    """
    Функция, которая производит поиск по введенному title БД

    :param title: получает введенный title
    :return: возвращает информацию о фильме с БД в соответствии с указанным title
    """
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title LIKE '%{title}%'
            ORDER BY release_year DESC limit 1""")
    result = db_connect.cur.fetchone()

    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def movies_by_to_years(year_one, year_two):
    """
    Функция поиска по диапазону лет выпуска

    :param year_one: получает первую дату - левая граница
    :param year_two: получает последнюю дату - правая граница
    :return: возвращает список фильмов с ограничением в 100 тайтлов
    """
    db_connect = DbConnect('netflix.db')
    query = f"""SELECT title, release_year
                FROM netflix
                WHERE release_year BETWEEN {year_one} AND {year_two} LIMIT 100"""

    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []

    for movie in result:
        result_list.append({"title": movie[0],
                            "release_year": movie[1]})

    return result_list


def movies_by_rating(rating):
    """
    Функция поиска по рейтингу

    :param rating: получает рейтинг
    :return: возвращает список словарей рейтингов
    """
    db_connect = DbConnect('netflix.db')
    rating_param = {"children": "'G'",
                    "family": "'G', 'PG', 'PG-13'",
                    "adult": "'R', 'NC-17'"
                    }

    if rating not in rating_param:
        return "Переданной группы не существует!"

    query = f"""SELECT title, rating, description
                FROM netflix
                WHERE rating in ({rating_param[rating]})"""

    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()

    result_list = []

    for movie in result:
        result_list.append({"title": movie[0],
                            "rating": movie[1],
                            "description": movie[2]})

    return result_list


def movies_by_genre(genre):
    """
    Функция, которая получает название жанра в качестве аргумента

    :param genre: получает название жанра в качестве аргумента
    :return: возвращает 10 самых свежих фильмов в формате json
    """
    db_connect = DbConnect('netflix.db')
    query = f"""SELECT title, description
                FROM netflix
                WHERE listed_in LIKE '%{genre}%'
                ORDER BY release_year DESC LIMIT 10"""

    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()

    result_list = []

    for movie in result:
        result_list.append([{"title": movie[0],
                             "description": movie[1]}])

    return result_list


def cast_partners(partner1, partner2):
    """
    Функция, которая получает в качестве аргумента имена двух актеров

    :param partner1: получает имя первого актера
    :param partner2: получает имя второго актера
    :return: возвращает всех актеров из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз.
    """
    query = f"""SELECT `cast`
                    FROM netflix
                    WHERE `cast` LIKE '%{partner1}%' AND `cast` LIKE '%{partner2}%'"""

    result = execute_query(query)

    actions_list = []
    for cast in result:
        actions_list.extend(cast[0].split(', '))
    counter = Counter(actions_list)

    result_list = []
    for partner, count in counter.items():
        if partner not in [partner1, partner2] and count > 2:
            result_list.append(partner)

    return result_list


def movies_search_by_param(movie_type, release_year, genre):
    """
    Функция, которая передает тип картины (фильм или сериал), год выпуска и ее жанр
    и получает на выходе список названий картин с их описаниями в JSON.
    
    :return: возвращает список названий картин с их описаниями в JSON.
    """
    query = f"""SELECT title, description
                FROM netflix
                WHERE type = '{movie_type}'
                AND release_year = '{release_year}'
                AND listed_in LIKE '%{genre}%'"""

    result = execute_query(query)

    result_list = []
    for movie in result:
        result_list.append({'title': movie[0], 'description': movie[1]})

    return result_list


# Проверка работы функции cast_partners()
print(f"{cast_partners('Rose McIver', 'Ben Lamb')}\n")

# Проверка работы функции movies_search_by_param()
print(movies_search_by_param('Movie', 2020, 'Drama'))
