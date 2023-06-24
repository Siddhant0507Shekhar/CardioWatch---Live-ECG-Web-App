from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# from .models import User

# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a new page
            return redirect('/home')
        else:
            messages.error(request, 'Incorrect username or password.')
    return render(request, "authoriz/login.html", {})

def signup_page(request):
    if request.user.is_authenticated:
        return redirect('/home')
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_pass']
        if password!=confirm:
            messages.error(request,"Password and confirm password should be same. ")
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            return redirect('/authoriz/login')
    return render(request, "authoriz/signup.html", {})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/authoriz/login')
