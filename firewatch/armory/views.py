from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Watch, ServiceMember
from django.urls import reverse



@login_required
def watch_status(request):
    """View that checks if the user has an active watch and redirects accordingly."""
    try:
        servicemember = request.user.servicemember  
    except ServiceMember.DoesNotExist:
        return redirect("dashboard")  

    
    active_watch = Watch.objects.filter(member_id=servicemember, check_in_time__isnull=True).first()

    return render(request, "armory/watch_status.html", {"active_watch": active_watch})

@login_required
def check_out_watch(request, watch_id):
    """Handles watch check-out"""
    servicemember = request.user.servicemember  

   
    existing_watch = Watch.objects.filter(member_id=servicemember, check_in_time__isnull=True).first()
    if existing_watch:
        return redirect("watch_status")


    armory = servicemember.command_id.armory_set.first()
    if not armory: 
        return redirect(reverse("users:dashboard"))
    
    
    
    watch = Watch.objects.create(
        member_id=servicemember,
        check_out_time=now(),
        watch_type="Standard Watch",
        is_qualified=True,  
        ammunition_count=0,  
        armory_id=servicemember.command_id.armory_set.first(),
    )
    
    watch.ammunition_id.set([])
    watch.firearm_id.set([])
    watch.qualification_id.set([])
    return redirect("watch_status")

@login_required
def check_in_watch(request, watch_id):
    """Handles watch check-in"""
    try:
        watch = Watch.objects.get(id=watch_id, member_id=request.user.servicemember, check_in_time__isnull=True)
        watch.check_in()
    except Watch.DoesNotExist:
        pass  

    return redirect("watch_status")
