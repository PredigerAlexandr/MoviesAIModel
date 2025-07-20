import heapq
import json
from operator import itemgetter
from uuid import UUID

import null
import numpy as np
from typing import Optional

from .DataSetHelper import DataSetHelper
from .DbHelper import DbHelper
from sklearn.neighbors import NearestNeighbors

from .Models.Movie import MovieEntity
from .Models.ResultUserPreference import ResultUserPreference


def find_closest_sequence(input_sequence, target_sequences):
    input_array = np.array(input_sequence)
    distances = [np.linalg.norm(input_array - np.array(target)) for target in target_sequences]
    min_index = np.argmin(distances)
    return target_sequences[min_index], distances[min_index]


class AIModelHelper:
    model = null

    def GetRecommendedMovie(self) -> MovieEntity:
        dataset_helper = DataSetHelper()
        movies = DbHelper.get_movies_from_db()
        if AIModelHelper.model == null:
            DataSetHelper.PreparationData(movies)
            movies_dataset = DataSetHelper.CreateDataSet(movies)
            user_settings = []
            AIModelHelper.model = NearestNeighbors(metric='cosine')
            AIModelHelper.model.fit(movies_dataset)

        db_helper = DbHelper()
        user_preference = db_helper.get_preference_from_db()

        if len(user_preference.preference) == 0 or len(user_preference.rated_film_ids) == 0:
            recommended_movie = np.random.choice(movies)
            return recommended_movie

        modify_preference = dataset_helper.prepare_preference(user_preference.preference)

        distances, indices = AIModelHelper.model.kneighbors([modify_preference], n_neighbors=3)
        recommended_movies = [movies[i] for i in indices.flatten()]

        not_recommended_movies = [movie for movie in recommended_movies if
                                  UUID(movie.Id) not in user_preference.rated_film_ids]

        if len(not_recommended_movies) != 0:
            return not_recommended_movies[0]

        distances, indices = AIModelHelper.model.kneighbors([user_preference.preference], n_neighbors=5)
        recommended_movies = [movies[i] for i in indices.flatten()]
        not_recommended_movies = [movie for movie in recommended_movies if
                                  UUID(movie.Id) not in user_preference.rated_film_ids]

        if len(not_recommended_movies) != 0:
            return not_recommended_movies[0]

        distances, indices = AIModelHelper.model.kneighbors([user_preference.preference], n_neighbors=10)
        recommended_movies = [movies[i] for i in indices.flatten()]
        not_recommended_movies = [movie for movie in recommended_movies if
                                  UUID(movie.Id) not in user_preference.rated_film_ids]

        if len(not_recommended_movies) != 0:
            return not_recommended_movies[0]

        # Были сделаны 3 попытки подобрать фильм по рекомендациям, но в каждой из попытки мы получали уже те фильмы,
        # которые были оценены ранее, поэтому возвращаем просто рандомный фильм, который ранее ещё не был оценён пользователем

        not_recommended_movies = [movie for movie in recommended_movies if
                                  UUID(movie.Id) not in user_preference.rated_film_ids]

        return np.random.choice(not_recommended_movies)

    def set_user_preference(self, movie_id: str, liked: bool, user_id: str):
        db_helper = DbHelper()
        user_preference = db_helper.get_preference_from_db()
        movie = db_helper.get_movie_by_id(movie_id)
        user_preference.rated_film_ids.append(movie.Id)
        movie_dataset = DataSetHelper.CreateDataSet([movie])[0]
        if len(user_preference.preference) == 0:
            user_preference.preference = [0] * len(movie_dataset)

        if liked:
            user_preference.preference = [x + ((y - x) / len(user_preference.rated_film_ids)) for x, y in
                                          zip(user_preference.preference, movie_dataset)]
        else:
            user_preference.preference = [x + (((-y) - x) / len(user_preference.rated_film_ids)) for x, y in
                                          zip(user_preference.preference, movie_dataset)]

        db_helper.user_preference_update(user_preference)

    def get_user_preference(self, user_id):
        db_helper = DbHelper()
        user_preference = db_helper.get_preference_from_db()

        with open('actors.json', 'r', encoding='utf-8') as json_file:
            allActors = json.load(json_file)
        with open('genres.json', 'r', encoding='utf-8') as json_file:
            allGenres = json.load(json_file)
        with open('countries.json', 'r', encoding='utf-8') as json_file:
            allCreatedCountries = json.load(json_file)

        start_actors_index = 0
        end_actors_index = len(allActors) - 1
        start_genres_index = end_actors_index + 1
        end_genres_index = start_genres_index + len(allGenres) - 1
        start_countries_index = end_genres_index + 1
        end_countries_index = start_countries_index + len(allCreatedCountries) - 1
        start_year_index = end_countries_index + 1
        end_year_index = start_year_index + 4

        # Выбираем подсписок в заданном интервале
        actors_sublist = user_preference.preference[start_actors_index:end_actors_index]

        # Находим 5 наибольших значений и их индексы (относительно подсписка)
        largest_values = heapq.nlargest(5, enumerate(actors_sublist), key=lambda x: x[1])

        # Получаем индексы в исходном списке и значения
        actors_indexes = [idx for idx, value in largest_values]
        get_actor_elements = itemgetter(*actors_indexes)
        actors_result = list(get_actor_elements(allActors))

        # Выбираем подсписок в заданном интервале
        genres_sublist = user_preference.preference[start_genres_index:end_genres_index]

        # Находим 5 наибольших значений и их индексы (относительно подсписка)
        largest_values = heapq.nlargest(5, enumerate(genres_sublist), key=lambda x: x[1])

        # Получаем индексы в исходном списке и значения
        genres_indexes = [idx for idx, value in largest_values]
        get_genre_elements = itemgetter(*genres_indexes)
        genres_result = list(get_genre_elements(allGenres))

        # Выбираем подсписок в заданном интервале
        countries_sublist = user_preference.preference[start_countries_index:end_countries_index]

        # Находим 5 наибольших значений и их индексы (относительно подсписка)
        largest_values = heapq.nlargest(5, enumerate(countries_sublist), key=lambda x: x[1])

        # Получаем индексы в исходном списке и значения
        country_indexes = [idx for idx, value in largest_values]
        get_country_elements = itemgetter(*country_indexes)
        countries_result = list(get_country_elements(allCreatedCountries))

        # Выбираем подсписок в заданном интервале
        year_sublist = user_preference.preference[start_year_index:end_year_index]

        # последовательности чисел, которые используются для кодировки временных интервалов
        target_sequences = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        # ищем максимально близкую последоватльность к той, которая в предпочтениях у пользователя
        closest_sequence = find_closest_sequence(year_sublist, target_sequences)

        if closest_sequence == [0, 0, 0, 1]:
            year_result = "2015 год и моложе"
        elif closest_sequence == [0, 0, 1, 0]:
            year_result = "2000 - 2015 года"
        elif closest_sequence == [0, 1, 0, 0]:
            year_result = "1980 - 2000 года"
        else:
            year_result = "1980 и старше"

        return ResultUserPreference(actors_result, genres_result, countries_result, year_result)
