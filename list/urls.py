from django.urls import path
from django.conf.urls.static import static

from HellProject import settings
from . import views

app_name = 'list'

urlpatterns =[
    path('list_view/', views.list_view, name='list_view'),
    path('list_view/feed_Deatil/<str:id>', views.feed_Detail, name='feed_Detail'),

    path('delete/<str:id>', views.delete, name='delete'),
    path('ask/',views.ask, name='ask'),
    path('recentView/', views.recentview, name='recentView'),
    path('recentWrite/', views.recentWrite, name='recentWrite'),
    path('helpWrite/', views.helpWrite, name='helpWrite'),
]
