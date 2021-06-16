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
import os
import discord
from discord.ext import commands, tasks
from discord.errors import HTTPException
from functions   import *


credentials = read_file("credentials.md", filter=True)
token = credentials[0]
server = Minecraft(credentials[1], credentials[2])
allowed_users = credentials[3:]
commands_list = {
	"whitelist":["whitelist"],
	"list":["list"],
	"kick":["kick"],
	"op":["op"],
	"deop":["deop"],
	"ban":["ban"],
	"unban":["unban","pardon"],
	"pardon":["pardon","unban"],
	"restart":["restart", "reboot"],
	"reboot":["reboot", "restart"],
	"stop":["stop"],
	"start":["start"],
	"say":["say"],
	"trust":["trust","auth"],
	"auth":["auth","trust"],
	"help":["help"],
}
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
		bot.run(token)
	except Exception as error:
		print(f"Stopped with error: {error}")

async def check_perms(ctx):
	global allowed_users
	allowed_users = read_file("credentials.md", filter=True)[3:]
	author = ctx.message.author
	if str(author.id) in allowed_users:
		await log(ctx, True)
		return True
	await log(ctx, False)
	return False

@bot.event
async def on_ready():
	print(f"{bot.user} successfuly connected!")
	activity = discord.Streaming(name="server initialization...", url="IanMC.ga")
	await bot.change_presence(status=discord.Status.idle, activity=activity)
	print("RCON...")
	server.connect()
	set_status.start()

@tasks.loop(seconds=45)
async def set_status():
	players = server.list_players()
	if players:
		if players[0] == "0": status = discord.Status.idle
		else: status = discord.Status.online
		activity = discord.Game(f"IanMC {players}")
	else:
		status = discord.Status.dnd
		activity = discord.Activity(type=discord.ActivityType.listening, name="an offline server")
	await bot.change_presence(status=status, activity=activity)


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

@bot.command(pass_context=True, name="tps")
async def tps(ctx):
	msg = server.run("tps")
	msg, chunks = [], msg.split("§")
	for chunk in chunks: msg.append(chunk[1:])
	msg = "".join(msg).split(":")
	msg[1] = "".join([(f"***{tps.strip()}***, " if float(tps.strip()) < 18 else f"{tps.strip()}, ") for tps in msg[1].split(", ")]).strip(", ")
	msg = ": ".join(msg)
	await ctx.send(f"Ticks Per Second is a way to quantify the overall health of the server's performance, the higher the better (20.0 being a perfect score):\n> Average {msg}")

@bot.command(pass_context=True, name="help")
async def help(ctx):
	await ctx.message.delete()
	help_msg = """
		All Users:
		> help (display all commands)
		> whitelist list (list all whitelisted users) {whitelist}
		> list (show all online users)

		Mods/Trusted Only:
		> kick <player> [message] (kicks a player)
		> op <player> (ops a player)
		> deop <player> (deops a player)
		> ban <player> [message] (bans a player)
		> unban <player> (unbans a player) {pardon}
		> restart (restarts the server) {reboot}
		> stop (stops the server)
		> start (starts the server if it is off)
		> say <message> (sends a message through in-game chat)
		> find <command [player] | player [command]> [count] (searches the log for specific actions/actions a user has taken, W.I.P.)
		> whitelist add <player> (adds a player to the whitelist) {whitelist}
		> whitelist remove <player> (removes a player from the whitelist)

		Owner Only:
		> auth <user discord.Member> (adds a user to the Mod/Trusted list) {trust}
	"""
	await ctx.send(help_msg)

##################
# v ADMIN CMDS v #
##################
@bot.command(pass_context=True, name="kick")
async def kick(ctx, player, *args):
	if await check_perms(ctx):
		args = " ".join(args) if args else ""
		await ctx.send(server.run(f"kick {player} {args}"))

@bot.command(pass_context=True, name="op")
async def op(ctx, player):
	if await check_perms(ctx):
		await ctx.send(server.run(f"op {player}"))

@bot.command(pass_context=True, name="deop")
async def deop(ctx, player):
	if await check_perms(ctx):
		await ctx.send(server.run(f"deop {player}"))

@bot.command(pass_context=True, name="ban")
async def ban(ctx, player, *args):
	if await check_perms(ctx):
		args = " ".join(args) if args else ""
		await ctx.send(server.run(f"ban {player} {args}"))

@bot.command(pass_context=True, name="unban", aliases=commands_list["unban"][1:])
async def unban(ctx, player):
	if await check_perms(ctx):
		await ctx.send(server.run(f"pardon {player}"))

@bot.command(pass_context=True, name="restart", aliases=commands_list["restart"][1:])
async def restart(ctx):
	if await check_perms(ctx):
		server.run("restart")
		await ctx.send("Restarting the server")
		status = discord.Status.dnd
		activity = discord.Activity(type=discord.ActivityType.listening, name="an offline server")
		await bot.change_presence(status=status, activity=activity)

@bot.command(pass_context=True, name="stop")
async def stop(ctx):
	if await check_perms(ctx):
		server.run("stop")
		await ctx.send("Stopping the server")
		status = discord.Status.dnd
		activity = discord.Activity(type=discord.ActivityType.listening, name="an offline server")
		await bot.change_presence(status=status, activity=activity)

@bot.command(pass_context=True, name="start")
async def start(ctx):
	if await check_perms(ctx):
		if server.run("list") == "Error, server offline!":
			start_server()
			await ctx.send("Starting the server")
		else:
			await ctx.send("Server is already online")

@bot.command(pass_context=True, name="say")
async def say(ctx, *args):
	if await check_perms(ctx):
		if args:
			args = " ".join(args)
			server.run(f"say {args}")
			await ctx.send("Message sent")
		else:
			await ctx.send("Hey! You forgot to write a message to be sent!")

@bot.command(pass_context=True, name="find")
async def find(ctx, *args):
	# find <command [player] [count] | player [command] [count] | count>
	command = args[0].lower() if len(args) >= 1 else False
	player  = args[1].lower() if len(args) >= 2 else False
	count   = args[2]         if len(args) >= 3 else None

	if command not in commands_list:
		player, command = command, player

	while count is None:
		if command:
			try:
				count = int(command)
				command = False
				break
			except ValueError: count = False
		if player:
			try:
				count = int(player)
				player = False
				break
			except ValueError: count = False
		break

	resp = []
	log_data = read_file("log.txt", filter=True)[::-1]
	for line in log_data:
		if len(resp) >= int(count) and count:
			break
		if not player and command:
			if command in line.lower():
				resp.append(line)
		if player and command:
			if command in line.lower() and player in line.split("::")[0].split("]")[1].lower():
				resp.append(line)
		if player and not command:
			if player in line.split("::")[0].split("]")[1].lower():
				resp.append(line)
		if not player and not command:
			resp.append(line)

	target_length = 2000
	resp = "\n".join(resp)
	if len(resp) >= target_length:
		result = split_string(resp)
		while too_long(result):
			new_result = []
			for count, part in enumerate(result):
				halfed = split_string(part)
				new_result.append(halfed[0])
				new_result.append(halfed[1])
			result = new_result
	else:
		result = [resp]
	# print(result)

	print(f"DEBUG: command={command}, player={player}, count={count}")

	channel = bot.get_channel(850041698921873428)
	if ctx.channel.id != 850041698921873428:
		await ctx.send(f"Output redirected to {channel.name}")
	await channel.send(f"**Results of query with options, command={command}, player={player}, count={count}:**")
	try:
		for part in result:
			# print(part)
			# print(len(part))
			await channel.send(part)
	except HTTPException: await channel.send("Error, no results!")

@bot.command(pass_context=True, name="authenticate", aliases=commands_list["auth"][1:])
async def auth(ctx, user:discord.Member):
	if ctx.message.author.id == 354992856609325058:
		msg = f"\n# {user} ID\n{user.id}\n"
		append_file("credentials.md", msg)
		await ctx.send(f"Added \"{user}\" to list of trusted admins")
		await log(ctx, True)
	else:
		await ctx.send("Only the server owner can run this!")
		await log(ctx, False)


if __name__ == "__main__":
	run()
