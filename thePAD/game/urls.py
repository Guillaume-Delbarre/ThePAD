from django.urls import path

from . import views

app_name = 'game'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/points/', views.PointView.as_view(), name='points'),
    path('<int:user_id>/attribute/', views.attribute, name = 'attribute')
]