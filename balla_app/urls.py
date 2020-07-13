from django.urls import path
from . import views

urlpatterns = [
    path('postmessage', views.post_message),
]