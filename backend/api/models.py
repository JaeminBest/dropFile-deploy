from django.db import models

# Create your models here.
class Directory(models.Model):
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="children")
    path = models.CharField(max_length=500,unique=True)
    name = models.CharField(max_length=200)

class File(models.Model):
    name = models.CharField(max_length=200)
    directory = models.ForeignKey('Directory', on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="files")
    path = models.CharField(max_length=500,unique=True)
    temp_dir_path = models.CharField(max_length=500,null=True,blank=True,default=None)
    is_post = models.BooleanField(default=False)