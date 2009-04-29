#!/usr/bin/env python

#    Copyright (C) 2006  Andrew Straw  <strawman@astraw.com>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import os, stat, errno
# pull in some spaghetti to make this stuff work without fuse-py being installed
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse

def bash(command):		
	return os.popen(command).read().split("\n")[:-1]

def log(arg):
	bash("echo "+arg+" >> ~/desktop/log")

installed_apps = []
a = bash("dpkg --get-selections")
for item in a:
    if not "deinstall" in item:
        installed_apps.append("/"+item.split()[0])

if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

hello_path = installed_apps[:5]
hello_str = 'Hello World!\n'

class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

def get_target_file_path(path):
	application = path[1:].split("/")[0]
	relative_path = path[1:][len(application):]
	if relative_path == "":
		relative_path = "/"
	#log("relative_path"+relative_path)
	return relative_path

class HelloFS(Fuse):


	def getattr(self, path):
		#log("path "+path)
		st = MyStat()
		if path == '/':
			st.st_mode = stat.S_IFDIR | 0755
			st.st_nlink = 2
		elif path in hello_path:
			st.st_mode = stat.S_IFDIR | 0755
			st.st_nlink = 2 
		else:
			#log("in the else bit")
			if os.path.isdir(get_target_file_path(path)):
				#log("dir")
				st.st_mode = stat.S_IFDIR | 0755
				st.st_nlink = 2
			else:
				#log("file")
				st.st_mode = stat.S_IFREG | 0444
				st.st_nlink = 1
				
				st.st_size = len(open(get_target_file_path(path), 'rb').read())#len(hello_str)        			        			
#        elif not path in hello_path:
 #           st.st_mode = stat.S_IFREG | 0444
  #          st.st_nlink = 1
   #         st.st_size = len(hello_str)
#		else:#if "/"+path.split("/")[1] in hello_path:
#			st.st_mode = stat.S_IFDIR | 0755
#			st.st_nlink = 2            
#        else:
 #           return -errno.ENOENT
		return st

	def readdir(self, path, offset):
			if path == "/":
				for r in  ['.', '..'] + list(item[1:] for item in hello_path):
					yield fuse.Direntry(r)
			else:
				application = path[1:].split("/")[0]
				#log(application)
				relative_path = path[1:][len(application):]
				#log(relative_path)
				file_list = bash("dpkg -L "+application) #should cache this
				files = []
				for item in file_list:
					if item[:len(relative_path)] == relative_path: #same start bit
						filename_to_show = item[len(relative_path)+1:].split("/")[0]
						if not filename_to_show in files and not filename_to_show == "": #to stop dupes, as there will be loads
							#log("filename_to_show "+filename_to_show)
							files.append(filename_to_show) #the bit before the slash directly after the relative path
				for r in  ['.', '..'] + files:
					yield fuse.Direntry(r)

	def open(self, path, flags):
		if False:#not path in hello_path:
			return -errno.ENOENT
		accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
		if (flags & accmode) != os.O_RDONLY:
			return -errno.EACCES

	def read(self, path, size, offset):
		if False:#not path in hello_path:
			return -errno.ENOENT
		f = open(get_target_file_path(path), 'rb').read()
		content = f #previously content = hello_str
		#content = encode(content)
		log(content)
	
		
		slen = len(content)
		if offset < slen:
			if offset + size > slen:
				size = slen - offset
				buf = content[offset:offset+size]
			else:
				buf = ''
		return buf

def main():
    usage="""
Userspace hello example

""" + Fuse.fusage
    server = HelloFS(version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')

    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
