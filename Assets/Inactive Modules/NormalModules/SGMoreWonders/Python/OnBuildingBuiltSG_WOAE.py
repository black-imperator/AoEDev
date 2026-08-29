import CvUtil
from CvPythonExtensions import *
import PyHelpers
PyPlayer = PyHelpers.PyPlayer

gc = CyGlobalContext()

import CustomFunctions
cf = CustomFunctions.CustomFunctions()

def onBuildingBuilt(self, argsList):
	message = "This is a test in function"
	CyInterface().addMessage(iPlayer, True, 25, message, '', 2,  'Art/interface/buttons/terrainfeatures/flames.dds', ColorTypes(8),  pCity.getX(), pCity.getY(), True, True)
	'Building Completed'
	pCity, iBuildingType = argsList
	player = pCity.getOwner()
	pPlayer = gc.getPlayer(player)
	pPlot = pCity.plot()
	game = gc.getGame()
	iBuildingClass = gc.getBuildingInfo(iBuildingType).getBuildingClassType()

	if (iBuildingType==gc.getInfoTypeForString('BUILDING_TREE_OF_SUCELLUS')):
	
		iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
		iForest = gc.getInfoTypeForString('FEATURE_FOREST')
		iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
		iScrub = gc.getInfoTypeForString('FEATURE_SCRUB')
		iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
		iAncient = gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT')
		
		iX = pCity.getX()
		iY = pCity.getY()
		for iiX in range(iX-3, iX+4, 1):
			for iiY in range(iY-3, iY+4, 1):
				pLoopPlot = CyMap().plot(iiX,iiY)
				if not pLoopPlot.isNone():
					if not pLoopPlot.isWater():
						iFeature = pLoopPlot.getFeatureType()
						if iFeature == iForest:
							pLoopPlot.setFeatureType(iAncient, 0)
						if iFeature == iJungle:
							pLoopPlot.setFeatureType(iAncient, 0)
						if iFeature == iFlames:
							pLoopPlot.setFeatureType(-1, -1)
						iImprovement = pLoopPlot.getImprovementType()
						if iImprovement == iSmoke:
							pLoopPlot.setImprovementType(-1)						
	
	elif (iBuildingType==gc.getInfoTypeForString('BUILDING_ENGINEERING_CORPS')):		
		pPlayer.setHasTrait(gc.getInfoTypeForString('TRAIT_ENGINEER'),true)		

	else:
		message2 = "This is a test in if"
		CyInterface().addMessage(player, True, 25, message2, '', 2,  'Art/interface/buttons/terrainfeatures/flames.dds', ColorTypes(8),  pCity.getX(), pCity.getY(), True, True)