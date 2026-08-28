## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

import UnitStatisticsUtils
import UnitStatisticsTools
import CvStatisticsScreen
from UnitStatisticsDefines import *


# globals
###################################################

gg = UnitStatisticsTools.UnitStatisticsTools()
g_UnitStatistics = "placeHolder"
#gg = gc.getGame()
#g_UnitStatistics = ModOptionTypes.MODOPTION_UNIT_STATISTICS

objUnitStatisticsUtils = UnitStatisticsUtils.UnitStatisticsUtils()
objUnitStatisticsTools = UnitStatisticsTools.UnitStatisticsTools()



class CvUnitStatisticsEventManager:
	def __init__(self, eventManager):

		#################### ON EVENT MAP ######################
		self.EventKeyDown=6
		self.EventKeyUp=7
		self.eventManager = eventManager

		eventManager.addEventHandler("kbdEvent",self.onKbdEvent)
		eventManager.addEventHandler("combatResult",self.onCombatResult)
		eventManager.addEventHandler("unitBuilt",self.onUnitBuilt)
		eventManager.addEventHandler("unitMove",self.onUnitMove)
		eventManager.addEventHandler("unitSetXY",self.onUnitSetXY)
		eventManager.addEventHandler("unitCreated",self.onUnitCreated)
		eventManager.addEventHandler("unitPromoted",self.onUnitPromoted)
		eventManager.addEventHandler("unitLost",self.onUnitLost)
		eventManager.addEventHandler("unitKilled",self.onUnitKilled)
		eventManager.addEventHandler("goodyReceived",self.onGoodyReceived)
		eventManager.addEventHandler("BeginPlayerTurn",self.onBeginPlayerTurn)
		eventManager.addEventHandler("OnLoad",self.onLoadGame)
		eventManager.addEventHandler("GameStart",self.onGameStart)
		eventManager.setEventHandler("combatHit",self.onCombatHit)
		eventManager.setEventHandler("airIntercept", self.onAirIntercept)
		eventManager.setEventHandler("combatBegin",self.onCombatBegin)
		eventManager.setEventHandler("combatWithdrawal",self.onCombatWithdrawal)
		eventManager.setEventHandler("airStrikeHit", self.onAirStrikeHit)
		eventManager.setEventHandler("unitUpgraded",self.onUnitUpgraded)
		eventManager.setEventHandler("spellCast",self.onSpellCast)
		eventManager.setEventHandler("unitConverted",self.onUnitConverted)
#		eventManager.addEventHandler("cityAcquired",self.onCityAcquired)

	# Displays the unit statistics window if a unit is selected and the letter 'u' was pressed.
	def onKbdEvent(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		eventType,key,mx,my,px,py = argsList
		theKey=int(key)

		# Try to get the selected unit
		objUnit = CyInterface().getSelectionUnit(0)

		if (eventType == self.EventKeyDown and theKey == int(InputTypes.KB_U)):
			statisticsScreen = CvStatisticsScreen.CvStatisticsScreen()
			if (objUnit != None and (objUnit.getOwner() == gc.getGame().getActivePlayer() or g_bShowAllPlayers)):
				statisticsScreen.startScreen(objUnit, "unit")
				return 1
			else:
				statisticsScreen.startScreen(objUnit, "player")
				return 1

		return 0

	# Initializes UnitStats if there is something wrong with the game (if it hasn't been started
	# with UnitStats running for example).
	def onLoadGame(self, argsList):

		if(sdObjectExists("UnitStats", gc.getActivePlayer()) == False):
			objUnitStatisticsUtils.onLoadGame()

	def onGameStart(self, argsList):
		objUnitStatisticsUtils.onGameStart()

	# Logs the unit combat results (now called in onCombatHit)
	def onCombatResult(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return
		pWinner,pLoser = argsList
		# If we got a valid unit log the unit location.
		if(pWinner != None and (pWinner.getOwner() == gc.getGame().getActivePlayer() or (g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer())) and (objUnitStatisticsTools.isNotSpell(pWinner) or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.logCombatResults(pWinner,pLoser)
		if(pLoser != None and (pLoser.getOwner() == gc.getGame().getActivePlayer() or (g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer())) and (objUnitStatisticsTools.isNotSpell(pLoser)or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.logCombatLoss(pWinner,pLoser)


	# Begins logging the unit information
	def onUnitBuilt(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		city = argsList[0]
		unit = argsList[1]
		iPlayerID = city.getOwner()

		# If we got a valid unit and city then begin logging the unit.

		if(unit != None and city != None and ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or unit.getOwner() == gc.getGame().getActivePlayer()) and (unit.getUnitCombatType() != -1 or g_bTrackNonCombatants) and (objUnitStatisticsTools.isNotSpell(unit) or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.beginLoggingUnit(city.getName(), unit, iPlayerID)


	def onUnitMove(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		pPlot,pUnit,pOldPlot = argsList

		# If we got a valid unit log the unit move.

		if(g_bTrackMovement and pUnit != None and ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pUnit.getOwner() == gc.getGame().getActivePlayer()) and (pUnit.getUnitCombatType() != -1 or g_bTrackNonCombatants) and (objUnitStatisticsTools.isNotSpell(pUnit) or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.logUnitMove(pUnit)


	def onUnitSetXY(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		pPlot,pUnit = argsList

		# If we got a valid unit log the unit location.

		if(g_bTrackMovement and pUnit != None and ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pUnit.getOwner() == gc.getGame().getActivePlayer()) and (pUnit.getUnitCombatType() != -1 or g_bTrackNonCombatants) and (objUnitStatisticsTools.isNotSpell(pUnit) or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.logUnitLocation(pUnit)


	# Logs the unit created event information
	def onUnitCreated(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		pUnit = argsList[0]
		iPlayerID = pUnit.getOwner()

		# If we got a valid unit log the unit creation.

		if(pUnit != None and ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pUnit.getOwner() == gc.getGame().getActivePlayer()) and (pUnit.getUnitCombatType() != -1 or g_bTrackNonCombatants) and (objUnitStatisticsTools.isNotSpell(pUnit)or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.logUnitCreation(pUnit, iPlayerID)

		# For non-combat-units, create a dummy-file in order to avoid problems with the high score calculation
		elif(pUnit != None and ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pUnit.getOwner() == gc.getGame().getActivePlayer())):
			objUnitStatisticsUtils.setupUnitStats(pUnit)
			SdToolKitAdvanced.sdObjectSetVal("UnitStats", pUnit, STARTTURN, 6000)


	def onUnitLost(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		pUnit = argsList[0]

		if(pUnit != None and ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pUnit.getOwner() == gc.getGame().getActivePlayer()) and (pUnit.getUnitCombatType() != -1 or g_bTrackNonCombatants) and (objUnitStatisticsTools.isNotSpell(pUnit) or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.onUnitLost(argsList)


	# Logs the unit promoted event information
	def onUnitPromoted(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		pUnit, iPromotion = argsList

		# If we got a valid unit log the unit promotion.

		if(g_bTrackUnitPromotions and pUnit != None and ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pUnit.getOwner() == gc.getGame().getActivePlayer()) and (pUnit.getUnitCombatType() != -1 or g_bTrackNonCombatants) and (objUnitStatisticsTools.isNotSpell(pUnit) or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.logUnitPromotion(pUnit, iPromotion)


	# Logs the goody received event information
	def onGoodyReceived(self, argsList):
		'Goody received'

		if not gg.isModOption(g_UnitStatistics):
			return

		iPlayer, pPlot, pUnit, iGoodyType = argsList

		# If we got a valid unit log the unit promotion.

		if(g_bTrackGoodyReceived and pUnit != None and ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pUnit.getOwner() == gc.getGame().getActivePlayer()) and (pUnit.getUnitCombatType() != -1 or g_bTrackNonCombatants) and (objUnitStatisticsTools.isNotSpell(pUnit) or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.logUnitGoodyReceived(argsList)


	def onCombatHit(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		genericArgs = argsList[0][0]
		attackerUnit = genericArgs[0]
		defenderUnit = genericArgs[1]
		iIsAttacker = genericArgs[2]
		iDamage = genericArgs[3]


		# If we got a valid unit log the unit damage.

		iTrack = objUnitStatisticsTools.determineTrackedUnits(attackerUnit, defenderUnit)

		if iTrack != None:
			objUnitStatisticsUtils.onCombatHit(argsList, iTrack)


	def onAirIntercept(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		genericArgs = argsList[0][0]
		attackerUnit = genericArgs[0]
		interceptorUnit = genericArgs[1]
		iIsAttacker = genericArgs[2]
		iDamage = genericArgs[3]


		# If we got a valid unit log the unit damage.


		iTrack = objUnitStatisticsTools.determineTrackedUnits(attackerUnit, interceptorUnit)

		if iTrack != None:
			objUnitStatisticsUtils.onAirIntercept(argsList, iTrack)



	def onAirStrikeHit(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		genericArgs = argsList[0][0]
		attackerUnit = genericArgs[0]
		defenderUnit = genericArgs[1]
		iDamage = genericArgs[2]



		# Determine whether any units are tracked by our statistics, and initiate logging accordingly
		iTrack = objUnitStatisticsTools.determineTrackedUnits(attackerUnit, defenderUnit)

		if iTrack != None:
			objUnitStatisticsUtils.onAirStrikeHit(argsList, iTrack)


	def onCombatBegin(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		genericArgs = argsList[0][0]
		attackerUnit = genericArgs[0]
		defenderUnit = genericArgs[1]
		iDefenderOdds = genericArgs[2]

		# Determine whether any units are tracked by our statistics, and initiate logging accordingly
		iTrack = objUnitStatisticsTools.determineTrackedUnits(attackerUnit, defenderUnit)

		if iTrack != None:
			objUnitStatisticsUtils.onCombatBegin(argsList, iTrack)

	def onCombatWithdrawal(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		genericArgs = argsList[0][0]
		attackerUnit = genericArgs[0]
		defenderUnit = genericArgs[1]

		# Determine whether any units are tracked by our statistics, and initiate logging accordingly
		iTrack = objUnitStatisticsTools.determineTrackedUnits(attackerUnit, defenderUnit)

		if iTrack != None:
			objUnitStatisticsUtils.onCombatWithdrawal(argsList, iTrack)


	def onUnitKilled(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		pUnit = argsList[0]


		if((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pUnit.getOwner() == gc.getGame().getActivePlayer() and (objUnitStatisticsTools.isNotSpell(pUnit) or g_bFfHTrackSpells)):
			for i in range(10):
				objUnitStatisticsTools.checkHighScoresCurrentUnit([DAMAGETYPE[i]], pUnit)

	def onUnitUpgraded(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		genericArgs = argsList[0][0]
		pOldUnit = genericArgs[0]
		pNewUnit = genericArgs[1]

		if((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pOldUnit.getOwner() == gc.getGame().getActivePlayer() or pNewUnit.getOwner() == gc.getGame().getActivePlayer() and (objUnitStatisticsTools.isNotSpell(pNewUnit) or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.logUnitUpgraded(argsList)

	def onUnitConverted(self, argsList):


		if not gg.isModOption(g_UnitStatistics):
			return

		genericArgs = argsList[0][0]
		pNewUnit = genericArgs[0]
		pOldUnit = genericArgs[1]

		if((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pOldUnit.getOwner() == gc.getGame().getActivePlayer() or pNewUnit.getOwner() == gc.getGame().getActivePlayer() and (objUnitStatisticsTools.isNotSpell(pNewUnit) or g_bFfHTrackSpells)):
			objUnitStatisticsUtils.logUnitConverted(pNewUnit, pOldUnit)

## 	Not working.
#	def onCityAcquired(self, argsList):
#		'City Acquired'
#
#		if not gg.isModOption(g_UnitStatistics):
#			return
#
#		owner,playerType,city,bConquest,bTrade = argsList
#		print "city acquired test1"
#
#		if(bConquest and (playerType == gc.getGame().getActivePlayer() or (g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()))):
#			print "city acquired test2"
#			objUnitStatisticsUtils.logCityCapture(argsList)
##

	def onBeginPlayerTurn(self, argsList):

		if not gg.isModOption(g_UnitStatistics):
			return

		iGameTurn, iPlayer = argsList
		if(g_bTrackTurnInformation and ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or iPlayer == gc.getGame().getActivePlayer())):
			objUnitStatisticsUtils.logBeginPlayerTurn(argsList)

	def onSpellCast(self, argsList):

		genericArgs = argsList[0][0]
		pUnit = genericArgs[0]
		iSpell = genericArgs[2]

		if not gg.isModOption(g_UnitStatistics):
			return
		if(g_bFfHMode and (g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or pUnit.getOwner() == gc.getGame().getActivePlayer()):
			objUnitStatisticsUtils.logSpellCast(pUnit, iSpell)
