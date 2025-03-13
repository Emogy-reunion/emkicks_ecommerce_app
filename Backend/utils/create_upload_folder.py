'''
creates the upload folder
'''
import os

def create_upload_folder():
    '''
    checks it the uploads folder is available
    if not it is created
    if it exists nothing happens
    '''
    if not os.path.exists('/static/uploads'):
        os.makedirs('/static/uploads')
