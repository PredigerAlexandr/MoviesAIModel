from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from .AIModel import AIModelHelper


class AiModel(APIView):

    def get(self, request):
        ai_model_helper = AIModelHelper.AIModelHelper()
        recommended_movie = ai_model_helper.GetRecommendedMovie()
        return Response(recommended_movie.Id)

    def post(self, request:Request):
        ai_model_helper = AIModelHelper.AIModelHelper()
        movie_id = request.data['id']
        liked = request.data['liked']
        user_id = request.data['user_id']
        ai_model_helper.set_user_preference(movie_id, liked, user_id)
        return Response(status=status.HTTP_200_OK)
