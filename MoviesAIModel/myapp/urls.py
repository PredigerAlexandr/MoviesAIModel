from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('ai-model/', AiModel.as_view(), name='item-list'),
    path('ai-model/get_preference/<str:user_id>', get_preference, name='get_preference'),
]
