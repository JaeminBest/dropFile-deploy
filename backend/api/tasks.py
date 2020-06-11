from background_task import background
from background_task.models import Task
from collections import defaultdict
import os
import pickle

from . import *
from .dropFile import preprocessing
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
    # build new DTM and vocab
    # preprocessing : lookup hierarchy of root path
    directory_dict = defaultdict(list) # empty dictionary for lookup_directory function
    dir_hierarchy = preprocessing.lookup_directory('/storage', directory_dict) # change it to have 2 parameter

    file_list = list()
    dir_list = list()
    label_num = 0
    for tar_dir in dir_hierarchy:
        file_list += dir_hierarchy[tar_dir]
        dir_list.append(tar_dir)
        label_num += 1
        
    # preprocessing : build vocabulary from file_list
    doc_list = list()
    for file in file_list:
        doc_list.append(preprocessing.file2tok(file))
    vocab, synonym_dict = preprocessing.build_vocab(doc_list)
    
    # preprocessing : build DTM of files under root_path
    DTM = preprocessing.build_DTM(doc_list, vocab, synonym_dict)
    
    with open(DTM_pickle,'wb') as f:
        pickle.dump(DTM,f)
        
    with open(syndict_pickle,'wb') as f:
        pickle.dump(synonym_dict,f)
        
    with open(vocab_pickle,'wb') as f:
        pickle.dump(vocab,f)
        
    with open(filelist_pickle,'wb') as f:
        pickle.dump(file_list,f)
    
    if pk!=0:
        Task.objects.filter(queue='update-queue-{}'.format(pk)).delete() #clear queue
        pid = os.getpid()
        os.system("kill -9 {}".format(pid))


def dropfile_env_quick_update():
    # build new DTM and vocab
    # preprocessing : lookup hierarchy of root path
    directory_dict = defaultdict(list) # empty dictionary for lookup_directory function
    dir_hierarchy = preprocessing.lookup_directory('/storage', directory_dict) # change it to have 2 parameter

    file_list = list()
    dir_list = list()
    label_num = 0
    for tar_dir in dir_hierarchy:
        file_list += dir_hierarchy[tar_dir]
        dir_list.append(tar_dir)
        label_num += 1
        
    # preprocessing : build vocabulary from file_list
    doc_list = list()
    for file in file_list:
        doc_list.append(preprocessing.file2tok(file))
    vocab, synonym_dict = preprocessing.build_vocab(doc_list)
    
    # preprocessing : build DTM of files under root_path
    DTM = preprocessing.build_DTM(doc_list, vocab, synonym_dict)
    
    with open(DTM_pickle,'wb') as f:
        pickle.dump(DTM,f)
        
    with open(syndict_pickle,'wb') as f:
        pickle.dump(synonym_dict,f)
        
    with open(vocab_pickle,'wb') as f:
        pickle.dump(vocab,f)
        
    with open(filelist_pickle,'wb') as f:
        pickle.dump(file_list,f)