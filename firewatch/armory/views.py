from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from armory.models import Firearm

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse('users:login'))

    try:
        longarms = Firearm.objects.filter(firearm_type ="M4A1").all()
    except:
        longarms = None

    try:
        handguns = Firearm.objects.filter(firearm_type ="M9").all()
    except:
        handguns = None


    return render(request, "armory/index.html", {
        'longarms' : longarms,
        'handguns' : handguns        
    })

    