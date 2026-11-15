

from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvDebugTools
import CvWBPopups
import PyHelpers
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import sys
import CvWorldBuilderScreen
import CvAdvisorUtils
import CvTechChooser
import pickle # required for loads

import CvIntroMovieScreen
import CustomFunctions

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo


def onUnitPromoted(self, argsList):
		'Unit Promoted'
		pUnit, iPromotion = argsList
		player = PyPlayer(pUnit.getOwner())


		if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_DISCIPLE'):
			if iPromotion == gc.getInfoTypeForString("PROMOTION_ANCESTRY_AIR"):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR1'), True)
			if iPromotion == gc.getInfoTypeForString("PROMOTION_ANCESTRY_EARTH"):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EARTH1'), True)
			if iPromotion == gc.getInfoTypeForString("PROMOTION_ANCESTRY_FIRE"):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1'), True)
			if iPromotion == gc.getInfoTypeForString("PROMOTION_ANCESTRY_WATER"):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1'), True)
	

