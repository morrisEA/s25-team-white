from django.urls import path
from .views import firearm_selection 
app_name = 'armory' 
urlpatterns = [
    path('firearm/select/<int:member_id>/', firearm_selection, name='firearm_selection'),
    
]
