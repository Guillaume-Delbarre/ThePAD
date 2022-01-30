from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.detail, name='detail'),
    path('<int:user_id>/points/', views.points, name='points'),
    path('<int:user_id>/attribute', views.attribute, name = 'attribute')
]