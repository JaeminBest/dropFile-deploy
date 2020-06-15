from background_task import background
from background_task.models import Task
from collections import defaultdict
import os
import pickle

from . import *
from .dropFile import dropfile
from .models import *

DTM_pickle = '/home/data/dtm.pkl'
vocab_pickle = '/home/data/vocab.pkl'
syndict_pickle = '/home/data/syndict.pkl'
filelist_pickle = '/home/data/filelist.pkl'

@background(queue='update-managing-queue')
def dropfile_env_update_helper(pk):
    task_params = str([[pk],{}])
    target_task = Task.objects.filter(task_params=task_params).all()[0]
    target_task.queue = 'update-queue-{}'.format(pk)
    target_task.save()


@background(queue='update-queue')
def dropfile_env_update(pk):
    DTM, vocab, synonym_dict = dropfile.prepare_env('/storage')
    
    with open(DTM_pickle,'wb') as f:
        pickle.dump(DTM,f)
        
    with open(syndict_pickle,'wb') as f:
        pickle.dump(synonym_dict,f)
        
    with open(vocab_pickle,'wb') as f:
        pickle.dump(vocab,f)
    
    
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
    