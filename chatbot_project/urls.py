"""chatbot_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
import chatbot_app.views
import basic_auth.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_history/', chatbot_app.views.get_history, name='get_history'),
    path('chatbot/', chatbot_app.views.chatbot, name='chatbot'),
    path('login/', basic_auth.views.login, name="login"),
    path('logout/', basic_auth.views.logout, name="logout"),
    path('register_user/', basic_auth.views.register_user, name="register_user"),
]
