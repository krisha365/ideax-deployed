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
    img = models.ImageField(upload_to='blog_images')
    category = models.CharField(max_length = 20)

