from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('<int:game_id>/<int:company_id>/', views.index, name="index"),
    path('<int:game_id>/<int:company_id>/update/', views.update, name="update"),
    path('<int:game_id>/<int:company_id>/<int:turn_num>/wait/',
         views.wait, name="wait"),
    path('create/', views.create, name="create"),
    path('continue/', views.continue_game, name="continue"),
]
