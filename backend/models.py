from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Blogs(models.Model):
    
    # title = models.CharField(max_length = 200)
    # description = models.CharField(max_length = 500)
    # image = models.ImageField(upload_to='data_of_pics')
    # left = models.BooleanField(default = False)
    

    title = models.CharField(max_length=150)
    bloggerid = models.ForeignKey(User, on_delete=models.CASCADE)
    short_description = models.CharField(max_length = 500)
    content = models.FileField()
    category = models.CharField(max_length = 20)
    blogid = models.IntegerField(primary_key=True, unique=True)
    is_draft = models.BooleanField(default = True)
    main_img = models.ImageField(upload_to="blog-pics")
    created_on = models.DateTimeField(auto_now_add=True)
   
class User_profile(models.Model):
    bloggerid = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="profile-pics", default="/media/icons8-user-100.png")
    username = models.CharField(max_length=50)
    bio = models.TextField()
    location = models.CharField(max_length=80)

class Comment(models.Model):
    blogid = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    bloggerid = models.IntegerField(default=-1)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    message = models.TextField('message')
    created_on = models.DateTimeField(auto_now_add=True)
    main_img = models.ImageField(default="/media/icons8-user-100.png")