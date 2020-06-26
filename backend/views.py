from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Blogs, User_profile, Comment
from django.contrib.auth.models import auth, User
from base64 import b64encode
import random
from django.contrib.sites import requests
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.

context1 = {}
tempt = ""

def handle_uploaded_file(f, t):
    i = datetime.now()
    now = str(i.year) + '-' + str(i.month) + '-' + str(i.day) + '-' + str(i.day) + '-' + str(i.hour) + '-' + str(i.minute) + '-' + str(i.second)
    filenaam = 'media/' + str(t) + str(now) + '.txt'
    destination = open(filenaam, 'w+')
    destination.write(f)
    destination.close()
    return(filenaam)

def fileReaders(naam):
    destination = open(naam, 'r')
    conte = destination.read()
    destination.close()
    return(conte)

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
    return render(request, "blog-index.html", {'blogs': blogs, 'blogimg': blogimg})


def separateblog(request):
    global tempt
    if request.method == 'POST': 
        tempt = request.POST.get('title')
        print(tempt)
    else:
        print(tempt)
    blogs = Blogs.objects.filter(title=tempt)
    filen = Blogs.objects.get(title=tempt)
    conte = fileReaders(str(filen.content))
    temp = 0
    tempe = 0
    for blog in blogs:
        temp = blog.blogid
        tempe = blog.bloggerid
    name = request.user.username
    comm = Comment.objects.filter(bloggerid=temp)
    blogimg = User_profile.objects.all()
    return render(request, "separate-blog.html", {'blogs': blogs, 'blogimg':blogimg, 'comment':comm, 'blogim':conte})
        
    
def comment(request):
    global tempt
    if request.method == 'POST':
        if request.user.is_authenticated:
            name = request.POST.get('username')
            email = request.POST.get('email')
            blogid = request.POST.get('id')
            title = request.POST.get('title')
            tempt = title
            bloggerid = request.POST.get('bloggerid')
            message = request.POST.get('message')
            img = request.POST.get('image')
            print(img)
            coom = Comment(blogid=blogid, name=name, email=email, bloggerid=bloggerid, message=message, main_img=img)
            coom.save()
            return redirect('separateblog')
        else:
            name = request.POST.get('username')
            email = request.POST.get('email')
            blogid = request.POST.get('id')
            title = request.POST.get('title')
            tempt = title
            bloggerid = request.POST.get('bloggerid')
            message = request.POST.get('message')
            img = request.POST.get('image')
            coom = Comment(blogid=blogid, name=name, email=email, bloggerid=bloggerid, message=message, main_img=img)
            coom.save()
            return redirect('separateblog')
            
        
def selectcategory(request):
    blogimg = User_profile.objects.all()
    if request.method == 'POST':
        global context1
        title = request.POST.get('title', None)
        short = request.POST.get('shortd', None)
        context1['title'] = title
        context1['shortd'] = short
        context1['blogimg'] = blogimg.values()
        return render(request, "select_category.html", context1)
    else:
        return render(request, "select_category.html", {'blogimg':blogimg})
    
def selectphotos(request):
    blogimg = User_profile.objects.all()
    if request.method == 'POST':
        global context1
        data = request.POST.getlist('category', None)
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
        context1['blogimg'] = blogimg.values()
        cat = request.POST.get('category', None)
        i = 0
        context1['category'] = cat
        mime = "/media/"
        main = request.FILES.get("main")
        handle_main_file(main)
        main = mime + str(main)
        context1['main'] = main
        return render(request, "write_content.html", context1)
    else:
        return render(request, "write_content.html",  {'blogimg': blogimg})

def preview(request):
    global context1
    blogimg = User_profile.objects.filter(bloggerid=request.user.id)
    title = request.POST.get('title', None)
    content = request.POST.get('content', None)
    short = request.POST.get('shortd', None)
    context1['title'] = title
    filenaa = handle_uploaded_file(content, title)
    context1['content'] = filenaa
    context1['contente'] = content 
    context1['shortd'] = short
    context1['blogimg'] = blogimg.values()
    return render(request, "preview.html", context1)





def createblog(request):
    blogimg = User_profile.objects.all()
    if request.user.is_authenticated:
        id = request.user.id
        name = request.user.username
        if User_profile.objects.filter(bloggerid=id).exists():
            pass
        else:
            pro = User_profile(bloggerid=id, username=name)
            pro.save()
        return render(request, "createblog.html", {'blogimg': blogimg})
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
    blogs = Blogs.objects.all()
    blogimg = User_profile.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_active:
                user = request.user.id
                username = request.user.username
                mime = "/media/"
                main = request.FILES.get("maine", None)
                name = request.POST.get("usernaam", None)
                email = request.POST.get('useremail', None)
                country = request.POST.get('country', None)
                state = request.POST.get('state', None)
                
                bio = request.POST.get('bio', None)
                print(bio)
                if main != None:
                    handle_main_file(main)
                    main = mime + str(main)
                    if User_profile.objects.filter(bloggerid=user).exists():
                        User_profile.objects.filter(bloggerid=user).update(img=main)
                        return redirect('profile')
                    else:
                        blogimg = User_profile(bloggerid = user, img=main, username=username)
                        blogimg.save()
                        return redirect('/')
                elif name != None:
                    User.objects.filter(id=user).update(username=name)
                    return redirect('profile')
                elif email != None:
                    User.objects.filter(id=user).update(email=email)
                    return redirect('profile')
                elif bio != None:
                    User_profile.objects.filter(id=user).update(bio=bio)
                    return redirect('profile')
                elif country != None and state != None:
                    location = state+", "+country
                    User_profile.objects.filter(id=user).update(location=location)
                    return redirect('profile')
                
    else:
        return render(request, "profile.html", {'blogs': blogs, 'blogimg': blogimg})
    




# Backend Logic

def logout(request):
    
    auth.logout(request)
    return redirect('/')

def saveDraft(request):
    global context1
    if request.user.is_authenticated:
        if request.user.is_active:
            temp = random.randint(1,10000000)
            blog = Blogs(title = context1['title'], short_description = context1['shortd'], content=context1['content'], category=context1['category'], bloggerid=request.user.id, blogid= temp, is_draft=True,main_img=context1['main'])
            blog.save()
            # blogimg = Blogs_images(blogid = temp, img=context1['main'], is_main = True)
            # blogimg.save()
            # if context1['photos']:
            #     for i in context1['photos']:
            #         blogimg = Blogs_images(blogid = temp, img = context1['photos'][i])
            #         blogimg.save()
            return redirect('profile')
        
        
def postBlog(request):
    global context1
    if request.user.is_authenticated:
        if request.user.is_active:
            temp = random.randint(1,10000000)
            blog = Blogs(title = context1['title'], short_description = context1['shortd'], content=context1['content'], category=context1['category'], bloggerid=request.user.id, blogid= temp, is_draft=False,main_img=context1['main'])
            blog.save()
            # blogimg = Blogs_images(blogid = temp, img=context1['main'], is_main = True)
            # blogimg.save()
            # if context1['photos']:
            #     for i in context1['photos']:
            #         blogimg = Blogs_images(blogid = temp, img = context1['photos'][i])
            #         blogimg.save()
    
            return redirect('blogindex')
    