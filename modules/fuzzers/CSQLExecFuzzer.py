##      XSQLExecFuzzer.py
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

from lib.module import CIngumaFuzzerModule
from lib.libinformix import simpleFuzzer

name = "ifxfuzz"
brief_description = "An Informix SQLEXEC fuzzer"
type = "fuzzer"

class CSQLExecFuzzer(CIngumaFuzzerModule):

    def help(self):
        """ This is the entry point for info <module> """
        self.gom.echo("target = <target host or network>")
        self.gom.echo("port = <target port>")
        self.gom.echo("timeout = <timeout>")

    def run(self):
        if self.target == "":
            self.gom.echo("[+] No target specified, using 'localhost'")
            self.target = "localhost"

        if self.port == 0 or self.port == None:
            self.gom.echo("[+] No port specified, using 9088 (sqlexec)")
            self.port = 9088

        return simpleFuzzer(self.target,  self.port,  self.timeout)
