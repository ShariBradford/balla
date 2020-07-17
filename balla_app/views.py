from django.shortcuts import render, redirect
from .models import Message,Comment
from login_app.models import User
from django.contrib import messages

# Create your views here.
def welcome(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "wall_messages": Message.objects.all().order_by('-created_at'),
    }
    return render(request,'posts/balla.html', context)

def post_message(request):
    #It is a truth universally acknowledged, that a single man in possession of a good fortune must be in want of a wife.
    
    errors = Message.objects.basic_validator(request.POST, request.session['user_id'])
    if errors: 
        for k,v in errors.items():
            messages.error(request,v)
    else:
        Message.objects.create_post(request.POST, request.session['user_id'])
    return redirect("/posts")

def comment(request,message_id):
    errors = Comment.objects.basic_validator(request.POST, request.session['user_id'],message_id)
    if errors: 
        for k,v in errors.items():
            messages.error(request,v)
    else:
        Comment.objects.create_comment(request.POST, request.session['user_id'],message_id)
    return redirect("/posts")

def delete(request,message_id):
    message_to_delete = Message.objects.get(id=message_id)
    if message_to_delete.user.id == request.session['user_id']:
        message_to_delete.delete()
    return redirect("/posts")

