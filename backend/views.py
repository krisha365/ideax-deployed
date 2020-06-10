from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Blogs, Blogs_images, User_profile
from django.contrib.auth.models import auth, User
from base64 import b64encode
import random

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
    blogimg = User_profile.objects.all()
    
    return render(request, "index.html", {'blogimg':blogimg})

def blogindex(request):
    blogs = Blogs.objects.filter(is_draft=False)
    blogimg = User_profile.objects.all()
    blogimge = Blogs_images.objects.filter(is_main=True)
    return render(request, "blog-index.html", {'blogs': blogs, 'blogimg': blogimg, 'blogimge': blogimge})

def separateblog(request):
    if request.method == 'POST':
        titl = request.POST.get('title', None)
        print(titl)
        blogs = Blogs.objects.filter(title=titl)
        for blog in blogs:
            temp = blog.blogid
        print(temp)
        name = request.user.username
        id = request.user.id
        blogimg = Blogs_images.objects.filter(blogid=temp, is_main=False)
        blogimge = User_profile.objects.filter(bloggerid=id, username=name)
        return render(request, "separate-blog.html", {'blogs': blogs,'blogimg': blogimg, 'blogimge':blogimge})

def selectcategory(request):
    if request.method == 'POST':
        blogimg = User_profile.objects.all()
        global context1
        title = request.POST.get('title', None)
        short = request.POST.get('shortd', None)
        print(short)
        context1['title'] = title
        context1['shortd'] = short
        context1['blogimg'] = blogimg.values()
        return render(request, "select_category.html", context1)
    else:
        return render(request, "select_category.html", {'blogimg':blogimg})
    
def selectphotos(request):
    if request.method == 'POST':
        blogimg = User_profile.objects.all()
        global context1
        data = request.POST.getlist('category', None)
        print(data)
        cat = ", ".join(data)
        title = request.POST.get('title', None)
        short = request.POST.get('shortd', None)
        context1['title'] = title
        context1['shortd'] = short
        context1['category'] = cat
        context1['blogimg'] = blogimg.values()
        return render(request, "select_photos.html", context1)
    else:
        return render(request, "select_photos.html",  {'blogimg': blogimg})

def writecontent(request):
    if request.method == 'POST':
        blogimg = User_profile.objects.all()
        global context1
        title = request.POST.get('title', None)
        short = request.POST.get('shortd', None)
        context1['title'] = title
        context1['shortd'] = short
        context1['photos'] = {}
        context1['blogimg'] = blogimg.values()
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
        return render(request, "write_content.html",  {'blogimg': blogimg})

def preview(request):
    global context1
    blogimg = User_profile.objects.all()
    print(context1)
    title = request.POST.get('title', None)
    content = request.POST.get('content', None)
    short = request.POST.get('shortd', None)
    context1['title'] = title
    context1['content'] = content
    context1['shortd'] = short
    context1['blogimg'] = blogimg.values()
    print(short)
    return render(request, "preview.html", context1)





def createblog(request):
    if request.user.is_authenticated:
        blogimg = User_profile.objects.all()
        return render(request, "createblog.html", {'blogimg': blogimg})
    else:
        return redirect('login', {'blogimg': blogimg})

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
    blogs = Blogs.objects.all()
    blogimg = User_profile.objects.all()
    blogimge = Blogs_images.objects.filter(is_main=True)
    if request.method == 'POST':
        print(1)
        if request.user.is_authenticated:
            print(2)
            if request.user.is_active:
                print(3)
                user = request.user.id
                username = request.user.username
                print(user)
                mime = "/media/"
                main = request.FILES.get("maine")
                print(main)
                handle_main_file(main)
                main = mime + str(main)
                if User_profile.objects.filter(bloggerid=user).exists():
                    print('yes')
                    User_profile.objects.filter(bloggerid=user).update(img=main)
                    return redirect('/')
                else:
                    blogimg = User_profile(bloggerid = user, img=main, username=username)
                    blogimg.save()
                    return redirect('/')
                    
    else:
        return render(request, "profile.html", {'blogs': blogs, 'blogimg': blogimg, 'blogimge':blogimge})
    




# Backend Logic

def logout(request):
    
    auth.logout(request)
    return redirect('/')

def saveDraft(request):
    global context1
    print(context1)
    if request.user.is_authenticated:
        if request.user.is_active:
            print("hello")
            temp = random.randint(1,10000000)
            blog = Blogs(title = context1['title'], short_description = context1['shortd'], content=context1['content'], category=context1['category'], bloggerid=request.user.id, blogid= temp, is_draft=True,main_img=context1['main'])
            blog.save()
            blogimg = Blogs_images(blogid = temp, img=context1['main'], is_main = True)
            blogimg.save()
            if context1['photos']:
                for i in context1['photos']:
                    blogimg = Blogs_images(blogid = temp, img = context1['photos'][i])
                    blogimg.save()
            return redirect('profile')
        
        
def postBlog(request):
    global context1
    print(context1)
    if request.user.is_authenticated:
        if request.user.is_active:
            print("hello")
            temp = random.randint(1,10000000)
            blog = Blogs(title = context1['title'], short_description = context1['shortd'], content=context1['content'], category=context1['category'], bloggerid=request.user.id, blogid= temp, is_draft=False,main_img=context1['main'])
            blog.save()
            blogimg = Blogs_images(blogid = temp, img=context1['main'], is_main = True)
            blogimg.save()
            if context1['photos']:
                for i in context1['photos']:
                    blogimg = Blogs_images(blogid = temp, img = context1['photos'][i])
                    blogimg.save()
    
            return redirect('blogindex')
    