from django.conf.urls import url, include 
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from .views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'dirs', DirectoryViewSet)
router.register(r'files', FileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('show/', dir_hierarchy_show),
    # path('accept-upload/', file_post_accept),
]