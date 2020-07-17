from django.db import models
from login_app.models import User
from django.utils import timezone

# Create your models here.
class MessageManager(models.Manager):
    def basic_validator(self, postData, user_id):
        errors = {}

        if not postData['message']:
            errors['message'] = "Message is required."
        elif len(postData['message']) < 2:
            errors['message'] = "Message should be at least 2 characters."

        if not user_id:
            errors['user'] = "User is required."

        return errors

    def create_post(self,postData,user_id):
        return self.create(
            message=postData["message"], 
            user_id=user_id, 
        )    

class Message(models.Model):
    user=models.ForeignKey(User,related_name="messages", on_delete=models.CASCADE)
    message=models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()
    
    def __str__(self):
        return f'{self.user.first_name} says: {self.message[0:20]}... ({self.id})'

    def deletable(self):
        #returns true is a post was created in the last 30 minutes (1800 seconds); false otherwise.
        now = timezone.now()
        diff = now - self.created_at
        if diff.days == 0 and diff.seconds < 1800:
            return True
        return False


class CommentManager(models.Manager):
    def basic_validator(self, postData, user_id, message_id):
        errors = {}

        if not postData['comment']:
            errors['comment'] = "Comment is required."
        elif len(postData['comment']) < 2:
            errors['comment'] = "Comment should be at least 2 characters."

        if not user_id:
            errors['user'] = "User is required."

        if not message_id:
            errors['message'] = "Message is required."

        return errors

    def create_comment(self,postData,user_id, message_id):
        return self.create(
            message_id=message_id,
            comment=postData["comment"], 
            user_id=user_id, 
        )    

class Comment(models.Model):
    # id INT
    user=models.ForeignKey(User,related_name="comments", on_delete=models.CASCADE)
    message=models.ForeignKey(Message,related_name="comments", on_delete=models.CASCADE)
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = CommentManager()
    
    def __str__(self):
        return f'{self.user.first_name} says: {self.comment[0:20]}... ({self.id})'
