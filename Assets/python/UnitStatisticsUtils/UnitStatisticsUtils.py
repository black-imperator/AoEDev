# Unit Statistics Mod
#  by
# Teg_Navanis
# based on Kill List Mod by Roger Bacon

import UnitStatisticsTools
from UnitStatisticsDefines import *


## globals

objUnitStatisticsTools = UnitStatisticsTools.UnitStatisticsTools()



class UnitStatisticsUtils:

	# Initializes UnitStats if there is something wrong with the game (if it hasn't been started
	# with UnitStats running for example).
	def onLoadGame(self):

		unitList = []

		if (g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()):
			for iPlayer in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(iPlayer).isEverAlive()):
					pyPlayer = PyPlayer(iPlayer)
					unitList = unitList + pyPlayer.getUnitList()
		else:
			unitList = PyPlayer(gc.getGame().getActivePlayer()).getUnitList()

		for objUnit in unitList:
			self.setupUnitStats(objUnit)

	def onGameStart(self):

		if (g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()):
			for iPlayer in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(iPlayer).isEverAlive()):
					if(sdObjectExists("UnitStats", gc.getPlayer(iPlayer)) == False and gc.getPlayer(iPlayer) != None):
						sdObjectInit("UnitStats", gc.getPlayer(iPlayer), PlayerStatsData)


	# Begins logging the unit information.
	def beginLoggingUnit(self, strCityName, objUnit, iPlayerID):

		# Get the currently active player
		objPlayer = gc.getPlayer(objUnit.getOwner())

		# Return immediately if the city name passed in is invalid, if this
		# does happen then the unit information will still be logged through
		# the logUnitCreated method.
		if(strCityName == None):
			return

		# Return immediately if the city name passed in is empty, if this
		# does happen then the unit information will still be logged through
		# the logUnitCreated method.
		if(strCityName == ""):
			return

		# Return immediately if the unit passed in is invalid
		if(objUnit == None):
			return

		# Return immediately if the player ID passed in is invalid
		if(objPlayer == None):
			return

		# Get the game clock string
		strGameClock = self.getCurrentGameClockString(objUnit.getOwner())

		# Construct the unit built message
		newBuiltMessage = strGameClock + ": " + gc.getUnitInfo(objUnit.getUnitType()).getDescription() + " " + localText.getText("TXT_KEY_UNITSTATS_BUILTIN", ()) + " " + strCityName + "\n"

		# This call is used instead of updateUnitLog since using
		# updateUnitLog will cause a double entry when the unit is built.
		self.updateUnitLog(objUnit, newBuiltMessage)

		# Log Experience of the unit.

		sdObjectSetVal("UnitStats", objUnit, EXPERIENCE, objUnit.getExperienceTimes100())

		# Log Experience for player stats.
		sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), EXPERIENCE, sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), EXPERIENCE) + objUnit.getExperienceTimes100())

		#This checks the unit for high scores (experience)
		if (g_bTrackHighScore):
			objUnitStatisticsTools.checkHighScoresCurrentUnit([EXPERIENCE], objUnit)


	# Logs the creation of a unit by the player represented by the iPlayerID
	def logUnitCreation(self, objUnit, iPlayerID):

		# Get the currently active player
		objPlayer = gc.getPlayer(objUnit.getOwner())

		# Return immediately if the unit passed in is invalid
		if(objUnit == None):
			return

		# Return immediately if the player ID passed in is invalid
		if(objPlayer == None):
			return

		if (sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		# One line that says which unit and whose, instead of a bare "unit created"
		# followed by an "<id>X<owner>" string that had to be decoded by hand.
		# Deliberately built from objUnit and gc only: this module does not import
		# CvUtil, and it is loaded early enough that adding an import is not worth the
		# risk for a log line.
		iOwner = objUnit.getOwner()
		pOwner = gc.getPlayer(iOwner)
		if pOwner.isNone():
			szOwner = "player %d" % (iOwner,)
		else:
			szOwner = "%s (player %d)" % (pOwner.getName(), iOwner)
		print "unit created: %s id=%d owner=%s at (%d,%d)" % (
			objUnit.getName(), objUnit.getID(), szOwner, objUnit.getX(), objUnit.getY())

		# Save the new unit's location
		sdObjectSetVal("UnitStats", objUnit, PLOT, [objUnit.getX(), objUnit.getY()])

		# Save start turn, start year and starting experience
		sdObjectSetVal("UnitStats", objUnit, STARTTURN, gc.getGame().getGameTurn())
		sdObjectSetVal("UnitStats", objUnit, EXPERIENCE, objUnit.getExperienceTimes100())
		sdObjectSetVal("UnitStats", objUnit, UNITID, str(objUnit.getID()) + "X" + str(objUnit.getOwner()))

		# Get the game clock string
		strGameClock = self.getCurrentGameClockString(objUnit.getOwner())

		# Construct the unit creation message
		newCreatedMessage = "%s: %s " + localText.getText("TXT_KEY_UNITSTATS_CREATED", ()) + "\n"
		newCreatedMessage = newCreatedMessage %(strGameClock, gc.getUnitInfo(objUnit.getUnitType()).getDescription())

		# log the creation message for the unit.
		self.updateUnitLog(objUnit, newCreatedMessage)


		return


	# Logs the movement of a unit
	def logUnitMove(self, objUnit):

		iPlayerID = objUnit.getOwner()

		# Return immediately if the unit passed in is invalid
		if(objUnit == None):
			return

		if (sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		# Get the amount of moves the unit has made in the past and increment
		# it by one.
		iMovementCounter = sdObjectGetVal("UnitStats", objUnit, MOVEMENT_COUNTER) + 1

		# Set the new movement count
		sdObjectSetVal("UnitStats", objUnit, MOVEMENT_COUNTER, iMovementCounter)

		# Set the player statistics movement count.
		sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), MOVEMENT_COUNTER, sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), MOVEMENT_COUNTER) + 1)

		#Check movement high scores
		if (g_bTrackHighScore):
			objUnitStatisticsTools.checkHighScoresCurrentUnit([MOVEMENT_COUNTER], objUnit)


		# If the unit is a transport unit
		if (objUnit.hasCargo()):

			# Get the amount of moves the unit has made with cargo in the past and increment
			# it by one.
			sdObjectSetVal("UnitStats", objUnit, CARGO_COUNTER, sdObjectGetVal("UnitStats", objUnit, CARGO_COUNTER) + 1)

			# Set the player statistics cargo movement count.
			sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), CARGO_COUNTER, sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), CARGO_COUNTER) + 1)

			#Check cargo high scores
			if (g_bTrackHighScore):
				objUnitStatisticsTools.checkHighScoresCurrentUnit([CARGO_COUNTER], objUnit)


	# Logs the setting of the location of the unit.
	# should this really be called every time a unit moves? Maybe we just need
	# to fix all of the players units at the end of their upkeep cycle?
	def logUnitLocation(self, objUnit):

		# Return immediately if the unit passed in is invalid
		if(objUnit == None):
			return

		iDistanceWarped = 0

		if (sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		# Get the old unit location values
		OldPlot = sdObjectGetVal("UnitStats", objUnit, PLOT)

		iOldX = OldPlot[0]
		iOldY = OldPlot[1]

		# Get the new unit location values
		iNewX = objUnit.getX()
		iNewY = objUnit.getY()

		# Set the new unit location values
		sdObjectSetVal("UnitStats", objUnit, PLOT, [iNewX, iNewY])

		# If the old location values and the new location values are valid
		# then calculate the distance between the two
		if(iOldX > 0 and iOldY > 0 and iNewX > 0 and iNewY > 0):
			iDistanceWarped = max(abs(iOldX-iNewX), abs(iOldY-iNewY))

			# Get the old distance warped and add the new distance warped
			newDistanceWarped = sdObjectGetVal("UnitStats", objUnit, WARP) + iDistanceWarped

			# Set the new distance warped amount
			sdObjectSetVal("UnitStats", objUnit, WARP, newDistanceWarped)

			# Set the player statistics distance warped amount.
			sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), WARP, sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), WARP) + iDistanceWarped)

			# Check distance travelled high scores
			if (g_bTrackHighScore):
				objUnitStatisticsTools.checkHighScoresCurrentUnit([WARP], objUnit)

	# Logs everything that is checked every turn (so far, the number of turns fortified)
	def logBeginPlayerTurn(self, argsList):
		iGameTurn, iPlayer = argsList
		pyPlayer = PyPlayer(iPlayer)
		unitList = pyPlayer.getUnitList()
		playerturninformation = sdObjectGetVal("UnitStats", gc.getPlayer(iPlayer), TURNINFORMATION)
		for unit in unitList:
			unitturninformation = sdObjectGetVal("UnitStats", unit, TURNINFORMATION)
			if (unit.fortifyModifier() > 0):
				unitturninformation[0] = unitturninformation[0] + 1
				playerturninformation[0] = playerturninformation[0] + 1
				unitturninformation[1] = unitturninformation[1] + 1
				if (unitturninformation[1] > unitturninformation[2]):
					unitturninformation[2] = unitturninformation[1]
					if (unitturninformation[2] > playerturninformation[2]):
						playerturninformation[2] = unitturninformation[2]
			else:
				unitturninformation[1] = 0
			if (unit.plot().getOwner() != -1):
				objPlotOwner = gc.getPlayer(unit.plot().getOwner())
				objUnitOwner = gc.getPlayer(unit.getOwner())
				if gc.getTeam(objPlotOwner.getTeam()).isAtWar(objUnitOwner.getTeam()):
					unitturninformation[3] = unitturninformation[3] + 1
			sdObjectSetVal("UnitStats", unit, TURNINFORMATION, unitturninformation)
		sdObjectSetVal("UnitStats", gc.getPlayer(iPlayer), TURNINFORMATION, playerturninformation)

		objUnitStatisticsTools.checkHighScoresAllUnits(MAXTURNSFORTIFIED, iPlayer, None)
		objUnitStatisticsTools.checkHighScoresAllUnits(COMMANDO, iPlayer, None)
		objUnitStatisticsTools.checkHighScoresAllUnits(TOTALTURNSFORTIFIED, iPlayer, None)
		objUnitStatisticsTools.checkHighScoresAllUnits(UNITAGE, iPlayer, None)


	# Logs the goody received event
	def logUnitGoodyReceived(self, argsList):

		iPlayer, objPlot, objUnit, iGoodyType = argsList

		# Get the goody information
		objGoodyInfo = gc.getGoodyInfo(iGoodyType)

		# Return immediately if the unit passed in is invalid
		if(objUnit == None):
			return

		# Return immediately if the goody ID passed in is invalid
		if(objGoodyInfo == None):
			return

		# Return immediately if for some reason we haven't been logging the
		# unit.
		if(sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		if (objUnit.getID() != -1):
			# Get the game clock string
			strGameClock = self.getCurrentGameClockString(iPlayer)

			# Construct the unit creation message
			strGoodyDescription = objGoodyInfo.getDescription()
			newGoodyMessage = "%s: %s \n" %(strGameClock, strGoodyDescription)

			# log the goody message for the unit.
			self.updateUnitLog(objUnit, newGoodyMessage)

		# log the goody for player statistics:
		sdObjectSetVal("UnitStats", gc.getPlayer(iPlayer), GOODIES, sdObjectGetVal("UnitStats", gc.getPlayer(iPlayer), GOODIES) + 1)

	# Logs the city acquired event
	def logCityCapture(self, argsList):

		owner,playerType,city,bConquest,bTrade = argsList


		for i in range(city.plot().getNumUnits()):
			objUnit = city.plot().getUnit(i)
			if (objUnit.getOwner() == gc.getGame().getActivePlayer()):
				break
		else:
			return


		# Return immediately if for some reason we haven't been logging the
		# unit.
		if(sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		# Get the game clock string
		strGameClock = self.getCurrentGameClockString(objUnit.getOwner())

		# Construct the city capture message
		strCaptureDescription = "Captured %s from the %s" %(city.getName(), owner.getCivilizationDescriptionKey())
		newCaptureMessage = "%s: %s \n" %(strGameClock, strCaptureDescription)

		# log the capture message for the unit.
		self.updateUnitLog(objUnit, newCaptureMessage)

		# log the capture for player statistics:
		sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), CAPTURECOUNT, sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), CAPTURECOUNT) + 1)


	# Fall from Heaven function. Used when a unit is converted (by various spells, capturing and the like)
	def logUnitConverted(self, pNewUnit, pOldUnit):

		if (sdObjectExists("UnitStats", pOldUnit)):
			pNewUnit.setScriptData(pOldUnit.getScriptData())

		if not (sdObjectExists("UnitStats", pNewUnit)):
			self.setupUnitStats(pNewUnit)

		# Get the game clock string
		strGameClock = self.getCurrentGameClockString(pNewUnit.getOwner())

		oldUnitType = PyInfo.UnitInfo(pOldUnit.getUnitType()).getDescription()
		newUnitType = PyInfo.UnitInfo(pNewUnit.getUnitType()).getDescription()
		oldUnitCiv = PyPlayer(pOldUnit.getOwner()).getCivilizationAdjective()
		newUnitCiv = PyPlayer(pNewUnit.getOwner()).getCivilizationAdjective()

		# Construct the unit upgrade message
		newUpgradeMessage = strGameClock + ": " + localText.getText("TXT_KEY_UNITSTATS_CONVERT", (oldUnitCiv, oldUnitType, newUnitCiv, newUnitType)) +" \n"

		# log the goody message for the unit.
		self.updateUnitLog(pNewUnit, newUpgradeMessage)

		# Updates unit ID and high score references
		self.moveData(pOldUnit, pNewUnit)

	# Logs the upgrade event
	def logUnitUpgraded(self, argsList):

		genericArgs = argsList[0][0]
		pOldUnit = genericArgs[0]
		pNewUnit = genericArgs[1]

		# Return immediately if the unit passed in is invalid
		if(pOldUnit == None):
			return

		# Return immediately if the unit passed in is invalid
		if(pNewUnit == None):
			return

		# Return immediately if for some reason we haven't been logging the
		# unit.
		if(sdObjectExists("UnitStats", pOldUnit) == False):
			self.setupUnitStats(pOldUnit)

		# Return immediately if for some reason we haven't been logging the
		# unit.
		if(sdObjectExists("UnitStats", pNewUnit) == False):
			self.setupUnitStats(pNewUnit)

		# Get the game clock string
		strGameClock = self.getCurrentGameClockString(pNewUnit.getOwner())

		# Construct the unit upgrade message
		newUpgradeMessage = "%s: " + localText.getText("TXT_KEY_UNITSTATS_UPGRADE", ()) +" \n"
		newUpgradeMessage = newUpgradeMessage %(strGameClock, PyInfo.UnitInfo(pOldUnit.getUnitType()).getDescription(), PyInfo.UnitInfo(pNewUnit.getUnitType()).getDescription())

		# log the goody message for the unit.
		self.updateUnitLog(pNewUnit, newUpgradeMessage)

		self.moveData(pOldUnit, pNewUnit)


	# Logs the combat results event	(for the loser)
	def logCombatLoss(self, objWinner, objLoser):

		# Return immediately if the objWinner passed in is invalid
		if(objLoser == None):
			return

		objUnit = objLoser

		# Create an empty data sheet for the unit
		# if for some reason we haven't been logging it
		if(sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		UnitID = str(objUnit.getID())+ "X" + str(objUnit.getOwner())

		#Check defeat odds for high score

		oddsdata = sdObjectGetVal("UnitStats", objUnit, ODDSDATA)

		iCombatOdds = oddsdata[3]

		highestDefeatOdds = sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), HIGHEST_DEFEAT_ODDS)


		if (highestDefeatOdds < iCombatOdds and iCombatOdds < 101):
			sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), HIGHEST_DEFEAT_ODDS, iCombatOdds)


		# Update the total combat odds of the player (results in average if divided by number of combats)
		playerodds = sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), ODDSDATA)
		playerodds += iCombatOdds
		sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), ODDSDATA, playerodds)

	# Logs the combat results event	(for the winner)
	def logCombatResults(self, objWinner, objLoser):

		# Return immediately if the objWinner passed in is invalid
		if(objWinner == None):
			return

		objUnit = objWinner

		# Create an empty data sheet for the unit
		# if for some reason we haven't been logging it
		if(sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		UnitID = str(objUnit.getID())+ "X" + str(objUnit.getOwner())

		# log the experience of the unit
		oldXP = sdObjectGetVal("UnitStats", objUnit, EXPERIENCE)
		newXP = objUnit.getExperienceTimes100() - oldXP


		# Fall from Heaven only: If the defeated unit is a spell or summoned unit, increase the spell count by one
		if g_bFfHMode:
			if not objUnitStatisticsTools.isNotSpell(objLoser):
				oldSpellCount = sdObjectGetVal("UnitStats", objUnit, SPELLCOUNT)
				sdObjectSetVal("UnitStats", objUnit, SPELLCOUNT, oldSpellCount + 1)
				sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), SPELLCOUNT, sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), SPELLCOUNT) + 1)

				if (g_bTrackHighScore):
					objUnitStatisticsTools.checkHighScoresCurrentUnit([SPELLCOUNT], objUnit)
		if (newXP> 0):

			sdObjectSetVal("UnitStats", objUnit, EXPERIENCE, objUnit.getExperienceTimes100())
			# log experience for player stats.
			sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), EXPERIENCE, sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), EXPERIENCE) + newXP)



		oddsdata = sdObjectGetVal("UnitStats", objUnit, ODDSDATA)
		iCombatOdds = oddsdata[3]

		# Update the total combat odds of the player (results in average if divided by number of combats)
		playerodds = sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), ODDSDATA)
		playerodds += iCombatOdds
		sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), ODDSDATA, playerodds)

		# store oddsdata list
		sdObjectSetVal("UnitStats", objUnit, ODDSDATA, oddsdata)


		# Check combat high scores
		if (g_bTrackHighScore):
			objUnitStatisticsTools.checkHighScoresCurrentUnit([BATTLECOUNT, BODYCOUNT, EXPERIENCE, BESTODDS, LIFEODDS, AVERAGEODDSHIGHEST, AVERAGEODDSLOWEST], objWinner)

			highestoddsunit = objUnitStatisticsTools.getHighScoreVal("UnitStats", gc.getPlayer(objUnit.getOwner()), "HighscoreUnits", AVERAGEODDSHIGHEST)
			highestodds = objUnitStatisticsTools.getHighScoreVal("UnitStats", gc.getPlayer(objUnit.getOwner()), "Highscores", AVERAGEODDSHIGHEST)
			lowestoddsunit = objUnitStatisticsTools.getHighScoreVal("UnitStats", gc.getPlayer(objUnit.getOwner()), "HighscoreUnits", AVERAGEODDSLOWEST)
			lowestodds = objUnitStatisticsTools.getHighScoreVal("UnitStats", gc.getPlayer(objUnit.getOwner()), "Highscores", AVERAGEODDSLOWEST)

			if (highestoddsunit == UnitID):
				if (sdObjectGetVal("UnitStats", objUnit, AVERAGEODDS) < highestodds):
					objUnitStatisticsTools.checkHighScoresAllUnits(AVERAGEODDSHIGHEST, objUnit.getOwner(), None)

			if (lowestoddsunit == UnitID):
				if (sdObjectGetVal("UnitStats", objUnit, AVERAGEODDS) > lowestodds):
					objUnitStatisticsTools.checkHighScoresAllUnits(AVERAGEODDSLOWEST, objUnit.getOwner(), None)

	def onUnitLost(self, argsList):
		'Unit Lost'
		objUnit = argsList[0]

		# Create an empty data sheet for the unit
		# if for some reason we haven't been logging it
		if(sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		# Get the value whether the unit statistics are deleted or saved
		graveyard = sdObjectGetVal("UnitStats", objUnit, GRAVEYARD)

		# Set the age of the unit
		startturn = sdObjectGetVal("UnitStats", objUnit, STARTTURN)
		unitage = (gc.getGame().getGameTurn() - startturn)
		sdObjectSetVal("UnitStats", objUnit, UNITAGE, unitage)

		# Get an ID string that is unique (unit.getID() isn't unique)
		UnitID = str(objUnit.getID()) + "X" + str(objUnit.getOwner())
		#objUnitInfo = PyInfo.UnitInfo(objUnit.getUnitType()) #This was never used anyway
		if ((g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer()) or objUnit.getOwner() == gc.getGame().getActivePlayer()):

			#this updates the high scores
			highscorelist = HighScoreTypes.keys()
			graveyard = 0
			for htype in highscorelist:
				if (g_bTrackHighScore):
					#if the lost unit had a high score, check for the new high score holder.
					highscoreunit = objUnitStatisticsTools.getHighScoreVal("UnitStats", gc.getPlayer(objUnit.getOwner()), "HighscoreUnits", htype)
					if (highscoreunit == UnitID):
						graveyard = 1
						objUnitStatisticsTools.checkHighScoresAllUnits(htype, objUnit.getOwner(), objUnit)


			objUnitStatisticsTools.cleanGraveYardList(objUnit.getOwner())
			graveyardlist = sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), GRAVEYARDLIST)
			if (graveyardlist.count(0) > 0):
				newplace = graveyardlist.index(0)
				graveyardlist.insert(newplace, UnitID)
				graveyardlist.pop(newplace + 1)
			else:
				graveyardlist.append(UnitID)
			sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), GRAVEYARDLIST, graveyardlist)
			scriptdata = sdObjectGetAll("UnitStats", objUnit)
			objPlot = gc.getMap().plot(graveyardlist.index(UnitID), objUnit.getOwner())
			#self.setupUnitStats(objPlot) #This function takes a unit as argument, not a plot. Calling it on a plot can have unexpected consequences (such as bugging me with asserts all the time)
			sdObjectSetAll("UnitStats", objPlot, scriptdata)
			sdObjectSetVal("UnitStats", objPlot, UNITTYPE, objUnit.getUnitType())

			PromotionList = []
			for i in range(gc.getNumPromotionInfos()):
				if (objUnit.isHasPromotion(i)):
					PromotionList.append(i)
			sdObjectSetVal("UnitStats", objPlot, PROMOTION_LIST, PromotionList)

			sdObjectWipe("UnitStats", objUnit)


	# Logs the promotion of a unit
	def logUnitPromotion(self, objUnit, iPromotionID):


		# Get the promotion information
		objPromotionInfo = gc.getPromotionInfo(iPromotionID)

		# Return immediately if the unit passed in is invalid
		if(objUnit == None):
			return

		# Return immediately if the promotion ID passed in is invalid
		if(objPromotionInfo == None):
			return

		# Return immediately if for some reason we haven't been logging the
		# unit.
		if(sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		# Get the game clock string
		strGameClock = self.getCurrentGameClockString(objUnit.getOwner())

		# Construct the unit promotion message
		newPromoMessage = strGameClock + ": " + localText.getText("TXT_KEY_UNITSTATS_PROMOTION", (objPromotionInfo.getDescription(), ())) + "\n"

		# log the promotion message for the unit.
		self.updateUnitLog(objUnit, newPromoMessage)


	# this function is called when a unit is hit
	# iTrack = 0: attacker's and defender's stats are updated.
	# iTrack = 1: only attacker's stats are updated
	# iTrack = 2: only defender's stats are updated
	def onCombatHit(self, argsList, iTrack):
		'Combat Message'

		genericArgs = argsList[0][0]

		attackerUnit = genericArgs[0]
		defenderUnit = genericArgs[1]
		iTypeofAttack = genericArgs[2]
		iDamage = genericArgs[3]

		# iTypeofAttack
		# 0: (empty, reserved for total damage)
		# 1: Attacker is hit
		# 2: Defender is hit
		# 3: Collateral damage (defender is hit)
		# 4: Flanking strike (defender is hit)
		# 5: Air Strike (defender is hit)
		# 6: Other (FfH magic?) (defender is hit)

		# Decide whether units are tracked.
		bAttackerIsTracked = 0
		bDefenderIsTracked = 0
		if iTrack == 0 or iTrack == 1:
			bAttackerIsTracked = 1

			# Create an empty data sheet for the unit
			# if for some reason we haven't been logging it
			if(sdObjectExists("UnitStats", attackerUnit) == False):
				self.setupUnitStats(attackerUnit)

		if iTrack == 0 or iTrack == 2:
			bDefenderIsTracked = 1

			# Create an empty data sheet for the unit
			# if for some reason we haven't been logging it
			if(sdObjectExists("UnitStats", defenderUnit) == False):
				self.setupUnitStats(defenderUnit)

		# Check whether the units are air units (relevant for combat counter)
		if attackerUnit.getDomainType() == DomainTypes.DOMAIN_AIR:
			bAttIsAir = True
		else:
			bAttIsAir = False

		if defenderUnit.getDomainType() == DomainTypes.DOMAIN_AIR:
			bDefIsAir = True
		else:
			bDefIsAir = False

		# Calculate the damage value, depending on whether it is based off the attacker's or defender's base strength.
		if (iTypeofAttack == 1):

			# Get the damage (attacker)
			damage = iDamage * float(objUnitStatisticsTools.combatStrFunction(attackerUnit, true)) / float(attackerUnit.maxHitPoints())

		else:

			# Get the damage (defender)
			damage = iDamage * float(objUnitStatisticsTools.combatStrFunction(defenderUnit, false)) / float(defenderUnit.maxHitPoints())


		# Updates the attacker's stat if necessary
		if (bAttackerIsTracked):
			self.damageUpdater(attackerUnit, damage, iTypeofAttack, True)

		# Updates the defender's stat if necessary
		if (bDefenderIsTracked):
			self.damageUpdater(defenderUnit, damage, iTypeofAttack, False)

		# Attacker is hit
		if iTypeofAttack == 1:

			# Attacker is killed
			if (attackerUnit.currHitPoints() <= iDamage and not bAttIsAir) or (attackerUnit.currHitPoints() <= 0 and bAttIsAir):

				# log it
				self.UnitLogBattleResult(attackerUnit, defenderUnit, iTypeofAttack, iDamage, iTrack)

				# do some more logging
				if bAttackerIsTracked:
					self.logCombatLoss(defenderUnit, attackerUnit)

				if bDefenderIsTracked:
					self.logCombatResults(defenderUnit, attackerUnit)

				# Update combat counter
				if bAttackerIsTracked:
					self.combatcountUpdater(attackerUnit, objUnitStatisticsTools.returnTypeOfCombat(iTypeofAttack, True, bAttIsAir), 2, attackerUnit.getOwner())

					# Update high score
					if (g_bTrackHighScore and iTypeofAttack < 3):
						objUnitStatisticsTools.checkHighScoresCurrentUnit([DAMAGETYPE[0], DAMAGETYPE[2], DAMAGETYPE[7], DAMAGETYPE[8]], attackerUnit)


				if bDefenderIsTracked:
					self.combatcountUpdater(defenderUnit, objUnitStatisticsTools.returnTypeOfCombat(iTypeofAttack, False, bDefIsAir), 1, defenderUnit.getOwner())

					# Fall from Heaven only: If the defeated unit is a hero, increase the hero counter by one
					if g_bFfHMode:
						if attackerUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO')):
							sdObjectSetVal("UnitStats", defenderUnit, HEROCOUNT, sdObjectGetVal("UnitStats", defenderUnit, HEROCOUNT) + 1)
							sdObjectSetVal("UnitStats", gc.getPlayer(defenderUnit.getOwner()), HEROCOUNT, sdObjectGetVal("UnitStats", gc.getPlayer(defenderUnit.getOwner()), HEROCOUNT) + 1)

							if (g_bTrackHighScore):
								objUnitStatisticsTools.checkHighScoresCurrentUnit([HEROCOUNT], defenderUnit)

					# Update high score
					if (g_bTrackHighScore):
						objUnitStatisticsTools.checkHighScoresCurrentUnit([DAMAGETYPE[0], DAMAGETYPE[1], DAMAGETYPE[7], DAMAGETYPE[9]], defenderUnit)



		# Defender is hit
		if iTypeofAttack > 1:

			# Update combat counter and high scores (for everything but for normal battles, where the counter is in onCombatBegin and the high scores are only calculated when a unit dies)
			if iTypeofAttack > 2:
				if bAttackerIsTracked:
					self.combatcountUpdater(attackerUnit, objUnitStatisticsTools.returnTypeOfCombat(iTypeofAttack, True, bAttIsAir), 0, attackerUnit.getOwner())
				if bDefenderIsTracked:
					self.combatcountUpdater(defenderUnit, objUnitStatisticsTools.returnTypeOfCombat(iTypeofAttack, False, bDefIsAir), 3, defenderUnit.getOwner())

				# Update high scores
				if (g_bTrackHighScore):
					if (bAttackerIsTracked):
						objUnitStatisticsTools.checkHighScoresCurrentUnit([DAMAGETYPE[0], DAMAGETYPE[iTypeofAttack]], attackerUnit)
					if (bDefenderIsTracked):
						objUnitStatisticsTools.checkHighScoresCurrentUnit([DAMAGETYPE[7], DAMAGETYPE[iTypeofAttack + 7]], defenderUnit)


			# Defender is killed
			if (defenderUnit.currHitPoints() <= iDamage and not bDefIsAir) or (defenderUnit.currHitPoints() <= 0 and bDefIsAir):

				# log it
				self.UnitLogBattleResult(attackerUnit, defenderUnit, iTypeofAttack, iDamage, iTrack)

				# do some more logging
				if bAttackerIsTracked:
					self.logCombatResults(attackerUnit, defenderUnit)

				if bDefenderIsTracked:
					self.logCombatLoss(attackerUnit, defenderUnit)

				# Update combat counter
				if bDefenderIsTracked:
					self.combatcountUpdater(defenderUnit, objUnitStatisticsTools.returnTypeOfCombat(iTypeofAttack, False, bDefIsAir), 2, defenderUnit.getOwner())

					# Update high score
					if (g_bTrackHighScore and iTypeofAttack < 3):
						objUnitStatisticsTools.checkHighScoresCurrentUnit([DAMAGETYPE[0], DAMAGETYPE[1], DAMAGETYPE[7], DAMAGETYPE[9]], defenderUnit)


				if bAttackerIsTracked:
					self.combatcountUpdater(attackerUnit, objUnitStatisticsTools.returnTypeOfCombat(iTypeofAttack, True, bAttIsAir), 1, attackerUnit.getOwner())

					# Fall from Heaven only: If the defeated unit is a hero, increase the hero counter by one
					if g_bFfHMode:
						if defenderUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO')):
							sdObjectSetVal("UnitStats", attackerUnit, HEROCOUNT, sdObjectGetVal("UnitStats", attackerUnit, HEROCOUNT) + 1)
							sdObjectSetVal("UnitStats", gc.getPlayer(attackerUnit.getOwner()), HEROCOUNT, sdObjectGetVal("UnitStats", gc.getPlayer(attackerUnit.getOwner()), HEROCOUNT) + 1)

							if (g_bTrackHighScore):
								objUnitStatisticsTools.checkHighScoresCurrentUnit([HEROCOUNT], attackerUnit)


					# Update high score
					if (g_bTrackHighScore and iTypeofAttack < 3):
						objUnitStatisticsTools.checkHighScoresCurrentUnit([DAMAGETYPE[0], DAMAGETYPE[2], DAMAGETYPE[7], DAMAGETYPE[8]], attackerUnit)

	# this function is called when an air unit is intercepted
	# iTrack = 0: attacker's and interceptor's stats are updated.
	# iTrack = 1: only attacker's stats are updated
	# iTrack = 2: only interceptor's stats are updated
	def onAirIntercept(self, argsList, iTrack):
		'Combat Message'

		genericArgs = argsList[0][0]

		attackerUnit = genericArgs[0]
		interceptorUnit = genericArgs[1]
		iOurDamage = genericArgs[2]
		iTheirDamage = genericArgs[3]


		# Updates the units' battle count
		if(iTrack == 0 or iTrack == 2):

			# Create an empty data sheet for the unit
			# if for some reason we haven't been logging it
			if(sdObjectExists("UnitStats", interceptorUnit) == False):
				self.setupUnitStats(interceptorUnit)

			self.combatcountUpdater(interceptorUnit, AIRDEFENSE, 0, interceptorUnit.getOwner())
		if(iTrack == 0 or iTrack == 1):

			# Create an empty data sheet for the unit
			# if for some reason we haven't been logging it
			if(sdObjectExists("UnitStats", attackerUnit) == False):
				self.setupUnitStats(attackerUnit)

			self.combatcountUpdater(attackerUnit, AIRATTACK, 0, attackerUnit.getOwner())


		#if the attacking unit is hurt, call the combatHit event
		if (iOurDamage > 0):
			newArgsList = [[[attackerUnit, interceptorUnit, 1, iOurDamage]]]
			self.onCombatHit(newArgsList, iTrack)

		#if the intercepting unit is hurt, call the combatHit event
		if (iTheirDamage > 0):
			newArgsList = [[[attackerUnit, interceptorUnit, 2, iTheirDamage]]]
			self.onCombatHit(newArgsList, iTrack)


	# this function is called when a unit withdraws from combat
	# iTrack = 0: attacker's and defender's stats are updated.
	# iTrack = 1: only attacker's stats are updated
	# iTrack = 2: only defender's stats are updated
	def onCombatWithdrawal(self, argsList, iTrack):
		'Combat Message'

		genericArgs = argsList[0][0]

		attackerUnit = genericArgs[0]
		defenderUnit = genericArgs[1]


		# Adds a message to the attacker's (withdrawer's) log
		if (iTrack == 0 or iTrack == 1):

			# Create an empty data sheet for the unit
			# if for some reason we haven't been logging it
			if(sdObjectExists("UnitStats", attackerUnit) == False):
				self.setupUnitStats(attackerUnit)

			self.combatcountUpdater(attackerUnit, ATTACK, 3, attackerUnit.getOwner())

			oddsdata = sdObjectGetVal("UnitStats", attackerUnit, ODDSDATA)

			combatodds = str("%.1f%%") %(oddsdata[3])

			strAttackerHealth = str("%.2f") %(int(objUnitStatisticsTools.combatStrFunction(attackerUnit, true)) * float(attackerUnit.currHitPoints()) / float(attackerUnit.maxHitPoints()))
			strBaseStrength = str("%.2f") %(objUnitStatisticsTools.combatStrFunction(attackerUnit, true))

			objDefendingPlayer = PyPlayer(defenderUnit.getOwner())

			defenderCivName = objDefendingPlayer.getCivilizationAdjective()

			# Get the game clock string
			strGameClock = self.getCurrentGameClockString(attackerUnit.getOwner())

			newWithdrawalMessage = strGameClock + ": " + localText.getText("TXT_KEY_UNITSTATS_OWN_WITHDRAWAL", (defenderCivName, gc.getUnitInfo(defenderUnit.getUnitType()).getDescription(), strAttackerHealth, strBaseStrength, combatodds)) + "\n"

			# log the combat message for the unit.
			self.updateUnitLog(attackerUnit, newWithdrawalMessage)

			# log the experience of the unit
			oldXP = sdObjectGetVal("UnitStats", attackerUnit, EXPERIENCE)
			newXP = attackerUnit.getExperienceTimes100() - oldXP

			if (newXP> 0):

				sdObjectSetVal("UnitStats", attackerUnit, EXPERIENCE, attackerUnit.getExperienceTimes100())
				# log experience for player stats.
				sdObjectSetVal("UnitStats", gc.getPlayer(attackerUnit.getOwner()), EXPERIENCE, sdObjectGetVal("UnitStats", gc.getPlayer(attackerUnit.getOwner()), EXPERIENCE) + newXP)


			# Check some high scores
			if (g_bTrackHighScore):
				objUnitStatisticsTools.checkHighScoresCurrentUnit([BATTLECOUNT, LIFEODDS, EXPERIENCE, DAMAGETYPE[0], DAMAGETYPE[2], DAMAGETYPE[7], DAMAGETYPE[8]], attackerUnit)



		# Adds a message to the defender's log
		if (iTrack == 0 or iTrack == 2):

			# Create an empty data sheet for the unit
			# if for some reason we haven't been logging it
			if(sdObjectExists("UnitStats", defenderUnit) == False):
				self.setupUnitStats(defenderUnit)

			self.combatcountUpdater(defenderUnit, DEFENSE, 3, defenderUnit.getOwner())

			oddsdata = sdObjectGetVal("UnitStats", defenderUnit, ODDSDATA)

			combatodds = str("%.1f%%") %(oddsdata[3])

			strDefenderHealth = str("%.2f") %(int(objUnitStatisticsTools.combatStrFunction(defenderUnit, false)) * float(defenderUnit.currHitPoints()) / float(defenderUnit.maxHitPoints()))
			strBaseStrength = str("%.2f") %(objUnitStatisticsTools.combatStrFunction(defenderUnit, false))

			objAttackingPlayer = PyPlayer(attackerUnit.getOwner())

			attackerCivName = objAttackingPlayer.getCivilizationAdjective()

			# Get the game clock string
			strGameClock = self.getCurrentGameClockString(defenderUnit.getOwner())

			newWithdrawalMessage = strGameClock + ": " + localText.getText("TXT_KEY_UNITSTATS_ENEMY_WITHDRAWAL", (attackerCivName, gc.getUnitInfo(attackerUnit.getUnitType()).getDescription(), strDefenderHealth, strBaseStrength, combatodds)) + "\n"

			# log the combat message for the unit.
			self.updateUnitLog(defenderUnit, newWithdrawalMessage)

			# log the experience of the unit
			oldXP = sdObjectGetVal("UnitStats", defenderUnit, EXPERIENCE)
			newXP = defenderUnit.getExperienceTimes100() - oldXP

			if (newXP> 0):

				sdObjectSetVal("UnitStats", defenderUnit, EXPERIENCE, defenderUnit.getExperienceTimes100())
				# log experience for player stats.
				sdObjectSetVal("UnitStats", gc.getPlayer(defenderUnit.getOwner()), EXPERIENCE, sdObjectGetVal("UnitStats", gc.getPlayer(defenderUnit.getOwner()), EXPERIENCE) + newXP)


			# Check some high scores
			if (g_bTrackHighScore):
				objUnitStatisticsTools.checkHighScoresCurrentUnit([BATTLECOUNT, LIFEODDS, EXPERIENCE, DAMAGETYPE[0], DAMAGETYPE[1], DAMAGETYPE[7], DAMAGETYPE[9]], defenderUnit)




	def onCombatBegin(self, argsList, iTrack):
		'Combat Result'

		genericArgs = argsList[0][0]

		attackerUnit = genericArgs[0]
		defenderUnit = genericArgs[1]
		iDefenderOdds = genericArgs[2]

		Unitl = []

		if (iTrack == 0 or iTrack == 1):
			Unitl.append(attackerUnit)

		if (iTrack == 0 or iTrack == 2):
			Unitl.append(defenderUnit)

		# If at least one unit is to be updated, do the whole loop for each unit that has to be updated.
		if (len(Unitl) > 0):
			for objUnit in Unitl:

				# Create an empty data sheet for the unit
				# if for some reason we haven't been logging it
				if(sdObjectExists("UnitStats", objUnit) == False):
					self.setupUnitStats(objUnit)

				UnitID = str(objUnit.getID())+ "X" + str(objUnit.getOwner())

				# get the data for the average odds and the message string displayed
				oddsdata = sdObjectGetVal("UnitStats", objUnit, ODDSDATA)

				if (objUnit == attackerUnit):
					combatodds = iDefenderOdds/10.0
					self.combatcountUpdater(objUnit, ATTACK, 0, objUnit.getOwner())

				elif (objUnit == defenderUnit):
					combatodds = 100 - iDefenderOdds/10.0
					self.combatcountUpdater(objUnit, DEFENSE, 0, objUnit.getOwner())

				#item 0 in the oddsdata list is the additive amount of all combat odds
				oddsdata[0] = oddsdata[0] + combatodds

				#item 1 in the oddsdata list is the number of fights so far. item 0 / item 1 = average odds
				oddsdata[1] = oddsdata[1] + 1

				oddsdata[3] = combatodds

				# store average odds
				sdObjectSetVal("UnitStats", objUnit, AVERAGEODDS, oddsdata[0] / oddsdata[1])

				# store oddsdata list
				sdObjectSetVal("UnitStats", objUnit, ODDSDATA, oddsdata)

				# Get the probability that your unit survives.
				lifeodds = sdObjectGetVal("UnitStats", objUnit, LIFEODDS)
				if lifeodds == 101:
					lifeodds = 100
				if (objUnit == attackerUnit):
					lifeodds = lifeodds * (combatodds + (100 - combatodds) * objUnit.withdrawalProbability() / 100) / 100
				elif (objUnit == defenderUnit):
					lifeodds = lifeodds * combatodds / 100
				sdObjectSetVal("UnitStats", objUnit, LIFEODDS, lifeodds)



	# Returns a combination of the current game turn/year depending on the
	# INI file configuration
	def getCurrentGameClockString(self, iPlayerID):
		strGameClock = ""

		objPlayer = gc.getPlayer(iPlayerID)

		# if the player ID passed in is invalid then return only the game turn
		# regardless if the turn information has been turned off or not.

		strTurn = localText.getText("TXT_KEY_UNITSTATS_TURN", ())

		if(objPlayer == None):
			strCurrentTurn = gc.getGame().getGameTurn()
			strGameClock = strTurn + " %s" %(strCurrentTurn)
			return strGameClock

		# Get the current game turn
		strCurrentTurn = gc.getGame().getGameTurn()

		# Get the current game year
		strCurrentYear = CyGameTextMgr().getInterfaceTimeStr(iPlayerID)

		if(g_bShowLogTurnInformation and g_bShowLogDateInformation):
			if(g_bShowLogTurnInformationFirst):
				strGameClock = strTurn + " %s (%s)" %(strCurrentTurn, strCurrentYear)
			else:
				strGameClock = "%s (" + strTurn + " %s)" %(strCurrentYear, strCurrentTurn)
		elif(g_bShowLogTurnInformation and not g_bShowLogDateInformation):
				strGameClock = strTurn + " %s" %(strCurrentTurn)
		elif(not g_bShowLogTurnInformation and g_bShowLogDateInformation):
				strGameClock = "%s" %(strCurrentYear)
		else:
			strGameClock = strTurn  +" %s (%s)" %(strCurrentTurn, strCurrentYear)

		return strGameClock


	# Updates the log for objUnit with the message
	# passed in through strNewMessage. Returns True if the log was successfully
	# updated False otherwise
	def updateUnitLog(self, objUnit, strNewMessage):
		' boolean - Returns True if the log was successfully updated False otherwise.'

		# Return False immediately if an invalid unit was passed in
		if(objUnit == None):
			return False

		# Return False immediately if an invalid new message was passed in
		if(strNewMessage == None):
			return False

		# Return False immediately if an empty message was passed in
		if(len(strNewMessage) == 0):
			return False

		# Return False immediately if for some reason we haven't been logging
		# the unit.
		if(sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		# Get the units current log
		strUnitLog = sdObjectGetVal("UnitStats", objUnit, LIST)

		# Add the new message to the unit log
		strUnitLog = strUnitLog + strNewMessage

		# Save the updated unit log.
		sdObjectSetVal("UnitStats", objUnit, LIST, strUnitLog)

		return True


	# Updates the UnitID and the high score references when a unit is replaced by another one.
	def moveData(self, pOldUnit, pNewUnit):

		UnitID = str(pNewUnit.getID())+ "X" + str(pNewUnit.getOwner())
		sdObjectSetVal("UnitStats", pNewUnit, UNITID, UnitID)

		objPlayer = gc.getPlayer(pNewUnit.getOwner())

		if pOldUnit.getOwner() == pNewUnit.getOwner():
			highscorelist =[]
			highscorelist = objUnitStatisticsTools.getHighScoresCurrentUnit(pOldUnit, "highscore")
			for htype in highscorelist:
				objUnitStatisticsTools.setHighScoreVal("UnitStats", objPlayer, "HighscoreUnits", htype, UnitID)

			highscorelist =[]
			highscorelistHoF = objUnitStatisticsTools.getHighScoresCurrentUnit(pOldUnit, "halloffame")
			for htype in highscorelistHoF:
				objUnitStatisticsTools.setHighScoreVal("UnitStats", objPlayer, "HighscoreUnitsHoF", htype, UnitID)

		else:

#			#It's important that the unit statistics get properly deleted before the new high scores are generated. OnUnitLost will be
#			#called later again (the standard way), but doing it twice doesn't hurt.
	#		if(pOldUnit.getOwner() == gc.getGame().getActivePlayer() or (g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer())):
	#			self.onUnitLost([pOldUnit])
			if(pNewUnit.getOwner() == gc.getGame().getActivePlayer() or (g_bTrackAllPlayers or gc.getGame().isGameMultiPlayer())):
				highscorelist = objUnitStatisticsTools.getAllHighScores()
				objUnitStatisticsTools.checkHighScoresCurrentUnit(highscorelist, pNewUnit)



	# creates the scriptdata dummy files
	def setupUnitStats(self, objUnit):

		if (sdObjectExists("UnitStats", objUnit) == False):
			sdObjectInit("UnitStats", objUnit, UnitStatsData)

		if(sdObjectExists("UnitStats", gc.getPlayer(objUnit.getOwner())) == False and gc.getPlayer(objUnit.getOwner()) != None):
			sdObjectInit("UnitStats", gc.getPlayer(objUnit.getOwner()), PlayerStatsData)



	# Updates a dictionary in which the number of battles, wins and losses is stored
	def combatcountUpdater(self, objUnit, AttDef, iType, iOwner):

		# Return False immediately if an invalid unit was passed in
		if(objUnit == None):
			return False

		# Create an empty data sheet for the unit
		# if for some reason we haven't been logging it
		if(sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		# The combatcount dictionary looks like this: {ATTACK: [iBattles, iKills, iLosses, iWithdrawals], DEFENSE: [iBattles, iKills, iLosses, iWithdrawals], AIRATTACK: [iBattles, iKills, iLosses], AIRDEFENSE: [iBattles, iKills, iLosses], AIRSTRIKE: [iAttacks, iKills, iLosses, iDefenses], COLLATERAL: [iBattles, iKills, iLosses, iEnemyAttacks]}
		# combatcount[ATTACK][1] is thus the number of kills in attacks, (combatcount[ATTACK][1] + combatcount[DEFENSE][1]) the total number of kills
		if (objUnit != None):
			#updates dictionary for unit
			combatcount = sdObjectGetVal("UnitStats", objUnit, COMBATCOUNT)
			combatcount[AttDef][iType] = combatcount[AttDef][iType] + 1
			sdObjectSetVal("UnitStats", objUnit, COMBATCOUNT, combatcount)

		#updates dictionary for player
		combatcount = sdObjectGetVal("UnitStats", gc.getPlayer(iOwner), COMBATCOUNT)
		combatcount[AttDef][iType] = combatcount[AttDef][iType] + 1
		sdObjectSetVal("UnitStats", gc.getPlayer(iOwner), COMBATCOUNT, combatcount)

	# Updates the damage stats for a unit
	def damageUpdater(self, objUnit, damage, iTypeofAttack, bIsAttacker):

		# Load the player damage stats
		damagestatsplayer = sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), DAMAGESTATS)

		# Load the unit damage stats
		if(objUnit != None):
			damagestatsunit = sdObjectGetVal("UnitStats", objUnit, DAMAGESTATS)

		if (bIsAttacker and not iTypeofAttack == 1):
			sInfOrRec = INFLICTED
		elif (not bIsAttacker and iTypeofAttack == 1):
			sInfOrRec = INFLICTED
		else:
			sInfOrRec = SUFFERED


		# Updates player damage stat
		damagestatsplayer[sInfOrRec][0] = damagestatsplayer[sInfOrRec][0] + damage
		damagestatsplayer[sInfOrRec][iTypeofAttack] = damagestatsplayer[sInfOrRec][iTypeofAttack] + damage

		# Updates unit damage stat
		if (objUnit != None):
			damagestatsunit[sInfOrRec][0] = damagestatsunit[sInfOrRec][0] + damage
			damagestatsunit[sInfOrRec][iTypeofAttack] = damagestatsunit[sInfOrRec][iTypeofAttack] + damage

		# Stores unit damage stats
		if (objUnit != None):
			sdObjectSetVal("UnitStats", objUnit, DAMAGESTATS, damagestatsunit)

		# Stores player damage stats
		sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), DAMAGESTATS, damagestatsplayer)


	# Updates the log when a unit is killed in battle. Called from the onCombatHit function, not onCombatResult
	def UnitLogBattleResult(self, objAttacker, objDefender, iTypeofAttack, iDamage, iTrack):

		# Return False immediately if an invalid unit was passed in
		if(objAttacker == None):
			return False

		if(objDefender == None):
			return False

		# iTypeofAttack
		# 0: (empty, reserved for total damage)
		# 1: Attacker is hit
		# 2: Defender is hit
		# 3: Collateral damage (defender is hit)
		# 4: Flanking strike (defender is hit)
		# 5: Air Strike (defender is hit)
		# 6: Other (FfH magic?) (defender is hit)

		# Determine the winner and combat type
		if (iTypeofAttack == 1):

			objWinner = objDefender
			objLoser = objAttacker

		else:
			objWinner = objAttacker
			objLoser = objDefender


		logUpdateList = []

		# Setting some vars that are the same for both winner and loser

		objWinningPlayer = PyPlayer(objWinner.getOwner())
		objLosingPlayer = PyPlayer(objLoser.getOwner())
		strWinningCivName = objWinningPlayer.getCivilizationAdjective()
		strLosingCivName = objLosingPlayer.getCivilizationAdjective()

		strWinnerHealth = str("%.2f") %(int(objUnitStatisticsTools.combatStrFunction(objWinner, true)) * float(objWinner.currHitPoints()) / float(objWinner.maxHitPoints()))
		baseStrength = str("%.2f") %(objUnitStatisticsTools.combatStrFunction(objWinner, true))

		# Get the game clock string
		strGameClock = self.getCurrentGameClockString(objWinner.getOwner())


		if (iTrack == 0 or iTrack == 1):
			logUpdateList.append(objAttacker)
		if (iTrack == 0 or iTrack == 2):
			logUpdateList.append(objDefender)

		if (len(logUpdateList) > 0):

			for objUnit in logUpdateList:

				# Create an empty data sheet for the unit
				# if for some reason we haven't been logging it
				if(sdObjectExists("UnitStats", objUnit) == False):
					self.setupUnitStats(objUnit)

		# iTypeofAttack
		# 1: Attacker is hit
		# 2: Defender is hit
		# 3: Collateral damage (defender is hit)
		# 4: Flanking strike (defender is hit)
		# 5: Air Strike (defender is hit)
		# 6: Other (FfH magic?) (defender is hit)

				if iTypeofAttack == 4:
					strTypeofAttack = "FLANKING"
				elif iTypeofAttack == 3:
					strTypeofAttack = "COLLATERAL"
				elif iTypeofAttack == 5:
					strTypeofAttack = "AIRSTRIKE"
				elif iTypeofAttack > 5:
					strTypeofAttack = "OTHER"
				elif objUnit == objAttacker:
					strTypeofAttack = "ATTACK"
				elif objUnit == objDefender:
					strTypeofAttack = "DEFENSE"

				strTypeofAttackText = localText.getText("TXT_KEY_UNITSTATS_" + strTypeofAttack, ())


				# Combat odds only for 'normal' combats

				if (iTypeofAttack <= 2 and not objUnit.getDomainType() == DomainTypes.DOMAIN_AIR):

					# Get combat odds

					oddsdata = sdObjectGetVal("UnitStats", objUnit, ODDSDATA)

					iCombatOdds = oddsdata[3]

					strCombatOdds = str("%.1f%%") %(oddsdata[3])

					if objUnit == objWinner:
						newCombatMessage = strGameClock + ": " + localText.getText("TXT_KEY_UNITSTATS_KILL", (strLosingCivName, gc.getUnitInfo(objLoser.getUnitType()).getDescription(), strWinnerHealth, baseStrength, strCombatOdds)) + " (" + strTypeofAttackText + ")\n"


					# if this was the luckiest fight of the unit, save the combat odds as the unit's personal high score
						if (iCombatOdds < sdObjectGetVal("UnitStats", objUnit, BESTODDS) or sdObjectGetVal("UnitStats", objUnit, BESTODDS) == -1):
							sdObjectSetVal("UnitStats", objUnit, BESTODDS, iCombatOdds)

							#item 2 in the oddsdata list contains a string message that will be displayed on the unit statistics page
							oddsdata[2] = localText.getText("TXT_KEY_UNITSTATS_LUCKIEST_FIGHT", ()) + "\n" + newCombatMessage
							sdObjectSetVal("UnitStats", objUnit, ODDSDATA, oddsdata)


				else:
					strCombatOdds = "-"

				if objUnit == objWinner:
					newCombatMessage = strGameClock + ": " + localText.getText("TXT_KEY_UNITSTATS_KILL", (strLosingCivName, gc.getUnitInfo(objLoser.getUnitType()).getDescription(), strWinnerHealth, baseStrength, strCombatOdds)) + " (" + strTypeofAttackText + ")\n"

				elif objUnit == objLoser:
					newCombatMessage = strGameClock + ": " + localText.getText("TXT_KEY_UNITSTATS_KILLED", (strWinningCivName, gc.getUnitInfo(objWinner.getUnitType()).getDescription(), strWinnerHealth, baseStrength, strCombatOdds)) + " (" + strTypeofAttackText + ")\n"

				# log the combat message for the unit.
				self.updateUnitLog(objUnit, newCombatMessage)


	def logSpellCast(self, objUnit, iSpell):

		# Return False immediately if an invalid unit was passed in
		if(objUnit == None):
			return False

		# Create an empty data sheet for the unit
		# if for some reason we haven't been logging it
		if(sdObjectExists("UnitStats", objUnit) == False):
			self.setupUnitStats(objUnit)

		oldCastCount = sdObjectGetVal("UnitStats", objUnit, CASTCOUNT)
		sdObjectSetVal("UnitStats", objUnit, CASTCOUNT, oldCastCount + 1)
		sdObjectSetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), CASTCOUNT, sdObjectGetVal("UnitStats", gc.getPlayer(objUnit.getOwner()), CASTCOUNT) + 1)

		if (g_bTrackHighScore):
			objUnitStatisticsTools.checkHighScoresCurrentUnit([CASTCOUNT], objUnit)
