##############################################################################
## File: ErebusContinent.py version 2.57
## Author: Keith Sponburgh (Seven05) based on FaireWeather.py by Rich Marinaccio
## Copyright 2008 Rich Marinaccio
##############################################################################
##
## This map script is designed to simulate a single continental region, such as
## Europe or Africa rather than an entire global world.  The script attempts to
## generate a single primary landmass with a highly detailed coastline and
## features that are interesting and add a believable atmosphere to the game
## world.  Being a regional map, features such as wrapping are only partially
## supported, they work from a functional standpoint however the world isn't
## created with wrapping in mind so there may be anomolies near the world edges.
##
## The climate is also designed to simulate a single region rather than a global
## climate.  This means that while you can have a full range of tropical, arctic
## and temperate zones you will not have two arctic zones.  This is done so the
## climate zones can be larger and more detailed even with the reduced detail
## caused by the coarse resolution of Civ4's tile-based maps.
##
##############################################################################
## Version History
##
## 2.57 -   Fixed an error where the default option for Deserts, Jungles
##             and Taiga were using a High selection instead
##          Added an option for team start player distribution (MST)
##          Added a new selection for the Desert option: Minimal
##          Added two new selections for the Plains option: Low, Reduced
##
## 2.56 -   Fixed an error that could potentially overwite unique features when
##             ancient city ruins were enabled
##          Added support for IMPROVEMENT_CITY_RUINS_ANCIENT from RiFE
##          Added support for FEATURE_REEF and TERRAIN_OCEAN_DEEP from RiFE
##          Fix preventing Kelp from appearing in freshwater lakes
##          Tweaked Kelp rules, pushing it further away from cool water
##          Fixed 'detail map' used in randomizing high altitude areas, this
##             significantly reduces the chance for long, straight mountain ranges
##
## 2.55 -   Adjusted bonus values in starting plot finder so resources that can
##             be used right away are worth more.
##
## 2.54 -   Added multiplayer specific flavor settings for the Doviello and
##             Illians so they don't start so deep in the snow/tundra
##
## 2.53 -   Adjusted starting plot selection to work from a shuffled list to help
##             prevent the civs from clustering in the southeast corner
##
## 2.52 -   Removed previous change allowing coast tiles based on ocean depth,
##             and returned it to only place coast adjacent to land as that was
##             breaking game mechanics.  Will have to wait for somebody to add
##             a deep ocean texture to their mod (hint, hint)
##
## 2.51 -   Added support for Faerie civilization flavor
##          Fixed a minor indexing error in starting code selection
##
## 2.50 -   Added pre-placed ruins and roads`
##          Added pre-placed haunted lands
##          Re-wrote starting plot selection (Faster and better)
##          Moved parts of the normilization code to get around FalvourMod's
##             DLL changes that disables them
##
## 2.45 -   Test Release
##          Adjusted civ preference weights for coast, ocean and rivers
##          Fixed error with marsh placement
##          Increased number of plots available for start plot selection
##          Add test again plot value for second try when placing civs
##
## 2.44 -   Test release
##          Added 'Smart Climate' options
##          Optimized some code, thanks odalrick!
##
## 2.43 -   Test release for RifE mod civ preferences
##          Added tuning variables for kelp
##          Added second pass in starting plot sleection for picky civs
##
## 2.42 -   Test release for RifE mod kelp feature
##          Adjusted the method for handling underwater terrain altitudes
##          Added slight altitude boost based on distance from center to
##             help compensate for meteor/fissure passes breaking up maps
##
## 2.41 -   Added check to prevent starting plots on peaks even in mods where
##             peaks have a commerce, production or food value above zero.
##          Added safety code to eliminate peaks at the starting plot.
##          Fixed logic error with bonuses limited to a single area
##
## 2.40 -   Added map option to turn the advanced generation on and off
##          Fixed a bug in the 2.30 bonus placement code
##
## 2.30 -   Disabled default Civ4 peak normilization (Thanks Cephalo!)
##          Added 'meteor' passes, before and after tectonics
##          Added 'volcano' pass during tectonics
##          Increased base desert & plain amounts
##          Added custom bonus placement
##
## 2.20 -   Added map option to control plains
##          Added map option to control forest density
##          Adjusted land:water ratio, better fits the default number of civs
##
## 2.10 -	Added map options for controling rivers/lakes
##			Renamed options, hopefully more clear now
##			Added support for Flavour Mod features (outdated?)
##
## 2.00 -	New starting plot code, more emphasis on civ prefernces
##			New preference for neighbor likelyhood added to civ prefs
##			Updated river code based on PerfectWorld2.py by Cephalo
##			Added erosion pass for high rainfall areas to smooth the map
##			Added erosion pass to very low rainfall areas to smooth the map
##			Re-worked detail pass to enhance mountain ranges and coastlines
##			Added new rules for clearing the start plots of 'bad' features
##
## 1.70 -	Replaced code to add bonus resources to start plots
##			Tundra/snow on y-wrap maps will gravitate towards the middle (e-w)
##			Forest and Jungle thinning variable added to map constants
##			Snowy evergreen trees only generated on tundra & snow terrain
##			Changed method of clearing jungles and forests around start plots
##
## 1.61 -	Oops, I was skipping the entire check for starting plot distance
##
## 1.60 -	Improved starting plot selection based on FfH rules
##			Added flavor start rules for civs that have specific requirements
##				or abilities (e.g. Lanun forced to have a coastal start)
##
## 1.51 -	Test version of modified starting plot selection
##
## 1.50 -	Increased number of variations for jungle, tundra and desert options
##			Changed ice placement for y-wrap, depending on x position as well
##				with more ice in the center(x) and less at the edges(x).
##			Minor adjustment to detail overlay map to allow hills to turn into
##				peaks at high altitude prior to peak reduction to prevent
##				creating more isolated areas.
##			Plot generation 'post processing' can remove more hills at lower
##				altitudes.
##			Reduced the density of jungles and forests slightly
##			Adjusted base heightmap size to accept larger worlds (Thanks Cephalo)
##
## 1.40 -	Added Option to start all player units on the same tile
##			Moved separation to map edge for worlds with wrap enabled
##			Polar ice allowed on y-wrap maps, sparse enough to pass though
##			Increased chance of forcing coastal peaks to hills
##
## 1.30 -	Added sea level support
##			Added 'tiny islands' (more on lower cohesion maps)
##			Clamped lake size to sea level, only fresh water at low sea level
##			Reduced latitude range for maps with Y wrap enabled
##
## 1.20 -	Added world wrap (x, y and both)
##			Re-enabled default food bonus normilization for start plots
##			Added function to remove forest & jungles on start plots
##			Changed 'landform' function to 'Cohesion' and re-worked the method
##				of dispersing land to creat islands and smaller landmasses
##			Fine-tuned the climate adjustments for better results
##
## 1.10 -	Added Ice Feature
##			Added 'Mountain' map option to control how rough the map is
##			Added 'Desert' option to control desert frequency
##			Added 'Tundra' option to control tundra & snow frequency
##			Added 'Jungle' option to control jungle frequency
##			Changed the detail map overlay, improved hill density
##
## 1.00 -	Initial Release
##############################################################################

from CvPythonExtensions import *
import CvUtil
import CvMapGeneratorUtil

from array import array
from random import random,randint,seed
import math
import sys
import time
import operator

import MapScriptTools as mst

def beforeGeneration():
	mst.getModInfo()

class MapConstants :
	def __init__(self):
		return
	def initialize(self):
##############################################################################
## GLOBAL TUNING VARIABLES: Change these to customize the map results

		#Percent of land vs. water
		self.landPercent = 0.27

		#Maximum lake size for river generation lake growth, larger lakes are
		#possible if multiple lakes grow near each other and merge.
		self.maxLakeSize = 9

		#Tiny islands created after heightmap generation
		self.tinyIslandCount = 5

		#This is the chance a tile will have a jungle when it has enough rain
		#and a high enough temperature.  Lower numbers result in 'thinner'
		#jungle regions
		self.jungleChance = 0.85

		#This is the chance a tile will have a forest when it has enough rain.
		#Lower numbers result in 'thinner' forests
		self.forestChance = 0.50

		#These two settings control kelp placement (if support by the mod).  The
		#chance value is a final chance modifier, so at 1.0 it will use the base
		#temperature values.  Use kelpChance to thin out the kelp if it's too thick
		#or thicken it if it's too thin.  The kelpTemp value is a modifier of the
		#current map's tundra temperature so at 1.0 it will use the tundra temp.
		#Increasing this will push kelp further away from the cold zones.
		self.kelpChance = 0.66
		self.kelpTemp = 1.25

		#This control the maximum sea depth where kelp is allowed.  This is a
		#percentage of the total depth of the water which is a range from 0.0 up
		#to the sea level (which is variable).  So a value of 0.75 will allow
		#kelp in the upper 25% of the ocean depths.
		self.kelpDepth = 0.75

		#How many map squares will be above peak threshold and thus 'peaks'.
		self.PeakPercent = 0.04

		#How many map squares will be above hill threshold and thus 'hills' unless
		#they are also above peak threshold in which case they will be 'peaks'.
		#Only affects initial hill placement after tectonics, higher values here will
		#result in 'thicker' hills near plate boundries.
		self.HillPercent = 0.14

		#In addition to the relative peak and hill generation, there is also a
		#process that changes flats to hills or peaks based on altitude. This tends
		#to randomize the high altitude areas somewhat and improve their appearance.
		#These variables control the frequency of hills and peaks at the highest altitude.
		self.HillChanceAtOne = .08
		self.PeakChanceAtOne = .01

		#How many map squares will be below desert rainfall threshold. In this case,
		#rain levels close to zero are very likely to be desert, while rain levels close
		#to the desert threshold will more likely be plains.
		self.DesertPercent = 0.10

		#How many map squares will be below plains rainfall threshold. Rain levels close
		#to the desert threshold are likely to be plains, while those close to the plains
		#threshold are likely to be grassland.
		self.PlainsPercent = 0.25

		#How many map squares will be below grass rainfall threshold. Rain levels close
		#to the plains threshold are likely to be grass, while those close to the grass
		#threshold are likely to be marsh. Any rain above grass threshold will be
		#temperature tested for marsh.
		self.GrassPercent = 0.64

		#---The following variables are not based on percentages. Because temperature
		#---is so strongly tied to latitude, using percentages for things like ice and
		#---tundra leads to very strange results if most of the worlds land lies near
		#---the equator

		#What temperature will be considered cold enough to be ice. Temperatures range
		#from coldest 0.0 to hottest 1.0.
		self.TundraTemp = .30

		#What temperature will be considered cold enough to be tundra. Temperatures range
		#from coldest 0.0 to hottest 1.0.
		self.TaigaTemp = .40

		#Hotter than this temperature will be considered deciduous forest, colder will
		#be evergreen forest.Temperatures range from coldest 0.0 to hottest 1.0.
		self.ForestTemp = .60

		#High temps will be more likely to allow marsh, while temps at MinMarshTemp
		#will have no likelyhood of allowing marsh.
		self.MinMarshTemp = .80

		#When there is enough rain to create marsh, there is only a chance to create a
		#marsh based on temperature. At this temperature a marsh will always be created
		#on flat land when there is enough rain.
		#Even above this temperature there is a 66% chance the tile will NOT be a marsh
		#since marshes are inhospitable terrain in Fall From Heaven.
		self.alwaysMarshTemp = 0.95

		#What temperature will be considered hot enough to be jungle. Temperatures range
		#from coldest 0.0 to hottest 1.0.
		self.JungleTemp = .85

		#This is the chance for light forest to exist on plains or grassland.
		self.chanceForLightForest = 0.05

		#Marsh appears where there is the most rainfall, which is also where there
		#are the most trees. Since marsh looks good without trees, it should
		#sometimes not have them.
		self.chanceForTreelessMarsh = 0.50

		#How many squares are added to a lake for each unit of drainage flowing
		#into it.
		self.LakeSizePerDrainage = 14.0

		#This value modifies LakeSizePerRiverLength when a lake begins in desert
		self.DesertLakeModifier = .33

		#This value controls the amount of siltification in lakes
		self.maxSiltPanSize = 200

		#This value controls the number of mid-altitude lake depressions per
		#map square. It will become a lake if enough water flows into the
		#depression.
		self.numberOfLakesPerPlot = 0.002

		#This value sets the minimum altitude of lake depressions. They
		#generally look better higher up.
		self.minLakeAltitude = 0.40

		#This value is used to decide if enough water has accumulated to form a river.
		#A lower value creates more rivers over the entire map.
		self.RiverThreshold = 6.0

		#Modifier for city plot boosting function, a lower value results in fewer added
		#bonuses during normilization. Values greater than 0.5 will use region value,
		#0.5 and below will only evaluate the starting plot city radius. 0.0 will not
		#apply any normilization
		self.cityBoostPercent = 0.75

		#Degrees lattitude for the top and bottom of the map. This allows
		#for more specific climate zones
		#The are actually backwards, the 'topLattitude' is the bottom of the map in
		#game.  The default settings here puts snow & tundra in the north and jungles
		#in the south.
		self.topLattitude = -10
		self.bottomLattitude = 90

		########################################################################
		#The following wind zone settings are ignored at this time since the map
		#script has been changed to simulate a single continent it uses one wind
		#zone.  I left these in place to allow for future fine tuning.

		#Horse lattitudes and polar fronts plus and minus in case you
		#want some zones to be compressed or emphasized.
		self.horseLattitude = 25
		self.polarFrontLattitude = 40

		#Tropics of Cancer and Capricorn plus and minus respectively
		self.tropicsLattitude = 20
		########################################################################

		#Oceans are slow to gain and lose heat, so the max and min temps
		#are reduced and raised by this much.
		self.oceanTempClamp = .10

		#Minimum amount of rain dropped by default before other factors
		#add to the amount of rain dropped
		self.minimumRainCost = 0.01

		#Strength of geostrophic rainfall versus monsoon rainfall
		self.geostrophicFactor = 2.0

		#Height and Width of main climate and height maps. This does not
		#reflect the resulting map size. Both dimensions( + 1 if wrapping in
		#that dimension = False) must be evenly divisble by self.hmMaxGrain
		self.hmWidth = 193
		self.hmHeight = 145

		#Controls wrapping (not sure if this makes sense yet)
		self.WrapX = False
		self.WrapY = False

		#Cheap hack, testing forced margins on wrap enabled worlds
		self.FinalWrapX = False
		self.FinalWrapY = False

		#Size of largest map increment to begin midpoint displacement. Must
		#be a power of 2.
		self.hmMaxGrain = 16

		#Option to divide map into two continents as far as the midpoint
		#displacement is concerned. For guaranteed continent separation, further
		#steps will be needed but this option will cause more ocean in the
		#middle of the map. The possible choices are 0 = NO_SEPARATION,
		#1 = NORTH_SOUTH_SEPARATION and 2 = EAST_WEST_SEPARATION.
		self.hmSeparation = 0

		#If you sink the margins all the way to 0.0, they become too obvious.
		#This variable sets the maximum amount of sinking
		self.hmMarginDepth = 0.35

		#Margin of ocean around map edge when not wrapping and also through
		#middle when using separation.
		self.hmGrainMargin = 1.6

		#These are not mountain peaks, but points on the height map initialized
		#to 1.0 before the midpoint displacement process begins. This sets the
		#percentage of 'peaks' for points that are not on the grain margin.
		self.hmInitialPeakPercent = 0.10

		#Scales the heuristic for random midpoint displacement. A higher number
		#will create more noise(bumpy), a smaller number will make less
		#noise(smooth).
		self.hmNoiseLevel = 1.0

		#Number of tectonic plates
		self.hmNumberOfPlates = int(float(self.hmWidth * self.hmHeight) * 0.0016)

		#Influence of the plate map, or how much of it is added to the height map.
		self.plateMapScale = 2.50

		#Minimun distance from one plate seed to another
		self.minSeedRange = 10

		#Minimum distance from a plate seed to edge of map
		self.minEdgeRange = 5

		#Chance for plates to grow. Higher chance tends to make more regular
		#shapes. Lower chance makes more irregular shapes and takes longer.
		self.plateGrowthChanceX = 0.40
		self.plateGrowthChanceY = 0.40

		#This sets the amount that tectonic plates differ in altitude.
		self.plateStagger = 0.15

		#This sets the max amount a plate can be staggered up to on the heightmap
		self.plateStaggerRange = 1.0

		#This is the frequency of the cosine ripple near plate boundaries.
		self.rippleFrequency = 1.5

		#This is the amplitude of the ripples near plate boundaries.
		self.rippleAmplitude = 0.75

		#Filter size for temperature smoothing. Must be odd number
		self.filterSize = 7

		#Filter size for altitude smoothing and distance finding. Must be
		#odd number
		self.distanceFilterSize = 9

		#It is necessary to eliminate small inland lakes during the initial
		#heightmap generation. Keep in mind this number is in relation to
		#the initial large heightmap (mc.hmWidth, mc.hmHeight) before the
		#shrinking process
		self.minInlandSeaSize = 100

		#After generating the heightmap, bands of ocean can be added to the map
		#to allow a more consistent climate generation. These bands are useful
		#if you are generating part of a world where the weather might be coming
		#in from off the map. These bands can be kept if needed or cropped off
		#later in the process.
		self.northWaterBand = 2
		self.southWaterBand = 2
		self.eastWaterBand = 30
		self.westWaterBand = 30

		#These variables are intended for use with the above water band variables
		#but you can crop the map edge after climate generation for any reason.
		self.northCrop = 2
		self.southCrop = 2
		self.eastCrop = 30
		self.westCrop = 30

		#Decides whether to use the Python random generator or the one that is
		#intended for use with civ maps. The Python random has much higher precision
		#than the civ one. 53 bits for Python result versus 16 for getMapRand. The
		#rand they use is actually 32 bits, but they shorten the result to 16 bits.
		#However, the problem with using the Python random is that it may create
		#syncing issues for multi-player now or in the future, therefore it must
		#be optional.
		self.UsePythonRandom = True

		#The default spread out units doesn't always work well, this allows the
		#players atrting units to all be on the same tile like it does for the
		#AI players.
		self.HumansOnSameTile = False

		#Use 'advanced' creation routines
		self.UseAdvancedFeatures = False

		#Below here are static defines. If you change these, the map won't work.
		#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		self.L = 0
		self.N = 1
		self.S = 2
		self.E = 3
		self.W = 4
		self.NE = 5
		self.NW = 6
		self.SE = 7
		self.SW = 8

		self.NO_SEPARATION = 0
		self.NORTH_SOUTH_SEPARATION = 1
		self.EAST_WEST_SEPARATION = 2

		self.width = 70
		self.height = 70

		self.OCEAN = 0
		self.LAND = 1
		self.HILLS = 2
		self.PEAK = 3

		self.OCEAN = 0
		self.COAST = 1
		self.MARSH = 2
		self.GRASS = 3
		self.PLAINS = 4
		self.DESERT = 5
		self.TAIGA = 6
		self.TUNDRA = 7
		self.DEEPOCEAN = 8

		return

	def initInGameOptions(self):
		gc = CyGlobalContext()
		mmap = gc.getMap()


		if mmap.getCustomMapOption(11) > 0:
			print "Smart Climate On"
			civPreferenceList = GetCivPreferences()
			jungleNeeded = False
			desertNeeded = False
			taigaNeeded = False
			jungleValue = 0.00
			desertValue = 0.00
			taigaValue = 0.00
			players = 0.00
			for playerIndex in range(gc.getMAX_CIV_PLAYERS()):
				player = gc.getPlayer(playerIndex)

				if player.isEverAlive():
					if player.isEverAlive():
						civType = player.getCivilizationType()
						civInfo = gc.getCivilizationInfo(civType)
						players += 1.00

						for civPreference in civPreferenceList:
							if civPreference.civ == civType:
								civPref = civPreference
								if civPref.desertValue > 0:
									desertNeeded = True
									desertValue += 1.00
								if civPref.jungleValue > 0:
									jungleNeeded = True
									jungleValue += 1.00
								if civPref.taigaValue > 0:
									taigaNeeded = True
									taigaValue += 1.00
								break

			jungleWeight = 2.0 * (jungleValue/players)
			desertWeight = 2.0 * (desertValue/players)
			taigaWeight = 2.0 * (taigaValue/players)

			jungleMod = -2 + int(6 * jungleWeight + 0.5)
			desertMod = -2 + int(6 * desertWeight + 0.5)
			taigaMod = -2 + int(6 * taigaWeight + 0.5)

			print "Smart climate - %(c)2d Desert: %(d)4f %(m)2d" % {"c":desertValue,"d":desertWeight,"m":desertMod}
			print "Smart climate - %(c)2d Taiga: %(d)4f %(m)2d" % {"c":taigaValue,"d":taigaWeight,"m":taigaMod}
			print "Smart climate - %(c)2d Jungle: %(d)4f %(m)2d" % {"c":jungleValue,"d":jungleWeight,"m":jungleMod}

		seaLevel = CyMap().getSeaLevel()

		if seaLevel == GetInfoType("SEALEVEL_LOW"):
			mc.landPercent = 0.36
			mc.hmGrainMargin = 1.1
		elif seaLevel == GetInfoType("SEALEVEL_HIGH"):
			mc.landPercent = 0.22
			mc.hmGrainMargin = 2.20
			mc.kelpChance = 0.9

		#Cohesion
		selectionID = mmap.getCustomMapOption(0)
		if selectionID == 1: # Medium
			mc.maxLakeSize = 18
			mc.hmNumberOfPlates = int(float(self.hmWidth * self.hmHeight) * 0.0028)
			mc.minSeedRange = 6
			mc.plateGrowthChanceX = 0.25
			mc.plateGrowthChanceY = 0.35
			if seaLevel == GetInfoType("SEALEVEL_LOW"):
				mc.landPercent = 0.33
				mc.hmGrainMargin = 0.5
				mc.kelpChance = 1.0
			elif seaLevel == GetInfoType("SEALEVEL_HIGH"):
				mc.landPercent = 0.21
				mc.hmGrainMargin = 1.5
				mc.kelpChance = 0.8
			else:
				mc.landPercent = 0.27
				mc.hmGrainMargin = 0.75
				mc.kelpChance = 0.9
			mc.plateMapScale = 1.0
			mc.hmNoiseLevel *= 2.0
			mc.tinyIslandCount = 10
		if selectionID == 2: # Low
			mc.maxLakeSize = 27
			mc.hmMaxGrain = 8
			mc.hmNumberOfPlates = int(float(self.hmWidth * self.hmHeight) * 0.0032)
			mc.minSeedRange = 4
			mc.plateGrowthChanceX = 0.20
			mc.plateGrowthChanceY = 0.30
			if seaLevel == GetInfoType("SEALEVEL_LOW"):
				mc.landPercent = 0.29
				mc.hmGrainMargin = 0.25
				mc.kelpChance = 0.85
			elif seaLevel == GetInfoType("SEALEVEL_HIGH"):
				mc.landPercent = 0.19
				mc.hmGrainMargin = 0.75
				mc.kelpChance = 0.65
			else:
				mc.landPercent = 0.23
				mc.hmGrainMargin = 0.5
				mc.kelpChance = 0.75
			mc.plateMapScale = 1.0
			mc.hmNoiseLevel *= 3.0
			mc.tinyIslandCount = 20
		if selectionID == 3: # Mediterrenean
			mc.hmNumberOfPlates = int(float(self.hmWidth * self.hmHeight) * 0.0012)
			mc.minSeedRange = 8
			mc.plateGrowthChanceX = 0.5
			mc.plateGrowthChanceY = 0.5
			if seaLevel == GetInfoType("SEALEVEL_LOW"):
				mc.landPercent = 0.66
				mc.kelpChance = 0.85
			elif seaLevel == GetInfoType("SEALEVEL_HIGH"):
				mc.landPercent = 0.33
				mc.kelpChance = 0.65
			else:
				mc.landPercent = 0.50
				mc.kelpChance = 0.75
			mc.plateMapScale = 1.1

		#Mountains
		selectionID = mmap.getCustomMapOption(1)
		if selectionID == 1:
			mc.PeakPercent = 0.03
			mc.HillPercent = 0.10
			mc.PeakChanceAtOne = 0.01
			mc.HillChanceAtOne = 0.06
		elif selectionID == 2:
			mc.PeakPercent = 0.05
			mc.HillPercent = 0.18
			mc.PeakChanceAtOne = 0.05
			mc.HillChanceAtOne = 0.12

		#Desert
		selectionID = mmap.getCustomMapOption(2)
		if mmap.getCustomMapOption(11) == 2:
			if desertNeeded:
				mc.DesertPercent = 0.08 + (0.09 * desertWeight)
				mc.PlainsPercent = 0.24 + (0.09 * desertWeight)
				mc.GrassPercent = 0.66 - (0.07 * desertWeight)
			else:
				mc.DesertPercent = 0.00
				mc.PlainsPercent = 0.18
				mc.GrassPercent = 0.56
		else:
			if mmap.getCustomMapOption(11) == 3:
				selectionID += desertMod
			if selectionID < 1: # None
				if mmap.getCustomMapOption(11) > 0 and desertNeeded:
					mc.DesertPercent = 0.05
					mc.PlainsPercent = 0.21
					mc.GrassPercent = 0.71
				else:
					mc.DesertPercent = 0.00
					mc.PlainsPercent = 0.18
					mc.GrassPercent = 0.56
			elif selectionID == 1: # Minimal
				mc.DesertPercent = 0.02
				mc.PlainsPercent = 0.21
				mc.GrassPercent = 0.74
			elif selectionID == 2: # Low
				mc.DesertPercent = 0.05
				mc.PlainsPercent = 0.21
				mc.GrassPercent = 0.71
			elif selectionID == 3: # Reduced
				mc.DesertPercent = 0.08
				mc.PlainsPercent = 0.24
				mc.GrassPercent = 0.66
			elif selectionID == 5: # Increased
				mc.DesertPercent = 0.12
				mc.PlainsPercent = 0.28
				mc.GrassPercent = 0.62
			elif selectionID == 6: # High
				mc.DesertPercent = 0.17
				mc.PlainsPercent = 0.33
				mc.GrassPercent = 0.59

		#Taiga
		selectionID = mmap.getCustomMapOption(3)
		if mmap.getCustomMapOption(11) == 2:
			if taigaNeeded:
				mc.TundraTemp = 0.25 + (0.15 * taigaWeight)
				mc.TaigaTemp = 0.35 + (0.15 * taigaWeight)
			else:
				mc.TundraTemp = 0.0
				mc.TaigaTemp = 0.0
		else:
			if mmap.getCustomMapOption(11) == 3:
				selectionID += taigaMod
			if selectionID < 1: # None
				if mmap.getCustomMapOption(11) > 0 and taigaNeeded:
					mc.TundraTemp = 0.25
					mc.TaigaTemp = 0.35
				else:
					mc.TundraTemp = 0.0
					mc.TaigaTemp = 0.0
			elif selectionID == 1: # Minimal
				mc.TundraTemp = 0.20
				mc.TaigaTemp = 0.30
			elif selectionID == 2: # Reduced
				mc.TundraTemp = 0.25
				mc.TaigaTemp = 0.35
			elif selectionID == 4: # Increased
				mc.TundraTemp = 0.35
				mc.TaigaTemp = 0.45
			elif selectionID == 5: # Massive
				mc.TundraTemp = 0.40
				mc.TaigaTemp = 0.50

		#Jungle
		selectionID = mmap.getCustomMapOption(5)
		if mmap.getCustomMapOption(11) == 2:
			if jungleNeeded:
				mc.JungleTemp = 0.90 - (0.10 * jungleWeight)
				mc.alwaysMarshTemp = 0.95 - (0.10 * jungleWeight)
				mc.MinMarshTemp = 0.85 - (0.10 * jungleWeight)
				mc.jungleChance = 0.80 + (0.10 * jungleWeight)
			else:
				mc.JungleTemp = 2.0
				mc.alwaysMarshTemp = 2.0
				mc.MinMarshTemp = 2.0
		else:
			if mmap.getCustomMapOption(11) == 3:
				selectionID += jungleMod
			if selectionID < 1: # None
				if mmap.getCustomMapOption(11) > 0 and jungleNeeded:
					mc.JungleTemp = 0.90
					mc.alwaysMarshTemp = 0.95
					mc.MinMarshTemp = 0.85
					mc.jungleChance = 0.80
				else:
					mc.JungleTemp = 2.0
					mc.alwaysMarshTemp = 2.0
					mc.MinMarshTemp = 2.0
			elif selectionID == 1: # Minimal
				mc.JungleTemp = 0.95
				mc.alwaysMarshTemp = 1.0
				mc.MinMarshTemp = 0.90
				mc.jungleChance = 0.75
			elif selectionID == 2: # Reduced
				mc.JungleTemp = 0.90
				mc.alwaysMarshTemp = 0.95
				mc.MinMarshTemp = 0.85
				mc.jungleChance = 0.80
			elif selectionID == 4: # Increased
				mc.JungleTemp = 0.85
				mc.alwaysMarshTemp = 0.90
				mc.MinMarshTemp = 0.80
				mc.jungleChance = 0.85
			elif selectionID == 5: # Massive
				mc.JungleTemp = 0.80
				mc.alwaysMarshTemp = 0.85
				mc.MinMarshTemp = 0.75
				mc.jungleChance = 0.90

		#Forest Density
		selectionID = mmap.getCustomMapOption(6)
		if selectionID == 0: # Reduced
			mc.forestChance = 0.60
		elif selectionID == 1: # Default
			mc.forestChance = 0.70
		elif selectionID == 2: # Increased
			mc.forestChance = 0.80

		#Wrap
		selectionID = mmap.getCustomMapOption(7)
		if mmap.getCustomMapOption(0) == 3: #mediterenean, no wrap possible
			mc.eastWaterBand = 0
			mc.eastCrop = 0
			mc.westWaterBand = 0
			mc.westCrop = 0
			mc.northWaterBand = 0
			mc.northCrop = 0
			mc.southWaterBand = 0
			mc.southCrop = 0
			self.hmMaxGrain = 8
		elif selectionID == 1: # X
			mc.FinalWrapX = True
			mc.eastWaterBand = 0
			mc.eastCrop = 0
			mc.westWaterBand = 0
			mc.westCrop = 0
			self.hmMaxGrain = 8
		elif selectionID == 2: # Y
			mc.FinalWrapY = True
			mc.northWaterBand = 0
			mc.northCrop = 0
			mc.southWaterBand = 0
			mc.southCrop = 0
			mc.topLattitude = -85
			mc.bottomLattitude = 85
			mc.hmMaxGrain = 8
		elif selectionID == 3: # Both
			mc.FinalWrapX = True
			mc.eastWaterBand = 0
			mc.eastCrop = 0
			mc.westWaterBand = 0
			mc.westCrop = 0
			mc.FinalWrapY = True
			mc.northWaterBand = 0
			mc.northCrop = 0
			mc.southWaterBand = 0
			mc.southCrop = 0
			mc.topLattitude = -85
			mc.bottomLattitude = 85
			mc.hmMaxGrain = 8

		#Unit Placement
		selectionID = mmap.getCustomMapOption(8)
		if selectionID == 1: # Same tile
			mc.HumansOnSameTile = True

		#Rivers & lakes
		selectionID = mmap.getCustomMapOption(9)
		if selectionID == 0: # Reduced
			mc.RiverThreshold = 8.0
			mc.minLakeAltitude = 0.5
			mc.maxSiltPanSize = 250
		elif selectionID == 2: # Increased
			mc.RiverThreshold = 4.0
			mc.minLakeAltitude = 0.3
			mc.maxSiltPanSize = 150

		#Advanced terrain features
		selectionID = mmap.getCustomMapOption(10)
		if selectionID == 1: # On
			mc.UseAdvancedFeatures = True
		return

mc = MapConstants()

class PythonRandom :
	def __init__(self):
		return
	def seed(self):
		#Python randoms are not usable in network games.
		if mc.UsePythonRandom:
			self.usePR = True
		else:
			self.usePR = False
		if self.usePR and CyGame().isNetworkMultiPlayer():
			print "Detecting network game. Setting UsePythonRandom to False."
			self.usePR = False
		if self.usePR:
			# Python 'long' has unlimited precision, while the random generator
			# has 53 bits of precision, so I'm using a 53 bit integer to seed the map!
			seed() #Start with system time
			seedValue = randint(0,9007199254740991)
			seed(seedValue)
			print "Random seed (Using Python rands) for this map is %(s)20d" % {"s":seedValue}

##            seedValue = 5436076319370800
##            seed(seedValue)
##            print "Pre-set seed (Using Pyhon rands) for this map is %(s)20d" % {"s":seedValue}
		else:
			gc = CyGlobalContext()
			self.mapRand = gc.getGame().getMapRand()

			seedValue = self.mapRand.get(65535,"Seeding mapRand - FairWeather.py")
			self.mapRand.init(seedValue)
			print "Random seed (Using getMapRand) for this map is %(s)20d" % {"s":seedValue}

##            seedValue = 56870
##            self.mapRand.init(seedValue)
##            print "Pre-set seed (Using getMapRand) for this map is %(s)20d" % {"s":seedValue}
		return
	def random(self):
		if self.usePR:
			return random()
		else:
			#This formula is identical to the getFloat function in CvRandom. It
			#is not exposed to Python so I have to recreate it.
			fResult = float(self.mapRand.get(65535,"Getting float -FairWeather.py"))/float(65535)
#            print fResult
			return fResult
	def randint(self,rMin,rMax):
		#if rMin and rMax are the same, then return the only option
		if rMin == rMax:
			return rMin
		#returns a number between rMin and rMax inclusive
		if self.usePR:
			return randint(rMin,rMax)
		else:
			#mapRand.get() is not inclusive, so we must make it so
			return rMin + self.mapRand.get(rMax + 1 - rMin,"Getting a randint - FairWeather.py")
#Set up random number system for global access
PRand = PythonRandom()

################################################################################
## Global functions
################################################################################
#This function converts x and y to an index.
def GetIndex(x,y):
	#Check X for wrap
	if mc.WrapX:
		xx = x % mc.width
	elif x < 0 or x >= mc.width:
		return -1
	else:
		xx = x
	#Check y for wrap
	if mc.WrapY:
		yy = y % mc.height
	elif y < 0 or y >= mc.height:
		return -1
	else:
		yy = y

	i = yy * mc.width + xx
	return i

def GetHmIndex(x,y):
	#Check X for wrap
	if mc.WrapX:
		xx = x % mc.hmWidth
	elif x < 0 or x >= mc.hmWidth:
		return -1
	else:
		xx = x
	#Check y for wrap
	if mc.WrapY:
		yy = y % mc.hmHeight
	elif y < 0 or y >= mc.hmHeight:
		return -1
	else:
		yy = y

	i = yy * mc.hmWidth + xx
	return i

#Handles arbitrary size
def GetIndexGeneral(x,y,width,height):
	#Check X for wrap
	if mc.WrapX:
		xx = x % width
	elif x < 0 or x >= width:
		return -1
	else:
		xx = x
	#Check y for wrap
	if mc.WrapY:
		yy = y % height
	elif y < 0 or y >= height:
		return -1
	else:
		yy = y

	i = yy * width + xx
	return i

# #This function scales a float map so that all values are between
# #0.0 and 1.0.
def NormalizeMap(fMap,width,height):
	#find highest and lowest points
	maxAlt = 0.0
	minAlt = 0.0
	for i in range(height*width):
		minAlt = min(minAlt,fMap[i])
		maxAlt = max(maxAlt,fMap[i])
	#normalize map so that all altitudes are between 1 and 0
	#first add minAlt to all values if necessary
	if minAlt < 0.0:
		for i in range(height*width):
			fMap[i] -= minAlt
	#add minAlt to maxAlt also before scaling entire map
	maxAlt -= minAlt
	scaler = 1.0/maxAlt
	for i in range(height*width):
		fMap[i] = fMap[i] * scaler
	return

def ShrinkMap(largeMap,lWidth,lHeight,sWidth,sHeight):
	smallMap = array('d')
	yScale = float(lHeight)/float(sHeight)
	xScale = float(lWidth)/float(sWidth)
	for y in range(sHeight):
		for x in range(sWidth):
			weights = 0.0
			contributors = 0.0
			yyStart = int(y * yScale)
			yyStop = int((y + 1) * yScale)
			if yyStop < ((y + 1) * yScale):
				yyStop += 1
			for yy in range(yyStart,yyStop):
				xxStart = int(x * xScale)
				xxStop = int((x + 1) * xScale)
				if xxStop < ((x + 1) * xScale):
					xxStop += 1
				for xx in range(xxStart,xxStop):
					weight = GetWeight(x,y,xx,yy,xScale,yScale)
					i = yy * lWidth + xx
					contributor = largeMap[i]
					weights += weight
					contributors += weight * contributor
			smallMap.append(contributors/weights)
	return smallMap

def GetWeight(x,y,xx,yy,xScale,yScale):
	xWeight = 1.0
	if float(xx) < x * xScale:
		xWeight = 1.0 - ((x * xScale) - float(xx))
	elif float(xx + 1) > (x + 1) * xScale:
		xWeight = ((x + 1) * xScale) - float(xx)

	yWeight = 1.0
	if float(yy) < y * yScale:
		yWeight = 1.0 - ((y * yScale) - float(yy))
	elif float(yy + 1) > (y + 1) * yScale:
		yWeight = ((y + 1) * yScale) - float(yy)
	return xWeight * yWeight

def CenterWeight(x,y,width,height):
	# Returns 0.0 - 1.0, percent of max distance from map center
	x1 = float(min(x,width - x))
	y1 = float(min(y,height - y))
	xWeight = float(x1 / (width / 2))
	yWeight = float(y1 / (height / 2))
	weight = min(xWeight,yWeight)
	return weight

def EdgeWeight(x,y,width,height):
	# Returns 0.0 - 1.0, percent of distance from map edge
	x1 = float(min(x,width - x))
	y1 = float(min(y,height - y))
	xWeight = float(x1 / (width / 2))
	yWeight = float(y1 / (height / 2))
	weight = 1.0 - min(xWeight,yWeight)
	return weight

def CropMap(theMap):
	newMap = array('d')
	for y in range(mc.hmHeight):
		if y < mc.southCrop or y >= mc.hmHeight - mc.northCrop:
			continue
		for x in range(mc.hmWidth):
			if x < mc.westCrop or x >= mc.hmWidth - mc.eastCrop:
				continue
			i = GetHmIndex(x,y)
			newMap.append(theMap[i])
	return newMap

def AngleDifference(a1,a2):
	diff = a1 - a2
	while(diff < -180.0):
		diff += 360.0
	while(diff > 180.0):
		diff -= 360.0
	return diff

def ShuffleList(theList):
	return sorted( theList, key=lambda x: PRand.random() )

# def GetInfoType(string):
	# cgc = CyGlobalContext()
	# return cgc.getInfoTypeForString(string)
GetInfoType = CyGlobalContext().getInfoTypeForString

def GetDistance(x,y,dx,dy):
	return ( (x - dx)**2  + (y - dy)**2 )**.5

def GetOppositeDirection(direction):
	opposite = mc.L
	if direction == mc.N:
		opposite = mc.S
	elif direction == mc.S:
		opposite = mc.N
	elif direction == mc.E:
		opposite = mc.W
	elif direction == mc.W:
		opposite = mc.E
	elif direction == mc.NW:
		opposite = mc.SE
	elif direction == mc.SE:
		opposite = mc.NW
	elif direction == mc.SW:
		opposite = mc.NE
	elif direction == mc.NE:
		opposite = mc.SW
	return opposite

def GetXYFromDirection(x,y,direction, _DirectionCache={} ):
	if not _DirectionCache:
		_DirectionCache[mc.N] = ( 0, 1 )
		_DirectionCache[mc.S] = ( 0, -1 )
		_DirectionCache[mc.E] = ( 1, 0 )
		_DirectionCache[mc.W] = ( -1, 0 )
		_DirectionCache[mc.SE] = ( 1, -1 )
		_DirectionCache[mc.NW] = ( -1, 1 )
		_DirectionCache[mc.SW] = ( -1, -1 )
		_DirectionCache[mc.NE] = ( 1, 1 )
	dx, dy = _DirectionCache[direction]
	return ( x+dx, y+dy )

##This function is a general purpose value tuner. It finds a value that will be greater
##than or less than the desired percent of a whole map. Map values
##should be between 0 and 1.
def FindValueFromPercent(mmap,width,height,percent,tolerance,greaterThan=False):
	percentage = 100 * percent

	if greaterThan:
		percentage = 100 - percentage

	sortedSequence = sorted( mmap )
	return sortedSequence[ int(len(sortedSequence)*percentage//100) ]

def isWaterMatch(x,y):
	result = hm.isBelowSeaLevel(x,y)
	return result

def isCoast(plot):
	WaterArea = plot.waterArea()
	if not WaterArea.isNone():
		if not WaterArea.isLake():
			return True
	return False

class HeightMap :
	def __init__(self):
		return

	def generateHeightMap(self):
		self.heightMap = array('d')
		for i in range(mc.hmWidth * mc.hmHeight):
			self.heightMap.append(0.0)

		self.generateMidpointDisplacement()
		return

	def checkMaxGrain(self):
		#hm map dimensions(minus 1 if no wrapping) must be evenly divisible
		#by max grain
		ok = True
		# Doesn't like wrapping, so we force it :)
		width = mc.hmWidth - 1
		height = mc.hmHeight - 1
		if 0 != width % mc.hmMaxGrain:
			ok = False
		if 0 != height % mc.hmMaxGrain:
			ok = False

		if ok == False:
			raise ValueError, "height map dimesions not divisible by mc.hmMaxGrain. also check wrapping options"

		return

	def isPlotOnMargin(self,x,y):
		if mc.hmSeparation != mc.NO_SEPARATION:
			if mc.hmSeparation == mc.NORTH_SOUTH_SEPARATION:
				dimension = y
				middle = mc.hmHeight/2
			elif mc.hmSeparation == mc.EAST_WEST_SEPARATION:
				dimension = x
				middle = mc.hmWidth/2
			else:
				raise ValueError, "bad hmSeparation type"

			if dimension > middle - (mc.hmMaxGrain * mc.hmGrainMargin) \
			and dimension < middle + (mc.hmMaxGrain * mc.hmGrainMargin):
				return True

		if y < (mc.hmMaxGrain * mc.hmGrainMargin):
			return True
		if y > (mc.hmHeight - (mc.hmMaxGrain * mc.hmGrainMargin)):
			return True
		if x < (mc.hmMaxGrain * mc.hmGrainMargin):
			return True
		if x > (mc.hmWidth - (mc.hmMaxGrain * mc.hmGrainMargin)):
			return True
		return False

	def generateMidpointDisplacement(self):
		self.checkMaxGrain()

		gc = CyGlobalContext()
		mmap = gc.getMap()
		landformID = mmap.getCustomMapOption(0)

		#make list of map plots that aren't on margin for each
		#map quadrant. We want to place the initial peaks randomly, but we
		#also want to ensure fairly even distribution so that
		#not all the peaks are on one side of the map. For this purpose
		#we will treat each map quadrant separately.

		peaksNWList = list()
		peaksNEList = list()
		peaksSWList = list()
		peaksSEList = list()
		middleX = mc.hmWidth/2
		middleY = mc.hmHeight/2
		for y in range(0,mc.hmHeight,mc.hmMaxGrain):
			for x in range(0,mc.hmWidth,mc.hmMaxGrain):
				if not self.isPlotOnMargin(x,y):
					if x < middleX and y < middleY:
						peaksSWList.append((x,y))
					elif x >= middleX and y < middleY:
						peaksSEList.append((x,y))
					elif x < middleX and y >= middleY:
						peaksNWList.append((x,y))
					elif x >= middleX and y >= middleY:
						peaksNEList.append((x,y))
		#shuffle the lists
		peaksNWList = ShuffleList(peaksNWList)
		peaksNEList = ShuffleList(peaksNEList)
		peaksSWList = ShuffleList(peaksSWList)
		peaksSEList = ShuffleList(peaksSEList)

		#place desired number of peaks in each quadrant
		totalNonMargin = len(peaksNWList)
		totalNonMargin += len(peaksNEList)
		totalNonMargin += len(peaksSWList)
		totalNonMargin += len(peaksSEList)

		count = max(1,int(float(totalNonMargin) * mc.hmInitialPeakPercent * 0.25))
		print "peak count = %d" % (count)
		for n in range(count):
			x,y = peaksNWList[n]
			i = GetHmIndex(x,y)
			self.heightMap[i] = 1.0

			x,y = peaksNEList[n]
			i = GetHmIndex(x,y)
			self.heightMap[i] = 1.0

			x,y = peaksSWList[n]
			i = GetHmIndex(x,y)
			self.heightMap[i] = 1.0

			x,y = peaksSEList[n]
			i = GetHmIndex(x,y)
			self.heightMap[i] = 1.0

		if landformID == 3:
			for y in range(0,mc.hmHeight):
				for x in range(0,mc.hmWidth):
					weight = EdgeWeight(x,y,mc.hmWidth,mc.hmHeight)
					self.heightMap[i] += weight

			NormalizeMap(self.heightMap,mc.hmWidth,mc.hmHeight)

		#Now use a diamond-square algorithm(sort of) to generate the rest
		currentGrain = float(mc.hmMaxGrain)
		while currentGrain > 1.0:
			#h is scalar for random displacement
			h = (currentGrain/float(mc.hmMaxGrain)) * float(mc.hmNoiseLevel)
			#First do the 'square' pass
			for y in range(0,mc.hmHeight,int(currentGrain)):
				for x in range(0,mc.hmWidth,int(currentGrain)):
					#on the square pass, GetHmIndex should handle all wrapping needs
					topLeft = GetHmIndex(x,y)
					topRight = GetHmIndex(x + int(currentGrain),y)
					if topRight == -1:
						continue #this means no wrap in x direction
					bottomLeft = GetHmIndex(x,y + int(currentGrain))
					if bottomLeft == -1:
						continue #this means no wrap in y direction
					bottomRight = GetHmIndex(x + int(currentGrain),y + int(currentGrain))
					middle = GetHmIndex(x + int(currentGrain/2.0),y + int(currentGrain/2.0))
					average = (self.heightMap[topLeft] + self.heightMap[topRight] \
					+ self.heightMap[bottomLeft] + self.heightMap[bottomRight])/4.0
					displacement = h * PRand.random() - h/2.0
					self.heightMap[middle] = average + displacement
					#now add that heuristic to the four points to diminish
					#artifacts. We don't need this on the diamond pass I don't think
					displacement = h * PRand.random() - h/2.0
					self.heightMap[topLeft] += displacement
					displacement = h * PRand.random() - h/2.0
					self.heightMap[topRight] += displacement
					displacement = h * PRand.random() - h/2.0
					self.heightMap[bottomLeft] += displacement
					displacement = h * PRand.random() - h/2.0
					self.heightMap[bottomRight] += displacement
			#Now do the 'diamond' pass, there are two diamonds for each x.
			#Possible wrapping is a big complication on this pass. Sorry!
			for y in range(0,mc.hmHeight,int(currentGrain)):
				for x in range(0,mc.hmWidth,int(currentGrain)):
					#first do the right facing diamond
					left = GetHmIndex(x,y)
					right = GetHmIndex(x + int(currentGrain),y)
					if right != -1: #if we're off map at this point go to next diamond
						average = self.heightMap[left] + self.heightMap[right]
						contributers = 2 #each diamond may have two or three contributers, 2 so far
						top = GetHmIndex(x + int(currentGrain/2.0),y - int(currentGrain/2.0))
						if top != -1:
							contributers += 1
							average += self.heightMap[top]
						bottom = GetHmIndex(x + int(currentGrain/2.0),y + int(currentGrain/2.0))
						if bottom != -1:
							contributers += 1
							average += self.heightMap[bottom]
						average = average/float(contributers)
						middle = GetHmIndex(x + int(currentGrain/2.0),y)
						displacement = h * PRand.random() - h/2.0
						self.heightMap[middle] = average + displacement
					#now do the down facing diamond
					top = GetHmIndex(x,y)
					bottom = GetHmIndex(x,y + int(currentGrain))
					if bottom != -1:
						average = self.heightMap[top] + self.heightMap[bottom]
						contributers = 2
						right = GetHmIndex(x + int(currentGrain/2.0),y + int(currentGrain/2.0))
						if right != -1:
							contributers += 1
							average += self.heightMap[right]
						left = GetHmIndex(x - int(currentGrain/2.0),y + int(currentGrain/2.0))
						if left != -1:
							contributers += 1
							average += self.heightMap[left]
						average = average/float(contributers)
						middle = GetHmIndex(x,y + int(currentGrain/2.0))
						displacement = h * PRand.random() - h/2.0
						self.heightMap[middle] = average + displacement
			currentGrain = currentGrain/2.0

		NormalizeMap(self.heightMap,mc.hmWidth,mc.hmHeight)

		return

	def performTectonics(self):
		gc = CyGlobalContext()
		mmap = gc.getMap()
		landformID = mmap.getCustomMapOption(0) #1 is islands

		self.plateMap = list()
		self.detailPlateMap = list()
		borderMap = array('i')#this will help in later distance calculations
		detailBorderMap = array('i')
		self.plateHeightMap = array('d')
		self.detailPlateHeightMap = array('d')
		preSmoothMap = array('d')
		preSmoothDetailMap = array('d')
		growthPlotList = list()
		detailGrowthPlotList = list()
		plateList = list()
		detailPlateList = list()
		maxDistance = math.sqrt(pow(float(mc.distanceFilterSize/2),2) + pow(float(mc.distanceFilterSize/2),2))
		#initialize maps
		for i in range(mc.hmHeight*mc.hmWidth):
				self.plateMap.append(PlatePlot(0,maxDistance))
				borderMap.append(False)
				self.plateHeightMap.append(0.0)
				preSmoothMap.append(0.0)

				self.detailPlateMap.append(DetailPlatePlot(0,maxDistance))
				detailBorderMap.append(False)
				self.detailPlateHeightMap.append(0.0)
				preSmoothDetailMap.append(0.0)

		plateList.append(Plate(0,-1,-1))#zero placeholder (very silly I know)
		detailPlateList.append(DetailPlate(0,-1,-1))

		#seed plates
		firstPlate = False
		width = mc.hmWidth
		height = mc.hmHeight

		for i in range(1,mc.hmNumberOfPlates + 1):
			#first find a random seed point that is not blocked by
			#previous points
			iterations = 0
			while(True):
				iterations += 1
				if iterations > 10000:
					raise ValueError, "endless loop in region seed placement"

				seedX = PRand.randint(0,width + 1)
				seedY = PRand.randint(0,height + 1)

				n = GetHmIndex(seedX,seedY)
				if self.isSeedBlocked(plateList,seedX,seedY) == False:
					self.plateMap[n].plateID = i
					plate = Plate(i,seedX,seedY)
					plateList.append(plate)
					#Now fill a 3x3 area to insure a minimum region size
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(seedX,seedY,direction)
						nn = GetHmIndex(xx,yy)
						if nn != -1:
							self.plateMap[nn].plateID = i
							plot = (xx,yy,i)
							growthPlotList.append(plot)

					break

		for i in range(1,3 * mc.hmNumberOfPlates + 1):
			#first find a random seed point that is not blocked by
			#previous points
			iterations = 0
			while(True):
				iterations += 1
				if iterations > 10000:
					raise ValueError, "endless loop in region seed placement"

				seedX = PRand.randint(0,width + 1)
				seedY = PRand.randint(0,height + 1)

				n = GetHmIndex(seedX,seedY)
				if self.isSeedBlocked(detailPlateList,seedX,seedY) == False:
					self.detailPlateMap[n].plateID = i
					plate = DetailPlate(i,seedX,seedY)
					detailPlateList.append(plate)
					#Now fill a 3x3 area to insure a minimum region size
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(seedX,seedY,direction)
						nn = GetHmIndex(xx,yy)
						if nn != -1:
							self.detailPlateMap[nn].plateID = i
							plot = (xx,yy,i)
							detailGrowthPlotList.append(plot)

					break

		#Now cause the seeds to grow into plates
		iterations = 0
		while(len(growthPlotList) > 0):
			iterations += 1
			if iterations > 200000:
				self.printPlateMap(self.plateMap)
				print "length of growthPlotList = %d" % (len(growthPlotList))
				raise ValueError, "endless loop in plate growth"
			plot = growthPlotList[0]
			roomLeft = False
			for direction in range(1,5,1):
				x,y,plateID = plot
				i = GetHmIndex(x,y)
				xx,yy = GetXYFromDirection(x,y,direction)
				ii = GetHmIndex(xx,yy)
				if ii == -1:
					plateList[plateID].isOnMapEdge = True
					continue
				if self.plateMap[ii].plateID != plateID and self.plateMap[ii].plateID != 0:
					borderMap[i] = True
					borderMap[ii] = True
				elif self.plateMap[ii].plateID == 0:
					roomLeft = True
					if direction == mc.N or direction == mc.S:
						growthChance = mc.plateGrowthChanceY
					else:
						growthChance = mc.plateGrowthChanceX
					if PRand.random() < growthChance:
						self.plateMap[ii].plateID = plateID
						newPlot = (xx,yy,plateID)
						growthPlotList.append(newPlot)

			#move plot to the end of the list if room left, otherwise
			#delete it if no room left
			if roomLeft:
				growthPlotList.append(plot)
			del growthPlotList[0]

		iterations = 0
		while(len(detailGrowthPlotList) > 0):
			iterations += 1
			if iterations > 200000:
				print "length of detailGrowthPlotList = %d" % (len(detailGrowthPlotList))
				raise ValueError, "endless loop in detail plate growth"
			plot = detailGrowthPlotList[0]
			roomLeft = False
			for direction in range(1,5,1):
				x,y,plateID = plot
				i = GetHmIndex(x,y)
				xx,yy = GetXYFromDirection(x,y,direction)
				ii = GetHmIndex(xx,yy)
				if ii == -1:
					detailPlateList[plateID].isOnMapEdge = True
					continue
				if self.detailPlateMap[ii].plateID != plateID and self.detailPlateMap[ii].plateID != 0:
					detailBorderMap[i] = True
					detailBorderMap[ii] = True
				elif self.detailPlateMap[ii].plateID == 0:
					roomLeft = True
					if direction == mc.N or direction == mc.S:
						growthChance = min(mc.plateGrowthChanceY * 1.5, 0.75)
					else:
						growthChance = min(mc.plateGrowthChanceX * 1.5, 0.75)
					if PRand.random() < growthChance:
						self.detailPlateMap[ii].plateID = plateID
						newPlot = (xx,yy,plateID)
						detailGrowthPlotList.append(newPlot)

			#move plot to the end of the list if room left, otherwise
			#delete it if no room left
			if roomLeft:
				detailGrowthPlotList.append(plot)
			del detailGrowthPlotList[0]

		#Stagger the plates somewhat to add interest
		steps = int(mc.plateStaggerRange/mc.plateStagger)
		for i in range(0,width*height):
			if plateList[self.plateMap[i].plateID].isOnMapEdge:
				if landformID < 3:
					preSmoothMap[i] = 0.0
				else:
					preSmoothMap[i] = float(self.plateMap[i].plateID % steps) * mc.plateStagger * 1.5
			else:
				preSmoothMap[i] = float(self.plateMap[i].plateID % steps) * mc.plateStagger

			if detailPlateList[self.detailPlateMap[i].plateID].isOnMapEdge:
				if landformID < 3:
					preSmoothMap[i] = 0.0
				else:
					preSmoothMap[i] = float(self.plateMap[i].plateID % steps) * mc.plateStagger * 1.5
			else:
				preSmoothDetailMap[i] = float(self.detailPlateMap[i].plateID % steps) * mc.plateStagger

		#Now smooth the plate height map and create the distance map at the same time
		#Since the algorithm is the same
		for y in range(0,height):
			for x in range(0,width):
				contributers = 0
				avg = 0
				detailAvg = 0
				weight = 0
				i = GetHmIndex(x,y)
				isBorder = False
				isDetailBorder = False

				if borderMap[i]:
					isBorder = True
				if detailBorderMap[i]:
					isDetailBorder = True

				plateID = self.plateMap[i].plateID
				detailPlateID = self.detailPlateMap[i].plateID
				for yy in range(y - mc.distanceFilterSize/2,y + mc.distanceFilterSize/2 + 1,1):
					for xx in range(x - mc.distanceFilterSize/2,x + mc.distanceFilterSize/2 + 1,1):
						ii = GetHmIndex(xx,yy)
						if landformID < 2:
							weight = CenterWeight(xx,yy,width,height) * 0.33
						if ii == -1:
							continue
						contributers += 1
						avg += preSmoothMap[ii] + weight
						detailAvg += preSmoothDetailMap[ii] + weight
						if isBorder and plateID != self.plateMap[ii].plateID:
							distance = math.sqrt(pow(float(y - yy),2) + pow(float(x - xx),2))
							if distance < self.plateMap[ii].distanceList[plateID]:
								self.plateMap[ii].distanceList[plateID] = distance

						if isDetailBorder and detailPlateID != self.detailPlateMap[ii].plateID:
							distance = math.sqrt(pow(float(y - yy),2) + pow(float(x - xx),2))
							if distance < self.detailPlateMap[ii].distanceList[detailPlateID]:
								self.detailPlateMap[ii].distanceList[detailPlateID] = distance

				avg = avg/float(contributers)
				detailAvg = detailAvg/float(contributers)
				self.plateHeightMap[i] = avg
				self.detailPlateHeightMap[i] = detailAvg

		#Now add ripple formula
		for i in range(width*height):
			avgRippleTop = 0.0
			avgRippleBottom = 0.0
			for plateID in range(1,mc.hmNumberOfPlates + 1):
				distanceWeight = maxDistance - self.plateMap[i].distanceList[plateID]
				if plateList[plateID].seedX < plateList[self.plateMap[i].plateID].seedX:
					angleDifference = AngleDifference(plateList[self.plateMap[i].plateID].angle,plateList[plateID].angle)
				else:
					angleDifference = AngleDifference(plateList[plateID].angle,plateList[self.plateMap[i].plateID].angle)
				ripple = (pow(math.cos(mc.rippleFrequency * self.plateMap[i].distanceList[plateID]) * \
				(-self.plateMap[i].distanceList[plateID]/maxDistance + 1),2) + (-self.plateMap[i].distanceList[plateID]/maxDistance + 1)) \
				* mc.rippleAmplitude * math.sin(math.radians(angleDifference))
				avgRippleTop += (ripple * distanceWeight)
				avgRippleBottom += distanceWeight
			if avgRippleBottom == 0.0:
				avgRipple = 0.0
			else:
				avgRipple = avgRippleTop/avgRippleBottom
			self.plateHeightMap[i] += avgRipple - (avgRipple * PRand.random() * 1.2)

			minDistance = maxDistance
			for plateID in range(1,3 * mc.hmNumberOfPlates + 1):
				distance = maxDistance - min(maxDistance,self.detailPlateMap[i].distanceList[plateID])
				if distance < minDistance:
					minDistance = distance

			avgRipple = 1.0 - (minDistance / maxDistance)
			self.detailPlateHeightMap[i] += avgRipple * avgRipple

		NormalizeMap(self.plateHeightMap,mc.hmWidth,mc.hmHeight)
		NormalizeMap(self.detailPlateHeightMap,mc.hmWidth,mc.hmHeight)

		#Advanced feature - volcanos/fissures
		if mc.UseAdvancedFeatures:
			points = int(width * height * 0.1)
			quakeCount = 0
			quakeMax = max(1,int(height / 48))
			while points > 0:
				x = PRand.randint(int(width * 0.1), int(width * 0.9))
				y = PRand.randint(int(height * 0.1), int(height * 0.9))
				i = GetHmIndex(x,y)

				points -= 1
				size = 4
				featureType = 0 #Quake
				plateID = self.plateMap[i].plateID

				if borderMap[i]: # Only works on plate boundries
					if PRand.random() > 0.5 or quakeCount > quakeMax:
						featureType = 1 #Volcano
						size = 2
					for xx in range(x-size, x+size):
						for yy in range(y-size,y+size):
							ii = GetHmIndex(xx,yy)
							dist = GetDistance(x,y,xx,yy)

							if featureType == 1: #push the land up from the center point
								weight = 1.0 - float(dist / 2)
								adj = self.plateHeightMap[i] * weight
								if dist < 1:
									self.plateHeightMap[ii] += adj
								else:
									adj = abs(self.plateHeightMap[i] - self.plateHeightMap[ii])
									self.plateHeightMap[ii] += adj * weight
							else: #depress this plate, push adjacent ones up
								quakeCount += 1
								weight = 1.0 - float(dist / 2)
								adj = self.plateHeightMap[i] * weight
								if dist < 1:
									self.plateHeightMap[ii] -= adj * EdgeWeight(xx,yy,width,height)
								else:
									adj = abs(self.plateHeightMap[i] - self.plateHeightMap[ii])
									if self.plateMap[ii] == plateID:
										self.plateHeightMap[ii] -= adj * weight * EdgeWeight(xx,yy,width,height)
									else:
										self.plateHeightMap[ii] += adj * weight * CenterWeight(xx,yy,width,height)

			NormalizeMap(self.plateHeightMap,width,height)

	def combineMaps(self):
		gc = CyGlobalContext()
		mmap = gc.getMap()
		landformID = mmap.getCustomMapOption(0) #Cohesion = 0 high

		#Now add plateHeightMap to HeightMap
		#for i in range(mc.hmWidth * mc.hmHeight):
		for x in range(mc.hmWidth):
			for y in range(mc.hmHeight):
				i = y * mc.hmWidth + x
				detail = self.detailPlateHeightMap[i] * self.detailPlateHeightMap[i] * 0.5
				self.heightMap[i] += (detail + self.plateHeightMap[i]) * mc.plateMapScale

				if mc.UseAdvancedFeatures and landformID < 3:
					mod = landformID * 0.25 + 0.1
					offset = 1.0 - mod
					self.heightMap[i] += (PRand.random() * mod + offset) * CenterWeight(x,y,mc.hmWidth,mc.hmHeight) * offset * 0.25
				if landformID == 3:
					mod = 0.25
					offset = 0.75
					self.heightMap[i] -= (PRand.random() * mod + offset) * CenterWeight(x,y,mc.hmWidth,mc.hmHeight) * offset * 0.25
					self.heightMap[i] += (PRand.random() * mod + offset) * EdgeWeight(x,y,mc.hmWidth,mc.hmHeight) * offset * 0.25

		#depress margins, this time with brute force
		if landformID < 3:
			marginSize = mc.hmMaxGrain * mc.hmGrainMargin
			for y in range(mc.hmHeight):
				for x in range(mc.hmWidth):
					i = GetHmIndex(x,y)
					if mc.WrapX == False:
						if x < marginSize:
							self.heightMap[i] *= (float(x)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth

						elif mc.hmWidth - x < marginSize:
							self.heightMap[i] *= (float(mc.hmWidth - x)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth
					if mc.WrapY == False:
						if y < marginSize:
							self.heightMap[i] *= (float(y)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth

						elif mc.hmHeight - y < marginSize:
							self.heightMap[i] *= (float(mc.hmHeight - y)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth

					if mc.hmSeparation == mc.NORTH_SOUTH_SEPARATION:
						difference = abs((mc.hmHeight/2) - y)
						if difference < marginSize:
							self.heightMap[i] *= (float(difference)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth

					elif mc.hmSeparation == mc.EAST_WEST_SEPARATION:
						difference = abs((mc.hmWidth/2) - x)
						if difference < marginSize:
							self.heightMap[i] *= (float(difference)/float(marginSize)) * (1.0 - mc.hmMarginDepth) + mc.hmMarginDepth

		#Now lets square the heightmap to simulate erosion
#		for i in range(mc.hmWidth * mc.hmHeight):
#			self.heightMap[i] = self.heightMap[i] * self.heightMap[i]
		# NormalizeMap(self.heightMap,mc.hmWidth,mc.hmHeight)

		# seaLevel = FindValueFromPercent(self.heightMap,mc.hmWidth,mc.hmHeight,mc.landPercent,0.02,True)
		# velocity = list()
		# altitude = list()
		# for y in range(1, mc.hmHeight - 1):
			# for x in range(mc.hmWidth):
				# if y == 1:
					# velocity.append(1.0)
					# altitude.append(seaLevel)

				# middle = y * mc.hmWidth + x
				# below = (y - 1) * mc.hmWidth + x
				# above = (y + 1) * mc.hmWidth + x

				# if self.heightMap[middle] > seaLevel:
					# if self.heightMap[middle] > altitude[x]:
						# velocity[x] -= self.heightMap[middle] - altitude[x]
						# altitude[x] = self.heightMap[middle]
					# elif self.heightMap[middle] < altitude[x]:
						# velocity[x] +=  0.01
						# altitude[x] -= 0.001

					# if velocity[x] > 0.0:
						# diff = altitude[x] - self.heightMap[middle]
						# avg = (self.heightMap[middle] + self.heightMap[below] + self.heightMap[above]) / 3.0
						# adj = (self.heightMap[middle] - avg) * (max(0,velocity[x] - diff))
						# self.heightMap[middle] -= adj

		NormalizeMap(self.heightMap,mc.hmWidth,mc.hmHeight)

	def addWaterBands(self):
		#validate water bands. Maps that wrap cannot have one in that direction
		if mc.WrapX and (mc.eastWaterBand != 0 or mc.westWaterBand != 0):
			raise ValueError,"east/west water bands cannot be used when wrapping in X direction."
		if mc.WrapY and (mc.northWaterBand != 0 or mc.southWaterBand != 0):
			raise ValueError,"north/south water bands cannot be used when wrapping in Y direction."

		newWidth = mc.hmWidth + mc.eastWaterBand + mc.westWaterBand
		newHeight = mc.hmHeight + mc.northWaterBand + mc.southWaterBand
		newHeightMap = array('d')
		for y in range(newHeight):
			for x in range(newWidth):
				oldX = x - mc.westWaterBand
				oldY = y - mc.southWaterBand
#                i = GetIndexGeneral(x,y,newWidth,newHeight)
				ii = GetHmIndex(oldX,oldY)
				if ii == -1:
					newHeightMap.append(0.0)
				else:
					newHeightMap.append(self.heightMap[ii])

		mc.hmWidth = newWidth
		mc.hmHeight = newHeight
		self.heightMap = newHeightMap

	def calculateSeaLevel(self):
		self.seaLevel = FindValueFromPercent(self.heightMap,mc.hmWidth,mc.hmHeight,mc.landPercent,0.02,True)
		return

	def isBelowSeaLevel(self,x,y):
		i = GetHmIndex(x,y)
		if self.heightMap[i] < self.seaLevel:
			return True
		return False

	## This function returns altitude in relation to sea level with
	## 0.0 being seaLevel and 1.0 being highest altitude
	def getAltitudeAboveSeaLevel(self,x,y):
		i = GetHmIndex(x,y)
		if i == -1:
			return 0.0
		altitude = self.heightMap[i]
		if altitude < self.seaLevel:
			return 0.0
		altitude = 1.0/(1.0 - self.seaLevel) * (altitude - self.seaLevel)
		return altitude

	def isSeedBlocked(self,plateList,seedX,seedY):
		for plate in plateList:
			if seedX > plate.seedX - mc.minSeedRange and seedX < plate.seedX + mc.minSeedRange:
				if seedY > plate.seedY - mc.minSeedRange and seedY < plate.seedY + mc.minSeedRange:
					return True
		#Check for edge
		if seedX < mc.minEdgeRange or seedX >= (mc.hmWidth + 1) - mc.minEdgeRange:
			return True
		if seedY < mc.minEdgeRange or seedY >= (mc.hmHeight + 1) - mc.minEdgeRange:
			return True
		return False

	def GetInfluFromDistance(self,sinkValue,peakValue,searchRadius,distance):
		influence = peakValue
		maxDistance = math.sqrt(pow(float(searchRadius),2) + pow(float(searchRadius),2))
		#minDistance = 1.0
		influence -= ((peakValue - sinkValue)* (distance - 1.0))/(maxDistance - 1.0)
		return influence

	def FindDistanceToPlateBoundary(self,x,y,searchRadius):
		minDistance = 10.0
		i = self.GetIndex(x,y)
		for yy in range(y - searchRadius,y + searchRadius):
			for xx in range(x - searchRadius,x + searchRadius):
				ii = self.GetIndex(xx,yy)
				if self.plateMap[i] != self.plateMap[ii]:
					distance = math.sqrt(pow(float(xx-x),2) + pow(float(yy-y),2))
					if distance < minDistance:
						minDistance = distance

		if minDistance == 10.0:
			return 0.0

		return minDistance

	def fillInLakes(self):
		#smaller lakes need to be filled in for now. The river system will
		#most likely recreate them later due to drainage calculation
		#according to certain rules. This makes the lakes look much better
		#and more sensible.
		am = Areamap(mc.hmWidth,mc.hmHeight,True,True)
		am.defineAreas(isWaterMatch)
		oceanID = am.getOceanID()
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				if self.isBelowSeaLevel(x,y) and am.areaMap[i] != oceanID:
					#check the size of this body of water, if too small,
					#change to land
					for a in am.areaList:
						if a.ID == am.areaMap[i] and a.size < mc.minInlandSeaSize:
							self.heightMap[i] = self.seaLevel
		return

	def printInitialPeaks(self):
		lineString = "midpoint displacement peaks and margins"
		print lineString
		if not mc.WrapY:
			adjustedHeight = mc.hmHeight - 1
		else:
			adjustedHeight = mc.hmHeight - mc.hmMaxGrain
		for y in range(adjustedHeight,-1,-mc.hmMaxGrain):
			lineString = ""
			for x in range(0,mc.hmWidth,mc.hmMaxGrain):
				i = GetHmIndex(x,y)
				if self.isPlotOnMargin(x,y):
					lineString += "*"
				elif self.heightMap[i] == 1.0:
					lineString += "1"
				elif self.heightMap[i] == 0.0:
					lineString += "0"
			print lineString
		lineString = " "
		print lineString

	def printHeightMap(self):
		lineString = "Height Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int((self.heightMap[i] - self.seaLevel)/(1.0 - self.seaLevel) * 10)
				#mapLoc = int(self.heightMap[i] * 10)
				if self.heightMap[i] < self.seaLevel:
					lineString += '.'
				else:
					lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString

	def printPlateMap(self,plateMap):
		lineString = "Plate Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = plateMap[i].plateID
				if mapLoc > 40:
					mapLoc = 41
				lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString

	def printPreSmoothMap(self,preSmoothMap):
		lineString = "Pre-Smooth Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int(preSmoothMap[i] * 40)
				lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString

	def printPlateHeightMap(self):
		lineString = "Plate Height Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int(self.plateHeightMap[i] * 40)
				lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString

	def printDistanceMap(self,distanceMap,maxDistance):
		lineString = "Plate Height Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int((distanceMap[i]/maxDistance) * 40)
				lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString

	def getCirclePoints(self,xCenter,yCenter,radius):
		circlePointList = list()
		x = 0
		y = radius
		p = 1 - radius

		self.addCirclePoints(xCenter,yCenter,x,y,circlePointList)

		while (x < y):
			x += 1
			if p < 0:
				p += 2*x + 1
			else:
				y -= 1
				p += 2*(x - y) + 1
			self.addCirclePoints(xCenter,yCenter,x,y,circlePointList)

		return circlePointList

	def addCirclePoints(self,xCenter,yCenter,x,y,circlePointList):
		circlePointList.append(CirclePoint(xCenter + x,yCenter + y))
		circlePointList.append(CirclePoint(xCenter - x,yCenter + y))
		circlePointList.append(CirclePoint(xCenter + x,yCenter - y))
		circlePointList.append(CirclePoint(xCenter - x,yCenter - y))
		circlePointList.append(CirclePoint(xCenter + y,yCenter + x))
		circlePointList.append(CirclePoint(xCenter - y,yCenter + x))
		circlePointList.append(CirclePoint(xCenter + y,yCenter - x))
		circlePointList.append(CirclePoint(xCenter - y,yCenter - x))
		return

class Plate :
	def __init__(self,ID,seedX,seedY):
		self.ID = ID
		self.seedX = seedX
		self.seedY = seedY
		self.isOnMapEdge = False
		self.angle = (PRand.random() * 360) - 180

class PlatePlot :
	def __init__(self,plateID,maxDistance):
		self.plateID = plateID
		self.distanceList = list()
		for i in range(mc.hmNumberOfPlates + 1):
			self.distanceList.append(maxDistance)

class DetailPlate :
	def __init__(self,ID,seedX,seedY):
		self.ID = ID
		self.seedX = seedX
		self.seedY = seedY
		self.isOnMapEdge = False
		self.angle = (PRand.random() * 360) - 180

class DetailPlatePlot :
	def __init__(self,plateID,maxDistance):
		self.plateID = plateID
		self.distanceList = list()
		for i in range(3 * mc.hmNumberOfPlates + 1):
			self.distanceList.append(maxDistance)

class ClimateMap :
	def __init__(self):
		return

	def createClimateMaps(self):
		summerSunMap = array('d')
		winterSunMap = array('d')
		self.summerTempsMap = array('d')
		self.winterTempsMap = array('d')
		self.averageTempMap = array('d')
		self.moistureMap = array('d')
		self.rainFallMap = array('d')

		self.initializeTempMap(summerSunMap,-mc.tropicsLattitude)
		self.initializeTempMap(winterSunMap,0)

		#smooth both sun maps into the temp maps
		for y in range(0,mc.hmHeight):
			for x in range(0,mc.hmWidth):
				contributers = 0
				summerAvg = 0
				winterAvg = 0
				i = GetHmIndex(x,y)
				for yy in range(y - mc.filterSize/2,y + mc.filterSize/2 + 1,1):
					for xx in range(x - mc.filterSize/2,x + mc.filterSize/2 + 1,1):
						ii = GetHmIndex(xx,yy)
						if ii == -1:
							continue
						contributers += 1
						summerAvg += summerSunMap[ii]
						winterAvg += winterSunMap[ii]
				summerAvg = summerAvg/float(contributers)
				winterAvg = winterAvg/float(contributers)
				self.summerTempsMap.append(summerAvg)
				self.winterTempsMap.append(winterAvg)

		#create average temp map
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				#average summer and winter
				avgTemp = (self.summerTempsMap[i] + self.winterTempsMap[i])/2.0
				#cool map for altitude
				#self.averageTempMap.append(avgTemp * (1.0 - hm.getAltitudeAboveSeaLevel(x,y)))
				self.averageTempMap.append(avgTemp)

		#init moisture and rain maps
		for i in range(mc.hmHeight*mc.hmWidth):
			self.moistureMap.append(0.0)
			self.rainFallMap.append(0.0)

		#create sortable plot list for summer monsoon rains
		temperatureList = list()
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				rainPlot = RainPlot(x,y,self.summerTempsMap[i],0)
				temperatureList.append(rainPlot)
		#sort by temperature, coldest first
		temperatureList.sort(lambda x,y:cmp(x.order,y.order))

		#Drop summer monsoon rains
		self.dropRain(temperatureList,self.summerTempsMap,False,None)

		#clear moisture map
		for i in range(mc.hmHeight*mc.hmWidth):
			self.moistureMap[i] = 0.0

		#create sortable plot list for winter monsoon rains
		temperatureList = list()
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				i = GetHmIndex(x,y)
				rainPlot = RainPlot(x,y,self.winterTempsMap[i],0)
				temperatureList.append(rainPlot)
		#sort by temperature, coldest first
		temperatureList.sort(lambda x,y:cmp(x.order,y.order))

		#Drop winter monsoon rains
		self.dropRain(temperatureList,self.winterTempsMap,False,None)

		#clear moisture map
		for i in range(mc.hmHeight*mc.hmWidth):
			self.moistureMap[i] = 0.0

		#set up WindZones class
		wz = WindZones(mc.hmHeight,mc.topLattitude,mc.bottomLattitude)

		#create ordered list for geostrophic rain
		orderList = list()
		for zone in range(6):
			topY = wz.GetYFromZone(zone,True)
			bottomY = wz.GetYFromZone(zone,False)
			if topY == -1 and bottomY == -1:
				continue #This wind zone is not represented on this map at all so skip it
			if topY == -1: #top off map edge
				topY = mc.hmHeight - 1
			if bottomY == -1:
				bottomY = 0

			dx,dy = wz.GetWindDirectionsInZone(zone)
			if dy < 0:
				yStart = topY
				yStop = bottomY - 1
			else:
				yStart = bottomY
				yStop = topY + 1
			if dx < 0:
				xStart = mc.hmWidth - 1
				xStop = -1
			else:
				xStart = 0
				xStop = mc.hmWidth
			order = 0.0
			for y in range(yStart,yStop,dy):
				for x in range(xStart,xStop,dx):
					rainPlot = RainPlot(x,y,order,abs(yStop - y))
					orderList.append(rainPlot)
					order += 1.0

		#Sort order list
		orderList.sort(lambda x,y:cmp(x.order,y.order))

		#drop geostrophic rain
		self.dropRain(orderList,self.averageTempMap,True,wz)

		NormalizeMap(self.rainFallMap,mc.hmWidth,mc.hmHeight)

	def dropRain(self,plotList, tempMap, bGeostrophic, windZones):
		countRemaining = len(plotList)
		bDebug = False
		for plot in plotList:
			i = GetHmIndex(plot.x,plot.y)
			if bDebug:
				print "rainplot at %d,%d" % (plot.x,plot.y)
				print "order = %f" % (plot.order)
				print "initial moisture = %f" % (self.moistureMap[i])
			#First collect moisture from sea
			if hm.isBelowSeaLevel(plot.x,plot.y):
				self.moistureMap[i] += tempMap[i]
				if bDebug:
					print "collecting %f moisture from sea" % (tempMap[i])

			nList = list()
			if bGeostrophic:
				#make list of neighbors in geostrophic zone, even if off map
				zone = windZones.GetZone(plot.y)
				dx,dy = windZones.GetWindDirectionsInZone(zone)
				if bDebug:
					if dy < 0:
						yString = "v"
					else:
						yString = "^"
					if dx < 0:
						xString = "<"
					else:
						xString = ">"
					print "Wind direction ------------------------------- %s%s - %s" % (xString,yString,windZones.GetZoneName(zone))
				nList.append((plot.x,plot.y + dy))
				nList.append((plot.x + dx,plot.y))
				nList.append((plot.x + dx,plot.y + dy))

			else:
				#make list of neighbors with higher temp
				for direction in range(1,9,1):
					xx,yy = GetXYFromDirection(plot.x,plot.y,direction)
					ii = GetHmIndex(xx,yy)
					if ii != -1 and tempMap[i] <= tempMap[ii]:
						nList.append((xx,yy))
				#divide moisture by number of neighbors for distribution
				if len(nList) == 0:
					continue #dead end, dump appropriate rain
			moisturePerNeighbor = self.moistureMap[i]/float(len(nList))
			if bDebug:
				print "moisturePerNeighbor = %f for %d neighbors" % (moisturePerNeighbor,len(nList))

			geostrophicFactor = 1.0
			if bGeostrophic:
				geostrophicFactor = mc.geostrophicFactor
			for xx,yy in nList:
				ii = GetHmIndex(xx,yy)
				if bDebug:
					print "  neighbor %d,%d" % (xx,yy)
					print "  countRemaining = %d" % countRemaining
				#Get the rain cost to enter this plot. Cost is
				#percentage of present moisture available for this
				#neighbor
				if bGeostrophic:
					cost = self.getRainCost(plot.x,plot.y,xx,yy,plot.uplift)
				else:
					cost = self.getRainCost(plot.x,plot.y,xx,yy,countRemaining)

				if bDebug:
					print "  rain cost = %f" % cost

				#Convert moisture into rain
				#self.moistureMap[i] -= cost * moisturePerNeighbor (this line is unecessary actually, we are finished with moisture map for this plot)
				self.rainFallMap[i] += cost * moisturePerNeighbor * geostrophicFactor #geostrophicFactor is not involved with moisture, only to weigh against monsoons
				if bDebug:
					print "  dropping %f rain here" % (cost * moisturePerNeighbor)

				#send remaining moisture to neighbor
				if ii != -1:
					self.moistureMap[ii] += moisturePerNeighbor - (cost * moisturePerNeighbor)
					if bDebug:
						print "  remaining moisture to neighbor = %f" % (moisturePerNeighbor - (cost * moisturePerNeighbor))

			if bDebug:
				print "total rainfall = %f" % self.rainFallMap[i]
			countRemaining -= 1

	def getRainCost(self,x1,y1,x2,y2,distanceToUplift):
		cost = mc.minimumRainCost
		cRange = 1.0 - mc.minimumRainCost/1.0#We don't want to go over 1.0 so the range is reduced
		upliftCost = (1.0/(float(distanceToUplift) + 1.0)) * cRange
		cost += max((hm.getAltitudeAboveSeaLevel(x2,y2) - hm.getAltitudeAboveSeaLevel(x1,y1)) * 2.0 * cRange,upliftCost)
		return cost

	def initializeTempMap(self,tempMap,tropic):
		for y in range(mc.hmHeight):
			for x in range(mc.hmWidth):
				tempMap.append(self.getInitialTemp(x,y,tropic))
		return

	def getInitialTemp(self,x,y,tropic):
		i = GetHmIndex(x,y)
		lat = self.getLattitude(y)
		latRange = float(90 + abs(tropic))
		latDifference = abs(float(lat - tropic))
		aboveSeaLevel = hm.heightMap[i] > hm.seaLevel
		if aboveSeaLevel:
			tempPerLatChange = 1.0/latRange
			temp = 1.0 - (tempPerLatChange * latDifference)
		else:
			tempPerLatChange = (1.0 - (2.0*mc.oceanTempClamp))/latRange
			temp = 1.0 - mc.oceanTempClamp - (tempPerLatChange * latDifference)
		return temp

	def getLattitude(self,y):
		latitudeRange = mc.topLattitude - mc.bottomLattitude
		degreesPerDY = float(latitudeRange)/float(mc.hmHeight)
		latitude = (mc.topLattitude - (int(round(float(y)* degreesPerDY)))) * -1
		return latitude

	def printRainFallMap(self,bOcean):
		lineString = "Rainfall Map"
		print lineString
		wz = WindZones(mc.hmHeight,mc.topLattitude,mc.bottomLattitude)
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				if bOcean:
					mapLoc = int(self.rainFallMap[i] * 10)
					lineString += chr(mapLoc + 48)
				else:
					if hm.isBelowSeaLevel(x,y):
						lineString += '.'
					elif self.rainFallMap[i] < 0.00001:
						lineString += 'X'
					else:
						mapLoc = int(self.rainFallMap[i] * 10)
						lineString += chr(mapLoc + 48)
			z = wz.GetZone(y)
			dx,dy = wz.GetWindDirectionsInZone(z)
			lineString += ' - '
			if dx < 0:
				lineString += '<'
			else:
				lineString += '>'
			if dy < 0:
				lineString += 'v'
			else:
				lineString += '^'
			lineString += ' ' + wz.GetZoneName(z)
			print lineString
		lineString = " "
		print lineString

	def printTempMap(self,tempMap):
		lineString = "Temp Map"
		print lineString
		for y in range(mc.hmHeight - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.hmWidth,1):
				i = GetHmIndex(x,y)
				mapLoc = int(tempMap[i] * 10)
				lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString

class RainPlot :
	def __init__(self,x,y,order,uplift):
		self.x = x
		self.y = y
		self.order = order
		self.uplift = uplift

class WindZones :
	def __init__(self,mapHeight,topLat,botLat):
		self.NPOLAR = 0
		self.NTEMPERATE = 1
		self.NEQUATOR = 2
		self.SEQUATOR = 3
		self.STEMPERATE = 4
		self.SPOLAR = 5
		self.NOZONE = 99
		self.mapHeight = mapHeight
		self.topLat = topLat
		self.botLat = botLat
	def GetZone(self,y):
		if y < 0 or y >= self.mapHeight:
			return self.NOZONE
		else:
			return self.NEQUATOR
		#if lat > mc.polarFrontLattitude:
		#    return self.NPOLAR
		#elif lat > mc.horseLattitude:
		#    return self.NTEMPERATE
		#elif lat > 0:
		#    return self.NEQUATOR
		#elif lat > -mc.horseLattitude:
		#    return self.SEQUATOR
		#elif lat > -mc.polarFrontLattitude:
		#    return self.STEMPERATE
		#else:
		#    return self.SPOLAR
		return
	def GetZoneName(self,zone):
		if zone == self.NPOLAR:
			return "NPOLAR"
		elif zone == self.NTEMPERATE:
			return "NTEMPERATE"
		elif zone == self.NEQUATOR:
			return "NEQUATOR"
		elif zone == self.SEQUATOR:
			return "SEQUATOR"
		elif zone == self.STEMPERATE:
			return "STEMPERATE"
		else:
			return "SPOLAR"
		return
	def GetYFromZone(self,zone,bTop):
		if bTop:
			for y in range(mc.hmHeight - 1,-1,-1):
				if zone == self.GetZone(y):
					return y
		else:
			for y in range(mc.hmHeight):
				if zone == self.GetZone(y):
					return y
		return -1

	def GetZoneSize(self):
		latitudeRange = self.topLat - self.botLat
		degreesPerDY = float(latitudeRange)/float(self.mapHeight)
		size = 30.0/degreesPerDY
		return size

	def GetLatitude(self,y):
		latitudeRange = self.topLat - self.botLat
		degreesPerDY = float(latitudeRange)/float(self.mapHeight)
		latitude = (self.topLat - (int(round(float(y)* degreesPerDY)))) * -1
		return latitude

	def GetWindDirections(self,y):
		z = self.GetZone(y)
		#get x,y directions
		return self.GetWindDirectionsInZone(z)

	def GetWindDirectionsInZone(self,z):
		#get x,y directions
		if z == self.NPOLAR:
			return (-1,-1)
		elif z == self.NTEMPERATE:
			return (1,1)
		elif z == self.NEQUATOR:
			return (-1,-1)
		elif z == self.SEQUATOR:
			return (-1,1)
		elif z == self.STEMPERATE:
			return (1,-1)
		elif z == self.SPOLAR:
			return (-1,1)
		return (0,0)

def isSmallWaterMatch(x,y):
	return sm.isBelowSeaLevel(x,y)

def isPeakMatch(x,y):
	i = y * hm.width + x
	if sm.plotMap[i] == mc.PEAK:
		return True
	return False

class SmallMaps :
	def __init__(self):
		return

	def initialize(self):
		self.cropMaps()
		newHeightMap = ShrinkMap(hm.heightMap,mc.hmWidth ,mc.hmHeight,mc.width,mc.height)
		newRainFallMap = ShrinkMap(cm.rainFallMap,mc.hmWidth,mc.hmHeight,mc.width,mc.height)
		newAverageTempMap = ShrinkMap(cm.averageTempMap,mc.hmWidth,mc.hmHeight,mc.width,mc.height)
		newDetailMap = ShrinkMap(hm.detailPlateHeightMap,mc.hmWidth,mc.hmHeight,mc.width,mc.height)

		self.heightMap = array('d')
		self.rainFallMap = array('d')
		self.averageTempMap = array('d')
		self.detailMap = array('d')

		for y in range(mc.height):
			for x in range(mc.width):
				oldX = x
				i = GetIndexGeneral(oldX,y,mc.width,mc.height)
				if i != -1:
					self.heightMap.append(newHeightMap[i])
					self.rainFallMap.append(newRainFallMap[i])
					self.averageTempMap.append(newAverageTempMap[i])
					self.detailMap.append(newDetailMap[i])
				else:
					self.heightMap.append(0.0)
					self.rainFallMap.append(0.0)
					self.averageTempMap.append(0.0)
					self.detailMap.append(0.0)

		self.desertThreshold = FindValueFromPercent(self.rainFallMap,mc.width,mc.height,mc.DesertPercent,.001,False)
		self.plainsThreshold = FindValueFromPercent(self.rainFallMap,mc.width,mc.height,mc.PlainsPercent,.001,False)

		#Find minimum rainfall on land
		self.minRain = 10.0
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if not self.isBelowSeaLevel(x,y):
					if self.rainFallMap[i] < self.minRain:
						self.minRain = self.rainFallMap[i]

		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				#Smooth coasts first
				if self.isBelowSeaLevel(x,y):
					isCoast = False
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if not self.isBelowSeaLevel(xx,yy):
							isCoast = True
							break
					if isCoast:
						self.heightMap[i] = hm.seaLevel - 0.000001
				else:
					isCoast = False
					avgAlt = self.heightMap[i]
					count = 1
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						avgAlt += self.heightMap[ii]
						count += 1
						if self.isBelowSeaLevel(xx,yy):
							isCoast = True
					if isCoast:
						self.heightMap[i] = max(avgAlt / count, hm.seaLevel + 0.000001)

					# Smooth plots with heavy rainfall
					elif self.rainFallMap[i] > self.plainsThreshold * 1.5:
						self.heightMap[i] = max(avgAlt / count, hm.seaLevel + 0.000001)

					# Smooth and depress plots with very low rainfall and warm temps
					elif self.rainFallMap[i] < ((self.desertThreshold - self.minRain) + self.desertThreshold - self.minRain)/2.0 + self.minRain and self.averageTempMap[i] + 0.25 > ((PRand.random() * 0.25 + 1.0) * mc.TaigaTemp):
						self.heightMap[i] = max(avgAlt / count * 0.9, hm.seaLevel + 0.000001)

		self.fillInLakes()

		self.createPlotMap()
		self.printPlotMap()
		self.createTerrainMap()

	def fillInLakes(self):
		#smaller lakes need to be filled in again because the map
		#shrinker sometimes creates lakes.
		am = Areamap(mc.width,mc.height,True,True)
		am.defineAreas(isSmallWaterMatch)
		oceanID = am.getOceanID()
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.isBelowSeaLevel(x,y) and am.areaMap[i] != oceanID:
					#check the size of this body of water, if too small,
					#change to land
					for a in am.areaList:
						if a.ID == am.areaMap[i] and a.size < mc.minInlandSeaSize:
							self.heightMap[i] = hm.seaLevel
		return

	def isBelowSeaLevel(self,x,y):
		i = GetIndex(x,y)
		if self.heightMap[i] < hm.seaLevel:
			return True
		return False

	## This function returns altitude in relation to sea level with
	## 0.0 being seaLevel and 1.0 being highest altitude
	def getAltitudeAboveSeaLevel(self,x,y):
		i = GetIndex(x,y)
		if i == -1:
			return 0.0
		altitude = self.heightMap[i]
		if altitude < hm.seaLevel:
			return 0.0
		altitude = 1.0/(1.0 - hm.seaLevel) * (altitude - hm.seaLevel)
		return altitude

	def createPlotMap(self):
		self.plotMap = array('i')
		#create height difference map to allow for tuning
		diffMap = array('d')
		for i in range(0,mc.height*mc.width):
			diffMap.append(0.0)
		#I tried using a deviation from surrounding average altitude
		#to determine hills and peaks but I didn't like the
		#results. Therefore I an using lowest neighbor
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				myAlt = self.heightMap[i]
				minAlt = 1.0

				if myAlt > hm.seaLevel:
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if ii == -1:
							continue
						if self.heightMap[ii] < minAlt:
							minAlt = self.heightMap[ii]
					diffMap[i] = myAlt - minAlt
				else:
					diffMap[i] = 0

		NormalizeMap(diffMap,mc.width,mc.height)

		peakHeight = FindValueFromPercent(diffMap,mc.width,mc.height,mc.PeakPercent,0.001,True)
		hillHeight = FindValueFromPercent(diffMap,mc.width,mc.height,mc.HillPercent,0.001,True)

		self.plotMap = array('i')
		#initialize map with 0CEAN
		for i in range(0,mc.height*mc.width):
			self.plotMap.append(mc.OCEAN)
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				altDiff = diffMap[i]
				if self.heightMap[i] < hm.seaLevel:
					self.plotMap[i] = mc.OCEAN
				elif altDiff < hillHeight:
					self.plotMap[i] = mc.LAND
				elif altDiff < peakHeight:
					self.plotMap[i] = mc.HILLS
				else:
					self.plotMap[i] = mc.PEAK

		#Randomize high altitude areas
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				randomNum = PRand.random()
				if self.plotMap[i] == mc.HILLS:
					if randomNum < mc.PeakChanceAtOne * self.getAltitudeAboveSeaLevel(x,y):
						self.plotMap[i] = mc.PEAK
					elif randomNum < self.detailMap[i] * self.getAltitudeAboveSeaLevel(x,y):
						self.plotMap[i] = mc.PEAK
					elif randomNum > self.detailMap[i]:
						self.plotMap[i] = mc.LAND
				elif self.plotMap[i] == mc.LAND:
					if randomNum < mc.HillChanceAtOne * self.getAltitudeAboveSeaLevel(x,y):
						self.plotMap[i] = mc.HILLS
					elif randomNum < self.detailMap[i]:
						self.plotMap[i] = mc.HILLS

		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				peakCount = 0
				hillCount = 0
				onCoast = False

				if self.plotMap[i] == mc.HILLS:
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if self.plotMap[ii] == mc.HILLS:
							hillCount += 1
						if self.plotMap[ii] == mc.OCEAN:
							onCoast = True
					if hillCount > 5:
						for direction in range(1,9,1):
							xx,yy = GetXYFromDirection(x,y,direction)
							ii = GetIndex(xx,yy)
							if self.plotMap[ii] == mc.HILLS and PRand.randint(1,8) < hillCount:
								hillCount -= 1
								self.plotMap[ii] = mc.LAND
					if onCoast and PRand.random() < 0.50:
						self.plotMap[i] = mc.LAND
				elif self.plotMap[i] == mc.PEAK:
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if self.plotMap[ii] == mc.PEAK:
							peakCount += 1
						if self.plotMap[ii] == mc.OCEAN:
							onCoast = True
					if peakCount == 8:
						for direction in range(1,9,1):
							xx,yy = GetXYFromDirection(x,y,direction)
							ii = GetIndex(xx,yy)
							if self.plotMap[ii] == mc.PEAK and PRand.randint(1,16) < peakCount:
								peakCount -= 1
								self.plotMap[ii] = mc.HILLS
					if onCoast and PRand.random() < 0.75:
						self.plotMap[i] = mc.HILLS
				elif self.plotMap[i] != mc.OCEAN:
					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if self.plotMap[ii] == mc.PEAK:
							peakCount += 1

					if peakCount == 8:
						self.plotMap[i] = mc.PEAK
					elif peakCount > 5:
						for direction in range(1,9,1):
							xx,yy = GetXYFromDirection(x,y,direction)
							ii = GetIndex(xx,yy)
							if self.plotMap[ii] == mc.PEAK and PRand.randint(1,8) < peakCount:
								peakCount -= 1
								self.plotMap[ii] = mc.HILLS

		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				peakCount = 0

				if self.plotMap[i] == mc.PEAK:
					continue
				if self.plotMap[i] == mc.OCEAN:
					continue

				for direction in range(1,9,1):
					xx,yy = GetXYFromDirection(x,y,direction)
					ii = GetIndex(xx,yy)
					if self.plotMap[ii] == mc.PEAK:
						peakCount += 1
				if peakCount == 8:
					for direction in range(1,9,1):
						self.plotMap[i] = mc.PEAK

		islandCount = 0
		iterations = int(mc.width * mc.height * 0.5)
		while (islandCount < mc.tinyIslandCount):
			iterations -= 1
			x = PRand.randint(8,mc.width - 8)
			y = PRand.randint(8,mc.height - 8)
			i = GetIndex(x,y)
			islandSpot = True
			if self.plotMap[i] == mc.OCEAN:
				for direction in range(1,9,1):
					xx,yy = GetXYFromDirection(x,y,direction)
					ii = GetIndex(xx,yy)
					if self.plotMap[ii] != mc.OCEAN:
						islandSpot = False
				if islandSpot and PRand.random() * hm.seaLevel < self.heightMap[i]:
					islandCount += 1
					self.plotMap[i] = mc.LAND
			if iterations < 1:
				break
		return

	def createTerrainMap(self):
		mmap = CyMap()
		self.terrainMap = array('i')
		#initialize terrainMap with OCEAN
		for i in range(0,mc.height*mc.width):
			self.terrainMap.append(mc.DEEPOCEAN)

		##Find minimum rainfall on land
		#minRain = 10.0
		#for i in range(mc.width*mc.height):
		#	if self.plotMap[i] != mc.OCEAN:
		#		if self.rainFallMap[i] < minRain:
		#			minRain = self.rainFallMap[i]

		plains = mmap.getCustomMapOption(4)
		plainsPercent = mc.PlainsPercent
		desertPercent = mc.DesertPercent
		grassPercent = mc.GrassPercent
		tundraTemp = mc.TundraTemp
		taigaTemp = mc.TaigaTemp

		if plains == 0:
			plainsPercent -= 0.08
			grassPercent += 0.08
		elif plains == 1:
			plainsPercent -= 0.04
			grassPercent += 0.04
		elif plains == 3:
			plainsPercent += 0.04
			grassPercent -= 0.04
		elif plains == 4:
			plainsPercent += 0.08
			grassPercent -= 0.08

		if mmap.getCustomMapOption(11) > 0: #Smart climate on
			am = Areamap(mc.width,mc.height,True,True)
			am.defineAreas(isSmallWaterMatch)
			continentPercent = 0.70 - am.getLargestContinentPercent()

			print "Evaluating continent percent: %(d)4f" % {"d":continentPercent}

			north = 0
			south = 0
			for y in range(mc.height):
				for x in range(mc.width):
					i = y * mc.width + x
					if self.heightMap[i] > hm.seaLevel:
						if y > mc.height * 0.5: #north landmass
							north += 1
						else:
							south += 1

			if north > south * 1.5: # too much cold land
				print "Excessive northern land detected"
				tundraTemp *= 0.8
				taigaTemp *= 0.8
			elif north > south:
				print "Heavy northern land detected"
				tundraTemp *= 0.9
				taigaTemp *= 0.9

			if continentPercent < -0.20: #Huge continent
				print "Massive Continent, reducing desert and plains"
				if north > south and taigaTemp > 0.35:
					plainsPercent *= 0.9
					desertPercent *= 0.9
					grassPercent *= 1.1
				else:
					if mmap.getCustomMapOption(11) > 1:
						plainsPercent *= 0.9
						desertPercent *= 0.9
						grassPercent *= 1.1
					else:
						plainsPercent *= 0.8
						desertPercent *= 0.8
						grassPercent *= 1.2

			elif continentPercent > 0.20: #Tiny continent
				print "Tiny Continent, increasing desert and plains"
				plainsPercent *= 1.2
				desertPercent *= 1.2
				grassPercent *= 0.8

		self.desertThreshold = FindValueFromPercent(self.rainFallMap,mc.width,mc.height,desertPercent,.001,False)
		self.plainsThreshold = FindValueFromPercent(self.rainFallMap,mc.width,mc.height,plainsPercent,.001,False)
		self.grassThreshold = FindValueFromPercent(self.rainFallMap,mc.width,mc.height,grassPercent,.001,False)

		centerWeight = 1.0

		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.plotMap[i] == mc.OCEAN:
					for direction in range (1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if self.plotMap[ii] != mc.OCEAN:
							self.terrainMap[i] = mc.COAST

		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if mc.FinalWrapY:
					centerWeight = 1.0 - float(abs(x - mc.width/2)) / (mc.width * 0.5)
				if self.plotMap[i] == mc.OCEAN:
					shallow = False
					for direction in range (1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if self.terrainMap[ii] == mc.COAST or self.plotMap[ii] != mc.OCEAN:
							shallow = true
					if shallow or self.heightMap[i] > hm.seaLevel * 0.85:
						if self.terrainMap[i] == mc.DEEPOCEAN:
							self.terrainMap[i] = mc.OCEAN
				#instead of harsh thresholds, allow a random deviation chance
				#based on how close to the threshold the rainfall is
				elif self.rainFallMap[i] < self.desertThreshold:
					if self.averageTempMap[i] < ((PRand.random() * 0.5 + 0.75) * tundraTemp):
						if PRand.random() < centerWeight:
							self.terrainMap[i] = mc.TUNDRA
						else:
							self.terrainMap[i] = mc.TAIGA
					elif self.averageTempMap[i] < ((PRand.random() * 0.25 + 1.0) * taigaTemp) and PRand.random() < centerWeight:
						self.terrainMap[i] = mc.TAIGA
					else:
						if self.rainFallMap[i] < (PRand.random() * (self.desertThreshold - self.minRain) + self.desertThreshold - self.minRain)/2.0 + self.minRain and self.averageTempMap[i] + 0.25 > ((PRand.random() * 0.25 + 1.0) * taigaTemp):
							self.terrainMap[i] = mc.DESERT
						else:
							self.terrainMap[i] = mc.PLAINS
				elif self.rainFallMap[i] < self.plainsThreshold:
					if self.averageTempMap[i] < ((PRand.random() * 0.5 + 0.75) * tundraTemp):
						if PRand.random() < centerWeight:
							self.terrainMap[i] = mc.TUNDRA
						else:
							self.terrainMap[i] = mc.TAIGA
					elif self.averageTempMap[i] < ((PRand.random() * 0.25 + 1.0) * taigaTemp) and PRand.random() < centerWeight:
						self.terrainMap[i] = mc.TAIGA
					else:
						if self.rainFallMap[i] < ((PRand.random() * (self.plainsThreshold - self.desertThreshold) + self.plainsThreshold - self.desertThreshold))/2.0 + self.desertThreshold:
							self.terrainMap[i] = mc.PLAINS
						else:
							self.terrainMap[i] = mc.GRASS
				elif self.rainFallMap[i] < self.grassThreshold:
					if self.averageTempMap[i] < ((PRand.random() * 0.5 + 0.75) * tundraTemp):
						if PRand.random() < centerWeight:
							self.terrainMap[i] = mc.TUNDRA
						else:
							self.terrainMap[i] = mc.TAIGA
					elif self.averageTempMap[i] < ((PRand.random() * 0.25 + 1.0) * taigaTemp) and PRand.random() < centerWeight:
						self.terrainMap[i] = mc.TAIGA
					else:
						if self.rainFallMap[i] < ((PRand.random() * (self.grassThreshold - self.plainsThreshold) + self.grassThreshold - self.plainsThreshold))/2.0 + self.plainsThreshold:
							self.terrainMap[i] = mc.GRASS
						else:
							self.terrainMap[i] = mc.GRASS
				else:
					if self.averageTempMap[i] < ((PRand.random() * 0.5 + 0.75) * tundraTemp):
						if PRand.random() < centerWeight:
							self.terrainMap[i] = mc.TUNDRA
						else:
							self.terrainMap[i] = mc.TAIGA
					elif self.averageTempMap[i] < ((PRand.random() * 0.25 + 1.0) * taigaTemp) and PRand.random() < centerWeight:
						self.terrainMap[i] = mc.TAIGA
					elif self.plotMap[i] != mc.LAND:
						self.terrainMap[i] = mc.GRASS
					else:
						if self.averageTempMap[i] > mc.alwaysMarshTemp - mc.MinMarshTemp + mc.MinMarshTemp and PRand.random() < 0.66:
							self.terrainMap[i] = mc.MARSH
						else:
							self.terrainMap[i] = mc.GRASS

		# Clean up the map, reducing hills and touching up the terrain in deserts
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.terrainMap[i] == mc.DESERT:
					if self.plotMap[i] == mc.HILLS:
						flattenChance = 0.75
						for direction in range (1,9,1):
							xx,yy = GetXYFromDirection(x,y,direction)
							ii = GetIndex(xx,yy)
							if self.plotMap[ii] == mc.PEAK:
								flattenChance *= 0.75
						if PRand.random() < flattenChance:
							self.plotMap[i] = mc.LAND
					elif self.plotMap[i] == mc.PEAK:
						self.terrainMap[i] = mc.PLAINS

					for direction in range(1,9,1):
						xx,yy = GetXYFromDirection(x,y,direction)
						ii = GetIndex(xx,yy)
						if self.terrainMap[ii] == mc.GRASS or self.terrainMap[ii] == mc.TAIGA:
							self.terrainMap[i] = mc.PLAINS
							break
		return

	def cropMaps(self):
		hm.heightMap = CropMap(hm.heightMap)
		cm.averageTempMap = CropMap(cm.averageTempMap)
		cm.rainFallMap = CropMap(cm.rainFallMap)
		mc.hmWidth = mc.hmWidth - mc.westCrop - mc.eastCrop
		mc.hmHeight = mc.hmHeight - mc.northCrop - mc.southCrop

	def printHeightMap(self):
		lineString = "Height Map"
		print lineString
		for y in range(mc.height - 1,-1,-1):
			lineString = ""
			for x in range(0,mc.width,1):
				i = GetIndexGeneral(x,y,mc.width,mc.height)
				mapLoc = int((self.heightMap[i] - hm.seaLevel)/(1.0 - hm.seaLevel) * 10)
				#mapLoc = int(self.heightMap[i] * 10)
				if self.heightMap[i] < hm.seaLevel:
					lineString += '.'
				else:
					lineString += chr(mapLoc + 48)
			print lineString
		lineString = " "
		print lineString

	def printPlotMap(self):
		print "Plot Map"
		for y in range(mc.height - 1,-1,-1):
			lineString = ""
			for x in range(mc.width):
				mapLoc = self.plotMap[GetIndex(x,y)]
				if mapLoc == mc.PEAK:
					lineString += 'A'
				elif mapLoc == mc.HILLS:
					lineString += 'n'
				elif mapLoc == mc.LAND:
					lineString += '+'
				else:
					lineString += '.'
			print lineString
		lineString = " "
		print lineString
	def printTerrainMap(self):
		print "Terrain Map"
		wz = WindZones(mc.height,80,-80)
		for y in range(mc.height - 1,-1,-1):
			lineString = ""
			for x in range(mc.width):
				mapLoc = self.terrainMap[GetIndex(x,y)]
				if mapLoc == mc.OCEAN:
					lineString += ','
				elif mapLoc == mc.COAST:
					lineString += '.'
				elif mapLoc == mc.DESERT:
					lineString += 'D'
				elif mapLoc == mc.GRASS:
					lineString += '+'
				elif mapLoc == mc.MARSH:
					lineString += 'M'
				elif mapLoc == mc.PLAINS:
					lineString += 'P'
				elif mapLoc == mc.TAIGA:
					lineString += 'T'
				elif mapLoc == mc.TUNDRA:
					lineString += 'I'
			lineString += "-" + wz.GetZoneName(wz.GetZone(y))
			print lineString
		lineString = " "
		print lineString

class Areamap :
	def __init__(self,width,height,b8connected,bSwitch4Or8OnFalseMatch):
		self.mapWidth = width
		self.mapHeight = height
		self.areaMap = array('i')
		self.b8connected = b8connected
		self.bSwitch4Or8OnFalseMatch = bSwitch4Or8OnFalseMatch
		#initialize map with zeros
		for i in range(0,self.mapHeight*self.mapWidth):
			self.areaMap.append(0)
		return
	def defineAreas(self,matchFunction):
		#coastIsLand = True means that we are trying to find continents that
		#are not connected by coasts to the main landmasses, allowing us to
		#find continents suitable as a 'New World'. Otherwise, we
		#are just looking to fill in lakes and coast needs to be considered
		#water in that case

		self.areaList = list()
		areaID = 0
		#make sure map is erased in case it is used multiple times
		for i in range(0,self.mapHeight*self.mapWidth):
			self.areaMap[i] = 0
#        for i in range(0,1):
		for i in range(0,self.mapHeight*self.mapWidth):
			if self.areaMap[i] == 0: #not assigned to an area yet
				areaID += 1
				areaSize,match = self.fillArea(i,areaID,matchFunction)
				area = Area(areaID,areaSize,match)
				self.areaList.append(area)
		return

	def getAreaByID(self,areaID):
		for i in range(0,len(self.areaList),1):
			if self.areaList[i].ID == areaID:
				return self.areaList[i]
		return None
	def getOceanID(self):
		self.areaList.sort(lambda x,y:cmp(x.size,y.size))
		self.areaList.reverse()
		for a in self.areaList:
			if a.water:
				return a.ID

	def getContinentCenter(self,ID):
		#first find center in x direction
		changes = list()
		yMin = mc.height
		yMax = -1
		meridianOverlap = False
		onContinent = False
		for x in range(mc.width):
			continentFoundThisPass = False
			for y in range(mc.height):
				i = self.getIndex(x,y)
				if self.areaMap[i] == ID:
					continentFoundThisPass = True
					if y < yMin:
						yMin = y
					elif y > yMax:
						yMax = y
			if x == 0 and continentFoundThisPass:
				meridianOverlap = True
				onContinent = True
			if onContinent and not continentFoundThisPass:
				changes.append(x)
				onContinent = False
			elif not onContinent and continentFoundThisPass:
				changes.append(x)
				onContinent = True
		changes.sort()
		xCenter = -1
		if len(changes) == 0: #continent is continuous
			xCenter = -1
		elif len(changes) == 1:#continent extends to map edge
			if meridianOverlap:
				xCenter = changes[0]/2
			else:
				xCenter = (mc.width - changes[0])/2 + changes[0]
		else:
			if meridianOverlap:
				xCenter = ((changes[1] - changes[0])/2 + changes[0] + (mc.width/2)) % mc.width
			else:
				xCenter = (changes[1] - changes[0])/2 + changes[0]
		yCenter = (yMax - yMin)/2 + yMin
		center = xCenter,yCenter
		return center

	def isPangea(self):
		continentList = list()
		for a in self.areaList:
			if a.water == False:
				continentList.append(a)

		totalLand = 0
		for c in continentList:
			totalLand += c.size

		#sort all the continents by size, largest first
		continentList.sort(lambda x,y:cmp(x.size,y.size))
		continentList.reverse()
		biggestSize = continentList[0].size
		if 0.70 < float(biggestSize)/float(totalLand):
			return True
		return False
	def getMeteorStrike(self):
		continentList = list()
		for a in self.areaList:
			if a.water == False:
				continentList.append(a)

		#sort all the continents by size, largest first
		continentList.sort(lambda x,y:cmp(x.size,y.size))
		continentList.reverse()
		biggestContinentID = continentList[0].ID

		chokeList = list()
		for y in range(mc.height):
			for x in range(mc.width):
				i = self.getIndex(x,y)
				if self.areaMap[i] == biggestContinentID:
					if self.isChokePoint(x,y):
						ap = AreaPlot(x,y)
						chokeList.append(ap)
		#calculate distances to center
		center = self.getContinentCenter(biggestContinentID)
		xCenter,yCenter = center
		for n in range(0,len(chokeList),1):
			distance = self.getDistance(chokeList[n].x,chokeList[n].y,xCenter,yCenter)
			chokeList[n].avgDistance = distance

		#sort plotList for most avg distance and chokeList for least
		#average distance
		chokeList.sort(lambda x,y:cmp(x.avgDistance,y.avgDistance))

		if len(chokeList) == 0:#return bad value if no chokepoints
			return -1,-1
		return chokeList[0].x,chokeList[0].y

	def isChokePoint(self,x,y):
		circlePoints = self.getCirclePoints(x,y,4)
		waterOpposite = False
		landOpposite = False
		for cp in circlePoints:
			if self.isWater(cp.x,cp.y,True):
				#Find opposite
				ox = x + (x - cp.x)
				oy = y + (y - cp.y)
				if self.isWater(ox,oy,True):
					waterOpposite = True
			else:
				#Find opposite
				ox = x + (x - cp.x)
				oy = y + (y - cp.y)
				if not self.isWater(ox,oy,True):
					landOpposite = True
		if landOpposite and waterOpposite:
			return True
		return False
	def getDistance(self,x,y,dx,dy):
		xx = x - dx
		if abs(xx) > mc.width/2:
			xx = mc.width - abs(xx)

		distance = max(abs(xx),abs(y - dy))
		return distance

	def getNewWorldID(self):
		nID = 0
		continentList = list()
		for a in self.areaList:
			if a.water == False:
				continentList.append(a)

		totalLand = 0
		for c in continentList:
			totalLand += c.size

		print totalLand

		#sort all the continents by size, largest first
		continentList.sort(lambda x,y:cmp(x.size,y.size))
		continentList.reverse()

		print ''
		print "All continents"
		print self.PrintList(continentList)

		#now remove a percentage of the landmass to be considered 'Old World'
		oldWorldSize = 0

		#biggest continent is automatically 'Old World'
		oldWorldSize += continentList[0].size
		del continentList[0]

		oldWorldMinSize = max(16,totalLand * 0.03)
		idealOldWorldSize = int(totalLand * 0.66)

		oldWorldPercent = float(oldWorldSize)/float(totalLand)
		print "Ideal Old World total size is %(w)2d" % {"w":idealOldWorldSize}
		print "Current Old World size is %(w)2d" % {"w":oldWorldSize}

		#Select 'old world' continents that can have players start on them, we
		#only want continents that are large enough to be useful but we also
		#need to make sure we have enough room for everybody
		while oldWorldSize < idealOldWorldSize:
			print "Minimum Old World continent size is %(w)2d" % {"w":oldWorldMinSize}
			print "There are %(c)2d continents in the list." % {"c":len(continentList)}
			o = len(continentList) - 1
			n = 0
			while n < o:
				if oldWorldPercent > 0.66:
					print "Old world continent selection complete, total size is %(t)2d" % {"t":oldWorldSize}
					break
				print "Evaluating continent ID %(d)2d, size is %(s)2d." % {"d":continentList[n].ID,"s":continentList[n].size}
				if continentList[n].size > oldWorldMinSize:
					oldWorldSize += continentList[n].size
					oldWorldPercent = float(oldWorldSize)/float(totalLand)
					print "Adding continent %(c)2d to old world, total size is now %(t)2d" % {"c":continentList[n].ID,"t":oldWorldSize}
					del continentList[n]
					#decrease the list length (o) by one to prevent going out of bounds
					#do not incriment the current count (n) here since that list item was removed
					o -= 1
				else: #incriment the counter if no continent was removed from the list
					n += 1
			oldWorldMinSize *= 0.75
			idealOldWorldSize *= 0.75

		#what remains in the list will be considered 'New World'
		print ''
		print "New World Continents"
		print self.PrintList(continentList)

		#get ID for the next continent, we will use this ID for 'New World'
		#designation
		nID = continentList[0].ID
		del continentList[0] #delete to avoid unnecessary overwrite

		#now change all the remaining continents to also have nID as their ID
		for i in range(self.mapHeight*self.mapWidth):
			for c in continentList:
				if c.ID == self.areaMap[i]:
					self.areaMap[i] = nID

		return nID

	def getLargestContinentPercent(self):
		continentList = list()
		for a in self.areaList:
			if a.water == False:
				continentList.append(a)

		totalLand = 0
		for c in continentList:
			totalLand += c.size

		#sort all the continents by size, largest first
		continentList.sort(lambda x,y:cmp(x.size,y.size))
		continentList.reverse()

		size = 0
		size += continentList[0].size

		percent = float(size)/float(totalLand)
		return percent

	def getIndex(self,x,y):
		#Check X for wrap
		if mc.WrapX:
			xx = x % self.mapWidth
		elif x < 0 or x >= self.mapWidth:
			return -1
		else:
			xx = x
		#Check y for wrap
		if mc.WrapY:
			yy = y % self.mapHeight
		elif y < 0 or y >= self.mapHeight:
			return -1
		else:
			yy = y

		i = yy * self.mapWidth + xx
		return i

	def fillArea(self,index,areaID,matchFunction):
		#first divide index into x and y
		y = index/self.mapWidth
		x = index%self.mapWidth
		#We check 8 neigbors for land,but 4 for water. This is because
		#the game connects land squares diagonally across water, but
		#water squares are not passable diagonally across land
		self.segStack = list()
		self.size = 0
		matchValue = matchFunction(x,y)
		#place seed on stack for both directions
		seg = LineSegment(y,x,x,1)
		self.segStack.append(seg)
		seg = LineSegment(y+1,x,x,-1)
		self.segStack.append(seg)
		while(len(self.segStack) > 0):
			seg = self.segStack.pop()
			self.scanAndFillLine(seg,areaID,matchValue,matchFunction)
##            if (seg.y < 8 and seg.y > 4) or (seg.y < 70 and seg.y > 64):
##            if (areaID == 4
##                PrintPlotMap(hm)
##                self.PrintAreaMap()

		return self.size,matchFunction(x,y)
	def scanAndFillLine(self,seg,areaID,matchValue,matchFunction):
		#check for y + dy being off map
		i = self.getIndex(seg.xLeft,seg.y + seg.dy)
		if i < 0:
##            print "scanLine off map ignoring",str(seg)
			return
		debugReport = False
##        if (seg.y < 8 and seg.y > 4) or (seg.y < 70 and seg.y > 64):
##        if (areaID == 4):
##            debugReport = True
		#for land tiles we must look one past the x extents to include
		#8-connected neighbors
		if self.b8connected:
			if self.bSwitch4Or8OnFalseMatch and matchValue:
				landOffset = 0
			else:
				landOffset = 1
		else:
			if self.bSwitch4Or8OnFalseMatch and matchValue:
				landOffset = 1
			else:
				landOffset = 0

		lineFound = False
		#first scan and fill any left overhang
		if debugReport:
			print ""
			print "areaID = %(a)4d" % {"a":areaID}
			print "matchValue = %(w)2d, landOffset = %(l)2d" % {"w":matchValue,"l":landOffset}
			print str(seg)
			print "Going left"
		if mc.WrapX:
			xStop = 0 - (self.mapWidth*20)
		else:
			xStop = -1
		for xLeftExtreme in range(seg.xLeft - landOffset,xStop,-1):
			i = self.getIndex(xLeftExtreme,seg.y + seg.dy)
			if debugReport:
				print "xLeftExtreme = %(xl)4d" % {'xl':xLeftExtreme}
			if debugReport:
				print "i = %d, seg.y + seg.dy = %d" % (i,seg.y + seg.dy)
				print "areaMap[i] = %d, matchValue match = %d" % (self.areaMap[i],matchValue == matchFunction(xLeftExtreme,seg.y + seg.dy))
			if self.areaMap[i] == 0 and matchValue == matchFunction(xLeftExtreme,seg.y + seg.dy):
				self.areaMap[i] = areaID
				self.size += 1
				lineFound = True
			else:
				#if no line was found, then xLeftExtreme is fine, but if
				#a line was found going left, then we need to increment
				#xLeftExtreme to represent the inclusive end of the line
				if lineFound:
					xLeftExtreme += 1
				break
		if debugReport:
			print "xLeftExtreme finally = %(xl)4d" % {'xl':xLeftExtreme}
			print "Going Right"
		#now scan right to find extreme right, place each found segment on stack
#        xRightExtreme = seg.xLeft - landOffset #needed sometimes? one time it was not initialized before use.
		xRightExtreme = seg.xLeft #needed sometimes? one time it was not initialized before use.
		if mc.WrapX:
			xStop = self.mapWidth*20
		else:
			xStop = self.mapWidth
		for xRightExtreme in range(seg.xLeft + lineFound - landOffset,xStop,1):
			if debugReport:
				print "xRightExtreme = %(xr)4d" % {'xr':xRightExtreme}
			i = self.getIndex(xRightExtreme,seg.y + seg.dy)
			if debugReport:
				print "i = %d, seg.y + seg.dy = %d" % (i,seg.y + seg.dy)
				print "areaMap[i] = %d, matchValue match = %d" % (self.areaMap[i],matchValue == matchFunction(xRightExtreme,seg.y + seg.dy))
			if self.areaMap[i] == 0 and matchValue == matchFunction(xRightExtreme,seg.y + seg.dy):
				self.areaMap[i] = areaID
				self.size += 1
				if lineFound == False:
					lineFound = True
					xLeftExtreme = xRightExtreme #starting new line
					if debugReport:
						print "starting new line at xLeftExtreme= %(xl)4d" % {'xl':xLeftExtreme}
			elif lineFound: #found the right end of a line segment!
				lineFound = False
				#put same direction on stack
				newSeg = LineSegment(seg.y + seg.dy,xLeftExtreme,xRightExtreme - 1,seg.dy)
				self.segStack.append(newSeg)
				if debugReport:
					print "same direction to stack",str(newSeg)
				#determine if we must put reverse direction on stack
				if xLeftExtreme < seg.xLeft or xRightExtreme >= seg.xRight:
					#out of shadow so put reverse direction on stack also
					newSeg = LineSegment(seg.y + seg.dy,xLeftExtreme,xRightExtreme - 1,-seg.dy)
					self.segStack.append(newSeg)
					if debugReport:
						print "opposite direction to stack",str(newSeg)
				if xRightExtreme >= seg.xRight + landOffset:
					if debugReport:
						print "finished with line"
					break; #past the end of the parent line and this line ends
			elif lineFound == False and xRightExtreme >= seg.xRight + landOffset:
				if debugReport:
					print "no additional lines found"
				break; #past the end of the parent line and no line found
			else:
				continue #keep looking for more line segments
		if lineFound: #still a line needing to be put on stack
			if debugReport:
				print "still needing to stack some segs"
			lineFound = False
			#put same direction on stack
			newSeg = LineSegment(seg.y + seg.dy,xLeftExtreme,xRightExtreme - 1,seg.dy)
			self.segStack.append(newSeg)
			if debugReport:
				print str(newSeg)
			#determine if we must put reverse direction on stack
			if xLeftExtreme < seg.xLeft or xRightExtreme - 1 > seg.xRight:
				#out of shadow so put reverse direction on stack also
				newSeg = LineSegment(seg.y + seg.dy,xLeftExtreme,xRightExtreme - 1,-seg.dy)
				self.segStack.append(newSeg)
				if debugReport:
					print str(newSeg)

		return
	#for debugging
	def PrintAreaMap(self):

		print "Area Map"
		for y in range(self.mapHeight - 1,-1,-1):
			lineString = ""
			for x in range(self.mapWidth):
				mapLoc = self.areaMap[self.getIndex(x,y)]
				if mapLoc + 34 > 127:
					mapLoc = 127 - 34
				lineString += chr(mapLoc + 34)
			lineString += "-" + str(y)
			print lineString
		oid = self.getOceanID()
		if oid == None or oid + 34 > 255:
			print "Ocean ID is unknown"
		else:
			print "Ocean ID is %(oid)4d or %(c)s" % {'oid':oid,'c':chr(oid + 34)}
		lineString = " "
		print lineString

		return
	def PrintList(self,s):
		for a in s:
			char = chr(a.ID + 34)
			lineString = str(a) + ' ' + char
			print lineString

	def getCirclePoints(self,xCenter,yCenter,radius):
		circlePointList = list()
		x = 0
		y = radius
		p = 1 - radius

		self.addCirclePoints(xCenter,yCenter,x,y,circlePointList)

		while (x < y):
			x += 1
			if p < 0:
				p += 2*x + 1
			else:
				y -= 1
				p += 2*(x - y) + 1
			self.addCirclePoints(xCenter,yCenter,x,y,circlePointList)

		return circlePointList

	def addCirclePoints(self,xCenter,yCenter,x,y,circlePointList):
		circlePointList.append(CirclePoint(xCenter + x,yCenter + y))
		circlePointList.append(CirclePoint(xCenter - x,yCenter + y))
		circlePointList.append(CirclePoint(xCenter + x,yCenter - y))
		circlePointList.append(CirclePoint(xCenter - x,yCenter - y))
		circlePointList.append(CirclePoint(xCenter + y,yCenter + x))
		circlePointList.append(CirclePoint(xCenter - y,yCenter + x))
		circlePointList.append(CirclePoint(xCenter + y,yCenter - x))
		circlePointList.append(CirclePoint(xCenter - y,yCenter - x))
		return
class CirclePoint :
	def __init__(self,x,y):
		self.x = x
		self.y = y

class LineSegment :
	def __init__(self,y,xLeft,xRight,dy):
		self.y = y
		self.xLeft = xLeft
		self.xRight = xRight
		self.dy = dy
	def __str__ (self):
		string = "y = %(y)3d, xLeft = %(xl)3d, xRight = %(xr)3d, dy = %(dy)2d" % \
		{'y':self.y,'xl':self.xLeft,'xr':self.xRight,'dy':self.dy}
		return string

class Area :
	def __init__(self,iD,size,water):
		self.ID = iD
		self.size = size
		self.water = water

	def __str__(self):
		string = "{ID = %(i)4d, size = %(s)4d, water = %(w)1d}" % \
		{'i':self.ID,'s':self.size,'w':self.water}
		return string
class AreaPlot :
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.avgDistance = -1

#OK! now that directions N,S,E,W are important, we have to keep in mind that
#the map plots are ordered from 0,0 in the SOUTH west corner! NOT the northwest
#corner! That means that Y increases as you go north.
class RiverMap :
	def __init__(self):
		#To provide global access without allocating alot of resources for
		#nothing, object initializer must be empty
		return
	def generateRiverMap(self):
		self.L = 0 #also denotes a 'pit' or 'flat'
		self.N = 1
		self.S = 2
		self.E = 3
		self.W = 4
		self.NE = 5
		self.NW = 6
		self.SE = 7
		self.SW = 8
		self.O = 5 #used for ocean or land without a river

		#averageHeightMap, flowMap, averageRainfallMap and drainageMap are offset from the other maps such that
		#each element coincides with a four tile intersection on the game map
		self.averageHeightMap = array('d')
		self.flowMap = array('i')
		self.averageRainfallMap = array('d')
		self.drainageMap = array('d')
		self.riverMap = array('i')
		#initialize maps with zeros
		for i in range(0,mc.height*mc.width):
			self.averageHeightMap.append(0.0)
			self.flowMap.append(0)
			self.averageRainfallMap.append(0.0)
			self.drainageMap.append(0.0)
			self.riverMap.append(self.O)
		#Get highest intersection neighbor
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				maxHeight = 0.0;
				for yy in range(y,y-2,-1):
					for xx in range(x,x+2):
						ii = GetIndex(xx,yy)
						#use an average hight of <0 to denote an ocean border
						#this will save processing time later
						if(sm.plotMap[ii] == mc.OCEAN):
							maxHeight = -100.0
						elif maxHeight < sm.heightMap[ii] and maxHeight >= 0:
							maxHeight = sm.heightMap[ii]
				self.averageHeightMap[i] = maxHeight
		#Now try to silt in any lakes
		self.siltifyLakes()
		self.createLakeDepressions()
		#create flowMap by checking for the lowest of each 4 connected
		#neighbor plus self
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				lowestAlt = self.averageHeightMap[i]
				if(lowestAlt < 0.0):
					#if height is <0 then that means this intersection is
					#adjacent to an ocean and has no flow
					self.flowMap[i] = self.O
				else:
					#First assume this place is lowest, like a 'pit'. Then
					#for each place that is lower, add it to a list to be
					#randomly chosen as the drainage path
					drainList = list()
					nonDrainList = list()
					self.flowMap[i] = self.L
					ii = GetIndex(x,y+1)
					#in the y direction, avoid wrapping
					if(y > 0 and self.averageHeightMap[ii] < lowestAlt):
						drainList.append(self.N)
					else:
						nonDrainList.append(self.N)
					ii = GetIndex(x,y-1)
					if(y < mc.height - 1 and self.averageHeightMap[ii] < lowestAlt):
						drainList.append(self.S)
					else:
						nonDrainList.append(self.S)
					ii = GetIndex(x-1,y)
					if(self.averageHeightMap[ii] < lowestAlt):
						drainList.append(self.W)
					else:
						nonDrainList.append(self.W)
					ii = GetIndex(x+1,y)
					if(self.averageHeightMap[ii] < lowestAlt):
						drainList.append(self.E)
					else:
						nonDrainList.append(self.E)

					#never go straight when you have other choices
					count = len(drainList)
					if count == 3:
						oppDir = GetOppositeDirection(nonDrainList[0])
						for n in range(count):
							if drainList[n] == oppDir:
								del drainList[n]
								break
						count = len(drainList)

					if count > 0:
						choice = int(PRand.random()*count)
						self.flowMap[i] = drainList[choice]

		#Create average rainfall map so that each intersection is an average
		#of the rainfall from rm.rainMap
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				avg = 0.0;
				for yy in range(y,y-2,-1):
					for xx in range(x,x+2):
						ii = GetIndex(xx,yy)
						avg += sm.rainFallMap[ii]
				avg = avg/4.0
				self.averageRainfallMap[i] = avg

		#Now use the flowMap as a guide to distribute average rainfall.
		#Wherever the most rainfall ends up is where the rivers will be.
		print "Distributing rainfall"
		# Bugfix: flow map can contain cycles on some seeds (siltifyLakes /
		# createLakeDepressions modify heightmap but don't guarantee the
		# flow map stays a DAG).  Without a step cap the while-loop below
		# hangs the engine forever during "Distributing rainfall".
		_rainfall_step_cap = mc.height * mc.width
		_rainfall_cycle_hits = 0
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				flow = self.flowMap[i]
				rainFall = self.averageRainfallMap[i]
				xx = x
				yy = y
				_steps = 0
				while(flow != self.L and flow != self.O):
					_steps += 1
					if _steps > _rainfall_step_cap:
						_rainfall_cycle_hits += 1
						break
					if(flow == self.N):
						yy += 1
					elif(flow == self.S):
						yy -= 1
					elif(flow == self.W):
						xx -= 1
					elif(flow == self.E):
						xx += 1
					#wrap
					if(xx < 0):
						xx = mc.width - 1
					elif(xx >= mc.width):
						xx = 0
					if(yy < 0):
						yy = mc.height - 1
					elif(yy >= mc.height):
						yy = 0
					#dump rainfall here
					ii = GetIndex(xx,yy)
					self.drainageMap[ii] += rainFall
					#reset flow
					flow = self.flowMap[ii]

		if _rainfall_cycle_hits > 0:
			print "  WARN: flow-map cycles detected on %d origin tiles" % _rainfall_cycle_hits
		riverThreshold = sm.plainsThreshold * mc.RiverThreshold
		for i in range(mc.height*mc.width):
			if(self.drainageMap[i] > riverThreshold):
				self.riverMap[i] = self.flowMap[i]
			else:
				self.riverMap[i] = self.O

		#at this point river should be in tolerance or close to it
		#riverMap is ready for use

	def rxFromPlot(self,x,y,direction):
		if direction == self.NE:
			return x,y + 1
		if direction == self.SW:
			return x - 1,y
		if direction == self.SE:
			return x,y
		raise ValueError,"rxFromPlot using bad direction input"

	def siltifyLakes(self):
		lakeList = []
		onQueueMap = array('i')
		for y in range(mc.height):
			for x in range(mc.width):
				onQueueMap.append(0)
				i = GetIndex(x,y)
				if self.isLake(x,y):
					lakeList.append((x,y,1))
					onQueueMap[i] = 1
		largestLength = len(lakeList)
		while len(lakeList) > 0:
			if len(lakeList) > largestLength:
				largestLength = len(lakeList)
			x,y,lakeSize = lakeList[0]
			del lakeList[0]
			i = GetIndex(x,y)
			onQueueMap[i] = 0

			if lakeSize > mc.maxSiltPanSize:
				continue
			lakeSize += 1
			lowestNeighborAlt = self.getLowestNeighborAltitude(x,y)
			self.averageHeightMap[i] = lowestNeighborAlt + 0.005
			for direction in range(1,5,1):
				xx,yy = GetXYFromDirection(x,y,direction)
				ii = GetIndex(xx,yy)
				if ii == -1:
					continue
				if self.isLake(xx,yy) and onQueueMap[ii] == 0:
					lakeList.append((xx,yy,lakeSize))
					onQueueMap[ii] = 1
		return

	def isLake(self,x,y):
		i = GetIndex(x,y)
		alt = self.averageHeightMap[i]
		if alt < 0.0:
			return False
		for direction in range(1,5,1):
			xx,yy = GetXYFromDirection(x,y,direction)
			ii = GetIndex(xx,yy)
			if ii == -1:
				continue
			if self.averageHeightMap[ii] < alt:
				return False
		return True

	def getLowestNeighborAltitude(self,x,y):
		lowest = 1.0
		for direction in range(1,5,1):
			xx,yy = GetXYFromDirection(x,y,direction)
			ii = GetIndex(xx,yy)
			if ii == -1:
				continue
			if self.averageHeightMap[ii] < lowest:
				lowest = self.averageHeightMap[ii]
		return lowest

	def createLakeDepressions(self):
		lakeList = []
		for y in range(mc.height):
			for x in range(mc.width):
				i = GetIndex(x,y)
				if self.averageHeightMap[i] > mc.minLakeAltitude:
					lakeList.append((x,y))
		lakeList = ShuffleList(lakeList)
		numLakes = int(mc.height * mc.width * mc.numberOfLakesPerPlot)
		for n in range(numLakes):
			x,y = lakeList[n]
			i = GetIndex(x,y)
			lowestAlt = self.getLowestNeighborAltitude(x,y)
			if lowestAlt < 0.0:
				continue
			self.averageHeightMap[i] = lowestAlt - 0.001

	def printRiverMap(self):
		print "River Map"
		wz = WindZones(mc.height,80,-80)
		for y in range(mc.height - 1,-1,-1):
			lineString = ""
			for x in range(mc.width):
				mapLoc = self.riverMap[GetIndex(x,y)]
				if mapLoc == self.O:
					lineString += '.'
				elif mapLoc == self.L:
					lineString += 'L'
				elif mapLoc == self.N:
					lineString += 'N'
				elif mapLoc == self.S:
					lineString += 'S'
				elif mapLoc == self.E:
					lineString += 'E'
				elif mapLoc == self.W:
					lineString += 'W'
			lineString += "-" + wz.GetZoneName(wz.GetZone(y))
			print lineString
		lineString = " "
		print lineString

	def printFlowMap(self):
		print "Flow Map"
		wz = WindZones(mc.height,80,-80)
		for y in range(mc.height - 1,-1,-1):
			lineString = ""
			for x in range(mc.width):
				mapLoc = self.flowMap[GetIndex(x,y)]
				if mapLoc == self.O:
					lineString += '.'
				elif mapLoc == self.L:
					lineString += 'L'
				elif mapLoc == self.N:
					lineString += 'N'
				elif mapLoc == self.S:
					lineString += 'S'
				elif mapLoc == self.E:
					lineString += 'E'
				elif mapLoc == self.W:
					lineString += 'W'
			lineString += "-" + wz.GetZoneName(wz.GetZone(y))
			print lineString
		lineString = " "
		print lineString

	def printRiverAndTerrainAlign(self):
		print "River Alignment Check"
		for y in range(mc.height - 1,-1,-1):
			lineString1 = ""
			lineString2 = ""
			for x in range(mc.width):
				mapLoc = sm.terrainMap[GetIndex(x,y)]
				if mapLoc == mc.OCEAN:
					lineString1 += ',.'
				elif mapLoc == mc.COAST:
					lineString1 += ',.'
				elif mapLoc == mc.DESERT:
					lineString1 += 'D.'
				elif mapLoc == mc.GRASS:
					lineString1 += 'R.'
				elif mapLoc == mc.PLAINS:
					lineString1 += 'P.'
				elif mapLoc == mc.TAIGA:
					lineString1 += 'T.'
				elif mapLoc == mc.MARSH:
					lineString1 += 'M.'
				elif mapLoc == mc.TUNDRA:
					lineString1 += 'I.'
				mapLoc = rm.riverMap[GetIndex(x,y)]
				if mapLoc == rm.O:
					lineString2 += '..'
				elif mapLoc == rm.L:
					lineString2 += '.L'
				elif mapLoc == rm.N:
					lineString2 += '.^'
				elif mapLoc == rm.S:
					lineString2 += '.v'
				elif mapLoc == rm.E:
					lineString2 += '.>'
				elif mapLoc == rm.W:
					lineString2 += '.<'
			print lineString1
			print lineString2
		lineString1 = " "
		print lineString1

hm = HeightMap()
cm = ClimateMap()
sm = SmallMaps()
rm = RiverMap()

###############################################################################
#functions that civ is looking for
###############################################################################
def getDescription():
	"""
	A map's Description is displayed in the main menu when players go to begin a game.
	For no description return an empty string.
	"""
	return "Random map that simulates earth-like plate tectonics, " +\
		"geostrophic and monsoon winds and rainfall."
def getWrapX():
	return mc.FinalWrapX

def getWrapY():
	return mc.FinalWrapY

def getNumCustomMapOptions():
	"""
	Number of different user-defined options for this map
	Return an integer
	"""
	return 13

def getCustomMapOptionName(argsList):
		"""
		Returns name of specified option
		argsList[0] is Option ID (int)
		Return a Unicode string
		"""
		optionID = argsList[0]
		if optionID == 0:
			return "Cohesion"
		elif optionID == 1:
			return "Mountains"
		elif optionID == 2:
			return "Desert Chance"
		elif optionID == 3:
			return "Taiga Chance"
		elif optionID == 4:
			return "Plains Chance"
		elif optionID == 5:
			return "Jungle Chance"
		elif optionID == 6:
			return "Forest Density"
		elif optionID == 7:
			return "World Wrap"
		elif optionID == 8:
			return "Unit Placement"
		elif optionID == 9:
			return "Rivers and Lakes"
		elif optionID == 10:
			return "Advanced Terrain"
		elif optionID == 11:
			return "Smart Climate"
		elif optionID == 12:
			return "Ancient City Ruins"
		elif optionID == 13:
			return "Team Start"
		return u""

def getNumCustomMapOptionValues(argsList):
		"""
		Number of different choices for a particular setting
		argsList[0] is Option ID (int)
		Return an integer
		"""
		optionID = argsList[0]
		if optionID == 0:
			return 4
		elif optionID == 1:
			return 3
		elif optionID == 2:
			return 7
		elif optionID == 3:
			return 6
		elif optionID == 4:
			return 5
		elif optionID == 5:
			return 6
		elif optionID == 6:
			return 3
		elif optionID == 7:
			return 4
		elif optionID == 8:
			return 2
		elif optionID == 9:
			return 3
		elif optionID == 10:
			return 2
		elif optionID == 11:
			return 4
		elif optionID == 12:
			return 2
		elif optionID == 13:
			return 3
		return 0

def getCustomMapOptionDescAt(argsList):
	"""
	Returns name of value of option at specified row
	argsList[0] is Option ID (int)
	argsList[1] is Selection Value ID (int)
	Return a Unicode string
	"""
	optionID = argsList[0]
	selectionID = argsList[1]
	if optionID == 0: #Cohesion
		if selectionID == 0:
			return "High"
		elif selectionID == 1:
			return "Medium"
		elif selectionID == 2:
			return "Low"
		elif selectionID == 3:
			return "Inland Sea"
	elif optionID == 1: #Mountains
		if selectionID == 0:
			return "Standard (Default)"
		elif selectionID == 1:
			return "Fewer"
		elif selectionID == 2:
			return "More"
	elif optionID == 2: #Desert
		if selectionID == 0:
			return "No Desert"
		elif selectionID == 1:
			return "Minimal (-0.08)"
		elif selectionID == 2:
			return "Low (-0.05)"
		elif selectionID == 3:
			return "Reduced (-0.02)"
		elif selectionID == 4:
			return "Standard (Default)"
		elif selectionID == 5:
			return "Increased (+0.02)"
		elif selectionID == 6:
			return "High (+0.07)"
	elif optionID == 3: #Taiga
		if selectionID == 0:
			return "No Taiga"
		elif selectionID == 1:
			return "Low"
		elif selectionID == 2:
			return "Reduced"
		elif selectionID == 3:
			return "Standard (Default)"
		elif selectionID == 4:
			return "Increased"
		elif selectionID == 5:
			return "High"
	elif optionID == 4: #Plains
		if selectionID == 0:
			return "Low (-0.08)"
		elif selectionID == 1:
			return "Reduced (-0.04)"
		elif selectionID == 2:
			return "Standard (Default)"
		elif selectionID == 3:
			return "High (+0.04)"
		elif selectionID == 4:
			return "Very High (+0.08)"
	elif optionID == 5: #Jungle
		if selectionID == 0:
			return "No Jungles"
		elif selectionID == 1:
			return "Low"
		elif selectionID == 2:
			return "Reduced"
		elif selectionID == 3:
			return "Standard (Default)"
		elif selectionID == 4:
			return "Increased"
		elif selectionID == 5:
			return "High"
	elif optionID == 6: #Forest Density
		if selectionID == 0:
			return "Reduced"
		elif selectionID == 1:
			return "Moderate (Default)"
		elif selectionID == 2:
			return "Increased"
	elif optionID == 7: #Wrap
		if selectionID == 0:
			return "Flat (Default)"
		elif selectionID == 1:
			return "East-West (x)"
		elif selectionID == 2:
			return "North-South (y)"
		elif selectionID == 3:
			return "All (x & y)"
	elif optionID == 8: #Unit placement
		if selectionID == 0:
			return "Spread Out (Default)"
		elif selectionID == 1:
			return "Same Tile"
	elif optionID == 9: #Rivers & lakes
		if selectionID == 0:
			return "Reduced"
		if selectionID == 1:
			return "Moderate (Default)"
		if selectionID == 2:
			return "Increased"
	elif optionID == 10: #Advanced Terrain
		if selectionID == 0:
			return "Off (may be faster)"
		if selectionID == 1:
			return "On"
	elif optionID == 11: #Smart Climate
		if selectionID == 0:
			return "Off"
		if selectionID == 1:
			return "On (ensure exists)"
		if selectionID == 2:
			return "On (override selection)"
		if selectionID == 3:
			return "On (modify selection)"
	elif optionID == 12: #Ancient Ruins
		if selectionID == 0:
			return "Off"
		elif selectionID == 1:
			return "On"
	elif optionID == 13: #Team Start
		if selectionID == 0:
			return "Team Neighbors"
		if selectionID == 1:
			return "Team Separated"
		if selectionID == 2:
			return "Randomly Placed"
	return u""

def getCustomMapOptionDefault(argsList):
	"""
	Returns default value of specified option
	argsList[0] is Option ID (int)
	Return an integer
	"""
	optionID = argsList[0]
	if optionID == 2:
		return 4
	elif optionID == 3:
		return 3
	elif optionID == 4:
		return 2
	elif optionID == 5:
		return 3
	elif optionID == 6:
		return 1
	elif optionID == 9:
		return 1
	elif optionID == 10:
		return 1

	return 0

def isRandomCustomMapOption(argsList):
	"""
	Returns a flag indicating whether a random option should be provided
	argsList[0] is Option ID (int)
	Return a bool
	"""
	optionID = argsList[0]
	if optionID > 6:
		return False
	return True

#This doesn't work with my river system so it is disabled.
def normalizeAddRiver():
	return
def normalizeRemovePeaks():
	gc = CyGlobalContext()
	gameMap = CyMap()
	civPreferenceList = GetCivPreferences()

	print "Removing peaks and hills ..."

	for playerIndex in range(gc.getMAX_CIV_PLAYERS()):
		player = gc.getPlayer(playerIndex)

		if player.isEverAlive():
			plot = player.getStartingPlot()
			civType = player.getCivilizationType()
			jv = 0
			fv = 0
			hv = 0
			foundPref = False

			for civPreference in civPreferenceList:
				if civPreference.civ == civType:
					civPref = civPreference
					jv = int(civPref.jungleValue)
					fv = int(civPref.forestValue)
					hv = int(civPref.hillValue)
					foundPref = True
					break

			if foundPref:
				print "Player" + str(playerIndex) + " preference found- Jungle Val: " + str(jv) + " Forest Val: " + str(fv) + " Hill Val: " + str(hv)
			else:
				civPref = CivPreference(civType)
				print "Player" + str(playerIndex) + " no preference found, using defaults"

			if plot.getPlotType() == PlotTypes.PLOT_PEAK: #Should never happen, but just in case it does
				plot.setPlotType(PlotTypes.PLOT_HILLS,True,True)

			x = plot.getX()
			y = plot.getY()

			# cycle through the surrounding plots
			for xx in range(x - 3, x + 3):
				for yy in range(y - 3, y + 3):
					if yy == y or xx == x:
						continue
					nPlot = gameMap.plot(xx,yy)
					cityRing = float(max(abs(x-xx),abs(y-yy)))

					# With FfH we need to make sure we don't break the unique
					# features, which are really improvements.
					if nPlot.getImprovementType() == ImprovementTypes.NO_IMPROVEMENT:
						if nPlot.getPlotType() == PlotTypes.PLOT_HILLS:
							if hv < 1:
								if PRand.random() > 0.2 * cityRing:
									nPlot.setPlotType(PlotTypes.PLOT_LAND,True,True)
							# For civs that have a preference for hills we'll do
							# this backwards and reduce some hills further from
							# the starting plot
							elif PRand.random() < 0.2 * cityRing:
								nPlot.setPlotType(PlotTypes.PLOT_LAND,True,True)

						if nPlot.getPlotType() == PlotTypes.PLOT_PEAK:
							if PRand.random() > 0.15 * cityRing or cityRing == 1:
								nPlot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
	return
def normalizeAddLakes():
	return
def normalizeAddGoodTerrain():
	return
def normalizeRemoveBadTerrain():
	gc = CyGlobalContext()
	gameMap = CyMap()
	civPreferenceList = GetCivPreferences()
	playerList = list()

	print "Removing bad features ..."

	for playerIndex in range(gc.getMAX_CIV_PLAYERS()):
		player = gc.getPlayer(playerIndex)

		if player.isEverAlive():
			plot = player.getStartingPlot()
			featureType = plot.getFeatureType()
			civType = player.getCivilizationType()

			jv = 0
			fv = 0
			foundPref = False

			for civPreference in civPreferenceList:
				if civPreference.civ == civType:
					civPref = civPreference
					jv = int(civPref.jungleValue)
					fv = int(civPref.forestValue)
					break

			if featureType == GetInfoType("FEATURE_FOREST") or featureType == GetInfoType("FEATURE_JUNGLE") or featureType == GetInfoType("FEATURE_FOREST_ANCIENT"):
				plot.setFeatureType(GetInfoType("NO_FEATURE"),0)

			x = plot.getX()
			y = plot.getY()

			# cycle through the surrounding plots, chance to remove a feature
			# is based on the distance from the starting plot
			for xx in range(x - 3, x + 3):
				for yy in range(y - 3, y + 3):
					if yy == y or xx == x:
						continue
					nPlot = gameMap.plot(xx,yy)
					featureType = nPlot.getFeatureType()
					cityRing = float(max(abs(x-xx),abs(y-yy)))

					# With FfH we need to make sure we don't break the unique
					# features, which are really improvements.
					if nPlot.getImprovementType() == ImprovementTypes.NO_IMPROVEMENT:
					# Jungles are almost always bad, so cut them regardless of
					# bonuses (resources)
						if featureType == GetInfoType("FEATURE_JUNGLE") and jv < 1:
							if PRand.random() > 0.2 * cityRing:
								nPlot.setFeatureType(GetInfoType("NO_FEATURE"),0)

						# If a plot has a bonus (resource) leave hills & forests intact
						if nPlot.getBonusType(TeamTypes.NO_TEAM) == BonusTypes.NO_BONUS:
							if featureType == GetInfoType("FEATURE_FOREST") or featureType == GetInfoType("FEATURE_FOREST_ANCIENT"):
								if PRand.random() > 0.25 * cityRing  and fv < 1:
									nPlot.setFeatureType(GetInfoType("NO_FEATURE"),0)
	return
def normalizeRemoveBadFeatures():
	return
def normalizeAddFoodBonuses():
	return

def startHumansOnSameTile():
	"Returns true if all human units should start on the same tile"
	return mc.HumansOnSameTile

def normalizeAddExtras():
	gc = CyGlobalContext()
	mmap = gc.getMap()

	if mmap.getCustomMapOption(12) > 0:
		rx, ry = findRuinCenters()
		for (ix, iy) in zip (rx, ry):
			(usedx, usedy) = fillRuinCenter (ix, iy)
			addSuburbsRoads(ix, iy, usedx, usedy)
		addHighways(rx, ry)
		blowRoads()
	return

def isAdvancedMap():
	"""
	Advanced maps only show up in the map script pulldown on the advanced menu.
	Return 0 if you want your map to show up in the simple singleplayer menu
	"""
	return 0
def isClimateMap():
	"""
	Uses the Climate options
	"""
	return 0

def isSeaLevelMap():
	"""
	Uses the Sea Level options
	"""
	return True

def getTopLatitude():
	"Default is 90. 75 is past the Arctic Circle"
	return 90

def getBottomLatitude():
	"Default is -90. -75 is past the Antartic Circle"
	return -10

def beforeInit():
	mc.initialize()
	mc.initInGameOptions()

def generatePlotTypes():
	gc = CyGlobalContext()
	mmap = gc.getMap()
	mc.width = mmap.getGridWidth()
	mc.height = mmap.getGridHeight()
	PRand.seed()
	hm.performTectonics()
	hm.generateHeightMap()
	hm.combineMaps()
	hm.calculateSeaLevel()
	hm.fillInLakes()
	hm.addWaterBands()
	cm.createClimateMaps()
	sm.initialize()
	rm.generateRiverMap()
	plotTypes = [PlotTypes.PLOT_OCEAN] * (mc.width*mc.height)

	for i in range(mc.width*mc.height):
		mapLoc = sm.plotMap[i]
		if mapLoc == mc.PEAK:
			plotTypes[i] = PlotTypes.PLOT_PEAK
		elif mapLoc == mc.HILLS:
			plotTypes[i] = PlotTypes.PLOT_HILLS
		elif mapLoc == mc.LAND:
			plotTypes[i] = PlotTypes.PLOT_LAND
		else:
			plotTypes[i] = PlotTypes.PLOT_OCEAN
	print "Finished generating plot types."
	return plotTypes
def generateTerrainTypes():
	NiTextOut("Generating Terrain  ...")
	print "Adding Terrain"
	gc = CyGlobalContext()

	terrainDesert = GetInfoType("TERRAIN_DESERT")
	terrainPlains = GetInfoType("TERRAIN_PLAINS")
	terrainTundra = GetInfoType("TERRAIN_TUNDRA")
	terrainTaiga = GetInfoType("TERRAIN_TAIGA")
	terrainGrass = GetInfoType("TERRAIN_GRASS")
	terrainHill = GetInfoType("TERRAIN_HILL")
	terrainCoast = GetInfoType("TERRAIN_COAST")
	terrainOcean = GetInfoType("TERRAIN_OCEAN")
	terrainMarsh = GetInfoType("TERRAIN_MARSH")
	if GetInfoType("TERRAIN_OCEAN_DEEP") != -1:
		terrainDeepOcean = GetInfoType("TERRAIN_OCEAN_DEEP")
	else:
		terrainDeepOcean = GetInfoType("TERRAIN_OCEAN")

	terrainTypes = [0]*(mc.width*mc.height)
	for i in range(mc.width*mc.height):
		if sm.terrainMap[i] == mc.OCEAN:
			terrainTypes[i] = terrainOcean
		elif sm.terrainMap[i] == mc.DEEPOCEAN:
			terrainTypes[i] = terrainDeepOcean
		elif sm.terrainMap[i] == mc.COAST:
			terrainTypes[i] = terrainCoast
		elif sm.terrainMap[i] == mc.DESERT:
			terrainTypes[i] = terrainDesert
		elif sm.terrainMap[i] == mc.PLAINS:
			terrainTypes[i] = terrainPlains
		elif sm.terrainMap[i] == mc.GRASS:
			terrainTypes[i] = terrainGrass
		elif sm.terrainMap[i] == mc.TAIGA:
			terrainTypes[i] = terrainTaiga
		elif sm.terrainMap[i] == mc.TUNDRA:
			terrainTypes[i] = terrainTundra
		elif sm.terrainMap[i] == mc.MARSH:
			terrainTypes[i] = terrainMarsh
	print "Finished generating terrain types."
	return terrainTypes

def findRuinCenters ():
	gc = CyGlobalContext() ; map = CyMap() ; game = CyGame()
	tundra = GetInfoType("TERRAIN_TAIGA")
	snow = GetInfoType("TERRAIN_TAIGA")
	desert = GetInfoType("TERRAIN_DESERT")
	xmax = map.getGridWidth() ; ymax = map.getGridHeight ()
	iArea = map.findBiggestArea(false).getID()
	ra = [] ; px = [] ; py = [] ; rx = [] ; ry = [] ; cx = [] ; cy = []
	# Create list of player locations
	for iPlay in range(gc.getMAX_CIV_PLAYERS()):
		pPlay = gc.getPlayer(iPlay)
		if (pPlay.isAlive()):
			pPlot = pPlay.getStartingPlot()
			px.append(pPlot.getX())
			py.append(pPlot.getY())
	# Create array, mark plots between 5-8 distance from all players
	for ix in range(xmax):
		ra.append([])
		for iy in range(ymax):
			ra[ix].append(0)
			pPlot = map.plot(ix, iy)
			# Reject if bad terrain or on island
			if pPlot.isPeak(): continue
			if pPlot.isWater(): continue
			if pPlot.getTerrainType() == snow: continue
			if pPlot.getTerrainType() == desert: continue
			if pPlot.getArea() != iArea: continue
			dmin = 10000
			for (x, y) in zip (px, py):
				d = max (abs (x - ix), abs (y - iy))
				if (d < dmin): dmin = d
			if (dmin > 4) and (dmin < 9):
				ra[ix][iy] = 1
				cx.append(ix) ; cy.append(iy)
	# cxy now has list of all nonzero points in ra
	while 1:
		# Pick a point; clear neighborhood; rebuild candidate list
		if len(cx) == 0: break
		n = game.getMapRandNum(len(cx), "")
		rx.append(cx[n]) ; ry.append(cy[n])
		for ix in range(cx[n]-6, cx[n]+7):
			if (ix < 0) or (ix >= xmax): continue
			for iy in range(cy[n]-6, cy[n]+7):
				if (iy < 0) or (iy >= ymax): continue
				ra[ix][iy] = 0
		cx = [] ; cy = []
		for ix in range(xmax):
			for iy in range(ymax):
				if ra[ix][iy] > 0:
					cx.append(ix) ; cy.append(iy)
	return rx, ry

def addRuinBonus(rx, ry, usedx, usedy, type):
	ruinsType = GetInfoType("IMPROVEMENT_CITY_RUINS_ANCIENT")
	if ruinsType == -1:
		ruinsType = GetInfoType("IMPROVEMENT_CITY_RUINS")
	gc = CyGlobalContext() ; map = CyMap() ; game = CyGame()
	if len(rx) > 0:
		n = game.getMapRandNum(len(rx), "")
		ix = rx[n] ; iy = ry[n]
		pPlot = map.plot(ix, iy)
		if pPlot.getImprovementType() == ruinsType:
			pPlot.setBonusType(type)
			pPlot.setImprovementType(GetInfoType("NO_IMPROVEMENT"))
			pPlot.setRouteType(GetInfoType("ROUTE_ROAD"))
		del rx[n] ; del ry[n]
		usedx.append(ix) ; usedy.append(iy)
	return rx, ry, usedx, usedy

def fillRuinCenter (cx, cy):
	gc = CyGlobalContext() ; map = CyMap() ; game = CyGame()
	ruin = GetInfoType("IMPROVEMENT_CITY_RUINS_ANCIENT")
	if ruin == -1:
		ruin = GetInfoType("IMPROVEMENT_CITY_RUINS")
	grave = GetInfoType("IMPROVEMENT_GRAVEYARD")
	mana = GetInfoType("BONUS_MANA")
	artifact = GetInfoType("BONUS_PATRIAN_ARTIFACTS")
	road = GetInfoType("ROUTE_ROAD")
	if GetInfoType("PLOT_EFFECT_HAUNTED_LANDS") != -1:
		haunted = GetInfoType("PLOT_EFFECT_HAUNTED_LANDS")
	else:
		haunted = GetInfoType("FEATURE_FOREST_BURNT")
	nobonus = BonusTypes.NO_BONUS
	xmax = map.getGridWidth() ; ymax = map.getGridHeight ()
	rx = [] ; ry = []
	# Center, plus most of the squares around it are ruins
	for ix in range(cx-1, cx+2):
		if (ix < 0) or (ix >= xmax): continue
		for iy in range(cy-1, cy+2):
			if (iy < 0) or (iy >= ymax): continue
			type = ruin
			if (ix != cx) or (iy != cy):
				n = game.getMapRandNum(1000, "")
				if n < 150: type = grave
				elif n < 600: continue
			pPlot = map.plot(ix, iy)
			if pPlot.isPeak(): continue
			if pPlot.isWater(): continue
			if pPlot.getImprovementType() == GetInfoType("NO_IMPROVEMENT"):
				pPlot.setImprovementType(type)
			if type == grave:
				pPlot.setBonusType(nobonus)
				if pPlot.getFeatureType() == GetInfoType("FEATURE_FOREST"):
					pPlot.setPlotEffectType(haunted)
			else:
				rx.append(ix) ; ry.append(iy)
				pPlot.setRouteType(road)
				if pPlot.getFeatureType() == GetInfoType("FEATURE_FOREST") and PRand.random() < 0.33:
					pPlot.setPlotEffectType(haunted)
	usedx = [] ; usedy = []

	if pPlot.getBonusType(TeamTypes.NO_TEAM) == BonusTypes.NO_BONUS:
		n = game.getMapRandNum(1000, "")
		if n < 300:
			(rx, ry, usedx, usedy) = addRuinBonus(rx, ry, usedx, usedy, mana)
		elif n < 600 and artifact != -1:
			(rx, ry, usedx, usedy) = addRuinBonus(rx, ry, usedx, usedy, artifact)
	return usedx, usedy

def addSuburbRoad(cx, cy, sx, sy, ra):
	gc = CyGlobalContext() ; map = CyMap()
	ruin = GetInfoType("IMPROVEMENT_CITY_RUINS_ANCIENT")
	if ruin == -1:
		ruin = GetInfoType("IMPROVEMENT_CITY_RUINS")
	road = GetInfoType("ROUTE_ROAD")
	pPlot = map.plot(sx+cx-4, sy+cy-4)
	if not pPlot.isPeak():
		if pPlot.getImprovementType() == GetInfoType("NO_IMPROVEMENT") and PRand.random() > 0.5:
			pPlot.setImprovementType(ruin)
		pPlot.setRouteType(road)
		r = ra[sx][sy]
		while r > 0:
			found = 0
			for x1 in range (sx-1,sx+2):
				for y1 in range (sy-1,sy+2):
					if x1<0 or x1>8 or y1<0 or y1>8: continue
					if ra[x1][y1] == r - 1: found = 1
					if found: break;
				if found: break;
			map.plot(x1+cx-4, y1+cy-4).setRouteType(road)
			sx = x1 ; sy = y1
			r = r - 1

def addSuburbsRoads (cx, cy, rxs, rys):
	gc = CyGlobalContext() ; map = CyMap() ; game = CyGame()
	ra = []
	iInvalid = 1000 ; iUnreach = 1001
	iArea = map.findBiggestArea(false).getID()
	# Create 5x5 local array
	for x1 in range(0,9):
		ra.append([])
		for y1 in range(0,9):
			ra[x1].append(iUnreach)
			# Set invalid if water, offgrid or impassable
			x = cx + x1 - 4 ; y = cy + y1 - 4
			if not map.isPlot(x, y): ra[x1][y1] = iInvalid
			pPlot = map.plot(x, y)
			# Reject if bad terrain or on island
			if pPlot.isPeak() or pPlot.isWater(): ra[x1][y1] = iInvalid
			if pPlot.getArea() != iArea: ra[x1][y1] = iInvalid
	# Mark center and ruin points as distance 0 and add to dixy lists
	dixs = [] ; diys = [] ; dixs.append([]) ; diys.append([])
	ra[4][4] = 0 ; dixs[0].append(4) ; diys[0].append(4)
	for (x1, y1) in zip (rxs, rys):
		ra[x1-cx+4][y1-cy+4] = 0
		dixs[0].append(x1-cx+4) ; diys[0].append(y1-cy+4)
	# Extend out to range 3
	for r in range (1,4):
		dixs.append([]); diys.append([]);
		for (x1, y1) in zip (dixs[r-1], diys[r-1]):
			for x2 in range (x1-1,x1+2):
				for y2 in range (y1-1,y1+2):
					if x2<0 or x2>8 or y2<0 or y2>8: continue
					if ra[x2][y2] == iUnreach:
						ra[x2][y2] = r
						dixs[r].append(x2) ; diys[r].append(y2)
	# Pick a small number of candidates
	candx = dixs[2] + dixs[3] ; candy = diys[2] + diys[3]
	x = game.getMapRandNum(1000, "")
	if x < 300: numcands = 0
	elif x < 600: numcands = 1
	elif x < 900: numcands = 2
	else: numcands = 3
	for n in range(numcands):
		if len(candx) == 0: break
		posn = game.getMapRandNum(len(candx), "")
		x = candx[posn] ; y = candy[posn]
		addSuburbRoad(cx, cy, x, y, ra)
		del candx[posn] ; del candy[posn]

def highwaySort(l1, l2):
	d1 = l1[0] ; d2 = l2[0]
	if d1 > d2: return 1
	elif d1 < d2: return -1
	else: return 0

def addHighway(x1, y1, x2, y2):
	gc = CyGlobalContext() ; map = CyMap()
	iArea = map.findBiggestArea(false).getID()
	iInvalid = 1000 ; iUnreach = 1001
	ra = []
	xmax = map.getGridWidth() ; ymax = map.getGridHeight ()
	# Build array with unreachable except where invalid
	for x in range(xmax):
		ra.append([])
		for y in range(ymax):
			ra[x].append(iUnreach)
			pPlot = map.plot(x, y)
			if pPlot.isImpassable() or pPlot.isWater(): ra[x][y] = iInvalid
			if pPlot.getArea() != iArea: ra[x][y] = iInvalid
	# Extend out to range 15 or we arrive at destination
	oldx = [x1] ; oldy = [y1] ; ra[x1][y1] = 0
	bFound = false
	for r in range (1,15):
		newx = [] ; newy = []
		for (x, y) in zip (oldx, oldy):
			for xc in range (x-1,x+2):
				for yc in range (y-1,y+2):
					if not map.isPlot(xc, yc): continue
					if ra[xc][yc] == iUnreach:
						ra[xc][yc] = r
						if (xc == x2) and (yc == y2):
							bFound = true
							break
						newx.append(xc) ; newy.append(yc)
				if bFound: break
			if bFound: break
		oldx = newx ; oldy = newy
	if not bFound: return
	road  = gc.getInfoTypeForString("ROUTE_ROAD")
	r = ra[x2][y2] ; sx = x2 ; sy = y2
	while r > 0:
		cands = []
		for xc in range (sx-1,sx+2):
			for yc in range (sy-1,sy+2):
				if not map.isPlot(xc, yc): continue
				if ra[xc][yc] == r - 1:
					dx = xc - x1 ; dy = yc - y1
					cands.append([(dx*dx)+(dy*dy), xc, yc])
		candsort = sorted(cands, highwaySort)
		xc = candsort[0][1] ; yc = candsort[0][2]
		if not map.plot(xc,yc).isPeak():
			map.plot(xc, yc).setRouteType(road)
		sx = xc ; sy = yc
		r -= 1

def addHighways(rx, ry):
	dists = [] ; used = []
	# Make list of (distance, index1, index2) for each pair of cities
	for i in range(len(rx)-1):
		for j in range(i+1, len(rx)):
			dx = abs (rx[i] - rx[j]) ; dy = abs (ry[i] - ry[j])
			if dy > dx: dx = dy
			dists.append([dx,i,j])
	# Make sure each city is connected once
	for i in range(len(rx)): used.append(false)
	for d12 in sorted(dists, highwaySort):
		i = d12[1] ; j = d12[2]
		if (used[i]) and (used[j]): continue
		addHighway(rx[i], ry[i], rx[j], ry[j])
		used[i] = true ; used[j] = true

def blowRoads():
	gc = CyGlobalContext() ; map = CyMap() ; game = CyGame()
	road  = gc.getInfoTypeForString("ROUTE_ROAD")
	ruin = GetInfoType("IMPROVEMENT_CITY_RUINS_ANCIENT")
	if ruin == -1:
		ruin = GetInfoType("IMPROVEMENT_CITY_RUINS")
	for iPlotLoop in range(map.numPlots()):
		pPlot = map.plotByIndex(iPlotLoop)
		if pPlot.getRouteType() != road: continue
		chance = 200
		if pPlot.getImprovementType() == ruin:
			chance = 100
		elif pPlot.getFeatureType() != GetInfoType("NO_FEATURE"):
			chance = 700
		elif pPlot.getTerrainType() == GetInfoType("TERRAIN_DESERT") or pPlot.getTerrainType() == GetInfoType("TERRAIN_TUNDRA"):
			chance = 750
		if game.getMapRandNum(1000, "") < chance:
			pPlot.setRouteType(-1)

def addRivers():
	NiTextOut("Adding Rivers....")
	print "Adding Rivers"
	gc = CyGlobalContext()
	pmap = gc.getMap()
	for y in range(mc.height):
		for x in range(mc.width):
			placeRiversInPlot(x,y)

	#peaks and rivers don't always mix well graphically, so lets eliminate
	#these potential glitches. Basically if there are adjacent peaks on both
	#sides of a river, either in a cardinal direction or diagonally, they
	#will look bad.
	for y in range(mc.height):
		for x in range(mc.width):
			plot = pmap.plot(x,y)
			if plot.isPeak():
				if plot.isNOfRiver():
					for xx in range(x - 1,x + 2,1):
						yy = y - 1
						if yy < 0:
							break
						#wrap in x direction
						if xx == -1:
							xx = mc.width - 1
						elif xx == mc.width:
							xx = 0
						newPlot = pmap.plot(xx,yy)
						ii = GetIndex(xx,yy)
						if newPlot.isPeak():
							plot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
							sm.plotMap[ii] = mc.HILLS
							break
			#possibly changed so checked again
			if plot.isPeak():
				if plot.isWOfRiver():
					for yy in range(y - 1,y + 2,1):
						xx = x + 1
						if xx == mc.width:
							xx = 0
						#do not wrap in y direction
						if yy == -1:
							continue
						elif yy == mc.height:
							continue
						newPlot = pmap.plot(xx,yy)
						ii = GetIndex(xx,yy)
						if newPlot.isPeak():
							plot.setPlotType(PlotTypes.PLOT_HILLS,True,True)
							sm.plotMap[ii] = mc.HILLS
							break

def placeRiversInPlot(x,y):
	gc = CyGlobalContext()
	pmap = gc.getMap()
	plot = pmap.plot(x,y)
	#NE
	xx,yy = rm.rxFromPlot(x,y,rm.NE)
	ii = GetIndex(xx,yy)
	if ii != -1:
		if rm.riverMap[ii] == rm.S:
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
	#SW
	xx,yy = rm.rxFromPlot(x,y,rm.SW)
	ii = GetIndex(xx,yy)
	if ii != -1:
		if rm.riverMap[ii] == rm.E:
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_EAST)
	#SE
	xx,yy = rm.rxFromPlot(x,y,rm.SE)
	ii = GetIndex(xx,yy)
	if ii != -1:
		if rm.riverMap[ii] == rm.N:
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
		elif rm.riverMap[ii] == rm.W:
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_WEST)
'''
This function examines a lake area and removes ugly surrounding rivers. Any
river that is flowing away from the lake, or alongside the lake will be
removed. This function also returns a list of riverID's that flow into the
lake.
'''
def cleanUpLake(x,y):
	gc = CyGlobalContext()
	mmap = gc.getMap()
	riversIntoLake = list()
	plot = mmap.plot(x,y+1)#North
	if plot != 0 and plot.isNOfRiver():
		plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	if plot != 0 and plot.isWOfRiver():
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_SOUTH:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x - 1,y)#West
	if plot != 0 and plot.isWOfRiver():
		plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	if plot != 0 and plot.isNOfRiver():
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_EAST:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x + 1,y)#East
	if plot != 0 and plot.isNOfRiver():
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_WEST:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x,y-1)#South
	if plot != 0 and plot.isWOfRiver():
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_NORTH:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x-1,y+1)#Northwest
	if plot != 0 and plot.isWOfRiver():
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_SOUTH:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	if plot != 0 and plot.isNOfRiver():
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_EAST:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x+1,y+1)#Northeast
	if plot != 0 and plot.isNOfRiver():
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_WEST:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot = mmap.plot(x-1,y-1)#Southhwest
	if plot != 0 and plot.isWOfRiver():
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_NORTH:
			riversIntoLake.append(plot.getRiverID())
		else:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	#Southeast plot is not relevant

	return riversIntoLake
'''
This function replaces rivers to update the river crossings after a lake or
channel is placed at X,Y. There had been a long standing problem where water tiles
added after a river were causing graphical glitches and incorrect river rules
due to not updating the river crossings.
'''
def replaceRivers(x,y):
	gc = CyGlobalContext()
	mmap = gc.getMap()
	plot = mmap.plot(x,y+1)#North
	if plot != 0 and plot.isWOfRiver():
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_SOUTH:
			#setting the river to what it already is will be ignored by the dll,
			#so it must be unset and then set again.
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
	plot = mmap.plot(x - 1,y)#West
	if plot != 0 and plot.isNOfRiver():
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_EAST:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_EAST)
	plot = mmap.plot(x + 1,y)#East
	if plot != 0 and plot.isNOfRiver():
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_WEST:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_WEST)
	plot = mmap.plot(x,y-1)#South
	if plot != 0 and plot.isWOfRiver():
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_NORTH:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
	plot = mmap.plot(x-1,y+1)#Northwest
	if plot != 0 and plot.isWOfRiver():
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_SOUTH:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_SOUTH)
	if plot != 0 and plot.isNOfRiver():
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_EAST:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_EAST)
	plot = mmap.plot(x+1,y+1)#Northeast
	if plot != 0 and plot.isNOfRiver():
		if plot.getRiverWEDirection() == CardinalDirectionTypes.CARDINALDIRECTION_WEST:
			plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setNOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_WEST)
	plot = mmap.plot(x-1,y-1)#Southhwest
	if plot != 0 and plot.isWOfRiver():
		if plot.getRiverNSDirection() == CardinalDirectionTypes.CARDINALDIRECTION_NORTH:
			plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
			plot.setWOfRiver(True,CardinalDirectionTypes.CARDINALDIRECTION_NORTH)
	#Southeast plot is not relevant

	return

'''
It looks bad to have a lake, fed by a river, sitting right next to the coast.
This function tries to minimize that occurance by replacing it with a
natural harbor, which looks much better.
'''
def makeHarbor(x,y,oceanMap):
	oceanID = oceanMap.getOceanID()
	i = oceanMap.getIndex(x,y)
	if oceanMap.areaMap[i] != oceanID:
		return
	#N
	xx = x
	yy = y + 2
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x,y + 1)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#S
	xx = x
	yy = y - 2
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x,y - 1)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#E
	xx = x + 2
	yy = y
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x + 1,y)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#W
	xx = x - 2
	yy = y
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x - 1,y)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#NW
	xx = x - 1
	yy = y + 1
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x - 1,y)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#NE
	xx = x + 1
	yy = y + 1
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x + 1,y)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#SW
	xx = x - 1
	yy = y - 1
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x ,y - 1)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	#NW
	xx = x - 1
	yy = y + 1
	ii = oceanMap.getIndex(xx,yy)
	if ii > -1 and \
	oceanMap.getAreaByID(oceanMap.areaMap[ii]).water and \
	oceanMap.areaMap[ii] != oceanID:
		makeChannel(x,y + 1)
		oceanMap.defineAreas(isSmallWaterMatch)
		oceanID = oceanMap.getOceanID()
	return
def makeChannel(x,y):
	gc = CyGlobalContext()
	mmap = gc.getMap()

	terrainCoast = GetInfoType("TERRAIN_COAST")
	plot = mmap.plot(x,y)
	cleanUpLake(x,y)
	plot.setTerrainType(terrainCoast,True,True)
	plot.setRiverID(-1)
	plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	replaceRivers(x,y)
	i = GetIndex(x,y)
	sm.plotMap[i] = mc.OCEAN
	return
def expandLake(x,y,riversIntoLake,oceanMap):
	class LakePlot :
		def __init__(self,x,y,altitude):
			self.x = x
			self.y = y
			self.altitude = altitude
	gc = CyGlobalContext()
	mmap = gc.getMap()
	lakePlots = list()
	lakeNeighbors = list()
	i = oceanMap.getIndex(x,y)
	desertModifier = 1.0
	if sm.terrainMap[i] == mc.DESERT:
		desertModifier = mc.DesertLakeModifier
	drainage = rm.drainageMap[i]
	lakeSize = min(max(3,int(drainage * mc.LakeSizePerDrainage * desertModifier )),mc.maxLakeSize)
	start = LakePlot(x,y,sm.heightMap[i])
	lakeNeighbors.append(start)
	while lakeSize > 0 and len(lakeNeighbors) > 0:
		lakeNeighbors.sort(lambda x,y:cmp(x.altitude,y.altitude))
		currentLakePlot = lakeNeighbors[0]
		del lakeNeighbors[0]
		lakePlots.append(currentLakePlot)
		plot = mmap.plot(currentLakePlot.x,currentLakePlot.y)
		#if you are erasing a river to make a lake, make the lake smaller
		if plot.isNOfRiver() or plot.isWOfRiver():
			lakeSize -= 1
		makeChannel(currentLakePlot.x,currentLakePlot.y)
		#Add valid neighbors to lakeNeighbors
		for n in range(4):
			if n == 0:#N
				xx = currentLakePlot.x
				yy = currentLakePlot.y + 1
				ii = oceanMap.getIndex(xx,yy)
			elif n == 1:#S
				xx = currentLakePlot.x
				yy = currentLakePlot.y - 1
				ii = oceanMap.getIndex(xx,yy)
			elif n == 2:#E
				xx = currentLakePlot.x + 1
				yy = currentLakePlot.y
				ii = oceanMap.getIndex(xx,yy)
			elif n == 3:#W
				xx = currentLakePlot.x - 1
				yy = currentLakePlot.y
				ii = oceanMap.getIndex(xx,yy)
			else:
				raise ValueError, "too many cardinal directions"
			if ii != -1:
				#if this neighbor is in water area, then quit
				areaID = oceanMap.areaMap[ii]
				if areaID == 0:
					raise ValueError, "areaID = 0 while generating lakes. This is a bug"
				for n in range(0,len(oceanMap.areaList),1):
					if oceanMap.areaList[n].ID == areaID:
						if oceanMap.areaList[n].water:
							return

				#don't allow lake to grow into plots with 3+ surrounding peaks
				peakCount = 0
				for direction in range(1,9,1):
					dx,dy = GetXYFromDirection(currentLakePlot.x,currentLakePlot.y,direction)
					di = GetIndex(dx,dy)
					if sm.plotMap[di] == mc.PEAK:
						peakCount += 1

				if rm.riverMap[ii] != rm.L and mmap.plot(xx,yy).isWater() == False and peakCount < 3:
					lakeNeighbors.append(LakePlot(xx,yy,sm.heightMap[ii]))

		lakeSize -= 1
	return

def addLakes():
	print "Adding Lakes"
	gc = CyGlobalContext()
	mmap = gc.getMap()
	oceanMap = Areamap(mc.width,mc.height,True,True)
	oceanMap.defineAreas(isSmallWaterMatch)
	for y in range(mc.height):
		for x in range(mc.width):
			i = GetIndex(x,y)
			if rm.flowMap[i] == rm.L:
				riversIntoLake = cleanUpLake(x,y)
				plot = mmap.plot(x,y)
				if len(riversIntoLake) > 0:
					expandLake(x,y,riversIntoLake,oceanMap)
				else:
					#no lake here, but in that case there should be no rivers either
					plot.setRiverID(-1)
					plot.setNOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
					plot.setWOfRiver(False,CardinalDirectionTypes.NO_CARDINALDIRECTION)
	oceanMap.defineAreas(isSmallWaterMatch)
	for y in range(mc.height):
		for x in range(mc.width):
			i = GetIndex(x,y)
			makeHarbor(x,y,oceanMap)
	return

def addFeatures():
	NiTextOut("Generating Features  ...")
	print "Adding Features"
	gc = CyGlobalContext()
	mmap = gc.getMap()

	featureIce = GetInfoType("FEATURE_ICE")
	featureKelp = GetInfoType("FEATURE_KELP")
	featureReef = GetInfoType("FEATURE_REEFS")
	featureJungle = GetInfoType("FEATURE_JUNGLE")
	featureForest = GetInfoType("FEATURE_FOREST")
	featureAncientForest = GetInfoType("FEATURE_FOREST_ANCIENT")
	featureHauntedForest = GetInfoType("PLOT_EFFECT_HAUNTED_LANDS")
	featureLightForest = GetInfoType("FEATURE_FOREST_NEW")
	featureFloodPlains = GetInfoType("FEATURE_FLOOD_PLAINS")
	featureOasis = GetInfoType("FEATURE_OASIS")
	featureScrub = GetInfoType("FEATURE_SCRUB")
	FORESTLEAFY = 0
	FORESTEVERGREEN = 1
	FORESTSNOWY = 2

	am = Areamap(mc.hmWidth,mc.hmHeight,True,True)
	am.defineAreas(isSmallWaterMatch)
	oceanID = am.getOceanID()

	if mc.TaigaTemp > 0.0:
		if mc.FinalWrapY:
			iceChance = mc.TaigaTemp * 2.0
			maxY = 0
			for y in range(0,mc.hmMaxGrain * 2):
				for x in range(mc.width):
					plot = mmap.plot(x,y)
					i = GetIndex(x,y)
					if plot != 0 and plot.isWater():
						iceProb = iceChance * (1.0 - float(abs(x - mc.width/2)) / (mc.width * 0.5))
						maxY = mc.hmMaxGrain * 2 * (1.0 - float(abs(x - mc.width/2)) / (mc.width * 0.5))
						if sm.averageTempMap[i] > mc.TaigaTemp:
							iceProb *= 0.25
						if sm.terrainMap[i] == mc.COAST:
							iceProb *= 3.00

						if PRand.random() < iceProb and y < maxY:
							plot.setFeatureType(featureIce,0)
				iceChance *= 0.66

			iceChance = mc.TaigaTemp * 2.0
			minY = 0
			for y in range(mc.height - 1,mc.height - mc.hmMaxGrain * 2,-1):
				for x in range(mc.width):
					plot = mmap.plot(x,y)
					i = GetIndex(x,y)
					if plot != 0 and plot.isWater():
						iceProb = iceChance * (1.0 - float(abs(x - mc.width/2)) / (mc.width * 0.5))
						minY = mc.height - mc.hmMaxGrain * 2 * (1.0 - float(abs(x - mc.width/2)) / (mc.width * 0.5))
						if sm.averageTempMap[i] > mc.TaigaTemp:
							iceProb *= 0.25
						if sm.terrainMap[i] == mc.COAST:
							iceProb *= 3.00

						if PRand.random() < iceProb and y > minY:
							plot.setFeatureType(featureIce,0)
				iceChance *= 0.66

		else:
			iceChance = 1.5
			for y in range(mc.height - 1,mc.height - mc.hmMaxGrain,-1):
				for x in range(mc.width):
					plot = mmap.plot(x,y)
					i = GetIndex(x,y)
					if plot != 0 and plot.isWater():
						iceProb = iceChance
						if sm.averageTempMap[i] > mc.TaigaTemp:
							iceProb *= 0.25
						if sm.terrainMap[i] == mc.COAST:
							iceProb *= 2.00

						if PRand.random() < iceProb:
							plot.setFeatureType(featureIce,0)
				iceChance *= 0.66

	#Now forest or jungle
	tries = 0
	ancientForest = False
	if mc.UseAdvancedFeatures:
		while tries < 50 and ancientForest == False:
			tries += 1
			ancientForestRegionX = PRand.randint(int(mc.width * 0.25),int(mc.width * 0.75))
			ancientForestRegionY = PRand.randint(int(mc.height * 0.25),int(mc.height * 0.75))
			i = GetIndex(ancientForestRegionX,ancientForestRegionY)

			goodCount = 0
			for xx in range(ancientForestRegionX - 4, ancientForestRegionX + 4):
				for yy in range(ancientForestRegionY - 4, ancientForestRegionY + 4):
					ii = GetIndex(xx,yy)
					if sm.rainFallMap[ii] > sm.plainsThreshold * 1.5 and sm.averageTempMap[ii] < mc.JungleTemp:
						goodCount += 1
			if goodCount > 6:
				ancientForest = True

	tries = 0
	hauntedForest = False
	if mc.UseAdvancedFeatures and featureHauntedForest != -1:
		while tries < 50 and hauntedForest == False:
			tries += 1
			hauntedForestRegionX = PRand.randint(int(mc.width * 0.25),int(mc.width * 0.75))
			hauntedForestRegionY = PRand.randint(int(mc.height * 0.25),int(mc.height * 0.75))
			i = GetIndex(hauntedForestRegionX,hauntedForestRegionY)

			goodCount = 0
			for xx in range(hauntedForestRegionX - 5, hauntedForestRegionX + 5):
				for yy in range(hauntedForestRegionY - 5, hauntedForestRegionY + 5):
					ii = GetIndex(xx,yy)
					if sm.rainFallMap[ii] > sm.plainsThreshold and sm.rainFallMap[ii] < sm.plainsThreshold * 1.5:
						goodCount += 1
			if goodCount > 6:
				hauntedForest = True

	for y in range(mc.height):
		for x in range(mc.width):
			i = GetIndex(x,y)
			plot = mmap.plot(x,y)
			#forest and jungle
			if plot.isWater() == False and sm.terrainMap[i] != mc.DESERT and\
			plot.isPeak() == False:
				if sm.rainFallMap[i] > sm.plainsThreshold * 1.5 and sm.averageTempMap[i] > mc.JungleTemp:#jungle
					if PRand.random() < mc.jungleChance:
						if sm.terrainMap[i] == mc.PLAINS:
							if PRand.random() < mc.forestChance:
								plot.setFeatureType(featureForest,FORESTLEAFY)
						else:
							plot.setFeatureType(featureJungle,0)
				elif sm.rainFallMap[i] > sm.desertThreshold and PRand.random() < mc.forestChance:#forest
					if sm.rainFallMap[i] > sm.plainsThreshold * 1.5 and ancientForest:
						dist = float(max(abs(x - ancientForestRegionX),abs(y - ancientForestRegionY)) / 4)
						if sm.averageTempMap[i] > mc.ForestTemp:
							if PRand.random() > dist and PRand.random() < mc.forestChance:
								plot.setFeatureType(featureAncientForest,0)
							else:
								plot.setFeatureType(featureForest,FORESTLEAFY)
						elif sm.averageTempMap[i] > mc.TaigaTemp:
							if PRand.random() > dist and PRand.random() < mc.forestChance * 0.75:
								plot.setFeatureType(featureAncientForest,0)
							else:
								plot.setFeatureType(featureForest,FORESTEVERGREEN)
						elif sm.averageTempMap[i] > mc.TundraTemp * 0.8:
							if sm.terrainMap[i] == mc.TAIGA or sm.terrainMap[i] == mc.TUNDRA:
								plot.setFeatureType(featureForest,FORESTSNOWY)
							else:
								plot.setFeatureType(featureForest,FORESTEVERGREEN)
					elif sm.rainFallMap[i] > PRand.random() * sm.plainsThreshold * 1.5 and PRand.random() < mc.forestChance:
						if hauntedForest:
							dist = float(max(abs(x - hauntedForestRegionX),abs(y - hauntedForestRegionY)) / 5)
						if sm.averageTempMap[i] > mc.ForestTemp:
							if hauntedForest and PRand.random() > dist and PRand.random() < mc.forestChance:
								plot.setPlotEffectType(featureHauntedForest)
							else:
								plot.setFeatureType(featureForest,FORESTLEAFY)
						elif sm.averageTempMap[i] > mc.TaigaTemp:
							if hauntedForest and PRand.random() > dist and PRand.random() < mc.forestChance * 0.5:
								plot.setPlotEffectType(featureHauntedForest)
							else:
								plot.setFeatureType(featureForest,FORESTEVERGREEN)
						elif sm.averageTempMap[i] > mc.TundraTemp * 0.8:
							if sm.terrainMap[i] == mc.TAIGA or sm.terrainMap[i] == mc.TUNDRA:
								plot.setFeatureType(featureForest,FORESTSNOWY)
							else:
								plot.setFeatureType(featureForest,FORESTEVERGREEN)

			if mc.UseAdvancedFeatures:
				waterArea = plot.waterArea()
				if plot.isWater() and not waterArea.isLake() and not waterArea.isNone():
					# Place RiFE's reef feature if supported
					noReef = True
					if plot.isWater() and sm.averageTempMap[i] > mc.TaigaTemp * 1.5 and featureReef != -1:
						reefChance = sm.averageTempMap[i] * sm.averageTempMap[i]
						if sm.terrainMap[i] == mc.COAST:
							reefChance *= 0.1
						elif sm.terrainMap[i] == mc.DEEPOCEAN:
							reefChance = 0.0
						elif sm.terrainMap[i] == mc.OCEAN:
							chanceMod = 0.0
							for yy in range(y - 2,y + 2):
								for xx in range(x - 2,x + 2):
									ii = GetIndex(xx,yy)
									surPlot = mmap.plot(xx,yy)
									if not surPlot.isWater():
										chanceMod += 0.1

							reefChance *= chanceMod

						if PRand.random() < reefChance:
							plot.setFeatureType(featureReef,0)
							noReef = False

					# Now we place Kelp for RifE and other mods that include it
					if noReef and plot.isWater() and sm.averageTempMap[i] > mc.TaigaTemp * mc.kelpTemp and featureKelp != -1:
						# Reduce the cap to thin out kelp, increase it to thicken it.
						edgeWeight = min(0.50,EdgeWeight(x,y,mc.width,mc.height))

						kelpTemp = sm.averageTempMap[i] * 0.75
						kelpChance = (edgeWeight + kelpTemp) * 0.4

						if sm.terrainMap[i] == mc.OCEAN:
							if sm.heightMap[i] > hm.seaLevel * mc.kelpDepth:
								kelpChance = (kelpChance + sm.averageTempMap[i]) * (sm.heightMap[i] / hm.seaLevel)
							else:
								kelpChance = 0.0
						elif sm.terrainMap[i] == mc.DEEPOCEAN:
							kelpChance = 0.0

						kelpChance *= mc.kelpChance

						if PRand.random() < kelpChance and PRand.random() < edgeWeight:
							plot.setFeatureType(featureKelp,0)

			if plot.isPeak() == False and plot.isWater() == False:
				if sm.terrainMap[i] in (mc.PLAINS, mc.GRASS) and PRand.random() < mc.chanceForLightForest and sm.plotMap[i] != mc.HILLS:
					plot.setFeatureType(featureLightForest,0)
				if sm.terrainMap[i] == mc.MARSH and PRand.random() < mc.chanceForTreelessMarsh :
					plot.setFeatureType(FeatureTypes.NO_FEATURE,0)
				if sm.terrainMap[i] == mc.TAIGA:
					if plot.isRiver():
						plot.setFeatureType(featureForest,FORESTSNOWY)
					elif PRand.random() < mc.forestChance * 0.5:
						plot.setFeatureType(featureForest,FORESTSNOWY)
				if sm.terrainMap[i] == mc.DESERT:
					if plot.isRiver() and sm.plotMap[i] != mc.HILLS:
						plot.setFeatureType(featureFloodPlains,0)
					else:
						foundNonDesert = False
						for yy in range(y - 2,y + 2):
							for xx in range(x - 2,x + 2):
								ii = GetIndex(xx,yy)
								surPlot = mmap.plot(xx,yy)
								if sm.terrainMap[ii] != mc.DESERT:
									foundNonDesert = True
								elif surPlot == 0:
									foundNonDesert = True
								elif surPlot.isWater():
									foundNonDesert = True
								elif surPlot.getFeatureType() == featureOasis:
									foundNonDesert = True
								elif surPlot.isRiver():
									foundNonDesert
						if sm.plotMap[i] != mc.HILLS:
							if foundNonDesert == False:
								if PRand.random() < 0.20:
									plot.setFeatureType(featureOasis,0)
							elif PRand.random() < 0.20:
								plot.setFeatureType(featureScrub,0)
	return

def addBonuses():
	bp.AddBonuses()
	return

def assignStartingPlots():
	gc = CyGlobalContext()
	gameMap = CyMap()
	iPlayers = gc.getGame().countCivPlayersEverAlive()
	spf.SetStartingPlots()
	return

class StartingPlotFinder :
	def __init__(self):
		self.newWorldID = -1
		return
	def SetStartingPlots(self):
		gc = CyGlobalContext()
		gameMap = CyMap()
		iPlayers = gc.getGame().countCivPlayersEverAlive()
		gameMap.recalculateAreas()
		areas = CvMapGeneratorUtil.getAreas()

		#get old/new world status
		areaOldWorld = self.setupOldWorldAreaList()

		#Shuffle players so the same player doesn't always get the first pick.
		#lifted from Highlands.py that ships with Civ.
		player_list = []
		for plrCheckLoop in range(gc.getMAX_CIV_PLAYERS()):
				if CyGlobalContext().getPlayer(plrCheckLoop).isEverAlive():
						player_list.append(plrCheckLoop)
		shuffledPlayers = []
		for playerLoop in range(iPlayers):
				iChoosePlayer = PRand.randint(0,len(player_list)-1)
				shuffledPlayers.append(player_list[iChoosePlayer])
				del player_list[iChoosePlayer]

		self.startingAreaList = list()
		for i in range(0,len(areas),1):
			if areaOldWorld[i] and areas[i].getNumTiles() > 8:
				startArea = StartingArea(areas[i].getID())
				self.startingAreaList.append(startArea)

		#Get the value of the whole old world
		oldWorldValue = 0
		for i in range(0,len(self.startingAreaList),1):
			oldWorldValue += self.startingAreaList[i].rawValue

		#calulate value per player of old world
		oldWorldValuePerPlayer = oldWorldValue/len(shuffledPlayers)

		#Sort startingAreaList by rawValue
		self.startingAreaList.sort(lambda x, y: cmp(x.rawValue, y.rawValue))

		#Get rid of areas that have less value than oldWorldValuePerPlayer
		#as they are too small to put a player on, however leave at least
		#half as many continents as there are players, just in case the
		#continents are *all* quite small.
		numAreas = max(1,len(self.startingAreaList) - len(shuffledPlayers)/2)
		for i in range(numAreas):
			if self.startingAreaList[0].rawValue < oldWorldValuePerPlayer:
				del self.startingAreaList[0]
			else:
				break #All remaining should be big enough

		#Recalculate the value of the whole old world
		oldWorldValue = 0
		for i in range(0,len(self.startingAreaList),1):
			oldWorldValue += self.startingAreaList[i].rawValue

		#Recalulate value per player of old world so we are starting more
		#accurately
		oldWorldValuePerPlayer = oldWorldValue/len(shuffledPlayers)

		#Record the ideal number of players for each continent
		for startingArea in self.startingAreaList:
			startingArea.idealNumberOfPlayers = int(round(float(startingArea.rawValue)/float(oldWorldValuePerPlayer)))

		#Now we want best first
		self.startingAreaList.reverse()
		print "number of starting areas is %(s)3d" % {"s":len(self.startingAreaList)}

		iterations = 0
		while True:
			iterations += 1
			if iterations > 20:
				raise ValueError, "Too many iterations in starting area choosing loop."
			chosenStartingAreas = list()
			playersPlaced = 0
			#add up idealNumbers
			idealNumbers = 0
			for startingArea in self.startingAreaList:
				idealNumbers += startingArea.idealNumberOfPlayers
			if idealNumbers < len(shuffledPlayers):
				self.startingAreaList[0].idealNumberOfPlayers += 1
			elif idealNumbers > len(shuffledPlayers):
				self.startingAreaList[0].idealNumberOfPlayers -= 1

			#Choose areas
			for startingArea in self.startingAreaList:
				if startingArea.idealNumberOfPlayers + playersPlaced <= len(shuffledPlayers):
					chosenStartingAreas.append(startingArea)
					playersPlaced += startingArea.idealNumberOfPlayers

			#add up idealNumbers again
			idealNumbers = 0
			for startingArea in chosenStartingAreas:
				idealNumbers += startingArea.idealNumberOfPlayers
			if idealNumbers == len(shuffledPlayers):
				break

		for startingArea in chosenStartingAreas:
			for i in range(startingArea.idealNumberOfPlayers):
				startingArea.playerList.append(shuffledPlayers[0])
				del shuffledPlayers[0]
			startingArea.FindStartingPlots()

		if len(shuffledPlayers) > 0:
			raise ValueError,"Some players not placed in starting plot finder!"

		self.plotList = list()
		for startingArea in self.startingAreaList:
			for i in range(0,len(startingArea.plotList),1):
				self.plotList.append(startingArea.plotList[i])
		return

	def setupOldWorldAreaList(self):
		gc = CyGlobalContext()
		gameMap = CyMap()
		#get official areas and make corresponding lists that determines old
		#world vs. new and also the pre-settled value.
		areas = CvMapGeneratorUtil.getAreas()
		areaOldWorld = list()

		cmap = Areamap(mc.width,mc.height,True,True)
		cmap.defineAreas(isSmallWaterMatch)
		newWorldID = cmap.getNewWorldID()

		for i in range(0,len(areas),1):
			for pI in range(mc.height * mc.width):
				plot = gameMap.plotByIndex(pI)
				if plot.getArea() == areas[i].getID():
					if cmap.areaMap[pI] == newWorldID:
						areaOldWorld.append(False)#new world true = old world false
					else:
						areaOldWorld.append(True)
					break
		return areaOldWorld
#Global access
spf = StartingPlotFinder()

class CityPlot :
	def __init__(self,food,value):
		self.food = food
		self.value = value
class Improvement :
	def __init__(self,e,food,production,commerce,value):
		self.e = e
		self.food = food
		self.production = production
		self.commerce = commerce
		self.value = value

class StartingArea :
	def __init__(self,areaID):
		self.areaID = areaID
		self.playerList = list()
		self.plotList = list()
		self.rawValue = 0
		self.CalculatePlotList()
		self.idealNumberOfPlayers = 0
		return

	def getCivPreference(self,civPreferenceList,civType):
		for civPref in civPreferenceList:
			if civPref.civ == civType:
				return civPref
		#None defined so let's make a generic one
		civPref = CivPreference(civType)
		return civPref

	def CalculatePlotList(self):
		gc = CyGlobalContext()
		gameMap = CyMap()
		game = CyGame()
		players = game.countCivPlayersAlive()

		desert = GetInfoType("TERRAIN_DESERT")
		plains = GetInfoType("TERRAIN_PLAINS")
		grass = GetInfoType("TERRAIN_GRASS")
		marsh = GetInfoType("TERRAIN_MARSH")
		tundra = GetInfoType("TERRAIN_TAIGA")
		snow = GetInfoType("TERRAIN_TUNDRA")
		forest = GetInfoType("FEATURE_FOREST")
		jungle = GetInfoType("FEATURE_JUNGLE")

		rawValue = 0

		for y in range(5,mc.height-5):
			for x in range(5,mc.width-5):
				plot = gameMap.plot(x,y)
				if plot.getArea() == self.areaID and not plot.isWater():
					#don't place a city on top of a bonus
					if plot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS:
						continue
					if plot.isPeak(): # Some mods have peaks with a possitive value here
						continue
					desertValue = 0
					plainsValue = 0
					grassValue = 0
					marshValue = 0
					taigaValue = 0
					tundraValue = 0
					hillValue = 0
					peakValue = 0
					forestValue = 0
					jungleValue = 0
					coastValue = 0
					bonusValue = 0
					northValue = float(y / mc.height)
					westValue = float(x / mc.width)
					edgeValue = EdgeWeight(x,y,mc.width,mc.height)

					for xx in range(x-2,x+2):
						for yy in range(y-2,y+2):
							tPlot = gameMap.plot(xx,yy)
							feature = tPlot.getFeatureType()
							terrain = tPlot.getTerrainType()
							bonusEnum = plot.getBonusType(TeamTypes.NO_TEAM)
							bonusInfo = gc.getBonusInfo(bonusEnum)

							if tPlot.isWater():
								coastValue += 1
								if bonusInfo != None:
									bonusValue += 1
								continue
							if tPlot.isPeak():
								peakValue += 1
								continue

							rawValue += 1

							if bonusInfo != None:
								bonusValue += 2
								rawValue += 1
								# Double the value for resources that can be used right away
								if (gc.getTechInfo(bonusInfo.getTechCityTrade()) == None or gc.getTechInfo(bonusInfo.getTechCityTrade()).getEra() <= game.getStartEra()):
									bonusValue += 2
									rawValue += 1

							if tPlot.isHills():
								hillValue += 1

							if terrain == desert:
								if tPlot.isRiverSide():
									desertValue += 2
								else:
									desertValue += 1
								continue

							if feature == forest:
								forestValue += 1
							elif feature == jungle:
								jungleValue += 1

							if terrain == plains:
								if tPlot.isRiverSide():
									plainsValue += 2
								else:
									plainsValue += 1
								continue
							if terrain == grass:
								grassValue += 1
							if terrain == marsh:
								marshValue += 1
								continue
							if terrain == tundra:
								taigaValue += 1
								continue
							if terrain == snow:
								tundraValue += 1

					startPlot = StartPlot(x,y,desertValue,plainsValue,grassValue,marshValue,taigaValue,tundraValue,hillValue,peakValue,forestValue,jungleValue,coastValue,bonusValue,northValue,westValue,edgeValue)
					self.plotList.append(startPlot)
		self.rawValue += rawValue
		return
	def FindStartingPlots(self):
		gc = CyGlobalContext()
		gameMap = CyMap()
		multiplayer = CyGame().isNetworkMultiPlayer()

		numPlayers = len(self.playerList)
		plotCount = len(self.plotList)
		killPlots = list()
		shuffledPlots = list()

		if numPlayers <= 0 or plotCount < numPlayers:
			return

		desert = GetInfoType("TERRAIN_DESERT")
		plains = GetInfoType("TERRAIN_PLAINS")
		grass = GetInfoType("TERRAIN_GRASS")
		marsh = GetInfoType("TERRAIN_MARSH")
		tundra = GetInfoType("TERRAIN_TAIGA")
		snow = GetInfoType("TERRAIN_TUNDRA")

		# Varying distance preferences based on world size and cohesion
		worldsizes = {
			WorldSizeTypes.WORLDSIZE_DUEL:      [7,6,5],
			WorldSizeTypes.WORLDSIZE_TINY:      [7,6,5],
			WorldSizeTypes.WORLDSIZE_SMALL:     [8,7,6],
			WorldSizeTypes.WORLDSIZE_STANDARD:  [8,7,6],
			WorldSizeTypes.WORLDSIZE_LARGE:     [9,8,7],
			WorldSizeTypes.WORLDSIZE_HUGE:      [9,8,7],
			WorldSizeTypes.WORLDSIZE_HUGER:      [10,9,8]
			}
#FlavourMod: Added by Jean Elcard 02/26/2009
		if hasattr(WorldSizeTypes, "WORLDSIZE_GIANT"):
			worldsizes[WorldSizeTypes.WORLDSIZE_GIANT] = [10,9,8]

		grain_list = worldsizes[gameMap.getWorldSize()]
		grain = grain_list[gameMap.getCustomMapOption(0)]

		for i in range(0,len(self.plotList)-1):
			killPlots.append(False)

		plotsLeft = len(self.plotList)-1

		print "%(p)2d plots available for %(s)2d starting plots" % {"p":plotCount,"s":numPlayers}
		print "%(g)2d tile seperation grain" % {"g":grain}

		#Now place all starting positions
		shuffledPlots = sorted( self.plotList, key=lambda x: PRand.random() )

		civPreferenceList = GetCivPreferences()

		for n in range(numPlayers):
			bestSpot = -1
			bestValue = 20

			playerID = self.playerList[n]
			player = gc.getPlayer(playerID)
			civType = player.getCivilizationType()
			civInfo = gc.getCivilizationInfo(civType)
			civPref = self.getCivPreference(civPreferenceList,civType)

			if grain > plotsLeft / (numPlayers - n):
				grain = int(plotsLeft / (numPlayers - n))
				print "Adjusting grain: %(g)2d tile seperation grain" % {"g":grain}

			for m in range(0,len(shuffledPlots)-1):
				value = 0.0
				if shuffledPlots[m].vacant and not killPlots[m]:
					x = shuffledPlots[m].x
					y = shuffledPlots[m].y

					sPlot = gameMap.plot(shuffledPlots[m].x,shuffledPlots[m].y)
					if sPlot.isWater():
						raise ValueError, "Start plot is water!"

					if civPref.needCoastalStart and not isCoast(sPlot):
						continue

					if sPlot.isRiver(): #small bonus for river starts
						if sPlot.getTerrainType() == desert and civPref.desertValue > 0:
							value += civPref.desertValue * 2
						elif sPlot.getTerrainType() == plains and civPref.plainsValue > 0:
							value += civPref.plainsValue * 2
						elif sPlot.getTerrainType() == grass and civPref.grassValue > 0:
							value += civPref.grassValue * 2
						elif sPlot.getTerrainType() == marsh and civPref.marshValue > 0:
							value += civPref.marshValue * 2
						elif sPlot.getTerrainType() == tundra and civPref.taigaValue > 0:
							value += civPref.taigaValue * 2
						elif sPlot.getTerrainType() == snow and civPref.tundraValue > 0:
							value += civPref.tundraValue * 2

					if not civPref.needCoastalStart:
						value -= shuffledPlots[m].coastValue

					value += shuffledPlots[m].desertValue * civPref.desertValue
					value += shuffledPlots[m].plainsValue * civPref.plainsValue
					value += shuffledPlots[m].grassValue * civPref.grassValue
					value += shuffledPlots[m].marshValue * civPref.marshValue
					value += shuffledPlots[m].taigaValue * civPref.taigaValue
					value += shuffledPlots[m].tundraValue * civPref.tundraValue
					value += shuffledPlots[m].forestValue * civPref.forestValue
					value += shuffledPlots[m].jungleValue * civPref.jungleValue
					value += shuffledPlots[m].hillValue * civPref.hillValue
					value += shuffledPlots[m].bonusValue
					northMod = 1 + shuffledPlots[m].northValue * civPref.northValue
					westMod = 1 + shuffledPlots[m].westValue * civPref.westValue
					if multiplayer:
						edgeMod = 1 + shuffledPlots[m].edgeValue * (civPref.edgeValue - 1)
					else:
						edgeMod = 1 + shuffledPlots[m].edgeValue * civPref.edgeValue

					valueMod = northMod * westMod * edgeMod

					value *= valueMod
					if value > bestValue:
						bestValue = int(value)
						bestSpot = m

			if bestSpot == -1:
				print "Player %(p)2d second attempt" % {"p":playerID}
				#Try one more time, with less strict rules
				bestValue = 0
				for m in range(0,len(shuffledPlots)-1):
					value = 0.0
					if shuffledPlots[m].vacant and not killPlots[m]:
						x = shuffledPlots[m].x
						y = shuffledPlots[m].y

						sPlot = gameMap.plot(shuffledPlots[m].x,shuffledPlots[m].y)
						if sPlot.isWater():
							raise ValueError, "Start plot is water!"

						if sPlot.isRiver(): #small bonus for river starts
							if sPlot.getTerrainType() == desert and civPref.desertValue > 0:
								value += civPref.desertValue * 4
							elif sPlot.getTerrainType() == plains and civPref.plainsValue > 0:
								value += civPref.plainsValue * 4
							elif sPlot.getTerrainType() == grass and civPref.grassValue > 0:
								value += civPref.grassValue * 4
							elif sPlot.getTerrainType() == marsh and civPref.marshValue > 0:
								value += civPref.marshValue * 4
							elif sPlot.getTerrainType() == tundra and civPref.taigaValue > 0:
								value += civPref.taigaValue * 4
							elif sPlot.getTerrainType() == snow and civPref.tundraValue > 0:
								value += civPref.tundraValue * 4

						value += shuffledPlots[m].desertValue * civPref.desertValue
						value += shuffledPlots[m].plainsValue * civPref.plainsValue
						value += shuffledPlots[m].grassValue * civPref.grassValue
						value += shuffledPlots[m].marshValue * civPref.marshValue
						value += shuffledPlots[m].taigaValue * civPref.taigaValue
						value += shuffledPlots[m].tundraValue * civPref.tundraValue
						value += shuffledPlots[m].forestValue * civPref.forestValue
						value += shuffledPlots[m].jungleValue * civPref.jungleValue
						value += shuffledPlots[m].hillValue * civPref.hillValue
						value += shuffledPlots[m].bonusValue
						northMod = 1 + shuffledPlots[m].northValue * civPref.northValue
						westMod = 1 + shuffledPlots[m].westValue * civPref.westValue
						if CyGame().isNetworkMultiPlayer():
							edgeMod = 1 + shuffledPlots[m].edgeValue * (civPref.edgeValue - 1)
						else:
							edgeMod = 1 + shuffledPlots[m].edgeValue * civPref.edgeValue

						valueMod = northMod * westMod * edgeMod

						value *= valueMod
						if value > bestValue:
							bestValue = int(value)
							bestSpot = m
			if bestSpot == -1:
				print "Player %(p)2d starting plot forced" % {"p":playerID}
				#ok, now I give up :)
				for m in range(0,len(shuffledPlots)-1):
					if shuffledPlots[m].vacant and not killPlots[m]:
						bestSpot = m
						bestValue = -1

			y = shuffledPlots[bestSpot].y
			x = shuffledPlots[bestSpot].x

			for p in range(0,len(shuffledPlots)-1):
				distance = max(abs(x - shuffledPlots[p].x),abs(y - shuffledPlots[p].y))
				killRange = grain - civPref.neighborValue

				if distance <= killRange and not killPlots[p]:
					killPlots[p] = True
					plotsLeft -= 1

			print "Player %(p)2d starting plot %(s)2d value is %(v)2d" % {"p":playerID,"s":bestSpot,"v":bestValue}
			print "%(p)2d plots remaining" % {"p":plotsLeft}

			sPlot = gameMap.plot(shuffledPlots[bestSpot].x,shuffledPlots[bestSpot].y)
			sPlot.setImprovementType(GetInfoType("NO_IMPROVEMENT"))
			sPlot.setStartingPlot(True)
			player.setStartingPlot(sPlot,True)
			shuffledPlots[bestSpot].vacant = False

		#at this point we can clean up the plot list
		i = 0
		while i < len(self.plotList):
			if self.plotList[i].vacant:
				del self.plotList[i]
			else:
				i += 1

		print "%(p)2d plots remaining after clean-up" % {"p":len(self.plotList)}

		return

	def getDistance(self,x,y,dx,dy):
		xx = x - dx
		if abs(xx) > mc.width/2:
			xx = mc.width - abs(xx)

		distance = max(abs(xx),abs(y - dy))
		return distance

class StartPlot :
	def __init__(self,x,y,desertValue,plainsValue,grassValue,marshValue,taigaValue,tundraValue,hillValue,peakValue,forestValue,jungleValue,coastValue,bonusValue,northValue,westValue,edgeValue):
		self.x = x
		self.y = y
		self.desertValue = desertValue
		self.plainsValue = plainsValue
		self.grassValue = grassValue
		self.marshValue = marshValue
		self.taigaValue = taigaValue
		self.tundraValue = tundraValue
		self.hillValue = hillValue
		self.peakValue = peakValue
		self.forestValue = forestValue
		self.jungleValue = jungleValue
		self.coastValue = coastValue
		self.bonusValue = bonusValue
		self.northValue = northValue
		self.westValue = westValue
		self.edgeValue = edgeValue
		self.vacant = True
		return
	def isCoast(self):
		gameMap = CyMap()
		plot = gameMap.plot(self.x,self.y)
		waterArea = plot.waterArea()
		if waterArea.isNone() or waterArea.isLake():
			return False
		return True
	def plot(self):
		gameMap = CyMap()
		return gameMap.plot(self.x,self.y)
	def copy(self):
		cp = StartPlot(self,x,y,desertValue,plainsValue,grassValue,marshValue,taigaValue,tundraValue,hillValue,peakValue,forestValue,jungleValue,coastValue,bonusValue,northValue,westValue,edgeValue)
		cp.totalValue = self.totalValue
		cp.numberOfOwnedCities = self.numberOfOwnedCities
		cp.distanceToOwner = self.distanceToOwner
		cp.nearestStart = self.nearestStart
		cp.vacant = self.vacant
		cp.owner = self.owner
		cp.avgDistance = self.avgDistance
		return cp
	def __str__(self):
		linestring = "x=%(x)3d,y=%(y)3d,localValue=%(lv)6d,totalValue =%(tv)6d, nearestStart=%(ad)6d, coastalCity=%(cc)d" % \
		{"x":self.x,"y":self.y,"lv":self.localValue,"tv":self.totalValue,"ad":self.nearestStart,"cc":self.isCoast()}
		return linestring

class CivPreference :
	def __init__(self,civ):
		self.civ = civ
		self.desertValue = -1 #value per plot by terrain type
		self.plainsValue = 1
		self.grassValue = 2
		self.marshValue = -1
		self.taigaValue = -1
		self.tundraValue = -2
		self.hillValue = 0 #Hill, peak, forest & jungle value adds to terrain value
		self.peakValue = 0
		self.forestValue = 0
		self.jungleValue = 0
		self.neighborValue = 0 #positive values decrease the min range of nearby starts
		self.needCoastalStart = False
		self.northValue = 0 # recommeded values -1 (south), 0 (neither), 1 (north)
		self.westValue = 0
		self.edgeValue = 0 # 0 = don't care, 1 = outer edge, -1 = towards center
		return

# Notes on Civ Preferences:
#
# neighborValue is added to the distance calculation when determining which starting
# plots to kill (prevent others from using).  It does not scale with map size so
# you need to be careful with excessively high (or negative) numbers.  A safe range
# for all maps sizes is -2 to +2, you can get away with a larger range if few civs
# use negative values.
#
# The terrain values should be self explanatory, higher numbers encourage the civ
# to pick a starting plot with the same terrain(s).  The hill, peak, forest and
# jungle vlaues are added to the terrain value per plot.  So a preference for
# grassland AND jungle will stack in most cases since most jungles are on grass.
# These preference values are also used when cleaning up the starting plots, a
# positive value for forests and jungles will prevent them from being cut and
# a positive value for hills will reverse the cut process causing a few hills to
# be removed but preserving the ones closest to the 'city' plot.  Peaks always
# have the same 33% chance of being downgraded to hills regardless of preference.
#
# Civs with needCoastalStart set to True will reject any starting locations not
# on a coast.  This can result in no valid plots being available in which case
# they will select one randomly (it will be usually be bad).
#
# Adding multiplayer versions of civ preferences can be done by copying the code
# used by the Illians and Doviello, using CyGame().isNetworkMultiPlayer() does
# not detect hotseat games.


def GetCivPreferences():
	multiplayer = CyGame().isNetworkMultiPlayer()
##  Civs without preferences will use default values.
	civPreferenceList = list()


# Base FfH2 Civs
	pref = CivPreference(GetInfoType("CIVILIZATION_MALAKIM"))
	pref.desertValue = 2
	pref.plainsValue = 1
	pref.grassValue = -2
	pref.marshValue = -2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 0
	pref.peakValue = -2
	pref.forestValue = -1
	pref.jungleValue = -2
	pref.neighborValue = 0
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 0
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_LANUN"))
	pref.desertValue = -1
	pref.plainsValue = 1
	pref.grassValue = 2
	pref.marshValue = -2
	pref.taigaValue = -1
	pref.tundraValue = -2
	pref.hillValue = 0
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = 0
	pref.neighborValue = 0
	pref.needCoastalStart = True
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 1
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_DOVIELLO"))
	if multiplayer: # Don't burry them in the tundra for mp games
		pref.desertValue = -2
		pref.plainsValue = 1
		pref.grassValue = 2
		pref.marshValue = -2
		pref.taigaValue = 1
		pref.tundraValue = 0
		pref.hillValue = 0
		pref.peakValue = 0
		pref.forestValue = 0
		pref.jungleValue = -2
		pref.neighborValue = 2
		pref.needCoastalStart = False
		pref.northValue = 2
		pref.westValue = 0
		pref.edgeValue = 0
	else:
		pref.desertValue = -2
		pref.plainsValue = 1
		pref.grassValue = 1
		pref.marshValue = -2
		pref.taigaValue = 2
		pref.tundraValue = 2
		pref.hillValue = 0
		pref.peakValue = 0
		pref.forestValue = 0
		pref.jungleValue = -2
		pref.neighborValue = 2
		pref.needCoastalStart = False
		pref.northValue = 1
		pref.westValue = 0
		pref.edgeValue = 0
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_ILLIANS"))
	if multiplayer: #don't bury them in the snow and let other civs start closer in mp games
		pref.desertValue = -1
		pref.plainsValue = 2
		pref.grassValue = 1
		pref.marshValue = -2
		pref.taigaValue = 1
		pref.tundraValue = 0
		pref.hillValue = 0
		pref.peakValue = 0
		pref.forestValue = 0
		pref.jungleValue = -2
		pref.neighborValue = 1
		pref.needCoastalStart = False
		pref.northValue = 2
		pref.westValue = 0
		pref.edgeValue = 0
	else:
		pref.desertValue = -1
		pref.plainsValue = 0
		pref.grassValue = -1
		pref.marshValue = -2
		pref.taigaValue = 3
		pref.tundraValue = 3
		pref.hillValue = 0
		pref.peakValue = 0
		pref.forestValue = 0
		pref.jungleValue = -2
		pref.neighborValue = 0
		pref.needCoastalStart = False
		pref.northValue = 1
		pref.westValue = 0
		pref.edgeValue = 0
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_KHAZAD"))
	pref.desertValue = -1
	pref.plainsValue = 2
	pref.grassValue = 1
	pref.marshValue = -2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 2
	pref.peakValue = 2
	pref.forestValue = 0
	pref.jungleValue = -2
	pref.neighborValue = 0
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 0
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_LUCHUIRP"))
	pref.desertValue = -1
	pref.plainsValue = 2
	pref.grassValue = 1
	pref.marshValue = -2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 2
	pref.peakValue = 2
	pref.forestValue = 0
	pref.jungleValue = -2
	pref.neighborValue = 0
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 0
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_KURIOTATES"))
	pref.desertValue = -2
	pref.plainsValue = 0
	pref.grassValue = 2
	pref.marshValue = -2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 0
	pref.peakValue = -2
	pref.forestValue = 0
	pref.jungleValue = -2
	pref.neighborValue = -1
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 0
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_LJOSALFAR"))
	pref.desertValue = -2
	pref.plainsValue = 0
	pref.grassValue = 3
	pref.marshValue = -2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 0
	pref.peakValue = 0
	pref.forestValue = 2
	pref.jungleValue = -2
	pref.neighborValue = 0
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 0
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_SVARTALFAR"))
	pref.desertValue = -2
	pref.plainsValue = 0
	pref.grassValue = 3
	pref.marshValue = -2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 0
	pref.peakValue = 0
	pref.forestValue = 2
	pref.jungleValue = -2
	pref.neighborValue = 1
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = -1
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_SIDAR"))
	pref.desertValue = -1
	pref.plainsValue = 0
	pref.grassValue = 2
	pref.marshValue = -2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 0
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = -2
	pref.neighborValue = -2
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 1
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_HIPPUS"))
	pref.desertValue = 0
	pref.plainsValue = 2
	pref.grassValue = 1
	pref.marshValue = -2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 0
	pref.peakValue = -2
	pref.forestValue = 0
	pref.jungleValue = -2
	pref.neighborValue = 1
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = -1
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_CLAN_OF_EMBERS"))
	pref.desertValue = -2
	pref.plainsValue = -1
	pref.grassValue = 2
	pref.marshValue = -2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 0
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = 0
	pref.neighborValue = 2
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = -1
	civPreferenceList.append(pref)

# RifE Civs
	pref = CivPreference(GetInfoType("CIVILIZATION_AUSTRIN"))
	pref.desertValue = 0
	pref.plainsValue = 1
	pref.grassValue = 1
	pref.marshValue = 0
	pref.taigaValue = 1
	pref.tundraValue = 0
	pref.hillValue = 0
	pref.peakValue = 0
	pref.forestValue = -1
	pref.jungleValue = -1
	pref.neighborValue = -2
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 1
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_ARCHOS"))
	pref.desertValue = 0
	pref.plainsValue = 1
	pref.grassValue = 1
	pref.marshValue = 0
	pref.taigaValue = -1
	pref.tundraValue = -2
	pref.hillValue = 1
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = 0
	pref.neighborValue = 1
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = -1
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_DURAL"))
	pref.desertValue = 0
	pref.plainsValue = 1
	pref.grassValue = 0
	pref.marshValue = 0
	pref.taigaValue = -1
	pref.tundraValue = -2
	pref.hillValue = 2
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = 0
	pref.neighborValue = 0
	pref.needCoastalStart = True
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 0
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_CHISLEV"))
	pref.desertValue = 0
	pref.plainsValue = 2
	pref.grassValue = 1
	pref.marshValue = -1
	pref.taigaValue = 0
	pref.tundraValue = -1
	pref.hillValue = 0
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = -1
	pref.neighborValue = -1
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 0
	civPreferenceList.append(pref)


	pref = CivPreference(GetInfoType("CIVILIZATION_CUALLI"))
	pref.desertValue = -2
	pref.plainsValue = -2
	pref.grassValue = 1
	pref.marshValue = 2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 0
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = 2
	pref.neighborValue = 1
	pref.needCoastalStart = False
	pref.northValue = -1
	pref.westValue = 0
	pref.edgeValue = -1
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_MAZATL"))
	pref.desertValue = -2
	pref.plainsValue = -2
	pref.grassValue = 1
	pref.marshValue = 2
	pref.taigaValue = -2
	pref.tundraValue = -2
	pref.hillValue = 0
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = 2
	pref.neighborValue = -1
	pref.needCoastalStart = False
	pref.northValue = -1
	pref.westValue = 0
	pref.edgeValue = 1
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_JOTNAR"))
	if multiplayer: # Don't burry them in the tundra for mp games
		pref.desertValue = -2
		pref.plainsValue = 1
		pref.grassValue = 2
		pref.marshValue = -2
		pref.taigaValue = 1
		pref.tundraValue = 0
		pref.hillValue = 1
		pref.peakValue = 1
		pref.forestValue = 0
		pref.jungleValue = -2
		pref.neighborValue = 0
		pref.needCoastalStart = False
		pref.northValue = 2
		pref.westValue = 0
		pref.edgeValue = 0
	else:
		pref.desertValue = 0
		pref.plainsValue = 1
		pref.grassValue = 1
		pref.marshValue = -2
		pref.taigaValue = 2
		pref.tundraValue = 1
		pref.hillValue = 1
		pref.peakValue = 1
		pref.forestValue = 0
		pref.jungleValue = -2
		pref.neighborValue = 0
		pref.needCoastalStart = True
		pref.northValue = 1
		pref.westValue = 0
		pref.edgeValue = 0
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_DTESH"))
	pref.desertValue = 2
	pref.plainsValue = 0
	pref.grassValue = -2
	pref.marshValue = -2
	pref.taigaValue = 0
	pref.tundraValue = -2
	pref.hillValue = 1
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = -2
	pref.neighborValue = 1
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = -1
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_MECHANOS"))
	pref.desertValue = 1
	pref.plainsValue = 1
	pref.grassValue = 1
	pref.marshValue = 1
	pref.taigaValue = 1
	pref.tundraValue = 1
	pref.hillValue = 2
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = 0
	pref.neighborValue = 0
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 0
	civPreferenceList.append(pref)

	pref = CivPreference(GetInfoType("CIVILIZATION_SCIONS"))
	pref.desertValue = 2
	pref.plainsValue = 0
	pref.grassValue = -2
	pref.marshValue = -2
	pref.taigaValue = 0
	pref.tundraValue = -2
	pref.hillValue = 2
	pref.peakValue = 0
	pref.forestValue = 0
	pref.jungleValue = -2
	pref.neighborValue = 0
	pref.needCoastalStart = False
	pref.northValue = 0
	pref.westValue = 0
	pref.edgeValue = 0
	civPreferenceList.append(pref)

#added wildmana
	pref = CivPreference(GetInfoType("CIVILIZATION_FAERIES"))
	pref.desertValue = -2
	pref.plainsValue = 1
	pref.grassValue = 2
	pref.marshValue = -2
	pref.taigaValue = 1
	pref.tundraValue = 0
	pref.hillValue = -1
	pref.peakValue = -2
	pref.forestValue = 2
	pref.jungleValue = -2
	pref.neighborValue = 0
	pref.needCoastalStart = False
	pref.northValue = 1
	pref.westValue = 0
	pref.edgeValue = 0
	civPreferenceList.append(pref)
#wildmana end

	return civPreferenceList

class BonusPlacer :
	def __init__(self):
		return
	def AddBonuses(self):
		gc = CyGlobalContext()
		gameMap = CyMap()
		gameMap.recalculateAreas()
		self.AssignBonusAreas()
		numBonuses = gc.getNumBonusInfos()
		for order in range(numBonuses):
			for i in range(numBonuses):
				bonusInfo = gc.getBonusInfo(self.bonusList[i].eBonus)
				if bonusInfo.getPlacementOrder() == order:
					self.AddBonusType(self.bonusList[i].eBonus)#Both unique and non-unique bonuses

		#now check to see that all resources have been placed at least once, this
		#pass ignoring area rules
		for i in range(numBonuses):
			bonus = self.bonusList[i]
			if bonus.currentBonusCount == 0 and bonus.desiredBonusCount > 0:
				self.AddEmergencyBonus(bonus,False)

		#now check again to see that all resources have been placed at least once,
		#this time ignoring area rules and also class spacing
		for i in range(numBonuses):
			bonus = self.bonusList[i]
			if bonus.currentBonusCount == 0 and bonus.desiredBonusCount > 0:
				self.AddEmergencyBonus(bonus,True)

		#now report resources that simply could not be placed
		for i in range(numBonuses):
			bonus = self.bonusList[i]
			if bonus.currentBonusCount == 0 and bonus.desiredBonusCount > 0:
				bonusInfo = gc.getBonusInfo(bonus.eBonus)
				print "No room at all found for %(bt)s!!!" % {"bt":bonusInfo.getType()}
		return
	def AddEmergencyBonus(self,bonus,ignoreClass):
		gc = CyGlobalContext()
		gameMap = CyMap()

		featureForest = GetInfoType("FEATURE_FOREST")
		plotIndexList = list()
		for i in range(mc.width*mc.height):
			plotIndexList.append(i)
		plotIndexList = ShuffleList(plotIndexList)
		bonusInfo = gc.getBonusInfo(bonus.eBonus)
		for i in range(0,len(plotIndexList),1):
			index = plotIndexList[i]
			plot = gameMap.plotByIndex(index)
			x = plot.getX()
			y = plot.getY()
			if (ignoreClass and self.PlotCanHaveBonus(plot,bonus.eBonus,False,True)) or \
			self.CanPlaceBonusAt(plot,bonus.eBonus,False,True):
				#temporarily remove any feature
				featureEnum = plot.getFeatureType()
				if featureEnum == featureForest:
					featureVariety = plot.getFeatureVariety()
					plot.setFeatureType(FeatureTypes.NO_FEATURE,-1)
				#place bonus
				plot.setBonusType(bonus.eBonus)
				bonus.currentBonusCount += 1
				#restore the feature if possible
				if featureEnum == featureForest:
					if bonusInfo == None or bonusInfo.isFeature(featureEnum):
						plot.setFeatureType(featureEnum,featureVariety)
				print "Emergency placement of 1 %(bt)s" % {"bt":bonusInfo.getType()}
				break

		return
	def AddBonusType(self,eBonus):
		gc = CyGlobalContext()
		gameMap = CyMap()

		featureForest = GetInfoType("FEATURE_FOREST")
		#first get bonus/area link
		for i in range(gc.getNumBonusInfos()):
			if self.bonusList[i].eBonus == eBonus:
				bonus = self.bonusList[i]
		bonus.currentBonusCount = 0
		bonusInfo = gc.getBonusInfo(eBonus)
		if bonus.desiredBonusCount <= 0:#Non map bonuses?
			print "Desired bonus count for %(bt)s is zero, so none will be placed." % {"bt":bonusInfo.getType()}
			return
		#Create a list of map indices and shuffle them
		preshuffle = list()
		plotIndexList = list()
		for i in range(mc.width*mc.height):
			preshuffle.append(i)
		for i in range(mc.width*mc.height):
			preshufflength = len(preshuffle)
			randIndex = PRand.randint(1,preshufflength) - 1
			if randIndex < 0 or randIndex >= len(preshuffle):
				raise ValueError, " bad index shuffling plot list randIndex=%(r)d listLength=%(l)d, mapSize=%(s)d" % {"r":randIndex,"l":len(preshuffle),"s":mc.width*mc.height}
			if preshufflength != len(preshuffle):
				raise ValueError, "preshufflength != len(preshuffle) preshufflength=%(r)d listLength=%(l)d" % {"r":preshufflength,"l":len(preshuffle)}
			plotIndexList.append(preshuffle[randIndex])
			del preshuffle[randIndex]
			if len(preshuffle) == 0:
				break
		print "Trying to place %(n)d of %(bt)s" % {"n":bonus.desiredBonusCount,"bt":bonusInfo.getType()}
		#now add bonuses
		for i in range(0,len(plotIndexList),1):
			index = plotIndexList[i]
			plot = gameMap.plotByIndex(index)
			x = plot.getX()
			y = plot.getY()
			if self.CanPlaceBonusAt(plot,eBonus,False,False):
				#temporarily remove any feature
				featureEnum = plot.getFeatureType()
				if featureEnum == featureForest:
					featureVariety = plot.getFeatureVariety()
					plot.setFeatureType(FeatureTypes.NO_FEATURE,-1)
				#place bonus
				plot.setBonusType(eBonus)
				bonus.currentBonusCount += 1
				#restore the feature if possible
				if featureEnum == featureForest:
					if bonusInfo == None or bonusInfo.isFeature(featureEnum) or (bonusInfo.getTechReveal() != TechTypes.NO_TECH):
						plot.setFeatureType(featureEnum,featureVariety)
				groupRange = bonusInfo.getGroupRange()
				for dx in range(-groupRange,groupRange + 1):
					for dy in range(-groupRange,groupRange + 1):
						if bonus.currentBonusCount < bonus.desiredBonusCount:
							loopPlot = self.plotXY(x,y,dx,dy)
							if loopPlot != None:
								if loopPlot.getX() == -1:
									raise ValueError, "plotXY returns invalid plots plot= %(x)d, %(y)d" % {"x":x,"y":y}
								if self.CanPlaceBonusAt(loopPlot,eBonus,False,False):
									if PRand.randint(0,99) < bonusInfo.getGroupRand():
										#temporarily remove any feature
										featureEnum = loopPlot.getFeatureType()
										if featureEnum == featureForest:
											featureVariety = loopPlot.getFeatureVariety()
											loopPlot.setFeatureType(FeatureTypes.NO_FEATURE,-1)
										#place bonus
										loopPlot.setBonusType(eBonus)
										bonus.currentBonusCount += 1
										#restore the feature if possible
										if featureEnum == featureForest:
											if bonusInfo == None or bonusInfo.isFeature(featureEnum) or (bonusInfo.getTechReveal() != TechTypes.NO_TECH):
												loopPlot.setFeatureType(featureEnum,featureVariety)
			if bonus.currentBonusCount == bonus.desiredBonusCount:
				break
		if bonus.currentBonusCount < bonus.desiredBonusCount:
			print "Could not place %(n)d of %(bt)s" % {"n":bonus.desiredBonusCount - bonus.currentBonusCount,"bt":bonusInfo.getType()}
		else:
			print "Successfully placed %(n)d of %(bt)s" % {"n":bonus.desiredBonusCount,"bt":bonusInfo.getType()}
		return
	def plotXY(self,x,y,dx,dy):
		gameMap = CyMap()
		#The one that civ uses will return junk so I have to make one
		#that will not
		x = (x + dx) % mc.width
		y = y + dy
		if y < 0 or y > mc.height - 1:
			return None
		return gameMap.plot(x,y)

	def AssignBonusAreas(self):
		gc = CyGlobalContext()
		self.areas = CvMapGeneratorUtil.getAreas()
		gameMap = CyMap()
		preShuffledBonusList = list()
		self.bonusList = list()
		#Create and shuffle the bonus list and keep tally on
		#one-area bonuses and find the smallest min area requirement
		#among those
		numUniqueBonuses = 0
		minLandAreaSize = -1
		for i in range(gc.getNumBonusInfos()):
			bonus = BonusArea()
			bonus.eBonus = i
			preShuffledBonusList.append(bonus)
			bonusInfo = gc.getBonusInfo(i)
			if bonusInfo.isOneArea():
				numUniqueBonuses += 1
				minAreaSize = max(9,bonusInfo.getMinAreaSize())
				if (minLandAreaSize == -1 or minLandAreaSize > minAreaSize) and \
				minAreaSize > 0:
					minLandAreaSize = minAreaSize
		for i in range(gc.getNumBonusInfos()):
			iChooseBonus = PRand.randint(0,len(preShuffledBonusList)-1)
			self.bonusList.append(preShuffledBonusList[iChooseBonus])
			del preShuffledBonusList[iChooseBonus]
		numBonuses = gc.getNumBonusInfos()
		for i in range(numBonuses):
			self.bonusList[i].desiredBonusCount = self.CalculateNumBonusesToAdd(self.bonusList[i].eBonus)
			bonusInfo = gc.getBonusInfo(self.bonusList[i].eBonus)
			eBonus = self.bonusList[i].eBonus
			if bonusInfo.isOneArea() == False:
				continue #Only assign areas to area bonuses
##            print "Trying to find room for %(bt)s, desiredCount=%(dc)d" % {"bt":bonusInfo.getType(),"dc":self.bonusList[i].desiredBonusCount}
			areaSuitabilityList = list()
			for area in self.areas:
				if area.getNumTiles() >= minLandAreaSize:
					aS = AreaSuitability(area.getID())
					aS.suitability,aS.numPossible = self.CalculateAreaSuitability(area,eBonus)
					areaSuitabilityList.append(aS)
##                    print "suitability on areaID=%(aid)d, size=%(s)d is %(r)f" % \
##                    {"aid":area.getID(),"s":area.getNumTiles(),"r":aS.suitability}
			#Calculate how many areas to assign (numUniqueBonuses will be > 0 if we get here)
##            areasPerBonus = (len(areaSuitabilityList)/numUniqueBonuses) + 1
			areasPerBonus = len(areaSuitabilityList)
			#Sort areaSuitabilityList best first
			areaSuitabilityList.sort(lambda x,y:cmp(x.numPossible,y.numPossible))
			areaSuitabilityList.reverse()
			#assign the best areas to this bonus
			for n in range(areasPerBonus):
				self.bonusList[i].areaList.append(areaSuitabilityList[n].areaID)
			#assign areas that have a high suitability also
			for n in range(areasPerBonus,len(areaSuitabilityList)):
				if areaSuitabilityList[n].suitability > 0.3:
					self.bonusList[i].areaList.append(areaSuitabilityList[n].areaID)
		return
	def CanPlaceBonusAt(self,plot,eBonus,bIgnoreLatitude,bIgnoreArea):
		gc = CyGlobalContext()
		gameMap = CyMap()
		x = plot.getX()
		y = plot.getY()
		areaID = plot.getArea()
		if self.PlotCanHaveBonus(plot,eBonus,bIgnoreLatitude,bIgnoreArea) == False:
			return False
		for i in range(DirectionTypes.NUM_DIRECTION_TYPES):
			loopPlot = plotDirection(x,y,DirectionTypes(i))
			if loopPlot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS and loopPlot.getBonusType(TeamTypes.NO_TEAM) != eBonus:
			   return False

		bonusInfo = gc.getBonusInfo(eBonus)
		classInfo = gc.getBonusClassInfo(bonusInfo.getBonusClassType())
		if plot.isWater():
			if gameMap.getNumBonusesOnLand(eBonus) * 100/(gameMap.getNumBonuses(eBonus) + 1) < bonusInfo.getMinLandPercent():
				return False
		#Make sure there are no bonuses of the same class (but a different type) nearby:
		if classInfo != None:
			iRange = classInfo.getUniqueRange()
			for dx in range(-iRange,iRange+1):
				for dy in range(-iRange,iRange+1):
					loopPlot = self.plotXY(x,y,dx,dy)
					if loopPlot != None:
						if areaID == loopPlot.getArea():
							if plotDistance(x, y, loopPlot.getX(), loopPlot.getY()) <= iRange:
								eOtherBonus = loopPlot.getBonusType(TeamTypes.NO_TEAM)
								if eOtherBonus != BonusTypes.NO_BONUS:
									if gc.getBonusInfo(eOtherBonus).getBonusClassType() == bonusInfo.getBonusClassType():
										return False
		#Make sure there are no bonuses of the same type nearby:
		iRange = bonusInfo.getUniqueRange()
		for dx in range(-iRange,iRange+1):
			for dy in range(-iRange,iRange+1):
				loopPlot = self.plotXY(x,y,dx,dy)
				if loopPlot != None:
					if areaID == loopPlot.getArea():
						if plotDistance(x, y, loopPlot.getX(), loopPlot.getY()) <= iRange:
							eOtherBonus = loopPlot.getBonusType(TeamTypes.NO_TEAM)
							if eOtherBonus != BonusTypes.NO_BONUS:
								if eOtherBonus == eBonus:
									return False


		return True
	def PlotCanHaveBonus(self,plot,eBonus,bIgnoreLatitude,bIgnoreArea):
		#This function is like CvPlot::canHaveBonus but will
		#ignore blocking features and checks for a valid area.
		gc = CyGlobalContext()

		featureForest = GetInfoType("FEATURE_FOREST")
		if eBonus == BonusTypes.NO_BONUS:
			return True
		if plot.getBonusType(TeamTypes.NO_TEAM) != BonusTypes.NO_BONUS:
			return False
		if plot.isPeak():
			return False
		bonusInfo = gc.getBonusInfo(eBonus)
		#Here is the change from canHaveBonus. Forest does not block bonus
		requiresForest = bonusInfo.isFeature(featureForest)
		plotIsForest = plot.getFeatureType() == featureForest
		#To avoid silk and spices on ice/tundra
		if plotIsForest and requiresForest:
			if bonusInfo.isFeatureTerrain(plot.getTerrainType()) == False:
				return False
		#now that bonuses that require forest are dealt with, count forest
		#as no feature
		else:
			if plot.getFeatureType() != FeatureTypes.NO_FEATURE and not plotIsForest:
				if bonusInfo.isFeature(plot.getFeatureType()) == False:
					return False
				if bonusInfo.isFeatureTerrain(plot.getTerrainType()) == False:
					return False
			else:
				if bonusInfo.isTerrain(plot.getTerrainType()) == False:
					return False

		if plot.isHills():
			if bonusInfo.isHills() == False:
				return False
		if plot.isFlatlands():
			if bonusInfo.isFlatlands() == False:
				return False
		if bonusInfo.isNoRiverSide():
			if plot.isRiverSide():
				return False
		if bonusInfo.getMinAreaSize() != -1:
			if plot.area().getNumTiles() < bonusInfo.getMinAreaSize():
				return False
		if bIgnoreLatitude == False:
			if plot.getLatitude() > bonusInfo.getMaxLatitude():
				return False
			if plot.getLatitude() < bonusInfo.getMinLatitude():
				return False
	#	if plot.isPotentialCityWork() == False:
	#		return False
		return True
	def CalculateNumBonusesToAdd(self,eBonus):
		#This is like the function in CvMapGenerator except it uses
		#self.PlotCanHaveBonus instead of CvPlot::canHaveBonus
		gc = CyGlobalContext()
		gameMap = CyMap()
		game = CyGame()
		bonusInfo = gc.getBonusInfo(eBonus)
		rand1 = PRand.randint(0,bonusInfo.getRandAppearance1())
		rand2 = PRand.randint(0,bonusInfo.getRandAppearance2())
		rand3 = PRand.randint(0,bonusInfo.getRandAppearance3())
		rand4 = PRand.randint(0,bonusInfo.getRandAppearance4())
		baseCount = bonusInfo.getConstAppearance() + rand1 + rand2 + rand3 + rand4

		bIgnoreLatitude = False
		bIgnoreArea = True
		landTiles = 0
		numPossible = 0
		if bonusInfo.getTilesPer() > 0:
			for i in range(mc.width*mc.height):
				plot = gameMap.plotByIndex(i)
				if self.PlotCanHaveBonus(plot,eBonus,bIgnoreLatitude,bIgnoreArea):
					numPossible += 1
			landTiles += numPossible/bonusInfo.getTilesPer()
		players = game.countCivPlayersAlive() * bonusInfo.getPercentPerPlayer()/100
		bonusCount = baseCount * (landTiles + players)/100
		bonusCount = max(1,bonusCount)
##        print "Calculating bonus amount for %(bt)s" % {"bt":bonusInfo.getType()}
##        print "baseCount=%(bc)d, numPossible=%(np)d, landTiles=%(lt)d, players=%(p)d" % \
##        {"bc":baseCount,"np":numPossible,"lt":landTiles,"p":players}
##        print ""
		return bonusCount

	def GetUniqueBonusTypeCountInArea(self,area):
		gc = CyGlobalContext()
		areaID = area.getID()
		uniqueBonusCount = 0
		for i in range(0,len(self.bonusList),1):
			areaList = self.bonusList[i].areaList
			bonusInfo = gc.getBonusInfo(self.bonusList[i].eBonus)
			if bonusInfo.isOneArea() == False:
				continue
			for n in range(0,len(areaList),1):
				if areaList[n] == areaID:
					uniqueBonusCount += 1
					break

		return uniqueBonusCount

	def GetSameClassTypeCountInArea(self,area,eBonus):
		gc = CyGlobalContext()
		areaID = area.getID()
		uniqueBonusCount = 0
		bonusInfo = gc.getBonusInfo(eBonus)
		eClass = bonusInfo.getBonusClassType()
		if eClass == BonusClassTypes.NO_BONUSCLASS:
			return 0
		classInfo = gc.getBonusClassInfo(eClass)
		if classInfo == None:
			return 0
		uRange = classInfo.getUniqueRange()
		for i in range(0,len(self.bonusList),1):
			areaList = self.bonusList[i].areaList
			bonusInfo = gc.getBonusInfo(self.bonusList[i].eBonus)
			if bonusInfo.isOneArea() == False:
				continue
			if bonusInfo.getBonusClassType() != eClass:
				continue
			for n in range(0,len(areaList),1):
				if areaList[n] == areaID:
					uniqueBonusCount += 1
					break
		#Same class types tend to really crowd out any bonus
		#types that are placed later. A single cow can block
		#5 * 5 squares of pig territory for example. Probably
		#shouldn't place them on the same area at all, but
		#sometimes it might be necessary.
		return uniqueBonusCount * uRange * uRange

	def CalculateAreaSuitability(self,area,eBonus):
		gc = CyGlobalContext()
		gameMap = CyMap()
		areaID = area.getID()
		uniqueTypesInArea = self.GetUniqueBonusTypeCountInArea(area)
		sameClassTypesInArea = self.GetSameClassTypeCountInArea(area,eBonus)
		#Get the raw number of suitable tiles
		numPossible = 0
		for i in range(mc.width*mc.height):
			plot = gameMap.plotByIndex(i)
			if plot.getArea() == areaID:
				if self.PlotCanHaveBonus(plot,eBonus,False,True):
					numPossible += 1
		numPossible = numPossible/(uniqueTypesInArea + sameClassTypesInArea + 1)
		suitability = float(numPossible)/float(area.getNumTiles())
		return suitability,numPossible
#Global Access
bp = BonusPlacer()

class BonusArea :
	def __init__(self):
		self.eBonus = -1
		self.desiredBonusCount = -1
		self.currentBonusCount = -1
		self.areaList = list()

class AreaSuitability :
	def __init__(self,areaID):
		self.areaID = areaID
		self.suitability = 0
		self.numPossible = 0