from django.urls.conf import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'inquiry'

urlpatterns=[
    path('CS/', views.CS, name = 'CS'),
    path('FAQ/', views.FAQ, name = 'FAQ'),
]
