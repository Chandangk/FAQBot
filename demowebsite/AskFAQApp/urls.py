from django.conf.urls import url
from . import views

urlpatterns =[
  url(r'^$',views.index,name="index"),
 #question request 
 # url(r'^(?P<question>[A-Za-z]*)$',views.detail,name="detail"),
  url(r'^execution([A-Za-z]*)$',views.executor,name="executor"),
  url(r'^evaluation([A-Za-z]*)$',views.evaluation,name="evaluation"),
  url(r'^first([A-Za-z]*)$',views.firstPage,name="firstPage"),
    url(r'^feedback([A-Za-z]*)$',views.feedback,name="feedback"),
 url(r'^startPage?([A-Za-z=]*)$',views.startPage,name="startPage"),
 url(r'^insertService([A-Za-z= ]*)$',views.insertService,name="insertService"),  
]