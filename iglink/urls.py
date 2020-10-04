from django.urls import path
from .views import recent_media_json, profile_data_json

urlpatterns = [
    path('ig-recent_media/', recent_media_json),
    path('ig-profile/', profile_data_json)
]
