from rest_framework.views import APIView
from rest_framework.response import Response

from AIModel import AIModel


class ItemList(APIView):

    def get(self, request):

        return Response('ZAEBOK')