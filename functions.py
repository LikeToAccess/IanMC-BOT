# -*- coding: utf-8 -*-
# filename          : functions.py
# description       : Helper functions
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 04-04-2021
# version           : v1.0
# usage             : python functions.py
# notes             : This should not be run directly
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import os
from datetime import datetime
from mcrcon   import MCRcon


def read_file(filename, directory=None, filter=False):
	if directory:
		os.chdir(f"{os.getcwd()}/{directory}")
	with open(filename, "r") as file:
		lines = file.read().split("\n")
	if filter:
		lines = filter_list(lines)
	return lines

def write_file(filename, msg):
	with open(filename, "w") as file:
		file.write(msg)

def append_file(filename, msg):
	with open(filename, "a") as file:
		file.write(msg)

def filter_list(lines, filename=False):
	if filename:
		lines = read_file(filename)
	data = []
	for line in lines:
		if line[:1] != "#" and line != "":
			data.append(line)
	return data

async def log(ctx, authenticated, filename="log.txt"):
	if not authenticated:
		await ctx.message.delete()
		await ctx.send(f"User *\"{ctx.author}\"*, is not in the allowed users list!\nThis event has been logged.")
	authenticated = "FAILED to execute" if not authenticated else "SUCCESFULLY executed"
	data = ctx.message.content
	data = f"[{datetime.now()}]{ctx.message.author} :: {authenticated} \"{data}\"\n"
	print(data.strip("\n"))
	append_file(filename, data)


class Minecraft:
	def __init__(self, address, password):
		mcr = MCRcon(address, password)
		self.address = address
		self.password = password
		self.mcr = mcr

	def connect(self):
		self.mcr.connect()

	def disconnect(self):
		self.mcr.disconnect()

	# Only highest level users should access
	def run(self, cmd):
		if cmd[:1] == "/":
			cmd = f"{cmd}"
		print(f"DEBUG: {cmd}")
		try:
			resp = self.mcr.command(cmd)
		except BrokenPipeError:
			print("DEBUG: Reconnecting...")
			self.disconnect()
			self.connect()
			self.run(cmd)
		return resp if resp else f"Error, no response. Please let Ian know so he can fix this!\n```Command that gave the error: {cmd}```"

	def list_players(self):
		resp = self.run("list").split()
		return f"{resp[2]}/{resp[7]}"

	# Requires Authentication
	async def whitelist_add(self, ctx, player):
		resp = self.run(f"whitelist add {player}")
		await ctx.send(resp)
		return resp

	# Requires Authentication
	async def whitelist_remove(self, ctx, player):
		resp = self.run(f"whitelist remove {player}")
		await ctx.send(resp)
		return resp

	async def whitelist_list(self, ctx):
		resp = self.run("whitelist list")
		await ctx.send(resp)
		return resp


if __name__ == "__main__":
	print("Wrong module, switchihng to \"bot.py\"...")
	os.system("python bot.py")
