from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("vijesti/", views.news_list, name="news_list"),
    path("vijesti/nova/", views.news_create, name="news_create"),
    path("vijesti/<int:pk>/", views.news_detail, name="news_detail"),
    path("vijesti/<int:pk>/favorite/", views.add_news_to_favorites, name="news_favorite_add"),
]
