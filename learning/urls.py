from django.urls import path

from . import views

app_name = 'learning'

urlpatterns = [
    path("session/<int:id>/", views.learning, name="learn"),
]

htmx_urlpatterns = [
    path('process-video/<int:id>/<str:video_id>/', views.process_timestamps, name='process'),
]

urlpatterns += htmx_urlpatterns