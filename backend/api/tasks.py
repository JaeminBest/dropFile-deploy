from background_task import background
from background_task.models import Task
from collections import defaultdict
import os
import pickle

from . import *
from .dropFile import dropfile
from .models import *

PICKLE_DIR = os.environ.get('PICKLE_DIR')
WATCHER_DIR = os.environ.get('WATCH')
DTM_pickle = '{}/dtm.pkl'.format(PICKLE_DIR)
vocab_pickle = '{}/vocab.pkl'.format(PICKLE_DIR)
syndict_pickle = '{}/syndict.pkl'.format(PICKLE_DIR)
token_pickle = '{}/token.pkl'.format(PICKLE_DIR)
watch_pickle = '{}/watch.pkl'.format(PICKLE_DIR)

@background(queue='watcher-queue')
def dropfile_watcher():
    old_filelist = list()
    if os.path.exists(watch_pickle):
        with open(watch_pickle,'rb') as f:
            old_filelist = pickle.load(f)
        cur_filelist = list()
        for root,dirs,files in os.walk('/watch'):
            if (root==watch_path):
                for file in files:
                    cur_filelist.append(file)
        oldset = set(old_filelist)
        curset = set(cur_filelist)
        new = list(curset.difference(oldset))
        
        if new:
            # load DTM matrix
            DTM = None
            if os.path.exists(DTM_pickle):
                with open(DTM_path,'rb') as f:
                    DTM = pickle.load(f)
            # load voacbulary list
            vocab = None
            if os.path.exists(vocab_pickle):
                with open(vocab_pickle,'rb') as f:
                    vocab = pickle.load(f)
            # load syndict
            syndict = None
            if os.path.exists(syndict_pickle):
                with open(syndict_pickle,'rb') as f:
                    syndict = pickle.load(f)
            
            for el in new:
                fpath = os.path.join('/watch',el).rstrip('/')
                new_dir_path,_,_,_ = dropfile.dropfile(fpath,'/storage',DTM,vocab,syndict,verbose=False)
                new_file = File(name=el,path=fpath.replace('/watch',WATCHER_DIR),temp_path = new_dir_path)
                new_file.save()
    else:
        return
    

@background(queue='update-managing-queue')
def dropfile_env_update_helper(pk):
    task_params = '[["{}"], {{}}]'.format(pk)
    target_task = Task.objects.filter(task_name="backend.api.tasks.dropfile_env_update",task_params=task_params).all()[0]
    target_task.queue = 'update-queue-{}'.format(pk)
    target_task.save()


@background(queue='update-queue')
def dropfile_env_update(pk):
    if os.path.exists(token_pickle):
        with open(token_pickle,'rb') as f:
            old_T = pickle.load(f)
        D,V,S,T = dropfile.prepare_env('/storage',old_T)
    else:
        D,V,S,T = dropfile.prepare_env('/storage')
    
    with open(DTM_pickle,'wb') as f:
        pickle.dump(D,f)
        
    with open(syndict_pickle,'wb') as f:
        pickle.dump(S,f)
        
    with open(vocab_pickle,'wb') as f:
        pickle.dump(V,f)
    
    with open(token_pickle,'wb') as f:
        pickle.dump(T,f)
    
    if pk!=0:
        Task.objects.filter(queue='update-queue-{}'.format(pk)).delete() #clear queue
        pid = os.getpid()
        os.system("kill -9 {}".format(pid))


def dropfile_env_quick_update():
    if os.path.exists(token_pickle):
        with open(token_pickle,'rb') as f:
            old_T = pickle.load(f)
        D,V,S,T = dropfile.prepare_env('/storage',old_T)
    else:
        D,V,S,T = dropfile.prepare_env('/storage')
    
    with open(DTM_pickle,'wb') as f:
        pickle.dump(D,f)
        
    with open(syndict_pickle,'wb') as f:
        pickle.dump(S,f)
        
    with open(vocab_pickle,'wb') as f:
        pickle.dump(V,f)
    
    with open(token_pickle,'wb') as f:
        pickle.dump(T,f)

