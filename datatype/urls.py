from django.urls import path
from .views import csv_file_upload

from django.urls.resolvers import URLPattern

INFER_ENDPOINT:str = ''

urlpatterns: list[URLPattern] = [
    path(INFER_ENDPOINT,view=csv_file_upload,name='file_upload')
]