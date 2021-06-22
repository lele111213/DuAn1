import Web
import json
from users.models import UserManager
from django.http.response import HttpResponse, JsonResponse
from django.middleware import csrf
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


def home(request):
    if request.method == "GET":
        username = request.user.username
        context = {
        }
        if request.user.is_authenticated:
            context['name'] = username

        return render(request, 'Web/home.html', context)

def contact(request):
    return render(request, 'Web/contact.html')

# register
def register(request):
    if request.method == "GET":
        csrf.get_token(request)
        return render(request, 'Web/register.html')
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            UserManager.create_user(User.objects, username=data['username'],fullname=data['fullname'],phonenumber=data['phonenumber'],addressId=data['addressId'], addressName=data['addressName'], gender=data['gender'], password=data['password'])
            context = {
                'message': "Đăng ký thành công!",
                'status': True
            }
        except:
            context = {
                'message': "Tên đăng nhập đã được sử dụng!",
                'status': False
            }
        return JsonResponse(context)


# login
def login(request):
    if request.method == "GET":
        csrf.get_token(request)
        return render(request, 'Web/login.html')
    if request.method == "POST":
        context = {
            'message': "Tên tài khoản hoặc mật khẩu không chính xác!",
            'status': False
        }
        data = json.loads(request.body)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None :
            user_login(request, user)
            context['message'] = "Đăng nhập thành công"
            context['status'] = True
        return JsonResponse(context)


# logout
def logout(request):
    user_logout(request)
    return redirect('home')


# user infomation
@login_required(login_url='/login/?next=/user_info/')
def user_info(request):
    if request.method == "GET":
        context = {
            'name': request.user.username
        }
        return render(request, 'Web/user_info.html', context)

@login_required
def get_user_info(request):
    if request.method == "GET":
        user = request.user
        context = {
            'user': {
                'uname' : user.username,
                'ufullname': user.fullname,
                'uphonenumber': user.phonenumber,
                'uaddressId': user.addressId,
                'uaddressName': user.addressName,
                'ugender': user.gender,
                'uage': user.age,
                'uheight': user.height,
                'uhobbies': user.hobbies,
                'uimage': user.image.url
            },
            'status': True,
            'message': ''
        }
        return JsonResponse(context)

@login_required
def update_user(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        try:
            user.fullname = data['user']['ufullname']
            user.addressId = data['user']['uaddressId']
            user.addressName = data['user']['uaddressName']
            user.hobbies = data['user']['uhobbies']
            user.height = data['user']['uheight']
            user.gender = data['user']['ugender']
            user.age = data['user']['uage']
            user.phonenumber = data['user']['uphonenumber']
            user.save(using=User.objects._db)
            context = {
                'status': True,
                'message': 'success!'
            }
        except:
            context = {
                'status': False,
                'message': 'failed!'
            }
        return JsonResponse(context)

@login_required
def update_user_image(request):
    if request.method=="POST":
        if request.FILES['image']:
            image = request.FILES['image']
            user = request.user
            user.image = image
            user.save(using=User.objects._db)
            context = {
                'status': True,
                'message': 'success!'
            }
            return JsonResponse(context)