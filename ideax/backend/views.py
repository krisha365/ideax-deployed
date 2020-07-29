from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Blogs, User_profile, Comment
from django.contrib.auth.models import auth, User
from base64 import b64encode
import random, os
from django.contrib.sites import requests
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context



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
    i = datetime.now()
    now = str(i.year) + '-' + str(i.month) + '-' + str(i.day) + '-' + str(i.day) + '-' + str(i.hour) + '-' + str(i.minute) + '-' + str(i.second)
    filenaam = 'media/' + str(now) + str(f.name)  
    destination = open('media/%s' % f.name, 'wb+')

    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    os.rename('media/%s' % f.name, filenaam)
    filenaam = '/' + filenaam
    return(filenaam)
    
    

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
        tempt = request.POST.get('blogid')
        print(tempt)
    else:
        print(tempt)
    blogs = Blogs.objects.filter(blogid=tempt)
    filen = Blogs.objects.get(blogid=tempt)
    conte = fileReaders(str(filen.content))
    temp = 0
    tempe = 0
    for blog in blogs:
        temp = blog.blogid
        tempe = blog.bloggerid_id
    name = request.user.username
    comm = Comment.objects.filter(blogid=temp)
    blogimg = User_profile.objects.all()
    return render(request, "separate-blog.html", {'blogs': blogs, 'blogimg':blogimg, 'comment':comm, 'blogim':conte})
        
    
def comment(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            name = request.POST.get('username')
            email = request.POST.get('email')
            bloggerid = request.POST.get('id')
            title = request.POST.get('title')
            tempt = title
            blogid = request.POST.get('blogid')
            message = request.POST.get('message')
            img = request.POST.get('image')
            coom = Comment(blogid=Blogs.objects.get(blogid=blogid), bloggerid=bloggerid, name=name, email=email, message=message, main_img=img)
            coom.save()
            return redirect('separateblog')
        else:
            name = request.POST.get('username')
            email = request.POST.get('email')
            bloggerid = request.POST.get('id')
            title = request.POST.get('title')
            tempt = title
            blogid = request.POST.get('blogid')
            message = request.POST.get('message')
            img = request.POST.get('image')
            coom = Comment(blogid=Blogs.objects.get(blogid=blogid), bloggerid=bloggerid, message=message, email=email,   main_img=img, name=name)
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
        main = handle_main_file(main)
        context1['main'] = main
        return render(request, "write_content.html", context1)
    else:
        return render(request, "write_content.html",  {'blogimg': blogimg})

def preview(request):
    global context1
    blogimg = User_profile.objects.filter(bloggerid_id=request.user.id)
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
        if User_profile.objects.filter(bloggerid_id=id).exists():
            pass
        else:
            pro = User_profile( username=name, bloggerid=User.objects.get(id=id))
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
                '''htmly = get_template('emaill.html') 
                d = { 'user_name': user_name } 
                subject = 'welcome'
                from_email = 'ideaxlive@gmail.com'
                to = user_email 
                html_content = htmly.render(d) 
                msg = EmailMultiAlternatives(subject, html_content, from_email, [to]) 
                msg.attach_alternative(html_content, "text / html")
                msg.send()'''
                send_mail(
                    'welcome',
                    'hope you enjoy this',
                    'ideaxlive@gmail.com',
                    [user_email], fail_silently = False
                )
                ######
                messages.success(request, f'Your account has been created ! You are now able to create blogs') 
                ######          
                user = User.objects.create_user(username=user_name, email=user_email, password=user_password_1, first_name=first_name, last_name=last_name)
                user.save()
                user = auth.authenticate(username=user_name, password=user_password_1)
                auth.login(request, user)
                print('user created')
                return redirect('createblog')
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
    user = request.user.id
    blogs = Blogs.objects.all().filter(bloggerid_id=user)
    blogimg = User_profile.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_active:

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
                    maine = handle_main_file(main)
                    print(maine)
                    if User_profile.objects.filter(bloggerid=user).exists():
                        User_profile.objects.filter(bloggerid=user).update(img=maine)
                        Comment.objects.filter(bloggerid=user).update(main_img=maine)
                        return redirect('profile')
                elif name != None:
                    User.objects.filter(id=user).update(username=name)
                    User_profile.objects.filter(bloggerid_id=user).update(username=name)
                    Comment.objects.filter(bloggerid=user).update(name=name)
                    return redirect('profile')
                elif email != None:
                    User.objects.filter(id=user).update(email=email)
                    Comment.objects.filter(bloggerid=user).update(email=email)
                    return redirect('profile')
                elif bio != None:
                    User_profile.objects.filter(bloggerid=user).update(bio=bio)
                    return redirect('profile')
                elif country != None and state != None:
                    location = state+", "+country
                    User_profile.objects.filter(bloggerid=user).update(location=location)
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
            return redirect('profile')
        
        
def postBlog(request):
    global context1
    if request.user.is_authenticated:
        if request.user.is_active:
            temp = random.randint(1,10000000)
            blog = Blogs(title = context1['title'], bloggerid_id=request.user.id, short_description = context1['shortd'], content=context1['content'], category=context1['category'],  blogid= temp, is_draft=False,main_img=context1['main'])
            blog.save()
            return redirect('blogindex')