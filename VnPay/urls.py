"""vnpayPayment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('payment/', views.payment, name='payment'),
    path('momo_payment/', views.momo_payment, name='momo_payment'),
    path('payment_ipn/', views.payment_ipn, name='payment_ipn'),
    path('momo_payment_ipn/', views.momo_payment_ipn, name='momo_payment_ipn'),
    path('payment_return/', views.payment_return, name='payment_return'),
    path('momo_payment_return/', views.momo_payment_return, name='momo_payment_return'),
    path('query/', views.query, name='query'),
    path('refund/', views.refund, name='refund'),
]
