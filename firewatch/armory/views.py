from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def firearm_selection(request, member_id):
    member = get_object_or_404(ServiceMember, pk=member_id)
    watch = Watch.objects.filter(member_id=member, check_in__isnull=True).first()

    if request.method == 'POST':
        firearm_id = request.POST.get('firearm_id')
        firearm = get_object_or_404(Firearm, pk=firearm_id)
        firearm.available = False
        firearm.save()

        if watch:
            watch.firearm_id.add(firearm)

        # Gather ammo amounts
            ammo_inputs = {
                '9mm': int(request.POST.get('ammo_9mm', 0)),
                '5.56': int(request.POST.get('ammo_556', 0)),
                '7.62': int(request.POST.get('ammo_762', 0)),
                'm9': int(request.POST.get('ammo_m9', 0)),
                'm4a1': int(request.POST.get('ammo_m4a1', 0))
            }

            for ammo_type, qty in ammo_inputs.items():
                if qty > 0:
                    ammo_obj = Ammunition.objects.filter(ammunition_type__iexact=ammo_type).first()
                    if ammo_obj:
                        IssuedAmmunition.objects.create(
                            watch=watch,
                            ammunition=ammo_obj,
                            quantity_issued=qty
                        )
                        watch.ammunition_id.add(ammo_obj)

            watch.save()

        return redirect('users:manage_watch')
  

    else:
        available_firearms = Firearm.objects.filter(available=True)
        return render(request, 'armory/firearm_selection.html', {
            'firearms': available_firearms,
            'member': member
        })
