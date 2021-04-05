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
from discord.ext import commands
from functions import *


credentials = read_file("credentials.md", filter=True)
token = credentials[0]
server = Minecraft(credentials[1], credentials[2])
allowed_users = credentials[3:]
bot = commands.Bot(command_prefix=["please ", "!", "-", "ian!", "ian ", "in!", "i!"], help_command=None, case_insensitive=True)


def run():
	try:
		server.connect()
		# print(server.list_players())
		bot.run(token)
	except Exception as e:
		print(f"Stopped with error: {e}")

@bot.event
async def on_ready():
	print(f"{bot.user} successfuly connected!")
	set_status.start()

@tasks.loop(seconds=20)
async def set_status():
	status = server.list_players()


if __name__ == "__main__":
	run()
