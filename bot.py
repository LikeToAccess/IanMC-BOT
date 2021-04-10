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
		log(ctx, True)
		return True
	await log(ctx, False)
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


##################
# v MIXED CMDS v #
##################
@bot.command(pass_context=True, name="whitelist")
async def whitelist(ctx, func=None, player=None):
	if not player:
		if not func:
			await server.whitelist_list(ctx)
		elif await check_perms(ctx):
			await server.whitelist_add(ctx, func)
	elif func == "list":
		await server.whitelist_list(ctx)
	elif func == "add" and await check_perms(ctx):
		await server.whitelist_add(ctx, player)
	elif func == "remove" and await check_perms(ctx):
		await server.whitelist_remove(ctx, player)

#################
# v USER CMDS v #
#################
@bot.command(pass_context=True, name="list")
async def list(ctx):
	await ctx.send(server.run("list"))

##################
# v ADMIN CMDS v #
##################
@bot.command(pass_context=True, name="kick")
async def kick(ctx, player):
	if await check_perms(ctx):
		await ctx.send(server.run(f"kick {player}"))

@bot.command(pass_context=True, name="op")
async def op(ctx, player):
	if await check_perms(ctx):
		await ctx.send(server.run(f"op {player}"))

@bot.command(pass_context=True, name="deop")
async def deop(ctx, player):
	if await check_perms(ctx):
		await ctx.send(server.run(f"deop {player}"))

@bot.command(pass_context=True, name="ban")
async def ban(ctx, player):
	if await check_perms(ctx):
		await ctx.send(server.run(f"ban {player}"))

@bot.command(pass_context=True, name="unban", aliases=["pardon"])
async def unban(ctx, player):
	if await check_perms(ctx):
		await ctx.send(server.run(f"pardon {player}"))

@bot.command(pass_context=True, name="restart")
async def restart(ctx):
	if await check_perms(ctx):
		await ctx.send(server.run("restart"))

@bot.command(pass_context=True, name="stop")
async def stop(ctx):
	if await check_perms(ctx):
		await ctx.send(server.run("stop"))

@bot.command(pass_context=True, name="authenticate", aliases=["auth","trust"])
async def auth(ctx, user:discord.Member):
	if ctx.message.author.id == 354992856609325058:
		msg = f"\n# {user} ID\n{user.id}\n"
		append_file("credentials.md", msg)
		await ctx.send(f"Added \"{user}\" to list of trusted admins.")
		await log(ctx, True)
	else:
		await ctx.send("Only the server owner can run this!")
		await log(ctx, False)


if __name__ == "__main__":
	run()
