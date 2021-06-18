from django.shortcuts import render

# Create your views here.


def home(request):
    if request.method == "GET":
        context = {
        }
        if request.user.is_authenticated:
            context['name'] = request.user.username
        return render(request, 'Web/home.html', context)


# register
def register(request):
    if request.method == "GET":
        context = {
            'name': "1333"
        }
        return render(request, 'Web/register.html', context)


# login
def login(request):
    if request.method == "GET":
        context = {
            'name': "tranle"
        }
        return render(request, 'Web/login.html', context)


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
