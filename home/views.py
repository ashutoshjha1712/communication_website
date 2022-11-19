from django.shortcuts import render, HttpResponse
from home.models import Student
from django.core.mail import EmailMessage
from home import views
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from my_proj import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from . tokens import generate_token

# Create your views here.
def index(request):
    page_data = {'name': 'Praveen Kumar', 'roll':191020101037}
    return render(request,'index.html',page_data)
    return render(request,'index.html')
    #return HttpResponse("<h1> Hello, this is Home Page</h1>")

def about(request):
    #return HttpResponse("<h1>This is About Page</h1>")
    return render (request,'about.html')

def contact(request):
    return render(request,'contact.html')

def login(request):
    return render(request,'login.html')


# def sign_up(request):
#     page_data = {'usrnm':0, 'email':0,'psw':0,'msg':''}
#     if(request.method == 'POST'):
#         try:
#             page_data['usrnm'] = request.POST.get('usrnm')
#             page_data['email'] = request.POST.get('email')
#             page_data['psw'] = request.POST.get('psw')
#         except:
#             page_data['area'] = 'Data entered wrongly'
#         else:
#             page_data['email'] = request.POST.get('email')
#         finally:
#             page_data['msg'] = 'Processed at SERVER'
#      return render(request,'sign_up.html',page_data) 

#def downloads(request):
    return HttpResponse("<h1>This is Download Page</h1>")

def sign_up(request):
    page_data = {'msg':''}
    if(request.method == 'POST'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        collage_name = request.POST.get('collage_name')
        gender = request.POST.get('gender')
        user = Student(name=name,email=email,phone=phone,password=password,collage_name=collage_name,gender=gender)
        user.save()
        page_data['msg'] = 'User Registerd.........'
    return render(request,'sign_up.html',page_data)





# Create your views here.
def index(request):
    return render(request,'index.html')
def signup(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['E-mail']
        password1=request.POST['pass1']
        password2=request.POST['pass2']
        if User.objects.filter(username=username):
            messages.error(request,'this username already exist,try with some username')
            return render(request ,'index.html')
        if User.objects.filter(email=email):
            messages.error(request,'email already exist')
            return render(request,'index.html')
        if len(username)>10:
            messages.error(request,'username should be less than 06 character')
        if password1!=password2:
            messages.error(request,'password did not match!')
        if not username.isalnum():
            messages.error(request,'username must be alphanumeric')
            return render(request,'index.html')
        myuser=User.objects.create_user(username,email,password1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.is_active=False
        myuser.save()
        messages.success(request,'you have registered succesfully')
       
        

        #welcome to email
        subject='welcome to Englishbuddy System..... login !!!'
        message='hello' + myuser.first_name +'!!\n' + 'welcome to Englishbuddy thanks for registering in this website'+'\n'+'\n'+ 'We have also send you the confirmation email please click the link to activate your account'  
        from_email=settings.EMAIL_HOST_USER 
        to_list=[myuser.email]  
        send_mail(subject,message,from_email,to_list,fail_silently=True) 


        #email address confirmation

        current_site=get_current_site(request)
        email_subject='Confirmation email Englishbuddy login!!'
        message2=render_to_string('email_confirmation.html',{
            'name':myuser.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser),

        })
        email=EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently=True
        email.send()







        return render(request,'signin.html')
        
    return render(request,'signup.html')
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password1=request.POST['pass1']
        user=authenticate(username=username,password=password1)
        if user is not None:

            login(request,user)
            fname=user.first_name
        
            return render(request,'index.html',{'fname':fname})
            
            
            
        else:
            messages.error(request,'bad credintials')
            return redirect('home')
    return render(request,'signin.html')
def signout(request):
    logout(request)
    messages.success(request,'logged out successfully')
    return render(request,'signout.html')
def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else:
        return render(request,'activation_failed.html')





    

