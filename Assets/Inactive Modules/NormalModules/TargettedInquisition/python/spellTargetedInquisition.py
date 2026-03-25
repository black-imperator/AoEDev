#Spell system and FfH specific callout python functions
#All code by Kael, all bugs by woodelf

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import CvScreensInterface
import sys
import PyHelpers
import CustomFunctions
import ScenarioFunctions
import CvEventInterface
import random

PyInfo              = PyHelpers.PyInfo
PyPlayer            = PyHelpers.PyPlayer
gc                  = CyGlobalContext()

getInfoType         = gc.getInfoTypeForString

IEndbringers = ['RELIGION_WHITE_HAND', 'RELIGION_THE_ASHEN_VEIL', 'RELIGION_OCTOPUS_OVERLORDS']

def reqInquisitionAntiEndbringer(caster):
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
	for target in IEndbringers:
		rReligion = getInfoType(target)
		if (StateBelief != rReligion and pCity.isHasReligion(rReligion) and pCity.isHolyCityByType(rReligion) == False):
			return True
	return False

def spellInquisitionAntiEndbringer(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	StateBelief = gc.getPlayer(pCity.getOwner()).getStateReligion()
	iRnd = CyGame().getSorenRandNum(4, "Bob")
	if StateBelief == getInfoType('RELIGION_THE_ORDER'):
		iRnd = iRnd - 1
	for target in IEndbringers:
		rReligion = getInfoType(target)
		if (not StateBelief == rReligion and pCity.isHasReligion(rReligion) and not pCity.isHolyCityByType(rReligion)):
			pCity.setHasReligion(rReligion, False, True, True)
			iRnd = iRnd + 1
			for i in range(gc.getNumBuildingInfos()):
				if gc.getBuildingInfo(i).getPrereqReligion() == rReligion:
					pCity.setNumRealBuilding(i, 0)
	if iRnd >= 1:
		pCity.changeHurryAngerTimer(iRnd)