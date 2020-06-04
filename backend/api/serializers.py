from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Directory,File

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class DirectorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Directory
        fields = ['name','path']

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['name','directory']
