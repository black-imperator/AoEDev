## Hamstalf CvSpellInterface.py

from CvPythonExtensions import *
import PyHelpers
import CvEventInterface
import CvUtil

PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()
localText = CyTranslator()
getInfoType = gc.getInfoTypeForString

def elvenRacialSelection(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	iElven = getInfoType('PROMOTION_ALFAR_LJOS_EFFECT')
	iDarkElven = getInfoType('PROMOTION_ALFAR_SVART_EFFECT')
	iHamsterCommander = getInfoType('PROMOTION_HAMSTER_COMMANDER')

	if pCaster.isHasPromotion(iElven) or pCaster.isHasPromotion(iDarkElven):
		return

	if pPlayer.getCivilizationType() == getInfoType('CIVILIZATION_HAMSTALFAR'):
		iElvenRace = 50  #Used to determine Elven or Dark Elven status. 50 is neutral, 0 is Dark Elven, 100 is Elven.
		iReconCombat = getInfoType('UNITCOMBAT_RECON')
		iArcherCombat = getInfoType('UNITCOMBAT_ARCHER')
		iAdeptCombat = getInfoType('UNITCOMBAT_ADEPT')
		iDiscipleCombat = getInfoType('UNITCOMBAT_DISCIPLE')

		if pCaster.getUnitCombatType() == iReconCombat:
			iElvenRace -= 25
		if pCaster.getUnitCombatType() == iArcherCombat:
			iElvenRace += 25
		if pCaster.getUnitCombatType() == iAdeptCombat:
			iElvenRace -= 10
		if pCaster.getUnitCombatType() == iDiscipleCombat:
			iElvenRace += 10

		iRnd = CyGame().getSorenRandNum(100, "Racial Selection")
		if iRnd < iElvenRace:
			pCaster.setHasPromotion(iElven, True)
		if iRnd > iElvenRace:
			pCaster.setHasPromotion(iDarkElven, True)
		if iRnd == iElvenRace:
			pCaster.setHasPromotion(iElven, True)
			pCaster.setHasPromotion(iHamsterCommander, True)

def postCombatWonHamsterCommander(pCaster, pOpponent):
	iHamsterCommander = getInfoType('PROMOTION_HAMSTER_COMMANDER')

	iOdds = getCombatOdds(pCaster, pOpponent)

	iOdds = iOdds / 100

	iOdds = 2 - iOdds

	iLevel = pCaster.getLevel()

	iHCOdds = (iLevel * 5) * iOdds

	iRnd = CyGame().getSorenRandNum(100, "Commander Chance")
	if iRnd < iHCOdds:
		pCaster.setHasPromotion(iHamsterCommander, True)

def reqHamsterTrial(caster):
	iHamsterCommander = getInfoType('PROMOTION_HAMSTER_COMMANDER')
	iTrialLeash = getInfoType('PROMOTION_TRIAL_LEASH')

	if caster.isHasPromotion(iHamsterCommander):
		return False
	if caster.isHasPromotion(iTrialLeash):
		return False
	return True

def spellHamsterTrial(caster):
	iHamsterCommander = getInfoType('PROMOTION_HAMSTER_COMMANDER')
	iTrialLeash = getInfoType('PROMOTION_TRIAL_LEASH')

	iRnd = CyGame().getSorenRandNum(100, "Trial Results")

	if iRnd < 15:
		caster.setHasPromotion(iHamsterCommander, True)
	elif iRnd < 85:
		caster.setHasPromotion(iTrialLeash, True)
	else:
		caster.kill(False,-1)

def reqCelvarSpawn(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())

	if pPlayer.getCivCounterMod() > 0:
		return False
	return True

def spellCelvarSpawn(pCaster):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	iEagle = getInfoType('UNIT_CELVAR')

	spawnUnit = pPlayer.initUnit(iEagle, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	spawnUnit.setLeashUnit(pCaster)
	spawnUnit.setLeashRange(4)
	pPlayer.setCivCounterMod(100)