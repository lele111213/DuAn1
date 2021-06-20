import json
from json.encoder import JSONEncoder
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.middleware import csrf
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    if request.method == "GET":
        username = request.user.username
        context = {
        }
        if request.user.is_authenticated:
            context['name'] = username

        return render(request, 'Web/home.html', context)


# register
def register(request):
    if request.method == "GET":
        csrf.get_token(request)
        return render(request, 'Web/register.html')
    if request.method == "POST":
        data = json.loads(request.body)
        if(data['username'] == "12"):
            context = {
                'message': "Đăng ký thành công!",
                'status': True
            }
        else:
            context = {
                'message': "Đăng ký thất bại",
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
@login_required
def user_info(request):
    if request.method == "GET":
        context = {
            'name': "eeeeeee"
        }
        return render(request, 'Web/user_info.html', context)
