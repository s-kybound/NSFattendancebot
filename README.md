# NSFattendancebot
DISCLAIMER

I built this bot for self-interest, as a way to improve my own programming skill. I take no responsibility for what you do with this project, and will not be held responsible for any damages incurred.

This is a simple attendance bot that I have designed for NSF ASAs to use. As it is, it is designed for usage in more office-like environments. I would assume such a system is most suitable for Navy units, given the high Navy activity on Telegram.
It prompts users for their attendance every 30 minutes, based on start and end times that you enter. After which, admins can access the attendance data to enter into parade state.

It is currently designed to run on a computer that is active, at least for office hours. It can be run 24/7 without issue. It is able to save and restore its information,
however, for security purposes, it deletes any previous day information after reloading it into its system.

It has the following commands:

/start - Enter/reenter your particulars.

/help - Brings up the list of all commands available.

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

As for reasons for absence, I have left a general list of these in the bot, however they can be changed.

Defining a few things:

PRESENT - When the bot asks you for attendance, PRESENT in this case means physically present in camp.

ADMIN - A user IN the unit, meaning he is subject to the attendance system and will appear when returning information on attendance. Has admin powers to propmt for attendance, receive attendance data etc.

SUPERADMIN - A user OUTSIDE of the unit, by default. Not subject to attendance (by default), but holds all admin powers as well as superadmin powers allowing him to make announcements via the system, etc.

Requirements:
This system runs on python and will require a python IDE, such as spyder.
This system will also require external modules, in this case schedule and pyTelegramBotAPI. For spyder, install with these commands:

! pip install pyTelegramBotAPI

! pip install schedule

As mentioned, this system requires a computer to run on. I would recommend using a SBC such as a low-cost Raspberry Pi (a model with wifi acceess) for this.
This system requires a new Telegram bot account to run on. To do this, go to BotFather on Telegram via @BotFather to create a new bot.

Setup:
Upon downloading the code in your preferred IDE, set up the variables which are near the start of the script, replacing all text within the single quotation marks. It will look exactly like this:

key = 'Insert the key for yout telegram bot here.'

password = 'Insert the password for admins here.'

highpassword = 'Insert the password for superadmins here.'

starttime = 'HH:MM'

endtime = 'HH:MM'

ranks = [
    'COL', 'SLTC', 'LTC',
    'MAJ', 'CPT', 'LTA',
    'ME4', 'ME3', 'ME2',
    'ME1', 'DX7', 'DX4',
    '1WO', '2WO', 'CFC',
    'CPL', 'LCP', 'PTE'
    ] 
    
options = [
    'WFH', 'WFH(AM)',
    'WFH(PM)', 'FULL DAY LEAVE',
    'LEAVE(AM)', 'LEAVE(PM)',
    'OFF', 'CHILDCARE LEAVE',
    'MEDICAL LEAVE', 'MEDICAL APPOINTMENT',
    'REPORTING SICK', 'HOSPITALIZED',
    'ON COURSE', 'OUTSTATION',
    'SAILING', 'OVERSEAS'
    ]  
    
After which, the bot can be run inside the IDE. For this method, the IDE must be left open for the bnot to continmue running. Test if the bot is alive with /start.
From then on, the bot will begin to leave a file, labelled as 'databaseDDMMYY.txt' in your system files. This is the bot's backup memory in case of system shutdown. It will only leave one database file in the system, deleting all older database files except the file of the day itself.

If the bot is run on a Raspberry Pi or other linux/unix based computers, the bot can be set up to run on bootup. In the script /etc/rc.local, add this line above the 'exit 0' line:

'sudo python3 /path to program(change this accordingly/attendancebot.py'

Either way, the program should run in the background, not interrupting usage of the computer for other purposes.
