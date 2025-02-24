from django.shortcuts import render, redirect

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

    return render(request, "users/login.html")



