from .models import Directory,File
from .dropFile.dropfile import prepare_env
import pickle
import os

STORAGE_DIR = os.environ.get('STORAGE_DIR')
PICKLE_DIR = os.environ.get('PICKLE_DIR')
DTM_pickle = '{}/dtm.pkl'.format(PICKLE_DIR)
vocab_pickle = '{}/vocab.pkl'.format(PICKLE_DIR)
syndict_pickle = '{}/syndict.pkl'.format(PICKLE_DIR)
token_pickle = '{}/token.pkl'.format(PICKLE_DIR)
watch_pickle = '{}/watch.pkl'.format(PICKLE_DIR)
WATCHER_DIR = os.environ.get('WATCH')


def default_db_update():
    root_path = '/storage'
    is_change = False
    for dirobj in Directory.objects.all():
        if not os.path.isdir(dirobj.path.replace('/storage',STORAGE_DIR)):
            is_change = True
            dirobj.delete()
    for fileobj in File.objects.all():
        if not os.path.isfile(fileobj.path.replace('/storage',STORAGE_DIR)):
            is_change = True
            fileobj.delete()
    
    if os.environ.get('WATCH'):
        watch_path = '/watch'
        filelist = list()
        for root,dirs,files in os.walk(watch_path):
            if (root==watch_path):
                for file in files:
                    filelist.append(file)
        with open(watch_pickle,'wb') as f:
            pickle.dump(filelist,f)
  
    for root, dirs, files in os.walk(root_path):
        parent = None
        if (root!=root_path):
            try:
                parent = Directory.objects.filter(path=root.replace('/storage',STORAGE_DIR)).all()[0]
            except:
                print("invalid update")
                break
      
        for dir in dirs:
            path = os.path.join(root,dir)
            new_path = path.replace('/storage',STORAGE_DIR)
            if not Directory.objects.filter(parent=parent,name=dir,path=new_path).all():
                is_change = True
                new = Directory(parent=parent,name=dir,path=new_path)
                new.save()
        for file in files:
            path = os.path.join(root,file)
            new_path = path.replace('/storage',STORAGE_DIR)
            if not File.objects.filter(directory=parent,name=file,path=new_path,is_post=True).all():
                is_change = True
                new = File(directory=parent,name=file,path=new_path,is_post=True)
                new.save()
  
    if is_change:
        if os.path.exists(token_pickle):
            with open(token_pickle,'rb') as f:
                old_T = pickle.load(f)
            D,V,S,T = prepare_env(root_path, old_T)
        else:
            D,V,S,T = prepare_env(root_path)
        
        with open(DTM_pickle,'wb') as f:
            pickle.dump(D,f)
        with open(syndict_pickle,'wb') as f:
            pickle.dump(S,f)
        with open(vocab_pickle,'wb') as f:
            pickle.dump(V,f)
        with open(token_pickle,'wb') as f:
            pickle.dump(T,f)



PICKLE_DIR = os.environ.get('PICKLE_DIR')
watch_pickle = '{}/watch.pkl'.format(PICKLE_DIR)

def update_filelist():
    cur_filelist = list()
    for root,dirs,files in os.walk('/watch'):
        if (root==watch_path):
            for file in files:
                cur_filelist.append(file)
    with open(watch_pickle,'wb') as f:
        pickle.dump(cur_filelist,f)