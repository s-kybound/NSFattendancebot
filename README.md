# NSFattendancebot
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
password = 'Insert the password for admins here.'  #admin password
highpassword = 'Insert the password for superadmins here.'  #superadmin password
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