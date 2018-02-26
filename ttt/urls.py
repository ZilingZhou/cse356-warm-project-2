from django.urls import path
from . import views
#app_name = 'ttt'
urlpatterns = [
    path('', views.index,name ='index'),
    path('play/',views.service),
    path('play',views.service),
    #path('test', views.index2,name ='index'),
]

