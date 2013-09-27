#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# nohup.py 
# Copyright (C) 2013  Alex Revetchi
#
# nohup.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
 This is a python implementation of the well known nohup utility.

 * If the standard output is a terminal, all output written to
 * its standard output shall be appended to the end of the file
 * nohup.out in the current directory.  If nohup.out cannot be
 * created or opened for appending, the output shall be appended
 * to the end of the file nohup.out in the directory specified
 * by the HOME environment variable.
'''
import os
import sys
import signal

if len(sys.argv) < 2:
	print "usage: nohup.py utility [arg ...]"

def dofile():
	p='nohup.out'
	try:
		fd = open(p, 'a', 0)
	except:
		home = os.getenv('HOME')
		if not home:
			sys.stderr.write("can't open a %s file\n" %p)
			sys.exit(127)
		p=home + '/' + p
		try:
			fd = open(p, 'a', 0)
		except:
			sys.stderr.write("can't open a %s file\n" %p)
			sys.exit(127)

	try:
		os.dup2(fd.fileno(), sys.stdout.fileno())
	except:
		sys.exit(127)
	sys.stderr.write("sending output to %s\n" %p)

def donohup(argv):
	if os.isatty(sys.stdout.fileno()):
		dofile()

	try:
		if os.isatty(sys.stderr.fileno()):
			os.dup2(sys.stdout.fileno(), sys.stderr.fileno())
	except:
		print 'Could not redirect stderr\n'
		os.exit(127)

	signal.signal(signal.SIGHUP, signal.SIG_IGN)
	os.execvp(argv[1], argv[1:])

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "usage: nohup.py utility [arg ...]"
		os.exit(-1)

	donohup(sys.argv)
