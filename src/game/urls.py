from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('best/', views.best, name='best'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/points/', views.PointView.as_view(), name='points'),
    path('<int:player_id>/attribute/', views.attribute, name = 'attribute'),
    path('<int:player_id>/delete', views.delete, name='delete'),
    path('add_player', views.add_player, name="add_player"),
    path('add_action', views.add_action, name="add_action"),
]