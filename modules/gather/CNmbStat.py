#!/usr/bin/python

"""
Module NmbStat for Inguma
Copyright (c) 2007 Joxean Koret <joxeankoret@yahoo.es>

License is GPL
"""

import sys

from lib.core import getMacVendor
from impacket import smb, nmb
from lib.libexploit import CIngumaModule

name = "nmbstat"
brief_description = "Gather NetBIOS information for target"
type = "gather"

class CNmbStat(CIngumaModule):
    target = ""
    port = 8000
    waitTime = 0
    timeout = 1
    exploitType = 1
    services = {}
    results = {}
    dict = None
    url = None
    interactive = True
    data = []
    isWin32 = False
    macVendor = ""
    masterBrowser = False

    def help(self):
        print "target = <target host or network>"
        print "port = <target port>"

    def showHelp(self):
        print 

    def run(self):
        FIXED_SIZE = 17
        if self.target == "":
            self.gom.echo( "[!] No target specified, using localhost as target" )
            self.target = "localhost"

        objNmb = nmb.NetBIOS()
        self.data = []

        for node in objNmb.getnodestatus("*", self.target):
            data = node.get_nbname()

            data = data.replace("\x02", "").replace("\x01", "")

            if len(data) < FIXED_SIZE:
                data += " "*(FIXED_SIZE - len(data))
            else:
                data = data[:FIXED_SIZE]
            
            if data.find("__MSBROWSE__") > -1:
                self.masterBrowser = True

            x = nmb.NAME_TYPES.get(node.get_nametype(), "?")
            if len(x) < FIXED_SIZE:
                x += " "*(FIXED_SIZE - len(x))
            else:
                x = x[:FIXED_SIZE]

            data += x
            mac = objNmb.getmacaddress()
            if mac == "00-00-00-00-00-00":
                self.isWin32 = False
            else:
                self.isWin32 = True
                self.macVendor = getMacVendor(mac.replace("-", ""))
            self.mac = mac
            data += " " + mac

            if node.is_active():
                data += " ACTIVE "
            if node.is_group():
                data += " GROUP "
            if node.is_deleting():
                data += " DELETING"
            if node.is_conflict():
                data += " CONFLICT "
            if node.is_permanent():
                data += " PERMANENT "

            self.data.append(data)

        return True

    def printSummary(self):
        self.gom.echo( "NetBIOS Information" )
        self.gom.echo( "-------------------" )
        self.gom.echo( "" )

        for line in self.data:
            self.gom.echo( line )
        self.gom.echo( "" )

        if self.masterBrowser:
            self.gom.echo( "Is a Master Browser." )

        if self.isWin32:
            self.gom.echo( "MAC Address: " + self.mac.replace("-", ":") + " (" + self.macVendor + ")" )
            self.gom.echo( "Is a Windows based server." )
        else:
            self.gom.echo( "Is an Unix based server (Samba)." )

