from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from armory.models import Firearm, WatchType, Magazine, ServiceMember, Watch, Armorer
import datetime

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse('users:login'))
    
    if request.method == "POST":
        issue_type = request.POST.get("form_type") 

        if issue_type == "checkout":
           return checkout(request)
        
        if issue_type == "checkin":
            return checkin(request)

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
        'servicemembers' : servicemembers,
    })

def checkout(request):
    fields = [
        "watch", "servicemember", "longarm", "handgun",
        "556-ammo", "762-ammo", "9mm-ammo",
        "mag-556", "mag-762", "mag-9mm"
    ]

    # to create a watch
    checkout_data = {field: request.POST.get(field) for field in fields}
    date = datetime.datetime.now()
    watch_type = WatchType.objects.get(name=checkout_data["watch"])
    armory_id = Armorer.objects.get(pk=1)
    member_id = ServiceMember.objects.get(pk=checkout_data["servicemember"])


    if checkout_data["longarm"] is not None:
        update_longarm = Firearm.objects.filter(serial_number=checkout_data["longarm"]).first()
        update_longarm.available = False
        update_longarm.save()

        w = Watch(watch_type=watch_type,
                  is_qualified=True, 
                  check_out=date, 
                  check_in=None,
                  ammunition_count=checkout_data["556-ammo"], 
                  armory_id=armory_id,
                  member_id=member_id,
                  )
        w.save()
        w.firearm_id.add(update_longarm)
        w.save()

    if checkout_data["handgun"] is not None:
        update_handgun = Firearm.objects.filter(serial_number=checkout_data["handgun"]).first()
        update_handgun.available = False
        update_handgun.save()

        w = Watch(watch_type=watch_type, 
                  is_qualified=True, 
                  check_out=date, 
                  check_in=None,
                  ammunition_count=checkout_data["9mm-ammo"], 
                  armory_id=armory_id,
                  member_id=member_id,
                  )
        w.save()
        w.firearm_id.add(update_handgun)
        w.save()
    

    if checkout_data["9mm-ammo"] != 0:
        update_mag_9mm = Magazine.objects.filter(id=checkout_data["mag-9mm"]).first()
        update_mag_9mm.total_9mm -= int(checkout_data["9mm-ammo"])
        update_mag_9mm.save()

    if checkout_data["556-ammo"] != 0:
        update_mag_556 = Magazine.objects.filter(id=checkout_data["mag-556"]).first()
        update_mag_556.total_556 -= int(checkout_data["556-ammo"])
        update_mag_556.save()

    if checkout_data["762-ammo"] != 0:
        update_mag_762 = Magazine.objects.filter(id=checkout_data["mag-762"]).first()
        update_mag_762.total_556 -= int(checkout_data["762-ammo"])
        update_mag_762.save()

    return redirect(reverse('eventlog:eventlog'))

def checkin(request, watch_id):
    if request.method == "POST":
        watch = get_object_or_404(Watch, pk=watch_id)
        if not watch.check_in:
            ammo_count = request.POST.get("ammunition_count")
            magazine_id = request.POST.get("magazine_id")
            firearm = watch.firearm_id.first()
            magazine = get_object_or_404(Magazine, pk=magazine_id)

            if ammo_count is not None:
                if firearm.firearm_type == "M9":
                    magazine.total_9mm += int(ammo_count)
                elif firearm.firearm_type == "M4A1":
                    magazine.total_556 += int(ammo_count)
                else:
                    magazine.total_762 += int(ammo_count)
                watch.check_in = datetime.datetime.now()
                firearm.available = True
                watch.save()
                magazine.save()
                firearm.save()
    return redirect('eventlog:eventlog')

  

    





