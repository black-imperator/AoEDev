# Frozen originally created by TC01
# Updated by Derf for Ashes of Erebus compatibility
# python amended to line up with modular format by LPlate

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
import pickle

import CvIntroMovieScreen
import CustomFunctions


# globals

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
getInfoType = gc.getInfoTypeForString
getPlot	= CyMap().plot

getPlayer = gc.getPlayer

def onUnitKilled(self, argsList):
	'Unit Killed'
	pLoserUnit, iWinnerPlayer = argsList
	
	gc              = CyGlobalContext()
	cf              = self.cf
	getInfoType     = gc.getInfoTypeForString
	map             = CyMap()
	game            = CyGame()
	iLoserPlayer    = pLoserUnit.getOwner()
	attacker        = PyPlayer(iWinnerPlayer)
	player          = PyPlayer(iLoserPlayer) 
	pWinnerPlayer   = gc.getPlayer(iWinnerPlayer)
	pLoserPlayer    = gc.getPlayer(iLoserPlayer)
	iWinnerCiv      = pWinnerPlayer.getCivilizationType()
	iLoserCiv       = pLoserPlayer.getCivilizationType()
	Civ             = self.Civilizations
	Rel             = self.Religions
	Promo           = self.Promotions["Effects"]
	Generic         = self.Promotions["Generic"]
	Race            = self.Promotions["Race"]
	Hero            = self.Heroes
	iLoserUnitRel   = pLoserUnit.getReligion()
	iUnitType       = pLoserUnit.getUnitType()
	iUnitCombat     = pLoserUnit.getUnitCombatType()
	pPlot           = pLoserUnit.plot()
	getPlot         = map.plot
	giftUnit        = cf.giftUnit
	getXP           = pLoserUnit.getExperienceTimes100
	hasPromo        = pLoserUnit.isHasPromotion
	Tech            = self.Techs
	Frozen          = self.Units["Frozen"]
	Building        = self.Buildings
	UnitCombat      = self.UnitCombats
	addMsg          = CyInterface().addMessage
	getText         = CyTranslator().getText
	iNoAI           = UnitAITypes.NO_UNITAI
	iSouth          = DirectionTypes.DIRECTION_SOUTH
	randNum         = CyGame().getSorenRandNum
	iX              = pPlot.getX()
	iY              = pPlot.getY()
	iFrozenSoul = gc.getInfoTypeForString('UNIT_FROZEN_SOUL')

#Added in Frozen: TC01
#	If units with the Winterborn or Wintered promotion die, the Frozen get Frozen Souls.
	if (pLoserUnit.isAlive() and pLoserUnit.isImmortal() == False):
		if (hasPromo( Promo["Winterborn"]) or hasPromo(Promo["Wintered"])): # if victim has promotion winterborn or wintered
			if iLoserCiv != Civ["Frozen"]:
				bValid = True
				if game.countKnownTechNumTeams(Tech["Infernal Pact"]) > 0 and game.getNumCivActive(Civ["Infernal"]) > 0:
					if (iLoserUnitRel in(Rel["Council of Esus"],Rel["Ashen Veil"],Rel["Octopus Overlords"]) or hasPromo(Generic["Death I"]) or hasPromo(Generic["Entropy I"])):
						bValid = False		#We will have already created two Manes, so don't create a Frozen Soul! - To balance Frozen population

				# TODO Ronkhar rewrite all this
				if game.getBuildingClassCreatedCount(Building["Mercurian Gate"]) > 0 and game.getNumCivActive(Civ["Mercurians"]) > 0:
					if (iLoserUnitRel in (Rel["Empyrean"],Rel["Order"],Rel["Runes of Kilmorph"]) or (iUnitCombat == UnitCombat["Animal"] and iLoserCiv == Civ["Mercurians"])):
						bValid = False		#We will have already created an Angel, so don't create a Frozen Soul! 	- To balance Frozen population
				if bValid:
					giftUnit( Frozen["Frozen Souls"], Civ["Frozen"], 0, pPlot, iLoserPlayer)
#End of Frozen
