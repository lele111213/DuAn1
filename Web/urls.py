from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('contact/', views.contact, name='contact'),

    # api
    path('api/get_user_info/', views.get_user_info, name='get_user_info'),
    path('api/update_user/', views.update_user, name='update_user'),
    path('api/update_user_image/', views.update_user_image, name='update_user_image'),
    path('api/get_user_lichsu/', views.get_user_lichsu, name='get_user_lichsu'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
