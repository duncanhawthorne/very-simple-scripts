#! /usr/bin/env python
#disablegss.py 
#  
#  Copyright (c) 2006 crazy___cow@hotmail.com
# 
#  This program is free software; you can redistribute it and/or 
#  modify it under the terms of the GNU General Public License as 
#  published by the Free Software Foundation; either version 2 of the
#  License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
#  USA


 
import dbus
import dbus.glib
import sys
import os
import string
import time
from stat import *



def disable_sleep(myprogram): 
	try:
		bus = dbus.Bus(dbus.Bus.TYPE_SESSION)
      		devobj = bus.get_object('org.freedesktop.PowerManagement',  '/org/freedesktop/PowerManagement/Inhibit')
      		dev = dbus.Interface(devobj, "org.freedesktop.PowerManagement.Inhibit")
      		cookie = dev.Inhibit(myprogram, 'Disabled by DisableGSS Daemon')
		print "DisableGSS: power manager stopped."		
      		return (dev, cookie)
	except Exception, e:
      		print "DisableGSS: could not send the dbus Inhibit signal: %s" % e
		#sys.exit(0)		
		return (False, False)


def allow_sleep(dev, cookie):
	try:
		dev.UnInhibit(cookie)
		print "DisableGSS: power manager enabled."
		return(True)	
	except Exception, e:
      		print "DisableGSS: could not send the dbus UnInhibit signal: %s" % e
		#sys.exit(0)
		return (False)


def pids(program):
	result = []
	f = os.popen('ps aux', 'r')
	for l in f.readlines():
		fields = string.split(l)
		if fields[10] == program:
			#print fields[1]+"   "+fields[10]
			return(True)



def read_file():
	__psaux = []
	try:
		f=open(homedir+'/.disablegss', 'r')
		for line in f:
			#print line.rstrip('\n')
			__psaux.append(line.rstrip('\n'))
		f.close();
		print "DisableGSS: config file read."		
		return __psaux
	except IOError:
		print "DisableGSS: config file ~/.disablegss doesn't exist! Write it by hand. Add applications name that could disable gnome screensaver: one app name for every line of file."
		sys.exit(0)





if __name__ == '__main__':
	state = "screen"

	homedir = os.getenv('HOME')
	condition = True
	disabled = False
	old_program = ""
	psaux = []
	last_last_time_modified = ""
	last_time_modified = ""
	
	psaux=read_file()
	last_time_modified=	os.stat(homedir+'/.disablegss')[ST_MTIME]
	last_last_time_modified=last_time_modified

	while condition == True:
		if os.system("pactl list | grep Client:") == 0:
			
   			print "somthing is playing audio"
			program=psaux[0]
			old_program=program
			found = True
			if disabled==False:	
				(dev, cookie) = disable_sleep(program)
				disabled=True
		else:
			found = False
			for i in range(len(psaux)):
				#print "%s->%s" % (i,psaux[i]) 
				program=psaux[i]
				if pids(program) == True:
					found = True
					if program !=old_program:
						print "DisableGSS: there is a program ("+program+") in the config list that is currently running."		
						old_program=program
					if disabled==False:	
						(dev, cookie) = disable_sleep(program)
						disabled=True
						break
		
		if found == False and disabled == True:
			print "DisableGSS: there are no more programs that could stop gnome screensaver."
			allow_sleep(dev, cookie)
			disabled = False
		time.sleep(60)		
		last_time_modified=	os.stat(homedir+'/.disablegss')[ST_MTIME]
		if last_time_modified!=last_last_time_modified:
			print "DisableGSS: config file modified."		
			psaux=read_file()
			last_time_modified=	os.stat(homedir+'/.disablegss')[ST_MTIME]
			last_last_time_modified=last_time_modified
			old_program = ""
		#condition=False
			


