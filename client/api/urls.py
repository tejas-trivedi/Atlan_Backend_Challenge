from .views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('slang/', GetSlangView.as_view(), name='slang'),
    path('validateData/', ValidateData.as_view()),
    path('validateAll/', ValidateAll.as_view()),
    path('send/', SendSMS.as_view())

]