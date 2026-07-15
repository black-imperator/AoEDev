## AnimalLairs CvSpellInterface.py
## By TiberiusW 03/05/2023

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

# Quick list of lairs
LairBear1			= git('IMPROVEMENT_BEAR_DEN')
LairBear2			= git('IMPROVEMENT_BEAR_DEN_2')
LairBear3			= git('IMPROVEMENT_BEAR_DEN_3')
LairRoc1			= git('IMPROVEMENT_HIPPOGRIFF_WEYR')
LairRoc2			= git('IMPROVEMENT_GRIFFIN_WEYR')
LairRoc3			= git('IMPROVEMENT_ROC_WEYR')
LairLion1			= git('IMPROVEMENT_LION_DEN')
LairLion2			= git('IMPROVEMENT_LION_DEN_2')
LairLion3			= git('IMPROVEMENT_LION_DEN_3')
LairSpider1			= git('IMPROVEMENT_DEN_SPIDER')
LairSpider2			= git('IMPROVEMENT_SPIDER_DEN_2')
LairSpider3			= git('IMPROVEMENT_SPIDER_DEN_3')
LairWolf1			= git('IMPROVEMENT_DEN_WOLF')
LairWolf2			= git('IMPROVEMENT_WOLF_LAIR_2')
LairWolf3			= git('IMPROVEMENT_WOLF_LAIR_3')
LairScorpion1		= git('IMPROVEMENT_SCORPION_NEST_1')
LairScorpion2		= git('IMPROVEMENT_SCORPION_NEST_2')
LairScorpion3		= git('IMPROVEMENT_SCORPION_NEST_3')

AllAnimalLairs		= [LairBear1,LairBear2,LairBear3,LairRoc1,LairRoc2,LairRoc3,LairLion1,LairLion2,LairLion3,LairSpider1,LairSpider2,LairSpider3,LairWolf1,LairWolf2,LairWolf3,LairScorpion1,LairScorpion2,LairScorpion3]

# Lairs by type
BearLairs			= [LairBear1,LairBear2,LairBear3]
RocLairs			= [LairRoc1,LairRoc2,LairRoc3]
LionLairs			= [LairLion1,LairLion2,LairLion3]
SpiderLairs			= [LairSpider1,LairSpider2,LairSpider3]
WolfLairs			= [LairWolf1,LairWolf2,LairWolf3]
ScorpionLairs		= [LairScorpion1,LairScorpion2,LairScorpion3]

# Lairs by tier
# AnimalLairsT1		= [LairBear1,LairRoc1,LairLion1,LairSpider1,LairWolf1,LairScorpion1]
# AnimalLairsT2		= [LairBear2,LairRoc2,LairLion2,LairSpider2,LairWolf2,LairScorpion2]
# AnimalLairsT3		= [LairBear3,LairRoc3,LairLion3,LairSpider3,LairWolf3,LairScorpion3]

# GOODY_EXPLORE_LAIR_DEN_FRIENDLY_ANIMAL
def exploreLairFriendly(pUnit, pPlot):

	pPlayer			= gc.getPlayer(pUnit.getOwner())
	iRandStrength	= gc.getGame().getSorenRandNum(100, "Friendly Animal Lair") # 0-49 - weak result; 50-89 - normal result; 90-99 - strong result
	iLair			= pPlot.getImprovementType()
	if iLair in BearLairs:
		newUnit = pPlayer.initUnit(git('UNIT_BEAR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength < 50:
			newUnit.setHasPromotion(git('PROMOTION_WEAK'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)
	elif iLair in RocLairs:
		if iRandStrength < 50:
			newUnit = pPlayer.initUnit(git('UNIT_HIPPOGRIFF'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit = pPlayer.initUnit(git('UNIT_GRIFFON'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if iRandStrength >= 90:
				newUnit.setHasPromotion(git('PROMOTION_MOBILITY1'),True)
	elif iLair in LionLairs:
		if iRandStrength < 90:
			newUnit = pPlayer.initUnit(git('UNIT_LION'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if iRandStrength < 50:
				newUnit.setHasPromotion(git('PROMOTION_WEAK'),True)
		if iRandStrength >= 90:
			newUnit = pPlayer.initUnit(git('UNIT_LION_PRIDE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	elif iLair in SpiderLairs:
		if iRandStrength < 50:
			newUnit = pPlayer.initUnit(git('UNIT_BABY_SPIDER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit = pPlayer.initUnit(git('UNIT_SPIDER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if iRandStrength >= 90:
				SpiderPromo = [('PROMOTION_SPIDER_RHAGODESSA',1),('PROMOTION_SPIDER_MUCRO',1),('PROMOTION_SPIDER_TEXTUS',1),('PROMOTION_SPIDER_ARGYRONETA',1),('PROMOTION_SPIDER_VENENUM',1)]
				getSpiderPromo = wchoice(SpiderPromo,'Roll Spider Promo')
				newUnit.setHasPromotion(git(getSpiderPromo()),True)
	elif iLair in WolfLairs:
		if iRandStrength < 90:
			newUnit = pPlayer.initUnit(git('UNIT_WOLF'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if iRandStrength < 50:
				newUnit.setHasPromotion(git('PROMOTION_WEAK'),True)
		if iRandStrength >= 90:
			newUnit = pPlayer.initUnit(git('UNIT_WOLF_PACK'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	elif iLair in ScorpionLairs:
		newUnit = pPlayer.initUnit(git('UNIT_SCORPION'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength < 50:
			newUnit.setHasPromotion(git('PROMOTION_WEAK'),True)
		if iRandStrength >= 90:
			pUnit.setHasPromotion(git('PROMOTION_POISONED_BLADE'),True)
	else: # If somehow there are lairs with animal class that are not in the list it will spawn bears
		newUnit = pPlayer.initUnit(git('UNIT_BEAR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength < 50:
			newUnit.setHasPromotion(git('PROMOTION_WEAK'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)

# GOODY_EXPLORE_LAIR_HOSTILE_ANIMAL_T1
def exploreLairHostileT1(pUnit, pPlot):

	pPlayer			= gc.getPlayer(pUnit.getOwner())
	CernPlayer		= gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot		= findClearPlot(-1, pPlot)
	iRandStrength	= gc.getGame().getSorenRandNum(100, "Hostile Animal Lair T1") # 0-49 - weak result; 50-89 - normal result; 90-99 - strong result
	iRandLoyalty	= gc.getGame().getSorenRandNum(100, "Loyalty Animal Lair T1") # 0-49 - apply Loyalty; 50-99 - don't
	iLair			= pPlot.getImprovementType()
	if iLair in BearLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_BEAR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)
	elif iLair in RocLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_HIPPOGRIFF'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_HEROIC_STRENGTH'),True)
			newUnit.setHasPromotion(git('PROMOTION_HEROIC_DEFENSE'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_HEROIC_STRENGTH2'),True)
			newUnit.setHasPromotion(git('PROMOTION_HEROIC_DEFENSE2'),True)
	elif iLair in LionLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_LION'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_BLITZ'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_MOBILITY1'),True)
	elif iLair in SpiderLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_BABY_SPIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			SpiderPromo = [('PROMOTION_SPIDER_RHAGODESSA',1),('PROMOTION_SPIDER_MUCRO',1),('PROMOTION_SPIDER_TEXTUS',1),('PROMOTION_SPIDER_ARGYRONETA',1),('PROMOTION_SPIDER_VENENUM',1)]
			getSpiderPromo = wchoice(SpiderPromo,'Roll Spider Promo')
			newUnit.setHasPromotion(git(getSpiderPromo()),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)
	elif iLair in WolfLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_WOLF'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_WOODSMAN2'),True)
	elif iLair in ScorpionLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_SCORPION'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_DRILL1'),True)
			newUnit.setHasPromotion(git('PROMOTION_COMBAT1'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_DRILL2'),True)
			newUnit.setHasPromotion(git('PROMOTION_COMBAT2'),True)
	else: # If somehow there are lairs with animal class that are not in the list it will spawn bears
		newUnit = CernPlayer.initUnit(git('UNIT_BEAR'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)
	if iRandLoyalty < 50:
		newUnit.setHasPromotion(git('PROMOTION_LOYALTY2'),True)

# GOODY_EXPLORE_LAIR_DEN_HOSTILE_RECON
def exploreLairHostileGoblin(pUnit, pPlot):

	pPlayer 		= gc.getPlayer(pUnit.getOwner())
	GoblinCiv		= gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot		= findClearPlot(-1, pPlot)
	iRandStrength	= gc.getGame().getSorenRandNum(100, "Hostile Goblin T1") # 0-49 - weak result; 50-89 - normal result; 90-99 - strong result
	iRandLoyalty	= gc.getGame().getSorenRandNum(100, "Loyalty Goblin T1") # Peace with Bhall or Goblin explorer have chance to turn spawned unit
	GoblinClan		= [('UNIT_GOBLIN_MURIS_CLAN',1),('UNIT_GOBLIN_MURIS_CLAN',1),('UNIT_GOBLIN_LUKOS_CLAN',1),('UNIT_GOBLIN_NEITH_CLAN',1)]
	getGoblinClan	= wchoice(GoblinClan,'Roll Goblin Clan')
	if pUnit.isHasPromotion(git('PROMOTION_GOBLIN')) or not gc.getTeam(pPlayer.getTeam()).isAtWar(gc.getORC_TEAM()):
		if iRandLoyalty >= 50:
			GoblinCiv	= pPlayer
	newUnit			= GoblinCiv.initUnit(git(getGoblinClan()), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	if iRandStrength >= 50:
		newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)
	if iRandStrength >= 90:
		newUnit.setHasPromotion(git('PROMOTION_MOBILITY1'),True)

# GOODY_EXPLORE_LAIR_HOSTILE_ANIMAL_T2
def exploreLairHostileT2(pUnit, pPlot):

	pPlayer			= gc.getPlayer(pUnit.getOwner())
	CernPlayer		= gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot		= findClearPlot(-1, pPlot)
	iRandStrength	= gc.getGame().getSorenRandNum(100, "Hostile Animal Lair T2") # 0-49 - weak result; 50-89 - normal result; 90-99 - strong result
	iRandLoyalty	= gc.getGame().getSorenRandNum(100, "Loyalty Animal Lair T2") # 0-49 - apply Loyalty; 50-99 - don't
	iLair			= pPlot.getImprovementType()
	if iLair in BearLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_BEAR_GROUP'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)
	elif iLair in RocLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_GRIFFON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_HEROIC_STRENGTH'),True)
			newUnit.setHasPromotion(git('PROMOTION_HEROIC_DEFENSE'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_HEROIC_STRENGTH2'),True)
			newUnit.setHasPromotion(git('PROMOTION_HEROIC_DEFENSE2'),True)
	elif iLair in LionLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_LION_PRIDE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_BLITZ'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_MOBILITY1'),True)
	elif iLair in SpiderLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_SPIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			SpiderPromo = [('PROMOTION_SPIDER_RHAGODESSA',1),('PROMOTION_SPIDER_MUCRO',1),('PROMOTION_SPIDER_TEXTUS',1),('PROMOTION_SPIDER_ARGYRONETA',1),('PROMOTION_SPIDER_VENENUM',1)]
			getSpiderPromo = wchoice(SpiderPromo,'Roll Spider Promo')
			newUnit.setHasPromotion(git(getSpiderPromo()),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)
	elif iLair in WolfLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_WOLF_PACK'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_WOODSMAN2'),True)
	elif iLair in ScorpionLairs:
		newUnit = CernPlayer.initUnit(git('UNIT_SCORPION_SWARM'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_DRILL1'),True)
			newUnit.setHasPromotion(git('PROMOTION_COMBAT1'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_DRILL2'),True)
			newUnit.setHasPromotion(git('PROMOTION_COMBAT2'),True)
	else: # If somehow there are lairs with animal class that are not in the list it will spawn bears
		newUnit = CernPlayer.initUnit(git('UNIT_BEAR_GROUP'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRandStrength >= 50:
			newUnit.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
		if iRandStrength >= 90:
			newUnit.setHasPromotion(git('PROMOTION_STRONG'),True)
	if iRandLoyalty < 50:
		newUnit.setHasPromotion(git('PROMOTION_LOYALTY2'),True)

# GOODY_EXPLORE_LAIR_HOSTILE_ANIMAL_T3
def exploreLairHostileT3(pUnit, pPlot):

	pPlayer			= gc.getPlayer(pUnit.getOwner())
	CernPlayer		= gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot		= findClearPlot(-1, pPlot)
	iRandStrength	= gc.getGame().getSorenRandNum(100, "Hostile Animal Lair T3") # 0-49 - weak result; 50-89 - normal result; 90-99 - strong result
	iRandLoyalty	= gc.getGame().getSorenRandNum(100, "Loyalty Animal Lair T3") # 0-74 - apply Loyalty; 75-99 - don't
	iLair			= pPlot.getImprovementType()
	if iLair in BearLairs:
		newUnit1 = CernPlayer.initUnit(git('UNIT_CAVE_BEARS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
		newUnit1.setHasPromotion(git('PROMOTION_DISEASED'),True)
		newUnit1.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
		newUnit1.setHasPromotion(git('PROMOTION_STRONG'),True)
		if iRandStrength >= 50:
			newUnit2 = CernPlayer.initUnit(git('UNIT_BEAR_GROUP'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit2.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit2.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit2.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
			newUnit2.setHasPromotion(git('PROMOTION_STRONG'),True)
		if iRandStrength >= 90:
			newUnit3 = CernPlayer.initUnit(git('UNIT_BEAR_GROUP'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit3.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit3.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit3.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
			newUnit3.setHasPromotion(git('PROMOTION_STRONG'),True)
	elif iLair in RocLairs:
		newUnit1 = CernPlayer.initUnit(git('UNIT_ROC'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
		newUnit1.setHasPromotion(git('PROMOTION_DISEASED'),True)
		newUnit1.setHasPromotion(git('PROMOTION_STRONG'),True)
		newUnit1.setHasPromotion(git('PROMOTION_HEROIC_STRENGTH'),True)
		newUnit1.setHasPromotion(git('PROMOTION_HEROIC_DEFENSE'),True)
		newUnit1.setHasPromotion(git('PROMOTION_HEROIC_STRENGTH2'),True)
		newUnit1.setHasPromotion(git('PROMOTION_HEROIC_DEFENSE2'),True)
		if iRandStrength >= 50:
			newUnit2 = CernPlayer.initUnit(git('UNIT_GRIFFON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit2.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit2.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit2.setHasPromotion(git('PROMOTION_STRONG'),True)
			newUnit2.setHasPromotion(git('PROMOTION_HEROIC_STRENGTH'),True)
			newUnit2.setHasPromotion(git('PROMOTION_HEROIC_DEFENSE'),True)
			newUnit2.setHasPromotion(git('PROMOTION_HEROIC_STRENGTH2'),True)
			newUnit2.setHasPromotion(git('PROMOTION_HEROIC_DEFENSE2'),True)
		if iRandStrength >= 90:
			newUnit3 = CernPlayer.initUnit(git('UNIT_GRIFFON'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit3.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit3.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit3.setHasPromotion(git('PROMOTION_STRONG'),True)
			newUnit3.setHasPromotion(git('PROMOTION_HEROIC_STRENGTH'),True)
			newUnit3.setHasPromotion(git('PROMOTION_HEROIC_DEFENSE'),True)
			newUnit3.setHasPromotion(git('PROMOTION_HEROIC_STRENGTH2'),True)
			newUnit3.setHasPromotion(git('PROMOTION_HEROIC_DEFENSE2'),True)
	elif iLair in LionLairs:
		newUnit1 = CernPlayer.initUnit(git('UNIT_SABRETOOTH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
		newUnit1.setHasPromotion(git('PROMOTION_DISEASED'),True)
		newUnit1.setHasPromotion(git('PROMOTION_BLITZ'),True)
		newUnit1.setHasPromotion(git('PROMOTION_MOBILITY1'),True)
		if iRandStrength >= 50:
			newUnit2 = CernPlayer.initUnit(git('UNIT_LION_PRIDE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit2.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit2.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit2.setHasPromotion(git('PROMOTION_BLITZ'),True)
			newUnit2.setHasPromotion(git('PROMOTION_MOBILITY1'),True)
		if iRandStrength >= 90:
			newUnit3 = CernPlayer.initUnit(git('UNIT_LION_PRIDE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit3.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit3.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit3.setHasPromotion(git('PROMOTION_BLITZ'),True)
			newUnit3.setHasPromotion(git('PROMOTION_MOBILITY1'),True)
		if iRandStrength == 99: # Their Battle Will Be Legendary!
			newUnit1.changeStrBoost(5)
			newUnit1.setHasPromotion(git('PROMOTION_AWAKENED'),True)
			newUnit1.setName("Sparemane")
	elif iLair in SpiderLairs:
		SpiderPromo = [('PROMOTION_SPIDER_RHAGODESSA',1),('PROMOTION_SPIDER_MUCRO',1),('PROMOTION_SPIDER_TEXTUS',1),('PROMOTION_SPIDER_ARGYRONETA',1),('PROMOTION_SPIDER_VENENUM',1)]
		getSpiderPromo = wchoice(SpiderPromo,'Roll Spider Promo')
		newUnit1 = CernPlayer.initUnit(git('UNIT_GIANT_SPIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
		newUnit1.setHasPromotion(git('PROMOTION_DISEASED'),True)
		newUnit1.setHasPromotion(git(getSpiderPromo()),True)
		newUnit1.setHasPromotion(git('PROMOTION_STRONG'),True)
		if iRandStrength >= 50:
			newUnit2 = CernPlayer.initUnit(git('UNIT_SPIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit2.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit2.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit2.setHasPromotion(git(getSpiderPromo()),True)
			newUnit2.setHasPromotion(git('PROMOTION_STRONG'),True)
		if iRandStrength >= 90:
			newUnit3 = CernPlayer.initUnit(git('UNIT_SPIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit3.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit3.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit3.setHasPromotion(git(getSpiderPromo()),True)
			newUnit3.setHasPromotion(git('PROMOTION_STRONG'),True)
	elif iLair in WolfLairs:
		newUnit1 = CernPlayer.initUnit(git('UNIT_DIRE_WOLF'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
		newUnit1.setHasPromotion(git('PROMOTION_DISEASED'),True)
		newUnit1.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
		newUnit1.setHasPromotion(git('PROMOTION_WOODSMAN2'),True)
		if iRandStrength >= 50:
			newUnit2 = CernPlayer.initUnit(git('UNIT_WOLF_PACK'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit2.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit2.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit2.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
			newUnit2.setHasPromotion(git('PROMOTION_WOODSMAN2'),True)
		if iRandStrength >= 90:
			newUnit3 = CernPlayer.initUnit(git('UNIT_WOLF_PACK'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit3.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit3.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit3.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
			newUnit3.setHasPromotion(git('PROMOTION_WOODSMAN2'),True)
	elif iLair in ScorpionLairs:
		newUnit1 = CernPlayer.initUnit(git('UNIT_SCORPION_GIANT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
		newUnit1.setHasPromotion(git('PROMOTION_DISEASED'),True)
		newUnit1.setHasPromotion(git('PROMOTION_DRILL1'),True)
		newUnit1.setHasPromotion(git('PROMOTION_COMBAT1'),True)
		newUnit1.setHasPromotion(git('PROMOTION_DRILL2'),True)
		newUnit1.setHasPromotion(git('PROMOTION_COMBAT2'),True)
		if iRandStrength >= 50:
			newUnit2 = CernPlayer.initUnit(git('UNIT_SCORPION_SWARM'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit2.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit2.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit2.setHasPromotion(git('PROMOTION_DRILL1'),True)
			newUnit2.setHasPromotion(git('PROMOTION_COMBAT1'),True)
			newUnit2.setHasPromotion(git('PROMOTION_DRILL2'),True)
			newUnit2.setHasPromotion(git('PROMOTION_COMBAT2'),True)
		if iRandStrength >= 90:
			newUnit3 = CernPlayer.initUnit(git('UNIT_SCORPION_SWARM'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit3.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit3.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit3.setHasPromotion(git('PROMOTION_DRILL1'),True)
			newUnit3.setHasPromotion(git('PROMOTION_COMBAT1'),True)
			newUnit3.setHasPromotion(git('PROMOTION_DRILL2'),True)
			newUnit3.setHasPromotion(git('PROMOTION_COMBAT2'),True)
	else: # If somehow there are lairs with animal class that are not in the list it will spawn bears
		newUnit1 = CernPlayer.initUnit(git('UNIT_CAVE_BEARS'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
		newUnit1.setHasPromotion(git('PROMOTION_DISEASED'),True)
		newUnit1.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
		newUnit1.setHasPromotion(git('PROMOTION_STRONG'),True)
		if iRandStrength >= 50:
			newUnit2 = CernPlayer.initUnit(git('UNIT_BEAR_GROUP'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit2.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit2.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit2.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
			newUnit2.setHasPromotion(git('PROMOTION_STRONG'),True)
		if iRandStrength >= 90:
			newUnit3 = CernPlayer.initUnit(git('UNIT_BEAR_GROUP'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
			newUnit3.setHasPromotion(git('PROMOTION_PLAGUE_CARRIER'),True)
			newUnit3.setHasPromotion(git('PROMOTION_DISEASED'),True)
			newUnit3.setHasPromotion(git('PROMOTION_WOODSMAN1'),True)
			newUnit3.setHasPromotion(git('PROMOTION_STRONG'),True)
	if iRandLoyalty < 75:
		newUnit1.setHasPromotion(git('PROMOTION_LOYALTY2'),True)
		if iRandStrength >= 50:
			newUnit2.setHasPromotion(git('PROMOTION_LOYALTY2'),True)
			if iRandStrength >= 90:
				newUnit3.setHasPromotion(git('PROMOTION_LOYALTY2'),True)

# New lairs for Doviello lair convertion spell
# SPELL_PACIFIC_COHABITATION
def reqConvertLairDovielloAL(pCaster):
	pPlot			= pCaster.plot()
	iPlayer			= pCaster.getOwner()
	iImprovement	= pPlot.getImprovementType()
	iImprovementOwner = pPlot.getImprovementOwner()
	if iImprovementOwner != iPlayer:
		if iImprovement in AllAnimalLairs:
			return True
	return False

# Alt result for Nature Minor Blood promotions
# GOODY_EXPLORE_LAIR_ANIMAL_BLOOD
def exploreLairAnimalBlood(pUnit, pPlot):

	pPlayer			= gc.getPlayer(pUnit.getOwner())
	iLair			= pPlot.getImprovementType()
	BloodListExt	= [git('PROMOTION_BEAR_BLOOD'),git('PROMOTION_BOAR_BLOOD'),git('PROMOTION_ELEPHANT_BLOOD'),git('PROMOTION_GORILLA_BLOOD'),git('PROMOTION_GRIFFON_BLOOD'),git('PROMOTION_LION_BLOOD'),git('PROMOTION_RAPTOR_BLOOD'),git('PROMOTION_SCORPION_BLOOD'),git('PROMOTION_SPIDER_BLOOD'),git('PROMOTION_STAG_BLOOD'),git('PROMOTION_TIGER_BLOOD'),git('PROMOTION_WOLF_BLOOD'),git('PROMOTION_WYRM_BLOOD'),git('PROMOTION_SERPENT_BLOOD')]
	if iLair in BearLairs:
		pUnit.setHasPromotion(git('PROMOTION_BEAR_BLOOD'),True)
	elif iLair in RocLairs:
		pUnit.setHasPromotion(git('PROMOTION_GRIFFON_BLOOD'),True)
	elif iLair in LionLairs:
		pUnit.setHasPromotion(git('PROMOTION_LION_BLOOD'),True)
	elif iLair in SpiderLairs:
		pUnit.setHasPromotion(git('PROMOTION_SPIDER_BLOOD'),True)
	elif iLair in WolfLairs:
		pUnit.setHasPromotion(git('PROMOTION_WOLF_BLOOD'),True)
	elif iLair in ScorpionLairs:
		pUnit.setHasPromotion(git('PROMOTION_SCORPION_BLOOD'),True)
	else: # Nature class lairs or animal class lairs that are not in the list
		for iProm in range(gc.getNumPromotionInfos()):
			if pUnit.isHasPromotion(iProm):
				if iProm in BloodListExt:
					BloodListExt.remove(iProm) # Removing duplicate promotions
		if BloodListExt != []:
			iBlood		= BloodListExt[gc.getGame().getSorenRandNum(len(BloodListExt), "Pick Blood Promotion")]
			pUnit.setHasPromotion((iBlood),True)
		else:
			CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_NO_NEW_BLOOD", ()),'AS2D_GOODY_SETTLER',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			RndGold		= gc.getGame().getSorenRandNum(26, "Old Blood")
			pPlayer.changeGold(25+RndGold)

def reqLairAnimalBlood(argsList):
	pUnit, pPlot	= argsList
	iLair			= pPlot.getImprovementType()
	if iLair in BearLairs:
		if pUnit.isHasPromotion(git('PROMOTION_BEAR_BLOOD')):
			return False
	elif iLair in RocLairs:
		if pUnit.isHasPromotion(git('PROMOTION_GRIFFON_BLOOD')):
			return False
	elif iLair in LionLairs:
		if pUnit.isHasPromotion(git('PROMOTION_LION_BLOOD')):
			return False
	elif iLair in SpiderLairs:
		if pUnit.isHasPromotion(git('PROMOTION_SPIDER_BLOOD')):
			return False
	elif iLair in WolfLairs:
		if pUnit.isHasPromotion(git('PROMOTION_WOLF_BLOOD')):
			return False
	elif iLair in ScorpionLairs:
		if pUnit.isHasPromotion(git('PROMOTION_SCORPION_BLOOD')):
			return False
	return True

# GOODY_EXPLORE_LAIR_DEN_LIVESTOCK
def exploreLairLivestock(pUnit, pPlot):

	BonusList		= []
	BonusList.append(git('BONUS_SHEEP'))
	BonusList.append(git('BONUS_COW'))
	BonusList.append(git('BONUS_CAMEL'))
	BonusList.append(git('BONUS_HORSE'))
	BonusList.append(git('BONUS_PIG'))
	BonusList.append(git('BONUS_DEER'))
	BonusList.append(git('BONUS_FUR'))
	BonusList.append(git('BONUS_IVORY'))
	BonusList.append(git('BONUS_BISON'))
	Bonus			= BonusList[gc.getGame().getSorenRandNum(len(BonusList), "Pick Bonus Livestock")]
	pPlot.setBonusType(Bonus)

def reqLairLivestock(argsList):
	pUnit, pPlot	= argsList
	if pPlot.getBonusType(-1) == -1:
		return True
	return False