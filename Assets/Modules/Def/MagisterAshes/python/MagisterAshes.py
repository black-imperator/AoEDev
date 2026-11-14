## MODULAR PYTHON EXAMPLE
## ArcticNightWolf 29-may-2010
## ArcticNightWolf@gmail.com

from CvPythonExtensions import *

import PyHelpers

import FoxDebug
import FoxTools
import time
import CustomFunctions
from BasicFunctions import *

gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
PyPlayer = PyHelpers.PyPlayer
cf = CustomFunctions.CustomFunctions()


def onBeginGameTurn(self, argsList):
		'Called at the beginning of the end of each turn'
		iGameTurn = argsList[0]
		bPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
		if (iGameTurn + 1) % (40- 5*CyGame().getGameSpeedType()) == 0 and not bPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_DEAD_BADB')):
			iBB = gc.getInfoTypeForString('IMPROVEMENT_BADBS_BLIZZARD')
			lBB = cf.findImprovements(iBB)
			if len(lBB) > 0:
				pPlotBB = lBB[0]
				lCold = [gc.getInfoTypeForString('TERRAIN_TUNDRA'),gc.getInfoTypeForString('TERRAIN_SNOW'),gc.getInfoTypeForString('TERRAIN_GLACIER')]
				iBestValue = 0
				pBestPlot = -1
				for i in xrange (CyMap().numPlots()):
					pTargetPlot = CyMap().plotByIndex(i)
					if pTargetPlot == pPlotBB:
						continue
					if pTargetPlot.isPeak():
						continue
					if pTargetPlot.isWater():
						continue
					if pTargetPlot.getBonusType(-1) != -1:
						continue
					if pTargetPlot.getRealBonusType() != -1:
						continue
					if pTargetPlot.isCity():
						continue
					if pTargetPlot.getNumUnits() > 0:
						continue

					iValue = 0
					iImp = pTargetPlot.getImprovementType()
					if iImp == -1:
						iValue += 1000
					elif gc.getImprovementInfo(iImp).isPermanent():
						continue
					if pTargetPlot.getTerrainType() in lCold:
						iValue += 500
					iValue += CyGame().getSorenRandNum(1000, "Badb move ")
					if not pTargetPlot.isOwned():
						iValue += 500
					if iValue > iBestValue:
						iBestValue = iValue
						pBestPlot = pTargetPlot

				if pBestPlot != -1:
					# Place new improvement
					pBestPlot.setImprovementType(iBB) #this spawns ice mana, we know there's no current bonus present
					pBestPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_BLIZZARD'), 0)

					# Copy over values from old improvement
					pBestPlot.setExploreNextTurn(pPlotBB.getExploreNextTurn())

					# Move the guardian, if exists
					iBadb = gc.getInfoTypeForString('UNIT_BADB')
					bFound = False
					for iX, iY in RANGE1:
						pAdjPlot = CyMap().plot(pPlotBB.getX()+iX, pPlotBB.getY()+iY)
						for i in xrange(pAdjPlot.getNumUnits()):
							pUnit = pAdjPlot.getUnit(i)
							if pUnit.getUnitType() == iBadb:
								pUnit.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True, False)
								pUnit.setImmobileTimer(2)
								if pUnit.isLeashed():
									pUnit.setLeashX(pBestPlot.getX())
									pUnit.setLeashY(pBestPlot.getY())
								bFound = True
								break
						if bFound:
							break

					# Remove old improvement
					pPlotBB.setImprovementType(-1)
					pPlotBB.setBonusType(-1)
					pPlotBB.setFeatureType(-1, 0)
					pPlotBB.setExploreNextTurn(0)

		# Carnivean's Camp
		if (iGameTurn + 1) % (20 - 2*CyGame().getGameSpeedType()) == 0 and not bPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_DEAD_CARNIVEAN')):
			iCC = gc.getInfoTypeForString('IMPROVEMENT_CARNIVEANS_CAMP')
			lCC = cf.findImprovements(iCC)
			if len(lCC) > 0:
				pPlotCC = lCC[0]
				iBestValue = 0
				pBestPlot = -1
				for i in xrange (CyMap().numPlots()):
					adjCity = False
					pTargetPlot = CyMap().plotByIndex(i)
					if pTargetPlot == pPlotCC:
						continue
					if pTargetPlot.isPeak():
						continue
					if pTargetPlot.isWater():
						continue
					if pTargetPlot.getBonusType(-1) != -1:
						continue
					if pTargetPlot.getRealBonusType() != -1:
						continue
					if pTargetPlot.isCity():
						continue
					if pTargetPlot.getNumUnits() > 0:
						continue
					for iX, iY in SURROUND1:
						pAdjPlot = CyMap().plot(pTargetPlot.getX()+iX, pTargetPlot.getY()+iY)
						if pAdjPlot.isCity():
							adjCity = True
							break
					if adjCity:
						continue

					iValue = 0
					iImp = pTargetPlot.getImprovementType()
					if iImp == -1:
						iValue += 250
					elif gc.getImprovementInfo(iImp).isPermanent():
						continue
					iValue += CyGame().getSorenRandNum(750, "Carnivean move")
					if (CyGame().getSorenRandNum(100,"Carnivean Taking a vacation")<30):
						if pTargetPlot.isOwned():
							iValue -= 500
					else:
						if pTargetPlot.isOwned():
							iValue += 500
					if pTargetPlot.getRouteType() != -1:
						iValue += 250
					if iValue > iBestValue:
						iBestValue = iValue
						pBestPlot = pTargetPlot

				if pBestPlot != -1:
					# Place new improvement=
					pBestPlot.setImprovementType(iCC) #this spawns chaos mana, we know there's no current bonus present

					# Copy over values from old improvement
					# Move the guardian, if exists
					iCarnivean = gc.getInfoTypeForString('UNIT_CARNIVEAN')
					for iX, iY in RANGE1:
						pAdjPlot = CyMap().plot(pPlotCC.getX()+iX, pPlotCC.getY()+iY)
						for i in xrange(pAdjPlot.getNumUnits()):
							pUnit = pAdjPlot.getUnit(i)
							if pUnit.getUnitType() == iCarnivean:
								pUnit.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True, False)
								pUnit.setSpawnPlot(pBestPlot)
								pUnit.setImmobileTimer(2)
								if pUnit.isLeashed():
									pUnit.setLeashX(pBestPlot.getX())
									pUnit.setLeashY(pBestPlot.getY())
								break

					# Remove old improvement
					pPlotCC.setImprovementType(-1)
					pPlotCC.setBonusType(-1)