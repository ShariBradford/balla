from django.shortcuts import render, redirect, HttpResponse
from .models import User
from balla_app.models import *
import bcrypt
from django.contrib import messages
from balla_app.templates import *

def index(request): 
    return render(request,'index.html')

def register(request):
    print(request.POST)

    errors = User.objects.basic_validator(request.POST)
    if errors: 
        for k,v in errors.items():
            messages.add_message(request,messages.ERROR,v, extra_tags='register')
        return redirect("/")
        
    else:
        user = User.objects.register(request.POST)
        request.session['user_id'] = user.id
        messages.success(request,"Successfully logged in!")
        return redirect('/posts')

def login(request):
    if request.method != "POST":
       redirect('/')

    if User.objects.authenticate(request.POST['email'],request.POST['password']):
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/posts')
    else:
        request.session.clear()
        messages.error(request,"Invalid email or password.",extra_tags="login")
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect('/')