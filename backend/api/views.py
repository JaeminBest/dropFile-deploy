from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404
from background_task.models import Task

import secrets
import os
import pickle
import json
import shutil

from . import add_access_control_headers
from .models import Directory, File
from .utils import update_filelist
from .serializers import UserSerializer, DirectorySerializer, FileSerializer, HierarchySerializer
from .dropFile import dropfile
from .tasks import dropfile_env_update_helper,dropfile_env_quick_update,dropfile_env_update

DATA_DIR = os.environ['PICKLE_DIR']
STORAGE_DIR = os.environ['STORAGE_DIR']
DTM_path = os.path.join(DATA_DIR,'dtm.pkl')
VOCAB_path = os.path.join(DATA_DIR,'vocab.pkl')
FLST_path = os.path.join(DATA_DIR,'filelist.pkl')
SYNDICT_path = os.path.join(DATA_DIR,'syndict.pkl')

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class DirectoryViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer
    
    '''
    directory delete overwrite
    '''
    def destroy(self,request,pk=None):
        directory = self.get_object()
        path = directory.path
        shutil.rmtree(path.replace(STORAGE_DIR,'/storage'))
        for file in directory.files.all():
            file.delete()
        directory.delete()
        dropfile_env_quick_update() # not background
        
        return Response({'status':'ok'})
    
    '''
    directory create overwrite
    '''
    @csrf_exempt
    def create(self,request):
        queries = request.POST
        new_path = queries['path'].rstrip('/')
        name = new_path.split('/')[-1]
        parent_path = "/".join(new_path.split('/')[:-1])
        try:
            parent = None if parent_path == STORAGE_DIR \
                        else Directory.objects.filter(path=parent_path).all()[0]
        except:
            return Response({'status':'no'})
        
        new_dir = Directory(parent=parent,path=new_path,name=name)
        os.makedirs(new_path.replace(STORAGE_DIR,'/storage'),exist_ok=True)
        new_dir.save()
        return Response({'status':'ok'})


    '''
    directory move
    '''
    @action(methods=['get'], detail=True, url_path='move', url_name='move')
    def dir_move(self,request,pk=None):
        queries = request.GET
        dirobj = self.get_object()
        new_path = queries['path'].rstrip('/').strip()
        old_path = dirobj.path.replace(STORAGE_DIR,'/storage')

        # dirobj query
        try:
            target_dirobj = Directory.objects.filter(new_path=new_path).all()[0]
        except:
            return Response({'status':'no'})
        
        # storage change
        shutil.copytree(old_path,new_path.replace(STORAGE_DIR,'/storage'))
        for file in dirobj.file_set.all():
            file.directory = target_dirobj
            file.path = target_dirobj.path+'/'+file.name
            file.save()
        
        dropfile_env_quick_update() # not background
        
        return Response({'status':'ok'})


    
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    
    '''
    file list overwrite
    '''
    def list(self,request):
        queryset = File.objects.filter(is_post=True).all()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

    '''
    file delete overwrite
    '''
    def destroy(self,request,pk=None):
        file = self.get_object()
        path = file.path.replace(STORAGE_DIR,'/storage')
        os.remove(path)
        file.delete()
        dropfile_env_update(0)
        dropfile_env_update_helper(0)
        return Response({'status':'ok'})

    '''
    file upload and recommend path
    '''
    @action(methods=['post'], detail=False, url_path='pre-upload', url_name='pre-upload')
    @csrf_exempt
    def file_post(self,request):
        files = request.FILES
        fs = FileSystemStorage()
        if (len(files)!=1):
            result = dict()
            result['path'] = None
            response = HttpResponse(json.dumps(result), content_type=u"application/json; charset=utf-8")
            add_access_control_headers(response)
            return response
        for key in files:
            fileobj = files[key]
            fname = fileobj.name
            fpath = DATA_DIR+'/{}.pdf'.format(secrets.token_hex(16))
            fs.save(fpath,fileobj)
        
        # load DTM matrix
        DTM = None
        if os.path.exists(DTM_path):
            with open(DTM_path,'rb') as f:
                DTM = pickle.load(f)
        # load voacbulary list
        vocab = None
        if os.path.exists(VOCAB_path):
            with open(VOCAB_path,'rb') as f:
                vocab = pickle.load(f)
        # load syndict
        syndict = None
        if os.path.exists(SYNDICT_path):
            with open(SYNDICT_path,'rb') as f:
                syndict = pickle.load(f)
        
        new_dir_path,_,_,_ = dropfile.dropfile(fpath,'/storage',DTM,vocab,syndict,verbose=False)
        
        # add to DB
        new_file = File(name=fname,path=fpath)
        new_file.save()
        
        # background task
        dropfile_env_update(new_file.pk)
        dropfile_env_update_helper(new_file.pk) # add new task
        
        result = dict()
        result['pk'] = new_file.pk
        result['name'] = new_file.name
        result['new_dir_path'] = new_dir_path.replace('/storage',STORAGE_DIR)
        response = HttpResponse(json.dumps(result), content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response


    '''
    set upload path and upload
    '''
    @action(methods=['get'], detail=True, url_path='accept-upload', url_name='accept-upload')
    def file_post_accept(self,request,pk=None):
        queries = request.GET
        fileobj = File.objects.get(pk)
        if fileobj is None:
            return Response({'status':'no'})
        new_dir_path = queries['new_dir_path'].rstrip('/')
        old_path = fileobj.path
        if not os.path.isdir(str(new_dir_path)):
            return Response({'status':'no'})
        new_path = os.path.join(new_dir_path,fileobj.name)
        try:
            dirobj = Directory.objects.filter(path=new_dir_path).all()[0]
        except:
            return Response({'status':'no'})
        
        # update info
        fileobj.directory = dirobj
        fileobj.path = new_path
        fileobj.is_post = True
        fileobj.temp_path = None
        try:
            fileobj.save()
            shutil.move(old_path.replace(STORAGE_DIR,'/storage'),new_path.replace(STORAGE_DIR,'/storage'))
            if os.environ.get('WATCH'):
                update_filelist()
        except:
            return Response({'status':'no'})
        
        # execute background task - DTM building and preprocessing
        os.system("nohup python manage.py process_tasks --queue=update-queue-{} &".format(pk))
        
        return Response({'status':'ok'})

    '''
    move file to another directory
    '''
    @action(methods=['get'], detail=True, url_path='move', url_name='move')
    def file_move(self,request,pk=None):
        queries = request.GET
        fileobj = File.objects.get(pk)
        if fileobj is None:
            return Response({'status':'no'})
        if fileobj.is_post:
            dir_path = queries['new_dir_path']
            new_path = os.path.join(dir_path.replace(STORAGE_DIR,'/storage'),fileobj.name)
            try:
                dirobj = Directory.objects.filter(path=dir_path).all()[0]
            except:
                return Response({'status':'no'})
            try:
                shutil.move(fileobj.path.replace(STORAGE_DIR,'/storage'),new_path)
            except:
                return Response({'status':'no'})
            fileobj.path = new_path
            fileobj.directory = dirobj
            fileobj.save()
            
            return Response({'status':'ok'})
        else:
            return Response({'status':'no'})



'''
file and directory hierarchy show
'''
def dir_hierarchy_show(request):
    if request.method == 'GET':
        queryset = Directory.objects.filter(parent=None).all()
        result = dict()
        serializer = HierarchySerializer(queryset,many=True)
        result['items'] = serializer.data
        result['parent_path'] = os.environ['ROOT']
        response = HttpResponse(json.dumps(result), content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response
    else:
        response = HttpResponse({'status':'no'}, content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response

'''
file and directory hierarchy show
'''
def dropfile_queue_show(request):
    if request.method == 'GET':
        queryset = File.objects.filter(is_post=False).all()
        result = dict()
        serializer = FileSerializer(queryset,many=True)
        result['items'] = serializer.data
        result['parent_path'] = os.environ['WATCH']
        response = HttpResponse(json.dumps(result), content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response
    else:
        response = HttpResponse({'status':'no'}, content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response