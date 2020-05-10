from django.urls import path
from . import views

urlpatterns = [
    
    path('profile/', views.profile, name="profile"),
    path('blogindex/', views.blogindex, name="blogindex"),
    path('createblog/', views.createblog, name="createblog"),
    path('signup/', views.signup, name="signup"),
    path('separateblog/', views.separateblog, name="separateblog"),
    path('selectcategory/', views.selectcategory, name="selectcategory"),
    path('selectphotos/', views.selectphotos, name="selectphotos"),
    path('writecontent/', views.writecontent, name="writecontent"),
    path('', views.index, name='index')
]