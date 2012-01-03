#
# s3_converter.py
#
# Copyright: Tim Desjardins - (c) 2007 BlogMatrix.com
# Copyright: Ben Bridts - (c) 2011-2012 benbridts.be
#
# License: Use at your own risk, don't contact us if you have problems or for
# support.
#
#

import os
import re
import sys
import time

debug = False
file_out = sys.stdout
error_count = 0
line_count = 0

def process_file( file_name, fout ) :
	""" process a file, given file_name and write the results to fout."""
	reader = file( file_name )

	for x in reader :
		process_line( x, fout )

	reader.close()

def debug_sm( sm ) :
	""" debug the regex. """
	print "------------------------------------"
	print sm.group( 'ip' )
	print sm.group( 'date' )
	print sm.group( 'get' )
	print sm.group( 'status' )
	print sm.group( 'bytes1' )
	print sm.group( 'url' )
	print sm.group( 'user_agent' )
	print "------------------------------------"
	
#
# this regex was built using Pyreb
#
split_re = '[\w\:\-_\#\$\%\@]*\s(?P<uri>.+?)\s(?P<date>\[\d\d/\w\w\w/\d\d\d\d:\d\d:\d\d.+\])\s(?P<ip>[\d\.\w]+)\s(?P<requester>[\-\w]+)\s(?:\w+\s[\w\.\d]+)\s(?P<file_name>[\w\d\.\-_/%]*)\s\"(?P<get>[\w\d\.\-_\S /]*)\"\s(?P<status>\d\d\d)\s[\-\w]+\s(?P<bytes1>[\d\-]+)\s(?P<bytes2>[\d\-]+)\s(?P<bytes3>[\d\-]+)\s(?P<bytes4>[\d\-]+)\s"(?P<url>.*)"\s"(?P<user_agent>.*)"$'

split_rex = re.compile( split_re, re.VERBOSE )

def process_line( line, fout ) :
	""" process a line, write the resulting converted line to fout. """
	global error_count, line_count, split_rex
	sm = split_rex.match( line )
	line = line.rstrip( os.linesep)
	line = line.rstrip( ' -0123456789' )
	line_count += 1

	if sm:
		if debug:
			debug_sm(sm)

		print >> fout, """%(ip)s - - %(date)s "%(get)s" %(status)s %(bytes1)s "%(url)s" "%(user_agent)s" """ % sm.groupdict()
	else:
		error_count += 1
		if debug:
			print >> sys.stderr, " Error: ", error_count, "\n", line

#
# parse command line args
#
def optParser( args = None  ) :
	from optparse import OptionParser

	parser = OptionParser()
	parser.add_option( "", "--debug", action="store_true", default = False, dest = "debug", help = "")
	parser.add_option( "", "--fileout", default = "", dest = "file_out", help = "")
	parser.add_option( "", "--verbose", action="store_true", default = False, dest = "verbose", help = "")

	return parser.parse_args()

#
# Main
#
if __name__ == "__main__" :
	( options, args ) = optParser()

	debug = options.debug
	if options.file_out :
		file_out = file( options.file_out, "w" )

	if len( sys.argv ) > 1 :
		# read from a file(s)
		for arg in args :
			process_file( arg, file_out )
	else :
		# read from stdin
		reader = sys.stdin

		for line in reader :
			process_line( line, file_out )

	file_out.close()

	if options.verbose:
		print " lines processed: ", line_count
		print " errors: ", error_count
