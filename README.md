# NSFattendancebot
DISCLAIMER

I built this bot for self-interest, as a way to improve my own programming skill, and to improve 'quality-of-life' at work. I take no responsibility for what you do with this project, and will not be held responsible for any damages incurred.



ABOUT

This is a simple attendance bot that I have designed for NSF ASAs to use. As it is, it is designed for usage in more office-like environments.
It prompts users for their attendance every 30 minutes, based on start and end times that you enter. After which, admins can access the attendance data to enter into parade state.

I have only tested this program on Raspberry Pi OS. There, it can be run 24/7 without issue.

It has the following commands:

/start - Enter/reenter your particulars.

/commands - Brings up the list of all commands available.

/info - Sends a link to this Github page.

/removeme - Removes you from the bot. Use when you leave the unit.

/reportattendance - Manually enter attendance.

/test - Returns the particulars you have in the bot.

/admin - Password protected. Grants superadmin or admin access if successful. If admin, provides list of admin commands.

/superadmin - Password protected. Grants Superadmin. If superadmin, providdes list of superadmin commands.

/longtermabsence - For long-duration leaves or events such as overseas exercise. Use on first and last day of leave.

/poke - ADMIN command. Reminds anyone who hasn't entered attendance to do so.

/getfullps - ADMIN command. Returns name and reasoning of those absent.

/holiday - ADMIN command. DEACTIVATES autoattendance for the day by assigning everyone(who hasn't replied) a HOLIDAY value.

/superadminbroadcast - SUPERADMIN command. Broadcasts a message to all users of the bot.

/giveme - Obtain a text with data on all the data the bot holds.

/feedme - Using aformentioned text, reenter it to a fresh copy of the bot to restore its data.

As for reasons for absence, I have left a general list of these in the bot, however they can be changed.



DEFENITIONS

PRESENT - When the bot asks you for attendance, PRESENT in this case means physically present in camp.

ADMIN - A user IN the unit, meaning he is subject to the attendance system and will appear when returning information on attendance. Has admin powers to propmt for attendance, receive attendance data etc.

SUPERADMIN - A user OUTSIDE of the unit, by default. Not subject to attendance (by default), but holds all admin powers as well as superadmin powers allowing him to make announcements via the system, etc.



REQUIREMENTS

This program requires Python 3.
This program will also require external modules, in this case schedule and pyTelegramBotAPI. With python3 PIP, install with these commands:

$ pip3 install pyTelegramBotAPI

$ pip3 install schedule

I would recommend using a SBC such as a low-cost Raspberry Pi (a model with wifi acceess) for this.
I have not yet tested running the bot on a cloud service.
A new Telegram bot account is needed. To do this, go to BotFather on Telegram via @BotFather to create a new bot.



SETUP

Upon downloading the code, set up the variables which are near the start of the script, replacing all text within the single quotation marks. It will look exactly like this:

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
    
If the bot is run on a Raspberry Pi or other linux/unix based computers, the bot can be set up to run on boot. In the script /etc/rc.local, add this line above the 'exit 0' line:

'sudo python3 /path to program/attendancebot.py'

The program will run in the background without interrupting usage of the computer for other purposes.

This was a very interesting first practical project/application of my programming knowledge!
