## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CvCameraControls
import CvEventInterface


# globals
#gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

from collections import deque

def onBeginGameTurn(self, argsList):
	'Called at the beginning of the end of each turn'
	gc 			= CyGlobalContext()
	game 		= CyGame()
	Civ		 	= gc.getInfoTypeForString('CIVILIZATION_AOSNISIRA')
	getNum		= game.getNumCivActive
	git			= gc.getInfoTypeForString
	getRandNum	= game.getSorenRandNum
 
	iAreThereAosNiSiraHere		= getNum(Civ)
 
	if not (iAreThereAosNiSiraHere):
		return

	map 			= CyMap()
 
	featureForest 	= git("FEATURE_FOREST")
	featureForestNew = git("FEATURE_FOREST_NEW")
	featureForestAncient = git("FEATURE_FOREST_ANCIENT")
	featureVulcano 	= git("FEATURE_VOLCANO")
	featureOasis 	= git("FEATURE_OASIS")
	featureFlames 	= git("FEATURE_FLAMES")
	
	terrainToNotOverrideWithForest = [featureForest, featureForestNew, featureForestAncient, featureVulcano, featureOasis, featureFlames]
 
	terrainOcean 	= git("TERRAIN_OCEAN")
	terrainCoast	= git("TERRAIN_COAST")
	terrainDeepOcean = git("TERRAIN_OCEAN_DEEP")
	terrainGrass	= git("TERRAIN_GRASS")
	terrainPlains	= git("TERRAIN_PLAINS")
	terrainMarsh	= git("TERRAIN_MARSH")
	terrainTundra 	= git("TERRAIN_TUNDRA")
	terrainTaiga 	= git("TERRAIN_TAIGA")
 
	forestTerrain = [terrainGrass, terrainPlains, terrainMarsh, terrainTundra, terrainTaiga]
 
	impFarm			= git("IMPROVEMENT_FARM")
	impCamp			= git("IMPROVEMENT_CAMP")
	impCottage		= git("IMPROVEMENT_COTTAGE")
	impHamlet		= git("IMPROVEMENT_HAMLET")
	impLumbermill	= git("IMPROVEMENT_LUMBERMILL")
	impMine			= git("IMPROVEMENT_MINE")
	impPasture		= git("IMPROVEMENT_PASTURE")
	impPlantation	= git("IMPROVEMENT_PLANTATION")
	impQuarry		= git("IMPROVEMENT_QUARRY")
	impTown			= git("IMPROVEMENT_TOWN")
	impVillage		= git("IMPROVEMENT_VILLAGE")
	impWatermill	= git("IMPROVEMENT_WATERMILL")
	impWindmill		= git("IMPROVEMENT_WINDMILL")
	impWinery		= git("IMPROVEMENT_WINERY")
	impWorkshop		= git("IMPROVEMENT_WORKSHOP")
	impBedouinCamp	= git("IMPROVEMENT_BEDOUIN_CAMP")
	impBedouinGatherin	= git("IMPROVEMENT_BEDOUIN_GATHERING")
	impBedouinSit	= git("IMPROVEMENT_BEDOUIN_SIT")
	impBedouinVillage	= git("IMPROVEMENT_BEDOUIN_VILLAGE")
	impDCrypt		= git("IMPROVEMENT_DTESH_CRYPT")
	impDCrypt2		= git("IMPROVEMENT_DTESH_CRYPT_DEFILED")
	impDPasture		= git("IMPROVEMENT_PASTURE_CORRUPTED")
	impPyre			= git("IMPROVEMENT_DTESH_PYRE")
	impDCata		= git("IMPROVEMENT_DTESH_CATACOMBS")
	impEnclave		= git("IMPROVEMENT_ENCLAVE")
	impHomestead	= git("IMPROVEMENT_HOMESTEAD")
	impYaranga		= git("IMPROVEMENT_YARANGA")
 
	normalImprovements  = [impFarm, impCamp, impCottage, impHamlet, impLumbermill, impMine, impPasture, impPlantation, impQuarry, impTown, impVillage, impWatermill, impWindmill, impWinery, impWorkshop, impBedouinCamp, impBedouinGatherin, impBedouinSit, impBedouinVillage, impDCrypt, impDCrypt2, impDPasture, impPyre, impDCata, impEnclave, impHomestead, impYaranga]
 
	impRoad			= git("IMPROVEMENT_ROAD")
	impTrail		= git("IMPROVEMENT_TRAIL")
 
	roadImprovements = [impRoad]
 
	bonusClassTypeMana  = git("BONUSCLASS_MANA")
	bonusClassRawMana 	= git("BONUSCLASS_RAWMANA")
    
	impForestHeartSapling	= git("IMPROVEMENT_FORESTHEART_SAPLING")
	impForestHeart			= git("IMPROVEMENT_FORESTHEART")
	impForestHeartTitan		= git("IMPROVEMENT_FORESTHEART_TITAN")
 
	forestHeartImprovements = [impForestHeartSapling, impForestHeart, impForestHeartTitan]

	for i in xrange(map.numPlots()):
		pPlot			 	= map.plotByIndex(i)
		if pPlot == None: continue

		pPlotIsOwned = pPlot.isOwned()
  
		if pPlotIsOwned == False: continue

		# If Owner is not of Aos Ni Sira, Forest Heart has no effect
		if pPlot.isOwned():
			iOwner 			= pPlot.getOwner()
			pPlayer 		= gc.getPlayer(iOwner)
			eCiv 			= pPlayer.getCivilizationType()
			if eCiv != Civ: continue			

		pPlotImprovement 	= pPlot.getImprovementType()
		pRouteType 			= pPlot.getRouteType()
  
		# Destroy "Civilization" Improvements like Farms, Mines, etc
		if pPlotImprovement in normalImprovements:
			pPlot.setImprovementType(-1)

		# Replace Roads with Trails
		if pRouteType in roadImprovements:
			pPlot.setRouteType(impTrail)

		# Check for Forest Heart Improvements in the World and get their Range
		if pPlotImprovement == impForestHeartSapling:
			iRange = 1
		elif pPlotImprovement == impForestHeart:
			iRange = 2
		elif pPlotImprovement == impForestHeartTitan:
			iRange = 3
		else:
			iRange = 0

		# If Field is not a Forest heart, Ignore
		if iRange == 0: continue
  
		# Terrain directly under Forest Heart becomes Grassland and Ancient Forest
		forestHeartFeature = pPlot.getFeatureType()
		forestHeartTerrain = pPlot.getTerrainType()
		if not (forestHeartTerrain == terrainGrass):
			pPlot.setTerrainType( terrainGrass, True, True )
   
		if not (forestHeartFeature == featureForestAncient):
			pPlot.setFeatureType(featureForestAncient, 0)
  
		# Search for all Plots around the Forest Heart
		for x, y in plotsInRange(pPlot.getX(), pPlot.getY(), iRange):
			iPlot = map.plot(x, y)
   
			if iPlot == None: continue
  
			iFeature 			= iPlot.getFeatureType()
			iImprovement 		= iPlot.getImprovementType()
			iTerrain 			= iPlot.getTerrainType()
			setImprov			= iPlot.setImprovementType
			bPeak				= iPlot.isPeak()
			bCity				= iPlot.isCity()

			# Do not touch Forest Hearts
			if iImprovement in forestHeartImprovements:
				continue

			# Peaks and Oceans are not Terraformed
			if bPeak: continue
			if iTerrain == terrainOcean: continue
			if iTerrain == terrainCoast: continue
			if iTerrain == terrainDeepOcean: continue

			iPlotIsOwned = iPlot.isOwned()
   
			if iPlotIsOwned == False: continue

			if iPlotIsOwned:
				plotOwner 			= iPlot.getOwner()
				plotPlayer 			= gc.getPlayer(plotOwner)
				plotPlayerCiv 		= plotPlayer.getCivilizationType()
				# If the Plot is not owned by a Aos Si Nira Civ, its not changed
				if plotPlayerCiv != Civ: continue

			# Let Forest Grow
			if iTerrain in forestTerrain:
				if iFeature == -1 or iFeature not in terrainToNotOverrideWithForest:
					if getRandNum(100, "AosSiNira Forest Grow") < 25:				
						iPlot.setFeatureType(featureForestNew, 0)
   
			if bCity: continue
   
			iTeam 				= plotPlayer.getTeam()
			iBonus 				= iPlot.getBonusType(iTeam)
   
			# If No Bonus here, nothing to Plant
			if iBonus == -1:
				continue
   
			# Create Forest Roots if Ressource is on Plot (Except for Mana Ressources)
			if iImprovement == -1:
				iBonusInfo 	= gc.getBonusInfo(iBonus)
				iBonusClass = iBonusInfo.getBonusClassType()
				if not iBonusClass == bonusClassTypeMana:
					if not iBonusClass == bonusClassRawMana:
						setImprov(git("IMPROVEMENT_TREEROOT"))
