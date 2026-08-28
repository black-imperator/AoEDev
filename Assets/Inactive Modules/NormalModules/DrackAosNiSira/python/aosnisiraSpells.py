import CvUtil
from CvPythonExtensions import *
import PyHelpers
PyPlayer = PyHelpers.PyPlayer

gc		  = CyGlobalContext()
git			= gc.getInfoTypeForString

import CustomFunctions
cf = CustomFunctions.CustomFunctions()

def reqPlantForestHeartOnFort(pCaster):
	pPlot = pCaster.plot()
	iPlayer = pPlot.getOwner()
	iImprovement = pPlot.getImprovementType()
	iForestHeart1 = git('IMPROVEMENT_FORESTHEART_SAPLING')
	iForestHeart2 = git('IMPROVEMENT_FORESTHEART')
	iForestHeart3 = git('IMPROVEMENT_FORESTHEART_TITAN')
	invalidFortTypes = [iForestHeart1, iForestHeart2, iForestHeart3]
	
	# Forest Hearts terraform their plot to Grassland; never allow one on water. (issue #255)
	if pPlot.isWater():
		return False
  
	if iPlayer != -1:
		if iImprovement != -1:
			pImprovement = gc.getImprovementInfo(iImprovement)
			if pImprovement.isFort() and not pImprovement.isUnique():
				if not iImprovement in invalidFortTypes:
					return True
	return False

def spellPlantForestHeartOnFort(pCaster):
	pPlot = pCaster.plot()
	iPlayer = pPlot.getOwner()
	iImprovement = pPlot.getImprovementType()
	pPlot.clearCultureControl(iPlayer, iImprovement, 1)
	pPlot.setImprovementType(git('IMPROVEMENT_FORESTHEART_SAPLING'))
	iImprovement = pPlot.getImprovementType()
	pPlot.setImprovementOwner(iPlayer)
	pPlot.addCultureControl(iPlayer, iImprovement, 1)
 
def spellEatAnimal(pCaster):
    pPlot = pCaster.plot()  # Get the plot where the caster is standing
    pCity = pPlot.getPlotCity()  # Get the city on that plot

    if pCity:
        pCity.changeFood(30)  # Add 30 food to the city