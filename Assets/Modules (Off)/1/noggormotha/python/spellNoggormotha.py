from CvPythonExtensions import *
from BasicFunctions import *
from CvSpellInterface import *
import PyHelpers
import CvEventInterface
import CvUtil

# Globals
PyPlayer			= PyHelpers.PyPlayer
gc					= CyGlobalContext()
localText			= CyTranslator()
git					= gc.getInfoTypeForString

# Quick list of Keeper Promotions
bKeeperEffect		= git("PROMOTION_KEEPER_EFFECT")
iKeeperLevel01		= git("PROMOTION_NOGGORMOTHA_KEEPER_01")
iKeeperLevel02		= git("PROMOTION_NOGGORMOTHA_KEEPER_02")
iKeeperLevel03		= git("PROMOTION_NOGGORMOTHA_KEEPER_03")
iKeeperLevel04		= git("PROMOTION_NOGGORMOTHA_KEEPER_04")
iKeeperLevel05		= git("PROMOTION_NOGGORMOTHA_KEEPER_05")
iKeeperLevel06		= git("PROMOTION_NOGGORMOTHA_KEEPER_06")
iKeeperLevel07		= git("PROMOTION_NOGGORMOTHA_KEEPER_07")
iKeeperLevel08		= git("PROMOTION_NOGGORMOTHA_KEEPER_08")
iKeeperLevel09		= git("PROMOTION_NOGGORMOTHA_KEEPER_09")
iKeeperLevel10		= git("PROMOTION_NOGGORMOTHA_KEEPER_10")
iKeeperLevel11		= git("PROMOTION_NOGGORMOTHA_KEEPER_11")
iKeeperLevel12		= git("PROMOTION_NOGGORMOTHA_KEEPER_12")
iKeeperLevel13		= git("PROMOTION_NOGGORMOTHA_KEEPER_13")
iKeeperLevel14		= git("PROMOTION_NOGGORMOTHA_KEEPER_14")
iKeeperLevel15		= git("PROMOTION_NOGGORMOTHA_KEEPER_15")
iKeeperLevel16		= git("PROMOTION_NOGGORMOTHA_KEEPER_16")

lKeeperList			= [bKeeperEffect,iKeeperLevel01,iKeeperLevel02,iKeeperLevel03,iKeeperLevel04,iKeeperLevel05,iKeeperLevel06,iKeeperLevel07,iKeeperLevel08,iKeeperLevel09,iKeeperLevel10,iKeeperLevel11,iKeeperLevel12,iKeeperLevel13,iKeeperLevel14,iKeeperLevel15,iKeeperLevel16]

# Quick list of Keeper Units
iUnitKeeper			= git("UNIT_KEEPER")
iUnitKeeperDark		= git("UNIT_KEEPER_DARK")
iUnitKeeperBlessed	= git("UNIT_KEEPER_BLESSED")

lUnitKeeperList		= [iUnitKeeper,iUnitKeeperDark,iUnitKeeperBlessed]

# Set Keeper level; for pKeeper set keeper level promotion based on iLevel, if iLevel is 0 all keeper promotions are removed; Nog's spawn moved here from pyperturn, checks for Nog spawn are for iLevel >= 16 (spawn Nog from the strongest keeper) or iLevel = 0 (checks if only one keeper on the map is left)
def setKeeperLevel(pKeeper, iLevel):
	for i in lKeeperList:												# Remove both effect promotion and any keeper level to prevent overlaps
		pKeeper.setHasPromotion(i, False)
	if iLevel >= 16:													# If Keeper reaches 16th level spawn Nog instead
		if CyGame().getUnitClassCreatedCount(git('UNITCLASS_NOGGORMOTHA')) == 0:
			pPlayer = gc.getPlayer(pKeeper.getOwner())
			pPlot = pKeeper.plot()										# Spawn Nog from keeper's plot
			newUnit = pPlayer.initUnit(git('UNIT_NOGGORMOTHA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				CyInterface().addMessage(iPlayer,True,25,localText.getText("TXT_KEY_MESSAGE_NOGGORMOTHA_LEFT_SAVIOUR", ()),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Stigmata.dds',ColorTypes(2),pPlot.getX(),pPlot.getY(),True,True)	
				for pUnit in PyPlayer(iPlayer).getUnitList():			# Removing Keeper Effect from every unit, level will drop itself (bMustMaintain)
					setKeeperLevel(pUnit, 0)
			return
		else:															# Failsafe, should not be possible, but if it is, don't ruin the fun. Set the level to 16
			pKeeper.setHasPromotion(bKeeperEffect, True)
			pKeeper.setHasPromotion(iKeeperLevel16, True)
			return
	if iLevel > 0:
		pKeeper.setHasPromotion(bKeeperEffect, True)					# Set both effect and level promotion
		pKeeper.setHasPromotion(lKeeperList[iLevel], True)				# Promotion position in the list = promotion's level
		ForceWishForAI(pKeeper)											# Function that forces teleport for AI owner of pKeeper to cast Nog's Wish, similar function was removed from onBeginGameTurn, T_W
	if iLevel == 0:														
		if CyGame().getUnitClassCreatedCount(git('UNITCLASS_NOGGORMOTHA')) == 0:
			iRemainingKeepers = 0										# Counter increases with every keeper, if only one is left Nog is released
			pBestHost = -1
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				for pUnit in PyPlayer(iPlayer).getUnitList():
					if pUnit.isHasPromotion(bKeeperEffect):
						iRemainingKeepers += 1
						pBestHost = pUnit
			if iRemainingKeepers == 1:
				pPlayer = gc.getPlayer(pBestHost.getOwner())
				pPlot = pBestHost.plot()								# Spawn Nog from keeper's plot
				newUnit = pPlayer.initUnit(git('UNIT_NOGGORMOTHA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				setKeeperLevel(pBestHost, 0)			# No need to cycle through every unit to remove keeper effect, that was the last keeper
				for iPlayer in xrange(gc.getMAX_PLAYERS()):
					CyInterface().addMessage(iPlayer,True,25,localText.getText("TXT_KEY_MESSAGE_NOGGORMOTHA_LEFT", ()),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Stigmata.dds',ColorTypes(2),pPlot.getX(),pPlot.getY(),True,True)
				return

# Get Keeper level, looks at pKeeper, returns keeper's level.
def getKeeperLevel(pKeeper):
	iLevel = 0
	if not pKeeper.isHasPromotion(bKeeperEffect):						# No keeper effect promotion, no level
		return iLevel
	else:
		for i in lKeeperList:
			if pKeeper.isHasPromotion(i):
				iLevel = lKeeperList.index(i)							# Promotion position in the list = promotion's level
	return iLevel

# PROMOTION_NOGGORMOTHA_STIGAMTA
def effectNoggormothaStigmata(pCaster):
	iStrBoost		= pCaster.getStrBoost()
	iCounterFactor	= 4*(CyGame().getGlobalCounter() / 10)				# Nog gets 4 Strength per 10 AC counter
	pCaster.changeStrBoost(iCounterFactor - iStrBoost)					# Reset current Strength boost while adding new one

def getHelpNoggormothaStigmata(argsList):
	ePromotion, pCaster = argsList
	if pCaster == -1 or pCaster.isNone():
		szHelp			= ""
	else:
		iStrBoost = pCaster.getStrBoost()
		szHelp			= localText.getText("TXT_KEY_NOG_PYHELP_PROMOTION_STIGMATA", (iStrBoost,))
	return szHelp

# Keeper Level Promotions
def getHelpKeeper(argsList):
	ePromotion, pCaster = argsList
	if pCaster == -1 or pCaster.isNone():
		szHelp			= ""
	else:
		iLevelCaster	= getKeeperLevel(pCaster)
		iSpreadChance	= (CyGame().getGlobalCounter() / 2) + 5
		pShrine			= -1
		pShrine			= spellEscapeKeeper(pCaster,False)
		if not pShrine == -1:
			if pCaster.getUnitType() in lUnitKeeperList:
				szHelp	= localText.getText("TXT_KEY_NOG_PYHELP_PROMOTION_KEEPER", (iLevelCaster,pShrine.getNameKey(),iSpreadChance,))
			else:
				szHelp	= localText.getText("TXT_KEY_NOG_PYHELP_PROMOTION_KEEPER_NOT_TRUE_KEEPER", (iLevelCaster,pShrine.getNameKey(),iSpreadChance,))
		else:
			szHelp		= localText.getText("TXT_KEY_NOG_PYHELP_PROMOTION_KEEPER_NO_HOME", (iLevelCaster,))
	return szHelp

# SPELL_LOCATE_KEEPER
def spellLocateKeeper(pCaster):
	iRemainingKeepers = 0
	for iPlayer in xrange(gc.getMAX_PLAYERS()):							# Cycle through every unit, Mark every plot with keeper effect
		if iPlayer != pCaster.getOwner():
			for pUnit in PyPlayer(iPlayer).getUnitList():
				if pUnit.isHasPromotion(bKeeperEffect):
					CyInterface().addMessage(pCaster.getOwner(),True,25,localText.getText("TXT_KEY_SPELL_LOCATE_KEEPER_MESSAGE", ()),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Locate.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
					iRemainingKeepers += 1
	CyInterface().addMessage(pCaster.getOwner(),True,25,localText.getText("TXT_KEY_SPELL_LOCATE_KEEPER_REMAINING_KEEPERS", (iRemainingKeepers,)),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Locate.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)

# SPELL_ESCAPE_KEEPER
def reqEscapeKeeper(pCaster):
	iPlayer				= pCaster.getOwner()
	pShrine				= -1
	for pCity in PyPlayer(iPlayer).getCityList():
		if pCity.isCapital() and pShrine == -1:
			pShrine		= pCity
		if (pCity.getNumBuilding(git('BUILDING_SHRINE_KEEPERS1')) > 0 or pCity.getNumBuilding(git('BUILDING_SHRINE_KEEPERS2')) > 0):
			pShrine		= pCity
	if pShrine == -1:
		return False
	else:
		return True

def spellEscapeKeeper(pCaster,pSource):
	iPlayer				= pCaster.getOwner()
	pShrine				= -1
	for pCity in PyPlayer(iPlayer).getCityList():
		if pCity.isCapital() and pShrine == -1:							# Makes capital a point of teleporatation if no shrines are built
			pShrine		= pCity
		if (pCity.getNumBuilding(git('BUILDING_SHRINE_KEEPERS1')) > 0 or pCity.getNumBuilding(git('BUILDING_SHRINE_KEEPERS2')) > 0):
			pShrine		= pCity
	if pSource == "Spell" and pShrine != -1:							# Can use it for both spell
		pCaster.setXY(pShrine.getX(), pShrine.getY(), False, True, True, False)
		return
	else:																# And respawn
		return pShrine

def getHelpEscapeKeeper(argsList):
	eSpell, pCaster = argsList
	if pCaster == -1 or pCaster.isNone():
		szHelp			= ""
	else:
		pShrine			= -1
		iPlayer			= pCaster.getOwner()
		for pCity in PyPlayer(iPlayer).getCityList():
			if pCity.isCapital() and pShrine == -1:
				pShrine		= pCity
			if (pCity.getNumBuilding(git('BUILDING_SHRINE_KEEPERS1')) > 0 or pCity.getNumBuilding(git('BUILDING_SHRINE_KEEPERS2')) > 0):
				pShrine		= pCity
		if pShrine != -1:
			szHelp	= localText.getText("TXT_KEY_PYHELP_KEEPER_ESCAPE", (pShrine.getNameKey(),))
	return szHelp

# SPELL_NOGGORMOTHAS_WISH
def reqNoggormothasWish(pCaster):
	pPlot				= pCaster.plot()
	iTeam				= pCaster.getTeam()
	for i in xrange(pPlot.getNumUnits()):								# Checks for another keerper on the same team
		pUnit = pPlot.getUnit(i)
		if pUnit.isHasPromotion(bKeeperEffect) and pUnit.getID() != pCaster.getID() and pUnit.getTeam() == iTeam:
			return True
	return False

def spellNoggormothasWish(pCaster):
	pPlot				= pCaster.plot()
	iTeam				= pCaster.getTeam()
	iPlayer				= pCaster.getOwner()
	iLevelCaster		= getKeeperLevel(pCaster)
	for i in xrange(pPlot.getNumUnits()):								# From all units on pCaster's plot...
		pUnit			= pPlot.getUnit(i)
		if (pUnit.isHasPromotion(bKeeperEffect) and pUnit.getID() != pCaster.getID()) and pUnit.getTeam() == iTeam:	# That have Keeper Effect, not a pCaster itself, on the same team as pCaster...
			iLevelCaster += getKeeperLevel(pUnit)						# Sum all keeper levels and add it to the pCaster
			setKeeperLevel(pCaster, iLevelCaster)						# !! If pCaster level change is set after pUnit's Level removal and if pCaster and pUnit are 2 last keepers it will restate Keeper effect on pCaster after Nog's effect wipe !!
			setKeeperLevel(pUnit, 0)									# Remove effect from pUnit
	CyInterface().addMessage(iPlayer,True,25,localText.getText("TXT_KEY_SPELL_NOGGORMOTHAS_WISH_MESSAGE", ()),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Wish.dds',ColorTypes(2),pPlot.getX(),pPlot.getY(),True,True)

# PROMOTION_KEEPER_EFFECT, Handles respawn, death, spread, keeper level changes
def postCombatKeeperLost(pCaster, pOpponent):
	bLostAgainstKeeper	= False											# Is pOpponent a keeper?
	bTrueKeeper			= False											# Is pCaster a UNIT_KEEPER (or it's upgrade)
	bSpread				= False											# Is Keeper Effect spreading?
	bForceDownLevel		= False											# Is Keeper Effect spreading and pCaster losing 1 keeper level
	bNoSpread			= False											# Is pOpponent a Golem or Mech unit or Saila
	iLevelOpponent		= getKeeperLevel(pOpponent)
	iLevelCaster		= getKeeperLevel(pCaster)
	if iLevelOpponent > 0:												# If pOpponent is a keeper pCaster will not respawn
		bLostAgainstKeeper = True
	if pCaster.getUnitType() in lUnitKeeperList:						# CombatLost results for non UNIT_KEEPERs keepers are harsher
		bTrueKeeper		= True
	if bLostAgainstKeeper:
		CyGame().changeGlobalCounter(1)
		iLevelSum		= iLevelOpponent + iLevelCaster
		setKeeperLevel(pOpponent,iLevelSum)								# Victorious keeper gets all the levels
		setKeeperLevel(pCaster,0)										# Check for Nog's spawn as total number of keepers decreasing
		for iPlayer in range(gc.getMAX_PLAYERS()):						# Send message for everyone, 
			CyInterface().addMessage(iPlayer,True,25,localText.getText("TXT_KEY_KEEPER_KILLED_KEEPER_MESSAGE", ()),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Locate.dds',ColorTypes(2),pOpponent.getX(),pOpponent.getY(),True,True)
	else:
		pShrine			= spellEscapeKeeper(pCaster,False)				# pCaster point of respawn
		iSpreadChance	= (CyGame().getGlobalCounter() / 2) + 5			# 5% to 55% chance to spread keeper effect depending on AC
		if pOpponent.isHasPromotion(git("PROMOTION_GOLEM")) or gc.getUnitInfo(pOpponent.getUnitType()).isMechUnit() or pOpponent.getUnitType() == git('UNIT_SAILA'):	 # Check for Golem and bMechanized
			bNoSpread	= True
		if CyGame().getSorenRandNum(100, "KeeperEffect spread roll") < iSpreadChance and not bNoSpread:
			bSpread		= True
		elif CyGame().getSorenRandNum(100, "bForceDownLevel roll") < 50 and not bTrueKeeper and not bNoSpread:
			bForceDownLevel = True
		# Respawn logic starts
		if pShrine == -1 or pCaster.isHasPromotion(git("PROMOTION_KEEPER_DIED")) or gc.getPlayer(pCaster.getOwner()).isBarbarian(): # Keeper will die and transfer it's promotions if 1. There is nowhere to respawn 2. Keeper died this turn already 3. Keeper is a barb
			if bNoSpread:												# Prevent units that can't have keeper effect from geting it
				setKeeperLevel(pCaster,0)								# if keeper dies from that unit, check for Nog's spawn as total number of keepers decreasing
			else:
				setKeeperLevel(pOpponent,iLevelCaster)
			for iPlayer in range(gc.getMAX_PLAYERS()):					# Send a message for everyone, one of the keepers died for good
				CyInterface().addMessage(iPlayer,True,25,localText.getText("TXT_KEY_KEEPER_DIED_NO_SHRINE", ()),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Locate.dds',ColorTypes(2),pOpponent.getX(),pOpponent.getY(),True,True)
		elif not pCaster.isImmortal():									# Immortal respawn should take priority to prevent keeper's dupe, no spread if so
			pPlayer		= gc.getPlayer(pCaster.getOwner())
			respawnedCaster = pPlayer.initUnit(pCaster.getUnitType(), pShrine.getX(), pShrine.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH) 		# Respawn keeper at shrine
			pCaster.getCommanderUnit().removeMinion(pCaster)																										# to remove all commander promotions from pCaster
			for iPromotion in xrange(gc.getNumPromotionInfos()):																									# check for promotions of old pCaster
				if (pCaster.isHasPromotion(iPromotion) and not gc.getPromotionInfo(iPromotion).isEquipment()) and iPromotion != git('PROMOTION_ASSURED_KEEPER'):	# Equipment is dropped, Assured Keeper is dropped
					iCount = pCaster.countHasPromotion(iPromotion)																									# If pCaster has stacked promotions, apply all of them
					for i in xrange(iCount):
						respawnedCaster.setHasPromotionExt(iPromotion,True,False,True)																				# I have no idea what's the difference between setHasPromotion and setHasPromotionExt, but it was in the original and it was working, T_W
			respawnedCaster.setLevel(pCaster.getLevel())																											# Level transfer
			respawnedCaster.setExperienceTimes100((pCaster.getExperienceTimes100() * 1 / 2), -1)																	# Remove half of xp
			if not ((pShrine.getNumBuilding(git('BUILDING_SHRINE_KEEPERS1')) > 0 or pShrine.getNumBuilding(git('BUILDING_SHRINE_KEEPERS2')) > 0)):					# Immobilize timer is less if Shrine is built
				respawnedCaster.changeImmobileTimer(2)																												# Immobilize respawned for a few turns
			respawnedCaster.changeImmobileTimer(2)
			respawnedCaster.setHasPromotion(git("PROMOTION_KEEPER_DIED"),True)																						# pCaster dies if defeated 2 times in one turn
			setKeeperLevel(respawnedCaster,iLevelCaster)																											# Set keeper level, This should be the solution to the keeper promotion problem all along, T_W
			iPlayer = respawnedCaster.getOwner()						# Send a message to respawned keeper owner, keeper respawned
			CyInterface().addMessage(iPlayer,True,25,localText.getText("TXT_KEY_KEEPER_RESPAWN", ()),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Locate.dds',ColorTypes(2),respawnedCaster.getX(),respawnedCaster.getY(),True,True)
			if bSpread or bForceDownLevel:
				setKeeperLevel(pOpponent,1)								# Keeper effect is spread on pOpponent
				for iPlayer in range(gc.getMAX_PLAYERS()):				# Send a message for everyone, keeper effect spread
					CyInterface().addMessage(iPlayer,True,25,localText.getText("TXT_KEY_KEEPER_EFFECT_SPREAD", ()),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Locate.dds',ColorTypes(2),pOpponent.getX(),pOpponent.getY(),True,True)
			if bForceDownLevel:
				respawnedCaster.changeImmobileTimer(2)					# Immobilize a non UNIT_KEEPER keeper further
				setKeeperLevel(respawnedCaster,iLevelCaster - 1)		# Remove one level
				iPlayer = respawnedCaster.getOwner()					# Send a message to respawned keeper owner, keeper lost power
				CyInterface().addMessage(iPlayer,True,25,localText.getText("TXT_KEY_KEEPER_LOST_POWER", ()),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Locate.dds',ColorTypes(2),respawnedCaster.getX(),respawnedCaster.getY(),True,True)

# Called from setKeeperLevel, used to help AI gather keepers ready for Nog's Wish
def ForceWishForAI(pKeeper):
	iPlayer				= pKeeper.getOwner()
	pPlayer				= gc.getPlayer(iPlayer)
	if not pPlayer.isHuman():											# Only for AI
		pShrine2		= -1
		for pCity in PyPlayer(iPlayer).getCityList():					# Check for shrine
			if pCity.getNumBuilding(git('BUILDING_SHRINE_KEEPERS2')) > 0:
				pShrine2 = pCity
		if pShrine2	!= -1:
			iNumKeepers = 0
			iLeveledKeepers = 0
			for pUnit in PyPlayer(iPlayer).getUnitList():				# If AI has at least 2 keeper unit and one of them at least level 5
				if pUnit.isHasPromotion(bKeeperEffect) and pUnit.getID() != pKeeper.getID:
					if pUnit.getLevel() > 4 or pKeeper.getLevel() > 4:
						pUnit.setXY(pShrine2.getX(), pShrine2.getY(), False, True, True, False)	# Teleport both of them
						pKeeper.setXY(pShrine2.getX(), pShrine2.getY(), False, True, True, False)
						return
	return