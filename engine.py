"""
## Main utility module

Contains useful functions

`from utils.engine import *` to import most common functions

Saves you having to do `engine.foo()` every time you cal a function

\- prov3ntus
"""

__VERSION__ = "v1.5"

import os, sys, ctypes

import PIL.Image

# Global vairables
UTILS_DIR		= os.path.dirname( os.path.abspath( __file__ ) )
ROOT_DIR		= os.path.abspath( os.path.join( UTILS_DIR, os.path.pardir ) )
GDT_UTILS_DIR	= os.path.join( UTILS_DIR, 'GDT_Utils' )
CONFIG_PATH		= os.path.join( ROOT_DIR, 'configuration.conf' ) # Unused
ASSETS_DIR		= os.path.join( ROOT_DIR, "assets" ) # Unused
DEBUG_STR		= "[    DEBUG    ]       "
ERROR_STR		= "[    ERROR    ]       "
WARNING_STR		= "[   WARNING   ]       "
CONSOLE_STR		= "[   CONSOLE   ]       "

true = True
false = False
undefined = None

# when you use "from engine import *", you have to define the things it imports with the __all__ variable:
__all__ = [ 'UTILS_DIR', 'ROOT_DIR', 'GDT_UTILS_DIR', 'CONFIG_PATH', 'ASSETS_DIR', 'DEBUG_STR', 'ERROR_STR', 'WARNING_STR', 'CONSOLE_STR', 'true', 'false', 'undefined' ]



# Init level
class GVar():
	__info = 'Global variable utilisation. No more worrying about variable scopes (Updates across scripts)'

# Change to "gvars" someday??
level = GVar() # Init default GVar
level.errors_occured = false

__all__.append( 'level' )



# Wait - like GSC
from time import sleep

def wait( n_time_to_wait : int | float ) -> None:
	sleep( n_time_to_wait ); 

__all__.append( 'wait' )



# Info Message Box
def MsgBox( title: str, text: str, style: int ):
	"""
	Message Box Styles: 
	
	MB_ABORTRETRYIGNORE = 2

	MB_CANCELTRYCONTINUE = 6

	MB_HELP = 0x4000

	MB_OK = 0

	MB_OKCANCEL = 1

	MB_RETRYCANCEL = 5

	MB_YESNO = 4

	MB_YESNOCANCEL = 3


	MB_ICONEXCLAMATION = MB_ICONWARNING = 0x30

	MB_ICONINFORMATION = MB_ICONASTERISK = 0x40

	MB_ICONQUESTION = 0x20

	MB_ICONSTOP = MB_ICONERROR = MB_ICONHAND = 0x10


	MB_DEFBUTTON1 = 0

	MB_DEFBUTTON2 = 0x100

	MB_DEFBUTTON3 = 0x200

	MB_DEFBUTTON4 = 0x300


	MB_APPLMODAL = 0

	MB_SYSTEMMODAL = 0x1000

	MB_TASKMODAL = 0x2000


	MB_DEFAULT_DESKTOP_ONLY = 0x20000

	MB_RIGHT = 0x80000

	MB_RTLREADING = 0x100000


	MB_SETFOREGROUND = 0x10000

	MB_TOPMOST = 0x40000

	MB_SERVICE_NOTIFICATION = 0x200000


	IDABORT = 3

	IDCANCEL = 2

	IDCONTINUE = 11

	IDIGNORE = 5

	IDNO = 7

	IDOK = 1

	IDRETRY = 4

	IDTRYAGAIN = 10

	IDYES = 6
	"""
	return ctypes.windll.user32.MessageBoxW(0, text, title, style)

__all__.append( 'MsgBox' )

# Pillow Installer
import subprocess
import sys

def InstallPillow():
	os.system("cls || clear");

	print( "This program requires pillow, which handles image processing." );
	wait( 1.25 );

	while( True ):
		print( "You do not have pillow" );
		wait( 1 );
		print( "Would you like to install now? \ny | n" );
		option = input( " --> " ).lower();
		if( option == "yes" or option == "y" ):
			break;
		else:
			print( "You must install pillow to use this application." );
			wait( 1.75 );
			
			print( "Quit? \ny | n" );
			quit_input = input( " --> " ).lower();
			quit = True if( quit_input != "no" or quit_input != "n" ) else False;
			
			if( quit is True ):
				sys.exit();
			continue;

	os.system("cls || clear")

	wait(1)
	print("Installing Pillow...")
	wait(1)

	print(f"\n{ '=' * 40 }\n")
	wait(0.5)

	# implement pip as a subprocess:
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pillow'])

	print("\n\nPillow installed successfully.\n\n")
	wait(0.75)
	print("Exiting...")
	wait(0.5)


# Progress bar

# Print iterations progress
def printProgressBar( iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r" ):
	"""
	Call in a loop to create terminal progress bar
	
	### @params:

		iteration   - Required  : current iteration (Int)

		total       - Required  : total iterations (Int)

		prefix      - Optional  : prefix string (Str)

		suffix      - Optional  : suffix string (Str)

		decimals    - Optional  : positive number of decimals in percent complete (Int)

		length      - Optional  : character length of bar (Int)

		fill        - Optional  : bar fill character (Str)

		printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)

	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
	# Print New Line on Complete
	if iteration == total: print()



# Write print lines to console.log
import logging

# Init log
logging.basicConfig( 
	level=logging.INFO, 
	filename=os.path.join( ROOT_DIR, "console.log" ), 
	filemode="w+", 
	format="%(asctime)-15s %(levelname)-8s %(message)s"
)

logging.info( f'{ "=" * 100 }' )
logging.info( f'{ "=" * 100 }' )

def PrintLn( *print_args, sep: str = ' ', end: str ='\n' ):
	"""
	Prints to console & writes print statements to `console.log`

	`console.log` can be found in pardir of engine.py
	"""

	print_str = ''
	
	for idx in range( len( print_args ) ):
		item = print_args[ idx ]

		if( not type( item ) == str ):
			item = str( item )
		
		print_str += item

		if( not idx == len( print_args ) - 1 ):
			print_str += sep
	
	print_str +=  bcolors.ENDC
	print( print_str, sep=sep, end=end )
	logging.log( logging.INFO, print_str.replace( '\033[', '' ) )

def log( *args ):
	"""
	Writes a statements to `console.log`.

	`console.log` can be found in cwd
	"""
	log_str = ''

	for item in args:
		if( not type( item ) == str ):
			item = str( item )
		
		log_str += item
	
	log_str +=  bcolors.ENDC
	logging.log( logging.INFO, log_str.replace( '\033[', '' )[ :-2 ] )

# Colour text when printing
class bcolors:
	"""
	Class of constants to color console text when printing

	Usage: print( bcolors.OKBLUE + "This text is blue" + bcolors.ENDC + engine.Bold(" and now it's BOLD!") );
	"""
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def RaiseWarning( *args, sep = ' ', end = '\n' ):
	_print_str = bcolors.WARNING + WARNING_STR + ' '
	for idx in range( len( args ) ):
		_print_str += str( args[ idx ] )

		if( not idx == len( args ) - 1 ):
			_print_str += sep
		
	PrintLn( _print_str, sep = sep, end = end )

def RaiseError( *args, sep = ' ', end = '\n' ):
	_print_str = bcolors.FAIL + ERROR_STR + ' '
	for idx in range( len( args ) ):
		_print_str += str( args[ idx ] )

		if( not idx == len( args ) - 1 ):
			_print_str += sep
		
	PrintLn( _print_str, sep = sep, end = end )

def Bold( *_args, sep = ' ' ):
	"""Returns a string with a bold format. 

	If you were to print this string, text would be bold in console
	
	You must clear console first for cmd otherwise it'll break"""
	_str = ''
	for idx in range( len( _args ) ):
		_str += str( _args[ idx ] )

		if( not idx == len( _args ) - 1 ):
			_str += sep
	
	return bcolors.BOLD + _str + bcolors.ENDC

def Underline( *_args, sep = ' ' ):
	"""Returns a string with an underlined format. 

	If you were to print this string, text would be underlined in console
	
	You must clear console first for cmd otherwise it'll break"""
	_str = ''
	for idx in range( len( _args ) ):
		_str += str( _args[ idx ] )

		if( not idx == len( _args ) - 1 ):
			_str += sep

	return bcolors.UNDERLINE + _str + bcolors.ENDC

_tuple = ( 'PrintLn', 'log', 'RaiseError', 'RaiseWarning', 'Bold', 'Underline', 'bcolors' );
for _str in _tuple: __all__.append( _str );
del _tuple



units_of_time = (
	( 'weeks',          86400 * 7   ),
	( 'days',           86400       ),
	( 'hours',          3600        ),
	( 'minutes',        60          ),
	( 'seconds',        1           ),
	( 'milliseconds',   0.001       )
)

def DisplayTime( seconds, granularity=2 ):
	"""
Converts the given time from seconds into a readable time format (useful when displaying time elapsed from engine.timer())

E.g.:
- 180 (w/ a granularity of 2) would return "3 minutes"
- 192 (w/ a granularity of 2) would return "3 minutes, 12 seconds"
- 3604 (w/ a granularity of 2) would return "1 hour, 4 seconds"
- 4825 (w/ a granularity of 2) would return "1 hour, 20 minutes"
- 4825 (w/ a granularity of 3) would return "1 hour, 20 minutes, 25 seconds"
	"""
	result = []

	for name, count in units_of_time:
		value = seconds // count
		if value:
			seconds -= value * count
			if value == 1:
				name = name.rstrip('s')
			result.append("{} {}".format(int(value), name))
	return ', '.join(result[:granularity])


byte_intervals = (
	( 'GB',     10**9   ),
	( 'MB',     10**6   ),
	( 'KB',     10**3   ),
	( 'bytes',  1       ),
	( 'bits',   0.125   )
)

def DisplaySize( bytes, granularity=2 ):
	"""
Converts a given byte int into readable str based on it's size
(useful when displaying size of files with enigne.GetFileSize()-like funcs)

E.g.:
- 650211430 (w/ a granularity of 2) would return "650 MB, 211 KB"
- 650211430 (w/ a granularity of 3) would return "650 MB, 211 KB, 430 bytes"
	"""
	result = []

	for name, count in byte_intervals:
		value = bytes // count
		if value:
			bytes -= value * count
			if value == 1:
				name = name.rstrip('s')
			result.append("{} {}".format(value, name))
	
	return ', '.join(result[:granularity])


from cv2 import imread

def GetImageDimensions( _img_path: str ):
	return imread( _img_path ).shape[ :2 ];

def ImageHasAlpha( image_path: str ):
	'''
	Returns True if image path has alpha channel
	'''
	img = PIL.Image.open( image_path )

	if img.info.get( "transparency", None ) is not None:
		return True

	if img.mode == "P":
		transparent = img.info.get( "transparency", -1 )
		for _, index in img.getcolors():
			if index == transparent:
				return True
	elif img.mode == "RGBA":
		extrema = img.getextrema()
		if extrema[3][0] < 255:
			return True

	return False


def GetFolderSize( _dir : str, granularity : int = 3 ):
	"""Returns the folder size in MB"""
	n_size = 0
	for path, dirs, files in os.walk( _dir ):
		for f in files:
			full_path = os.path.join( path, f )
			n_size += os.path.getsize( full_path )
	n_size = DisplaySize( n_size, granularity )
	return n_size

def GetFileSize( _filedir, granularity : int = 3 ):
	"""Returns the respective file size in MB"""
	return DisplaySize( os.path.getsize( _filedir ), granularity )

def GetFileArraySize( _filedirarray, granularity : int = 3 ):
	"""Returns the total file size of all the file paths in an array in MB"""
	n_size = 0
	for _dir in _filedirarray:
		n_size += os.path.getsize( _dir )
	n_size = DisplaySize( n_size, granularity )
	return n_size

def DeleteFile( _path: str | os.PathLike ) -> None:
	"""
PERMANENTLY deletes a file from the path given
	"""
	os.remove( _path )

def StripAll( _str : str, *strip_args ):
	"""
Basically does the work of str.strip()

But instead you can pass multiple chars and it will strip all the chars from the string, 1 by 1

### @params:
	
	_str - String to be stripped

	*strip_args - chars to strip from string
	"""
	for chars in strip_args:
		chars = str( chars )
		_str = _str.replace( chars, '' )
	
	return _str



def IsDefined( __param ):
	try:
		return True if __param is not None else False
	except NameError:
		return False

def IS_TRUE( __param ):
	return True if( __param is True or __param == True ) else False

def IS_EVEN( __number ):
	return True if ( __number % 2 ) == 0 else False

def IS_ODD( __number ):
	return True if ( __number % 2 ) == 1 else False

def DEFAULT( __var, __default ):
	if not IsDefined( __var ):
		return __default
	return __var

_tuple = ( 'IsDefined', 'IS_TRUE', 'IS_EVEN', 'IS_ODD', 'DEFAULT' );
for _ in _tuple: __all__.append( _ );
del _tuple;

from tkinter import filedialog
# v1.4 - 24th March, 2024
def UserOpenDir( **options ) -> str:
	"""
	Opens a file dialogue & requests the user to open a folder
	"""
	return filedialog.askdirectory( **options )

def UserOpenFile( b_multiple_files = False, **options ) -> str:
	"""
	Opens a file dialogue & requests the user to open a file or multiple files
	"""
	if( b_multiple_files ):
		return filedialog.askopenfilenames( **options )
	else:
		return filedialog.askopenfilename( **options )

def UserSaveAsFile( **options ) -> str:
	"""
	confirmoverwrite: bool | None = ...,

    defaultextension: str | None = ...,

    filetypes: Iterable[tuple[str, str | list[str] | tuple[str, ...]]] | None = ...,

    initialdir: StrOrBytesPath | None = ...,

    initialfile: StrOrBytesPath | None = ...,

    parent: Misc | None = ...,

    title: str | None = ...,

    typevariable: StringVar | str | None = ...
	"""
	return filedialog.asksaveasfilename( options )



def GetParentDir( __file__: str | os.PathLike, dirs_to_move_up: int = 1 ) -> str | os.PathLike | None:
	_path = __file__
	for i in range( dirs_to_move_up ):
		_path = os.path.abspath( os.path.join( _path, os.pardir ) )
	
	return _path

	# My code:
	#indexes = [i for i in range(len(__file__)) if __file__.startswith(( '\\', '/' ), i)]
	#return __file__[ :indexes[ -1 ] ]




def GetDirName( __file__: str | os.PathLike ):
	""" 
	Gets the directory of the folder from a file path
	"""
	return GetFolderName( __file__ )

def GetFolderName( __file__: str | os.PathLike ):
	""" 
	Gets the directory of the folder from a file path
	"""
	return os.path.dirname( __file__ )

def GetFileName( __file__: str | os.PathLike, extention: bool = False ) -> str:
	"""
	Retuns the file name from a full file path ( w/ an extention if 'extention' param is true )
	"""
	if not extention:
		return os.path.splitext( os.path.basename( __file__ ) )[0]
	return os.path.basename( __file__ )

def GetBaseName( __file__: str | os.PathLike, extention: bool = False ) -> str:
	"""
	Retuns the file name from a full file path ( w/ an extention if 'extention' param is true )
	"""
	return GetFileName( __file__, extention )

def GetFileType( __file__: str | os.PathLike ) -> str:
	"""
	Returns the extention of a file

	E.g. '.png'
	"""
	return os.path.splitext( __file__ )[1]

def GetFileExtention( __file__: str | os.PathLike ) -> str:
	"""
	Retuns the extention of a file

	E.g. '.png'
	"""
	return GetFileType( __file__ )

def GetFileTypesInDir( dir, file_format: str | list | tuple ) ->  str | list[ str ]:
	list = []
	
	if( type( file_format ) == str ):
		for f in os.scandir( dir ):
			if( f.name.endswith( file_format ) ):
				list[ len( list ) ] = f.name
		return list
	
	return True if( [ [ f.name for f in os.scandir( dir ) if f.name.endswith( type_ ) ] for type_ in file_format ] ) else False

def GetFilesInDir( dir: str | os.PathLike, full_path=False, extention: str = None, include_dirs: bool = True ) -> list[ str ]:
	"""
	Returns all the files in the directory

	Can optionally include directories as well

	### @params:

	"full_path" - True returns the full path to the file, false only the file

	"extention" - can filter by file type

	"include_dirs" - Can choose whether to return directories ( true ) or skip them ( false )
	"""
	files = []; 
	if not full_path:
		if not extention is None:
			for f in os.scandir( dir ):
				if os.path.isdir( f ) and not include_dirs:
					continue;
				if f.name.endswith( extention ):
					files.append(f.name); 
		else:
			for f in os.scandir( dir ):
				if os.path.isdir( f ) and not include_dirs:
					continue;
				files.append(f.name);
		
		return files
	
	# Code below runs if full_path = true
	if not extention is None:
		for f in os.scandir( dir ):
			if os.path.isdir( f ) and not include_dirs:
				continue;
			if f.name.endswith( extention ):
				files.append( os.path.join( dir, f.name ) ); 
	else:
		for f in os.scandir( dir ):
			if os.path.isdir( f ) and not include_dirs:
				continue;
			files.append( os.path.join( dir, f.name ) ); 
	
	return files

def SearchFileForKeyword( file_path: str | os.PathLike, kword: str, return_idx=False, return_all=True ) -> str | int | list[ str | int ]:
	"""
	Searches a file and returns a list of all lines in that file that have the keyword in.

	If nothing is found it returns an empty list.

	### @params:

	if all is False, it will return the first occurence.

	If return_idx is True, then it will return the line numbers.
	"""

	with open( file_path, 'r' ) as f:
		lines = f.readlines(); 
		matches = []; 
		matches_idx = []; 
		for line in lines:
			idx = lines.index( line ); 
			if( line.find( kword ) != -1 ):
				matches.append( line ); 
				matches_idx.append( idx ); 
				if not return_all:
					break;

	if matches == []:
		return []

	if not return_idx:

		if not return_all:
			return matches[0] # Return 1st match
		
		return matches # Return all matches
	
	if not return_all:
		return matches_idx[0] # Return line number of 1st match
	
	return matches_idx # Return line number of all matches

_tuple = ( 'GetParentDir', 'GetDirName', 'GetFolderName', 'GetFileName', 'GetBaseName', 'GetFileType', 'GetFileExtention', 'GetFileTypesInDir', 'GetFilesInDir', "SearchFileForKeyword" );
for _str in _tuple: __all__.append( _str );
del _tuple;


def Concatenate( *__params: str | int | float, sep: str = '' ):
	"""
	Concatenates all params, with an optional separator defined by doing sep=
	"""
	concatenation = ''
	for string in __params:
		concatenation += str( string ) + sep
	return concatenation

def Concat( *__params: str | int | float, sep: str = '' ):
	"""
	Concatenates all params, with an optional separator defined by doing sep=
	"""
	return Concatenate( *__params, sep=sep )

def ClearConsole():
	os.system( "cls || clear" ); 

_tuple = ( "Concatenate", "Concat", "ClearConsole" );
for _str in _tuple: __all__.append( _str );
del _tuple



from time import perf_counter

def timer():
	return perf_counter(); 

__all__.append( 'timer' );



def GetPyVersion():
	"""
	Returns current python version.

	E.g. will return 3.11
	"""
	
	return Concatenate( sys.version_info[ 0 ], '.', sys.version_info[ 1 ] )



def init( _str : str = 'INIT' ):
	ClearConsole()
	print( f'{"="*40} { _str } {"="*40}' )

def __exit__( input_str: str = 'Press [ENTER] to exit...' ):
	"""
	Exits application after input
	"""
	if level.errors_occured:
		RaiseWarning( "Errors occured. Check console.log in the root of this program:", os.path.join( ROOT_DIR, 'console.log' ) )
	input( input_str );
	sys.exit();