from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import *

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'directories', DirectoryViewSet)
router.register(r'files', FileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('file/post', file_post),
    path('file/accept', file_post_accept),
    path('file/delete', file_delete),
    path('file/move', file_move),
    path('dir/show', dir_hierarchy_show),
    path('dir/delete', dir_delete),
    path('dir/create', dir_create),
]