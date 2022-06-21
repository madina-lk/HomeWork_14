import sqlite3
from collections import Counter


class DbNetflix:

    def __init__(self, path):
        """Конструктор"""
        self.connection = sqlite3.connect(path, check_same_thread=False)                # Подключаемся к БД
        self.cur = self.connection.cursor()                                             # Запускаем курсор

    def get_movie_by_title(self, title):
        """Получение данных по названию фильма """

        sqlite_query = ("SELECT `title`, `country`, `release_year`, `description` "     # Запрос для вывода фильмов по названию
                        "FROM `netflix` "
                        "WHERE `title` like :substring_pattern ")

        self.cur.execute(sqlite_query, {"substring_pattern": f"%{title}%"})             # Выполнение запроса

        result_list_of_dict = [{'title': col1, 'country': col2, 'release_year': col3, 'description': col4} for
                               (col1, col2, col3, col4) in self.cur.fetchall()]         # формирование результата

        return result_list_of_dict

    def get_movie_by_year(self, year1, year2):
        """Получение фильмов за определенные года"""

        sqlite_query = (f"SELECT `title`, `release_year` "
                        f"FROM `netflix` "
                        f"WHERE `release_year` BETWEEN {year1} AND {year2}  "
                        f"order by `release_year` limit 100")

        self.cur.execute(sqlite_query)

        query_result = [dict(line) for line in
                        [zip([column[0] for column in self.cur.description], row) for row in self.cur.fetchall()]]

        return query_result

    def get_movie_by_genre(self, genre):
        """Получение фильмов по жанру"""

        sqlite_query = (f"SELECT `title`, `description` "
                        f"FROM `netflix` "
                        f"WHERE `listed_in` LIKE '%{genre}%' "
                        f"ORDER BY `release_year` DESC LIMIT 10")

        self.cur.execute(sqlite_query)

        result_list_of_dict = [{'title': col1, 'description': col2} for (col1, col2) in self.cur.fetchall()]

        return result_list_of_dict

    def rating_formation(self):
        """Формирование списков по запросу групп"""
        sqlite_query = (f"SELECT DISTINCT rating "
                        f"FROM `netflix` "
                        f"WHERE rating in ('G', 'PG', 'PG-13', 'R', 'NC-17') ")

        self.cur.execute(sqlite_query)
        result = [row[0] for row in self.cur.fetchall()]

        return result

    def get_movie_by_rating(self, rating_list):
        """Получение фильма по возрастной группе"""

        placeholder = '?'                                                               # Конструкция для корректной передачи списка в параметр запроса
        placeholders = ', '.join(placeholder for unused in rating_list)                 # Запрос
        query = 'SELECT title, rating, description ' \
                'FROM `netflix` ' \
                'WHERE `rating` IN (%s)' \
                'GROUP BY title, rating, description' % placeholders
        self.cur.execute(query, rating_list)                                            # Выполнение запроса

        query_result = [{'title': col1, 'rating': col2, 'description': col3} for (col1, col2, col3) in self.cur.fetchall()]

        return query_result

    def get_movie_by_param(self, movie_type, year, genre):
        """Получение фильма по переданным параметрам (типу, жанру, году)"""
        sqlite_query = (f"SELECT `title`, `description` "
                        f"FROM `netflix` "
                        f"WHERE `listed_in` LIKE '%{genre}%' and `release_year` == {year} and `type` LIKE '%{movie_type}%' ")

        self.cur.execute(sqlite_query)

        result_list_of_dict = [{'title': col1, 'description': col2} for (col1, col2) in self.cur.fetchall()]

        return result_list_of_dict

    def get_casts_by_cast(self, cast1, cast2):
        """Получение данных по названию фильма """

        sqlite_query = ("SELECT `cast` "     # Запрос для вывода фильмов по названию
                        "FROM `netflix` "
                        "WHERE `cast` like :substring_pattern_1 and `cast` like :substring_pattern_2")

        self.cur.execute(sqlite_query, {"substring_pattern_1": f"%{cast1}%", "substring_pattern_2": f"%{cast2}%"})             # Выполнение запроса

        casts = ','.join([row[0] for row in self.cur.fetchall()]).split(', ')
        c = Counter(casts)

        return list(set([result for result in casts if c[result] > 2 and result not in (cast1, cast2)]))




