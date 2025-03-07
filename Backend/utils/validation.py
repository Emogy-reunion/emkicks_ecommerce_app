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
        errors.append('First name must not exceed  30 characters long!')
    return errors


def validate_lastname(lastname):
    '''
    checks to ensure that the last name is in the required format
    '''
    errors = []
    if not lastname:
        errors.append('Last name is required!')
    elif len(lastname) < 2:
        errors.append('Last name must be at least 2 characters long!')
    elif len(lastname) > 50:
        errors.append('Last name must not exceed 30 characters long!'0
    return errors
