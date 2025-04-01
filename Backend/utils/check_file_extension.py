'''
verifies the file extension
'''

def allowed_extension(filename):
    '''
    filename: file to verify it's extension
    '''
    allowed_extensions = ['png', 'jpg', 'jpeg', 'webp']

    if '.' in filename:
        #split the filename and extract the extension
        extension = filename.rsplit('.', 1)[1].lower() 
        if extension in allowed_extensions:
            return True
        else:
            return False
    else:
        return False
