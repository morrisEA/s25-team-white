from django.urls import path
from . import views

app_name = "armory"

urlpatterns = [
    path('watch/<int:watch_id>/check_out/', views.check_out_watch, name='watch_check_out'),
    path('watch/<int:watch_id>/check_in/', views.check_in_watch, name='watch_check_in'),
]
