## tribalLawElection.py
## This file applies the effects of each election choice.
## Created by Alsark, 2/3/2018
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

#Global
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

def reqProprietorStealCulture(caster):
	iPlayer	= caster.getOwner()
	pPlayer	= gc.getPlayer(iPlayer)
	pCity = caster.plot().getPlotCity()
	pCapital = pPlayer.getCapitalCity()

	if pCapital.isNone():
		return False

	if pCapital.atPlot(caster.plot()):
		return False

	if pCity.getCultureLevel() < 2:
		return False

	if not pCity.isHasReligion(getInfoType('RELIGION_COUNCIL_OF_ESUS')):
		return False
	return True

def spellProprietorStealCulture(caster):
	pCity = caster.plot().getPlotCity()
	iPlayer2 = pCity.getOwner()
	pPlayer = gc.getPlayer(caster.getOwner())
	pCapital = 	pPlayer.getCapitalCity()

	pCity.changeCulture(iPlayer2, -15, True)

	pCapital.changeCulture(pCapital.getOwner(), 15, True)

def reqProprietorStealGPP(caster):
	iPlayer	= caster.getOwner()
	pPlayer	= gc.getPlayer(iPlayer)
	pCity = caster.plot().getPlotCity()
	pCapital = pPlayer.getCapitalCity()

	if pCapital.isNone():
		return False

	if pCapital.atPlot(caster.plot()):
		return False

	if not pCity.isHasReligion(getInfoType('RELIGION_COUNCIL_OF_ESUS')):
		return False

	if pCity.getGreatPeopleProgress() < 15:
		return False
	return True

def spellProprietorStealGPP(caster):
	pCity = caster.plot().getPlotCity()
	iPlayer2 = pCity.getOwner()
	pPlayer2 = gc.getPlayer(iPlayer2)
	pPlayer = gc.getPlayer(caster.getOwner())
	pCapital = 	pPlayer.getCapitalCity()

	pCity.changeGreatPeopleProgress(-15)

	pCapital.changeGreatPeopleProgress(15)

def reqDeathMerchantArmSmuggling(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if not pCity.isHasReligion(getInfoType('RELIGION_COUNCIL_OF_ESUS')):
		return False

	if pPlayer.isHuman() == False:
		if pPlayer.getStateReligion() != getInfoType('RELIGION_COUNCIL_OF_ESUS'):
			return False
	return True

def reqDeathMerchantWarProfiteering(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if not pCity.isHasReligion(getInfoType('RELIGION_COUNCIL_OF_ESUS')):
		return False

	if pPlayer.isHuman() == False:
		if pPlayer.getStateReligion() != getInfoType('RELIGION_COUNCIL_OF_ESUS'):
			return False
		#I do not trust the AI to use this repsonsibly in their own cities
		if pCity.getOwner() == caster.getOwner():
			return False
	return True

def spellDeathMerchantWarProfiteering(caster):
	pCity = caster.plot().getPlotCity()
	iPlayer2 = pCity.getOwner()
	pPlayer2 = gc.getPlayer(iPlayer2)
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()

	pCity.changeCrime(100)

def reqProprietorCultureBomb(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if pCity.getCrime() < 5:
		return False

	if not pCity.isHasReligion(getInfoType('RELIGION_COUNCIL_OF_ESUS')):
		return False

	if pPlayer.isHuman() == False:
		if pPlayer.getStateReligion() != getInfoType('RELIGION_COUNCIL_OF_ESUS'):
			return False
	return True

def spellProprietorCultureBomb(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())

	iCrime = (int)(pCity.getCrime() / 2)

	pCity.changeCulture(pCity.getOwner(), iCrime, True)

	pCity.changeCrime(-iCrime)

	szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_PROPRIETOR_FORGERY", (iCrime, ))
	CyInterface().addMessage(caster.getOwner(),True,25,szBuffer,'',1,'Modules/NormalModules/XtraEsusUnits/Art/Interface/Buttons/Spells/proprietor1.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

def spellDeathMerchantTradeMission(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())

	iCrime = (int)(pCity.getCrime() / 2)

	pPlayer.changeGold(iCrime)
	pCity.changeCrime(-iCrime)
	szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_DEATH_MERCHANT_TRADE", (iCrime, ))
	CyInterface().addMessage(caster.getOwner(),True,25,szBuffer,'',1,'Modules/NormalModules/XtraEsusUnits/Art/Interface/Buttons/Spells/deathmerchant3.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)

def crimeLordStrength(caster):
	pCity = caster.plot().getWorkingCity()
	iCrime = (int)(pCity.getCrime() / 200)
	iStrength = caster.getStrBoost()

	if iCrime < 0:
		iCrime = 0

	if not pCity.getOwner() == caster.getOwner():
		iCrime = 0

	if iCrime > 3:
		iCrime = 3

	iDif = iCrime - iStrength
	caster.changeStrBoost(iDif)


def crimeLordStrengthRemove(caster):
	pCity = caster.plot().getPlotCity()
	iCrime = (int)(pCity.getCrime() / 200)
	iStrength = caster.getStrBoost()
	iBaseStrength = caster.baseCombatStr()

	if iCrime < 0:
		iCrime = 0

	if iCrime > 3:
		iCrime = 3

	iDif = iCrime - iStrength
	caster.changeStrBoost(iDif)

	if iCrime > 0:
		caster.changeStrBoost(-iCrime)

def crimeLordStrengthUpgraded(caster):
	pCity = caster.plot().getWorkingCity()
	iCrime = (int)(pCity.getCrime() / 200)
	iStrength = caster.getStrBoost()

	if iCrime < 0:
		iCrime = 0

	if iCrime > 3:
		iCrime = 3

	iDif = iCrime - iStrength
	caster.changeStrBoost(iDif)

def reqUpgradeAphoticThrone(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()
	#if pCity.isHasReligion(getInfoType('RELIGION_COUNCIL_OF_ESUS')):
	#	return False

	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_MERCHANT_UPGRADED")):
		return False

	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_SLAVER_UPGRADED")):
		return False

	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_POISONER_UPGRADED")):
		return False

	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_BORED_NOBLE_UPGRADED")):
		return False

	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_FAERYL")):
		return False

	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_FAERYL_UPGRADED_PRIESTHOOD")):
		return False

	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_FAERYL_UPGRADED_COURT")):
		return False

	if pPlayer.isHuman() == False:
		if pPlayer.getStateReligion() != getInfoType('RELIGION_COUNCIL_OF_ESUS'):
			return False

	return True

def spellUpgradeThrone(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()
		
	thrones=["BUILDING_APHOTIC_THRONE_MERCHANT_UPGRADED","BUILDING_APHOTIC_THRONE_SLAVER_UPGRADED","BUILDING_APHOTIC_THRONE_POISONER_UPGRADED","BUILDING_APHOTIC_THRONE_BORED_NOBLE_UPGRADED"]

	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_POISONER")):
		pCity.setNumRealBuilding(getInfoType("BUILDING_APHOTIC_THRONE_POISONER"),0)
		pCity.setNumRealBuilding(getInfoType(thrones[2]),1)
		return
	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_MERCHANT")):
		pCity.setNumRealBuilding(getInfoType("BUILDING_APHOTIC_THRONE_MERCHANT"),0)
		pCity.setNumRealBuilding(getInfoType(thrones[0]),1)
		return
	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_SLAVER")):
		pCity.setNumRealBuilding(getInfoType("BUILDING_APHOTIC_THRONE_SLAVER"),0)
		pCity.setNumRealBuilding(getInfoType(thrones[1]),1)
		return
	if pCity.isHasBuilding(getInfoType("BUILDING_APHOTIC_THRONE_BORED_NOBLE")):
		pCity.setNumRealBuilding(getInfoType("BUILDING_APHOTIC_THRONE_BORED_NOBLE"),0)
		pCity.setNumRealBuilding(getInfoType(thrones[3]),1)
		return

def spellUpgradeThronePriest(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if(pPlayer.getCivilizationType()==getInfoType("CIVILIZATION_SVARTALFAR")):
		pCity.setNumRealBuilding(getInfoType("BUILDING_APHOTIC_THRONE_FAERYL"),0)
		pCity.setNumRealBuilding(getInfoType("BUILDING_APHOTIC_THRONE_FAERYL_UPGRADED_PRIESTHOOD"),1)
		return

def spellUpgradeThroneCourt(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()

	if(pPlayer.getCivilizationType()==getInfoType("CIVILIZATION_SVARTALFAR")):
		pCity.setNumRealBuilding(getInfoType("BUILDING_APHOTIC_THRONE_FAERYL"),0)
		pCity.setNumRealBuilding(getInfoType("BUILDING_APHOTIC_THRONE_FAERYL_UPGRADED_COURT"),1)
		return