from typing import Literal
from rest_framework import serializers
from .models import UploadedCSVFile

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedCSVFile
        fields: tuple[str] = ('file','uploaded_on')  # type: ignore
