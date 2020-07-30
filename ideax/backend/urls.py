from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    
    path('profile/', views.profile, name="profile"),
    path('blogindex/', views.blogindex, name="blogindex"),
    path('createblog/', views.createblog, name="createblog"),
    path('signup', views.signup, name="signup"),
    path('separateblog/', views.separateblog, name="separateblog"),
    path('selectcategory/', views.selectcategory, name="selectcategory"),
    path('selectphotos/', views.selectphotos, name="selectphotos"),
    path('writecontent/', views.writecontent, name="writecontent"),
    path('preview/', views.preview, name="preview"),
    path('post/', views.postBlog, name="postBlog"),
    path('logout', views.logout, name="logout"),
    path('login', views.login, name="login"),
    path('', views.index, name='index'),
        url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('draft/', views.saveDraft, name="saveDraft"),
    path('comment/', views.comment, name="comment")
]