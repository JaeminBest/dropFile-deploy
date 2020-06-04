from django.db import models

# Create your models here.
class Directory(models.Model):
    id = models.AutoField(primary_key=True, help_text='PK AutoIncrement')
    parent = models.ForeignKey('self',on_delete=models.CASCADE)
    path = models.FilePathField()

class File(models.Model):
    id = models.AutoField(primary_key=True, help_text='PK AutoIncrement')
    name = models.CharField(max_length=200)
    directory = models.ForeignKey('Directory', on_delete=models.CASCADE)
    path = models.FilePathField()
