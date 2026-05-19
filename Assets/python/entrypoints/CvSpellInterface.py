#Spell system and FfH specific callout python functions
#All code by Kael, all bugs by woodelf

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
import Blizzards # Added in Frozen: Blizzards: TC01
import random # needed for shuffle(list)

PyInfo              = PyHelpers.PyInfo
PyPlayer            = PyHelpers.PyPlayer
gc                  = CyGlobalContext()
localText           = CyTranslator()
cf                  = CustomFunctions.CustomFunctions()
sf                  = ScenarioFunctions.ScenarioFunctions()

Manager             = CvEventInterface.getEventManager()

Bonus               = Manager.Resources
Civ                 = Manager.Civilizations
Race                = Manager.Promotions["Race"]
GenericPromo               = Manager.Promotions["Generic"]
Effect              = Manager.Promotions["Effects"]
Feature             = Manager.Feature
Terrain             = Manager.Terrain
Event               = Manager.EventTriggers
Goody               = Manager.Goodies
Mana                = Manager.Mana
UniqueImprovement   = Manager.UniqueImprovements
Improvement         = Manager.Improvements
Lair                = Manager.Lairs
Trait               = Manager.Traits
Animal              = Manager.Units["Animal"]
UnitCombat          = Manager.UnitCombats

getInfoType         = gc.getInfoTypeForString

# IRacial does not contain avatar, dragon, giant... but contains shade. Why/what for?
# iRacial is used in function spellRandomRacial (used for spawngroups "Reconnaissance Team" and "Partisans")
IRacial = [Race["Angel"], Race["Centaur"], Race["Demon"], Race["Dwarven"], Race["Elemental"], Race["Dark Elven"], Race["Elven"], Race["Fallen Angel"],Race["Frostling"],Race["Goblinoid"],Race["Golem"],Race["Lizardman"],Race["Minotaur"],Race["Musteval"],Race["Orcish"],getInfoType('PROMOTION_SHADE'),Race["Trollkin"]]

Blizzards2 = Blizzards.Blizzards() # Added in Frozen: Blizzards: TC01

IFarm = [Bonus["Corn"],Bonus["Rice"],Bonus["Wheat"]]
ICamp = [Bonus["Bison"],Bonus["Deer"],Bonus["Fur"],Bonus["Ivory"]]
IPasture = [Bonus["Camel"],Bonus["Cow"],Bonus["Horse"],Bonus["Pig"],Bonus["Sheep"]]
# perhaps create IPastureHorse = IPasture+ iHorse
IPlantation = [Bonus["Banana"],Bonus["Cotton"],Bonus["Dye"],Bonus["Incense"],Bonus["Reagents"],Bonus["Silk"],Bonus["Sugar"]]
#iGulagarm  = getInfoType('BONUS_GULAGARM')
#iRazorweed = getInfoType('BONUS_RAZORWEED')
#IPlantationHell = IPlantation+[iGulagarm,iRazorweed]
IFishing = [Bonus["Clam"],Bonus["Crab"],Bonus["Fish"],Bonus["Shrimp"]]
# iPearl  = getInfoType('BONUS_PEARL')
# IFishingLanun = IFishing + iPearl

iTundra     = Terrain["Tundra"]
iGlacier    = Terrain["Glacier"]
iCoast      = Terrain["Coast"]
iOcean      = Terrain["Ocean"]

ISpellLvl1Promotion = [
	getInfoType('PROMOTION_AIR1'),
	getInfoType('PROMOTION_BODY1'),
	getInfoType('PROMOTION_CHAOS1'),
	getInfoType('PROMOTION_CREATION1'),
	getInfoType('PROMOTION_DEATH1'),
	getInfoType('PROMOTION_DIMENSIONAL1'),
	getInfoType('PROMOTION_EARTH1'),
	getInfoType('PROMOTION_ENCHANTMENT1'),
	getInfoType('PROMOTION_ENTROPY1'),
	getInfoType('PROMOTION_FIRE1'),
	getInfoType('PROMOTION_FORCE1'),
	getInfoType('PROMOTION_ICE1'),
	getInfoType('PROMOTION_LAW1'),
	getInfoType('PROMOTION_LIFE1'),
	getInfoType('PROMOTION_METAMAGIC1'),
	getInfoType('PROMOTION_MIND1'),
	getInfoType('PROMOTION_NATURE1'),
	getInfoType('PROMOTION_SHADOW1'),
	getInfoType('PROMOTION_SPIRIT1'),
	getInfoType('PROMOTION_SUN1'),
	getInfoType('PROMOTION_WATER1')
]

# *******************
# Modular Python: ANW 16-feb-2010
#                     29-may-2010
#                     20-aug-2010
#                     02-sep-2010
#
# this part defines new spells
# part at the end of this file overrides existing files
#

#import glob   # Unix style pathname pattern expansion
import os
import CvPath # path to current assets
import imp    # importing module

# Load spells from modules
MLFlist = []
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\NormalModules\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FirstLoad\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\SecondLoad\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\ThirdLoad\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FourthLoad\\")

for pathToMLF in MLFlist:
	for modules in os.listdir(pathToMLF):
		pathToModuleRoot = pathToMLF+modules+"\\"
		# Ignore all xml files
		if modules.lower()[-4:] != ".xml":
			# Check whether path exists // whether current directory isn't actually a file
			if os.path.exists(pathToModuleRoot):
				# Check whether python folder is present
				if "python" in os.listdir(pathToModuleRoot):
					pathToModulePython = pathToModuleRoot+"python\\"
					# For every file in that folder
					for pythonFileSourceName in os.listdir(pathToModulePython):
						pythonFileSource = pathToModulePython+pythonFileSourceName
						# Is it non-python file ?
						if (pythonFileSource.lower()[-3:] != ".py"):
							continue
						# Is it non-spell file ?
						if pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ].upper()[0:5] != "SPELL":
							continue
						# Is it spelloverwrite file ?
						if pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ].upper()[0:8] == "SPELLOVR":
							continue

						tempFileName = file(pythonFileSource)
						tempModuleName = pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ]
						imp.load_module( tempModuleName, tempFileName, tempModuleName+".py", ("","",1))
						#print(pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ])
						exec("from "+tempModuleName+" import *")
						tempFileName.close()

# Modular Python End
# *******************

def cast(argsList):
	pCaster,eSpell,pPlot = argsList
	spell = gc.getSpellInfo(eSpell)
	eval(spell.getPyResult())

def canCast(argsList):
	pCaster, eSpell, pPlot = argsList
	spell = gc.getSpellInfo(eSpell)
	return eval(spell.getPyRequirement())

def effect(argsList):
	pCaster, eProm = argsList
	prom = gc.getPromotionInfo(eProm)
	eval(prom.getPyPerTurn())

def effectPlot(argsList):
	pPlot, ePlotEffect = argsList
	plotEffect = gc.getPlotEffectInfo(ePlotEffect)
	eval(plotEffect.getPyPerTurn())

# Broader Alignments: Added by Grey Fox 04/10/2008
def effectUnits(argsList):
	pCaster, eUnit = argsList
	unit = gc.getUnitInfo(eUnit)
	eval(unit.getPyPerTurn())

def postPromotionCombatLost(argsList):
	pCaster, pOpponent, eProm = argsList
	prom = gc.getPromotionInfo(eProm)
	eval(prom.getPyPostCombatLost())

def postPromotionCombatWon(argsList):
	pCaster, pOpponent, eProm = argsList
	prom = gc.getPromotionInfo(eProm)
	eval(prom.getPyPostCombatWon())
# Broader Alignments: End Add

def onPromoTaken(argsList):
	pCaster, eProm = argsList
	prom = gc.getPromotionInfo(eProm)
	eval(prom.getPyOnPromoTaken())

def postDeath(argsList):
	pCaster, eKiller, eUnit = argsList
	if eKiller >= 0:
		pKiller = gc.getPlayer(eKiller)
	unit = gc.getUnitInfo(eUnit)
	eval(unit.getPyDeath())

def promotionRemove(argsList):
	pCaster, ePromotion = argsList
	promotion = gc.getPromotionInfo(ePromotion)
	return eval(promotion.getPyOnRemove())

def atRange(argsList):
	pCaster, pPlot, eImp = argsList
	imp = gc.getImprovementInfo(eImp)
	eval(imp.getPythonAtRange())

def onMove(argsList):
	pCaster, pPlot, eImp = argsList
	imp = gc.getImprovementInfo(eImp)
	eval(imp.getPythonOnMove())

def onMoveFeature(argsList):
	pCaster, pPlot, eFeature = argsList
	feature = gc.getFeatureInfo(eFeature)
	eval(feature.getPythonOnMove())

def vote(argsList):
	eVote, int = argsList
	vote = gc.getVoteInfo(eVote)
	eval(vote.getPyResult())

def miscast(argsList):
	pCaster, eSpell = argsList
	spell = gc.getSpellInfo(eSpell)
	eval(spell.getPyMiscast())

def globalAnnounce(argsList):
	unit, eSpell = argsList
	spell = gc.getSpellInfo(eSpell)
	player = PyPlayer(unit.getOwner())
	if gc.getGame().getAIAutoPlay() == 0:
		sPlayerName = player.getName()
		sSpellName = spell.getDescription()
		sQuote = spell.getQuote()
		sPopupText = CyTranslator().getText('TXT_KEY_MISC_SPELL_POPUP',(sPlayerName, sSpellName, sQuote))
		addPopup(sPopupText, str(gc.getLeaderHeadInfo(player.getLeaderType()).getImage()))

def postCombatLost(argsList):
	pCaster, pOpponent = argsList
	unit = gc.getUnitInfo(pCaster.getUnitType())
	eval(unit.getPyPostCombatLost())

def preCombat(argsList):
	pCaster, pOpponent = argsList
	unit = gc.getUnitInfo(pCaster.getUnitType())
	eval(unit.getPyPreCombat())

def postCombatWon(argsList):
	pCaster, pOpponent = argsList
	unit = gc.getUnitInfo(pCaster.getUnitType())
	eval(unit.getPyPostCombatWon())

# def findClearPlot(pUnit, plot,iPlayer=-1):
	# BestPlot = -1
	# iBestPlot = 0
	# if (plot==None):
		# return -1
	# getPlot	= CyMap().plot
	# if pUnit == -1:
		# for x, y in plotsInRange( plot.getX(), plot.getY(), 1 ):
			# pPlot = getPlot(x, y)
			# iCurrentPlot = 0
			# if not pPlot.isNone():
				# if pPlot.getNumUnits() == 0 or pPlot.getUnit(0).getOwner==iPlayer:
					# if pPlot.isWater() == plot.isWater():
						# if not pPlot.isPeak():
							# if not pPlot.isCity():
								# iCurrentPlot = CyGame().getSorenRandNum(5, "findClearPlot")
								# if iCurrentPlot >= iBestPlot:
									# BestPlot = pPlot
									# iBestPlot = iCurrentPlot
		# return BestPlot
	# for x, y in plotsInRange( pUnit.getX(), pUnit.getY(), 1 ):
		# pPlot = getPlot(x, y)
		# iCurrentPlot = 0
		# if pPlot.getNumUnits() == 0:
			# if pUnit.canMoveOrAttackInto(pPlot, False):
				# iCurrentPlot = iCurrentPlot + 5
		
		# if(pUnit.getOwner()==iPlayer or iPlayer==-1):		
			# for i in range(pPlot.getNumUnits()):
				# if pPlot.getUnit(i).getOwner() == pUnit.getOwner():
					# if pUnit.canMoveOrAttackInto(pPlot, False):
						# iCurrentPlot = iCurrentPlot + 15
			# if pPlot.isCity():
				# if pPlot.getPlotCity().getOwner() == pUnit.getOwner():
					# iCurrentPlot = iCurrentPlot + 50
			# if iCurrentPlot >= 1:
				# iCurrentPlot = iCurrentPlot + CyGame().getSorenRandNum(5, "findClearPlot")
				# if iCurrentPlot >= iBestPlot:
					# BestPlot = pPlot
					# iBestPlot = iCurrentPlot
		# else:
			# for i in range(pPlot.getNumUnits()):	
				# if pPlot.getUnit(i).getOwner() == iPlayer:
					# iCurrentPlot = iCurrentPlot + 15
			# if pPlot.isCity():
				# if pPlot.getPlotCity().getOwner() == iPlayer:
					# iCurrentPlot = iCurrentPlot + 50
				# else:
					# iCurrentPlot = iCurrentPlot - 50
			# if iCurrentPlot >= 1:
				# iCurrentPlot = iCurrentPlot + CyGame().getSorenRandNum(5, "findClearPlot")
				# if iCurrentPlot >= iBestPlot:
					# BestPlot = pPlot
					# iBestPlot = iCurrentPlot
	# return BestPlot
def findClearPlot(pUnit, plot,iPlayer=-1):
	BestPlot = -1
	iBestPlot = 0
	if (plot==None):
		return -1
	getPlot	= CyMap().plot
	iRange = 1
	if pUnit == -1:
		while(BestPlot==-1):
			for x, y in plotsInRange( plot.getX(), plot.getY(), iRange, iRange -1 ):
				pPlot = getPlot(x, y)
				iCurrentPlot = 0
				if not pPlot.isNone():
					if pPlot.getNumUnits() == 0 or pPlot.getUnit(0).getOwner==iPlayer:
						if pPlot.isWater() == plot.isWater():
							if not pPlot.isPeak():
								if not pPlot.isCity():
									iCurrentPlot = CyGame().getSorenRandNum(5, "findClearPlot")
									if iCurrentPlot >= iBestPlot:
										BestPlot = pPlot
										iBestPlot = iCurrentPlot						
			if BestPlot == -1:
				iRange = iRange+1
				if (iRange>10):
					return plot
			else:
				return BestPlot
	while(BestPlot==-1):
		for x, y in plotsInRange( pUnit.getX(), pUnit.getY(), iRange,iRange -1 ):
			pPlot = getPlot(x, y)
			iCurrentPlot = 0
			if pPlot.getNumUnits() == 0:
				if pUnit.canMoveOrAttackInto(pPlot, False):
					iCurrentPlot = iCurrentPlot + 5
		
			if(pUnit.getOwner()==iPlayer or iPlayer==-1):		
				for i in range(pPlot.getNumUnits()):
					if pPlot.getUnit(i).getOwner() == pUnit.getOwner():
						if pUnit.canMoveOrAttackInto(pPlot, False):
							iCurrentPlot = iCurrentPlot + 15
				if pPlot.isCity():
					if pPlot.getPlotCity().getOwner() == pUnit.getOwner():
						iCurrentPlot = iCurrentPlot + 50
				if iCurrentPlot >= 1:
					iCurrentPlot = iCurrentPlot + CyGame().getSorenRandNum(5, "findClearPlot")
					if iCurrentPlot >= iBestPlot:
						BestPlot = pPlot
						iBestPlot = iCurrentPlot
			else:
				for i in range(pPlot.getNumUnits()):	
					if pPlot.getUnit(i).getOwner() == iPlayer:
						iCurrentPlot = iCurrentPlot + 15
				if pPlot.isCity():
					if pPlot.getPlotCity().getOwner() == iPlayer:
						iCurrentPlot = iCurrentPlot + 50
					else:
						iCurrentPlot = iCurrentPlot - 50
				if iCurrentPlot >= 1:
					iCurrentPlot = iCurrentPlot + CyGame().getSorenRandNum(5, "findClearPlot")
					if iCurrentPlot >= iBestPlot:
						BestPlot = pPlot
						iBestPlot = iCurrentPlot
		if BestPlot == -1:
			iRange = iRange+1
			if (iRange>10):
				return pUnit.plot()
		else:
			return BestPlot
	return BestPlot
	
def plotsInRange( centerX, centerY, maxRange, minRange=None ):
	if minRange is None:
		minRange = 0
	for offsetX in xrange( -maxRange, maxRange + 1 ):
		plotX = centerX + offsetX
		for offsetY in xrange( -maxRange, maxRange + 1 ):
			plotY = centerY + offsetY
			distance = stepDistance( centerX, centerY, plotX, plotY )
			if minRange <= distance <= maxRange:
				yield ( plotX, plotY )

def plotsInCircularRange( centerX, centerY, maxRange, minRange=None ):
	if minRange is None:
		minRange = 0
	for offsetX in xrange( -maxRange, maxRange + 1 ):
		plotX = centerX + offsetX
		for offsetY in xrange( -maxRange, maxRange + 1 ):
			plotY = centerY + offsetY
			distance = plotDistance( centerX, centerY, plotX, plotY )
			if minRange <= distance <= maxRange:
				yield ( plotX, plotY )

def postCombatAC(pCaster,pOpponent):
	gc = CyGlobalContext()
	pPlayer 	= gc.getPlayer(pCaster.getOwner())
	pPlayer.changeGlobalCounterContrib(1)

# When a beast of Agares kills a paladin
def postCombatConsumePaladin(pCaster, pOpponent):
	gc  = CyGlobalContext()
	if (pOpponent.getUnitClassType() == getInfoType('UNITCLASS_PALADIN')):
		pCaster.setDamage(0, pCaster.getOwner())
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_CONSUME_PALADIN", ()),'',1,'Art/Interface/Buttons/Units/Beast of Agares.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)

def postCombatScionPriest(pCaster, pOpponent):
	gc 			= CyGlobalContext()
	pPlayer 	= gc.getPlayer(pCaster.getOwner())
	randNum		= CyGame().getSorenRandNum

	if (pCaster.getUnitClassType() == getInfoType('UNITCLASS_DOOMGIVER')):
		pPlot = pOpponent.plot()
		if pPlot.isCity():
			pCity = pPlot.getPlotCity()
			CyInterface().addMessage(pCity.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POPULATION_REDUCED", ()),'',1,'Art/Interface/Buttons/Units/Angel of Death.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOOMGIVER_CITY_ATTACK", ()),'',1,'Art/Interface/Buttons/Units/Angel of Death.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
			iDoomgiverHurryAnger = (5 + randNum(10, "Doomgiver attack anger amount"))
			pCity.changeHurryAngerTimer(iDoomgiverHurryAnger)
			if pCity.getPopulation() > 1:
				if randNum(5, "Doomgiver chance to reduce pop") == 1:
					pCity.changePopulation(-1)

	#pPlot = pCaster.plot()
	#if pOpponent.isAnimal(): return
	#if not pOpponent.isAlive(): return
	#iCasterLevel = pCaster.getLevel()
	#iBarbMod = 0
	#if pOpponent.isBarbarian():
	#	iBarbMod = 5
	#iPriestMod = 0
	#iDivine = getInfoType('PROMOTION_DIVINE')
	#hasPromo	= pCaster.isHasPromotion
	#if hasPromo(iDivine):	iPriestMod = 3
	#iCommand1 = getInfoType('PROMOTION_COMMAND1')
	#iCommand2 = getInfoType('PROMOTION_COMMAND2')
	#iCommand3 = getInfoType('PROMOTION_COMMAND3')
	#iCommandMod = 0
	#if hasPromo(iCommand1): iCommandMod = 3
	#if hasPromo(iCommand2):	iCommandMod = 6
	#if hasPromo(iCommand3):	iCommandMod = 9
	#iTurnRoll = randNum(100, "Scion priest Turn roll")
	#if iTurnRoll < (7 + iPriestMod + iCommandMod - iBarbMod + (iCasterLevel * 2)):
	#	iUnitRoll = randNum(100, "Scion priest Unit roll")
	#	if iUnitRoll < (30 + (8 * iBarbMod) - (100 * iCommandMod)):
	#		iArcher = getInfoType('UNITCOMBAT_ARCHER')
	#		iRecon 	= getInfoType('UNITCOMBAT_RECON')
	#		if pOpponent.getUnitCombatType() == iArcher:
	#			newUnit = pPlayer.initUnit(getInfoType('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	#			newUnit.setExperienceTimes100((pOpponent.getExperienceTimes100() / 3), -1)
	#			newUnit.setDamage(50, -1)
	#			newUnit.finishMoves()
	#			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_SPAWNED_PRIEST", ()),'',1,'Art/Interface/Buttons/Units/Scions/reborn.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
	#			return
	#		if pOpponent.getUnitCombatType() == iRecon:
	#			newUnit = pPlayer.initUnit(getInfoType('UNIT_VELITES'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	#			newUnit.setExperienceTimes100((pOpponent.getExperienceTimes100() / 3), -1)
	#			newUnit.setDamage(50, -1)
	#			newUnit.finishMoves()
	#			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_SPAWNED_PRIEST", ()),'',1,'Art/Interface/Buttons/Units/Scions/reborn.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
	#			return
	#		iUnreliable 		= getInfoType('PROMOTION_UNRELIABLE')
	#		iTurnedUndeadArt 	= getInfoType('PROMOTION_TURNED_UNDEAD_ART')
	#		newUnit = pPlayer.initUnit(getInfoType('UNIT_CENTENI'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	#		newUnit.setHasPromotion(iUnreliable, False)
	#		newUnit.setHasPromotion(iTurnedUndeadArt, True)
	#		newUnit.setHasPromotion(Race["Undead"], True)
	#		newUnit.setExperienceTimes100((pOpponent.getExperienceTimes100() / 3), -1)
	#		newUnit.setDamage(50, -1)
	#		newUnit.finishMoves()
	#		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_SPAWNED_PRIEST", ()),'',1,'Art/Interface/Buttons/Units/Scions/reborn.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
	#		return
	#	else:
	#		newUnit = pPlayer.initUnit(getInfoType('UNIT_REBORN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	#		newUnit.finishMoves()
	#		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_REBORN_SPAWNED_PRIEST", ()),'',1,'Art/Interface/Buttons/Units/Scions/reborn.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
	#		return

def postCombatDonal(pCaster, pOpponent):
	gc 			= CyGlobalContext()
	hasPromo	= pOpponent.isHasPromotion
	if (hasPromo(Race["Demon"]) or hasPromo(Race["Undead"])):
		pCaster.setHasPromotion(getInfoType('PROMOTION_RECRUITER'), True)

def postCombatExplode(pCaster, pOpponent):

	fireSpreadToTile(pCaster.getX(), pCaster.getY())
	fireSpreadToTile(pOpponent.getX(), pOpponent.getY())

	pOpponent.doDamage(20, 100, pCaster, getInfoType('DAMAGE_FIRE'), False)
	if pCaster.isHasPromotion(getInfoType('PROMOTION_SHEUT_STONE')):
		pOpponent.doDamage(20, 100, pCaster, getInfoType('DAMAGE_DEATH'), False)

def postCombatBigExplode(pCaster, pOpponent):

#	pPlot = CyMap().plot(pCaster.getX(), pCaster.getY())

	fireSpreadToTile(pCaster.getX(), pCaster.getY())
	fireSpreadToTile(pOpponent.getX(), pOpponent.getY())

#	pPlot.setImprovementType(-1)

	pOpponent.doDamage(35, 100, pCaster, getInfoType('DAMAGE_FIRE'), False)
	if pCaster.isHasPromotion(getInfoType('PROMOTION_SHEUT_STONE')):
		pOpponent.doDamage(20, 100, pCaster, getInfoType('DAMAGE_DEATH'), False)

# Removed for redundancy with new fort rules. Also, killing a unit as a result of its death causes crashes...
# def onDeathBigExplode(pCaster):
# 	pPlot = pCaster.plot()
# 	pCaster.DeselectUnit()
# 	iImprovement = pPlot.getImprovementType()
# 	if iImprovement != -1:
# 		pImprovement = gc.getImprovementInfo(iImprovement)
# 		if not pImprovement.isUnique():
# 			pPlot.setImprovementType(-1) #This can kill the unit!

def fireSpreadToTile(iX, iY):
	pPlot = CyMap().plot(iX,iY)

	iFeature = pPlot.getFeatureType()

	if iFeature == -1:
		return

	if (iFeature == getInfoType('FEATURE_FOREST') or iFeature == getInfoType('FEATURE_JUNGLE') or iFeature == getInfoType('FEATURE_FOREST_NEW')):
		if CyGame().getSorenRandNum(100, "Flames Spread") <= gc.getDefineINT('FLAMES_SPREAD_CHANCE'):
			bValid = True
			iImprovement = pPlot.getImprovementType()
			if iImprovement != -1 :
				if gc.getImprovementInfo(iImprovement).isPermanent() :
					bValid = False
			if bValid:
				pPlot.setImprovementType(getInfoType('IMPROVEMENT_SMOKE'))


def postCombatHeal50(pCaster, pOpponent):
	if pCaster.getDamageReal() > 0:
		pCaster.setDamageReal(pCaster.getDamageReal() / 2, pCaster.getOwner())

def postCombatIra(pCaster, pOpponent):
	if pOpponent.isAlive():
		if pCaster.baseCombatStr() < 32:
			pCaster.changeStrBoost(1)

def pyPerTurnIra(pCaster):
	iStrength = pCaster.getStrBoost()
	if iStrength >= -4:
		iRnd = CyGame().getSorenRandNum(100, "Ira Strength Decrease")
		if iRnd < 33:
			pCaster.changeStrBoost(-1)

def postCombatMimic(pCaster, pOpponent):
	gc 				= CyGlobalContext()
	iBronze 		= getInfoType('PROMOTION_BRONZE_WEAPONS')
	iDivine 		= getInfoType('PROMOTION_DIVINE')
	iGreatCommander = getInfoType('PROMOTION_GREAT_COMMANDER')
	iIron 			= getInfoType('PROMOTION_IRON_WEAPONS')
	iMithril	 	= getInfoType('PROMOTION_MITHRIL_WEAPONS')
	iUndead 		= getInfoType('PROMOTION_UNDEAD')
	iLeashAch = getInfoType('PROMOTION_ACHERON_LEASHED')	
	iLeashCommand	= getInfoType('PROMOTION_INFLUENCE')
	iLeashMana = getInfoType('PROMOTION_MANA_GUARDIAN')
	iLeashMin1 = getInfoType('PROMOTION_MINOTAUR_LEASH1')
	iLeashMin2 = getInfoType('PROMOTION_MINOTAUR_LEASH2')
	iLeashMin3 = getInfoType('PROMOTION_MINOTAUR_LEASH3')
	iLeashMin4	 = getInfoType('PROMOTION_MINOTAUR_LEASH4')
	iLeashPristin = getInfoType('PROMOTION_PRISTIN_LEASH')
	iLeash0	 = getInfoType('PROMOTION_LEASH_0')	
	iLeash1	 = getInfoType('PROMOTION_LEASH_1')	
	iLeashLich = getInfoType('PROMOTION_LICH_DURATION')
	iHaste 		= getInfoType('PROMOTION_HASTED')
	iFatigue 		= getInfoType('PROMOTION_FATIGUED')
	iObscured		= getInfoType('PROMOTION_OBSCURED_LOS')
	iWaaagh 		= getInfoType('PROMOTION_WAAAGH')
	iSlow 		= getInfoType('PROMOTION_SLOW')
	iSpooked 		= getInfoType('PROMOTION_SPOOKED')
	iLost 		= getInfoType('PROMOTION_LOST')
	iHauntStalk 		= getInfoType('PROMOTION_HAUNTSTALK')
	iFortCaptain 		= getInfoType('PROMOTION_FORTCAPTAIN')
	iBlur 		= getInfoType('PROMOTION_BLUR')
	iDance 		= getInfoType('PROMOTION_DANCE_OF_BLADES')
	iLoyalty 		= getInfoType('PROMOTION_LOYALTY')
	iDesertStealth 		= getInfoType('PROMOTION_DESERT_STEALTH')
	iHeld		= getInfoType('PROMOTION_HELD')
	iWalls 		= getInfoType('PROMOTION_WALL_DEFENDER')
	iFreelancer 		= getInfoType('PROMOTION_FREELANCER')
	#iCreeper 		= getInfoType('PROMOTION_FOREST_CREEPER_TIMER')
	iNewborn 		= getInfoType('PROMOTION_NEWBORN')
	iFrostling		= getInfoType('PROMOTION_SUSTAIN_FROSTLING')
	iPoisoned = getInfoType('PROMOTION_POISONED')
	iAngryDemon = getInfoType('PROMOTION_DEMONIC_BERSERK')
	listProms = []
	iCount = 0
	for iProm in range(gc.getNumPromotionInfos()):
		if pCaster.isHasPromotion(iProm):
			iCount += 1
		else:
			if (pOpponent.isHasPromotion(iProm)):
				if gc.getPromotionInfo(iProm).isEquipment() == False:
					if (iProm != iUndead and iProm != iDivine and iProm != iBronze and iProm != iIron and iProm != iMithril and iProm != iGreatCommander and iProm != iAngryDemon and iProm != iLeashAch and iProm != iLeashCommand and iProm != iLeashMana and iProm != iLeashMin1 and iProm != iLeashMin2 and iProm != iLeashMin3 and iProm != iLeashMin4 and iProm != iLeashPristin and iProm != iLeash0 and iProm != iLeash1 and iProm != iLeashLich and iProm != iHaste and iProm != iFatigue and iProm != iObscured and iProm != iWaaagh and iProm != iSlow and iProm != iSpooked and iProm != iLost and iProm != iHauntStalk and iProm != iFortCaptain and iProm != iBlur and iProm != iDance and iProm != iLoyalty and iProm != iDesertStealth and iProm != iHeld and iProm != iWalls and iProm != iFreelancer and iProm != iNewborn  and iProm != iFrostling and iProm != iPoisoned):
						if gc.getPromotionInfo(iProm).isRace() == False:
							if gc.getPromotionInfo(iProm).isEffectProm() == False:
								if gc.getPromotionInfo(iProm).isMustMaintain() == False:
									if gc.getPromotionInfo(iProm).getExpireChance() ==0:
										if gc.getPromotionInfo(iProm).isDispellable() ==False:
											if gc.getPromotionInfo(iProm).isLeashed()==False:
												if (gc.getPromotionInfo(iProm).getPromotionClass() != gc.getInfoTypeForString("PROMOTIONCLASS_NAVAL_CREW") and gc.getPromotionInfo(iProm).getPromotionClass() != gc.getInfoTypeForString("PROMOTIONCLASS_MOUNT")):
													listProms.append(iProm)
	if len(listProms) > 0:
		iCount += 1
		iRnd = CyGame().getSorenRandNum(len(listProms), "Mimic")
		pCaster.setHasPromotion(listProms[iRnd], True)
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PROMOTION_STOLEN", ()),'',1,gc.getPromotionInfo(listProms[iRnd]).getButton(),ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
	if iCount >= 20:
		pPlayer = gc.getPlayer(pCaster.getOwner())
		if pPlayer.isHuman():
			t = "TROPHY_FEAT_MIMIC_20"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)

def postCombatAcheron(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_ACHERON"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatArs(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_ARS"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatAuricAscendedLost(pCaster, pOpponent):
	iPlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_AURIC"))==0 and pPlayer.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_AURIC_WINTER"))==0 and pPlayer.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_AURIC_ASCENDED"))==0 :
		for iTrait in range(gc.getNumTraitInfos()):
			if pPlayer.hasTrait(iTrait):
				pPlayer.setHasTrait(iTrait,False)
			
	if pOpponent.isHasPromotion(getInfoType('PROMOTION_GODSLAYER')):
		pOppPlayer = gc.getPlayer(pOpponent.getOwner())
		if pOppPlayer.isHuman():
			t = "TROPHY_FEAT_GODSLAYER"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)

def postCombatAuricAscendedWon(pCaster, pOpponent):
	if pOpponent.isHasPromotion(getInfoType('PROMOTION_GODSLAYER')):
		iPlayer = pCaster.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		for iTrait in range(gc.getNumTraitInfos()):
			if pPlayer.hasTrait(iTrait):
				if not gc.isNoCrash():
					pPlayer.setHasTrait(iTrait,False,-1,True,True)
				else:
					pPlayer.setHasTrait(iTrait,False)
		
		pCaster.kill(True, pOpponent.getOwner())
		pOppPlayer = gc.getPlayer(pOpponent.getOwner())
		if pOppPlayer.isHuman():
			t = "TROPHY_FEAT_GODSLAYER"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)

def onDeathAuric(pCaster):
	iPlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_AURIC"))+ pPlayer.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_AURIC_WINTER"))+pPlayer.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_AURIC_ASCENDED"))<=1 :
		for iTrait in range(gc.getNumTraitInfos()):
			if pPlayer.hasTrait(iTrait):
				pPlayer.setHasTrait(iTrait,False)
		pPlayer.setCivCounterMod(100)

def postCombatBasium(pCaster, pOpponent):
	if not pCaster.isImmortal():
		iPlayer = pCaster.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		for iTrait in range(gc.getNumTraitInfos()):
			if pPlayer.hasTrait(iTrait):
				if not gc.isNoCrash():
					pPlayer.setHasTrait(iTrait,False,-1,True,True)
				else:
					pPlayer.setHasTrait(iTrait,False)
				
		pOppPlayer = gc.getPlayer(pOpponent.getOwner())
		if pOppPlayer.isHuman():
			t = "TROPHY_DEFEATED_BASIUM"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)

def postCombatBuboes(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_BUBOES"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatHyborem(pCaster, pOpponent):
	if not pCaster.isImmortal():
		iPlayer = pCaster.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		for iTrait in range(gc.getNumTraitInfos()):
			if iTrait != getInfoType('TRAIT_FALLOW'):
				if pPlayer.hasTrait(iTrait):
					if not gc.isNoCrash():
						pPlayer.setHasTrait(iTrait,False,-1,True,True)
					else:
						pPlayer.setHasTrait(iTrait,False)
		pOppPlayer = gc.getPlayer(pOpponent.getOwner())
		if pOppPlayer.isHuman():
			t = "TROPHY_DEFEATED_HYBOREM"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)

def postCombatLeviathan(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_LEVIATHAN"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatBleedingGod(pCaster,pOpponent):
	pCasterPlot=pCaster.plot()
	if pCasterPlot.getBonusType(-1)==-1:
		iRand = CyGame().getSorenRandNum(100,"bleedinggod")
		if (iRand<10):
			pCasterPlot.setBonusType(gc.getInfoTypeForString("BONUS_BLEEDING_GOD_WINE"))
	
def postCombatOrthus(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_ORTHUS"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatZarcaz(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_ZARCAZ"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatStephanos(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_STEPHANOS"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatTreant(pCaster):
	pPlot = pCaster.plot()
	if pPlot.getFeatureType() == -1:
		if pPlot.canHaveFeature(getInfoType('FEATURE_FOREST_NEW')):
			pPlot.setFeatureType(getInfoType('FEATURE_FOREST_NEW'), 1)

def postCombatYersinia(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_YERSINIA"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatReduceCombat1(pCaster, pOpponent):
	if pOpponent.isAlive():
		if pCaster.baseCombatStr() > 5:
			pCaster.changeStrBoost(-1)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_STRENGTH_REDUCED", ()),'',1,'Art/Interface/Buttons/Units/Repentant Angel.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)

def postCombatReducePopulation(pCaster, pOpponent):
	pPlot = pOpponent.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getPopulation() > 1:
			pCity.changePopulation(-1)
			CyInterface().addMessage(pCity.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POPULATION_REDUCED", ()),'',1,'Art/Interface/Buttons/Units/Angel of Death.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)

def postCombatReducePopulationDTesh(pCaster, pOpponent):
	pPlot = pOpponent.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getPopulation() > 1:
			pCity.changePopulation(-1)
			CyInterface().addMessage(pCity.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POPULATION_REDUCED", ()),'',1,'Art/Interface/Buttons/Units/Angel of Death.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
			pPlayer = gc.getPlayer(pCaster.getOwner())
			iUnit = getInfoType('UNIT_SLAVE_UNDEAD')
			newUnit = pPlayer.initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
def postCombatLostSailorsDirge(pCaster, pOpponent):
	iPlayer = pOpponent.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
#	iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_SAILORS_DIRGE_DEFEATED')
#	triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCaster.getX(), pCaster.getY(), iPlayer, -1, -1, -1, -1, -1)

def postCombatLostPhoenix(pCaster, pOpponent):
	iPlayer = pOpponent.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if (pOpponent.isAlive()):
		pOpponent.setHasPromotion(getInfoType("PROMOTION_IMMORTAL"),True)

def postCombatLostRamVir(pCaster, pOpponent):
	iPlayer = pOpponent.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if (pOpponent.isAlive()):
		pOpponent.setHasPromotion(getInfoType("PROMOTION_CRAZED"),False)
		pOpponent.setHasPromotion(getInfoType("PROMOTION_DISEASED"),False)
		pOpponent.setHasPromotion(getInfoType("PROMOTION_ENERVATED"),False)
		pOpponent.setHasPromotion(getInfoType("PROMOTION_FATIGUED"),False)
		pOpponent.setHasPromotion(getInfoType("PROMOTION_PLAGUED"),False)
		pOpponent.setHasPromotion(getInfoType("PROMOTION_POISONED"),False)
		pOpponent.setHasPromotion(getInfoType("PROMOTION_SHATTERED_NERVE"),False)
		pOpponent.setHasPromotion(getInfoType("PROMOTION_UNWHOLESOME_ADDICTION"),False)
		pOpponent.setHasPromotion(getInfoType("PROMOTION_WINTERED"),False)
		pOpponent.setHasPromotion(getInfoType("PROMOTION_WITHERED"),False)
		pOpponent.setHasPromotion(getInfoType("PROMOTION_CRAZED"),False)



def postCombatSplit(pCaster, pOpponent):
	gc 				= CyGlobalContext()
	if pCaster.isHasPromotion(getInfoType('PROMOTION_WEAK')) == False:
		pPlayer = gc.getPlayer(pCaster.getOwner())
		iUnit = pCaster.getUnitType()
		newUnit = pPlayer.initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = pPlayer.initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(getInfoType('PROMOTION_STRONG'), False)
		newUnit2.setHasPromotion(getInfoType('PROMOTION_STRONG'), False)
		newUnit.setDamage(25, -1)
		newUnit2.setDamage(25, -1)
		if pCaster.isHasPromotion(getInfoType('PROMOTION_STRONG')) == False:
			newUnit.setHasPromotion(getInfoType('PROMOTION_WEAK'), True)
			newUnit2.setHasPromotion(getInfoType('PROMOTION_WEAK'), True)
		#Should we make this assign the units to the same Master as the original unit had?
		newUnit.setDuration(pCaster.getDuration())
		newUnit2.setDuration(pCaster.getDuration())
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SPLIT", ()),'',1,gc.getUnitInfo(iUnit).getButton(),ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)

def postCombatWolfRider(pCaster, pOpponent):
	if (pOpponent.getUnitType() == getInfoType('UNIT_WOLF') or pOpponent.getUnitType() == getInfoType('UNIT_WOLF_PACK')):
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WOLF_RIDER", ()),'',1,'Art/Interface/Buttons/Units/Wolf Rider.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
		pPlayer = gc.getPlayer(pCaster.getOwner())
		newUnit = pPlayer.initUnit(getInfoType('UNIT_WOLF_RIDER'), pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.convert(pCaster)

def postCombatDeathMarked(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if(pCaster.isAlive()):
		newUnit = pPlayer.initUnit(pCaster.getUnitType(), pOpponent.getX(), pOpponent.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), True)
		newUnit.setUnitArtStyleType(pCaster.getUnitArtStyleType())


def postCombatDeadLands(pCaster, pOpponent):
	pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
	if(pCaster.isAlive()):
		pPlot2 = findClearPlot(-1, pCaster.plot())
		if pPlot2!=-1:
			newUnit = pDemonPlayer.initUnit(pCaster.getUnitType(), pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(getInfoType('PROMOTION_UNDEAD'), True)
			newUnit.setUnitArtStyleType(pCaster.getUnitArtStyleType())
			newUnit.setMadeAttack(True)

def babySpiderGrowth(pCaster, ePromotion):
	gc 			= CyGlobalContext()
	CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SPIDER_GROWTH", (pCaster.getName(), )),'',1,'Art/Interface/Buttons/Units/Spider.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
	pPlayer 	= gc.getPlayer(pCaster.getOwner())

	iUnit 		= getInfoType('UNITCLASS_SPIDER')
	infoCiv 	= gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iUnit 		= infoCiv.getCivilizationUnits(iUnit)
	if iUnit == -1:
		iUnit = getInfoType('UNIT_SPIDER')

	pCaster.safeRemovePromotion(ePromotion)
	newUnit = pPlayer.initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.convert(pCaster)

def hauntedLandsEffects(pCaster):
	gc 				= CyGlobalContext()
	iHaunted 		= getInfoType('PROMOTION_HAUNTED')
	iSpooked 		= getInfoType('PROMOTION_SPOOKED')
	iShatteredNerve = getInfoType('PROMOTION_SHATTERED_NERVE')
	iUnwholesomeAddiction = getInfoType('PROMOTION_UNWHOLESOME_ADDICTION')
	setHasPromo		= pCaster.setHasPromotion

	pPlot = pCaster.plot()
	if pPlot.getPlotEffectType() != Feature["Haunted Lands"]:
		setHasPromo(iHaunted, False)
		setHasPromo(iUnwholesomeAddiction, False)
		setHasPromo(iSpooked, False)

	iSiege 		= getInfoType('UNITCOMBAT_SIEGE')
	iGolem 		= Race["Golem"]
	iGhostwalker= getInfoType('UNIT_GHOSTWALKER')
	#iCreeper 	= getInfoType('UNIT_CREEPER')

	randNum = CyGame().getSorenRandNum
	if randNum(9, "Haunted Lands Effects 1") == 1:
		if pCaster.isAlive() or pCaster.getUnitType == iGhostwalker: # or pCaster.getUnitCombatType() == iSiege or pCaster.getRace() == iGolem:

			if pCaster.getUnitType == iGhostwalker:
				if pCaster.getDamage() > 50:
					if randNum(2, "HL wounded Ghostwalker creeper check") == 0:
	#					spawnUnit = pPlayer.initUnit(iCreeper, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	#					CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("A Reaching Creeper is born of a Ghostwalker's blood.", ()),'',1,'Art/Interface/Buttons/Units/Scions/creeper.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
						return

			iEstranged = getInfoType('PROMOTION_ESTRANGED')
			if pCaster.getDamage() >= 20:
				setHasPromo(Race["Undead"], True)
				setHasPromo(iEstranged, True)
				CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_HAUNTED_LANDS_TURN_UNDEAD", ()),'',3,'Art/Interface/Buttons/Promotions/races/Undead.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)
				return

			iRnd = randNum(100, "Haunted Lands Effects 2")
			if iRnd < 30:
				CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_HAUNTED_LANDS_TAKEN_TOLL", ()),'',3,'Art/Interface/Buttons/TerrainFeatures/haunted.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)
				iRnd2 = randNum(17, "Haunted Lands Effects 3")
				if iRnd2 <= 2:
					setHasPromo(iUnwholesomeAddiction, True)
				if (iRnd2 >=3 and iRnd2 <= 6):
					setHasPromo(iShatteredNerve, True)
				if (iRnd2 >= 7 and iRnd2 <= 11):
					setHasPromo(iHaunted, True)
				if (iRnd2 >= 12 and iRnd2 <= 17):
					setHasPromo(iSpooked, True)
			if iRnd < 10:
				iRnd3 = randNum(17, "Haunted Lands Effects 4")
				if iRnd3 <= 2:
					setHasPromo(iUnwholesomeAddiction, True)
				if (iRnd3 >=3 and iRnd3 <= 6):
					setHasPromo(iShatteredNerve, True)
				if (iRnd3 >= 7 and iRnd3 <= 11):
					setHasPromo(iHaunted, True)
				if (iRnd3 >= 12 and iRnd3 <= 17):
					setHasPromo(iSpooked, True)

def postCombatGainKnowledge(pCaster, pOpponent):
		iOpponentLevel = pOpponent.getLevel()
		if iOpponentLevel > 0:
				CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_GAIN_KNOWLEDGE", ()),'',1,'Art/Interface/Buttons/Units/Wolf Rider.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
				pCaster.changeExperience(iOpponentLevel*2, 100, True, False, True)
									
def canGainPromFleshGolem(iPromotion, pFleshGolem):
	if pFleshGolem.isHasPromotion(iPromotion):
		return False
	iChanneling 	= getInfoType('PROMOTION_CHANNELING1')
	iChanneling2 	= getInfoType('PROMOTION_CHANNELING2')
	iChanneling3 	= getInfoType('PROMOTION_CHANNELING3')
	iDivine 		= getInfoType('PROMOTION_DIVINE')
	iUndead			= Race["Undead"]
	if iPromotion in [iChanneling, iChanneling2, iChanneling3, iDivine, iUndead]:
		return False
	pPromotion = gc.getPromotionInfo(iPromotion)
	if pPromotion.isRace():
		return False
	if pPromotion.getBonusPrereq() != -1:
		return False
	if pPromotion.getNumPrereqPromotionANDs()>0:
		for i in range(0,pPromotion.getNumPrereqPromotionANDs(),1):
			if pPromotion.getPrereqPromotionANDs(i,False) in [iChanneling2, iChanneling3]:
				return False
	if pPromotion.isEquipment():
		return False
	return True
	
def willImproveFleshGolem(pUnit, pFleshGolem):
	if pUnit.baseCombatStr() > pFleshGolem.baseCombatStr():
		return True
	for iCount in xrange(gc.getNumPromotionInfos()):
		if pUnit.isHasPromotion(iCount):
			if canGainPromFleshGolem(iCount, pFleshGolem):
				return True
	return False

def reqAddToFleshGolem(caster):
	if caster.isImmortal():
		return False
	if caster.isImmuneToMagic():
		return False
	if not caster.getMasterUnit().isNone():
		return False
	iFleshGolem = getInfoType('UNITCLASS_FLESH_GOLEM')
	pPlot = caster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitClassType() == iFleshGolem):
			if willImproveFleshGolem(caster, pUnit):
				return True
	return False

def spellAddToFleshGolem(caster):
	gc 				= CyGlobalContext()
	pPlayer 		= gc.getPlayer(caster.getOwner())
	pPlot 			= caster.plot()
#Can either use Tarq's fix (block all immortals) or this one (cancel any immortality).  Personally I don't care
#	caster.changeImmortal(-20)
	iChanneling 	= getInfoType('PROMOTION_CHANNELING1')
	iChanneling2 	= getInfoType('PROMOTION_CHANNELING2')
	iChanneling3 	= getInfoType('PROMOTION_CHANNELING3')
	iDivine 		= getInfoType('PROMOTION_DIVINE')
	iFleshGolem 	= getInfoType('UNITCLASS_FLESH_GOLEM')
	pFleshGolem 	= -1
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitClassType() == iFleshGolem):
			if willImproveFleshGolem(caster, pUnit):
				pFleshGolem = pUnit
	if pFleshGolem != -1:
		if caster.baseCombatStr() > pFleshGolem.baseCombatStr():
			pFleshGolem.changeStrBoost(1)
		getPromInfo = gc.getPromotionInfo
		setHasPromo	= pFleshGolem.setHasPromotion
		for iCount in xrange(gc.getNumPromotionInfos()):
			if caster.isHasPromotion(iCount):
				if canGainPromFleshGolem(iCount, pFleshGolem):
					setHasPromo(iCount, True)
		if pFleshGolem.baseCombatStr() >= 15:
			if pPlayer.isHuman():
				t = "TROPHY_FEAT_FLESH_GOLEM_15"
				if not CyGame().isHasTrophy(t):
					CyGame().changeTrophyValue(t, 1)

def reqAddToFreakShowHuman(caster):
	if caster.getRace() != -1:
		return False
	return True

def reqArcaneLacuna(caster):
	gc 			= CyGlobalContext()
	pPlayer 	= gc.getPlayer(caster.getOwner())
	manaTypes = [ 'BONUS_MANA_AIR','BONUS_MANA_BODY','BONUS_MANA_CHAOS','BONUS_MANA_DEATH','BONUS_MANA_EARTH','BONUS_MANA_ENCHANTMENT','BONUS_MANA_ENTROPY','BONUS_MANA_FIRE','BONUS_MANA_LAW','BONUS_MANA_LIFE','BONUS_MANA_METAMAGIC','BONUS_MANA_MIND','BONUS_MANA_NATURE','BONUS_MANA_SHADOW','BONUS_MANA_SPIRIT','BONUS_MANA_SUN','BONUS_MANA_WATER' ]
	iCount = 0
	getNumBoni 	= CyMap().getNumBonuses
	for szBonus in manaTypes:
		iBonus = getInfoType(szBonus)
		iCount += getNumBoni(iBonus)
	if iCount == 0:
		return False
	if not pPlayer.isHuman():
		if iCount < 7:
			return False
	return True

def spellArcaneLacuna(caster):
	gc 				= CyGlobalContext()
	manaTypes 	= [ 'BONUS_MANA_AIR','BONUS_MANA_BODY','BONUS_MANA_CHAOS','BONUS_MANA_DEATH','BONUS_MANA_EARTH','BONUS_MANA_ENCHANTMENT','BONUS_MANA_ENTROPY','BONUS_MANA_FIRE','BONUS_MANA_LAW','BONUS_MANA_LIFE','BONUS_MANA_METAMAGIC','BONUS_MANA_MIND','BONUS_MANA_NATURE','BONUS_MANA_SHADOW','BONUS_MANA_SPIRIT','BONUS_MANA_SUN','BONUS_MANA_WATER' ]
	iAdept 		= getInfoType('UNITCOMBAT_ADEPT')
	iCount 		= 0
	getPlayer	= gc.getPlayer
	pPlayer 	= getPlayer(caster.getOwner())
	getNumBoni	= CyMap().getNumBonuses
	for szBonus in manaTypes:
		iBonus = getInfoType(szBonus)
		iCount += getNumBoni(iBonus)
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if pUnit.getUnitCombatType() == iAdept:
			pUnit.changeExperience(iCount, -1, False, False, False)
	iDelay = 20
	eGameSpeed	= CyGame().getGameSpeedType()
	if eGameSpeed == getInfoType('GAMESPEED_QUICK'): 	iDelay = 14
	if eGameSpeed == getInfoType('GAMESPEED_EPIC'): 	iDelay = 30
	if eGameSpeed == getInfoType('GAMESPEED_MARATHON'):	iDelay = 60
	for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
		pPlayer2 = getPlayer(iPlayer2)
		if pPlayer2.isAlive():
			if pPlayer2.getTeam() != pPlayer.getTeam():
				pPlayer2.changeDisableSpellcasting(iDelay)

def reqArdor(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getGreatPeopleCreated() == 0:
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getGreatPeopleCreated() < 5:
			return False
	return True

def spellArdor(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.setGreatPeopleCreated(0)
	pPlayer.setGreatPeopleThresholdModifier(0)

def reqArenaBattle(caster):
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_MELEE'):
		return True
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_RECON'):
		return True
	if caster.getUnitClassType() == getInfoType('UNITCLASS_SLAVE'):
		return True
	return False

def spellArenaBattle(caster):
	pCity = caster.plot().getPlotCity()
	pCity.changeHappinessTimer(3)
	if CyGame().getSorenRandNum(100, "Arena Battle") < 50:
		caster.changeExperience(CyGame().getSorenRandNum(6, "Arena Battle") + 1, -1, False, False, False)
		caster.setDamage(25, caster.getOwner())
		CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ARENA_WIN", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
		if caster.getUnitClassType() == getInfoType('UNITCLASS_SLAVE'):
			pPlayer = gc.getPlayer(caster.getOwner())
			newUnit = pPlayer.initUnit(getInfoType('UNIT_WARRIOR'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(caster)
	else:
		CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ARENA_LOSE", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(7),caster.getX(),caster.getY(),True,True)
		caster.kill(True, PlayerTypes.NO_PLAYER)

def reqCallBlizzard(caster):
	iBlizzard = getInfoType('FEATURE_BLIZZARD')
	pPlot = caster.plot()
	if pPlot.getFeatureType() == iBlizzard:
		return False
	if pPlot.getFeatureType() == Feature["Ancient Forest"]:
		return False
	getPlot	= CyMap().plot
	iRange = 1
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = CyMap().plot(x, y)
		if pPlot.getFeatureType() == iBlizzard:
			return True
	return False

def spellCallBlizzard(caster):
	iBlizzard = getInfoType('FEATURE_BLIZZARD')
	pBlizPlot = -1
	getPlot	= CyMap().plot
	iRange = 1
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = CyMap().plot(x, y)
		if pPlot.getFeatureType() == iBlizzard:
			pBlizPlot = pPlot
	if pBlizPlot != -1:
		pBlizPlot.setFeatureType(-1, -1)
	pPlot = caster.plot()
	pPlot.setFeatureType(iBlizzard, 0)
	Blizzards2.doBlizzard(pPlot)		#Added in Frozen: TC01

def reqCallForm(caster):
	if caster.getSummoner() == -1:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	pUnit = pPlayer.getUnit(caster.getSummoner())
	pPlot = caster.plot()
	if not pUnit.canMoveInto(pPlot, False, False, False):
		return False
	return True

def spellCallForm(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pUnit = pPlayer.getUnit(caster.getSummoner())
	pPlot = caster.plot()
	pUnit.setXY(pPlot.getX(), pPlot.getY(), False, True, True,False)

def reqCallOfTheGrave(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = gc.getTeam(pPlayer.getTeam())
	iGraveyard = getInfoType('IMPROVEMENT_GRAVEYARD')
	getPlot	= CyMap().plot
	iRange = 2
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = CyMap().plot(x, y)
		for i in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			p2Player = gc.getPlayer(pUnit.getOwner())
			e2Team = p2Player.getTeam()
			if pTeam.isAtWar(e2Team) == True:
				return True
			if pUnit.isHasPromotion(Race["Undead"]) == True:
				if pUnit.isHurt():
					return True
			if pPlot.getImprovementType() == iGraveyard:
				return True
	return False

def spellCallOfTheGrave(caster):
	gc 				= CyGlobalContext()
	getPlayer		= gc.getPlayer
	pPlayer 		= getPlayer(caster.getOwner())
	pTeam 		= gc.getTeam(pPlayer.getTeam())
	iGraveyard 	= getInfoType('IMPROVEMENT_GRAVEYARD')
	iWraith		= getInfoType('UNIT_WRAITH')
	iDeath		= getInfoType('DAMAGE_DEATH')
	initUnit	= pPlayer.initUnit
	getPlot		= CyMap().plot
	iNoAI		= UnitAITypes.NO_UNITAI
	iSouth		= DirectionTypes.DIRECTION_SOUTH
	trigger		= CyEngine().triggerEffect
	iSacrifice	= getInfoType('EFFECT_SACRIFICE')
	getPlot	= CyMap().plot
	iRange = 2
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = CyMap().plot(x, y)
		bValid = False
		for i in xrange(pPlot.getNumUnits()):
			pUnit 		= pPlot.getUnit(i)
			p2Player 	= gc.getPlayer(pUnit.getOwner())
			e2Team 		= p2Player.getTeam()
			if pTeam.isAtWar(e2Team) == True:
				pUnit.doDamage(40, 100, caster, iDeath, True)
				bValid = True
			else:
				if pUnit.isHasPromotion(Race["Undead"]) == True:
					if pUnit.isHurt():
						pUnit.setDamage(0, caster.getOwner())
			if pPlot.getImprovementType() == iGraveyard:
				pPlot.setImprovementType(-1)
				initUnit(iWraith, x, y, iNoAI, iSouth)
				initUnit(iWraith, x, y, iNoAI, iSouth)
				initUnit(iWraith, x, y, iNoAI, iSouth)
				bValid = True
		if bValid:
			trigger(iSacrifice,pPlot.getPoint())

def reqCommanderJoin(caster):
	gc 				= CyGlobalContext()
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	if caster.isHasPromotion(getInfoType('PROMOTION_GREAT_COMMANDER')):
		return False
	iCommander = getInfoType('UNITCLASS_COMMANDER')
	pCommander = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitClassType() == iCommander):
			pCommander = pUnit
	if pCommander == -1:
		return False
	if pCommander.isHasCasted():
		return False
	if pPlayer.isHuman() == False:
		if caster.baseCombatStr() <= 5:
			return False
	return True

def spellCommanderJoin(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iCommander = getInfoType('UNITCLASS_COMMANDER')
	pCommander = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitClassType() == iCommander):
			pCommander = pUnit
	if pCommander != -1:
		pCommander.setHasPromotion(getInfoType('PROMOTION_GOLEM'), True)
		pCommander.kill(False, PlayerTypes.NO_PLAYER)

def spellCommanderJoinDecius(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iDecius = getInfoType('UNIT_DECIUS')
	pCommander = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitType() == iDecius):
			pCommander = pUnit
	if pCommander != -1:
		caster.setScenarioCounter(iDecius)
		pCommander.setHasPromotion(getInfoType('PROMOTION_GOLEM'), True)
		pCommander.kill(False, PlayerTypes.NO_PLAYER)

def spellCommanderSplit(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iCommander = getInfoType('UNIT_COMMANDER')
	if caster.getScenarioCounter() == getInfoType('UNIT_DECIUS'):
		iCommander = getInfoType('UNIT_DECIUS')
		caster.setScenarioCounter(-1)
	newUnit = pPlayer.initUnit(iCommander, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def getHelpAdmiralJoin(argsList):
	eSpell, pCaster = argsList
	pPlot		= pCaster.plot()
	iTeam		= pCaster.getTeam()
	iAdmClass	= git("UNITCLASS_COMMANDER")
	fCasterXP	= pCaster.getExperience()
	pTarget		= -1
	szHelp		= ""
	for iUnit in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(iUnit)
		if not pUnit.getUnitClassType() == iAdmClass:
			continue
		if not pUnit.getTeam() == iTeam:
			continue
		pTarget = pUnit
		szHelp = localText.getText("TXT_KEY_ADM_JOIN_PYHELP_TARGET", (pTarget.getNameKey(),))
		return szHelp
	return szHelp

def spellAdmiralJoin(pCaster):
	pPlot		= pCaster.plot()
	iTeam		= pCaster.getTeam()
	iAdmClass	= git("UNITCLASS_COMMANDER")
	fCasterXP	= pCaster.getExperience()
	pTarget		= -1
	for iUnit in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(iUnit)
		if not pUnit.getUnitClassType() == iAdmClass:
			continue
		if not pUnit.getTeam() == iTeam:
			continue
		pTarget = pUnit
		sTargetName = pTarget.getNameKey()
		fTargetXP = pTarget.getExperience()
		pCaster.setName(sTargetName)
		if fTargetXP > fCasterXP:
			pCaster.setExperience(fTargetXP,-1)
		pTarget.kill(True, PlayerTypes.NO_PLAYER)
		return

def reqAdmiralJoin(pCaster):
	pPlot		= pCaster.plot()
	iTeam		= pCaster.getTeam()
	iAdmClass	= git("UNITCLASS_COMMANDER")
	lBlackList	= [git("UNITCLASS_TRADESHIP"),git("UNITCLASS_WYRMFISHER"),git("UNITCLASS_WORKBOAT")]
	if not pCaster.getDomainType() == DomainTypes.DOMAIN_SEA:
		return False
	if pCaster.getUnitClassType() in lBlackList:
		return False
	for iUnit in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(iUnit)
		if not pUnit.getUnitClassType() == iAdmClass:
			continue
		if not pUnit.getTeam() == iTeam:
			continue
		return True
	return False

def reqConvertCityBasium(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if pCity.getOwner() == caster.getOwner():
		return False
	return True

def spellConvertCityBasium(caster):
	pCity = caster.plot().getPlotCity()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.acquireCity(pCity,False,False)
	pCity = caster.plot().getPlotCity()
	pCity.changeCulture(iPlayer, 300, True)

def reqConvertCityRantine(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if pCity.getOwner() == caster.getOwner():
		return False
	if pCity.getOwner() != gc.getORC_PLAYER():
		return False
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == gc.getORC_PLAYER():
			if pUnit.baseCombatStr() > caster.baseCombatStr():
				return False
	return True

def spellConvertCityRantine(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.acquireCity(pCity,False,False)


def spellPaxDiabolis(caster):
	pCity = caster.plot().getPlotCity()
	iPop = pCity.getPopulation()
	gc	= CyGlobalContext()
	giftUnit = CvEventInterface.getEventManager().cf.giftUnit
	if CyGame().countKnownTechNumTeams(getInfoType('TECH_INFERNAL_PACT')) > 0 and CyGame().getNumCivActive(Civ["Infernal"]) > 0:
		for i in xrange(iPop):
			giftUnit(getInfoType('UNIT_MANES'), Civ["Infernal"], 0, caster.plot(), caster.getOwner())
	pCity.kill()

	pPlayer = gc.getPlayer(caster.getOwner())
	iDemonTeam = gc.getPlayer(gc.getDEMON_PLAYER()).getTeam()
	pTeam = gc.getTeam(pPlayer.getTeam())
	pTeam.makePeace(iDemonTeam)


def spellCreateBatteringRam(caster):
	pPlot = caster.plot()
	pPlot.setFeatureType(-1, -1)

def effectCrownOfBrillance(caster):
	caster.cast(getInfoType('SPELL_CROWN_OF_BRILLANCE'))

def reqCrownOfBrillance(caster):
	if caster.isHasPromotion(getInfoType('PROMOTION_CROWN_OF_BRILLANCE')):
		return False
	return True

def hyboremAI(caster):
	if caster.isHasPromotion(getInfoType('PROMOTION_IMMORTAL')):
		return
	else:
		caster.setUnitAIType(getInfoType('UNITAI_CITY_DEFENSE'))

def reqCrush(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	getPlot	= CyMap().plot
	iRange = 2 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			bEnemy = False
			bNeutral = False
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pTeam.isAtWar(pUnit.getTeam()):
					bEnemy = True
				else:
					bNeutral = True
			if (bEnemy and bNeutral == False):
				return True
	return False

def spellCrush(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iBestValue = 0
	pBestPlot = -1
	getPlot	= CyMap().plot
	iRange = 2 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			bNeutral = False
			iValue = 0
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pTeam.isAtWar(pUnit.getTeam()):
					iValue = iValue + 10
				else:
					bNeutral = True
			if (iValue > iBestValue and bNeutral == False):
				iBestValue = iValue
				pBestPlot = pPlot
	if pBestPlot != -1:
		for i in range(pBestPlot.getNumUnits()):
			pUnit = pBestPlot.getUnit(i)
			pUnit.doDamage(50, 75, caster, getInfoType('DAMAGE_PHYSICAL'), True)
		CyEngine().triggerEffect(getInfoType('EFFECT_CRUSH'),pBestPlot.getPoint())

def reqBanishment(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.isHasPromotion(Race["Undead"]) or pUnit.isHasPromotion(Race["Demon"]):
					pOtherPlayer = gc.getPlayer(pUnit.getOwner())
					iOtherTeam = pOtherPlayer.getTeam()
					if pPlayer.isHuman() and iTeam != iOtherTeam :
						return True
					pOtherTeam = gc.getTeam(iOtherTeam)
					if pOtherTeam.isAtWar(iTeam):
						return True
	return False

def spellBanishment(caster):
	iIra = getInfoType('UNIT_IRA')
	pPlayer = gc.getPlayer(caster.getOwner())
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x,y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.isHasPromotion(Race["Undead"]) or pUnit.isHasPromotion(Race["Demon"]) or pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_ICE_DEMON")):
					pUnit.doDamage(20, 50, caster, getInfoType('DAMAGE_HOLY'), True)
				if pUnit.getUnitType() == iIra:
					iStrength = pUnit.getStrBoost()
					if iStrength >= 0:
						pUnit.changeStrBoost(-4)

def reqDispelMagic(caster):
	if caster.canDispel(getInfoType('SPELL_DISPEL_MAGIC')):
		return True
	pPlot = caster.plot()
	if pPlot.getBonusType(-1) != -1:
		if gc.getBonusInfo(pPlot.getBonusType(-1)).getBonusClassType() == getInfoType('BONUSCLASS_MANA'):
			if pPlot.getImprovementType() == -1:
				return True
			if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent() == False:
				return True
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			if pPlot.getPlotEffectType() == Feature["Haunted Lands"]:
				if pPlot.isOwned():
					if(caster.getOwner()==pPlot.getOwner() or gc.getPlayer(caster.getOwner()).isHuman() or gc.getTeam(caster.getTeam()).isAtWar(gc.getPlayer(pPlot.getOwner()).getTeam())):
						if gc.getPlayer(pPlot.getOwner()).getCivilizationType() != Civ["Scions"]:
							return True
					else:
						return False
				else:
					return True
	return False

def spellDispelMagic(caster):
	pPlot = caster.plot()
	if pPlot.getBonusType(-1) != -1:
		if gc.getBonusInfo(pPlot.getBonusType(-1)).getBonusClassType() == getInfoType('BONUSCLASS_MANA'):
			if pPlot.getImprovementType() == -1:
				pPlot.setBonusType(getInfoType('BONUS_MANA'))
			else:
				if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent() == False and not gc.getImprovementInfo(pPlot.getImprovementType()).isFort() :
					pPlot.setBonusType(getInfoType('BONUS_MANA'))
					pPlot.setImprovementType(-1)
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			if pPlot.getPlotEffectType() == Feature["Haunted Lands"]:
				if pPlot.isOwned():
					if gc.getPlayer(pPlot.getOwner()).getCivilizationType() != Civ["Scions"]:
						pPlot.setFeatureType(-1, -1)
				else:
					pPlot.setFeatureType(-1, -1)

def reqDisrupt(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if caster.getTeam() == pCity.getTeam():
		return False
	if pCity.getTeam() == gc.getORC_TEAM():
		return False
	return True

def spellDisrupt(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iPlayer2 = pCity.getOwner()
	pPlayer2 = gc.getPlayer(iPlayer2)
	pCity.changeHurryAngerTimer(2)
	iRnd = CyGame().getSorenRandNum(3, "Disrupt")
	if iRnd != 0:
		pCity.changeCulture(iPlayer2,-1 * iRnd,True)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISRUPT_ENEMY",()),'',1,'Art/Interface/Buttons/Spells/Disrupt.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
	CyInterface().addMessage(iPlayer2,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISRUPT",()),'',1,'Art/Interface/Buttons/Spells/Disrupt.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
	if pCity.getCulture(iPlayer2) < 1:
		pPlayer.acquireCity(pCity,False,False)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-4)

def reqDivineRetribution(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		pTeam = gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) < 2:
			return False
	return True

def spellDivineRetribution(caster):
	gc 				= CyGlobalContext()
	iBlackLady 		= getInfoType('UNIT_KORRINA_BLACK_LADY')
	iBlackLadyHaunt = getInfoType('UNIT_HAUNT_KORRINA')
	iHoly			= getInfoType('DAMAGE_HOLY')
	getPlayer		= gc.getPlayer
	for iPlayer in xrange(gc.getMAX_PLAYERS()):
		if getPlayer(iPlayer).isAlive():
			py = PyPlayer(iPlayer)
			for pUnit in py.getUnitList():
				if (pUnit.getRace() == Race["Demon"] or pUnit.isHasPromotion(Race["Undead"]) == True or pUnit.isHasPromotion(getInfoType("PROMOTION_ICE_DEMON"))==True) and pUnit.getCivilizationType() != Civ["Scions"]:
					pUnit.doDamageCity(50, 100, caster, iHoly, False)
				if pUnit.getCivilizationType() == Civ["Scions"] and pUnit.getUnitType() != iBlackLady:
					if pUnit.getUnitType() != iBlackLadyHaunt:
						pUnit.doDamageCity(25, 100, caster, iHoly, False)

def reqDomination(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if caster.getNumForcedMinions() >= 3:
		return False
	iResistMax = 95
	if pPlayer.isHuman() == False:
		iResistMax = 65
	iTeam 	= pPlayer.getTeam()
	pTeam 	= gc.getTeam(iTeam)
	isAtWar	= pTeam.isAtWar
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.isAlive():
					if not pUnit.isDelayedDeath():
						if isAtWar(pUnit.getTeam()):
							iResist = pUnit.getResistChance(caster, getInfoType('SPELL_DOMINATION'))
							if iResist <= iResistMax:
								return True
	return False

def spellDomination(caster):
	gc 				= CyGlobalContext()
	iSpell 			= getInfoType('SPELL_DOMINATION')
	pPlayer = gc.getPlayer(caster.getOwner())
	iResistMax = 95
	iBestValue = 0
	pBestUnit = -1
	if not pPlayer.isHuman():
		iResistMax = 20
	iTeam 	= pPlayer.getTeam()
	pTeam 	= gc.getTeam(iTeam)
	isAtWar	= pTeam.isAtWar
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				iValue = 0
				if pUnit.isAlive():
					if pUnit.isDelayedDeath() == False:
						if isAtWar(pUnit.getTeam()):
							iResist = pUnit.getResistChance(caster, iSpell)
							if iResist <= iResistMax:
								iValue = pUnit.baseCombatStr() * 10
								iValue = iValue + (100 - iResist)
								if iValue > iBestValue:
									iBestValue = iValue
									pBestUnit = pUnit
	if pBestUnit != -1:
		pPlot = caster.plot()
		iPreviousOwner = pBestUnit.getOwner()
		if pBestUnit.isResisted(caster, iSpell) == False:
			CyInterface().addMessage(pBestUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOMINATION", ()),'',1,'Art/Interface/Buttons/Spells/Domination.dds',ColorTypes(7),pBestUnit.getX(),pBestUnit.getY(),True,True)
			CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOMINATION_ENEMY", ()),'',1,'Art/Interface/Buttons/Spells/Domination.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			newUnit = pPlayer.initUnit(pBestUnit.getUnitType(), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(pBestUnit)
			newUnit.changeImmobileTimer(1)
			newUnit.setPreviousOwner(iPreviousOwner)
			caster.addMinion(newUnit)
		else:
			CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOMINATION_FAILED", ()),'',1,'Art/Interface/Buttons/Spells/Domination.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
				
def reqDousingTorrent(caster, spell):
	iRange = 1 + caster.getSpellExtraRange()
	getPlot	= CyMap().plot
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			if pPlot.getFeatureType() == getInfoType('FEATURE_FLAMES') or pPlot.getImprovementType() == getInfoType('IMPROVEMENT_SMOKE'):
				return True

def spellDousingTorrent(caster, spell):
	iRange = 1 + caster.getSpellExtraRange()
	getPlot	= CyMap().plot
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			bEffect = False
			if pPlot.getFeatureType() == getInfoType('FEATURE_FLAMES'):
				pPlot.setFeatureType(-1, -1)
				bEffect = True
			if pPlot.getImprovementType() == getInfoType('IMPROVEMENT_SMOKE'):
				pPlot.setImprovementType(-1)
				bEffect = True
			if bEffect:
				CyEngine().triggerEffect(getInfoType('EFFECT_SPRING'), pPlot.getPoint())

def reqEarthquake(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		pTeam = pPlayer.getTeam()
		getPlot	= CyMap().plot
		iRange = 1 + caster.getSpellExtraRange()
		for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
			pPlot = getPlot(x, y)
			if not pPlot.isNone():
				p2Player = gc.getPlayer(pPlot.getOwner())
				if pPlot.isOwned():
					e2Team = gc.getTeam(p2Player.getTeam())
					if not e2Team.isAtWar(pTeam):
						return False
	return True

def spellEarthquake(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = pPlayer.getTeam()
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			if (pPlot.isCity() or pPlot.getImprovementType() != -1):
				if pPlot.isOwned():
					startWar(caster.getOwner(), pPlot.getOwner(), WarPlanTypes.WARPLAN_TOTAL)
			if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				for i in xrange(gc.getNumBuildingInfos()):
					iRnd = CyGame().getSorenRandNum(100, "Earthquake - destory building")
					if (gc.getBuildingInfo(i).getConquestProbability() != 100 and gc.getBuildingClassInfo(gc.getBuildingInfo(i).getBuildingClassType()).getMaxPlayerInstances()==0 and iRnd <= 25):
						pCity.setNumRealBuilding(i, 0)
			for iUnit in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(iUnit)
				if pUnit.isFlying() == False:
					pUnit.setFortifyTurns(0)
			iRnd = CyGame().getSorenRandNum(100, "Earthquake - destroy improvment")
			if iRnd <= 25:
				iImprovement = pPlot.getImprovementType()
				if iImprovement != -1:
					if gc.getImprovementInfo(iImprovement).isPermanent() == False:
						pPlot.setImprovementType(-1)

def spellEnterPortal(caster):
	pPlot = caster.plot()
	iX = pPlot.getPortalExitX()
	iY = pPlot.getPortalExitY()
	pExitPlot = CyMap().plot(iX,iY)
	if not pPlot.isNone() and not pExitPlot.isNone():
		caster.setXY(iX, iY, False, True, True,False)

def reqEntertain(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if pCity.getTeam() == gc.getORC_TEAM():
		return False
	return True

def spellEntertain(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	iPlayer2 = pCity.getOwner()
	if iPlayer != iPlayer2:
		pPlayer = gc.getPlayer(iPlayer)
		pPlayer2 = gc.getPlayer(iPlayer2)
		iGold = (pCity.getPopulation() / 2) + 1
		pPlayer.changeGold(iGold)
		szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_ENTERTAIN_GOOD", (iGold, ))
		CyInterface().addMessage(iPlayer,True,25,szBuffer,'',1,'Art/Interface/Buttons/Spells/Entertain.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
		iGold = iGold * -1
		pPlayer2.changeGold(iGold)
		szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_ENTERTAIN_BAD", (iGold, ))
		CyInterface().addMessage(iPlayer2,True,25,szBuffer,'',1,'Art/Interface/Buttons/Spells/Entertain.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
	pCity.changeHappinessTimer(2)

def reqEscape(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if caster.getDamage() >= 50:
			return False
	return True

def reqFeast(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	eCiv = pPlayer.getCivilizationType()
#	if eCiv != Civ["Calabim"] and pPlayer.getLeaderType() != getInfoType('LEADER_ZARIA'):
#		return False
	if pCity.getPopulation() < 3:
		return False
	return True

def spellFeast(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	caster.changeExperience(pCity.getPopulation()-2, -1, False, False, False)
	pCity.changeHurryAngerTimer(3)
	pCity.changeCrime(-pCity.getPopulation()*5)
	

def reqFeed(caster):
	if not caster.isHurt(): return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		if caster.getDamage() < 20:
			return False
	return True

def spellFeed(caster):
	caster.setDamage(caster.getDamage() - 20, caster.getOwner())
	caster.setMadeAttack(False)
	pVictim = -1
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == caster.getOwner():
			if pUnit.getUnitType() == getInfoType('UNIT_BLOODPET'):
				if (pVictim == -1 or pVictim.getLevel() > pUnit.getLevel()):
					pVictim = pUnit
	if pVictim != -1:
		pVictim.kill(True, 0)
	pPlayer = gc.getPlayer(caster.getOwner())
	
	if pPlayer.hasTrait(getInfoType('TRAIT_DOMINANT')):
		caster.setHasPromotion(getInfoType('PROMOTION_COMMAND1'),True)
	if pPlayer.hasTrait(getInfoType('TRAIT_DOMINANT2')):
		caster.setHasPromotion(getInfoType('PROMOTION_COMMAND2'),True)
	if pPlayer.hasTrait(getInfoType('TRAIT_DOMINANT3')):
		caster.setHasPromotion(getInfoType('PROMOTION_COMMAND3'),True)

def reqFeastGraveleech(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	eCiv = pPlayer.getCivilizationType()
#	if eCiv != Civ["Calabim"] and pPlayer.getLeaderType() != getInfoType('LEADER_ZARIA'):
#		return False
	if  caster.isHasPromotion(getInfoType('PROMOTION_GRAVELEECH')):
		if not pCity.getNumRealBuilding(getInfoType('BUILDING_UNDYING_RITUAL_HOUSE')):
			return False
	if pCity.getPopulation() < 3:
		return False
	return True	

def reqFeedGraveleech(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.hasTrait(getInfoType('TRAIT_GRAVELEECH')): return False
	if not caster.isHurt(): return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		if caster.getDamage() < 20:
			return False
	return True

def reqFeedUndeadGraveyard(caster):
	pPlot = caster.plot()
	if (pPlot.getImprovementType() == getInfoType("IMPROVEMENT_GRAVEYARD") or pPlot.getImprovementType() == getInfoType("IMPROVEMENT_BARROW") or pPlot.getImprovementType() == getInfoType("IMPROVEMENT_CITY_RUINS")  or pPlot.getImprovementType() == getInfoType("IMPROVEMENT_CITY_RUINS_ANCIENT")  or pPlot.getImprovementType() == getInfoType("IMPROVEMENT_BARROW_GLOOMY")  or pPlot.getImprovementType() == getInfoType("IMPROVEMENT_BARROW_HOWLING")):
		return True
	return False
def spellFeedUndeadGraveyard(caster):
	caster.setDamage(caster.getDamage() - 20, caster.getOwner())
	caster.setMadeAttack(False)
	pPlot = caster.plot()
	pPlot.setImprovementType(-1)
	caster.changeExperienceTimes100(500,-1,False,False,False)
	
def reqFeedUndead(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if not caster.isHurt(): return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		if caster.getDamage() < 20:
			return False
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == caster.getOwner():
			if pUnit.getID() != caster.getID():
				if pUnit.isHasPromotion(getInfoType('PROMOTION_UNDEAD')):
					return True
	return False

	
def spellFeedUndead(caster):
	caster.setDamage(caster.getDamage() - 20, caster.getOwner())
	caster.setMadeAttack(False)
	pVictim = -1
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == caster.getOwner():
			if pUnit.getID() != caster.getID():
				if pUnit.isHasPromotion(getInfoType('PROMOTION_UNDEAD')):
					if (pVictim == -1 or pVictim.getLevel() > pUnit.getLevel()):
						pVictim = pUnit
	if pVictim != -1:
		pVictim.kill(True, 0)
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.hasTrait(getInfoType('TRAIT_GRAVELEECH2')): 
		caster.setHasPromotion(getInfoType('PROMOTION_UNDEAD_SOUL'),True)

def postCombatWinUndeadEater(pCaster, pOpponent):
	if pOpponent.isHasPromotion(getInfoType("PROMOTION_UNDEAD")):
		pCaster.setDamage(caster.getDamage() - 20, caster.getOwner())
		pCaster.setHasPromotion(getInfoType('PROMOTION_UNDEAD_SOUL'),True)

	
def reqForTheHorde(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	bPlayer = gc.getPlayer(gc.getORC_PLAYER())
	if gc.getTeam(pPlayer.getTeam()).isAtWar(bPlayer.getTeam()):
		return False
	if bPlayer.getNumUnits() == 0:
		return False
	if pPlayer.isHuman() == False:
		if bPlayer.getNumUnits() < 60:
			return False
	return True

def spellForTheHorde(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iHero = getInfoType('PROMOTION_HERO')
	iPromotionHorde = getInfoType('PROMOTION_FOR_THE_HORDE')
	iFrostling = getInfoType('PROMOTION_FROSTLING')

	py = PyPlayer(gc.getORC_PLAYER())
	for pUnit in py.getUnitList():                                                  # teleport everyone except:
		 if not pUnit.isHasPromotion(iHero):                                        # heroes
			if not pUnit.isHasPromotion(iFrostling):                                # frostlings
				if not (pUnit.getImmobileTimer() > 0):                              # immobile units
					if not pUnit.isLeashed():                                       # leashed units
						if not pUnit.isHasPromotion(Effect["Mana Guardian"]):       # Mana Guardians
							newUnit = pPlayer.initUnit(pUnit.getUnitType(), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							newUnit.convert(pUnit)
							newUnit.setHasPromotion(iPromotionHorde, True)

def reqGiftsOfNantosuelta(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumCities() == 0:
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getNumCities() < 5:
			return False
	return True

def spellGiftsOfNantosuelta(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iGoldenHammer = getInfoType('EQUIPMENT_GOLDEN_HAMMER')
	for pyCity in PyPlayer(iPlayer).getCityList() :
		pCity = pyCity.GetCy()
		newUnit = pPlayer.initUnit(iGoldenHammer, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def reqGiftVampirism(caster):
	if (not gc.isNoCrash()) and caster.isMercenary():	# deny spell for mercs - azatote
		return False
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner()):
			if not pUnit.isHasPromotion(getInfoType('PROMOTION_VAMPIRE')):
				if (pUnit.getLevel() >= 6 and pPlayer.getCivilizationType() == Civ["Calabim"]):
					return True
				if (pUnit.getLevel() >= 4 and pUnit.getUnitType() == getInfoType('UNIT_MOROI')):
					return True
				if (pUnit.getLevel() >= 8):
					return True
	return False

def spellGiftVampirism(caster):
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		pPlayer=gc.getPlayer(caster.getOwner())
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner()):
			if not pUnit.isHasPromotion(getInfoType('PROMOTION_VAMPIRE')):
				if (pUnit.getLevel() >= 6 and pPlayer.getCivilizationType() == Civ["Calabim"]):
					pUnit.setHasPromotion(getInfoType('PROMOTION_VAMPIRE'),True)
				if (pUnit.getLevel() >= 4 and pUnit.getUnitType() == getInfoType('UNIT_MOROI')):
					pUnit.setHasPromotion(getInfoType('PROMOTION_VAMPIRE'),True)
				if (pUnit.getLevel() >= 8):
					pUnit.setHasPromotion(getInfoType('PROMOTION_VAMPIRE'),True)

def spellGiveHammerToCraftsman(caster, promotion):
	pCity = caster.plot().getPlotCity()
	pCity.changeFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_ENGINEER'), 1)
	caster.setHasPromotion(getInfoType(promotion), False)

def reqHastursRazor(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = pPlayer.getTeam()
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.isHurt():
					if pPlayer.isHuman():
						return True
					if pUnit.getOwner() == caster.getOwner():
						return True
	return False

def spellHastursRazor(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	listDamage = []
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( iX, iY, iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				listDamage.append(pUnit.getDamageReal())
	for x, y in plotsInRange( iX, iY, iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				iRnd = listDamage[CyGame().getSorenRandNum(len(listDamage), "Hastur's Razor")]
				if iRnd != pUnit.getDamageReal():
					CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_HASTURS_RAZOR",()),'AS2D_CHARM_PERSON',1,'Art/Interface/Buttons/Spells/Hasturs Razor.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
					if pUnit.getOwner() != caster.getOwner():
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_HASTURS_RAZOR",()),'AS2D_CHARM_PERSON',1,'Art/Interface/Buttons/Spells/Hasturs Razor.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
					pUnit.setDamageReal(iRnd, caster.getOwner())

def reqHeal(caster):
	pPlot = caster.plot()
	iPoisoned = getInfoType('PROMOTION_POISONED')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.isHurt()):
			return True
		if pUnit.isHasPromotion(iPoisoned):
			return True
	return False

def spellHeal(caster,amount):
	pPlot = caster.plot()
	iPoisoned = getInfoType('PROMOTION_POISONED')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		pUnit.setHasPromotion(iPoisoned,False)
		if pUnit.isAlive():
			pUnit.changeDamage(-amount,0) #player doesn't matter - it won't kill

def spellHealingSalve(caster):
	caster.setDamage(0, caster.getOwner())

def reqHealingSalve(caster):
	if caster.isHasPromotion(getInfoType('PROMOTION_DISEASED')):
		return True
	if caster.isHasPromotion(getInfoType('PROMOTION_PLAGUED')):
		return True
	if caster.isHasPromotion(getInfoType('PROMOTION_POISONED')):
		return True
	if caster.isHasPromotion(getInfoType('PROMOTION_WITHERED')):
		return True
	if not caster.isHurt():
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if caster.getDamage() < 25:
			return False
	return True

def spellHealingPotion(caster):
	caster.setDamage(0, False)
	if (CyGame().getSorenRandNum(10, "Potion run out chance") < 3):
		caster.setHasPromotion(getInfoType('PROMOTION_HEALING_POTION'), False)

def reqNewtsDraught(caster):
	if caster.isHasCasted():
		return True
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if caster.getDamage() < 25:
			return False
	return True

def spellNewtsDraught(caster):
	caster.setHasCasted(False)

def reqHellfire(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getCivilizationType() != Civ["Infernal"]:
		return False
	pPlot = caster.plot()
	if pPlot.isCity():
		return False
	if pPlot.isWater():
		return False
	if pPlot.getImprovementType() != -1:
		return False
	iHellFire = getInfoType('IMPROVEMENT_HELLFIRE')
	getPlot	= CyMap().plot
	iMinDistance = 2
	for x, y in plotsInRange( caster.getX(), caster.getY(), iMinDistance ):
		pPlot2 = getPlot(x, y)
		if pPlot2.getImprovementType() == iHellFire:
			return False
	if pPlayer.isHuman() == False:
		if pPlot.isOwned():
			if pPlot.getOwner() == caster.getOwner():
				return False
	return True

def reqHeraldsCall(caster):
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner()):
			return True
	return False

def spellHeraldsCall(caster):
	iValor = getInfoType('PROMOTION_VALOR')
	iBlessed = getInfoType('PROMOTION_BLESSED')
	iCourage = getInfoType('PROMOTION_COURAGE')
	iLoyalty = getInfoType('PROMOTION_LOYALTY')
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner()):
			pUnit.setHasPromotion(iValor,True)
			pUnit.setHasPromotion(iBlessed, True)
			pUnit.setHasPromotion(iCourage, True)
			pUnit.setHasPromotion(iLoyalty, True)
			pUnit.setDuration(1)

def reqHide(caster):
	if caster.isMadeAttack():
		return False
	if caster.isHasPromotion(getInfoType('PROMOTION_HIDDEN')):
		return False
	return True

def reqHireScorpionClan(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	bPlayer = gc.getPlayer(gc.getORC_PLAYER())
	pTeam = gc.getTeam(pPlayer.getTeam())
	if pTeam.isAtWar(bPlayer.getTeam()):
		return False
	return True

def spellHireArcher(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_ARCHER'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellHireGiant(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iHorde = getInfoType('PROMOTION_FOR_THE_HORDE')
	newUnit = pPlayer.initUnit(getInfoType('UNIT_HILL_GIANT'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(iHorde, True)

def spellHireWarrior(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_WARRIOR'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellHireCyklop(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iHorde = getInfoType('PROMOTION_FOR_THE_HORDE')
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CYKLOP'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(iHorde, True)

def spellHireMinotaur(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iHorde = getInfoType('PROMOTION_FOR_THE_HORDE')
	newUnit = pPlayer.initUnit(getInfoType('UNIT_MINOTAUR_LESSER'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(iHorde, True)

def spellHireTroll(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iHorde = getInfoType('PROMOTION_FOR_THE_HORDE')
	newUnit = pPlayer.initUnit(getInfoType('UNIT_JOT_TROLL'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(iHorde, True)

def spellHireLizardman(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iHorde = getInfoType('PROMOTION_FOR_THE_HORDE')
	newUnit = pPlayer.initUnit(getInfoType('UNIT_LIZARDMAN'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(iHorde, True)

def spellHireWolfRider(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_HORSEMAN'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellHireUnits(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pCity = caster.plot().getPlotCity()
	iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_MAGNADINE_HIRE_UNITS')
	triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCity.getX(), pCity.getY(), iPlayer, pCity.getID(), -1, -1, -1, -1)

def reqHyboremsWhisper(caster):
	if gc.getGame().isNetworkMultiPlayer():
		return False
	pCity = CvEventInterface.getEventManager().cf.getAshenVeilCity(3)
	if pCity == -1:
		return False
	return True

def getHelpHyboremsWhisper(argsList):
	eSpell, pCaster = argsList
	szHelp = ""
	if gc.getGame().isNetworkMultiPlayer() or pCaster == -1 or pCaster.isNone():
		return szHelp
	pCity3 = CvEventInterface.getEventManager().cf.getAshenVeilCity(3)
	if pCity3 == -1:
		szHelp = CyTranslator().getText("TXT_KEY_PYHELP_HYBOREM_WHISPER_NO_CITIES", ())
	else:
		pCity2 = CvEventInterface.getEventManager().cf.getAshenVeilCity(2)
		pCity1 = CvEventInterface.getEventManager().cf.getAshenVeilCity(1)
		szHelp = CyTranslator().getText("TXT_KEY_PYHELP_HYBOREM_WHISPER", (pCity1.getName(),pCity2.getName(),pCity3.getName(),))
	return szHelp

def spellHyboremsWhisper(pCaster):
	iPlayer		= pCaster.getOwner()
	pCity1		= CvEventInterface.getEventManager().cf.getAshenVeilCity(1)
	pCity2		= CvEventInterface.getEventManager().cf.getAshenVeilCity(2)
	pCity3		= CvEventInterface.getEventManager().cf.getAshenVeilCity(3)
	pPlayer		= gc.getPlayer(iPlayer)
	if pPlayer.isHuman():
		popupInfo	= CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("passToModNetMessage")
		popupInfo.setData1(iPlayer)
		popupInfo.setData3(104) # onModNetMessage id
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_HYBOREMS_WHISPER", ()))
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity1.getName(),)), "")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity2.getName(),)), "")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_HYBOREMS_WHISPER_HELP", (pCity3.getName(),)), "")
		popupInfo.addPopup(iPlayer)
	else:
		AIPick = CyGame().getSorenRandNum(2700, "HyboremsWhisper AI pick") # Based on iAIValue of events
		if AIPick < 1000:
			pPlayer.acquireCity(pCity1,False,False)
		if AIPick >= 1000 and AIPick < 1800:
			pPlayer.acquireCity(pCity2,False,False)
		if AIPick >= 1800:
			pPlayer.acquireCity(pCity3,False,False)

def reqImpersonateLeader(caster):
	pCity = caster.plot().getPlotCity()
	if pCity.isBarbarian():
		return False
	if pCity.getOwner() == caster.getOwner():
		return False
	if gc.getPlayer(pCity.getOwner()).isHuman():
		return False
	return True

def spellImpersonateLeader(caster):
	pCity = caster.plot().getPlotCity()
	iNewPlayer = pCity.getOwner()
	iOldPlayer = caster.getOwner()
	iTimer = 5 + CyGame().getSorenRandNum(10, "Impersonate Leader")
	CyGame().reassignPlayerAdvanced(iOldPlayer, iNewPlayer, iTimer)

def helpImpersonateLeader(lpUnits, eSpell=1):
	szBuffer = ''
	pCaster = lpUnits[0]
	pPlot = pCaster.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		iNewPlayer = pCity.getOwner()
		if iNewPlayer != pCaster.getOwner():
			iMin = 5
			iMax = 14
			sPlayerName = gc.getPlayer(iNewPlayer).getName()
			szBuffer += CyTranslator().getText("TXT_KEY_HELP_SPELL_IMPERSONATE", (sPlayerName, iMin, iMax, ))
	return szBuffer


def reqInquisition(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	StateBelief = pPlayer.getStateReligion()
	if StateBelief == -1:
		if caster.getOwner() != pCity.getOwner():
			return False
	if (StateBelief != gc.getPlayer(pCity.getOwner()).getStateReligion()):
		return False
	if pPlayer.getCivics(getInfoType('CIVICOPTION_GOVERNMENT')) == getInfoType('CIVIC_THEOCRACY'):
		return False
	for iTarget in range(gc.getNumReligionInfos()):
		if (StateBelief != iTarget and pCity.isHasReligion(iTarget) and pCity.isHolyCityByType(iTarget) == False):
			return True
	return False

def reqInquisitionTheocracy(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	StateBelief = pPlayer.getStateReligion()
	if StateBelief == -1:
		if caster.getOwner() != pCity.getOwner():
			return False
	if (StateBelief != gc.getPlayer(pCity.getOwner()).getStateReligion()):
		return False
	for iTarget in range(gc.getNumReligionInfos()):
		if (StateBelief != iTarget and pCity.isHasReligion(iTarget) and pCity.isHolyCityByType(iTarget) == False):
			return True
	return False

def spellInquisition(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	StateBelief = gc.getPlayer(pCity.getOwner()).getStateReligion()
	iRnd = CyGame().getSorenRandNum(4, "Bob")
	if StateBelief == getInfoType('RELIGION_THE_ORDER'):
		iRnd = iRnd - 1
	for iTarget in range(gc.getNumReligionInfos()):
		if (not StateBelief == iTarget and pCity.isHasReligion(iTarget) and not pCity.isHolyCityByType(iTarget)):
			pCity.setHasReligion(iTarget, False, True, True)
			iRnd = iRnd + 1
			for i in range(gc.getNumBuildingInfos()):
				if gc.getBuildingInfo(i).getPrereqReligion() == iTarget:
					pCity.setNumRealBuilding(i, 0)
	if iRnd >= 1:
		pCity.changeHurryAngerTimer(iRnd)

# Scions start - Allows Inqusition to remove  Poisoned Words, Corrupt Guild.
	if pCity.getNumRealBuilding(getInfoType('BUILDING_POISON_WORDS')) > 0:
		pCity.setNumRealBuilding(getInfoType('BUILDING_POISON_WORDS'), 0)

	if pCity.getNumRealBuilding(getInfoType('BUILDING_CORRUPT_GUILD')) > 0:
		pCity.setNumRealBuilding(getInfoType('BUILDING_CORRUPT_GUILD'), 0)
# Scions end

def reqIntoTheMist(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getNumUnits() < 40:
			return False
	return True

def spellIntoTheMist(caster):
	iInvisible = getInfoType('PROMOTION_HIDDEN')
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		pUnit.setHasPromotion(iInvisible, True)

def reqIraUnleashed(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getUnitClassCount(getInfoType('UNITCLASS_IRA')) >= 4:
		return False
	return True

def spellIraUnleashed(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iCount = 4 - pPlayer.getUnitClassCount(getInfoType('UNITCLASS_IRA'))
	for i in range(iCount):
		pPlayer.initUnit(getInfoType('UNIT_IRA'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def reqKidnap(caster):
	pCity = caster.plot().getPlotCity()
	if pCity.getTeam() == caster.getTeam():
		return False
	i = 0
	i = i + pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_PRIEST'))
	i = i + pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_ARTIST'))
	i = i + pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_MERCHANT'))
	i = i + pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_ENGINEER'))
	i = i + pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_SCIENTIST'))
	i = i + pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_HEALER'))
	if i == 0:
		return False
	return True

def spellKidnap(caster):
	pCity = caster.plot().getPlotCity()
	if pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_PRIEST')) > 0:
		iUnit = getInfoType('UNIT_PROPHET')
		iSpec = getInfoType('SPECIALISTCLASS_GREAT_PRIEST')
	if pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_ARTIST')) > 0:
		iUnit = getInfoType('UNIT_ARTIST')
		iSpec = getInfoType('SPECIALISTCLASS_GREAT_ARTIST')
	if pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_HEALER')) > 0:
		iUnit = getInfoType('UNIT_HEALER')
		iSpec = getInfoType('SPECIALISTCLASS_GREAT_HEALER')
	if pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_MERCHANT')) > 0:
		iUnit = getInfoType('UNIT_MERCHANT')
		iSpec = getInfoType('SPECIALIST_GREAT_MERCHANT')
	if pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_ENGINEER')) > 0:
		iUnit = getInfoType('UNIT_ENGINEER')
		iSpec = getInfoType('SPECIALISTCLASS_GREAT_ENGINEER')
	if pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_GREAT_SCIENTIST')) > 0:
		iUnit = getInfoType('UNIT_SCIENTIST')
		iSpec = getInfoType('SPECIALISTCLASS_GREAT_SCIENTIST')
	iChance = caster.baseCombatStr() * 8
	if iChance > 95:
		iChance = 95
	pPlayer = gc.getPlayer(caster.getOwner())
	if CyGame().getSorenRandNum(100, "Kidnap") <= iChance:
		newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pCity.changeFreeSpecialistClassCount(iSpec, -1)
	else:
		if CyGame().getSorenRandNum(100, "Kidnap") <= 50:
			caster.setXY(pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), False, True, True,False)
		else:
			caster.kill(True, 0)
		startWar(caster.getOwner(), pCity.getOwner(), WarPlanTypes.WARPLAN_TOTAL)

def reqLegends(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumCities() == 0:
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getNumCities() < 5:
			return False
	return True

def spellLegends(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	for pyCity in PyPlayer(iPlayer).getCityList() :
		pCity = pyCity.GetCy()
		pCity.changeCulture(iPlayer, 300, True)

def reqLichdom(caster):
	#if caster.getUnitClassType() == getInfoType('UNITCLASS_FLESH_GOLEM'):
		#return False
	if caster.isHasPromotion(getInfoType('PROMOTION_PUPPET')):
		return False
	if isWorldUnitClass(caster.getUnitClassType()):
		return False
	#pyPlayer = PyPlayer(caster.getOwner()) TODO REMOVE
	pPlayer = gc.getPlayer(caster.getOwner())
	return not pPlayer.isUnitClassMaxedOut(getInfoType('UNITCLASS_LICH'),0)

def reqMask(caster):
	if caster.isHiddenNationality():
		return False
	if caster.hasCargo():
		return False
	if caster.isCargo():
		return False
	if caster.getUnitCombatType()!=gc.getInfoTypeForString("UNITCOMBAT_RECON") and caster.getUnitCombatType()!=gc.getInfoTypeForString("UNITCOMBAT_ROGUE"):
		return False
	pGroup = caster.getGroup()
	if pGroup.isNone() == False:
		if pGroup.getNumUnits() > 1:
			return False
	return True

def reqJolly(caster):
	if caster.isHiddenNationality():
		return False
	if caster.hasCargo():
		return False
	if caster.isCargo():
		return False
	pGroup = caster.getGroup()
	if pGroup.isNone() == False:
		if pGroup.getNumUnits() > 1:
			return False
	return True

def reqMezmerizeAnimal(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iAnimal = gc.getPlayer(gc.getANIMAL_PLAYER())
	getPlot	= CyMap().plot
	iMonstrous = getInfoType('PROMOTION_MONSTROUS_CREATURE')
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getUnitCombatType() == getInfoType('UNITCOMBAT_ANIMAL'):
					if pUnit.getTeam() == iAnimal.getTeam():
						return True
					if pTeam.isAtWar(pUnit.getTeam()):
						return True
				if pPlayer.getCivilizationType() == Civ["Doviello"]:
					if pUnit.getUnitCombatType() == getInfoType('UNITCOMBAT_BEAST'):
						if not pUnit.isHasPromotion(iMonstrous): # block monstrous creatures
							if pUnit.getTeam() == iAnimal.getTeam():
								return True
							if pTeam.isAtWar(pUnit.getTeam()):
								return True
	return False

def spellMezmerizeAnimal(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iMonstrous = getInfoType('PROMOTION_MONSTROUS_CREATURE')
	iAnimal = gc.getPlayer(gc.getANIMAL_PLAYER())
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getUnitCombatType() == getInfoType('UNITCOMBAT_ANIMAL'):
					if pTeam.isAtWar(pUnit.getTeam()):
						if pUnit.isDelayedDeath() == False:
							if pUnit.isResisted(caster, getInfoType('SPELL_MEZMERIZE_ANIMAL')) == False:
								newUnit = pPlayer.initUnit(pUnit.getUnitType(), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.convert(pUnit)
					if pUnit.getTeam() == iAnimal.getTeam():
						if pUnit.isDelayedDeath() == False:
							if pUnit.isResisted(caster, getInfoType('SPELL_MEZMERIZE_ANIMAL')) == False:
								newUnit = pPlayer.initUnit(pUnit.getUnitType(), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.convert(pUnit)
				if pPlayer.getCivilizationType() == Civ["Doviello"]:
					if pUnit.getUnitCombatType() == getInfoType('UNITCOMBAT_BEAST'):
						if not pUnit.isHasPromotion(iMonstrous):
							if pTeam.isAtWar(pUnit.getTeam()):
								if pUnit.isDelayedDeath() == False:
									if pUnit.isResisted(caster, getInfoType('SPELL_MEZMERIZE_ANIMAL')) == False:
										newUnit = pPlayer.initUnit(pUnit.getUnitType(), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
										newUnit.convert(pUnit)
							if pUnit.getTeam() == iAnimal.getTeam():
								if pUnit.isDelayedDeath() == False:
									if pUnit.isResisted(caster, getInfoType('SPELL_MEZMERIZE_ANIMAL')) == False:
										newUnit = pPlayer.initUnit(pUnit.getUnitType(), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
										newUnit.convert(pUnit)

def reqConvertLairDoviello(pCaster): # Doviello spell to convert animal lairs (pacific cohabitation)
	pPlot           = pCaster.plot()
	#iPlotOwner      = pPlot.getOwner()
	iPlayer         = pCaster.getOwner()
	iImprovement    = pPlot.getImprovementType()
	iImprovementOwner = pPlot.getImprovementOwner()
	if iImprovementOwner != iPlayer:
		if pPlot.getImprovementType() in (Lair["Bear Den"],Lair["Lion Den"],Lair["Griffin Weyr"],Lair["Hippogriffin Weyr"],Lair["Spider Den"],Lair["Wolf Den"]):
			return True
	return False

def spellConvertLairDoviello(pCaster):
	pPlot           = pCaster.plot()
	iPlotOwner      = pPlot.getOwner()
	iPlayer         = pCaster.getOwner()
	iImprovement    = pPlot.getImprovementType()
	pPlot.clearCultureControl(iPlotOwner, iImprovement, 1)
	pPlot.setImprovementOwner(iPlayer)
	pPlot.addCultureControl(iPlayer, iImprovement, 1)

def reqMirror(caster):
	iPlayer = caster.getOwner()
	pPlot = caster.plot()
	if caster.isImmuneToMagic():
		return False
	if pPlot.isVisibleEnemyUnit(iPlayer):
		return False
	return True

def spellMirror(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(caster.getUnitType(), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	for iProm in range(gc.getNumPromotionInfos()):
		if (caster.isHasPromotion(iProm) and not gc.getPromotionInfo(iProm).isEquipment() and not gc.getPromotionInfo(iProm).isEffectProm()):
			iPromCount = caster.countHasPromotion(iProm)
			for i in xrange(iPromCount):
				newUnit.setHasPromotion(iProm, True)
		elif (gc.getPromotionInfo(iProm).isEquipment()): #Some units start with an equipment promotion. Such as Alazkan starting with mirror.
			iPromCount = newUnit.countHasPromotion(iProm)
			for i in xrange(iPromCount):
				newUnit.setHasPromotion(iProm, False)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ILLUSION'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_IMMORTAL'), False)
	if newUnit.isImmortal():
		newUnit.changeImmortal(-1)
	newUnit.setDamageReal(caster.getDamageReal(), caster.getOwner())
	newUnit.setLevel(caster.getLevel())
	newUnit.setExperienceTimes100(caster.getExperienceTimes100(), -1)
	if not caster.getUnitType() == getInfoType('UNIT_ALAZKAN'):
		newUnit.setUnitArtStyleType(caster.getUnitArtStyleType())
	newUnit.setHasCasted(True)
	newUnit.setDuration(1)

def reqPeace(caster):
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_CHANGING_WAR_PEACE):
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	if pTeam.getAtWarCount(True) == 0:
		return False
	return True

def spellPeace(caster):
	pTeam = gc.getTeam(gc.getPlayer(caster.getOwner()).getTeam())
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if (pPlayer.isAlive() and iPlayer != caster.getOwner() and not gc.getPlayer(iPlayer).isBarbarian()):
			i2Team = gc.getPlayer(iPlayer).getTeam()
			if pTeam.isAtWar(i2Team):
				pTeam.makePeace(i2Team)
	CyGame().changeGlobalCounter(-1 * (CyGame().getTrueGlobalCounter() / 2))

def reqPeaceSevenPines(caster):
	pPlot = caster.plot()
	if not pPlot.isPythonActive():
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	if pTeam.getAtWarCount(True) == 0:
		return False
	return True

def spellPeaceSevenPines(caster):
	pTeam = gc.getTeam(gc.getPlayer(caster.getOwner()).getTeam())
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if (pPlayer.isAlive() and iPlayer != caster.getOwner() and not gc.getPlayer(iPlayer).isBarbarian()):
			i2Team = gc.getPlayer(iPlayer).getTeam()
			if pTeam.isAtWar(i2Team):
				pTeam.makePeace(i2Team)
	CyGame().changeGlobalCounter(-1 * (CyGame().getTrueGlobalCounter() / 2))
	pPlot = caster.plot()
	pPlot.setPythonActive(False)

def reqPillarofFire(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	getPlot	= CyMap().plot
	iRange = 2 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			bEnemy = False
			bNeutral = False
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pTeam.isAtWar(pUnit.getTeam()):
					bEnemy = True
				else:
					bNeutral = True
			if (bEnemy and bNeutral == False):
				return True
	return False

def spellPillarofFire(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iBestValue = 0
	pBestPlot = -1
	getPlot	= CyMap().plot
	iRange = 2 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			bNeutral = False
			iValue = 0
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pTeam.isAtWar(pUnit.getTeam()):
					iValue += 5 * pUnit.baseCombatStr()
				else:
					bNeutral = True
			if (iValue > iBestValue and bNeutral == False):
				iBestValue = iValue
				pBestPlot = pPlot
	if pBestPlot != -1:
		for i in xrange(pBestPlot.getNumUnits()):
			pUnit = pBestPlot.getUnit(i)
			pUnit.doDamage(50, 75, caster, getInfoType('DAMAGE_FIRE'), True)
		if (pPlot.getFeatureType() == getInfoType('FEATURE_FOREST') or pPlot.getFeatureType() == getInfoType('FEATURE_JUNGLE')):
			bValid = True
			iImprovement = pPlot.getImprovementType()
			if iImprovement != -1 :
				if gc.getImprovementInfo(iImprovement).isPermanent():
					bValid = False
			if bValid:
				if CyGame().getSorenRandNum(100, "Flames Spread") <= gc.getDefineINT('FLAMES_SPREAD_CHANCE'):
					pPlot.setImprovementType(getInfoType('IMPROVEMENT_SMOKE'))
		CyEngine().triggerEffect(getInfoType('EFFECT_PILLAR_OF_FIRE'),pBestPlot.getPoint())


def reqMarchOfTheTrees(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		pTeam = gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) < 2:
			return False
	return True

def spellMarchOfTheTrees(caster):
	iTreant = getInfoType('UNIT_TREANT')
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	map	= CyMap()
	plotByIndex	= map.plotByIndex
	for i in xrange(map.numPlots()):
		pPlot = plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				if (pPlot.getFeatureType() == Feature["Forest"] or pPlot.getFeatureType() == Feature["Ancient Forest"]):
					newUnit = pPlayer.initUnit(iTreant, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit.setDuration(5)
					pPlot.setFeatureType(Feature["Forest New"],0)

def reqMotherLode(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_MINE')) < 10:
			return False
	return True

def spellMotherLode(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.changeGold(pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_MINE')) * 25)
	pPlayer.changeGold(pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_DWARVEN_MINE')) * 50)
	pPlayer.changeGold(pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_DWARVEN_SETTLEMENT')) * 75)
	pPlayer.changeGold(pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_DWARVEN_HALL')) * 100)
	pPlayer.changeGold(pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_DWARVEN_FORTRESS')) * 200)
	map	= CyMap()
	plotByIndex	= map.plotByIndex
	for i in xrange(map.numPlots()):
		pPlot = plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				if pPlot.isWater() == False:
					if pPlot.isPeak() == False:
						if pPlot.isHills() == False:
							if CyGame().getSorenRandNum(100, "Mother Lode") < 10:
								pPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)

def spellSlaveDrive(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iSlaveBuilding = getInfoType('BUILDING_SLAVE_PIT')

	for iCity in range(pPlayer.getNumCities()):
		pCity = pPlayer.getCity(iCity)
		pCity.setNumRealBuilding(iSlaveBuilding, 1)

def reqFoundWyvern(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iWyvernGuard = getInfoType('UNITCLASS_DRAGON_GUARDIAN')
	if pPlayer.getUnitClassCount(iWyvernGuard) >= 12:
		return True
	return False

def reqTravelLight(caster):
	pPlot = caster.plot()
	return not (pPlot.isCity() or caster.isHasPromotion(getInfoType('PROMOTION_LIGHT')))

def reqWakeMother(caster):
	pPlayer = gc.getPlayer(caster.getOwner())

	if pPlayer.getUnitClassCount(getInfoType('UNITCLASS_MOTHER_SPIDER')) > 0:
		return False

	pNest = pPlayer.getCapitalCity()
	iNestPop = pNest.getPopulation()
	if iNestPop >= 16:
		return True
	return False

def spellWakeMother(caster):
	iPlayer = caster.getOwner()
	iMother = getInfoType('UNIT_MOTHER_SPIDER')
	pPlayer = gc.getPlayer(iPlayer)
	pCity = pPlayer.getCapitalCity()
	motherUnit = pPlayer.initUnit(iMother, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def reqOpenChest(caster):
	if not caster.isGroupHead():
		return False
	return True

def spellOpenChest(caster):
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	bValid = True
	if CyGame().getWBMapScript():
		bValid = sf.openChest(caster, pPlot)
	if bValid:
		if CyGame().getSorenRandNum(100, "Open Chest") < 25:
			lTrapList = ['POISON', 'FIRE', 'SPORES']
			sTrap = lTrapList[CyGame().getSorenRandNum(len(lTrapList), "Pick Trap")-1]
			point = pPlot.getPoint()
			if sTrap == 'POISON':
				caster.setHasPromotion(getInfoType('PROMOTION_POISONED'), True)
				caster.doDamageNoCaster(25, 90, getInfoType('DAMAGE_POISON'), False)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TRAP_POISON", ()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Promotions/Poisoned.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			if sTrap == 'FIRE':
				caster.doDamageNoCaster(50, 90, getInfoType('DAMAGE_FIRE'), False)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TRAP_FIRE", ()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Spells/Ring of Flames.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
				CyEngine().triggerEffect(getInfoType('EFFECT_RING_OF_FLAMES'),point)
				CyAudioGame().Play3DSound("AS3D_SPELL_FIREBALL",point.x,point.y,point.z)
			if sTrap == 'SPORES':
				caster.changeImmobileTimer(3)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TRAP_SPORES", ()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Spells/Spores.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
				CyEngine().triggerEffect(getInfoType('EFFECT_SPORES'),point)
				CyAudioGame().Play3DSound("AS3D_SPELL_CONTAGION",point.x,point.y,point.z)

		lList = ['EMPTY', 'HIGH_GOLD', 'TECH']
		if pPlayer.canReceiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_HEALING_SALVE'), caster):
			lList += ['ITEM_HEALING_SALVE']
		if pPlayer.canReceiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_JADE_TORC'), caster):
			lList += ['ITEM_JADE_TORC']
		if pPlayer.canReceiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_POTION_OF_INVISIBILITY'), caster):
			lList += ['ITEM_POTION_OF_INVISIBILITY']
		if pPlayer.canReceiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_POTION_OF_RESTORATION'), caster):
			lList += ['ITEM_POTION_OF_RESTORATION']
		if pPlayer.canReceiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_ROD_OF_WINDS'), caster):
			lList += ['ITEM_ROD_OF_WINDS']
		if pPlayer.canReceiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_TIMOR_MASK'), caster):
			lList += ['ITEM_TIMOR_MASK']
		sGoody = lList[CyGame().getSorenRandNum(len(lList), "Pick Goody")-1]
		if sGoody == 'EMPTY':
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_TREASURE_EMPTY",()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Equipment/Treasure.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		if sGoody == 'HIGH_GOLD':
			pPlayer.receiveGoody(pPlot, getInfoType('GOODY_MARNOK_HIGH_GOLD'), caster)
		if sGoody == 'ITEM_HEALING_SALVE':
			pPlayer.receiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_HEALING_SALVE'), caster)
		if sGoody == 'ITEM_JADE_TORC':
			pPlayer.receiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_JADE_TORC'), caster)
		if sGoody == 'ITEM_POTION_OF_INVISIBILITY':
			pPlayer.receiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_POTION_OF_INVISIBILITY'), caster)
		if sGoody == 'ITEM_POTION_OF_RESTORATION':
			pPlayer.receiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_POTION_OF_RESTORATION'), caster)
		if sGoody == 'ITEM_ROD_OF_WINDS':
			pPlayer.receiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_ROD_OF_WINDS'), caster)
		if sGoody == 'ITEM_TIMOR_MASK':
			pPlayer.receiveGoody(pPlot, getInfoType('GOODY_EXPLORE_LAIR_ITEM_TIMOR_MASK'), caster)
		if sGoody == 'TECH':
			pPlayer.receiveGoody(pPlot, getInfoType('GOODY_MARNOK_TECH'), caster)
		pTreasure = -1
		iTreasure = getInfoType('EQUIPMENT_TREASURE')
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getUnitType() == iTreasure:
				pTreasure = pUnit
		pTreasure.kill(True, 0)

def reqPromoteSettlement(pCity):
	if not pCity.isSettlement():
		return False
	pPlayer = gc.getPlayer(pCity.getOwner())
	if pPlayer.getNumCities() - pPlayer.getNumSettlements() >= pPlayer.getMaxCities():
		return False
	if not pPlayer.isHuman():
		pNearestCity = gc.getMap().findCity(pCity.getX(), pCity.getY(), -1, pCity.getTeam(), False, False, -1, -1, pCity, True)
		if not pNearestCity.isNone():
			if (plotDistance(pCity.getX(), pCity.getY(), pNearestCity.getX(), pNearestCity.getY()) < 6):
				return False
	return True

def spellPromoteSettlement(pCity):
	pCity.setSettlement(False)

def reqRagingSeas(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		pTeam = gc.getTeam(pPlayer.getTeam())
		iArcane = getInfoType('UNITCLASS_ARCANE_BARGE')
		iCaravel = getInfoType('UNITCLASS_CARAVEL')
		iGalley = getInfoType('UNITCLASS_GALLEY')
		iFrigate = getInfoType('UNITCLASS_FRIGATE')
		iGalleon = getInfoType('UNITCLASS_GALLEON')
		iManOWar = getInfoType('UNITCLASS_MAN_O_WAR')
		iPrivateer = getInfoType('UNITCLASS_PRIVATEER')
		iQueenOfTheLine = getInfoType('UNITCLASS_QUEEN_OF_THE_LINE')
		iTrireme = getInfoType('UNITCLASS_TRIREME')
		for iPlayer2 in range(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			if pPlayer2.isAlive():
				iTeam2 = gc.getPlayer(iPlayer2).getTeam()
				if pTeam.isAtWar(iTeam2):
					iCount = pPlayer2.getUnitClassCount(iArcane)
					iCount += pPlayer2.getUnitClassCount(iCaravel)
					iCount += pPlayer2.getUnitClassCount(iGalley)
					iCount += pPlayer2.getUnitClassCount(iFrigate) * 2
					iCount += pPlayer2.getUnitClassCount(iGalleon) * 2
					iCount += pPlayer2.getUnitClassCount(iManOWar) * 3
					iCount += pPlayer2.getUnitClassCount(iPrivateer)
					iCount += pPlayer2.getUnitClassCount(iQueenOfTheLine) * 3
					iCount += pPlayer2.getUnitClassCount(iTrireme)
					if iCount > 10:
						return True
		return False
	return True

def spellRagingSeas(caster):
	iCold = getInfoType('DAMAGE_COLD')
	iFlames = getInfoType('FEATURE_FLAMES')
	iSmoke = getInfoType('IMPROVEMENT_SMOKE')
	iSpring = getInfoType('EFFECT_SPRING')
	for i in range (CyMap().numPlots()):
		beffect = False
		pPlot = CyMap().plotByIndex(i)
		if pPlot.isAdjacentToWater():
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getCivilizationType() != Civ["Lanun"]:
					pUnit.doDamageNoCaster(75, 100, iCold, False)
					beffect=True
			if pPlot.getImprovementType() != -1:
				if pPlot.getFeatureType() == iFlames:
					pPlot.setFeatureType(-1, 0)
					beffect=True
				if pPlot.getImprovementType() == iSmoke:
					pPlot.setImprovementType(-1)
					beffect=True
				else:
					if pPlot.isOwned():
						if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent() == False:
							if gc.getPlayer(pPlot.getOwner()).getCivilizationType() != Civ["Lanun"]:
								if CyGame().getSorenRandNum(100, "Raging Seas") <= 25:
									pPlot.setImprovementType(-1)
									beffect=True
			if pPlot.isVisibleToWatchingHuman() and beffect==True:
				CyEngine().triggerEffect(iSpring,pPlot.getPoint())

def spellRaiseSkeleton(caster):
	pPlot = caster.plot()
	if pPlot.getImprovementType() == getInfoType('IMPROVEMENT_GRAVEYARD'):
		pPlot.setImprovementType(-1)
		caster.cast(getInfoType('SPELL_RAISE_SKELETON'))
		caster.cast(getInfoType('SPELL_RAISE_SKELETON'))

def reqRally(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getCivics(getInfoType('CIVICOPTION_MEMBERSHIP')) != getInfoType('CIVIC_CRUSADE'):
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getNumCities() < 5:
			return False
	return True

def spellRally(caster):
	iOwner = caster.getOwner()
	pPlayer = gc.getPlayer(iOwner)
	iDemagog = getInfoType('UNIT_DEMAGOG')
	iTown = getInfoType('IMPROVEMENT_TOWN')
	iVillage = getInfoType('IMPROVEMENT_VILLAGE')
	iCount = 0
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getOwner() == iOwner:
			if pPlot.isCity():
				newUnit = pPlayer.initUnit(iDemagog, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pPlot.getImprovementType() == iTown:
				pPlot.setImprovementType(iVillage)
				newUnit = pPlayer.initUnit(iDemagog, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellReadTheGrimoire(caster):
	iRnd = CyGame().getSorenRandNum(100, "Read the Grimoire")
	if iRnd < 20:
		caster.cast(getInfoType('SPELL_SUMMON_SPECTRE'))
	if iRnd >= 20 and iRnd < 40:
		caster.setHasPromotion(getInfoType('PROMOTION_UNHOLY_TAINT'), True)
	if iRnd >= 40 and iRnd < 60:
		caster.cast(getInfoType('SPELL_WITHER'))
	if iRnd >= 60 and iRnd < 70:
		caster.cast(getInfoType('SPELL_SUMMON_PIT_BEAST'))
	if iRnd >= 70 and iRnd < 80:
		caster.cast(getInfoType('SPELL_BURNING_BLOOD'))
	if iRnd >= 80 and iRnd < 90:
		caster.setHasPromotion(getInfoType('PROMOTION_DEMON'), True)
	if iRnd >= 90:
		caster.kill(True, PlayerTypes.NO_PLAYER)

def reqRebuildBarnaxus(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pCityPlayer = gc.getPlayer(pCity.getOwner())
	if caster.getUnitType() == getInfoType('UNIT_BARNAXUS'):
		return False
	if pCityPlayer.getCivilizationType() != Civ["Luchuirp"]:
		return False
	return True

def spellRebuildBarnaxus(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pCityPlayer = gc.getPlayer(pCity.getOwner())
	newUnit = pCityPlayer.initUnit(getInfoType('UNIT_BARNAXUS'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.setDamage(75, caster.getOwner())
	newUnit.finishMoves()
	pCity.applyBuildEffects(newUnit)
	if pPlayer.getCivilizationType() != Civ["Luchuirp"]:
		pCityPlayer.AI_changeAttitudeExtra(iPlayer,2)

def reqRebuildMithrilGolem(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pCityPlayer = gc.getPlayer(pCity.getOwner())
	if caster.getUnitType() == getInfoType('UNIT_MITHRIL_GOLEM'):
		return False
		
		
	if pCityPlayer.getStateReligion() != getInfoType('RELIGION_RUNES_OF_KILMORPH'):
		return False
	return True

def spellRebuildMithrilGolem(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pCityPlayer = gc.getPlayer(pCity.getOwner())
	newUnit = pCityPlayer.initUnit(getInfoType('UNIT_MITHRIL_GOLEM'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.setDamage(75, caster.getOwner())
	newUnit.finishMoves()
	pCity.applyBuildEffects(newUnit)
	if iPlayer != pCity.getOwner():
		pCityPlayer.AI_changeAttitudeExtra(iPlayer,2)

def reqRebuildHive(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	iCityPlayer = pCity.getOwner()
	if caster.getUnitType() == getInfoType('UNIT_THE_HIVE'):
		return False
	if iCityPlayer!=iPlayer:
		return False
	return True

def spellRebuildHive(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pCityPlayer = gc.getPlayer(pCity.getOwner())
	newUnit = pCityPlayer.initUnit(getInfoType('UNIT_THE_HIVE'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.setDamage(75, caster.getOwner())
	newUnit.finishMoves()
	pCity.applyBuildEffects(newUnit)

def reqRebuildMechDragon(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	iCityPlayer = pCity.getOwner()
	if caster.getUnitType() == getInfoType('UNIT_MECH_DRAGON'):
		return False
	if iCityPlayer!=iPlayer:
		return False
	return True

def spellRebuildMechDragon(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pCityPlayer = gc.getPlayer(pCity.getOwner())
	newUnit = pCityPlayer.initUnit(getInfoType('UNIT_MECH_DRAGON'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.setDamage(75, caster.getOwner())
	newUnit.finishMoves()
	pCity.applyBuildEffects(newUnit)
	
def reqRebuildWarMachine(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pCityPlayer = gc.getPlayer(pCity.getOwner())
	if caster.getUnitType() == getInfoType('UNIT_WAR_MACHINE'):
		return False
	if pCityPlayer.getCivilizationType() != Civ["Doviello"]:
		return False
	return True

def spellRebuildWarMachine(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pCityPlayer = gc.getPlayer(pCity.getOwner())
	newUnit = pCityPlayer.initUnit(getInfoType('UNIT_WAR_MACHINE'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.setDamage(75, caster.getOwner())
	newUnit.finishMoves()
	pCity.applyBuildEffects(newUnit)
	if pPlayer.getCivilizationType() != Civ["Doviello"]:
		pCityPlayer.AI_changeAttitudeExtra(iPlayer,2)

def spellRecruit(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = gc.getTeam(pPlayer.getTeam())
	iLoop = (pCity.getPopulation() / 3) + 1
	if pPlayer.getStateReligion() == getInfoType('RELIGION_THE_ORDER'):
		iLoop = iLoop * 2
	for i in range(iLoop):
		iRnd = CyGame().getSorenRandNum(60, "Bob")
		iUnit = -1
		if iRnd <= 10:
			iUnit = getInfoType('UNITCLASS_SCOUT')
			if pTeam.isHasTech(getInfoType('TECH_HUNTING')):
				iUnit = getInfoType('UNITCLASS_HUNTER')
			if pTeam.isHasTech(getInfoType('TECH_ANIMAL_HANDLING')):
				iUnit = getInfoType('UNITCLASS_RANGER')
		elif iRnd <= 20:
			iUnit = getInfoType('UNITCLASS_SCOUT')
			if pTeam.isHasTech(getInfoType('TECH_HUNTING')):
				iUnit = getInfoType('UNITCLASS_HUNTER')
			if pTeam.isHasTech(getInfoType('TECH_POISONS')):
				iUnit = getInfoType('UNITCLASS_ASSASSIN')
		elif iRnd <= 30:
			iUnit = getInfoType('UNITCLASS_SCOUT')
			if pTeam.isHasTech(getInfoType('TECH_HORSEBACK_RIDING')):
				iUnit = getInfoType('UNITCLASS_HORSEMAN')
			if pTeam.isHasTech(getInfoType('TECH_STIRRUPS')):
				iUnit = getInfoType('UNITCLASS_HORSE_ARCHER')
		elif iRnd <= 40:
			iUnit = getInfoType('UNITCLASS_SCOUT')
			if pTeam.isHasTech(getInfoType('TECH_HORSEBACK_RIDING')):
				iUnit = getInfoType('UNITCLASS_HORSEMAN')
			if pTeam.isHasTech(getInfoType('TECH_TRADE')):
				iUnit = getInfoType('UNITCLASS_CHARIOT')
		elif iRnd <= 50:
			iUnit = getInfoType('UNITCLASS_WARRIOR')
			if pTeam.isHasTech(getInfoType('TECH_BRONZE_WORKING')):
				iUnit = getInfoType('UNITCLASS_AXEMAN')
			if pTeam.isHasTech(getInfoType('TECH_IRON_WORKING')):
				iUnit = getInfoType('UNITCLASS_CHAMPION')
		elif iRnd <= 60:
			iUnit = getInfoType('UNITCLASS_WARRIOR')
			if pTeam.isHasTech(getInfoType('TECH_ARCHERY')):
				iUnit = getInfoType('UNITCLASS_ARCHER')
			if pTeam.isHasTech(getInfoType('TECH_BOWYERS')):
				iUnit = getInfoType('UNITCLASS_LONGBOWMAN')
		if iUnit != -1:
			infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
			iUnit = infoCiv.getCivilizationUnits(iUnit)
			if iUnit != -1:
				newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)

	iPopLoss = -(iLoop / 5)
	pCity.changePopulation(iPopLoss)
	caster.setHasPromotion(getInfoType('PROMOTION_RECRUITER'), False)
#	if caster.getUnitType() != getInfoType('UNIT_DONAL'):
#		caster.kill(True, PlayerTypes.NO_PLAYER)


def reqWarpath(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getBuildingClassCount(getInfoType('BUILDINGCLASS_COUNCIL_OF_THE_WARCHIEF')) < 2:
			return False
	else:
		if pPlayer.getBuildingClassCount(getInfoType('BUILDINGCLASS_COUNCIL_OF_THE_WARCHIEF')) < 1:
			return False
	return True

def spellWarpath(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = gc.getTeam(pPlayer.getTeam())

	for iCity in range(pPlayer.getNumCities()):
		pCity = pPlayer.getCity(iCity)
		if pCity.getNumBuilding(getInfoType('BUILDING_COUNCIL_OF_THE_WARCHIEF')) == 1:
			iLoop = (pCity.getPopulation() / 3) + 3
			for i in range(iLoop):
				iRnd = CyGame().getSorenRandNum(60, "Bob")
				iUnit = -1
				if iRnd <= 10:
					iUnit = getInfoType('UNITCLASS_SCOUT')
					if pTeam.isHasTech(getInfoType('TECH_HUNTING')):
						iUnit = getInfoType('UNITCLASS_HUNTER')
					if pTeam.isHasTech(getInfoType('TECH_ANIMAL_HANDLING')):
						iUnit = getInfoType('UNITCLASS_RANGER')
				elif iRnd <= 20:
					iUnit = getInfoType('UNITCLASS_SCOUT')
					if pTeam.isHasTech(getInfoType('TECH_HUNTING')):
						iUnit = getInfoType('UNITCLASS_HUNTER')
					if pTeam.isHasTech(getInfoType('TECH_POISONS')):
						iUnit = getInfoType('UNITCLASS_ASSASSIN')
				elif iRnd <= 30:
					iUnit = getInfoType('UNITCLASS_SCOUT')
					if pTeam.isHasTech(getInfoType('TECH_HORSEBACK_RIDING')):
						iUnit = getInfoType('UNITCLASS_HORSEMAN')
					if pTeam.isHasTech(getInfoType('TECH_STIRRUPS')):
						iUnit = getInfoType('UNITCLASS_HORSE_ARCHER')
				elif iRnd <= 40:
					iUnit = getInfoType('UNITCLASS_SCOUT')
					if pTeam.isHasTech(getInfoType('TECH_HORSEBACK_RIDING')):
						iUnit = getInfoType('UNITCLASS_HORSEMAN')
					if pTeam.isHasTech(getInfoType('TECH_TRADE')):
						iUnit = getInfoType('UNITCLASS_CHARIOT')
				elif iRnd <= 50:
					iUnit = getInfoType('UNITCLASS_WARRIOR')
					if pTeam.isHasTech(getInfoType('TECH_BRONZE_WORKING')):
						iUnit = getInfoType('UNITCLASS_AXEMAN')
					if pTeam.isHasTech(getInfoType('TECH_IRON_WORKING')):
						iUnit = getInfoType('UNITCLASS_CHAMPION')
				elif iRnd <= 60:
					iUnit = getInfoType('UNITCLASS_WARRIOR')
					if pTeam.isHasTech(getInfoType('TECH_ARCHERY')):
						iUnit = getInfoType('UNITCLASS_ARCHER')
					if pTeam.isHasTech(getInfoType('TECH_BOWYERS')):
						iUnit = getInfoType('UNITCLASS_LONGBOWMAN')
				if iUnit != -1:
					infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
					iUnit = infoCiv.getCivilizationUnits(iUnit)
					if iUnit != -1:
						newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)


def reqRecruitMercenary(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		pPlot = caster.plot()
		if pPlayer.getCivilizationType() == Civ["Khazad"]:
			return False
		pTeam = gc.getTeam(pPlayer.getTeam())
		getPlot	= CyMap().plot
		iRange = 2
		for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
			pPlot = getPlot(x, y)
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				p2Player = gc.getPlayer(pUnit.getOwner())
				e2Team = p2Player.getTeam()
				if pTeam.isAtWar(e2Team) == True:
					return True
		return False
	return True

def spellRecruitMercenary(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iUnit = getInfoType('UNITCLASS_CHAMPION')
	infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iUnit = infoCiv.getCivilizationUnits(iUnit)
	newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.finishMoves()
	newUnit.setHasCasted(True)
	newUnit.setHasPromotion(Race["Undead"], False)
	if caster.getUnitType() == getInfoType('UNIT_MAGNADINE'):
		newUnit.setHasPromotion(getInfoType('PROMOTION_LOYALTY'), True)

def spellReleaseFromCage(caster):
	pPlot = caster.plot()
	pPlot.setImprovementType(-1)

def reqReligiousFervor(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iReligion = pPlayer.getStateReligion()
	if iReligion == -1:
		return False
	if pPlayer.isHuman() == False:
		iCount = 0
		for pyCity in PyPlayer(iPlayer).getCityList() :
			pCity = pyCity.GetCy()
			if pCity.isHasReligion(iReligion):
				iCount += 1
		if iCount < 5:
			return False
	return True

def spellReligiousFervor(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iReligion = pPlayer.getStateReligion()
	if iReligion == getInfoType('RELIGION_FELLOWSHIP_OF_LEAVES'):
		iUnit = getInfoType('UNIT_PRIEST_OF_LEAVES')
	elif iReligion == getInfoType('RELIGION_RUNES_OF_KILMORPH'):
		iUnit = getInfoType('UNIT_PRIEST_OF_KILMORPH')
	elif iReligion == getInfoType('RELIGION_THE_EMPYREAN'):
		iUnit = getInfoType('UNIT_PRIEST_OF_THE_EMPYREAN')
	elif iReligion == getInfoType('RELIGION_THE_ORDER'):
		iUnit = getInfoType('UNIT_PRIEST_OF_THE_ORDER')
	elif iReligion == getInfoType('RELIGION_OCTOPUS_OVERLORDS'):
		iUnit = getInfoType('UNIT_PRIEST_OF_THE_OVERLORDS')
	elif iReligion == getInfoType('RELIGION_THE_ASHEN_VEIL'):
		iUnit = getInfoType('UNIT_PRIEST_OF_THE_VEIL')
	elif iReligion == getInfoType('RELIGION_COUNCIL_OF_ESUS'):
		iUnit = getInfoType('UNIT_ASSASSIN')
	elif iReligion == getInfoType('RELIGION_WHITE_HAND'):
		iUnit = getInfoType('UNIT_PRIEST_OF_WINTER')
	iCount = 0
	for pyCity in PyPlayer(iPlayer).getCityList() :
		pCity = pyCity.GetCy()
		if pCity.isHasReligion(iReligion):
			iCount += 1
	for pyCity in PyPlayer(iPlayer).getCityList() :
		pCity = pyCity.GetCy()
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.changeExperience(iCount, -1, False, False, False)
		newUnit.setReligion(iReligion)

def reqRepair(caster):
	pPlot = caster.plot()
	iGolem = Race["Golem"]
	iNaval = UnitCombat["Naval"]
	iSiege = UnitCombat["Siege"]
	iHiddenNationality = getInfoType('PROMOTION_HIDDEN_NATIONALITY')

	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.getUnitCombatType() == iSiege or pUnit.getUnitCombatType() == iNaval or pUnit.isHasPromotion(iGolem)):
			if pUnit.isHurt() > 0 and not pUnit.isHasPromotion(iHiddenNationality) :
				return True
	return False

def spellRepair(caster,amount):
	pPlot = caster.plot()
	iGolem = getInfoType('PROMOTION_GOLEM')
	iNaval = getInfoType('UNITCOMBAT_NAVAL')
	iSiege = getInfoType('UNITCOMBAT_SIEGE')
	iHiddenNationality = getInfoType('PROMOTION_HIDDEN_NATIONALITY')

	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.getUnitCombatType() == iSiege or pUnit.getUnitCombatType() == iNaval or pUnit.isHasPromotion(iGolem)):
			if not pUnit.isHasPromotion(iHiddenNationality):
				pUnit.changeDamage(-amount,0)

def reqAccelerate(caster):
	pPlot = caster.plot()
	iGolem = getInfoType('PROMOTION_GOLEM')
	iSiege = getInfoType('UNITCOMBAT_SIEGE')
	iAccelerated = getInfoType('PROMOTION_ACCELERATED')

	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.getUnitCombatType() == iSiege or pUnit.isHasPromotion(iGolem)):
			if not pUnit.isHasPromotion(iAccelerated):
				return True
	return False

def spellAccelerate(caster):
	pPlot = caster.plot()
	iGolem = getInfoType('PROMOTION_GOLEM')
	iSiege = getInfoType('UNITCOMBAT_SIEGE')
	iAccelerated = getInfoType('PROMOTION_ACCELERATED')

	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.getUnitCombatType() == iSiege or pUnit.isHasPromotion(iGolem)):
			pUnit.setHasPromotion(iAccelerated, True)


def reqResurrection(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iHero = CvEventInterface.getEventManager().cf.getHero(pPlayer)
	if iHero == -1:
		return False
	if not CyGame().isUnitClassMaxedOut(iHero, 0):
		return False
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.getUnitClassCount(iHero) > 0:
			return False
	py = PyPlayer(caster.getOwner())
	iSpell = getInfoType('SPELL_RESURRECTION')
	for pUnit in py.getUnitList():
		if pUnit.getDelayedSpell() == iSpell:
			return False
# Scions start - Hopefully prevents innapropriate Korrina resurrections.
	if pPlayer.getUnitClassCount(getInfoType('UNITCLASS_KORRINA_BLACK_LADY')) > 0:
		return False
	if pPlayer.getUnitClassCount(getInfoType('UNITCLASS_KORRINA_RED_LADY')) > 0:
		return False
	if pPlayer.getUnitClassCount(getInfoType('UNITCLASS_KORRINA')) > 0:
		return False
# Scions end
	return True

def spellResurrection(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	iHero = CvEventInterface.getEventManager().cf.getHero(pPlayer)
	infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iUnit = infoCiv.getCivilizationUnits(iHero)
	iBarn = getInfoType('EQUIPMENT_PIECES_OF_BARNAXUS')
	iBarnProm = getInfoType('PROMOTION_PIECES_OF_BARNAXUS')
	if iUnit == getInfoType('UNIT_BARNAXUS'):
		for iPlayer2 in range(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			if pPlayer2.isAlive():
				py = PyPlayer(iPlayer2)
				for pUnit in py.getUnitList():
					if pUnit.isHasPromotion(iBarnProm):
						pUnit.setHasPromotion(iBarnProm, False)
						CyInterface().addMessage(iPlayer2,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PIECES_LOST", ()),'AS2D_CHARM_PERSON',1,'Art/Interface/Buttons/Units/Barnaxus.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
					if pUnit.getUnitType() == iBarn:
						CyInterface().addMessage(iPlayer2,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PIECES_LOST", ()),'AS2D_CHARM_PERSON',1,'Art/Interface/Buttons/Units/Barnaxus.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
	iCreated = gc.getGame().getUnitClassCreatedCount(iHero)
	for iClear in range(iCreated):
		gc.getGame().decrementUnitClassCreatedCount(iHero)
	newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	for iProm in range(gc.getNumPromotionInfos()):
		if (caster.isHasPromotion(iProm) and not gc.getPromotionInfo(iProm).isEquipment()):
			iPromCount = caster.countHasPromotion(iProm)
			for i in xrange(iPromCount):
				newUnit.setHasPromotion(iProm, True)

def spellResurrectionGraveyard(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iUnit = infoCiv.getCivilizationUnits(getInfoType('UNITCLASS_CHAMPION'))
	if iUnit == -1:
		iUnit = getInfoType('UNIT_CHAMPION')
	newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.changeExperience(CyGame().getSorenRandNum(30, "Resurrection Graveyard"), -1, False, False, False)
	pPlot.setImprovementType(-1)

def reqRevelry(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	#if pPlayer.isGoldenAge():
	#	return False
	if pPlayer.isHuman() == False:
		if pPlayer.getTotalPopulation() < 25:
			return False
	return True

def spellRevelry(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength() * 2)
	for iPlayer2 in range(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if iPlayer2 != iPlayer and pPlayer2.isAlive():
			for iCity in range(pPlayer2.getNumCities()):
				pCity = pPlayer2.getCity(iCity)
				pPlot = pCity.plot()
				if pPlot is not None and not pPlot.isNone():
					iCulture = 0
					for iPlayer3 in xrange(gc.getMAX_PLAYERS()):
						if iPlayer3 != iPlayer:
							iCulture = iCulture + pPlot.getCulture(iPlayer3)
							if iPlayer3 != pCity.getOwner() :
								pPlot.setCulture(iPlayer3,0,True)
						
					pPlot.setCulture(iPlayer,iCulture,True)
				
				
def reqRevelation(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	iHidden = getInfoType('PROMOTION_HIDDEN')
	iHiddenNationality = getInfoType('PROMOTION_HIDDEN_NATIONALITY')
	iIllusion = getInfoType('PROMOTION_ILLUSION')
	iInvisible = getInfoType('PROMOTION_INVISIBLE')
	getPlot	= CyMap().plot
	iRange = 3 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			for iUnit in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(iUnit)
				if pUnit.getTeam() != iTeam:
					if pUnit.isHasPromotion(iHidden):
						return True
					if pUnit.isHasPromotion(iHiddenNationality):
						return True
					if pUnit.isHasPromotion(iInvisible):
						return True
					if pUnit.isHasPromotion(iIllusion):
						return True
	return False

def spellRevelation(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	iHidden = getInfoType('PROMOTION_HIDDEN')
	iHiddenNationality = getInfoType('PROMOTION_HIDDEN_NATIONALITY')
	iIllusion = getInfoType('PROMOTION_ILLUSION')
	iInvisible = getInfoType('PROMOTION_INVISIBLE')
	getPlot	= CyMap().plot
	iRange = 3 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			for iUnit in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(iUnit)
				if pUnit.getTeam() != iTeam:
					if pUnit.isHasPromotion(iHidden):
						pUnit.setHasPromotion(iHidden, False)
					if pUnit.isHasPromotion(iHiddenNationality):
						pUnit.setHasPromotion(iHiddenNationality, False)
					if pUnit.isHasPromotion(iInvisible):
						pUnit.setHasPromotion(iInvisible, False)
					if pUnit.isHasPromotion(iIllusion):
						pUnit.kill(True, caster.getOwner())

def spellRingofFlames(caster):
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		bValid = True
		if pPlot.getImprovementType() != -1:
			if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent():
				bValid = False
		if bValid:
			if (pPlot.getFeatureType() == getInfoType('FEATURE_FOREST') or pPlot.getFeatureType() == getInfoType('FEATURE_JUNGLE') or pPlot.getFeatureType() == getInfoType('FEATURE_FOREST_NEW')):
				if CyGame().getSorenRandNum(100, "Flames Spread") <= gc.getDefineINT('FLAMES_SPREAD_CHANCE'):
					pPlot.setImprovementType(getInfoType('IMPROVEMENT_SMOKE'))

def reqRiverOfBlood(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumCities() == 0:
		return False
	if not pPlayer.isHuman():
		if pPlayer.getNumCities() < 5:
			return False
	return True

def spellRiverOfBlood(pCaster):
	iPlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iTeam   = pPlayer.getTeam()
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			iLoopTeam   = pLoopPlayer.getTeam()
			iLoopCiv    = pLoopPlayer.getCivilizationType()
			if iLoopPlayer == iPlayer: # if current player, pop+2
				for iCity in range(pPlayer.getNumCities()):
					pCity = pPlayer.getCity(iCity)
					pCity.changePopulation(2)
					CyInterface().addMessage(iLoopPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RIVER_OF_BLOOD_CALABIM", ()),'',1,'Art/Interface/Buttons/Spells/River of Blood.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
			elif (iLoopTeam != iTeam) and (iLoopCiv not in [Civ["Scions"],Civ["D'Tesh"],Civ["Infernal"]]): # if not immune (player's team or special civilization), lose 2 pop (lose 1 if pop is 2)
				for iCity in range(pLoopPlayer.getNumCities()):
					pCity = pLoopPlayer.getCity(iCity)
					if pCity.getPopulation() > 1:
						if pCity.getPopulation() > 2:
							iLoss = -2
						else:
							iLoss = -1
						pCity.changePopulation(iLoss)
						CyInterface().addMessage(iLoopPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RIVER_OF_BLOOD", (iLoss, )),'',1,'Art/Interface/Buttons/Spells/River of Blood.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)

def reqRoar(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = gc.getTeam(pPlayer.getTeam())
	iTarget = -1
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if not pUnit.isImmuneToFear():
				p2Player = gc.getPlayer(pUnit.getOwner())
				e2Team = p2Player.getTeam()
				if pTeam.isAtWar(e2Team) == True:
					return True
	return False

def spellRoar(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pTeam = gc.getTeam(pPlayer.getTeam())
	pPlot = caster.plot()
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pLoopPlot = getPlot(x, y)
		if not pLoopPlot.isNone():
			for i in range(pLoopPlot.getNumUnits() -1, -1, -1):
				pUnit = pLoopPlot.getUnit(i)
				p2Player = gc.getPlayer(pUnit.getOwner())
				i2Team = p2Player.getTeam()
				if pTeam.isAtWar(i2Team):
					if doFear(pUnit, pPlot, caster, True):
						CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_FEAR", (gc.getUnitInfo(pUnit.getUnitType()).getDescription(), )),'',1,'Art/Interface/Buttons/Spells/Roar.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
						CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_FEAR_ENEMY", (gc.getUnitInfo(pUnit.getUnitType()).getDescription(), )),'',1,'Art/Interface/Buttons/Spells/Roar.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)

def reqRobGrave(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		if pPlayer.getAlignment() == getInfoType('ALIGNMENT_GOOD') or pPlayer.isBarbarian():
			return False
	return True

def spellRobGrave(caster):
	CyGame().changeGlobalCounter(1)
	pPlot = caster.plot()
	pPlot.setImprovementType(-1)
	pPlayer = gc.getPlayer(caster.getOwner())
	lList = ['LOW_GOLD', 'HIGH_GOLD']
	if pPlayer.canReceiveGoody(pPlot, getInfoType('GOODY_GRAVE_SPECTRE'), caster):
		lList += ['SPAWN_SPECTRE']
	if pPlayer.canReceiveGoody(pPlot, getInfoType('GOODY_GRAVE_SKELETONS'), caster):
		lList += ['SPAWN_SKELETONS']
	if pPlayer.canReceiveGoody(pPlot, getInfoType('GOODY_GRAVE_TECH'), caster):
		lList = lList + ['TECH']
	sGoody = lList[CyGame().getSorenRandNum(len(lList), "Pick Goody")-1]
	if sGoody == 'LOW_GOLD':
		pPlayer.receiveGoody(pPlot, getInfoType('GOODY_GRAVE_LOW_GOLD'), caster)
	if sGoody == 'HIGH_GOLD':
		pPlayer.receiveGoody(pPlot, getInfoType('GOODY_GRAVE_HIGH_GOLD'), caster)
	if sGoody == 'TECH':
		pPlayer.receiveGoody(pPlot, getInfoType('GOODY_GRAVE_TECH'), caster)
	if sGoody == 'SPAWN_SKELETONS':
		pPlayer.receiveGoody(pPlot, getInfoType('GOODY_GRAVE_SKELETONS'), caster)
	if sGoody == 'SPAWN_SPECTRE':
		pPlayer.receiveGoody(pPlot, getInfoType('GOODY_GRAVE_SPECTRE'), caster)

def spellSacrificeAltar(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	pTeam = gc.getTeam(pPlayer.getTeam())
	iTech = pPlayer.getCurrentResearch()
	iNum = 10 + (caster.getLevel() * caster.getLevel())
	pTeam.changeResearchProgress(iTech, iNum, caster.getOwner())

def spellSacrificePyre(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	caster.cast(getInfoType('SPELL_RING_OF_FLAMES'))
	iCount = 1
	if caster.isImmortal():
		caster.changeImmortal(-10)
	if isWorldUnitClass(caster.getUnitClassType()):
		iCount = 7
	for i in range(iCount):
		newUnit = pPlayer.initUnit(getInfoType('UNIT_FIRE_ELEMENTAL'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		#Should we make this assign the units to the same Master as the original unit had?
		newUnit.setDuration(caster.getDuration())


def spellSacrificeCualli(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	pTeam = gc.getTeam(pPlayer.getTeam())
	iLevel = caster.getLevel()
	iPriest = getInfoType('UNIT_LIZARD_PRIEST_OF_AGRUONN')
	iShadowPriest = getInfoType('UNIT_SHADOW_PRIEST_OF_AGRUONN')
	iHeroPriest = getInfoType('UNIT_MIQUIZTLI')
	bPriest = caster.getUnitType() == iPriest or caster.getUnitType() == iShadowPriest or caster.getUnitType() == iHeroPriest
	bBrigit = caster.getUnitType()==getInfoType('UNIT_BRIGIT')
	bOdio = caster.getUnitType()== getInfoType('UNIT_ODIO')
	bSauros = pPlayer.getLeaderType()==getInfoType("LEADER_SAUROS")
	
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		
		if pUnit.getUnitCombatType()==getInfoType("UNITCOMBAT_DISCIPLE"):
			iEmpower1 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_1')
			iEmpower2 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_2')
			iEmpower3 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_3')
			iEmpower4 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_4')
			iEmpower5 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_5')
			iEmpower6 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_6')
			iEmpower7 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_7')
			iEmpower8 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_8')
			iEmpowerPriest = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_PRIEST')
			iEmpowerDivine = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_DIVINE')
			iEmpowerFire = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_FIRE')
			pUnit.setHasPromotion(iEmpower1, True)
			if(iLevel>2):
				pUnit.setHasPromotion(iEmpower2, True)
			if(iLevel>3):
				pUnit.setHasPromotion(iEmpower3, True)
			if(iLevel>5):
				pUnit.setHasPromotion(iEmpower4, True)
			if(iLevel>7):
				pUnit.setHasPromotion(iEmpower5, True)
			if(iLevel>9):
				pUnit.setHasPromotion(iEmpower6, True)
			if(iLevel>11):
				pUnit.setHasPromotion(iEmpower7, True)
			if(iLevel>14):
				pUnit.setHasPromotion(iEmpower8, True)
			if(bPriest):
				pUnit.setHasPromotion(iEmpowerPriest, True)
			if(bOdio):
				pUnit.setHasPromotion(iEmpowerDivine, True)
			if(bBrigit and bSauros):
				pUnit.setHasPromotion(iEmpowerFire,True)

	return

def reqSacrificeCualli(caster):
	pPlot = caster.plot()
	iPriest = getInfoType('UNIT_LIZARD_PRIEST_OF_AGRUONN')
	iShadowPriest = getInfoType('UNIT_SHADOW_PRIEST_OF_AGRUONN')
	iHeroPriest = getInfoType('UNIT_MIQUIZTLI')
	if (not caster.getUnitType() == iShadowPriest) and (not caster.getUnitType()== iHeroPriest) and (not caster.getUnitType()==iPriest) and (not(caster.getUnitType()==getInfoType('UNIT_BRIGIT'))) and (not (caster.getUnitType()== getInfoType('UNIT_ODIO'))) :
		return False	
	return True	

def reqSacrificeSlaveCualli(caster):
	pPlot = caster.plot()
	iShadowPriest = getInfoType('UNIT_SHADOW_PRIEST_OF_AGRUONN')
	iHeroPriest = getInfoType('UNIT_MIQUIZTLI')
	if (not caster.getUnitType() == iShadowPriest) and (not caster.getUnitType()== iHeroPriest):
		return False

	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == getInfoType('UNIT_SLAVE'):
			return True

	return False

def spellSacrificeSlaveCualli(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	pTeam = gc.getTeam(pPlayer.getTeam())
	iLevel = 0
	iPriest = getInfoType('UNIT_LIZARD_PRIEST_OF_AGRUONN')
	iShadowPriest = getInfoType('UNIT_SHADOW_PRIEST_OF_AGRUONN')
	iHeroPriest = getInfoType('UNIT_MIQUIZTLI')
	bPriest = caster.getUnitType() == iPriest or caster.getUnitType() == iShadowPriest or caster.getUnitType() == iHeroPriest
	
	bOdio = caster.getUnitType()== getInfoType('UNIT_ODIO')
	bBrigit = caster.getUnitType()==getInfoType('UNIT_BRIGIT')
	bSauros = pPlayer.getLeaderType()==getInfoType("LEADER_SAUROS")

	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == getInfoType('UNIT_SLAVE'):
			iLevel=iLevel+1
			pUnit.kill(True,caster.getOwner())
	iLevel=(iLevel*2)/3
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)

		if pUnit.getUnitCombatType()==getInfoType("UNITCOMBAT_DISCIPLE"):
			iEmpower1 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_1')
			iEmpower2 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_2')
			iEmpower3 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_3')
			iEmpower4 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_4')
			iEmpower5 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_5')
			iEmpower6 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_6')
			iEmpower7 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_7')
			iEmpower8 = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_8')
			iEmpowerPriest = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_PRIEST')
			iEmpowerDivine = getInfoType('PROMOTION_SACRIFICIAL_BLOOD_DIVINE')
			pUnit.setHasPromotion(iEmpower1, True)
			if(iLevel>2):
				pUnit.setHasPromotion(iEmpower2, True)
			if(iLevel>3):
				pUnit.setHasPromotion(iEmpower3, True)
			if(iLevel>5):
				pUnit.setHasPromotion(iEmpower4, True)
			if(iLevel>7):
				pUnit.setHasPromotion(iEmpower5, True)
			if(iLevel>9):
				pUnit.setHasPromotion(iEmpower6, True)
			if(iLevel>11):
				pUnit.setHasPromotion(iEmpower7, True)
			if(iLevel>14):
				pUnit.setHasPromotion(iEmpower8, True)
			if(bPriest):
				pUnit.setHasPromotion(iEmpowerPriest, True)
			if(bOdio):
				pUnit.setHasPromotion(iEmpowerDivine, True)
			if(bBrigit and bSauros):
				pUnit.setHasPromotion(iEmpowerFire,True)

	return
			

def reqSacrifice(caster):
	if caster.getFoodSacrifice()==0 and caster.getBeakerSacrifice()==0 and	caster.getCultureSacrifice()==0 and	caster.getGoldSacrifice()==0:
		return False
	return True	

def spellSacrifice(caster):
	pPlot=caster.plot()
	pCity=pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = gc.getTeam(pPlayer.getTeam())
	
	if(caster.getFoodSacrifice()!=0):
		pCity.changeFood(caster.getFoodSacrifice())
	if(caster.getBeakerSacrifice()!=0):
		iTech = pPlayer.getCurrentResearch()
		pTeam.changeResearchProgress(iTech, caster.getBeakerSacrifice(), caster.getOwner())
	if(caster.getCultureSacrifice()!=0):
		pCity.changeCulture(caster.getOwner(),caster.getCultureSacrifice(),True)
	if(caster.getGoldSacrifice()!=0):
		pPlayer.changeGold(caster.getGoldSacrifice())

def reqPurify(caster):
	pPlot = caster.plot()
	if reqSanctify(caster):
		return True

	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.isHasPromotion(getInfoType('PROMOTION_DISEASED')):
			return True

	return False


def reqSanctify(caster):
	pPlot = caster.plot()
	bValid = False
	if pPlot.getImprovementType() == getInfoType('IMPROVEMENT_CITY_RUINS'):
		return True
	if pPlot.getImprovementType() == getInfoType('IMPROVEMENT_CITY_RUINS_ANCIENT'):
		return True
	if pPlot.getImprovementType() == getInfoType('IMPROVEMENT_GRAVEYARD'):
		return True
	if pPlot.getImprovementType() == getInfoType('IMPROVEMENT_SNAKE_PILLAR'):
		return True
	if pPlot.getImprovementType() == getInfoType('IMPROVEMENT_AERON_VAULTGATE'):
		return True
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_PLOT_COUNTER):
		lValidTerrains = [
			Terrain["Broken lands"],
			Terrain["Burning sands"],
			Terrain["Fields of perdition"],
			Terrain["Shallows"],
			Terrain["Blackwater"],
			Terrain["Blighted coast"]
		]
		for x,y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
			pPlot = getPlot(x,y)
			if not pPlot.isNone():
				if pPlot.getTerrainType() in lValidTerrains:
					bValid = True
					break
	else:
		for x,y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
			pPlot = getPlot(x,y)
			if not pPlot.isNone():
				if pPlot.getPlotCounter() > gc.getDefineINT('PLOT_COUNTER_HELL_THRESHOLD'):
					bValid = True
					break
	if bValid == False:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		if caster.getOwner() != pPlot.getOwner():
			return False
		if pPlayer.getCivilizationType() == Civ["Infernal"]:
			return False
	return True

def sanctifyResource(pPlot):
	iBonus = pPlot.getBonusType(-1)
	setBonus = pPlot.setBonusType
	randNum = CyGame().getSorenRandNum
	iImprovement = pPlot.getImprovementType()
	chance = randNum(100, "Hell Convert")
	
        if iBonus == Bonus["Toad"]:
                if chance < 25: setBonus(Bonus["Sheep"])
                elif chance < 50: setBonus(Bonus["Pig"])
                elif chance < 75: setBonus(Bonus["Fur"])
                else: setBonus(Bonus["Deer"])
        if iBonus == Bonus["Nightmare"]:
                if chance < 20: setBonus(Bonus["Horse"])
                elif chance < 40: setBonus(Bonus["Hyapon"])
                elif chance < 60: setBonus(Bonus["Ivory"])
                elif chance < 80: setBonus(Bonus["Cow"])
                else: setBonus(Bonus["Camel"])
        if iBonus == getInfoType('BONUS_JETEYE'):
                if chance < 34: setBonus(Bonus["Fish"])
                elif chance < 66: setBonus(Bonus["Shrimp"])
                else: setBonus(getInfoType('BONUS_WHALE'))
        if iBonus == getInfoType('BONUS_BLEEDING_GOD_WINE'):
                if chance < 34: setBonus(Bonus["Clam"])
                elif chance < 66: setBonus(Bonus["Pearl"])
                else: setBonus(Bonus["Crab"])
        if iBonus == Bonus["Razorweed"]:
                if chance < 34: setBonus(Bonus["Cotton"])
                elif chance < 66: setBonus(Bonus["Silk"])
                else: setBonus(Bonus["Wine"])
	if iBonus == Bonus["Gulagarm"]:
		if randNum(100, "Hell Convert") < 50: setBonus(Bonus["Banana"])
		else: setBonus(Bonus["Sugar"])
	if (iBonus == Bonus["Sheut"]): setBonus(Bonus["Marble"])
	if iImprovement == Improvement["Snake Pillar"]:
		pPlot.setImprovementType(-1)
		iCount = randNum(100, "Hell Convert")
		if iCount < 33: setBonus(Bonus["Corn"])
		else:
			if iCount < 66: setBonus(Bonus["Rice"])
			else: setBonus(Bonus["Wheat"])

def spellSanctify(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	iImprovement = pPlot.getImprovementType()
        iCrossroad = getInfoType('UNIT_DEVILCASTER')
	if iImprovement == getInfoType('IMPROVEMENT_AERON_VAULTGATE'):
		pPlot.setImprovementType(-1)
		pPlot.setBonusType(-1)
		pPlayer.changeGlobalCounterContrib(-1)
                for x,y in plotsInRange( caster.getX(), caster.getY(), iRange ):
                        pPlot = getPlot(x,y)
                        if not pPlot.isNone():
                                for i in xrange(pPlot.getNumUnits()):
                                        pUnit = pPlot.getUnit(i)
                                        if pUnit.getUnitType() == iCrossroad:
                                                pUnit.kill(True,0)

	if pPlot.getImprovementType() == Improvement["City Ruins"] or pPlot.getImprovementType() == getInfoType('IMPROVEMENT_CITY_RUINS_ANCIENT') :
		pPlot.setImprovementType(-1)
		pPlayer.changeGlobalCounterContrib(-1)
	if pPlot.getImprovementType() == Lair["Graveyard"]:
		pPlot.setImprovementType(-1)
		pPlayer.changeGlobalCounterContrib(-1)
		if pPlayer.isHasTech(getInfoType('TECH_DIVINATION')):
			newUnit = pPlayer.initUnit(getInfoType('UNIT_TOMB_WARDEN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			newUnit = pPlayer.initUnit(getInfoType('UNIT_SPEARMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(getInfoType('PROMOTION_ANGEL'), True)
			newUnit.setHasPromotion(getInfoType('PROMOTION_MEDIC1'), True)

	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_PLOT_COUNTER):
		for x,y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
			bSwapped = False
			pPlot = getPlot(x,y)
			if not pPlot.isNone():
				iTerrain = pPlot.getTerrainType()
				if iTerrain == Terrain["Blackwater"]:
					pPlot.setTerrainType(Terrain["Ocean"], False, False)
					bSwapped = True
				if iTerrain == Terrain["Blighted coast"]:
					bSwapped = True
					pPlot.setTerrainType(Terrain["Coast"], False, False)
					bSwapped = True
				if iTerrain == Terrain["Broken lands"]:
					pPlot.setTerrainType(Terrain["Grass"], False, False)
					bSwapped = True
				if iTerrain == Terrain["Burning sands"]:
					pPlot.setTerrainType(Terrain["Desert"], False, False)
					bSwapped = True
				if iTerrain == Terrain["Fields of perdition"]:
					pPlot.setTerrainType(Terrain["Plains"], False, False)
					bSwapped = True
				if iTerrain == Terrain["Shallows"]:
					pPlot.setTerrainType(Terrain["Marsh"], False, False)
					bSwapped = True
			if bSwapped:
				sanctifyResource(pPlot)
	else:
		for x,y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
			pPlot = getPlot(x,y)
			if not pPlot.isNone():
				if gc.getTerrainInfo(pPlot.getTerrainType()).isHell():
					sanctifyResource(pPlot)
				pPlot.setPlotCounter(0)

# FF: Added by Jean Elcard 14/01/2009 (speed tweak)
		rebuildGraphics()
# FF: End Add

def reqSanctuary(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumCities() == 0:
		return False
	if not pPlayer.isHuman():
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		pTeam = gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) < 2:
			return False
	return True

def spellSanctuary(caster):
	iPlayer = caster.getOwner()
	iTeam = caster.getTeam()
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.changeSanctuaryTimer(30)
	map	= CyMap()
	plotByIndex = map.plotByIndex
	for i in xrange(map.numPlots()):
		pPlot = plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				for i in xrange(pPlot.getNumUnits(), -1, -1):
					pUnit = pPlot.getUnit(i)
					if pUnit.getTeam() != iTeam:
						pUnit.jumpToNearestValidPlot()

def reqSandLion(caster):
	pPlot = caster.plot()
	if (pPlot.getTerrainType() != Terrain["Desert"] and pPlot.getTerrainType() != Terrain["Burning sands"]):
		return False
	return True

def reqScorch(caster):
	pPlot           = caster.plot()
	iTerrain        = pPlot.getTerrainType()
	pPlayer         = gc.getPlayer(caster.getOwner())
	iValidTerrains  = [Terrain["Glacier"],Terrain["Tundra"],Terrain["Taiga"],Terrain["Marsh"],Terrain["Grass"],Terrain["Plains"],Terrain["Shallows"],Terrain["Broken lands"],Terrain["Fields of perdition"]]
	iCiv            = pPlayer.getCivilizationType()
	# Frozen and Illians like the coldest weather: they never scorch anything
	if iCiv in [Civ["Illians"],Civ["Frozen"]]:
		return False
	# Dtesh likes the hottest driest weather: they always scorch (and don't fear war if they scorch their neighbours)
	if iCiv == Civ["D'Tesh"]:
		if iTerrain != Terrain["Wasteland"]:
			return True
		return False
	if iTerrain in iValidTerrains:                                                                  # Normal civilizations can scorch all terrains except desert, burning sands, fields of perdition and wasteland
		if not pPlayer.isHuman():                                                                   # Several limitations to help AIs choices:
			if caster.getOwner() != pPlot.getOwner():                                               # - Avoid terraforming foreign territory (and getting at war automatically)
				return False
			if iTerrain == Terrain["Marsh"] and iCiv in [Civ["Mazatl"],Civ["Cualli"]]:              # - Marsh is good for lizards
				return False
			if iTerrain == Terrain["Taiga"] and iCiv == Civ["Doviello"]:                            # - Taiga is not worse than plains for Doviello
				return False
			if iTerrain == Terrain["Plains"] and iCiv !=Civ["Malakim"]:                             # - Keeping plains (instead of desert) is good for everyone except Malakim
				return False
			if iTerrain == Terrain["Fields of perdition"] and iCiv !=Civ["Infernal"]:               # - Keeping fields of perdition (instead of burning sands) is "good" for everyone except Infernal
				return False
		return True
	return False


def spellScorch(caster):
	gc              = CyGlobalContext()
	pPlot           = caster.plot()
	iTerrain        = pPlot.getTerrainType()
	iFeature        = pPlot.getFeatureType()
	iImprovement    = pPlot.getImprovementType()
	iPlayer         = caster.getOwner()
	pPlayer         = gc.getPlayer(iPlayer)
	iCiv            = pPlayer.getCivilizationType()

	# 1) spawn a defender in scorched terrain
	pSpawnPlot = findClearPlot(UnitTypes.NO_UNIT, pPlot)
	if iFeature == gc.getInfoTypeForString("FEATURE_FOREST_ANCIENT"):
		if pSpawnPlot != -1:
			iTreant      = getInfoType('UNIT_TREANT')
			eDirection   = directionXYFromPlot(pSpawnPlot, pPlot)
			pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
			pTreant      = pDemonPlayer.initUnit(iTreant, pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, eDirection)
			pTreant.setDuration(5)
	elif iFeature == gc.getInfoTypeForString("FEATURE_FOREST_BURNT"):
		if CyGame().getSorenRandNum(100, "Mistform Spawn") < 25:
			if pSpawnPlot != -1:
				iMistform    = getInfoType('UNIT_MISTFORM')
				eDirection   = directionXYFromPlot(pSpawnPlot, pPlot)
				pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
				pMistform    = pDemonPlayer.initUnit(iMistform, pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, eDirection)
				pMistform.setDuration(5)
	elif iFeature == gc.getInfoTypeForString("FEATURE_JUNGLE"):
		if CyGame().getSorenRandNum(100, "Jungle Defender Spawn") < 5:
			if pSpawnPlot != -1:
				lJList          = ['UNIT_GOBLIN', 'UNIT_GOBLIN', 'UNIT_GOBLIN', 'UNIT_WOLF_RIDER', 'UNIT_LIZARDMAN', 'UNIT_LIZARDMAN', 'UNIT_LIZARDMAN', 'UNIT_LIZARDMAN', 'UNIT_LIZARDMAN_RANGER', 'UNIT_LIZARDMAN_ASSASSIN']
				sJungleDefender = lJList[CyGame().getSorenRandNum(len(lJList), "Pick Jungle Defender")]
				iJungleDefender = getInfoType(sJungleDefender)
				eDirection      = directionXYFromPlot(pSpawnPlot, pPlot)
				pOrcPlayer      = gc.getPlayer(gc.getORC_PLAYER())
				pJungleDefender = pOrcPlayer.initUnit(iJungleDefender, pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, eDirection)
	elif iFeature in [gc.getInfoTypeForString("FEATURE_FOREST"),gc.getInfoTypeForString("FEATURE_FOREST_NEW")]:
		if CyGame().getSorenRandNum(100, "Forest Defender Spawn") < 5:
			if pSpawnPlot != -1:
				lFList          = ['UNIT_WOLF', 'UNIT_WOLF', 'UNIT_WOLF', 'UNIT_WOLF', 'UNIT_WOLF', 'UNIT_WOLF_PACK', 'UNIT_WOLF_PACK', 'UNIT_WOLF_PACK', 'UNIT_BABY_SPIDER', 'UNIT_BABY_SPIDER', 'UNIT_BABY_SPIDER', 'UNIT_BABY_SPIDER', 'UNIT_BABY_SPIDER', 'UNIT_GRIFFON', 'UNIT_BEAR','UNIT_BEAR', 'UNIT_FAWN', 'UNIT_FAWN', 'UNIT_FAWN', 'UNIT_FAWN', 'UNIT_FAWN', 'UNIT_SATYR']
				sForestDefender = lFList[CyGame().getSorenRandNum(len(lFList), "Pick Forest Defender")]
				iForestDefender = getInfoType(sForestDefender)
				eDirection      = directionXYFromPlot(pSpawnPlot, pPlot)
				pAnimalPlayer   = gc.getPlayer(gc.getANIMAL_PLAYER())
				pForestDefender = pAnimalPlayer.initUnit(iForestDefender, pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, eDirection)

	# 2) terraform the terrain
	if iImprovement == Improvement["Swamp"]:
		pPlot.setImprovementType(-1)

	if iTerrain == Terrain["Glacier"]:
		pPlot.setTerrainType(Terrain["Tundra"], True, True)
	elif iTerrain == Terrain["Tundra"]:
		pPlot.setTerrainType(Terrain["Taiga"], True, True)
	elif iTerrain == Terrain["Taiga"]:
		pPlot.setTerrainType(Terrain["Plains"], True, True)
	elif iTerrain == Terrain["Marsh"]:
		pPlot.setTerrainType(Terrain["Grass"], True, True)
	elif iTerrain == Terrain["Shallows"]: # hell equivalent of marsh
		pPlot.setTerrainType(Terrain["Broken lands"], True, True) # hell grass
	elif iTerrain == Terrain["Grass"]:
		pPlot.setTerrainType(Terrain["Plains"], True, True)
	elif iTerrain == Terrain["Broken lands"]: # hell grass
		pPlot.setTerrainType(Terrain["Fields of perdition"], True, True)# hell plains
	elif iTerrain == Terrain["Plains"]:
		if iCiv != Civ["D'Tesh"]:
			pPlot.setTerrainType(Terrain["Desert"], True, True)
			if iFeature in [Feature["Forest"],Feature["Forest New"]]:
				pPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
				if CyGame().getSorenRandNum(100, "Scorch Forest Scrub") < 33:
					pPlot.setFeatureType(Feature["Scrub"], -1)
			elif iFeature == Feature["Jungle"]:
				pPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
				if CyGame().getSorenRandNum(100, "Scorch Jungle Scrub") < 25:
					pPlot.setFeatureType(Feature["Scrub"], -1)
			elif iFeature == Feature["Ancient Forest"]:
				pPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
				if CyGame().getSorenRandNum(100, "Scorch Ancient Forest Scrub") < 20:
					pPlot.setFeatureType(Feature["Scrub"], -1)
			elif iFeature == Feature["Burnt Forest"]:
				pPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
			# add flood plains to new desert along rivers (delayed)
			if pPlot.canHaveFeature(Feature["Flood Plains"]):
				pPlot.setFeatureType(Feature["Flood Plains"], -1)
				pPlot.setTempFeatureType(FeatureTypes.NO_FEATURE, -1, scale(5))
			# adds an oasis to some of the new deserts
			if pPlot.canHaveFeature(Feature["Oasis"]):
				if CyGame().getSorenRandNum(10000, "Scorch Oasis") < gc.getFeatureInfo(Feature["Oasis"]).getAppearanceProbability():
					pPlot.setFeatureType(Feature["Oasis"], -1)
		else: #if dtesh, plain becomes wasteland directly
			pPlot.setTerrainType(Terrain["Wasteland"], True, True)
			if iFeature in [Feature["Forest"],Feature["Forest New"],Feature["Ancient Forest"],Feature["Burnt Forest"],Feature["Jungle"],Feature["Scrub"]]:
				pPlot.setPlotEffectType(Feature["Haunted Lands"])
	elif iTerrain == Terrain["Fields of perdition"]: # hell plains
		if iCiv != Civ["D'Tesh"]: # only infernal because of reqscorch
			pPlot.setTerrainType(Terrain["Burning sands"], True, True) # hell desert
		else: #if dtesh
			pPlot.setTerrainType(Terrain["Wasteland"], True, True)
			pPlot.changePlotCounter(0)
	elif iTerrain in [Terrain["Desert"],Terrain["Burning sands"]]:
		if iCiv == Civ["D'Tesh"]:
			pPlot.setTerrainType(Terrain["Wasteland"], True, True)
			pPlot.changePlotCounter(0)

	# 3) declare war at plot owner
	if pPlot.isOwned() and iPlayer != pPlot.getOwner():
		startWar(iPlayer, pPlot.getOwner(), WarPlanTypes.WARPLAN_TOTAL)

	# 4) Melt Ice
	getPlot = CyMap().plot
	iIce    = Feature["Ice"]
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pTargetPlot = getPlot(x, y)
		if pTargetPlot.getFeatureType() == iIce:
				pTargetPlot.setFeatureType(-1, -1)


def spellSing(caster):
	pPlot = caster.plot()
	point = pPlot.getPoint()
	iRnd = CyGame().getSorenRandNum(100, "Sing")
	szText = "AS3D_SING1"
	if iRnd > 25:
		szText = "AS3D_SING2"
	if iRnd > 50:
		szText = "AS3D_SING3"
	if iRnd > 75:
		szText = "AS3D_SING4"
	CyAudioGame().Play3DSound(szText,point.x,point.y,point.z)

def reqSironasTouch(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isFeatAccomplished(FeatTypes.FEAT_HEAL_UNIT_PER_TURN) == False:
		return False
	if not caster.isHurt():
		return False
	if pPlayer.isHuman() == False:
		if caster.getDamage() < 15:
			return False
	return True

def spellSironasTouch(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.setFeatAccomplished(FeatTypes.FEAT_HEAL_UNIT_PER_TURN, False)
	caster.changeDamage(-15,0)

def reqSlaveTradeBuy(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	eCiv 			= pPlayer.getCivilizationType()
	iCiv = pPlayer.getCivilizationType()
	if iCiv in [Civ["D'Tesh"],Civ["Mekara Order"]]:
		return False
	if eCiv == gc.getInfoTypeForString("CIVILIZATION_MEKARA_V2"):
		return False
	return True

def spellSlaveTradeBuy(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	newUnit = pPlayer.initUnit(getInfoType('UNIT_SLAVE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	iPromotion = -1
	iRnd = CyGame().getSorenRandNum(100, "Slave Trade Buy")
	if (iRnd >= 60 and iRnd < 70):
		iPromotion = getInfoType('PROMOTION_DWARF')
	if (iRnd >= 70 and iRnd < 80):
		iPromotion = getInfoType('PROMOTION_ELF')
	if (iRnd >= 80):
		iPromotion = getInfoType('PROMOTION_ORC')
	if iPromotion != -1:
		newUnit.setHasPromotion(iPromotion, True)

def spellSnowfall(caster):
	iFlames = getInfoType('FEATURE_FLAMES')
	iSmoke = getInfoType('IMPROVEMENT_SMOKE')
	randNum = CyGame().getSorenRandNum
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			if not pPlot.isWater():
				if pPlot.getTerrainType() not in [iTundra,iGlacier]:
					iRnd = randNum(6, "Snowfall") + 3
					pPlot.setTempTerrainType(iTundra, iRnd)
					if pPlot.getFeatureType() == iFlames:
						pPlot.setFeatureType(-1, -1)
					if pPlot.getImprovementType() == iSmoke:
						pPlot.setImprovementType(-1)

def spellSnowfallGreater(caster):
	iFlames = getInfoType('FEATURE_FLAMES')
	iSmoke = getInfoType('IMPROVEMENT_SMOKE')
	getPlot	= CyMap().plot
	iRange = 2 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			if not pPlot.isWater():
				if pPlot.getTerrainType() != iGlacier:
					iRnd = CyGame().getSorenRandNum(12, "Snowfall") + 6
					pPlot.setTempTerrainType(iGlacier, iRnd)
					if pPlot.getFeatureType() == iFlames:
						pPlot.setFeatureType(-1, -1)
					if pPlot.getImprovementType() == iSmoke:
						pPlot.setImprovementType(-1)

def reqSpreadTheCouncilOfEsus(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()
	#if pCity.isHasReligion(getInfoType('RELIGION_COUNCIL_OF_ESUS')):
	#	return False
	if pCity.isHasBuildingClass(getInfoType("BUILDINGCLASS_APHOTIC_THRONE")):
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getStateReligion() != getInfoType('RELIGION_COUNCIL_OF_ESUS'):
			return False
	return True

def spellFoundThrone(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()
	if(pPlayer.getCivilizationType()==getInfoType("CIVILIZATION_SVARTALFAR")):
		pCity.setNumRealBuilding(getInfoType("BUILDING_APHOTIC_THRONE_FAERYL"),1)
		return
	thrones=["BUILDING_APHOTIC_THRONE_MERCHANT","BUILDING_APHOTIC_THRONE_MERCHANT","BUILDING_APHOTIC_THRONE_SLAVER","BUILDING_APHOTIC_THRONE_SLAVER","BUILDING_APHOTIC_THRONE_POISONER","BUILDING_APHOTIC_THRONE_POISONER","BUILDING_APHOTIC_THRONE_BORED_NOBLE"]
	randNum		= CyGame().getSorenRandNum
	ind = randNum(len(thrones),"aphotic throne")
	pCity.setNumRealBuilding(getInfoType(thrones[ind]),1)
	
def reqSpring(caster):
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iCiv = pPlayer.getCivilizationType()
	iTerrain = pPlot.getTerrainType()
	iImprovement = pPlot.getImprovementType()
	
	iDesert	= getInfoType('TERRAIN_DESERT')
	iPlains	= getInfoType('TERRAIN_PLAINS')
	iGrass	= getInfoType('TERRAIN_GRASS')
	iTaiga	= getInfoType('TERRAIN_TAIGA')
	iMarsh	= getInfoType('TERRAIN_MARSH')
	iFieldsOfPerdition	= getInfoType('TERRAIN_FIELDS_OF_PERDITION')
	iBrokenLands		= getInfoType('TERRAIN_BROKEN_LANDS')
	
	#if iCiv == Civ["Malakim"]:
	#	return False
	if iTerrain not in [iDesert, iPlains, iGrass, iTaiga, iMarsh, iFieldsOfPerdition, iBrokenLands]:
		return False
	if iTerrain == iMarsh:
		if iCiv not in [Civ['Mazatl'], Civ['Cualli']]:
			return False
		if pPlot.isCity():
			return False
		if iImprovement == getInfoType('IMPROVEMENT_SWAMP'):
			return False
		if iImprovement != -1 and gc.getImprovementInfo(iImprovement).isUnique():
			return False
	if not pPlayer.isHuman():
		if pPlot.getOwner() != iPlayer:
			return False
		if iCiv in [Civ['Mazatl'], Civ['Cualli']]:
			if iImprovement != -1 and iImprovement != getInfoType('IMPROVEMENT_FARM'):
				return False
		else:
			if iTerrain == getInfoType('TERRAIN_GRASS'):
				return False
		if iCiv == Civ["Infernal"]:
			return False
	return True

def spellSpring(caster):
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iCiv = pPlayer.getCivilizationType ()
	iTerrain = pPlot.getTerrainType()
	
	iDesert	= getInfoType('TERRAIN_DESERT')
	iPlains	= getInfoType('TERRAIN_PLAINS')
	iGrass	= getInfoType('TERRAIN_GRASS')
	iTaiga	= getInfoType('TERRAIN_TAIGA')
	iMarsh	= getInfoType('TERRAIN_MARSH')
	iFieldsOfPerdition	= getInfoType('TERRAIN_FIELDS_OF_PERDITION')
	iBrokenLands		= getInfoType('TERRAIN_BROKEN_LANDS')
	iShallows			= getInfoType('TERRAIN_SHALLOWS')
	
	if iTerrain == iDesert:
		pPlot.setTerrainType(iPlains,True,True)
		if pPlot.getFeatureType() == getInfoType('FEATURE_FLOOD_PLAINS'):
			pPlot.setFeatureType(-1, -1)
	elif iTerrain == iPlains:
		pPlot.setTerrainType(iGrass,True,True)
	elif iTerrain in [iGrass, iTaiga]:
		pPlot.setTerrainType(iMarsh,True,True)
	elif iTerrain in [iFieldsOfPerdition, iBrokenLands]:
		pPlot.setTerrainType(iShallows,True,True)
	elif iTerrain == iMarsh and iCiv in [Civ['Mazatl'], Civ['Cualli']]:
		pPlot.setImprovementType(getInfoType('IMPROVEMENT_SWAMP'))
	
def reqSprint(caster):
	if caster.isHasPromotion(getInfoType('PROMOTION_FATIGUED')):
		return False
	return True

def reqStasis(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHasTech(getInfoType('TECH_KNOWLEDGE_OF_THE_ETHER')):
		return True
	return False

def spellStasis(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iDelay = 20
	iTeam = pPlayer.getTeam()
	if CyGame().getGameSpeedType() == getInfoType('GAMESPEED_QUICK'):
		iDelay = 14
	if CyGame().getGameSpeedType() == getInfoType('GAMESPEED_EPIC'):
		iDelay = 30
	if CyGame().getGameSpeedType() == getInfoType('GAMESPEED_MARATHON'):
		iDelay = 60
	for iPlayer2 in range(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if pPlayer2.isAlive():
			if pPlayer2.getTeam() != iTeam:
				pPlayer2.changeDisableProduction(iDelay)
				pPlayer2.changeDisableResearch(iDelay)

def reqSteal(caster):
	iTeam = caster.getTeam()
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getTeam() != iTeam and not pUnit.isCommunalProperty():
			for iProm in range(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(iProm):
					if gc.getPromotionInfo(iProm).isEquipment():
						return True
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getTeam() != iTeam:
			for iBuild in range(gc.getNumBuildingInfos()):
				if pCity.getNumRealBuilding(iBuild) > 0:
					if gc.getBuildingInfo(iBuild).getEquipmentPromotion() != -1:
						return True
	return False

def spellSteal(caster):
	iTeam = caster.getTeam()
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getTeam() != iTeam:
			for iProm in range(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(iProm) and not pUnit.isCommunalProperty():
					if gc.getPromotionInfo(iProm).isEquipment():
						if CyGame().getSorenRandNum(100, "Steal") <= 20:
							startWar(caster.getOwner(), pUnit.getOwner(), WarPlanTypes.WARPLAN_TOTAL)
						else:
							caster.setHasPromotion(iProm, True)
							pUnit.setHasPromotion(iProm, False)
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getTeam() != iTeam:
			for iBuild in range(gc.getNumBuildingInfos()):
				if pCity.getNumRealBuilding(iBuild) > 0:
					if gc.getBuildingInfo(iBuild).getEquipmentPromotion() != -1:
						if CyGame().getSorenRandNum(100, "Steal") <= 20:
							startWar(caster.getOwner(), pUnit.getOwner(), WarPlanTypes.WARPLAN_TOTAL)
						else:
							pCity.setNumRealBuilding(iBuild, 0)
							caster.setHasPromotion(gc.getBuildingInfo(iBuild).getEquipmentPromotion(), True)

def reqTakeEquipmentBuilding(caster,building):
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_NAVAL'):
		return False
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_SIEGE'):
		return False
	if caster.getSpecialUnitType() == getInfoType('SPECIALUNIT_SPELL'):
		return False
	if caster.isHasPromotion(getInfoType('PROMOTION_ILLUSION')):
		return False
	iBuilding = getInfoType(building)
	iProm = gc.getBuildingInfo(iBuilding).getEquipmentPromotion()
	if caster.isHasPromotion(iProm):
		return False
	return True

def spellTakeEquipmentBuilding(caster,building):
	iBuilding = getInfoType(building)
	pPlot = caster.plot()
	pPlot.getPlotCity().setNumRealBuilding(iBuilding, 0)

def reqTakeEquipmentPromotion(caster,promotion):
	iBird = getInfoType('SPECIALUNIT_BIRD')
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_NAVAL'):
		return False
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_SIEGE'):
		return False
	if caster.getSpecialUnitType() == getInfoType('SPECIALUNIT_SPELL'):
		return False
	if (caster.getSpecialUnitType()==iBird):
		return False
	if caster.isHasPromotion(getInfoType('PROMOTION_ILLUSION')):
		return False
	iProm = getInfoType(promotion)
	if caster.isHasPromotion(iProm):
		return False
	iPlayer = caster.getOwner()
	pPlot = caster.plot()
	pHolder = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if ((pUnit.getOwner() == iPlayer or pUnit.isCommunalProperty()) and pUnit.isHasPromotion(iProm) and not pUnit.isHasCasted()):
			pHolder = pUnit
	if pHolder == -1:
		return False
	if pHolder.getUnitType() == getInfoType('UNIT_BARNAXUS'):
		if iProm == getInfoType('PROMOTION_PIECES_OF_BARNAXUS'):
			return False
	if pHolder.getUnitType() == getInfoType('UNIT_THE_HIVE'):
		if iProm == getInfoType('PROMOTION_PIECES_OF_THE_HIVE'):
			return False
	if pHolder.getUnitType() == getInfoType('UNIT_MITHRIL_GOLEM'):
		if iProm == getInfoType('PROMOTION_PIECES_OF_MITHRIL_GOLEM'):
			return False
	if pHolder.getUnitType() == getInfoType('UNIT_WAR_MACHINE'):
		if iProm == getInfoType('PROMOTION_PIECES_OF_WAR_MACHINE'):
			return False
	if pHolder.getUnitType() == getInfoType('UNIT_MECH_DRAGON'):
		if iProm == getInfoType('PROMOTION_PIECES_OF_MECH_DRAGON'):
			return False
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.isHuman() == False and pHolder.getUnitType() != getInfoType('EQUIPMENT_CONTAINER'):
		if caster.baseCombatStr() - 2 <= pHolder.baseCombatStr():
			return False
		if gc.getUnitInfo(pHolder.getUnitType()).getFreePromotions(iProm):
			return False
	return True

def spellTakeEquipmentPromotion(caster,promotion):
	iProm = getInfoType(promotion)
	iPlayer = caster.getOwner()
	pPlot = caster.plot()
	pHolder = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if ((pUnit.getOwner() == iPlayer or pUnit.isCommunalProperty()) and pUnit.isHasPromotion(iProm) and not pUnit.isHasCasted()):
			pHolder = pUnit
	if pHolder != -1:
		pHolder.setHasPromotion(iProm, False)
		caster.setHasPromotion(iProm, True)
		if promotion == 'PROMOTION_BAIR_GEM_RECHARGING' and not pHolder.isCommunalProperty():
			pHolder.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BAIR_GEM_ACTIVE'), False)

def reqTakeEquipmentUnit(caster,unit):
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_NAVAL'):
		return False
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_SIEGE'):
		return False
	if caster.getSpecialUnitType() == getInfoType('SPECIALUNIT_SPELL'):
		return False
	if caster.isHasPromotion(getInfoType('PROMOTION_ILLUSION')):
		return False
	iUnit = getInfoType(unit)
	iProm = gc.getUnitInfo(iUnit).getEquipmentPromotion()
	if caster.isHasPromotion(iProm):
		return False
	iPlayer = caster.getOwner()
	pPlot = caster.plot()
	pHolder = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if ((pUnit.getOwner() == iPlayer or pUnit.isCommunalProperty()) and pUnit.getUnitType() == iUnit):
			if pUnit.isDelayedDeath() == False:
				pHolder = pUnit
	if pHolder == -1:
		return False
	return True

def spellTakeEquipmentUnit(caster,unit):
	iUnit = getInfoType(unit)
	iProm = gc.getUnitInfo(iUnit).getEquipmentPromotion()
	iPlayer = caster.getOwner()
	pPlot = caster.plot()
	pHolder = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if ((pUnit.getOwner() == iPlayer or pUnit.isCommunalProperty()) and pUnit.getUnitType() == iUnit):
			if pUnit.isDelayedDeath() == False:
				pHolder = pUnit
	if pHolder != -1:
		pHolder.kill(True, PlayerTypes.NO_PLAYER)

def reqTaunt(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	bValid = False
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pLoopPlot = getPlot(x, y)
		for i in range(pLoopPlot.getNumUnits()):
			pUnit = pLoopPlot.getUnit(i)
			if pTeam.isAtWar(pUnit.getTeam()):
				if pUnit.isAlive():
					if not pUnit.isOnlyDefensive():
						if pUnit.getImmobileTimer() == 0:
							bValid = True
	return bValid

def spellTaunt(caster):
	iEnraged = getInfoType('PROMOTION_ENRAGED')
	iSpell = getInfoType('SPELL_TAUNT')
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	bValid = False
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pLoopPlot = getPlot(x, y)
		for i in xrange(pLoopPlot.getNumUnits()):
			pUnit = pLoopPlot.getUnit(i)
			if pTeam.isAtWar(pUnit.getTeam()):
				if pUnit.isAlive():
					if not pUnit.isOnlyDefensive():
						if not pUnit.isResisted(caster, iSpell):
							pUnit.setHasPromotion(iEnraged, True)
							pUnit.attack(pPlot, False)
							pUnit.setHasPromotion(iEnraged, False)

def spellTeleport(caster,loc):
	player = caster.getOwner()
	pPlayer = gc.getPlayer(player)
	pCity = pPlayer.getCapitalCity()
	if loc == 'Capital':
		if pCity.isNone():
			pPlot = caster.getSpawnPlot()
			if caster.canMoveInto(pPlot, False, False, True):
				caster.setXY(pPlot.getX(), pPlot.getY(), False, True, True,False)
		else:
			if (caster.getDomainType()==getInfoType("DOMAIN_SEA")and not pCity.isCoastal(10)):
				pNearestCity = gc.getMap().findCity(pCity.getX(), pCity.getY(), -1, pCity.getTeam(), False, True, -1, -1, pCity, True)
				if (not pNearestCity.isNone()):
					caster.setXY(pNearestCity.getX(),pNearestCity.getY(),False,True,True,False)
			else:
				caster.setXY(pCity.getX(), pCity.getY(), False, True, True,False)
	if loc == 'Random':
		pBestPlot	= -1
		iBestPlot	= -1
		for i in xrange(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlotValue = -1
			if not pPlot.isWater() and not pPlot.isCity() and not pPlot.isImpassable() and not pPlot.isOwned() and pPlot.getNumUnits() == 0:
				iPlotValue = CyGame().getSorenRandNum(1000,"spellTeleport")
				if iPlotValue > iBestPlot:
					iBestPlot = iPlotValue
					pBestPlot = pPlot
		if pBestPlot != -1:
			caster.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True,False)

def reqTeachSpellcasting(caster):
	iAnimal = getInfoType('UNITCOMBAT_ANIMAL')
	iBird = getInfoType('SPECIALUNIT_BIRD')
	lList = filter( caster.isHasPromotion, ISpellLvl1Promotion )
	if len(lList) > 0:
		pPlot = caster.plot()
		iPlayer = caster.getOwner()
		for i in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getOwner() == iPlayer:
				if pUnit.isAlive():
					if pUnit.getUnitCombatType() != iAnimal:
						if pUnit.getSpecialUnitType() != iBird:
							for iProm in range(len(lList)):
								if not pUnit.isHasPromotion(lList[iProm]):
									return True
	return False

def spellTeachSpellcasting(caster):
	iAnimal = getInfoType('UNITCOMBAT_ANIMAL')
	iBird = getInfoType('SPECIALUNIT_BIRD')
	lList = filter( caster.isHasPromotion, ISpellLvl1Promotion )
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == iPlayer:
			if pUnit.isAlive():
				if pUnit.getUnitCombatType() != iAnimal:
					if pUnit.getSpecialUnitType() != iBird:
						for iProm in range(len(lList)):
							if not pUnit.isHasPromotion(lList[iProm]):
								pUnit.setHasPromotion(lList[iProm], True)

def reqTransmutation(caster):
	#iBonus = pPlot.getBonusType(-1)
	#IFertilizable = IFarm+ICamp+IPasture+IPlantation+IFishing
	#return iBonus in IFertilizable
	pPlot = caster.plot()
	if pPlot.getOwner() != caster.getOwner():
		return False
	if (pPlot.getBonusType(-1) != Bonus["Copper"] and pPlot.getBonusType(-1) != Bonus["Gold"]):
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if (pPlot.getBonusType(-1) == Bonus["Copper"] and pPlayer.countOwnedBonuses(Bonus["Copper"]) >= 2 and pPlayer.countOwnedBonuses(Bonus["Gold"]) == 0):
			return True
		if (pPlot.getBonusType(-1) == Bonus["Gold"] and pPlayer.countOwnedBonuses(Bonus["Gold"]) >= 2 and pPlayer.countOwnedBonuses(Bonus["Copper"]) == 0):
			return True
		return False
	return True

def spellTransmutation(caster):
	pPlot = caster.plot()
	iBonus = -1
	if pPlot.getBonusType(-1) == Bonus["Copper"]:
		iBonus = Bonus["Gold"]
	if pPlot.getBonusType(-1) == Bonus["Gold"]:
		iBonus = Bonus["Copper"]
	if iBonus != -1:
		pPlot.setBonusType(iBonus)

def reqMinorBrood(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = gc.getTeam(pPlayer.getTeam())
	if pPlot.getOwner() != caster.getOwner():
		return False
	if (pPlot.getBonusType(-1) != Bonus["Cow"] and pPlot.getBonusType(-1) != Bonus["Horse"] and pPlot.getBonusType(-1) != Bonus["Arctic Deer"] and pPlot.getBonusType(-1) != Bonus["Deer"] and pPlot.getBonusType(-1) != Bonus["Sheep"] and pPlot.getBonusType(-1) != Bonus["Pig"] and pPlot.getBonusType(-1) != Bonus["Bison"]):
		return False

	if pPlot.getBonusType(-1) == Bonus["Horse"]:
		if pTeam.isHasTech(getInfoType('TECH_ANIMAL_HUSBANDRY')) == False:
			return False

	if pPlayer.isHuman() == False:
		if (pPlot.getBonusType(-1) == Bonus["Cow"] and pPlayer.countOwnedBonuses(Bonus["Cow"]) < 3):
			return False
		if (pPlot.getBonusType(-1) == Bonus["Pig"] and pPlayer.countOwnedBonuses(Bonus["Pig"]) < 3):
			return False
		if (pPlot.getBonusType(-1) == Bonus["Sheep"] and pPlayer.countOwnedBonuses(Bonus["Sheep"]) < 3):
			return False
		if (pPlot.getBonusType(-1) == Bonus["Deer"] and pPlayer.countOwnedBonuses(Bonus["Deer"]) < 3):
			return False
		if (pPlot.getBonusType(-1) == Bonus["Arctic Deer"] and pPlayer.countOwnedBonuses(Bonus["Arctic Deer"]) < 3):
			return False
		if (pPlot.getBonusType(-1) == Bonus["Horse"] and pPlayer.countOwnedBonuses(Bonus["Horse"]) < 3):
			return False
		if pPlot.isCityRadius() :
			return False
		return True


	return True

def spellMinorBrood(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	iBabySpider = getInfoType('UNIT_BABY_SPIDER')
	
	if (pPlot.getBonusType(-1) == Bonus["Cow"] or pPlot.getBonusType(-1) == Bonus["Horse"] or pPlot.getBonusType(-1) == Bonus["Arctic Deer"] or pPlot.getBonusType(-1) == Bonus["Deer"] or pPlot.getBonusType(-1) == Bonus["Sheep"] or pPlot.getBonusType(-1) == Bonus["Pig"]):
		pPlot.setBonusType(-1)

		iCasterLevel = caster.getLevel()
		iEmpower1 = getInfoType('PROMOTION_EMPOWER1')
		iEmpower2 = getInfoType('PROMOTION_EMPOWER2')
		iEmpower3 = getInfoType('PROMOTION_EMPOWER3')
		iEmpower4 = getInfoType('PROMOTION_EMPOWER4')
		iEmpower5 = getInfoType('PROMOTION_EMPOWER5')


		iCount1 = CyGame().getSorenRandNum(2, "Minor Brood count 1") + 1
		iCount2 = CyGame().getSorenRandNum(2, "Minor Brood count 2") + 1
		iCountTotal = iCount1 + iCount2

		for i in xrange(iCountTotal):
			newUnit = pPlayer.initUnit(getInfoType('UNIT_BABY_SPIDER'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if iCasterLevel >= 3:
				newUnit.setHasPromotion(iEmpower1, True)
			if iCasterLevel >= 4:
				newUnit.setHasPromotion(iEmpower2, True)
			if iCasterLevel >= 5:
				newUnit.setHasPromotion(iEmpower3, True)
			if iCasterLevel >= 6:
				newUnit.setHasPromotion(iEmpower4, True)
			if iCasterLevel >= 7:
				newUnit.setHasPromotion(iEmpower5, True)



def spellTreetopDefence(caster):
	pPlot = caster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getTeam() == caster.getTeam():
			pUnit.setFortifyTurns(5)

def reqTrust(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isFeatAccomplished(FeatTypes.FEAT_TRUST):
		return False
	if pPlayer.isBarbarian():
		return False
	return True

def spellTrust(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = pPlayer.getCapitalCity()
	pPlayer.setFeatAccomplished(FeatTypes.FEAT_TRUST, True)


def reqTsunamiKraken(caster):
	gc			= CyGlobalContext()
	pPlayer 	= gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman(): return True
	pTeam 		= gc.getTeam(pPlayer.getTeam())
	pCasterPlot	= caster.plot()
	getPlot	= CyMap().plot
	iRange = 2 + caster.getSpellExtraRange()
	for x,y in plotsInRange( caster.getX(), caster.getY(), iRange, 1 ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			if pPlot.isAdjacentToWater():
				for i in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					if pTeam.isAtWar(pUnit.getTeam()):
						return True
	return False

def spellTsunami(caster):
	gc			= CyGlobalContext()
	eCold		= getInfoType('DAMAGE_COLD')
	effect		= CyEngine().triggerEffect
	pCasterPlot	= caster.plot()
	randNum		= CyGame().getSorenRandNum
	getPlot	= CyMap().plot
	iRange = 2 + caster.getSpellExtraRange()
	for x,y in plotsInRange( caster.getX(), caster.getY(), iRange, 1 ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			if pPlot.isAdjacentToWater():
				bEffect = False
				for i in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					pUnit.doDamage(30, 75, caster, eCold, True)
					bEffect = True
				if pPlot.getImprovementType() != -1:
					if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent() == False:
						if randNum(100, "Tsunami") <= 25:
							pPlot.setImprovementType(-1)
							bEffect = True
				if bEffect==True:
					effect(getInfoType('EFFECT_SPRING'),pPlot.getPoint())

def spellUnyieldingOrder(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pCity.setOccupationTimer(0)
	pCity.changeHurryAngerTimer(-9)

def spellArchon(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pCity.changeHurryAngerTimer(-20)

def reqUpgradeDovielloWarrior(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		pTeam = gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) == 0:
			return False
		if pTeam.getAtWarCount(True) == 1:
			if pPlayer.getNumCities() > 1:
				return False
	return True

def spellUseSupplies(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_USE_SUPPLIES')
	triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCity.getX(), pCity.getY(), iPlayer, pCity.getID(), -1, -1, -1, -1)

def reqVeilOfNight(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if getInfoType("MODULE_NOT_YET_EMERGENT_LEADERS")!=-1 and pPlayer.hasTrait(Trait["Sylvan Shade 1"]): # EmergentLeaders Module
		eTeam = gc.getTeam(pPlayer.getTeam())
		if eTeam.isHasTech(getInfoType('TECH_WAY_OF_THE_FORESTS')) == False:
			return False
	if pPlayer.isHuman() == False:
		if pPlayer.getNumUnits() < 25:
			return False
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		pTeam = gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) > 0:
			return False
	return True

def spellVeilOfNight(caster):
	iHiddenNationality = getInfoType('PROMOTION_HIDDEN_NATIONALITY')
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	py = PyPlayer(iPlayer)
	if getInfoType("MODULE_NOT_YET_EMERGENT_LEADERS")!=-1 and pPlayer.hasTrait(Trait["Sylvan Shade 1"]): # EmergentLeaders Module
		iTreant = getInfoType('UNIT_TREANT')
		map	= CyMap()
		plotByIndex	= map.plotByIndex
		for i in xrange(map.numPlots()):
			pPlot = plotByIndex(i)
			if pPlot.isOwned():
				if pPlot.getOwner() == iPlayer:
					if (pPlot.getFeatureType() == Feature["Forest"] or pPlot.getFeatureType() == Feature["Ancient Forest"]):
						newUnit = pPlayer.initUnit(iTreant, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setDuration(5)
						if pPlayer.hasTrait(Trait["Sylvan Shade 2"]):
							newUnit.setDuration(10)
						pPlot.setFeatureType(Feature["Forest New"],0)
	else:
		for pUnit in py.getUnitList():
			if pUnit.baseCombatStr() > 0:
				pUnit.setHasPromotion(iHiddenNationality, True)

def reqWane(caster):
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_ANIMAL'):
		return False
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_BEAST'):
		return False
	if caster.isImmortal():
		return False
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_WORKER'):
		return False
	if caster.getUnitClassType() == getInfoType('UNITCLASS_FORT_COMMANDER'):
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getUnitClassCount(getInfoType('UNITCLASS_SHADE')) >= 4:
		return False
	return True

def reqWarcry(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getNumUnits() < 25:
			return False
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		pTeam = gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) == 0:
			return False
	return True

def spellWarcry(caster):
	iWarcry = getInfoType('PROMOTION_WARCRY')
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if pUnit.getUnitCombatType() != -1:
			pUnit.setHasPromotion(iWarcry, True)

def reqWhiteout(caster):
	pPlot = caster.plot()
	if caster.isHasPromotion(getInfoType('PROMOTION_HIDDEN')):
		return False
	if pPlot.getTerrainType() != getInfoType('TERRAIN_TUNDRA') and pPlot.getTerrainType() != getInfoType('TERRAIN_GLACIER'):
		return False
	return True

def reqWildHunt(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.isHuman() == False:
		iTeam = gc.getPlayer(iPlayer).getTeam()
		pTeam = gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) == 0:
			return False
		if pPlayer.getNumUnits() < 20:
			return False
	return True

def spellWildHunt(caster):
	gc			= CyGlobalContext()
	iPlayer 	= caster.getOwner()
	pPlayer 	= gc.getPlayer(iPlayer)
	pDen 		= pPlayer.getCapitalCity()
	pPlot 		= pDen.plot()
	iNumAnimals = pPlayer.getNumUnits()
	Manager		= CvEventInterface.getEventManager()
	iAnimalChance = 0
	if pDen != None:
		iAnimalChance = pDen.getCityCounter()
	iAnimalChance += scaleInverse(2500)
	iReligion 	= pPlayer.getStateReligion()
	randNum		= CyGame().getSorenRandNum

	lList = Manager.cf.doAnimalListDoviello(iPlayer)

	for i in xrange(iNumAnimals):
		if randNum(10000, "Animal Spawn") < iAnimalChance:
			iUnit = lList[randNum(len(lList), "Pick Animal")-1]
			newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
			newUnit.setHasPromotion(getInfoType('PROMOTION_LOYALTY3'), True)
			if iReligion != -1:
				newUnit.setReligion(iReligion)
			if pPlayer.getCivics(getInfoType('CIVICOPTION_MEMBERSHIP')) == getInfoType('CIVIC_WILDCOUNCIL'):
				newUnit.setHasPromotion(getInfoType('PROMOTION_HEROIC_STRENGTH'), True)

def spellWonder(caster):
	bFavored = caster.isHasPromotion(getInfoType('PROMOTION_FAVORED_SON'))
	iCount = CyGame().getSorenRandNum(3, "Wonder") + 3
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	bCity = False
	point = pPlot.getPoint()
	iStartingCasts = caster.getCastingLimit()
	bStartingCast = caster.isHasCasted()
	if pPlot.isCity():
		bCity = True
	for i in xrange(iCount):
		iRnd = CyGame().getSorenRandNum(66, "Wonder")
		iUnit = -1
		if iRnd == 0:
			caster.cast(getInfoType('SPELL_BLAZE')) #gonna say this cancels out with bloom for bFavored
		elif iRnd == 1:
			caster.cast(getInfoType('SPELL_BLESS'))
		elif iRnd == 2:
			caster.cast(getInfoType('SPELL_BLINDING_LIGHT'))
		elif iRnd == 3:
			caster.cast(getInfoType('SPELL_BLOOM')) #gonna say this cancels out with blaze for bFavored
		elif iRnd == 4:
			caster.cast(getInfoType('SPELL_BLUR'))
		elif iRnd == 5:
			caster.cast(getInfoType('SPELL_CHARM_PERSON'))
		elif iRnd == 6:
			caster.cast(getInfoType('SPELL_CONTAGION'))
		elif iRnd == 7:
			caster.cast(getInfoType('SPELL_COURAGE'))
		elif iRnd == 8:
			caster.cast(getInfoType('SPELL_CRUSH'))
		elif iRnd == 9:
			caster.cast(getInfoType('SPELL_DESTROY_UNDEAD'))
		elif iRnd == 10:
			caster.cast(getInfoType('SPELL_DISPEL_MAGIC'))
		elif iRnd == 11:
			caster.cast(getInfoType('SPELL_EARTHQUAKE'))
		elif iRnd == 12:
			caster.cast(getInfoType('SPELL_ENCHANTED_BLADE'))
		elif iRnd == 13:
			if not bFavored:
				CyEngine().triggerEffect(getInfoType('EFFECT_SPELL1'),point)
				CyAudioGame().Play3DSound("AS3D_SPELL_DEFILE",point.x,point.y,point.z)
				getPlot = CyMap().plot
				iRange = 1 + caster.getSpellExtraRange()
				for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
					pLoopPlot = CyMap().plot(x, y)
					if not pLoopPlot.isNone():
						pLoopPlot.changePlotCounter(80)
			else:
				caster.cast(getInfoType('SPELL_ENTANGLE'))
		elif iRnd == 14:
			caster.cast(getInfoType('SPELL_ENTANGLE'))
		elif iRnd == 15:
			if not bFavored:
				caster.cast(getInfoType('SPELL_ESCAPE'))
			else:
				caster.cast(getInfoType('SPELL_FIREBALL'))
		elif iRnd == 16:
			caster.cast(getInfoType('SPELL_FIREBALL'))
		elif iRnd == 17:
			caster.cast(getInfoType('SPELL_FLAMING_ARROWS'))
		elif iRnd == 18:
			if not bFavored:
				caster.cast(getInfoType('SPELL_FLOATING_EYE'))
			else:
				caster.cast(getInfoType('SPELL_MORALE'))
		elif iRnd == 19:
			caster.cast(getInfoType('SPELL_HASTE'))
		elif iRnd == 20:
			caster.cast(getInfoType('SPELL_HASTURS_RAZOR'))
			if bFavored:
				caster.cast(getInfoType('SPELL_HEAL'))
		elif iRnd == 21:
			caster.cast(getInfoType('SPELL_HEAL'))
		elif iRnd == 22:
			caster.cast(getInfoType('SPELL_HIDE'))
		elif iRnd == 23:
			caster.cast(getInfoType('SPELL_LOYALTY'))
		elif iRnd == 24:
			caster.cast(getInfoType('SPELL_MAELSTROM'))
		elif iRnd == 25:
			caster.cast(getInfoType('SPELL_MORALE'))
		elif iRnd == 26:
			caster.cast(getInfoType('SPELL_MUTATION'))
		elif iRnd == 27:
			caster.cast(getInfoType('SPELL_PILLAR_OF_FIRE'))
		elif iRnd == 28:
			caster.cast(getInfoType('SPELL_POISONED_BLADE'))
		elif iRnd == 29:
			caster.cast(getInfoType('SPELL_REVELATION'))
		elif iRnd == 30:
			caster.cast(getInfoType('SPELL_RING_OF_FLAMES'))
		elif iRnd == 31:
			caster.cast(getInfoType('SPELL_RUST'))
		elif iRnd == 32:
			caster.cast(getInfoType('SPELL_SANCTIFY'))
		elif iRnd == 33:
			if not bFavored:
				caster.cast(getInfoType('SPELL_SCORCH'))
			else:
				caster.cast(getInfoType('SPELL_RUST'))
		elif iRnd == 34:
			caster.cast(getInfoType('SPELL_SHADOWWALK'))
		elif iRnd == 35:
			caster.cast(getInfoType('SPELL_SPORES'))
		elif iRnd == 36:
			if not bFavored:
				caster.cast(getInfoType('SPELL_SPRING'))
			else:
				caster.cast(getInfoType('SPELL_STONESKIN'))
		elif iRnd == 37:
			caster.cast(getInfoType('SPELL_STONESKIN'))
		elif iRnd == 38:
			caster.cast(getInfoType('SPELL_SUMMON_AIR_ELEMENTAL'))
		elif iRnd == 39:
			caster.cast(getInfoType('SPELL_SUMMON_AUREALIS'))
		elif iRnd == 40:
			caster.cast(getInfoType('SPELL_SUMMON_BALOR'))
		elif iRnd == 41:
			caster.cast(getInfoType('SPELL_SUMMON_DJINN'))
		elif iRnd == 42:
			caster.cast(getInfoType('SPELL_SUMMON_EARTH_ELEMENTAL'))
		elif iRnd == 43:
			caster.cast(getInfoType('SPELL_SUMMON_EINHERJAR'))
		elif iRnd == 44:
			caster.cast(getInfoType('SPELL_SUMMON_FIRE_ELEMENTAL'))
		elif iRnd == 45:
			iUnit = getInfoType('UNIT_KRAKEN')
		elif iRnd == 46:
			caster.cast(getInfoType('SPELL_SUMMON_MISTFORM'))
		elif iRnd == 47:
			caster.cast(getInfoType('SPELL_SUMMON_PIT_BEAST'))
		elif iRnd == 48:
			caster.cast(getInfoType('SPELL_SUMMON_SAND_LION'))
		elif iRnd == 49:
			caster.cast(getInfoType('SPELL_SUMMON_SPECTRE'))
		elif iRnd == 50:
			iUnit = getInfoType('UNIT_TIGER')
		elif iRnd == 51:
			iUnit = getInfoType('UNIT_TREANT')
		elif iRnd == 52:
			caster.cast(getInfoType('SPELL_SUMMON_WATER_ELEMENTAL'))
		elif iRnd == 53:
			caster.cast(getInfoType('SPELL_SUMMON_WRAITH'))
		elif iRnd == 54:
			caster.cast(getInfoType('SPELL_TSUNAMI'))
		elif iRnd == 55:
			caster.cast(getInfoType('SPELL_VALOR'))
		elif iRnd == 56:
			if not bFavored:
				caster.cast(getInfoType('SPELL_VITALIZE'))
			else:
				caster.cast(getInfoType('SPELL_SUMMON_MISTFORM'))
		elif iRnd == 57:
			caster.cast(getInfoType('SPELL_WITHER'))
		elif iRnd == 58:
			if not bFavored or bCity == False:
				iImprovement = pPlot.getImprovementType()
				bValid = True
				if iImprovement != -1 :
					if gc.getImprovementInfo(iImprovement).isPermanent() :
						bValid = False
				if bValid :
					pPlot.setImprovementType(getInfoType('IMPROVEMENT_PENGUINS'))
					CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_PENGUINS", ()),'',1,'Art/Interface/Buttons/Improvements/Penguins.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			else:
				caster.cast(getInfoType('SPELL_SWARM_OF_LOCUSTS'))
		elif iRnd == 59:
			if not bFavored or bCity == False:
				iImprovement = pPlot.getImprovementType()
				bValid = True
				if iImprovement != -1 :
					if gc.getImprovementInfo(iImprovement).isPermanent() :
						bValid = False
				if bValid :
					pPlot.setImprovementType(getInfoType('IMPROVEMENT_MUSHROOMS'))
					CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_MUSHROOMS", ()),'',1,'Art/Interface/Buttons/Improvements/Mushrooms.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			else:
				caster.cast(getInfoType('SPELL_STARE'))
		elif iRnd == 60:
			if not bFavored:
				for iProm in range(gc.getNumPromotionInfos()):
					if caster.isHasPromotion(iProm):
						if gc.getPromotionInfo(iProm).isRace():
							caster.setHasPromotion(iProm, False)
				caster.setUnitArtStyleType(getInfoType('UNIT_ARTSTYLE_BABOON'))
				CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_BABOON", ()),'',1,'Art/Interface/Buttons/Units/Margalard.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
				if pPlayer.isHuman():
					t = "TROPHY_FEAT_BABOON"
					if not CyGame().isHasTrophy(t):
						CyGame().changeTrophyValue(t, 1)
			else:
				# oh god, he goes again! Roughly 1/15 chance to trigger, so doesn't go infinitely, but...
				caster.cast(getInfoType('SPELL_WONDER'))
		elif iRnd == 61:
			if not bFavored:
				CyEngine().triggerEffect(getInfoType('EFFECT_SPELL1'),point)
				CyAudioGame().Play3DSound("AS3D_SPELL_SANCTIFY",point.x,point.y,point.z)
				getPlot = CyMap().plot
				iRange = 2 + caster.getSpellExtraRange()
				for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
					pLoopPlot = CyMap().plot(x, y)
					if pLoopPlot.isNone() == False:
						pLoopPlot.setPlotCounter(0)
			else:
				caster.cast(getInfoType('SPELL_BREATH_LIGHTNING'))
		elif iRnd == 62:
			caster.cast(getInfoType('SPELL_SEVER_SOUL'))
		elif iRnd == 63:
			caster.cast(getInfoType('SPELL_SLOW'))
		elif iRnd == 64:
			caster.cast(getInfoType('SPELL_SUMMON_ICE_ELEMENTAL'))
		elif iRnd == 65:
			caster.cast(getInfoType('SPELL_SNOWFALL'))



		if iUnit != -1:
			newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pPlayer.hasTrait(getInfoType('TRAIT_SUMMONER')):
				newUnit.setDuration(3)
			else:
				newUnit.setDuration(1)

# FF: Added by Jean Elcard 14/01/2009 (speed tweak)
	rebuildGraphics()
# FF: End Add

	caster.setCastingLimit(iStartingCasts)
	caster.setHasCasted(bStartingCast)


def reqWorldbreak(caster):
	if CyGame().getGlobalCounter() == 0:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if CyGame().getGlobalCounter() < 50:
			return False
	return True

def spellWorldbreak(caster):
	iCounter = CyGame().getGlobalCounter()
	iFire = getInfoType('DAMAGE_FIRE')
	iForest = getInfoType('FEATURE_FOREST')
	iJungle = getInfoType('FEATURE_JUNGLE')
	iPillar = getInfoType('EFFECT_PILLAR_OF_FIRE')
	iSmoke 	= getInfoType('IMPROVEMENT_SMOKE')
	Manager	= CvEventInterface.getEventManager()
	randNum	= CyGame().getSorenRandNum
	getPlot	= CyMap().plotByIndex
	for i in xrange(CyMap().numPlots()):
		pPlot = getPlot(i)
		bValid = True
		if pPlot.isOwned():
			if pPlot.getOwner() == caster.getOwner():
				bValid = False
		if bValid:
			if pPlot.isCity():
				if randNum(100, "Worldbreak") <= (iCounter / 4):
					Manager.cf.doCityFire(pPlot.getPlotCity())
				for i in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					pUnit.doDamageCity(iCounter, 100, caster, iFire, False)
				CyEngine().triggerEffect(iPillar,pPlot.getPoint())
			if (pPlot.getFeatureType() == iForest or pPlot.getFeatureType() == iJungle):
				if pPlot.getImprovementType() == -1:
					if randNum(100, "Flames Spread") <= (iCounter / 4):
						pPlot.setImprovementType(iSmoke)
						
def spellBreakRottingFlesh(pCaster,id):
	gc.getGame().changeGlobalFlagValue(gc.getInfoTypeForString("FLAG_URN_ROTTING_OPEN"),1)
	pPlot=pCaster.plot()		
	iPlayer=pCaster.getOwner()
	pPlayer=gc.getPlayer(iPlayer)
	if pPlayer.getFlagValue(gc.getInfoTypeForString("FLAG_URN_ROTTING_OPEN"))==7 and CyGame().getUnitCreatedCount(gc.getInfoTypeForString("UNIT_YERSINIA"))==0:
		if pPlayer.getStateReligion()==gc.getInfoTypeForString("RELIGION_THE_ASHEN_VEIL"):
			pPlayer.initUnit(gc.getInfoTypeForString("UNIT_YERSINIA"),pPlot.getX(),pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			bPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
			bPlayer.initUnit(gc.getInfoTypeForString("UNIT_YERSINIA"),pPlot.getX(),pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				
	
def atRangeGuardian(pCaster, pPlot):
	iX = pPlot.getX()
	iY = pPlot.getY()
	# if pPlot.getNumUnits() == 0: # Allow for gargoyles to spawn and push off units on the tile. Autokills fort commanders on it, but makes the event actually able to fire sensically...
	# Delays trigger in case of spawning too near it
	if CyGame().getGameTurn() > (10 * (1 + gc.getGame().isOption(GameOptionTypes.GAMEOPTION_THAW))) * gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent()/100:
		iPlayer = pCaster.getOwner()
		if not gc.getPlayer(iPlayer).isBarbarian():
			pPlot.setPythonActive(False) # Turn off trigger first so that gargoyles don't multispawn when units are shunted off of the pass
			bPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
			iUnit = getInfoType('UNIT_GARGOYLE')
			newUnit1 = bPlayer.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit1.changeStrBoost(3-CyGame().getSorenRandNum(10, "Gargoyle Weakening"))
			newUnit1.setHasPromotion(getInfoType('PROMOTION_SHARD_COURAGE'), True)
			newUnit1.setHasPromotion(getInfoType('PROMOTION_PRISTIN_LEASH'), True)
			newUnit2 = bPlayer.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit2.changeStrBoost(3-CyGame().getSorenRandNum(10, "Gargoyle Weakening"))
			newUnit2.setHasPromotion(getInfoType('PROMOTION_SHARD_STRENGTH'), True)
			newUnit2.setHasPromotion(getInfoType('PROMOTION_PRISTIN_LEASH'), True)
			newUnit3 = bPlayer.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit3.changeStrBoost(3-CyGame().getSorenRandNum(10, "Gargoyle Weakening"))
			newUnit3.setHasPromotion(getInfoType('PROMOTION_SHARD_WISDOM'), True)
			newUnit3.setHasPromotion(getInfoType('PROMOTION_PRISTIN_LEASH'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_GUARDIAN", ()),'',1,gc.getUnitInfo(iUnit).getButton(),ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)

def atRangeCitadel(pCaster, pPlot):
	iPlayer = pPlot.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pTeam = gc.getTeam(pPlayer.getTeam())
	p2Plot = pCaster.plot()
	if pTeam.isAtWar(pCaster.getTeam()):
		if pPlayer.isHuman() == True:
			if pPlot.getNumUnits() != 0:
				pCaster.doDamageNoCaster(10, 40, getInfoType('DAMAGE_FIRE'), False)
				CyEngine().triggerEffect(getInfoType('EFFECT_PILLAR_OF_FIRE'),p2Plot.getPoint())
		if pPlayer.isHuman() == False:
			pCaster.doDamageNoCaster(10, 40, getInfoType('DAMAGE_FIRE'), False)
			CyEngine().triggerEffect(getInfoType('EFFECT_PILLAR_OF_FIRE'),p2Plot.getPoint())

def atRangeJungleAltar(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.atRangeJungleAltar(pCaster, pPlot)

def atRangeNecrototem(pCaster, pPlot):
	if doFear(pCaster, pPlot, -1, False):
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_FEAR", (gc.getUnitInfo(pCaster.getUnitType()).getDescription(), )),'',1,'Art/Interface/Buttons/Improvements/Necrototem.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)

def atRangeWellOfSouls(pCaster, pPlot):
	if (pCaster.isAlive()):
		pCaster.setHasPromotion(gc.getInfoTypeForString("PROMOTION_DEAD_LANDS"),True)


def onMoveForest(pCaster, pPlot):
	if pPlot.isOwned():
		pPlayer		= gc.getPlayer(pCaster.getOwner())
		pTeam		= gc.getTeam(pPlayer.getTeam())
		p2Player	= gc.getPlayer(pPlot.getOwner())
		i2Team		= p2Player.getTeam()					
		if (pCaster.getOwner() != pPlot.getOwner() and pTeam.isAtWar(i2Team)):
			if (gc.getPlayer(pPlot.getOwner()).hasTrait(gc.getInfoTypeForString("TRAIT_SKIAMANCER"))):
				iChance = 5
				iUnit = gc.getInfoTypeForString("UNIT_SCEADUGENGAN")
				if (gc.getPlayer(pPlot.getOwner()).hasTrait(gc.getInfoTypeForString("TRAIT_SKIAMANCER3"))):
					iChance = 10
					iUnit = gc.getInfoTypeForString("UNIT_SHADOW_TREANT")
				if (CyGame().getSorenRandNum(100,"Rivanna Spawn Chance")<iChance):
					pPlot2=findClearPlot(-1, pPlot)
					pUnit=gc.getPlayer(pPlot.getOwner()).initUnit(iUnit,pPlot2.getX(), pPlot2.getY(),UnitAITypes.NO_UNITAI,DirectionTypes.DIRECTION_SOUTH)
					pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ILLUSION"),True)


def onMoveAncientForest(pCaster, pPlot):
	if pPlot.isOwned():
		pPlayer		= gc.getPlayer(pCaster.getOwner())
		pTeam		= gc.getTeam(pPlayer.getTeam())
		p2Player	= gc.getPlayer(pPlot.getOwner())
		i2Team		= p2Player.getTeam()					
		if (pCaster.getOwner() != pPlot.getOwner() and pTeam.isAtWar(i2Team)):
			if (gc.getPlayer(pPlot.getOwner()).hasTrait(gc.getInfoTypeForString("TRAIT_SKIAMANCER"))):
				iChance = 10
				iUnit = gc.getInfoTypeForString("UNIT_SCEADUGENGAN")
				if (gc.getPlayer(pPlot.getOwner()).hasTrait(gc.getInfoTypeForString("TRAIT_SKIAMANCER3"))):
					iChance = 20
					iUnit = gc.getInfoTypeForString("UNIT_SHADOW_TREANT")
				if (CyGame().getSorenRandNum(100,"Rivanna Spawn Chance")<iChance):
					pPlot2=findClearPlot(-1, pPlot)
					pUnit=gc.getPlayer(pPlot.getOwner()).initUnit(iUnit,pPlot2.getX(), pPlot2.getY(),UnitAITypes.NO_UNITAI,DirectionTypes.DIRECTION_SOUTH)
					pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_ILLUSION"),True)
					
		if pPlot.getNumUnits() == 1:
			if pCaster.isFlying() == False:
				iChance	= gc.getDefineINT('TREANT_SPAWN_CHANCE')
				if pPlot.isCityRadius():
					pCity		= CyMap().findCity(pPlot.getX(), pPlot.getY(), -1, -1, False, False, -1, -1, CyCity(), False)
					if pCity.getOwner() == pPlot.getOwner():
						if pCity.getNumBuilding(getInfoType('BUILDING_TEMPLE_OF_LEAVES')) > 0:
							iChance	= iChance * 3
				if CyGame().getSorenRandNum(100, "Treant Spawn Chance") < iChance:
					pPlayer		= gc.getPlayer(pCaster.getOwner())
					pTeam		= gc.getTeam(pPlayer.getTeam())
					p2Player	= gc.getPlayer(pPlot.getOwner())
					i2Team		= p2Player.getTeam()
					if (pTeam.isAtWar(i2Team) and p2Player.getStateReligion() == getInfoType('RELIGION_FELLOWSHIP_OF_LEAVES')):
						pCaster.finishMoves()
						newPlot	= findClearPlot(-1, pPlot)
						newUnit	= p2Player.initUnit(getInfoType('UNIT_TREANT'), newPlot.getX(), newPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setDuration(3)
						if getInfoType("MODULE_NOT_YET_EMERGENT_LEADERS")!=-1: # EmergentLeaders Module
							if p2Player.hasTrait(getInfoType("TRAIT_SYLVAN_SHADE")):
								newUnit.setDuration(10)
						CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TREANT_ENEMY",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Units/Treant.dds',ColorTypes(7),newUnit.getX(),newUnit.getY(),True,True)
						CyInterface().addMessage(pPlot.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TREANT",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Units/Treant.dds',ColorTypes(8),newUnit.getX(),newUnit.getY(),True,True)

# Frozen units should not be damaged by Blizzards. If the module is loaded, they will not be, otherwise, I use the original code. The line I changed is marked.
def onMoveBlizzard(pCaster, pPlot):
	if pCaster.isHasPromotion(getInfoType('PROMOTION_WINTERBORN')) == False:
		if gc.getPlayer(pCaster.getOwner()).getCivilizationType() != Civ["Frozen"]:
			pCaster.doDamage(10, 50, pCaster, getInfoType('DAMAGE_COLD'), False)

def onMoveLetumFrigus(pCaster, pPlot):
	pPlayer	= gc.getPlayer(pCaster.getOwner())
	git		= gc.getInfoTypeForString
	if not pPlayer.isHasFlag(git("FLAG_LETUM_FRIGUS_FIRST_TIME")):
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

def onMoveMaelstrom(pCaster, pPlot):
	if CyGame().getSorenRandNum(100, "Maelstrom") <= 25:
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_KILL",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
		pCaster.getGroup().clearMissionQueue();
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
			pCaster.getGroup().clearMissionQueue();
			pCaster.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True,False)
			pCaster.setDamage(25, PlayerTypes.NO_PLAYER)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_MOVE",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)

def onMovePoolOfTears(pCaster, pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	git				= gc.getInfoTypeForString
	lIllness		= [git("PROMOTION_DISEASED"),git("PROMOTION_PLAGUED"),git("PROMOTION_POISONED"),git("PROMOTION_WITHERED")]
	for iPromotion in lIllness:
		if pCaster.isHasPromotion(iPromotion):
			pCaster.setHasPromotion(iPromotion, false)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POOL_OF_TEARS_CURED",(gc.getUnitInfo(pCaster.getUnitType()).getTextKey(),gc.getPromotionInfo(iPromotion).getTextKey())),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/pooloftears.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)

	# Remnants from somme Elohim lore things?
	# pPlayer = gc.getPlayer(pCaster.getOwner())
	 #if pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_POOL_OF_TEARS) == False:
	#	if pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_ELOHIM"):
	#		iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_POOL_OF_TEARS_ELOHIM')
	#		triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCaster.getX(), pCaster.getY(), -1, -1, -1, -1, -1, -1)
	#		pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_POOL_OF_TEARS, True)



def onMoveJungleAltar(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.onMoveJungleAltar(pCaster, pPlot)

def onMovePortal(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.onMovePortal(pCaster, pPlot)

def onMoveWarningPost(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.onMoveWarningPost(pCaster, pPlot)

def onMoveCarcer(pCaster, pPlot):
	if (pCaster.getLevel() > 14 and not gc.getPlayer(pCaster.getOwner()).isBarbarian()):
		pPlot.setImprovementType(-1)
		pPlayer = gc.getPlayer(pCaster.getOwner())
		if CyGame().getUnitClassCreatedCount(getInfoType('UNITCLASS_BRIGIT')) == 0:
			if pPlot.isVisibleToWatchingHuman():
				CyEngine().triggerEffect(getInfoType('EFFECT_ICE_SUMMON'),pPlot.getPoint())
				CyAudioGame().Play3DSound("AS3D_ICEBREAK",pPlot.getPoint().x,pPlot.getPoint().y,pPlot.getPoint().z)
			newUnit = pPlayer.initUnit(getInfoType('UNIT_BRIGIT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pPlayer.isHuman():
				t = "TROPHY_FEAT_RESCUE_BRIGIT"
				if not CyGame().isHasTrophy(t):
					CyGame().changeTrophyValue(t, 1)

def onMoveSironasBeacon(pCaster, pPlot):
	# pPlayer = gc.getPlayer(pCaster.getOwner())
	# if pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_SIRONAS_BEACON) == False:

	#	if pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_ELOHIM"):
	#		iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_SIRONAS_BEACON_ELOHIM')
	#		triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCaster.getX(), pCaster.getY(), -1, -1, -1, -1, -1, -1)
	#		pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_SIRONAS_BEACON, True)
	return

def onMoveMirrorOfHeaven(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.onMoveMirrorOfHeaven(pCaster, pPlot)
		return
	iPlayer		= pCaster.getOwner()
	pPlayer		= gc.getPlayer(iPlayer)
	pCapital	= pPlayer.getCapitalCity()
	if not pCapital.isNone() and pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_MIRROR_OF_HEAVEN) == False and pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_MALAKIM"):
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
			effectMalakimMirror(argsList)

def effectMalakimMirror(argsList):
	iButtonId	= argsList[0]
	iPlayer		= argsList[1]
	pPlayer		= gc.getPlayer(iPlayer)
	git			= gc.getInfoTypeForString
	pCapital	= pPlayer.getCapitalCity()
	if iButtonId == 0:
		pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_MIRROR_OF_HEAVEN, False)
		return
	if iButtonId == 1:
		newUnit = pPlayer.initUnit(git('UNIT_LIGHTBRINGER'), pCapital.getX(), pCapital.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_MALAKIM_MIRROR_2_HERMIT_NAME",()))
		newUnit.setHasPromotion(git('PROMOTION_HERO'), True)
		newUnit.setHasPromotion(git('PROMOTION_MOBILITY1'), True)
	if iButtonId == 2:
		pCapital.setNumRealBuilding(git('BUILDING_MALAKIM_TEMPLE_MIRROR'), 1)

def onMoveRemnantsOfPatria(pCaster, pPlot):
	iPlayer	= pCaster.getOwner()
	pPlayer	= gc.getPlayer(iPlayer)
	git		= gc.getInfoTypeForString
	if pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_REMNANTS_OF_PATRIA) == False:
		if pPlayer.getCivilizationType() == git("CIVILIZATION_SCIONS"):
			pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_REMNANTS_OF_PATRIA, True)
			newUnit1 = pPlayer.initUnit(git('UNIT_SUPPLIES'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit2 = pPlayer.initUnit(git('UNIT_SUPPLIES'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REMNANTS_OF_PATRIA_SCIONS", ()),'',3,"Art/Interface/Buttons/Improvements/remnantsofpatria.dds",git("COLOR_GREEN"),pPlot.getX(),pPlot.getY(),True,True)

	
def onMoveOdiosPrison(pCaster, pPlot):
	# pPlayer = gc.getPlayer(pCaster.getOwner())
	# if pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_ODIOS_PRISON) == False:

	#	if pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_ELOHIM"):
	#		iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_ODIOS_PRISON_ELOHIM')
	#		triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCaster.getX(), pCaster.getY(), -1, -1, -1, -1, -1, -1)
	return

def onMoveBradelinesWell(pCaster, pPlot):
	# pPlayer = gc.getPlayer(pCaster.getOwner())
	# if pPlayer.isFeatAccomplished(FeatTypes.FEAT_VISIT_BRADELINES_WELL) == False:
	#	if pPlayer.getCivilizationType() == getInfoType("CIVILIZATION_ELOHIM"):
	#		iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_BRADELINES_WELL_ELOHIM')
	#		triggerData = pPlayer.initTriggeredData(iEvent, True, -1, pCaster.getX(), pCaster.getY(), -1, -1, -1, -1, -1, -1)
	#		pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_BRADELINES_WELL, True)
	#		pPlot.setImprovementType(getInfoType("IMPROVEMENT_BRADELINES_WELL_PURIFIED"))
	return

def onMoveFoxford(pCaster,pPlot):
	iPlayer			= pCaster.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	git				= gc.getInfoTypeForString
	iCaster			= pCaster.getID()
	pDemonPlayer	= gc.getPlayer(gc.getDEMON_PLAYER())
	if not pDemonPlayer.isHasFlag(git("FLAG_FOXFORD_FIRST_TIME")): # Flag is set globally, and even if a new player is presented to the game, the flag value for the demon player would be right
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
				popupInfo.setData3(106) # onModNetMessage id
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
				effectFoxford(argsList)

def effectFoxford(argsList):
	iButtonId	= argsList[0]
	iCaster		= argsList[1]
	iPlayer		= argsList[2]
	pPlayer		= gc.getPlayer(iPlayer)
	pCaster		= pPlayer.getUnit(iCaster)
	pPlot		= pCaster.plot()
	git			= gc.getInfoTypeForString
	if iButtonId == 2:
		gc.getGame().setGlobalFlag(git("FLAG_FOXFORD_FIRST_TIME"),False)
		return
	iRnd		= CyGame().getSorenRandNum(100, "Foxford General Roll")
	if iButtonId == 0:
		pCaster.setHasPromotion(git('PROMOTION_ADVENTURER'), True)
		pCaster.changeExperienceTimes100(500, -1, False, False, False)
		iGold = 20 + CyGame().getSorenRandNum(10, "Foxford Gold Roll")
		pPlayer.changeGold(iGold)
		if iRnd < 15:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_FOXFORD_WOLFKILLED", ()),'',3,'Art/Interface/Buttons/Promotions/Werewolf.dds',git("COLOR_RED"),pPlot.getX(),pPlot.getY(),True,True)
			pCaster.kill(False,-1)
		return
	if iButtonId == 1:
		pCaster.setHasPromotion(git('PROMOTION_WEREWOLF'), True)
		CyGame().setPlotExtraYield (pPlot.getX(),pPlot.getY(), git("YIELD_COMMERCE"), -3)
		pPlayer.setHasFlag(git("FLAG_FOXFORD_RAZED"),True)
		CyEngine().removeLandmark(pPlot)
		if iRnd < 33:
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_FOXFORD_LYNCHED", ()),'',3,'Art/Interface/Buttons/Actions/Pillage.dds',git("COLOR_RED"),pPlot.getX(),pPlot.getY(),True,True)
			pCaster.kill(False,-1)

def voteFundDissidents():
	iOvercouncil = getInfoType('DIPLOVOTE_OVERCOUNCIL')
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			if pPlayer.isFullMember(iOvercouncil):
				for pyCity in PyPlayer(iPlayer).getCityList() :
					if CyGame().getSorenRandNum(100, "Fund Dissidents") < 50:
						pCity = pyCity.GetCy()
						pCity.changeHurryAngerTimer(1 + CyGame().getSorenRandNum(3, "Fund Dissidents"))

def reqSummonPegasus(caster):
	pPlayer = PyPlayer(caster.getOwner())
	iCount = 0
	iMax = 0
	iPegasusRiderPromotion = getInfoType('PROMOTION_PEGASUS')
	iPegasusUnitType = getInfoType('UNIT_PEGASUS')
	iSummonLimitPromotion = getInfoType('PROMOTION_CHANNELING2')
	iSummonLimitPromotion2 = getInfoType('PROMOTION_AIR2')

	for pUnit in pPlayer.getUnitList():
		if pUnit.isHasPromotion(iPegasusRiderPromotion) or pUnit.getUnitType() == iPegasusUnitType:
			iCount += 1

		if pUnit.isHasPromotion(iSummonLimitPromotion) and pUnit.isHasPromotion(iSummonLimitPromotion2):
			iMax += 1

	if iCount < iMax:
		return True

def reqMountPegasus(caster):
	iPegasusRiderPromotion = getInfoType('PROMOTION_PEGASUS')
	if caster.isHasPromotion(iPegasusRiderPromotion):
		return False
	if caster.getUnitCombatType()==getInfoType("UNITCOMBAT_ANIMAL") or caster.getUnitCombatType()==getInfoType("UNITCOMBAT_BEAST")or caster.getUnitCombatType()==getInfoType("UNITCOMBAT_NAVAL")or caster.getUnitCombatType()==getInfoType("UNITCOMBAT_SIEGE"):
		return False
	return True

def spellMountPegasus(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iPegasus = getInfoType('UNIT_PEGASUS')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitType() == iPegasus):
			pUnit.setHasPromotion(getInfoType('PROMOTION_GOLEM'), True)
			pUnit.kill(False,0)
			return True
	return False

def reqKillPhoenix(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iPegasus = getInfoType('UNIT_PHOENIX')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitType() == iPegasus):
			if( pUnit.isHasPromotion(getInfoType('PROMOTION_PHOENIX_EGG_HELD'))):
				return True
	return False
	
def spellKillPhoenix(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iPegasus = getInfoType('UNIT_PHOENIX')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitType() == iPegasus):
			pUnit.kill(False,0)
			return True
	return False

def reqTempest(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		pTeam = gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) < 2:
			return False
	return True

def spellTempest(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iAirElementalChance = 9
	iAirElly = getInfoType('UNIT_AIR_ELEMENTAL')
	iTeam = pPlayer.getTeam()


	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		iOwner = pPlot.getOwner()

		if iOwner == iPlayer:
			if pPlot.getNumUnits() == 0:
				if CyGame().getSorenRandNum(100, "AirEllySpawn") < iAirElementalChance:
					newUnit = pPlayer.initUnit(iAirElly, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
					newUnit.setDuration(CyGame().getSorenRandNum(5, "AirEllySpawn") + 1)
			else:
				for i in range(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					iTeam2 = gc.getTeam(gc.getPlayer(pUnit.getOwner()).getTeam())
					if iTeam2.isAtWar(iTeam):
						pUnit.setImmobileTimer(CyGame().getSorenRandNum(5, "AirEllySpawn") + 1)

def reqFertility(caster):
	pPlot = caster.plot()
	iBonus = pPlot.getBonusType(-1)
	IFertilizable = IFarm+ICamp+IPasture+IPlantation+IFishing
	return iBonus in IFertilizable

def spellFertility(caster):
	pPlot = caster.plot()
	iBonus = pPlot.getBonusType(-1)

	if iBonus in IFarm:
		IImprovement = IFarm
	elif iBonus in ICamp:
		IImprovement = ICamp
	elif iBonus in IPasture:
		IImprovement = IPasture
	elif iBonus in IPlantation:
		IImprovement = IPlantation
	else: # (elif iBonus in IFishing:) #useful if the caster has water walking
		IImprovement = IFishing
	ii = IImprovement.index(iBonus)
	iBonusNext = IImprovement[(ii+1)%len(IImprovement)]
	pPlot.setBonusType(iBonusNext)

def reqBirth(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if pPlayer.isIgnoreFood():
		return False
	if pCity.getPopulation() > 7:
		return False
	return True

def getHelpFrozenLands(argsList):
	eSpell, pCaster = argsList
	if pCaster == -1 or pCaster.isNone():
		szHelp = ""
	else:
		if pCaster.isHasPromotion(getInfoType('PROMOTION_MASTER_OF_ICE')):
			szHelp = localText.getText("TXT_KEY_SPELL_FROZEN_LANDS_MASTER_HELP", ())
		else:
			szHelp = localText.getText("TXT_KEY_SPELL_FROZEN_LANDS_ICE3_HELP", ())
	return szHelp

def reqFrozenLands(caster):
	getPlayer   = gc.getPlayer
	iPlayer     = caster.getOwner()
	pPlayer		= getPlayer(iPlayer)
	iDesert     = getInfoType('TERRAIN_DESERT')
	iGrass      = getInfoType('TERRAIN_GRASS')
	iWetland    = getInfoType('TERRAIN_MARSH')
	iPlains     = getInfoType('TERRAIN_PLAINS')
	iTundra     = getInfoType('TERRAIN_TUNDRA')
	iTaiga      = getInfoType('TERRAIN_TAIGA')
	iTeam       = pPlayer.getTeam()
	pTeam       = gc.getTeam(iTeam)
	iRange		= 2 + caster.getSpellExtraRange()
	getPlot     = CyMap().plot
	validTerrain	= [iDesert, iGrass, iWetland, iPlains, iTundra, iTaiga]
	bValid		= False
	bEnemy		= False
	bOwn		= False
	for x,y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone() and not pPlot.isWater():
			iPlotOwner = pPlot.getOwner()
			if not pPlot.isOwned() or iPlotOwner == iPlayer or pTeam.isAtWar(getPlayer(iPlotOwner).getTeam()):
				iTerrain = pPlot.getTerrainType()
				if iTerrain in validTerrain:
					bValid = True
				if iPlotOwner == iPlayer:
					bOwn = True
				elif pPlot.isOwned() and pTeam.isAtWar(getPlayer(iPlotOwner).getTeam()):
					bEnemy = True
	if not pPlayer.isHuman():	# AI players who don't like snow will only use this spell if it hits at least one enemy and not themselves.
		bLikesSnow = pPlayer.getCivilizationType() == Civ["Illians"] or pPlayer.getStateReligion() == getInfoType('RELIGION_WHITE_HAND')
		if not bLikesSnow and (bOwn or not bEnemy):
			return False
	return bValid

def spellFrozenLands(caster):
	iPlayer     = caster.getOwner()
	iDesert     = getInfoType('TERRAIN_DESERT')
	iGrass      = getInfoType('TERRAIN_GRASS')
	iWetland    = getInfoType('TERRAIN_MARSH')
	iPlains     = getInfoType('TERRAIN_PLAINS')
	iTundra     = getInfoType('TERRAIN_TUNDRA')
	iTaiga      = getInfoType('TERRAIN_TAIGA')
	getPlayer   = gc.getPlayer
	iTeam       = getPlayer(iPlayer).getTeam()
	pTeam       = gc.getTeam(iTeam)
	getPlot     = CyMap().plot
	randNum     = CyGame().getSorenRandNum
	iRange		= 2 + caster.getSpellExtraRange()
	bIsMaster	= caster.isHasPromotion(getInfoType('PROMOTION_MASTER_OF_ICE'))
	for x,y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone():
			iPlotOwner = pPlot.getOwner()
			if not pPlot.isOwned() or iPlotOwner == iPlayer or pTeam.isAtWar(getPlayer(iPlotOwner).getTeam()):
				if  pPlot.getFeatureType() == getInfoType("FEATURE_SMOKE")or pPlot.getFeatureType() == getInfoType("FEATURE_FLAMES"):
					pPlot.setFeatureType(-1,-1)
				if randNum(100, "Plot affected chance") < 40:
					if not pPlot.isWater():
						iTerrain = pPlot.getTerrainType()
						if iTerrain == iTaiga:
							if bIsMaster:
								pPlot.setTerrainType(iTundra, True, True)
							else:
								pPlot.setTempTerrainType(iTundra, randNum(10, "Bob") + 10)
						if iTerrain == iGrass or iTerrain == iWetland or iTerrain == iPlains:
							if bIsMaster:
								pPlot.setTerrainType(iTaiga, True, True)
							else:
								pPlot.setTempTerrainType(iTaiga, randNum(10, "Bob") + 10)
						if iTerrain == iDesert:
							if bIsMaster:
								pPlot.setTerrainType(iPlains, True, True)
							else:
								pPlot.setTempTerrainType(iPlains, randNum(10, "Bob") + 10)

def spellWallOfForce(caster):
	pPlot = caster.plot()
	
# Scions start
def spellArawnsCall(caster):
	iSpell = getInfoType('SPELL_ARAWN_BECKONS')
	iCalled = getInfoType('PROMOTION_CALLED')
	pPlayer = gc.getPlayer(caster.getOwner())
	randNum	= CyGame().getSorenRandNum
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		for i in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.isHasPromotion(Race["Undead"]):
				iResist = pUnit.getResistChance(caster, iSpell)
				if randNum(100, "Arawan Beckons resist roll") > iResist:
					pUnit.setHasPromotion(iCalled, True)

def reqArawnsCall(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = pPlayer.getTeam()
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		for i in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.isHasPromotion(Race["Undead"]):
				if pUnit.getCivilizationType() != Civ["Scions"]:
					if pPlayer.isHuman():
						return True
					p2Player = gc.getPlayer(pUnit.getOwner())
					e2Team = gc.getTeam(p2Player.getTeam())
					if e2Team.isAtWar(pTeam):
						return True
	return False

# Spell for Awakened and Reborn
def reqAddPop(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if (pCity.happyLevel() - pCity.unhappyLevel(0)) < 1:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		if pCity.getOwner() != caster.getOwner():
			return False
	return True

# Used when some Pelemoc spells start a war.
def spellCB(caster):
	pPlot = caster.plot()
	startWar(caster.getOwner(), pPlot.getOwner(), WarPlanTypes.WARPLAN_LIMITED)

# Many of Pelemoc's spells require that he be in another civ's city.
def reqStrife(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	if pCity.getOwner() == caster.getOwner():
		return False
	return True

# req for Succor
def reqSuccor(caster):
	iUH = 0
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	iUH = pCity.goodHealth() - pCity.badHealth(False)
	if pCity.getOwner() == caster.getOwner():
		return False
	if iUH > -2:
		return False
	return True

# Pelemoc's Subversion spell.
def spellSubversion(caster,loc):
	pPlot = caster.plot()
	if CyGame().getSorenRandNum(4, "subversion war odds") < 1:
		startWar(caster.getOwner(), pPlot.getOwner(), WarPlanTypes.WARPLAN_LIMITED)

	player = caster.getOwner()
	pPlayer = gc.getPlayer(player)
	pCity = pPlayer.getCapitalCity()

	iReborn = getInfoType('UNIT_REBORN')
	spawnUnit = pPlayer.initUnit(iReborn, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# Pelemoc's Bring Out Your I'm Not Dead Yet spell.
def spellSuccor(caster,loc):
	pPlot = caster.plot()

	player = caster.getOwner()
	pPlayer = gc.getPlayer(player)
	pCity = pPlayer.getCapitalCity()

	iReborn = getInfoType('UNIT_REBORN')
	spawnUnit = pPlayer.initUnit(iReborn, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# Many spells also require that a particular building not already be present.  This one's for Emperor's Claim.
def reqEclaim(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	if pCity.getOwner() == caster.getOwner():
		return False
	if pCity.getNumRealBuilding(getInfoType('BUILDING_EMPERORS_CLAIM')) > 0:
		return False
	return True

# Req. for Rousing Oration.
def reqOrat(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	if pCity.getOwner() == caster.getOwner():
		return False
	if pCity.getNumRealBuilding(getInfoType('BUILDING_ROUSING_ORATION')) > 0:
		return False
	return True

# Req for Poison Words
def reqPwords(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	if pCity.getOwner() == caster.getOwner():
		return False
	if pCity.getNumRealBuilding(getInfoType('BUILDING_POISON_WORDS')) > 0:
		return False
	return True

# Req for Corrupt Guild
def reqPac(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	if pCity.getOwner() == caster.getOwner():
		return False
	if pCity.getNumRealBuilding(getInfoType('BUILDING_CORRUPT_GUILD')) > 0:
		return False
	return True

# Req for Melante's Estate.
def reqMelante(caster):
	pCity = caster.plot().getPlotCity()
	if pCity.getNumRealBuilding(getInfoType('BUILDING_PALACE_SCIONS')) > 0:
		return False
	if pCity.getNumRealBuilding(getInfoType('BUILDING_MELANTE')) > 0:
		return False
	return True

# Req for Thaumaturge's Keep
def reqAA(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()
	if (CyGame().isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE) and pPlayer.isFeatAccomplished(FeatTypes.FEAT_BUILT_KEEP) == False):
		return True
	if pCity.getNumRealBuilding(getInfoType('BUILDING_PALACE_SCIONS')) > 0:
		return False
	if pPlayer.isFeatAccomplished(FeatTypes.FEAT_BUILT_KEEP) == True:
		return False
	return True

# Sets up the Thaumaturge's Keep campus.
def spellAA(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.setFeatAccomplished(FeatTypes.FEAT_BUILT_KEEP, True)
	pCity = caster.plot().getPlotCity()
	caster.cast(getInfoType('SPELL_BUILD_KEEP_MAIN'))
# The line above creates the base Keep building.  The randomly-slected-from lists below add the  buildings - 1 or 2 mana and 1 to 3 other buildings.
	iChance = CyGame().getSorenRandNum(11, "Keep building roll")
	if iChance <= 0:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_FORCE'))
	if iChance == 1:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_ENTROPY'))
	if iChance == 2:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_EARTH'))
	if iChance == 3:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_AIR'))
	if iChance == 4:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_FIRE'))
	if iChance == 5:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_WATER'))
	if iChance == 6:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_SHADOW'))
	if iChance == 7:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_CHAOS'))
	if iChance == 8:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_BODY'))
	if iChance == 9:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_MIND'))
	if iChance == 10:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_ENCHANTMENT'))
	if iChance == 11:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_METAMAGIC'))

	iChance2 = CyGame().getSorenRandNum(13, "Keep building roll 2")
	if iChance2 == iChance:
		iChance2 = 14
	if iChance2 <= 0:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_FORCE'))
	if iChance2 == 1:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_ENTROPY'))
	if iChance2 == 2:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_EARTH'))
	if iChance2 == 3:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_AIR'))
	if iChance2 == 4:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_FIRE'))
	if iChance2 == 5:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_WATER'))
	if iChance2 == 6:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_SHADOW'))
	if iChance2 == 7:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_CHAOS'))
	if iChance2 == 8:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_BODY'))
	if iChance2 == 9:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_MIND'))
	if iChance2 == 10:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_ENCHANTMENT'))
	if iChance2 == 11:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_METAMAGIC'))
	if iChance2 == 12:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_SCHOLA_FURO'))
	if iChance2 == 13:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_ALCINUS_TROVE'))
	if iChance2 == 14:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_DEATH'))

	iChance3 = CyGame().getSorenRandNum(3, "Keep building roll 3")
	if iChance3 <= 0:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_MILITARY_ABATTOIR'))
	if iChance3 == 1:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_ALCHEMIST'))

	iChance4 = CyGame().getSorenRandNum(3, "Keep building roll 4")
	if iChance4 <= 0:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_NOXIOUS_SMELL'))
	if iChance4 == 1:
		caster.cast(getInfoType('SPELL_BUILD_KEEP_CORROSIVE_SPILL'))


# req for Emperor's Mark.
def reqEmark(caster):
	pCity = caster.plot().getPlotCity()
	if pCity.getNumRealBuilding(getInfoType('BUILDING_EMPERORS_MARK')) > 0:
		return False
	return True

# Redactor's Haunted Land creating spell. AoE with reduced effectiveness as range increases
def spellHL(caster):
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not plotValidForHL(pPlot):
			continue
		iDist = stepDistance(x, y, caster.getX(), caster.getY())
		# Always center, 1/2 at range 1, 1/3 at range 2, etc
		if CyGame().getSorenRandNum(iDist, "Reduced HL spread odds at range") == 0:
			pPlot.setPlotEffectType(getInfoType('PLOT_EFFECT_HAUNTED_LANDS'))

# Creeper's HL spell.
def spellHL3(caster):
	pPlot = caster.plot()
	if plotValidForHL(pPlot):
		pPlot.setPlotEffectType(getInfoType('PLOT_EFFECT_HAUNTED_LANDS'))

# Ghostwalker's HL spell.  Also creates Creepers.
def spellHL2(caster):
	# iCreeper = getInfoType('UNIT_CREEPER')
	pPlot = caster.plot()
	if plotValidForHL(pPlot):
		pPlot.setPlotEffectType(getInfoType('PLOT_EFFECT_HAUNTED_LANDS'))
	# pPlayer = gc.getPlayer(caster.getOwner())
	# iChance = CyGame().getSorenRandNum(3, "Create Creeper from HL spell Chance")
	# if iChance == 0:
	# 	newUnit = pPlayer.initUnit(getInfoType('UNIT_CREEPER'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# Creates Creepers when Ghostwalker killed.
def spelldeadG(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	# iChance = CyGame().getSorenRandNum(3, "Chance")
	# if iChance == 1:
	# caster.cast(getInfoType('SPELL_CREEPER'))
	# caster.cast(getInfoType('SPELL_CREEPER'))
	# newUnit = pPlayer.initUnit(getInfoType('UNIT_CREEPER'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def plotValidForHL(pPlot):
	if pPlot.isPeak():
		return False
	# HL can exist on water..... but this can confuse ghostwalkers, and IMO looks weird. Let it only naturally grow there
	if pPlot.isWater():
		return False
	if pPlot.isCity():
		return False
	# Volcano, Ice
	if pPlot.isImpassable():
		return False
	# Can't convert another plot effect
	if pPlot.getPlotEffectType() != -1:
		return False
	return True

# Keeps HL spell from being cast on water or in a HL tile.
def reqHL(caster):
	return plotValidForHL(caster.plot())

# Req for Give Gift spell.
def reqGiveGift(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iGhastlyDragoon = getInfoType('PROMOTION_GHASTLY_DRAGOON')
	iNaval = getInfoType('UNITCOMBAT_NAVAL')
	iMounted = getInfoType('UNITCOMBAT_MOUNTED')
	iSiege = getInfoType('UNITCOMBAT_SIEGE')
	iGolem = getInfoType('PROMOTION_GOLEM')
	iRedLady = getInfoType('UNIT_KORRINA_RED_LADY')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() or pUnit.getUnitCombatType() == iSiege or pUnit.getRace() == iGolem or pUnit.getUnitCombatType() == iNaval):
			if pUnit.isHasPromotion(Race["Undead"]) == False:
				if pUnit.getCivilizationType() == Civ["Scions"]:
					if pUnit.getUnitType() != iRedLady:
						return True
		if pUnit.getCivilizationType() == Civ["Scions"]:
			if pUnit.getUnitCombatType() == iMounted:
				if pUnit.isHasPromotion(iGhastlyDragoon) == False:
					return True
	return False

# Redactor spell that makes some non-undead units Undead.
def spellGiveGift(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iGhastlyDragoon = getInfoType('PROMOTION_GHASTLY_DRAGOON')
	iNaval = getInfoType('UNITCOMBAT_NAVAL')
	iMounted = getInfoType('UNITCOMBAT_MOUNTED')
	iSiege = getInfoType('UNITCOMBAT_SIEGE')
	iGolem = getInfoType('PROMOTION_GOLEM')
	iRedLady = getInfoType('UNIT_KORRINA_RED_LADY')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)

		if (pUnit.isAlive() or pUnit.getUnitCombatType() == iSiege or pUnit.getRace() == iGolem or pUnit.getUnitCombatType() == iNaval):
				if pUnit.getCivilizationType() == Civ["Scions"]:
					if pUnit.getUnitType() != iRedLady:
						pUnit.setHasPromotion(Race["Undead"], True)
		if pUnit.getCivilizationType() == Civ["Scions"]:
			if pUnit.getUnitCombatType() == iMounted:
				pUnit.setHasPromotion(iGhastlyDragoon, True)

# Wraithlord's body 3 spell works via a pyperturn promo.
def effectUPush(caster):
	caster.cast(getInfoType('SPELL_GRAND_WARD'))

def reqUPush(caster):
	if caster.isHasPromotion(getInfoType('PROMOTION_GRAND_WARD')):
		return False
	return True

# Used to keep Scions from using normal Body spells.  (Not needed anymore, I believe.)
def reqnotScions(caster):
	if caster.getCivilizationType() == Civ["Scions"]:
		return False
	return True

# Ghostwalkers can only become Haunts on a HL tile.
def reqHaunt(caster):
	pPlot = caster.plot()
	if pPlot.getPlotEffectType() != getInfoType('PLOT_EFFECT_HAUNTED_LANDS'):
		return False
	return True

# Changes Ghostwalker to a Haunt.
def spellHaunt(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_HAUNT'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	for iProm in range(gc.getNumPromotionInfos()):
		if (caster.isHasPromotion(iProm) and not gc.getPromotionInfo(iProm).isEquipment()):
			iPromCount = caster.countHasPromotion(iProm)
			for i in xrange(iPromCount):
				newUnit.setHasPromotion(iProm, True)
	newUnit.setDamageReal(caster.getDamageReal(), caster.getOwner())
	newUnit.setHasPromotion(getInfoType('PROMOTION_HAUNT'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_SUBDUE_ANIMAL'), False)
	newUnit.setLevel(caster.getLevel())
	newUnit.setExperienceTimes100(caster.getExperienceTimes100(), -1)# Changes Ghostwalker to a Haunt.

def reqHauntKorrina(caster):
	if caster.isMadeAttack():
		return False
	return True

def spellHauntKorrina(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_HAUNT_KORRINA'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	for iProm in range(gc.getNumPromotionInfos()):
		if (caster.isHasPromotion(iProm) and not gc.getPromotionInfo(iProm).isEquipment()):
			iPromCount = caster.countHasPromotion(iProm)
			for i in xrange(iPromCount):
				newUnit.setHasPromotion(iProm, True)
	newUnit.setDamageReal(caster.getDamageReal(), caster.getOwner())
	newUnit.setHasPromotion(getInfoType('PROMOTION_HAUNT_KORRINA'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_INVISIBLE'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_STEALTH'), False)
	newUnit.setLevel(caster.getLevel())
	newUnit.setExperienceTimes100(caster.getExperienceTimes100(), -1)
	newUnit.setHasCasted(True)

def spellKorrinaHaunt(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_KORRINA_BLACK_LADY'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	for iProm in range(gc.getNumPromotionInfos()):
		if (caster.isHasPromotion(iProm) and not gc.getPromotionInfo(iProm).isEquipment()):
			iPromCount = caster.countHasPromotion(iProm)
			for i in xrange(iPromCount):
				newUnit.setHasPromotion(iProm, True)
	newUnit.setDamageReal(caster.getDamageReal(), caster.getOwner())
	newUnit.setHasPromotion(getInfoType('PROMOTION_HAUNT_KORRINA'), False)
	newUnit.setHasPromotion(getInfoType('PROMOTION_INVISIBLE'), False)
	newUnit.setHasPromotion(getInfoType('PROMOTION_STEALTH'), True)
	newUnit.setLevel(caster.getLevel())
	newUnit.setExperienceTimes100(caster.getExperienceTimes100(), -1)
	newUnit.setHasCasted(True)
	newUnit.setMadeAttack(True)

# For the Chan 1 version of Alcinus.
def resMit(caster):
	if CyGame().GetWorldBuilderMode():
		return 0
	bContinue = True
	gc.getGame().decrementUnitClassCreatedCount(caster.getUnitClassType())
	gc.getGame().decrementUnitClassCreatedCount(caster.getUnitClassType())
	if CyGame().getSorenRandNum(100, "Alcinus death defection Check") <= 25 or (caster.isHasPromotion(getInfoType('PROMOTION_ALCINUS_HOSTILE')) == True):
		for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive()):
				if pPlayer.getCivilizationType() == Civ["Scions"]:
					pCity = pPlayer.getCapitalCity()
					newUnit = pPlayer.initUnit(getInfoType('UNIT_ALCINUS'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					caster.setDamage(95, -1)
					newUnit.convert(caster)
					bContinue = False
	if bContinue:
		listPlayers = []
		for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive()):
				listPlayers.append(pPlayer)
		iGift = CyGame().getSorenRandNum(len(listPlayers), "Who gets Alcinus Gift")
		pCity = listPlayers[iGift].getCapitalCity()
		pPlayer = listPlayers[iGift]
		newUnit = pPlayer.initUnit(getInfoType('UNIT_ALCINUS'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		caster.setDamage(95, -1)
		newUnit.convert(caster)
	return 1

# For the Mage version of Alcinus.
def MIT2(caster):
	if CyGame().GetWorldBuilderMode():
		return 0
	bContinue = True
	gc.getGame().decrementUnitClassCreatedCount(caster.getUnitClassType())
	gc.getGame().decrementUnitClassCreatedCount(caster.getUnitClassType())
	if CyGame().getSorenRandNum(100, "Alcinus death defection Check") <= 25 or (caster.isHasPromotion(getInfoType('PROMOTION_ALCINUS_HOSTILE')) == True):
		for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive()):
				if pPlayer.getCivilizationType() == Civ["Scions"]:
					pCity = pPlayer.getCapitalCity()
					newUnit = pPlayer.initUnit(getInfoType('UNIT_ALCINUS_UPGRADED'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					caster.setDamage(95, -1)
					newUnit.convert(caster)
					bContinue = False
	if bContinue:
		listPlayers = []
		for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive()):
				listPlayers.append(pPlayer)
		iGift = CyGame().getSorenRandNum(len(listPlayers) * 1, "Alcinus death Gift")
		pCity = listPlayers[iGift].getCapitalCity()
		pPlayer = listPlayers[iGift]
		newUnit = pPlayer.initUnit(getInfoType('UNIT_ALCINUS_UPGRADED'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		caster.setDamage(95, -1)
		newUnit.convert(caster)
		return 1

# For the Archmage version of Alcinus.
def MIT3(caster):
	if CyGame().GetWorldBuilderMode():
		return 0
	bContinue = True
	gc.getGame().decrementUnitClassCreatedCount(caster.getUnitClassType())
	gc.getGame().decrementUnitClassCreatedCount(caster.getUnitClassType())
	if CyGame().getSorenRandNum(100, "Alcinus death defection Check") <= 25 or (caster.isHasPromotion(getInfoType('PROMOTION_ALCINUS_HOSTILE')) == True):
		for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive()):
				if pPlayer.getCivilizationType() == Civ["Scions"]:
					pCity = pPlayer.getCapitalCity()
					newUnit = pPlayer.initUnit(getInfoType('UNIT_ALCINUS_ARCHMAGE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					caster.setDamage(95, -1)
					newUnit.convert(caster)
					bContinue = False
	if bContinue:
		listPlayers = []
		for iPlayer in range(gc.getMAX_CIV_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive()):
				listPlayers.append(pPlayer)
		iGift = CyGame().getSorenRandNum(len(listPlayers) * 1, "Alcinus death Gift")
		pCity = listPlayers[iGift].getCapitalCity()
		pPlayer = listPlayers[iGift]
		newUnit = pPlayer.initUnit(getInfoType('UNIT_ALCINUS_ARCHMAGE'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		caster.setDamage(95, -1)
		newUnit.convert(caster)
		return 1

# Per-turn check to return non-barbarian Haunts to Ghostwalker.
def checkHaunt(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isBarbarian():
		return
	if CyGame().getSorenRandNum(4, "Haunt to Ghostwalker Check") >= 1:
		return
	newUnit = pPlayer.initUnit(getInfoType('UNIT_GHOSTWALKER'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	for iProm in range(gc.getNumPromotionInfos()):
		if (caster.isHasPromotion(iProm) and not gc.getPromotionInfo(iProm).isEquipment()):
			iPromCount = caster.countHasPromotion(iProm)
			for i in xrange(iPromCount):
				newUnit.setHasPromotion(iProm, True)
	newUnit.setDamageReal(caster.getDamageReal(), caster.getOwner())
	newUnit.setHasPromotion(getInfoType('PROMOTION_SUBDUE_ANIMAL'), True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_HAUNT'), False)
	newUnit.setLevel(caster.getLevel())
	newUnit.setExperienceTimes100(caster.getExperienceTimes100(), -1)
	caster.kill(True, 0)

# MoP don't always use suicide attacks, and never aginast workers and hawks.
def mopsuicide(pCaster, pOpponent):
	if (pOpponent.getUnitClassType() == getInfoType('UNITCLASS_HAWK')):
		return
	if (pOpponent.getUnitCombatType() == getInfoType('UNITCOMBAT_WORKER')):
		return
	if CyGame().getSorenRandNum(3, "MoP suicide attack Check") > 1:
		pCaster.kill(True, 0)

# Req for Feeding Creepers.
def reqPlant(caster):
	pPlot = caster.plot()
#	iCreeper = getInfoType('UNIT_CREEPER')
#	iPPromo = getInfoType('PROMOTION_FED_CREEPER')
#	iPSent = getInfoType('PROMOTION_SENTRY2')
#	if caster.getExperience() < 4:
#			return False
#	for i in range(pPlot.getNumUnits()):
#		pUnit = pPlot.getUnit(i)
#		if pUnit.getUnitType() == iCreeper:
#			if pUnit.isHasPromotion(iPSent):
#				return True
	return False

# Req for Dark Council spell.  Makes sure the whole Council is assembled in 1 square.
## VEHEM: Rewritten to use named booleans to keep track of each member - easier to read.

def reqDarkC(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	iPelemoc = getInfoType('UNIT_PELEMOC')
	iThemoch = getInfoType('UNIT_THEMOCH')
	iAlcinus = getInfoType('UNIT_ALCINUS')
	iAlcinus2 = getInfoType('UNIT_ALCINUS_UPGRADED')
	iAlcinus3 = getInfoType('UNIT_ALCINUS_ARCHMAGE')

	if pPlayer.isHuman() == False:
		return True

	if(pPlayer.getNumBuilding(getInfoType("BUILDING_DARK_COUNCIL"))>0):
		return False

	bPelemocPresent = False
	bThemochPresent = False
	bAlcinusPresent = False

	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)

		if pUnit.getUnitType() == iPelemoc:
			bPelemocPresent = True

		if pUnit.getUnitType() == iThemoch:
			bThemochPresent = True

		if pUnit.getUnitType() == iAlcinus or pUnit.getUnitType() == iAlcinus2 or pUnit.getUnitType() == iAlcinus3:
			bAlcinusPresent = True

	if bPelemocPresent and bThemochPresent and bAlcinusPresent:
		return True

	return False

def reqSpiralGate(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = gc.getTeam(pPlayer.getTeam())

	if pPlayer.isHuman() == False:
		iCastingChance = -1
		if pTeam.isHasTech(getInfoType('TECH_ARCANE_LORE')) == True:
			iCastingChance += 1
		if pTeam.isHasTech(getInfoType('TECH_RELIGIOUS_LAW')) == True:
			iCastingChance += 2
		if pTeam.isHasTech(getInfoType('TECH_MITHRIL_WORKING')) == True:
			iCastingChance += 2
		if pTeam.isHasTech(getInfoType('TECH_GUILDS')) == True:
			iCastingChance += 2
		if pTeam.isHasTech(getInfoType('TECH_ENGINEERING')) == True:
			iCastingChance += 2
		if CyGame().getSorenRandNum(199, "AI chance for Spiral Gate") < iCastingChance:
			return True

	return True

def spellSpiralGate(argslist):
	if isinstance( argslist, tuple ):
		makeHelpText = True
		eSpell, caster = argslist
	else:
		caster = argslist
		makeHelpText=False
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pTeam = gc.getTeam(pPlayer.getTeam())

	bonusCategory = dict()
	bonusCategory['false laroth'] = dict()
	bonusCategory['archer'] = dict()
	bonusCategory['adept'] = dict()
	bonusCategory['melee'] = dict()
	bonusCategory['recon'] = dict()
	bonusCategory['mounted'] = dict()
	bonusCategory['supplies'] = dict()
	bonusCategory['population'] = dict()
	bonusCategory['creeper'] = dict()
	unitUpgrades = dict()

	# A list of units to be given
	# Each unit is described with a tuple
	# ( unitString, bonusCategoryName, promotionList, name)
	giveUnits = []
	giveUnits.append( ( 'UNIT_NECROMANCER', 'false laroth', ['PROMOTION_DEATH1', 'PROMOTION_DEATH2', 'PROMOTION_SPIRIT1', 'PROMOTION_SPIRIT2', 'PROMOTION_SHADOW1', 'PROMOTION_SHADOW2', 'PROMOTION_COMBAT1', 'PROMOTION_COMBAT2', 'PROMOTION_HIDDEN', 'PROMOTION_ADVENTURER', ], CyTranslator().getText('TXT_KEY_UNIT_FALSE_LAROTH',() ) ) )
	bonusCategory['false laroth']['xp'] = 10
	if pTeam.isHasTech(getInfoType('TECH_ARCHERY') ):
		giveUnits.append( ( 'UNIT_ARCHER', 'archer', ['PROMOTION_ADVENTURER', ],  'Anyon' ) )
		giveUnits.append( ( 'UNIT_ARCHER', 'archer', ['PROMOTION_ADVENTURER', ],  'Lann' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_ROOTED'],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_YOUNG'],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_BRONZE_WORKING') ):
		giveUnits.append( ( 'UNIT_HONORED_BAND', 'melee', ['PROMOTION_ADVENTURER', ],  'Medb' ) )
		giveUnits.append( ( 'UNIT_HONORED_BAND', 'melee', ['PROMOTION_ADVENTURER', ],  'Aife' ) )
		bonusCategory['melee']['weapons'] = 'PROMOTION_BRONZE_WEAPONS'
		bonusCategory['false laroth']['weapons'] = 'PROMOTION_BRONZE_WEAPONS'
	if pTeam.isHasTech(getInfoType('TECH_IRON_WORKING') ):
		giveUnits.append( ( 'UNIT_PRINCIPES', 'melee', ['PROMOTION_ADVENTURER', ],  'Scathach' ) )
		giveUnits.append( ( 'UNIT_PRINCIPES', 'melee', ['PROMOTION_ADVENTURER', ],  'Voadica' ) )
		giveUnits.append( ( 'UNIT_HONORED_BAND', 'melee', [],  '' ) )
		bonusCategory['melee']['weapons'] = 'PROMOTION_IRON_WEAPONS'
		bonusCategory['false laroth']['weapons'] = 'PROMOTION_IRON_WEAPONS'
	if pTeam.isHasTech(getInfoType('TECH_TRADE')):
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_STIRRUPS')):
		giveUnits.append( ( 'UNIT_HORSE_ARCHER', 'mounted', [],  '' ) )
		giveUnits.append( ( 'UNIT_HORSE_ARCHER', 'mounted', [],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_BLOOMING'],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_WARHORSES')):
		giveUnits.append( ( 'UNIT_HORSE_ARCHER', 'mounted', [],  '' ) )
		giveUnits.append( ( 'UNIT_HORSE_ARCHER', 'mounted', [],  '' ) )
		giveUnits.append( ( 'UNIT_HORSE_ARCHER', 'mounted', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_ARMORED_CAVALRY')):
		giveUnits.append( ( 'UNIT_HORSE_ARCHER', 'mounted', ['PROMOTION_COMBAT1', ],  '' ) )
		giveUnits.append( ( 'UNIT_HORSE_ARCHER', 'mounted', ['PROMOTION_COMBAT1', ],  '' ) )
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
		bonusCategory['mounted']['xp'] = 10
	if pTeam.isHasTech(getInfoType('TECH_ANIMAL_HANDLING')):
		giveUnits.append( ( 'UNIT_CETRATUS', 'recon', [],  '' ) )
		giveUnits.append( ( 'UNIT_CETRATUS', 'recon', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_FERAL_BOND')):
		giveUnits.append( ( 'UNIT_GHOSTWALKER', 'recon', [],  '' ) )
		giveUnits.append( ( 'UNIT_GHOSTWALKER', 'recon', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_ANIMAL_MASTERY')):
		giveUnits.append( ( 'UNIT_GHOSTWALKER', 'recon', ['PROMOTION_ADVENTURER', ],  'Gurith' ) )
		giveUnits.append( ( 'UNIT_GHOSTWALKER', 'recon', ['PROMOTION_ADVENTURER', 'PROMOTION_COMBAT1', 'PROMOTION_COMBAT2', ],  'Fathen' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_BLOOMING'],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_SMELTING')):
		giveUnits.append( ( 'UNIT_HONORED_BAND', 'melee', [],  '' ) )
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_MATURE'],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_SANITATION')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_MEDICINE')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_MITHRIL_WORKING')):
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
		giveUnits.append( ( 'UNIT_PHALANX', 'melee', [ ],  '' ) )
		giveUnits.append( ( 'UNIT_PHALANX', 'melee', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		bonusCategory['melee'].setdefault( 'promotions', [] ).append( 'PROMOTION_ENCHANTED_BLADE' )
	if pTeam.isHasTech(getInfoType('TECH_ASTRONOMY')):
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_BOWYERS')):
		giveUnits.append( ( 'UNIT_LONGBOWMAN', 'archer', [],  '' ) )
		giveUnits.append( ( 'UNIT_LONGBOWMAN', 'archer', [],  '' ) )
		giveUnits.append( ( 'UNIT_LONGBOWMAN', 'archer', [],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_PRECISION')):
		giveUnits.append( ( 'UNIT_LONGBOWMAN', 'archer', [],  '' ) )
		giveUnits.append( ( 'UNIT_LONGBOWMAN', 'archer', [],  '' ) )
		giveUnits.append( ( 'UNIT_MARKSMAN', 'archer', ['PROMOTION_ADVENTURER', ],  'Tadc' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_TAXATION')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_BLOOMING'],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_GUILDS')):
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_MERCANTILISM')):
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_MILITARY_STRATEGY')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		bonusCategory['melee']['xp'] = 6
		bonusCategory['archer']['xp'] = 6
		bonusCategory['recon']['xp'] = 6
	if pTeam.isHasTech(getInfoType('TECH_ENGINEERING')):
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
		giveUnits.append( ( 'UNIT_CATAPULT', 'supplies', ['PROMOTION_ASSAULT1', ],  '' ) )
		giveUnits.append( ( 'UNIT_CATAPULT', 'supplies', ['PROMOTION_BARRAGE1', ],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_BLOOMING'],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_BLASTING_POWDER')):
		giveUnits.append( ( 'UNIT_BONE_HORDE', 'archer', [],  '' ) )
		giveUnits.append( ( 'UNIT_BONE_HORDE', 'archer', [],  '' ) )
		giveUnits.append( ( 'UNIT_BONE_HORDE', 'archer', [],  '' ) )
		giveUnits.append( ( 'UNIT_BONE_HORDE', 'archer', [],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_MATURE'],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_SORCERY')):
		unitUpgrades['UNIT_ADEPT'] = 'UNIT_NECROMANCER'
	if pTeam.isHasTech(getInfoType('TECH_ARCANE_LORE')):
		giveUnits.append( ( 'UNIT_NECROMANCER', 'adept', ['PROMOTION_DEATH1', 'PROMOTION_DEATH2', ], '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_STRENGTH_OF_WILL')):
		giveUnits.append( ( 'UNIT_NECROMANCER', 'adept', ['PROMOTION_DEATH1', 'PROMOTION_DEATH2', 'PROMOTION_COMBAT1', ], '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_PASS_THROUGH_THE_ETHER')):
		giveUnits.append( ( 'UNIT_NECROMANCER', 'adept', ['PROMOTION_DEATH1', 'PROMOTION_COMBAT2', 'PROMOTION_COMBAT1', ], '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_MACHINERY')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_CATAPULT', 'supplies', [],  '' ) )
		giveUnits.append( ( 'UNIT_CATAPULT', 'supplies', [],  '' ) )
		giveUnits.append( ( 'UNIT_SPIRAL_SUPPLIES', 'supplies', [],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_YOUNG'],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_OMNISCIENCE')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_NECROMANCER', 'adept', ['PROMOTION_DEATH1', 'PROMOTION_DEATH2', 'PROMOTION_COMBAT1', 'PROMOTION_COMBAT2', 'PROMOTION_COMBAT3', ], '' ) )
		giveUnits.append( ( 'UNIT_NECROMANCER', 'adept', ['PROMOTION_DEATH1', 'PROMOTION_DEATH2', 'PROMOTION_COMBAT1', 'PROMOTION_FIRE1', 'PROMOTION_FIRE2', 'PROMOTION_ADVENTURER', ], 'Tetricues' ) )
	if pTeam.isHasTech(getInfoType('TECH_DIVINATION')):
		bonusCategory['adept']['xp'] = bonusCategory['adept'].get('xp', 0 ) +2
	if pTeam.isHasTech(getInfoType('TECH_ALTERATION')):
		giveUnits.append( ( 'UNIT_GHOSTWALKER', 'recon', ['PROMOTION_ILLUSION', 'PROMOTION_ADVENTURER', ],  'Otal the Faded' ) )
		bonusCategory['adept']['xp'] = bonusCategory['adept'].get('xp', 0 ) +2
	if pTeam.isHasTech(getInfoType('TECH_NECROMANCY')):
		bonusCategory['adept']['xp'] = bonusCategory['adept'].get('xp', 0 ) +2
	if pTeam.isHasTech(getInfoType('TECH_ELEMENTALISM')):
		bonusCategory['archer'].setdefault( 'promotions', [] ).append( 'PROMOTION_FLAMING_ARROWS' )
		bonusCategory['adept']['xp'] = bonusCategory['adept'].get('xp', 0 ) +2
	if pTeam.isHasTech(getInfoType('TECH_RELIGIOUS_LAW')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_YOUNG'],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_THEOLOGY')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_COMMUNE_WITH_NATURE')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_FANATICISM')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_REVENANT', 'melee', ['PROMOTION_ADVENTURER', ],  'Rasaec the Hollow' ) ) # Revenants are disciples, but very melee like disciples
	if pTeam.isHasTech(getInfoType('TECH_MALEVOLENT_DESIGNS')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_RIGHTEOUSNESS')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
	#	giveUnits.append( ( 'UNIT_CREEPER', 'creeper', ['PROMOTION_CREEPER_BLOOMING'],  '' ) )
	if pTeam.isHasTech(getInfoType('TECH_DIVINE_ESSENCE')):
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_AWAKENED', 'population', [],  '' ) )
		giveUnits.append( ( 'UNIT_ABOMINATION', 'melee', [],  '' ) )

	if not makeHelpText:
		pCapital = pPlayer.getCapitalCity()
		capitalX = pCapital.getX()
		capitalY = pCapital.getY()
		bestPlotGoodness = -1
		iBestPlot = None
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			plotGoodness = -1
			if ( pPlot.getOwner() != iPlayer
				and not pPlot.isWater()
				and pPlot.getNumUnits() == 0
				and not pPlot.isCity()
				and not pPlot.isImpassable() ):
					plotGoodness = CyGame().getSorenRandNum(500, "Place Spiral Gate")
					# I'm placing a limit on the added goodness.
					# This makes final goodness a bit less map dependant and less predictable.
					# The limits will need finetuning.
					# With a limit of 250, all continents with at least 175 tiles are equally good.
					plotGoodness += min( pPlot.area().getNumTiles() * 2, 100 )
					# With a limit of 500, all continents with at least 100 unclaimed tiles are equally good.
					plotGoodness += min( pPlot.area().getNumUnownedTiles() * 5, 400 )
					# Distance to capital is squared, since area is squared
					# With a limit of 450, all tiles further away than 450**.5 or 21 squares are equally good
					plotGoodness += min( ( (pPlot.getX()-capitalX)**2 + (pPlot.getY()-capitalY)**2 ), 750)
					if not pPlot.isOwned():
						plotGoodness += 300
			if plotGoodness > bestPlotGoodness:
				bestPlotGoodness = plotGoodness
				pBestPlot = pPlot
		if pBestPlot is None:
			# It's a world spell, it shouldn't fail just because. Probably won't anyway
			# but just to be sure.
			pBestPlot = pCapital.plot()

		pBestPlot.setPlotEffectType(getInfoType('PLOT_EFFECT_HAUNTED_LANDS'))

		commonInitUnitArgs = ( pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH )
		for unitString, bonusCategoryName, promotionList, name in giveUnits:
			while unitString in unitUpgrades:
				unitString = unitUpgrades[unitString]
			newUnit = pPlayer.initUnit( getInfoType(unitString), *commonInitUnitArgs )
			for promotionString in promotionList:
				newUnit.setHasPromotion( getInfoType( promotionString ), True)
			if 'promotions' in bonusCategory[bonusCategoryName]:
				for promotionString in bonusCategory[bonusCategoryName]['promotions']:
					newUnit.setHasPromotion( getInfoType( promotionString ), True)
			if 'weapons' in bonusCategory[bonusCategoryName]:
				newUnit.setHasPromotion( getInfoType( bonusCategory[bonusCategoryName]['weapons'] ), True)
			if 'xp' in bonusCategory[bonusCategoryName]:
				newUnit.setExperienceTimes100(bonusCategory[bonusCategoryName]['xp']*100, -1)
			if name:
				newUnit.setName(name)

	else:
		counts = dict( (key,0) for key in [ 'False laroth', 'archer', 'adept', 'melee', 'recon', 'mounted', 'supplies', 'creeper', 'population' ])
		for unitString, bonusCategoryName, promotionList, name in giveUnits:
			counts[unitString] = counts.get( unitString, 0) +1
			counts[bonusCategoryName] += 1
		counts['military'] = sum( c for key, c in counts.iteritems() if key in set( [ 'False laroth', 'archer', 'adept', 'melee', 'recon', 'mounted', ] ) )
		templateHelpString = 'Treachery in the Land of the Dead.  A False Laroth steals away additional subjects for the Scions.  Currently casting this spell will give %(military)i military units, %(supplies)i supplies, %(population)i Awakened, and %(creeper)i Creepers.  The units will appear in a random, probably distant, location.'
		return templateHelpString % counts

# "Feed" spell - Ghostwalkers spend xps to allow Creepers to create HL - The Creeper spell requires the Sentry2 promo.
def spellPlant(caster):
	pPlot = caster.plot()
#	caster.changeExperience(-3, -1, False, False, False)
#	iCreeper = getInfoType('UNIT_CREEPER')
#	iPPromo = getInfoType('PROMOTION_FED_CREEPER')
#	iPSent = getInfoType('PROMOTION_SENTRY2')
#	for i in range(pPlot.getNumUnits()):
#		pUnit = pPlot.getUnit(i)
#		if pUnit.getUnitType() == iCreeper:
#			if pUnit.isHasPromotion(iPSent):
#				pUnit.setHasPromotion(iPPromo, True)
	#			pUnit.setHasPromotion(iPSent, False)
#				return

# Req for Corrupt Quartermaster
def reqOTT(caster):
	pPlot = caster.plot()
	iPPromo = getInfoType('PROMOTION_CORRUPT_QUARTERMASTER')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() != pUnit.getOwner()):
			if pUnit.isHasPromotion(getInfoType('PROMOTION_CORRUPT_QUARTERMASTER')) == False:
				return True
	return False

# Corrupt Quartermaster
def spellOTT(caster):
	pPlot = caster.plot()
	iPPromo = getInfoType('PROMOTION_CORRUPT_QUARTERMASTER')
	iAnimal = getInfoType('UNITCOMBAT_ANIMAL')
	iBeast = getInfoType('UNITCOMBAT_BEAST')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitCombatType() != iAnimal:
			if pUnit.getUnitCombatType() != iBeast:
				if (caster.getOwner() != pUnit.getOwner()):
#			if pUnit.isHasPromotion(iPPromo):
					if pUnit.isHasPromotion(getInfoType('PROMOTION_CORRUPT_QUARTERMASTER')) == False:
						pUnit.setHasPromotion(iPPromo, True)
						return

# Pelemoc's Horsemen.  Gives Pelemoc and effect promo and carries slight chance for war.
def effectSuperSchemer(caster):
	pCity = caster.plot().getPlotCity()
	iUH = CyGame().getSorenRandNum(15, "Pelemocs Horsemen anger amount")
#	if CyGame().getSorenRandNum(10, "AirEllySpawn") < 5:
#		pCity.changeHappinessTimer(-3)
#		pCity.changeExtraHappiness(-1)
	pCity.changeHurryAngerTimer(iUH)

	caster.setHasPromotion(getInfoType('PROMOTION_SUPER_SCHEMER'), True)

#	if CyGame().getSorenRandNum(150, "Pelemocs Horesman war odds") == 1:
#		startWar(caster.getOwner(), pPlot.getOwner(), WarPlanTypes.WARPLAN_LIMITED)

# Req for Pelemoc's Horsemen
def reqSuperSchemer(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	if pCity.getOwner() == caster.getOwner():
		return False
	return True

# Req for Arawn's Dust
def reqSpoil(caster):
	pPlot = caster.plot()
#	pUnit = pPlot.getUnit(i)
	iFarm = getInfoType('IMPROVEMENT_FARM')
	iPasture = getInfoType('IMPROVEMENT_PASTURE')
	iPlantation = getInfoType('IMPROVEMENT_PLANTATION')
	iCamp = getInfoType('IMPROVEMENT_CAMP')
#	iPPromo = getInfoType('PROMOTION_PLANT')
#	if caster.isHasPromotion(getInfoType('PROMOTION_FED_CREEPER')):
#		return False
	if pPlot.getImprovementType() == iFarm:
		return True
	if pPlot.getImprovementType() == iCamp:
		return True
	if pPlot.getImprovementType() == iPasture:
		return True
	if pPlot.getImprovementType() == iPlantation:
		return True
	return False

# Arawn's Dust
def spellSpoil(caster):
	pPlot = caster.plot()
	pPlot.setImprovementType(-1)
	caster.kill(True, 0)

def spellSeekAlcinus(caster):

	iAlcinus1 = getInfoType('UNIT_ALCINUS')
	iAlcinus2 = getInfoType('UNIT_ALCINUS_UPGRADED')
	iAlcinus3 = getInfoType('UNIT_ALCINUS_ARCHMAGE')

	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		py = PyPlayer(iPlayer)
		if (pPlayer.isAlive()):
			for pUnit in py.getUnitList():
				if pUnit.getUnitType() == iAlcinus1 or pUnit.getUnitType() == iAlcinus2 or pUnit.getUnitType() == iAlcinus3:
					pPlot = pUnit.plot()
					pPlayer = gc.getPlayer(caster.getOwner())
					iTeam = pPlayer.getTeam()
					pPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
					CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("We have found the traitor!", ()),'',1,'Art/Interface/Buttons/Units/Scions/MIT.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)

def effectDyingCreeper(caster):
	pPlayer = gc.getPlayer(caster.getOwner())

#	iChance = CyGame().getSorenRandNum(3, "Dying Creeper death chance")
#	if iChance == 0:
#		newUnit = pPlayer.initUnit(getInfoType('UNIT_CREEPER'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
#	caster.kill(True,0)

def reqManifestHornedDread(caster):

	iGhostwalker = getInfoType('UNIT_GHOSTWALKER')
	iHornedDreadPromo = getInfoType('PROMOTION_HORNED_DREAD')

	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isFeatAccomplished(FeatTypes.FEAT_MANIFEST_HORNED_DREAD) == False:
		return False
	if pPlayer.isFeatAccomplished(FeatTypes.FEAT_MANIFEST_FIRST_HORNED_DREAD) == False:
		return False

	if caster.isHasPromotion(iHornedDreadPromo):
		return False

	return True

def spellManifestHornedDread(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	py = PyPlayer(caster.getOwner())
	pPlayer.setFeatAccomplished(FeatTypes.FEAT_MANIFEST_HORNED_DREAD, False)

	iGhostwalker = getInfoType('UNIT_GHOSTWALKER')
	iHornedDreadPromo = getInfoType('PROMOTION_HORNED_DREAD')

	for pUnit in py.getUnitList():
		if pUnit.getUnitType() == iGhostwalker:
			if pUnit.isHasPromotion(iHornedDreadPromo):
				pUnit.setHasPromotion(iHornedDreadPromo, False)

	caster.setHasPromotion(iHornedDreadPromo, True)

def reqManifestFirstHornedDread(caster):
	pPlayer = gc.getPlayer(caster.getOwner())

	if pPlayer.isFeatAccomplished(FeatTypes.FEAT_MANIFEST_FIRST_HORNED_DREAD) == True:
		return False

	return True

def spellManifestFirstHornedDread(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.setFeatAccomplished(FeatTypes.FEAT_MANIFEST_FIRST_HORNED_DREAD, True)

	iGhostwalker = getInfoType('UNIT_GHOSTWALKER')
	iHornedDreadPromo = getInfoType('PROMOTION_HORNED_DREAD')

	caster.setHasPromotion(iHornedDreadPromo, True)

# Scions end
def reqLoyalty(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iLoyalty = getInfoType('PROMOTION_LOYALTY')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if caster.getTeam() == pUnit.getTeam() and not pUnit.isHasPromotion(iLoyalty):
			pLoyalty = gc.getPromotionInfo(iLoyalty)
			if pUnit.getUnitCombatType()!=-1 and pLoyalty.getUnitCombat(pUnit.getUnitCombatType()):
				return True
	return False

def spellLoyalty(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iEnraged = getInfoType('PROMOTION_ENRAGED')
	iFreelancer = getInfoType('PROMOTION_FREELANCER_EFFECT')
	iSuppressedRage = getInfoType('PROMOTION_SUPPRESSED_RAGE')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getTeam() == pUnit.getTeam() and (pUnit.isHasPromotion(iEnraged) or pUnit.isHasPromotion(iFreelancer))):
			pUnit.setHasPromotion(iEnraged, False)
			pUnit.setHasPromotion(iFreelancer, False)
			pUnit.setHasPromotion(iSuppressedRage, True)

def reqMotherDevour(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()

	iBroodStrength = 4

	if pCity.getPopulation() < 4:
		return False

	if pCity.getNumBuilding(getInfoType('BUILDING_ARCHOS_NEST_ADDON1')) > 0:
		iBroodStrength = 5
		if pCity.getPopulation() < 8:
			return False
	elif pCity.getNumBuilding(getInfoType('BUILDING_ARCHOS_NEST_ADDON2')) > 0:
		iBroodStrength = 6
		if pCity.getPopulation() < 12:
			return False
	elif pCity.getNumBuilding(getInfoType('BUILDING_ARCHOS_NEST_ADDON3')) > 0:
		iBroodStrength = 7
		if pCity.getPopulation() < 15:
			return False
	elif pCity.getNumBuilding(getInfoType('BUILDING_ARCHOS_NEST_ADDON4')) > 0:
		return False

	if caster.getLevel() >= iBroodStrength:
		return True

	return False

def spellMotherDevour(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iAddon1 = getInfoType('BUILDING_ARCHOS_NEST_ADDON1')
	iAddon2 = getInfoType('BUILDING_ARCHOS_NEST_ADDON2')
	iAddon3 = getInfoType('BUILDING_ARCHOS_NEST_ADDON3')
	iAddon4 = getInfoType('BUILDING_ARCHOS_NEST_ADDON4')

	if pCity.getNumBuilding(iAddon3) > 0:
		pCity.setNumRealBuilding(iAddon3, 0)
		pCity.setNumRealBuilding(iAddon4, 1)

	elif pCity.getNumBuilding(iAddon2) > 0:
		pCity.setNumRealBuilding(iAddon2, 0)
		pCity.setNumRealBuilding(iAddon3, 1)

	elif pCity.getNumBuilding(iAddon1) > 0:
		pCity.setNumRealBuilding(iAddon1, 0)
		pCity.setNumRealBuilding(iAddon2, 1)

	else:
		pCity.setNumRealBuilding(iAddon1, 1)

def reqOasis(caster):
	pPlot = caster.plot()
	if pPlot.getTerrainType() != getInfoType('TERRAIN_DESERT'):
		return False
	if pPlot.isCity():
		return False
	if pPlot.getImprovementType() != -1:
		return False
	if pPlot.getFeatureType() == getInfoType('FEATURE_FLOOD_PLAINS'):
		return False
	iOasis = getInfoType('FEATURE_OASIS')
	iDesert = getInfoType('TERRAIN_DESERT')
	iX = caster.getX()
	iY = caster.getY()
	getPlot	= CyMap().plot
	iMinDistance = 4
	for x, y in plotsInRange( iX, iY, iMinDistance ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			iFeature = pPlot.getFeatureType()
			if iFeature == iOasis:
				return False
	for x, y in plotsInRange( iX, iY, 1 ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			sValidTerrains = ['DESERT', 'COAST', 'OCEAN']
			iValidTerrains = [getInfoType('TERRAIN_' + sTerrain) for sTerrain in sValidTerrains]
			if not (pPlot.getTerrainType() in iValidTerrains):
				return False
	return True

def spellOasis(caster):
	pPlot = caster.plot()
	pPlot.setFeatureType(getInfoType('FEATURE_OASIS'),0)

def reqDesertStealth(caster):
	pPlot = caster.plot()
	if pPlot.getTerrainType() == getInfoType('TERRAIN_DESERT'):
		if caster.isHasPromotion(getInfoType('PROMOTION_DESERT_STEALTH')):
			return False
		return True

def effectAutoSanctify(caster):
	if caster.isHasCasted():
		return
	spellSanctify(caster)
	caster.setHasCasted(True)

	# Chose not to use caster.cast here as sound effects from many adepts at the start of turn would be annoying

def reqAutoSanctify(caster):
	if caster.isHasPromotion(getInfoType("PROMOTION_WARDEN")):
		return False
	return True

def reqSpreadJotKilmorph(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if pPlayer.getStateReligion() != getInfoType('RELIGION_RUNES_OF_KILMORPH'):
		return False

	pTeam = gc.getTeam(pPlayer.getTeam())
	if pTeam.isHasTech(getInfoType('TECH_WAY_OF_THE_EARTHMOTHER')) == False:
		return False

	if pCity.isHasReligion(getInfoType('RELIGION_RUNES_OF_KILMORPH')):
		return False

	return True

def reqSpreadJotEsus(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if pPlayer.getStateReligion() != getInfoType('RELIGION_COUNCIL_OF_ESUS'):
		return False

	pTeam = gc.getTeam(pPlayer.getTeam())
	if pTeam.isHasTech(getInfoType('TECH_DECEPTION')) == False:
		return False

	if pCity.isHasReligion(getInfoType('RELIGION_COUNCIL_OF_ESUS')):
		return False

	return True

def reqSpreadJotEmpyrean(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if pPlayer.getStateReligion() != getInfoType('RELIGION_THE_EMPYREAN'):
		return False

	pTeam = gc.getTeam(pPlayer.getTeam())
	if pTeam.isHasTech(getInfoType('TECH_HONOR')) == False:
		return False

	if pCity.isHasReligion(getInfoType('RELIGION_THE_EMPYREAN')):
		return False

	return True

def reqSpreadJotLeaves(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if pPlayer.getStateReligion() != getInfoType('RELIGION_FELLOWSHIP_OF_LEAVES'):
		return False

	pTeam = gc.getTeam(pPlayer.getTeam())
	if pTeam.isHasTech(getInfoType('TECH_WAY_OF_THE_FORESTS')) == False:
		return False

	if pCity.isHasReligion(getInfoType('RELIGION_FELLOWSHIP_OF_LEAVES')):
		return False

	return True



def reqSpreadJotOO(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if pPlayer.getStateReligion() != getInfoType('RELIGION_OCTOPUS_OVERLORDS'):
		return False

	pTeam = gc.getTeam(pPlayer.getTeam())
	if pTeam.isHasTech(getInfoType('TECH_MESSAGE_FROM_THE_DEEP')) == False:
		return False

	if pCity.isHasReligion(getInfoType('RELIGION_OCTOPUS_OVERLORDS')):
		return False

	return True

def reqSpreadJotOrder(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if pPlayer.getStateReligion() != getInfoType('RELIGION_THE_ORDER'):
		return False

	pTeam = gc.getTeam(pPlayer.getTeam())
	if pTeam.isHasTech(getInfoType('TECH_ORDERS_FROM_HEAVEN')) == False:
		return False

	if pCity.isHasReligion(getInfoType('RELIGION_THE_ORDER')):
		return False

	return True

def reqAustrinRemoteFound(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())

	if not pPlayer.isFeatAccomplished(FeatTypes.FEAT_EXPEDITION_READY):
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
		if pPlot.getFoundValue(pPlayer.getID()) < (pPlot.area().getBestFoundValue(pPlayer.getID()) * 2) / 3:
			return False

	return True

def spellAustrinRemoteFound(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())

	pCity = pPlayer.initCity(pPlot.getX(),pPlot.getY())
	CvEventInterface.getEventManager().onCityBuilt([pCity])
	pPlayer.setFeatAccomplished(FeatTypes.FEAT_EXPEDITION_READY, False)

def onDeathToad(pCaster):
        pPlot = pCaster.plot()
        iRnd = CyGame().getSorenRandNum(100, "Toadify")
	if pPlot.getBonusType(-1) != -1:                                        # can't cast if bonus
		return False
        if pPlot.getRealBonusType() != -1:                                      # can't cast if hidden bonus
		return False
        if pPlot.isWater() != -1:                                               # can't cast if on water
		return False
        if pPlot.pPlot.isPeak() != -1:                                          # can't cast if on peaks
		return False
        if pPlot.getTerrainType() == getInfoType('TERRAIN_DESERT'):             # can't cast if on desert
                return False
        if pPlot.getTerrainType() == getInfoType('TERRAIN_GLACIER'):            # can't cast if on glacier
                return False
        if pPlot.getTerrainType() == getInfoType('TERRAIN_TUNDRA'):             # can't cast if on tundra
                return False
        if iRnd < 10:
                pPlot.setBonusType(Bonus["Toad"])

def onDeathForestCreeper(pCaster):
	 iForest = getInfoType('FEATURE_FOREST')
	# iNewForest = getInfoType('FEATURE_FOREST_NEW')
	# iJungle = getInfoType('FEATURE_JUNGLE')
	# pPlot = pCaster.plot()
	# if not pPlot.isOwned():
		# if pPlot.getFeatureType() == iNewForest:
			# if CyGame().getSorenRandNum(3, "Chance to Spawn Extra Forest Creeper from New Forest") == 1:
				# pPlayer = gc.getPlayer(pCaster.getOwner())
				# newUnit = pPlayer.initUnit(getInfoType('UNIT_FOREST_CREEPER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				# return
			# if CyGame().getSorenRandNum(3, "Chance to Change New Forest to Forest") == 1:
				# pPlot.setFeatureType(-1, -1)
				# pPlot.setFeatureType(iForest, 0)
				# return
		# if (pPlot.getFeatureType() != iForest or pPlot.getFeatureType() != iNewForest or pPlot.getFeatureType() != iJungle):
			# if pPlot.canHaveFeature(iNewForest):
				# if pPlot.getFeatureType() == -1:
					# pPlot.setFeatureType(-1, -1)
					# pPlot.setFeatureType(iNewForest, 0)
					# return
		# if (pPlot.getFeatureType() == iForest or pPlot.getFeatureType() == iJungle):
			# iFallenForest = getInfoType('IMPROVEMENT_BLIGHTED_FOREST')
			# iImprovementCount = 0
			# getPlot	= CyMap().plot
			# iRange = 2
			# for x, y in plotsInRange( pCaster.getX(), pCaster.getY(), iRange ):
				# pPlot = getPlot(x, y)
				# if pPlot.isNone() == False:
					# if pPlot.getImprovementType() == iFallenForest:
						# iImprovementCount += 1
			# if iImprovementCount == 0:
				# pPlot = pCaster.plot()
				# pPlayer = gc.getPlayer(pCaster.getOwner())
				# pPlot.setImprovementType(iFallenForest)
				# newUnit = pPlayer.initUnit(getInfoType('UNIT_FOREST_CREEPER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				# if CyGame().getSorenRandNum(5, "Chance to Spawn Malignant Flora from Fallen Forest Creation") < 3:
					# newUnit = pPlayer.initUnit(getInfoType('UNIT_MALIGNANT_FLORA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					# return
			# if iImprovementCount > 0:
				# if CyGame().getSorenRandNum(3, "Chance to Spawn Extra Forest Creeper from Forest when Lair fails") == 1:
					# pPlayer = gc.getPlayer(pCaster.getOwner())
					# newUnit = pPlayer.initUnit(getInfoType('UNIT_FOREST_CREEPER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def onDeathDragon(pCaster): # TODO Ronkhar. Obsolete function: remove or add to a unit of race dragon
	iPlayer = pCaster.getOwner()
	iAnimalPlayer = gc.getANIMAL_PLAYER()
	iBones = getInfoType('IMPROVEMENT_DRAGON_BONES')
	pPlot = pCaster.plot()
	if iPlayer == iAnimalPlayer:
		pPlot.setImprovementType(iBones)

def effectMalignantFlora(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlot.isCity():
		caster.kill(True, 0)
	if CyGame().getSorenRandNum(4, "Chance to Spawn Forest Creeper from Malignant Flora") == 1:
		#newUnit = pPlayer.initUnit(getInfoType('UNIT_FOREST_CREEPER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if pPlot.getFeatureType() == getInfoType('FEATURE_FOREST'):
			if CyGame().getSorenRandNum(20, "Chance to Animal from Malignant Flora Forest") == 1:
				if CyGame().getSorenRandNum(10, "Chance to Wolf or Bear from Malignant Flora") >= 3:
					newUnit = pPlayer.initUnit(getInfoType('UNIT_WOLF'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				else:
					newUnit = pPlayer.initUnit(getInfoType('UNIT_BEAR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if pPlot.getFeatureType() == getInfoType('FEATURE_JUNGLE'):
			if CyGame().getSorenRandNum(20, "Chance to Animal from Malignant Flora Jungle") == 1:
				if CyGame().getSorenRandNum(10, "Chance to Panther or Gorilla from Malignant Flora") >= 5:
					newUnit = pPlayer.initUnit(getInfoType('UNIT_TIGER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				else:
					newUnit = pPlayer.initUnit(getInfoType('UNIT_GORILLA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if (pPlot.getFeatureType() != getInfoType('FEATURE_FOREST') or pPlot.getFeatureType() != getInfoType('FEATURE_JUNGLE')):
			pPlot.setFeatureType(getInfoType('FEATURE_FOREST'), 0)

def atRangeWiddershinsCurse(pCaster,pPlot):
	if(pCaster.getPerception()>2):
		return
	else:
		pCaster.setHasPromotion(getInfoType("PROMOTION_LOST"),True)
		
def atRangeBlightedForest(pCaster, pPlot):
	if CvEventInterface.getEventManager().cf.doForestPush(pCaster, pPlot, -1, False):
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_BLIGHTED_FOREST", (gc.getUnitInfo(pCaster.getUnitType()).getDescription(), )),'',1,'Art/Interface/Buttons/Improvements/blightedforest.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)

def effectWanderingCurse(caster):
	if caster.isHasPromotion(gc.getInfoTypeForString("PROMOTION_MANA_GUARDIAN")):
		return
	pPlot = caster.plot()
	pPlot2 = findClearPlot(caster, caster.plot())
	if pPlot2 != -1:
		caster.setXY(pPlot2.getX(), pPlot2.getY(), False, True, True,True)
		CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_WANDERING", ()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Promotions/Lost.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)

def effectFieldExercise(caster):
	caster.changeExperienceTimes100(200/(caster.getLevel()*caster.getLevel()+1),-1,False,False,False)

def reqBloodMoon(caster):
	if caster.isHasPromotion(getInfoType('PROMOTION_WEREWOLF_FORM1')):
		return False
	if caster.isHasPromotion(getInfoType('PROMOTION_WEREWOLF_FORM2')):
		return False
	if caster.isHasPromotion(getInfoType('PROMOTION_WEREWOLF_FORM3')):
		return False
	if caster.isHasPromotion(getInfoType('PROMOTION_LOYALTY2')):
		return False
	if caster.isHasPromotion(getInfoType('PROMOTION_PACK_ALPHA')):
		return False
	if caster.getUnitType() == getInfoType('UNIT_DUIN'):
		return False
	if caster.getUnitType() == getInfoType('UNIT_DOVIELLO_WEREWOLF'):
		return False
	if caster.getUnitType() == getInfoType('UNIT_RAVENOUS_WEREWOLF'):
		return False
	return True

def postCombatWinWerewolf(pCaster, pOpponent):
	if pOpponent.isAlive() and pOpponent.canDefend(pOpponent.plot()):                                       #Can only convert Living Combat Units
		if pCaster.baseCombatStr() < gc.getUnitInfo(pCaster.getUnitType()).getCombat() * 3 / 2:             # If the werewolf has not attained maximal strength (50% bonus)
			iGrowChance = pOpponent.baseCombatStr() * 5                                                     # There is a chance to strengthen the werewolf (proportional to the strength of the vanquished enemy)
			if pCaster.isEnraged():
				iGrowChance = iGrowChance * 2
			if CyGame().getSorenRandNum(100, "Werewolf Growth") < iGrowChance:                              # If the roll is successful
				pCaster.changeStrBoost(1)                                                                   # we strengthen the werewolf by +1
				if not pCaster.baseCombatStr() < gc.getUnitInfo(pCaster.getUnitType()).getCombat() * 3 / 2: # If this pushes the werewolf to maximal strength (50% bonus), it becomes a "greater werewolf"
					oldName = pCaster.getName()
					pCaster.setName(CyTranslator().getText('TXT_KEY_UNIT_GREATER_WEREWOLF',()))
					CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_WEREWOLF_SATIATED", (oldName, pCaster.getName())),'',1,'Art/Interface/Buttons/Promotions/Werewolf.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
					pCaster.setHasPromotion(getInfoType('PROMOTION_CRAZED'), False)
				elif pCaster.baseCombatStr() == gc.getUnitInfo(pCaster.getUnitType()).getCombat():          # Else if this pushes the werewolf to base strength, it becomes a "blooded werewolf"
					oldName = pCaster.getName()
					pCaster.setName(CyTranslator().getText('TXT_KEY_UNIT_BLOODED_WEREWOLF',()))
					CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_WEREWOLF_CALMED", (oldName, pCaster.getName())),'',1,'Art/Interface/Buttons/Promotions/Werewolf.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
					pCaster.setHasPromotion(getInfoType('PROMOTION_CRAZED'), False)
#			elif pCaster.baseCombatStr() < gc.getUnitInfo(pCaster.getUnitType()).getCombat():	#We should MAYBE include a chance for going enraged if you don't gain strength, could be somewhat annoying to always gain strength or enrage, it essentially means you NEVER control a Ravenous Werewolf directly without Loyalty applied
#				pCaster.setHasPromotion(getInfoType('PROMOTION_ENRAGED'), True)
#				CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_WEREWOLF_ENRAGING", (pCaster.getName(), )),'',1,'Art/Interface/Buttons/Promotions/Werewolf.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)

	#	if (not pOpponent.isImmuneToCapture()) or (not gc.isNoCrash() and  not pOpponent.isAlreadyResurrected()):	#Let Loyalty grant Immunity
	#		if not pOpponent.isImmortal():
	#			if (pOpponent.getCaptureUnitType(pOpponent.getCivilizationType()) == -1 and gc.getUnitInfo(pCaster.getUnitType()).getUnitCreateFromCombat() == -1):	#Prevents gaining 2 units from a single combat, could still get a Wolf and a Slave right now however, but don't want to have Werewolves disabled completely by following Slavery Civic
	#				iConvertChance = 30                                                                     # Chance for a normal unit to convert the vanquished enemy into a werewolf
	#				if isWorldUnitClass(pCaster.getUnitClassType()):
	#					iConvertChance = 50                                                                 # Higher chance for a hero to convert the vanquished enemy into a werewolf
	#				if CyGame().getSorenRandNum(100, "Werewolf Curse") < iConvertChance:                    # If the roll is successful
	#					pPlayer = gc.getPlayer(pCaster.getOwner())                                          # We convert the enemy into a werewolf
	#					newUnit = pPlayer.initUnit(pOpponent.getUnitType(), pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	#					newUnit.convert(pOpponent)
						#for i in range(gc.getNumPromotionInfos()):
						#	if pOpponent.isHasPromotion(i) and not gc.getPromotionInfo(i).isEquipment():
						#		newUnit.setHasPromotion(i, True)
							#if gc.getPromotionInfo(i).isEquipment():
							#	newUnit.setHasPromotion(i, False)
						#newUnit.setLevel(pOpponent.getLevel())
						#newUnit.setExperienceTimes100(pOpponent.getExperienceTimes100(), -1)
	#					newUnit.setHasCasted(True)
	#					newUnit.finishMoves()
	#					if newUnit.baseCombatStr() > 1:                                                     # If the ex-enemy/new werewolf has at least 2 strength
	#						newUnit.changeStrBoost(-newUnit.baseCombatStr()/4)                              # he gets weakened by 1/4. probably floor(value). 5 becomes 3, 6 becomes 4
	#					oldName = pOpponent.getName()
	#					newUnit.setHasPromotion(getInfoType('PROMOTION_WEREWOLF'), True)
	#					if newUnit.baseCombatStr() == gc.getUnitInfo(newUnit.getUnitType()).getCombat():    # If the ex-enemy/new werewolf had 1 strength
	#						newUnit.setName(CyTranslator().getText('TXT_KEY_UNIT_BLOODED_WEREWOLF',()))     # He becomes a blooded werewolf (under control)
	#					else:
	#						newUnit.setName(CyTranslator().getText('TXT_KEY_UNIT_RAVENOUS_WEREWOLF',()))    # If the ex-enemy/new werewolf had 2+ strength
	#						newUnit.setHasPromotion(getInfoType('PROMOTION_CRAZED'), True)                  # He becomes a ravenous werewolf (crazy)
	#					CyInterface().addMessage(newUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_WEREWOLF_INFECTED", (oldName, newUnit.getName())),'',1,'Art/Interface/Buttons/Promotions/Werewolf.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)

def postCombatLossWerewolf(pCaster, pOpponent):
	if pOpponent.isAlive():
		if pOpponent.isHurt():	#Must be hurt to be infected, better if we force it to require that the wolf itself hurt you, but this still works nicely.
			iInfectChance = 10
			if CyGame().getSorenRandNum(100, "Werewolf Infection") < iInfectChance:	#Low rigid chance for now, will set something up for variability some other time
				pOpponent.setHasPromotion(getInfoType('PROMOTION_WEREWOLF'), True)

def postCombatSaverous(pCaster, pOpponent):
	if (pOpponent.getUnitType() == getInfoType('UNIT_VALIN') or pOpponent.getUnitType() == getInfoType('UNIT_HIGH_PRIEST_OF_THE_ORDER') or pOpponent.getUnitType() == getInfoType('UNIT_SPHENER')):
		pPlayer = gc.getPlayer(pOpponent.getOwner())
		newUnit = pPlayer.initUnit(getInfoType('UNIT_SAVEROUS_REDEEMED'), pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)




def findCommander(caster):
	py = PyPlayer(caster.getOwner())
	pPlot = caster.plot()
	pBestUnit = -1
	iBestRank = 7
	iBestLevel = 9999
	bSameGroup = False
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == caster.getOwner():
			if not pUnit.getID() == caster.getID():
				if (bSameGroup and pUnit.getGroupID() == caster.getGroupID()) or (not bSameGroup):
					if caster.getDomainType() == pUnit.getDomainType():
						bvalid=True
						pLoopCommander=pUnit.getCommanderUnit()
						while( not pLoopCommander.isNone()):
							if (pLoopCommander.getID()==caster.getID()):
								bvalid=False
								break
							pLoopCommander=pLoopCommander.getCommanderUnit()
						if (not bvalid):
							continue
						if not pUnit.getID() == caster.getCommanderUnit().getID() and not pUnit.getCommanderUnit().getID() == caster.getID():		#Neither of us is leading the other one
							if pUnit.getNumMinions() < pUnit.getCommandLimit():
								iCorporal = getInfoType('PROMOTION_CORPORAL')
								if(iCorporal == -1):									#If we don't have the Bannor Chain of Command Module Loaded
									if(pUnit.getGroupID() == caster.getGroupID()):
										if not (bSameGroup):
											pBestUnit = pUnit
											iBestLevel = pUnit.getLevel()
											bSameGroup = True
										elif pUnit.getLevel() <iBestLevel:
											pBestUnit = pUnit
											iBestLevel = pUnit.getLevel()
									else:
										if pUnit.getLevel() <iBestLevel:
											pBestUnit = pUnit
											iBestLevel = pUnit.getLevel()
								else:
									iSarge = getInfoType('PROMOTION_SEARGENT')
									iMasterSarge = getInfoType('PROMOTION_MASTER_SEARGENT')
									iCaptain = getInfoType('PROMOTION_CAPTAIN')
									iGeneral = getInfoType('PROMOTION_GENERAL')
									iMinionRank = 0
									if caster.isHasPromotion(iGeneral):
										iMinionRank = 5
									elif caster.isHasPromotion(iCaptain):
										iMinionRank = 4
									elif caster.isHasPromotion(iMasterSarge):
										iMinionRank = 3
									elif caster.isHasPromotion(iSarge):
										iMinionRank = 2
									elif caster.isHasPromotion(iCorporal):
										iMinionRank = 1
									elif caster.getCommandLimit() > 0:
										iMinionRank = 6

									iCommanderRank = 6
									if pUnit.isHasPromotion(iGeneral):
										iCommanderRank = 5
									elif pUnit.isHasPromotion(iCaptain):
										iCommanderRank = 4
									elif pUnit.isHasPromotion(iMasterSarge):
										iCommanderRank = 3
									elif pUnit.isHasPromotion(iSarge):
										iCommanderRank = 2
									elif pUnit.isHasPromotion(iCorporal):
										iCommanderRank = 1

									if iCommanderRank > iMinionRank:	#If you have a rank, you cannot lead someone who outranks you
										if(pUnit.getGroupID() == caster.getGroupID()):
											if not (bSameGroup):
												pBestUnit = pUnit
												iBestRank = iCommanderRank
												iBestLevel = pUnit.getLevel()
												bSameGroup = True
											elif iCommanderRank < iBestRank:	#Prefer to follow the lowest Commander available
												pBestUnit = pUnit
												iBestRank = iCommanderRank
												iBestLevel = pUnit.getLevel()
											elif (iCommanderRank == iBestRank):
												if (pUnit.getLevel() < iBestLevel):
													pBestUnit = pUnit
													iBestLevel = pUnit.getLevel()
										else:
											if iCommanderRank < iBestRank:	#Prefer to follow the lowest Commander available
												pBestUnit = pUnit
												iBestRank = iCommanderRank
												iBestLevel = pUnit.getLevel()
											elif (iCommanderRank == iBestRank):
												if (pUnit.getLevel() < iBestLevel):
													pBestUnit = pUnit
													iBestLevel = pUnit.getLevel()
	return pBestUnit

def reqAttachMinion(caster):
	if not caster.getMasterUnit().isNone():
		return False
	pCommander = -1
	if caster.getUnitClassType() == getInfoType("UNITCLASS_SLUGA") or caster.getUnitClassType() == getInfoType("UNITCLASS_BATTLE_SLUGA") or caster.getUnitClassType() == getInfoType("UNITCLASS_WAR_SLUGA") or caster.getUnitClassType() == getInfoType("UNITCLASS_BEHEMOTH_SLUGA"):
		pCommander = findSlugaCommander(caster)
	else:
		pCommander = findCommander(caster)
	if pCommander != -1:
		return True
	return False

def attachMinion(caster):
	pCommander = -1
	if caster.getUnitClassType() == getInfoType("UNITCLASS_SLUGA") or caster.getUnitClassType() == getInfoType("UNITCLASS_BATTLE_SLUGA") or caster.getUnitClassType() == getInfoType("UNITCLASS_WAR_SLUGA") or caster.getUnitClassType() == getInfoType("UNITCLASS_BEHEMOTH_SLUGA"):
		pCommander = findSlugaCommander(caster)
	else:
		pCommander = findCommander(caster)
	if pCommander != -1:
		pCommander.addMinion(caster)

def removeMinion(caster):
	pUnit = caster.getCommanderUnit()
	pUnit.removeMinion(caster)

def getHelpAttachMinion(argsList):
	eSpell, pCaster = argsList
	if pCaster == -1 or pCaster.isNone():
		szHelp = ""
	else:
		pCommander = -1
		if pCaster.getUnitClassType() == getInfoType("UNITCLASS_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BATTLE_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_WAR_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BEHEMOTH_SLUGA"):
			pCommander = findSlugaCommander(pCaster)
		else:
			pCommander = findCommander(pCaster)
		if not (pCommander == -1):
			szHelp = localText.getText("TXT_KEY_SPELL_JOIN_COMMANDER", (pCommander.getName(),pCaster.getName()))
	return szHelp

def reqAdvancement(caster):
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_ANIMAL'):
		return False
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_BEAST'):
		return False
	if caster.isImmortal():
		return False
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_WORKER'):
		return False
	if caster.getCommandLimit() > 0:
		return False
	return True

def doAdvancement(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	newUnit = pPlayer.initUnit(getInfoType('UNIT_COMMANDER_BANNOR_CAPTAIN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def displayAllUnits(pCaster):
	for iPlayer in xrange(0,int(gc.getMAX_PLAYERS())):
		if ((gc.getPlayer(iPlayer).isAlive()) and (gc.getPlayer(iPlayer).isBarbarian()!=True) ):
			for j in xrange( CyGlobalContext().getNumUnitClassInfos() ):
				eLoopUnit = CyGlobalContext().getCivilizationInfo(gc.getPlayer(iPlayer).getCivilizationType()).getCivilizationUnits(j)
				if (eLoopUnit != -1):
					x = j%10 + 1 + iPlayer*12
					y = (j/10) + 5
					gc.getPlayer(iPlayer).initUnit( eLoopUnit, x, y, UnitAITypes.UNITAI_UNKNOWN, DirectionTypes.NO_DIRECTION )

def increaseAC(caster):
	CyGame().changeGlobalCounter(10)

def decreaseAC(caster):
	CyGame().changeGlobalCounter(-10)

def zeroAC(caster):
	CyGame().changeGlobalCounter(-1 * (CyGame().getTrueGlobalCounter()))

def maxAC(caster):
	CyGame().changeGlobalCounter(9999)

def WorstUnit(player, location, combat):
	py = player
	pPlot = location
	pWorstUnit = -1
	fWorstValue = 9999999999999999999999999999 #Nothing returned could be higher than this value, so the first unit will always be the worst to begin with.
	for i in range(pPlot.getNumUnits()):
		fValue = 999999999999999999
		pUnit = pPlot.getUnit(i)
		if (combat == -1 or pUnit.getUnitCombatType() == combat) and pUnit.getSummoner() == -1: #used by dark empowerment only. We want real units only (not summons)
			if pUnit.getOwner() == player:
				iLevel = pUnit.getLevel()
				iStrength = pUnit.baseCombatStr()
				fStrength = iStrength * (1.0 - (pUnit.getDamage() / 100))#Find the unit's actual strength by factoring in its damage
				fModifier = iLevel / 2.0+1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_HERO')) or pUnit.isHasPromotion(getInfoType('PROMOTION_ADVENTURER')):
					fModifier += 999999999999 #Heroes should never be chosen
				if pUnit.isHasPromotion(getInfoType('PROMOTION_HEROIC')):
					fModifier += 999999999999 #Nor should Battle-Hardened units
				if pUnit.isHasPromotion(getInfoType('PROMOTION_WEAK')):
					fModifier -= 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_STRONG')):
					fModifier += 2.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_CRAZED')):
					fModifier -= 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_DISEASED')):
					fModifier -= 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_ENRAGED')):
					fModifier -= 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_UNDISCIPLINED')):
					fModifier -= 1.0
				if pUnit.isHasPromotion(getInfoType('PROMOTION_PLAGUED')):
					fModifier -= 1.0
				if fModifier<0:
					fModifier=0
				fValue = fStrength * fModifier
				if fValue < fWorstValue:
					fWorstValue = fValue
					pWorstUnit = pUnit

	return pWorstUnit

def spellDovielloChallenge(caster):
	caster.setHasPromotion(getInfoType('PROMOTION_CHALLENGER'), True)

def reqDovielloChallenge(caster):
	pPlot = caster.plot()
	iChallenger = getInfoType('PROMOTION_CHALLENGER')
	iStack = 0
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getID() != caster.getID() and pUnit.getOwner() == caster.getOwner() and pUnit.getUnitCombatType() != getInfoType('UNITCOMBAT_ANIMAL'):
			if pUnit.getUnitCombatType() != getInfoType('UNITCOMBAT_NAVAL'):
				if pUnit.getUnitClassType() != getInfoType('UNITCLASS_SETTLER'):
					if pUnit.getUnitClassType() != getInfoType('UNITCLASS_WORKER'):
						if pUnit.getUnitClassType() != getInfoType('UNITCLASS_HAWK'):
							iStack += 1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_ANIMAL') or caster.getUnitCombatType() == getInfoType('UNITCOMBAT_NAVAL'):
			return False
		if caster.getUnitClassType() == getInfoType('UNITCLASS_SETTLER'):
			return False
		if caster.getUnitClassType() == getInfoType('UNITCLASS_WORKER'):
			return False
		if caster.getUnitClassType() == getInfoType('UNITCLASS_HAWK'):
			return False
		if pUnit.isHasPromotion(iChallenger):
			return False
		if iStack < 1:
			return False
	return True

def reqDovielloDuel(caster):
	pPlot = caster.plot()
	if caster.getUnitCombatType() == getInfoType('UNITCOMBAT_ANIMAL') or caster.getUnitCombatType() == getInfoType('UNITCOMBAT_NAVAL'):
		return False
	if caster.getUnitClassType() == getInfoType('UNITCLASS_WORKER'):
		return False
	if caster.getUnitClassType() == getInfoType('UNITCLASS_SETTLER'):
		return False
	return True

def spellDovielloDuel(caster):
	pPlot = caster.plot()
	iChallengerProm = getInfoType('PROMOTION_CHALLENGER')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iRnd = CyGame().getSorenRandNum(100, "Doviello Duel")
		if pUnit.isHasPromotion(iChallengerProm) == True:
			iChallengerOdds = getCombatOdds(pUnit, caster)
			iChallengerRnd = (iRnd + (iChallengerOdds * 2)) / 3
			iDefenderOdds = getCombatOdds(caster, pUnit)
			iDefenderRnd = (iRnd + (iDefenderOdds * 2)) / 3
			if iDefenderOdds > iChallengerOdds:
				iDefenseRnd = CyGame().getSorenRandNum(100, "Doviello Duel Defender")
				iDefenseTieRnd = CyGame().getSorenRandNum(100, "Doviello Duel Defender Tie")
				if iDefenseTieRnd < 10:
					caster.changeExperience(pUnit.getExperienceTimes100() / 1000, -1, False, False, False)
					caster.setDamage(75, caster.getOwner())
					pUnit.changeExperience(caster.getExperienceTimes100() / 1000, -1, False, False, False)
					pUnit.setDamage(75, pUnit.getOwner())
					pUnit.setHasPromotion(getInfoType('PROMOTION_CHALLENGER'), False)
					CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOVIELLO_DUEL_DRAW", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
				elif (iDefenseTieRnd <= 12 and iDefenseTieRnd >= 10):
					iVictorRnd = CyGame().getSorenRandNum(100, "Doviello Duel")
					if iVictorRnd < 50:
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ARENA_DEATH_DEFENDER", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(7),caster.getX(),caster.getY(),True,True)
						caster.kill(True, PlayerTypes.NO_PLAYER)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
					else:
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ARENA_DEATH_CHALLENGER", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(7),caster.getX(),caster.getY(),True,True)
						caster.kill(True, PlayerTypes.NO_PLAYER)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
				elif iDefenseTieRnd > 12:
					if iDefenseRnd > iDefenderOdds:
						pUnit.changeExperience((caster.getExperienceTimes100() / 200) + 2, -1, False, False, False)
						pUnit.setDamage(25, pUnit.getOwner())
						pUnit.setHasPromotion(getInfoType('PROMOTION_CHALLENGER'), False)
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOVIELLO_DUEL_LOSS", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
						caster.kill(True, PlayerTypes.NO_PLAYER)
					if iDefenseRnd < iDefenderOdds:
						caster.changeExperience((pUnit.getExperienceTimes100() / 200) + 2, -1, False, False, False)
						caster.setDamage(25, caster.getOwner())
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOVIELLO_DUEL_WIN", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
			if iChallengerOdds > iDefenderOdds:
				iChallengeRnd = CyGame().getSorenRandNum(100, "Doviello Duel Challenger")
				iChallengerTieRnd = CyGame().getSorenRandNum(100, "Doviello Duel Challenger Tie")
				if iChallengerTieRnd < 10:
					caster.changeExperience(pUnit.getExperienceTimes100() / 1000, -1, False, False, False)
					caster.setDamage(75, caster.getOwner())
					pUnit.changeExperience(caster.getExperienceTimes100() / 1000, -1, False, False, False)
					pUnit.setDamage(75, pUnit.getOwner())
					pUnit.setHasPromotion(getInfoType('PROMOTION_CHALLENGER'), False)
					CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOVIELLO_DUEL_DRAW", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
				elif (iChallengerTieRnd <= 12 and iChallengerTieRnd >= 10):
					iVictorRnd = CyGame().getSorenRandNum(100, "Doviello Duel")
					if iVictorRnd < 50:
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ARENA_DEATH_DEFENDER", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(7),caster.getX(),caster.getY(),True,True)
						caster.kill(True, PlayerTypes.NO_PLAYER)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
					else:
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ARENA_DEATH_CHALLENGER", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(7),caster.getX(),caster.getY(),True,True)
						caster.kill(True, PlayerTypes.NO_PLAYER)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
				elif iChallengerTieRnd > 12:
					if iChallengeRnd < iChallengerOdds:
						pUnit.changeExperience((caster.getExperienceTimes100() / 200) + 2, -1, False, False, False)
						pUnit.setDamage(25, pUnit.getOwner())
						pUnit.setHasPromotion(getInfoType('PROMOTION_CHALLENGER'), False)
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOVIELLO_DUEL_LOSS", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
						caster.kill(True, PlayerTypes.NO_PLAYER)
					if iChallengeRnd > iChallengerOdds:
						caster.changeExperience((pUnit.getExperienceTimes100() / 200) + 2, -1, False, False, False)
						caster.setDamage(25, caster.getOwner())
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOVIELLO_DUEL_WIN", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
			if iChallengerOdds == iDefenderOdds:
				iEqualRnd = CyGame().getSorenRandNum(100, "Doviello Duel Equals")
				iEqualTieRnd = CyGame().getSorenRandNum(100, "Doviello Duel Equals Tie")
				if iEqualTieRnd < 10:
					caster.changeExperience(pUnit.getExperienceTimes100() / 1000, -1, False, False, False)
					caster.setDamage(75, caster.getOwner())
					pUnit.changeExperience(caster.getExperienceTimes100() / 1000, -1, False, False, False)
					pUnit.setDamage(75, pUnit.getOwner())
					pUnit.setHasPromotion(getInfoType('PROMOTION_CHALLENGER'), False)
					CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOVIELLO_DUEL_DRAW", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
				elif (iEqualTieRnd <= 12 and iEqualTieRnd >= 10):
					iVictorRnd = CyGame().getSorenRandNum(100, "Doviello Duel")
					if iVictorRnd < 50:
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ARENA_DEATH_DEFENDER", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(7),caster.getX(),caster.getY(),True,True)
						caster.kill(True, PlayerTypes.NO_PLAYER)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
					else:
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ARENA_DEATH_CHALLENGER", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(7),caster.getX(),caster.getY(),True,True)
						caster.kill(True, PlayerTypes.NO_PLAYER)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
				elif iEqualTieRnd > 12:
					if iEqualRnd < 50:
						pUnit.changeExperience((caster.getExperienceTimes100() / 200) + 2, -1, False, False, False)
						pUnit.setDamage(25, pUnit.getOwner())
						pUnit.setHasPromotion(getInfoType('PROMOTION_CHALLENGER'), False)
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOVIELLO_DUEL_LOSS", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
						caster.kill(True, PlayerTypes.NO_PLAYER)
					if iEqualRnd >= 50:
						caster.changeExperience((pUnit.getExperienceTimes100() / 200) + 2, -1, False, False, False)
						caster.setDamage(25, caster.getOwner())
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOVIELLO_DUEL_WIN", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
			break

def postCombatScavenger(pCaster, pOpponent):
	if pOpponent.isAlive():
		pCaster.setHasPromotion(getInfoType('PROMOTION_SCAVENGER'), False)
		pCaster.setHasPromotion(getInfoType('PROMOTION_SCAVENGER'), True)
	if pOpponent.isHasPromotion(getInfoType('PROMOTION_BRONZE_WEAPONS')):
		pCaster.setHasPromotion(getInfoType('PROMOTION_BRONZE_WEAPONS'), True)
	if pOpponent.isHasPromotion(getInfoType('PROMOTION_IRON_WEAPONS')):
		pCaster.setHasPromotion(getInfoType('PROMOTION_IRON_WEAPONS'), True)
	if pOpponent.isHasPromotion(getInfoType('PROMOTION_MITHRIL_WEAPONS')):
		pCaster.setHasPromotion(getInfoType('PROMOTION_MITHRIL_WEAPONS'), True)
	if pOpponent.isHasPromotion(getInfoType('PROMOTION_ENCHANTED_BLADE')):
		pCaster.setHasPromotion(getInfoType('PROMOTION_ENCHANTED_BLADE'), True)

def spellVarulv(Caster):
	Caster.setHasPromotion(getInfoType('PROMOTION_VARULV_SPELL'), False)
	Caster.setHasPromotion(getInfoType('PROMOTION_VARULV_SPELL_BLOCK'), True)

def reqInciteFervor(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	StateBelief = gc.getPlayer(pCity.getOwner()).getStateReligion()

	if (StateBelief != -1):
		if pCity.getOwner() == caster.getOwner():
			if pCity.getPopulation() > 3:
				return True

	if pPlayer.getCivilizationType() == Civ["Scions"]:
		if pPlayer.getLeaderType() == getInfoType('LEADER_RISEN_EMPEROR'):
			if pCity.getOwner() == caster.getOwner():
				if pCity.getPopulation() > 3:
					return True
					
	return False


def spellInciteFervor(caster):
	iOwner = caster.getOwner()
	pPlayer = gc.getPlayer(iOwner)
	pCiv = pPlayer.getCivilizationType()
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iOrderP = getInfoType('UNIT_DISCIPLE_THE_ORDER')
	iVeilP = getInfoType('UNIT_DISCIPLE_THE_ASHEN_VEIL')
	iLeavesP = getInfoType('UNIT_DISCIPLE_FELLOWSHIP_OF_LEAVES')
	iOOP = getInfoType('UNIT_DISCIPLE_OCTOPUS_OVERLORDS')
	iRoKP = getInfoType('UNIT_DISCIPLE_RUNES_OF_KILMORPH')
	iEmpyP = getInfoType('UNIT_DISCIPLE_EMPYREAN')
	iWhiteP = getInfoType('UNIT_DISCIPLE_OF_WINTER')
	iLegate = getInfoType('UNIT_LEGATE')
	iLeaves = getInfoType('RELIGION_FELLOWSHIP_OF_LEAVES')
	iRoK = getInfoType('RELIGION_RUNES_OF_KILMORPH')
	iEmpy = getInfoType('RELIGION_THE_EMPYREAN')
	iOrder = getInfoType('RELIGION_THE_ORDER')
	iOO = getInfoType('RELIGION_OCTOPUS_OVERLORDS')
	iVeil = getInfoType('RELIGION_THE_ASHEN_VEIL')
	iWhiteHand = getInfoType('RELIGION_WHITE_HAND')
	StateBelief = pPlayer.getStateReligion()

	if StateBelief == iLeaves:
		newUnit = pPlayer.initUnit(iLeavesP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iLeavesP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iLeavesP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pCity.changeHurryAngerTimer(3)
		pCity.changePopulation(-3)
	if StateBelief == iRoK:
		newUnit = pPlayer.initUnit(iRoKP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iRoKP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iRoKP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pCity.changeHurryAngerTimer(3)
		pCity.changePopulation(-3)
	if StateBelief == iEmpy:
		newUnit = pPlayer.initUnit(iEmpyP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iEmpyP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iEmpyP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pCity.changeHurryAngerTimer(3)
		pCity.changePopulation(-3)
	if StateBelief == iOrder:
		newUnit = pPlayer.initUnit(iOrderP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iOrderP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iOrderP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pCity.changeHurryAngerTimer(3)
		pCity.changePopulation(-3)
	if StateBelief == iOO:
		newUnit = pPlayer.initUnit(iOOP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iOOP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iOOP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pCity.changeHurryAngerTimer(3)
		pCity.changePopulation(-3)
	if StateBelief == iVeil:
		newUnit = pPlayer.initUnit(iVeilP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iVeilP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iVeilP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pCity.changeHurryAngerTimer(3)
		pCity.changePopulation(-3)
	if StateBelief == iWhiteHand:
		newUnit = pPlayer.initUnit(iWhiteP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iWhiteP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iWhiteP, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pCity.changeHurryAngerTimer(3)
		pCity.changePopulation(-3)
	if pCiv == Civ["Scions"]:
		newUnit = pPlayer.initUnit(iLegate, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iLegate, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit = pPlayer.initUnit(iLegate, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pCity.changeHurryAngerTimer(3)
		pCity.changePopulation(-3)

def reqDeathsDominion(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getNumUnits() < 25:
			return False
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		pTeam = gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) == 0:
			return False
	return True

def spellDeathsDominion(caster):
	iDominion = getInfoType('PROMOTION_UNDEATHS_DOMINION')
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if pUnit.getUnitCombatType() != -1:
			pUnit.setHasPromotion(iDominion, True)

def reqPioneer(caster):
	pPlot = caster.plot()
	if (pPlot.isOwned()
		or pPlot.getImprovementType() != -1
		or pPlot.isWater()):
		return False
	iMinDistance = 1
	getPlot	= CyMap().plot
	for x, y in plotsInRange( caster.getX(), caster.getY(), iMinDistance ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			iImprovement = pPlot.getImprovementType()
			if iImprovement != -1:
				if gc.getImprovementInfo(iImprovement).isFort():
					return False
	return True

def reqFieldFortification(caster):
	iCounterProm = getInfoType('PROMOTION_FIELD_FORTIFICATION_COUNTER')
	pPlayer = gc.getPlayer(caster.getOwner())
	iCounter = 0

	pPlot = caster.plot()
	if pPlot.getImprovementType() != -1:
		return False
	if pPlot.isCity():
		return False
	getPlot	= CyMap().plot
	iMinDistance = 1
	for x, y in plotsInRange( caster.getX(), caster.getY(), iMinDistance ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			iImprovement = pPlot.getImprovementType()
			if iImprovement != -1:
				if gc.getImprovementInfo(iImprovement).isFort():
					return False

	for i in xrange(caster.countHasPromotion(iCounterProm)):
		iCounter += 1
	if iCounter >= caster.getLevel():
		return False
	return True

def spellPioneer(caster):
	pPlot = caster.plot()
	iFeature = pPlot.getFeatureType()
	iCivType = gc.getPlayer(caster.getOwner()).getCivilizationType()
	if iFeature in ( getInfoType(forest) for forest in ('FEATURE_FOREST', 'FEATURE_FOREST_BURNT', 'FEATURE_FOREST_NEW', 'FEATURE_FOREST_ANCIENT', ) ):
		if iCivType not in ( getInfoType(elf) for elf in ('CIVILIZATION_LJOSALFAR', 'CIVILIZATION_SVARTALFAR', ) ):
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
	if iFeature in ( getInfoType(jungle) for jungle in ('FEATURE_JUNGLE', ) ):
		if iCivType not in ( getInfoType(lizard) for lizard in ('CIVILIZATION_CUALLI', 'CIVILIZATION_MAZATL', 'CIVILIZATION_CLAN_OF_EMBERS', ) ):
			pPlot.setFeatureType(FeatureTypes.NO_FEATURE, -1)
	caster.claimFort(True)
	if caster.isHasPromotion(getInfoType("PROMOTION_RECRUITER")):
		caster.setHasPromotion(getInfoType("PROMOTION_FIELD_FORTIFICATION_COUNTER"), True)

def reqBosom(caster):
	pPlot = caster.plot()
	if pPlot.isFlatlands() or pPlot.isPeak():
		return True
	return False

def spellBosom(caster):
	pPlot = caster.plot()
	pPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
	# test 1 Ronkhar NOT WORKING
	#pPlot.rebuildGraphics()
	 	 
	# test 2 Ronkhar
	# OK        Mine            mountain  --> hill
	# NOK       dwarven mine    mountain -> hill
	# NOK       dwarven mine    plain -> hill
	# CURIOUS   mine            plain -> hill
	# map = CyMap()
	# map.rebuildGraphics()
	
	# test 3 Ronkhar: similar to test2
	# rebuildGraphics()
	
	
	# declare war at plot owner
	if pPlot.isOwned():
		startWar(caster.getOwner(), pPlot.getOwner(), WarPlanTypes.WARPLAN_TOTAL)

def reqChin(caster):
	pPlot = caster.plot()
	if not pPlot.isHills():             # needs a hill
		return False
	if pPlot.isCity():                  # can't cast in city
		return False
	if pPlot.getBonusType(-1) != -1:    # can't cast if bonus
		return False
	# can't cast if one of the 4 vertical/horizontal neighbour tiles is a moutain or water
	iX = pPlot.getX()
	iY = pPlot.getY()
	getPlot = CyMap().plot
	for iiX,iiY in ADJPLUS1:
		pTempPlot = getPlot(iX+iiX,iY+iiY)
		if pTempPlot.isWater() or pTempPlot.isPeak():
			return False
	return True

def spellChin(caster):
	bCanCast = reqChin(caster)	# 2nd check in case the player settled after launching the spell or the player "cheated" by casting simultaneously Chin on 2 neighbour tiles
	if bCanCast:
		pPlot.setPlotType(PlotTypes.PLOT_PEAK, True, True)

def reqWomb(caster):
	return caster.plot().isHills()

def spellWomb(caster):
	pPlot = caster.plot()
	pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
	if pPlot.isOwned():
		startWar(caster.getOwner(), pPlot.getOwner(), WarPlanTypes.WARPLAN_TOTAL)

# Vitalize

baseVitalizeUpgrades = dict( ( getInfoType( start_terrain ), getInfoType( end_terrain ) )
							for start_terrain, end_terrain in [
								('TERRAIN_GLACIER', 'TERRAIN_TUNDRA'),
								('TERRAIN_TUNDRA', 'TERRAIN_TAIGA'),
								('TERRAIN_TAIGA', 'TERRAIN_PLAINS'),
								('TERRAIN_WASTELAND', 'TERRAIN_DESERT'),
								('TERRAIN_DESERT', 'TERRAIN_PLAINS'),
								('TERRAIN_PLAINS', 'TERRAIN_GRASS'),
								('TERRAIN_MARSH', 'TERRAIN_GRASS'),
								('TERRAIN_OCEAN', 'TERRAIN_COAST'),
								] )
civSpecificVitalize = dict()
civSpecificVitalize[Civ["Illians"]] = dict( ( getInfoType( start_terrain ), getInfoType( end_terrain ) )
							for start_terrain, end_terrain in [
								('TERRAIN_TUNDRA', 'TERRAIN_GLACIER'),
								('TERRAIN_TAIGA', 'TERRAIN_TUNDRA'),
								('TERRAIN_DESERT', 'TERRAIN_TUNDRA'),
								('TERRAIN_PLAINS', 'TERRAIN_TUNDRA'),
								('TERRAIN_WASTELAND', 'TERRAIN_TUNDRA'),
								('TERRAIN_GRASS', 'TERRAIN_TUNDRA'),
								('TERRAIN_MARSH', 'TERRAIN_TUNDRA'),
								('TERRAIN_BURNING_SANDS', 'TERRAIN_TUNDRA'),
								('TERRAIN_BROKEN_LANDS', 'TERRAIN_TUNDRA'),
								('TERRAIN_FIELDS_OF_PERDITION', 'TERRAIN_TUNDRA'),
								('TERRAIN_OCEAN', 'TERRAIN_COAST'),
								] )
civSpecificVitalize[Civ["Frozen"]] = dict (civSpecificVitalize[Civ["Illians"]])
civSpecificVitalize[Civ["Mazatl"]] = dict( baseVitalizeUpgrades )
civSpecificVitalize[Civ["Mazatl"]].update( dict( ( getInfoType( start_terrain ), getInfoType( end_terrain ) )
							for start_terrain, end_terrain in [
								('TERRAIN_GRASS', 'TERRAIN_MARSH'),
								('TERRAIN_MARSH', 'TERRAIN_MARSH'),
								] ) )
civSpecificVitalize[Civ["Cualli"]] = dict (civSpecificVitalize[getInfoType('CIVILIZATION_MAZATL')])
civSpecificVitalize[Civ["Malakim"]] = dict( baseVitalizeUpgrades )
civSpecificVitalize[Civ["Malakim"]].update( dict( ( getInfoType( start_terrain ), getInfoType( end_terrain ) )
							for start_terrain, end_terrain in [
								('TERRAIN_DESERT', 'TERRAIN_DESERT'),
								] ) )

def reqVitalize(caster):
	pPlayer = gc.getPlayer( caster.getOwner() )
	iRange = 1 + caster.getSpellExtraRange()
	vitalizeUpgrades = civSpecificVitalize.get( pPlayer.getCivilizationType(), baseVitalizeUpgrades )
	getPlot = CyMap().plot
	for x, y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone() and pPlot.getOwner() == caster.getOwner():
			terrain = pPlot.getTerrainType()
			if terrain in vitalizeUpgrades and vitalizeUpgrades[terrain] != terrain:
				return True
			if terrain == getInfoType('TERRAIN_DESERT') and pPlot.isRiver() and pPlot.isFlatlands() and not pPlot.isCity() and pPlot.getFeatureType()==-1:
				return True
	return False

def spellVitalize(caster,bInsideBorders=True):
	grass = getInfoType( 'TERRAIN_GRASS' )
	plains = getInfoType( 'TERRAIN_PLAINS' )
	desert = getInfoType( 'TERRAIN_DESERT' )
	floodPlains = getInfoType('FEATURE_FLOOD_PLAINS')
	ice = getInfoType('FEATURE_ICE')
	pPlayer = gc.getPlayer( caster.getOwner() )
	iRange = 1 + caster.getSpellExtraRange()
	vitalizeUpgrades = civSpecificVitalize.get( pPlayer.getCivilizationType(), baseVitalizeUpgrades )
	getPlot = CyMap().plot
	for x, y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone() and (pPlot.getOwner() == caster.getOwner() or not bInsideBorders):
			terrain = pPlot.getTerrainType()
			if terrain in vitalizeUpgrades:
				pPlot.setTerrainType( vitalizeUpgrades[terrain], True, True )
			# From here on terrain refers to what pPlot was before the upgrade
			if terrain == desert and pPlot.getFeatureType() == floodPlains and terrain != pPlot.getTerrainType():
				pPlot.setFeatureType(-1, -1)
			if pPlot.getTerrainType() == grass and pPlot.isHills() and pPlot.isCity():
				pPlot.setTerrainType( plains, True, True )
			if pPlot.isWater() and pPlot.getFeatureType() == ice:
				pPlot.setFeatureType(-1, -1)
			if terrain == getInfoType('TERRAIN_DESERT') and pPlot.isRiver() and pPlot.isFlatlands() and not pPlot.isCity() and pPlot.getFeatureType()==-1:
				pPlot.setFeatureType(floodPlains,1)
def reqVitalizeCompanion(caster):
	grass = getInfoType( 'TERRAIN_GRASS' )
	player = caster.getOwner()
	iRange = 1 + caster.getSpellExtraRange()
	getPlot = CyMap().plot
	for x,y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x,y)
		if not pPlot.isNone() and pPlot.getOwner() == player:
			terrain = pPlot.getTerrainType()
			if terrain == grass:
				return True

def spellVitalizeCompanion(caster):
	'''
	Transforms concentric circles of grassland to plains.
	'''
	grass = getInfoType( 'TERRAIN_GRASS' )
	plains = getInfoType( 'TERRAIN_PLAINS' )
	player = caster.getOwner()
	iRange = 1 + caster.getSpellExtraRange()
	getPlot = CyMap().plot
	for transformRange in xrange( iRange + 1 ):
		altered = False
		for x,y in plotsInCircularRange( caster.getX(), caster.getY(), transformRange, transformRange ):
			pPlot = getPlot(x,y)
			if not pPlot.isNone() and pPlot.getOwner() == player:
				terrain = pPlot.getTerrainType()
				if terrain == grass:
					pPlot.setTerrainType( plains, True, True )
					CyEngine().triggerEffect(getInfoType('EFFECT_SCORCH'), pPlot.getPoint())
					altered = True
		if altered:
			return

# Vitalize end

def spellGiftEssence(caster):
	pPlot = caster.plot()
	iXP = (caster.getLevel() * 100)
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == getInfoType('UNIT_DTESHI_COMMANDER'):
			pUnit.changeExperienceTimes100(iXP, -1, False, False, False)
			break

def reqDarkEmpowerment(caster):
	iEmpowerment = getInfoType('PROMOTION_DARK_EMPOWERMENT')
	pPlot = caster.plot()
	pPlayer			= gc.getPlayer(caster.getOwner())
	iMelee = getInfoType('UNITCOMBAT_DEFENSIVE_MELEE')
	if pPlayer.isHuman():
		Selected=0
		for iUnit in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(iUnit)
			if pUnit.IsSelected():
				Selected += 1
		if Selected > 1: # Prevent human player from casting spell if more than one unit is selected
			return False

	if not caster.isHasPromotion(iEmpowerment):
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getOwner() == caster.getOwner() and pUnit.getUnitCombatType() == iMelee and pUnit.getSummoner() == -1:
				return True
	return False

def spellDarkEmpowerment(caster):
	iEmpowerment = getInfoType('PROMOTION_DARK_EMPOWERMENT')
	caster.setHasPromotion(iEmpowerment, True)
	iOwner = caster.getOwner()
	pVictim = -1
	pPlot = caster.plot()
	iMelee = getInfoType('UNITCOMBAT_DEFENSIVE_MELEE')
	pVictim = WorstUnit(iOwner, pPlot, iMelee)
	if pVictim != -1:
		pVictim.kill(True, 0)

def spellSnowfallPassive(caster):
	gc			= CyGlobalContext()
	randNum		= CyGame().getSorenRandNum
	getPlot		= CyMap().plot
	iFlames 	= getInfoType('FEATURE_FLAMES')
	iFloodPlains= getInfoType('FEATURE_FLOOD_PLAINS')
	iForest 	= getInfoType('FEATURE_FOREST')
	iJungle 	= getInfoType('FEATURE_JUNGLE')
	iScrub 		= getInfoType('FEATURE_SCRUB')
	iSmoke 		= getInfoType('IMPROVEMENT_SMOKE')
	iTundra 	= getInfoType('TERRAIN_TUNDRA')
	iIce 		= getInfoType('FEATURE_ICE')
	iRange		= 2
	for x, y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			iRnd = randNum(12, "Snowfall") + 6
			if not pPlot.isWater():
				if pPlot.getTerrainType() != iTundra:
					pPlot.setTempTerrainType(iTundra, iRnd)
					if pPlot.getImprovementType() == iSmoke:
						pPlot.setImprovementType(-1)
					iFeature = pPlot.getFeatureType()
					if iFeature == iForest:
						pPlot.setFeatureType(iForest, 2)
					if iFeature == iJungle:
						pPlot.setFeatureType(iForest, 2)
					if iFeature == iFlames:
						pPlot.setFeatureType(-1, -1)
					if iFeature == iFloodPlains:
						pPlot.setFeatureType(-1, -1)
					if iFeature == iScrub:
						pPlot.setFeatureType(-1, -1)
			if pPlot.isWater():
				if pPlot.getFeatureType() != iIce:
					pPlot.setFeatureType(iIce, 0)

	return False

def effectWinter(pCaster):
	iTundra = getInfoType('TERRAIN_TUNDRA')
	iFlames = getInfoType('FEATURE_FLAMES')
	iFloodPlains = getInfoType('FEATURE_FLOOD_PLAINS')
	iForest = getInfoType('FEATURE_FOREST')
	iJungle = getInfoType('FEATURE_JUNGLE')
	iScrub = getInfoType('FEATURE_SCRUB')
	iSmoke = getInfoType('IMPROVEMENT_SMOKE')
	getPlot	= CyMap().plot
	iRange = 2
	for x, y in plotsInCircularRange( pCaster.getX(), pCaster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			if not pPlot.isWater():
				pPlot.setTerrainType(iTundra, True, True)
				if pPlot.getImprovementType() == iSmoke:
					pPlot.setImprovementType(-1)
				iFeature = pPlot.getFeatureType()
				if iFeature == iForest:
					pPlot.setFeatureType(iForest, 2)
				if iFeature == iJungle:
					pPlot.setFeatureType(iForest, 2)
				if iFeature == iFlames:
					pPlot.setFeatureType(-1, -1)
				if iFeature == iFloodPlains:
					pPlot.setFeatureType(-1, -1)
				if iFeature == iScrub:
					pPlot.setFeatureType(-1, -1)


def postCombatLossTriforce(pCaster, pOpponent):
	pOpponent.setHasPromotion(getInfoType('PROMOTION_TRIFORCE'), True)

def spellTriforce(pCaster):
	pPlot = pCaster.plot()
	iPlayer = pCaster.getOwner()
	iPlayer2 = pPlot.getOwner()
	iImprovement = pPlot.getImprovementType()
	pPlayer = gc.getPlayer(pCaster.getOwner())
	iUnit = getInfoType('UNITCLASS_FORT_COMMANDER')
	infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iUnit = infoCiv.getCivilizationUnits(iUnit)
	if iUnit == -1:
		iUnit = getInfoType('UNIT_FORT_COMMANDER')
	iRace = infoCiv.getDefaultRace()
	newUnit = pPlayer.initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	if iRace != -1:
		newUnit.setHasPromotion(iRace, True)
	pPlot.clearCultureControl(iPlayer2, iImprovement, 1)
	pPlot.setImprovementOwner(iPlayer)
	pPlot.addCultureControl(iPlayer, iImprovement, 1)
	newUnit.convert(pCaster)

def spellMobileFortCreate(pCaster):
	pPlot = pCaster.plot()
	iPlayer = pCaster.getOwner()
	iImprovement = pPlot.getImprovementType()
	pPlayer = gc.getPlayer(pCaster.getOwner())
	iUnit = getInfoType('UNIT_MOBILE_FORTRESS')
	if iImprovement != -1:
		pPlot.setImprovementType(-1)
	newUnit = pPlayer.initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.convert(pCaster)

def spellMobileFortSettleCastle(pCaster):
	pPlot = pCaster.plot()
	iPlayer = pCaster.getOwner()
	iPlayer2 = pPlot.getOwner()
	iImprovement = pPlot.getImprovementType()
	pPlayer = gc.getPlayer(pCaster.getOwner())
	iUnit = getInfoType('UNIT_FORT_COMMANDER')
	if iImprovement == -1:
		pPlot.setImprovementType(getInfoType('IMPROVEMENT_CASTLE'))
		iImprovement = pPlot.getImprovementType()
	newUnit = pPlayer.initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.convert(pCaster)
	pPlot.clearCultureControl(iPlayer2, iImprovement, 1)
	pPlot.setImprovementOwner(iPlayer)
	pPlot.addCultureControl(iPlayer, iImprovement, 1)
	newUnit.convert(pCaster)

def spellMobileFortSettleCitadel(pCaster):
	pPlot = pCaster.plot()
	iPlayer = pCaster.getOwner()
	iPlayer2 = pPlot.getOwner()
	iImprovement = pPlot.getImprovementType()
	pPlayer = gc.getPlayer(pCaster.getOwner())
	iUnit = getInfoType('UNIT_FORT_COMMANDER')
	if iImprovement == -1:
		pPlot.setImprovementType(getInfoType('IMPROVEMENT_CITADEL'))
		iImprovement = pPlot.getImprovementType()
	newUnit = pPlayer.initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.convert(pCaster)
	pPlot.clearCultureControl(iPlayer2, iImprovement, 1)
	pPlot.setImprovementOwner(iPlayer)
	pPlot.addCultureControl(iPlayer, iImprovement, 1)
	newUnit.convert(pCaster)

def reqMobileFortSettle(pCaster):
	pPlot = pCaster.plot()
	if pPlot.getImprovementType() != -1:
		return False
	if pPlot.isCity():
		return False
	return True

def spellPotionOfRestoration(caster):

	if (CyGame().getSorenRandNum(10, "Potion run out chance") < 3):
		caster.setHasPromotion(getInfoType('PROMOTION_POTION_OF_RESTORATION'), False)
		
def reqMasterOfForce(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iRange = 1 + caster.getSpellExtraRange()
	getPlot	= CyMap().plot
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		for i in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pTeam.isAtWar(pUnit.getTeam()):
				if not pUnit.getMasterUnit().isNone() or pUnit.getDuration() > 0:
					return True

def spellMasterOfForce(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iRange = 1 + caster.getSpellExtraRange()
	getPlot	= CyMap().plot
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		for i in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pTeam.isAtWar(pUnit.getTeam()):
				if not pUnit.getMasterUnit().isNone() or pUnit.getDuration() > 0:
					pUnit.kill(True, iPlayer)
	return False

def reqCommandUndead(caster):
	iHero = getInfoType('PROMOTION_HERO')
	iSpell = getInfoType('SPELL_COMMAND_UNDEAD')
	pPlayer = gc.getPlayer(caster.getOwner())
	if caster.getNumForcedMinions() >= 8:
		return False
	iResistMax = 40
	if not pPlayer.isHuman():
		iResistMax = 20
	if pPlayer.getCivilizationType() == Civ["Scions"]:
		iResistMax = 65
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iRange = 2 + caster.getSpellExtraRange()
	getPlot	= CyMap().plot
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.isHasPromotion(iHero):
				iResistMax = iResistMax + 20
			if pUnit.isHasPromotion(Race["Undead"]):
				if pTeam.isAtWar(pUnit.getTeam()):
					iResist = pUnit.getResistChance(caster, iSpell)
					if iResist <= iResistMax:
						return True
	return False

def spellCommandUndead(caster):
	iHero = getInfoType('PROMOTION_HERO')
	iSpell = getInfoType('SPELL_COMMAND_UNDEAD')
	pPlayer = gc.getPlayer(caster.getOwner())
	iResistMax = 40
	iBestValue = 0
	pBestUnit = -1
	if not pPlayer.isHuman():
		iResistMax = 20
	if pPlayer.getCivilizationType() == Civ["Scions"]:
		iResistMax = 65
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iRange = 2 + caster.getSpellExtraRange()
	getPlot	= CyMap().plot
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		for i in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.isHasPromotion(iHero):
				iResistMax = iResistMax + 20
			iValue = 0
			if pUnit.isHasPromotion(Race["Undead"]):
				if pTeam.isAtWar(pUnit.getTeam()):
					iResist = pUnit.getResistChance(caster, iSpell)
					if iResist <= iResistMax:
						iValue = pUnit.baseCombatStr() * 10
						iValue = iValue + (100 - iResist)
						if iValue > iBestValue:
							iBestValue = iValue
							pBestUnit = pUnit
	if pBestUnit != -1:
		pPlot = caster.plot()
		iPreviousOwner = pBestUnit.getOwner()
		if pBestUnit.isResisted(caster, iSpell) == False:
			CyInterface().addMessage(pBestUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_COMMAND_UNDEAD", ()),'',1,'Art/Civs/Dtesh/OpalusMortis.dds',ColorTypes(7),pBestUnit.getX(),pBestUnit.getY(),True,True)
			CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_COMMAND_UNDEAD_ENEMY", ()),'',1,'Art/Civs/Dtesh/OpalusMortis.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			newUnit = pPlayer.initUnit(pBestUnit.getUnitType(), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(pBestUnit)
			newUnit.changeImmobileTimer(1)
			newUnit.setPreviousOwner(iPreviousOwner)
			caster.addMinion(newUnit)
		else:
			CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOMINATION_FAILED", ()),'',1,'Art/Interface/Buttons/Spells/Domination.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)


def spellClanBlaze(caster):
	pPlot = caster.plot()
	pPlayer	= gc.getPlayer(caster.getOwner())
	if pPlayer.hasTrait(getInfoType('TRAIT_SCORCHED_EARTH')):
		pPlot.setFeatureType(getInfoType('FEATURE_FLAMES'),1)
	else:
		pPlot.setFeatureType(getInfoType('FEATURE_FOREST_BURNT'),1)

def reqRantineDomination(caster):
	iOrc	= gc.getORC_PLAYER()
	iHero	= getInfoType('PROMOTION_HERO')
	iSpell	= getInfoType('SPELL_RANTINE_DOMINATION')
	pPlayer	= gc.getPlayer(caster.getOwner())
	if caster.getNumForcedMinions() >= 8:
		return False
	iResistMax = 40
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iRange = 2 + caster.getSpellExtraRange()
	getPlot = CyMap().plot
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.isHasPromotion(iHero):
					iResistMax = iResistMax + 20
				if pUnit.getOwner == iOrc:
					iResist = pUnit.getResistChance(caster, iSpell)
					if iResist <= iResistMax:
						return True
	return False

def spellRantineDomination(caster):
	gc			= CyGlobalContext()
	iOrc 		= gc.getORC_PLAYER()
	iHero 		= getInfoType('PROMOTION_HERO')
	iSpell 		= getInfoType('SPELL_RANTINE_DOMINATION')
	pPlayer = gc.getPlayer(caster.getOwner())
	iResistMax = 40
	iBestValue = 0
	pBestUnit = -1
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	iRange = 2 + caster.getSpellExtraRange()
	getPlot = CyMap().plot
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.isHasPromotion(iHero):
					iResistMax = iResistMax + 20
				iValue = 0
				if pUnit.getOwner == iOrc:
					iResist = pUnit.getResistChance(caster, iSpell)
					if iResist <= iResistMax:
						iValue = pUnit.baseCombatStr() * 10
						iValue = iValue + (100 - iResist)
						if iValue > iBestValue:
							iBestValue = iValue
							pBestUnit = pUnit
	if pBestUnit != -1:
		pPlot = caster.plot()
		iPreviousOwner = pBestUnit.getOwner()
		if pBestUnit.isResisted(caster, iSpell) == false:
			CyInterface().addMessage(pBestUnit.getOwner(),true,25,CyTranslator().getText("TXT_KEY_MESSAGE_COMMAND_UNDEAD", ()),'',1,'Art/Civs/Dtesh/OpalusMortis.dds',ColorTypes(7),pBestUnit.getX(),pBestUnit.getY(),True,True)
			CyInterface().addMessage(caster.getOwner(),true,25,CyTranslator().getText("TXT_KEY_MESSAGE_COMMAND_UNDEAD_ENEMY", ()),'',1,'Art/Civs/Dtesh/OpalusMortis.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			newUnit = pPlayer.initUnit(pBestUnit.getUnitType(), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(pBestUnit)
			newUnit.changeImmobileTimer(1)
			newUnit.setPreviousOwner(iPreviousOwner)
			caster.addMinion(newUnit)
		else:
			CyInterface().addMessage(caster.getOwner(),true,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOMINATION_FAILED", ()),'',1,'Art/Interface/Buttons/Spells/Domination.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)

def spellClearSwamp(caster):
	pPlot = caster.plot()
	iImprovement = pPlot.getImprovementType()
	if iImprovement == Improvement["Swamp"]:
		pPlot.setImprovementType(-1)

def reqCreateSwamp(caster):
	pPlot = caster.plot()
	iTerrain = pPlot.getTerrainType()
	iImprovement = pPlot.getImprovementType()
	if iImprovement!=-1:
		if gc.getImprovementInfo(iImprovement).isUnique():
			return False
	if iTerrain == Terrain["Marsh"] and iImprovement != Improvement["Swamp"] and iImprovement not in UniqueImprovement.values():
		return True
	else:
		return False

def spellCreateSwamp(caster):
	pPlot = caster.plot()
	iTerrain = pPlot.getTerrainType()
	pPlot.setImprovementType(Improvement["Swamp"])

def reqShapeJungle(caster):
	pPlot = caster.plot()
	if (pPlot.getTerrainType() == Terrain["Grass"] or pPlot.getTerrainType() == Terrain["Marsh"]):
		if (pPlot.getFeatureType() == -1):
			return True
	return False

def reqDeepenForest(caster):
	pPlot = caster.plot()
	if (pPlot.getTerrainType() == Terrain["Grass"] or pPlot.getTerrainType() == Terrain["Marsh"]):
		return True
	return False

def spellShapeJungle(caster):
	pPlot = caster.plot()
	pPlot.setTempFeatureType(FeatureTypes.NO_FEATURE, -1, 0)
	pPlot.setFeatureType(getInfoType('FEATURE_JUNGLE'), 0)

def reqGiantSpiderUpgrade(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if (pPlayer.getNumCities() > 0):
		pNest = pPlayer.getCapitalCity()
		iNestPop = pNest.getPopulation()
		if iNestPop >= 12:
			return True
	return False

def reqIgnitePyre(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		pPlot = caster.plot()
		pTeam = gc.getTeam(pPlayer.getTeam())
		iRange = 1
		getPlot	= CyMap().plot
		for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
			pPlot = getPlot(x, y)
			if not pPlot.isNone():
				for i in range(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					p2Player = gc.getPlayer(pUnit.getOwner())
					e2Team = p2Player.getTeam()
					if pTeam.isAtWar(e2Team) == True:
						return True
		return False
	return True

def spellIgnitePyre(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iUnit = getInfoType('UNIT_PYRE_ZOMBIE')
	newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.finishMoves()
	newUnit.setHasCasted(True)


def reqAllowCheats(caster):
	return CvEventInterface.getEventManager().bAllowCheats

def spellSelfDestruct(caster):
	gc 	= CyGlobalContext()
	iRange = 2
	getPlot = CyMap().plot
	for x, y in plotsInCircularRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		for i in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			pUnit.kill(True, PlayerTypes.NO_PLAYER)
		if not pPlot.isWater():
			pPlot.setFeatureType(-1, -1)
			pPlot.setFeatureType(getInfoType('FEATURE_FALLOUT'), 0)
	caster.kill(True,-1)

def reqAddToCityDtesh(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if (pCity.getPopulation() >= pCity.getCityPopulationCap()):
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		if pCity.getOwner() != caster.getOwner():
			return False
	return True

def spellRemoveFromCityDtesh(pCaster):
	pPlot = pCaster.plot()
	pPlayer = gc.getPlayer(pCaster.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_SLAVE_UNDEAD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellUndeadLivingUnit(pCaster):
	pCaster.setHasPromotion(Race["Undead"], True)

def reqCorruptFort(pCaster):
	pPlot = pCaster.plot()
	iPlayer = pPlot.getOwner()
	iImprovement = pPlot.getImprovementType()
	iMaus1 = getInfoType('IMPROVEMENT_DTESH_MAUSOLEUM_LESSER')
	iMaus2 = getInfoType('IMPROVEMENT_DTESH_MAUSOLEUM')
	iMaus3 = getInfoType('IMPROVEMENT_DTESH_MAUSOLEUM_GREATER')
	if iPlayer != -1:
		if iImprovement != -1:
			pImprovement = gc.getImprovementInfo(iImprovement)
			if pImprovement.isFort() and not pImprovement.isUnique():
				if not pCaster.isHasPromotion(getInfoType('PROMOTION_MAUSOLEUM')):
					return True
	return False

def spellCorruptFort(pCaster):
	pPlot = pCaster.plot()
	iPlayer = pPlot.getOwner()
	iImprovement = pPlot.getImprovementType()
	pPlot.clearCultureControl(iPlayer, iImprovement, 1)
	pPlot.setImprovementType(getInfoType('IMPROVEMENT_DTESH_MAUSOLEUM_LESSER'))
	iImprovement = pPlot.getImprovementType()
	pPlot.setImprovementOwner(iPlayer)
	pPlot.addCultureControl(iPlayer, iImprovement, 1)

def postCombatWinDteshAffinityEntropy(pCaster, pOpponent):
	pPlot = pCaster.plot()
	pEnemyPlot = pOpponent.plot()
	pPlayer = gc.getPlayer(pCaster.getOwner())
	iEntropyNum = pPlayer.getNumAvailableBonuses(getInfoType('BONUS_MANA_ENTROPY'))
	iWasteland = getInfoType('TERRAIN_WASTELAND')

	if pPlot.getTerrainType() != iWasteland:
		if CyGame().getSorenRandNum(100, "Wasteland Chance") < (iEntropyNum * 5):
			pPlot.setTempTerrainType(iWasteland, 10)
			pEnemyPlot.setTempTerrainType(iWasteland, 5)

def postCombatLossDteshAffinityEntropy(pCaster, pOpponent):
	pPlot = pCaster.plot()
	pEnemyPlot = pOpponent.plot()
	pPlayer = gc.getPlayer(pCaster.getOwner())
	iEntropyNum = pPlayer.getNumAvailableBonuses(getInfoType('BONUS_MANA_ENTROPY'))
	iWasteland = getInfoType('TERRAIN_WASTELAND')

	if pPlot.getTerrainType() != iWasteland:
		if CyGame().getSorenRandNum(100, "Wasteland Chance") < (iEntropyNum * 5):
			pPlot.setTempTerrainType(iWasteland, 10)
			pEnemyPlot.setTempTerrainType(iWasteland, 5)

def reqDefileCrypt(caster):
	pPlot = caster.plot()

	if pPlot.isCityRadius():
		return True
	return False

def spellDefileCrypt(pCaster):
	pPlot = pCaster.plot()
	pPlayer = gc.getPlayer(pCaster.getOwner())
	pPlot.setImprovementType(getInfoType('IMPROVEMENT_DTESH_CRYPT_DEFILED'))
	newUnit = pPlayer.initUnit(getInfoType('UNIT_SLAVE_UNDEAD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


#Snarko 26-06-2010
#Making lairs use the SDK/XML system. But not all of them...
# Note: This one is mostly depreciated; custom function one used more often. Should probably be merged... later...
def exploreLairBigBad(argsList):
	pUnit, pPlot = argsList
	Manager		= CvEventInterface.getEventManager()
	gc = CyGlobalContext()
	getTeam 			= gc.getTeam
	getGame				= gc.getGame
	isOption			= gc.getGame().isOption
	orcTeam				= gc.getORC_TEAM()
	animalTeam			= gc.getANIMAL_TEAM()
	demonTeam			= gc.getDEMON_TEAM()
	if not pUnit.isNone():
		iPlayer 		= pUnit.getOwner()
	else:
		iPlayer			= pPlot.getOwner()
	getPlayer 			= gc.getPlayer
	pPlayer				= getPlayer(iPlayer)
	iTeam 				= pPlayer.getTeam()
	bOrcs 				= False
	bDemons		 		= False
	bAnimals 			= False
	iSpawnPlayer 		= -1
	iNoAI				= UnitAITypes.NO_UNITAI
	iSouth				= DirectionTypes.DIRECTION_SOUTH
	isAtWar 			= getTeam(iTeam).isAtWar
	isAtWarOrcs 		= isAtWar(orcTeam)
	isAtWarAnimals		= isAtWar(animalTeam)
	isAtWarDemons 		= isAtWar(demonTeam)
	game 				= CyGame()
	getGlobalCounter	= game.getGlobalCounter()
	bNoBarbarians 		= isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS)
	bNoAnimals 			= isOption(GameOptionTypes.GAMEOPTION_NO_ANIMALS)
	bNoDemons 			= isOption(GameOptionTypes.GAMEOPTION_NO_DEMONS)
	iFeature			= pPlot.getFeatureType()
	#Terrain				= Manager.Terrain
	randNum 			= game.getSorenRandNum
	spawnPlayers = []
	if isAtWarOrcs and not bNoBarbarians:
		spawnPlayers += [orcTeam]
	if isAtWarAnimals and not bNoAnimals:
		spawnPlayers += [animalTeam]
	if isAtWarDemons and not bNoDemons:
		spawnPlayers += [demonTeam]
	if len(spawnPlayers) > 0:
		iSpawnPlayer = spawnPlayers[randNum(len(spawnPlayers), "Choose Barbarian for BigBad")]
		if iSpawnPlayer == orcTeam:
			bOrcs = True
		elif iSpawnPlayer == animalTeam:
			bAnimals = True
		elif iSpawnPlayer == demonTeam:
			bDemons = True
	else:
		return 0

	lPromoList = []
	lList = []
	lHenchmanList = []
	if bDemons:
		lList += ['UNIT_AZER']
		lHenchmanList += ['UNIT_AZER']
	if bAnimals:
		lList += ['UNIT_ROC']
		lHenchmanList += ['UNIT_ROC']
		lPromoList = ['PROMOTION_MUTATED', 'PROMOTION_CANNIBALIZE', 'PROMOTION_MOBILITY1', 'PROMOTION_STRONG', 'PROMOTION_BLITZ', 'PROMOTION_COMMAND1', 'PROMOTION_HEROIC_STRENGTH', 'PROMOTION_HEROIC_DEFENSE', 'PROMOTION_MAGIC_IMMUNE', 'PROMOTION_STONESKIN', 'PROMOTION_VALOR', 'PROMOTION_VILE_TOUCH']
	if not grace():
		if bDemons:
			lList += ['UNIT_AIR_ELEMENTAL']
	if not pPlot.isWater():
		if bOrcs:
			lList += ['UNIT_OGRE', 'UNIT_ASSASSIN', 'UNIT_AXEMAN', 'UNIT_AXEMAN', 'UNIT_AXEMAN', 'UNIT_WOLF_RIDER', 'UNIT_LIZARDMAN']
			lHenchmanList += ['UNIT_AXEMAN', 'UNIT_AXEMAN', 'UNIT_AXEMAN', 'UNIT_WOLF_RIDER', 'UNIT_LIZARDMAN', 'UNIT_WARRIOR', 'UNIT_WARRIOR', 'UNIT_WARRIOR', 'UNIT_WARRIOR', 'UNIT_WARRIOR', 'UNIT_GOBLIN', 'UNIT_GOBLIN', 'UNIT_GOBLIN', 'UNIT_GOBLIN', 'UNIT_GOBLIN']
		if bAnimals:
			lList += ['UNIT_GIANT_SPIDER', 'UNIT_LION', 'UNIT_RED_DRAKE']
			lHenchmanList += ['UNIT_WOLF', 'UNIT_LION', 'UNIT_TIGER', 'UNIT_BABY_SPIDER', 'UNIT_FAWN']
		if bDemons:
			lList += ['UNIT_SPECTRE', 'UNIT_HELLHOUND', 'UNIT_SKELETON', 'UNIT_SKELETON', 'UNIT_SKELETON', 'UNIT_SUCCUBUS', 'UNIT_DROWN', 'UNIT_DISEASED_CORPSE', 'UNIT_DISEASED_CORPSE', 'UNIT_DISEASED_CORPSE', 'UNIT_PYRE_ZOMBIE']
			lHenchmanList += ['UNIT_CHAOS_MARAUDER', 'UNIT_MISTFORM', 'UNIT_SKELETON', 'UNIT_SKELETON', 'UNIT_SKELETON', 'UNIT_DISEASED_CORPSE', 'UNIT_DISEASED_CORPSE', 'UNIT_DISEASED_CORPSE', 'UNIT_HELLHOUND', 'UNIT_HELLHOUND']
		if not grace():
			if bOrcs:
				lList += ['UNIT_OGRE_WARCHIEF']
				lHenchmanList += ['UNIT_OGRE']
			if bAnimals:
				lList += ['UNIT_MYCONID', 'UNIT_SATYR']
			if bDemons:
				lList += ['UNIT_EARTH_ELEMENTAL', 'UNIT_FIRE_ELEMENTAL', 'UNIT_GARGOYLE', 'UNIT_VAMPIRE', 'UNIT_EIDOLON', 'UNIT_LICH']
				lPromoList = lPromoList + ['PROMOTION_FIRE2', 'PROMOTION_AIR2', 'PROMOTION_HERO', 'PROMOTION_MARKSMAN', 'PROMOTION_SHADOWWALK']
	if iFeature == Feature["Forest"] or iFeature == Feature["Ancient Forest"]:
		if bAnimals:
			lList += ['UNIT_TREANT']
	if pPlot.getTerrainType() == Terrain["Tundra"]:
		if bOrcs:
			lHenchmanList += ['UNIT_FROSTLING_ARCHER', 'UNIT_FROSTLING_WOLF_RIDER']
		if bAnimals:
			lHenchmanList += ['UNIT_WHITE_DRAKE']
	if pPlot.isHills():
			if bOrcs:
				lList += ['UNIT_HILL_GIANT']
				lPromoList = ['PROMOTION_GUERILLA1','PROMOTION_GUERILLA2']
	if iFeature == Feature["Forest"] or iFeature == Feature["Ancient Forest"]:
		if bAnimals:
			lList += ['UNIT_TREANT','UNIT_SATYR']
			lHenchmanList += ['UNIT_TIGER', 'UNIT_BABY_SPIDER', 'UNIT_FAWN']
			lPromoList = lPromoList + ['PROMOTION_WOODSMAN1', 'PROMOTION_WOODSMAN2']
	if pPlot.getImprovementType() == Lair["Barrow"]:
		if bDemons:
			lList += ['UNIT_SPECTRE']
			lHenchmanList += ['UNIT_SKELETON', 'UNIT_PYRE_ZOMBIE']
			lPromoList = lPromoList + ['PROMOTION_DEATH2']
		if not grace():
			if bDemons:
				lList += ['UNIT_LICH', 'UNIT_WRAITH']
	if pPlot.getImprovementType() == Lair["Ruins"]:
		lPromoList = lPromoList + ['PROMOTION_POISONED_BLADE']
		if bOrcs:
			lHenchmanList += ['UNIT_LIZARDMAN']
		if bAnimals:
			lHenchmanList += ['UNIT_GORILLA_TROOP']
		if not grace():
			if bDemons:
				lList += ['UNIT_MANTICORE']
	if getGlobalCounter > 40:
		if bDemons:
			lList += ['UNIT_PIT_BEAST', 'UNIT_DEATH_KNIGHT', 'UNIT_BALOR']
			lHenchmanList += ['UNIT_IMP', 'UNIT_HELLHOUND']
			lPromoList = lPromoList + ['PROMOTION_FEAR']
	if pPlot.isWater():
		if bOrcs:
			lList += ['UNIT_PIRATE']
			lHenchmanList += ['UNIT_PIRATE']
		if bAnimals:
			lList += ['UNIT_SEA_SERPENT']
		if bDemons:
			lList += ['UNIT_STYGIAN_GUARD']
			lHenchmanList += ['UNIT_DROWN']
		if not grace():
			if bAnimals:
				lList += ['UNIT_KRAKEN']
			if bDemons:
				lList += ['UNIT_WATER_ELEMENTAL']

	sMonster 	= lList[randNum(len(lList), "Pick Monster")]
	sHenchman 	= lHenchmanList[randNum(len(lHenchmanList), "Pick Henchman")]
	iUnit 		= getInfoType(sMonster)
	iHenchman 	= getInfoType(sHenchman)
	newUnit 	= addUnitFixed(pPlot, iUnit, iSpawnPlayer)
	if newUnit != -1:
		setPromo 	= newUnit.setHasPromotion
		for i in xrange(randNum(len(lPromoList)/4 + 1, "Pick Promotion Quantity")):
			sPromo = lPromoList[randNum(len(lPromoList), "Pick Promotion")]
			setPromo(getInfoType(sPromo), True)
		newUnit.setName(CvEventInterface.getEventManager().cf.MarnokNameGenerator(newUnit))
##		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_BIGBAD",()),'',1,gc.getUnitInfo(iUnit).getButton(),ColorTypes(7),newUnit.getX(),newUnit.getY(),True,True)
		bPlayer = getPlayer(iSpawnPlayer)
		iHench1 = randNum(4, "BigBad Lair Henchmen number 1")
		iHench2 = randNum(4, "BigBad Lair Henchmen number 2")
		if pUnit != -1:
			iNoBadMod = pUnit.getNoBadExplore()/10
		else:
			iNoBadMod = -1
		iHenchtotal = iHench1 + iHench2 - iNoBadMod
		getHandicap = getGame().getHandicapType()
		if iHenchtotal > int(getHandicap):
			iHenchtotal = int(getHandicap)
		initUnit = bPlayer.initUnit
		iX = newUnit.getX()
		iY = newUnit.getY()
		for i in xrange(iHenchtotal):
			initUnit(iHenchman, iX, iY, iNoAI, iSouth)
	return


def exploreLairPortal(argsList):
	pUnit, pPlot	= argsList
	iPlayer			= pUnit.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iUnit			= pUnit.getID()
	if pPlayer.isHuman():
		popupInfo		= CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("passToModNetMessage")
		popupInfo.setData1(iUnit)
		popupInfo.setData2(iPlayer)
		popupInfo.setData3(107) # onModNetMessage id
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_PORTAL", ()))
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_PORTAL_1", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_PORTAL_2", ()),"")
		popupInfo.addPopup(iPlayer)
	else:
		AIPick = CyGame().getSorenRandNum(2, "LairPortal AI pick")
		argsList = [AIPick,iUnit,iPlayer]
		effectLairPortal(argsList)

def effectLairPortal(argsList):
	iButtonId	= argsList[0]
	iUnit		= argsList[1]
	iPlayer		= argsList[2]
	pUnit		= gc.getPlayer(iPlayer).getUnit(iUnit)
	if iButtonId == 0:
		iBestValue = 0
		pBestPlot = -1
		for i in xrange (CyMap().numPlots()):
			iValue = 0
			pPlot = CyMap().plotByIndex(i)
			if not pPlot.isWater() and not pPlot.isPeak() and pPlot.getNumUnits() == 0:
				iValue = CyGame().getSorenRandNum(1000, "Portal")
				if not pPlot.isOwned():
					iValue += 1000
				if iValue > iBestValue:
					iBestValue = iValue
					pBestPlot = pPlot
		if pBestPlot != -1:
			pUnit.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True,False)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_PORTAL",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pBestPlot.getX(),pBestPlot.getY(),True,True)

def exploreLairDwarfVsLizard(argsList):
	pUnit, pPlot	= argsList
	iPlayer			= pUnit.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iUnit			= pUnit.getID()
	if pPlayer.isHuman():
		popupInfo	= CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("effectHumanLairDwarfVsLizard") # if the popup is using all 3 iData to work, ignore passToModNetMessage, sendModNetMessage with separate function
		popupInfo.setPythonModule("CvSpellInterface")
		popupInfo.setData1(iUnit)
		popupInfo.setData2(iPlayer)
		popupInfo.setData3(1)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_DWARF_VS_LIZARDMEN", ()))
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_DWARF_VS_LIZARDMEN_1", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_DWARF_VS_LIZARDMEN_2", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_DWARF_VS_LIZARDMEN_3", ()),"")
		popupInfo.addPopup(iPlayer)
	else:
		AIPick = CyGame().getSorenRandNum(2, "DwarfVsLizard AI pick")
		if gc.getCivilizationInfo(pPlayer.getCivilizationType()).getDefaultRace() == gc.getInfoTypeForString("PROMOTION_DWARF"):
			AIPick = 0
		if gc.getCivilizationInfo(pPlayer.getCivilizationType()).getDefaultRace() == gc.getInfoTypeForString("PROMOTION_LIZARDMAN") or gc.getCivilizationInfo(pPlayer.getCivilizationType()).getDefaultRace() == gc.getInfoTypeForString("PROMOTION_LIZARDMAN_MAZATL") or gc.getCivilizationInfo(pPlayer.getCivilizationType()).getDefaultRace() == gc.getInfoTypeForString("PROMOTION_LIZARDMAN_CUALLI"):
			AIPick = 1
		argsList = [AIPick,iUnit,iPlayer,1]
		effectLairDwarfVsLizard(argsList)

def effectHumanLairDwarfVsLizard(argsList):
	iButtonId		= argsList[0]
	iUnit			= argsList[1]
	iPlayer			= argsList[2]
	pType			= argsList[3]
	CyMessageControl().sendModNetMessage(108,iButtonId,iUnit,iPlayer,pType)

def effectLairDwarfVsLizard(argsList):
	iButtonId		= argsList[0]
	iUnit			= argsList[1]
	iPlayer			= argsList[2]
	pType			= argsList[3]
	if iButtonId == 2:
		return
	git				= gc.getInfoTypeForString
	pPlayer			= gc.getPlayer(iPlayer)
	pUnit			= pPlayer.getUnit(iUnit)
	pPlot			= pUnit.plot()
	pNewPlot		= findClearPlot(-1, pPlot)
	bPlayer			= gc.getPlayer(gc.getORC_PLAYER())
	pPlayer1		= bPlayer
	pPlayer2		= bPlayer
	iCount1			= 3
	iCount2			= 3
	pPlot1			= pNewPlot
	pPlot2			= pNewPlot
	bBronze			= False
	bPoison			= False
	if pType == 1:		# DwarfVsLizard
		pUnitType1	= git("UNIT_AXEMAN")
		pUnitType2	= git("UNIT_LIZARDMAN")
	elif pType == 2:	# RedVsYellow
		pUnitType1	= git("UNIT_ARCHER_SCORPION_CLAN")
		pUnitType2	= git("UNIT_GOBLIN_MURIS_CLAN")
	if bPlayer.isHasTech(git('TECH_BRONZE_WORKING')):
		bBronze = True
	if bPlayer.isHasTech(git('TECH_HUNTING')):
		bPoison = True
	if iButtonId == 0:
		pPlayer1	= pPlayer
		iCount1		= 2
		pPlot1		= pPlot
	elif iButtonId == 1:
		pPlayer2	= pPlayer
		iCount2		= 2
		pPlot2		= pPlot
	if pNewPlot != -1:
		for i in xrange(iCount1):
			newUnitFirst = pPlayer1.initUnit(pUnitType1, pPlot1.getX(), pPlot1.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pType == 1:
				newUnitFirst.setHasPromotion(git('PROMOTION_DWARF'), True)
				if bBronze == True:
					newUnitFirst.setHasPromotion(git('PROMOTION_BRONZE_WEAPONS'), True)
			elif bPoison == True and pType == 2:
				newUnitFirst.setHasPromotion(git('PROMOTION_POISONED_WEAPON'), True) # Poisoned Blade switched for Poisoned Weapon
		for j in xrange(iCount2):
			newUnitSecond = pPlayer2.initUnit(pUnitType2, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if bPoison == True:
				newUnitSecond.setHasPromotion(git('PROMOTION_POISONED_BLADE'), True)

def exploreLairDepths(argsList):
	pUnit, pPlot	= argsList
	iPlayer			= pUnit.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iUnit			= pUnit.getID()
	if pPlayer.isHuman():
		popupInfo	= CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("passToModNetMessage")
		popupInfo.setData1(iUnit)
		popupInfo.setData2(iPlayer)
		popupInfo.setData3(109) # onModNetMessage id
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_DEPTHS", ()))
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_DEPTHS_1", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_DEPTHS_2", ()),"")
		popupInfo.addPopup(iPlayer)
	else:
		AIPick = CyGame().getSorenRandNum(2, "LairDepth AI pick")
		argsList = [AIPick,iUnit,iPlayer]
		effectLairDepths(argsList)

def effectLairDepths(argsList):
	iButtonId	= argsList[0]
	iUnit		= argsList[1]
	iPlayer		= argsList[2]
	pPlayer		= gc.getPlayer(iPlayer)
	pUnit		= pPlayer.getUnit(iUnit)
	git			= gc.getInfoTypeForString
	if iButtonId == 0:
		possibleGoodies = []
		iRnd = CyGame().getSorenRandNum(2, "Lair Depth, Roll Class")
		if iRnd == 0:
			eGoodyClass = git("GOODYCLASS_GENERIC_MODERATE")
		else:
			eGoodyClass = git("GOODYCLASS_GENERIC_MAJOR")
		for i in xrange(gc.getNumGoodyInfos()):
			if gc.getGoodyInfo(i).isGoodyClassType(eGoodyClass):
				if (pPlayer.canReceiveGoody(pUnit.plot(), i, pUnit)):
					possibleGoodies.append(i)
		if possibleGoodies:
			eGoody = possibleGoodies[CyGame().getSorenRandNum(len(possibleGoodies), "Lair Depth, Roll Goody")]
			pPlayer.receiveGoody(pUnit.plot(), eGoody, pUnit)

def exploreLairTreasure(argsList):
	pUnit, pPlot = argsList
	Manager		= CvEventInterface.getEventManager()
	placeTreasure(pUnit.getOwner(), Manager.Units["Equipment"]["Treasure"])
	return

def exploreLairGoldenAge(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())
	return

def exploreBlightedForest(argsList):
	pUnit, pPlot	= argsList
		#TODO What if the animal civ is turned off?
	pPlayer			= gc.getPlayer(pUnit.getOwner())
	pTeam			= gc.getTeam(pPlayer.getTeam())
	iRnd			= CyGame().getSorenRandNum(100, "Explore Blighted Forest")
	iRnd			+= pUnit.getNoBadExplore()/2
	pNewPlot		= findClearPlot(-1, pPlot) #r363 fixing pushing units out

	if pTeam.isHasTech(getInfoType('TECH_IRON_WORKING')):
		iRnd += 20

	if iRnd < 30:
		pPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())
		newUnit = pPlayer.initUnit(getInfoType('UNIT_MALIGNANT_FLORA'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	elif iRnd >= 30 and iRnd < 40:
		pPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())
		newUnit = pPlayer.initUnit(getInfoType('UNIT_BEAR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setDamage(25, -1)
		newUnit.setHasPromotion(getInfoType('PROMOTION_DISEASED'), True)
	elif iRnd >= 40:
		pPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())
		newUnit = pPlayer.initUnit(getInfoType('UNIT_WOLF'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setDamage(25, -1)
		newUnit.setHasPromotion(getInfoType('PROMOTION_DISEASED'), True)
	return

def exploreLairArmageddonIncrease(argsList):
	pUnit, pPlot = argsList
	gc = CyGlobalContext()
	gc.getGame().changeGlobalCounter(3)
	
def exploreLairArmageddonDecrease(argsList):
	pUnit, pPlot = argsList
	gc = CyGlobalContext()
	gc.getGame().changeGlobalCounter(-3)

def exploreLairFort(argsList):
	pUnit, pPlot = argsList
	gc = CyGlobalContext()
	getInfoType 		= gc.getInfoTypeForString
	pPlot.setImprovementType(getInfoType("IMPROVEMENT_FORT"))
	
def exploreLairVitalize(argsList):
	pUnit, pPlot = argsList
	gc = CyGlobalContext()
	getInfoType 		= gc.getInfoTypeForString
	spellVitalize(pUnit,False)
	
def exploreLairDungeon(argsList):
	pUnit, pPlot = argsList
	gc = CyGlobalContext()
	getInfoType 		= gc.getInfoTypeForString
	pPlot.setImprovementType(getInfoType("IMPROVEMENT_DUNGEON"))

def exploreLairGraveyard(argsList):
	pUnit, pPlot = argsList
	gc = CyGlobalContext()
	getInfoType 		= gc.getInfoTypeForString
	pPlot.setImprovementType(getInfoType("IMPROVEMENT_GRAVEYARD"))

def exploreLairPopulation(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	pCapital = pPlayer.getCapitalCity()
	pNearestCity = CyMap().findCity(pUnit.getX(), pUnit.getY(), -1, pUnit.getTeam(), False, False, -1, -1, pCapital, False)
	pNearestCity.changePopulation(1)

def exploreLairResurrect(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	pCapital = pPlayer.getCapitalCity()
	if (not gc.isNoCrash()):
		if pUnit.canCastResurrect():
			pUnit.castResurrect()

def exploreLairSpecterEvil(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_SPECTRE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_PROPHECY_MARK'),True)
	
def exploreLairSpecterNeutral(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SPECTRE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_PROPHECY_MARK'),True)
	
def exploreLairBhallHighPriest(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_PRIEST_OF_BHALL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_FIRE1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_FIRE2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_FIRE3'),True)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_FIRE_ELEMENTAL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairGolemDefender(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_NULLSTONE_GOLEM'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_NULLSTONE_GOLEM'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairUnblemishedShelter(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_PHOENIX'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_DRUID'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_DRUID'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_DRUID'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_GUARDIAN'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_GUARDIAN'),True)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_GUARDIAN'),True)

def reqUnblemishedShelter(argsList):
	pUnit, pPlot		= argsList
	getPlot				= CyMap().plot
	return (not CyGame().isUnitClassMaxedOut(getInfoType("UNITCLASS_PHOENIX"),0))
	
def exploreLairMurderhoof(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MURDERHOOF'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_AWAKENED'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_HERO'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)

def exploreLairSeedDragon(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SEED_DRAGON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairScaledDragon(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SCALED_DRAGON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	
def exploreLairKezef(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_KEZEF'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	
def exploreLairUndeadCarnival(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MIMIC'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UNDEAD'),True)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_MIMIC'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_UNDEAD'),True)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_FREAK'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_UNDEAD'),True)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_FREAK'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_UNDEAD'),True)
	
def exploreLairVelgyrKnight(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_KNIGHT_VELGYR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairClockworkGolem(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_CLOCKWORK_GOLEM'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
def exploreLairVelgyrKnight2(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = pPlayer.initUnit(getInfoType('UNIT_KNIGHT_VELGYR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
	
def exploreLairHallWarriorsEvil(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_HONORED_BAND'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ENCHANTED_BLADE'),True)
	
def exploreLairGatesHell(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_BALOR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_LEASH_1'),True)
	pNewPlot.setImprovementType(getInfoType("IMPROVEMENT_HELLFIRE"))
	
def exploreLairHauntedSpawn(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	for x, y in plotsInRange( pUnit.getX(), pUnit.getY(), 1 ):
		getPlot	= CyMap().plot
		pLoopPlot = getPlot(x, y)
		pLoopPlot.setPlotEffectType(getInfoType("PLOT_EFFECT_HAUNTED_LANDS"))
	
def exploreLairMimicEnemy(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MIMIC'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	for id in range(gc.getNumPromotionInfos()):
		if pUnit.isHasPromotion(id) and not gc.getPromotionInfo(id).isEquipment():
			newUnit.setHasPromotion(id,True)

def exploreLairGoblinConflictRedYellow(argsList):
	pUnit, pPlot	= argsList
	iPlayer			= pUnit.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	iUnit			= pUnit.getID()
	if pPlayer.isHuman():
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("effectHumanLairDwarfVsLizard") # if the popup is using all 3 iData to work, ignore passToModNetMessage, sendModNetMessage with separate function
		popupInfo.setPythonModule("CvSpellInterface")
		popupInfo.setData1(iUnit)
		popupInfo.setData2(iPlayer)
		popupInfo.setData3(2)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_RED_VS_YELLOW", ()))
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_RED_VS_YELLOW_1", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_RED_VS_YELLOW_2", ()),"")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_EXPLORE_LAIR_RED_VS_YELLOW_3", ()),"")
		popupInfo.addPopup(iPlayer)
	else:
		AIPick		= CyGame().getSorenRandNum(3, "RedVsYellow AI pick")
		argsList	= [AIPick,iUnit,iPlayer,2]
		effectLairDwarfVsLizard(argsList)
	
def exploreLairMurisPrisoner(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_GOBLIN_MURIS_CLAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairLukosPrisoner(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_GOBLIN_LUKOS_CLAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairNeithPrisoner(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_GOBLIN_NEITH_CLAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairScorpionPrisoner(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_GOBLIN_SCORPION_CLAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			
def exploreLairGoblinTroop(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_GOBLIN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_HEROIC'),True)
	
def exploreLairGoblinAdept(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_ADEPT_MURIS_CLAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_FIRE1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_CHAOS1'),True)

def exploreLairCannibalCentaur(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CENTAUR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_CANNIBALIZE'),True)

def exploreLairClanChiefDuel(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CENTAUR_CLANCHIEF'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.changeDamage(70,0)

def exploreLairMulyalfar(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_ICE_DRUID'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.changeDamage(70,0)

def exploreLairPriestWinter(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_PRIEST_OF_WINTER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.changeDamage(70,0)
	newUnit.setHasPromotion(getInfoType("PROMOTION_IMMORTAL"),True)

def exploreLairFrostlingWarrior(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_FROSTLING_AXEMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.changeDamage(70,0)
	newUnit.setHasPromotion(getInfoType("PROMOTION_MITHRIL_WEAPONS"),True)
	newUnit.setHasPromotion(getInfoType("PROMOTION_MAGIC_IMMUNE"),True)

def exploreLairDwarvenDruid(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_DWARVEN_DRUID'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.changeDamage(70,0)

def exploreLairBoardingParty(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_BOARDING_PARTY'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairVelgyrGolem2(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_VELGYR_GOLEM'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairSuccubus(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairNemed(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_NEMED'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairSeaSerpent2(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_SEA_SERPENT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairEinherjarVsDiseasedCorpse(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_DISEASED_CORPSE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_EINHERJAR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairEinherjar2(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_EINHERJAR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairPegasus(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_PEGASUS'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairSlyph(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_SLYPH'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairStag(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_STAG'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairGoat(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	RndApophis = gc.getGame().getSorenRandNum(25, "Apophis")
	if RndApophis == 21 and CyGame().getUnitCreatedCount(getInfoType('UNIT_GOAT_2')) == 0:
		newUnit = pPlayer.initUnit(getInfoType('UNIT_GOAT_2'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	else:
		newUnit = pPlayer.initUnit(getInfoType('UNIT_GOAT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def reqAkharien(argsList):
	pUnit, pPlot	= argsList
	pPlayer=gc.getPlayer(pUnit.getOwner())
	if pPlayer.isHasFlag(gc.getInfoTypeForString("FLAG_AKHARIEN_LOST")):
		return False
	return True
def exploreLairAkharien(argsList):
	gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_AKHARIEN_LOST'),False)
						

def exploreLairDjinn2(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_DJINN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairBoar(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_BOAR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairWolf(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_WOLF'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairDomesticatedWarTortoise(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_WAR_TORTOISE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairKalshekk(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_LIZARD_PRIEST_OF_KALSHEKK'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_LIZARDMAN_MAZATL"),True)
	
def exploreLairOmorr(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_LIZARD_PRIEST_OF_OMORR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_LIZARDMAN_MAZATL"),True)
	
def exploreLairPirate(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_PIRATE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairRogueAdept(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_APPRENTICE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	listMana = [
				( gc.getInfoTypeForString('PROMOTION_AIR1'), gc.getInfoTypeForString('PROMOTION_AIR2'), gc.getInfoTypeForString('PROMOTION_AIR3')),
				( gc.getInfoTypeForString('PROMOTION_BODY1'), gc.getInfoTypeForString('PROMOTION_BODY2'), gc.getInfoTypeForString('PROMOTION_BODY3')),
				( gc.getInfoTypeForString('PROMOTION_CHAOS1'), gc.getInfoTypeForString('PROMOTION_CHAOS2'), gc.getInfoTypeForString('PROMOTION_CHAOS3')),
				( gc.getInfoTypeForString('PROMOTION_CREATION1'), gc.getInfoTypeForString('PROMOTION_CREATION2'), gc.getInfoTypeForString('PROMOTION_CREATION3')),
				( gc.getInfoTypeForString('PROMOTION_DEATH1'), gc.getInfoTypeForString('PROMOTION_DEATH2'), gc.getInfoTypeForString('PROMOTION_DEATH3')),
				( gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1'), gc.getInfoTypeForString('PROMOTION_DIMENSIONAL2'), gc.getInfoTypeForString('PROMOTION_DIMENSIONAL3')),
				( gc.getInfoTypeForString('PROMOTION_EARTH1'), gc.getInfoTypeForString('PROMOTION_EARTH2'), gc.getInfoTypeForString('PROMOTION_EARTH3')),
				( gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1'), gc.getInfoTypeForString('PROMOTION_ENCHANTMENT2'), gc.getInfoTypeForString('PROMOTION_ENCHANTMENT3')),
				( gc.getInfoTypeForString('PROMOTION_ENTROPY1'), gc.getInfoTypeForString('PROMOTION_ENTROPY2'), gc.getInfoTypeForString('PROMOTION_ENTROPY3')),
				( gc.getInfoTypeForString('PROMOTION_FIRE1'), gc.getInfoTypeForString('PROMOTION_FIRE2'), gc.getInfoTypeForString('PROMOTION_FIRE3')),
				( gc.getInfoTypeForString('PROMOTION_FORCE1'), gc.getInfoTypeForString('PROMOTION_FORCE2'), gc.getInfoTypeForString('PROMOTION_FORCE3')),
				( gc.getInfoTypeForString('PROMOTION_ICE1'), gc.getInfoTypeForString('PROMOTION_ICE2'), gc.getInfoTypeForString('PROMOTION_ICE3')),
				( gc.getInfoTypeForString('PROMOTION_LAW1'), gc.getInfoTypeForString('PROMOTION_LAW2'), gc.getInfoTypeForString('PROMOTION_LAW3')),
				( gc.getInfoTypeForString('PROMOTION_LIFE1'), gc.getInfoTypeForString('PROMOTION_LIFE2'), gc.getInfoTypeForString('PROMOTION_LIFE3')),
				( gc.getInfoTypeForString('PROMOTION_METAMAGIC1'), gc.getInfoTypeForString('PROMOTION_METAMAGIC2'), gc.getInfoTypeForString('PROMOTION_METAMAGIC3')),
				( gc.getInfoTypeForString('PROMOTION_MIND1'), gc.getInfoTypeForString('PROMOTION_MIND2'), gc.getInfoTypeForString('PROMOTION_MIND3')),
				( gc.getInfoTypeForString('PROMOTION_NATURE1'), gc.getInfoTypeForString('PROMOTION_NATURE2'), gc.getInfoTypeForString('PROMOTION_NATURE3')),
				( gc.getInfoTypeForString('PROMOTION_SHADOW1'), gc.getInfoTypeForString('PROMOTION_SHADOW2'), gc.getInfoTypeForString('PROMOTION_SHADOW3')),
				( gc.getInfoTypeForString('PROMOTION_SPIRIT1'), gc.getInfoTypeForString('PROMOTION_SPIRIT2'), gc.getInfoTypeForString('PROMOTION_SPIRIT3')),
				( gc.getInfoTypeForString('PROMOTION_SUN1'), gc.getInfoTypeForString('PROMOTION_SUN2'), gc.getInfoTypeForString('PROMOTION_SUN3')),
				( gc.getInfoTypeForString('PROMOTION_WATER1'), gc.getInfoTypeForString('PROMOTION_WATER2'), gc.getInfoTypeForString('PROMOTION_WATER3'))
	]
	for i in range(2):
		iSphere = listMana[CyGame().getSorenRandNum(len(listMana), "Mana choice")]
		newUnit.setHasPromotion(iSphere[0],True)
		
							
def exploreLairRogueMage(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_WIZARD'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	listMana = [
				 ( gc.getInfoTypeForString('PROMOTION_AIR1'), gc.getInfoTypeForString('PROMOTION_AIR2'), gc.getInfoTypeForString('PROMOTION_AIR3')),
				( gc.getInfoTypeForString('PROMOTION_BODY1'), gc.getInfoTypeForString('PROMOTION_BODY2'), gc.getInfoTypeForString('PROMOTION_BODY3')),
				( gc.getInfoTypeForString('PROMOTION_CHAOS1'), gc.getInfoTypeForString('PROMOTION_CHAOS2'), gc.getInfoTypeForString('PROMOTION_CHAOS3')),
				( gc.getInfoTypeForString('PROMOTION_CREATION1'), gc.getInfoTypeForString('PROMOTION_CREATION2'), gc.getInfoTypeForString('PROMOTION_CREATION3')),
				( gc.getInfoTypeForString('PROMOTION_DEATH1'), gc.getInfoTypeForString('PROMOTION_DEATH2'), gc.getInfoTypeForString('PROMOTION_DEATH3')),
				( gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1'), gc.getInfoTypeForString('PROMOTION_DIMENSIONAL2'), gc.getInfoTypeForString('PROMOTION_DIMENSIONAL3')),
				( gc.getInfoTypeForString('PROMOTION_EARTH1'), gc.getInfoTypeForString('PROMOTION_EARTH2'), gc.getInfoTypeForString('PROMOTION_EARTH3')),
				( gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1'), gc.getInfoTypeForString('PROMOTION_ENCHANTMENT2'), gc.getInfoTypeForString('PROMOTION_ENCHANTMENT3')),
				( gc.getInfoTypeForString('PROMOTION_ENTROPY1'), gc.getInfoTypeForString('PROMOTION_ENTROPY2'), gc.getInfoTypeForString('PROMOTION_ENTROPY3')),
				( gc.getInfoTypeForString('PROMOTION_FIRE1'), gc.getInfoTypeForString('PROMOTION_FIRE2'), gc.getInfoTypeForString('PROMOTION_FIRE3')),
				( gc.getInfoTypeForString('PROMOTION_FORCE1'), gc.getInfoTypeForString('PROMOTION_FORCE2'), gc.getInfoTypeForString('PROMOTION_FORCE3')),
				( gc.getInfoTypeForString('PROMOTION_ICE1'), gc.getInfoTypeForString('PROMOTION_ICE2'), gc.getInfoTypeForString('PROMOTION_ICE3')),
				( gc.getInfoTypeForString('PROMOTION_LAW1'), gc.getInfoTypeForString('PROMOTION_LAW2'), gc.getInfoTypeForString('PROMOTION_LAW3')),
				( gc.getInfoTypeForString('PROMOTION_LIFE1'), gc.getInfoTypeForString('PROMOTION_LIFE2'), gc.getInfoTypeForString('PROMOTION_LIFE3')),
				( gc.getInfoTypeForString('PROMOTION_METAMAGIC1'), gc.getInfoTypeForString('PROMOTION_METAMAGIC2'), gc.getInfoTypeForString('PROMOTION_METAMAGIC3')),
				( gc.getInfoTypeForString('PROMOTION_MIND1'), gc.getInfoTypeForString('PROMOTION_MIND2'), gc.getInfoTypeForString('PROMOTION_MIND3')),
				( gc.getInfoTypeForString('PROMOTION_NATURE1'), gc.getInfoTypeForString('PROMOTION_NATURE2'), gc.getInfoTypeForString('PROMOTION_NATURE3')),
				( gc.getInfoTypeForString('PROMOTION_SHADOW1'), gc.getInfoTypeForString('PROMOTION_SHADOW2'), gc.getInfoTypeForString('PROMOTION_SHADOW3')),
				( gc.getInfoTypeForString('PROMOTION_SPIRIT1'), gc.getInfoTypeForString('PROMOTION_SPIRIT2'), gc.getInfoTypeForString('PROMOTION_SPIRIT3')),
				( gc.getInfoTypeForString('PROMOTION_SUN1'), gc.getInfoTypeForString('PROMOTION_SUN2'), gc.getInfoTypeForString('PROMOTION_SUN3')),
				( gc.getInfoTypeForString('PROMOTION_WATER1'), gc.getInfoTypeForString('PROMOTION_WATER2'), gc.getInfoTypeForString('PROMOTION_WATER3'))
	]
	for i in range(3):
		iSphere = listMana[CyGame().getSorenRandNum(len(listMana), "Mana choice")]
		newUnit.setHasPromotion(iSphere[0],True)
		newUnit.setHasPromotion(iSphere[1],True)
	
def exploreLairRogueArchmage(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_BATTLEMAGE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	listMana = [
				( gc.getInfoTypeForString('PROMOTION_AIR1'), gc.getInfoTypeForString('PROMOTION_AIR2'), gc.getInfoTypeForString('PROMOTION_AIR3')),
				( gc.getInfoTypeForString('PROMOTION_BODY1'), gc.getInfoTypeForString('PROMOTION_BODY2'), gc.getInfoTypeForString('PROMOTION_BODY3')),
				( gc.getInfoTypeForString('PROMOTION_CHAOS1'), gc.getInfoTypeForString('PROMOTION_CHAOS2'), gc.getInfoTypeForString('PROMOTION_CHAOS3')),
				( gc.getInfoTypeForString('PROMOTION_CREATION1'), gc.getInfoTypeForString('PROMOTION_CREATION2'), gc.getInfoTypeForString('PROMOTION_CREATION3')),
				( gc.getInfoTypeForString('PROMOTION_DEATH1'), gc.getInfoTypeForString('PROMOTION_DEATH2'), gc.getInfoTypeForString('PROMOTION_DEATH3')),
				( gc.getInfoTypeForString('PROMOTION_DIMENSIONAL1'), gc.getInfoTypeForString('PROMOTION_DIMENSIONAL2'), gc.getInfoTypeForString('PROMOTION_DIMENSIONAL3')),
				( gc.getInfoTypeForString('PROMOTION_EARTH1'), gc.getInfoTypeForString('PROMOTION_EARTH2'), gc.getInfoTypeForString('PROMOTION_EARTH3')),
				( gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1'), gc.getInfoTypeForString('PROMOTION_ENCHANTMENT2'), gc.getInfoTypeForString('PROMOTION_ENCHANTMENT3')),
				( gc.getInfoTypeForString('PROMOTION_ENTROPY1'), gc.getInfoTypeForString('PROMOTION_ENTROPY2'), gc.getInfoTypeForString('PROMOTION_ENTROPY3')),
				( gc.getInfoTypeForString('PROMOTION_FIRE1'), gc.getInfoTypeForString('PROMOTION_FIRE2'), gc.getInfoTypeForString('PROMOTION_FIRE3')),
				( gc.getInfoTypeForString('PROMOTION_FORCE1'), gc.getInfoTypeForString('PROMOTION_FORCE2'), gc.getInfoTypeForString('PROMOTION_FORCE3')),
				( gc.getInfoTypeForString('PROMOTION_ICE1'), gc.getInfoTypeForString('PROMOTION_ICE2'), gc.getInfoTypeForString('PROMOTION_ICE3')),
				( gc.getInfoTypeForString('PROMOTION_LAW1'), gc.getInfoTypeForString('PROMOTION_LAW2'), gc.getInfoTypeForString('PROMOTION_LAW3')),
				( gc.getInfoTypeForString('PROMOTION_LIFE1'), gc.getInfoTypeForString('PROMOTION_LIFE2'), gc.getInfoTypeForString('PROMOTION_LIFE3')),
				( gc.getInfoTypeForString('PROMOTION_METAMAGIC1'), gc.getInfoTypeForString('PROMOTION_METAMAGIC2'), gc.getInfoTypeForString('PROMOTION_METAMAGIC3')),
				( gc.getInfoTypeForString('PROMOTION_MIND1'), gc.getInfoTypeForString('PROMOTION_MIND2'), gc.getInfoTypeForString('PROMOTION_MIND3')),
				( gc.getInfoTypeForString('PROMOTION_NATURE1'), gc.getInfoTypeForString('PROMOTION_NATURE2'), gc.getInfoTypeForString('PROMOTION_NATURE3')),
				( gc.getInfoTypeForString('PROMOTION_SHADOW1'), gc.getInfoTypeForString('PROMOTION_SHADOW2'), gc.getInfoTypeForString('PROMOTION_SHADOW3')),
				( gc.getInfoTypeForString('PROMOTION_SPIRIT1'), gc.getInfoTypeForString('PROMOTION_SPIRIT2'), gc.getInfoTypeForString('PROMOTION_SPIRIT3')),
				( gc.getInfoTypeForString('PROMOTION_SUN1'), gc.getInfoTypeForString('PROMOTION_SUN2'), gc.getInfoTypeForString('PROMOTION_SUN3')),
				( gc.getInfoTypeForString('PROMOTION_WATER1'), gc.getInfoTypeForString('PROMOTION_WATER2'), gc.getInfoTypeForString('PROMOTION_WATER3'))
	]
	for i in range(4):
		iSphere = listMana[CyGame().getSorenRandNum(len(listMana), "Mana choice")]
		newUnit.setHasPromotion(iSphere[0],True)
		newUnit.setHasPromotion(iSphere[1],True)
		newUnit.setHasPromotion(iSphere[2],True)
	
def exploreLairAngryGoblinEasy(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairRedcaps(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_REDCAP'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_REDCAP'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairElvenAeron(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_ELVEN_AERON_WORSHIPPER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


def exploreLairCentaurAmbushEasy(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_CENTAUR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairMyconid(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MYCONID'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairBoneGolem(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_BONE_GOLEM'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairAbomination(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_ABOMINATION'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_DEMON_LAIR"),True)
	
def exploreLairHellhounds(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_HELLHOUND'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_HELLHOUND'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_HELLHOUND'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairBlowpipe(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairAgruonnRitual(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SHADOW_PRIEST_OF_AGRUONN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_LIZARD_PRIEST_OF_AGRUONN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_LIZARD_PRIEST_OF_AGRUONN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
	
def exploreLairGraveleech(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_VAMPIRE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UNDEAD'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_GRAVELEECH'),True)
	
def exploreLairAngryGoblinMedium(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_ARCHER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit4 = bPlayer.initUnit(getInfoType('UNIT_ARCHER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairWolfRiderAmbush(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_WOLF_RIDER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_WOLF_RIDER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_WOLF_RIDER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_WOLF_RIDER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairCentaurAmbushMedium(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_CENTAUR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit4 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairAngryGoblinHard(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit5 = bPlayer.initUnit(getInfoType('UNIT_GOBLIN_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_ARCHER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit4 = bPlayer.initUnit(getInfoType('UNIT_ARCHER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit6 = bPlayer.initUnit(getInfoType('UNIT_ARCHER_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit7 = bPlayer.initUnit(getInfoType('UNIT_CHARIOT_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit8 = bPlayer.initUnit(getInfoType('UNIT_CHARIOT_SCORPION_CLAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairFrostlingAmbushHard(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit5 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit4 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit6 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit7 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_WOLF_RIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit8 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_WOLF_RIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	
def exploreLairCentaurAmbushHard(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_CENTAUR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit5 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit4 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit6 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit7 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR_LANCER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit8 = bPlayer.initUnit(getInfoType('UNIT_CENTAUR_CLANCHIEF'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairOrcishBullies(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_WAR_BOSS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairPitBeast(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_PIT_BEAST'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairBeastOfAgares(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_BEAST_OF_AGARES'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_DEMON_LAIR"),True)

def exploreLairCurseThirstSavant(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_DISCIPLE_THE_ASHEN_VEIL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_RAGESWORD"),True)

def exploreLairSuccubusAngel(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_BANESWORD_ANGEL"),True)

def exploreLairSkeletonPatrian(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SKELETON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_CUIRASS_DRAGON"),True)

def exploreLairNinjaFawn(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_FAWN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_TRICKY_DAGGER"),True)

def exploreLairSluaghLord(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SLUAGH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_ICXTH"),True)

def exploreLairScreamingPuppet(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_DEVOUT'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_SPIRIT_SEVER"),True)
	newUnit.setHasPromotion(getInfoType("PROMOTION_PUPPET"),True)

def exploreLairRighteousNobhead(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_DISCIPLE_THE_ORDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_BANESWORD_DEMON"),True)
	
def exploreLairWarrior(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_WARRIOR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairAxemen(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairOgre(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_OGRE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairOgreChief(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_OGRE_WARCHIEF'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairBasilisk(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_BASILISK'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairNightWatch(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_NIGHTWATCH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairShadow(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SHADOW'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairShadowRider(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SHADOWRIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairCyklop(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_CYKLOP'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairHillGiant(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_HILL_GIANT'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairFawn(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_FAWN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairPriestAgruonn(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_LIZARD_PRIEST_OF_AGRUONN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairWraith(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_WRAITH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DEATH1'),True)

def exploreLairAirElemental(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_AIR_ELEMENTAL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairMobiusWitch(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MOBIUS_WITCH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairEarthElemental(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_EARTH_ELEMENTAL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairFireElemental(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_FIRE_ELEMENTAL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairMistform(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MISTFORM'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairWaterElemental(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_WATER_ELEMENTAL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairTheHive(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_THE_HIVE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairDjinn(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_DJINN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairBear(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_BEAR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairGiantSpider(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_GIANT_SPIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairTreant(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_TREANT'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairShadowTreant(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SHADOW_TREANT'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairSkeleton(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SKELETON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairSkeletons(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SKELETON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_SKELETON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_SKELETON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairEinherjar(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_EINHERJAR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairDiseasedCorpse(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_DISEASED_CORPSE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairSpectre(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SPECTRE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairTombWarden(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_TOMB_WARDEN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairLich(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_LICH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DEATH2'),True)

def exploreLairDrown(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_DROWN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairSeaSerpent(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SEA_SERPENT'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairVampireKraken(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_KRAKEN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_VAMPIRE"),True)
	newUnit.setHasPromotion(getInfoType("PROMOTION_DEMON"),True)

def exploreLairOtoloch2(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_OTOLOCH_2'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setName("Kumitara, the Otoloch Whisperer")

def exploreLairCondatis(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_CONDATIS'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairTsunami(argsList):
	pUnit, pPlot = argsList
	pUnit.cast(getInfoType("SPELL_TSUNAMI"))

def exploreLairTortoise(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_GIANT_TORTOISE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairKraken(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_KRAKEN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairStygianGuard(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_STYGIAN_GUARD'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairChaosMarauder(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_CHAOS_MARAUDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairManticore(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MANTICORE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairMinotaur(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MINOTAUR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairTarDemon(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_TAR_DEMON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairSuccubusOrgy(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit4 = bPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairBarbatos(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_BARBATOS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairRottenEarthElem(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_EARTH_ELEMENTAL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_ROTTEN"),True)

def exploreLairDeathKnight(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_DEATH_KNIGHT'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairUndeadDrake(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_UNDEAD_DRAKE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairFrostGiant(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_FROST_GIANT'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairPlaguedRats(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_PLAGUED_RAT_PACK'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairIceElemental(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_ICE_ELEMENTAL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairSeraph(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_SERAPH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreLairMechDragon(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MECH_DRAGON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_LEASH_0'),True)

def exploreLairVelgyrGolem(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_VELGYR_GOLEM'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		
def exploreLairNoSheaimPrereq(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	if pPlayer.getCivilizationType() == Civ["Sheaim"]:
		return False
	return True

def exploreLairNoGoodUnitPrereq(argsList):
	pUnit, pPlot = argsList
	if (pUnit.getLevel()>9 or pUnit.isHasPromotion(getInfoType("PROMOTION_HERO")) or pUnit.isHasPromotion(getInfoType("PROMOTION_HEROIC")) or pUnit.isHasPromotion(getInfoType("PROMOTION_ADVENTURER"))):
		return False
	return True
	
def exploreLairUrorBand(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('EQUIPMENT_CONTAINER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UROR_BAND'),True)

def exploreLairSkullAsmoday(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('EQUIPMENT_CONTAINER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_SKULL_OF_ASMODAY'),True)
	
def exploreLairBreakBair(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_CONTROLED_LACUNA'),True)
	
def exploreLairBairMobiusWitches(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_MOBIUS_WITCH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_MOBIUS_WITCH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_MOBIUS_WITCH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_FIRE1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_FIRE2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ENTROPY1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ENTROPY2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_CHAOS1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_CHAOS2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DIMENSIONAL1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DIMENSIONAL2'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_FIRE1'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_FIRE2'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_ENTROPY1'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_ENTROPY2'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_CHAOS1'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_CHAOS2'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_DIMENSIONAL1'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_DIMENSIONAL2'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_FIRE1'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_FIRE2'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_ENTROPY1'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_ENTROPY2'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_CHAOS1'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_CHAOS2'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_DIMENSIONAL1'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_DIMENSIONAL2'),True)

def exploreLairBairEmrys(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_EATER_OF_DREAMS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DEATH1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DEATH2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DEATH3'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_FIRE1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_FIRE2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_FIRE3'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ENTROPY1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ENTROPY2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ENTROPY3'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_CHAOS1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_CHAOS2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_CHAOS3'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DIMENSIONAL1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DIMENSIONAL2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_DIMENSIONAL3'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_MIND1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_MIND2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_MIND3'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_SHADOW1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_SHADOW2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_SHADOW3'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_EMRYS'),True)
	
def exploreLairSecondaryCommander(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	pUnit.setHasPromotion(getInfoType('PROMOTION_SECONDARY_COMMANDER'),True)

def exploreLairFriendlyFrostling(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)	
	newUnit.setHasPromotion(getInfoType('PROMOTION_AMBUSH1'),True)

def exploreLairSnow(argsList):
	pUnit, pPlot = argsList
	pPlot.setTerrainType(Terrain["Tundra"], True, True)

def exploreLairWintered(argsList):
	pUnit, pPlot = argsList
	pUnit.setHasPromotion(getInfoType('PROMOTION_WINTERED'),True)

def exploreLairColdStrength(argsList):
	pUnit, pPlot = argsList
	pUnit.setHasPromotion(getInfoType('PROMOTION_COLD_STRENGTH'),True)

def exploreLairBlizzard(argsList):
	pUnit, pPlot = argsList
	pPlot.setFeatureType(getInfoType("FEATURE_BLIZZARD"), -1)
	
def exploreLairFrostlingAdept(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_FROSTLING_SHAMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ICE1'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_LAW1'),True)

def exploreLairGoblinCommander(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_MURIS_CLAN_LORD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setExperienceTimes100(1000,-1)	
	
def exploreLairAngryFrostlingEasy(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairAngryFrostlingMedium(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit4 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def exploreLairAngryFrostlingHard(argsList):
	pUnit, pPlot = argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit5 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit4 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit6 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_ARCHER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit7 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_WOLF_RIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit8 = bPlayer.initUnit(getInfoType('UNIT_FROSTLING_WOLF_RIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def perTurnArmaWeapon(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if (pPlayer.getAlignment()==getInfoType("ALIGNMENT_GOOD") and not pCaster.isHasPromotion(getInfoType("PROMOTION_ARMA_GOOD_WEAPON"))):
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_GOOD_WEAPON"),True)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_NEUTRAL_WEAPON"),False)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_EVIL_WEAPON"),False)
	
	if (pPlayer.getAlignment()==getInfoType("ALIGNMENT_NEUTRAL") and not pCaster.isHasPromotion(getInfoType("PROMOTION_ARMA_NEUTRAL_WEAPON"))):
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_GOOD_WEAPON"),False)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_NEUTRAL_WEAPON"),True)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_EVIL_WEAPON"),False)
	
	if (pPlayer.getAlignment()==getInfoType("ALIGNMENT_EVIL") and not pCaster.isHasPromotion(getInfoType("PROMOTION_ARMA_EVIL_WEAPON"))):
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_GOOD_WEAPON"),False)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_NEUTRAL_WEAPON"),False)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_EVIL_WEAPON"),True)

def perTurnArmaArmor(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if (pPlayer.getAlignment()==getInfoType("ALIGNMENT_GOOD") and not pCaster.isHasPromotion(getInfoType("PROMOTION_ARMA_GOOD_ARMOR"))):
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_GOOD_ARMOR"),True)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_NEUTRAL_ARMOR"),False)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_EVIL_ARMOR"),False)
	
	if (pPlayer.getAlignment()==getInfoType("ALIGNMENT_NEUTRAL") and not pCaster.isHasPromotion(getInfoType("PROMOTION_ARMA_NEUTRAL_ARMOR"))):
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_GOOD_ARMOR"),False)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_NEUTRAL_ARMOR"),True)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_EVIL_ARMOR"),False)
	
	if (pPlayer.getAlignment()==getInfoType("ALIGNMENT_EVIL") and not pCaster.isHasPromotion(getInfoType("PROMOTION_ARMA_EVIL_ARMOR"))):
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_GOOD_ARMOR"),False)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_NEUTRAL_ARMOR"),False)
		pCaster.setHasPromotion(getInfoType("PROMOTION_ARMA_EVIL_ARMOR"),True)
		
def perTurnUrorBand(pCaster):
	if pCaster.isAlive() and not pCaster.isImmortal():
		pCaster.kill(True,0)

def perTurnApophis(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	for id in range(gc.getNumPromotionInfos()):
		if pCaster.isHasPromotion(id) and gc.getPromotionInfo(id).isEquipment():
			pCaster.setHasPromotion(id,False)
			if pCaster.getStrBoost()<15:
				pCaster.changeStrBoost(1)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_GOAT_CONSUME_EQUIPMENT", ()),'',1,'Art/Interface/Buttons/Units/Goat.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
			if not pPlayer.isHasFlag(getInfoType("FLAG_APOPHIS_REVEALED")):
				pPlayer.setHasFlag(getInfoType("FLAG_APOPHIS_REVEALED"),True)
				pCaster.setName(CyTranslator().getText("TXT_KEY_UNIT_GOAT_2", ()))
				CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_APOPHIS_REVEALED", ()),'',1,'Art/Interface/Buttons/Units/Goat.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
				pCaster.setHasPromotion(getInfoType('PROMOTION_APOPHIS'),True)

					
def spellHauntedBreath(pCaster):
	getPlot		= CyMap().plot
	pCaster.changeStrBoost(1)
	
	for x, y in plotsInRange( pCaster.getX(), pCaster.getY(), 1 ):
		pPlot = getPlot(x, y)
		iFeature = pPlot.getPlotEffectType()
		if iFeature==getInfoType("PLOT_EFFECT_HAUNTED_LANDS"):
			pPlot.setPlotEffectType(-1)
				
def spellGustOfWind(pCaster):
	gc 			= CyGlobalContext()
	iRange		= 1 + pCaster.getSpellExtraRange()
	getPlot		= CyMap().plot
	for x, y in plotsInRange( pCaster.getX(), pCaster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if pPlot.isPeak(): continue
		#iPerceptionCost = pPlot.getPerceptionCost()
		#if iPerceptionCost > 0:
		#	pPlot.setMistChangeTemp(iPerceptionCost)
		#	pPlot.setMistChangeTimer(scale(3))
		#	pPlot.setPerceptionCost(0)

def reqGustOfWind(pCaster):
	gc 			= CyGlobalContext()
	pPlayer		= gc.getPlayer(pCaster.getOwner())
	iRange		= 1 + pCaster.getSpellExtraRange()
	getPlot		= CyMap().plot

	if not pPlayer.isHuman():
		if pPlayer.getCivilizationType() == Civ["Sidar"]: return False

	for x, y in plotsInRange( pCaster.getX(), pCaster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if pPlot==-1 : continue
		if pPlot.isPeak(): continue
		if pPlot.getPerceptionCost() > 0: return True
	return False

# Hydromancer leader - City spell - Defensive wave
def spellDefensiveWave(pCity):
	pPlayer     = gc.getPlayer(pCity.getOwner())
	pTeam       = gc.getTeam(pPlayer.getTeam())
	iRange		= pCity.getPlotRadius() + pCity.getSpellExtraRange() 

	iNumWater   = pPlayer.getNumAvailableBonuses(Mana["Water"]) # - count water mana
	bHydro2     = pPlayer.hasTrait(Trait["Hydromancer 2"]) # hydromancer level
	bHydro3     = pPlayer.hasTrait(Trait["Hydromancer 3"])
	# Damage inflicted by the spell. Scales with Hydromancer level and water mana nodes.
	iDmg        = 5*(2+bHydro2+bHydro3 + iNumWater) # At least 15%
	# Max damage inflicted by the spell. Scales with Hydromancer level and water mana nodes.
	iDmgMax     = 2 * iDmg # At least 30%
	iDmgCold    = getInfoType('DAMAGE_COLD')
	getPlot 	= CyMap().plot
	
	for x, y in plotsInCircularRange( pCity.getX(), pCity.getY(), iRange ):
		pPlot = getPlot(x, y)
		if pPlot.isWater() or pPlot.isAdjacentToWater() or (pPlot.isRiver() and (pPlot.isFlatlands() or (pPlot.isHills() and bHydro2) or (pPlot.isPeak() and bHydro3))):
			for iLoopUnit in range(pPlot.getNumUnits()):
				pLoopUnit = pPlot.getUnit(iLoopUnit)
				pLoopPlayer = gc.getPlayer(pLoopUnit.getOwner())
				iLoopTeam = pLoopPlayer.getTeam()
				if pTeam.isAtWar(iLoopTeam): # The water hurts only enemy units
					pLoopUnit.doDamageNoCaster(iDmg, iDmgMax, iDmgCold, False)
					CyEngine().triggerEffect(getInfoType('EFFECT_SPRING'), pPlot.getPoint())

def reqDefensiveWave(pCity):
	pPlayer     = gc.getPlayer(pCity.getOwner())
	pTeam       = gc.getTeam(pPlayer.getTeam())
	iNumWater   = pPlayer.getNumAvailableBonuses(Mana["Water"])
	bHydro2     = pPlayer.hasTrait(Trait["Hydromancer 2"])
	bHydro3     = pPlayer.hasTrait(Trait["Hydromancer 3"])
	iRange		= pCity.getPlotRadius() + pCity.getSpellExtraRange() 
	getPlot		= CyMap().plot
	if (iNumWater != 0):
		for x, y in plotsInCircularRange( pCity.getX(), pCity.getY(), iRange ):
			pPlot = getPlot(x, y)
			if pPlot.isWater() or pPlot.isAdjacentToWater() or (pPlot.isRiver() and (pPlot.isFlatlands() or (pPlot.isHills() and bHydro2) or (pPlot.isPeak() and bHydro3))):
				for iLoopUnit in range(pPlot.getNumUnits()):
					pLoopUnit = pPlot.getUnit(iLoopUnit)
					pLoopPlayer = gc.getPlayer(pLoopUnit.getOwner())
					iLoopTeam = pLoopPlayer.getTeam()
					if pTeam.isAtWar(iLoopTeam): # The water hurts only enemy units
						return True
	return False


	return True
# Hydromancer leader - City spell - Defensive wave END
# Scorched Earth leader - City spell - Circle of Flames
def spellCircleOfFlames(pCity):
	getPlot     = CyMap().plot
	pPlayer     = gc.getPlayer(pCity.getOwner())
	pTeam       = gc.getTeam(pPlayer.getTeam())
	iRange		= 1 + pCity.getSpellExtraRange()
	for x, y in plotsInCircularRange( pCity.getX(), pCity.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isWater():
			pPlot.setFeatureType(getInfoType('FEATURE_FLAMES'), -1)	

def spellCreateMist(pCity):
	getPlot		= CyMap().plot
	iX 			= pCity.getX()
	iY 			= pCity.getY()

	#pCity.plot().setMistChangeTemp(5)
	#pCity.plot().setMistChangeTimer(0)
	pCity.setNumRealBuilding(getInfoType('BUILDING_HIDDEN_CITY'), 1)

	blocked = (getInfoType('FEATURE_VOLCANO'), getInfoType('FEATURE_VOLCANO'))

	#for x, y in plotsInCircularRange( iX, iY, 1, 1 ):
	#	pPlot = getPlot(x, y)
	#	if pPlot.isCity(): continue
	#	if pPlot.isPeak(): continue
	#	if pPlot.getFeatureType() in blocked: continue
	#	if pPlot.getOwner() != -1:
	#		if gc.getPlayer(pPlot.getOwner()).getCivilizationType() != Civ["Sidar"]: continue
	#	pPlot.setMistChangeTemp(4)
	#	pPlot.setMistChangeTimer(scale(3))
#
#	for x, y in plotsInCircularRange( iX, iY, 2, 2 ):
#		pPlot = getPlot(x, y)
#		if pPlot.isCity(): continue
#		if pPlot.isPeak(): continue
#		if pPlot.getFeatureType() in blocked: continue
#		if pPlot.getOwner() != -1:
#			if gc.getPlayer(pPlot.getOwner()).getCivilizationType() != Civ["Sidar"]: continue
#		pPlot.setMistChangeTemp(3)
#		pPlot.setMistChangeTimer(scale(6))

def reqWane(caster):
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'):
		return False
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BEAST'):
		return False
	if caster.isImmortal():
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_SHADE')) >= 4:
		return False
	return True


def reqCreateMist(pCity):
	pPlayer = gc.getPlayer(pCity.getOwner())

	if not pPlayer.isHuman():
		if pCity.isCapital(): return False

	if pCity.getNumRealBuilding(getInfoType('BUILDING_HIDDEN_CITY')) > 0:
		return False

	return True

def spellRemoveMist(pCity):
	gc 		= CyGlobalContext()
	getPlot	= CyMap().plot
	iX 			= pCity.getX()
	iY 			= pCity.getY()
	blocked = (getInfoType('FEATURE_VOLCANO'), getInfoType('FEATURE_VOLCANO'))

#	pCity.plot().setMistChangeTimer(scale(6))
#	pCity.plot().setMistChangeTemp(0)
#	pCity.setNumRealBuilding(getInfoType('BUILDING_HIDDEN_CITY'), 0)
#
#	for x, y in plotsInCircularRange( iX, iY, 1, 1 ):
#		pPlot = getPlot(x, y)
#		if pPlot.isCity(): continue
#		if pPlot.isPeak(): continue
#		if pPlot.getFeatureType() in blocked: continue
#		if pPlot.getOwner() != -1:
#			if gc.getPlayer(pPlot.getOwner()).getCivilizationType() != Civ["Sidar"]: continue
#		pPlot.setMistChangeTemp(0)
#		pPlot.setMistChangeTimer(scale(6))
#
#	for x, y in plotsInCircularRange( iX, iY, 2, 2 ):
#		pPlot = getPlot(x, y)
#		if pPlot.isCity(): continue
#		if pPlot.isPeak(): continue
#		if pPlot.getFeatureType() in blocked: continue
#		if pPlot.getOwner() != -1:
#			if gc.getPlayer(pPlot.getOwner()).getCivilizationType() != Civ["Sidar"]: continue
#		pPlot.setMistChangeTemp(0)
#		pPlot.setMistChangeTimer(scale(3))

def reqRemoveMist(pCity):
	pPlayer = gc.getPlayer(pCity.getOwner())

	if not pPlayer.isHuman():
		if pCity.isCapital():
			return False

	if pCity.getNumRealBuilding(getInfoType('BUILDING_HIDDEN_CITY')) > 0:
		return True

def reqSteamworks(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if (pPlayer.getCurrentResearch()==-1):
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_WORKSHOP')) < 5:
			return False
	return True

def spellSteamworks(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pTeam = gc.getTeam(pPlayer.getTeam())
	iTech = pPlayer.getCurrentResearch()
	iNum = 20 + (pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_WORKSHOP')) * 60) + (pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_WATERMILL')) * 50) + (pPlayer.getImprovementCount(getInfoType('IMPROVEMENT_WINDMILL')) * 50)
	pTeam.changeResearchProgress(iTech, iNum, caster.getOwner())

def getHelpMutation(argsList):
	ePromotion, pCaster = argsList
	bFirst = True

	## Good Promos
	iStrengthPer = getInfoType('PROMOTION_MUTATION_STRENGTH_PERCENT')
	iAttackPer = getInfoType('PROMOTION_MUTATION_STRENGTH_PERCENT_ATTACK')
	iDefensePer = getInfoType('PROMOTION_MUTATION_STRENGTH_PERCENT_DEFENSE')
	iMovement = getInfoType('PROMOTION_MUTATION_MOVEMENT')
	iFSChance = getInfoType('PROMOTION_MUTATION_FIRST_STRIKE_CHANCE')
	iFS = getInfoType('PROMOTION_MUTATION_FIRST_STRIKE')
	iDS = getInfoType('PROMOTION_MUTATION_DEFENSIVE_STRIKE')
	iStrength = getInfoType('PROMOTION_MUTATION_STRENGTH')
	iAttackStr = getInfoType('PROMOTION_MUTATION_STRENGTH_ATTACK')
	iDefenseStr = getInfoType('PROMOTION_MUTATION_STRENGTH_DEFENSE')
	iHealing = getInfoType('PROMOTION_MUTATION_HEALING')
	iHealingCombat = getInfoType('PROMOTION_MUTATION_HEALING_COMBAT')
	iFly = getInfoType("PROMOTION_MUTATION_FLYING")

	## Bad Promos
	iStrengthPerBad = getInfoType('PROMOTION_MUTATION_STRENGTH_PERCENT_BAD')
	iAttackPerBad = getInfoType('PROMOTION_MUTATION_STRENGTH_PERCENT_ATTACK_BAD')
	iDefensePerBad = getInfoType('PROMOTION_MUTATION_STRENGTH_PERCENT_DEFENSE_BAD')
	iMovementBad = getInfoType('PROMOTION_MUTATION_MOVEMENT_BAD')
	iFSChanceBad = getInfoType('PROMOTION_MUTATION_FIRST_STRIKE_CHANCE_BAD')
	iFSBad = getInfoType('PROMOTION_MUTATION_FIRST_STRIKE_BAD')
	iDSBad = getInfoType('PROMOTION_MUTATION_DEFENSIVE_STRIKE_BAD')
	iStrengthBad = getInfoType('PROMOTION_MUTATION_STRENGTH_BAD')
	iAttackStrBad = getInfoType('PROMOTION_MUTATION_STRENGTH_ATTACK_BAD')
	iDefenseStrBad = getInfoType('PROMOTION_MUTATION_STRENGTH_DEFENSE_BAD')
	iHealingBad = getInfoType('PROMOTION_MUTATION_HEALING_BAD')
	iCrazed = getInfoType('PROMOTION_MUTATION_CRAZED')

	if pCaster == -1 or pCaster.isNone():
		szHelp = ""
	else:
		szHelp = ""
		iNumStrengthPer = pCaster.countHasPromotion(iStrengthPer) - pCaster.countHasPromotion(iStrengthPerBad)
		iNumAttackPer = pCaster.countHasPromotion(iAttackPer) - pCaster.countHasPromotion(iAttackPerBad)
		iNumDefensePer = pCaster.countHasPromotion(iDefensePer) - pCaster.countHasPromotion(iDefensePerBad)
		iNumMovement = pCaster.countHasPromotion(iMovement)
		iNumFSChance = pCaster.countHasPromotion(iFSChance) - pCaster.countHasPromotion(iFSChanceBad)
		iNumFS = pCaster.countHasPromotion(iFS) - pCaster.countHasPromotion(iFSBad)
		iNumDS = pCaster.countHasPromotion(iDS) - pCaster.countHasPromotion(iDSBad)
		iNumStrength = pCaster.countHasPromotion(iStrength) - pCaster.countHasPromotion(iStrengthBad)
		iNumAttackStr = pCaster.countHasPromotion(iAttackStr) - pCaster.countHasPromotion(iAttackStrBad)
		iNumDefenseStr = pCaster.countHasPromotion(iDefenseStr) - pCaster.countHasPromotion(iDefenseStrBad)
		iNumHealing = pCaster.countHasPromotion(iHealing) - pCaster.countHasPromotion(iHealingBad)
		iNumHealingCombat = pCaster.countHasPromotion(iHealingCombat)
		iNumFlying = pCaster.countHasPromotion(iFly)
		
		iNumMovementBad = pCaster.countHasPromotion(iMovementBad)
		iNumCrazed = pCaster.countHasPromotion(iCrazed)

		##Good
		if not (iNumStrengthPer == 0):
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_STRENGTHPER", (iNumStrengthPer * 5,))
			bFirst = False
		if not (iNumAttackPer == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_ATTACKPER", (iNumAttackPer * 5,))
			bFirst = False
		if not (iNumDefensePer == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_DEFENSEPER", (iNumDefensePer * 5,))
			bFirst = False
		if not (iNumMovement == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_MOVEMENT", (iNumMovement,))
			bFirst = False
		if not (iNumFSChance == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_FSCHANCE", (iNumFSChance,))
			bFirst = False
		if not (iNumFS == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_FS", (iNumFS,))
			bFirst = False
		if not (iNumDS == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_DS", (iNumDS * 5,))
			bFirst = False
		if not (iNumStrength == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_STRENGTH", (iNumStrength,))
			bFirst = False
		if not (iNumAttackStr == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_ATTACKSTR", (iNumAttackStr,))
			bFirst = False
		if not (iNumDefenseStr == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_DEFENSESTR", (iNumDefenseStr,))
			bFirst = False
		if not (iNumHealing == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_HEALING", (iNumHealing * 5,))
			bFirst = False
		if not (iNumHealingCombat == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_HEALINGCOMBAT", (iNumHealingCombat * 5,))
			bFirst = False
			
		if not (iNumFlying == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_FLYING", ())
			bFirst = False

		##Bad
		if not (iNumMovementBad == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_MOVEMENT_BAD", (iNumMovementBad,))
			bFirst = False
		if not (iNumCrazed == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MUTATION_CRAZED", ())
			bFirst = False

	return szHelp

#SpawnGroup Spells Start
def reqOrthusSpawn(argsList):
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ORTHUS):
		return False
	else:
		return True

def reqRepairGolem(caster):
	pPlot = caster.plot()
	iGolem = getInfoType('PROMOTION_GOLEM')
	iHiddenNationality = getInfoType('PROMOTION_HIDDEN_NATIONALITY')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.isHasPromotion(iGolem):
			if pUnit.isHurt() and not pUnit.isHasPromotion(iHiddenNationality) :
				return True
	return False

def spellRepairGolem(caster,amount):
	pPlot = caster.plot()
	iGolem = getInfoType('PROMOTION_GOLEM')
	iHiddenNationality = getInfoType('PROMOTION_HIDDEN_NATIONALITY')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.isHasPromotion(iGolem):
			if not pUnit.isHasPromotion(iHiddenNationality):
				pUnit.changeDamage(-amount,0)

def spellIlusionRandom(argsList):
	pPlot = argsList[0]
	iIllusion = getInfoType('PROMOTION_ILLUSION')
	iIlluRand = CyGame().getSorenRandNum(100, "Illusion Chance")
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if iIlluRand > 50:
			if pUnit.isHasPromotion(Race["Demon"]):
				pUnit.setHasPromotion(Race["Demon"], False)
				pUnit.setHasPromotion(iIllusion, True)
			else:
				pUnit.setHasPromotion(iIllusion, True)

def spellRandomSong(argsList):
	pPlot = argsList[0]
	iFiery = getInfoType('PROMOTION_FIERY_WANGOLE')
	iWhispers = getInfoType('PROMOTION_THE_WHISPERS')
	iSongRand = CyGame().getSorenRandNum(100, "Song Chance")
	iWildKha = getInfoType('UNIT_WILD_KHA')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == iWildKha:
			if iSongRand > 50:
				pUnit.setHasPromotion(iFiery, True)
			else:
				pUnit.setHasPromotion(iWhispers, True)

def spellFellowshipRacial(argsList):
	pPlot = argsList[0]
	iElven = getInfoType('PROMOTION_ELF')
	iDwarf= getInfoType('PROMOTION_DWARF')
	iArcher = getInfoType('UNIT_ARCHER')
	iAxeman = getInfoType('UNIT_AXEMAN')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == iArcher:
					pUnit.setHasPromotion(iElven, True)
		if pUnit.getUnitType() == iAxeman:
					pUnit.setHasPromotion(iDwarf, True)

def spellRandomRacial(argsList):
	pPlot = argsList[0]
	iRaceNumber = CyGame().getSorenRandNum(len(IRacial), "Race Number")
	iRace = IRacial[iRaceNumber]
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		pUnit.setHasPromotion(iRace, True)

def spellFremen(argsList):
	pPlot = argsList[0]
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == getInfoType('UNIT_CHAMPION'):
			pUnit.setName("Fremen")

def postCombatStolenCattle(caster, opponent):
	iCattle = getInfoType('PROMOTION_STOLEN_CATTLE')
	opponent.setHasPromotion(iCattle, True)

def reqStealCattle(pCaster):
	pPlot = pCaster.plot()
	if pPlot.getBonusType(-1) == Bonus["Cow"]:
		return True

def spellStealCattle(pCaster):
	pPlot = pCaster.plot()
	iCattle = getInfoType('PROMOTION_STOLEN_CATTLE')
	if pPlot.getBonusType(-1) == Bonus["Cow"]:
		pPlot.setBonusType(-1)
		pCaster.setHasPromotion(iCattle, True)

def spellReturnCattle(pCaster):
	pPlot = pCaster.plot()
	iCattle = getInfoType('PROMOTION_STOLEN_CATTLE')
	pPlot.setBonusType(Bonus["Cow"])
	pCaster.setHasPromotion(iCattle, False)
	
def reqDriveCattle(pCaster):
	pPlot = pCaster.plot()
	pOwner=gc.getPlayer(pCaster.getOwner())
	if(pPlot.isOwned() and not pPlot.getOwner()==pCaster.getOwner()):
		return False
	if pCaster.isHasPromotion(getInfoType('PROMOTION_LEADING_CATTLE')):
		return False
	if pPlot.getBonusType(pOwner.getTeam()) == Bonus["Cow"] or pPlot.getBonusType(pOwner.getTeam())==getInfoType("BONUS_SHEEP")or pPlot.getBonusType(pOwner.getTeam())==getInfoType("BONUS_PIG")or pPlot.getBonusType(pOwner.getTeam())==getInfoType("BONUS_HORSE")or pPlot.getBonusType(pOwner.getTeam())==getInfoType("BONUS_HYAPON")or pPlot.getBonusType(pOwner.getTeam())==getInfoType("BONUS_NIGHTMARE")or pPlot.getBonusType(pOwner.getTeam())==getInfoType("BONUS_CAMEL"):
		return True

def spellDriveCattle(pCaster):
	pPlot = pCaster.plot()
	pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_CATTLE'), True)
	if pPlot.getBonusType(-1) == getInfoType("BONUS_COW"):
		pPlot.setBonusType(-1)
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_COW'), True)
	if pPlot.getBonusType(-1) == getInfoType("BONUS_SHEEP"):
		pPlot.setBonusType(-1)
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_SHEEP'), True)
	if pPlot.getBonusType(-1) == getInfoType("BONUS_PIG"):
		pPlot.setBonusType(-1)
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_PIG'), True)
	if pPlot.getBonusType(-1) == getInfoType("BONUS_HORSE"):
		pPlot.setBonusType(-1)
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_HORSE'), True)
	if pPlot.getBonusType(-1) == getInfoType("BONUS_HYAPON"):
		pPlot.setBonusType(-1)
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_HYAPON'), True)
	if pPlot.getBonusType(-1) == getInfoType("BONUS_NIGHTMARE"):
		pPlot.setBonusType(-1)
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_NIGHTMARE'), True)
	if pPlot.getBonusType(-1) == getInfoType("BONUS_CAMEL"):
		pPlot.setBonusType(-1)
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_CAMEL'), True)
	if pPlot.getImprovementType()==getInfoType("IMPROVEMENT_PASTURE"):
		pPlot.setImprovementType(-1)

def spellSettleCattle(pCaster):
	pPlot = pCaster.plot()
	iCattle = getInfoType('PROMOTION_STOLEN_CATTLE')
	pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_CATTLE'), False)
	if pCaster.isHasPromotion(getInfoType('PROMOTION_LEADING_COW')):
		pPlot.setBonusType(getInfoType("BONUS_COW"))
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_COW'), False)
	if pCaster.isHasPromotion(getInfoType('PROMOTION_LEADING_SHEEP')):
		pPlot.setBonusType(getInfoType("BONUS_SHEEP"))
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_SHEEP'), False)
	if pCaster.isHasPromotion(getInfoType('PROMOTION_LEADING_PIG')):
		pPlot.setBonusType(getInfoType("BONUS_PIG"))
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_PIG'), False)
	if pCaster.isHasPromotion(getInfoType('PROMOTION_LEADING_HORSE')):
		pPlot.setBonusType(getInfoType("BONUS_HORSE"))
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_HORSE'), False)
	if pCaster.isHasPromotion(getInfoType('PROMOTION_LEADING_HYAPON')):
		pPlot.setBonusType(getInfoType("BONUS_HYAPON"))
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_HYAPON'), False)
	if pCaster.isHasPromotion(getInfoType('PROMOTION_LEADING_NIGHTMARE')):
		pPlot.setBonusType(getInfoType("BONUS_NIGHTMARE"))
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_NIGHTMARE'), False)
	if pCaster.isHasPromotion(getInfoType('PROMOTION_LEADING_CAMEL')):
		pPlot.setBonusType(getInfoType("BONUS_CAMEL"))
		pCaster.setHasPromotion(getInfoType('PROMOTION_LEADING_CAMEL'), False)
	
#SpawnGroup Spells End
# *******************
# Mekara Python: Jheral 4-mars-2011
#
# Python belonging to the Mekara Civilization
#Do not trust any Sluga code
#def findSlugaCommander(caster):
#	py = PyPlayer(caster.getOwner())
#	pPlot = caster.plot()
#	pBestUnit = -1
#	iBestRank = 7
#	iBestLevel = 9999
#	bSameGroup = False
#	for i in range(pPlot.getNumUnits()):
#		pUnit = pPlot.getUnit(i)
#		if pUnit.getOwner() == caster.getOwner():
#			if not pUnit.getID() == caster.getID():
#				if (bSameGroup and pUnit.getGroupID() == caster.getGroupID()) or (not bSameGroup):
#					if caster.getDomainType() == pUnit.getDomainType():
#						if not pUnit.getID() == caster.getCommanderUnit().getID() and not pUnit.getCommanderUnit().getID() == caster.getID():
#							if pUnit.getNumMinions() < pUnit.getCommandLimit():
#								if pUnit.getUnitClassType() == getInfoType("UNITCLASS_OVERSEER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_COMBAT_OVERSEER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_SLUGA_COMMANDER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_KARAS"):
#									iCommanderWeight = pUnit.getLevel()
#									if caster.getUnitClassType() == getInfoType("UNITCLASS_SLUGA") and pUnit.getUnitClassType() == getInfoType("UNITCLASS_OVERSEER"):
#										iCommanderWeight += 100
#									if (caster.getUnitClassType() == getInfoType("UNITCLASS_BATTLE_SLUGA") or caster.getUnitClassType() == getInfoType("UNITCLASS_WAR_SLUGA") or caster.getUnitClassType() == getInfoType("UNITCLASS_BEHEMOTH_SLUGA")) and (pUnit.getUnitClassType() == getInfoType("UNITCLASS_COMBAT_OVERSEER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_SLUGA_COMMANDER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_KARAS")):
#										iCommanderWeight += 100
#									if(pUnit.getGroupID() == caster.getGroupID()):
#										if not (bSameGroup):
#											pBestUnit = pUnit
#											iBestLevel = iCommanderWeight
#											bSameGroup = True
#										elif iCommanderWeight < iBestLevel:
#											pBestUnit = pUnit
#											iBestLevel = iCommanderWeight
#									else:
#										if iCommanderWeight < iBestLevel:
#											pBestUnit = pUnit
#											iBestLevel = iCommanderWeight
#	return pBestUnit
#Seems fine
def reqMekaraWorldspell(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	py = PyPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		iUnitCounter = 0
		for pUnit in py.getUnitList():
			if (pUnit.getUnitType() == getInfoType('UNIT_SLUGA_V2')
				or pUnit.getUnitClassType() == getInfoType('UNITCLASS_SLAVE')):
					iUnitCounter += 1
		if iUnitCounter < 12:
			return False
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		pTeam = gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) == 0:
			return False
	return True
#Seems fine
def spellMekaraWorldspell(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iBattleSluga = getInfoType('UNIT_WAR_SLUGA_V2')
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if (pUnit.getUnitType() == getInfoType('UNIT_SLUGA_V2') or pUnit.getUnitClassType() == getInfoType('UNITCLASS_SLAVE')):
				newUnit = pPlayer.initUnit(iBattleSluga, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(getInfoType('PROMOTION_INDEPENDENT_V2'), True)
				pUnit.kill(True,0)
#Seems fine
def reqAscension(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if isWorldUnitClass(caster.getUnitClassType()):
		return False
	if caster.getUnitType() == getInfoType("UNIT_ASCENDANT"):
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getUnitClassCount(getInfoType('UNITCLASS_IMMORTAL')) >= 4:
		return False
	return True

def spellLifedrinkerCombatWon(pCaster, pOpponent):
	if pOpponent.isAlive():
		pCaster.setHasPromotion(getInfoType('PROMOTION_VAMPIRIC_STRENGTH'), True)

def getHelpLifedrinker(argsList):
	ePromotion, pCaster = argsList
	iVampiricStrength = getInfoType('PROMOTION_VAMPIRIC_STRENGTH')

	if pCaster == -1 or pCaster.isNone():
		szHelp = ""
	else:
		iKillCount = pCaster.countHasPromotion(iVampiricStrength)
		szHelp = localText.getText("TXT_KEY_PYHELP_LIFEDRINKER", (iKillCount,iKillCount))
	return szHelp

def spellMokkaCauldronCombatWon(pCaster, pOpponent):
	if pOpponent.isAlive():
		iUnit = cf.getUnholyVersion(pOpponent)
		if iUnit != -1:
			newUnit = gc.getPlayer(pCaster.getOwner()).initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion( getInfoType('PROMOTION_DEMON'), True)
			newUnit.setDamage(50, PlayerTypes.NO_PLAYER)
			newUnit.finishMoves()
			szBuffer = gc.getUnitInfo(newUnit.getUnitType()).getDescription()
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MOKKAS_CAULDRON",((szBuffer, ))),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/Buildings/MokkasCauldron.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)


def spellAscension(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iUnit = getInfoType("UNIT_ASCENDANT")
	newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	iVampiricStrength = getInfoType('PROMOTION_VAMPIRIC_STRENGTH')
	iVampCount = caster.countHasPromotion(iVampiricStrength)
	if caster.isHasPromotion(getInfoType('PROMOTION_ASPIRANT')):
		newUnit.setHasPromotion(getInfoType('PROMOTION_ASPIRANT'),True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_ASPIRANT_1'),True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_ASPIRANT_2'),True)
		newUnit.setHasPromotion(getInfoType('PROMOTION_ASPIRANT_3'),True)
	for iProm in range(gc.getNumPromotionInfos()):
		if caster.isHasPromotion(iProm):
			if gc.getPromotionInfo(iProm).isEquipment():
				newUnit.setHasPromotion(iProm, True)
				caster.safeRemovePromotion(iProm)
			if iProm == getInfoType('PROMOTION_IMMORTAL'):
				caster.safeRemovePromotion(iProm)
			if iProm == getInfoType('PROMOTION_VAMPIRE'):
				newUnit.setHasPromotion(iProm, True)
				for i in xrange(iVampCount):
					newUnit.setHasPromotion(iVampiricStrength, True)
	caster.kill(True,0)

def spellCorgayleAscension(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iUnit = getInfoType("UNIT_CORGAYLE_ASCENDED")
	newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	iVampiricStrength = getInfoType('PROMOTION_VAMPIRIC_STRENGTH')
	iVampCount = caster.countHasPromotion(iVampiricStrength)
	for iProm in range(gc.getNumPromotionInfos()):
		if caster.isHasPromotion(iProm):
			if gc.getPromotionInfo(iProm).isEquipment():
				newUnit.setHasPromotion(iProm, True)
				caster.safeRemovePromotion(iProm)
			if iProm == getInfoType('PROMOTION_IMMORTAL'):
				caster.safeRemovePromotion(iProm)
			if iProm == getInfoType('PROMOTION_VAMPIRE'):
				newUnit.setHasPromotion(iProm, True)
				for i in xrange(iVampCount):
					newUnit.setHasPromotion(iVampiricStrength, True)
	caster.kill(True,0)
#Disabled
#def spellSlugaCreation(caster, slugaType):
#	pPlayer = gc.getPlayer(caster.getOwner())
#	pPlot = caster.plot()
#	if slugaType == 0:
#		iUnit = getInfoType("UNIT_SLUGA")
#	if slugaType == 1:
#		iUnit = getInfoType("UNIT_BATTLE_SLUGA")
#	if slugaType == 2:
#		iUnit = getInfoType("UNIT_SLAVE")
#	newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
#	caster.kill(True,0)
#Disabled
#def reqBehemothCreation(caster):
#	pPlayer = gc.getPlayer(caster.getOwner())
#	pPlot = caster.plot()
#	if pPlayer.getLeaderType() != getInfoType('LEADER_JAMAL'): return False
#	if pPlayer.getUnitClassCount(getInfoType('UNITCLASS_BEHEMOTH_SLUGA')) >= 4: return False
#	for i in range(pPlot.getNumUnits()):
#		pUnit = pPlot.getUnit(i)
#		if (pUnit.getUnitClassType() == getInfoType('UNITCLASS_SLAVE')
#			or pUnit.getUnitType() == getInfoType('UNIT_SLUGA')
#			or pUnit.getUnitType() == getInfoType('UNIT_BATTLE_SLUGA')
#			or pUnit.getUnitType() == getInfoType('UNIT_WAR_SLUGA')):
#			iMaterialCount += 1
#			if pUnit.isHasPromotion(getInfoType('PROMOTION_GIANTKIN')):
#				iMaterialCount += 1
#			if iMaterialCount >= 4:
#				return True
#	return False
#Disabled
#def spellBehemothCreation(caster):
#	pPlayer = gc.getPlayer(caster.getOwner())
#	pPlot = caster.plot()
#	iCounter = 0
#	iUnit = getInfoType('UNIT_BEHEMOTH_SLUGA')
#	while iCounter < 4:
#		for i in range(pPlot.getNumUnits()):
#			pUnit = pPlot.getUnit(i)
#			if (pUnit.getUnitClassType() == getInfoType('UNITCLASS_SLAVE')
#				or pUnit.getUnitType() == getInfoType('UNIT_SLUGA')
#				or pUnit.getUnitType() == getInfoType('UNIT_BATTLE_SLUGA')
#				or pUnit.getUnitType() == getInfoType('UNIT_WAR_SLUGA')):
#				if iCounter < 4:
#					if pUnit.isHasPromotion(getInfoType('PROMOTION_GIANTKIN')):
#						iCounter += 1
#					iCounter += 1
#					pUnit.kill(True, 0)
#	if iCounter == 4:
#		pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
#Seems fine
def reqEnslaveWorker(caster):
	if caster.getUnitType()==getInfoType('UNIT_OVERSEER_V2'):
		return False
	return True
#Seems fine
def reqEnslaveDissidents(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if pCity.getPopulation() < 3:
		return False
	if (pCity.happyLevel() - pCity.unhappyLevel(0)) < 0:
		return True
	return False	
#Seems fine	
def spellEnslaveDissidents(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iUnit = getInfoType("UNIT_SLAVE")
	newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	pCity.changeHurryAngerTimer(3)
#Seems fine
def spellGladiatorGames(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iGames = getInfoType('PROMOTION_WARGAMES_HELD')
	caster.setHasPromotion(iGames, True)
	pCity.setNumRealBuilding(getInfoType('BUILDING_WARGAMES'), 1)
#Seems fine
def spellGladiatorPerTurn(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iUnit = getInfoType('UNIT_GLADIATOR')
	iGames = getInfoType('PROMOTION_WARGAMES_HELD')
	iRnd = CyGame().getSorenRandNum(100, "Wargames Results")
	iDestruction = 1
	if iRnd < 45:
		caster.setHasPromotion(iGames, False)
		if iRnd < 20:
			caster.kill(True,0)
		elif caster.getUnitType() != iUnit:
			newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(caster)
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.isHasPromotion(iGames):
				iDestruction = 0
		if iDestruction == 1:
			pCity.setNumRealBuilding(getInfoType('BUILDING_WARGAMES'), 0)
#Seems fine (If ugly...)
def spellAugmentation(caster, augmentationType):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iTarget = getInfoType('PROMOTION_MEKARA_RITUAL_TARGET')
	pTarget = -1
	iEffectCounter = 3
	iManaCounter = 0
	manaTypes = -1

	for i in range(pPlot.getNumUnits()): #The target of the ritual is found...
		pUnit = pPlot.getUnit(i)
		if pUnit.isHasPromotion(iTarget):
			pTarget = pUnit #...and pointed to.

	if pTarget != -1:
		genericGoodEffects = [
			('PROMOTION_MEKARA_AUG_STREGTH_PERCENT_BONUS_1', 2),
			('PROMOTION_MEKARA_AUG_FSCHANCE_BONUS_1', 2)
			]       # Generic bonuses are defined
		genericBadEffects =  [
			('PROMOTION_MEKARA_AUG_STREGTH_PERCENT_PENALTY_1', 2),
			('PROMOTION_MEKARA_AUG_FSCHANCE_PENALTY_1', 2)
			]       # Generic drawbacks are defined

		# Aspected bonuses, drawbacks and specials are defined based on the type of augmentation used
		if augmentationType == 0: # Beserker
			pTarget.setHasPromotion( getInfoType('PROMOTION_MEKARA_AUG_OFFENCE_BASE_1'), True )
			manaTypes = [ 'BODY', 'FORCE' ]
			aspectedGoodEffects = [
				('PROMOTION_MEKARA_AUG_LIFESTEAL_1', 4),
				('PROMOTION_MEKARA_AUG_STREGTH_OFFENCE_BONUS_1', 3),
				('PROMOTION_MEKARA_AUG_CITYATT_BONUS_1', 3),
				('PROMOTION_MEKARA_AUG_STROFF_PERCENT_BONUS_1', 5)
				]
			aspectedBadEffects = [
				('PROMOTION_MEKARA_AUG_HEALRATE_PENALTY_1', 4),
				('PROMOTION_MEKARA_AUG_CITYDEF_PENALTY_1', 3),
				('PROMOTION_MEKARA_AUG_STREGTH_DEFENCE_PENALTY_1', 3),
				('PROMOTION_MEKARA_AUG_STRDEF_PERCENT_PENALTY_1', 5)
				]
			aspectedSpecialEffects = [
				('PROMOTION_MEKARA_AUG_OFFENCE_SPECIAL_1', 1)
				]
		elif augmentationType == 1: # Protector
			pTarget.setHasPromotion( getInfoType('PROMOTION_MEKARA_AUG_DEFENCE_BASE_1'), True )
			manaTypes = [ 'EARTH', 'LAW' ]
			aspectedGoodEffects = [
				('PROMOTION_MEKARA_AUG_HEALRATE_BONUS_1', 3),
				('PROMOTION_MEKARA_AUG_DSCHANCE_BONUS_1', 3),
				('PROMOTION_MEKARA_AUG_STREGTH_DEFENCE_BONUS_1', 2),
				('PROMOTION_MEKARA_AUG_CITYHILLDEF_BONUS_1', 4),
				('PROMOTION_MEKARA_AUG_STRDEF_PERCENT_BONUS_1', 5)
				]
			aspectedBadEffects = [
				('PROMOTION_MEKARA_AUG_TERRAINCOST_PENALTY_1', 5),
				('PROMOTION_MEKARA_AUG_WITHDRAW_PENALTY_1', 3),
				('PROMOTION_MEKARA_AUG_STREGTH_OFFENCE_PENALTY_1', 2),
				('PROMOTION_MEKARA_AUG_STROFF_PERCENT_PENALTY_1', 4)
				]
			aspectedSpecialEffects = [
				('PROMOTION_MEKARA_AUG_DEFENCE_SPECIAL_1', 1)
				]
		elif augmentationType == 2: # Assassin
			pTarget.setHasPromotion( getInfoType('PROMOTION_MEKARA_AUG_EVASION_BASE_1'), True )
			manaTypes = [ 'AIR', 'SHADOW' ]
			aspectedGoodEffects = [
				('PROMOTION_MEKARA_AUG_MOVEMENT_BONUS_1', 1),
				('PROMOTION_MEKARA_AUG_TERRAINCOST_BONUS_1', 3),
				('PROMOTION_MEKARA_AUG_HEALMOVE_BONUS_1', 2),
				('PROMOTION_MEKARA_AUG_WITHDRAW_BONUS_1', 4),
				('PROMOTION_MEKARA_AUG_FS_BONUS_1', 5),
				('PROMOTION_MEKARA_AUG_FSCHANCE_BONUS_2', 5)
				]
			aspectedBadEffects = [
				('PROMOTION_MEKARA_AUG_CITYATT_PENALTY_1', 3),
				('PROMOTION_MEKARA_AUG_STREGTH_DEFENCE_PENALTY_1', 1),
				('PROMOTION_MEKARA_AUG_STRDEF_PERCENT_PENALTY_2', 3)
				]
			aspectedSpecialEffects = [
				('PROMOTION_MEKARA_AUG_EVASION_SPECIAL_1', 1)
				]

	if manaTypes != -1:     # If mana types have been assigned...
		for szBonus in manaTypes:
			iBonus = pPlayer.getNumAvailableBonuses(getInfoType('BONUS_MANA_' + szBonus)) - 1
			for i in xrange(iBonus):
				iEffectCounter += 1     # ...add all the instances of the different mana types together...
				iManaCounter += 1
			if caster.isHasPromotion(getInfoType('PROMOTION_' + szBonus + '2')):
				iEffectCounter += 1
			if caster.isHasPromotion(getInfoType('PROMOTION_' + szBonus + '3')):
				iEffectCounter += 2     # ...along with the relevant promotions, to get the effect count


	iRnd = CyGame().getSorenRandNum(100, "Augmentation Results")
	if iRnd < 2:		# 2% chance of a special effect
		getAspectedSpecialEffect = wchoice( aspectedSpecialEffects, 'Roll mutation special effect' )
		pTarget.setHasPromotion( getInfoType( getAspectedSpecialEffect() ), True )

	for i in range(iEffectCounter):		# The effect count sets the number of effects that will be added.
		iRnd = CyGame().getSorenRandNum(100, "Augmentation Results")
		iRnd += iManaCounter * 2   		# The number of mana you have modifies the results
		iRnd = min(99,iRnd)
		if iRnd < 25:					# 25% chance of a aspected bad effect
			getAspectedBadEffect = wchoice( aspectedBadEffects, 'Roll mutation aspected bad effect' )
			pTarget.setHasPromotion( getInfoType( getAspectedBadEffect() ), True )
		if iRnd >= 25 and iRnd < 40:	# 15% chance of a generic bad effect
			getGenericBadEffect = wchoice( genericBadEffects, 'Roll mutation generic  bad effect' )
			pTarget.setHasPromotion( getInfoType( getGenericBadEffect() ), True )
		if iRnd >= 40 and iRnd < 60:	# 20% chance of no effect
			continue
		if iRnd >= 60 and iRnd < 75:	# 15% chance of a generic good effect
			getGenericGoodEffect = wchoice( genericGoodEffects, 'Roll mutation generic good effect' )
			pTarget.setHasPromotion( getInfoType( getGenericGoodEffect() ), True )
		if iRnd >= 75 and iRnd < 100:	# 25% chance of a aspected good effect
			getAspectedGoodEffect = wchoice( aspectedGoodEffects, 'Roll mutation aspected good effect' )
			pTarget.setHasPromotion( getInfoType( getAspectedGoodEffect() ), True )

		pTarget.setHasPromotion(getInfoType('PROMOTION_MEKARA_RITUAL_TARGET'), False)	# Remove target promotion, since the ritual is over
		pTarget.setHasPromotion(getInfoType('PROMOTION_MEKARA_AUGMENTED'), True)
		# Add the Augmented promotion, making the unit immune to futher augmentation or mutation
#Seems fine
def reqAugmentation(caster, augmentationType):
	pPlayer = gc.getPlayer(caster.getOwner())
	if augmentationType == 0: # Beserker
		manaTypes = [ 'BODY', 'FORCE' ]
	elif augmentationType == 1: # Protector
		manaTypes = [ 'EARTH', 'LAW' ]
	elif augmentationType == 2: # Assassin
		manaTypes = [ 'AIR', 'SHADOW' ]

	for szBonus in manaTypes:
		iBonus = pPlayer.getNumAvailableBonuses(getInfoType('BONUS_MANA_' + szBonus))
		if iBonus < 1:
			return False
	return True
#Seems fine(If ugly...)
def getHelpAugmentation(argsList):
	ePromotion, pCaster = argsList
	bFirst = True
	chp = pCaster.countHasPromotion

	## Generic Promotions
	iGenericGood1 = getInfoType('PROMOTION_MEKARA_AUG_STREGTH_PERCENT_BONUS_1')
	iGenericGood2 = getInfoType('PROMOTION_MEKARA_AUG_FSCHANCE_BONUS_1')
	iGenericBad1 = getInfoType('PROMOTION_MEKARA_AUG_STREGTH_PERCENT_PENALTY_1')
	iGenericBad2 = getInfoType('PROMOTION_MEKARA_AUG_FSCHANCE_PENALTY_1')

	## Beserker Promotions
	iOffenceGood1 = getInfoType('PROMOTION_MEKARA_AUG_LIFESTEAL_1')
	iOffenceGood2 = getInfoType('PROMOTION_MEKARA_AUG_STREGTH_OFFENCE_BONUS_1')
	iOffenceGood3 = getInfoType('PROMOTION_MEKARA_AUG_CITYATT_BONUS_1')
	iOffenceGood4 = getInfoType('PROMOTION_MEKARA_AUG_STROFF_PERCENT_BONUS_1')
	iOffenceBad1 = getInfoType('PROMOTION_MEKARA_AUG_HEALRATE_PENALTY_1')
	iOffenceBad2 = getInfoType('PROMOTION_MEKARA_AUG_CITYDEF_PENALTY_1')
	iOffenceBad3 = getInfoType('PROMOTION_MEKARA_AUG_STREGTH_DEFENCE_PENALTY_1')
	iOffenceBad4 = getInfoType('PROMOTION_MEKARA_AUG_STRDEF_PERCENT_PENALTY_1')
	iOffenceBase1 = getInfoType('PROMOTION_MEKARA_AUG_OFFENCE_BASE_1')
	iOffenceSpecial1 = getInfoType('PROMOTION_MEKARA_AUG_OFFENCE_SPECIAL_1')

	## Protector Promotions
	iDefenceGood1 = getInfoType('PROMOTION_MEKARA_AUG_HEALRATE_BONUS_1')
	iDefenceGood2 = getInfoType('PROMOTION_MEKARA_AUG_DSCHANCE_BONUS_1')
	iDefenceGood3 = getInfoType('PROMOTION_MEKARA_AUG_STREGTH_DEFENCE_BONUS_1')
	iDefenceGood4 = getInfoType('PROMOTION_MEKARA_AUG_CITYHILLDEF_BONUS_1')
	iDefenceGood5 = getInfoType('PROMOTION_MEKARA_AUG_STRDEF_PERCENT_BONUS_1')
	iDefenceBad1 = getInfoType('PROMOTION_MEKARA_AUG_TERRAINCOST_PENALTY_1')
	iDefenceBad2 = getInfoType('PROMOTION_MEKARA_AUG_WITHDRAW_PENALTY_1')
	iDefenceBad3 = getInfoType('PROMOTION_MEKARA_AUG_STREGTH_OFFENCE_PENALTY_1')
	iDefenceBad4 = getInfoType('PROMOTION_MEKARA_AUG_STROFF_PERCENT_PENALTY_1')
	iDefenceBase1 = getInfoType('PROMOTION_MEKARA_AUG_DEFENCE_BASE_1')
	iDefenceSpecial1 = getInfoType('PROMOTION_MEKARA_AUG_DEFENCE_SPECIAL_1')

	## Assassin Promotions
	iEvasionGood1 = getInfoType('PROMOTION_MEKARA_AUG_MOVEMENT_BONUS_1')
	iEvasionGood2 = getInfoType('PROMOTION_MEKARA_AUG_HEALMOVE_BONUS_1')
	iEvasionGood3 = getInfoType('PROMOTION_MEKARA_AUG_WITHDRAW_BONUS_1')
	iEvasionGood4 = getInfoType('PROMOTION_MEKARA_AUG_FS_BONUS_1')
	iEvasionGood5 = getInfoType('PROMOTION_MEKARA_AUG_FSCHANCE_BONUS_2')
	iEvasionGood6 = getInfoType('PROMOTION_MEKARA_AUG_TERRAINCOST_BONUS_1')
	iEvasionBad1 = getInfoType('PROMOTION_MEKARA_AUG_CITYATT_PENALTY_1')
	iEvasionBad2 = getInfoType('PROMOTION_MEKARA_AUG_STREGTH_DEFENCE_PENALTY_1')
	iEvasionBad3 = getInfoType('PROMOTION_MEKARA_AUG_STRDEF_PERCENT_PENALTY_2')
	iEvasionBase1 = getInfoType('PROMOTION_MEKARA_AUG_EVASION_BASE_1')
	iEvasionSpecial1 = getInfoType('PROMOTION_MEKARA_AUG_EVASION_SPECIAL_1')


	if pCaster == -1 or pCaster.isNone():
		szHelp = ""
	else:
		szHelp = ""
		iSTRPerNum			= (chp(iGenericGood1) * 2) - chp(iGenericBad1)
		iSTRDefPerNum		= (chp(iDefenceGood5) * 4) - (chp(iOffenceBad4) * 1) - (chp(iEvasionBad3) * 2)
		iSTROffPerNum		= (chp(iOffenceGood4) * 4) - (chp(iDefenceBad4) * 1)
		iSTRDefFlatNum		= (chp(iDefenceGood3) + (chp(iDefenceSpecial1) * 3) + (chp(iDefenceBase1) * 2) + (chp(iOffenceSpecial1) * 2)) - chp(iEvasionBad2) - chp(iOffenceBad3)
		iSTROffFlatNum		= (chp(iOffenceGood2) + (chp(iOffenceSpecial1) * 2) + (chp(iOffenceBase1) * 1)) - chp(iDefenceBad3)
		iSTRDefCityPerNum	= (chp(iDefenceGood4) * 4) - (chp(iOffenceBad2) * 2)
		iSTROffCityPerNum	= (chp(iOffenceGood3) * 3) - (chp(iEvasionBad1) * 2)
		iSTRDefHillPerNum	= (chp(iDefenceGood4) * 4)
		iFSChanceNum		= (chp(iGenericGood2) + (chp(iEvasionGood5) * 2) + (chp(iEvasionBase1) * 2)) - chp(iGenericBad2)
		iFSNum				= chp(iEvasionGood4) + chp(iEvasionBase1)
		iDSNum				= (chp(iDefenceGood2) * 2)
		iHealRateNum		= (chp(iDefenceGood1) * 3) - (chp(iOffenceBad1) * 2)
		iHealMoveNum		= chp(iEvasionGood2)
		iHealCombatNum		= (chp(iOffenceGood1) * 5)
		iWithdrawNum		= (chp(iEvasionGood3) * 5) + (chp(iEvasionBase1) * 5) - (chp(iDefenceBad2) * 5)
		if iWithdrawNum > 90: iWithdrawNum = 90
		iMovesNum			= chp(iEvasionGood1) + chp(iEvasionSpecial1)
		iTerrCostNum		= chp(iDefenceBad1) - chp(iEvasionGood6) - chp(iEvasionBase1)
		iOffSpec			= chp(iOffenceSpecial1)
		iDefSpec			= chp(iDefenceSpecial1)
		iEvaSpec			= chp(iEvasionSpecial1)

		if not (iSTRPerNum == 0):
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_STR_PER", (iSTRPerNum * 5,))
			bFirst = False
		if not (iSTROffPerNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_STR_PER_OFF", (iSTROffPerNum * 5,))
			bFirst = False
		if not (iSTRDefPerNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_STR_PER_DEF", (iSTRDefPerNum * 5,))
			bFirst = False
		if not (iSTROffFlatNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_STR_OFF", (iSTROffFlatNum,))
			bFirst = False
		if not (iSTRDefFlatNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_STR_DEF", (iSTRDefFlatNum,))
			bFirst = False
		if not (iSTROffCityPerNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_STR_PER_OFFCITY", (iSTROffCityPerNum * 5,))
			bFirst = False
		if not (iSTRDefCityPerNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_STR_PER_DEFCITY", (iSTRDefCityPerNum * 5,))
			bFirst = False
		if not (iSTRDefHillPerNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_STR_PER_DEFHILL", (iSTRDefHillPerNum * 5,))
			bFirst = False
		if not (iFSChanceNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_FSCHANCE", (iFSChanceNum,))
			bFirst = False
		if not (iFSNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_FS", (iFSNum,))
			bFirst = False
		if not (iDSNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_DS", (iDSNum * 5, iDSNum * 5))
			bFirst = False
		if not (iHealRateNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_HEALRATE", (iHealRateNum,))
			bFirst = False
		if not (iHealMoveNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_HEALMOVE", (iHealMoveNum,))
			bFirst = False
		if not (iHealCombatNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_HEALCOMBAT", (iHealCombatNum,))
			bFirst = False
		if not (iWithdrawNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_WITHDRAW", (iWithdrawNum,))
			bFirst = False
		if not (iMovesNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_MOVES", (iMovesNum,))
			bFirst = False
		if not (iTerrCostNum == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_TERRCOST", (iTerrCostNum,))
			bFirst = False
		if not (iOffSpec == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_OFF_SPECIAL", (0,))
			bFirst = False
		if not (iDefSpec == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_DEF_SPECIAL", (0,))
			bFirst = False
		if not (iEvaSpec == 0):
			if not (bFirst):
				szHelp += localText.getText("TXT_KEY_PYHELP_AUG_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_AUG_EVA_SPECIAL", (0,))
			bFirst = False

	return szHelp
#Seems fine
def spellShaperExperiments(caster):
	pTarget = -1
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitClassType() == getInfoType('UNITCLASS_SLAVE'):
			pTarget = pUnit
	if pTarget != -1:
		caster.setHasPromotion(getInfoType('PROMOTION_SHAPER_EXPERIMENTS'), True)
		pTarget.kill(True,0)

def spellSlugaMaelstrom1(caster):
	getPlot	= CyMap().plot
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				pUnit.doDamage(20, 40, caster, getInfoType('DAMAGE_LIGHTNING'), True)

def spellSlugaMaelstrom2(caster):
	getPlot	= CyMap().plot
	pPlayer = gc.getPlayer(caster.getOwner())
	pTeam = gc.getTeam(pPlayer.getTeam())
	iRange = 1 + caster.getSpellExtraRange()
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			for i in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				pPlayer2 = gc.getPlayer(pUnit.getOwner())
				eTeam2 = pPlayer2.getTeam()
				if pTeam.isAtWar(eTeam2) == true:
					pUnit.doDamage(30, 60, caster, getInfoType('DAMAGE_LIGHTNING'), True)

def reqSlaveSettle(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iMax = pCity.getPopulation() / 4
	if pCity.getNumBuilding(getInfoType('BUILDING_PAGAN_TEMPLE_MEKARA')) == 1:
		iMax += 2
	if pCity.getNumBuilding(getInfoType('BUILDING_SHAPER_LAB')) == 1:
		iMax += 2
	if pCity.getNumBuilding(getInfoType('BUILDING_PALACE_MEKARA')) == 1:
		iMax += 2
	if pCity.getNumBuilding(getInfoType('BUILDING_COLOSSEUM')) == 1:
		iMax += 2
	if pCity.getNumBuilding(getInfoType('BUILDING_SLAVE_MARKET')) == 1:
		iMax += 4
	if pCity.getNumBuilding(getInfoType('BUILDING_BREEDING_PIT')) == 1:
		iMax += 4
	if pCity.getNumBuilding(getInfoType('BUILDING_GOVERNORS_MANOR')) == 1:
		iMax += 4
	if pCity.getNumBuilding(getInfoType('BUILDING_TEMPLE_OF_AGRUONN')) == 1:
		iMax += 2
	if pCity.getNumBuilding(getInfoType('BUILDING_TEMPLE_OF_BLOODTHIRSTY_FLAME')) == 1:
		iMax += 2
	if pCity.getNumBuilding(getInfoType('BUILDING_CRIME_BLOOD_SLAVERY')) == 1:
		iMax += 2
	if pCity.getNumBuilding(getInfoType('BUILDING_SACRIFICIAL_ALTAR')) == 1:
		iMax += 4
	if pCity.getNumBuilding(getInfoType('BUILDING_PALACE_CUALLI')) == 1:
		iMax += 2
	if pCity.getNumBuilding(getInfoType('BUILDING_MARKET_SLAVE')) == 1:
		iMax += 4
	if pCity.getNumBuilding(getInfoType('BUILDING_SLAVE_PIT')) == 1:
		iMax += 4
	if pCity.getNumBuilding(getInfoType('BUILDING_MINISTRY_OF_TRUTH')) == 1:
		iMax += 4
	iCount = pCity.getFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_SLAVE'))
	if iCount >= iMax:
		return False
	else:
		return True

def spellSlaveSettle(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pCity.changeFreeSpecialistClassCount(getInfoType('SPECIALISTCLASS_SLAVE'), 1)
	caster.kill(True,0)
#Seems fine
def reqCorgayleChanneling1(pCaster):
	if (pCaster.isHasPromotion(getInfoType('PROMOTION_CHANNELING1'))):
		return False
	return True
#Seems fine
def reqCorgayleChanneling2(pCaster):
	if (pCaster.isHasPromotion(getInfoType('PROMOTION_CHANNELING2'))):
		return False
	return True
#Seems fine
def spellBloom(caster):
	pPlot = caster.plot()
	iTerrain = pPlot.getTerrainType()
	if iTerrain == getInfoType('TERRAIN_TUNDRA'):
		pPlot.setFeatureType(getInfoType('FEATURE_FOREST_NEW'), -1)
	elif iTerrain == getInfoType('TERRAIN_GRASS'):
		pPlot.setFeatureType(getInfoType('FEATURE_FOREST_NEW'), -1)
	elif iTerrain == getInfoType('TERRAIN_PLAINS'):
		pPlot.setFeatureType(getInfoType('FEATURE_FOREST_NEW'), -1)
	elif iTerrain == getInfoType('TERRAIN_TAIGA'):
		pPlot.setFeatureType(getInfoType('FEATURE_FOREST_NEW'), -1)
	elif iTerrain == getInfoType('TERRAIN_MARSH'):
		pPlot.setFeatureType(getInfoType('FEATURE_FOREST_NEW'), -1)
# *******************
# Mekara V2 Python: 2025-04-13
#
# Python belonging to the Mekara V2 Civilization
#
Slaves = [
	getInfoType("UNIT_SLAVE"),
	getInfoType("UNIT_SLAVE_UNDEAD")
]
#New V2 Behemoth spell, converted from Flight of Drakes
def reqFormSlugaBehemoth(caster):
	pPlot = caster.plot()
	iUnitType = caster.getUnitType()
	numSameTypeSlaves = 0 # Will add self
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner() and pUnit.getUnitType() == iUnitType):
			numSameTypeSlaves += 1
	return numSameTypeSlaves >= 4
#New V2 Behemoth spell, converted from Flight of Drakes
def spellFormSlugaBehemoth(caster):
	# The actual upgrading of the original unit is done in the XML,
	# so this code just kills the two lowest experienced drakes of the same type
	pPlot = caster.plot()
	iUnitType = caster.getUnitType()
	iID = caster.getID()
	sameTypeSlaves = [] # Will not include self
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner() and pUnit.getUnitType() == iUnitType and pUnit.getID() != iID):
			sameTypeSlaves.append(pUnit)
	sameTypeSlaves.sort(cmp = lambda a, b: a.getExperienceTimes100() - b.getExperienceTimes100())
	for i in range(3):
		if sameTypeSlaves[i].isImmortal():
			sameTypeSlaves[i].changeImmortal(-10)
		sameTypeSlaves[i].kill(True, 0)


def reqAddT1Wolf(pCaster):
	# check units on tile. If at least one wolf T2 or t3 is present and has not combat V, return true
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		print "Hello Test"
		print GenericPromo.keys()
		pPromo = GenericPromo["Combat V"]
		if iUnit in (Animal["Wolf Pack"], Animal["Dire Wolf"]):
			if not pUnit.isHasPromotion(pPromo):
				return True
	return False

def spellAddT1Wolf(pCaster):
	# TODO: realize better version of this spell: if human player, show list of wolf units without combat V to choose from
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		HasPromo = pUnit.isHasPromotion
		SetPromo = pUnit.setHasPromotion
		if iUnit in (Animal["Wolf Pack"], Animal["Dire Wolf"]) and not HasPromo(GenericPromo["Combat V"]):
			if not HasPromo(GenericPromo["Combat I"]):
				SetPromo(GenericPromo["Combat I"], True)
			elif not HasPromo(GenericPromo["Combat II"]):
				SetPromo(GenericPromo["Combat II"], True)
			elif not HasPromo(GenericPromo["Combat III"]):
				SetPromo(GenericPromo["Combat III"], True)
			elif not HasPromo(GenericPromo["Combat IV"]):
				SetPromo(GenericPromo["Combat IV"], True)
			else:
				SetPromo(GenericPromo["Combat V"], True)
			break

def reqAddT2Wolf(pCaster):
	# check units on tile. If at least one wolf T2 or t3 is present and has not combat V, return true
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		if iUnit == Animal["Dire Wolf"]:
			if not pUnit.isHasPromotion(GenericPromo["Combat V"]):
				return True
	return False

def spellAddT2Wolf(pCaster):
	# TODO: realize better version of this spell: if human player, show list of wolf units without combat V to choose from
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		HasPromo = pUnit.isHasPromotion
		SetPromo = pUnit.setHasPromotion
		if iUnit == Animal["Dire Wolf"] and not HasPromo(GenericPromo["Combat V"]):
			if not HasPromo(GenericPromo["Combat I"]):
				SetPromo(GenericPromo["Combat I"], True)
			elif not HasPromo(GenericPromo["Combat II"]):
				SetPromo(GenericPromo["Combat II"], True)
			elif not HasPromo(GenericPromo["Combat III"]):
				SetPromo(GenericPromo["Combat III"], True)
			elif not HasPromo(GenericPromo["Combat IV"]):
				SetPromo(GenericPromo["Combat IV"], True)
			else:
				SetPromo(GenericPromo["Combat V"], True)
			break

def reqAddT1Bear(pCaster):
	# check units on tile. If at least one Bear T2 or t3 is present and has not combat V, return true
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		if iUnit in (Animal["Bear group"], Animal["Cave Bears"]):
			if not pUnit.isHasPromotion(GenericPromo["Combat V"]):
				return True
	return False

def spellAddT1Bear(pCaster):
	# TODO: realize better version of this spell: if human player, show list of Bear units without combat V to choose from
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		HasPromo = pUnit.isHasPromotion
		SetPromo = pUnit.setHasPromotion
		if iUnit in (Animal["Bear group"], Animal["Cave Bears"]) and not HasPromo(GenericPromo["Combat V"]):
			if not HasPromo(GenericPromo["Combat I"]):
				SetPromo(GenericPromo["Combat I"], True)
			elif not HasPromo(GenericPromo["Combat II"]):
				SetPromo(GenericPromo["Combat II"], True)
			elif not HasPromo(GenericPromo["Combat III"]):
				SetPromo(GenericPromo["Combat III"], True)
			elif not HasPromo(GenericPromo["Combat IV"]):
				SetPromo(GenericPromo["Combat IV"], True)
			else:
				SetPromo(GenericPromo["Combat V"], True)
			break

def reqAddT2Bear(pCaster):
	# check units on tile. If at least one Bear T2 or t3 is present and has not combat V, return true
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		if iUnit == Animal["Cave Bears"]:
			if not pUnit.isHasPromotion(GenericPromo["Combat V"]):
				return True
	return False

def spellAddT2Bear(pCaster):
	# TODO: realize better version of this spell: if human player, show list of Bear units without combat V to choose from
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		HasPromo = pUnit.isHasPromotion
		SetPromo = pUnit.setHasPromotion
		if iUnit == Animal["Cave Bears"] and not HasPromo(GenericPromo["Combat V"]):
			if not HasPromo(GenericPromo["Combat I"]):
				SetPromo(GenericPromo["Combat I"], True)
			elif not HasPromo(GenericPromo["Combat II"]):
				SetPromo(GenericPromo["Combat II"], True)
			elif not HasPromo(GenericPromo["Combat III"]):
				SetPromo(GenericPromo["Combat III"], True)
			elif not HasPromo(GenericPromo["Combat IV"]):
				SetPromo(GenericPromo["Combat IV"], True)
			else:
				SetPromo(GenericPromo["Combat V"], True)
			break

def reqAddT1Boar(pCaster):
	# check units on tile. If at least one Boar T2 or t3 is present and has not combat V, return true
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		if iUnit in (Animal["Boar Herd"], Animal["Blood Boar"]):
			if not pUnit.isHasPromotion(GenericPromo["Combat V"]):
				return True
	return False

def spellAddT1Boar(pCaster):
	# TODO: realize better version of this spell: if human player, show list of Boar units without combat V to choose from
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		HasPromo = pUnit.isHasPromotion
		SetPromo = pUnit.setHasPromotion
		if iUnit in (Animal["Boar Herd"], Animal["Blood Boar"]) and not HasPromo(GenericPromo["Combat V"]):
			if not HasPromo(GenericPromo["Combat I"]):
				SetPromo(GenericPromo["Combat I"], True)
			elif not HasPromo(GenericPromo["Combat II"]):
				SetPromo(GenericPromo["Combat II"], True)
			elif not HasPromo(GenericPromo["Combat III"]):
				SetPromo(GenericPromo["Combat III"], True)
			elif not HasPromo(GenericPromo["Combat IV"]):
				SetPromo(GenericPromo["Combat IV"], True)
			else:
				SetPromo(GenericPromo["Combat V"], True)
			break

def reqAddT2Boar(pCaster):
	# check units on tile. If at least one Boar T2 or t3 is present and has not combat V, return true
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		if iUnit == Animal["Blood Boar"]:
			if not pUnit.isHasPromotion(GenericPromo["Combat V"]):
				return True
	return False

def spellAddT2Boar(pCaster):
	# TODO: realize better version of this spell: if human player, show list of Boar units without combat V to choose from
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		HasPromo = pUnit.isHasPromotion
		SetPromo = pUnit.setHasPromotion
		if iUnit == Animal["Blood Boar"] and not HasPromo(GenericPromo["Combat V"]):
			if not HasPromo(GenericPromo["Combat I"]):
				SetPromo(GenericPromo["Combat I"], True)
			elif not HasPromo(GenericPromo["Combat II"]):
				SetPromo(GenericPromo["Combat II"], True)
			elif not HasPromo(GenericPromo["Combat III"]):
				SetPromo(GenericPromo["Combat III"], True)
			elif not HasPromo(GenericPromo["Combat IV"]):
				SetPromo(GenericPromo["Combat IV"], True)
			else:
				SetPromo(GenericPromo["Combat V"], True)
			break

def reqAddT1Gorilla(pCaster):
	# check units on tile. If at least one Gorilla T2 or t3 is present and has not combat V, return true
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		if iUnit in (Animal["Gorilla Troop"], Animal["Silverback"]):
			if not pUnit.isHasPromotion(GenericPromo["Combat V"]):
				return True
	return False

def spellAddT1Gorilla(pCaster):
	# TODO: realize better version of this spell: if human player, show list of Gorilla units without combat V to choose from
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		HasPromo = pUnit.isHasPromotion
		SetPromo = pUnit.setHasPromotion
		if iUnit in (Animal["Gorilla Troop"], Animal["Silverback"]) and not HasPromo(GenericPromo["Combat V"]):
			if not HasPromo(GenericPromo["Combat I"]):
				SetPromo(GenericPromo["Combat I"], True)
			elif not HasPromo(GenericPromo["Combat II"]):
				SetPromo(GenericPromo["Combat II"], True)
			elif not HasPromo(GenericPromo["Combat III"]):
				SetPromo(GenericPromo["Combat III"], True)
			elif not HasPromo(GenericPromo["Combat IV"]):
				SetPromo(GenericPromo["Combat IV"], True)
			else:
				SetPromo(GenericPromo["Combat V"], True)
			break

def reqAddT2Gorilla(pCaster):
	# check units on tile. If at least one Gorilla T2 or t3 is present and has not combat V, return true
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		if iUnit == Animal["Silverback"]:
			if not pUnit.isHasPromotion(GenericPromo["Combat V"]):
				return True
	return False

def spellAddT2Gorilla(pCaster):
	# TODO: realize better version of this spell: if human player, show list of Gorilla units without combat V to choose from
	pPlot = pCaster.plot()
	for i in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnit = pUnit.getUnitType()
		HasPromo = pUnit.isHasPromotion
		SetPromo = pUnit.setHasPromotion
		if iUnit == Animal["Silverback"] and not HasPromo(GenericPromo["Combat V"]):
			if not HasPromo(GenericPromo["Combat I"]):
				SetPromo(GenericPromo["Combat I"], True)
			elif not HasPromo(GenericPromo["Combat II"]):
				SetPromo(GenericPromo["Combat II"], True)
			elif not HasPromo(GenericPromo["Combat III"]):
				SetPromo(GenericPromo["Combat III"], True)
			elif not HasPromo(GenericPromo["Combat IV"]):
				SetPromo(GenericPromo["Combat IV"], True)
			else:
				SetPromo(GenericPromo["Combat V"], True)
			break
# FoL - boats spread kelp
def reqPlantKelp(pCaster):
	# We need at least 1 free water tile around the caster
	getPlot = CyMap().plot
	for x, y in plotsInRange( pCaster.getX(), pCaster.getY(), 1, 1 ):
		pPlot = getPlot(x, y)
		if pPlot.getTerrainType() in [iCoast, iOcean] and pPlot.getFeatureType() == -1:
			return True
	return False

def spellPlantKelp(pCaster):
	getPlot 	= CyMap().plot
	iBestValue	= -1
	pBestPlot	= -1
	for x, y in plotsInRange( pCaster.getX(), pCaster.getY(), 1, 1 ):
		pPlot = getPlot(x, y)
		if pPlot.getTerrainType() in [iCoast, iOcean] and pPlot.getFeatureType() == -1:
			iValue = CyGame().getSorenRandNum(10, "Plant Kelp")
			if iValue > iBestValue:
				iBestValue = iValue
				pBestPlot = pPlot
	if pBestPlot != -1:
		pBestPlot.setFeatureType(Feature["Kelp"], 0)
# FoL - boats spread kelp END


def spellFreePromotion(pCaster):
	pCaster.changeFreePromotionPick(1)

	
def postCombatWinIntolerant(pCaster, pOpponent):
	
	pPlayer = gc.getPlayer(pCaster.getOwner())
	StateBelief = pPlayer.getStateReligion()
	pOtherPlayer = gc.getPlayer(pOpponent.getOwner())
	OtherStateBelief = pOtherPlayer.getStateReligion()
	if StateBelief != OtherStateBelief:
		pCaster.setHasPromotion(getInfoType("PROMOTION_CRUSADER"),True)

def spellDivinePurge(pCaster):
	for i in range(pCaster.getNumMinions()):
		pMinion=pCaster.getMinionUnit(i)
		pMinion.setHasPromotion(getInfoType("PROMOTION_CRUSADER"),False)
		
	pPlot = pCaster.plot()
	pCity = pPlot.getPlotCity()
	for iPlayer in xrange(gc.getMAX_PLAYERS()):
		if iPlayer != pCaster.getOwner():
			pCity.setCultureTimes100(iPlayer,0,True)
			
def spellHolyCleansing(pCaster):
	for i in range(pCaster.getNumMinions()):
		pMinion=pCaster.getMinionUnit(i)
		pMinion.setHasPromotion(getInfoType("PROMOTION_CRUSADER"),False)


def spellRecycle(pCaster):
	pPlot = pCaster.plot()
	pCity = pPlot.getPlotCity()
	pCity.changeProduction(gc.getUnitInfo(pCaster.getUnitType()).getProductionCost()/5)
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if pPlayer.hasTrait(getInfoType('TRAIT_CRAFTMASTER2')):
		pCity.changeCulture(pCaster.getOwner(), gc.getUnitInfo(pCaster.getUnitType()).getProductionCost()/5, True)

def reqRecycle(pCaster):
	if isWorldUnitClass(pCaster.getUnitClassType()):
		return false
	return true

def reqSidequest(pCaster):
	if (pCaster.getDomainType()!=gc.getInfoTypeForString("DOMAIN_LAND")):
		return False
	return True

def reqGiftWerewolf(caster):
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner()):
			if not pUnit.isHasPromotion(getInfoType('PROMOTION_WEREWOLF')):
				return True
	return False

def spellGiftWerewolf(caster):
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner()):
			if not pUnit.isHasPromotion(getInfoType('PROMOTION_WEREWOLF')):
				pUnit.setHasPromotion(getInfoType('PROMOTION_WEREWOLF'),True)
				iInfectChance = 30
				if pPlayer.hasTrait(Trait["Lycanthropic2"]):
					iInfectChance = 15
				if pPlayer.hasTrait(Trait["Lycanthropic3"]):
					iInfectChance = 0
				if CyGame().getSorenRandNum(100, "Werewolf Infection") < iInfectChance:
					pUnit.kill(False,-1)
	
def spellBreakClavaVindex(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if not gc.isNoCrash():
		gc.getGame().emptyDeathListtoDeathList(gc.getInfoTypeForString('DEATHLIST_BASIUM'),gc.getInfoTypeForString('DEATHLIST_DEMON_CONVERSION'))
		gc.getGame().emptyDeathListtoDeathList(gc.getInfoTypeForString('DEATHLIST_BASIUM_DEMON'),gc.getInfoTypeForString('DEATHLIST_DEMON_REBIRTH'))
	
def reqBreakClavaVindex(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getStateReligion() == getInfoType('RELIGION_THE_ASHEN_VEIL'):
		return True
	return False
	
def spellBreakNetherBlade(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if not gc.isNoCrash():
		gc.getGame().emptyDeathListtoResurrectList(gc.getInfoTypeForString('DEATHLIST_NETHERBLADE'),-1)
def reqBreakNetherBlade(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.getCivilizationType() != Civ["Sidar"]:
		return True
	return False
	
def postCombatGodslayer(pCaster, pOpponent):
	gc 		= CyGlobalContext()
	iWinner	= pCaster.getOwner()	
	iAvatar = gc.getInfoTypeForString('PROMOTION_AVATAR')
	if pOpponent.isHasPromotion(iAvatar):
		pOpponent.setHasPromotion(iAvatar, False)
		pOpponent.kill(True, iWinner)	
		
def postCombatNetherBlade(pCaster, pOpponent):
	gc 		= CyGlobalContext()
	iWinner	= pCaster.getOwner()
	pPlot = pCaster.plot()
	if (pOpponent.isAlive()):
		if not gc.isNoCrash():
			gc.getGame().addtoDeathList(gc.getInfoTypeForString('DEATHLIST_NETHERBLADE'),pOpponent)
		pOpponent.kill(True, iWinner)
		CyInterface().addMessage(pOpponent.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_NETHERBLADE", ()),'AS2D_UNIT_FALLS',3,'Art/Interface/Buttons/equipment/netherblade.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
	
def postCombatClavaVindex(pCaster, pOpponent):
	gc 		= CyGlobalContext()
	iWinner	= pCaster.getOwner()	
	if pOpponent.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON')) or pOpponent.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ICE_DEMON')) :
		if not gc.isNoCrash():
			gc.getGame().addtoDeathList(gc.getInfoTypeForString('DEATHLIST_BASIUM_DEMON'),pOpponent)
		pOpponent.changeImmortal(-100)
		pOpponent.kill(True, iWinner)
		
				
	elif CvEventInterface.getEventManager().cf.angelorMane(pOpponent) == gc.getInfoTypeForString('UNIT_MANES'):
		if not gc.isNoCrash():
			gc.getGame().addtoDeathList(gc.getInfoTypeForString('DEATHLIST_BASIUM'),pOpponent)
		pOpponent.kill(True, iWinner)
	

# Mekara Python End

	
def spellCreateUtopia(pCity):
	pCity.setNumRealBuilding(getInfoType('BUILDING_UTOPIA'), 1)

	

def reqCreateUtopia(pCity):
	pPlayer = gc.getPlayer(pCity.getOwner())

	if not pPlayer.isHuman():
		if pCity.isCapital(): return False

	if pCity.getNumRealBuilding(getInfoType('BUILDING_UTOPIA')) > 0:
		return False

	return True

def spellRemoveUtopia(pCity):
	pCity.setNumRealBuilding(getInfoType('BUILDING_UTOPIA'), 0)


def reqRemoveUtopia(pCity):
	pPlayer = gc.getPlayer(pCity.getOwner())

	if not pPlayer.isHuman():
		if pCity.isCapital():
			return False

	if pCity.getNumRealBuilding(getInfoType('BUILDING_UTOPIA')) > 0:
		return True

def spellOpenWellSouls(pCaster):
	pPlot=pCaster.plot()
	pPlot.setImprovementType(getInfoType("IMPROVEMENT_WELL_OF_SOULS_OPEN"))

def reqPurifyWell(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if pPlayer.getStateReligion()==getInfoType('RELIGION_THE_ASHEN_VEIL'):
		return False
	hasPromo	= pCaster.isHasPromotion
	if hasPromo(getInfoType('PROMOTION_LIFE3')) or hasPromo(getInfoType('PROMOTION_METAMAGIC3')) or hasPromo(getInfoType('PROMOTION_SPIRIT3')) :
		return True
	return False

def spellPurifyWell(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	hasPromo	= pCaster.isHasPromotion
	iDuration = 20
	if hasPromo(getInfoType('PROMOTION_LIFE3')):
		iDuration -=3
	if hasPromo(getInfoType('PROMOTION_METAMAGIC3')):
		iDuration -=3
	if hasPromo(getInfoType('PROMOTION_SPIRIT3')):
		iDuration -=3
		
	pCaster.setHasPromotion(getInfoType('PROMOTION_PURIFYING_WELL'),True)
	pCaster.setPromotionDuration(getInfoType('PROMOTION_PURIFYING_WELL'),iDuration)
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			iLoopTeam   = pLoopPlayer.getTeam()
			iLoopCiv    = pLoopPlayer.getCivilizationType()
			if iLoopCiv==Civ["Infernal"]:
				startWar(iLoopPlayer, pCaster.getOwner(), WarPlanTypes.WARPLAN_TOTAL)

def spellTurnPurifyWell(pCaster):
	iWarPlayer=-1
	for iLoopPlayer in range(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iLoopPlayer)
		if pLoopPlayer.isAlive():
			iLoopTeam   = pLoopPlayer.getTeam()
			iLoopCiv    = pLoopPlayer.getCivilizationType()
			if iLoopCiv==Civ["Infernal"]:
				iWarPlayer =iLoopPlayer
	if iWarPlayer==-1:
		iWarPlayer=gc.getDEMON_PLAYER()
	pWarPlayer=gc.getPlayer(iWarPlayer)
	iDuration = pCaster.getPromotionDuration(getInfoType("PROMOTION_PURIFYING_WELL"))
	if iDuration %3==1:
		if iDuration ==19 :
			pSpawnPlot= findClearPlot(pCaster,-1,iWarPlayer)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_HELLHOUND'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(1000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_HELLHOUND'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(1000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_HELLHOUND'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(1000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_CHAOS_MARAUDER'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(1000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_CHAOS_MARAUDER'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(1000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_PIT_BEAST'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(1000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_PIT_BEAST'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(1000, -1)
		elif iDuration ==16:
			pSpawnPlot= findClearPlot(pCaster,-1,iWarPlayer)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_HELLHOUND'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(2000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_HELLHOUND'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(2000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_CHAOS_MARAUDER'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(2000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_MOBIUS_WITCH'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(4000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_PIT_BEAST'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(2000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_PIT_BEAST'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(2000, -1)
		elif iDuration ==13:
			pSpawnPlot= findClearPlot(pCaster,-1,iWarPlayer)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_SECT_OF_FLIES'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(4000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_SECT_OF_FLIES'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(4000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(4000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_DISEASED_CORPSE'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(4000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_IRA'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(4000, -1)
		elif iDuration ==10:
			pSpawnPlot= findClearPlot(pCaster,-1,iWarPlayer)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_SECT_OF_FLIES'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(5000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(5000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_DISEASED_CORPSE'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(5000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_IRA'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(5000, -1)
			
		elif iDuration ==7:
			pSpawnPlot= findClearPlot(pCaster,-1,iWarPlayer)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_SECT_OF_FLIES'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(6000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(6000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_DISEASED_CORPSE'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(6000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_PRIEST_OF_THE_VEIL'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(6000, -1)
		elif iDuration ==4:
			pSpawnPlot= findClearPlot(pCaster,-1,iWarPlayer)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_BALOR'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(8000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_BEAST_OF_AGARES'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(8000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_HIGH_PRIEST_OF_THE_VEIL'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(8000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_EIDOLON'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(8000, -1)
		elif iDuration ==1:
			pSpawnPlot= findClearPlot(pCaster,-1,iWarPlayer)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_BEAST_OF_AGARES'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(10000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_HIGH_PRIEST_OF_THE_VEIL'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(10000, -1)
			newUnit = pWarPlayer.initUnit(getInfoType('UNIT_EIDOLON'), pSpawnPlot.getX(), pSpawnPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setExperienceTimes100(10000, -1)
		
def spellFinalPurifyWell(pCaster):
	pPlot=pCaster.plot()
	pPlot.setImprovementType(getInfoType("IMPROVEMENT_BRADELINES_WELL_PURIFIED"))
	gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_PURIFIED_WELL'),True)
	pCaster.setHasPromotion(getInfoType('PROMOTION_WELL_PURIFIER'),True)
	
def spellArchosCriminalFeed(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	caster.changeExperience(pCity.getCrime()/50, -1, False, False, False)
	pCity.changeCrime(-pCity.getCrime()/2)
	
def spellArchosCriminalFeedMiscast(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	caster.changeExperience(pCity.getCrime()/25, -1, False, False, False)
	pCity.changeCrime(-pCity.getCrime()/4)
	if (pCity.getPopulation()>3):
		pCity.changePopulation(-3)
		pCity.changeHurryAngerTimer(5)
	elif(pCity.getPopulation()>1):
		pCity.changePopulation(-1)
		pCity.changeHurryAngerTimer(5)

def spellSlaverCriminalEnslave(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pCity.changeCrime(-pCity.getCrime()/2)
	newUnit1 = pPlayer.initUnit(getInfoType('UNIT_SLAVE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2 = pPlayer.initUnit(getInfoType('UNIT_SLAVE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellDrownCrew(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iCombat = caster.baseCombatStr()
	pPlot = caster.plot()
	for i in range (iCombat/3):
		newUnit = pPlayer.initUnit(getInfoType('UNIT_DROWN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def spellDrownCrewUpgraded(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iCombat = caster.baseCombatStr()
	pPlot = caster.plot()
	for i in range (iCombat/3):
		newUnit = pPlayer.initUnit(getInfoType('UNIT_STYGIAN_GUARD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def helpDemonOfTheDeep(argsList):
	eSpell, pCaster = argsList
	if pCaster == -1 or pCaster.isNone():
		szHelp = ""
	else:
		iCount = pCaster.baseCombatStr() / 3
		if eSpell == gc.getInfoTypeForString("SPELL_DROWN_CREW"):
			szUnitDescription = gc.getUnitInfo(gc.getInfoTypeForString("UNIT_DROWN")).getDescription()
		elif eSpell == gc.getInfoTypeForString("SPELL_DROWN_CREW_UPGRADED"):
			szUnitDescription = gc.getUnitInfo(gc.getInfoTypeForString("UNIT_STYGIAN_GUARD")).getDescription()
		szHelp = localText.getText("TXT_KEY_PYHELP_SPELL_DROWN_CREW", (szUnitDescription,iCount,szUnitDescription))
	return szHelp

#Kahd's Vault Gate Help
def helpVaultGates (argsList):
	eBuilding, pCity = argsList
	if pCity == -1 or pCity.isNone():
		szHelp 			= ""
	else:
		szHelp 			= ""
		pPlayer			= gc.getPlayer(pCity.getOwner())
		git				= gc.getInfoTypeForString
		iCityB			= pCity.getNumBuilding
		iNumB			= pPlayer.countNumBuildings
		iNumUC			= pPlayer.getUnitClassCount
		iNumMana		= pPlayer.getNumAvailableBonuses
		UnitCap			= 1
		ChanceMult 		= 1
		SpawnChance		= 0
		if pPlayer.hasTrait(getInfoType("TRAIT_KAHD_OGHMA")):
			UnitCap		= 1.5
			ChanceMult	= 3
		if iCityB(getInfoType('BUILDING_LIBRARY')) > 0:
			ChanceMult	+= 0.5
		iGates			= iNumB(getInfoType('BUILDING_KAHDI_VAULT_GATE'))
		iLibrary		= iNumB(getInfoType('BUILDING_LIBRARY'))
		iSchool			= iNumB(getInfoType('BUILDING_SCHOOL_OF_GOVANNON'))
		iGreatLibrary 	= iNumB(getInfoType('BUILDING_GREAT_LIBRARY'))
		iMageGuild		= iNumB(getInfoType('BUILDING_WIZARDS_HALL'))
		bWH				= iCityB(getInfoType('BUILDING_WIZARDS_HALL'))
		bGov			= iCityB(getInfoType('BUILDING_SCHOOL_OF_GOVANNON'))
		iMMMana			= iNumMana(getInfoType('BONUS_MANA_METAMAGIC'))
		iFireMana		= iNumMana(getInfoType('BONUS_MANA_FIRE'))
		iAirMana		= iNumMana(getInfoType('BONUS_MANA_AIR'))
		iDeathMana		= iNumMana(getInfoType('BONUS_MANA_DEATH'))
		iBodyMana		= iNumMana(getInfoType('BONUS_MANA_BODY'))
		iEntropyMana	= iNumMana(getInfoType('BONUS_MANA_ENTROPY'))
		iIceMana		= iNumMana(getInfoType('BONUS_MANA_ICE'))
		iLawMana		= iNumMana(getInfoType('BONUS_MANA_LAW'))
		iShadowMana		= iNumMana(getInfoType('BONUS_MANA_SHADOW'))
		iSunMana		= iNumMana(getInfoType('BONUS_MANA_SUN'))
		iWaterMana		= iNumMana(getInfoType('BONUS_MANA_WATER'))
		# Calculation start
		print "testing vault help"
		SpawnChance		= round(((ChanceMult * gc.getDefineINT('PLANAR_GATE_CHANCE')) / 100), 2)
		UnitCap			= UnitCap * (iGates + iLibrary + iSchool + iGreatLibrary * 4 + iMageGuild)
		iGnoslingCur	= iNumUC(getInfoType('UNITCLASS_GNOSLING'))
		iGnoslingMax	= UnitCap / 2
		if iGnoslingMax != int(iGnoslingMax):
			iGnoslingMax = int(iGnoslingMax)+1
		iThadeCur		= iNumUC(getInfoType('UNITCLASS_THADE'))
		iThadeMax		= bWH * UnitCap / 3
		if iThadeMax != int(iThadeMax):
			iThadeMax = int(iThadeMax)+1
		iDjinnCur		= iNumUC(getInfoType('UNITCLASS_DJINN'))
		iDjinnMax		= bGov * iMMMana * UnitCap / 8
		if iDjinnMax != int(iDjinnMax):
			iDjinnMax = int(iDjinnMax)+1
		iFElementalCur	= iNumUC(getInfoType('UNITCLASS_FIRE_ELEMENTAL'))
		iFElementalMax	= bGov * iFireMana * UnitCap / 6
		if iFElementalMax != int(iFElementalMax):
			iFElementalMax = int(iFElementalMax)+1
		iAElementalCur	= iNumUC(getInfoType('UNITCLASS_AIR_ELEMENTAL'))
		iAElementalMax	= bGov * iAirMana * UnitCap / 6
		if iAElementalMax != int(iAElementalMax):
			iAElementalMax = int(iAElementalMax)+1
		iSpectreCur		= iNumUC(getInfoType('UNITCLASS_SPECTRE'))
		iSpectreMax		= bGov * iDeathMana * UnitCap / 4
		if iSpectreMax != int(iSpectreMax):
			iSpectreMax = int(iSpectreMax)+1
		iFleshGolemCur	= iNumUC(getInfoType('UNITCLASS_FLESH_GOLEM'))
		iFleshGolemMax	= bGov * iBodyMana * UnitCap / 6
		if iFleshGolemMax != int(iFleshGolemMax):
			iFleshGolemMax = int(iFleshGolemMax)+1
		iPitBeastCur	= iNumUC(getInfoType('UNITCLASS_PIT_BEAST'))
		iPitBeastMax	= bGov * iEntropyMana * UnitCap / 4
		if iPitBeastMax != int(iPitBeastMax):
			iPitBeastMax = int(iPitBeastMax)+1
		iIElementalCur	= iNumUC(getInfoType('UNITCLASS_ICE_ELEMENTAL'))
		iIElementalMax	= bGov * iIceMana * UnitCap / 4
		if iIElementalMax != int(iIElementalMax):
			iIElementalMax = int(iIElementalMax)+1
		iEinherjarCur	= iNumUC(getInfoType('UNITCLASS_EINHERJAR'))
		iEinherjarMax	= bGov * iLawMana * UnitCap / 4
		if iEinherjarMax != int(iEinherjarMax):
			iEinherjarMax = int(iEinherjarMax)+1
		iMistformCur	= iNumUC(getInfoType('UNITCLASS_MISTFORM'))
		iMistformMax	= bGov * iShadowMana * UnitCap / 8
		if iMistformMax != int(iMistformMax):
			iMistformMax = int(iMistformMax)+1
		iAurealisCur	= iNumUC(getInfoType('UNITCLASS_AUREALIS'))
		iAurealisMax	= bGov * iSunMana * UnitCap / 6
		if iAurealisMax != int(iAurealisMax):
			iAurealisMax = int(iAurealisMax)+1
		iWElementalCur	= iNumUC(getInfoType('UNITCLASS_WATER_ELEMENTAL'))
		iWElementalMax	= bGov * iWaterMana * UnitCap / 6
		if iWElementalMax != int(iWElementalMax):
			iWElementalMax = int(iWElementalMax)+1
		iPsionCur		= iNumUC(getInfoType('UNITCLASS_PSION'))
		iPsionMax		= 0
		if pPlayer.hasTrait(getInfoType("TRAIT_KAHD_MAMMON")):
			iPsionMax	= 1 + UnitCap / 10
		if iPsionMax != int(iPsionMax):
			iPsionMax = int(iPsionMax)+1
		# Calculation end
		# Pop-up start
		if not SpawnChance == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_CHANCE", (int(SpawnChance),))
		if not iGnoslingMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_GNOSLING", (iGnoslingCur,iGnoslingMax,))
		if not iThadeMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_THADE", (iThadeCur,iThadeMax,))
		if not iDjinnMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_DJINN", (iDjinnCur,iDjinnMax,))
		if not iFElementalMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_F_ELEMENTAL", (iFElementalCur,iFElementalMax,))
		if not iAElementalMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_A_ELEMENTAL", (iAElementalCur,iAElementalMax,))
		if not iSpectreMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_SPECTRE", (iSpectreCur,iSpectreMax,))
		if not iFleshGolemMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_FLESH_GOLEM", (iFleshGolemCur,iFleshGolemMax,))
		if not iPitBeastMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_PIT_BEAST", (iPitBeastCur,iPitBeastMax,))
		if not iIElementalMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_I_ELEMENTAL", (iIElementalCur,iIElementalMax,))
		if not iEinherjarMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_EINHERJAR", (iEinherjarCur,iEinherjarMax,))
		if not iMistformMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_MISTFORM", (iMistformCur,iMistformMax,))
		if not iAurealisMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_AUREALIS", (iAurealisCur,iAurealisMax,))
		if not iWElementalMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_W_ELEMENTAL", (iWElementalCur,iWElementalMax,))
		if not iPsionMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_PSION", (iPsionCur,iPsionMax,))
		if iCityB(getInfoType('BUILDING_LIBRARY')) == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_LIBRARY", ())
		if bWH == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_WIZARD_HALL", ())
		if bGov == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_SCHOOL_OF_GOVANNON", ())
		# Pop-up end
	return szHelp	
	
# Wizard`s Hall Help
def helpWizardsHall (argsList):
	eBuilding, pCity = argsList
	if pCity == -1 or pCity.isNone():
		szHelp 			= ""
	else:
		szHelp 			= ""
		pPlayer			= gc.getPlayer(pCity.getOwner())
		git				= gc.getInfoTypeForString
		iCityB			= pCity.getNumBuilding
		iNumMana		= pPlayer.getNumAvailableBonuses
		bCav			= iCityB(getInfoType('BUILDING_CAVE_OF_ANCESTORS'))
		bGov			= iCityB(getInfoType('BUILDING_SCHOOL_OF_GOVANNON'))
		iAirNum 		= iNumMana(getInfoType('BONUS_MANA_AIR'))
		iBodNum 		= iNumMana(getInfoType('BONUS_MANA_BODY'))
		iChaNum			= iNumMana(getInfoType('BONUS_MANA_CHAOS'))
		iCreNum			= iNumMana(getInfoType('BONUS_MANA_CREATION'))
		iDeaNum 		= iNumMana(getInfoType('BONUS_MANA_DEATH'))
		iDimNum 		= iNumMana(getInfoType('BONUS_MANA_DIMENSIONAL'))
		iEarNum 		= iNumMana(getInfoType('BONUS_MANA_EARTH'))
		iEncNum			= iNumMana(getInfoType('BONUS_MANA_ENCHANTMENT'))
		iEntNum 		= iNumMana(getInfoType('BONUS_MANA_ENTROPY'))
		iFirNum 		= iNumMana(getInfoType('BONUS_MANA_FIRE'))
		iForNum 		= iNumMana(getInfoType('BONUS_MANA_FORCE'))
		iIceNum 		= iNumMana(getInfoType('BONUS_MANA_ICE'))
		iLawNum 		= iNumMana(getInfoType('BONUS_MANA_LAW'))
		iLifNum 		= iNumMana(getInfoType('BONUS_MANA_LIFE'))
		iMetNum 		= iNumMana(getInfoType('BONUS_MANA_METAMAGIC'))
		iMinNum 		= iNumMana(getInfoType('BONUS_MANA_MIND'))
		iNatNum 		= iNumMana(getInfoType('BONUS_MANA_NATURE'))
		iShaNum 		= iNumMana(getInfoType('BONUS_MANA_SHADOW'))
		iSpiNum 		= iNumMana(getInfoType('BONUS_MANA_SPIRIT'))
		iSunNum 		= iNumMana(getInfoType('BONUS_MANA_SUN'))
		iWatNum 		= iNumMana(getInfoType('BONUS_MANA_WATER'))
		# Calculation start
		PromoChance		= 20 + ((iAirNum + iBodNum + iChaNum + iCreNum + iDeaNum + iDimNum + iEarNum + iEncNum + iEntNum + iFirNum + iForNum + iIceNum + iLawNum + iLifNum + iMetNum + iMinNum + iNatNum + iShaNum + iSpiNum + iSunNum + iWatNum) * 5)
		if PromoChance > 100:
			PromoChance = 100
		# Calculation end
		# Pop-up start
		if bCav == 0 and bGov == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_WH_1", (PromoChance,))
		if bCav == 1 and bGov == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_WH_1_AND_2", (PromoChance,))
		if bCav == 0 and bGov == 1:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_WH_1", (PromoChance,))
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_WH_GOV", (PromoChance,))
		if bCav == 1 and bGov == 1:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_WH_1_AND_2", (PromoChance,))
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_WH_GOV", (PromoChance,))
		if bCav == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_WH_NO_CAV", (PromoChance,))
		if bGov == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_WH_NO_GOV", (PromoChance,))
		# Pop-up end
	return szHelp
#Planar Gate Help
def helpPlanarGate (argsList):
	eBuilding, pCity = argsList
	if pCity == -1 or pCity.isNone():
		szHelp 			= ""
	else:
		szHelp 			= ""
		pPlayer			= gc.getPlayer(pCity.getOwner())
		git				= gc.getInfoTypeForString
		iCityB			= pCity.getNumBuilding
		iNumB			= pPlayer.countNumBuildings
		iNumUC			= pPlayer.getUnitClassCount
		iGC				= CyGame().getGlobalCounter()
		iGates			= iNumB(getInfoType('BUILDING_PLANAR_GATE'))
		bGH				= iCityB(getInfoType('BUILDING_GAMBLING_HOUSE'))
		bMG				= iCityB(getInfoType('BUILDING_MAGE_GUILD'))
		bCarnival		= iCityB(getInfoType('BUILDING_CARNIVAL'))
		bGrove			= iCityB(getInfoType('BUILDING_GROVE'))
		bPB				= iCityB(getInfoType('BUILDING_PUBLIC_BATHS'))
		bOG				= iCityB(getInfoType('BUILDING_OBSIDIAN_GATE'))
		bTOTV			= iCityB(getInfoType('BUILDING_TEMPLE_OF_THE_VEIL'))
		UnitCap			= 1
		# Calculation start
		if iGC			>= 50:
			UnitCap		= 2
		if iGC			>= 75:
			UnitCap		= 3
		if iGC			>= 100:
			UnitCap		= 4 
		UnitCap			= UnitCap * iGates
		iRevelersCur	= iNumUC(getInfoType('UNITCLASS_REVELERS'))
		iRevelersMax	= UnitCap * bGH
		iMobiusWitchCur	= iNumUC(getInfoType('UNITCLASS_MOBIUS_WITCH'))
		iMobiusWitchMax	= UnitCap * bMG
		iMarauderCur	= iNumUC(getInfoType('UNITCLASS_CHAOS_MARAUDER'))
		iMarauderMax	= UnitCap * bCarnival
		iManticoreCur	= iNumUC(getInfoType('UNITCLASS_MANTICORE'))
		iManticoreMax	= UnitCap * bGrove
		iSuccubusCur	= iNumUC(getInfoType('UNITCLASS_SUCCUBUS'))
		iSuccubusMax	= UnitCap * bPB
		iMinotaurCur	= iNumUC(getInfoType('UNITCLASS_MINOTAUR'))
		iMinotaurMax	= UnitCap * bOG
		iTarDemonCur	= iNumUC(getInfoType('UNITCLASS_TAR_DEMON'))
		iTarDemonMax	= UnitCap * bTOTV
		iBurningEyeCur	= iNumUC(getInfoType('UNITCLASS_FIREBALL'))
		iBurningEyeMax	= UnitCap
		# Calculation end
		# Pop-up start
		if not iBurningEyeMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_FIREBALL", (iBurningEyeCur,iBurningEyeMax,))
		if not iRevelersMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_REVELERS", (iRevelersCur,iRevelersMax,))
		if not iMobiusWitchMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_MOBIUS_WITCH", (iMobiusWitchCur,iMobiusWitchMax,))
		if not iMarauderMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_CHAOS_MARAUDER", (iMarauderCur,iMarauderMax,))
		if not iManticoreMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_MANTICORE", (iManticoreCur,iManticoreMax,))
		if not iSuccubusMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_SUCCUBUS", (iSuccubusCur,iSuccubusMax,))
		if not iMinotaurMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_MINOTAUR", (iMinotaurCur,iMinotaurMax,))
		if not iTarDemonMax == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_TAR_DEMON", (iTarDemonCur,iTarDemonMax,))
		if bGH == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_NO_GAMBLING_HOUSE", ())
		if bMG == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_NO_MAGE_GUILD", ())
		if bCarnival == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_NO_CARNIVAL", ())
		if bGrove == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_NO_GROVE", ())
		if bPB == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_NO_PUBLIC_BATHS", ())
		if bOG == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_NO_OBSIDIAN_GATE", ())
		if bTOTV == 0:
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_PGATE_NO_TEMPLE_OF_THE_VEIL", ())
		# Pop-up end
	return szHelp
# *******************
# Modular Python: ANW 16-feb-2010
#                     29-may-2010
#                     15-aug-2010
#                     02-sep-2010
#
# this part overrides existing spells :)
#

## Load spells from modules
MLFlist = []
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\NormalModules\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FirstLoad\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\SecondLoad\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\ThirdLoad\\")
MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FourthLoad\\")

for pathToMLF in MLFlist:
	for modules in os.listdir(pathToMLF):
		pathToModuleRoot = pathToMLF+modules+"\\"
		# Ignore all xml files
		if modules.lower()[-4:] != ".xml":
			# Check whether path exists // whether current directory isn't actually a file
			if os.path.exists(pathToModuleRoot):
				# Check whether python folder is present
				if "python" in os.listdir(pathToModuleRoot):
					pathToModulePython = pathToModuleRoot+"python\\"
					# For every file in that folder
					for pythonFileSourceName in os.listdir(pathToModulePython):
						pythonFileSource = pathToModulePython+pythonFileSourceName
						# Is it non-python file ?
						if (pythonFileSource.lower()[-3:] != ".py"):
							continue
						# Is it non-spelloverwrite file ?
						if pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ].upper()[0:8] != "SPELLOVR":
							continue

						tempFileName = file(pythonFileSource)
						tempModuleName = pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ]
						imp.load_module( tempModuleName, tempFileName, tempModuleName+".py", ("","",1))
						#print(pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ])
						exec("from "+tempModuleName+" import *")
						tempFileName.close()

# Modular Python End
# *******************

def spellRestoreFP(caster):
	pPlot = caster.plot()
	pPlot.setFeatureType(getInfoType('FEATURE_FLOOD_PLAINS'),1)

def reqRestoreFP(caster):
	pPlot = caster.plot()
	if pPlot.getTerrainType() == getInfoType('TERRAIN_DESERT') and pPlot.isRiver() and pPlot.isFlatlands() and not pPlot.isCity() and pPlot.getFeatureType()==-1:
		return true

# Combining similar goodies r363
# GOODY_MARNOK_GEAR_STASH
def exploreGearStash(argsList):
	pUnit, pPlot	= argsList
	pUnitCombat		= pUnit.getUnitCombatType()
	pPlayer			= gc.getPlayer(pUnit.getOwner())
	ReconUC			= getInfoType('UNITCOMBAT_RECON')
	MeleeUC			= getInfoType('UNITCOMBAT_MELEE')
	MountedUC		= getInfoType('UNITCOMBAT_MOUNTED')
	ArcherUC		= getInfoType('UNITCOMBAT_ARCHER')
	ReconGearSet	= [('PROMOTION_CLIMBING_KIT_RECON',1),('PROMOTION_DEADLY_TRAPS_RECON',1),('PROMOTION_DESERT_GEAR_RECON',1),('PROMOTION_FINE_KIT_RECON',1),('PROMOTION_ICE_GEAR_RECON',1),('PROMOTION_MANTRAPS_RECON',1),('PROMOTION_MARCH_WINE_RECON',1),('PROMOTION_SNOW_GEAR_RECON',1),('PROMOTION_WOODS_GEAR_RECON',1),('PROMOTION_SUPERIOR_KIT_RECON',1),('PROMOTION_EXCELLENT_KIT_RECON',1)]
	MeleeGearSet	= [('PROMOTION_BARBED_WEAPONS_MELEE',1),('PROMOTION_BLESSED_ARMOR_MELEE',1),('PROMOTION_CURSED_WEAPONS_MELEE',1),('PROMOTION_SLAB_PLATE_MELEE',1),('PROMOTION_FINE_EQUIPMENT_MELEE',1),('PROMOTION_PLATE_MELEE',1)]
	MountedGearSet	= [('PROMOTION_BLESSED_ARMOR_MOUNTED',1),('PROMOTION_CATAPHRACT_ARMOR_MOUNTED',1),('PROMOTION_CURSED_LANCES_MOUNTED',1),('PROMOTION_EXCELLENT_TACK_MOUNTED',1),('PROMOTION_HORSELORDS_TACK_MOUNTED',1),('PROMOTION_SUPERIOR_TACK_MOUNTED',1)]
	ArcherGearSet	= [('PROMOTION_COMPOSITE_BOWS_ARCHER',1),('PROMOTION_COMPOUND_BOWS_ARCHER',1),('PROMOTION_FINE_BOWS_ARCHER',1)]
	Tries			= 5 # rerolling promotion few times if pUnit already have that one
	listPromoBefore	= []
	listPromoAfter	= []
	for PromosBefore in range(gc.getNumPromotionInfos()): # if promotions before = promotions after - give player some gold
		if pUnit.isHasPromotion(PromosBefore):
			listPromoBefore.append(PromosBefore)
	while Tries > 0:
		if pUnitCombat == ReconUC:
			getReconGearSet = wchoice(ReconGearSet,'Roll Recon Stash Promo')
			iPromo = getInfoType(getReconGearSet())
			pUnit.setHasPromotion(iPromo,True)
			listPromoAfter = []
			for PromosAfter in range(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(PromosAfter):
					listPromoAfter.append(PromosAfter)
			if listPromoBefore == listPromoAfter:
				Tries += -1
				continue
			else:
				break
		elif pUnitCombat == MeleeUC:
			getMeleeGearSet = wchoice(MeleeGearSet,'Roll Melee Stash Promo')
			iPromo = getInfoType(getMeleeGearSet())
			pUnit.setHasPromotion(iPromo,True)
			listPromoAfter = []
			for PromosAfter in range(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(PromosAfter):
					listPromoAfter.append(PromosAfter)
			if listPromoBefore == listPromoAfter:
				Tries += -1
				continue
			else:
				break
		elif pUnitCombat == MountedUC:
			getMountedGearSet = wchoice(MountedGearSet,'Roll Mounted Stash Promo')
			iPromo = getInfoType(getMountedGearSet())
			pUnit.setHasPromotion(iPromo,True)
			listPromoAfter = []
			for PromosAfter in range(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(PromosAfter):
					listPromoAfter.append(PromosAfter)
			if listPromoBefore == listPromoAfter:
				Tries += -1
				continue
			else:
				break
		elif pUnitCombat == ArcherUC:
			getArcherGearSet = wchoice(ArcherGearSet,'Roll Archer Stash Promo')
			iPromo = getInfoType(getArcherGearSet())
			pUnit.setHasPromotion(iPromo,True)
			listPromoAfter = []
			for PromosAfter in range(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(PromosAfter):
					listPromoAfter.append(PromosAfter)
			if listPromoBefore == listPromoAfter:
				Tries += -1
				continue
			else:
				break
	if listPromoBefore == listPromoAfter:
		CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_NO_NEW_EQUIPMENT", ()),'AS2D_GOODY_SETTLER',3,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		RndGold		= gc.getGame().getSorenRandNum(26, "Empty Stash")
		pPlayer.changeGold(25+RndGold)


def reqGearStash(argsList):
	pUnit, pPlot	= argsList
	pUnitCombat		= pUnit.getUnitCombatType()
	ReconUC			= getInfoType('UNITCOMBAT_RECON')
	MeleeUC			= getInfoType('UNITCOMBAT_MELEE')
	MountedUC		= getInfoType('UNITCOMBAT_MOUNTED')
	ArcherUC		= getInfoType('UNITCOMBAT_ARCHER')
	AllowedUC		= [ReconUC,MeleeUC,MountedUC,ArcherUC]
	if pUnitCombat in AllowedUC:
		return True
	return False

def reqBereguine(argsList):
	pUnit, pPlot	= argsList
	pPlayer=gc.getPlayer(pUnit.getOwner())
	if pPlayer.getStateReligion() !=getInfoType("RELIGION_FELLOWSHIP_OF_LEAVES"):
		return True
	return False
def exploreLairBereguine(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	OrcPlayer			= gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot			= findClearPlot(-1, pPlot)
	newUnit				= OrcPlayer.initUnit(getInfoType('UNIT_BEREGUINE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def reqBocquillon(argsList):
	pUnit, pPlot	= argsList
	pPlayer=gc.getPlayer(pUnit.getOwner())
	if pPlayer.getStateReligion()==getInfoType("RELIGION_FELLOWSHIP_OF_LEAVES"):
		return True
	return False
def exploreLairBocquillon(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	OrcPlayer			= gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot			= findClearPlot(-1, pPlot)
	newUnit				= pPlayer.initUnit(getInfoType('UNIT_BOCQUILLON'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	

# GOODY_MARNOK_RELEASE_PRISONER_MAJOR
def exploreReleasePrisoner(argsList):
	pUnit, pPlot	= argsList
	pPlayer			= gc.getPlayer(pUnit.getOwner())
	PrisonersList	= []
	PrisonersList.append('UNIT_ADVENTURER')
	if pPlayer.isHasTech(getInfoType('TECH_FESTIVALS')):
		PrisonersList.append('UNIT_ARTIST')
		PrisonersList.append('UNIT_MERCHANT')
	if pPlayer.isHasTech(getInfoType('TECH_KNOWLEDGE_OF_THE_ETHER')):
		PrisonersList.append('UNIT_SCIENTIST')
	if pPlayer.isHasTech(getInfoType('TECH_CONSTRUCTION')):
		PrisonersList.append('UNIT_ENGINEER')
	if pPlayer.isHasTech(getInfoType('TECH_WARFARE')):
		PrisonersList.append('UNIT_COMMANDER')
	if pPlayer.isHasTech(getInfoType('TECH_PHILOSOPHY')):
		PrisonersList.append('UNIT_PROPHET')
	if pPlayer.isHasTech(getInfoType('TECH_AGRICULTURE')):
		PrisonersList.append('UNIT_HEALER')
	Prisoner		= PrisonersList[gc.getGame().getSorenRandNum(len(PrisonersList), "Pick Prisoner Major")]
	newUnit			= pPlayer.initUnit(getInfoType(Prisoner), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# GOODY_MARNOK_SUBTERRAN_BONUS_MINOR
def exploreSubterranBonusMinor(argsList):
	pUnit, pPlot	= argsList
	BonusList		= []
	BonusList.append(getInfoType('BONUS_GOLD'))
	BonusList.append(getInfoType('BONUS_COPPER'))
	BonusList.append(getInfoType('BONUS_GEMS'))
	BonusList.append(getInfoType('BONUS_MARBLE'))
	BonusList.append(getInfoType('BONUS_STONE'))
	BonusList.append(getInfoType('BONUS_SALT'))
	Bonus			= BonusList[gc.getGame().getSorenRandNum(len(BonusList), "Pick Bonus Minor")]
	pPlot.setBonusType(Bonus)

def reqSubterranBonusMinor(argsList):
	pUnit, pPlot	= argsList
	if pPlot.getBonusType(-1) == -1:
		return True
	return False

# GOODY_MARNOK_RANDOM_MANA
def exploreMarnokMana(argsList):
	pUnit, pPlot	= argsList
	ManaList		= []
	ManaList.append('_AIR')
	ManaList.append('_BODY')
	ManaList.append('_CHAOS')
	ManaList.append('_CREATION')
	ManaList.append('_DEATH')
	ManaList.append('_DIMENSIONAL')
	ManaList.append('_EARTH')
	ManaList.append('_ENCHANTMENT')
	ManaList.append('_ENTROPY')
	ManaList.append('_FIRE')
	ManaList.append('_FORCE')
	ManaList.append('_ICE')
	ManaList.append('_LAW')
	ManaList.append('_LIFE')
	ManaList.append('_METAMAGIC')
	ManaList.append('_MIND')
	ManaList.append('_NATURE')
	ManaList.append('_SHADOW')
	ManaList.append('_SPIRIT')
	ManaList.append('_SUN')
	ManaList.append('_WATER')
	szMana			= ManaList[gc.getGame().getSorenRandNum(len(ManaList), "Pick Bonus Mana")]
	pPlot.setBonusType(getInfoType('BONUS_MANA' + szMana))
	pUnit.setHasPromotion(getInfoType('PROMOTION' + szMana + '1'),True)

def reqMarnokMana(argsList):
	pUnit, pPlot	= argsList
	if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent():
		return False
	if pPlot.getBonusType(-1) == -1:
		return True
		
	return False
# GOODY_EXPLORE_LAIR_ANIMAL_BLOOD
def exploreAnimalBlood(argsList):
	pUnit, pPlot	= argsList
	pPlayer			= gc.getPlayer(pUnit.getOwner())
	iLair			= pPlot.getImprovementType()
	BloodList		= [getInfoType('PROMOTION_BEAR_BLOOD'),getInfoType('PROMOTION_BOAR_BLOOD'),getInfoType('PROMOTION_ELEPHANT_BLOOD'),getInfoType('PROMOTION_GORILLA_BLOOD'),getInfoType('PROMOTION_GRIFFON_BLOOD'),getInfoType('PROMOTION_LION_BLOOD'),getInfoType('PROMOTION_RAPTOR_BLOOD'),getInfoType('PROMOTION_SCORPION_BLOOD'),getInfoType('PROMOTION_SPIDER_BLOOD'),getInfoType('PROMOTION_STAG_BLOOD'),getInfoType('PROMOTION_TIGER_BLOOD'),getInfoType('PROMOTION_WOLF_BLOOD')]
	for iProm in range(gc.getNumPromotionInfos()):
		if pUnit.isHasPromotion(iProm):
			if iProm in BloodList:
				BloodList.remove(iProm) # Removing duplicate promotions
	if BloodList != []:
		iBlood		= BloodList[gc.getGame().getSorenRandNum(len(BloodList), "Pick Blood Promotion")]
		pUnit.setHasPromotion((iBlood),True)
	else:
		CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_NO_NEW_BLOOD", ()),'AS2D_GOODY_SETTLER',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		RndGold		= gc.getGame().getSorenRandNum(26, "Old Blood")
		pPlayer.changeGold(25+RndGold)
			
# GOODY_DEAL_WITH_IMP
def exploreDealWithImp(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	ElementalPromo		= [('PROMOTION_FIRE1', 1),('PROMOTION_ICE1', 1),('PROMOTION_WATER1', 1),('PROMOTION_EARTH1', 1),('PROMOTION_AIR1', 1)]
	NecromancyPromo		= [('PROMOTION_ENTROPY1', 1),('PROMOTION_DIMENSIONAL1', 1),('PROMOTION_DEATH1', 1),('PROMOTION_SHADOW1', 1),('PROMOTION_CHAOS1', 1)]
	GetElementalPromo	= wchoice( ElementalPromo, 'Roll Imp 1' ) 
	GetNecromancyPromo	= wchoice( NecromancyPromo, 'Roll Imp 2' ) 
	newUnit				= pPlayer.initUnit(getInfoType('UNIT_IMP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType(GetElementalPromo()),True)
	newUnit.setHasPromotion(getInfoType(GetNecromancyPromo()),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_HIGH_MAINTENANCE'),True)

# GOODY_SUCCUBUS_TRAP
def exploreSuccubusTrap(argsList):
	pUnit, pPlot		= argsList
	pNewPlot			= findClearPlot(-1, pPlot)
	pDemonPlayer		= gc.getPlayer(gc.getDEMON_PLAYER())
	newUnit1			= pDemonPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_COMMAND1'),True)
	newUnit2			= pDemonPlayer.initUnit(getInfoType('UNIT_SUCCUBUS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_COMMAND1'),True)
	if pUnit.isAlive() and not pUnit.isImmuneToCapture():
		pUnit.changeImmobileTimer(2)

# GOODY_ABANDONED_RITUAL
def exploreAbandonedRitual(argsList):
	pUnit, pPlot	= argsList
	iPlayer			= pUnit.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	git				= gc.getInfoTypeForString
	if pPlayer.isHuman():
		popupInfo = CyPopupInfo()
		popupInfo.setOption2(True)
		popupInfo.setFlags(126)
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("passToModNetMessage")
		popupInfo.setData1(iPlayer)
		popupInfo.setData3(110) # onModNetMessage id
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENTTRIGGER_ABANDONED_RITUAL", ()))
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_ABANDONED_RITUAL_1", ()),"EVENT_ABANDONED_RITUAL_1")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_ABANDONED_RITUAL_2", ()),"EVENT_ABANDONED_RITUAL_2")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_ABANDONED_RITUAL_3", ()),"EVENT_ABANDONED_RITUAL_3")
		popupInfo.addPopup(iPlayer)
	else:
		iAlignment	= pPlayer.getAlignment()
		if iAlignment == git("ALIGNMENT_EVIL"):
			pPlayer.changeGlobalCounterContrib(5)
			CyGame().changeGlobalCounter(5)
		elif iAlignment == git("ALIGNMENT_GOOD"):
			pPlayer.changeGlobalCounterContrib(-5)
			CyGame().changeGlobalCounter(-5)
		elif pPlayer.getEthicalAlignment() == git("ETHICAL_ALIGNMENT_CHAOTIC"):
			iChange = CyGame().getSorenRandNum(10, "AbandonedRitual Neutral Chaotic AI") - 5
			pPlayer.changeGlobalCounterContrib(iChange)
			CyGame().changeGlobalCounter(iChange)

# GOODY_COWARDLY_CULTIST
def exploreCowardlyCultist(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	NecromancyPromoList	= []
	NecromancyPromoList.append('PROMOTION_ENTROPY')
	NecromancyPromoList.append('PROMOTION_DEATH')
	NecromancyPromoList.append('PROMOTION_SHADOW')
	NecromancyPromoList.append('PROMOTION_CHAOS')
	szNecromancyPromo	= NecromancyPromoList[gc.getGame().getSorenRandNum(len(NecromancyPromoList), "Pick Cowardly Cultist Promotion")]
	CultistList			= []
	CultistList.append('UNIT_ILLUSIONIST')
	CultistList.append('UNIT_MAGE')
	CultistList.append('UNIT_MOBIUS_WITCH')
	CultistList.append('UNIT_NECROMANCER')
	CultistList.append('UNIT_SHAPER')
	CultistList.append('UNIT_WIZARD')
	iCultist			= CultistList[gc.getGame().getSorenRandNum(len(CultistList), "Pick Cowardly Cultist Unit")]
	newUnit				= pPlayer.initUnit(getInfoType(iCultist), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType(szNecromancyPromo + '1'),True)
	newUnit.setHasPromotion(getInfoType(szNecromancyPromo + '2'),True)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UNLOYAL'),True)
	newUnit.setDamage(50,-1)

# GOODY_SEALED_WELL
def exploreSealedWell(argsList):
	pUnit, pPlot		= argsList
	getPlot				= CyMap().plot
	pPlot.changePlotCounter(10 + CyGame().getSorenRandNum(70, "Could be a little evil, could be a lot of evil..."))

# GOODY_BURNED_LAIR
def reqBurnedLair(argsList):
	pUnit, pPlot		= argsList
	getPlot				= CyMap().plot
	ClearTreesCount		= 0
	for x, y in plotsInRange(pPlot.getX(),pPlot.getY(),1,0):
		iPlot			= getPlot(x,y)
		if iPlot.getFeatureType() == getInfoType("FEATURE_JUNGLE") or iPlot.getFeatureType() == getInfoType("FEATURE_FOREST"):
			if iPlot.getImprovementType() == -1:
				ClearTreesCount += 1
	if ClearTreesCount > 1:
		return True
	return False

def exploreBurnedLair(argsList):
	pUnit, pPlot		= argsList
	getPlot				= CyMap().plot
	for x, y in plotsInRange(pPlot.getX(),pPlot.getY(),1,0):
		iPlot			= getPlot(x,y)
		if iPlot.getFeatureType() == getInfoType("FEATURE_JUNGLE") or iPlot.getFeatureType() == getInfoType("FEATURE_FOREST"):
			if iPlot.getImprovementType() == -1:
				iPlot.setImprovementType(getInfoType('IMPROVEMENT_SMOKE'))

# GOODY_BOTTLE_OF_LIQUID_STONE
def exploreLiquidStone(argsList):
	pUnit, pPlot		= argsList
	pUnit.changeImmobileTimer(4)
	pUnit.setHasPromotion(getInfoType('PROMOTION_STONESKIN'),True)
	if pUnit.getUnitType() == getInfoType('UNIT_EARTH_ELEMENTAL'):
		pUnit.changeStrBoost(1)

# GOODY_NEW_CHIEFTAIN
def exploreNewChieftain(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	OrcPlayer			= gc.getPlayer(gc.getORC_PLAYER())
	newUnit				= pPlayer.initUnit(getInfoType('UNIT_AXEMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_ORC'),True)

# GOODY_UNIQUE_MAP
def reqUniqueMap(argsList):
	pUnit, pPlot		= argsList
	for i in range (CyMap().numPlots()):
		iPlot = CyMap().plotByIndex(i)
		if iPlot == -1 or iPlot.getImprovementType() == -1:
			continue
		if iPlot.isRevealed(pUnit.getTeam(), False):
			continue
		if gc.getImprovementInfo(iPlot.getImprovementType()).isUnique():
			return True
	return False

def exploreUniqueMap(argsList):
	pUnit, pPlot		= argsList
	getPlot				= CyMap().plot
	pTeam				= pUnit.getTeam()
	iNumPlots = CyMap().numPlots()
	iOffset = CyGame().getSorenRandNum(iNumPlots, "Starting plot for random UF search")
	for i in range (iOffset, iNumPlots):
		iPlot = CyMap().plotByIndex(i % iNumPlots)
		if iPlot == -1 or iPlot.getImprovementType() == -1:
			continue
		if iPlot.isRevealed(pTeam, False):
			continue
		if gc.getImprovementInfo(iPlot.getImprovementType()).isUnique():
			iPlot.setRevealed(pTeam, True, False, TeamTypes.NO_TEAM)
			for x, y in plotsInRange(iPlot.getX(),iPlot.getY(),1,1):
				jPlot	= getPlot(x,y)
				jPlot.setRevealed(pTeam, True, False, TeamTypes.NO_TEAM)
			for x, y in plotsInRange(iPlot.getX(),iPlot.getY(),2,2):
				jPlot	= getPlot(x,y)
				iRnd	= CyGame().getSorenRandNum(100, "Unique Map Lair Result")
				if iRnd > 64:
					jPlot.setRevealed(pTeam, True, False, TeamTypes.NO_TEAM)
			break

# GOODY_TWENTY_ONE_ARGUING_FIGURES
def exploreArguingFigures(argsList):
	pUnit, pPlot		= argsList
	PromotionList		= []
	PromotionList.append('PROMOTION_AIR1')
	PromotionList.append('PROMOTION_BODY1')
	PromotionList.append('PROMOTION_CHAOS1')
	PromotionList.append('PROMOTION_CREATION1')
	PromotionList.append('PROMOTION_DEATH1')
	PromotionList.append('PROMOTION_DIMENSIONAL1')
	PromotionList.append('PROMOTION_EARTH1')
	PromotionList.append('PROMOTION_ENCHANTMENT1')
	PromotionList.append('PROMOTION_ENTROPY1')
	PromotionList.append('PROMOTION_FIRE1')
	PromotionList.append('PROMOTION_FORCE1')
	PromotionList.append('PROMOTION_ICE1')
	PromotionList.append('PROMOTION_LAW1')
	PromotionList.append('PROMOTION_LIFE1')
	PromotionList.append('PROMOTION_METAMAGIC1')
	PromotionList.append('PROMOTION_MIND1')
	PromotionList.append('PROMOTION_NATURE1')
	PromotionList.append('PROMOTION_SHADOW1')
	PromotionList.append('PROMOTION_SPIRIT1')
	PromotionList.append('PROMOTION_SUN1')
	PromotionList.append('PROMOTION_WATER1')
	Tries				= 5 # rerolling promotion few times if pUnit already have that one
	listPromoBefore		= []
	listPromoAfter		= []
	for PromosBefore in range(gc.getNumPromotionInfos()):
		if pUnit.isHasPromotion(PromosBefore):
			listPromoBefore.append(PromosBefore)
	while Tries > 0:
		GetSphere = PromotionList[gc.getGame().getSorenRandNum(len(PromotionList), "21 Figures, Sphere")]
		pUnit.setHasPromotion(getInfoType(GetSphere),True)
		listPromoAfter = []
		for PromosAfter in range(gc.getNumPromotionInfos()):
			if pUnit.isHasPromotion(PromosAfter):
				listPromoAfter.append(PromosAfter)
		if listPromoBefore == listPromoAfter:
			Tries += -1
			continue
		else:
			break
	iRnd				= CyGame().getSorenRandNum(100, "21 Figures, Channeling")
	if listPromoBefore == listPromoAfter:
		iRnd = iRnd + 25 # If no new sphere added chances of getting channeling are better
	if pUnit.isHasPromotion(getInfoType('PROMOTION_CHANNELING1')) and iRnd > 74:
		pUnit.setHasPromotion(getInfoType('PROMOTION_CHANNELING2'),True)
	if iRnd > 89:
		pUnit.setHasPromotion(getInfoType('PROMOTION_CHANNELING1'),True)

# GOODY_MIRROR_OF_POSSIBILITY
def reqMirror1(argsList):
	pUnit, pPlot		= argsList
	if pUnit.isAlive() and pUnit.getExperienceTimes100() > 1000:
		return True
	return False


def exploreMirror1(argsList):
	pUnit, pPlot		= argsList
	BaseXP				= pUnit.getExperienceTimes100()
	ExtraXP				= BaseXP * 0.2
	ExtraXP				= int(ExtraXP)
	if ExtraXP > 4000:
		ExtraXP = 4000
	NewXP				= BaseXP + ExtraXP
	pUnit.setExperienceTimes100(NewXP, -1)

# GOODY_SWANMAY_GOOD
def reqSwanmayGood(argsList):
	pUnit, pPlot		= argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	if pPlayer.getAlignment() == getInfoType('ALIGNMENT_GOOD') and pUnit.isAlive() and pUnit.getExperienceTimes100() > 1000:
		return True
	return False

def exploreSwanmayGood(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	newUnit				= pPlayer.initUnit(getInfoType('UNIT_SWANMAY'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# GOODY_SWANMAY_EVIL
def reqSwanmayEvil(argsList):
	pUnit, pPlot		= argsList
	pPlayer = gc.getPlayer(pUnit.getOwner())
	if pPlayer.getAlignment() == getInfoType('ALIGNMENT_EVIL') and pUnit.isAlive() and pUnit.getExperienceTimes100() > 1000:
		return True
	return False

def exploreSwanmayEvil(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	pUnit.setHasPromotion(getInfoType("PROMOTION_SWANMAY_CLOAK"),True)
	
# GOODY_HORRORS_OF_FUTURE
def exploreMirror2(argsList):
	pUnit, pPlot		= argsList
	BaseXP				= pUnit.getExperienceTimes100()
	ExtraXP				= BaseXP * 0.2
	ExtraXP				= int(ExtraXP)
	if ExtraXP > 4000:
		ExtraXP = 4000
	NewXP				= BaseXP - ExtraXP
	pUnit.setExperienceTimes100(NewXP, -1)

# GOODY_MIRROR_MIRROR
def exploreMirror3(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	iPlayer				= pUnit.getOwner()
	qUnit				= pPlayer.initUnit(pUnit.getUnitType(), pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	iRnd				= CyGame().getSorenRandNum(3, "Mirror, Mirror")
	for iProm in range(gc.getNumPromotionInfos()):
		if (pUnit.isHasPromotion(iProm) and not gc.getPromotionInfo(iProm).isEquipment() and not gc.getPromotionInfo(iProm).isEffectProm()):
			iPromCount = pUnit.countHasPromotion(iProm)
			for i in xrange(iPromCount):
				qUnit.setHasPromotion(iProm, True)
	qUnit.setDamageReal(pUnit.getDamageReal(), pUnit.getOwner())
	qUnit.setLevel(pUnit.getLevel())
	qUnit.setExperienceTimes100(pUnit.getExperienceTimes100(), -1)
	if iRnd == 0: # Old (Less Strength)
		if pUnit.baseCombatStr() > 2:
			qUnit.changeStrBoost(-1)
		if pUnit.baseCombatStr() > 6:
			qUnit.changeStrBoost(-1)
		if pUnit.baseCombatStr() > 10:
			qUnit.changeStrBoost(-1)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_GOODY_MIRROR_MIRROR_OLD",()),'',3,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
	elif iRnd == 1: # Young (Less XP)
		OldXP = pUnit.getExperienceTimes100()
		NewXP = OldXP * 0.6
		NewXP = int(NewXP)
		qUnit.setExperienceTimes100(NewXP, -1)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_GOODY_MIRROR_MIRROR_YOUNG",()),'',3,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
	elif iRnd == 2: # Different Race
		for iProm in range(gc.getNumPromotionInfos()):
			if (pUnit.isHasPromotion(iProm) and gc.getPromotionInfo(iProm).isRace()):
				qUnit.setHasPromotion(iProm, False)
		iRaceNumber = CyGame().getSorenRandNum(len(IRacial), "Race Number")
		iRace = IRacial[iRaceNumber]
		qUnit.setHasPromotion(iRace, True)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_GOODY_MIRROR_MIRROR_DIFFERENT",()),'',3,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
	if getInfoType("MODULE_NOGGORMOTHA") != -1:
		if pUnit.getUnitType() == getInfoType("UNIT_KEEPER"):
			setKeeperLevel(qUnit,getKeeperLevel(qUnit))
# GOODY_CAVE_IN
def exploreCaveIn(argsList):
	pUnit, pPlot		= argsList
	pUnit.changeImmobileTimer(3)

# GOODY_EARTHQUAKE
def reqLairEarthquake(argsList):
	pUnit, pPlot		= argsList
	getPlot				= CyMap().plot
	for x, y in plotsInRange(pPlot.getX(),pPlot.getY(),1,0):
		iPlot = getPlot(x,y)
		if iPlot.getImprovementType() != -1:
			if gc.getImprovementInfo(iPlot.getImprovementType()).isUnique():
				return False
	return True

def exploreEarthquake(argsList):
	pUnit, pPlot		= argsList
	getPlot				= CyMap().plot
	for x, y in plotsInRange(pPlot.getX(),pPlot.getY(),1,0):
		iPlot = getPlot(x,y)
		if iPlot.getImprovementType() != -1:
			iPlot.setImprovementType(-1)
		if iPlot.isPeak():
			iPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
		if iPlot.isFlatlands() :
			iRnd = CyGame().getSorenRandNum(100, "Goody Earthquake")
			if iRnd > 49:
				iPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)

# GOODY_STOLEN_SUPPLIES
def exploreStolenSupplies(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	newUnit				= pPlayer.initUnit(getInfoType('UNIT_SUPPLIES'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# GOODY_SLAVERS
def exploreSlavers(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	infoCiv 	= gc.getCivilizationInfo(pPlayer.getCivilizationType())
	if pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_DTESH'):
		newUnit1		= pPlayer.initUnit(getInfoType('UNIT_SLAVE_UNDEAD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2		= pPlayer.initUnit(getInfoType('UNIT_SLAVE_UNDEAD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	if pPlayer.getCivics(getInfoType('CIVICOPTION_LABOR')) == getInfoType('CIVIC_SLAVERY') and pPlayer.getCivilizationType() != getInfoType('CIVILIZATION_DTESH'):
		newUnit1		= pPlayer.initUnit(getInfoType('UNIT_SLAVE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2		= pPlayer.initUnit(getInfoType('UNIT_SLAVE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit3		= pPlayer.initUnit(getInfoType('UNIT_SLAVE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	if pPlayer.getCivics(getInfoType('CIVICOPTION_LABOR')) != getInfoType('CIVIC_SLAVERY') and pPlayer.getCivilizationType() != getInfoType('CIVILIZATION_DTESH'):
		iRnd			= CyGame().getSorenRandNum(100, "Goody Slavers")
		iUnit			= infoCiv.getCivilizationUnits(getInfoType('UNITCLASS_SETTLER'))
		jUnit			= infoCiv.getCivilizationUnits(getInfoType('UNITCLASS_WORKER'))
		if iRnd > 84 and iUnit != -1:
			newUnit		= pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		elif jUnit != -1:
			newUnit1	= pPlayer.initUnit(jUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit2	= pPlayer.initUnit(jUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		else:
			newUnit1	= pPlayer.initUnit(getInfoType('UNIT_SLAVE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit2	= pPlayer.initUnit(getInfoType('UNIT_SLAVE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# GOODY_ENCHANTED_MAP
def reqEnchantedMap(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	if pPlayer.isHasTech(getInfoType('TECH_OMNISCIENCE')):
		return False
	return True

def exploreEnchantedMap(argsList):
	pUnit, pPlot		= argsList
	getPlot				= CyMap().plot
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	pTeam 				= pPlayer.getTeam()
	for i in range (CyMap().numPlots()):
		iPlot = CyMap().plotByIndex(i)
		if iPlot.getRouteType() == getInfoType('ROUTE_ROAD'):
			iPlot.setRevealed(pTeam, True, False, TeamTypes.NO_TEAM)

# GOODY_THE_OUTRUNEREST
def exploreTheOutrunerest(argsList):
	pUnit, pPlot		= argsList
	pOrcPlayer			= gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot			= findClearPlot(-1, pPlot)
	newUnit1			= pOrcPlayer.initUnit(getInfoType('UNIT_CENTAUR_OUTRUNNER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_MOBILITY1'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_MOBILITY2'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_FAST_HORSES_MOUNTED'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_LIGHT'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_UNSTOPPABLE'),True)
	newUnit2			= pOrcPlayer.initUnit(getInfoType('UNIT_CENTAUR_OUTRUNNER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_MOBILITY1'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_MOBILITY2'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_FAST_HORSES_MOUNTED'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_LIGHT'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_UNSTOPPABLE'),True)

# GOODY_EVASIVE_CENTAURS
def exploreEvasiveCentaurs(argsList):
	pUnit, pPlot		= argsList
	pOrcPlayer			= gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot			= findClearPlot(-1, pPlot)
	newUnit1			= pOrcPlayer.initUnit(getInfoType('UNIT_CENTAUR_CLANCHIEF'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_FLANKING1'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_FLANKING2'),True)
	newUnit2			= pOrcPlayer.initUnit(getInfoType('UNIT_CENTAUR_MARAUDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_FLANKING1'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_FLANKING2'),True)
	newUnit3			= pOrcPlayer.initUnit(getInfoType('UNIT_CENTAUR_MARAUDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_FLANKING1'),True)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_FLANKING2'),True)

# GOODY_DEAL_WITH_CENTAURS_TRIBE
def reqDealwithTribe(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	if pPlayer.isHasFlag(getInfoType("FLAG_DEAL_WITH_CENTAURS_TRIBE")):
		return False
	return True

def exploreDealwithTribe(argsList):
	pUnit, pPlot	= argsList
	iPlayer			= pUnit.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	git				= gc.getInfoTypeForString
	lReqBonus = [git("BONUS_COW"),git("BONUS_DEER"),git("BONUS_PIG"),git("BONUS_DEER_ARCTIC"),git("BONUS_BANANA"),git("BONUS_RICE"),git("BONUS_WHEAT"),git("BONUS_WINE"),git("BONUS_CORN")]
	bOption2		= False
	pCapital		= pPlayer.getCapitalCity()
	for i in range (CyMap().numPlots()):
		iPlot = CyMap().plotByIndex(i)
		if iPlot.getBonusType(-1) in lReqBonus and iPlot.getOwner() == iPlayer:
			bOption2 = True
	if pPlayer.isHuman():
		popupInfo = CyPopupInfo()
		popupInfo.setOption2(True)
		popupInfo.setFlags(126)
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("passToModNetMessage")
		popupInfo.setData1(iPlayer)
		popupInfo.setData3(111) # onModNetMessage id
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENTTRIGGER_DEAL_WITH_CENTAURS_TRIBE", ()))
		if pPlayer.getGold() >= 350:
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_DEAL_WITH_CENTAURS_TRIBE_1", ()),"EVENT_DEAL_WITH_CENTAURS_TRIBE_1")
		if bOption2 == True:
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_DEAL_WITH_CENTAURS_TRIBE_2", ()),"EVENT_DEAL_WITH_CENTAURS_TRIBE_2")
		if pPlayer.getCivilizationType() == git("CIVILIZATION_KURIOTATES") and pCapital != -1:
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_DEAL_WITH_CENTAURS_TRIBE_3", ()),"EVENT_DEAL_WITH_CENTAURS_TRIBE_3")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_DEAL_WITH_CENTAURS_TRIBE_4", ()),"EVENT_DEAL_WITH_CENTAURS_TRIBE_4")
		popupInfo.addPopup(iPlayer)
	else:
		AIPick = 3
		if pPlayer.getCivilizationType() == git("CIVILIZATION_KURIOTATES") and pCapital != -1:
			AIPick = 2
		elif pPlayer.getGold() >= 350:
			AIPick = 0
		elif bOption2 == True:
			AIPick = 1
		argsList = [AIPick,iPlayer]
		effectDealwithTribe(argsList)

def effectDealwithTribe(argsList):
	iButtonId	= argsList[0]
	iPlayer		= argsList[1]
	pPlayer		= gc.getPlayer(iPlayer)
	git			= gc.getInfoTypeForString
	bOption2	= False
	pCapital	= pPlayer.getCapitalCity()
	lReqBonus = [git("BONUS_COW"),git("BONUS_DEER"),git("BONUS_PIG"),git("BONUS_DEER_ARCTIC"),git("BONUS_BANANA"),git("BONUS_RICE"),git("BONUS_WHEAT"),git("BONUS_WINE"),git("BONUS_CORN")]
	for i in range (CyMap().numPlots()):
		iPlot = CyMap().plotByIndex(i)
		if iPlot.getBonusType(-1) in lReqBonus and iPlot.getOwner() == iPlayer:
			bOption2 = True
	if pPlayer.getGold() < 350 and iButtonId >= 0: # I don't know how else to simulate option shift caused by reqs in popup
		iButtonId += 1
	if bOption2 != True and iButtonId >= 1: # Option shift
		iButtonId += 1
	if pPlayer.getCivilizationType() != git("CIVILIZATION_KURIOTATES") or pCapital == -1 or pCapital.isNone(): # Option shift
		if iButtonId >= 2:
			iButtonId += 1
	if iButtonId == 3:
		return
	if iButtonId == 0:
		pPlayer.changeGold(-350)
	if iButtonId == 1:
		iRemovedBonus = 0
		for i in range (CyMap().numPlots()):
			if iRemovedBonus == 0:
				iPlot = CyMap().plotByIndex(i)
				if iPlot.getBonusType(-1) in lReqBonus and iPlot.getOwner() == iPlayer:
					iPlot.setBonusType(-1)
					iRemovedBonus += 1
	if iButtonId == 2:
		pCapital = pPlayer.getCapitalCity()
		pCapital.changePopulation(1)
	pPlayer.setHasFlag(git('FLAG_DEAL_WITH_CENTAURS_TRIBE'), True)
	# TODO Remove comment when setFreePromotion is exposed to python
	# pPlayer.setFreePromotion(git("UNITCOMBAT_MOUNTED"),git("PROMOTION_SHOCK"),true)

# GOODY_AGARES_WORSHIPERS
def exploreAgaresWorshipers(argsList):
	pUnit, pPlot		= argsList
	pNewPlot			= findClearPlot(-1, pPlot)
	pDemonPlayer		= gc.getPlayer(gc.getDEMON_PLAYER())
	newUnit1			= pDemonPlayer.initUnit(getInfoType('UNIT_CENTAUR_CLANCHIEF'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_DEMON'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_NIGHTMARE'),True)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_FEAR'),True)
	newUnit1.changeStrBoost(1)
	newUnit2			= pDemonPlayer.initUnit(getInfoType('UNIT_CENTAUR_MARAUDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_DEMON'),True)
	newUnit2.setHasPromotion(getInfoType('PROMOTION_NIGHTMARE'),True)
	newUnit2.changeStrBoost(1)
	newUnit3			= pDemonPlayer.initUnit(getInfoType('UNIT_CENTAUR_MARAUDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_DEMON'),True)
	newUnit3.setHasPromotion(getInfoType('PROMOTION_NIGHTMARE'),True)
	newUnit3.changeStrBoost(1)
	newUnit4			= pDemonPlayer.initUnit(getInfoType('UNIT_CENTAUR_OUTRUNNER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit4.setHasPromotion(getInfoType('PROMOTION_DEMON'),True)
	newUnit4.setHasPromotion(getInfoType('PROMOTION_NIGHTMARE'),True)
	newUnit4.changeStrBoost(1)
	newUnit5			= pDemonPlayer.initUnit(getInfoType('UNIT_CENTAUR_OUTRUNNER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit5.setHasPromotion(getInfoType('PROMOTION_DEMON'),True)
	newUnit5.setHasPromotion(getInfoType('PROMOTION_NIGHTMARE'),True)
	newUnit5.changeStrBoost(1)
	iRnd				= CyGame().getSorenRandNum(100, "Agares Worshipers Strength")
	if iRnd > 24:
		newUnit1.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)
		newUnit2.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)
		newUnit3.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)
		newUnit4.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)
		newUnit5.setHasPromotion(getInfoType('PROMOTION_COMBAT1'),True)
	if iRnd > 49:
		newUnit1.setHasPromotion(getInfoType('PROMOTION_COMBAT2'),True)
		newUnit2.setHasPromotion(getInfoType('PROMOTION_COMBAT2'),True)
		newUnit3.setHasPromotion(getInfoType('PROMOTION_COMBAT2'),True)
		newUnit4.setHasPromotion(getInfoType('PROMOTION_COMBAT2'),True)
		newUnit5.setHasPromotion(getInfoType('PROMOTION_COMBAT2'),True)
	if iRnd > 74:
		newUnit1.changeStrBoost(1)
		newUnit2.changeStrBoost(1)
		newUnit3.changeStrBoost(1)
		newUnit4.changeStrBoost(1)
		newUnit5.changeStrBoost(1)

# GOODY_PET_ROC
def explorePetRoc(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	newUnit				= pPlayer.initUnit(getInfoType('UNIT_ROC'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

# GOODY_LIZARDMEN_BOOZE
def exploreLizardmenBooze(argsList):
	pUnit, pPlot		= argsList
	if not pUnit.isHasPromotion(getInfoType('PROMOTION_IMMUNE_DISEASE')) or pUnit.isHasPromotion(getInfoType('PROMOTION_LIZARDMAN')):
		pUnit.doDamage(20, 100, pUnit, getInfoType('DAMAGE_POISON'), False)

# GOODY_HIDDEN_RUINS
def reqHiddenRuins(argsList):
	pUnit, pPlot		= argsList
	getPlot				= CyMap().plot
	ClearJungleCount	= 0
	for x, y in plotsInRange(pPlot.getX(),pPlot.getY(),1,1):
		iPlot = getPlot(x,y)
		if iPlot.getFeatureType() == getInfoType("FEATURE_JUNGLE"):
			if iPlot.getImprovementType() == -1:
				ClearJungleCount += 1
	if ClearJungleCount > 0:
		return True
	return False

def exploreHiddenRuins(argsList):
	pUnit, pPlot		= argsList
	getPlot				= CyMap().plot
	RuinCap				= 2
	ExtraRandomRuins	= CyGame().getSorenRandNum(3, "Extra Ruins")
	RuinCap				= RuinCap + ExtraRandomRuins
	FarmCap				= 2
	if pPlot.getRouteType()	== -1:
		pPlot.setRouteType(getInfoType('ROUTE_TRAIL'))
	RuinType = [('IMPROVEMENT_RUINS',10),('IMPROVEMENT_RUINS_SPRAWLING',3),('IMPROVEMENT_RUINS_COLOSSAL',1)]
	for x, y in plotsInRange(pPlot.getX(),pPlot.getY(),1,1):
		iPlot = getPlot(x,y)
		if iPlot.getFeatureType() == getInfoType("FEATURE_JUNGLE"):
			if iPlot.getImprovementType() == -1:
				GetRuinType = wchoice(RuinType,'Roll Ruin Type')
				iPlot.setImprovementType(getInfoType(GetRuinType()))
				if iPlot.getRouteType()	== -1:
					iPlot.setRouteType(getInfoType('ROUTE_TRAIL'))
				RuinCap += - 1
				if RuinCap == 0:
					break
	for x, y in plotsInRange(pPlot.getX(),pPlot.getY(),1,1):
		iPlot = getPlot(x,y)
		if iPlot.getImprovementType() == -1 and not iPlot.isPeak():
			iPlot.setImprovementType(getInfoType('IMPROVEMENT_FARM'))
			if iPlot.getRouteType()	== -1:
				iPlot.setRouteType(getInfoType('ROUTE_TRAIL'))
			FarmCap += - 1
			if FarmCap == 0:
				break

# GOODY_CITY_OF_GOLD
def exploreCityOfGold(argsList):
	pUnit, pPlot	= argsList
	iPlayer			= pUnit.getOwner()
	pPlayer			= gc.getPlayer(iPlayer)
	git				= gc.getInfoTypeForString
	iUnit			= pUnit.getID()
	if pPlayer.isHuman():
		popupInfo = CyPopupInfo()
		popupInfo.setOption2(True)
		popupInfo.setFlags(126)
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setOnClickedPythonCallback("passToModNetMessage")
		popupInfo.setData1(iPlayer)
		popupInfo.setData2(iUnit)
		popupInfo.setData3(112) # onModNetMessage id
		popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENTTRIGGER_CITY_OF_GOLD", ()))
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CITY_OF_GOLD_1", ()),"EVENT_CITY_OF_GOLD_1")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CITY_OF_GOLD_2", ()),"EVENT_CITY_OF_GOLD_2")
		if pPlayer.getCivilizationType() == git('CIVILIZATION_MAZATL') or pPlayer.getCivilizationType() ==  git('CIVILIZATION_CUALLI'):
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CITY_OF_GOLD_3", ()),"EVENT_CITY_OF_GOLD_3")
		popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CITY_OF_GOLD_4", ()),"EVENT_CITY_OF_GOLD_4")
		popupInfo.addPopup(iPlayer)
	else:
		if pPlayer.getCivilizationType() == git('CIVILIZATION_MAZATL') or pPlayer.getCivilizationType() ==  git('CIVILIZATION_CUALLI'):
			AIPick = 2
		else:
			AIPick = CyGame().getSorenRandNum(3, "CityOfGold AI pick")
			if AIPick == 2:
				AIPick = 3
		argsList = [AIPick,iPlayer,iUnit]
		effectCityOfGold(argsList)

def effectCityOfGold(argsList):
	iButtonId	= argsList[0]
	iPlayer		= argsList[1]
	iUnit		= argsList[2]
	pPlayer		= gc.getPlayer(iPlayer)
	pUnit		= pPlayer.getUnit(iUnit)
	git			= gc.getInfoTypeForString
	pPlot		= pUnit.plot()
	if pPlayer.getCivilizationType() != git('CIVILIZATION_MAZATL') and pPlayer.getCivilizationType() !=  git('CIVILIZATION_CUALLI') and iButtonId >= 2: # I don't know how else to simulate option shift caused by reqs in popup
		iButtonId += 1
	if iButtonId == 3:
		return
	iGold = 250 + CyGame().getSorenRandNum(100, "CityOfGold Gold")
	if iButtonId == 2:
		pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())
		pPlayer.changeGold(iGold)
		return
	if iButtonId == 0:
		pPlayer.changeGold(iGold)
	iRnd = CyGame().getSorenRandNum(100, "CityOfGold Guards")
	if iButtonId == 1 or iRnd < 34: # Spawn Guards
		pOrcPlayer	= gc.getPlayer(gc.getORC_PLAYER())
		pNewPlot	= findClearPlot(-1, pPlot)
		newUnit1		= pOrcPlayer.initUnit(git('UNIT_LIZARD_PRIEST_OF_AGRUONN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(git('PROMOTION_COMBAT1'),True)
		newUnit1.setHasPromotion(git('PROMOTION_COMBAT2'),True)
		newUnit2		= pOrcPlayer.initUnit(git('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
		newUnit2.setHasPromotion(git('PROMOTION_COMBAT1'),True)
		newUnit3		= pOrcPlayer.initUnit(git('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
		newUnit3.setHasPromotion(git('PROMOTION_COMBAT1'),True)
		if iButtonId == 1:
			pUnit.changeImmobileTimer(3)
			pUnit.setHasPromotion(git('PROMOTION_PILLAGED_GOLD'),True)

# GOODY_SACELLUM
def exploreSacellum(argsList):
	pUnit, pPlot		= argsList
	iPlayer				= pUnit.getOwner()
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	iRndConflict		= CyGame().getSorenRandNum(100, "Sacellum, Chance to avoid conflict")
	iRndType			= CyGame().getSorenRandNum(2, "Sacellum, Group Type") # 0 - Kalshekk group, 1 - Omorr group
	if iRndConflict > 49 and pPlayer.getCivilizationType() != getInfoType('CIVILIZATION_MAZATL'): # Mazatl Have 50% chance to avoid conflict
		if iRndType == 0:
			if iRndConflict > 49 and pPlayer.getStateReligion() != getInfoType('RELIGION_RUNES_OF_KILMORPH'): # Player Have 50% chance to avoid conflict if matching religion with spawned group
				pOrcPlayer	= gc.getPlayer(gc.getORC_PLAYER())
				pNewPlot	= findClearPlot(-1, pPlot)
				newUnit1	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_HIGH_PRIEST_OF_KALSHEKK'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit2	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_DISCIPLE_OF_KALSHEKK'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit3	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_DISCIPLE_OF_KALSHEKK'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit4	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit5	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			else:
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_GOODY_GOODY_SACELLUM_AVOIDED",()),'',3,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		if iRndType == 1:
			if iRndConflict > 49 and pPlayer.getStateReligion() != getInfoType('RELIGION_THE_EMPYREAN'): # Player Have 50% chance to avoid conflict if matching religion with spawned group
				pOrcPlayer	= gc.getPlayer(gc.getORC_PLAYER())
				pNewPlot	= findClearPlot(-1, pPlot)
				newUnit1	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_HIGH_PRIEST_OF_OMORR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit2	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_DISCIPLE_OF_OMORR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit3	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_DISCIPLE_OF_OMORR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit4	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit5	= pOrcPlayer.initUnit(getInfoType('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			else:
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_GOODY_GOODY_SACELLUM_AVOIDED",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
	else:
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_GOODY_GOODY_SACELLUM_AVOIDED",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)

# GOODY_FLARE_OF_ARCANE_ENERGY
def reqArcaneFlare(argsList):
	pUnit, pPlot		= argsList
	iPlayer				= pUnit.getOwner()
	for i in range (CyMap().numPlots()):
		iPlot = CyMap().plotByIndex(i)
		if iPlot.getBonusType(-1) != -1 and iPlot.getOwner() == iPlayer:
			if gc.getBonusInfo(iPlot.getBonusType(-1)).getBonusClassType() == getInfoType('BONUSCLASS_MANA'):
				if iPlot.getImprovementType() == -1:
					return True
				else:
					if gc.getImprovementInfo(iPlot.getImprovementType()).isUnique() == False:
						return True
	return False

def exploreArcaneFlare(argsList):
	pUnit, pPlot		= argsList
	iPlayer				= pUnit.getOwner()
	iRnd				= CyGame().getSorenRandNum(3, "Arcane Flare, Extra Dispel")
	NodesDispeled		= 1 + iRnd
	for i in range (CyMap().numPlots()):
		iPlot = CyMap().plotByIndex(i)
		if iPlot.getBonusType(-1) != -1 and iPlot.getOwner() == iPlayer:
			if gc.getBonusInfo(iPlot.getBonusType(-1)).getBonusClassType() == getInfoType('BONUSCLASS_MANA'):
				if iPlot.getImprovementType() == -1:
					iPlot.setBonusType(getInfoType('BONUS_MANA'))
					NodesDispeled += -1
					if NodesDispeled == 0:
						break
				else:
					if gc.getImprovementInfo(iPlot.getImprovementType()).isUnique() == False:
						iPlot.setBonusType(getInfoType('BONUS_MANA'))
						iPlot.setImprovementType(-1)
						NodesDispeled += -1
						if NodesDispeled == 0:
							break

# GOODY_TRADE_SHIP
def exploreTradeShip(argsList):
	pUnit, pPlot		= argsList
	pPlayer				= gc.getPlayer(pUnit.getOwner())
	newUnit				= pPlayer.initUnit(getInfoType('UNIT_TRADESHIP'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	
def exploreKelp(argsList):
	pUnit, pPlot		= argsList
	for x, y in plotsInRange(pPlot.getX(),pPlot.getY(),1,1):
		iPlot = CyMap().plot(x,y)
		iPlot.setFeatureType(getInfoType("FEATURE_KELP"),0)
	
def exploreKelpReagents(argsList):
	pUnit, pPlot		= argsList
	pPlot.setFeatureType(getInfoType("FEATURE_KELP"),0)
	
	
def reqBuyMount(caster,promotion):
	if caster.getUnitCombatType()!=getInfoType("UNITCOMBAT_MOUNTED") and not caster.isSecondaryUnitCombat(getInfoType("UNITCOMBAT_MOUNTED")):
		return False
	if caster.isHasPromotion(getInfoType(promotion)):
		return False
	if promotion=="PROMOTION_CAMEL" and gc.getPlayer(caster.getOwner()).getCivilizationType()!=getInfoType("CIVILIZATION_MALAKIM"):
		return False
	if not (gc.getUnitInfo(caster.getUnitType()).getPrereqOrBonuses(0)==getInfoType("BONUS_HORSE")):
		return False
	if (gc.getUnitInfo(caster.getUnitType()).getPrereqOrBonuses(0)==getInfoType("BONUS_HORSE")) and not promotion in ["PROMOTION_HORSE","PROMOTION_NIGHTMARE","PROMOTION_HYAPON","PROMOTION_CAMEL"]:
		return False
	if promotion=="PROMOTION_HORSE" and not gc.getPlayer(caster.getOwner()).hasBonus(getInfoType("BONUS_HORSE")):
		return False
	if promotion=="PROMOTION_HYAPON" and not gc.getPlayer(caster.getOwner()).hasBonus(getInfoType("BONUS_HYAPON")):
		return False		
	if promotion=="PROMOTION_NIGHTMARE" and not gc.getPlayer(caster.getOwner()).hasBonus(getInfoType("BONUS_NIGHTMARE")):
		return False
	if promotion=="PROMOTION_CAMEL" and not gc.getPlayer(caster.getOwner()).hasBonus(getInfoType("BONUS_CAMEL")):
		return False

	if  not gc.getPlayer(caster.getOwner()).isHuman() and gc.getPlayer(caster.getOwner()).getGold()<1000:
		return False
	return True
	
def reqChangeForm(caster):
	return caster.isAlive() and not( caster.getUnitCombatType()==getInfoType("UNITCOMBAT_MOUNTED") or  caster.getUnitCombatType()==getInfoType("UNITCOMBAT_ANIMAL") or caster.getUnitCombatType()==getInfoType("UNITCOMBAT_BEAST"))
	
def spellChangeForm(caster):
	hasform = False
	for iProm in ["PROMOTION_TIGER_FORM","PROMOTION_SPIDER_FORM","PROMOTION_MAMMOTH_FORM","PROMOTION_GRIFFON_FORM","PROMOTION_GORILLA_FORM","PROMOTION_TORTOISE_FORM","PROMOTION_SCORPION_FORM","PROMOTION_STAG_FORM","PROMOTION_ELEPHANT_FORM","PROMOTION_BOAR_FORM","PROMOTION_DRAKE_FORM","PROMOTION_BEAR_FORM","PROMOTION_RAPTOR_FORM","PROMOTION_WOLF_FORM","PROMOTION_LION_FORM","PROMOTION_SWAN_FORM"]:
		if caster.isHasPromotion(getInfoType(iProm)):
			hasform=True
			caster.setHasPromotion(getInfoType(iProm),False)
	
	if not hasform:
		if caster.getUnitType()==getInfoType("UNIT_SWANMAY"):
			caster.setHasPromotion(getInfoType("PROMOTION_SWAN_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_MELEE") and gc.getUnitInfo((caster.getUnitType())).getTier()<3:
			caster.setHasPromotion(getInfoType("PROMOTION_LION_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_MELEE") and gc.getUnitInfo((caster.getUnitType())).getTier()>2:
			caster.setHasPromotion(getInfoType("PROMOTION_BEAR_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_DEFENSIVE_MELEE") and gc.getUnitInfo((caster.getUnitType())).getTier()<3:
			caster.setHasPromotion(getInfoType("PROMOTION_BOAR_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_DEFENSIVE_MELEE") and gc.getUnitInfo((caster.getUnitType())).getTier()>2:
			caster.setHasPromotion(getInfoType("PROMOTION_ELEPHANT_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_RECON") and gc.getUnitInfo((caster.getUnitType())).getTier()<3:
			caster.setHasPromotion(getInfoType("PROMOTION_WOLF_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_RECON") and gc.getUnitInfo((caster.getUnitType())).getTier()>2:
			caster.setHasPromotion(getInfoType("PROMOTION_GRIFFON_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_ROGUE") and gc.getUnitInfo((caster.getUnitType())).getTier()<3:
			caster.setHasPromotion(getInfoType("PROMOTION_SPIDER_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_ROGUE") and gc.getUnitInfo((caster.getUnitType())).getTier()>2:
			caster.setHasPromotion(getInfoType("PROMOTION_RAPTOR_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_ARCHER") and gc.getUnitInfo((caster.getUnitType())).getTier()<3:
			caster.setHasPromotion(getInfoType("PROMOTION_SCORPION_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_ARCHER") and gc.getUnitInfo((caster.getUnitType())).getTier()>2:
			caster.setHasPromotion(getInfoType("PROMOTION_GORILLA_FORM"),True)
		elif caster.getUnitCombatType()==getInfoType("UNITCOMBAT_ADEPT") or caster.getUnitCombatType()==getInfoType("UNITCOMBAT_DISCIPLE"):
			caster.setHasPromotion(getInfoType("PROMOTION_DRAKE_FORM"),True)
	return
# Master Buildings Help
def helpMasterBuildings (argsList):
	eBuilding, pCity = argsList
	if pCity == -1 or pCity.isNone():
		szHelp 			= ""
	else:
		szHelp 			= ""
		pPlayer			= gc.getPlayer(pCity.getOwner())
		git				= gc.getInfoTypeForString
		iMaster			= eBuilding
		iNumTechCount	= 0
		iNumBonusCount	= 0
		iNumBuildCount	= 0
		lPromo			= [] # List of promotions tied to master building
		lPromoCiv		= [] # Promotions that are locked behind non pPlayer Civ are discarded
		lPromoTech		= [] # Discarded by missing tech
		lPromoBonus		= [] # Discarded by missing bonus
		lPromoBuilding	= [] # Discarded by missing building
		lPromoReligion	= [] # Discarded by missing State Rel
		lNoTech			= [] # List of all tech that pPlayer is missing that would add extra promotions
		lCompareTech	= [] # list to check tech that pPlayer is missing but can't ever research
		lNoBonus		= [] # list of all bonuses that pPlayer is missing that would add extra promotions
		lNoBuilding		= [] # list of all buildings that pPlayer is missing that would add extra promotions
		lNoRel			= [] # list of all religion that pPlayer can adopt that would add extra promotions
		# Check start
		for iPromotion in range(gc.getNumPromotionInfos()): # Checking all promotions
			for iBuildingOR in range(gc.getPromotionInfo(iPromotion).getNumPrereqBuildingORs()):
				if iMaster == gc.getPromotionInfo(iPromotion).getPrereqBuildingOR(iBuildingOR):
					lPromo.append(iPromotion) # Adding all that using Master Smith as PrereqBuildingOR
			for iBuildingAND in range(gc.getPromotionInfo(iPromotion).getNumPrereqBuildingANDs()):
				if iMaster == gc.getPromotionInfo(iPromotion).getPrereqBuildingAND(iBuildingAND):
					lPromo.append(iPromotion) # Adding all that using Master Smith as PrereqBuildingAND
		for iPromo in lPromo: # Discarding all Civ-locked promotions
			if gc.getPromotionInfo(iPromo).getNumPrereqCivilizations() > 0:
				for iCiv in range(gc.getPromotionInfo(iPromo).getNumPrereqCivilizations()):
					if pPlayer.getCivilizationType() == gc.getPromotionInfo(iPromo).getPrereqCivilization(iCiv):
						lPromoCiv.append(iPromo)
			else:
				lPromoCiv.append(iPromo)
		for iPromoCiv in lPromoCiv: # Checking tech prereq
			iNumTechCount = gc.getPromotionInfo(iPromoCiv).getNumPrereqTechANDs() # Counting all AND techs
			if gc.getPromotionInfo(iPromoCiv).getTechPrereq() > -1:
				iNumTechCount += 1 # TechPrereq is AND too
				if pPlayer.isHasTech(gc.getPromotionInfo(iPromoCiv).getTechPrereq()):
					iNumTechCount += - 1 # pPlayer has Tech, checking next
				elif pPlayer.canEverResearch(gc.getPromotionInfo(iPromoCiv).getTechPrereq()):
					lCompareTech.append(gc.getPromotionInfo(iPromoCiv).getTechPrereq()) # pPlayer doesn't have tech, but it's possible to research
			for iTechAND in range(gc.getPromotionInfo(iPromoCiv).getNumPrereqTechANDs()):
				if pPlayer.isHasTech(gc.getPromotionInfo(iPromoCiv).getPrereqTechAND(iTechAND)):
					iNumTechCount += -1 # pPlayer has Tech, checking next
				elif pPlayer.canEverResearch(gc.getPromotionInfo(iPromoCiv).getPrereqTechAND(iTechAND)):
					lCompareTech.append(gc.getPromotionInfo(iPromoCiv).getPrereqTechAND(iTechAND)) # pPlayer doesn't have tech, but it's possible to research
			if iNumTechCount == 0 and gc.getPromotionInfo(iPromoCiv).getNumPrereqTechORs() == 0: # pPlayer has all AND techs and there are no OR tech
				lPromoTech.append(iPromoCiv)
			elif iNumTechCount > 0:
				if len(lCompareTech) == iNumTechCount: # pPlayer can research all missing tech
					for iTech in lCompareTech:
						if not iTech in lNoTech: # Avoiding duplicates, missing tech could already be in
							lNoTech.append(iTech)
			elif gc.getPromotionInfo(iPromoCiv).getNumPrereqTechORs() > 0:
				for iTechOR in range(gc.getPromotionInfo(iPromoCiv).getNumPrereqTechORs()):
					if pPlayer.isHasTech(gc.getPromotionInfo(iPromoCiv).getPrereqTechOR(iTechOR)):
						if not iPromoCiv in lPromoTech: # Avoiding duplicates, if multiple ORs are already researched
							lPromoTech += [iPromoCiv]
							break
					elif pPlayer.canEverResearch(gc.getPromotionInfo(iPromoCiv).getPrereqTechOR(iTechOR)):
						if not iPromoCiv in lPromoTech: # if none of ORs are researched
							lNoTech += [gc.getPromotionInfo(iPromoCiv).getPrereqTechOR(iTechOR)]
			lCompareTech = [] # Reseting List
		for iPromoTech in lPromoTech: # Checking Bonus prereq
			iNumBonusCount = gc.getPromotionInfo(iPromoTech).getNumPrereqBonusANDs()
			for iBonusAND in range(gc.getPromotionInfo(iPromoTech).getNumPrereqBonusANDs()):
				if pCity.hasBonus(gc.getPromotionInfo(iPromoTech).getPrereqBonusAND(iBonusAND)):
					iNumBonusCount += -1 # pPlayer has bonus, checking next
				elif not gc.getPromotionInfo(iPromoTech).getPrereqBonusAND(iBonusAND) in lNoBonus: # Avoiding duplicates, missing bonus could already be in
					lNoBonus.append(gc.getPromotionInfo(iPromoTech).getPrereqBonusAND(iBonusAND))
			if iNumBonusCount == 0 and gc.getPromotionInfo(iPromoTech).getNumPrereqBonusORs() == 0: # pPlayer has all AND bonuses and there are no OR bonuses
				lPromoBonus.append(iPromoTech)
			elif iNumBonusCount == 0 and gc.getPromotionInfo(iPromoTech).getNumPrereqBonusORs() > 0:
				for iBonusOR in range(gc.getPromotionInfo(iPromoTech).getNumPrereqBonusORs()):
					if pCity.hasBonus(gc.getPromotionInfo(iPromoTech).getPrereqBonusOR(iBonusOR)):
						if not iPromoTech in lPromoBonus: # Avoiding duplicates, if multiple ORs are already obtained
							lPromoBonus.append(iPromoTech)
							break
					elif not iPromoTech in lPromoBonus: # if none of ORs are obtained
						lNoBonus.append(gc.getPromotionInfo(iPromoTech).getPrereqBonusOR(iBonusOR))
		for iPromoBonus in lPromoBonus: # Checking building prereq
			iNumBuildCount = gc.getPromotionInfo(iPromoBonus).getNumPrereqBuildingANDs()
			iNumTotalBuildCount = gc.getPromotionInfo(iPromoBonus).getNumPrereqBuildingANDs() + gc.getPromotionInfo(iPromoBonus).getNumPrereqBuildingORs()
			if iNumTotalBuildCount > 1: # all promotions already have master building as a prereq we can ignore
				for iBuildingAND in range(gc.getPromotionInfo(iPromoBonus).getNumPrereqBuildingANDs()):
					if pCity.getNumBuilding(gc.getPromotionInfo(iPromoBonus).getPrereqBuildingAND(iBuildingAND)) > 0:
						iNumBuildCount += -1
					elif pCity.canConstruct(gc.getPromotionInfo(iPromoBonus).getPrereqBuildingAND(iBuildingAND), False, False, False):
						if not gc.getPromotionInfo(iPromoBonus).getPrereqBuildingAND(iBuildingAND) in lNoBuilding:
							lNoBuilding.append(gc.getPromotionInfo(iPromoBonus).getPrereqBuildingAND(iBuildingAND))
				if iNumBuildCount == 0 and gc.getPromotionInfo(iPromoBonus).getNumPrereqBuildingORs == 0:
					lPromoBuilding.append(iPromoBonus)
				elif iNumBuildCount == 0 and gc.getPromotionInfo(iPromoBonus).getNumPrereqBuildingORs > 0:
					for iBuildingOR in range(gc.getPromotionInfo(iPromoBonus).getNumPrereqBuildingORs()):
						if pCity.getNumBuilding(gc.getPromotionInfo(iPromoBonus).getPrereqBuildingOR(iBuildingOR)) > 0:
							if not iPromoBonus in lPromoBuilding:
								lPromoBuilding.append(iPromoBonus)
								break
						elif not iPromoBonus in lPromoBuilding:
							if pCity.canConstruct(gc.getPromotionInfo(iPromoBonus).getPrereqBuildingOR(iBuildingOR), False, False, False):
								if not gc.getPromotionInfo(iPromoBonus).getPrereqBuildingOR(iBuildingOR) in lNoBuilding:
									lNoBuilding.append(gc.getPromotionInfo(iPromoBonus).getPrereqBuildingOR(iBuildingOR))
			elif not iPromoBonus in lPromoBuilding:
				lPromoBuilding.append(iPromoBonus)
		for iPromoBuilding in lPromoBuilding: # Checking State Religion prereq
			if gc.getPromotionInfo(iPromoBuilding).getStateReligionPrereq() > -1:
				if gc.getPromotionInfo(iPromoBuilding).getStateReligionPrereq() == pPlayer.getStateReligion():
					lPromoReligion.append(iPromoBuilding)
				elif pPlayer.canDoReligion(gc.getPromotionInfo(iPromoBuilding).getStateReligionPrereq()) and not gc.getPromotionInfo(iPromoBuilding).getStateReligionPrereq() in lNoRel:
					lNoRel.append(gc.getPromotionInfo(iPromoBuilding).getStateReligionPrereq())
			else:
				lPromoReligion.append(iPromoBuilding)
		# Check end
		# Pop-up start
		TotalPromos = len(lPromoReligion)
		szHelp += localText.getText("TXT_KEY_PYHELP_MASTER_TOTAL", (TotalPromos,))
		for iAPromo in lPromoReligion:
			sName = gc.getPromotionInfo(iAPromo).getDescription()
			iCost = gc.getPromotionInfo(iAPromo).getGoldCost()
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MASTER_AVAILABLE_PROMOTION", (sName, iCost, ))
		for iNoTech in lNoTech:
			sName = gc.getTechInfo(iNoTech).getDescription()
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MASTER_NO_TECH", (sName, ))
		for iNoBonus in lNoBonus:
			sName = gc.getBonusInfo(iNoBonus).getDescription()
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MASTER_NO_BONUS", (sName, ))
		for iNoBuilding in lNoBuilding:
			sName = gc.getBuildingInfo(iNoBuilding).getDescription()
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MASTER_NO_BUILDING", (sName, ))
		for iNoRel in lNoRel:
			sName = gc.getReligionInfo(iNoRel).getDescription()
			szHelp += localText.getText("TXT_KEY_PYHELP_VAULT_NEWLINE", ())
			szHelp += localText.getText("TXT_KEY_PYHELP_MASTER_NO_REL", (sName, ))
		# Pop-up end
	return szHelp
	
# SPELL_COMMANDER_JOIN
# PyRequirement checking if pPlot have any available commander to lead pCaster
def reqCommanderPicker(pCaster):
	pPlot			= pCaster.plot()
	pPlayer			= gc.getPlayer(pCaster.getOwner())
	Selected		= 0
	if pPlayer.isHuman():
		for iUnit in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(iUnit)
			if pUnit.IsSelected():
				Selected += 1
		if Selected > 1: # Prevent human player from casting spell if more than one unit is selected
			return False
	if not pCaster.getMasterUnit().isNone():
		return False
	pCommander = -1
	if pCaster.getUnitClassType() == getInfoType("UNITCLASS_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BATTLE_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_WAR_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BEHEMOTH_SLUGA"):
		pCommander = findSlugaCommanderAI(pCaster)
	else:
		pCommander = findCommanderAI(pCaster)
	if pCommander != -1:
		return True
	return False

# PyResult AI pPlayer will use old system and human pPlayer will use new one
def doCommanderPicker(pCaster):
	pPlot			= pCaster.plot()
	pPlayer			= gc.getPlayer(pCaster.getOwner())
	pCommander		= -1
	if pPlayer.isHuman():
		findCommanderHuman(pCaster)
	else:
		if pCaster.getUnitClassType() == getInfoType("UNITCLASS_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BATTLE_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_WAR_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BEHEMOTH_SLUGA"):
			pCommander = findSlugaCommanderAI(pCaster)
		else:
			pCommander = findCommanderAI(pCaster)
		if pCommander != -1:
			pCommander.addMinion(pCaster)
		#	pCaster.DeselectUnit()
		#	pCaster.SelectUnit()

# Old findCommander and findSlugaCommander functions for AI Player and PyRequirement
def findCommanderAI(pCaster):
	py = PyPlayer(pCaster.getOwner())
	pPlot = pCaster.plot()
	pBestUnit = -1
	iBestRank = 7
	iBestLevel = 9999
	bSameGroup = False
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == pCaster.getOwner():
			if not pUnit.getID() == pCaster.getID():
				if (bSameGroup and pUnit.getGroupID() == pCaster.getGroupID()) or (not bSameGroup):
					if pCaster.getDomainType() == pUnit.getDomainType():
						bvalid=True
						pLoopCommander=pUnit.getCommanderUnit()
						while( not pLoopCommander.isNone()):
							if (pLoopCommander.getID()==pCaster.getID()):
								bvalid=False
								break
							pLoopCommander=pLoopCommander.getCommanderUnit()
						if (not bvalid):
							continue
						if not pUnit.getID() == pCaster.getCommanderUnit().getID() and not pUnit.getCommanderUnit().getID() == pCaster.getID():		#Neither of us is leading the other one
							if pUnit.getNumMinions() < pUnit.getCommandLimit():
								iMinionRank = 0
								if pCaster.isHasPromotion(getInfoType('PROMOTION_GENERAL')):
									iMinionRank = 5
								elif pCaster.isHasPromotion(getInfoType('PROMOTION_CAPTAIN')):
									iMinionRank = 4
								elif pCaster.isHasPromotion(getInfoType('PROMOTION_MASTER_SEARGENT')):
									iMinionRank = 3
								elif pCaster.isHasPromotion(getInfoType('PROMOTION_SEARGENT')):
									iMinionRank = 2
								elif pCaster.isHasPromotion(getInfoType('PROMOTION_CORPORAL')):
									iMinionRank = 1
								elif pCaster.getCommandLimit() > 0:
									iMinionRank = 6
								iCommanderRank = 6
								if pUnit.isHasPromotion(getInfoType('PROMOTION_GENERAL')):
									iCommanderRank = 5
								elif pUnit.isHasPromotion(getInfoType('PROMOTION_CAPTAIN')):
									iCommanderRank = 4
								elif pUnit.isHasPromotion(getInfoType('PROMOTION_MASTER_SEARGENT')):
									iCommanderRank = 3
								elif pUnit.isHasPromotion(getInfoType('PROMOTION_SEARGENT')):
									iCommanderRank = 2
								elif pUnit.isHasPromotion(getInfoType('PROMOTION_CORPORAL')):
									iCommanderRank = 1
								if iCommanderRank > iMinionRank:	#If you have a rank, you cannot lead someone who outranks you
									if(pUnit.getGroupID() == pCaster.getGroupID()):
										if not (bSameGroup):
											pBestUnit = pUnit
											iBestRank = iCommanderRank
											iBestLevel = pUnit.getLevel()
											bSameGroup = True
										elif iCommanderRank < iBestRank:	#Prefer to follow the lowest Commander available
											pBestUnit = pUnit
											iBestRank = iCommanderRank
											iBestLevel = pUnit.getLevel()
										elif (iCommanderRank == iBestRank):
											if (pUnit.getLevel() < iBestLevel):
												pBestUnit = pUnit
												iBestLevel = pUnit.getLevel()
									else:
										if iCommanderRank < iBestRank:	#Prefer to follow the lowest Commander available
											pBestUnit = pUnit
											iBestRank = iCommanderRank
											iBestLevel = pUnit.getLevel()
										elif (iCommanderRank == iBestRank):
											if (pUnit.getLevel() < iBestLevel):
												pBestUnit = pUnit
												iBestLevel = pUnit.getLevel()
	return pBestUnit

def findSlugaCommanderAI(pCaster):
	py = PyPlayer(pCaster.getOwner())
	pPlot = pCaster.plot()
	pBestUnit = -1
	iBestRank = 7
	iBestLevel = 9999
	bSameGroup = False
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == pCaster.getOwner():
			if not pUnit.getID() == pCaster.getID():
				if (bSameGroup and pUnit.getGroupID() == pCaster.getGroupID()) or (not bSameGroup):
					if pCaster.getDomainType() == pUnit.getDomainType():
						if not pUnit.getID() == pCaster.getCommanderUnit().getID() and not pUnit.getCommanderUnit().getID() == pCaster.getID():
							if pUnit.getNumMinions() < pUnit.getCommandLimit():
								if pUnit.getUnitClassType() == getInfoType("UNITCLASS_OVERSEER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_COMBAT_OVERSEER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_SLUGA_COMMANDER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_KARAS"):
									iCommanderWeight = pUnit.getLevel()
									if pCaster.getUnitClassType() == getInfoType("UNITCLASS_SLUGA") and pUnit.getUnitClassType() == getInfoType("UNITCLASS_OVERSEER"):
										iCommanderWeight += 100
									if (pCaster.getUnitClassType() == getInfoType("UNITCLASS_BATTLE_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_WAR_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BEHEMOTH_SLUGA")) and (pUnit.getUnitClassType() == getInfoType("UNITCLASS_COMBAT_OVERSEER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_SLUGA_COMMANDER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_KARAS")):
										iCommanderWeight += 100
									if(pUnit.getGroupID() == pCaster.getGroupID()):
										if not (bSameGroup):
											pBestUnit = pUnit
											iBestLevel = iCommanderWeight
											bSameGroup = True
										elif iCommanderWeight < iBestLevel:
											pBestUnit = pUnit
											iBestLevel = iCommanderWeight
									else:
										if iCommanderWeight < iBestLevel:
											pBestUnit = pUnit
											iBestLevel = iCommanderWeight
	return pBestUnit

# New findCommander and findSlugaCommander functions for Human Player. Similar to old functions, but instead of choosing mechanism it gathers all available commanders to the list
# Changes to forming the list of commanders should be reflected in CvScreensInterface.py def SelectCommanderCallback counterpart
def findCommanderHuman(pCaster):
	pPlot			= pCaster.plot()
	iPlayer			= pCaster.getOwner()
	listCommander	= []
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == pCaster.getOwner():
			if not pUnit.getID() == pCaster.getID():	
				if pCaster.getDomainType() == pUnit.getDomainType():
					bvalid=True
					pLoopCommander=pUnit.getCommanderUnit()
					while( not pLoopCommander.isNone()):
						if (pLoopCommander.getID()==pCaster.getID()):
							bvalid=False
							break
						pLoopCommander=pLoopCommander.getCommanderUnit()
					if (not bvalid):
						continue
					if not pUnit.getID() == pCaster.getCommanderUnit().getID() and not pUnit.getCommanderUnit().getID() == pCaster.getID():		#Neither of us is leading the other one
						if pUnit.getNumMinions() < pUnit.getCommandLimit():
							if pCaster.getUnitClassType() == getInfoType("UNITCLASS_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BATTLE_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_WAR_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BEHEMOTH_SLUGA"): # Mekara part additionaly checks if pCaster is Sluga and pUnit is Overseer
								if pUnit.getUnitClassType() == getInfoType("UNITCLASS_OVERSEER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_COMBAT_OVERSEER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_SLUGA_COMMANDER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_KARAS"):
									listCommander.append(pUnit)
							else: # Non-Mekara part checks for BCoC and default commanders at the same time
								iMinionRank = 0
								if pCaster.isHasPromotion(getInfoType('PROMOTION_GENERAL')):
									iMinionRank = 5
								elif pCaster.isHasPromotion(getInfoType('PROMOTION_CAPTAIN')):
									iMinionRank = 4
								elif pCaster.isHasPromotion(getInfoType('PROMOTION_MASTER_SEARGENT')):
									iMinionRank = 3
								elif pCaster.isHasPromotion(getInfoType('PROMOTION_SEARGENT')):
									iMinionRank = 2
								elif pCaster.isHasPromotion(getInfoType('PROMOTION_CORPORAL')):
									iMinionRank = 1
								elif pCaster.getCommandLimit() > 0:
									iMinionRank = 6
								iCommanderRank = 6
								if pUnit.isHasPromotion(getInfoType('PROMOTION_GENERAL')):
									iCommanderRank = 5
								elif pUnit.isHasPromotion(getInfoType('PROMOTION_CAPTAIN')):
									iCommanderRank = 4
								elif pUnit.isHasPromotion(getInfoType('PROMOTION_MASTER_SEARGENT')):
									iCommanderRank = 3
								elif pUnit.isHasPromotion(getInfoType('PROMOTION_SEARGENT')):
									iCommanderRank = 2
								elif pUnit.isHasPromotion(getInfoType('PROMOTION_CORPORAL')):
									iCommanderRank = 1
								if iCommanderRank > iMinionRank:
									listCommander.append(pUnit)
	if len(listCommander) == 1: # No need to call popup if there is only one commander
		pCommander = listCommander[0]
		pCommander.addMinion(pCaster)
	elif len(listCommander) > 1: # popup starts if list contains at least two commanders
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_ADD_TO_COMMANDER",()))
		popupInfo.setData1(pCaster.getID())
		popupInfo.setData2(iPlayer)
		popupInfo.setData3(113) # onModNetMessage id
		popupInfo.setOnClickedPythonCallback("passToModNetMessage")
		popupInfo.addPythonButton(localText.getText("TXT_KEY_CANCEL", ()), "")
		for pCommander in listCommander:
			promotionBCOC = -1
			if pCommander.isHasPromotion(getInfoType('PROMOTION_GENERAL')):
				promotionBCOC = getInfoType('PROMOTION_GENERAL')
			elif pCommander.isHasPromotion(getInfoType('PROMOTION_CAPTAIN')):
				promotionBCOC = getInfoType('PROMOTION_CAPTAIN')
			elif pCommander.isHasPromotion(getInfoType('PROMOTION_MASTER_SEARGENT')):
				promotionBCOC = getInfoType('PROMOTION_MASTER_SEARGENT')
			elif pCommander.isHasPromotion(getInfoType('PROMOTION_SEARGENT')):
				promotionBCOC = getInfoType('PROMOTION_SEARGENT')
			elif pCommander.isHasPromotion(getInfoType('PROMOTION_CORPORAL')):
				promotionBCOC = getInfoType('PROMOTION_CORPORAL')
			if promotionBCOC == -1:
				popupInfo.addPythonButton(localText.getText("TXT_KEY_SPELL_JOIN_COMMANDER_POPUP",(pCommander.getName(),pCommander.getLevel(),pCommander.getNumMinions(),pCommander.getCommandLimit(),pCaster.getName(),)),"")
			else:
				popupInfo.addPythonButton(localText.getText("TXT_KEY_SPELL_JOIN_BCOC_COMMANDER_POPUP",(pCommander.getName(),gc.getPromotionInfo(promotionBCOC).getDescription(),pCommander.getLevel(),pCommander.getNumMinions(),pCommander.getCommandLimit(),pCaster.getName(),)),"")
		popupInfo.addPopup(iPlayer)
	elif len(listCommander) < 1:
		print "Commander Picker: findCommanderHuman is called with 0 available commanders despite reqCommanderPicker."

# PyHelp similar to findCommanderHuman, instead of starting a popup returns szHelp
def helpCommanderPicker(argsList):
	eSpell, pCaster = argsList
	pPlot			= pCaster.plot()
	iPlayer			= gc.getGame().getActivePlayer()
	listCommander	= []
	szHelp			= ""
	if pCaster == -1 or pCaster.isNone():
		return szHelp
	else:
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getOwner() == pCaster.getOwner():
				if not pUnit.getID() == pCaster.getID():	
					if pCaster.getDomainType() == pUnit.getDomainType():
						bvalid=True
						pLoopCommander=pUnit.getCommanderUnit()
						while( not pLoopCommander.isNone()):
							if (pLoopCommander.getID()==pCaster.getID()):
								bvalid=False
								break
							pLoopCommander=pLoopCommander.getCommanderUnit()
						if (not bvalid):
							continue
						if not pUnit.getID() == pCaster.getCommanderUnit().getID() and not pUnit.getCommanderUnit().getID() == pCaster.getID():		#Neither of us is leading the other one
							if pUnit.getNumMinions() < pUnit.getCommandLimit():
								if pCaster.getUnitClassType() == getInfoType("UNITCLASS_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BATTLE_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_WAR_SLUGA") or pCaster.getUnitClassType() == getInfoType("UNITCLASS_BEHEMOTH_SLUGA"): # Mekara part additionaly checks if pCaster is Sluga and pUnit is Overseer
									if pUnit.getUnitClassType() == getInfoType("UNITCLASS_OVERSEER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_COMBAT_OVERSEER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_SLUGA_COMMANDER") or pUnit.getUnitClassType() == getInfoType("UNITCLASS_KARAS"):
										listCommander.append(pUnit)
								else: # Non-Mekara part checks for BCoC and default commanders
									iMinionRank = 0
									if pCaster.isHasPromotion(getInfoType('PROMOTION_GENERAL')):
										iMinionRank = 5
									elif pCaster.isHasPromotion(getInfoType('PROMOTION_CAPTAIN')):
										iMinionRank = 4
									elif pCaster.isHasPromotion(getInfoType('PROMOTION_MASTER_SEARGENT')):
										iMinionRank = 3
									elif pCaster.isHasPromotion(getInfoType('PROMOTION_SEARGENT')):
										iMinionRank = 2
									elif pCaster.isHasPromotion(getInfoType('PROMOTION_CORPORAL')):
										iMinionRank = 1
									elif pCaster.getCommandLimit() > 0:
										iMinionRank = 6
									iCommanderRank = 6
									if pUnit.isHasPromotion(getInfoType('PROMOTION_GENERAL')):
										iCommanderRank = 5
									elif pUnit.isHasPromotion(getInfoType('PROMOTION_CAPTAIN')):
										iCommanderRank = 4
									elif pUnit.isHasPromotion(getInfoType('PROMOTION_MASTER_SEARGENT')):
										iCommanderRank = 3
									elif pUnit.isHasPromotion(getInfoType('PROMOTION_SEARGENT')):
										iCommanderRank = 2
									elif pUnit.isHasPromotion(getInfoType('PROMOTION_CORPORAL')):
										iCommanderRank = 1
									if iCommanderRank > iMinionRank:
										listCommander.append(pUnit)
		if len(listCommander) == 1:
			pCommander = listCommander[0]
			szHelp = localText.getText("TXT_KEY_SPELL_JOIN_COMMANDER", (pCommander.getName(),pCaster.getName()))
		elif len(listCommander) > 1:
			szHelp = localText.getText("TXT_KEY_SPELL_JOIN_COMMANDER_MULTIPLE", ())
		elif len(listCommander) < 1:
			szHelp = localText.getText("You shouldn't see this, ping T_W in AoE discord", ())
		return szHelp

def reqLairImmortal(argsList):
	pUnit, pPlot		= argsList
	if pUnit.isAlive():
		return True
	return False
	
def reqAustrinCallFalcon(pCaster):
	return pCaster.cargoSpaceAvailable(getInfoType("SPECIALUNIT_BIRD"),DomainTypes.DOMAIN_AIR)>0
	
def spellAustrinCallFalcon(pCaster):
	pPlayer			= gc.getPlayer(pCaster.getOwner())
	newUnit			= pPlayer.initUnit(getInfoType("UNIT_FALCON"), pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.setTransportUnit(pCaster)
	newUnit2			= pPlayer.initUnit(getInfoType("UNIT_FALCON"), pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit2.setTransportUnit(pCaster)

def spellAustrinCallFalcon2(pCaster):
	pPlayer			= gc.getPlayer(pCaster.getOwner())
	newUnit			= pPlayer.initUnit(getInfoType("UNIT_FALCON2"), pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.setTransportUnit(pCaster)
	
	
	
def reqSapperBoom(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	bValid = False
	getPlot	= CyMap().plot
	iRange = 1 
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pLoopPlot = getPlot(x, y)
		if pLoopPlot.isCity() and pTeam.isAtWar(gc.getPlayer(pLoopPlot.getOwner()).getTeam()) and pLoopPlot.getPlotCity().getDefenseModifier(False)>0:
			return True
	return False

def spellSapperBoom(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	getPlot	= CyMap().plot
	iRange = 1
	for x, y in plotsInRange( caster.getX(), caster.getY(), iRange ):
		pLoopPlot = getPlot(x, y)
		if pLoopPlot.isCity() and pTeam.isAtWar(gc.getPlayer(pLoopPlot.getOwner()).getTeam()):
			pCity=pLoopPlot.getPlotCity()
			pCity.changeDefenseModifier(-caster.bombardRate()*10)
	
def spellDemonLairSpawn(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isBarbarian():
		pPlot.setImprovementType(getInfoType("IMPROVEMENT_HELLFIRE"))
		caster.setHasPromotion(getInfoType('PROMOTION_LEASH_1'),True)

def helpTakeEquipment(argsList):
	eSpell, pCaster = argsList
	if pCaster == -1 or pCaster.isNone():
		szHelp	= ""
	else:
		lEquipmentList	= []
		pPlot			= pCaster.plot()
		for iUnit in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(iUnit)
			if pUnit.isCommunalProperty():
				for iPromotion in xrange(gc.getNumPromotionInfos()):
					if pUnit.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
						if not pCaster.isHasPromotion(iPromotion):
							if not iPromotion in lEquipmentList:
								if cf.canRemoveEquipment(-1,pCaster,iPromotion) == True:
									lEquipmentList.append(iPromotion)
		if len(lEquipmentList) == 0:
			szHelp = "If you see this message report it as a bug"
		elif len(lEquipmentList) == 1:
			iEquipment = lEquipmentList[0]
			szHelp = localText.getText("TXT_KEY_PYHELP_TAKE_EQUIPMENT_NO_LIST",(gc.getPromotionInfo(iEquipment).getTextKey(),))
		elif len(lEquipmentList) > 1:
			szHelp = localText.getText("TXT_KEY_PYHELP_TAKE_EQUIPMENT_OPEN_LIST", ())
	return szHelp

def reqTakeEquipment(pCaster):
	pPlayer		= gc.getPlayer(pCaster.getOwner())
	Selected	= 0
	pPlot		= pCaster.plot()
	for iUnit in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.IsSelected():
			Selected += 1
	if Selected > 1: # Prevent player from casting spell if more than one unit is selected
		return False
	for iUnit in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.isCommunalProperty():
			for iPromotion in xrange(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
					if not pCaster.isHasPromotion(iPromotion):
						if cf.canRemoveEquipment(-1,pCaster,iPromotion) == True:
							return True
	return False

def spellTakeEquipment(pCaster):
	pPlot			= pCaster.plot()
	iPlayer			= pCaster.getOwner()
	pPlayer 		= gc.getPlayer(iPlayer)
	lEquipmentList	= []
	for iUnit in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.isCommunalProperty():
			for iPromotion in xrange(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
					if not pCaster.isHasPromotion(iPromotion):
						if not iPromotion in lEquipmentList:
							if cf.canRemoveEquipment(-1,pCaster,iPromotion) == True:
								lEquipmentList.append(iPromotion)
	if len(lEquipmentList) == 1:
		iEquipment = lEquipmentList[0]
		for iUnit in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(iUnit)
			if pUnit.isCommunalProperty() and pUnit.isHasPromotion(iEquipment):
				pUnit.setHasPromotion(iEquipment, False)
				pCaster.setHasPromotion(iEquipment, True)
				return
	if len(lEquipmentList) > 1:
		if pPlayer.isHuman():
			popupInfo	= CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("passToModNetMessage")
			popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_TAKE_EQUIPMENT", ()))
			popupInfo.setData1(pCaster.getID())
			popupInfo.setData2(iPlayer)
			popupInfo.setData3(123) # onModNetMessage id
			popupInfo.addPythonButton(localText.getText("TXT_KEY_CANCEL", ()), "")
			for iEquipment in lEquipmentList:
				szButtonText = localText.getText("TXT_KEY_TAKE_ONE",(gc.getPromotionInfo(iEquipment).getTextKey(),))
				popupInfo.addPythonButton(szButtonText, gc.getPromotionInfo(iEquipment).getButton())
			popupInfo.addPopup(iPlayer)
		else: 
			iBestEquipment	= -1
			iBestWeight		= -1
			for iEquipment in lEquipmentList:
				if gc.getPromotionInfo(iEquipment).getAIWeight() > 0:
					iAIWeight = gc.getPromotionInfo(iEquipment).getAIWeight()
					if iAIWeight > iBestWeight:
						iBestWeight		= iAIWeight
						iBestEquipment	= iEquipment
			if iBestEquipment != -1:
				for iUnit in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(iUnit)
					if pUnit.isCommunalProperty() and pUnit.isHasPromotion(iBestEquipment):
						pUnit.setHasPromotion(iBestEquipment, False)
						pCaster.setHasPromotion(iBestEquipment, True)
			else:
				iEquipment = lEquipmentList[0]
				for iUnit in xrange(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(iUnit)
					if pUnit.isCommunalProperty() and pUnit.isHasPromotion(iEquipment):
						pUnit.setHasPromotion(iEquipment, False)
						pCaster.setHasPromotion(iEquipment, True)
# SPELL_DROP_EQUIPMENT
def helpDropEquipment(argsList):
	eSpell, pCaster = argsList
	if pCaster == -1 or pCaster.isNone():
		szHelp	= ""
	else:
		lEquipmentList	= []
		for iPromotion in xrange(gc.getNumPromotionInfos()):
			if pCaster.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
				if cf.canRemoveEquipment(pCaster,-1,iPromotion) == True:
					lEquipmentList.append(iPromotion)
		if len(lEquipmentList) == 0:
			szHelp = "If you see this message report it as a bug"
		elif len(lEquipmentList) == 1:
			iEquipment = lEquipmentList[0]
			szHelp = localText.getText("TXT_KEY_PYHELP_DROP_EQUIPMENT_NO_LIST",(gc.getPromotionInfo(iEquipment).getTextKey(),))
		elif len(lEquipmentList) > 1:
			szHelp = localText.getText("TXT_KEY_PYHELP_DROP_EQUIPMENT_OPEN_LIST", ())
	return szHelp

def reqDropEquipment(pCaster):
	pPlayer		= gc.getPlayer(pCaster.getOwner())
	Selected	= 0
	pPlot		= pCaster.plot()
	for iUnit in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.IsSelected():
			Selected += 1
	if Selected > 1: # Prevent player from casting spell if more than one unit is selected
		return False
	for iPromotion in xrange(gc.getNumPromotionInfos()):
		if pCaster.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
			if cf.canRemoveEquipment(pCaster,-1,iPromotion) == True:
				return True
	return False

def spellDropEquipment(pCaster):
	pPlot			= pCaster.plot()
	iPlayer			= pCaster.getOwner()
	pPlayer 		= gc.getPlayer(iPlayer)
	lEquipmentList	= []
	for iPromotion in xrange(gc.getNumPromotionInfos()):
		if pCaster.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
			if cf.canRemoveEquipment(pCaster,-1,iPromotion) == True:
				lEquipmentList.append(iPromotion)
	if len(lEquipmentList) == 1:
		containerUnit = -1
		for iUnit in xrange(pPlot.getNumUnits()):
			if pPlot.getUnit(iUnit).getUnitType() == getInfoType('EQUIPMENT_CONTAINER'):
				containerUnit = pPlot.getUnit(iUnit)
		if containerUnit == -1:
			containerUnit = gc.getPlayer(gc.getORC_PLAYER()).initUnit(git('EQUIPMENT_CONTAINER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		containerUnit.setHasPromotion(lEquipmentList[0],True)
		pCaster.setHasPromotion(lEquipmentList[0],False)
	if len(lEquipmentList) > 1:
		if pPlayer.isHuman():
			popupInfo	= CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("passToModNetMessage")
			popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_DROP_EQUIPMENT", ()))
			popupInfo.setData1(pCaster.getID())
			popupInfo.setData2(iPlayer)
			popupInfo.setData3(124) # onModNetMessage id
			popupInfo.addPythonButton(localText.getText("TXT_KEY_CANCEL", ()), "")
			popupInfo.addPythonButton(localText.getText("TXT_KEY_DROP_ALL", ()), "")
			for iEquipment in lEquipmentList:
				szButtonText = localText.getText("TXT_KEY_DROP_ONE",(gc.getPromotionInfo(iEquipment).getTextKey(),))
				popupInfo.addPythonButton(szButtonText, gc.getPromotionInfo(iEquipment).getButton())
			popupInfo.addPopup(iPlayer)

# SPELL_SWAP_EQUIPMENT
def helpSwapEquipment(argsList):
	eSpell, pCaster = argsList
	if pCaster == -1 or pCaster.isNone():
		szHelp	= ""
	else:
		pPlot		= pCaster.plot()
		iCounter	= 0
		iEquipment	= -1
		pHolder		= -1
		iPlayer		= pCaster.getOwner()
		for iUnit in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(iUnit)
			if not pUnit.isCommunalProperty() and pUnit.getOwner() == iPlayer:
				for iPromotion in xrange(gc.getNumPromotionInfos()):
					if pUnit.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
						if not pCaster.isHasPromotion(iPromotion):
							if cf.canRemoveEquipment(pUnit,pCaster,iPromotion) == True:
								iCounter += 1
								iEquipment = iPromotion
								pHolder = pUnit
		if iCounter == 0:
			szHelp = "If you see this message report it as a bug"
		elif iCounter == 1:
			szHelp = localText.getText("TXT_KEY_PYHELP_SWAP_EQUIPMENT_NO_LIST",(gc.getPromotionInfo(iEquipment).getTextKey(),pHolder.getName(),))
		elif iCounter > 1:
			szHelp = localText.getText("TXT_KEY_PYHELP_SWAP_EQUIPMENT_OPEN_LIST", ())
	return szHelp

def reqSwapEquipment(pCaster):
	pPlot		= pCaster.plot()
	iPlayer		= pCaster.getOwner()
	pPlayer		= gc.getPlayer(iPlayer)
	Selected	= 0
	pPlot		= pCaster.plot()
	for iUnit in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(iUnit)
		if pUnit.IsSelected():
			Selected += 1
	if Selected > 1: # Prevent player from casting spell if more than one unit is selected
		return False
	for iUnit in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(iUnit)
		if not pUnit.isCommunalProperty() and pUnit.getOwner() == iPlayer and not pUnit.isHasCasted():
			for iPromotion in xrange(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
					if not pCaster.isHasPromotion(iPromotion):
						if cf.canRemoveEquipment(pUnit,pCaster,iPromotion) == True:
							return True
	return False

def spellSwapEquipment(pCaster):
	pPlot				= pCaster.plot()
	iPlayer				= pCaster.getOwner()
	pPlayer 			= gc.getPlayer(iPlayer)
	lEquipmentUnitPairs = []
	for iUnit in xrange(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(iUnit)
		if not pUnit.isCommunalProperty() and pUnit.getOwner() == iPlayer:
			for iPromotion in xrange(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
					if not pCaster.isHasPromotion(iPromotion):
						if cf.canRemoveEquipment(pUnit,pCaster,iPromotion) == True:
							lPair = [iPromotion,pUnit]
							lEquipmentUnitPairs.append(lPair)
	if len(lEquipmentUnitPairs) == 1:
		lPair		= lEquipmentUnitPairs[0]
		iPromotion	= lPair[0]
		pHolder		= lPair[1]
		pCaster.setHasPromotion(iPromotion,True)
		pHolder.setHasPromotion(iPromotion,False)
	if len(lEquipmentUnitPairs) > 1:
		if pPlayer.isHuman():
			popupInfo	= CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("passToModNetMessage")
			popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_SWAP_EQUIPMENT", ()))
			popupInfo.setData1(pCaster.getID())
			popupInfo.setData2(iPlayer)
			popupInfo.setData3(125) # onModNetMessage id
			popupInfo.addPythonButton(localText.getText("TXT_KEY_CANCEL", ()), "")
			for lPair in lEquipmentUnitPairs:
				iPromotion	= lPair[0]
				pHolder		= lPair[1]
				popupInfo.addPythonButton(localText.getText("TXT_KEY_SPELL_SWAP_EQUIPMENT_LIST",(gc.getPromotionInfo(iPromotion).getTextKey(), pHolder.getName(), pHolder.getLevel(),)),gc.getPromotionInfo(iPromotion).getButton())
			popupInfo.addPopup(iPlayer)
	

def effectOtoloch(caster):
	pPlot = caster.plot()
	if pPlot.getTerrainType()==gc.getInfoTypeForString("TERRAIN_OCEAN") and pPlot.getImprovementType()==-1 and not caster.isLeashed():
		if CyGame().getSorenRandNum(100, "otoloch")<5:
			caster.setHasPromotion(gc.getInfoTypeForString("PROMOTION_LEASH_1"),True)
			pPlot.setImprovementType(gc.getInfoTypeForString("IMPROVEMENT_SHIMMERING_PORTAL"))
