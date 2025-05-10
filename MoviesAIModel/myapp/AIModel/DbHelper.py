from uuid import UUID

import null
import psycopg2
from numpy import ndarray
from psycopg2.extras import RealDictCursor
from typing import List, Optional
import json

from .Models.UserPreference import UserPreference
from .Models.Movie import MovieEntity
import ast


class DbHelper:
    @staticmethod
    def get_movies_from_db():
        # Настройки подключения к базе данных
        connection = psycopg2.connect(
            dbname="usersdgb",  # Замените на имя вашей базы данных
            user="postgres",  # Замените на имя пользователя
            password="0000",  # Замените на пароль
            host="localhost",  # Например, "localhost" или IP-адрес
            port="5432"  # Порт PostgreSQL (по умолчанию 5432)
        )

        try:
            # Создаем курсор с использованием RealDictCursor для получения данных в виде словаря
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # SQL-запрос для получения всех данных из таблицы
                cursor.execute("SELECT * FROM public.\"Movies\" LIMIT 1000")  # Замените "movies" на имя вашей таблицы

                # Получаем все строки из результата запроса
                rows = cursor.fetchall()

                # Преобразуем строки в объекты MovieEntity
                movies = []
                for row in rows:
                    movies.append(MovieEntity(
                        id=row['Id'],
                        external_id=row['ExternalId'],
                        title=row['Title'],
                        genres=row['Genres'] if row['Genres'] else [],  # Преобразуем JSON-строку в список
                        actors=row['Actors'] if row['Actors'] else [],
                        created_year=row['CreatedYear'],
                        created_countries=row['CreatedCountries'] if row['CreatedCountries'] else []
                    ))

                return movies

        finally:
            # Закрываем соединение с базой данных
            connection.close()

    def get_preference_from_db(self):
        connection = psycopg2.connect(
            dbname="usersdgb",  # Замените на имя вашей базы данных
            user="postgres",  # Замените на имя пользователя
            password="0000",  # Замените на пароль
            host="localhost",  # Например, "localhost" или IP-адрес
            port="5432"  # Порт PostgreSQL (по умолчанию 5432)
        )
        try:
            # Создаем курсор с использованием RealDictCursor для получения данных в виде словаря
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # SQL-запрос для получения всех данных из таблицы
                cursor.execute(
                    "SELECT * FROM public.\"UserPreferences\" LIMIT 1")  # Замените "movies" на имя вашей таблицы

                # Получаем все строки из результата запроса
                rows = cursor.fetchall()

                if len(rows) == 0:
                    return null

                user_preference = UserPreference(
                    id=rows[0]['Id'],
                    user_id=rows[0]['UserId'],
                    preference=self.convert_string_to_array(rows[0]['Preference']),
                    rated_film_ids=self.transform_to_uuid_list(rows[0]['RatedFilmIds'])
                )

                return user_preference

        finally:
            # Закрываем соединение с базой данных
            connection.close()

    def get_movie_by_id(self, movie_id: str) -> MovieEntity:
        connection = psycopg2.connect(
            dbname="usersdgb",
            user="postgres",
            password="0000",
            host="localhost",
            port="5432"
        )

        try:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # SQL-запрос для получения всех данных из таблицы
                cursor.execute(f"SELECT * FROM public.\"Movies\" as m WHERE m.\"Id\"='{movie_id}'")

                rows = cursor.fetchall()
                row = rows[0]

                movie = MovieEntity(
                    id=row['Id'],
                    external_id=row['ExternalId'],
                    title=row['Title'],
                    genres=row['Genres'] if row['Genres'] else [],  # Преобразуем JSON-строку в список
                    actors=row['Actors'] if row['Actors'] else [],
                    created_year=row['CreatedYear'],
                    created_countries=row['CreatedCountries'] if row['CreatedCountries'] else []
                )

                return movie
        finally:
            # Закрываем соединение с базой данных
            connection.close()

    def user_preference_update(self, user_preference: UserPreference):
        connection = psycopg2.connect(
            dbname="usersdgb",
            user="postgres",
            password="0000",
            host="localhost",
            port="5432"
        )
        try:
            cursor = connection.cursor()

            sql = f'''
                    UPDATE public.\"UserPreferences\"
                    SET "UserId" = '{user_preference.user_id}', "Preference" = '{json.dumps(user_preference.preference)}', 
                    "RatedFilmIds" = ARRAY[{','.join(f"'{str(g)}'::uuid" for g in user_preference.rated_film_ids)}]
                    WHERE "Id" = '{user_preference.id}'
                    '''

            cursor.execute(sql)
            connection.commit()

        finally:
            # Закрываем соединение с базой данных
            connection.close()

    def transform_to_uuid_list(self, input_string: str):
        # Удаляем фигурные скобки и пробелы
        cleaned_string = input_string.strip('{} ')

        # Проверяем, пустая ли строка
        if not cleaned_string:
            return []  # Возвращаем пустой список, если строка пустая

        # Преобразуем строку в список UUID
        uuid_list = [UUID(guid.strip()) for guid in cleaned_string.split(',')]

        return uuid_list

    def convert_string_to_array(self, input_string: str):
        if input_string is None or input_string == '':
            return []
        return json.loads(input_string)

    def convert_array_to_string(self, array)->str:
        hui = json.dumps(array)
        string = ""
        for el in array:
            string += str(el)
        return string


