import os
import pickle
import secrets

INIT_PICKLE = '/home/data/init.pkl'

def find_db(root_path):
    init_pickle = dict()
    if os.path.exists(INIT_PICKLE):
        with open(INIT_PICKLE,'rb') as f:
            init_pickle = pickle.load(f)
    
    new_path = os.path.abspath(root_path.rstrip('/'))
    if not (new_path in init_pickle):
        init_pickle[new_path] = "/home/data/{}".format(secrets.token_hex(16))
        with open(INIT_PICKLE, 'wb') as f:
            pickle.dump(init_pickle,f)
    
    target_db = init_pickle[new_path]
    os.makedirs(target_db,exist_ok=True)
    os.environ['STORAGE_DIR'] = new_path
    os.environ['PICKLE_DIR'] = target_db
    
    return target_db
    
