from background_task import background
from background_task.models import Task
from collections import defaultdict
import os
import pickle

from . import *
from .dropFile import dropfile
from .models import *

PICKLE_DIR = '/home/data/{}'.format(os.environ.get('PICKLE_DIR'))
DTM_pickle = '{}/dtm.pkl'.format(PICKLE_DIR)
vocab_pickle = '{}/vocab.pkl'.format(PICKLE_DIR)
syndict_pickle = '{}/syndict.pkl'.format(PICKLE_DIR)
token_pickle = '{}/token.pkl'.format(PICKLE_DIR)

@background(queue='update-managing-queue')
def dropfile_env_update_helper(pk):
    task_params = str([[pk],{}])
    target_task = Task.objects.filter(task_params=task_params).all()[0]
    target_task.queue = 'update-queue-{}'.format(pk)
    target_task.save()


@background(queue='update-queue')
def dropfile_env_update(pk):
    if os.path.exists(token_pickle):
        with open(token_pickle,'rb') as f:
            old_T = pickle.load(f)
    
    D,V,S,T = dropfile.prepare_env(PICKLE_DIR,old_T)
    
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
    DTM, vocab, synonym_dict = dropfile.prepare_env('/storage')
    
    with open(DTM_pickle,'wb') as f:
        pickle.dump(DTM,f)
        
    with open(syndict_pickle,'wb') as f:
        pickle.dump(synonym_dict,f)
        
    with open(vocab_pickle,'wb') as f:
        pickle.dump(vocab,f)
    