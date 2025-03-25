from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required 
from armory.models import ServiceMember, Watch, Firearm, Magazine


from django.utils import timezone
# Create your views here.
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



@login_required
def manage_watch(request):
    user = request.user
    servicemember = ServiceMember.objects.get(user=user)
    user_in_watch = Watch.objects.filter(member_id=servicemember, check_in__isnull=True).exists()

    if request.method == 'POST':
        if 'start_watch' in request.POST and not user_in_watch:
            available_firearms = Firearm.objects.filter(available=True)

        # Check BEFORE creating the watch
            if not available_firearms.exists():
                messages.error(request, "Error: No firearms available at this time.")
                return redirect('users:manage_watch')

        # If firearms are available, create the watch
            new_watch = Watch.objects.create(
                watch_type="Standard",
                is_qualified=True,
                check_out=timezone.now(),
                check_in=None,
                member_id=servicemember,
                ammunition_count=0,
                armory_id=None  # Set later after firearm/armory selection
            )
            messages.success(request, "Watch started. Proceed to firearm selection.")
            return redirect('armory:firearm_selection', member_id=servicemember.id)

        elif 'stop_watch' in request.POST and user_in_watch:
            watch = Watch.objects.filter(member_id=servicemember, check_in__isnull=True).first()
            if watch:
                ammo_returned = int(request.POST.get('ammo_returned', 0))
                mags_returned = int(request.POST.get('mags_returned', 0))

                # Update Watch info
                watch.ammunition_count = ammo_returned
                watch.check_in = timezone.now()
                watch.save()

                # Update magazine inventory (example for 9mm)
                magazine = Magazine.objects.filter(armory_id__command_id=servicemember.command_id).first()
                if magazine:
                    magazine.total_9mm += mags_returned
                    magazine.save()

                # Set firearms as available
                for firearm in watch.firearm_id.all():
                    firearm.available = True
                    firearm.save()

                messages.success(request, f"Returned {ammo_returned} rounds and {mags_returned} magazines.")
            return redirect('users:manage_watch')

    return render(request, 'users/manage_watch.html', {
        'user_in_watch': user_in_watch
    })