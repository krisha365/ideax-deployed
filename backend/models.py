from django.db import models

# Create your models here.


class Blogs(models.Model):
    
    # title = models.CharField(max_length = 200)
    # description = models.CharField(max_length = 500)
    # image = models.ImageField(upload_to='data_of_pics')
    # left = models.BooleanField(default = False)
    

    title = models.CharField(max_length=150)
    bloggerid = models.IntegerField()
    short_description = models.CharField(max_length = 500)
    content = models.TextField()
    category = models.CharField(max_length = 20)
    blogid = models.IntegerField(primary_key=True, unique=True)
    is_draft = models.BooleanField(default = True)
    main_img = models.ImageField(upload_to="profile-pics")

class Blogs_images(models.Model):
    blogid = models.IntegerField()
    img = models.ImageField()
    is_main = models.BooleanField(default=False)
    
class User_profile(models.Model):
    bloggerid = models.IntegerField()
    img = models.ImageField(upload_to="profile-pics")
    username = models.CharField(max_length=50)