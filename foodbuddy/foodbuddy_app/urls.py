from django.urls import path

from . import views
#File to link between urlpatterns and views
urlpatterns = [
    path('', views.index, name='index'),
    path('res', views.restHome, name="restHome"),
    path('user', views.userHome, name="userHome"),
    path('restadmin', views.restAdmin, name="restadmin"),
    path('acceptofferR', views.acceptofferR, name="acceptR"),
    path('rejectofferR', views.rejectofferR, name="rejectR"),
    path('modifyofferR', views.modifyofferR, name="modifyR"),
    path('adddescrip', views.adddescrip, name="adddescript"),
    path("addrating",views.addrating, name="addrating"),
    path('acceptoffer', views.acceptoffer, name="accept"),
    path('rejectoffer', views.rejectoffer, name="reject"),
    path('usignup', views.usignup, name="usignup"),
    path('ulogin', views.ulogin, name="ulogin"),
    path('rsignup', views.rsignup, name="rsignup"),
    path("reserved_table",views.reserved_table, name="reservedtable"),
    path("logout",views.usr_logout, name="usrlogout"),

    
]
