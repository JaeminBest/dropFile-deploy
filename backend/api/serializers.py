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
        fields = ['pk','path']

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['pk','path','name']

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class HierarchySerializer(serializers.HyperlinkedModelSerializer):
    children = RecursiveSerializer(many=True)
    files = FileSerializer(many=True)
    
    class Meta:
        model = Directory
        fields = ['pk','path','name','files','children']