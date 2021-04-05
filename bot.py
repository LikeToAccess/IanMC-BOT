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
from discord.ext import commands, tasks
from functions   import *


credentials = read_file("credentials.md", filter=True)
token = credentials[0]
server = Minecraft(credentials[1], credentials[2])
allowed_users = credentials[3:]
bot = commands.Bot(command_prefix=
	[
		"please ",
		"!",
		"-",
		"ian!",
		"ian ",
		"in!",
		"i!",
		"/"
	],
	help_command=None, case_insensitive=True)


def run():
	try:
		server.connect()
		bot.run(token)
	except Exception as error:
		print(f"Stopped with error: {error}")

async def check_perms(ctx):
	author = ctx.message.author
	if str(author.id) in allowed_users:
		return True
	await log(ctx)
	return False

@bot.event
async def on_ready():
	print(f"{bot.user} successfuly connected!")
	set_status.start()

@tasks.loop(seconds=20)
async def set_status():
	players = server.list_players()
	if players[0] == "0": status = discord.Status.idle
	else: status = discord.Status.online
	await bot.change_presence(status=status, activity=discord.Game(f"IanMC {players}"))

@bot.command(pass_context=True, name="list")
async def list(ctx):
	await ctx.send(server.run("list"))

@bot.command(pass_context=True, name="whitelist")
async def whitelist(ctx, func, player):
	if func == "list":
		server.whitelist_list(player)
	elif func == "add" and await check_perms(ctx):
		server.whitelist_add(player)
	elif func == "remove" and await check_perms(ctx):
		server.whitelist_remove(player)

@bot.command(pass_context=True, name="kick")
async def kick(ctx, player):
	if await check_perms(ctx):
		await ctx.send(server.run(f"kick {player}"))


if __name__ == "__main__":
	run()
