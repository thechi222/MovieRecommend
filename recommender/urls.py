from django.urls import path
from recommender import views

app_name = "recommender"

urlpatterns = [
    path("<int:pk>/", views.recommend_api, name="api"),
]