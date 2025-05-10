import null
import numpy as np
from typing import Optional

from .DataSetHelper import DataSetHelper
from .DbHelper import DbHelper
from sklearn.neighbors import NearestNeighbors

from .Models.Movie import MovieEntity


class AIModelHelper:
    model = null

    def GetRecommendedMovie(self) -> MovieEntity:
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

        distances, indices = AIModelHelper.model.kneighbors([user_preference.preference], n_neighbors=3)
        recommended_movies = [movies[i] for i in indices.flatten()]

        not_recommended_movies = [movie for movie in recommended_movies if
                                  movie.Id not in user_preference.rated_film_ids]

        if len(not_recommended_movies) != 0:
            return not_recommended_movies[0]

        distances, indices = AIModelHelper.model.kneighbors([user_preference.preference], n_neighbors=5)
        recommended_movies = [movies[i] for i in indices.flatten()]
        not_recommended_movies = [movie for movie in recommended_movies if
                                  movie.Id not in user_preference.rated_film_ids]

        if len(not_recommended_movies) != 0:
            return not_recommended_movies[0]

        distances, indices = AIModelHelper.model.kneighbors([user_preference.preference], n_neighbors=10)
        recommended_movies = [movies[i] for i in indices.flatten()]
        not_recommended_movies = [movie for movie in recommended_movies if
                                  movie.Id not in user_preference.rated_film_ids]

        if len(not_recommended_movies) != 0:
            return not_recommended_movies[0]

        # Были сделаны 3 попытки подобрать фильм по рекомендациям, но в каждой из попытки мы получали уже те фильмы,
        # которые были оценены ранее, поэтому возвращаем просто рандомный фильм, который ранее ещё не был оценён пользователем

        not_recommended_movies = [movie for movie in movies if
                                  movie.Id not in user_preference.rated_film_ids]

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
