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
from mcrcon import MCRcon
import os


def read_file(filename, directory=None, filter=False):
	if directory:
		os.chdir(f"{os.getcwd()}/{directory}")
	with open(filename, "r") as f:
		lines = f.read().split("\n")
	if filter:
		lines = filter_list(lines)
	return lines

def write_file(filename, msg):
	with open(filename, "w") as f:
		f.write(msg)

def append_file(filename, msg):
	with open(filename, "a") as f:
		f.write(msg)

def filter_list(lines, filename=False):
	if filename:
		lines = read_file(filename)
	data = []
	for line in lines:
		if line[:1] != "#" and line != "":
			data.append(line)
	return data


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
		if not cmd[:1] == "/":
			cmd = f"/{cmd}"
		return self.mcr.command(cmd)

	def list_players(self):
		resp = self.run("list").split()
		return f"{resp[2]}/{resp[7]}"

	# Requires Authentication
	def whitelist_add(self, player):
		resp = self.run(f"whitelist add {player}")


if __name__ == "__main__":
	print("Wrong module, switchihng to \"bot.py\"...")
	os.system("python bot.py")
