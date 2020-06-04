from . import *
from background_task import background
import os
from .dropFile import preprocessing

DTM_pickle = '/data/dtm.pkl'
vocab_pickle = '/data/vocab.pkl'
syndict_pickle = '/data/syndict.pkl'
filelist_pickle = '/data/filelist.pkl'


@background(queue='update-queue')
def dropfile_env_update(old_path,new_path):
    # move file into correct position
    os.system("mv {} {}",old_path,new_path)
    root_path = '/storage'
    
    # build new DTM and vocab
    # preprocessing : lookup hierarchy of root path
    directory_dict = defaultdict(list) # empty dictionary for lookup_directory function
    dir_hierarchy = preprocessing.lookup_directory(root_path, directory_dict) # change it to have 2 parameter

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
        pickle.dump(f,DTM)
    with open(syndict_pickle,'wb') as f:
        pickle.dump(f,synonym_dict)
    with open(vocab_pickle,'wb') as f:
        pickle.dump(f,vocab)
    with open(filelist_pickle,'wb') as f:
        pickle.dump(f,file_list)
    
    pid = os.getpid()
    os.system("kill -9 {}".format(pid))
    
    
    
    
    
    