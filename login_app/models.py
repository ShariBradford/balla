from django.db import models
import datetime
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not postData['first_name']:
            errors['first_name'] = "First Name is required."
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters."

        if not postData['last_name']:
            errors['last_name'] = "Last name is required."
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters."

        if not postData['birth_date']:
            errors['birth_date'] = "Birth date is required."
        else:        
            today = datetime.date.today()
            birthday = datetime.datetime.strptime(postData['birth_date'],'%Y-%m-%d')
            years = today.year - birthday.year
            if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
                years -= 1
            print(f'Today: {today} | Birthday: {birthday} | Years: {years}')

            if years < 13:
                errors['birth_date'] = "You must be over 13 to register."

        if not postData['email']:
            errors['email'] = "Email is required."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        elif self.filter(email=postData['email']):
            errors['email'] = "Email address must be unique."

        if not postData['password']:
            errors['password'] = "Password is required."
        elif len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."
        elif postData['password'] != postData['password_confirm']:
            errors['password'] = "Passwords do not match."

        return errors

class User(models.Model):
    # id INT
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateTimeField(default=datetime.date.today)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    #created_at = models.DateTimeField(auto_now_add = True)
    #updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.id})'