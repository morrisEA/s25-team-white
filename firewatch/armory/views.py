from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from armory.models import Firearm, WatchType, Magazine, ServiceMember

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
    
    try:
        watches = WatchType.objects.all()
    except:
        watches = None

    try:
        magazines = Magazine.objects.all()
    except:
        magazines = None

    try:
        servicemembers = ServiceMember.objects.all()
    except:
        servicemembers = None


    return render(request, "armory/index.html", {
        'longarms' : longarms,
        'handguns' : handguns,
        'watches' : watches,
        'magazines' : magazines, 
        'servicemembers' : servicemembers       
    })

    