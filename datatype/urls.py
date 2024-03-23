from django.urls import path
from .views import view_user_detail,csv_file_upload

from django.urls.resolvers import URLPattern

INFER_ENDPOINT:str = ''

urlpatterns: list[URLPattern] = [
    path('user_detail/',view_user_detail,name="user_detail"),
    path(INFER_ENDPOINT,view=csv_file_upload,name='file_upload')
]