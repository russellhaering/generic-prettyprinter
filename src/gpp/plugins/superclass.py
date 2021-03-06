#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys

class   MetaPrettyPrinter( object ):

    def __init__( self ):
        self.reset()
        return

    def reset( self ):
        self.out    = sys.stdout
        self.fileno = 0
        self.lineno = 0
        self.filename = None
        self.multi = 0
        return

    def advise( self, **kwargs ):
        for key in kwargs:
            if key == 'argc':
                self.multi = kwargs[key]
        return

    def do_name( self, name ):
        if os.path.isfile( name ):
            self.do_file( name )
        elif os.path.isdir( name ):
            self.do_dir( name )
        elif os.path.islink( name ):
            self.error( 'ignoring symlink "%s".' % name )
        else:
            self.error( 'unknown file type, ignoring "%s".' % name )
            raise ValueError
        return

    def begin_file( self, fn ):
        if self.multi > 1:
            self.println( 'File %d of %d: %s' % (self.fileno, self.multi, fn) )
            self.println()
        return

    def end_file( self, fn ):
        self.report()
        if self.fileno < self.multi:
            self.println()
        self.filename = None
        self.lineno = 0
        return

    def next_line( self, s ):
        self.println( s )
        return

    def do_file( self, fn ):
        try:
            f = open( fn, 'rt' )
        except Exception, e:
            self.error( 'cannot open "%s" for reading.' % fn, e )
            raise e
        self.fileno += 1
        self.filename = fn
        self.lineno = 0
        self.begin_file( fn )
        self.do_open_file( f )
        self.end_file( fn )
        f.close()
        return

    def do_open_file( self, f = sys.stdin ):
        for line in f:
            self.lineno += 1
            self.next_line( line.rstrip() )
        return

    def ignore( self, name ):
        return False

    def do_dir( self, dn ):
        try:
            files = os.listdir( dn )
        except Exception, e:
            self.error( 'cannot list directory "%s".' % dn, e )
            raise e
        files.sort()
        for fn in files:
            if not self.ignore( fn ):
                self.do_name( os.path.join( dn, fn ) )
        return

    def println( self, s = '' ):
        print >>self.out, s
        return

    def report( self, final = False ):
        return

    def finish( self ):
        self.report( final = True )
        return

    def error( self, msg, e = None ):
        if self.filename is not None:
            print >>sys.stderr, 'File %s: ' % self.filename,
        if self.lineno > 0:
            print >>sys.stderr, 'Line %d: ' % self.lineno,
        print >>sys.stderr, msg
        if e is not None:
            print >>sys.stderr, e
            raise e
        return
