## tribalLawElection.py
## This file applies the effects of each election choice.
## Created by Alsark, 2/3/2018

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
getInfoType			= gc.getInfoTypeForString

Manager             = CvEventInterface.getEventManager()
Bonus               = Manager.Resources
Civ                 = Manager.Civilizations
Trait               = Manager.Traits
Buildings           = Manager.Buildings
UnitCombat          = Manager.UnitCombats
Race                = Manager.Promotions["Race"]
GenericPromo        = Manager.Promotions["Generic"]
Effect              = Manager.Promotions["Effects"]

def onMoveSurfaceTunnel(pCaster, pPlot):
	#gives a promo to a Settler since they do not have a unitcombattype to do so through XML
	if pCaster.getUnitType() == gc.getInfoTypeForString("UNIT_SETTLER"):
		iPromotion = gc.getInfoTypeForString("PROMOTION_MOLEMAN_TUNNEL_SUPPORT_SETTLER")
		iMoleman = gc.getInfoTypeForString("PROMOTION_MOLEMAN")
		if pCaster.isHasPromotion(iMoleman):
			pCaster.setHasPromotion(iPromotion,True)