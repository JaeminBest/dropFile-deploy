from .models import Directory,File
from .dropfile.dropfile import prepare_env

PICKLE_DIR = '/home/data/{}'.format(os.environ.get('PICKLE_DIR'))
DTM_pickle = '{}/dtm.pkl'.format(PICKLE_DIR)
vocab_pickle = '{}/vocab.pkl'.format(PICKLE_DIR)
syndict_pickle = '{}/syndict.pkl'.format(PICKLE_DIR)
token_pickle = '{}/token.pkl'.format(PICKLE_DIR)


def default_db_update():
    root_path = '/storage'
    is_change = False
    for dirobj in Directory.objects.all():
        if not os.path.isdir(dirobj.path):
            is_change = True
            dirobj.delete()
    for fileobj in File.objects.all():
        if not os.path.isfile(fileobj.path):
            is_change = True
            fileobj.delete()
            
  
    for root, dirs, files in os.walk(root_path):
        parent = None
        if (root!=root_path):
            try:
                parent = Directory.objects.filter(path=root).all()[0]
            except:
                print("invalid update")
                break
      
    for dir in dirs:
        path = os.path.join(root,dir)
        if not Directory.objects.filter(parent=parent,name=dir,path=path).all():
            is_change = True
            new = Directory(parent=parent,name=dir,path=path)
            new.save()
    for file in files:
        path = os.path.join(root,file)
        if not File.objects.filter(directory=parent,name=file,path=path,is_post=True).all():
            is_change = True
            new = File(directory=parent,name=file,path=path,is_post=True)
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
    