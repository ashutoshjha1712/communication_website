from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path ('', views.index, name= 'home'),
    path('about', views.about, name= 'about'),
    path('contact', views.contact, name='contact'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('login', views.login, name='login'),
    #path('downloads', views.downloads, name= 'downloads'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),  
]
