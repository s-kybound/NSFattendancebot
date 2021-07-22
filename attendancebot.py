#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATTENDANCE PROGRAM V1.4 OVERHAUL
Created on Tue Nov 24 23:06:18 2020
@author: pi
"""
import telebot
import time
import threading
import schedule
import os
from datetime import date, datetime, timedelta

key = 'Your bot token key here'
passw = 'A password for everyone meant to use the bot'  #global password for all users of bot
password = 'A password only for admins'  #admin password
highpassword = 'A password only for superadmins'  #superadmin password
ampmsystem = True #determines whether the system runs on one attendance value for the day or two, for AM and PM
database = 'database'  #denotes name of database, incase multiple instances are running
starttime = 'HH:MM'  #string to denote time to activate autoattendance, 24H clock in format 'HH:MM'
endtime = 'HH:MM'  #string to denote time to deactivate autoattendance, 24H clock in format 'HH:MM'
options = [
    'WFH', 'LL', 'OL', 
    'PCL', 'CCL', 'OML',
    'ML', 'MA', 'AUDIT',
    'OUTSTATION', 'ON COURSE'
    ]  #options for absence as required

bot = telebot.TeleBot(key)

def syncmemories():  #overwrites internal userbase variables with data taken from the current database.txt file
    global userbase
    global currentdatabase
    with open(currentdatabase, 'r') as sync:
        processing = sync.readlines()
    sync.close()
    count = 0
    userbase = {}
    for line in processing:
        goodline = line.strip()
        cycle = count % 7
        if cycle == 0:  #user id
            userbase[goodline] = []
            currentuser = goodline
        if cycle in range(5,7) or cycle == 1:  #strings
            userbase[currentuser].append(goodline)
        if cycle in range(2,5):  #boolean
            if goodline == 'True':
                userbase[currentuser].append(True)
            else:
                userbase[currentuser].append(False)
        count += 1

def newday():  #upon booting, searches for the database.txt for the current day. if unable to find, creates a new file, as well as resetting attendances, from the latest database.txt file, up to 10 years ago. else creates a new file.
    global userbase
    global today
    global database
    global sadmininunit
    today = date.today()
    print('Attempting to restore database...')
    try:
        syncmemories()  #does not tamper with attendance values, as this is most likely rebooting in the middle of the day due to error
        print('Database restored from today.')
    except FileNotFoundError:
        for datediff in range(1,3650,1):  #searches for older databases up to 10 years
            try:
                previousday = today - timedelta(days = datediff)
                olddatabase = database + previousday.strftime('%d%m%y') + '.txt'
                with open(olddatabase, 'r') as sync:
                    processing = sync.readlines()
                sync.close()
                count = 0
                userbase = {}
                for line in processing:
                    goodline = line.strip()
                    cycle = count % 7
                    if cycle == 0:  #user id
                        userbase[goodline] = []
                        currentuser = goodline
                    if cycle == 1:  #username
                        userbase[currentuser].append(goodline)
                    if cycle in range(2,5):  #boolean
                        if goodline == 'True':
                            userbase[currentuser].append(True)
                        else:
                            userbase[currentuser].append(False)
                    if cycle in range(5,7):  #attendances
                        if userbase[currentuser][3] == True:  #a unique attendance value that makes the bot never prompt you as long as long term absence is active
                            userbase[currentuser][cycle-1] == goodline  #attendance value from previous day is retained
                        else:
                            userbase[currentuser].append('NIL')  #erases previous data, bot will now annoy you
                    count += 1
                uploadmemories()
                os.remove(olddatabase)
                print('Database restored from %s.' % previousday.strftime('%d%m%y'))
                break
            except FileNotFoundError:
                continue
        if userbase == {}:
            print('No previous database found.')
            uploadmemories()

def uploadmemories():  #overwrites the data inside of the current database.txt file with the internal variables from userbase
    global userbase
    global currentdatabase
    listtoupload = []  #formats the userbase into format used by database.txt
    for key in userbase:
        listtoupload.append(key)
        for item in userbase[key]:
            listtoupload.append(item)
    with open(currentdatabase, 'w') as filehandle:
        for items in listtoupload:
            filehandle.write('%s\n' % items)
        filehandle.close()

@bot.message_handler(commands=['info'])
def info(message):  #returns info on bot
    bot.reply_to(message, '''ATTENDANCE PROGRAM V1.4 OVERHAUL
-Designed by skybound
Current functionality:
Database saving
'poke' capability to remind people to report attendance
Timed automatic attendance taking
Basic attendance formatting for admins
Basic holiday functionality
Leaving capability
Long term absence functionality
Basic error handling
Resistance to unauthorized entry
Limitations:
The coding is really horrible
Particulars system is very basic
''')

@bot.message_handler(commands=['start'])
def start(message):  #enters, or reenters, a user's data into the system as well as the external database.txt
    markup = telebot.types.ForceReply()
    nmessage = bot.reply_to(message, 'Please enter the password to join the group.', reply_markup = markup)
    bot.register_next_step_handler(nmessage, procpass)
    
def procpass(message):  #deals with unauthorized entry
    global userbase
    global passw
    chat_id = message.chat.id
    entry = message.text.strip()  #cleans up extra spaces
    if entry == passw:
        bot.send_message(chat_id,'Password is correct, entry approved.')
        userbase[str(chat_id)] = ['PLACEHOLDER'] * 6 #in the end, you should not see these in the final userbase or database.txt
        markup = telebot.types.ForceReply()
        nmessage = bot.reply_to(message, '''
Please enter your name/nickname, which will be seen by everyone else.
''', reply_markup = markup)
        bot.register_next_step_handler(nmessage, procname)
    else:
        bot.send_message(chat_id,'Password is incorrect.')

def procname(message):
    global userbase
    global ranks
    chat_id = message.chat.id
    user = str(chat_id)
    name = message.text.strip()  #cleans up extra spaces
    userbase[user][0] = name
    userbase[user][1] = False  #admin statuses
    userbase[user][2] = False
    userbase[user][3] = False  #Long-Term Address
    userbase[user][4] = 'NIL'
    userbase[user][5] = 'NIL'   
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chat_id,'''Particulars uploaded!
Nickname = %s
''' % (userbase[user][0]), reply_markup=markup)
    uploadmemories()
    for users in userbase.keys():
        if userbase[users][1] == True:
            bot.send_message(users,'New user %s' % (userbase[user][0]))  #alerts admins
        elif userbase[users][2] == True:
            bot.send_message(users,'%s' % (user+' '+userbase[user]))  #alerts superadmin
            
@bot.message_handler(commands=['test'])
def test(message):  #returns your data in the system. use to see if bot is alive/ if data is incorrect
    global userbase
    global ampmsystem
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if ampmsystem == True:
            bot.send_message(chat_id,'''Your particulars:
Nick/name = %s
Admin = %s
Superadmin = %s
Long-term absence = %s
AM Attendance = %s
PM Attendance = %s
''' % (userbase[user][0],userbase[user][1],userbase[user][2],userbase[user][3],userbase[user][4],userbase[user][5]))
        else:
            bot.send_message(chat_id,'''Your particulars:
Nick/name = %s
Admin = %s
Superadmin = %s
Long-term absence = %s
Attendance = %s
''' % (userbase[user][0],userbase[user][1],userbase[user][2],userbase[user][3],userbase[user][4]))
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')

@bot.message_handler(commands=['reportattendance'])
def manualattendance(message):  #to enter your attendance before the bot decides to start hunting you down at starttime - time variable of when to start
    global userbase
    global ampmsystem
    chat_id = message.chat.id
    user = str(chat_id)
    yesno = ['OFFICE', 'ABSENT']
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
    for option in yesno:
        markup.add(option)
    try:
        if ampmsystem == True:
            nmessage = bot.reply_to(message,'%s, are you present today (AM)?' % userbase[user][0], reply_markup = markup)
        else:
            nmessage = bot.reply_to(message,'%s, are you present today?' % userbase[user][0], reply_markup = markup)
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')
    else:
        bot.register_next_step_handler(nmessage, procAM)

@bot.message_handler(commands=['poke'])
def poke(message):  #for admins to directly take over in annoying everyone who hasn't responded
    global userbase
    global ampmsystem
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][1] == True:
            for users in userbase.keys():
                if userbase[users][1] == True:
                    bot.send_message(users,'%s has poked everyone' % (userbase[user][0]))  #alerts admins
            yesno = ['OFFICE', 'ABSENT']
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in yesno:
                markup.add(option)
            for users in userbase.keys():  #selectively messages everyone who hasn't responded
                if userbase[users][4] == 'NIL':
                    try:
                        if ampmsystem == True:
                            nmessage = bot.send_message(int(users),'%s, it is time %s! Are you present today (AM)?' % (userbase[users][0], datetime.now().strftime('%H:%M:%S')), reply_markup = markup)
                        else:
                            nmessage = bot.send_message(int(users),'%s, it is time %s! Are you present today?' % (userbase[users][0], datetime.now().strftime('%H:%M:%S')), reply_markup = markup)
                        bot.register_next_step_handler(nmessage, procAM)
                    except telebot.apihelper.ApiTelegramException:
                        print(userbase[users])  #this will return the particulars of someone who has either blocked or stopped the bot without /removeme. This previously broke the bot.
                else:
                    continue
        else:
            bot.reply_to(message,'%s, you do not have the admin rights to do this.' % userbase[user][0])
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')

def autoattendance():  #the bot's most amazing function, doing (your) job of hunting everyone for attendance
    global userbase
    global ampmsystem
    yesno = ['OFFICE', 'ABSENT']
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
    for option in yesno:
        markup.add(option)
    for user in userbase.keys():
        if userbase[user][4] == 'NIL':  #selectively messages everyone who has not responded
            try:
                if ampmsystem == True:
                    nmessage = bot.send_message(int(user),'%s, it is time %s! Are you present today (AM)?' % (userbase[user][0], datetime.now().strftime('%H:%M:%S')), reply_markup = markup)
                else:
                    nmessage = bot.send_message(int(user),'%s, it is time %s! Are you present today?' % (userbase[user][0], datetime.now().strftime('%H:%M:%S')), reply_markup = markup)
                bot.register_next_step_handler(nmessage, procAM)
            except telebot.apihelper.ApiTelegramException:
                print(userbase[user])
        else:
            continue

def procAM(message):  #processes attendance entered - present or not, if not, prompts for reason
    global userbase
    global options
    global ampmsystem
    chat_id = message.chat.id
    user = str(chat_id)
    attendance = message.text
    if attendance == 'OFFICE':
        markup = telebot.types.ReplyKeyboardRemove()
        bot.reply_to(message, '%s, thank you!' % userbase[user][0], reply_markup = markup)
        userbase[user][4] = attendance
        uploadmemories()
        if ampmsystem == True:
            yesno = ['OFFICE', 'ABSENT']
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in yesno:
                markup.add(option)
            nmessage = bot.send_message(int(user),'Will you be present today (PM)?', reply_markup = markup)
            bot.register_next_step_handler(nmessage, procPM)
        else:
            userbase[user][5] = attendance
    else:
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
        for option in options:
            markup.add(option)
        nmessage = bot.reply_to(message, 'Please elaborate on why you are not in base.', reply_markup = markup)
        bot.register_next_step_handler(nmessage, procAM2)

def procAM2(message):  #process additional attendance prompt on reason of absence
    global userbase
    global options
    global ampmsystem
    chat_id = message.chat.id
    user = str(chat_id)
    attendance = message.text
    markup = telebot.types.ReplyKeyboardRemove()
    bot.reply_to(message, '%s, thank you!' % userbase[user][0], reply_markup = markup)
    userbase[user][4] = attendance
    uploadmemories()
    if ampmsystem == True:
        if userbase[user][3] == True:
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in options:
                markup.add(option)
            nmessage = bot.reply_to(message, 'Please elaborate on why you are not in base (PM).', reply_markup = markup)
            bot.register_next_step_handler(nmessage, procPM2)
        else:
            yesno = ['OFFICE', 'ABSENT']
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in yesno:
                markup.add(option)
            nmessage = bot.send_message(int(user),'Will you be present today (PM)?', reply_markup = markup)
            bot.register_next_step_handler(nmessage, procPM)
    else:
        userbase[user][5] = attendance
    
def procPM(message):  #processes attendance entered - present or not, if not, prompts for reason
    global userbase
    global options
    chat_id = message.chat.id
    user = str(chat_id)
    attendance = message.text
    if attendance == 'OFFICE':
        markup = telebot.types.ReplyKeyboardRemove()
        bot.reply_to(message, '%s, thank you!' % userbase[user][0], reply_markup = markup)
        userbase[user][5] = attendance
        uploadmemories()
    else:
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
        for option in options:
            markup.add(option)
        nmessage = bot.reply_to(message, 'Please elaborate on why you are not in base.', reply_markup = markup)
        bot.register_next_step_handler(nmessage, procPM2)

def procPM2(message):  #process additional attendance prompt on reason of absence
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    attendance = message.text
    markup = telebot.types.ReplyKeyboardRemove()
    bot.reply_to(message, '%s, thank you!' % userbase[user][0], reply_markup = markup)
    userbase[user][5] = attendance
    uploadmemories()

@bot.message_handler(commands=['getps'])
def PS(message):  #returns more detailed data on who isn't here - reason, followed by total number, then rank + names, ordered alphabetically by their ranks
    global userbase
    global today
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][1] == True:
            bot.reply_to(message,'%s, collating data now.' % userbase[user][0])
            present = 0
            presentroster = []
            processing = {}  #filters out all those present
            if ampmsystem == True:
                am = 'AM\n'
            else:
                am = ''
            for users in userbase.keys():
                if userbase[users][4] == 'OFFICE':
                    present += 1
                    presentroster.append(userbase[users][0])
                    presentroster.sort()
                else:
                    processing.update({users:userbase[users]})
            presentnames = ''
            for people in presentroster:
                presentnames = presentnames + people + '\n'
            presentlist = ('%s\nOFFICE - %s\n' % (today.strftime('%d%m%y'),present)) + presentnames
            absentreasons = {}  #orders absentees by reason, followed by strength and rank + name eg. {reason : [strength, [guys]]}
            for users in processing.keys():
                if processing[users][4] in absentreasons:
                    absentreasons[processing[users][4]][0] += 1  #increase strength
                    absentreasons[processing[users][4]][1].append(processing[users][0])  #add guy
                    absentreasons[processing[users][4]][1].sort()  #orders the rank + names to make it more readable
                else:
                    absentreasons.update({processing[users][4]:[1, [processing[users][0]]]})  #makes a new dictionary value for a previously unencountered reason
            absenteelist = ''  #string to send to requester
            for reasons in absentreasons.keys():  #sorts absentreasons dictionary to a readable form in absenteelist string
                absenteelist = absenteelist + '%s - %s\n' % (reasons, absentreasons[reasons][0])  #shows 'REASON - strength'
                for people in absentreasons[reasons][1]:
                    absenteelist = absenteelist + '%s\n' % people  #below the reason, lists all the people with that reason
                absenteelist = absenteelist + '\n'
            absenteelist = '%s\n' % absenteelist
            bot.send_message(chat_id, am+presentlist+'\n'+absenteelist)
            if ampmsystem == True:
                present = 0  #do it again, but for PM
                presentroster = []
                processing = {}  #filters out all those present
                for users in userbase.keys():
                    if userbase[users][5] == 'OFFICE':
                        present += 1
                        presentroster.append(userbase[users][0])
                        presentroster.sort()
                    else:
                        processing.update({users:userbase[users]})
                presentnames = ''
                for people in presentroster:
                    presentnames = presentnames + people + '\n'
                presentlist = ('%s\nOFFICE - %s\n' % (today.strftime('%d%m%y'),present)) + presentnames
                absentreasons = {}  #orders absentees by reason, followed by strength and rank + name eg. {reason : [strength, [guys]]}
                for users in processing.keys():
                    if processing[users][5] in absentreasons:
                        absentreasons[processing[users][5]][0] += 1  #increase strength
                        absentreasons[processing[users][5]][1].append(processing[users][0])  #add guy
                        absentreasons[processing[users][5]][1].sort()  #orders the rank + names to make it more readable
                    else:
                        absentreasons.update({processing[users][5]:[1, [processing[users][0]]]})  #makes a new dictionary value for a previously unencountered reason
                absenteelist = ''  #string to send to requester
                for reasons in absentreasons.keys():  #sorts absentreasons dictionary to a readable form in absenteelist string
                    absenteelist = absenteelist + '%s - %s\n' % (reasons, absentreasons[reasons][0])  #shows 'REASON - strength'
                    for people in absentreasons[reasons][1]:
                        absenteelist = absenteelist + '%s\n' % people  #below the reason, lists all the people with that reason
                    absenteelist = absenteelist + '\n'
                absenteelist = '%s\n' % absenteelist
                bot.send_message(chat_id, 'PM\n'+presentlist+'\n'+absenteelist)
        else:
            bot.reply_to(message,'%s, you do not have the admin rights to do this.' % userbase[user][0])
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')

@bot.message_handler(commands=['removeme'])
def removeme(message):  #deletes your data from the userbase and database.txt
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        del userbase[user]
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')
    else:
        bot.reply_to(message,'Data removed from system.')
        uploadmemories()

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,'''/start - Enter/reenter your particulars.
/help - Brings up this text.
/info - Returns info about the bot, its version, limitations, etc.
/feedback - Provide feedback.
/removeme - Removes you from the system. Use when you leave the unit.
/reportattendance - Manually enter attendance.
/test - Returns the particulars you have in the system.
/documentation - Shows the GitHub page of the bot.
/adminaccess - Password protected. Grants superadmin or admin access if successful.
/longtermabsence - For long-duration leaves or events such as overseas exercise. Use on first and last day of leave.
/poke - ADMIN command. Reminds anyone who hasn't entered attendance to do so.
/getps - ADMIN command. Returns name and reasoning of those absent.
/holiday - ADMIN command. DEACTIVATES autoattendance for the day.
/superadminbroadcast - SUPERADMIN command. Broadcasts a message to all users of the bot.
''')

@bot.message_handler(commands=['feedback'])
def feedback(message):  #sends feedback with time and name to feedback.txt
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    markup = telebot.types.ForceReply()
    try:
        nmessage = bot.reply_to(message, '%s, please enter your feedback' % userbase[user][0], reply_markup = markup)
    except KeyError:
        bot.send_message(message.chat.id,'Your particulars are not in the system!')
    else:
        bot.register_next_step_handler(nmessage, procfeedback)

def procfeedback(message):  #processes feedback
    global today
    global userbase
    user = message.chat.id
    guy = (userbase[user][1]+' '+userbase[user][2])
    with open('feedback.txt', 'a') as filehandle:
        filehandle.write('%s - %s - %s\n' %(today.strftime('%d%m%y'), guy, message.text))
        filehandle.close()
    bot.send_message(message.chat.id,'Feedback uploaded!')

@bot.message_handler(commands=['adminaccess'])
def admin(message):  #function to request for admin or superadmin access
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    markup = telebot.types.ForceReply()
    try:
        nmessage = bot.reply_to(message, '%s, please enter the password:' % userbase[user][0], reply_markup = markup)
    except KeyError:
        bot.send_message(message.chat.id,'Your particulars are not in the system!')
    else:
        bot.register_next_step_handler(nmessage, procadmin)

def procadmin(message):  #processes password entered
    global userbase
    global password
    global highpassword
    chat_id = message.chat.id
    user = str(chat_id)
    attempt = message.text.strip()  #cleans up extra spaces
    markup = telebot.types.ReplyKeyboardRemove()
    if attempt == password:
        for users in userbase.keys():
                if userbase[users][1] == True:
                    bot.send_message(users,'%s has become an admin' % (userbase[user][0]))  #alerts admins
        userbase[user][1] = True
        userbase[user][2] = False
        bot.reply_to(message, 'Recognised as admin.', reply_markup = markup)
        uploadmemories()
    elif attempt == highpassword:
        userbase[user][1] = True
        userbase[user][2] = True
        bot.reply_to(message, 'Recognised as superadmin.', reply_markup = markup)
        uploadmemories()
    else:
        bot.reply_to(message, 'Incorrect entry!', reply_markup = markup)

@bot.message_handler(commands=['longtermabsence'])
def lta(message):
    global userbase
    global options
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][3] == True:  #deactivates this status
            yesno = ['OFFICE', 'ABSENT']
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in yesno:
                markup.add(option)
            bot.reply_to(message,'Long-term absence deactivated. Please report attendance now.')
            nmessage = bot.send_message(user,'%s, are you present today (AM)?' % userbase[user][0], reply_markup = markup)
            bot.register_next_step_handler(nmessage, procAM)
        else:  #activates status
            bot.reply_to(message,'''Long-term absence activated. Please deactivate on the morning this absence ends.
Please enter your absence reasons one last time.
''')
            userbase[user][3] = True  #placeholder value to deter bot from prompting
            for users in userbase.keys():
                if userbase[users][4] == True:
                    bot.send_message(users,'%s has activated long term absence.' % ((userbase[user][0])))
            uploadmemories()
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in options:
                markup.add(option)
            nmessage = bot.reply_to(message, 'Please elaborate on why you are not in base (AM).', reply_markup = markup)
            bot.register_next_step_handler(nmessage, procAM2)
    except KeyError:
        bot.send_message(message.chat.id,'Your particulars are not in the system!')

def proclta(message):  #alerts admins on reason for absence
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    bot.reply_to(message, 'Reason sent to admins.')
    for users in userbase.keys():
        if userbase[users][4] == True:
            bot.send_message(users,'%s has activated long term absence for reason: %s' % ((userbase[user][1]+' '+userbase[user][2]), message.text.strip()))

@bot.message_handler(commands=['superadminbroadcast'])
def sadminbroadcast(message):  #broadcasts superadmin message
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][2] == True:
            markup = telebot.types.ForceReply()
            nmessage = bot.send_message(user, 'what would you like to broadcast?', reply_markup = markup)
            bot.register_next_step_handler(nmessage, procsbroadcast)
        else:
            bot.reply_to(message,'%s, you do not have the admin rights to do this.' % userbase[user][0])
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')

def procsbroadcast(message):
    global userbase
    for user in userbase.keys():
        try:
            bot.send_message(user,'-SUPERADMIN BROADCAST-\n%s' % message.text)
        except telebot.apihelper.ApiTelegramException:
            print(userbase[user])

@bot.message_handler(commands=['holiday'])
def holiday(message):  #denotes that the day is a holiday
    global userbase
    global today
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][1] == True:
            for users in userbase.keys():
                if userbase[users][1] == True:
                    bot.send_message(users,'%s has turned today into a holiday' % (userbase[user][0]))  #alerts admins
            holidaycont()
        else:
            bot.reply_to(message,'%s, you do not have the admin rights to do this.' % userbase[user][0])
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')
        
@bot.message_handler(commands=['documentation'])
def documentation(message):
    bot.reply_to(message,'https://github.com/s-kybound/NSFattendancebot')
    
def run_threaded(job_func):
    job_thread = threading.Thread(target = job_func)
    job_thread.start()

def on():
    global bot
    print('bot active')
    bot.infinity_polling()

def off():
    global bot
    bot.stop_polling()
    print('bot inactive')

def autoattendancetimer():  #repeats autoattendance every 30 minutes to make it all the more painful
    global userbase
    for users in userbase.keys():
        if userbase[users][1] == True:
            bot.send_message(users,'Prompting for attendance has begun.')
    autoattendance()
    schedule.every(30).minutes.do(run_threaded, autoattendance).tag('daily')

def stopattendance():
    schedule.clear('daily')

def setauto():
    schedule.every().monday.at(starttime).do(run_threaded, autoattendancetimer).tag('weekly')
    schedule.every().tuesday.at(starttime).do(run_threaded, autoattendancetimer).tag('weekly')
    schedule.every().wednesday.at(starttime).do(run_threaded, autoattendancetimer).tag('weekly')
    schedule.every().thursday.at(starttime).do(run_threaded, autoattendancetimer).tag('weekly')
    schedule.every().friday.at(starttime).do(run_threaded, autoattendancetimer).tag('weekly')
    return schedule.CancelJob

def holidaycont():
    global endtime
    schedule.clear('weekly')
    schedule.every().day.at(endtime).do(run_threaded, setauto)

try:
    today = date.today()
    userbase = {}
    currentdatabase = database + today.strftime('%d%m%y') + '.txt'
    newday()
    run_threaded(on)
    schedule.every().day.at('00:05').do(run_threaded, newday)
    schedule.every().day.at(endtime).do(run_threaded, stopattendance)
    setauto()
    while 1:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    off()
