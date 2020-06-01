from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Blogs
from django.contrib.auth.models import auth, User
from base64 import b64encode

# Create your views here.

context1 = {}

def handle_uploaded_file(f):
    destination = open('media/%s' % f.name, 'wb+')

    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def handle_main_file(f):
    destination = open('media/%s' % f.name, 'wb+')

    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
    

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
        global context1
        data = request.POST.getlist('category', None)
        print(data)
        cat = ", ".join(data)
        context1['category'] = cat
        return render(request, "select_photos.html", context1)
    else:
        return render(request, "select_photos.html")

def writecontent(request):
    if request.method == 'POST':
        global context1
        context1['photos'] = {}
        cat = request.POST.get('category', None)
        i = 0
        context1['category'] = cat
        mime = "/media/"
        main = request.FILES.get("main")
        handle_main_file(main)
        main = mime + str(main)
        context1['main'] = main
        for inImg in request.FILES.getlist("files[]"):
            handle_uploaded_file(inImg)
            inImg = mime + str(inImg)
            context1['photos'][i] = inImg
            i = i + 1
        return render(request, "write_content.html", context1)
    else:
        return render(request, "write_content.html")

def preview(request):
    global context1
    print(context1)
    title = request.POST.get('title', None)
    content = request.POST.get('content', None)
    short = request.POST.get('shortd', None)
    context1['title'] = title
    context1['content'] = content
    context1['shortd'] = short
    return render(request, "preview.html", context1)

def postBlog(request):
    pass

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
    