from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    path('show_device/', views.show_device, name='show_device'),
    path('config_device/<int:device_id>',
         views.config_device, name='config_device')
]
