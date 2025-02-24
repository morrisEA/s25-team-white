from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),  
    path("login/", views.login_view, name="login"),
    path("main/", views.main_view, name="main"),
    path("inventory/", views.inventory_view, name="inventory"),
    path("scan/", views.scan_view, name="scan"),
    path("logs/", views.logs_view, name="logs"),
    path("notifications/", views.notifications_view, name="notifications"),
]
