from django.urls import path
from django.conf.urls.static import static

from HellProject import settings
from . import views

app_name = 'market'

urlpatterns =[
    path('', views.market_view, name='market_view'),
    path('marketDetail/<str:id>', views.market_Detail, name='market_Detail'),
    path('marketWrite/', views.market_Write, name='market_Write'),
    path('marketDelete/<str:id>', views.market_Delete, name='market_Delete'),
]
