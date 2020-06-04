from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from background_task import Tasks

import secrets
import os
import subprocess
import pickle

from .models import Directory, File
from .serializers import UserSerializer, DirectorySerializer, FileSerializer
from .dropFile import dropfile
from .tasks import dropfile_env_update

TMP_DIR = '/data'
STORAGE_DIR = '/storage'
DTM_path = os.path.join(TMP_DIR,'dtm.pkl')
VOCAB_path = os.path.join(TMP_DIR,'vocab.pkl')
FLST_path = os.path.join(TMP_DIR,'filelist.pkl')
SYNDICT_path = os.path.join(TMP_DIR,'syndict.pkl')

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class DirectoryViewSet(viewsets.ModelViewSet):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer
    
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


'''
file upload and recommend path
'''
def file_post(request):
    if request.method=='POST':
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
            fpath = TMP_DIR+'/{}.pdf'.format(secrets.token_hex(16))
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
        # load file list
        flst = None
        if os.path.exists(FLST_path):
            with open(FLST_path,'rb') as f:
                flst = pickle.load(f)
        # load syndict
        syndict = None
        if os.path.exists(SYNDICT_path):
            with open(SYNDICT_path,'rb') as f:
                flst = pickle.load(f)
        
        new_dir_path,_,_ = dropfile.dropfile(fpath,STORAGE_DIR,DTM,vocab,syndict,flst)
        # empty tasks. 
        # This web application is for single person, therfore only consider case that no multi-access occur
        Tasks.objects.all().delete() 
        # background task
        dropfile_env_update(fpath,os.path.join(new_dir_path,fname)) # add new task
        
        result = dict()
        result['path'] = fpath
        response = HttpResponse(json.dumps(result), content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response
    else:
        result = dict()
        result['path'] = None
        response = HttpResponse(json.dumps(result), content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response


'''
set upload path and upload
'''
def file_post_accept(request):
    if request.method=='GET':
        queries = request.GET
        file_path = queries['path']
        
        # execute background task
        os.system("nohup python manage.py process_tasks --queue=update_queue &")
        name = file_path.split('/')[-1]
        
        # parse directory
        dir_path = file_path.split('/')[:-1]
        directory = Directory.objects.filter(path=dir_path)
        
        # add to DB
        new_file = File(name=name,path=file_path,directory=directory)
        new_file.save()
        
        result = dict()
        result['flag'] = True
        response = HttpResponse(json.dumps(result), content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response
    else:
        result = dict()
        result['flag'] = False
        response = HttpResponse(json.dumps(result), content_type=u"application/json; charset=utf-8")
        add_access_control_headers(response)
        return response
    
    
'''
delete file
'''
def file_delete(request):
    return
    


'''
move file
'''
def file_move(request):
    return


'''
file and directory hierarchy show
'''
def dir_hierarchy_show(request):
    return
    
    
'''
file and directory hierarchy show
'''
def dir_delete(request):
    return

'''
file and directory hierarchy show
'''
def dir_create(request):
    return
    