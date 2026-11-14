# Frozen originally created by TC01
# Updated by Derf for Ashes of Erebus compatibility
# python amended to line up with modular format by LPlate

from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import CvScreensInterface
import sys
import PyHelpers
import CustomFunctions
import ScenarioFunctions
import CvEventInterface


#	Added in Frozen: TC01
#	Custom spell functions added in Frozen module. They do not need specific statements since they are only called from the XML. They are:
#		reqWintering checks if the Wintering worldspell can be casted
#		spellWintering does the effects of the Wintering worldspell
#		spellSnowfallPassive causes passive spread ice terrain as an Ascended moves about the map
#		reqFreezeForest checks if the Freeze Forest spell can be used
#		spellFreezeForest does the effects of the Freeze Forest spell
#		effectNested is the effect of Young being hatched from Nested units
#		effectYoung is the effect of a Young dying

# Common Definitions
gc                  = CyGlobalContext()
Manager             = CvEventInterface.getEventManager()
Terrain             = Manager.Terrain
Promo               = Manager.Promotions["Effects"]
Civ                 = Manager.Civilizations
Feature             = Manager.Feature
Frozen              = Manager.Units["Frozen"]

iTaiga      = Terrain["Taiga"]
iTundra     = Terrain["Tundra"]
iGlacier    = Terrain["Glacier"]
iForest     = Feature["Forest"]
iWinter     = Feature["Winter"]
iBlizzard   = Feature["Blizzard"]
iFrozen     = Civ["Frozen"]
iYoung      = Frozen["Young Kocrachon"]
iWinterborn = Promo["Winterborn"]
iWintered   = Promo["Wintered"]

def reqWintering(pCaster):
	iPlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	for i in xrange (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlayer.isHuman() == False:
			if iPlayer == pPlot.getOwner():
				if pPlot.getTerrainTypeCount(iTundra) < 20: # TODO Ronkhar. Find where this function is defined
					return False
		return True

def spellWintering(pCaster):
	iPlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iFrozenTeam = pPlayer.getTeam()
	for i in xrange (CyMap().numPlots()): # check whole map
		pPlot = CyMap().plotByIndex(i)
		if not pPlot.isWater():
			if pPlot.getOwner() == iPlayer: # if frozen tile
				if pPlot.getTerrainType() == iTundra:
					pPlot.setTerrainType(iGlacier,True,True) # tundra -> glacier
				elif pPlot.getTerrainType() == iTaiga:
					pPlot.setTerrainType(iTundra,True,True) # taiga -> tundra
				elif pPlot.getTerrainType() != iGlacier:
					pPlot.setTerrainType(iTaiga,True,True) # others -> taiga
				if pPlot.getTerrainType() == iGlacier:
					if pPlot.getFeatureType() in (-1,iBlizzard):
						pPlot.setFeatureType(iWinter, 0) # if glacier without inconvenient feature, add feature winter
			elif pPlot.getTerrainType() == iGlacier: # if glacier outside frozen territory
				if pPlot.getFeatureType() == -1: # and no feature is present already
					pPlot.setFeatureType(iBlizzard, 0) # then create Blizzard

		# all non-frozen, non winterborn, non-naval, alive units receive promotion wintered
		for e in range(pPlot.getNumUnits()): 
			pUnit = pPlot.getUnit(e)
			if not pUnit.isHasPromotion(iWinterborn):
				if pUnit.isAlive():
					if not pUnit.getDomainType() == gc.getInfoTypeForString('DOMAIN_WATER'):
						pOwner = gc.getPlayer(pUnit.getOwner())
						iOwnerTeam = pOwner.getTeam()
						if iOwnerTeam != iFrozenTeam:
							pUnit.setHasPromotion(iWintered, True)

def reqFreezeForest(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlot.getFeatureType() == -1:
		if pPlot.getTerrainType() == iTaiga:
			#Changed from Tundra to Taiga
			return True
	if pPlot.getFeatureType() == iForest:
		if not pPlot.getTerrainType() == iTaiga:
			#Changed from Tundra to Taiga
			return True
	if pPlayer.isHuman() == False:
		if caster.getOwner() == pPlot.getOwner():
			return True
	return False

def spellFreezeForest(caster):
	pPlot = caster.plot()
	if pPlot.getFeatureType() == -1:
		if pPlot.getTerrainType() == iTaiga:
			#Changed from Tundra to Taiga
			pPlot.setFeatureType(iForest, 2)
	if pPlot.getFeatureType() == iForest:
		if not pPlot.getFeatureType() == iTaiga:
			#Changed from Tundra to Taiga
			pPlot.setTerrainType(iTaiga, True, True)
			pPlot.setFeatureType(iForest, 2)

def effectNested(caster):
	iX = caster.getX()
	iY = caster.getY()

	for i in xrange(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(i)
		if pPlayer.isAlive():
			if pPlayer.getCivilizationType() == iFrozen:
				pFrozen = pPlayer
				break
		else:
			pFrozen = gc.getPlayer(gc.getORC_PLAYER())

	iRand = CyGame().getSorenRandNum(100, "Nested")
	iNumYoung = CyGame().getSorenRandNum(2, "Nested") + 1
	print ("Number of Young = %d" % (iNumYoung))
	if iRand <= 15:
		for i in xrange(iNumYoung - 1):
			pFrozen.initUnit(iYoung, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		caster.kill(True, PlayerTypes.NO_PLAYER)

def effectYoung(caster):
	pPlot = caster.plot()
	bFrozen = False
	if not caster.getUnitType() == iYoung:
		return

	iRand = CyGame().getSorenRandNum(100, "Young")
	if iRand <= 30:
		caster.kill(True, PlayerTypes.NO_PLAYER)

def spellSummonWinterCreatures(pCaster):
	iPlayer		= pCaster.getOwner()
	pPlayer		= gc.getPlayer(iPlayer)
	iCaster		= pCaster.getID()
	git			= gc.getInfoTypeForString
	if pPlayer.isHuman():
		popupInfo	= CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("passToModNetMessage")
		popupInfo.setData1(iCaster)
		popupInfo.setData2(iPlayer)
		popupInfo.setData3(117) # onModNetMessage id
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENTTRIGGER_SUMMON_WINTER_CREATURES", ()))
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_SUMMON_FROSTLINGS", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_SUMMON_WINTER_WOLVES", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_SUMMON_KOCRACHON", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_SUMMON_ICE_ELEMENTALS", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_SUMMON_AQUILAN", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_SUMMON_FROST_GIANT", ()),"")
		popupInfo.addPopup(iPlayer)
	else:
		AIPick = CyGame().getSorenRandNum(6, "WinterCreature AI pick")
		argsList = [AIPick,iCaster,iPlayer]
		effectWinterCreature(argsList)

def effectWinterCreature(argsList):
	iButtonId		= argsList[0]
	iCaster			= argsList[1]
	iPlayer			= argsList[2]
	git				= gc.getInfoTypeForString
	pPlayer			= gc.getPlayer(iPlayer)
	pCaster			= pPlayer.getUnit(iCaster)
	pPlot			= pCaster.plot()
	lSpell			= [[git("SPELL_SUMMON_FROSTLING_WARRIOR_GREATOR"),git("SPELL_SUMMON_FROSTLING_ARCHER_GREATOR")],[git("SPELL_SUMMON_WINTER_WOLF_GREATOR")],[git("SPELL_SUMMON_KOCRACHON_GREATOR")],[git("SPELL_SUMMON_ICE_ELEMENTAL_GREATOR")],[git("SPELL_SUMMON_AQUILAN_GREATOR")],[git("SPELL_SUMMON_FROST_GIANT_GREATER")]]
	for iSpell in lSpell[iButtonId]:
		pCaster.cast(iSpell)

def reqWinterCreatureSummoning(caster):
	return False
#End of Frozen
