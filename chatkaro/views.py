

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import jwt
import requests
import json
from time import time
API_KEY = 'gKcG8oHVTIKBxZeMRPk7dQ'
API_SEC = 'QYxmYqi73fkBaWbalHF8cFXDTRUZRcNfdXR6'
from .forms import UserForm
from .models import feedback as feed

def good(request):
    data=get_object_or_404(feed)
    print(data)
    data.good+=1
    data.save()
    return render(request,'chatkaro/thankyou.html',{'message':'It feels like there is room for improvement'})
    # return HttpResponse("good")

def best(request):
   data=get_object_or_404(feed)
   data.best+=1
   data.save()
   return render(request,'chatkaro/thankyou.html',{'message':'Thank you for an amazing feedback'})
#    return HttpResponse("best")


def bad(request):
    data=get_object_or_404(feed)
    data.bad+=1
    data.save()
    return render(request,'chatkaro/thankyou.html',{'message':'We are sorry for your disatisfaction will try to improve'})
    # return HttpResponse("Bad")

# def members(request):
#     return HttpResponse(" <h1>chatkaro</h1> ")

def home(request):
    if request.method=="GET":
        form=AuthenticationForm()
        return render(request,'chatkaro/index.html',{"form":form})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return HttpResponse("inavlid user")
@login_required
def dashboard(request):
    link=createMeeting()
    meet_link=link[0]
    meet_pass=link[1]
    return render(request,"chatkaro/dashboard.html",{"link":meet_link,"pass":meet_pass})
def generateToken():
    token = jwt.encode(
 
        # Create a payload of the token containing
        # API Key & expiration time
        {'iss': API_KEY, 'exp': time() + 5000},
 
        # Secret used to generate token signature
        API_SEC,
 
        # Specify the hashing alg
        algorithm='HS256'
    )
    return token.decode('utf-8')
meetingdetails = {"topic": "The title of your zoom meeting",
                  "type": 2,
                  "start_time": "2019-06-14T10: 21: 57",
                  "duration": "45",
                  "timezone": "Europe/Madrid",
                  "agenda": "test",
 
                  "recurrence": {"type": 1,
                                 "repeat_interval": 1
                                 },
                  "settings": {"host_video": "true",
                               "participant_video": "true",
                               "join_before_host": "False",
                               "mute_upon_entry": "False",
                               "watermark": "true",
                               "audio": "voip",
                               "auto_recording": "cloud"
                               }
                  }
def createMeeting():
    headers = {'authorization': 'Bearer'+ generateToken(),
               'content-type': 'application/json'}
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails))
 
    print("\n creating zoom meeting ... \n")
    # print(r.text)
    # converting the output into json and extracting the details
    y = json.loads(r.text)
    print(r)
    print(y)
    join_URL = y["join_url"]
    meetingPassword = y["password"]
 
    print(
        f'\n here is your zoom meeting link {join_URL} and your \
        password: "{meetingPassword}"\n')
    return (join_URL,meetingPassword)
def feedback(request):
    form=UserForm()
    if request.method=="POST":
        value=request.POST['fav']
        print(value)
        if value=='Bad':
            return redirect('bad')
        elif value=='Good':
            return redirect('good')
        else:
            return redirect('best')
    else:  
        return render(request,"chatkaro/feedback.html")
    
def aboutus(request):
    return render(request,"chatkaro/aboutus.html")

def register(request):
    if request.method=="GET":
        return render(request,"chatkaro/register.html",{"form":UserCreationForm()})
    else:
        uname=request.POST["username"]
        pass1=request.POST["password1"]
        pass2=request.POST["password2"]
        age=request.POST['age']
        age=int(age)
        if(age>=65):
            b=User.objects.filter(username=uname)
            if(b):
                return render(request,"chatkaro/register.html",{"form":UserCreationForm(),"message":"Username taken"})
            else:
                if(pass1==pass2):
                    user=User.objects.create_user(username=uname,password=pass1)
                    user.save()
                    return redirect("home")
                else:
                    return render(request,"chatkaro/register.html",{"form":UserCreationForm(),"message":"Password Mismatch "})
        else:
            return render(request,"chatkaro/register.html",{"form":UserCreationForm(),"message":"Age Should be Greater than 64 "})
        return HttpResponse("User created")
def logout_user(request):
    logout(request)
    return redirect("home")


