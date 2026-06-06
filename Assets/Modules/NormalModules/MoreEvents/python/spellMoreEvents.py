## MODULAR PYTHON FOR THE MEKARA ORDER MODULE
## Eric 'Jheral' Lindroth
## Last Edited: 23-june-2010
## ericl87@hotmail.com

from CvPythonExtensions import *
import PyHelpers
import CvEventInterface
import CvUtil
import CvScreensInterface
from BasicFunctions import *
import CvSpellInterface

import ScenarioFunctions
sf                  = ScenarioFunctions.ScenarioFunctions()
PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
localText = CyTranslator()

def doSpawnUndead (pPlot):
	bDemonPlayer 	= gc.getPlayer(gc.getDEMON_PLAYER())
	iX = pPlot.getX()
	iY = pPlot.getY()
	iSkeleton = getInfoType('UNIT_SKELETON')
	iSpectre = getInfoType('UNIT_SPECTRE')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if not pPlot2.isWater():
				if pPlot2.getNumUnits() == 0:
					if not pPlot2.isCity():
						Rand = CyGame().getSorenRandNum(500, "spawn Undead")
						if Rand <= 300:
							newUnit = bDemonPlayer.initUnit(iSkeleton, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						else :
							if Rand<=400:
								newUnit = bDemonPlayer.initUnit(iSpectre, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# Unused?
def doSpawnDemon (pPlot):
	bDemonPlayer 	= gc.getPlayer(gc.getDEMON_PLAYER())
	iX = pPlot.getX()
	iY = pPlot.getY()
	iChampion = getInfoType('UNIT_CHAMPION')
	iBalor = getInfoType('UNIT_BALOR')
	iDemon=getInfoType('PROMOTION_DEMON')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if not pPlot2.isWater():
				if pPlot2.getNumUnits() == 0:
					if not pPlot2.isCity():
						Rand = CyGame().getSorenRandNum(500, "spawn Undead")
						if Rand <= 300:
							newUnit = bDemonPlayer.initUnit(iChampion, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							newUnit.setHasPromotion(iDemon, True)
						else :
							if Rand<=325:
								newUnit = bDemonPlayer.initUnit(iBalor, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doSpawnOrc (pPlot):
	bDemonPlayer 	= gc.getPlayer(gc.getORC_PLAYER())
	iX = pPlot.getX()
	iY = pPlot.getY()
	iChampion = getInfoType('UNIT_CHAMPION')
	iAxeman = getInfoType('UNIT_AXEMAN')
	iOrc=getInfoType('PROMOTION_ORC')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if not pPlot2.isWater():
				if pPlot2.getNumUnits() == 0:
					if not pPlot2.isCity():
						Rand = CyGame().getSorenRandNum(500, "spawn Undead")
						if Rand <= 300:
							newUnit = bDemonPlayer.initUnit(iAxeman, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							newUnit.setHasPromotion(iOrc, True)
						else :
							if Rand<=400:
								newUnit = bDemonPlayer.initUnit(iChampion, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.setHasPromotion(iOrc, True)

# Unused?
def doSpawnDoviello (pPlot):
	bDemonPlayer 	= gc.getPlayer(gc.getORC_PLAYER())
	iX = pPlot.getX()
	iY = pPlot.getY()
	iChampion = getInfoType('UNIT_BATTLEMASTER')
	iAxeman = getInfoType('UNIT_SONS_OF_ASENA')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if not pPlot2.isWater():
				if pPlot2.getNumUnits() == 0:
					if not pPlot2.isCity():
						Rand = CyGame().getSorenRandNum(500, "spawn Undead")
						if Rand <= 300:
							newUnit = bDemonPlayer.initUnit(iAxeman, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						else :
							if Rand<=400:
								newUnit = bDemonPlayer.initUnit(iChampion, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def doSpawnLizard (pPlot):
	bDemonPlayer 	= gc.getPlayer(gc.getORC_PLAYER())
	iX = pPlot.getX()
	iY = pPlot.getY()
	iChampion = getInfoType('UNIT_CHAMPION')
	iBlowpipe = getInfoType('UNIT_LIZARD_BLOWPIPE')
	iLizard=getInfoType('PROMOTION_LIZARDMAN')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if not pPlot2.isWater():
				if pPlot2.getNumUnits() == 0:
					if not pPlot2.isCity():
						Rand = CyGame().getSorenRandNum(500, "spawn Undead")
						if Rand <= 300:
							newUnit = bDemonPlayer.initUnit(iBlowpipe, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						else :
							if Rand<=400:
								newUnit = bDemonPlayer.initUnit(iChampion, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.setHasPromotion(iLizard, True)

def doSpawnBeast(pPlot):
	pDemonPlayer 	= gc.getPlayer(gc.getANIMAL_PLAYER())
	iX = pPlot.getX()
	iY = pPlot.getY()
	iBear = getInfoType('UNIT_CAVE_BEARS')
	iLion = getInfoType('UNIT_LION')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if not pPlot2.isWater():
				if pPlot2.getNumUnits() == 0:
					if not pPlot2.isCity():
						Rand = CyGame().getSorenRandNum(500, "spawn Undead")
						if Rand <= 300:
							newUnit = pDemonPlayer.initUnit(iLion, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						else :
							if Rand<=350:
								newUnit = pDemonPlayer.initUnit(iBear, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


# Unused?
def doSpawnWaterBeast(pPlot):
	bDemonPlayer 	= gc.getPlayer(gc.getANIMAL_PLAYER())
	iX = pPlot.getX()
	iY = pPlot.getY()
	iBunyip = getInfoType('UNIT_BUNYIP')
	iSeaSerpent = getInfoType('UNIT_SEA_SERPENT')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if pPlot2.isWater():
				if pPlot2.getNumUnits() == 0:
					Rand = CyGame().getSorenRandNum(500, "spawn Undead")
					if Rand <= 150:
						newUnit = bDemonPlayer.initUnit(iSeaSerpent, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# Unused?
def doSpawnWaterUndead(pPlot):
	bDemonPlayer 	= gc.getPlayer(gc.getDEMON_PLAYER())
	iX = pPlot.getX()
	iY = pPlot.getY()
	iDrown = getInfoType('UNIT_DROWN')
	iStygian = getInfoType('UNIT_STYGIAN_GUARD')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if pPlot2.isWater():
				if pPlot2.getNumUnits() == 0:
					Rand = CyGame().getSorenRandNum(500, "spawn Undead")
					if Rand <= 300:
						bValid = True
						if bValid :
							newUnit = bDemonPlayer.initUnit(iDrown, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					else :
						if Rand<=350:
							newUnit = bDemonPlayer.initUnit(iStygian, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def onMoveSearchableUF(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iImprovement	= pPlot.getImprovementType()
	# There's probably a cleaner way to pass the improvement name string somehow rather than a quick search, but not seeing it rn
	for sImp in getSearchableUFList():
		if iImprovement != gc.getInfoTypeForString("IMPROVEMENT_" + sImp):
			continue
		if not pPlayer.isHasFlag(getInfoType("FLAG_TREASURE_HUNTER_" + sImp)):
			continue
		doTreasureHunterNewSearch(iPlayer, pPlayer, iImprovement)
		return

def onMoveBrokenSepulcher(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iImprovement	= pPlot.getImprovementType()
	iCaster			= pCaster.getID()
	if pPlayer.isHasFlag(getInfoType('FLAG_TREASURE_HUNTER_BROKEN_SEPULCHER')):
		doTreasureHunterNewSearch(iPlayer, pPlayer, iImprovement)
		doSpawnUndead(pPlot)
	if ((pCaster.isHasPromotion(getInfoType('PROMOTION_GELA'))) and (not (pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_INFERNAL"))) and (pPlayer.getAlignment() == getInfoType('ALIGNMENT_EVIL')) ):
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("effectHumanGelaImprovement")
			popupInfo.setData1(iCaster)
			popupInfo.setData2(iPlayer)
			popupInfo.setData3(iImprovement)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_GELA_BROKEN_SEPULCHER", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_YES", ()),"")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_NO", ()),"")
			popupInfo.addPopup(iPlayer)
		else:
			argsList = [0,iCaster,iPlayer,iImprovement]
			effectGelaImprovement(argsList)

def onMoveMountKalshekk(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iImprovement	= pPlot.getImprovementType()
	if pPlayer.isHasFlag(getInfoType('FLAG_TREASURE_HUNTER_MOUNT_KALSHEKK')):
		doTreasureHunterNewSearch(iPlayer, pPlayer, iImprovement)
		doSpawnLizard(pPlot)

def onMovePyreofTheSeraphic(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iImprovement	= pPlot.getImprovementType()
	iCaster			= pCaster.getID()
	if pPlayer.isHasFlag(getInfoType('FLAG_TREASURE_HUNTER_PYRE_OF_THE_SERAPHIC')):
		doTreasureHunterNewSearch(iPlayer, pPlayer, iImprovement)
		doSpawnOrc(pPlot)
	if ((pCaster.isHasPromotion(getInfoType('PROMOTION_GELA'))) and (not (pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_INFERNAL")))):
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("effectHumanGelaImprovement")
			popupInfo.setData1(iCaster)
			popupInfo.setData2(iPlayer)
			popupInfo.setData3(iImprovement)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_GELA_PYRE_OF_THE_SERAPHIC", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_YES", ()),"")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_NO", ()),"")
			popupInfo.addPopup(iPlayer)
		else:
			argsList = [0,iCaster,iPlayer,iImprovement]
			effectGelaImprovement(argsList)

def onMoveYggdrasil(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iImprovement	= pPlot.getImprovementType()
	if pPlayer.isHasFlag(getInfoType('FLAG_TREASURE_HUNTER_YGGDRASIL')):
		doTreasureHunterNewSearch(iPlayer, pPlayer, iImprovement)
		doSpawnBeast(pPlot)

def onMoveLetumFrigus2(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	git				= gc.getInfoTypeForString
	iImprovement	= pPlot.getImprovementType()
	if pPlayer.isHasFlag(git('FLAG_TREASURE_HUNTER_LETUM_FRIGUS')):
		doTreasureHunterNewSearch(iPlayer, pPlayer, iImprovement)
	elif not pPlayer.isHasFlag(git("FLAG_LETUM_FRIGUS_FIRST_TIME")):
		pPlayer.setHasFlag(git("FLAG_LETUM_FRIGUS_FIRST_TIME"), True)
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_EVENT_LETUM_FRIGUS", ()),'',3,'Art/Interface/Buttons/Improvements/letumfrigus.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		if pPlayer.getCivilizationType() == git("CIVILIZATION_ILLIANS"):
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_EVENT_LETUM_FRIGUS_3_HELP", ()),'',3,'Art/Interface/Buttons/Improvements/letumfrigus.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_EVENT_LETUM_FRIGUS_3", ()),'',3,'Art/Interface/Buttons/Improvements/letumfrigus.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			if not gc.isNoCrash():
				pPlayer.setHasTrait(git('TRAIT_AGGRESSIVE'),True,-1,True,True)
			else:
				pPlayer.setHasTrait(git('TRAIT_AGGRESSIVE'),True)
		elif pPlayer.getCivilizationType() == git("CIVILIZATION_AMURITES"):
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_EVENT_LETUM_FRIGUS_2", ()),'',3,'Art/Interface/Buttons/Improvements/letumfrigus.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())

def onMovePoolOfTears2(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	git				= gc.getInfoTypeForString
	iImprovement	= pPlot.getImprovementType()
	lIllness		= [git("PROMOTION_DISEASED"),git("PROMOTION_PLAGUED"),git("PROMOTION_POISONED"),git("PROMOTION_WITHERED")]
	for iPromotion in lIllness:
		if pCaster.isHasPromotion(iPromotion):
			pCaster.setHasPromotion(iPromotion, False)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POOL_OF_TEARS_CURED",(gc.getUnitInfo(pCaster.getUnitType()).getTextKey(),gc.getPromotionInfo(iPromotion).getTextKey())),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/pooloftears.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
	if pPlayer.isHasFlag(git('FLAG_TREASURE_HUNTER_POOL_OF_TEARS')):
		doTreasureHunterNewSearch(iPlayer, pPlayer, iImprovement)
	elif ((pCaster.isHasPromotion(getInfoType('PROMOTION_GELA'))) and (not (pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_INFERNAL"))) ):
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("effectHumanGelaImprovement")
			popupInfo.setData1(iCaster)
			popupInfo.setData2(iPlayer)
			popupInfo.setData3(iImprovement)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_GELA_POOL_OF_TEARS", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_YES", ()),"")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_NO", ()),"")
			popupInfo.addPopup(iPlayer)
		else:
			argsList = [0,iCaster,iPlayer,iImprovement]
			effectGelaImprovement(argsList)

def onMoveSironasBeacon2(pCaster, pPlot):
	# pPlayer = gc.getPlayer(pCaster.getOwner())
	# if pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_SIRONAS_BEACON) == False:

	#	if pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_ELOHIM"):
	#		iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_SIRONAS_BEACON_ELOHIM')
	#		triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCaster.getX(), pCaster.getY(), -1, -1, -1, -1, -1, -1)
	#		pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_SIRONAS_BEACON, True)
	onMoveSearchableUF(pCaster, pPlot)

def onMoveMirrorOfHeaven2(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.onMoveMirrorOfHeaven(pCaster, pPlot)
		return
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iImprovement	= pPlot.getImprovementType()
	iCaster			= pCaster.getID()
	pCapital		= pPlayer.getCapitalCity()
	if pPlayer.isHasFlag(getInfoType('FLAG_TREASURE_HUNTER_MIRROR_OF_HEAVEN')):
		doTreasureHunterNewSearch(iPlayer, pPlayer, iImprovement)
	elif not pCapital.isNone() and pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_MIRROR_OF_HEAVEN) == False and pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_MALAKIM"):
		pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_MIRROR_OF_HEAVEN, True) # If set locally in another function, popups for human players will queue up
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setOption2(True)
			popupInfo.setFlags(126)
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("passToModNetMessage")
			popupInfo.setData1(iPlayer)
			popupInfo.setData3(105) # onModNetMessage id
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_MALAKIM_MIRROR", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MALAKIM_MIRROR_1", ()),"EVENT_MALAKIM_MIRROR_1")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MALAKIM_MIRROR_2", ()),"EVENT_MALAKIM_MIRROR_2")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_MALAKIM_MIRROR_3", ()),"EVENT_MALAKIM_MIRROR_3")
			popupInfo.addPopup(iPlayer)
		else:
			AIPick = CyGame().getSorenRandNum(2, "MalakimMirror AI pick") + 1
			argsList = [AIPick,iPlayer]
			CvSpellInterface.effectMalakimMirror(argsList) ### TODO CHECK CALL FROM CORE SPELL FILE
	elif ((pCaster.isHasPromotion(getInfoType('PROMOTION_GELA'))) and (not (pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_INFERNAL"))) and (pPlayer.getAlignment() == getInfoType('ALIGNMENT_GOOD')) ):
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("effectHumanGelaImprovement")
			popupInfo.setData1(iCaster)
			popupInfo.setData2(iPlayer)
			popupInfo.setData3(iImprovement)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_GELA_MIRROR_OF_HEAVEN", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_YES", ()),"")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_NO", ()),"")
			popupInfo.addPopup(iPlayer)
		else:
			argsList = [0,iCaster,iPlayer,iImprovement]
			effectGelaImprovement(argsList)

def onMoveRemnantsOfPatria2(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	git				= gc.getInfoTypeForString
	iImprovement	= pPlot.getImprovementType()
	if pPlayer.isHasFlag(git('FLAG_TREASURE_HUNTER_REMNANTS_OF_PATRIA')):
		doTreasureHunterNewSearch(iPlayer, pPlayer, iImprovement)
	elif pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_REMNANTS_OF_PATRIA) == False:
		if pPlayer.getCivilizationType() == git("CIVILIZATION_SCIONS"):
			pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_REMNANTS_OF_PATRIA, True)
			newUnit1 = pPlayer.initUnit(git('UNIT_SUPPLIES'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit2 = pPlayer.initUnit(git('UNIT_SUPPLIES'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REMNANTS_OF_PATRIA_SCIONS", ()),'',3,"Art/Interface/Buttons/Improvements/remnantsofpatria.dds",git("COLOR_GREEN"),pPlot.getX(),pPlot.getY(),True,True)

def onMoveOdiosPrison2(pCaster, pPlot):
	# pPlayer = gc.getPlayer(pCaster.getOwner())
	# if pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_ODIOS_PRISON) == False:

	#	if pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_ELOHIM"):
	#		iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_ODIOS_PRISON_ELOHIM')
	#		triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCaster.getX(), pCaster.getY(), -1, -1, -1, -1, -1, -1)
	onMoveSearchableUF(pCaster, pPlot)

def onMoveBradelinesWell2(pCaster, pPlot):
	# pPlayer = gc.getPlayer(pCaster.getOwner())
	# if pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_BRADELINES_WELL) == False:
	#	if pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_ELOHIM"):
	#		iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_BRADELINES_WELL_ELOHIM')
	#		triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCaster.getX(), pCaster.getY(), -1, -1, -1, -1, -1, -1)
	#		pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_BRADELINES_WELL, True)
	#		pPlot.setImprovementType(getInfoType("IMPROVEMENT_BRADELINES_WELL_PURIFIED"))
	onMoveSearchableUF(pCaster, pPlot)

def onMoveFoxford2(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iImprovement	= pPlot.getImprovementType()
	git				= gc.getInfoTypeForString
	iCaster			= pCaster.getID()
	pDemonPlayer	= gc.getPlayer(gc.getDEMON_PLAYER())
	if pPlayer.isHasFlag(git('FLAG_TREASURE_HUNTER_FOXFORD')):
		doTreasureHunterNewSearch(iPlayer, pPlayer, iImprovement)
	elif not pDemonPlayer.isHasFlag(git("FLAG_FOXFORD_FIRST_TIME")): # Flag is set globally, and even if a new player is presented to the game, the flag value for the demon player would be right
		if not pPlayer.isBarbarian():
			gc.getGame().setGlobalFlag(git("FLAG_FOXFORD_FIRST_TIME"),True) # If set locally in another function, popups for human players will queue up
			if pPlayer.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setOption2(True)
				popupInfo.setFlags(126)
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setOnClickedPythonCallback("passToModNetMessage")
				popupInfo.setData1(iCaster)
				popupInfo.setData2(iPlayer)
				popupInfo.setData3(106)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_FOXFORD", ()))
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_FOXFORD_1", ()),"EVENT_FOXFORD_1")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_FOXFORD_2", ()),"EVENT_FOXFORD_2")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_FOXFORD_3", ()),"EVENT_FOXFORD_3")
				popupInfo.addPopup(iPlayer)
			else:
				if pPlayer.getAlignment() == git("ALIGNMENT_EVIL") or pPlayer.getLeaderType() == git("LEADER_DUIN"):
					iButtonId = 1
				else:
					iButtonId = 0
				argsList = [iButtonId,iCaster,iPlayer]
				CvSpellInterface.effectFoxford(argsList) ### TODO CHECK CALL FROM CORE SPELL FILE

def onMoveMaelstrom2(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iCaster			= pCaster.getID()
	iImprovement	= pPlot.getImprovementType()
	if ((pCaster.isHasPromotion(getInfoType('PROMOTION_GELA'))) and (not (pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_INFERNAL"))) ):
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("effectHumanGelaImprovement")
			popupInfo.setData1(iCaster)
			popupInfo.setData2(iPlayer)
			popupInfo.setData3(iImprovement)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_GELA_MAELSTROM", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_YES", ()),"")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_NO", ()),"")
			popupInfo.addPopup(iPlayer)
		else:
			argsList = [0,iCaster,iPlayer,iImprovement]
			effectGelaImprovement(argsList)
	else:
		if CyGame().getSorenRandNum(100, "Maelstrom") <= 25:
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_KILL",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			pCaster.kill(True, PlayerTypes.NO_PLAYER)
		else:
			iOcean = getInfoType('TERRAIN_OCEAN')
			iBestValue = 0
			pBestPlot = -1
			for i in range (CyMap().numPlots()):
				iValue = 0
				pTargetPlot = CyMap().plotByIndex(i)
				if pTargetPlot.getTerrainType() == iOcean:
					iValue = CyGame().getSorenRandNum(1000, "Maelstrom")
					if pTargetPlot.isOwned() == False:
						iValue += 1000
					if iValue > iBestValue:
						iBestValue = iValue
						pBestPlot = pTargetPlot
			if pBestPlot != -1:
				pCaster.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True, False)
				pCaster.setDamage(25, PlayerTypes.NO_PLAYER)
				CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_MOVE",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)

# Core treasure hunter events
def canTriggerTreasureHunter(argsList):
	kTriggeredData = argsList[0]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
		return True
	return False

def doTreasureHunterNewSearch(iPlayer, pPlayer, iSearchedImp):
	pHaven			= pPlayer.getCapitalCity()
	git				= gc.getInfoTypeForString

	# Spawn Patrian, clean up flags
	if pPlayer.isHasFlag(git("FLAG_TREASURE_HUNTER_5")):
		doSpawnPatrian(iPlayer, pPlayer)
		return

	lCounterFlags	= [git("FLAG_TREASURE_HUNTER_5"), git("FLAG_TREASURE_HUNTER_4"), git("FLAG_TREASURE_HUNTER_3"), git("FLAG_TREASURE_HUNTER_2"), git("FLAG_TREASURE_HUNTER_1")]
	# Add next counter flag to the player every time function is called
	for iCounter in lCounterFlags:
		if pPlayer.isHasFlag(iCounter):
			iNextFlag = lCounterFlags.index(iCounter) - 1
			pPlayer.setHasFlag(lCounterFlags[iNextFlag], True)

	# [(flag1, text1), (flag2, text2), ...]
	lCleanImps = calcTreasureHunterCleanLists(pPlayer, iSearchedImp)

	# If Clean list contains at least one improvement start a new search
	if lCleanImps:
		iNewSearchIndex = CyGame().getSorenRandNum(len(lCleanImps), "Treasure Hunter, New Search")
		pPlayer.setHasFlag(lCleanImps[iNewSearchIndex][0], True)
		if pPlayer.isHuman():
			popupInfo	= CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setText(CyTranslator().getText(lCleanImps[iNewSearchIndex][1], ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CONTINUE", ()),"")
			popupInfo.addPopup(iPlayer)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(lCleanImps[iNewSearchIndex][1], ()),'',3,'Art/Interface/Buttons/TechTree/Astronomy.dds',ColorTypes(8),pHaven.getX(),pHaven.getY(),True,True)
	# If Clean list is empty but counter is not reached (small maps) spawn a Patrian
	else:
		doSpawnPatrian(iPlayer, pPlayer)

def reqReviewTreasureHuntClue(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	FlagList = ["FLAG_TREASURE_HUNTER_" + sImp for sImp in getSearchableUFList()]
	for sFlag in FlagList:
		if pPlayer.isHasFlag(gc.getInfoTypeForString(sFlag)):
			return True
	return False

def spellReviewTreasureHuntClue(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if pCaster == -1 or pCaster.isNone():
		return
	iPlayer = pCaster.getOwner()
	for sImp in getSearchableUFList():
		if pPlayer.isHasFlag(gc.getInfoTypeForString("FLAG_TREASURE_HUNTER_" + sImp)):
			CyInterface().addMessage(iPlayer, True, 25, CyTranslator().getText("TXT_KEY_EVENT_TREASURE_HUNTER_" + sImp, ()), '', 3, '', ColorTypes(gc.getInfoTypeForString("COLOR_GREEN")), -1, -1, False, False)
			return

# Orphaned Gobs
def postCombatLossOrphanedGoblin(pCaster, pOpponent):
	git			= gc.getInfoTypeForString
	# If our winning unit (pOpponent) died in the same combat (mutual kill,
	# death-blow, etc.) there is no surviving unit to receive the orphaned-
	# goblin choice, so the event would fire and then throw when the choice is
	# applied to a missing unit.  isDead() (damage >= maxHitPoints, already set
	# by combat resolution) is the correct "was killed" test here -- NOT
	# isAlive(), which only distinguishes a living unit from undead/demons.
	if pOpponent.isDead():
		return
	iPlayer		= pOpponent.getOwner()
	pPlayer		= gc.getPlayer(iPlayer)
	iLostPlayer	= pCaster.getOwner()
	pCapital	= pPlayer.getCapitalCity()
	iUnit		= pOpponent.getID()
	iRnd		= CyGame().getSorenRandNum(100,"OrphanedGoblin")
	if iLostPlayer == gc.getORC_PLAYER() and iRnd < 2:
		if pPlayer.getCivilizationType() == git("CIVILIZATION_DTESH"):
			newUnit = pPlayer.initUnit(git('UNIT_SLAVE_UNDEAD'), pCapital.getX(),pCapital.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_DTESH_SLAVE_NAME", ()))
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_DTESH", ()),'',3,'Art/Interface/Buttons/Promotions/Races/Goblin.dds',ColorTypes(8),pCapital.getX(),pCapital.getY(),True,True)
		elif pPlayer.isHuman():
			popupInfo	= CyPopupInfo()
			popupInfo.setOption2(True)
			popupInfo.setFlags(126)
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("passToModNetMessage")
			popupInfo.setData1(iPlayer)
			popupInfo.setData2(iUnit)
			popupInfo.setData3(120) # onModNetMessage id
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_ORPHANED_GOBLIN", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_1", ()),"EVENT_ORPHANED_GOBLIN_1")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_2", ()),"EVENT_ORPHANED_GOBLIN_2")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_3", ()),"EVENT_ORPHANED_GOBLIN_3")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_ORPHANED_GOBLIN_4", ()),"EVENT_ORPHANED_GOBLIN_4")
			popupInfo.addPopup(iPlayer)
		else:
			if pPlayer.getAlignment() == git("ALIGNMENT_GOOD"):
				AIPick = CyGame().getSorenRandNum(3,"OrphanedGoblin AI pick, Good") + 1
			elif pPlayer.getAlignment() == git("ALIGNMENT_NEUTRAL"):
				AIPick = CyGame().getSorenRandNum(2,"OrphanedGoblin AI pick, Neutral") + 1
			else:
				AIPick = CyGame().getSorenRandNum(3,"OrphanedGoblin AI pick, Evil")
			argsList = [AIPick,iPlayer,iUnit]
			effectOrphanedGoblin(argsList)

def effectOrphanedGoblin(argsList):
	iButtonId		= argsList[0]
	iPlayer			= argsList[1]
	iUnit			= argsList[2]
	git				= gc.getInfoTypeForString
	pPlayer			= gc.getPlayer(iPlayer)
	pUnit			= pPlayer.getUnit(iUnit)
	pPlot			= pUnit.plot()
	iRnd			= CyGame().getSorenRandNum(100,"OrphanedGoblin effect")
	if iButtonId == 0:
		pUnit.setHasPromotion(git('PROMOTION_ORC_SLAYING'), True)
		pUnit.setHasPromotion(git('PROMOTION_CRAZED'), True)
	elif iButtonId == 1:
		pUnit.setHasPromotion(git('PROMOTION_GOBLIN'), True)
	elif iButtonId == 2:
		pNewPlot = findClearPlot(-1, pPlot)
		if pNewPlot != -1:
			if iRnd < 50:
				pGoblinPlayer = gc.getPlayer(gc.getORC_PLAYER())
			else:
				pGoblinPlayer = pPlayer
			newUnit = pGoblinPlayer.initUnit(git('UNIT_GOBLIN'), pNewPlot.getX(),pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(git('PROMOTION_WEAK'), True)
	else:
		pUnit.changeExperience(-1,-1,False,False,False)
		newUnit = pPlayer.initUnit(git('UNIT_GOBLIN'), pPlot.getX(),pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# Gela stuff
def perTurnGela(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString("CIVILIZATION_INFERNAL") and pPlayer.isHuman():
		if not pPlayer.isHasFlag(gc.getInfoTypeForString("FLAG_GELA_START")):
			pPlayer.setHasFlag(gc.getInfoTypeForString("FLAG_GELA_START"), True)
			popupInfo	= CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_GELA", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CONTINUE", ()),"")
			popupInfo.addPopup(pCaster.getOwner())

def effectHumanGelaImprovement(argsList):
	iButtonId		= argsList[0]
	iUnit			= argsList[1]
	iPlayer			= argsList[2]
	iImprovement	= argsList[3]
	CyMessageControl().sendModNetMessage(119,iButtonId,iUnit,iPlayer,iImprovement)

def effectGelaImprovement(argsList):
	iButtonId		= argsList[0]
	iUnit			= argsList[1]
	iPlayer			= argsList[2]
	iImprovement	= argsList[3]
	git				= gc.getInfoTypeForString
	pPlayer			= gc.getPlayer(iPlayer)
	pUnit			= pPlayer.getUnit(iUnit)
	pPlot			= pUnit.plot()
	if iButtonId == 1:
		return
	if iImprovement == git("IMPROVEMENT_BROKEN_SEPULCHER"):
		pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
		for pyCity in PyPlayer(iPlayer).getCityList() :
			pCity = pyCity.GetCy()
			if CyGame().getSorenRandNum(100,"effect Gela, Broken Sepulcher") <= 60:
				newUnit = pPlayer.initUnit(git('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pCity.getPopulation() > 2:
				pCity.changePopulation(-2)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_GELA_BROKEN",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/brokensepulcher.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
	elif iImprovement == git("IMPROVEMENT_MIRROR_OF_HEAVEN"):
		pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
		pUnit.setHasPromotion(git('PROMOTION_TEMP_HELD'), True)
		pUnit.setHasPromotion(git('PROMOTION_SOL'), True)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_GELA_MIRROR",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/mirrorofheaven.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
		pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
		for iPlayer2 in range(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			if (pPlayer2.isAlive()):
				if pPlayer2.getCivilizationType() == git('CIVILIZATION_INFERNAL'):
					pDemonPlayer = pPlayer2
					enemyTeam = pDemonPlayer.getTeam()
					pTeam = gc.getTeam(pPlayer.getTeam())
					pTeam.declareWar(enemyTeam, True, WarPlanTypes.WARPLAN_TOTAL)
		for iiX in range(pUnit.getX()-2, pUnit.getX()+3, 1):
			for iiY in range(pUnit.getY()-2, pUnit.getY()+3, 1):
				pPlot2 = CyMap().plot(iiX,iiY)
				if not pPlot2.isWater() and not pPlot2.isCity() and pPlot2.getNumUnits() == 0 and pPlot2.isFlatlands():
					if CyGame().getSorenRandNum(500, "effect Gela, Hellfire") <= 400:
						iImprovement = pPlot2.getImprovementType()
						bValid = True
						if iImprovement != -1 :
							if gc.getImprovementInfo(iImprovement).isPermanent():
								bValid = False
						if bValid :
							pPlot2.setImprovementType(git('IMPROVEMENT_HELLFIRE'))
							newUnit = pDemonPlayer.initUnit(git('UNIT_SECT_OF_FLIES'), pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							newUnit.setHasPromotion(git('PROMOTION_DEMON'), True)
	elif iImprovement == git("IMPROVEMENT_POOL_OF_TEARS"):
		pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
		pUnit.setHasPromotion(git('PROMOTION_PIKE_OF_TEARS'), True)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/pooloftears.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
		iRnd = CyGame().getSorenRandNum(100, "effect Gela, Pool of Tears, Plague") <= 20
		if iRnd <= 20 or (pPlayer.getStateReligion() != git('RELIGION_FELLOWSHIP_OF_LEAVES') and iRnd <= 50):
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA_PLAGUE",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/pooloftears.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
			for iPlayer2 in range(gc.getMAX_PLAYERS()):
				pPlayer2 = gc.getPlayer(iPlayer2)
				if pPlayer2.getCivilizationType() != git('CIVILIZATION_INFERNAL'):
					for pyCity in PyPlayer(iPlayer2).getCityList() :
						pCity = pyCity.GetCy()
						i = CyGame().getSorenRandNum(5, "Blight")
						i += pCity.getPopulation() - 2
						i -= pCity.totalGoodBuildingHealth()
						pCity.changeEspionageHealthCounter(i)
						py = PyPlayer(iPlayer2)
						for pUnit2 in py.getUnitList():
							if pUnit2.isAlive():
								pUnit2.doDamageNoCaster(10, 100, git('DAMAGE_DEATH'), False)
	elif iImprovement == git("IMPROVEMENT_PYRE_OF_THE_SERAPHIC"):
		pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
		pPlot.setImprovementType(-1)
		if CyGame().getSorenRandNum(100,"effect Gela, Pyre") <= 40:
			pUnit.setHasPromotion(git('PROMOTION_FROZEN_FLAME'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA_PYRE_1",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/pyreoftheseraphic.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
		else:
			mapSize = CyMap().getWorldSize()
			# i from 1 (duel) to 9 (huger)
			i = 1 + mapSize + int(mapSize/5) + int(mapSize/6)
			addBonus('BONUS_MANA',i,'Art/Interface/Buttons/WorldBuilder/mana_button.dds')
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA_PYRE_2",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/pyreoftheseraphic.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
	elif iImprovement == git("IMPROVEMENT_MAELSTROM"):
		pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
		pUnit.kill(True, PlayerTypes.NO_PLAYER)
		if  pPlayer.getStateReligion() == git('RELIGION_OCTOPUS_OVERLORDS'):
			newUnit1 = pPlayer.initUnit(git('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit1.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
			newUnit2 = pPlayer.initUnit(git('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit2.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
			newUnit3 = pPlayer.initUnit(git('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit3.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
			newUnit4 = pPlayer.initUnit(git('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit4.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
			newUnit5 = pPlayer.initUnit(git('UNIT_DISCIPLE_OCTOPUS_OVERLORDS'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit5.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
			newUnit5.setHasPromotion(git('PROMOTION_HERO'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_GELA_1",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
		else:
			iStygianChance = 300
			pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
			for i in range (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.isWater() and pPlot.getNumUnits() == 0:
					if CyGame().getSorenRandNum(10000, "effect Gela, Stygian") <= iStygianChance:
						newUnit = pDemonPlayer.initUnit(git('UNIT_STYGIAN_GUARD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setUnitAIType(git('UNITAI_ANIMAL'))
						newUnit.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
					elif CyGame().getSorenRandNum(10000, "effect Gela, SeaSerpent") <= iStygianChance:
						newUnit = pDemonPlayer.initUnit(git('UNIT_SEA_SERPENT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setUnitAIType(git('UNITAI_ANIMAL'))
						newUnit.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
			CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_GELA_2",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)

CvScreensInterface.effectHumanGelaImprovement	= effectHumanGelaImprovement