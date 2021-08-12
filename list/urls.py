from django.urls import path
from django.conf.urls.static import static

from HellProject import settings
from . import views

app_name = 'list'

urlpatterns =[
    path('list_view/', views.list_view, name='list_view'),

    path('helpWrite/', views.helpWrite, name='helpWrite'),
    path('helpUpdate/<str:id>', views.helpUpdate, name='helpUpdate'),
    path('helpDelete/<str:id>', views.helpDelete, name='helpDelete'),
    
    path('feed_Deatil/<str:id>', views.feed_Detail, name='feed_Detail'),
    path('donate/<str:id1>/<str:id2>/<str:id3>', views.donate, name='donate'),
]

