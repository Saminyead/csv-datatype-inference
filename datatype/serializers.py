from typing import Literal
from rest_framework import serializers
from .models import UploadedFile

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields: tuple[str] = ('file','uploaded_on')  # type: ignore
