from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:player_id>/', views.detail, name='detail'),
    path('<int:player_id>/delete', views.delete, name='delete'),
    path('add_action', views.add_action, name="add_action"),
]