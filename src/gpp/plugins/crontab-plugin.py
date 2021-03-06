#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'crontab-pp'
	DESCRIPTION = """Display crontab files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.entries = []
		self.vars    = []
		self.widths  = {}
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].strip()
		if line.find( '=' ) > -1:
			tokens = line.split( '=', 1 )
			self.vars.append( [ tokens[0].strip(), tokens[1].strip() ] )
		else:
			tokens = line.split()
			if len(tokens) >= 6:
				tokens[5] = tokens[5:]
				for i in xrange( 0, 6 ):
					try:
						self.widths[i] = max( self.widths[i], len(tokens[i]) )
					except:
						self.widths[i] = len(tokens[i])
				self.entries.append( tokens[:6] )
		return

	def	report( self, final = False ):
		if len(self.vars) > 0:
			for (n,v) in sorted(self.vars):
				print '%s=%s' % (n, v)
		if len(self.entries) > 0:
			fmt = ''
			sep = ''
			for i in xrange( 0, 6 ):
				fmt = fmt + ('%s%%%ds' % (sep, self.widths[i]))
				sep = '  '
			self.entries.sort()
			for tokens in self.entries:
				print fmt % (
					tokens[0],
					tokens[1],
					tokens[2],
					tokens[3],
					tokens[4],
					' '.join(tokens[5])
				)
		self._prepare()
		return
