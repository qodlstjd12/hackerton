from django.urls import path
from django.conf.urls.static import static

from HellProject import settings
from . import views

app_name = 'list'

urlpatterns =[
    path('list_view/', views.list_view, name='list_view'),
    path('new/',views.new, name ='new'),
    path('delete/<str:id>', views.delete, name='delete'),
]
