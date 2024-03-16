from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.IndexView, name="index"),
    path("<int:question_id>/", views.DetailView, name="detail"),
    path("<int:question_id>/results/", views.ResultView, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]