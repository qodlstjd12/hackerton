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
    path('findID/', views.findID, name='findID'),
    path('registerauth/', views.get_success_url, name='register_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),

    path('recovery/pw/', views.RecoveryPwView.as_view(), name='recovery_pw'),
    path('recovery/pw/find/', views.ajax_find_pw_view, name='ajax_pw'),
    path('recovery/pw/auth/', views.auth_confirm_view, name='recovery_auth'),
    path('recovery/pw/reset/', views.auth_pw_reset_view, name='recovery_pw_reset'),

    path('profile_view/', views.profile_view, name='profile_view'),
    path('profile_update_view/', views.profile_update_view, name='profile_update_view'),
    path('verify/', views.verify, name='verify'),
    path('sponserpage/', views.sponserpage, name="sponserpage"),

    path('recentView/<str:email>', views.recentView, name="recentView"),
    path('recentDetail/<str:id>', views.recentDetail, name='recentDetail'),
    path('recentWrite/', views.recentWrite, name="recentWrite"),
    path('recentWriteUpdate/<str:id>', views.recentWriteUpdate, name="recentWriteUpdate"),
]
