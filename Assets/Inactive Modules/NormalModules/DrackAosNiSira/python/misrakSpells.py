from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CvCameraControls
import CvEventInterface
PyPlayer = PyHelpers.PyPlayer

gc		  = CyGlobalContext()
git			= gc.getInfoTypeForString

import CustomFunctions
cf = CustomFunctions.CustomFunctions()

def reqWelcomeGuest(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iMax = 0
	if pCity.getNumBuilding(git('BUILDING_FAIRY_DOLLHOUSE')) == 1:
		iMax += 2
	if pCity.getNumBuilding(git('BUILDING_FAIRY_CARAMEL_CAGE')) == 1:
		iMax += 1
	if pCity.getNumBuilding(git('BUILDING_FAIRY_CANDY_SHOP')) == 1:
		iMax += 2
	iCount = pCity.getFreeSpecialistCount(git('SPECIALIST_SLAVE'))
	if iCount >= iMax:
		return False
	else:
		return True

def reqMaterializeCity(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())

	# Check if Player has enough Souls (Only Counts for Humans)
	currentSoulsOfPlayer = pPlayer.getCivCounter()
	if pPlayer.isHuman():
		if currentSoulsOfPlayer < 50:
			return False

	if pPlot.isOwned() and pPlot.getOwner() != caster.getOwner():
		return False

	if pPlot.isWater():
		return False

	iImprovement = pPlot.getImprovementType()
	if iImprovement!=-1 and gc.getImprovementInfo(iImprovement).isUnique():
			return False

	iRange = gc.getMIN_CITY_RANGE()
	getPlot	= CyMap().plot
	for x, y in plotsInRange(pPlot.getX(), pPlot.getY(), iRange):
		pLoopPlot = getPlot(x, y)
		if not pLoopPlot.isNone():
			if pLoopPlot.isCity():
				return False

	if not pPlayer.isHuman():
		currentTurn = gc.getGame().getGameTurn()
		maxAllowedCities = currentTurn // 20  # Integer division: 1 city per 20 turns
		if pPlayer.getNumCities() > maxAllowedCities:
			return False

	return True

def spellMaterializeCity(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())

	pCity = pPlayer.initCity(pPlot.getX(),pPlot.getY())
	CvEventInterface.getEventManager().onCityBuilt([pCity])
	# Remove Souls from CivCounter (Only Counts for Human Players)
	if pPlayer.isHuman():
		pPlayer.changeCivCounter(-50)

def reqPlantScrub(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())

	# Check if the plot is a desert
	terrainDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
	if pPlot.getTerrainType() != terrainDesert:
		return False

	# Check if the plot has any feature
	if pPlot.getFeatureType() != -1:  # -1 means no feature
		return False

	return True

def spellPlantScrub(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())

	# Add the FEATURE_SCRUB feature to the plot
	featureScrub = gc.getInfoTypeForString('FEATURE_SCRUB')
	pPlot.setFeatureType(featureScrub, 0)  # 0 is the default variety
 
def reqConsumeHolyShroom(caster):
	# Get the unit type for UNIT_FAIRY_SHROOMFAE
	iShroomfae = gc.getInfoTypeForString('UNIT_FAIRY_SHROOMFAE')
	iShroomfaeClass = gc.getInfoTypeForString('UNITCLASS_FAIRY_SHROOMFAE')

	# Check if the caster is not already a Shroomfae
	if caster.getUnitType() == iShroomfae:
		return False

	# Get the player
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)

	# Check if the national unit limit for Shroomfae is reached
	if pPlayer.isUnitClassMaxedOut(iShroomfaeClass, 0):
		return False

	return True

def spellConsumeHolyShroom(caster):
	# Get the unit type for UNIT_FAIRY_SHROOMFAE
	iShroomfae = gc.getInfoTypeForString('UNIT_FAIRY_SHROOMFAE')
	iShroomfaeClass = gc.getInfoTypeForString('UNITCLASS_FAIRY_SHROOMFAE')

	# Get the player
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	
	# Check if the national unit limit for Shroomfae is reached
	if pPlayer.isUnitClassMaxedOut(iShroomfaeClass, 0):
		return
	
	newUnit = pPlayer.initUnit(iShroomfae, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.convert(caster)