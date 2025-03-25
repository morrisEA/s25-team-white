from django.shortcuts import render, redirect, get_object_or_404
from .models import Firearm, ServiceMember, Watch

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
            watch.save()

        return redirect('users:index')  

    else:
        available_firearms = Firearm.objects.filter(available=True)
        return render(request, 'armory/firearm_selection.html', {
            'firearms': available_firearms,
            'member': member
        })
