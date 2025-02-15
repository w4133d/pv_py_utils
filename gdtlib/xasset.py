"""
## XAsset Module, v0.4 beta - prov3ntus

Python utility module defining objects of assets in APE, as well as the GDT itself.

Enables you to write/pull assets to/from GDTs, streamlining GDT automation in python.

Currently supported XAssets:
- XMaterials
- XImages
- XModels
\- pv
"""

import os
from math import log2
from pv_py_utils import *

VERBOSE_LOG = false

"""
TODO:

- Hierarchy images of the same material to the diffuse image

- If attempting to write a duplicate asset, compare properties to the one in the GDT and (ask to) update

- GDT.Delete() leaves a tab where it deletes the asset

- Create a JSON parser modified for GDTs for cleaner memory manipulation of assets (GDTN)
	- When instantiating a GDT from disk, parse it and load all of its contents into memory.
	- Creating a GDT during runtime should be equivalent to instantiating an empty GDT from disk.
"""

def mw4_get_semantic( _hex: str ):
	"""
	Gets the scemantic type from the mw4_semantics dictionary
	"""
	_hex = _hex.removeprefix( 'unk_semantic_' )
	
	return mw4_semantics[ _hex ]

# Finish me if you ever decide to do full mw2019 supp :)
mw4_semantics = {
	'0x0' : 'c&s',
	'0x1' : 'c&s',
	'0x2' : 'c&s',
	'0x9' : '',
	'0xA' : '',
	'0xB' : '',
	'0x1C' : '',
	'0x1D' : '',
	'0x3B' : '',
	'0x3C' : '',
	'0x3D' : '',
	'0x7B' : '',
	'0x7C' : ''
}



class XAsset():

	AssetTypes = {
	"mat"   	: 'material.gdf',
	"mtl"   	: 'material.gdf',
	"xmtl"   	: 'material.gdf',
	"material"	: 'material.gdf',
	"xmaterial"	: 'material.gdf',
	"img" 		: 'image.gdf',
	"image" 	: 'image.gdf',
	"anim"  	: 'xanim.gdf',
	"xanim"  	: 'xanim.gdf',
	"model" 	: 'xmodel.gdf',
	"xmodel" 	: 'xmodel.gdf'
	}

	def __init__( self, asset_name: str, asset_type: str ) -> None:
		"""Abstract class that contains common variables for XAssets"""
		self.name = asset_name
		self.type = XAsset.AssetTypes[ asset_type.removesuffix( '.gdf' ) ]
	
	def __str__( self ):
		return f'{self.type.removesuffix( ".gdf" )} asset \'{self.name}\''

	def __repr__( self ):
		return f'XAsset({self.name}, {self.type})'
	
	def save_to( self, _gdt ):
		_gdt.NewAsset( self )




# --XMODEL
class XModel( XAsset ):

	LOD_LEVELS : dict[ int : str ] = {
		0 : "filename",
		1 : "mediumLod",
		2 : "lowLod",
		3 : "lowestLod",
		4 : "lod4File",
		5 : "lod5File",
		6 : "lod6File",
		7 : "lod7File"
	}

	class BulletCollLevels:
		NONE = 'None'
		CUSTOM = 'Custom'
		LOD0 = 'High'
		LOD1 = 'Medium'
		LOD2 = 'Low'
		LOD3 = 'Lowest'
		LOD4 = 'LOD4'
		LOD5 = 'LOD5'
		LOD6 = 'LOD6'
		LOD7 = 'LOD7'

	def __init__( self, xmodel_name: str, lod_paths_array: list[ str ] | tuple[ str ] = [], bullet_col_lod: BulletCollLevels = BulletCollLevels.NONE, shadow_lod: str = 'Auto' ) -> None:
		"""
		### @params
		`xmodel_name` | Will be the name of the XModel asset in APE.
		If you've ripped xmodel_bin files from Greyhound, then you should make this the file name (excluding the LOD level on the end)

		`lod_paths_array` | A list or tuple of strings, with a max item count of 8 (because you can only have 8 LODs maximum)

		`bullet_col_lod` | A LOD level to set the bullet collision LOD to in APE (e.g. 'LOD1').\n
		You need this set to something other than 'None' (as it is by default) if you want the XModel to show bullet impacts when it's shot, or if 'SetCanDamage()' can be enabled in scripts for this model if it's a script_model in radiant

		`shadow_lod` | A LOD level to use when calculating shadow lighting. In APE (& this class) by default, it's set to 'Auto'
		"""
		super().__init__( xmodel_name, 'model' )

		self.LODs: dict[ str : str ] = {}
		self.shadow_lod = shadow_lod

		self.bullet_col_lod = bullet_col_lod

		# ADD LOD PATHS
		lod_paths_array = lod_paths_array[ :8 ]

		# Make the path relative to the model_export folder
		# If its in the bo3 root, then add a '../' to it
		# console.log( "Lod paths array before:", lod_paths_array )
		_steam_path = 'steamapps/common/Call of Duty Black Ops III/'
		
		for idx, lod in enumerate( lod_paths_array ):
			lod = lod.replace( '\\', '/' )
			if _steam_path + 'model_export/' in lod:
				lod_paths_array[ idx ] = lod.split( _steam_path + 'model_export/' )[ -1 ]
			elif _steam_path in lod:
				lod_paths_array[ idx ] = '../' + lod.split( _steam_path )[ -1 ]

		# console.log( "Lod paths array after:", lod_paths_array )

		for idx in range( len( lod_paths_array ) ):
			self.LODs[ XModel.LOD_LEVELS[ idx ] ] = lod_paths_array[ idx ]

		# Let's say lod_paths_array only has 3 LOD paths in. 
		# We would still need to define the other 5 LODs, even if they're 
		# empty, so we don't get an error when trying to generate the asset for GDT
		for idx in range( 8 - len( lod_paths_array ) ):
			self.LODs[ XModel.LOD_LEVELS[ len( lod_paths_array ) + idx ] ] = ''
	

	def GenerateGDTAsset( self ) -> list[ str ]:
		with open( f'pv_py_utils\\gdtlib\\templates\\{ self.type }' ) as f:
			data = f.read()
		
		lod_paths = list( self.LODs.values() )

		return data.format(
			_asset_name = self.name,
			bullet_col_lod = self.bullet_col_lod,
			shadow_lod = self.shadow_lod,
			lod0 = lod_paths[ 0 ],
			lod1 = lod_paths[ 1 ],
			lod2 = lod_paths[ 2 ],
			lod3 = lod_paths[ 3 ],
			lod4 = lod_paths[ 4 ],
			lod5 = lod_paths[ 5 ],
			lod6 = lod_paths[ 6 ],
			lod7 = lod_paths[ 7 ]
		)
	
	def __repr__( self ):
		return f'XModel({self.name}, {self.LODs}, {self.bullet_col_lod}, {self.shadow_lod} )'



# --XIMAGE
class XImage( XAsset ):

	Semantics = {
		'default' : '2d',
		'_c' : 'diffuseMap',
		'_g' : 'glossMap',
		'_n' : 'normalMap',
		'_o' : 'occlusionMap',
		'_r' : 'revealMap',
		'_s' : 'specularMap' # specMap has colour, specMask doesn't
	}

	def get_compression_method( self ) -> tuple:
		"""
		Returns a tuple of compression methods available for that semantic type

		(Just use the 1st index in most cases)
		"""
		if self.pbr_type == 'diffuseMap':
			return ( 'compressed high color', 'compressed low color', 'compressed no alpha', 'uncompressed' )
		
		return ( 'compressed', 'uncompressed' )

	def __init__( self, image_name: str = '', file_path: str = '' ) -> None:
		"""
		### @params:

		`image_name` | What the image will actually be called in APE, e.g. "i_pv_brushed_metal_c"\n
		(ideally, you want "image_name" to just be the file name, so you can keep files organised. Upon __init__, the "i_" will be appended if not already present.)

		`file_path` | The path to the image file.

		Note: XImage uses the file's name to determine semantic type (colorMap, normalMap, glossMap, etc.).
		Please ensure that the image's file name is suffixed correctly (e.g. "i_bricks_worn_white_c" AND NOT "i_bricks_worn_white")

		XImage will default to the semantic "2d" (like APE does) if there is no suffix.
		"""
		#if not image_name.startswith( 'i_' ) and image_name != '':
		#	image_name = 'i_' + image_name

		super().__init__( image_name, 'image' )
		self.path = file_path
		self.pbr_type = XImage.Semantics[ 'default' ]
		self.no_mip_maps = 0

		if self.name == '' or self.path == '':
			return

		# DETERMINE SEMANTIC
		# 1. Attempt to look for mtl_images.txt that comes in the _images folder (it's not in the images folder lol tf was i thinking about)
		"""
		print( gvar.mtl_text_files_dir )
		_mtl_file = engine.GetFilesInDir( gvar.mtl_text_files_dir, full_path=True, extention='.txt', include_dirs=False )
		if not len( _mtl_file ) ):
			RaiseError( 'Greyhound's images.txt files could not be found in chosen directory' )
			raise FileNotFoundError( 'There are no .txt files in the mtl_images.txt directory. Please make sure you\'ve chosen the right directory, and try agian.' )
		self.pbr_type = engine.SearchFileForKeyword( _mtl_file[0], self.name, all=False ).split( ',' )[0] # Needs finishing to account for unk_semantics
		"""

		# 2. Fallback - Determine semantic type based on suffix of the 
		# image file name e.g. "wooden_barrier_c.png" is an albedo map
		if self.pbr_type is None or self.pbr_type == '2d':
			_file_name = pathlib.get_base_name( self.path )

			_suffix = '_' + _file_name.split( '_' )[ -1 ]
			try:
				self.pbr_type = XImage.Semantics[ _suffix ]
			except KeyError:
				log.error( 'asset.py -> class XImage -> __init__(): Defaulting XImage', _file_name + '.png', f'to 2d - Unrecognised suffix "{_suffix}"' )
				gvar.errors_occurred = true

			for _suffix, _type in XImage.Semantics.items():

				if _file_name.endswith( _suffix ):
					self.pbr_type = _type
					break

		self.compression_method = self.get_compression_method()[0]

		# Image dimension checks
		for _dim in image.get_dimensions( self.path ):
			if not _dim:
				break
				
			if not log2( _dim ).is_integer():
				self.no_mip_maps = 1 # Disable mipMaps
				if _dim % 4 != 0:
					self.compression_method = self.get_compression_method()[ -1 ] # Diable compression
				
				break
		
	
	def GenerateGDTAsset( self ) -> list[ str ]:
		with open( f'pv_py_utils\\gdtlib\\templates\\{ self.type }' ) as f:
			data = f.read()

		if self.path == '':
			_path = ''
		else:
			_path = self.path.split( 'Call of Duty Black Ops III' + '\\' )[1].replace( '/', '\\' ).removeprefix( '\\' )

		return data.format(
			_asset_name		= self.name,
			_file_path		= _path,
			_pbr_type		= self.pbr_type,
			_compression	= self.compression_method,
			no_mip_maps		= self.no_mip_maps
		)

	def __repr__( self ):
		return f'XImage({self.name}, {self.path}, pbr_type={self.pbr_type}, compression_method={self.compression_method}, no_mip_maps={self.no_mip_maps})'



# --XMATERIAL --XMTL
class XMaterial( XAsset ):

	SURFACE_TYPES: tuple[ str ] = (
		"<none>", "asphalt", "brick", "carpet", "ceramic", "cloth", "concrete", "dirt", "flesh", "foliage", "glass", "grass",
		"gravel", "ice", "metal", "mud", "paper", "plaster", "plastic", "rock", "rubber", "sand", "snow", "water", "wood",
		"cushion", "fruit", "paintedmetal", "tallgrass", "riotshield", "bark", "player", "metalthin", "metalhollow",
		"metalcatwalk", "metalcar", "glasscar", "glassbulletproof", "watershallow", "bodyarmor"
	)

	GLOSS_SURFACE_TYPES: tuple[ str ] = (
		"<custom>", "<full>", "asphalt", "brick", "carpet", "ceramic", "cloth", "concrete",
		"dirt", "skin", "foliage", "glass", "gravel", "ice", "metal", "mud", "paint", "paper",
		"plaster", "plastic", "rock", "rubber", "sand", "snow", "water", "wood", "bark"
	)

	def __init__( self, mtl_name: str = "", _ximages: list[ XImage ] = None, mtl_category: str = 'Geometry', mtl_type: str = 'lit', surface_type: str = '<none>', gloss_range: str = '<full>', usage: str = '<not in editor>' ) -> None:
		"""
### @params:
		
mtl_name		| The name of the material asset\n
_ximages		| An array of XImage assets that belong to the XMtl. Semantic will be determined from file name suffix and applied respectively.\n
E.g. an XImage w/ the name "pv_pbr_texture_01_c" will be a color map, "_g" for gloss, and so on\n
mtl_category	| E.g. "Geometry", "Geometry Advanced", "2d", "Weapons", etc.\n
mtl_type		| Deps. on mtl_category. E.g. "lit", "lit_plus", "lit_emissive", "lit_alphatest_advanced_fullspec", etc.\n
surface_type	| Fallback for surface type. If XMaterial fails to determine one from the mtl name, it will default to this.\n
E.g. if my mtl name is "pv_street_asphalt_damaged_03", it will separate the underscores & recognise asphalt, applying that type\n
gloss_range		| Fallback for gloss surface type. 

### List of surface types (for reference):
- <none> (default)
- asphalt
- brick
- carpet
- ceramic
- cloth
- concrete
- dirt
- flesh
- foliage
- glass
- grass
- gravel
- ice
- metal
- mud
- paper
- plaster
- plastic
- rock
- rubber
- sand
- snow
- water
- wood
- cushion
- fruit
- paintedmetal
- tallgrass
- riotshield
- bark
- player
- metalthin
- metalhollow
- metalcatwalk
- metalcar
- glasscar
- glassbulletproof
- watershallow
- bodyarmor

### List of gloss ranges (for reference):
- <custom>
- <full> (default)
- asphalt
- brick
- carpet
- ceramic
- cloth
- concrete
- dirt
- skin
- foliage
- glass
- gravel
- ice
- metal
- mud
- paint
- paper
- plaster
- plastic
- rock
- rubber
- sand
- snow
- water
- wood
- bark
		"""
		super().__init__( mtl_name, 'mtl' )

		# Set defaults
		self.mtl_category 	= mtl_category
		self.surface_type 	= surface_type # Fallback surface type if one can't be determined below
		self.gloss_range 	= gloss_range # Fallback gloss type if one can't be determined below
		self.mtl_type		= mtl_type
		self.radiant_usage 	= usage

		# DETERMINE SURFACE TYPE
		for _type in XMaterial.SURFACE_TYPES:
			if _type in self.name.lower():
				self.surface_type = _type
		
		# DETERMINE GLOSS SURFACE TYPE
		for _type in XMaterial.GLOSS_SURFACE_TYPES:
			if _type in self.name.lower():
				self.gloss_range = _type

		self.ximages = {
			'revealMap' 	: XImage(),
			'diffuseMap' 	: XImage(),
			'glossMap' 		: XImage(),
			'normalMap' 	: XImage(),
			'occlusionMap' 	: XImage(),
			'specularMask' 	: XImage()
		}

		if _ximages:
			has_normal_map = false
			for _ximg in _ximages:
				self.ximages[ _ximg.pbr_type ] = _ximg
				
				# DETERMINE MTL TYPE
				if image.has_alpha( _ximg.path ):
					self.mtl_type = 'lit_alphatest'
				
				# DETERMINE MTL CATEGORY
				if _ximg.pbr_type in ( 'specularMap', 'specularMask' ):
					self.mtl_category = 'Geometry Advanced'
					self.mtl_type += '_advanced'

				elif _ximg.pbr_type in ( 'glossMap', 'occlusionMap' ) and '_advanced' not in self.mtl_type:
					self.mtl_category = 'Geometry Plus'
					if not self.mtl_type.endswith( '_plus' ): self.mtl_type += '_plus'

				if _ximg.pbr_type == 'normalMap':
					has_normal_map = true

			if VERBOSE_LOG:
				if _ximages.__len__() == 0:
					log.warning( f"XMaterial '{self.name}' has no XImage assets" )
				elif not has_normal_map:
					log.warning( f"XMaterial '{self.name}' has no normal map" )
					#gvar.errors_occurred = true



	def GenerateGDTAsset( self ) -> str:
		with open( f'pv_py_utils\\gdtlib\\templates\\{ self.type }' ) as f:
			data = f.read()
		
		# Texture maps
		_reveal = self.ximages[ "revealMap" 	].name
		_color 	= self.ximages[ "diffuseMap" 	].name
		_gloss 	= self.ximages[ "glossMap" 		].name
		_normal = self.ximages[ "normalMap" 	].name
		_occlu	= self.ximages[ "occlusionMap" 	].name
		_spec	= self.ximages[ "specularMask" 	].name

		# Category info
		_surface_type	= self.surface_type
		_gloss_range	= self.gloss_range
		_mtl_category	= self.mtl_category
		_mtl_type		= self.mtl_type
		_usage			= self.radiant_usage

		return data.format(
			_asset_name	= self.name,
			reveal_map	= _reveal,
			col_map		= _color,
			gloss_map	= _gloss,
			normal_map	= _normal,
			ao_map		= _occlu,
			spec_mask	= _spec,
			srfc_type	= _surface_type,
			gloss_range	= _gloss_range,
			category	= _mtl_category,
			mtl_type	= _mtl_type,
			usage		= _usage
		)



# --GDT FILE
class GDT():

	def __init__( self, _gdt_path: str ) -> None:
		"""
		Object that represents a GDT file.

		Has various utility functions.

		Options:
		
		`@param` `_gdt_path` | The absolute path to the GDT
		"""
		
		self.n_asset_count = 0
		
		if pathlib.get_file_ext( _gdt_path ) != '.gdt':
			_gdt_path += os.path.join( pathlib.get_dir_name( _gdt_path ), pathlib.get_base_name( _gdt_path ) + '.gdt')
		
		self.path = _gdt_path
		self.name = pathlib.get_base_name( self.path )
		
		if not pathlib.exists( self.path ):
			raise FileNotFoundError( f"Cannot find GDT '{self.name}.gdt'" )

		with open( self.path, 'r' ) as f:
			data = f.read()

		if not ( stdlib.strip_all( data, '\n', '\t', ' ', '{', '}' ) == '' ):
			with open( self.path, 'r' ) as self.file:
				lines = self.file.readlines()
			self.n_asset_count = lines.count( '{' ) - 1 if len( lines ) > 0 else 0 # quick way to check asset count

			while lines[ -1 ] == '\n':
				lines = lines[ :-1]  # remove all empty lines
			#lines = lines[ :-1 ] # remove the } at the end of the GDT in memory
			
			with open( self.path, 'w' ) as self.file:
				self.file.writelines( lines )
		else: # Wipes the file if it has no assets in, and starts writing to it
			with open( self.path, 'w' ) as f:
				f.write( '{\n}' )
		
		self.lines = self._readlines()
		
		# Create asset types dictionary
		# Key: <asset_type>, Value: <asset_name>
		self.asset_types: dict[ str : list[ str ] ] = {}
		
		for _type in XAsset.AssetTypes.values():
			self.asset_types[ _type ] = []

		_gdt_lines = self.lines
		for line in _gdt_lines:
			if not line.__contains__( '" ( "' ):
				continue
			
			kvp = line.strip().split( '"' )
			# Visualisation:
			# kvp = ['', 'i_pv_modular_building_kit_01_c', ' ( ', 'image.gdf', ' )']
			asset_name = kvp[ 1 ]
			asset_type = kvp[ -2 ]

			# if not IsDefined( self.asset_types.get( asset_type ) ):
			# 	self.asset_types[ asset_type ] = []
			
			self.asset_types[ asset_type ].append( asset_name )

			# Check for child assets
			for child in self.__get_child_assets( asset_name ):
				self.asset_types[ asset_type ].append( child )
		
		# Order lists of asset types alphabetically
		for type in self.asset_types:
			self.asset_types[ type ] = sorted( self.asset_types[ type ] )

		

	
	def IsEmpty( self ):
		#return true if engine.StripAll( self.file.read(), '\n', '\t', ' ' ) in ( '{}', '' ) else false
		return self.n_asset_count == 0

	def GetAsset( self, asset_name: str ) -> XImage | XModel | dict:
		pass # Needs to utilise GetAssetRaw and create a respective XAsset object from the data

	def GetAssetRaw( self, asset: XImage | XMaterial | XModel | str, dict_return: bool = false ) -> str | dict[ str, str ]:
		"""
		Returns the raw data of the asset from the GDT for copying assets 
		to / from GDTs, or for when they have properties unsupported by the 
		pv_py_utils that need to be preserved.
		
		If the asset is a child, it crawls to each parent recursively and gets all unchanged overrides.

		If `dict_return` is true, then an extra "name" key will be added before any other key, as the name 
		is only preserved in a str return (when`dict_return` is false)

		Returns an empty str if the asset doesn't exist in the GDT.
		"""

		if not self.asset_exists( asset ):
			log.warning( f'Could not find {"" if type( asset ) is str else asset.type.replace( ".gdf", "" ) + " "}asset "{asset if type( asset ) is str else asset.name}" in GDT file { self.path.split( 'Black Ops III' )[ -1 ] }' )
			return undefined

		raw_data = self._read()
		
		if type( asset ) is not str:
			_search_kwds = ( f'"{asset.name}" ( "{asset.type}" )', f'"{asset.name}" [' )
		else:
			_search_kwds = ( f'"{asset}" (', f'"{asset}" [' )
		
		# Slice gdt str from where it finds the asset to where it finds the next '}' after
		for kwd in _search_kwds:
			start_idx = raw_data.find( kwd )

			if start_idx != -1: break
		
		# Check if parented assets are the correct asset type

		#start_idx = raw_data.find( f'"{asset}" (' )
		#start_idx = start_idx if start_idx != -1 else raw_data.find( f'"{asset}" [' )
		raw_data = raw_data[ start_idx: ]
		raw_data = raw_data[ :raw_data.find( '}' ) + 1 ]
		#print( "Raw data of asset:\n\n", raw_data )

		raw_lines = raw_data.splitlines()
		has_parent = '[' in raw_lines[ 0 ]

		if has_parent or dict_return:
			_dict = {
				'name': asset if type( asset ) is str else asset.name
			}
			for line in raw_lines:
				if any( kwd in line for kwd in ( '{', '}', '(', '[' ) ):
					continue

				kvp = line.strip().replace( '"', '' ).split()
				if kvp.__len__() == 1:
					_dict[ kvp[ 0 ] ] = ""
				else:
					_dict[ kvp[ 0 ] ] = kvp[ 1 ]

			if not has_parent: return _dict

			# It's got a parent, recurse
			par_name = raw_lines[ 0 ].split( '"' )[ -2 ]
			d_parent_xdata = self.GetAssetRaw( par_name, dict_return=true )
			# Add non-override parent xdata to child's xdata
			for par_key in d_parent_xdata:
				if par_key in _dict.keys():
					continue
				_dict[ par_key ] = d_parent_xdata[ par_key ]
			
			if dict_return: return _dict

			# They're expecting a str if the script reaches this point, so we need to put the dict back into the GDT format
			__xdata = '\n'.join( f'\t\t"{key}" "{_dict[ key ]}"' for key in _dict )
			
			raw_data = stdlib.concat(
				f'\t"{_dict[ 'name' ]}" [ "{par_name}" ]',
				'\t{',
				__xdata,
				'\t}',
				sep='\n'
			)

		return raw_data

	def GetAssetNamesByGDF( self, gdf_type: str ) -> list[ str ]:
		"""
		Gets the names of all XAssets in a GDT with a specific asset type (.gdf)

		gdf_type | The type of asset to grab all the names of, e.g. 'material', 'image', 'xmodel', 'xanim', etc. (you can optionally suffix with .gdf)
		"""
		if( not gdf_type.endswith( '.gdf' ) ): gdf_type += '.gdf'
		asset_names = []
		gdt_lines = self._readlines()

		for line in gdt_lines:
			if f'( "{gdf_type}" )' not in line:
				continue

			split = line.strip().split()
			name = split[0].replace( '"', '' )

			"""
			if '_' not in name and name != '': # Validation check
				log_error( f"xasset -> GDT -> {inspect.currentframe().f_code.co_name}: Could not find underscore in asset name '{name}'" )
				gvar.errors_occurred = true
				continue
			"""

			asset_names.append( name )

		# Search for child assets
		for par_name in asset_names:
			__child_names = self.__get_child_assets( par_name )

			if __child_names.__len__():
				asset_names += __child_names

		return asset_names

	def __get_child_assets( self, __parent: str ) -> list[ str ]:
		_child_assets: list[ str ] = []
		for _line in self.lines:
			if '[ ' not in _line: continue

			parent_name = _line.strip().split( '"' )[-2]
			if parent_name == __parent:
				child_name = _line.strip().split( '"' )[1]
				_child_assets.append( child_name )

				# Recursively check if this child is a parent
				_child_assets += self.__get_child_assets( child_name )
		
		return _child_assets
	
	parent_recursions = 0 # Debug

	def __get_parent_assets( self, __child: str ) -> list[ str ] | str:
		_parent_assets = []
		for _line in self._readlines():
			if f'"{__child}" [' not in _line: continue

			parent_name = _line.strip().split( '"' )[-2]
			_parent_assets.append( parent_name )
			# Add parent's parent to the list if the parent is a child
			if self.asset_is_child( parent_name ):
				self.parent_recursions += 1
				_parent_assets += self.__get_parent_assets( parent_name )
		
		return _parent_assets
	
	def asset_is_child( self, _asset: str ):
		return true if f'"{_asset}" [ ' in self._read() else false

	def get_asset_count( self ):
		"""Returns `self.n_asset_count`
		"""
		self.n_asset_count = self._read().count( '{' ) - 1
		return self.n_asset_count

	def asset_exists( self, asset: XModel | XMaterial | XImage | str ):
		"""
		Returns true if the asset exists in the GDT

		Limitations:
		- Passing only a str into the `asset` param will not be able to check for 
		asset type.
		- (NOT THE CASE ANYMORE) xasset.GDT will also not be able to check for asset type if the asset is a child
		"""
		if type( asset ) is str:
			for line in self._readlines():
				if any( kwd in line for kwd in ( f'"{asset}" (', f'"{asset}" [' ) ):
					return true
		else:
			return stdlib.binary_search( asset.name, self.asset_types[ asset.type ] ) is not undefined

		# Old new method that reads parent asset type (uses __get_parent_assets(), which is MUCH slower)
		# Need to implement a better method by getting assets by searching for '{' & storing a dict 
		# of the assets & their type. (note from future me: done, see 'else' statement above)
		# I'll have to recursively check for parents there anyway, however I'll be able to do it on the fly
		# and only when I encounter a child asset
		"""
		else:
			for line in self._readlines():
				if f'"{asset.name}" ( "{asset.type}" )' in line:
					return true
				
				# Check if the asset is a child
				if '[ ' in line:
					print( "looking for parent assets" )
					parents = self.__get_parent_assets( asset )
					if parents:
						_parent = parents[ -1 ]
						for _line in self._readlines():
							if f'"{_parent}" ( ' not in _line: continue
							# "vm_ap9_ads_acog_down" ( "xanim.gdf" )
							parent_type = _parent.split( '"' )[-2]
							if parent_type == asset.type:
								return true
		"""
		
		"""
		# Old, faster method (doesn't read asset type if asset is a child)
		if type( asset ) is not str:
			_search_kwds = ( f'"{asset.name}" ( "{asset.type}" )', f'"{asset.name}" [' )
		else:
			_search_kwds = ( f'"{asset}" (', f'"{asset}" [' )
		
		data = self._read()
		
		for _str in _search_kwds:
			if _str in data:
				return True
		"""
	
		return false

	def HasAsset( self, asset: XModel | XMaterial | XImage | str ):
		"""
		Returns true if the asset exists in the GDT
		"""
		return self.asset_exists( asset )
	
	def Delete( self, asset: XImage | XMaterial | XModel ):
		"""
		Deletes & purges passed asset from the GDT

		### !!! WARNING: THIS WILL DELETE THE ASSET PERMANENTLY

		`@param` `asset` | An XAsset that is in the GDT
		"""
		asset_raw = self.GetAssetRaw( asset )

		if not asset_raw:
			console.error( f"Failed to delete { asset }, it does not currently exist in the GDT" )

		with open( self.path ) as f:
			raw = f.read()
		with open( self.path, 'w' ) as f:
			f.write( raw.replace( asset_raw, '' ) )
		
		# Remove asset from GDT asset types table
		self.asset_types[ asset.type ].remove( asset.name )

	

	def ParentTo( self, asset: XAsset | XImage | XMaterial | XImage | XModel | str, new_parent: XAsset | XImage | XMaterial | XImage | XModel ):
		"""
		TODO
		Parents the asset in param1 to the asset in param2 <--------------------------------------------------------- FINISH ME
		"""

		if asset.type != new_parent.type:
			console.error( f"Failed to parent {asset} to {new_parent} beause the asset types are different ({asset.type.removesuffix( '.gdf' )} vs. {new_parent.type.removesuffix( '.gdf' )}). Child assets need to be the same asset type as their parents." )
			return

		if not self.asset_exists( asset ):
			console.error( f"Failed to parent {asset} to {new_parent} because {asset} does not exist in the GDT {self.name}.gdt." )
			return

		...

	def MakeChildOf( self, asset: XAsset | XImage | XMaterial | XImage | XModel | str, new_parent: XAsset | XImage | XMaterial | XImage | XModel | str ):
		self.ParentTo( asset, new_parent )
	
	def NewAsset( self, asset: XImage | XMaterial | XModel ) -> None:
		"""
		Creates a new asset in the GDT (same as right clicking in APE & pressing 'New Asset')

		### @params:

		`asset` | an XAsset to be written to the GDT
		"""

		if self.asset_exists( asset ):
			log.warning( f"Tried to write { asset }', but an asset with that name already exists. Skipping..." )
			#gvar.errors_occurred = true
			return

		gdt_data = self._read()

		if gdt_data.strip() == '':
			gdt_data += '{\n}'
		elif gdt_data.strip().endswith( '}' ):
			gdt_data = gdt_data[ :-2 ] + '\n'

		with open( self.path, 'w' ) as self.file:
			self.file.writelines( gdt_data + asset.GenerateGDTAsset() + '\n}' )

		self.n_asset_count += 1
	
	def WriteAsset( self, asset: XImage | XMaterial | XModel ) -> None:
		"""
		Creates a new asset in the GDT (same as right clicking in APE & pressing 'New Asset')

		@params:

		asset = an XAsset to be written to the GDT
		"""
		self.NewAsset( asset )
	
	def _read( self ) -> str:
		with open( self.path ) as file: __str = file.read()
		return __str

	def _readlines( self ) -> list[ str ]:
		with open( self.path ) as file: __list = file.readlines()
		return __list



	def __clean_up__( self ):
		"""
		Cleans up and optimises the GDT:
		- Hierarchies each image to the color map of the material to lower GDT size (APE optimisation)
		- ... that's all it does for now lol
		"""

		line_array = self._readlines()
		ximages: list[ tuple[ int, str ] ] = [] # Filter out ximages

		# Get all the image asset names
		for idx, line in enumerate( line_array ):
			if '( "image.gdf" )' not in line:
				continue

			name = line.split( '"' )[1]
			if line.endswith( '_c' ): continue
			base_name = name[ :name.rindex( '_' ) ]
			ximages.append( ( idx, base_name ) )

		"""
		"i_pv_city_new_york_01_o" ( "image.gdf" )
		                         ^ splitting here & keeping left side
		"""
		for _line_idx, _base in ximages:
			
			if not self.asset_exists( _base + '_c' ):
				#print( "Could not find colour map for line:\n" + line_array[ _line_idx ][ :-1 ] )
				continue

			# Extra safety measure to avoid parenting an asset to itself
			if _base + '_c' in line_array[ _line_idx ]:
				continue
			
			new_line = line_array[ _line_idx ].split( ' ' )[0] + f' [ "{_base + "_c"}" ]\n'
			line_array[ _line_idx ] = new_line
			#print( "new_line =", new_line[ :-1 ] )

		with open( self.path, 'w' ) as self.file:
			if len( line_array ) != 0:
				self.file.writelines( line_array )
			
			

	def save_gdt( self, optimise_gdt: bool = true ) -> None:
		self.CloseGDT( optimise_gdt )
	
	def CloseGDT( self, optimise_gdt: bool = true ) -> None:
		
		file_data = self._read()

		if file_data.strip() == '':
			return

		file_data = self._readlines()

		while file_data[ -1 ] == '\n':
			print( "CloseGDT(): Last line was a new line" )
			file_data = file_data[ :-1 ]

		if not file_data[ -1 ] == '}':
			file_data += '}'
		
		file_data += '\n'
		with open( self.path, 'w' ) as self.file:
			self.file.writelines( file_data )
		
		if optimise_gdt:
			self.__clean_up__()





__all__ = [
	'XImage',
	'XMaterial',
	'XModel',
	'GDT',
	'mw4_get_semantic'
	]




