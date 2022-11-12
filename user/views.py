from django.shortcuts import render
from django.shortcuts import redirect
from hashlib import sha256
from django.http import HttpResponse
from tab import views
from tab.models import Message, Time
from .models import User
# Create your views here.

def register(request):
    if request.session.get("user"):
        return redirect("/home")
    status = request.GET.get('status')
    return render(request, 'register.html', {'status': status})

def login(request):
    if request.session.get("user"):
        return redirect("/home")
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    user = User.objects.filter(username=username)

    if len(username) > 20:
        return redirect("/register/?status=6")
        
    if len(password) < 7:
        return redirect("/register/?status=4")

    if password != confirm_password:
        return redirect("/register/?status=5")

    if len(username.strip()) == 0 or len(password.strip()) == 0:
        return redirect("/register/?status=1")

    if len(user) > 0:
        return redirect("/register/?status=2")

    try:
        password = sha256(password.encode()).hexdigest()
        user = User(username=username, password=password)
        user.save()
        return redirect("/login/?status=0")
    
    except:
        return redirect("/register/?status=3")


def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    password = sha256(password.encode()).hexdigest()
    
    user = User.objects.filter(username=username).filter(password=password)
    
    if len(user) == 0:
        return redirect("/login/?status=1")

    elif len(user) > 0:
        request.session['user'] = user[0].id
        return redirect("/home")
    
def logout(request):
    user = User.objects.get(id=request.session["user"])
    views.list_messages.clear()
    Message.objects.filter(user_id=user).update(messages="")
    Time.objects.filter(user_id=user).update(time="")
    request.session.flush() 
    return redirect("/login")