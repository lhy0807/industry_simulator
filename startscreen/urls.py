from django.urls import path

from . import views
app_name = 'startscreen'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_robot',views.create_robot, name='create_robot'),
    path('create_group/<int:game_id>/<int:company_id>',views.create_group, name='create_group'),
    path('join_group/<int:game_id>/<int:company_id>',views.join_group, name='join_group')
]