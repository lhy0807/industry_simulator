"""industry_simulator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('', include('startscreen.urls', namespace='index'), name='index'),
    path('create_robot/', include('startscreen.urls', namespace='startscreen'), name='create_robot'),
    path('create_group/<int:game_id>/<int:company_id>', include('startscreen.urls', namespace='create_group'), name='create_group'),
    path('join_group/', include('startscreen.urls', namespace='join_group'), name='join_group'),
    path('game/', include('game.urls'), name='game'),
    path('admin/', admin.site.urls),
]