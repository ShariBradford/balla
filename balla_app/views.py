from django.shortcuts import render, redirect
from .models import Message
from django.contrib import messages

# Create your views here.
def post_message(request):
    #It is a truth universally acknowledged, that a single man in possession of a good fortune must be in want of a wife.
    request.POST['user'] = request.session['user_id']
    errors = Message.objects.basic_validator(request.POST)
    if errors: 
        for k,v in errors.items():
            messages.error(request,v)
        return redirect("/success")
