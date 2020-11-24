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
def turnonoff():
    #admin function
    global on
    on = not on

def singlevariableselect(variable):
    confirm = True
    while confirm:
        print('May I have your',variable,'?')
        entry = input()
        entry = entry.upper()
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
    nickname = singlevariableselect('preferred nickname')
    rank = singlevariableselect('abbreviated rank')
    name = singlevariableselect('full name')
    service = multioptionselect('service status','REG','NSF')
    print('There are 2 options for the Parade State reminders, Daily and Weekly.')
    print('Option 1 (Daily) will message you on every workday at 0800H on your presence in OCS HQ(or reason of absence).')
    print('Option 2 (Weekly) will message you in the weekend on your attendance pattern for the entire work week. In case of emergency, in the weekday you are still able to change your attendance options.')
    reminderstate = multioptionselect('preferred reminder option','Daily','Weekly')
    if reminderstate == 'Weekly':
        reminderstate = multioptionselect('preferred weekly option','WeeklySaturday','WeeklySunday')
    if nickname == 'ADMIN':
        passkey = input('ADMIN access requested. Enter password: ')
        if passkey == 'Midswing123':
            print('Roger. Recognised as ADMIN.')
            admin = True
            sadmin = False
            nickname = 'ADMIN'
        elif passkey == 'IatoaoK2':
            print('Roger. Recognised as SUPERADMIN.')
            admin = True
            sadmin = True
            nickname = 'SUPERADMIN'
        else:
            print('Incorrect password. Please do not enter ADMIN as nickname!')
            nickname = singlevariableselect('preferred nickname')
    else:
        admin = False
        sadmin = False
    print('Confirming particulars...')
    print('Nickname =', nickname)
    print('Rank =', rank)
    print('Name =', name)
    print('Service status =', service)
    print('Reminder option =', reminderstate)
    if admin == True:
        print('ADMIN access =', admin)
        print('SUPERADMIN access =', sadmin)
    yesno = input('Confirm?(y/n)')
    if yesno == 'y':
        print('YAY! :D Now submitting your information,', nickname, '.')
        return [nickname,rank,name,service,reminderstate,admin,sadmin]

def weeklyoption():
    #reminder function to be created
    global workweek
    global nickname #to be taken from usersettings
    count = 0
    attnlist = []
    while count <= 4:
        print(nickname,', for',workweek[count],',')
        attnlist.append(multioptionselect('attendance','here','nothere'))
        count += 1
    return attnlist

'''to be done before ALPHA
telegram functionality
dailyoption
actual reminder function
database system
admin access tools
superadmin access tools
'''