#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIDS WING ATTENDANCE PROGRAM V0.01 PREALPHA
Created on Tue Nov 24 23:06:18 2020

@author: pi
"""
on = True
#when toggled false, will initiate shutdown
workweek = ('Monday','Tuesday','Wednesday','Thursday','Friday')
#tuple to convert numeral days to words
userno = 0 
#placeholder for telegram usernumber
userbase = {}
def turnonoff():
    #admin function
    global on
    on = not on

def singlevariableselect(variable):
    confirm = True
    while confirm:
        print('May I have your',variable,'?')
        entry = input()
        print('May I confirm that your',variable,'is',entry,'?(y/n)')
        yesno = input()
        if yesno.lower() == 'y':
            print('Roger!')
            confirm = False
            return entry

def multioptionselect(variable,*options):
    confirm = True
    while confirm:
        print('May I have your',variable,'?')
        count = 0
        for option in options:
            count += 1
            print(option,':',count)
        try:
            optionno = int(input('Option number: '))
        except ValueError:
            print('Please enter a number!')
        else:
            if optionno < 1 or optionno > count:
                print('Please enter a number ranging from 1 to',count,'!')
            else:
                print('May I confirm that your',variable,'is',options[optionno - 1],'?(y/n)')
                yesno = input()
                if yesno.lower() == 'y':
                    print('Roger!')
                    confirm = False
                    return options[optionno - 1]

def setup():
    #called when /start or reconfiguring settings
    global userno
    global userbase
    usernum = str(userno)
    userno += 1
    print('Do not worry about entering the right case, it is automatic!\n')
    nickname = singlevariableselect('preferred nickname')
    rank = singlevariableselect('abbreviated rank').upper()
    name = singlevariableselect('full name').title()
    service = multioptionselect('service status','REG','NSF')
    if nickname.upper() == 'ADMIN' or nickname.upper() == 'SUPERADMIN':
        passkey = input('ADMIN access requested. Enter password: ')
        if passkey == 'Midswing123':
            print('Roger. Recognised as ADMIN. Please enter actual nickname')
            admin = True
            sadmin = False
            nickname = singlevariableselect('actual nickname')
        elif passkey == 'IatoaoK2':
            print('Roger. Recognised as SUPERADMIN. Please enter actual nickname')
            admin = True
            sadmin = True
            nickname = singlevariableselect('actual nickname')
        else:
            print('Incorrect password. Please do not enter ADMIN as nickname!')
            nickname = singlevariableselect('preferred nickname')
            admin = True
            sadmin = True
    else:
        admin = False
        sadmin = False
    print('Confirming particulars...')
    print('Nickname =', nickname)
    print('Rank =', rank)
    print('Name =', name)
    print('Service status =', service)
    if admin == True:
        print('ADMIN access =', admin)
        print('SUPERADMIN access =', sadmin)
    yesno = input('Confirm?(y/n)')
    if yesno == 'y':
        print('YAY! :D Now submitting your information,', nickname, '.')
        userbase.update({usernum: [[nickname,rank,name,service,admin,sadmin]]})

'''to be done before ALPHA
telegram functionality
actual reminder function
database system
admin access tools
superadmin access tools
'''
