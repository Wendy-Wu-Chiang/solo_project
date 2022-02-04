from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=\S*[a-z])(?=\S*[A-Z])(?=\S*\d)(?=\S*([^\w\s]|[_]))\S{8,}$')
  
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First must be at least 3 characters"
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last_name must be at least 3 characters"
        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"
        users_with_email = User.objects.filter(email = postData['email'])
        if len(users_with_email) >= 1:
            errors['duplicate'] = "Email already exists."
        # if len(postData['password']) < 8:
            # errors['password'] = "Password must be at least 8 characters"
        if not PASSWORD_REGEX.match(postData['password']):   
            errors['password'] = "Password must have:  at least One Upper Case Character; At least one Lower Case character; At least one digit; At least one symbol/special character; Minimum 8 characters/digits"
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Password must match!"
        return errors
      
class ExperienceManager(models.Manager):
    def content_validator(self, postData, postFile):
        errors = {}
        if len(postData['title']) < 3:
            errors["title"] = "A post title must consist of 3 characters!"
        if len(postData['content']) < 3:
            errors["content"] = "post must consist of 3 characters!"
        # return errors
        if "videofile" in postFile: 
            if postFile['videofile'].size > 300*1024*1024:

                errors["vieofile"] = "file is too big!"
        
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 


class Experience(models.Model):
    title = models.CharField(max_length=45)
    content= models.TextField()
    videofile = models.FileField(upload_to= 'videos/', null = True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    user_content = models.ForeignKey(User, related_name="user_contents", on_delete=models.CASCADE ,null=True)
    viewed_by = models.ManyToManyField(User, related_name="viewed_contents")
    
    liked_by = models.ManyToManyField(User, related_name="liked_contents")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExperienceManager()   

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    content = models.ForeignKey(Experience, related_name='content_comments', on_delete=models.CASCADE)
