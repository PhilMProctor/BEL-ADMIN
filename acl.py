#!/usr/bin/env python
# Site Views and access


Guest = ['signup']
Student = ['workbook','u1','u2', 'signup']
Tutor = ['au1e','au1v', 'signup']
Admin = ['admin','adminU','au1c','au1e','au1v', 'users', 'modify', 'signup', 'verification', 'workbook', 'u1']



def acl_check(role, page):
    if role == 'Student':
        if page in Student:
            return True
    elif role == 'Admin':
        if page in Admin:
            return True
    elif role == "NoneType":
        if page in Guest:
            return True
    
    return False

    
