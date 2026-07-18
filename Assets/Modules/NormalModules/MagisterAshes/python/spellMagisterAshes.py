## Hamstalf CvSpellInterface.py

from CvPythonExtensions import *
from BasicFunctions import *
from CvSpellInterface import *
import PyHelpers
import CvEventInterface
import CvUtil

PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()
localText = CyTranslator()
getInfoType = gc.getInfoTypeForString

def reqUnleashUnraveling(pCaster, eSpell, sUnit='', iAC=0):
	if pCaster.getReligion() in [ gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL')]:
		iUnit = gc.getInfoTypeForString(sUnit)
		if -1 < iUnit < gc.getNumUnitInfos():
			if CyGame().getUnitCreatedCount(iUnit) == 0:
				if iAC < CyGame().getGlobalCounter():
					iPlayer = pCaster.getOwner()
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
						return True
	return False
	

def helpUnleashUnraveling(lpUnits, eSpell, sUnit='', iAC=0):
	szBuffer = ''
	iUnit = gc.getInfoTypeForString(sUnit)
	if -1 < iUnit < gc.getNumUnitInfos():
		sHelp = helpUnitHelp(iUnit)
		szBuffer += CyTranslator().getText("TXT_KEY_SPELL_SUMMON_UNIT", (sHelp,))
		if iAC > 0:
			sHelp = CyTranslator().getText("TXT_KEY_UNIT_PREREQ_GLOBAL_COUNTER", (iAC,))
			szBuffer += '\n' + sHelp
	return szBuffer

def helpUnleashAbaddon(argsList):
	szBuffer = ''
	iUnit = gc.getInfoTypeForString('UNIT_ABADDON')
	if -1 < iUnit < gc.getNumUnitInfos():
		Unitinfo =GC.getUnitInfo(iUnit)
		szBuffer += CyTranslator().getText("TXT_KEY_SPELL_SUMMON_UNIT", (Unitinfo.getDescription(),))
		if iAC > 0:
			sHelp = CyTranslator().getText("TXT_KEY_UNIT_PREREQ_GLOBAL_COUNTER", (iAC,))
			szBuffer += '\n' + sHelp
	return szBuffer
	
def spellUnleashAbaddon(caster):
	pPlot = caster.plot()
	iUnit = getInfoType('UNIT_ABADDON')
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


def spellUnleashApophis(caster):
	pPlot = caster.plot()
	iUnit = getInfoType('UNIT_APOPHIS')
	pPlayer = gc.getPlayer(caster.getOwner())
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == getInfoType("UNIT_GOAT_2"):
			pUnit.changeImmortal(-100)
			pUnit.kill(False,-1)
	
	newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellUnleashArs(caster):
	pPlot = caster.plot()
	iUnit = getInfoType('UNIT_ARS')
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellUnleashStephanos(caster):
	pPlot = caster.plot()
	iUnit = getInfoType('UNIT_STEPHANOS')
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	pPlot.getPlotCity().setNumRealBuilding(gc.getInfoTypeForString("BUILDING_HERON_THRONE"), 0)

def postCombatCarnivean(pCaster):
	gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_DEAD_CARNIVEAN'),True)

def postCombatBadb(pCaster):
	gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_DEAD_BADB'),True)

def exploreLairUmberguardHostile(pUnit, pPlot):

	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_DWARVEN_DEFENDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UMBERGUARD'),True)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_DWARVEN_DEFENDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(getInfoType('PROMOTION_UMBERGUARD'),True)

def exploreLairUmberguardFriend(pUnit, pPlot):

	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_DWARVEN_DEFENDER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType('PROMOTION_UMBERGUARD'),True)

def reqDiscoverOnceElves(argsList):
	pUnit, pPlot = argsList
	return not (pUnit.isHasPromotion(getInfoType("PROMOTION_SUN3")) or pUnit.isHasPromotion(getInfoType("PROMOTION_METAMAGIC3")))

def reqBreakWiddershinsCurse(argsList):
	pUnit, pPlot = argsList
	return (pUnit.isHasPromotion(getInfoType("PROMOTION_SUN3")) or pUnit.isHasPromotion(getInfoType("PROMOTION_METAMAGIC3")))

def reqNetherBlade(argsList):
	game 		= CyGame()
	pUnit, pPlot = argsList
	return not (game.getNumCivActive(getInfoType("CIVILIZATION_SIDAR"))>0)
	
def exploreLairNetherBlade(pUnit, pPlot):

	pUnit.setHasPromotion(getInfoType("PROMOTION_NETHER_BLADE"),True)
	
def exploreLairOstauriiPatrol(pUnit, pPlot):

	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_OSTAURII_RIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_ONCE_ELF"),True)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_OSTAURII_RIDER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1.setHasPromotion(getInfoType("PROMOTION_ONCE_ELF"),True)

def exploreLairRogueNecromancerBad(pUnit, pPlot):

	pPlayer = gc.getPlayer(pUnit.getOwner())
	bPlayer=gc.getPlayer(gc.getORC_PLAYER())
	pNewPlot = findClearPlot(-1, pPlot)
	newUnit = bPlayer.initUnit(getInfoType('UNIT_NECROMANCER'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_ONCE_ELF"),True)


def exploreLairRogueNecromancerGood(pUnit, pPlot):

	pPlayer = gc.getPlayer(pUnit.getOwner())
	newUnit = pPlayer.initUnit(getInfoType('UNIT_NECROMANCER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.setHasPromotion(getInfoType("PROMOTION_ONCE_ELF"),True)
	

def exploreLairBreakWiddershinsCurse(pUnit, pPlot):

	game 		= CyGame()
	iPlayer = pUnit.getOwner()
	map = CyMap()
	iInfernalPlayer = getOpenPlayer()
	pBestPlot=pPlot
	pPlot.setPythonActive(False)
	if (iInfernalPlayer != -1 and pBestPlot != -1):
		iX = pBestPlot.getX(); iY = pBestPlot.getY()
		pBestPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
		for iiX,iiY in RANGE2:
			getPlot = map.plot
			pPlot2 = getPlot(iX+iiX,iY+iiY)
			for i in xrange(pPlot2.getNumUnits()):
				pLoopUnit = pPlot.getUnit(i)
				if pLoopUnit.getOwner()==gc.getORC_PLAYER() or pLoopUnit.getOwner()==gc.getDEMON_PLAYER() or pLoopUnit.getOwner()==gc.getANIMAL_PLAYER():
					pLoopUnit.kill(False,-1)
		game.addPlayerAdvanced(iInfernalPlayer, -1, getInfoType("LEADER_HAERLOND"), getInfoType("CIVILIZATION_ONCE_ELVES"),iPlayer)
		iFounderTeam  = gc.getPlayer(iPlayer).getTeam()
		eFounderTeam  = gc.getTeam(gc.getPlayer(iPlayer).getTeam())
		iInfernalTeam = gc.getPlayer(iInfernalPlayer).getTeam()
		eInfernalTeam = gc.getTeam(iInfernalTeam)
		for iTech in xrange(gc.getNumTechInfos()):
			if eFounderTeam.isHasTech(iTech):
				eInfernalTeam.setHasTech(iTech, True, iInfernalPlayer, True, False)
		pInfernalPlayer = gc.getPlayer(iInfernalPlayer)
		pInfernalPlayer.AI_changeAttitudeExtra(iPlayer,4)
		pInfernalPlayer.initCity(iX,iY)
		initUnit = pInfernalPlayer.initUnit
		newUnit1  = initUnit(getInfoType("UNIT_WALDRUN"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit1.setExperienceTimes100(2500, -1)
		newUnit2  = initUnit( getInfoType("UNIT_OSTAURII_OFFICER"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit3  = initUnit( getInfoType("UNIT_OSTAURII_OFFICER"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit4  = initUnit( getInfoType("UNIT_OSTAURII"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit5  = initUnit( getInfoType("UNIT_OSTAURII"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit6  = initUnit( getInfoType("UNIT_NECROMANCER"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit7  = initUnit( getInfoType("UNIT_NECROMANCER"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit8  = initUnit( getInfoType("UNIT_OSTAURII_RIDER"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit9  = initUnit( getInfoType("UNIT_OSTAURII_RIDER"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit10  = initUnit( getInfoType("UNIT_WORKER"), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_CONTROL_ONCE_ELVES",()))
			popupInfo.setData1(player)
			popupInfo.setData2(iInfernalPlayer)
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()), "")
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()), "")
			popupInfo.setOnClickedPythonCallback("reassignPlayer")
			popupInfo.addPopup(player)
#		if getPlayer(iPlayer).isHuman() and not game.GetWorldBuilderMode():
#			popupInfo = CyPopupInfo()
#			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
#			popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_CONTROL_INFERNAL",()))
#			popupInfo.setData1(iPlayer)
#			popupInfo.setData2(iInfernalPlayer)
#			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()), "")
#			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()), "")
#			popupInfo.setOnClickedPythonCallback("reassignPlayer")
#			popupInfo.addPopup(iPlayer)
	
def reqUnleashOdio(pCaster, eSpell=-1):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
		return False
	if CyGame().getUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_ODIO')) > 0:
		return False
	return True

def spellUnleashOdio(pCaster, eSpell=-1):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ODIO'), pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	# pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))
	pCaster.plot().setImprovementType(-1)
	bPlayer=gc.getPlayer(gc.getANIMAL_PLAYER())
	pNewPlot = findClearPlot(-1, pCaster.plot())
	newUnit = bPlayer.initUnit(getInfoType('UNIT_EARTH_ELEMENTAL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit1 = bPlayer.initUnit(getInfoType('UNIT_EARTH_ELEMENTAL'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	pTeam = pPlayer.getTeam()
	getPlot	= CyMap().plot
	iRange = 5
	for x, y in plotsInRange( pCaster.getX(), pCaster.getY(), iRange ):
		pPlot = getPlot(x, y)
		if not pPlot.isNone():
			if (pPlot.isCity() or pPlot.getImprovementType() != -1):
				if pPlot.isOwned():
					startWar(pCaster.getOwner(), pPlot.getOwner(), WarPlanTypes.WARPLAN_TOTAL)
			if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				for i in xrange(gc.getNumBuildingInfos()):
					iRnd = CyGame().getSorenRandNum(100, "Earthquake - destory building")
					if (gc.getBuildingInfo(i).getConquestProbability() != 100 and iRnd <= 25):
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


def effectBoneCirclet(pCaster):
	iRnd = CyGame().getSorenRandNum(100,"Bonecirclet wraith")
	if iRnd<3:
		pNewPlot = findClearPlot(-1, pPlot)
		bPlayer=gc.getPlayer(gc.getDEMON_PLAYER())
		newUnit = bPlayer.initUnit(getInfoType('UNIT_WRAITH'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	