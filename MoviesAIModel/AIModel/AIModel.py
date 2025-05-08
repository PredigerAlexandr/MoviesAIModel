import null
import numpy as np

from AIModel.DataSetHelper import DataSetHelper
from AIModel.DbHelper import DbHelper
from sklearn.neighbors import NearestNeighbors


class AIModelHelper:
    model = null

    @staticmethod
    def GetRecommendedMovie():
        movies = DbHelper.get_movies_from_db()
        if AIModelHelper.model == null:
            DataSetHelper.PreparationData(movies)
            movies_dataset = DataSetHelper.CreateDataSet(movies)
            user_settings = []
            model = NearestNeighbors(metric='cosine')
            model.fit(movies_dataset)

        user_preference = DbHelper.get_preference_from_db()

        if user_preference == null:
            recommended_movie = np.random.choice(movies)
            return recommended_movie

        average_features = np.mean(user_preference, axis=0)
        distances, indices = model.kneighbors([average_features], n_neighbors=3)
        recommended_movies = [movies[i] for i in indices.flatten()]
