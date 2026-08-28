## THE FLAVOURMOD ENTRYPOINTS FROM THE SDK

from __future__ import division
from CvPythonExtensions import *
import CvUtil
import PyHelpers
import sys

## *******************
## Modular Flavour Start: estyles 25-Oct-2010
import os
import CvPath # path to current assets

import warnings
warnings.filterwarnings("ignore", "The xmllib module is obsolete.", DeprecationWarning, "xmllib")
# Yes, but the new xml.sax is not included. So I have to use it.
from xmllib import XMLParser, Error as xmllibError

## End Modular Flavour Start

## GLOBAL VARIABLES (do not change):

gc = CyGlobalContext()
dice = gc.getGame().getSorenRand()
cymap = CyMap()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

DEBUG_ENABLE_LOGGING = False

## GLOBAL TUNING VARIABLES (make your changes here):

# turn the main features of FlavourMod on or off:

ASSIGN_FLAVOURFUL_STARTING_LOCATIONS = True
ASSIGN_FLAVOURFUL_UNIQUE_IMPROVEMENT_LOCATIONS = True
ASSIGN_FLAVOURFUL_HOLDFAST_LOCATIONS = True
FLAVOURFUL_NORMALIZATION = True
RELOCATE_DANGEROUSLY_CLOSE_UNIQUE_IMPROVEMENTS_ONLY = False

# change size of area in which will be searched for plots matching flavour:

CORE_SEARCH_AREA_RADIUS = 2		# full weigt for matches in here (should be the same like the city radius)
EXTRA_SEARCH_AREA_RADIUS = 4	# linear decreasing weights for matches in these additional plot rings

# change the minimal number of plots between unique improvements and starting plots:
UNIQUE_IMPROVEMENT_SPACING = 4
UNIQUE_IMPROVEMENT_STARTING_PLOT_SPACING = 1
DANGEROUS_UNIQUE_IMPROVEMENT_STARTING_PLOT_SPACING = 4

# higher values reduce the odds of Kelp being placed
KELP_ODDS = 85

# lower values reduce the odds of Haunted Lands being placed
HL_ODDS = 5

# higher values favour starting plots on the same continent like the wanted unique
DIFFERENT_LANDAREA_PENALTY_FACTOR = 5

# name the uniques you don't want near any starting plot:
DANGEROUS_UNIQUE_IMPROVEMENTS = ["IMPROVEMENT_GUARDIAN"]

# higher values favour starting plots on the same continent like the wanted unique
DIFFERENT_LANDAREA_PENALTY_FACTOR = 5

# the number of land plots necessary to allow the placement of a certain type of improvement, bonus ...
NUM_LAND_PLOTS_ENABLE_TOWER = 150
NUM_LAND_PLOTS_ENABLE_HOLDFAST = 50

# minimal number of plots between improvements, bonuses, ...
SPACING_STEP_TOWER = 8
SPACING_PATH_HOLDFAST = 5

# holdfast type probabliities
GIANT_STEADING_PROBABILITY = 10
CASTLE_PROBABILITY = 15
FORT_PROBABILITY = 25
GOBLIN_FORT_PROBABILITY = 35
RUINS_PROBABILITY = 15

# chance for jungle to have marsh, and chance for marsh to replace jungle
ADD_MARSH_TERRAIN = True

# adds Kelp to the map
ADD_KELP = True

# adds Haunted Lands to the map
ADD_HL = True

# chance for a forest to be removed from the starting fat cross
FOREST_LOCK_SOFTENING = 50

# yield preference: influence of additional bonus yields (improved) by tech era
BONUS_REVEAL_ERA_WEIGHTS = {
	gc.getInfoTypeForString("ERA_END"):			3/3,
	gc.getInfoTypeForString("ERA_ANCIENT"):		3/3,
	gc.getInfoTypeForString("ERA_CLASSICAL"):	2/3,
	gc.getInfoTypeForString("ERA_MEDIEVAL"):	1/3
}

## FLAVOUR INFORMATION ABOUT CIVS: (make your changes here)

def RecursiveSearch(pfilename, ppath, pexact):
		##
		##  Recursive search
		##  -- arcticnightwolf, 26-Nov-2010
		##
		## note: search is case insensitive
		##       pexact: true   -- will search only for exact matches                       ( "c:/somefolder/somefile.txt" )
		##       pexact: false  -- will search only for files ending with specified string  ( "c:/somefolder/*somefile.txt" )
		##
		if (os.path.isdir(ppath)):
				fnlength = len(pfilename)
				for subitem in os.listdir(ppath):
						if (pexact or len(subitem) >= fnlength):
								if ((pexact and subitem.lower() == pfilename.lower()) or ((not pexact) and (subitem.lower()[-fnlength:] == pfilename.lower()))):
										yield os.path.join(ppath, subitem)
						if (os.path.isdir(ppath)):
								for subsubitem in RecursiveSearch(pfilename, os.path.join(ppath, subitem), pexact):
										yield subsubitem

def GetCivFlavourData():
	civFlavourInfos = {}

	## *******************
	## Modular Flavour Start: estyles 25-Oct-2010

	# Load modules (all *FlavourInfos.xml files should be in *\Flavour\)
	folderlist = []
	folderlist.append(CvPath.assetsPath[2] + "\\Modules\\NormalModules\\")
	folderlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FirstLoad\\")
	folderlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\SecondLoad\\")
	folderlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\ThirdLoad\\")
	folderlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FourthLoad\\")

	#we can't reuse the same parser, so we'll save the flavourInfos that it generates and use them to initialize the parser each time...
	#each new module with a flavourInfos.xml file will either add to the array or overwrite an element (if a mod chooses to change the flavour start for a civ)
	basexmlPath = CvPath.assetsPath[2] + "\\XML\\Civilizations\\FlavourInfos.xml"
	if os.path.exists(basexmlPath):
		parser = FlavourParser(civFlavourInfos)
		parser.load(basexmlPath)
		civFlavourInfos = parser.civFlavourInfos
	else:
		civFlavourInfos = GetHardCodedFlavourData()

	for folderpath in folderlist:
		if os.path.exists(folderpath):
			for module in os.listdir(folderpath):
				## look in "ModDir\\Flavour" and "ModDir\\xml\Flavour"
				## arcticnightwolf's edit 26-Nov-2010
					for flavourfile in RecursiveSearch("FlavourInfos.xml", os.path.join(folderpath, module), False):
							if os.path.exists(flavourfile):
									parser = FlavourParser(civFlavourInfos)
									parser.load(flavourfile)
									civFlavourInfos = parser.civFlavourInfos
								## end of edit
				# We don't need this anymore:
				# pathToFlavourXML = folderpath + module + "\\Flavour\\FlavourInfos.xml"
				# if not os.path.exists(pathToFlavourXML):
					# pathToFlavourXML = folderpath + module +"\\xml\\Flavour\\FlavourInfos.xml"
				# if os.path.exists(pathToFlavourXML):
					# parser = FlavourParser(civFlavourInfos)
					# parser.load(pathToFlavourXML)
					# civFlavourInfos = parser.civFlavourInfos

	return civFlavourInfos


	# I put this stuff (old flavour info) in a new function, called only if we can't find the flavourInfos.xml file
def GetHardCodedFlavourData():
	civFlavourInfos = {}

	## End Modular Flavour Start

	# Fall from Heaven Civilizations:

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_AMURITES")
	pCivFlavourInfo.addPreference("BONUS_MANA", 2)
	pCivFlavourInfo.addPreference("BONUS_REAGENTS", 4)
	pCivFlavourInfo.addPreference("IMPROVEMENT_LETUM_FRIGUS", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_BALSERAPHS")
	pCivFlavourInfo.addPreference("BONUS_DYE", 1)
	pCivFlavourInfo.addPreference("BONUS_SILK", 1)
	pCivFlavourInfo.addPreference("BONUS_COTTON", 1)
	pCivFlavourInfo.addPreference("BONUS_SHEEP", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_BANNOR")
	pCivFlavourInfo.addPreference("BONUS_COPPER", 3)
	pCivFlavourInfo.addPreference("BONUS_IRON", 2)
	pCivFlavourInfo.addPreference("BONUS_MITHRIL", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_CALABIM")
	pCivFlavourInfo.addPreference("YIELD_FOOD", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_CLAN_OF_EMBERS")
	pCivFlavourInfo.addPreference("IMPROVEMENT_PYRE_OF_THE_SERAPHIC", 8)
	pCivFlavourInfo.addPreference("BONUS_COPPER", 1)
	pCivFlavourInfo.addPreference("FEATURE_JUNGLE", 2)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_DOVIELLO")
	pCivFlavourInfo.addPreference("TERRAIN_TAIGA", 4)
	pCivFlavourInfo.addPreference("FEATURE_ICE", 1)
	pCivFlavourInfo.addPreference("BONUS_BISON", 3)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_ELOHIM")
	pCivFlavourInfo.addPreference("IMPROVEMENT_AIFON_ISLE", 1)
	pCivFlavourInfo.addPreference("IMPROVEMENT_BRADELINES_WELL", 1)
	pCivFlavourInfo.addPreference("IMPROVEMENT_DRAGON_BONES", 1)
	pCivFlavourInfo.addPreference("IMPROVEMENT_LETUM_FRIGUS", 1)
	pCivFlavourInfo.addPreference("IMPROVEMENT_MIRROR_OF_HEAVEN", 4)
	pCivFlavourInfo.addPreference("IMPROVEMENT_ODIOS_PRISON", 4)
	pCivFlavourInfo.addPreference("IMPROVEMENT_POOL_OF_TEARS", 8)
	pCivFlavourInfo.addPreference("IMPROVEMENT_PYRE_OF_THE_SERAPHIC", 1)
	pCivFlavourInfo.addPreference("IMPROVEMENT_REMNANTS_OF_PATRIA", 4)
	pCivFlavourInfo.addPreference("IMPROVEMENT_SEVEN_PINES", 1)
	pCivFlavourInfo.addPreference("IMPROVEMENT_SIRONAS_BEACON", 8)
	pCivFlavourInfo.addPreference("IMPROVEMENT_STANDING_STONES", 1)
	pCivFlavourInfo.addPreference("IMPROVEMENT_TOMB_OF_SUCELLUS", 1)
	pCivFlavourInfo.addPreference("IMPROVEMENT_YGGDRASIL", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_GRIGORI")
	pCivFlavourInfo.addPreference("ISOLATION", 2)
	pCivFlavourInfo.addPreference("IMPROVEMENT_SEVEN_PINES", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_HIPPUS")
	pCivFlavourInfo.addPreference("MOBILITY", 5)
	pCivFlavourInfo.addPreference("BONUS_HORSE", 1)
	pCivFlavourInfo.addPreference("TERRAIN_OCEAN", -2)
	pCivFlavourInfo.addPreference("TERRAIN_TUNDRA", -2)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_ILLIANS")
	pCivFlavourInfo.addPreference("IMPROVEMENT_LETUM_FRIGUS", 12)
	pCivFlavourInfo.addPreference("TERRAIN_TAIGA", 1)
	pCivFlavourInfo.addPreference("TERRAIN_TUNDRA", 4)
	pCivFlavourInfo.addPreference("FEATURE_ICE", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_KHAZAD")
	pCivFlavourInfo.addPreference("PLOT_PEAK", 8)
	pCivFlavourInfo.addPreference("PLOT_HILLS", 4)
	pCivFlavourInfo.addPreference("YIELD_COMMERCE", 2)
	pCivFlavourInfo.addPreference("BONUS_GOLD", 1)
	pCivFlavourInfo.addPreference("BONUS_PIG", 1)
	pCivFlavourInfo.addPreference("BONUS_MUSHROOMS", 1)
	pCivFlavourInfo.addPreference("TERRAIN_COAST", -1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_KURIOTATES")
	pCivFlavourInfo.addPreference("YIELD_FOOD", 2)
	pCivFlavourInfo.addPreference("YIELD_PRODUCTION", 2)
	pCivFlavourInfo.addPreference("YIELD_COMMERCE", 2)
	pCivFlavourInfo.addPreference("PLOT_OCEAN", -2)
	pCivFlavourInfo.changeSearchAreaSize(+1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_LANUN")
	pCivFlavourInfo.addPreference("TERRAIN_COAST", 1)
	pCivFlavourInfo.addPreference("FEATURE_KELP", 2)
	pCivFlavourInfo.addPreference("BONUS_PEARL", 2)
	pCivFlavourInfo.addPreference("COASTAL_START", 2)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_LJOSALFAR")
	pCivFlavourInfo.addPreference("FEATURE_FOREST", 2)
	pCivFlavourInfo.addPreference("TERRAIN_TAIGA", -1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_LUCHUIRP")
	pCivFlavourInfo.addPreference("PLOT_HILLS", 5)
	pCivFlavourInfo.addPreference("YIELD_PRODUCTION", 2)
	pCivFlavourInfo.addPreference("BONUS_MARBLE", 1)
	pCivFlavourInfo.addPreference("BONUS_IVORY", 1)
	pCivFlavourInfo.addPreference("BONUS_PIG", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_MALAKIM")
	pCivFlavourInfo.addPreference("TERRAIN_DESERT", 5)
	pCivFlavourInfo.addPreference("BONUS_INCENSE", 1)
	pCivFlavourInfo.addPreference("IMPROVEMENT_MIRROR_OF_HEAVEN", 1)
	pCivFlavourInfo.addPreference("BONUS_CAMEL", 3)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_SHEAIM")
	pCivFlavourInfo.addPreference("BONUS_MANA", 1)
	pCivFlavourInfo.addPreference("BONUS_REAGENTS", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_SIDAR")
	pCivFlavourInfo.addPreference("ISOLATION", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_SVARTALFAR")
	pCivFlavourInfo.addPreference("FEATURE_FOREST", 2)
	pCivFlavourInfo.addPreference("BONUS_MANA", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	# Fall Further Civilizations:

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_AUSTRIN")
	pCivFlavourInfo.addPreference("FEATURE_JUNGLE", -1)
	pCivFlavourInfo.addPreference("FEATURE_FOREST", -1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_ARCHOS")
	pCivFlavourInfo.addPreference("PLOT_HILLS", 1)
	pCivFlavourInfo.addPreference("YIELD_FOOD", 2)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_DURAL")
	pCivFlavourInfo.addPreference("BONUS_MARBLE", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_CHISLEV")
	pCivFlavourInfo.addPreference("TERRAIN_PLAINS", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_CUALLI")
	pCivFlavourInfo.addPreference("FEATURE_JUNGLE", 4)
	pCivFlavourInfo.addPreference("FEATURE_FOREST", 1)
	pCivFlavourInfo.addPreference("TERRAIN_GRASS", 1)
	pCivFlavourInfo.addPreference("RIVERSIDE", 2)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_MAZATL")
	pCivFlavourInfo.addPreference("IMPROVEMENT_MOUNT_KALSHEKK", 8)
	pCivFlavourInfo.addPreference("FEATURE_JUNGLE", 4)
	pCivFlavourInfo.addPreference("FEATURE_FOREST", 1)
	pCivFlavourInfo.addPreference("TERRAIN_GRASS", 1)
	pCivFlavourInfo.addPreference("RIVERSIDE", 2)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	#pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_JOTNAR")
	#pCivFlavourInfo.addPreference("COASTAL_START", 2)
	#pCivFlavourInfo.addPreference("IMPROVEMENT_YGGDRASIL", 8)
	#pCivFlavourInfo.addPreference("TERRAIN_TAIGA", 4)
	#pCivFlavourInfo.changeSearchAreaSize(-1)
	#civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_DTESH")
	pCivFlavourInfo.addPreference("TERRAIN_DESERT", 3)
	pCivFlavourInfo.addPreference("PLOT_PEAK", -2)
	pCivFlavourInfo.addPreference("YIELD_COMMERCE", 2)
	pCivFlavourInfo.addPreference("YIELD_PRODUCTION", 2)
	pCivFlavourInfo.addPreference("PLOT_OCEAN", -2)
	pCivFlavourInfo.addPreference("YIELD_FOOD", -2)
	pCivFlavourInfo.changeSearchAreaSize(+1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_MECHANOS")
	pCivFlavourInfo.addPreference("PLOT_HILLS", 4)
	pCivFlavourInfo.addPreference("YIELD_PRODUCTION", 4)
	pCivFlavourInfo.addPreference("BONUS_MANA", 1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	pCivFlavourInfo = CivFlavourInfo("CIVILIZATION_SCIONS")
	pCivFlavourInfo.addPreference("PLOT_HILLS", 2)
	pCivFlavourInfo.addPreference("BONUS_PATRIAN_ARTIFACTS", 4)
	pCivFlavourInfo.addPreference("TERRAIN_DESERT", 2)
	pCivFlavourInfo.addPreference("IMPROVEMENT_REMNANTS_OF_PATRIA", 4)
	pCivFlavourInfo.addPreference("YIELD_FOOD", -2)
	pCivFlavourInfo.changeSearchAreaSize(+1)
	civFlavourInfos[pCivFlavourInfo.civ] = pCivFlavourInfo

	return civFlavourInfos


## ENTRYPOINT FROM THE SDK

def generateFlavour():

	debugOut("FlavourMod enabled and running.")

	limitFlavor = False
	if not ('.CivBeyondSwordWBSave' in CyMap().getMapScriptName()):
		if (('ErebusContinent' or 'WorldOfErebus') in CyMap().getMapScriptName()):
			limitFlavor = True

	pFlavourGenerator = FlavourGenerator()

	if ADD_MARSH_TERRAIN and not limitFlavor:
		if not IsMapHasTerrainType("TERRAIN_MARSH"):
			pFlavourGenerator.addMarshTerrain()

	if ADD_HL and not limitFlavor:
		if not IsMapHasPlotEffectType("PLOT_EFFECT_HAUNTED_LANDS"):
			pFlavourGenerator.addHL()

	if ADD_KELP and not limitFlavor:
		pFlavourGenerator.addKelp()

	if ASSIGN_FLAVOURFUL_HOLDFAST_LOCATIONS:
		pFlavourGenerator.assignFlavourfulHoldfastLocations()

	if ASSIGN_FLAVOURFUL_UNIQUE_IMPROVEMENT_LOCATIONS:
		pFlavourGenerator.assignFlavourfulUniqueImprovementLocations()

	if ASSIGN_FLAVOURFUL_STARTING_LOCATIONS and not limitFlavor:
		pFlavourGenerator.assignFlavourfulStartingLocations()

	if FLAVOURFUL_NORMALIZATION:
		pFlavourGenerator.normalizeJungleStarts()
		pFlavourGenerator.normalizeForestLocks()
		pFlavourGenerator.normalizeAddFoodBonuses()

	del pFlavourGenerator

	return None

def onClimateChange(argsList):
	'plot climate just changed'
	pPlot = CyMap().plot(argsList[0], argsList[1])
	eClimateOld = argsList[2]
	eClimateNew = argsList[3]
	eTerrain = pPlot.getTerrainType()
	# CvPlot::setClimate has ALREADY switched the terrain before calling us, and
	# CvPlot::setTerrainType strips any feature that is not valid on the new
	# terrain - a Forest cannot stand on Desert. Reading pPlot.getFeatureType()
	# here therefore returns NO_FEATURE for exactly the transitions this hook is
	# meant to handle, which silently destroyed the feature instead of converting
	# it. The DLL now passes in the feature the plot held before the change.
	eFeature = argsList[4]
	iVariety = argsList[5]
	eImprovement = pPlot.getImprovementType()

	iOasis = GetInfoType('FEATURE_OASIS')
	iScrub = GetInfoType("FEATURE_SCRUB")
	iFloodPlains = GetInfoType("FEATURE_FLOOD_PLAINS")
	iCrystalPlains = GetInfoType("FEATURE_CRYSTAL_PLAINS")
	iHauntedLands = GetInfoType("PLOT_EFFECT_HAUNTED_LANDS")
	iForest = GetInfoType("FEATURE_FOREST")
	iAncientForest = GetInfoType("FEATURE_FOREST_ANCIENT")
	iBurntForest = GetInfoType("FEATURE_FOREST_BURNT")
	iNewForest = GetInfoType("FEATURE_FOREST_NEW")
	iBlightedForest = GetInfoType("IMPROVEMENT_BLIGHTED_FOREST")

	sTrees = ['FOREST', 'FOREST_NEW', 'JUNGLE', "SCRUB"]
	iTrees = [GetInfoType('FEATURE_' + sFeature) for sFeature in sTrees]

	# Each conversion below clears the plot before planting the replacement:
	# canHaveFeature() reports False while any feature is still present, and it
	# is what keeps us from planting a feature the new terrain cannot hold (for
	# instance Forest on the Tundra of a Frost zone). A plot whose replacement is
	# invalid is simply left bare, which is what happened before this fix.

	# Was Arid: Remove Flood Plains and transform Scrubs to New Forests
	if eClimateOld == GetInfoType("CLIMATEZONE_ARID"):
		if eFeature == iFloodPlains:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
		if eFeature == iScrub:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
			if pPlot.canHaveFeature(iNewForest):
				pPlot.setFeatureType(iNewForest, VarietyTypes.NO_VARIETY)

	# Was Glacial: Remove Crystal Plains
	elif eClimateOld == GetInfoType("CLIMATEZONE_GLACIAL"):
		if eFeature == iCrystalPlains:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)

	# Was Wasteland: Remove HL, Blighted Forest
	elif eClimateOld == GetInfoType("CLIMATEZONE_WASTELAND"):
		if eImprovement == iBlightedForest:
			pPlot.setImprovementType(ImprovementTypes.NO_IMPROVEMENT)

	# Became Frost: Make Forest Boreal
	if eClimateNew == GetInfoType("CLIMATEZONE_FROST"):
		if eFeature in iTrees:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
			if pPlot.canHaveFeature(iForest):
				pPlot.setFeatureType(iForest, VarietyTypes.BOREAL_FOREST)

	# Became Glacial: Make Forest Boreal
	elif eClimateNew == GetInfoType("CLIMATEZONE_GLACIAL"):
		if eFeature in iTrees:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
			if pPlot.canHaveFeature(iForest):
				pPlot.setFeatureType(iForest, VarietyTypes.BOREAL_FOREST)
		if pPlot.canHaveFeature(iCrystalPlains):
			pPlot.setFeatureType(iCrystalPlains, VarietyTypes.NO_VARIETY)

	# Became Boreal: Make Forest Boreal
	elif eClimateNew == GetInfoType("CLIMATEZONE_BOREAL"):
		if eFeature in iTrees:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
			if pPlot.canHaveFeature(iForest):
				pPlot.setFeatureType(iForest, VarietyTypes.BOREAL_FOREST)

	# Became Temperate:
	elif eClimateNew == GetInfoType("CLIMATEZONE_TEMPERATE"):
		if eFeature in iTrees:
			if eFeature != iNewForest:
				pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
				if pPlot.canHaveFeature(iForest):
					pPlot.setFeatureType(iForest, VarietyTypes.NO_VARIETY)

	# Became Semiarid:
	elif eClimateNew == GetInfoType("CLIMATEZONE_SEMIARID"):
		if eFeature in iTrees:
			if eFeature != iNewForest:
				pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
				if pPlot.canHaveFeature(iForest):
					pPlot.setFeatureType(iForest, VarietyTypes.NO_VARIETY)

	# Became Arid: Add Scrubs, Flood Plains and the occasional Oasis
	elif eClimateNew == GetInfoType("CLIMATEZONE_ARID"):
		if eFeature in iTrees:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
			if not pPlot.isRiver():
				if pPlot.canHaveFeature(iScrub):
					pPlot.setFeatureType(iScrub, VarietyTypes.NO_VARIETY)
		if pPlot.canHaveFeature(iFloodPlains):
			pPlot.setFeatureType(iFloodPlains, VarietyTypes.NO_VARIETY)
		if pPlot.canHaveFeature(iOasis):
			if CyGame().getSorenRandNum(10000, "onClimateChange") < gc.getFeatureInfo(iOasis).getAppearanceProbability():
				pPlot.setFeatureType(iOasis, VarietyTypes.NO_VARIETY)

	# Becomes Wasteland -> Add Haunted lands on forests, remove oasis and rivers
	elif eClimateNew == GetInfoType("CLIMATEZONE_WASTELAND"):
		if eFeature in iTrees:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
			pPlot.setPlotEffectType(iHauntedLands)
		if eFeature == iBurntForest:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
			pPlot.setPlotEffectType(iHauntedLands)
		if eFeature == iAncientForest:
			# Only blight a forest that is actually still standing.
			# IMPROVEMENT_BLIGHTED_FOREST is bPermanent + bRequiresFeature and lists
			# no FeatureMakesValid, so once it is placed CvPlot::setFeatureType
			# refuses every later feature change on the plot. Placing it on a tile
			# whose forest the terrain switch already removed would wedge that tile
			# with a permanent improvement and no feature.
			if pPlot.getFeatureType() == iAncientForest:
				pPlot.setImprovementType(iBlightedForest)
		if eFeature == iOasis:
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, VarietyTypes.NO_VARIETY)
		# Rather than remove rivers, wasteland gains no benefit from river adjacency.
		# if pPlot.isRiver():
		# 	pPlot.setWOfRiver(False,CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
		# 	pPlot.setNOfRiver(False,CardinalDirectionTypes.CARDINALDIRECTION_EAST)
		# 	pPlot.setWOfRiver(False,CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		# 	pPlot.setNOfRiver(False,CardinalDirectionTypes.CARDINALDIRECTION_WEST)

## FLAVOUR CLASSES:

## *******************
## Modular Flavour Start: estyles 25-Oct-2010

class FlavourParser(XMLParser):
	Error = xmllibError

	def __init__(self, civFlavourInfos):
		XMLParser.__init__(self)
		self.reset_data()
		self.civFlavourInfos = civFlavourInfos

	def load(self, filename):
		file = open(filename)
		for line in file:
			self.feed(line)
		file.close()

	def unknown_starttag(self, tag, attrs):
		tag = tag.upper()
		if tag in ( "CIVFLAVOURINFO", "CIVILIZATION", "PREFERENCE", "FLAVOURTYPE", "VALUE", "ISEARCHAREAMODIFIER" ):
			self.tag = tag
			if tag == "CIVFLAVOURINFO" :
				self.reset_data()
			elif tag == "PREFERENCE" :
				self.flavourType = None
				self.value = 0

	def handle_data(self, data):
		if self.tag:
			self.data += data.strip()

	def unknown_endtag(self, tag):
		tag = tag.upper()
		if tag == "CIVILIZATION" :
			if gc.getInfoTypeForString(self.data) != -1:
				self.civFlavourInfo = CivFlavourInfo(self.data)
				print "MODULAR FLAVOR: Civilization is %s" % (self.data)
		elif tag == "PREFERENCE" :
			if self.civFlavourInfo:
				if self.flavourType:
					if self.value:
						self.civFlavourInfo.addPreference(self.flavourType, self.value)
		elif tag == "FLAVOURTYPE" :
			self.flavourType = self.data
		elif tag == "VALUE":
			self.value = int(self.data) ## Modified by Opera
		elif tag == "ISEARCHAREAMODIFIER":
			if self.civFlavourInfo:
				self.civFlavourInfo.changeSearchAreaSize(int(self.data)) ## Modified by Opera
		elif tag == "CIVFLAVOURINFO" :
			if self.civFlavourInfo:
				self.civFlavourInfos[self.civFlavourInfo.civ] = self.civFlavourInfo
			self.reset_data()
		else:
			pass
		self.data = self.tag = ""

#	def syntax_error(self, message):
#		raise Error('Syntax error at line %d: %s' % (self.lineno, message))

	def reset_data(self):
		self.data = self.tag = ""
		self.civFlavourInfo = None
		self.flavourType = None
		self.value = 0

## End Modular Flavour Start


class FlavourGenerator:

	pStartingPlotList = []
	pUniqueImprovementList = []
	pFlavourPlotList = []
	MAX_PATH_DISTANCE = 0

	def __init__(self):
		self.pCivFlavourInfos = {} # Key: iPlayer
		self.__initCivFlavourInfos()
		FlavourGenerator.pStartingPlotList = []
		self.__initStartingPlotList()
		FlavourGenerator.pUniqueImprovementList = []
		self.__initUniqueImprovementList()
		FlavourGenerator.pFlavourPlotList = []
		self.__initFlavourPlotList()
		self.__calculateMaxPathDistance()

	def __initCivFlavourInfos(self):
		pCivFlavourData = GetCivFlavourData()
		iPlayerCount = gc.getGame().countCivPlayersEverAlive()
		for iPlayer in range(iPlayerCount):
			pPlayer = gc.getPlayer(iPlayer)
			eCivType = pPlayer.getCivilizationType()
			if eCivType in pCivFlavourData.keys():
				self.pCivFlavourInfos[iPlayer] = pCivFlavourData[eCivType]

	def __initStartingPlotList(self):
		iPlayerCount = gc.getGame().countCivPlayersEverAlive()
		for iPlayer in range(iPlayerCount):
			pPlayer = gc.getPlayer(iPlayer)
			FlavourGenerator.pStartingPlotList.append(pPlayer.getStartingPlot())

	def __initUniqueImprovementList(self):
		for iPlotIndex in range(cymap.numPlots()):
			pPlot = cymap.plotByIndex(iPlotIndex)
			pImprovement = gc.getImprovementInfo(pPlot.getImprovementType())
			if pImprovement != None and pImprovement.isUnique():
				pUniqueImprovement = UniqueImprovement(pPlot)
				FlavourGenerator.pUniqueImprovementList.append(pUniqueImprovement)

	def __initFlavourPlotList(self):
		NO_REGION_ID = -1
		FIRST_REGION_ID = 0
		for iPlotIndex in range(cymap.numPlots()):
			pPlot = cymap.plotByIndex(iPlotIndex)
			if FlavourPlot.isPotentialFlavourPlot(pPlot):
				iRegionMap = []
				iRegionId = FIRST_REGION_ID
				iImpassableLength = 0
				for iDirection in range(DirectionTypes.NUM_DIRECTION_TYPES):
					pAdjacentPlot = plotDirection(pPlot.getX(), pPlot.getY(), DirectionTypes(iDirection))
					if IsPassableLandPlot(pAdjacentPlot): # if plot passable
						if FIRST_REGION_ID in iRegionMap:
							if iImpassableLength > 1:
								iRegionId += 1
							elif iImpassableLength == 1:
								if IsCardinalDirection(iDirection-1):
									iRegionId += 1
						iRegionMap.append(iRegionId)
						iImpassableLength = 0
					else: # plot impassable:
						iRegionMap.append(NO_REGION_ID)
						iImpassableLength += 1
				if iRegionMap[DirectionTypes.DIRECTION_NORTH] != NO_REGION_ID: # if north passable ...
					iLastRegionId = max(iRegionMap[-2:])
					if iLastRegionId > FIRST_REGION_ID: # ... and west or north west too ...
						for i, item in enumerate(iRegionMap):
							if item == FIRST_REGION_ID:
								iRegionMap[i] = iLastRegionId-1 # ... merge fist with last region.
							elif item != NO_REGION_ID:
								iRegionMap[i] -= 1
				FlavourGenerator.pFlavourPlotList.append(FlavourPlot(pPlot, iRegionMap))

	def __runLinearOptimization(self, fCostMatrix):
		munkres = Munkres()
		optimum = munkres.compute(fCostMatrix)
		iTotalCosts = 0.0
		for i, j in optimum: iTotalCosts += fCostMatrix[i][j]
		debugOut('Total Cost: %f' % iTotalCosts)
		return optimum

	def __getCostMatrix(self, fProfitMatrix):
		return make_cost_matrix(fProfitMatrix, lambda x : 1.0 - x)

	def __getCivProfitMatrix(self):
		iNumPlayers = gc.getGame().countCivPlayersEverAlive()
		iNumStartingPlots = len(FlavourGenerator.pStartingPlotList)
		fProfitMatrix = []
		for iPlayer in range(iNumPlayers):
			if iPlayer in self.pCivFlavourInfos.keys():
				iTeam = TeamTypes(gc.getPlayer(iPlayer).getTeam())
				fProfitMatrix.append(self.pCivFlavourInfos[iPlayer].evaluateStartingPlots(iTeam))
			else: fProfitMatrix.append([0.0] * iNumStartingPlots)
		return fProfitMatrix

	def __calculateMaxPathDistance(self):
		FlavourGenerator.MAX_PATH_DISTANCE = GetMaxPathDistanceFast()
		debugOut("MAX_PATH_DISTANCE: %d" % FlavourGenerator.MAX_PATH_DISTANCE)

	def addMarshTerrain(self):

		def isValid(pPlot):
			if not pPlot.isFlatlands():
				return False
			if pPlot.getTerrainType() not in [GetInfoType("TERRAIN_GRASS"), GetInfoType("TERRAIN_PLAINS")]:
				return False
			return True

		def isDelta(pPlot):
			iNumDirections = DirectionTypes.NUM_DIRECTION_TYPES
			if pPlot.isRiver() and pPlot.isCoastalLand():
				for i in range(iNumDirections):
					if pPlot.isRiverCrossing(DirectionTypes(i)):
						for j in [(i-1)%iNumDirections, (i+1)%iNumDirections]:
							pAdjacentPlot = plotDirection(pPlot.getX(), pPlot.getY(), DirectionTypes(j))
							if not pAdjacentPlot.isNone():
								if pAdjacentPlot.isWater():
									return True
			return False

		def getChance(pPlot):
			iChance = 0
			if pPlot.getTerrainType() == GetInfoType("TERRAIN_GRASS"):
				iChance += 5
			if pPlot.isFreshWater():
				iChance += 10
				if pPlot.isRiver():
					iChance += pPlot.getRiverCrossingCount() * 5
					if isDelta(pPlot):
						iChance += 20
			if pPlot.getFeatureType() == GetInfoType("FEATURE_JUNGLE"):
				iChance += 10
			if pPlot.getBonusType(BonusTypes.NO_BONUS) == GetInfoType("BONUS_RICE"):
				iChance += 20
			return iChance

		for iPlotIndex in range(cymap.numPlots()):
			pPlot = cymap.plotByIndex(iPlotIndex)
			if isValid(pPlot):
				if dice.get(100, "FlavourMod: Add Marsh") < getChance(pPlot):
					pPlot.setTerrainType(GetInfoType("TERRAIN_MARSH"), False, False)
					if dice.get(100, "FlavourMod: Remove Marsh Vegetation") < 66:
						pPlot.setFeatureType(FeatureTypes.NO_FEATURE, 0)
		cymap.rebuildGraphics()

	def addKelp(self):

		def isValidK(pPlot):
			sValidTerrains = ['COAST']
			iValidTerrains = [gc.getInfoTypeForString('TERRAIN_' + sTerrain) for sTerrain in sValidTerrains]
			if not (pPlot.getTerrainType() in iValidTerrains):
				return False
			if pPlot.getFeatureType() != -1:
				return False
			return True

		def getChanceK(pPlot):
			iChance = 1
			iX = pPlot.getX()
			iY = pPlot.getY()
			for iiX in range(iX-2, iX+3, 1):
				for iiY in range(iY-2, iY+3, 1):
					pPlot = CyMap().plot(iiX,iiY)
					if not pPlot.isNone():
						iFeature = pPlot.getFeatureType()
						if iFeature == GetInfoType("FEATURE_KELP"):
							iChance = iChance + 1
			return iChance

		for iPlotIndex in range(cymap.numPlots()):
			pPlot = cymap.plotByIndex(iPlotIndex)
			if isValidK(pPlot):
				for i in range(getChanceK(pPlot)):
					if dice.get(100, "FlavourMod: Add Kelp") >= (KELP_ODDS - getChanceK(pPlot)):
						pPlot.setFeatureType(GetInfoType("FEATURE_KELP"),0)
		cymap.rebuildGraphics()

	def addHL(self):

		def isValidHL(pPlot):
			if pPlot.isPeak() or pPlot.isWater():
				return False
			if pPlot.getFeatureType() != -1:
				return False
			return True

		for iPlotIndex in range(cymap.numPlots()):
			pPlot = cymap.plotByIndex(iPlotIndex)
			if isValidHL(pPlot):
				if dice.get(100, "FlavourMod: Add HL") <= HL_ODDS:
					pPlot.setPlotEffectType(GetInfoType("PLOT_EFFECT_HAUNTED_LANDS"))
		cymap.rebuildGraphics()

	def assignFlavourfulUniqueImprovementLocations(self):
		debugOut("Uniques in the World: %d" % len(FlavourGenerator.pUniqueImprovementList))
		for pUniqueImprovement in FlavourGenerator.pUniqueImprovementList:
			if not RELOCATE_DANGEROUSLY_CLOSE_UNIQUE_IMPROVEMENTS_ONLY:
				pUniqueImprovement.unassign()
			else:
				if pUniqueImprovement.isDangerouslyClose():
					pUniqueImprovement.unassign()
		for pUniqueImprovement in FlavourGenerator.pUniqueImprovementList:
			if pUniqueImprovement.isUnassigned():
				pUniqueImprovement.assignFlavourfulLocation()
		FlavourGenerator.pUniqueImprovementList = [pUI for pUI in FlavourGenerator.pUniqueImprovementList if pUI.isAssigned()]
		debugOut("Uniques in the World after Reassignment: %d" % len(FlavourGenerator.pUniqueImprovementList))

	def assignFlavourfulStartingLocations(self):
		sCivNames = GetCivNameList()
		fProfitMatrix = self.__getCivProfitMatrix()
		debugOut(FormatMatrix(fProfitMatrix, "Profit Matrix:", sCivNames))
		fCostMatrix = self.__getCostMatrix(fProfitMatrix)
		debugOut(FormatMatrix(fCostMatrix, "Cost Matrix:", sCivNames))
		optimum = self.__runLinearOptimization(fCostMatrix)
		pStartingPlots = FlavourGenerator.pStartingPlotList
		for iPlayer, iStartingPlot in optimum:
			gc.getPlayer(iPlayer).setStartingPlot(pStartingPlots[iStartingPlot], True)
			debugOut("(%d, %d) %s -> %f (%s, %s)" % (iPlayer, iStartingPlot, sCivNames[iPlayer], fCostMatrix[iPlayer][iStartingPlot], \
				pStartingPlots[iStartingPlot].getX(), pStartingPlots[iStartingPlot].getY()))
			# send a little message to the interface event log about the sweetness of the starting plot
			if iPlayer in self.pCivFlavourInfos and self.pCivFlavourInfos[iPlayer].getNumPreferences > 0:
				sChoice = sorted(set(fCostMatrix[iPlayer])).index(fCostMatrix[iPlayer][iStartingPlot])+1
				sPercentage = "%.0f" % (100 * (1 - fCostMatrix[iPlayer][iStartingPlot]))
				message = CyTranslator().getText("TXT_KEY_MESSAGE_FLAVOUR_START_VALUE",(ordinal(sChoice), sPercentage,))
			else:
				message = CyTranslator().getText("TXT_KEY_MESSAGE_NO_FLAVOUR",())
			SendSimpleMessage(message, iPlayer)

	def assignFlavourfulHoldfastLocations(self):

		iTowerCount = 0
		# remove the current holdfasts/towers:
		for iPlotIndex in range(cymap.numPlots()):
			pPlot = cymap.plotByIndex(iPlotIndex)
			eImprovement = pPlot.getImprovementType()
			if eImprovement == GetInfoType("IMPROVEMENT_TOWER") \
			or eImprovement == GetInfoType("IMPROVEMENT_MARNOK_HILLGIANT_STEADING"):
				pPlot.setImprovementType(ImprovementTypes.NO_IMPROVEMENT)
				iTowerCount += 1
		debugOut("Removed Towers and Giant Steadings: %d" % iTowerCount)

		# decide how many new towers and holdfasts should be placed  on the map:
		iHoldfastsLeft = int(cymap.getLandPlots() / NUM_LAND_PLOTS_ENABLE_HOLDFAST)
		iTowersLeft = int(cymap.getLandPlots() / NUM_LAND_PLOTS_ENABLE_TOWER)
		debugOut("Land Plots: %d" % cymap.getLandPlots())
		debugOut("Max allowed Holdfasts: %d" % iHoldfastsLeft)
		debugOut("Max allowed Towers: %d" % iTowersLeft)

		pChokePointList = []
		# make a list of suitable choke points for holdfasts:
		for pFlavourPlot in FlavourGenerator.pFlavourPlotList:
			if pFlavourPlot.isChokePoint():
				if not pFlavourPlot.isPeak():
					if (pFlavourPlot.getNumDistinctRegions() > 1 \
						and min(pFlavourPlot.getIsolatedRegionSizes()) > 12) \
					or (pFlavourPlot.getNumDistinctRegions() == 1 \
						and pFlavourPlot.getDistanceRoundtrip() > 16):
						pChokePointList.append(pFlavourPlot)

		pHoldfastPlotList = []
		# put an appropriate number of holdfasts on the map:
		while iHoldfastsLeft > 0 and len(pChokePointList) > 0:
			bEnoughDistance = True
			# Get a random choke point and remove it from the choke points list.
			iRandomChokePoint = dice.get(len(pChokePointList), "FlavourMod: Holdfast")
			pRandomChokePoint = pChokePointList.pop(iRandomChokePoint)
			# Is there enough distance between this chokepoint and all existing holdfasts?
			for pHoldfastPlot in pHoldfastPlotList:
				iDistance = cymap.calculatePathDistance(pHoldfastPlot.getPlot(), pRandomChokePoint.getPlot())
				if iDistance <= SPACING_PATH_HOLDFAST and iDistance != -1:
					bEnoughDistance = False
					break
			if bEnoughDistance: # if 'yes' ...
				# ... decide holdfast type ...
				iTotal = GIANT_STEADING_PROBABILITY + CASTLE_PROBABILITY + FORT_PROBABILITY + RUINS_PROBABILITY
				iHoldfastType = dice.get(iTotal, "FlavourMod: Holdfast") + 1
				if iHoldfastType <= GIANT_STEADING_PROBABILITY:
					pRandomChokePoint.setImprovementType(GetInfoType("IMPROVEMENT_MARNOK_HILLGIANT_STEADING"))
				elif iHoldfastType <= GIANT_STEADING_PROBABILITY + CASTLE_PROBABILITY:
					pRandomChokePoint.setImprovementType(GetInfoType("IMPROVEMENT_CASTLE"))
				elif iHoldfastType <= GIANT_STEADING_PROBABILITY + CASTLE_PROBABILITY + FORT_PROBABILITY:
					pRandomChokePoint.setImprovementType(GetInfoType("IMPROVEMENT_FORT"))
				elif iHoldfastType <= GIANT_STEADING_PROBABILITY + CASTLE_PROBABILITY + FORT_PROBABILITY + GOBLIN_FORT_PROBABILITY:
					pRandomChokePoint.setImprovementType(GetInfoType("IMPROVEMENT_GOBLIN_CAMP"))
				else:
					pRandomChokePoint.setImprovementType(GetInfoType("IMPROVEMENT_CITY_RUINS"))
				# ... add the new holdfast plot to the holdfasts list ...
				pHoldfastPlotList.append(pRandomChokePoint)
				# ... and remove it from the availabe flavour plots list.
				FlavourGenerator.pFlavourPlotList.remove(pRandomChokePoint)

		debugOut("Holdfasts placed: %d" % len(pHoldfastPlotList))

		pTowerPlotList = []
		iVantagePointList = []
		# put an appropriate number of surveillance towers at vantage points on the map:
		for iFlavourPlotIndex, pFlavourPlot in enumerate(FlavourGenerator.pFlavourPlotList):
			if pFlavourPlot.isVantagePoint():
				iVantagePointList.append(iFlavourPlotIndex)
		while iTowersLeft > 0 and len(iVantagePointList) > 0:
			iRandomVantagePoint = iVantagePointList.pop(dice.get(len(iVantagePointList), "FlavourMod: Tower"))
			pRandomVantagePoint = FlavourGenerator.pFlavourPlotList[iRandomVantagePoint]
			pRandomVantagePoint.setImprovementType(GetInfoType("IMPROVEMENT_TOWER"))
			pTowerPlotList.append(pRandomVantagePoint)
			iNewVantagePointList = []
			for iVantagePoint in iVantagePointList:
				pVantagePoint = FlavourGenerator.pFlavourPlotList[iVantagePoint]
				if GetStepDistance(pRandomVantagePoint.getPlot(), pVantagePoint.getPlot()) > SPACING_STEP_TOWER:
					iNewVantagePointList.append(iVantagePoint)
			iVantagePointList = iNewVantagePointList
			iTowersLeft -= 1
		for pTowerPlot in pTowerPlotList:
			FlavourGenerator.pFlavourPlotList.remove(pTowerPlot)

		debugOut("Towers placed: %d" % len(pTowerPlotList))

	def normalizeAddFoodBonuses(self):

		iFoodYields = []
		pStartingPlots = []
		pPlayers = []

		iNumPlayers = gc.getGame().countCivPlayersEverAlive()
		for iPlayer in range(iNumPlayers):
			iFoodYield = 0
			pPlayer = gc.getPlayer(iPlayer)
			pStartingPlot = pPlayer.getStartingPlot()
			if not pStartingPlot.isNone():
				pSearchArea = SearchArea(FatCrossArea(2))
				for pPlot in pSearchArea.getRealPlots(pStartingPlot):
					if (pPlot.getX(), pPlot.getY()) != (pStartingPlot.getX(), pStartingPlot.getY()):
						iFoodYield += pPlot.calculateNatureYield(YieldTypes.YIELD_FOOD, PlayerTypes(iPlayer), False)
						if pPlot.getBonusType(-1) != BonusTypes.NO_BONUS:
							eBonus = pPlot.getBonusType(-1)
							iFoodYieldChanges = []
							for iImprovement in range(gc.getNumImprovementInfos()):
								pImprovement = gc.getImprovementInfo(iImprovement)
								if pImprovement.isImprovementBonusMakesValid(eBonus):
									iFoodYieldChange = pImprovement.getImprovementBonusYield(eBonus, YieldTypes.YIELD_FOOD)
									iFoodYieldChanges.append(iFoodYieldChange)
							if len(iFoodYieldChanges) > 0:
								iFoodYield += max(iFoodYieldChanges)
				iFoodYields.append(iFoodYield)
				pStartingPlots.append(pStartingPlot)
				pPlayers.append(pPlayer)
				print "Player: %s Food: %d" % (pPlayer.getName(), iFoodYield)

		iMeanFoodYield = int(sum(iFoodYields) / len(iFoodYields))
		print "Mittelwert: %d" % iMeanFoodYield

		for iFoodYield, pStartingPlot, pPlayer in zip(iFoodYields, pStartingPlots, pPlayers):
			if iFoodYield < iMeanFoodYield:
				pSearchArea = SearchArea(FatCrossArea(2))
				pCityPlots = pSearchArea.getRealPlots(pStartingPlot)
				while len(pCityPlots) > 0 and iFoodYield < iMeanFoodYield:
					pPlot = pCityPlots.pop(dice.get(len(pCityPlots), "FlavourMod"))
					if (pPlot.getX(), pPlot.getY()) != (pStartingPlot.getX(), pStartingPlot.getY()):
						if pPlot.getBonusType(TeamTypes.NO_TEAM) == BonusTypes.NO_BONUS:
							if not pPlot.isGoody():
								iValidBonuses = []
								for iBonus in range(gc.getNumBonusInfos()):
									if pPlot.canHaveBonus(BonusTypes(iBonus), False):
										if cymap.getArea(pPlot.getArea()).getNumBonuses(BonusTypes(iBonus)) > 0:
											pBonus = gc.getBonusInfo(iBonus)
											if pBonus.getYieldChange(YieldTypes.YIELD_FOOD) > 0:
												iValidBonuses.append(iBonus)
								if len(iValidBonuses) > 0:
									iBonus = iValidBonuses[dice.get(len(iValidBonuses), "FlavourMod")]
									iFoodYield += gc.getBonusInfo(iBonus).getYieldChange(YieldTypes.YIELD_FOOD)
									iBestImprovementYieldChange = 0
									for iImprovement in range(gc.getNumImprovementInfos()):
										pImprovement = gc.getImprovementInfo(iImprovement)
										if pImprovement.isImprovementBonusMakesValid(iBonus):
											iImprovementYieldChange = pImprovement.getImprovementBonusYield(iBonus, YieldTypes.YIELD_FOOD)
											if iImprovementYieldChange > iBestImprovementYieldChange:
												iBestImprovementYieldChange = iImprovementYieldChange
									iFoodYield += iBestImprovementYieldChange
									pPlot.setBonusType(BonusTypes(iBonus))
									print "Added: %s (%d)" % (gc.getBonusInfo(iBonus).getDescription(), iFoodYield)
			print "Player: %s Food: %d" % (pPlayer.getName(), iFoodYield)

	def normalizeForestLocks(self):
		eForest = GetInfoType("FEATURE_FOREST")
		iNumPlayers = gc.getGame().countCivPlayersEverAlive()
		for iPlayer in range(iNumPlayers):
			if iPlayer in self.pCivFlavourInfos.keys():
				if self.pCivFlavourInfos[iPlayer].isHasFeaturePreference(eForest):
					if self.pCivFlavourInfos[iPlayer].getFeaturePreferenceValue(eForest) > 0:
						continue
			pPlayer = gc.getPlayer(iPlayer)
			pStartingPlot = pPlayer.getStartingPlot()
			pSearchArea = SearchArea(SquareArea(1), FatCrossArea(2))
			for pPlot in pSearchArea.getRealPlots(pStartingPlot):
				if pPlot.getFeatureType() == eForest:
					if dice.get(100, "FlavourMod") < (FOREST_LOCK_SOFTENING * pSearchArea.getRealPlotWeight(pPlot, pStartingPlot)):
						pPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)

	def normalizeJungleStarts(self):
		eDeciduousForest = 0
		eJungle = GetInfoType("FEATURE_JUNGLE")
		eForest = GetInfoType("FEATURE_FOREST")
		eMarsh = GetInfoType("TERRAIN_MARSH")
		iNumPlayers = gc.getGame().countCivPlayersEverAlive()
		for iPlayer in range(iNumPlayers):
			if iPlayer not in self.pCivFlavourInfos.keys() or not self.pCivFlavourInfos[iPlayer].isHasFeaturePreference(eJungle):
				pPlayer = gc.getPlayer(iPlayer)
				pStartingPlot = pPlayer.getStartingPlot()
				pSearchArea = SearchArea(FatCrossArea(3))
				if pPlayer.getCivilizationType() == GetInfoType("CIVILIZATION_KURIOTATES"):
					pSearchArea.changeSize(+1)
				for pPlot in pSearchArea.getRealPlots(pStartingPlot):
					if pPlot.getFeatureType() == eJungle:
						result = dice.get(4, "FM")
						if result < 1 or pPlot.getTerrainType() == eMarsh:
							pPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
						elif result < 2 or max([abs(pStartingPlot.getX() - pPlot.getX()), abs(pStartingPlot.getY() - pPlot.getY())]) < 2:
							pPlot.setFeatureType(eForest, eDeciduousForest)
						else: pass # keep jungle

class FlavourPlot:

	def __init__(self, pPlot, iRegionMap):
		self.pPlot = pPlot
		self.bUsed = False
		self.iRegionMap = iRegionMap
		self.iIsolatedRegionSizes = {} # key: region
		self.iDistinctRegionSizes = {} # key: region tuple
		self.iRegionDistanceMatrix = None
		self.__initRegionDistanceMatrix()

	def __getattr__(self, name):
		if hasattr(self.pPlot, name):
			return getattr(self.pPlot, name)
		errargs = (self.pPlot.__class__.__name__, self.__class__.__name__, name)
		raise AttributeError("%s and %s instances have no attribute '%s'" % errargs)

	def __eq__(self, other):
		if self.getX() == other.getX() and self.getY() == other.getY():
			return True
		return False

	def __ne__(self, other):
		if self.getX() != other.getX() or self.getY() != other.getY():
			return True
		return False

	@classmethod
	def isPotentialFlavourPlot(cls, pPlot):
		if pPlot.isWater():
			return False
		if pPlot.isStartingPlot():
			return False
		if pPlot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS:
			return False
		if pPlot.getImprovementType() != ImprovementTypes.NO_IMPROVEMENT:
			if pPlot.getImprovementType() != GetInfoType("IMPROVEMENT_TOWER"):
				return False
		return True

	def __initRegionDistanceMatrix(self):
		if self.getNumRegions() == 1:
			self.iRegionDistanceMatrix = [0]
		else:
			# initialize an empty matrix
			iMatrix = []
			for i in range(self.getNumRegions()):
				iMatrix.append([None] * self.getNumRegions())
				iMatrix[i][i] = 0
			# move out of each region once, go always left and count steps till back on choke
			for iStartRegionId in range(self.getNumRegions()):
				iCurrentDirection = self.iRegionMap.index(iStartRegionId, self.iRegionMap.index(0))
				pCurrentPlot = plotDirection(self.getX(), self.getY(), DirectionTypes(iCurrentDirection))
				iStepCount = 0
				while not pCurrentPlot == self:
					for iDirection in range(8):
						iCandidateDirection = (iCurrentDirection + iDirection - 2) % 8
						pCandidatePlot = plotDirection(pCurrentPlot.getX(), pCurrentPlot.getY(), DirectionTypes(iCandidateDirection))
						if IsPassableLandPlot(pCandidatePlot) or (pCandidatePlot.isPeak() and pCandidatePlot == self):
							pCurrentPlot = pCandidatePlot
							iCurrentDirection = iCandidateDirection
							iStepCount += 1
							break
				# find out which region we were in, when we arrived
				iOppositeDirection = (iCurrentDirection + 4) % 8
				iEndRegionId = self.iRegionMap[iOppositeDirection]
				# save to matrix what we learned
				if iEndRegionId == iStartRegionId:
					for r in range(len(iMatrix)):
						for c in range(len(iMatrix[r])):
							if (r == iStartRegionId) ^ (c == iStartRegionId):
								iMatrix[r][c] = "Inf"
					self.iIsolatedRegionSizes[iStartRegionId] = iStepCount
				else: # different start and end region
					if iMatrix[iEndRegionId][iStartRegionId] == None or iMatrix[iEndRegionId][iStartRegionId] > iStepCount:
						iMatrix[iEndRegionId][iStartRegionId] = iStepCount
						iMatrix[iStartRegionId][iEndRegionId] = iStepCount
					else:
						iMatrix[iStartRegionId][iEndRegionId] = iMatrix[iEndRegionId][iStartRegionId]
			# set up the Distance Matrix
			if self.getNumRegions() > 2:
				self.iRegionDistanceMatrix = self.__calculateShortestPaths(iMatrix)
			else: self.iRegionDistanceMatrix = iMatrix

	def __calculateShortestPaths(self, iMatrix):
		# rare case handling for a size 4 region to prevent error in shortest path algorithm below
		if len(iMatrix[0]) == 4 and iMatrix[0].count(None) == 2:
			for ri, row in enumerate(iMatrix):
				for ii, item in enumerate(row):
					if item == None:
						iMatrix[ri][ii] = "Inf"
		# shortest path algorithm:
		iDimension = len(iMatrix[0])
		for r in range(iDimension):
			crange = range(iDimension)
			if None in iMatrix[r]:
				crange.insert(0, crange.pop(iMatrix[r].index(None)))
			for c in crange:
				if not c == r:
					iDistances = []
					if not iMatrix[r][c] == None:
						iDistances.append(iMatrix[r][c])
					for c2 in range(iDimension):
						if not (c2 == r or c2 == c) and iMatrix[r][c2] != None and iMatrix[c2][c] != None:
							if iMatrix[r][c2] == "Inf" or iMatrix[c2][c] == "Inf":
								iDistances.append("Inf")
							else:
								iDistances.append(iMatrix[r][c2] + iMatrix[c2][c])
					iMatrix[r][c] = min(iDistances)
		return iMatrix

	def getPlot(self):
		return self.pPlot

	def isUsed(self):
		return self.bUsed

	def setIsUsed(self, bUsed):
		self.bUsed = bUsed

	def getNumRegions(self):
		return max(self.iRegionMap) + 1

	def getNumIsolatedRegions(self):
		return len(self.iIsolatedRegionSizes)

	def getIsolatedRegionSizes(self):
		return self.iIsolatedRegionSizes.values()

	def getNumDistinctRegions(self):
		if self.getNumRegions() > self.getNumIsolatedRegions():
			return self.getNumIsolatedRegions() + 1
		return self.getNumIsolatedRegions()

	def getRegionDirections(self, iRegionId):
		if iRegionId > self.getNumRegions():
			raise IndexError("There is no region with index %s." % iRegionId)
		return [iDirection for iDirection, item in enumerate(self.iRegionMap) if item == iRegionId]

	def getRegionDistance(self, iRegionA, iRegionB):
		for region in [iRegionA, iRegionB]:
			if not region in self.iRegionMap:
				raise IndexError("There is no region with index %s." % region)
		return self.iRegionDistanceMatrix[iRegionA-1][iRegionB-1]

	def getDistanceRoundtrip(self):
		iRoundtrip = 0
		if self.isChokePoint():
			regions = range(self.getNumRegions())
			for iRegionA, iRegionB in zip(regions, regions[1:]+[0]):
				distance = self.getRegionDistance(iRegionA, iRegionB)
				if distance == "Inf": return "Inf"
				iRoundtrip += distance
		return iRoundtrip

	def isChokePoint(self):
		if self.getNumRegions() > 1:
			return True
		return False

	def seeThroughLevelArea(self):
		iSIZE = 1
		iAreaHeight = 0
		iPlotCounter = 0
		iNumPlots = ( iSIZE * 2 + 1 ) ** 2
		pSearchArea = SearchArea(SquareArea(iSIZE))
		for pPlot in pSearchArea.getRealPlots(self.pPlot):
			iAreaHeight += pPlot.seeThroughLevel()
			iPlotCounter += 1
		for iNonePlot in range(iNumPlots-iPlotCounter):
			iAreaHeight += 3
		return iAreaHeight / iNumPlots

	def isVantagePoint(self):
		if self.isPeak():
			return False
		if self.getTerrainType() == GetInfoType("TERRAIN_TUNDRA") and not self.isHills():
			return False
		iModifier = 0
		if self.isCoastalLand():
			iModifier += 1/2
		elif not self.isHills():
			iModifier -= 1/4
		iSeeThroughChange = 0
		if self.getFeatureType() != FeatureTypes.NO_FEATURE:
			iSeeThroughChange = gc.getFeatureInfo(self.getFeatureType()).getSeeThroughChange()
		if (self.seeThroughLevel() - iSeeThroughChange) < self.seeThroughLevelArea() + iModifier:
			return False
		return True

	def isMountainPass(self):
		iPeakCount = 0
		for i in range(CardinalDirectionTypes.NUM_CARDINALDIRECTION_TYPES):
			pAdjacentPlot = plotCardinalDirection(self.getX(), self.getY(), CardinalDirectionTypes(i))
			if not pAdjacentPlot.isNone() and pAdjacentPlot.isPeak():
				iPeakCount += 1
				if iPeakCount > 1:
					return True
		return False


class UniqueImprovement:

	def __init__(self, pPlot):
		self.pPlot = pPlot
		self.eImprovement = pPlot.getImprovementType()
		self.eBonus = pPlot.getBonusType(TeamTypes.NO_TEAM)
		self.pUnitList = []
		for iUnit in range(pPlot.getNumUnits()):
			self.pUnitList.append(pPlot.getUnit(iUnit))
		self.pSearchArea = SearchArea(SquareArea(1))

	def __getattr__(self, name):
		pImprovement = gc.getImprovementInfo(self.eImprovement)
		if hasattr(pImprovement, name):
			return getattr(pImprovement, name)
		errargs = (pImprovement.__class__.__name__, self.__class__.__name__, name)
		raise AttributeError("%s and %s instances have no attribute '%s'" % errargs)

	def getInfoType(self):
		return self.eImprovement

	def getPlot(self):
		return self.pPlot

	def unassign(self):
		if self.isAssigned():
			self.pPlot.setImprovementType(ImprovementTypes.NO_IMPROVEMENT)
			self.pPlot.setBonusType(BonusTypes.NO_BONUS)
			self.pPlot = None

	def isAssigned(self):
		if self.pPlot != None: return True
		return False

	def isUnassigned(self):
		if self.pPlot == None: return True
		return False

	def isDangerous(self):
		if self.getType() in DANGEROUS_UNIQUE_IMPROVEMENTS: return True
		return False

	def isDangerouslyClose(self):
		if self.isDangerous():
			for pStartingPlot in FlavourGenerator.pStartingPlotList:
				if GetStepDistance(self.pPlot, pStartingPlot) <= DANGEROUS_UNIQUE_IMPROVEMENT_STARTING_PLOT_SPACING:
					return True
		return False

	def getStartingPlotSpacing(self):
		if not self.isDangerous():
			return UNIQUE_IMPROVEMENT_STARTING_PLOT_SPACING
		else:
			return DANGEROUS_UNIQUE_IMPROVEMENT_STARTING_PLOT_SPACING

	def isPlotMakesValid(self, pTestPlot):
		if pTestPlot.canHaveImprovement(self.eImprovement, TeamTypes.NO_TEAM, False):
			if pTestPlot.getBonusType(TeamTypes.NO_TEAM) == BonusTypes.NO_BONUS:
				if pTestPlot.getImprovementType() == ImprovementTypes.NO_IMPROVEMENT:
					for pStartingPlot in FlavourGenerator.pStartingPlotList:
						if GetStepDistance(pTestPlot, pStartingPlot) <= self.getStartingPlotSpacing():
							return False
					for pUniqueImprovement in FlavourGenerator.pUniqueImprovementList:
						if pUniqueImprovement.isAssigned():
							if GetStepDistance(pTestPlot, pUniqueImprovement.getPlot()) <= UNIQUE_IMPROVEMENT_SPACING:
								return False
					return True
		return False

	def computeSurroundingAreaValue(self, pCandidatePlot):
		iSurroundingAreaValue = 0
		for pSearchAreaPlot in self.pSearchArea.getRealPlots(pCandidatePlot):
			#fSearchAreaPlotWeight = self.pSearchArea.getRealPlotWeight(pSearchAreaPlot, pCandidatePlot)
			if pSearchAreaPlot.canHaveImprovement(self.eImprovement, TeamTypes.NO_TEAM, False):
				iSurroundingAreaValue += SearchArea.FULL_WEIGHT
			elif pSearchAreaPlot.isPeak():
				iSurroundingAreaValue += SearchArea.FULL_WEIGHT * 9/10
			elif pSearchAreaPlot.isWater():
				iSurroundingAreaValue += SearchArea.FULL_WEIGHT * 5/10
		return iSurroundingAreaValue

	def assignFlavourfulLocation(self):
		# find valid candidates:
		pCandidatePlotList = []
		for iPlotIndex in xrange(cymap.numPlots()):
			pPlot = cymap.plotByIndex(iPlotIndex)
			if self.isPlotMakesValid(pPlot):
				pCandidatePlotList.append(pPlot)
		# flavourful surroundings?
		iCandidatePlotValueList = []
		if len(pCandidatePlotList) > 0:
			for pCandidatePlot in pCandidatePlotList:
				iCandidatePlotValueList.append(self.computeSurroundingAreaValue(pCandidatePlot))
		else:
			self.beForgotten()
			return
		# choose one of the plots with the highest value:
		iMaxValue = max(iCandidatePlotValueList)
		pairValuePlotList = zip(iCandidatePlotValueList, pCandidatePlotList)
		pBestPlotList = [pairValuePlot[1] for pairValuePlot in pairValuePlotList if pairValuePlot[0] == iMaxValue]

		# MAELSTROM (small sea placement special):
		if self.getType() == "IMPROVEMENT_MAELSTROM":
			iWaterAreaBySizeDictionary = {}
			for iArea in range(cymap.getNumAreas()):
				pArea = cymap.getArea(iArea)
				if pArea.isWater() and pArea.getNumTiles() > 8:
					iWaterAreaBySizeDictionary[pArea.getNumTiles()] = pArea.getID()
			debugOut(iWaterAreaBySizeDictionary)
			for iSize in sorted(iWaterAreaBySizeDictionary):
				pEvenBetterPlotList = [pBestPlot for pBestPlot in pBestPlotList if pBestPlot.getArea() == iWaterAreaBySizeDictionary[iSize]]
				if len(pEvenBetterPlotList) > 0:
					pBestPlotList = pEvenBetterPlotList
					break
		# MAELSTROM End

		# GUARDIAN (right on a choke point):
		if self.getType() == "IMPROVEMENT_GUARDIAN":
			pGuardianPlotList = []
			for pFlavourPlot in FlavourGenerator.pFlavourPlotList:
				if pFlavourPlot.isMountainPass() and self.isPlotMakesValid(pFlavourPlot):
					if (pFlavourPlot.getNumDistinctRegions() > 1 and min(pFlavourPlot.getIsolatedRegionSizes()) > 8):
						pGuardianPlotList.append(pFlavourPlot)
			if len(pGuardianPlotList) == 0:
				for pFlavourPlot in FlavourGenerator.pFlavourPlotList:
					if pFlavourPlot.isMountainPass() and self.isPlotMakesValid(pFlavourPlot):
						if pFlavourPlot.getNumRegions() > 1 and pFlavourPlot.getDistanceRoundtrip() > 12:
							pGuardianPlotList.append(pFlavourPlot)
			debugOut("Possible Guardian Plots: %d" % len(pGuardianPlotList))
			if len(pGuardianPlotList) > 0:
				iGuardianPlot = dice.get(len(pGuardianPlotList), "FlavourMod: Unique Improvements")
				pGuardianPlot = pGuardianPlotList[iGuardianPlot]
				pGuardianPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
				pGuardianPlot.setIsUsed(True)
				pBestPlotList = [pGuardianPlot.getPlot()]
			else:
				self.beForgotten()
				return
		# GUARDIAN End

		iBestPlot = dice.get(len(pBestPlotList), "FlavourMod: Unique Improvements")
		# assign improvement to the chosen plot:
		self.pPlot = pBestPlotList[iBestPlot]
		self.pPlot.setImprovementType(self.eImprovement)
		self.pPlot.setBonusType(self.eBonus)
		if self.pPlot.getNumUnits() == 0:
			for pUnit in self.pUnitList:
				pUnit.setXY(self.pPlot.getX(), self.pPlot.getY(), False, True, True,False)
		else: self.killThemAll()
		# debug information:
		sImprovementName = self.getDescription()
		debugOut("Assigned %s to (%d,%d) in Area %d." % (sImprovementName, self.pPlot.getX(), self.pPlot.getY(), self.pPlot.getArea()))

	def killThemAll(self):
		for pUnit in self.pUnitList:
			for iPromotion in range(gc.getNumPromotionInfos()):
				if gc.getPromotionInfo(iPromotion).isEquipment():
					pUnit.setHasPromotion(PromotionTypes(iPromotion), False)
			pUnit.kill(False, -1)

	def beForgotten(self):
		self.killThemAll()
		sImprovementName = self.getDescription()
		debugOut("Had to destroy %s." % sImprovementName)


class CivFlavourInfo:

	def __init__(self, sCivType):
		self.civ = GetInfoType(sCivType)
		self.pPreferences = []
		self.iSearchAreaSizeChange = 0

	def addPreference(self, *args):
		if not (len(args) == 2 or len(args) == 3):
			raise TypeError("CivFlavourInfo.addPreference() takes 2 or 3 arguments (%d given)"  % len(args))
		pPreference = None
		sType = args[0].upper()
		if sType.startswith("PLOT"):
			pPreference = PlotTypePreference(sType, args[1])
		elif sType.startswith("TERRAIN"):
			pPreference = TerrainPreference(sType, args[1])
		elif sType.startswith("FEATURE"):
			pPreference = FeaturePreference(sType, args[1])
		elif sType.startswith("BONUS"):
			pPreference = BonusPreference(sType, args[1])
		elif sType.startswith("IMPROVEMENT"):
			if gc.getImprovementInfo(GetInfoType(sType)).isUnique():
				pPreference = UniqueImprovementPreference(sType, args[1])
			else:
				pPreference = ImprovementPreference(sType, args[1])
		elif sType.startswith("YIELD"):
			pPreference = YieldPreference(sType, args[1])
		elif sType.startswith("MOBILITY"):
			pPreference = MobilityPreference(sType, args[1])
		elif sType.startswith("COASTAL_START"):
			pPreference = CoastalStartPreference(sType, args[1])
		elif sType.startswith("RIVERSIDE"):
			pPreference = RiverSidePreference(sType, args[1])
		elif sType.startswith("ISOLATION"):
			pPreference = IsolationPreference(sType, args[1])
		else: raise ValueError("%s is not a possible preference." % args[0])
		if len(args) == 3:
			pPreference.setSearchArea(args[2])
		if self.iSearchAreaSizeChange != 0 and not isinstance(pPreference, CoastalStartPreference):
			pPreference.getSearchArea().changeSize(+1)
		self.pPreferences.append(pPreference)

	def getNumPreferences(self):
		return len(self.pPreferences)

	def isHasFeaturePreference(self, eFeatureType):
		for pPreference in self.pPreferences:
			if isinstance(pPreference, FeaturePreference):
				if pPreference.getType() == eFeatureType:
					return True
		return False

	def getFeaturePreferenceValue(self, eFeatureType):
		if not self.isHasFeaturePreference(eFeatureType):
			civ = gc.getCivilizationInfo(self.civ).getDescription()
			feature = gc.getFeatureInfo(eFeatureType).getDescription()
			raise AttributeError, "The %s don't have a preference for %s." % (civ, feature)
		for pPreference in self.pPreferences:
			if isinstance(pPreference, FeaturePreference):
				if pPreference.getType() == eFeatureType:
					return pPreference.getValue()

	def changeSearchAreaSize(self, iChange):
		self.iSearchAreaSizeChange = iChange
		for pPreference in self.pPreferences:
			if not isinstance(pPreference, CoastalStartPreference):
				pPreference.getSearchArea().changeSize(+1)

	def getTotalValue(self):
		total = 0.0
		for pPreference in self.pPreferences:
			total += pPreference.getValue()
		return abs(total) # - * - = +

	def evaluateStartingPlots(self, iTeam):
		iCumNormAreaScores = [0.0] * len(FlavourGenerator.pStartingPlotList)
		debugOut(gc.getCivilizationInfo(self.civ).getDescription())
		s = ""
		for pStartingPlot in FlavourGenerator.pStartingPlotList:
			s += "(%s,%s) " % (pStartingPlot.getX(), pStartingPlot.getY())
		debugOut(s)
		for pPreference in self.pPreferences:
			iAreaScores = pPreference.evaluateStartingPlots(iTeam)
			iCumNormAreaScores = map(lambda x, y: x + y, iCumNormAreaScores, iAreaScores)
		debugOut(FormatList(iCumNormAreaScores, rowname = "Kummulierte Messungen"))
		return ScaleList(map(lambda x: x / self.getTotalValue(), iCumNormAreaScores))

class Preference: # virtual

	def __init__(self, sType, iValue):
		self.setType(sType)
		self.setValue(iValue)
		self.setSearchArea(self.getDefaultSearchArea()) # None -> use default

	def getType(self):
		return self.type

	def setType(self, sType):
		self.type = GetInfoType(sType)

	def getValue(self):
		return self.value

	def setValue(self, iValue):
		self.value = iValue

	def getSearchArea(self):
		return self.area

	def getDefaultSearchArea(self):
		return SearchArea(FatCrossArea(CORE_SEARCH_AREA_RADIUS), FatCrossArea(CORE_SEARCH_AREA_RADIUS + EXTRA_SEARCH_AREA_RADIUS))

	def setSearchArea(self, pSearchArea):
		if isinstance(pSearchArea, SearchArea):
			self.area = pSearchArea
		else: TypeError("Not a SeachArea.")

	def evaluateStartingPlots(self, iTeam):
		fAreaScores = []
		for pStartingPlot in FlavourGenerator.pStartingPlotList:
			fAreaScore = 0.0
			for pPlot in self.getSearchArea().getRealPlots(pStartingPlot):
				if self.isMatch(pPlot, iTeam):
					fAreaScore += self.getYield(pPlot, iTeam) * self.getSearchArea().getRealPlotWeight(pPlot, pStartingPlot)
			fRealAreaWeight = self.getSearchArea().getRealAreaWeight(pStartingPlot, self)
			if fRealAreaWeight > 0:
				fAreaScores.append(fAreaScore/fRealAreaWeight)
			else:
				fAreaScores.append(fAreaScore)
		return map(lambda x: x * self.getValue(), ScaleList(fAreaScores))

	def getYield(self, pPlot, iTeam):
		return 1

class PlotTypePreference(Preference):

	def setType(self, sPlotType):
		self.type = PLOT_TYPES[sPlotType]

	def isMatch(self, pPlot, iTeam):
		if pPlot.getPlotType() == self.getType(): return True
		return False

class TerrainPreference(Preference):

	def isMatch(self, pPlot, iTeam):
		if pPlot.getTerrainType() == self.getType(): return True
		return False

class FeaturePreference(Preference):

	def isMatch(self, pPlot, iTeam):
		if pPlot.getFeatureType() == self.getType(): return True
		return False

class BonusPreference(Preference):

	def isMatch(self, pPlot, iTeam):
		if pPlot.getBonusType(TeamTypes.NO_TEAM) == self.getType(): return True
		return False

class ImprovementPreference(Preference):

	def isMatch(self, pPlot, iTeam):
		if pPlot.getImprovementType() == self.getType(): return True
		return False

class UniqueImprovementPreference(Preference):

	def evaluateStartingPlots(self, iTeam):
		for pUniqueImprovement in FlavourGenerator.pUniqueImprovementList:
			if self.getType() == pUniqueImprovement.getInfoType():
				fAreaScores = []
				for pStartingPlot in FlavourGenerator.pStartingPlotList:
					fAreaScore = -GetStepDistance(pUniqueImprovement.getPlot(), pStartingPlot)
					if pUniqueImprovement.getPlot().getArea() != pStartingPlot.getArea():
						if not pUniqueImprovement.getPlot().isWater():
							fAreaScores.append(DIFFERENT_LANDAREA_PENALTY_FACTOR * fAreaScore)
							continue
					fAreaScores.append(fAreaScore)
				debugOut(FormatList(fAreaScores, rowname = pUniqueImprovement.getDescription()))
				fWeightedAreaScores = [x**10 * self.getValue() for x in ScaleList(fAreaScores, absmax = 0)]
				debugOut(FormatList(fWeightedAreaScores))
				return fWeightedAreaScores
		return [0] * len(FlavourGenerator.pStartingPlotList)


class YieldPreference(Preference):

	def setType(self, sYield):
		self.type = YIELD_TYPES[sYield]

	def getDefaultSearchArea(self):
		return SearchArea(FatCrossArea(CORE_SEARCH_AREA_RADIUS))

	def isMatch(self, pPlot, iTeam):
		if pPlot.hasYield(): return True
		return False

	def getYield(self, pPlot, iTeam):
		iYield = 0
		iYield = pPlot.calculateNatureYield(self.getType(), iTeam, False)
		# add potential extra yield from improved bonuses
		eBonus = pPlot.getBonusType(TeamTypes.NO_TEAM)
		if eBonus != BonusTypes.NO_BONUS:
			eTech = TechTypes(gc.getBonusInfo(eBonus).getTechReveal())
			if eTech == TechTypes.NO_TECH \
			or gc.getTechInfo(eTech).getResearchCost() != -1 \
			or gc.getTeam(iTeam).isHasTech(eTech):
				iYieldChanges = []
				for iImprovement in range(gc.getNumImprovementInfos()):
					pImprovement = gc.getImprovementInfo(iImprovement)
					if pImprovement.isImprovementBonusMakesValid(eBonus):
						iYieldChange = pImprovement.getImprovementBonusYield(eBonus, self.getType())
						iYieldChanges.append(iYieldChange)
				if len(iYieldChanges) > 0:
					if eTech != TechTypes.NO_TECH:
						iYield += int(max(iYieldChanges) * BONUS_REVEAL_ERA_WEIGHTS[gc.getTechInfo(eTech).getEra()])
					else:
						iYield += max(iYieldChanges)
		return iYield

class MobilityPreference(Preference):

	def setType(self, sMobility):
		self.type = 1 # only one type possible

	def getDefaultSearchArea(self):
		return SearchArea(SquareArea(0), SquareArea(CORE_SEARCH_AREA_RADIUS + EXTRA_SEARCH_AREA_RADIUS))

	def isMatch(self, pPlot, iTeam):
		if not (pPlot.isWater() or pPlot.isImpassable()): return True
		return False

	def getYield(self, pPlot, iTeam):
		iMovementCost = 0
		if pPlot.getFeatureType() != FeatureTypes.NO_FEATURE:
			iMovementCost = gc.getFeatureInfo(pPlot.getFeatureType()).getMovementCost()
		else:
			iMovementCost = gc.getTerrainInfo(pPlot.getTerrainType()).getMovementCost()
		if pPlot.isHills():
			iMovementCost += gc.getHILLS_EXTRA_MOVEMENT()
		return -iMovementCost

class CoastalStartPreference(Preference):

	def setType(self, sCoastalStart):
		self.type = 1 # only one type possible

	def getDefaultSearchArea(self):
		return SearchArea(SquareArea(0), SquareArea(0))

	def isMatch(self, pPlot, iTeam):
		for i in range(DirectionTypes.NUM_DIRECTION_TYPES):
			pAdjacentPlot = plotDirection(pPlot.getX(), pPlot.getY(), DirectionTypes(i))
			if not pAdjacentPlot.isNone():
				if pAdjacentPlot.isWater():
					if not pAdjacentPlot.isLake():
						return True
		return False

class RiverSidePreference(Preference):

	def setType(self, sRiver):
		self.type = 1 # only one type possible

	def getDefaultSearchArea(self):
		return SearchArea(FatCrossArea(0), FatCrossArea(CORE_SEARCH_AREA_RADIUS + EXTRA_SEARCH_AREA_RADIUS))

	def isMatch(self, pPlot, iTeam):
		if pPlot.isRiverSide():
			return True
		return False

class IsolationPreference(Preference):

	def setType(self, sType):
		self.type = -1

	def evaluateStartingPlots(self, iTeam):
		iStartingPlotScores = []
		for pStartingPlotA in FlavourGenerator.pStartingPlotList:
			iStartingPlotScore = 0
			for pStartingPlotB in FlavourGenerator.pStartingPlotList:
				iStepDistance = GetStepDistance(pStartingPlotA, pStartingPlotB)
				iPathDistance = cymap.calculatePathDistance(pStartingPlotA, pStartingPlotB)
				if iPathDistance > -1:
					iStartingPlotScore += iPathDistance
				else:
					iStartingPlotScore += max(FlavourGenerator.MAX_PATH_DISTANCE, iStepDistance)
			iStartingPlotScores.append(iStartingPlotScore**(1/2))
		debugOut(FormatList(iStartingPlotScores, rowname = "IsolationScores"))
		return [x * self.getValue() for x in ScaleList(iStartingPlotScores)]


## HELPER FUNCTIONS & GLOBAL VARAIABLES (internal)

PLOT_TYPES = {	'PLOT_PEAK': PlotTypes.PLOT_PEAK,
				'PLOT_HILLS': PlotTypes.PLOT_HILLS,
				'PLOT_LAND': PlotTypes.PLOT_LAND,
				'PLOT_OCEAN': PlotTypes.PLOT_OCEAN }

YIELD_TYPES = {	'YIELD_FOOD': YieldTypes.YIELD_FOOD,
				'YIELD_PRODUCTION': YieldTypes.YIELD_PRODUCTION,
				'YIELD_COMMERCE': YieldTypes.YIELD_COMMERCE }

class VarietyTypes:
	NO_VARIETY = -1
	DECIDUOUS_FOREST = 0
	CONIFEROUS_FOREST = 1
	BOREAL_FOREST = 2

def debugOut(output):
	if DEBUG_ENABLE_LOGGING: print(output)
	return

def GetInfoType(sInfoType, bIgnoreTypos = False):
	iInfoType = gc.getInfoTypeForString(sInfoType)
	if iInfoType == -1 and not bIgnoreTypos:
		arg = ("InfoType %s unknown! Probably just a Typing Error." % sInfoType)
		raise ValueError, arg
	return iInfoType

def GetCivNameList():
	sCivNameList = []
	iPlayerCount = gc.getGame().countCivPlayersEverAlive()
	for iPlayer in range(iPlayerCount):
		pPlayer = gc.getPlayer(iPlayer)
		eCivType = pPlayer.getCivilizationType()
		sCivNameList.append(gc.getCivilizationInfo(eCivType).getDescription())
	return sCivNameList

def ScaleList(values, absmin = None, absmax = None):
	minValue = absmin
	maxValue = absmax
	if minValue == None: minValue = min(values)
	if maxValue == None: maxValue = max(values)
	if minValue == maxValue: return [0.0] * len(values)
	return map(lambda x: (float(x)-minValue)/(maxValue-minValue), values)

def FormatList(l, description = None, rowname = None):
	if len(l) > 0:
		s = ""
		if description != None:
			s += description + 2 * "\n"
		for i in xrange(len(l)):
			s += "%8.4f" % float(l[i])
		if rowname != None:
			s += 3*" " + rowname
		return s
	return("Error while creating formated list string.")

def FormatMatrix(matrix, description = None, rownames = None):
	if len(matrix) > 0:
		s = ""
		if description != None:
			s += description + 2 * "\n"
		for r in xrange(len(matrix)):
			for c in xrange(len(matrix[0])):
				if matrix[r][c] != None:
					s += "%8.4f" % matrix[r][c]
				else:
					s += "%8s" % "None"
			if rownames != None:
				s += 3*" " + rownames[r]
			s += "\n"
		return s
	return("Error while creating formated matrix string.")

def GetStepDistance(pPlotA, pPlotB):
	return stepDistance(pPlotA.getX(), pPlotA.getY(), pPlotB.getX(), pPlotB.getY())

def GetMaxStepDistance():
	if CyMap().getGridWidth() > CyMap().getGridHeight():
		if CyMap().isWrapX():
			return (CyMap().getGridWidth() + 1) // 2
		return CyMap().getGridWidth()
	if CyMap().isWrapY():
		return (CyMap().getGridHeigth() + 1) // 2
	return CyMap().getGridHeight()

def GetMaxPathDistance():
	iMaxPathDistance = 0
	for iPlotA in range(cymap.numPlots()):
		pPlotA = cymap.plotByIndex(iPlotA)
		if IsPassableLandPlot(pPlotA):
			for iPlotB in range(iPlotA+1, cymap.numPlots()):
				pPlotB = cymap.plotByIndex(iPlotB)
				if IsPassableLandPlot(pPlotB):
					iDistance = cymap.calculatePathDistance(pPlotA, pPlotB)
					if iDistance > iMaxPathDistance:
						iMaxPathDistance = iDistance
	return iMaxPathDistance

def GetMaxPathDistanceFast():
	''' This is only a appoximation on base of the StartingPlot distances.'''
	iMaxPathDistance = 0
	for i, pPlotA in enumerate(FlavourGenerator.pStartingPlotList):
		for pPlotB in FlavourGenerator.pStartingPlotList[i+1:]:
			iDistance = cymap.calculatePathDistance(pPlotA, pPlotB)
			if iDistance > iMaxPathDistance:
				iMaxPathDistance = iDistance
	return iMaxPathDistance

def IsCardinalDirection(iDirection):
	if (iDirection % 2) == 0:
		return True
	return False

def IsPassableLandPlot(pPlot):
	if not (pPlot.isNone() or pPlot.isWater() or pPlot.isPeak()): return True
	return False

def IsMapHasTerrainType(sTerrainType):
	eTerrainType = GetInfoType(sTerrainType)
	for iPlotIndex in range(cymap.numPlots()):
		pPlot = cymap.plotByIndex(iPlotIndex)
		if pPlot.getTerrainType() == eTerrainType:
			return True
	return False

def IsMapHasFeatureType(sFeatureType):
	eFeatureType = GetInfoType(sFeatureType)
	for iPlotIndex in range(cymap.numPlots()):
		pPlot = cymap.plotByIndex(iPlotIndex)
		if pPlot.getFeatureType() == eFeatureType:
			return True
	return False
	
def IsMapHasPlotEffectType(sFeatureType):
	eFeatureType = GetInfoType(sFeatureType)
	for iPlotIndex in range(cymap.numPlots()):
		pPlot = cymap.plotByIndex(iPlotIndex)
		if pPlot.getPlotEffectType() == eFeatureType:
			return True
	return False

def SendSimpleMessage(sMessage, iPlayer = 0, eType = None, eColor = None, pPlot = None):
	# set up the message parameters
	ePlayer = PlayerTypes(iPlayer)
	if eType == None:
		eType = InterfaceMessageTypes.MESSAGE_TYPE_INFO
	if eColor == None:
		eColor = ColorTypes.NO_COLOR
	if pPlot == None:
		iX = -1
		iY = -1
	else:
		iX = pPlot.getX()
		iY = pPlot.getY()
	# send the message to the interface:
	CyInterface().addMessage(ePlayer, False, 25, sMessage, \
		None, eType, None, eColor, iX, iY, False, False)

def ordinal(cardinal):
	sLastDigit = str(cardinal)[-1:]
	sLastTwoDigits = str(cardinal)[-2:]
	if sLastDigit == "1" and sLastTwoDigits != "11":
		return str(cardinal) + "st"
	if sLastDigit == "2" and sLastTwoDigits != "12":
		return str(cardinal) + "nd"
	if sLastDigit == "3" and sLastTwoDigits != "13":
		return str(cardinal) + "rd"
	return  str(cardinal) + "th"


## AREA CLASSES

class Area: # abstract class

	def __init__(self, iNumRings):
		self.setNumRings(iNumRings)

	def copy(self):
		return eval("%s(%d)" % (self.__class__.__name__, self.getNumRings()))

	def getNumRings(self):
		return self.iNumRings

	def setNumRings(self, iNumRings):
		if iNumRings < 0:
			arg = "Size of Area has to be >= Zero!"
			raise ValueError(arg)
		self.iNumRings = iNumRings

	def getPlots(self):
		return self.getPlotsFromRings(0, self.iNumRings)

	def getPlotsFromRing(self, iRing):
		return self.getPlotsFromRings(iRing, iRing)

	def getPlotsFromRings(self, iFirstRing, iLastRing): # abstract (semi)
		if iFirstRing < 0:
			arg = "First argument has to be >= Zero!"
			raise ValueError(arg)
		if iLastRing < 0:
			arg = "Second argument has to be >= Zero!"
			raise ValueError(arg)
		if iFirstRing > iLastRing:
			arg = "First argument has to be <= second argument!"
			raise ValueError(arg)
		if iLastRing > self.iNumRings:
			arg = "Second argument has to be <= Size of Area!"
			raise ValueError(arg)

	def getRingFromPlot(self, iX, iY): # abstract
		raise "Error: not implemented. Has to be overwritten in subclasses"

	def isContainsPlot(self, iX, iY):
		iRing = self.getRingFromPlot(iX, iY)
		if iRing > self.iNumRings: return False
		return True


class SquareArea(Area):

	def getPlotsFromRings(self, iFirstRing, iLastRing):
		Area.getPlotsFromRings(self, iFirstRing, iLastRing)
		coords = []
		for x in range(-iLastRing, iLastRing+1):
			for y in range(-iLastRing, iLastRing+1):
				if not (abs(x) < iFirstRing and abs(y) < iFirstRing):
					coords.append((x,y))
		return coords

	def getRingFromPlot(self, iX, iY):
		return max(abs(iX), abs(iY))


class FatCrossArea(Area):

	def getPlotsFromRings(self, iFirstRing, iLastRing):
		Area.getPlotsFromRings(self, iFirstRing, iLastRing)
		coords = []
		for x in range(-iLastRing, iLastRing+1):
			for y in range(-iLastRing, iLastRing+1):
				dist = abs(x) + abs(y)
				if dist > iFirstRing and dist < iLastRing+2:
					coords.append((x,y))
				elif dist == iFirstRing and (x == 0 or y == 0):
					coords.append((x,y))
		return coords

	def getRingFromPlot(self, iX, iY):
		dist = abs(iX) + abs(iY)
		if iX == 0 or iY == 0: return dist
		return dist - 1


class SearchArea:

	FULL_WEIGHT = 1.0

	def __init__(self, pHeartLand, *args):
		if len(args) > 0:
			pHinterLand = args[0]
		else:
			pHinterLand = pHeartLand.copy()
		if not isinstance(pHeartLand, Area):
			arg = "pHeartLand has to be of type Area!"
			raise ValueError(arg)
		if not isinstance(pHinterLand, Area):
			arg = "pHinterLand has to be of type Area!"
			raise ValueError(arg)
		if pHeartLand.getNumRings() > pHinterLand.getNumRings():
			arg = "Size of HeartLand > HinterLand!"
			raise ValueError(arg)
		self.pHeartLand = pHeartLand
		self.pHinterLand = pHinterLand
		# save some stuff for very speedy recycling:
		self.pPlotIndexes = []
		self.__initPlotIndexes()
		self.PIDD = {} # plot index dictionaries dictionary (key: center plot address)
		self.PWD = {} # plot weight dictionary (key: plot index)

	def __initPlotIndexes(self):
		''' creates a list of the plot indices of this Area object '''
		iNumRings = self.pHinterLand.getNumRings()
		for x in range(-iNumRings, iNumRings + 1):
			for y in range(-iNumRings, iNumRings + 1):
				if self.pHeartLand.isContainsPlot(x,y) \
				or self.pHinterLand.isContainsPlot(x,y):
					self.pPlotIndexes.append((x,y))

	def geNumPlotIndexes(self):
		return len(self.pPlotIndexes)

	def changeSize(self, iChange):
		self.pHeartLand.setNumRings(self.pHeartLand.getNumRings() + iChange)
		self.pHinterLand.setNumRings(self.pHinterLand.getNumRings() + iChange)
		self.pPlotIndexes = []
		self.__initPlotIndexes()
		self.PIDD = {}
		self.PWD = {}

	def getPlotIndexDictionary(self, pCenterPlot):
		'''
		Translates the Area indices into real plot coordinates and saves them
		in a dictionary with the center plot address as a key for this
		particular dictionary.
		'''
		if pCenterPlot in self.PIDD:
			return self.PIDD[pCenterPlot]
		else:
			pxyPlotIndexDictionary = {} # key: plot coordinate; value: plot index
			for x, y in self.pPlotIndexes:
				pPlot = cymap.plot(pCenterPlot.getX() + x, pCenterPlot.getY() + y)
				if not pPlot.isNone():
					pxyPlotIndexDictionary[(pPlot.getX(), pPlot.getY())] = (x,y)
			self.PIDD[pCenterPlot] = pxyPlotIndexDictionary
			return pxyPlotIndexDictionary

	def getHeartLandPlots(self):
		return self.pHeartLand.getPlots()

	def getHinterLandBeltPlots(self):
		lBeltPlots = []
		iNumRings = self.pHinterLand.getNumRings()
		for x in range(-iNumRings, iNumRings + 1):
			for y in range(-iNumRings, iNumRings + 1):
				if self.pHinterLand.isContainsPlot(x,y) \
				and not self.pHeartLand.isContainsPlot(x,y):
					lBeltPlots.append((x,y))
		return lBeltPlots

	def getMaxHinterLandBeltSize(self):
		lBeltPlots = self.getHinterLandBeltPlots()
		iHinterLandSize = self.pHinterLand.getNumRings()
		iMaxBeltSize = 0
		for x, y in lBeltPlots:
			iHinterLandRing = self.pHinterLand.getRingFromPlot(x,y)
			iBeltSize = iHinterLandSize + 1 - iHinterLandRing
			if iBeltSize > iMaxBeltSize:
				iMaxBeltSize = iBeltSize
		return iMaxBeltSize

	def getPlotWeight(self, iX, iY):
		if (iX, iY) in self.PWD:
			return self.PWD[(iX, iY)]
		if self.pHeartLand.isContainsPlot(iX, iY):
			self.PWD[(iX, iY)] = self.FULL_WEIGHT
			return self.FULL_WEIGHT
		if self.pHinterLand.isContainsPlot(iX, iY):
			iNumRings = self.pHinterLand.getNumRings()
			iRing = self.pHinterLand.getRingFromPlot(iX, iY)
			iMaxBeltSize = self.getMaxHinterLandBeltSize()
			fDistanceWeight = (iNumRings - iRing + 1) / float(iMaxBeltSize+1)
			self.PWD[(iX, iY)] = fDistanceWeight * self.FULL_WEIGHT
			return fDistanceWeight * self.FULL_WEIGHT
		return 0.0 # plot even outside hinterland

	def getRealPlots(self, pCenterPlot):
		lpPlots = []
		for x, y in self.pPlotIndexes:
			pPlot = cymap.plot(pCenterPlot.getX() + x, pCenterPlot.getY() + y)
			if not pPlot.isNone():
				lpPlots.append(pPlot)
		return lpPlots

	def getRealPlotWeight(self, pPlot, pCenterPlot):
		xyIndex = self.getPlotIndexDictionary(pCenterPlot)[(pPlot.getX(), pPlot.getY())]
		return self.getPlotWeight(xyIndex[0], xyIndex[1])

	def getRealAreaWeight(self, pCenterPlot, pPreference):
		fSumAreaPlotWeights = 0.0
		pPlots = self.getRealPlots(pCenterPlot)
		for pPlot in pPlots:
			if isinstance(pPreference, MobilityPreference):
				if pPreference.isMatch(pPlot, -1):
					fSumAreaPlotWeights += self.getRealPlotWeight(pPlot, pCenterPlot)
			elif isinstance(pPreference, FeaturePreference):
				if pPreference.getValue() < 0:
					if pPlot.canHaveFeature(pPreference.getType()):
						fSumAreaPlotWeights += self.getRealPlotWeight(pPlot, pCenterPlot)
				else:
					fSumAreaPlotWeights += self.getRealPlotWeight(pPlot, pCenterPlot)
			else:
				fSumAreaPlotWeights += self.getRealPlotWeight(pPlot, pCenterPlot)
		return fSumAreaPlotWeights

###############################################################################
## The following class provides Munkres' Optimization Algorithm for the
## classical Linear Weighted Assignment Problem by Brian M. Clapper (c)
## Version:		"1.0.5.2"
## Author: 		"Brian Clapper, bmc@clapper.org"
## URL:			"http://www.clapper.org/software/python/munkres/"
## Copyright:	"(c) 2008 Brian M. Clapper"
## License:		"BSD-style license"

class Munkres:

	def __init__(self):
		'''Create a new instance'''
		self.C = None
		self.row_covered = []
		self.col_covered = []
		self.n = 0
		self.Z0_r = 0
		self.Z0_c = 0
		self.marked = None
		self.path = None

	def pad_matrix(self, matrix, pad_value=0):
		'''
		Pad a possibly non-square matrix to make it square.
		'''

		max_columns = 0
		total_rows = len(matrix)

		for row in matrix:
			max_columns = max(max_columns, len(row))

		total_rows = max(max_columns, total_rows)

		new_matrix = []
		for row in matrix:
			row_len = len(row)
			new_row = row[:]
			if total_rows > row_len:
				# Row too short. Pad it.
				new_row += [0] * (total_rows - row_len)
			new_matrix += [new_row]

		while len(new_matrix) < total_rows:
			new_matrix += [[0] * total_rows]

		return new_matrix

	def compute(self, cost_matrix):
		'''
		Compute the indexes for the lowest-cost pairings between rows and
		columns in the database. Returns a list of (row, column) tuples
		that can be used to traverse the matrix.

		:Parameters:
			cost_matrix : list of lists
				The cost matrix. If this cost matrix is not square, it
				will be padded with zeros, via a call to ``pad_matrix()``.
				(This method does *not* modify the caller's matrix. It
				operates on a copy of the matrix.)

				**WARNING**: This code handles square and rectangular
				matrices. It does *not* handle irregular matrices.

		:rtype: list
		:return: A list of ``(row, column)`` tuples that describe the lowest
				 cost path through the matrix
		'''

		self.C = self.pad_matrix(cost_matrix)
		self.n = len(self.C)
		self.original_length = len(cost_matrix)
		self.original_width = len(cost_matrix[0])
		self.row_covered = [False for i in range(self.n)]
		self.col_covered = [False for i in range(self.n)]
		self.Z0_r = 0
		self.Z0_c = 0
		self.path = self.__make_matrix(self.n * 2, 0)
		self.marked = self.__make_matrix(self.n, 0)

		done = False
		step = 1

		steps = { 1 : self.__step1,
				  2 : self.__step2,
				  3 : self.__step3,
				  4 : self.__step4,
				  5 : self.__step5,
				  6 : self.__step6 }

		while not done:
			try:
				func = steps[step]
				step = func()
			except KeyError:
				done = True

		# Look for the starred columns
		results = []
		for i in range(self.original_length):
			for j in range(self.original_width):
				if self.marked[i][j] == 1:
					results += [(i, j)]

		return results

	def __copy_matrix(self, matrix):
		'''Return an exact copy of the supplied matrix'''
		return copy.deepcopy(matrix)

	def __make_matrix(self, n, val):
		'''Create an *n*x*n* matrix, populating it with the specific value.'''
		matrix = []
		for i in range(n):
			matrix += [[val for j in range(n)]]
		return matrix

	def __step1(self):
		'''
		For each row of the matrix, find the smallest element and
		subtract it from every element in its row. Go to Step 2.
		'''
		C = self.C
		n = self.n
		for i in range(n):
			minval = min(self.C[i])
			# Find the minimum value for this row and subtract that minimum
			# from every element in the row.
			for j in range(n):
				self.C[i][j] -= minval

		return 2

	def __step2(self):
		'''
		Find a zero (Z) in the resulting matrix. If there is no starred
		zero in its row or column, star Z. Repeat for each element in the
		matrix. Go to Step 3.
		'''
		n = self.n
		for i in range(n):
			for j in range(n):
				if (self.C[i][j] == 0) and \
				   (not self.col_covered[j]) and \
				   (not self.row_covered[i]):
					self.marked[i][j] = 1
					self.col_covered[j] = True
					self.row_covered[i] = True

		self.__clear_covers()
		return 3

	def __step3(self):
		'''
		Cover each column containing a starred zero. If K columns are
		covered, the starred zeros describe a complete set of unique
		assignments. In this case, Go to DONE, otherwise, Go to Step 4.
		'''
		n = self.n
		count = 0
		for i in range(n):
			for j in range(n):
				if self.marked[i][j] == 1:
					self.col_covered[j] = True
					count += 1

		if count >= n:
			step = 7 # done
		else:
			step = 4

		return step

	def __step4(self):
		'''
		Find a noncovered zero and prime it. If there is no starred zero
		in the row containing this primed zero, Go to Step 5. Otherwise,
		cover this row and uncover the column containing the starred
		zero. Continue in this manner until there are no uncovered zeros
		left. Save the smallest uncovered value and Go to Step 6.
		'''
		step = 0
		done = False
		row = -1
		col = -1
		star_col = -1
		while not done:
			(row, col) = self.__find_a_zero()
			if row < 0:
				done = True
				step = 6
			else:
				self.marked[row][col] = 2
				star_col = self.__find_star_in_row(row)
				if star_col >= 0:
					col = star_col
					self.row_covered[row] = True
					self.col_covered[col] = False
				else:
					done = True
					self.Z0_r = row
					self.Z0_c = col
					step = 5

		return step

	def __step5(self):
		'''
		Construct a series of alternating primed and starred zeros as
		follows. Let Z0 represent the uncovered primed zero found in Step 4.
		Let Z1 denote the starred zero in the column of Z0 (if any).
		Let Z2 denote the primed zero in the row of Z1 (there will always
		be one). Continue until the series terminates at a primed zero
		that has no starred zero in its column. Unstar each starred zero
		of the series, star each primed zero of the series, erase all
		primes and uncover every line in the matrix. Return to Step 3
		'''
		count = 0
		path = self.path
		path[count][0] = self.Z0_r
		path[count][1] = self.Z0_c
		done = False
		while not done:
			row = self.__find_star_in_col(path[count][1])
			if row >= 0:
				count += 1
				path[count][0] = row
				path[count][1] = path[count-1][1]
			else:
				done = True

			if not done:
				col = self.__find_prime_in_row(path[count][0])
				count += 1
				path[count][0] = path[count-1][0]
				path[count][1] = col

		self.__convert_path(path, count)
		self.__clear_covers()
		self.__erase_primes()
		return 3

	def __step6(self):
		'''
		Add the value found in Step 4 to every element of each covered
		row, and subtract it from every element of each uncovered column.
		Return to Step 4 without altering any stars, primes, or covered
		lines.
		'''
		minval = self.__find_smallest()
		for i in range(self.n):
			for j in range(self.n):
				if self.row_covered[i]:
					self.C[i][j] += minval
				if not self.col_covered[j]:
					self.C[i][j] -= minval
		return 4

	def __find_smallest(self):
		'''Find the smallest uncovered value in the matrix.'''
		minval = sys.maxint
		for i in range(self.n):
			for j in range(self.n):
				if (not self.row_covered[i]) and (not self.col_covered[j]):
					if minval > self.C[i][j]:
						minval = self.C[i][j]
		return minval

	def __find_a_zero(self):
		'''Find the first uncovered element with value 0'''
		row = -1
		col = -1
		i = 0
		n = self.n
		done = False

		while not done:
			j = 0
			while True:
				if (self.C[i][j] == 0) and \
				   (not self.row_covered[i]) and \
				   (not self.col_covered[j]):
					row = i
					col = j
					done = True
				j += 1
				if j >= n:
					break
			i += 1
			if i >= n:
				done = True

		return (row, col)

	def __find_star_in_row(self, row):
		'''
		Find the first starred element in the specified row. Returns
		the column index, or -1 if no starred element was found.
		'''
		col = -1
		for j in range(self.n):
			if self.marked[row][j] == 1:
				col = j
				break

		return col

	def __find_star_in_col(self, col):
		'''
		Find the first starred element in the specified row. Returns
		the row index, or -1 if no starred element was found.
		'''
		row = -1
		for i in range(self.n):
			if self.marked[i][col] == 1:
				row = i
				break

		return row

	def __find_prime_in_row(self, row):
		'''
		Find the first prime element in the specified row. Returns
		the column index, or -1 if no starred element was found.
		'''
		col = -1
		for j in range(self.n):
			if self.marked[row][j] == 2:
				col = j
				break

		return col

	def __convert_path(self, path, count):
		for i in range(count+1):
			if self.marked[path[i][0]][path[i][1]] == 1:
				self.marked[path[i][0]][path[i][1]] = 0
			else:
				self.marked[path[i][0]][path[i][1]] = 1

	def __clear_covers(self):
		'''Clear all covered matrix cells'''
		for i in range(self.n):
			self.row_covered[i] = False
			self.col_covered[i] = False

	def __erase_primes(self):
		'''Erase all prime markings'''
		for i in range(self.n):
			for j in range(self.n):
				if self.marked[i][j] == 2:
					self.marked[i][j] = 0

# ---------------------------------------------------------------------------
# Munkres Helper Functions
# ---------------------------------------------------------------------------

def make_cost_matrix(profit_matrix, inversion_function):
	cost_matrix = []
	for row in profit_matrix:
		cost_matrix.append([inversion_function(value) for value in row])
	return cost_matrix