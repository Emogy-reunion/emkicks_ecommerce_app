import re

def validate_firstname(firstname):
    '''
    checks to ensure that the first name is in the required format
    '''
    errors = []
    if not firstname:
        errors.append('First name is required!')
    elif len(firstname) < 2:
        errors.append('First name must be at least 2 characters long!')
    elif len(firstname) > 50:
        errors.append('First name must not exceed  30 characters long')
