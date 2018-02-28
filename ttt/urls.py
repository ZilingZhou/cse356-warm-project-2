from django.urls import path
from . import views
#app_name = 'ttt'
urlpatterns = [
    path('ttt/', views.index,name ='index'),
    path('ttt', views.index,name ='index'),
    path('ttt/play/',views.statefulService),
    path('ttt/play',views.statefulService),
    path('adduser/',views.adduser),
    path('verify/',views.verify),
    path('login/',views.login),
    path('logout/',views.logout),
    path('listgames/',views.listgames),
    path('getgame/',views.getgame),
    path('getscore/',views.getscore),


    path('adduser',views.adduser),
    path('verify',views.verify),
    path('login',views.login),
    path('logout',views.logout),
    path('listgames',views.listgames),
    path('getgame',views.getgame),
    path('getscore',views.getscore),
    #path('test', views.index2,name ='index'),
]

