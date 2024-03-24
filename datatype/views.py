from django.shortcuts import render
from django.core.files.uploadedfile import UploadedFile

# Create your views here.
from rest_framework import request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import UploadedCSVFile
from .serializers import FileUploadSerializer
from .utils.infer_all import infer_all


def _check_csv(file:UploadedFile) -> bool:
    """Check if uploaded file is CSV"""
    file_name_split:list[str] = file.name.split('.')
    if file_name_split[-1] == 'csv':
        return True


@api_view(['POST'])
def csv_file_upload(
        request:request.Request,
        *args,
        **kwargs
) -> Response | None:
    if request.method=='POST':
        serializer = FileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            file:UploadedFile = serializer.validated_data['file']


            data_types = infer_all(file.name)

            uploaded_file = UploadedCSVFile.objects.create(
                file=file,
                original_data_types=data_types['original'],
                inferred_data_types=data_types['inferred']
            )

            response_data = {
                'metadata': {
                    'file_name': uploaded_file.file.name,
                    'uploaded_on': uploaded_file.uploaded_on,
                    'original_data_types':uploaded_file.original_data_types,
                    'inferred_data_types':uploaded_file.inferred_data_types
                },

            }


            return Response(response_data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
