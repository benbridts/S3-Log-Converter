#
# s3_converter.py
#
# Tim Desjardins - (c) 2007 BlogMatrix.com
#
# License: Use at your own risk, don't contact us if you have problems or for
# support.
#
# $Id: $
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
split_re = '[\w\:\-_\#\$\%\@]*\s(?P<uri>.+?)\s(?P<date>\[\d\d/\w\w\w/\d\d\d\d:\d\d:\d\d.+\])\s(?P<ip>[\d\.\w]+)\s(?:\w+\s\w+\s[\w\.\d]+)\s(?P<file_name>[\w\d\.\-_/]+)\s\"(?P<get>[\w\d\.\-_ /]*)\"\s(?P<status>\d\d\d)\s\-\s(?P<bytes1>\d+)\s(?P<bytes2>[\d\-]+)\s(?P<bytes3>[\d\-]+)\s(?P<bytes4>[\d\-]+)\s"(?P<url>.*)"\s"(?P<user_agent>.*)"$'

split_rex = re.compile( split_re, re.VERBOSE )

def process_line( line, fout ) :
	""" process a line, write the resulting converted line to fout. """
	global error_count, line_count, split_rex
	sm = split_rex.match( line )
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

	# testing
	##line = '9aa09e9d583a00ee9af2097bc421c6e08ee545ef5aecd859b2845489e12303e7 media.company.ca [18/Feb/2007:18:24:54 +0000] 72.137.197.138 65a018a28cdf8ec538ec3d1ccaae921c 1220FB5A0864EA78 REST.GET.OBJECT 2006/english/design/graphic.jpg "GET /2006/english/design/graphic.jpg HTTP/1.1" 200 - 30475 30475 1200 84 "http://www.company.ca/en/home/" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.9) Gecko/20061206 Firefox/1.5.0.9"'
	##line = '2007-02-18-16-16-50-193FDED5EADCE4E1:7aa09e9d883a00ee9af2097bc481c6e0fee545ef5aecd859b28854f9e12303e7 media.company.ca [18/Feb/2007:15:47:05 +0000] 74.107.211.39 9aa09e9d513a00ee8af2097bc421c6e0fee545ef8necd859b28454f9e12303e7 2C814085338D0FAF REST.GET.BUCKET - "GET /media.company.ca HTTP/1.1" 200 - 57898 - 163 96 "-" "-"'
	#line = '2007-02-18-19-16-46-1E2C24CFF4E8A383:9aa09e3d513a00ee9af2097bc431c6e0fee545ef5aecd859b28453f9e12303e7 media.company.ca [18/Feb/2007:18:24:59 +0000] 72.137.197.138 65a011a29cdf3ec533ec3d1ccaae981c 56DC85AB751C4309 REST.GET.OBJECT 2006/english/graphic.jpg "GET /2006/english/graphic.jpg HTTP/1.1" 200 - 31088 31088 560 64 "http://www.company.ca/en/home/" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.9) Gecko/20061206 Firefox/1.5.0.9"'

	##process_line( line, sys.stdout )

	"""
	192.167.2.111 - - [08/Dec/2006:20:42:46 -0500] "GET /post-2006-11-28-0005/ HTTP/1.1" 200 14994 "http://poster.company.org/approved/language/" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.8) Gecko/20061025 Firefox/1.5.0.8"
	"""

"""
2007-02-18-16-16-50-193FDED8EADCE9E1:9aa09e2d513a00ee9af7097bc421c6e0fee575ef5aecd959b28454f9e12303e7 media.company.ca [18/Feb/2007:15:47:05 +0000] 74.107.211.39 9aa07e9d573a00ee9af2047bc421c6e3fee525ef5aecd859b28454f9e12303e7 2C844005336D0FAF REST.GET.BUCKET - "GET /media.company.ca HTTP/1.1" 200 - 57898 - 163 96 "-" "-"
"""

# 9aa09e9d813a00ee9af2097bc428c6e0fee545ef5aecd889b28454f9e12303e7 media.company.ca [18/Feb/2007:18:24:54 +0000] 72.137.197.138 65a011a29cdf88c533ec3d8ccaae921c 1228FB5A8064EA88 REST.GET.OBJECT 2006/english/design/graphic.jpg "GET /2006/english/design/graphic.jpg HTTP/1.1" 200 - 30475 30475 1200 84 "http://www.company.ca/en/home/" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.9) Gecko/20061206 Firefox/1.5.0.9"

"""
74.107.211.39 - - [18/Feb/2007:15:52:59 +0000] "GET /2006/english/movie.mov HTTP/1.1" 200 17412392 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1" 

69.159.67.225 - - [18/Feb/2007:06:19:12 -0500] "GET /root/include/style.css HTTP/1.1" 200 3137 "http://recent.company.ca/" "Mozilla/4.0 (compatible; MSIE 6.0; WindowsNT 5.1; FunWebProducts; .NET CLR 1.0.3705)"
"""
