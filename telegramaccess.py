#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 23:18:07 2020

@author: pi
"""
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


updater = Updater('1460357050:AAEWv3FYanB7B6np7C28Hv20OOYVtG0e5wM')

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()