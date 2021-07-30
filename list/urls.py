from django.urls import path

from . import views

app_name = 'list'

urlpatterns =[
    path('list_view/', views.list_view, name='list_view')
]