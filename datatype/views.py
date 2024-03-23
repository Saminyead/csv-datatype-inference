from django.shortcuts import render

import os


# Create your views here.
from django.http import HttpRequest,JsonResponse
import pydantic

from rest_framework import response, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer

from django.core.exceptions import SuspiciousFileOperation

class UserModel(pydantic.BaseModel):
    id: int
    name: str
    email: str


def view_user_detail(request:HttpRequest,user_id:int=500) -> JsonResponse:
    test_user:UserModel = UserModel(
        id=user_id,
        name="Shakira",
        email="hipsdontlie@example.com"
    )

    json_response: str = test_user.model_dump_json()

    return JsonResponse(json_response,safe=False)


@api_view(['POST'])
def csv_file_upload(
        request:request.Request,
        *args,
        **kwargs
) -> Response | None:
    if request.method=='POST':
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save()

            response_data = {
                'file_name': uploaded_file.file.name,
                'uploaded_on': uploaded_file.uploaded_on
            }


            return Response(response_data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
