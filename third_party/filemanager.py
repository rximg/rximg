import os
import os.path as osp

def get_filelist(path="~"):
    
    if path=="~":
        path = osp.expanduser('~')
    path = os.path.abspath(path)
    path.replace('\\','/')
    if not osp.isdir(path):
        return ValueError('{} is not a exist dir.'.format(path))
    path,  dirs, files = next(os.walk(path))
    # print('get path',path)
    res = [{'value':'..','type':'rollback'}]
    res = res + [ {'value':d,'type':'folder'} for d in dirs]
    res = res + [ {'value':d,'type':'file'} for d in files]
    return res,path
# <a-icon type="rollback" />