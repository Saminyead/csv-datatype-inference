from django.db import models

# Create your models here.
class UploadedCSVFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    original_data_types = models.JSONField(null=True,blank=True)
    inferred_data_types = models.JSONField(null=True,blank=True)