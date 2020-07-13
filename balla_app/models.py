from django.db import models
from login_app.models import User

# Create your models here.
class MessageManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if not postData['message']:
            errors['message'] = "Message is required."
        elif len(postData['Message']) < 2:
            errors['message'] = "Message should be at least 2 characters."

        if not postData['user']:
            errors['user'] = "User is required."

        return errors

class Message(models.Model):
    user=models.ForeignKey(User,related_name="messages", on_delete=models.CASCADE)
    message=models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()
    
    def __str__(self):
        return f'{self.user.first_name} says: {self.message[0:20]}... ({self.id})'