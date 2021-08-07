import json
from django.http.response import HttpResponseNotAllowed, JsonResponse
from django.middleware import csrf
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from Web.models import ChatRoom, RoomChatMessage
from users.models import User

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
            User.objects.create_user(username=data['username'],fullname=data['fullname'],phonenumber=data['phonenumber'],addressId=data['addressId'], addressName=data['addressName'], gender=data['gender'], password=data['password'])
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
@login_required(login_url='/login')
def user_info(request):
    if request.method == "GET":
        return render(request, 'Web/user_info.html')

@login_required(login_url='/login')
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
                'uimage': user.image.url,
                'ucoin': user.coin
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

@login_required(login_url='/login')
def get_user_lichsu(request):
    if request.method == "GET":
        user = request.user
        room = user.room_view.all()
        
        list_room = []
        for r in room:
            list_room.append({
                'title' : r.title,
                'id': r.id,
            })
        context = {
            'list_room': list_room,
            'status': True,
            'ufullname': user.fullname,
            'uimage': user.image.url
        }
        return JsonResponse(context)


def open_ghep(request):
    user = request.user
    if(user.is_authenticated):
        return JsonResponse({'status': True})
    return JsonResponse({'status': False})


@login_required(login_url='/login')
def get_room_chat(request):
    room_id = json.loads(request.body)['room_id']
    room = ChatRoom.objects.filter(id=room_id).first()
    if room:
        room_title = room.title
    messages = RoomChatMessage.objects.all_chat(room_id)
    mess = []
    for ms in messages:
        mess.append({
            'fullname': ms.user.fullname,
            'uimage': ms.user.image.url,
            'timestamp': ms.timestamp.strftime('%Y-%m-%d %H:%M'),
            'content': ms.content,
            'username': ms.user.username,
            })
    return JsonResponse({'room_title': room_title, 'username': request.user.username, 'image':request.user.image.url, 'messages': mess})


@login_required(login_url='/login')
def room(request, room_id):
    room = ChatRoom.objects.filter(id=room_id).first()
    user = request.user
    if room and user in room.view_users.all():
        if request.method == "GET":
            return render(request, 'Web/room.html')
    return HttpResponseNotAllowed('405 ERROR')
    
        
# MOMO PAY
