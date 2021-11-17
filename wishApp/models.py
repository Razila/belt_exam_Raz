from django.db import models
import re
import bcrypt


# Create your models here.
PASSWIRD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):

    def basic_validator(self, post_data):
        errors = {}
        if post_data["first_name"].isalpha() != True:
            errors['first_name'] = "Invalid first name."
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be no fewer than 2 characters."
        if post_data["last_name"].isalpha() != True:
            errors['last_name'] = "Invalid last name."
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be no fewer than 2 characters."
        if len(post_data['user_name']) < 1:
            errors['user_name'] = 'User name is too short.'
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address."
            
        if len(post_data['email']) > 384:
            errors['email'] = 'Email address is too long.'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match.'
        try:
            user = User.objects.get(email=post_data['email'])
            errors['email_in_use'] = 'This email is already associated with an account.'
        except:
            pass
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=50)
    email = models.CharField(max_length=384)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class WishManager(models.Manager):

    def wish_validator(self, post_data):
        errors = {}
        if len(post_data['item']) < 3:
            errors['item'] = "Item must be no fewer than 3 characters."
        if len(post_data['description']) < 3:
            errors['first_name'] = "Description must be no fewer than 3 characters."
        return errors


class Wish(models.Model):
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="wishes", on_delete = models.CASCADE)
    objects = WishManager()


class Granted_wish(models.Model):
    item = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now=True)
    granted_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes')
    user = models.ForeignKey(User, related_name="granted_wishes", on_delete = models.CASCADE)

    def _str_(self):
        return '{} {} {}'.format(self.item, self.date_added, self.granted_at,self.likes,self.user)
