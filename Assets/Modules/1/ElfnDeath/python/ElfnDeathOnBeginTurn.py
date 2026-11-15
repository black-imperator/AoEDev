## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

from CvPythonExtensions import *
from BasicFunctions import *
import FoxTools
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CvCameraControls
import CvEventInterface


def onBeginGameTurn(self, argsList):
		'Called at the beginning of the end of each turn'
		iGameTurn = argsList[0]
		
		gc 			= CyGlobalContext()
		game 		= CyGame()
		Option		= self.GameOptions
		Civ			= self.Civilizations
		getNum		= game.getNumCivActive

		iAreThereOnceElvesHere  = gc.getInfoTypeForString("CIVILIZATION_ONCE_ELVES")
		if not (iAreThereOnceElvesHere):
			return

		map 			= CyMap()
		Terrain 		= self.Terrain
		Feature 		= self.Feature
		UnitCombat		= self.UnitCombats
		UnitClass		= self.UnitClasses
		Improvement		= self.Improvements
		Mana			= self.Mana
		Rel				= self.Religions
		Bonus			= self.Resources
		Define			= self.Defines
		Alignment		= self.Alignments
		iMistChance     = 25
		iGameTurn 		= game.getGameTurn()
		iGameSpeed		= gc.getGameSpeedInfo(game.getGameSpeedType()).getTrainPercent()
		iGameSpeedMod 	= iGameSpeed / 5
		interface 		= CyInterface()
		iCount			= game.getGlobalCounter()
		getPlot 		= map.plot

		byIndex 	= map.plotByIndex
		getPlayer 	= gc.getPlayer
		randNum 	= game.getSorenRandNum
		for i in xrange(map.numPlots()):
			pPlot			 	= byIndex(i)
			if pPlot == None: continue
			iBonus 				= pPlot.getBonusType(-1)
			iFeature 			= pPlot.getFeatureType()
			iImprovement 		= pPlot.getImprovementType()
			iTerrain 			= pPlot.getTerrainType()
			bIsOwned 			= pPlot.isOwned()
			setFeature 			= pPlot.setFeatureType
			setImprov			= pPlot.setImprovementType
			bPeak				= pPlot.isPeak()
			bCity				= pPlot.isCity()

			if bIsOwned:
				iOwner 			= pPlot.getOwner()
				pPlayer 		= getPlayer(iOwner)
				iAlignment 		= pPlayer.getAlignment()
				iStateReligion	= pPlayer.getStateReligion()
				eCiv 			= pPlayer.getCivilizationType()

								
#### Once Elves Hidden Forests Terrain Section
			if iAreThereOnceElvesHere:
				if bIsOwned:
					if eCiv == gc.getInfoTypeForString("CIVILIZATION_ONCE_ELVES"):
                                                        ###The Mist Spreads Through the Woods.
							if iFeature == Feature["Forest"] or iFeature == Feature["Ancient Forest"]:
								iChance = iMistChance * 5
								if randNum(1000, "Mist") < iChance :
									pPlot.setPlotEffectType(gc.getInfoTypeForString("PLOT_EFFECT_MIST"))
						        ###The Mist can not spread outside the forests(I dont know if this makes more work or less for the game)
							if not iFeature == Feature["Forest"] and not iFeature == Feature["Ancient Forest"]:
								iChance = iMistChance * 0.0
								if randNum(1000, "Mist") < iChance:
									pPlot.setPlotEffectType(gc.getInfoTypeForString("PLOT_EFFECT_MIST"))
						        ###The Mist will not spread through...Other Mists?(does this do anything?)
							if iFeature == gc.getInfoTypeForString("FEATURE_MIST"):
								iChance = iMistChance * 0.0
								if randNum(1000, "Mist") < iChance:
									pPlot.setPlotEffectType(gc.getInfoTypeForString("PLOT_EFFECT_MIST"))
						        ###The Woods are destroyed, the Mist Vanishes.
							if not iFeature == Feature["Forest"] and not iFeature == Feature["Ancient Forest"]:
								iChance = iMistChance * 10
								if randNum(1000, "Mist") < iChance:
									pPlot.setPlotEffectType(gc.getInfoTypeForString("NO_PLOT_EFFECT"))
						        ###Set fire to the woods also banishes the Mist
							if iImprovement == gc.getInfoTypeForString("IMPROVEMENT_SMOKE"):
								iChance = iMistChance * 10
								if randNum(1000, "Mist") < iChance:
									pPlot.setPlotEffectType(gc.getInfoTypeForString("NO_PLOT_EFFECT"))
