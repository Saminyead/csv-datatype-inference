from django.db import models

# Create your models here.
class UploadedCSVFile(models.Model):
    file = models.FileField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    original_data_json = models.JSONField(null=True,blank=True)
    original_data_types = models.JSONField(null=True,blank=True)
    original_data_types_readable = models.JSONField(null=True,blank=True)
    inferred_data_json = models.JSONField(null=True,blank=True)
    inferred_data_types = models.JSONField(null=True,blank=True)
    inferred_data_types_readable = models.JSONField(null=True,blank=True)


    def arrange_for_response(self):
        return {
            'metadata': {
                'file_name': self.file.name,
                'uploaded_on': self.uploaded_on,
            },
            'original_data': {
                'original_data_json': self.original_data_json,
                'original_data_types': self.original_data_types,
                'original_data_types_readable': self.original_data_types_readable
            },
            'inferred_data': {
                'inferred_data_json': self.inferred_data_json,
                'inferred_data_types':self.inferred_data_types,
                'inferred_data_types_readable':self.inferred_data_types_readable,
            }
        }