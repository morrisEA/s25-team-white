from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import *
from django.urls import reverse
from django.utils import timezone
from django.db.models import F

def firearm_selection(request, member_id):
    if not request.user.is_authenticated:
        return redirect(f"{reverse('users:login')}?next={request.path}")

    member = get_object_or_404(ServiceMember, pk=member_id)


    if request.method == 'POST':
        firearm_id = request.POST.get('firearm_id')
        firearm = get_object_or_404(Firearm, pk=firearm_id)

        ammo_types = ['9mm', 'm4a1', '5.56', '7.62', 'm9']
        
        ammo_inputs = {
           atype: int(request.POST.get(f"ammo_{atype}", 0) or 0)
           for atype in ammo_types
        }

        selected_types = {atype for atype, qty in ammo_inputs.items() if qty > 0}
        ammo_objects = list(Ammunition.objects.filter(ammunition_type__in=selected_types))
        ammo_map = {a.ammunition_type.lower(): a for a in ammo_objects}

        total_ammo_count = sum([qty for qty in ammo_inputs.values() if qty > 0])
        
        firearm.available = False
        firearm.save()
        armorer = Armorer.objects.filter(member_id=member).first()
        now = timezone.now()
        new_watch = Watch.objects.create(
            watch_type="Standard",
            is_qualified=True,
            check_out=now,
            check_in=now,
            member_id=member,
            ammunition_count=total_ammo_count,
            armory_id=armorer,
            
        )
        new_watch.firearm_id.add(firearm)
        
        for ammo_type, qty in ammo_inputs.items():
            if qty > 0:
                ammo_obj = ammo_map.get(ammo_type.lower())
                if ammo_obj:
                    new_watch.ammunition_id.add(ammo_obj)
                    ammo_obj.quantity -= qty
                    ammo_obj.save()

        new_watch.save()
        request.session['issued_ammo'] = ammo_inputs
        return redirect('users:manage_watch') 
    
    
    else:
        available_firearms = Firearm.objects.filter(available=True)
        return render(request, 'armory/firearm_selection.html', {
            'firearms': available_firearms,
            'member': member
        })
