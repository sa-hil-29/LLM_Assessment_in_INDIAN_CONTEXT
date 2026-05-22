from django.urls import path
from . import views

app_name = "assessment"

urlpatterns = [
    path("", views.home, name="home"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path('submit-model/', views.submit_model, name='submit_model'),
    path('reevaluate-all/', views.reevaluate_all, name='reevaluate_all'),
    path('about/', views.about, name='about'),
]
