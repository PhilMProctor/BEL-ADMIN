#!/usr/bin/env python
# Site Views and access

Student = ['workbook','u1','u2']
Tutor = ['au1e','au1v']
Admin = ['admin','adminU','au1c','au1e','au1v', 'users', 'modify']



def acl_check(role, page):
    if role == 'Student':
        if page in Student:
            return True
    elif role == 'Admin':
        if page in Admin:
            return True
    return False

    
