## MODULAR PYTHON EXAMPLE
## ArcticNightWolf 29-may-2010
## ArcticNightWolf@gmail.com

from CvPythonExtensions import *

import PyHelpers

import FoxDebug
import FoxTools
import time
from BasicFunctions import *
import CvScreensInterface

gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
PyPlayer = PyHelpers.PyPlayer

# def onUnitKilled(self, argsList):
	# 'Unit Killed'
	# pUnit, iAttacker = argsList
	# gc               = CyGlobalContext()
	# cf               = self.cf
	# map              = CyMap()
	# game             = CyGame()
	# iPlayer          = pUnit.getOwner()
	# player           = PyPlayer(iPlayer)
	# attacker         = PyPlayer(iAttacker)
	# pPlayer          = gc.getPlayer(iPlayer)
	# Civ              = self.Civilizations
	# Rel              = self.Religions
	# Promo            = self.Promotions["Effects"]
	# Generic          = self.Promotions["Generic"]
	# Hero             = self.Heroes
	# iCiv             = pPlayer.getCivilizationType()
	# iRel             = pUnit.getReligion()
	# iUnitType        = pUnit.getUnitType()
	# iUnitCombat      = pUnit.getUnitCombatType()
	# # iOwner           = pUnit.getOwner() # Ronkhar: duplicate of iPlayer
	# pPlot            = pUnit.plot()
	# getPlot          = map.plot
	# giftUnit         = cf.giftUnit
	# getXP            = pUnit.getExperienceTimes100
	# hasPromo         = pUnit.isHasPromotion
	# Tech             = self.Techs
	# Frozen           = self.Units["Frozen"]
	# Infernal         = self.Units["Infernal"]
	# Mercurian        = self.Units["Mercurian"]
	# Building         = self.Buildings
	# UnitCombat       = self.UnitCombats
	# addMsg           = CyInterface().addMessage
	# getText          = CyTranslator().getText
	# iNoAI            = UnitAITypes.NO_UNITAI
	# iSouth           = DirectionTypes.DIRECTION_SOUTH
	# randNum          = CyGame().getSorenRandNum

	# # more events mod starts #
	# if pUnit.isHasPromotion(getInfoType('PROMOTION_GOBLIN')):
		# if CyGame().getSorenRandNum(1000, "Goblin2")<20:
			# if iPlayer == gc.getORC_PLAYER() :
				# iX = pUnit.getX()
				# iY = pUnit.getY()
				# int=1
				# pAttacker = gc.getPlayer(iAttacker)
				# for iiX in range(iX-3, iX+2, 1):
					# for iiY in range(iY-3, iY+2, 1):
						# pPlot2 = CyMap().plot(iiX,iiY)
						# for i in range(pPlot2.getNumUnits()):
							# pUnit2 = pPlot2.getUnit(i)
							# if pUnit2.getOwner()== iAttacker:
								# iWorker = getInfoType('UNITCLASS_WORKER')
								# iSettler = getInfoType('UNITCLASS_SETTLER')
								# iHawk = getInfoType('UNITCLASS_HAWK')
								# if not pUnit2.getUnitClassType() == iWorker and not pUnit2.getUnitClassType() == iSettler and not pUnit2.getUnitClassType() == iHawk and int==1 :
									# iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_ORPHANED_GOBLIN')
									# triggerData = pAttacker.initTriggeredData(iEvent, true, -1, pUnit2.getX(), pUnit2.getY(), -1, -1, -1, -1, pUnit2.getID(), -1)
									# int=0
				# # more events mod ends #

def onUnitBuilt(self, argsList):
	'Unit Completed'
	pCity = argsList[0]
	pUnit = argsList[1]

	gc                 = CyGlobalContext()
	cf                 = self.cf
	game               = CyGame()
	map                = CyMap()
	player             = PyPlayer(pCity.getOwner())
	getPlayer          = gc.getPlayer
	pPlayer            = getPlayer(pUnit.getOwner())
	iFreeProm          = pUnit.getFreePromotionPick()
	getNumB            = pCity.getNumBuilding
	getNumAvailBonuses = pPlayer.getNumAvailableBonuses
	iCombatType        = pUnit.getUnitCombatType()
	setPromo           = pUnit.setHasPromotion
	randNum            = game.getSorenRandNum

	Promo      = self.Promotions["Effects"]
	Generic    = self.Promotions["Generic"]
	Race       = self.Promotions["Race"]
	Mana       = self.Mana
	Building   = self.Buildings
	Civ        = self.Civilizations
	Veil       = self.Units["Veil"]
	UnitCombat = self.UnitCombats
	Hero       = self.Heroes
	Terrain    = self.Terrain

	if pUnit.getUnitClassType() == getInfoType('UNITCLASS_ASSASSIN') or pUnit.getUnitClassType() == getInfoType('UNITCLASS_SHADOW'):
		if getNumB(getInfoType('BUILDING_ASSASSIN_CHAPTER_1'))>0:
			setPromo(getInfoType('PROMOTION_ASSASSIN_CHAPTER_1'), True)
		if getNumB(getInfoType('BUILDING_ASSASSIN_CHAPTER_2'))>0:
			setPromo(getInfoType('PROMOTION_ASSASSIN_CHAPTER_2'), True)

#def onUnitPromoted(self, argsList):
#	'Unit Promoted'
#	pUnit, iPromotion = argsList
#	pPlayer =gc.getPlayer(pUnit.getOwner())
#
						# More Events mod starts  #
#	if pPlayer.isHuman():
#		iGela=getInfoType('PROMOTION_GELA')
#		if iPromotion ==iGela :
#			if (not pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_INFERNAL')):
#				iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_GELA')
#				triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, -1, -1, -1, -1, -1, -1)
# r362 Picking up equipment can't trigger onUnitPromoted

def onUnitCreated(self, argsList):
		'Unit Completed'
		pUnit              = argsList[0]
		self.verifyLoaded()
		gc                 = CyGlobalContext()
		cf                 = self.cf
		game               = CyGame()
		player             = PyPlayer(pUnit.getOwner())
		getPlayer          = gc.getPlayer
		pPlayer            = getPlayer(pUnit.getOwner())
		Civ                = self.Civilizations
		Promo              = self.Promotions["Effects"]
		Generic            = self.Promotions["Generic"]
		Race               = self.Promotions["Race"]
		Equipment          = self.Promotions["Equipment"]
		UnitCombat         = self.UnitCombats
		Tech               = self.Techs
		Mana               = self.Mana
		Bannor             = self.Units["Bannor"]
		Mechanos           = self.Units["Mechanos"]
		ScorpClan          = self.Units["Scorpion Clan"]
		Summon             = self.Units["Summons"]
		Scions             = self.Units["Scions"]
		Veil               = self.Units["Veil"]
		setPromo           = pUnit.setHasPromotion
		hasTrait           = pPlayer.hasTrait
		Trait              = self.Traits
		iUnitType          = pUnit.getUnitType()
		initUnit           = pPlayer.initUnit
		getNumAvailBonuses = pPlayer.getNumAvailableBonuses
		getTeam            = gc.getTeam
		hasPromo           = pUnit.isHasPromotion
		randNum            = game.getSorenRandNum
		iNoAI              = UnitAITypes.NO_UNITAI
		iSouth             = DirectionTypes.DIRECTION_SOUTH
		pPlot              = pUnit.plot()
		iX                 = pPlot.getX(); iY = pPlot.getY()


		if iUnitType == getInfoType("UNIT_MURIS_CLAN_WHELP"):
			GoblinChoice = [(getInfoType("UNIT_GOBLIN_MURIS_CLAN"), 10)]

			if pPlot.getNumUnits() > 5:                        GoblinChoice = [(getInfoType("UNIT_MURIS_CLAN_LORD"), 25)]
			if pPlayer.isHasTech( Tech["Bowyers"]):            GoblinChoice = [(getInfoType("UNIT_MURIS_CLAN_SAPPER"), 25), (getInfoType("UNIT_ARCHER_MURIS_CLAN"), 10)]
			elif pPlayer.isHasTech( Tech["Archery"]):          GoblinChoice = [(getInfoType("UNIT_ARCHER_MURIS_CLAN"), 25)]
			if pPlayer.isHasTech( Tech["Stirrups"]):           GoblinChoice = [(getInfoType("UNIT_MURIS_CLAN_WOLF_ARCHER"), 25), (getInfoType("UNIT_WOLF_RIDER_MURIS_CLAN"), 10)]
			elif pPlayer.isHasTech( Tech["Trade"]): GoblinChoice = [(getInfoType("UNIT_WOLF_RIDER_MURIS_CLAN"), 25)]
			if pPlayer.isHasTech( Tech["Military Strategy"]):       GoblinChoice = [(getInfoType("UNIT_CHARIOT_MURIS_CLAN"), 25)]

			getGoblin = wchoice( GoblinChoice, 'Goblin Whelp Upgrade' )
			newUnit = initUnit(getGoblin(), iX, iY, iNoAI, iSouth)
			newUnit.convert(pUnit)
			pUnit = newUnit

def onCityDoTurn(self, argsList):
	'City Production'
	pCity	= argsList[0]
	iPlayer	= argsList[1]
	pPlot	= pCity.plot()
	iPlayer	= pCity.getOwner()
	pPlayer	= gc.getPlayer(iPlayer)
	git		= gc.getInfoTypeForString
	if pPlayer.getCivilizationType() == git('CIVILIZATION_MERCURIANS'):
		for i in xrange(pPlot.getNumUnits()):
			pLoopUnit	= pPlot.getUnit(i)
			iLoopPlayer	= pLoopUnit.getOwner()
			pLoopPlayer	= gc.getPlayer(iLoopPlayer)
			if pLoopUnit.isHasPromotion(git('PROMOTION_GELA')) and pLoopPlayer.getCivilizationType() != git("CIVILIZATION_INFERNAL") and pLoopPlayer.getCivilizationType() != git("CIVILIZATION_MERCURIANS"):
				iCaster	= pLoopUnit.getID()
				if pLoopPlayer.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
					popupInfo.setOnClickedPythonCallback("passToModNetMessage")
					popupInfo.setData1(iCaster)
					popupInfo.setData2(iLoopPlayer)
					popupInfo.setData3(118) # onModNetMessage id
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_GELA_MERCURIANS", ()))
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_YES", ()),"")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_NO", ()),"")
					popupInfo.addPopup(iLoopPlayer)
				else:
					argsList = [0,iCaster,iLoopPlayer]
					effectGelaMercurians(argsList)

def effectGelaMercurians(argsList):
	iButtonId		= argsList[0]
	iUnit			= argsList[1]
	iPlayer			= argsList[2]
	git				= gc.getInfoTypeForString
	pPlayer			= gc.getPlayer(iPlayer)
	pUnit			= pPlayer.getUnit(iUnit)
	if iButtonId == 1:
		return
	pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
	CyGame().changeGlobalCounter(-10)
	pPlayer.changeGlobalCounterContrib(-10)
	newUnit = pPlayer.initUnit(git('UNIT_ANGEL'), pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(git('PROMOTION_HERO'), True)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_BASIUM_GELA",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Units/Basium.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
	for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
		pLoopPlayer	= gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.getCivilizationType() == git('CIVILIZATION_MERCURIANS'):
			pLoopPlayer.AI_changeAttitudeExtra(3,1)
