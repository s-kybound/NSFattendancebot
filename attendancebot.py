#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATTENDANCE PROGRAM V1.5
Created on Tue Nov 24 23:06:18 2020
@author: sky
"""
import telebot
#required python package pyTelegramBotAPI
import time
import threading
import schedule
#required python package schedule
from datetime import date, datetime

key = 'Your bot token key here'
passw = 'A password for everyone meant to use the bot' 
password = 'A password only for admins'  #admin password
highpassword = 'A password only for superadmins'  #superadmin password
starttime = 'HH:MM'  #string to denote time to activate autoattendance, 24H clock in format 'HH:MM'
endtime = 'HH:MM'  #string to denote time to deactivate autoattendance, 24H clock in format 'HH:MM'
ranks = [
    'COL', 'SLTC', 'LTC',
    'MAJ', 'CPT', 'LTA',
    'ME4', 'ME3', 'ME2',
    'ME1', 'DX7', 'DX4',
    '1WO', '2WO', 'CFC',
    'CPL', 'LCP', 'PTE'
    ]  #ranks as required
options = [
    'WFH', 'WFH(AM)',
    'WFH(PM)', 'FULL DAY LEAVE',
    'LEAVE(AM)', 'LEAVE(PM)',
    'OFF', 'CHILDCARE LEAVE',
    'MEDICAL LEAVE', 'MEDICAL APPOINTMENT',
    'REPORTING SICK', 'HOSPITALIZED',
    'ON COURSE', 'OUTSTATION',
    'SAILING', 'OVERSEAS'
    ]  #options for absence as required
sadminingroup = False

bot = telebot.TeleBot(key)

@bot.message_handler(commands=['giveme'])
def giveme():
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][4] == True:
		string = ''
		for key in userbase:
			string = f"{string}\n{key}"
				for item in userbase[key]
					string = f"{string}\n{item}"
		bot.send_message(chat_id,string)
        else:
            bot.reply_to(message,'%s, you are not permitted to do this.' % userbase[user][0])
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')

@bot.message_handler(commands=['feedme'])
def feedme():	
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    markup = telebot.types.ForceReply()
	try:
	    if userbase[user][4] == True:
		nmessage = bot.reply_to(message,'Feed me your data', reply_markup = markup)
		bot.register_next_step_handler(nmessage, procreload)			
        else:
            bot.reply_to(message,'%s, you are not permitted to do this.' % userbase[user][0])
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')

def procreload(message):
	global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    procstr = message.text
    count = 0
    userbase = {}
	markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
	markup.add('NEWDAY')
	markup.add('MIDDAY')
    for line in procstr.splitlines():
        goodline = line.strip()
        cycle = count % 9
        if cycle == 0:  #user id
            userbase[goodline] = []
            currentuser = goodline
        if cycle in range(1,5) or cycle == 8:  #strings
            userbase[currentuser].append(goodline)
        if cycle in range(5,8):  #boolean
            if goodline == 'True':
                userbase[currentuser].append(True)
            else:
                userbase[currentuser].append(False)
        count += 1
	bot.send_message(chat_id,'Data Uploaded.')
    nmessage = bot.reply_to(message, 'Is it the start of the day? Do you need me to reset all attendances?', reply_markup = markup)
    bot.register_next_step_handler(nmessage, procnewday)

def newday():
    global userbase
		for users in userbase.keys():
			if userbase[currentuser][6] == False:
				userbase[currentuser[7] == 'NIL'  #erases previous data, bot will now annoy you
						 
@bot.message_handler(commands=['info'])
def info(message):  #returns info on bot
    bot.reply_to(message, '''ATTENDANCE PROGRAM V1.5
Github: https://github.com/s-kybound/NSFattendancebot
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
        userbase[str(chat_id)] = ['PLACEHOLDER'] * 8 #in the end, you should not see these in the final userbase or database.txt
        markup = telebot.types.ForceReply()
        nmessage = bot.reply_to(message, '''
How would you like me to address you?
''', reply_markup = markup)
        bot.register_next_step_handler(nmessage, procnick)
    else:
        

def procnick(message):  #processes the nickname entered and prompts for rank
    global userbase
    global ranks
    chat_id = message.chat.id
    user = str(chat_id)
    nick = message.text.strip()  #cleans up extra spaces
    userbase[user][0] = nick
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
    for srank in ranks:
        markup.add(srank)
    nmessage = bot.reply_to(message, 'What rank are you?', reply_markup = markup)
    bot.register_next_step_handler(nmessage, procrank)

def procrank(message):  #processes the rank entered and prompts for full name
    global userbase
    global ranks
    chat_id = message.chat.id
    user = str(chat_id)
    rank = message.text
    if rank not in ranks:
        bot.send_message(chat_id,'Invalid rank. Retrying rank section.')
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
        for srank in ranks:
            markup.add(srank)
        nmessage = bot.reply_to(message, 'What rank are you?', reply_markup = markup)
        bot.register_next_step_handler(nmessage, procrank)
    else:
        userbase[user][1] = rank
        markup = telebot.types.ForceReply()
        nmessage = bot.reply_to(message, 'May I have your full name?', reply_markup = markup)
        bot.register_next_step_handler(nmessage, procname)

def procname(message):  #processes full name and prompts for terms of service
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    name = message.text.title().strip()  #capitalises every word, cleans up extra spaces
    userbase[user][2] = name
    tos = ['REG', 'NSF']
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
    for serv in tos:
        markup.add(serv)
    nmessage = bot.reply_to(message, 'May I have your terms of service?', reply_markup = markup)
    bot.register_next_step_handler(nmessage, proctos)

def proctos(message):  #processes terms of service, enters NIL attendance and admin privileges. presents final data to user
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    tos = message.text
    if tos not in ['REG', 'NSF']:
        bot.send_message(chat_id,'Invalid TOS. Retrying TOS section.')
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
        for serv in ['REG', 'NSF']:
            markup.add(serv)
        nmessage = bot.reply_to(message, 'May I have your terms of service?', reply_markup = markup)
        bot.register_next_step_handler(nmessage, proctos)
    else:
        userbase[user][3] = tos
        userbase[user][4] = False  #admin statuses
        userbase[user][5] = False
        userbase[user][6] = False  #long absence value
        userbase[user][7] = 'NIL'  #placeholder attendance
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(chat_id,'''Particulars uploaded!
Nickname = %s
Rank = %s
Name = %s
Terms of service = %s
''' % (userbase[user][0],userbase[user][1],userbase[user][2],userbase[user][3]), reply_markup=markup)
        for users in userbase.keys():
            if userbase[users][4] == True:
                bot.send_message(users,'New user %s' % (userbase[user][1]+' '+userbase[user][2]+' ,'+userbase[user][3]))  #alerts admins
            
@bot.message_handler(commands=['test'])
def test(message):  #returns your data in the system. use to see if bot is alive/ if data is incorrect
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        bot.send_message(chat_id,'''Your particulars:
Nickname = %s
Rank = %s
Name = %s
Terms of service = %s
Attendance status = %s
''' % (userbase[user][0],userbase[user][1],userbase[user][2],userbase[user][3],userbase[user][7]))
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')

@bot.message_handler(commands=['reportattendance'])
def manualattendance(message):  #to enter your attendance before the bot decides to start hunting you down at starttime - time variable of when to start
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    yesno = ['PRESENT', 'ABSENT']
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
    for option in yesno:
        markup.add(option)
    try:
        nmessage = bot.reply_to(message,'%s, are you present today?' % userbase[user][0], reply_markup = markup)
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')
    else:
        bot.register_next_step_handler(nmessage, procprescence)

@bot.message_handler(commands=['poke'])
def poke(message):  #for admins to directly take over in annoying everyone who hasn't responded
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][4] == True:
            for users in userbase.keys():
                if userbase[users][4] == True:
                    bot.send_message(users,'%s has poked everyone' % (userbase[user][1]+' '+userbase[user][2]))  #alerts admins
            yesno = ['PRESENT', 'ABSENT']
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in yesno:
                markup.add(option)
            for users in userbase.keys():  #selectively messages everyone who hasn't responded
                if userbase[users][7] == 'NIL':
                    try:
                        nmessage = bot.send_message(int(users),'%s, it is time %s! Are you present today?' % (userbase[user][0], datetime.now().strftime('%H:%M:%S')), reply_markup = markup)
                        bot.register_next_step_handler(nmessage, procprescence)
                    except telebot.apihelper.ApiTelegramException:
                        print(userbase[user])  #this will return the particulars of someone who has either blocked or stopped the bot without /removeme. This previously broke the bot.
                else:
                    continue
        else:
            bot.reply_to(message,'%s, you do not have the admin rights to do this.' % userbase[user][0])
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')

def autoattendance():  #the bot's most amazing function, doing (your) job of hunting everyone for attendance
    global userbase
    yesno = ['PRESENT', 'ABSENT']
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
    for option in yesno:
        markup.add(option)
    for user in userbase.keys():
        if userbase[user][7] == 'NIL':  #selectively messages everyone who hasn't responded
            try:
                nmessage = bot.send_message(int(user),'%s, it is time %s! Are you present today?' % (userbase[user][0], datetime.now().strftime('%H:%M:%S')), reply_markup = markup)
                bot.register_next_step_handler(nmessage, procprescence)
            except telebot.apihelper.ApiTelegramException:
                print(userbase[user])
        else:
            continue

def procprescence(message):  #processes attendance entered - present or not, if not, prompts for reason
    global userbase
    global options
    chat_id = message.chat.id
    user = str(chat_id)
    attendance = message.text
    if attendance == 'PRESENT':
        markup = telebot.types.ReplyKeyboardRemove()
        bot.reply_to(message, '%s, thank you!' % userbase[user][0], reply_markup = markup)
        userbase[user][7] = attendance
    else:
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
        for option in options:
            markup.add(option)
        nmessage = bot.reply_to(message, 'Please elaborate on why you are not in base.', reply_markup = markup)
        bot.register_next_step_handler(nmessage, procprescence2)

def procprescence2(message):  #process additional attendance prompt on reason of absence
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    attendance = message.text
    markup = telebot.types.ReplyKeyboardRemove()
    bot.reply_to(message, '%s, thank you!' % userbase[user][0], reply_markup = markup)
    userbase[user][7] = attendance

@bot.message_handler(commands=['getsimpleps'])
def abridgedPS(message):  #returns the total and present strength
    global userbase
    global today
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][4] == True:
            bot.reply_to(message,'%s, collating data now.' % userbase[user][0])
            total = 0
            totalregs = 0
            totalnsfs = 0
            present = 0
            presentregs = 0
            presentnsfs = 0
            nils = 0
            for users in userbase.keys():  #filters userbase to obtain required numbers
                if userbase[users][7] == 'PRESENT':
                    total += 1
                    present += 1
                    if userbase[users][3] == 'REG':
                        totalregs += 1
                        presentregs += 1
                    else:
                        totalnsfs += 1
                        presentnsfs += 1
                elif userbase[users][7] == 'SADMIN':  #superadmin is not counted as part of the group
                    continue
                else:
                    total += 1
                    if userbase[users][7] == 'NIL':
                        nils += 1
                    if userbase[users][3] == 'REG':
                        totalregs += 1
                    else:
                        totalnsfs += 1
            bot.send_message(chat_id,'''%s have not replied.
DATE %s
1. Perm Staff Total Strength
Total: %s
REG: %s
NSF: %s
2. Perm Staff Present Strength
Total: %s
REG: %s
NSF: %s
''' % (nils,today.strftime('%d%m%y'),total,totalregs,totalnsfs,present,presentregs,presentnsfs))
        else:
            bot.reply_to(message,'%s, you do not have the admin rights to do this.' % userbase[user][0])
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')

@bot.message_handler(commands=['getfullps'])
def PS(message):  #returns more detailed data on who isn't here - reason, followed by total number, then rank + names, ordered alphabetically by their ranks
    global userbase
    global today
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][4] == True:
            bot.reply_to(message,'%s, collating data now.' % userbase[user][0])
            present = 0
            presentroster = []
            processing = {}  #filters out all those present and superadmin
            for users in userbase.keys():
                if userbase[users][7] == 'PRESENT':
                    present += 1
                    presentroster.append(userbase[users][1]+' '+userbase[users][2])
                    presentroster.sort()
                elif userbase[users][7] == 'SADMIN':
                    continue
                else:
                    processing.update({users:userbase[users]})
            presentnames = ''
            for people in presentroster:
                presentnames = presentnames + people + '\n'
            presentlist = ('%s\nPRESENT - %s\n' % (today.strftime('%d%m%y'),present)) + presentnames
            absentreasons = {}  #orders absentees by reason, followed by strength and rank + name eg. {reason : [strength, [guys]]}
            for users in processing.keys():
                if processing[users][7] in absentreasons:
                    absentreasons[processing[users][7]][0] += 1  #increase strength
                    absentreasons[processing[users][7]][1].append(processing[users][1]+' '+processing[users][2])  #add guy
                    absentreasons[processing[users][7]][1].sort()  #orders the rank + names to make it more readable
                else:
                    absentreasons.update({processing[users][7] : [1, [(processing[users][1]+' '+processing[users][2])]]})  #makes a new dictionary value for a previously unencountered reason
            absenteelist = ''  #string to send to requester
            for reasons in absentreasons.keys():  #sorts absentreasons dictionary to a readable form in absenteelist string
                absenteelist = absenteelist + '%s - %s\n' % (reasons, absentreasons[reasons][0])  #shows 'REASON - strength'
                for people in absentreasons[reasons][1]:
                    absenteelist = absenteelist + '%s\n' % people  #below the reason, lists all the people with that reason
                absenteelist = absenteelist + '\n'
            absenteelist = '%s\n%s\n' % (today.strftime('%d%m%y'), absenteelist)
            bot.send_message(chat_id, presentlist)
            bot.send_message(chat_id, absenteelist)
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

#this section needs to be revampedvvv
@bot.message_handler(commands=['longtermabsence'])
def lta(message):
    global userbase
    global options
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][6] == True:  #deactivates this status
            userbase[user][6] = False
            yesno = ['PRESENT', 'ABSENT']
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in yesno:
                markup.add(option)
            bot.reply_to(message,'Long-term absence deactivated. Please report new attendance now.')
            nmessage = bot.send_message(user,'%s, are you present today?' % userbase[user][0], reply_markup = markup)
            bot.register_next_step_handler(nmessage, procprescence)
        else:  #activates status
            bot.reply_to(message,'Long-term absence activated. Please deactivate on the morning this absence ends.')
            userbase[user][6] = True  #placeholder value to deter bot from prompting
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in options:
                markup.add(option)
            nmessage = bot.reply_to(message, 'Please explain the reason you are activating long term absence.', reply_markup = markup)
            bot.register_next_step_handler(nmessage, proclta)
    except KeyError:
        bot.send_message(message.chat.id,'Your particulars are not in the system!')

def proclta(message):  #alerts admins on reason for absence
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    attendance = message.text
    markup = telebot.types.ReplyKeyboardRemove()
    bot.reply_to(message, '%s, thank you! Reason sent to admins.' % userbase[user][0], reply_markup = markup)
    userbase[user][7] = attendance
    for users in userbase.keys():
        if userbase[users][4] == True:
            bot.send_message(users,'%s has activated long term absence for reason: %s' % ((userbase[user][1]+' '+userbase[user][2]), userbase[user][7]))
#
@bot.message_handler(commands=['superadminbroadcast'])
def sadminbroadcast(message):  #broadcasts superadmin message
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][5] == True:
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
        if userbase[user][4] == True:
            for users in userbase.keys():
                if userbase[users][4] == True:
                    bot.send_message(users,'%s has turned today into a holiday' % (userbase[user][1]+' '+userbase[user][2]))  #alerts admins
            holidaycont()
        else:
            bot.reply_to(message,'%s, you do not have the admin rights to do this.' % userbase[user][0])
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')
        
@bot.message_handler(commands=['commands'])
def help(message):
    bot.reply_to(message,'''COMMANDS LIST
/start - Enter/reenter your particulars.
/commands - Brings up this text.
/test - Returns the particulars you have in the system.
/reportattendance - Manually enter attendance.
/removeme - Removes you from the system. Use when you leave the unit.
/longtermabsence - For long-duration leaves or events such as overseas exercise. Use on first and last day of leave.
/misc - Displays some miscellaneous functions.
/admin - Password protected. Grants superadmin or admin access if successful.
settings - currently nonexistent. Allows users to change specific particulars.
''')

@bot.message_handler(commands=['misc'])
def misc(message):
    bot.reply_to(message,'''MISCELLANEOUS COMMANDS
/info
''')

@bot.message_handler(commands=['admin'])
def admin(message):  #function to request for admin or superadmin access. if admin, brings up commands for admins.
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    markup = telebot.types.ForceReply()
    try:
        if userbase[user][5] == True:
            bot.send_message(message.chat.id,'''ADMIN COMMANDS
/poke - Reminds anyone who hasn't entered attendance to do so.
/getsimpleps - Returns total and present strength.
/getfullps - Returns name and reasoning of those absent.
/holiday - DEACTIVATES autoattendance for the day by assigning everyone(who hasn't replied) a HOLIDAY value. IRREVERSIBLE FOR THE DAY!
/feedme - updates the local userbase with a text file given by you
/giveme - gives user a text file with all the data from the system
/superadmin - Password protected. Grants admin access if successful.
chuser - Forces changes on a user's settings.
''')
        else:
            nmessage = bot.reply_to(message, '%s, please enter the password:' % userbase[user][0], reply_markup = markup)
    except KeyError:
        bot.send_message(message.chat.id,'Your particulars are not in the system!')
    else:
        bot.register_next_step_handler(nmessage, procadmin)
        
@bot.message_handler(commands=['superadmin'])     
def superadmin(message): #functions to request for superadmin access. if superadmin, brings up commands for superadmins.
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    markup = telebot.types.ForceReply()
    try:
        if userbase[user][5] == True:
            bot.send_message(message.chat.id,'''SUPERADMIN COMMANDS
/superadminbroadcast - SUPERADMIN command. Broadcasts a message to all users of the bot.
deluser - Force removes a user from the system.
bsettings - Changes base settings on how the bot operates.
''')
        else:
            nmessage = bot.reply_to(message, '%s, please enter the password:' % userbase[user][0], reply_markup = markup)
    except KeyError:
        bot.send_message(message.chat.id,'Your particulars are not in the system!')
    else:
        bot.register_next_step_handler(nmessage, procadmin)
        
def procadmin(message):  #processes password entered
    global userbase
    global password
    global highpassword
    global sadminingroup
    chat_id = message.chat.id
    user = str(chat_id)
    attempt = message.text.strip()  #cleans up extra spaces
    markup = telebot.types.ReplyKeyboardRemove()
    if attempt == password:
        for users in userbase.keys():
                if userbase[users][4] == True:
                    bot.send_message(users,'%s has become an admin' % (userbase[user][1]+' '+userbase[user][2]))  #alerts admins
        userbase[user][4] = True
        userbase[user][5] = False
        bot.reply_to(message, 'Recognised as admin.', reply_markup = markup)
    elif attempt == highpassword:
        userbase[user][4] = True
        userbase[user][5] = True
        if sadminingroup == False:
			userbase[user][6] = True
            userbase[user][7] = 'SADMIN'  #a unique attendance value that makes the bot never prompt you; superadmin is not part of the group
        bot.reply_to(message, 'Recognised as superadmin.', reply_markup = markup)
    else:
        bot.reply_to(message, 'Incorrect entry!', reply_markup = markup)

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
        if userbase[users][4] == True:
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
    run_threaded(on)
    schedule.every().day.at('00:05').do(run_threaded, newday)
    schedule.every().day.at(endtime).do(run_threaded, stopattendance)
    setauto()
    while 1:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    off()
