from django.urls import path
from .views import AiModel

urlpatterns = [
    path('ai-model/', AiModel.as_view(), name='item-list'),
]
