#django
from django.urls import path
from django.conf.urls import url

from .views import TestColbView, TestCardView, ParCardView

urlpatterns = [    
    url(r'^colb/(?P<id_user>\d+)/$', TestColbView.as_view()),
    url(r'^card/(?P<id_user>\d+)/$', TestCardView.as_view()),    
    url(r'^par/(?P<id_user>\d+)/$', ParCardView.as_view()),    
    ]