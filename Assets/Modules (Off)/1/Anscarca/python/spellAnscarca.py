from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import CvScreensInterface
import sys
import CvSpellInterface
import CvEventInterface


gc = CyGlobalContext()

def reqLichdomAnsarca(caster):
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PUPPET')):
		return False
	if isWorldUnitClass(caster.getUnitClassType()):
		return False
		
	pPlayer		= gc.getPlayer(caster.getOwner())
	eCiv		= pPlayer.getCivilizationType()
		
	if eCiv == gc.getInfoTypeForString("CIVILIZATION_ANSCARCA"):
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	return not pPlayer.isUnitClassMaxedOut(gc.getInfoTypeForString('UNITCLASS_LICH'),0)

def escapeAnsaraca(caster):
	caster.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SPAWNING_ANSCARCA_2"), True)
	CvSpellInterface.spellTeleport(caster, 'Capital')

def reqRecyleUnit(caster):
	return caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VIRAL_LINK_ANSCARCA')) \
		and caster.getUnitType() != gc.getInfoTypeForString('UNIT_OVERSEER_ANSCARCA') \
		and caster.getUnitType() != gc.getInfoTypeForString('UNIT_WHISPER') \
		and caster.getUnitType() != gc.getInfoTypeForString('UNIT_GROWTH_ANSCARCA') \
		and caster.getUnitType() != gc.getInfoTypeForString('UNIT_SETTLER_ANSCARCA') \
		and caster.getSummoner() == -1

def spellRecyleUnit(caster):
	game = CyGame()
	randNum = game.getSorenRandNum
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	iUnitType = caster.getUnitType()
	
	growthCount = 2
	pPlayer.setCivCounterMod(pPlayer.getCivCounterMod() + 1) #Get a counter increase regardless of if the spell is successfull
	
	# Cheaper units don't get a perfect chance to convert
	if iUnitType == gc.getInfoTypeForString('UNIT_SWARMLINGS'):
		if randNum(1000, "ANSCARCA_RECYLE") < 500: #90% chance of failure
			return
	elif iUnitType == gc.getInfoTypeForString('UNIT_PLAGUE') or iUnitType == gc.getInfoTypeForString('UNIT_MONSTROSITY_ANSCARCA') or iUnitType == gc.getInfoTypeForString('UNIT_DOOM_HERALD_ANSCARCA'):
		growthCount = 20
			
	iUnit = gc.getInfoTypeForString("UNIT_GROWTH_ANSCARCA")
	for i in range(growthCount):
		pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	
	if growthCount > 1:
		pPlayer.setCivCounterMod(pPlayer.getCivCounterMod() + growthCount - 1)
	
def reqImproveMana(caster):
	pPlot = caster.plot()
	if pPlot.getBonusType(-1) != -1:
		if gc.getBonusInfo(pPlot.getBonusType(-1)).getBonusClassType() == gc.getInfoTypeForString('BONUSCLASS_MANA'):
			if pPlot.getImprovementType() == -1:
				return True
	return False
	
	
def spellAnscarcaBore(caster):
	pPlot = caster.plot()
	pPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
	pPlot.setFeatureType(-1, -1)
	pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_BORE'))
	
def spellAnscarcaFarm(caster):
	pPlot = caster.plot()
	pPlot.setFeatureType(-1, -1)
	if not pPlot.isWater():
		pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
	pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_CAMP_ANSCARCA'))

def reqImprovePlot(caster, waterImprovement, improvementName):
	pPlot = caster.plot()
	if improvementName != 'Bore' and pPlot.isPeak():
		return False
	if waterImprovement == False and pPlot.isWater():
		return False
	if pPlot.isCity():
		return False
		
	iImprovement = pPlot.getImprovementType()
	if iImprovement != -1 and improvementName != 'Road' and improvementName != 'Railroad':
		if gc.getImprovementInfo(iImprovement).isPermanent():
			return False
			
		if improvementName == 'Farm' and (iImprovement == gc.getInfoTypeForString('IMPROVEMENT_CAMP_ANSCARCA') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_FARM_ANSCARCA') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_HARVESTER_ANSCARCA') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_REAPER_ANSCARCA')):
			return False
			
		if improvementName == 'Bore' and (iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BORE') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_SIPHON_ANSCARCA') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_EXTRACTOR')) and not (pPlot.isPeak() or pPlot.isHills()):
			return False
		
		if improvementName == 'Node' and (iImprovement == gc.getInfoTypeForString('IMPROVEMENT_NODE_ANSCARCA') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_SPIKE_ANSCARCA') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_SPIRE_ANSCARCA') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_GREATER_SPIRE_ANSCARCA')):
			return False
			
		if improvementName == 'Fort' and (iImprovement == gc.getInfoTypeForString('IMPROVEMENT_FORT') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_CASTLE') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_CITADEL')):
			return False
	
	if improvementName == 'Road' and (pPlot.getRouteType() == gc.getInfoTypeForString('ROUTE_ROAD') or pPlot.getRouteType() == gc.getInfoTypeForString('ROUTE_RAILROAD')):
			return False
			
	if improvementName == 'Railroad' and pPlot.getRouteType() != gc.getInfoTypeForString('ROUTE_ROAD'):
		return False
	
	# Have to space out the forts by having at least one space in between.
	if improvementName == 'Fort' or improvementName == 'Node':
		if pPlot.isPeak():
			return False
		
		getPlot	= CyMap().plot
		for x in range(caster.getX() - 1, caster.getX()+2):
			for y in range(caster.getY() - 1, caster.getY()+2):
				if x == caster.getX() and y == caster.getY(): #Allow replacement of a fort/node
					continue
				pPlotLoop = getPlot(x, y)
				iImprovementLoop = pPlotLoop.getImprovementType()
				if iImprovementLoop != -1 and gc.getImprovementInfo(iImprovementLoop).isFort():
					return False
			
	if reqImproveMana(caster) and improvementName != 'Road' and improvementName != 'Railroad': #Bonus mana resource, leave alone
		return False
		

	return True
	
	
def spellCreateRoad(caster):
	pPlot = caster.plot()
	pPlot.setRouteType(gc.getInfoTypeForString('ROUTE_ROAD'))

def spellCreateRailroad(caster):
	pPlot = caster.plot()
	pPlot.setRouteType(gc.getInfoTypeForString('ROUTE_RAILROAD'))

#Nodes are a Anscarca exclusive improvement so other civs moving onto it will destroy and give them gold for destroying the Anscarca
def onMoveNode(pCaster, pPlot, tier):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString("CIVILIZATION_ANSCARCA"):
		pPlot.setImprovementType(-1)
		pPlayer.changeGold(25*tier)
		
def reqCreateOverseer(caster):
	pPlot = caster.plot()
	if pPlot.isCity():
		return True
	iImprovement = pPlot.getImprovementType()
	if iImprovement != -1 and gc.getImprovementInfo(iImprovement).isFort():
		return True
		
	return False
	
def spellAnscarcaNode(caster):
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	iPlayer2 = pPlot.getOwner()
	iImprovement = gc.getInfoTypeForString('IMPROVEMENT_NODE_ANSCARCA')
	pPlot.setImprovementType(iImprovement)

	pPlot.clearCultureControl(iPlayer2, iImprovement, 1)
	pPlot.setImprovementOwner(iPlayer)
	pPlot.addCultureControl(iPlayer, iImprovement, 1)
	
	if not pPlot.isWater():
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_WASTELAND'),True,True)
	
	
	
def spellAnscarcaFort(caster):
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	iPlayer2 = pPlot.getOwner()
	iImprovement = gc.getInfoTypeForString('IMPROVEMENT_FORT')
	pPlot.setImprovementType(iImprovement)
	
	pPlayer = gc.getPlayer(caster.getOwner())
	iUnit = gc.getInfoTypeForString('UNIT_OVERSEER_ANSCARCA')
	newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)

	pPlot.clearCultureControl(iPlayer2, iImprovement, 1)
	pPlot.setImprovementOwner(iPlayer)
	pPlot.addCultureControl(iPlayer, iImprovement, 1)
	
	if not pPlot.isWater():
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_WASTELAND'),True,True)
	
	
def spellOutbreakAnscarca(pCity):
	game 	= CyGame()
	Speed	= CvEventInterface.getEventManager().GameSpeeds
	eSpeed 	= game.getGameSpeedType()
	iPlayer = pCity.getOwner()
	pPlayer = gc.getPlayer(pCity.getOwner())
	
	unrest = 6
	if eSpeed == Speed["Quick"]:
		unrest = 4
	elif eSpeed == Speed["Epic"]:
		unrest = 9
	elif eSpeed == Speed["Marathon"]:
		unrest = 18
	feverUnit = gc.getInfoTypeForString("UNIT_FEVER")
	plagueUnit = gc.getInfoTypeForString("UNIT_PLAGUE")

	#Spawn Fevers/Plagues in each city depending on population
	for pyCity in PyHelpers.PyPlayer(iPlayer).getCityList():
		iX = pyCity.getX()
		iY = pyCity.getY()
		newUnit = pPlayer.initUnit(feverUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CRAZED"), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ENRAGED"), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_PLAGUE_CARRIER"), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_PROPHECY_MARK"), True) #Note: Only on the initial unit and plagues
		newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MARKSMAN"), True)
		
		
		for i in range(pyCity.getPopulation() // 10):
			newUnit = pPlayer.initUnit(feverUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CRAZED"), True)
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ENRAGED"), True)
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_PLAGUE_CARRIER"), True)
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MARKSMAN"), True)
		
		for i in range(pyCity.getPopulation() // 50):
			newUnit = pPlayer.initUnit(plagueUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CRAZED"), True)
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ENRAGED"), True)
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_PLAGUE_CARRIER"), True)
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_PROPHECY_MARK"), True) #Note: Only on the initial unit and plagues
			newUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MARKSMAN"), True)

def reqNoLurkerLair(pCity):
	return pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_LURKER_LAIR_ANSCARCA")) == 0

def removeLurkerLair(pCity):
	pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_LURKER_LAIR_ANSCARCA"), 0)

def reqPlanetExtraction(pCity):
	popCost = [0,10,20,30,50,80,130,210,340,550,890] #Congratulations to those who know the sequence

	extractionTier = getExtractionTier(pCity) + 1 #Adding one since that's the tier we want to upgrade to
	
	#Tier 10 is the max hence the length check
	return extractionTier < len(popCost) and pCity.getPopulation() > popCost[extractionTier]
	
def spellPlanetExtraction(pCity):
	game = CyGame()
	randNum = game.getSorenRandNum
	getPlot = CyMap().plot
	popCost = [0,10,20,30,50,80,130,210,340,550,890] #Congratulations to those who know the sequence
	extractionTier = getExtractionTier(pCity) + 1 #Adding one since that's the tier we want to upgrade to
	
	game.changeGlobalCounter(extractionTier * 2 + 1) #Increase AC counter
	if randNum(100, 'BUILDING_RESOURCE_CAVERN_ANSCARCA') < getResourceChance(6-extractionTier):
		pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_RESOURCE_CAVERN_ANSCARCA"), 1)
	if randNum(100, 'BUILDING_LAVAFLOW_ANSCARCA') < getResourceChance(8-extractionTier):
		pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_LAVAFLOW_ANSCARCA"), 1)
	if randNum(100, 'BUILDING_LIFE_VEIN_ANSCARCA') < getResourceChance(10-extractionTier):
		pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_LIFE_VEIN_ANSCARCA"), 1)
	pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_PLANETARY_EXTRACTOR_ANSCARCA_"+str(extractionTier)), 1)
	pCity.changePopulation(-popCost[extractionTier])
	pCity.setOccupationTimer(extractionTier * 2)
	
	#10% chance for plots in extractionTier range to spawn hell and deletes improvement
	iX = pCity.getX()
	iY = pCity.getY()
	for iiX in range(-extractionTier,+extractionTier+1):
		for iiY in range(-extractionTier,+extractionTier+1):
			pAdjacentPlot = getPlot(iX+iiX,iY+iiY)
			if pAdjacentPlot.isNone() == False and randNum(100, 'extraction') < 10:
				if not game.isOption(GameOptionTypes.GAMEOPTION_NO_PLOT_COUNTER):
					pAdjacentPlot.changePlotCounter(100)
				
				iImprovement = pAdjacentPlot.getImprovementType()
				if not pAdjacentPlot.isCity() and iImprovement != -1 and not gc.getImprovementInfo(iImprovement).isPermanent():
					pAdjacentPlot.setImprovementType(-1)


def getResourceChance(offset):
	if offset == 5:
		return 1
	elif offset == 4:
		return 2
	elif offset == 3:
		return 4
	elif offset == 2:
		return 20
	elif offset == 1:
		return 100
	return 0
	

def getExtractionTier(pCity):
	extractionTier = 0
	for i in range(1,11): #1-10
		if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_PLANETARY_EXTRACTOR_ANSCARCA_" + str(i))) > 0:
			extractionTier = i
		else: #No need to continue once we hit the highest in the city
			break
	return extractionTier

def getHelpAnscarcaPandemic(argsList):
	ePromotion, pCaster = argsList
	szHelp = ""
	if pCaster != -1 and not pCaster.isNone():
		promoEffectTextList = []
		adaptationPromos = ["PROMOTION_GENERAL_ADAPTATION_ANSCARCA","PROMOTION_ANGEL_ADAPTATION_ANSCARCA","PROMOTION_CENTAUR_ADAPTATION_ANSCARCA","PROMOTION_DEMON_ADAPTATION_ANSCARCA","PROMOTION_DRAGON_ADAPTATION_ANSCARCA","PROMOTION_DWARF_ADAPTATION_ANSCARCA","PROMOTION_ELEMENTAL_ADAPTATION_ANSCARCA","PROMOTION_ELF_ADAPTATION_ANSCARCA","PROMOTION_SATYR_ADAPTATION_ANSCARCA","PROMOTION_FROSTLING_ADAPTATION_ANSCARCA","PROMOTION_GIANTKIN_ADAPTATION_ANSCARCA","PROMOTION_GOBLIN_ADAPTATION_ANSCARCA","PROMOTION_GOLEM_ADAPTATION_ANSCARCA","PROMOTION_ILLUSION_ADAPTATION_ANSCARCA","PROMOTION_LIZARDMAN_ADAPTATION_ANSCARCA","PROMOTION_MINOTAUR_ADAPTATION_ANSCARCA","PROMOTION_MUSTEVAL_ADAPTATION_ANSCARCA","PROMOTION_ORC_ADAPTATION_ANSCARCA","PROMOTION_PUPPET_ADAPTATION_ANSCARCA","PROMOTION_SHADE_ADAPTATION_ANSCARCA","PROMOTION_TROLLKIN_ADAPTATION_ANSCARCA","PROMOTION_UNDEAD_ADAPTATION_ANSCARCA"]
		newlineStr = CyTranslator().getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
	
		for promoName in adaptationPromos:
			iPromotion = gc.getInfoTypeForString(promoName)
			if pCaster.isHasPromotion(iPromotion):
				promoEffectTextList.append(CyTranslator().getText("TXT_KEY_" + promoName, (pCaster.countHasPromotion(iPromotion),)))
			
		if len(promoEffectTextList) > 0:
			szHelp = newlineStr.join(promoEffectTextList)
	
	return szHelp
	
	