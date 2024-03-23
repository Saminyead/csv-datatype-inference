from django.db import models

from .utils.inference import (
    infer_datetime,infer_numeric
)

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)


# TODO: a model for the original data types
    # - a model for the converted data types

class OriginalDataTypes(models.Model):
    ...


class InferredDataTypes(models.Model):
    ...