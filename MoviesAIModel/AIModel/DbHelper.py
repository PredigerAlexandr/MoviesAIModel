import null
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
import json

from AIModel.Models.UserPreference import UserPreference
from Models.Movie import MovieEntity
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

    @staticmethod
    def get_preference_from_db():
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
                cursor.execute("SELECT * FROM public.\"UserPreferences\" LIMIT 1")  # Замените "movies" на имя вашей таблицы

                # Получаем все строки из результата запроса
                rows = cursor.fetchall()

                if len(rows)==0:
                    return null

                user_preference = UserPreference(
                    id = rows[0]['Id'],
                    user_id = rows[0]['UserId'],
                    preference = rows[0]['Preference']
                )

                return user_preference

        finally:
            # Закрываем соединение с базой данных
            connection.close()

    def get_unrated_movies(movies: List[MovieEntity], userId):
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

                cursor.execute("SELECT * FROM public.\"UserPreferences\" as m "
                               "WHERE m.\"UserId\" = \"62d777c0-3bd7-4603-96ec-305a28d10875\"")

                rows = cursor.fetchall()

                if len(rows)==0:
                    return null

                user_preference = UserPreference(
                    id = rows[0]['Id'],
                    user_id = rows[0]['UserId'],
                    preference = rows[0]['Preference']
                )

                return user_preference

        finally:
            # Закрываем соединение с базой данных
            connection.close()
        return null
