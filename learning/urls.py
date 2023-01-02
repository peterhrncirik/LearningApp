from django.urls import path

from . import views

app_name = 'learning'

urlpatterns = [
    path("", views.learning, name="learn"),
    path("load/", views.get_video, name="load_video"),
]
