# -*- coding: utf-8 -*-
# filename          : bot.py
# description       :
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 04-04-2021
# version           : v1.0
# usage             : python bot.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import discord
from functions import *

allowed_users = read_file("credentials.md", filter=True)
bot = commands.Bot(command_prefix=["please ", "!", "-", "ian!"], help_command=None, case_insensitive=True)





