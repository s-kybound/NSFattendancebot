"""
ATTENDANCE PROGRAM V0.10 STABILITY TEST
Created on Tue Nov 24 23:06:18 2020
"""
import telebot
import time
import threading
import schedule
import os
from datetime import date, datetime, timedelta

key = 'INSERT YOUR TELEGRAM BOT KEY HERE'
password = 'INSERT YOUR GENERAL USAGE ADMIN PASSWORD HERE'  #admin password
highpassword = 'INSERT YOUR SUPERADMIN PASSWORD HERE'  #superadmin password
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
        cycle = count % 8
        if cycle == 0:  #user id
            userbase[goodline] = []
            currentuser = goodline
        if cycle in range(1,5) or cycle == 7:  #nickname, rank, name, attendance
            userbase[currentuser].append(goodline)
        if cycle in range(5,7):  #admin status
            if goodline == 'True':
                userbase[currentuser].append(True)
            else:
                userbase[currentuser].append(False)
        count += 1

def newday():  #upon booting, searches for the database.txt for the current day. if unable to find, creates a new file, as well as resetting attendances, from the latest database.txt file, up to 10 years ago. else creates a new file.
    global userbase
    global today
    global currentdatabase
    today = date.today()
    currentdatabase = 'database' + today.strftime('%d%m%y') + '.txt'
    print('Attempting to restore database...')
    try:
        syncmemories()  #does not tamper with attendance values, as this is most likely rebooting in the middle of the day due to error
        print('Database restored from today.')
    except FileNotFoundError:
        for datediff in range(1,3650,1):  #searches for older databases up to 10 years
            try:
                previousday = today - timedelta(days = datediff)
                olddatabase = 'database' + previousday.strftime('%d%m%y') + '.txt'
                with open(olddatabase, 'r') as sync:
                    processing = sync.readlines()
                sync.close()
                count = 0
                userbase = {}
                for line in processing:
                    goodline = line.strip()
                    cycle = count % 8
                    if cycle == 0:  #user id
                        userbase[goodline] = []
                        currentuser = goodline
                    if cycle in range(1,5):  #nickname, rank, name
                        userbase[currentuser].append(goodline)
                    if cycle in range(5,7):  #admin status
                        if goodline == 'True':
                            userbase[currentuser].append(True)
                        else:
                            userbase[currentuser].append(False)
                    if cycle == 7:  #attendance
                        if userbase[currentuser][5] == True:
                            userbase[currentuser].append('SADMIN')  #a unique attendance value that makes the bot never prompt you; superadmin is not part of the group
                        elif goodline == 'LONG TERM ABSENCE':  #a unique attendance value that makes the bot never prompt you as long as long term absence is active
                            userbase[currentuser].append(goodline)  #attendance value that prevents bot from annoying you
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
    bot.reply_to(message, '''ATTENDANCE PROGRAM V0.10 STABILITY TEST
-Designed by skybound
Current functionality:
Database saving
'poke' capability to remind people to report attendance
Timed automatic attendance taking
Basic attendance formatting for admins
Basic holiday functionality
Leaving capability
Long term absence functionality
Limitations:
The coding is really horrible
Particulars system is very basic
Very little exception handling capability
''')

@bot.message_handler(commands=['start'])
def start(message):  #enters, or reenters, a user's data into the system as well as the external database.txt
    global userbase
    chat_id = message.chat.id
    userbase[str(chat_id)] = ['PLACEHOLDER','PLACEHOLDER','PLACEHOLDER','PLACEHOLDER','PLACEHOLDER','PLACEHOLDER','PLACEHOLDER'] #in the end, you should not see these in the final userbase or database.txt
    markup = telebot.types.ForceReply()
    nmessage = bot.reply_to(message, '''
Don't worry about entering the right case, it's automatic!
How would you like me to address you?
''', reply_markup = markup)
    bot.register_next_step_handler(nmessage, procnick)

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
    chat_id = message.chat.id
    user = str(chat_id)
    rank = message.text
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
    userbase[user][3] = tos
    userbase[user][4] = False  #admin statuses
    userbase[user][5] = False
    userbase[user][6] = 'NIL'  #placeholder attendance
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chat_id,'''Particulars uploaded!
Nickname = %s
Rank = %s
Name = %s
Terms of service = %s
Admin access = %s
Superadmin access = %s
''' % (userbase[user][0],userbase[user][1],userbase[user][2],userbase[user][3],userbase[user][4],userbase[user][5]), reply_markup=markup)
    uploadmemories()

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
Admin access = %s
Superadmin access = %s
Attendance status = %s
''' % (userbase[user][0],userbase[user][1],userbase[user][2],userbase[user][3],userbase[user][4],userbase[user][5],userbase[user][6]))
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
            bot.reply_to(message,'%s, poking everyone now.' % userbase[user][0])
            yesno = ['PRESENT', 'ABSENT']
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in yesno:
                markup.add(option)
            for user in userbase.keys():  #selectively messages everyone who hasn't responded
                if userbase[user][6] == 'NIL':
                    nmessage = bot.send_message(int(user),'%s, it is time %s! Are you present today?' % (userbase[user][0], datetime.now().strftime('%H:%M:%S')), reply_markup = markup)
                    bot.register_next_step_handler(nmessage, procprescence)
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
        if userbase[user][6] == 'NIL':  #selectively messages everyone who hasn't responded
            nmessage = bot.send_message(int(user),'%s, it is time %s! Are you present today?' % (userbase[user][0], datetime.now().strftime('%H:%M:%S')), reply_markup = markup)
            bot.register_next_step_handler(nmessage, procprescence)
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
        userbase[user][6] = attendance
        uploadmemories()
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
    userbase[user][6] = attendance
    uploadmemories()

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
                if userbase[users][6] == 'PRESENT':
                    total += 1
                    present += 1
                    if userbase[users][3] == 'REG':
                        totalregs += 1
                        presentregs += 1
                    else:
                        totalnsfs += 1
                        presentnsfs += 1
                elif userbase[users][6] == 'SADMIN':  #superadmin is not counted as part of the group
                    continue
                else:
                    total += 1
                    if userbase[users][6] == 'NIL':
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
                if userbase[users][6] == 'PRESENT':
                    present += 1
                    presentroster.append(userbase[users][1]+' '+userbase[users][2])
                    presentroster.sort()
                elif userbase[users][6] == 'SADMIN':
                    continue
                else:
                    processing.update({users:userbase[users]})
            presentnames = ''
            for people in presentroster:
                presentnames = presentnames + people + '\n'
            presentlist = ('%s\nPRESENT - %s\n' % (today.strftime('%d%m%y'),present)) + presentnames
            absentreasons = {}  #orders absentees by reason, followed by strength and rank + name eg. {reason : [strength, [guys]]}
            for users in processing.keys():
                if processing[users][6] in absentreasons:
                    absentreasons[processing[users][6]][0] += 1  #increase strength
                    absentreasons[processing[users][6]][1].append(processing[users][1]+' '+processing[users][2])  #add guy
                    absentreasons[processing[users][6]][1].sort()  #orders the rank + names to make it more readable
                else:
                    absentreasons.update({processing[users][6] : [1, [(processing[users][1]+' '+processing[users][2])]]})  #makes a new dictionary value for a previously unencountered reason
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
/adminaccess - Password protected. Grants superadmin or admin access if successful.
/longtermabsence - For long-duration leaves or events such as overseas exercise. Use on first and last day of leave.
/poke - ADMIN command. Reminds anyone who hasn't entered attendance to do so.
/getsimpleps - ADMIN command. Returns total and present strength.
/getfullps - ADMIN command. Returns name and reasoning of those absent.
/holiday - ADMIN command. DEACTIVATES autoattendance for the day by assigning everyone(who hasn't replied) a HOLIDAY value.
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
        userbase[user][4] = True
        userbase[user][5] = False
        bot.reply_to(message, 'Recognised as admin.', reply_markup = markup)
        uploadmemories()
    elif attempt == highpassword:
        userbase[user][4] = True
        userbase[user][5] = True
        userbase[user][6] = 'SADMIN'  #a unique attendance value that makes the bot never prompt you; superadmin is not part of the group
        bot.reply_to(message, 'Recognised as superadmin.', reply_markup = markup)
        uploadmemories()
    else:
        bot.reply_to(message, 'Incorrect entry!', reply_markup = markup)

@bot.message_handler(commands=['longtermabsence'])
def lta(message):
    global userbase
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][6] == 'LONG TERM ABSENCE':  #deactivates this status
            yesno = ['PRESENT', 'ABSENT']
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
            for option in yesno:
                markup.add(option)
            bot.reply_to(message,'Long-term absence deactivated. Please report attendance now.')
            nmessage = bot.send_message(user,'%s, are you present today?' % userbase[user][0], reply_markup = markup)
            bot.register_next_step_handler(nmessage, procprescence)
        else:  #activates status
            bot.reply_to(message,'Long-term absence activated. Please deactivate on the morning this absence ends.') 
            userbase[user][6] = 'LONG TERM ABSENCE'  #placeholder value to deter bot from prompting
            uploadmemories()
            markup = telebot.types.ForceReply()
            nmessage = bot.send_message(user, 'Please explain the reason you are activating long term absence.', reply_markup = markup)
            bot.register_next_step_handler(nmessage, proclta)
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
        bot.send_message(user,'-SUPERADMIN BROADCAST-\n%s' % message.text)

@bot.message_handler(commands=['holiday'])
def holiday(message):  #denotes that the day is a holiday
    global userbase
    global today
    chat_id = message.chat.id
    user = str(chat_id)
    try:
        if userbase[user][4] == True:
            for users in userbase.keys():
                if userbase[users][6] == 'NIL':  #selects everyone who hasn't responded
                    userbase[users][6] = 'HOLIDAY'  #placeholder value to deter bot from prompting
                if userbase[users][4] == True:
                    bot.send_message(users,'%s has turned today into a holiday' % (userbase[user][1]+' '+userbase[user][2]))  #alerts admins
            uploadmemories()
        else:
            bot.reply_to(message,'%s, you do not have the admin rights to do this.' % userbase[user][0])
    except KeyError:
        bot.send_message(chat_id,'Your particulars are not in the system!')

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
            bot.send_message(users,'autoattendance has started')
    autoattendance()
    schedule.every(30).minutes.do(run_threaded, autoattendance).tag('daily')
    
def stopattendance():
    schedule.clear('daily')

try:
    today = date.today()
    userbase = {}
    currentdatabase = 'database' + today.strftime('%d%m%y') + '.txt'
    newday()
    run_threaded(on)
    schedule.every().day.at('00:05').do(run_threaded, newday)
    schedule.every().day.at(endtime).do(run_threaded, stopattendance)
    schedule.every().monday.at(starttime).do(run_threaded, autoattendancetimer)
    schedule.every().tuesday.at(starttime).do(run_threaded, autoattendancetimer)
    schedule.every().wednesday.at(starttime).do(run_threaded, autoattendancetimer)
    schedule.every().thursday.at(starttime).do(run_threaded, autoattendancetimer)
    schedule.every().friday.at(starttime).do(run_threaded, autoattendancetimer)
    while 1:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    off()
