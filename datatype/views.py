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


def _check_csv(file:UploadedFile) -> bool|Response:
    """Check if uploaded file is CSV"""
    file_name_split:list[str] = file.name.split('.')
    if file_name_split[-1] == 'csv':
        return True
    else:
        return False


@api_view(['POST'])
def csv_file_upload(
        request:request.Request,
        *args,
        **kwargs
) -> Response | None:
    if request.method=='POST':
        serializer = FileUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file:UploadedFile = serializer.validated_data['file']
        
        if not _check_csv(file):
            return Response(
                f"The uploaded file {file} is not a CSV file",
                status.HTTP_400_BAD_REQUEST
            )

        data_types = infer_all(file)

        uploaded_file = UploadedCSVFile.objects.create(
            file=file,
            original_data_types=data_types['original'],
            inferred_data_types=data_types['inferred']
        )

        response_data = uploaded_file.arrange_for_response()


        return Response(response_data,status=status.HTTP_201_CREATED)
        