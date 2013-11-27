#!/usr/bin/env python
# Site Views and access


Guest = ['signup']
Student = ['failure','workbook','u1','u2', 'signup', 'suc', 'sue', 'suv', 'chk', 'library']
Tutor = ['failure','aue','auv', 'signup']
Admin = ['failure','cloud', 'library', 'admin','adminU','auc','aue','auv', 'users', 'modify', 'signup', 'verification', 'workbook', 'u1',
         'suc', 'sue', 'suv', 'chk', 'loader']



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

    
