from django.shortcuts import render, redirect, HttpResponse
from .models import User
from balla_app.models import *
import bcrypt
from django.contrib import messages
from balla_app.templates import *

def index(request): 
    context = {
        "form": request.GET.get('form','')
    }
    return render(request,'index.html',context)

def register(request):
    #print(f"Method: {request.method}")
    #if request.method == "GET":
    #    redirect('/')
    #else:
    print(request.POST)

    errors = User.objects.basic_validator(request.POST)
    if errors: 
        for k,v in errors.items():
            messages.error(request,v)
        return redirect("/?form=register")
        
    else:
        pw = request.POST["password"]
        pw_hash = bcrypt.hashpw(
            pw.encode(),
            bcrypt.gensalt()
        ).decode()

        user = User.objects.create(
            first_name=request.POST["first_name"], 
            last_name=request.POST["last_name"], 
            email=request.POST["email"], 
            password=pw_hash, 
        )
        request.session['user_id'] = user.id
        messages.success(request,"Successfully logged in!")
        return redirect('/success')

def login(request):
    #if request.method != "POST":
    #    redirect('/')
        
    print(request.POST)

    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_in_user = user.first()
        if bcrypt.checkpw(
            request.POST['password'].encode(),
            logged_in_user.password.encode()):
            request.session['user_id'] = logged_in_user.id
            messages.success(request,"Successfully logged in!")
            return redirect('/success')

        else:
            request.session['user_id'] = ''
            messages.error(request,"Invalid email or password.")
            return redirect("/?form=login")

    else:
        request.session['user_id'] = ''
        messages.error(request,"Invalid email or password.")
        return redirect("/?form=login")

def welcome(request):
    #if request.method != 'POST':
    #    return redirect('/')
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    wall_messages = Message.objects.all()
    context = {
        "user": User.objects.filter(id=request.session['user_id']).first(),
        "wall_messages": wall_messages,
    }
    return render(request,'balla.html', context)

def logout(request):
    del request.session['user_id']
    return redirect('/')