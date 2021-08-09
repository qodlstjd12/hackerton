from django.urls.conf import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'user_info'

urlpatterns=[
    path('', views.home, name = 'home'),
    path('mypage', views.mypage, name = 'mypage'),
    path('login', views.login_view, name = 'login_view'),
    path('signup', views.signup, name = 'signup'),
    path('logout_view/', views.logout_view, name="logout_view"),

    path('sponserpage/', views.sponserpage, name="sponserpage"),
    path('recentView/<str:email>', views.recentView, name="recentView"),
    path('recentDetail/<str:id>', views.recentDetail, name='recentDetail'),
    path('recentWrite/', views.recentWrite, name="recentWrite"),
]
