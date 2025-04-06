from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from armory.models import * 
from django.utils import timezone
from django.conf import settings
from django.db.models import F
def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse("users:login")) 
    try:
        servicemember = ServiceMember.objects.filter(user=request.user).first()
        command = servicemember.command_id
    except:
        servicemember = None
        
    return render(request, "users/dashboard.html", {
        'servicemember': servicemember,
        'command': command
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("users:index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })

    return render(request, "users/login.html")

def logout_view(request):
    user = request.user.username
    logout(request)
    messages.success(request, f"{user} has logged out.")
    return redirect('users:login')



def manage_watch(request):
    
    if not request.user.is_authenticated:
        return redirect(f"{reverse('users:login')}?next={request.path}")
    
    user = request.user
    servicemember = ServiceMember.objects.get(user=user)
    active_watch = Watch.objects.filter(member_id=servicemember).order_by('-check_out').first()

    user_in_watch = active_watch and (active_watch.check_in == active_watch.check_out)

    if request.method == 'POST':
        if 'start_watch' in request.POST and not user_in_watch:
            available_firearms = Firearm.objects.filter(available=True)
            if not available_firearms.exists():
                messages.error(request, "Error: No firearms available at this time.")
                return redirect('users:manage_watch')


            now = timezone.now()
            Watch.objects.create(
                watch_type="Standard",
                is_qualified=True,
                check_out=now,
                check_in=now,
                member_id=servicemember,
                ammunition_count=0,
                armory_id=None
            )
            
            return redirect('armory:firearm_selection', member_id=servicemember.id)

        elif 'stop_watch' in request.POST and user_in_watch:
            ammo_fields ={
                "9mm": "returned_9mm",
                "5.56": "returned_556", 
                "7.62": "returned_762",
                "m9": "returned_m9",
                "m4a1": "returned_m4a1"
            }
            
            returned = {
                ammo_type: int(request.POST.get(field, 0))
                for ammo_type, field in ammo_fields.items()
            }

            
            issued_ammo = request.session.get('issued_ammo', {})
            
            over_returned = [
                ammo_type for ammo_type, qty in returned.items() 
                if qty > int(issued_ammo.get(ammo_type, 0))
                ]
          
            if over_returned:
                messages.error(
                    request,
                    f"Return failed. Try again."
                )
                return redirect('users:manage_watch')
            
            
            
            total_ammo = sum(returned.values())
            active_watch.ammunition_count = total_ammo
            active_watch.check_in = timezone.now()
            active_watch.save()

    
            for ammo in active_watch.ammunition_id.all():
                ammo_type = ammo.ammunition_type.lower()
                if ammo_type in returned:
                    ammo.quantity += returned[ammo_type]
                    ammo.save()

    
            for firearm in active_watch.firearm_id.all():
                firearm.available = True
                firearm.save()


            if 'issued_ammo' in request.session:
                del request.session['issued_ammo']
            messages.success(request, f"Returned {total_ammo} rounds successfully.")
            return redirect('users:manage_watch')
        
        
    return render(request, 'users/manage_watch.html', {
        'user_in_watch': user_in_watch
    })