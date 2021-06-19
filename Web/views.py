from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.middleware import csrf
from django.shortcuts import render

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
        context = {
            'name': "lam lam",
            'age': 18
        }
        return JsonResponse(context)


# login
def login(request):
    if request.method == "GET":
        csrf.get_token(request)
        return render(request, 'Web/login.html')
    if request.method == "POST":
        return JsonResponse({'message': "Đăng nhập thành công!"})


# logout
def logout(request):
    if request.method == "GET":
        context = {
            'name': "1333"
        }
        return render(request, 'Web/index.html', context)


# user infomation
def user_info(request):
    if request.method == "GET":
        context = {
            'name': "eeeeeee"
        }
        return render(request, 'Web/user_info.html', context)
