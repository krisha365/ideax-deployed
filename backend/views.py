from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Blogs
from django.contrib.auth.models import auth, User
from base64 import b64encode

# Create your views here.

input_image = 0

def index(request):
    return render(request, "index.html")

def blogindex(request):
    context = {
    "five" : [1, 2, 3, 4, 5],
    }
    return render(request, "blog-index.html", context)

def separateblog(request):
    return render(request, "separate-blog.html")

def selectcategory(request):
    return render(request, "select_category.html")

def selectphotos(request):
    if request.method == 'POST':
        context1 = {}
        data = request.POST.getlist('category', None)
        print(data)
        cat = ", ".join(data)
        context1['category'] = cat
        return render(request, "select_photos.html", context1)
    else:
        return render(request, "select_photos.html")

def writecontent(request):
    if request.method == 'POST':
        global input_image
        context1 = {}
        cat = request.POST.get('category', None)
        print(cat)
        context1['category'] = cat
        inImg = request.FILES["files[]"].read()

        encoded = b64encode(inImg).decode('ascii')
        mime = "img/upload"
        mime = mime + ";" if mime else ";"
        input_image = "data:%sbase64,%s" % (mime, encoded)        
        context1['photos'] = input_image
        return render(request, "write_content.html", context1)
    else:
        return render(request, "write_content.html")

def preview(request):
    context1 = {}
    cat = request.POST.get('category', None)
    img = input_image
    title = request.POST.get('title', None)
    content = request.POST.get('content', None)
    context1['category'] = cat
    context1['photos'] = img
    context1['title'] = title
    context1['content'] = content
    return render(request, "preview.html", context1)

def createblog(request):
    if request.user.is_authenticated:
        return render(request, "createblog.html")
    else:
        return redirect('login')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = first_name
        user_email = request.POST['user_email']
        user_password_1 = request.POST['user_password_1']
        user_password_2 = request.POST['user_password_2']

        if user_password_1 == user_password_2:
            if User.objects.filter(username=user_name).exists():
                context = { "message" : 'username already taken'}
                messages.info(request, 'Username taken')
                return render(request, 'signup.html', context)
            elif User.objects.filter(email=user_email).exists():
                context = { "message" : 'Email ID already taken'}
                messages.info(request, 'Email ID taken')
                return render(request, 'signup.html', context)
            else:            
                user = User.objects.create_user(username=user_name, email=user_email, password=user_password_1, first_name=first_name, last_name=last_name)
                user.save()
                print('user created')
                return redirect('index')
        else:
                context = { "message" : 'Password not matching'}
                messages.info(request, 'Password not matching')
                return render(request, 'signup.html', context)
    else:    
        return render(request, "signup.html")

def login(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        user_password = request.POST['user_password_1']
        user = auth.authenticate(username=user_name, password=user_password)
        if user is not None:
            auth.login(request, user)
            print('Successfully Logged in')
            return redirect('createblog')
        else:
            print('Invalid Login Credentials')
            return redirect('blogindex')
    else:
        print('not good')
        return render(request, "login.html")





def profile(request):
    context = {
        "five" : [1, 2, 3,4, 5,6,7,8],
    }
    return render(request, "profile.html", context)




# Backend Logic

def logout(request):
    
    auth.logout(request)
    return redirect('/')
    