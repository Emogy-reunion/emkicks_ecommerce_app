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
    upload_path = os.path.join(os.getcwd(), 'static', 'uploads')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
