from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Watch, ServiceMember

@login_required
def check_out_watch(request, watch_id):
    """Handles watch check-out"""
    servicemember = request.user.servicemember

    if watch_id == 0:
        # If watch_id is 0, create a new watch for the user
        watch = Watch.objects.create(member_id=servicemember, check_out_time=now())
    else:
        watch = get_object_or_404(Watch, id=watch_id, member_id=servicemember)
        if not watch.check_out_time:  # Prevent multiple check-outs
            watch.check_out_time = now()
            watch.save()

    return redirect('dashboard')

@login_required
def check_in_watch(request, watch_id):
    """Handles watch check-in"""
    watch = get_object_or_404(Watch, id=watch_id, member_id=request.user.servicemember)
    if watch.check_out_time and not watch.check_in_time:  # Prevent check-in without check-out
        watch.check_in_time = now()
        watch.save()
    return redirect('dashboard')
