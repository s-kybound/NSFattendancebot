"""
MIDS WING ATTENDANCE PROGRAM V0.01 PREALPHA
Created on Tue Nov 24 23:06:18 2020
@author: pi
"""
import schedule
import telebot
from datetime import date, timedelta

def syncmemories():
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
        if cycle == 0:
            userbase[goodline] = []
            currentuser = goodline
        if cycle in range(1,5) or cycle == 7:
            userbase[currentuser].append(goodline)
        if cycle in range(5,7):
            userbase[currentuser].append(bool(goodline))
        count += 1 
        
def newday():
    global userbase
    global today
    print('Attempting to restore database...')
    try:
        syncmemories()
        print('Database restored from today.')
    except FileNotFoundError:
        for datediff in range(1,3650,1):
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
                    if cycle == 0:
                        userbase[goodline] = []
                        currentuser = goodline
                    if cycle in range(1,5):
                        userbase[currentuser].append(goodline)
                    if cycle in range(5,7):
                        userbase[currentuser].append(bool(goodline))
                    if cycle == 7:
                        userbase[currentuser].append('NIL')
                    count += 1
                uploadmemories()
                print('Database restored from %s.' % previousday.strftime('%d%m%y'))
                break
            except FileNotFoundError:
                continue
        if userbase == {}:
            print('No previous database found.')
            uploadmemories()
            
def uploadmemories():
    global userbase
    global currentdatabase
    listtoupload = []
    for key in userbase:
        listtoupload.append(key)
        for item in userbase[key]:
            listtoupload.append(item)
    with open(currentdatabase, 'w') as filehandle:
        for items in listtoupload:
            filehandle.write('%s\n' % items)
        filehandle.close()
        
def info(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Attendancebot v0.0')
               
def singlevariableselect(variable):
    confirm = True
    while confirm:
        entry = input('May I have your %s?' % variable)
        yesno = input('May I confirm that your %s is %s?(y/n)' % (variable,entry))
        if yesno.lower() == 'y':
            context.bot.send_message(chat_id=update.effective_chat.id, text='Roger!')
            confirm = False
            return entry

def multioptionselect(variable,*options):
    confirm = True
    while confirm:
        context.bot.send_message(chat_id=update.effective_chat.id, text=('May I have your %s?' % variable))
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

def start(update, context):
    #called when /start or reconfiguring settings
    global userbase
    global currentdatabase
    usernum = update.message.from_user
    context.bot.send_message(chat_id=update.effective_chat.id, text="Do not worry about entering the right case, it's automatic!")
    confirm = True
    while confirm:
        nickname = singlevariableselect('preferred nickname')
        if nickname.upper() == 'SUPERADMIN':
            passkey = input('SUPERADMIN access requested. Enter password: ')
            if passkey == 'IatoaoK2':
                context.bot.send_message(chat_id=update.effective_chat.id, text='Roger. Recognised as SUPERADMIN.')
                nickname = 'SUPERADMIN'
                rank = 'SUPERADMIN'
                name = 'SUPERADMIN'
                service = 'SUPERADMIN'
                admin = True
                sadmin = True
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Incorrect password. Please do not enter SUPERADMIN as nickname!')
                nickname = singlevariableselect('preferred nickname')
                admin = False
                sadmin = False
        else:
            rank = singlevariableselect('abbreviated rank').upper()
            name = singlevariableselect('full name').title()
            service = multioptionselect('service status','REG','NSF')
            if nickname.upper() == 'ADMIN':
                passkey = input('ADMIN access requested. Enter password: ')
                if passkey == 'Midswing123':
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Roger. Recognised as ADMIN. Please enter actual nickname')
                    admin = True
                    sadmin = False
                    nickname = singlevariableselect('actual nickname',update,context)
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Incorrect password. Please do not enter ADMIN as nickname!')
                    nickname = singlevariableselect('preferred nickname',update,context)
                    admin = False
                    sadmin = False
            else:
                admin = False
                sadmin = False
        context.bot.send_message(chat_id=update.effective_chat.id, text='Confirming particulars...')
        context.bot.send_message(chat_id=update.effective_chat.id, text='Nickname = %s' % nickname)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Rank = %s' % rank)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Name = %s' % name)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Service status = %s' % service)
        if admin == True:
            context.bot.send_message(chat_id=update.effective_chat.id, text='ADMIN access = %s' % admin)
            context.bot.send_message(chat_id=update.effective_chat.id, text='SUPERADMIN access = %s' % sadmin)
        yesno = input('Confirm?(y/n)')
        if yesno == 'y':
            context.bot.send_message(chat_id=update.effective_chat.id, text=('YAY! :D Now submitting your information, %s.' % nickname))
            if userbase.get(usernum) != None:
                attendance = userbase[usernum][6]
            else:
                attendance = 'NIL'
            userbase.update({usernum: [nickname,rank,name,service,admin,sadmin,attendance]})
            uploadmemories()
            confirm = False
            
#def tinput(string):
         
userbase = {}
today = date.today()
currentdatabase = 'database' + today.strftime('%d%m%y') + '.txt'
newday()

bot = telebot.TeleBot('1618494441:AAGvmJmpS7dEIkdmzeHEz6LNdyQix1QU7-o')
'''
def query():
    global today
    global userbase
    global currentdatabase
    if today.weekday() < 5:
        attendance = ''
        while attendance == '':
            multioptionselect(attendance,'present in camp', 'absent')
            time.sleep(3600)
            #i am aware this will not work as intended for now.

    else:
        #placeholder

def admin():
    global userbase
    global currentdatabase
'''
