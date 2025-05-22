import numpy as np

from .Models.Movie import MovieEntity
from typing import List, Optional
import json


class DataSetHelper:
    i = 0

    def PreparationData(movies: List[MovieEntity]):
        actors = set()
        genres = set()
        countries = set()

        for movie in movies:
            if movie.Actors:  # Проверяем, что поле Actors не пустое
                if movie.Actors:
                    actors.update(movie.Actors)
                if movie.Genres:
                    genres.update(movie.Genres)
                if movie.CreatedCountries:
                    countries.update(movie.CreatedCountries)

        with open('actors.json', 'w', encoding='utf-8') as json_file:
            json.dump(list(actors), json_file, ensure_ascii=False, indent=4)

        with open('genres.json', 'w', encoding='utf-8') as json_file:
            json.dump(list(genres), json_file, ensure_ascii=False, indent=4)

        with open('countries.json', 'w', encoding='utf-8') as json_file:
            json.dump(list(countries), json_file, ensure_ascii=False, indent=4)

    def CreateDataSet(movies: List[MovieEntity]):
        feature_matrix = np.array(
            [DataSetHelper.extract_features(movie) for movie in movies])
        return feature_matrix

    @staticmethod
    def extract_features(movie: MovieEntity):
        with open('actors.json', 'r', encoding='utf-8') as json_file:
            allActors = json.load(json_file)
        with open('genres.json', 'r', encoding='utf-8') as json_file:
            allGenres = json.load(json_file)
        with open('countries.json', 'r', encoding='utf-8') as json_file:
            allCreatedCountries = json.load(json_file)

        genres_vector = [1 if genre in movie.Genres else 0 for genre in allGenres]
        actors_vector = [1 if actor in movie.Actors else 0 for actor in allActors]
        countries_vector = [1 if country in movie.CreatedCountries else 0 for country in allCreatedCountries]

        if movie.CreatedYear < 1980:
            created_year_vector = [1, 0, 0, 0]
        elif movie.CreatedYear < 2000:
            created_year_vector = [0, 1, 0, 0]
        elif movie.CreatedYear < 2015:
            created_year_vector = [0, 0, 1, 0]
        else:
            created_year_vector = [0, 0, 0, 1]

        print(DataSetHelper.i)
        DataSetHelper.i = DataSetHelper.i+1

        return np.array(genres_vector + actors_vector + countries_vector + created_year_vector)

    def prepare_preference(self, preference:List[float]):
        with open('actors.json', 'r', encoding='utf-8') as json_file:
            allActors = json.load(json_file)
            actorsCount = len(allActors)
        with open('genres.json', 'r', encoding='utf-8') as json_file:
            allGenres = json.load(json_file)
            genresCount = len(allGenres)
        with open('countries.json', 'r', encoding='utf-8') as json_file:
            allCreatedCountries = json.load(json_file)
            countriesCount = len(allCreatedCountries)

        #требуется выделить предпочтения пользователя по жанрам, странам и годам производства, т.к. актёров слишком много, чтобы они имели такой де приоритет
        weights = np.array([0.1]*actorsCount+[2]*genresCount+[5]*countriesCount+[10]*4)
        prepared_preference = np.array(preference) * weights
        return prepared_preference.tolist()

