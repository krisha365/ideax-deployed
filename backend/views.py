from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "index.html")

def signup(request):
    return render(request, "signup.html")

def createblog(request):
    return render(request, "createblog.html")

def blogindex(request):
    return render(request, "blog-index.html")

def profile(request):
    return render(request, "profile.html")

def separateblog(request):
    return render(request, "separate-blog.html")

def selectcategory(request):
    return render(request, "select_category.html")

def selectphotos(request):
    return render(request, "select_photos.html")

def writecontent(request):
    return render(request, "write_content.html")

    