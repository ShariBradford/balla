from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),
    path('postmessage', views.post_message),
    path('<int:message_id>/comment',views.comment),
    path('<int:message_id>/delete',views.delete),
]