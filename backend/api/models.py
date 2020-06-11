from django.db import models

# Create your models here.
class Directory(models.Model):
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)
    path = models.CharField(max_length=500,unique=True)

class File(models.Model):
    name = models.CharField(max_length=200)
    directory = models.ForeignKey('Directory', on_delete=models.CASCADE, null=True, blank=True)
    path = models.CharField(max_length=500,unique=True)
    is_post = models.BooleanField(default=False)