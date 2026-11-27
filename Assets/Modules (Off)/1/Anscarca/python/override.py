## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

import types
from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CvCameraControls
import CvEventInterface
import random


PyPlayer = PyHelpers.PyPlayer

def warScriptReplacement(self, iPlayer):
		gc 				= CyGlobalContext()
		getPlayer 		= gc.getPlayer
		game 			= CyGame()
		getRank 		= game.getPlayerRank
		getGCounter		= game.getGlobalCounter
		getTeam 		= gc.getTeam
		pPlayer 		= getPlayer(iPlayer)
		Civ				= self.Civilizations
		Rel				= self.Religions
		iCiv 			= pPlayer.getCivilizationType()
		iTeam 			= pPlayer.getTeam()
		iAlignment		= pPlayer.getAlignment()
		Alignment		= self.Alignments
		BuildingClass	= self.BuildingClasses
		Building		= self.Buildings
		iEnemy 			= -1
		WarPlanTotal 	= WarPlanTypes.WARPLAN_TOTAL

		getRandNum 	= game.getSorenRandNum
		for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
			pPlayer2 = getPlayer(iPlayer2)
			if pPlayer2.isAlive():
				iTeam2 = pPlayer2.getTeam()
				pTeam = getTeam(iTeam)
				if pTeam.isAVassal() == False:
					if pTeam.isAtWar(iTeam2):
						randName = "War Script, Player %s vs Player %s" % (iPlayer, iPlayer2)
						if getRandNum(100, randName) < 5:
							self.dogpile(iPlayer, iPlayer2)
					if self.warScriptAllow(iPlayer, iPlayer2):
						getNumB = pPlayer2.getNumBuilding
						if pPlayer2.getBuildingClassMaking(BuildingClass["Tower of Mastery"]) > 0:
							if pTeam.getAtWarCount(True) == 0:
								startWar(iPlayer, iPlayer2, WarPlanTotal)
						if (getNumB(Building["Altar - Divine"]) > 0 or getNumB(Building["Altar - Exalted"]) > 0):
							if iAlignment == Alignment["Evil"]:
								if pTeam.getAtWarCount(True) == 0:
									startWar(iPlayer, iPlayer2, WarPlanTotal)
						if iCiv == Civ["Mercurians"]:
							if pPlayer2.getStateReligion() == Rel["Ashen Veil"]:
								startWar(iPlayer, iPlayer2, WarPlanTotal)
						if getGCounter() > 20:
							if iCiv == Civ["Svartalfar"]:
								if (pPlayer2.getCivilizationType() == Civ["Ljosalfar"] and getRank(iPlayer) > getRank(iPlayer2)):
									startWar(iPlayer, iPlayer2, WarPlanTotal)
							elif iCiv == Civ["Ljosalfar"]:
								if (pPlayer2.getCivilizationType() == Civ["Svartalfar"] and getRank(iPlayer) > getRank(iPlayer2)):
									startWar(iPlayer, iPlayer2, WarPlanTotal)
						if (getGCounter() > 40 or iCiv == Civ["Infernal"] or Civ["Doviello"]):
							if iAlignment == Alignment["Evil"]:
								if (pTeam.getAtWarCount(True) == 0 and getRank(iPlayer2) > getRank(iPlayer)):
									if (iEnemy == -1 or getRank(iPlayer2) > getRank(iEnemy)):
										iEnemy = iPlayer2
						#Special Logic for Anscarca to force wars.
						#For each tier of planet extraction, increase the chance of war
						if gc.getInfoTypeForString("MODULE_ANSCARCA")!=-1:
							anscarcaAgro = 0
							for i in range(1,11):
								anscarcaAgro = anscarcaAgro + getNumB(gc.getInfoTypeForString("BUILDING_PLANETARY_EXTRACTOR_ANSCARCA_" + str(i))) * .1 * i
								if anscarcaAgro == 0: #Break if we don't have any value from first loop since higher tiers require lower tier.
									break
							randName = "War Script, Player %s vs Player %s" % (iPlayer, iPlayer2)
							if anscarcaAgro > 0 and getRandNum(1000, randName) < anscarcaAgro:
								startWar(iPlayer, iPlayer2, WarPlanTotal)
							
		if iEnemy != -1:
			if getRank(iPlayer) > getRank(iEnemy):
				startWar(iPlayer, iEnemy, WarPlanTotal)

def onLoadGame(self, argsList):
	self.cf.warScript = types.MethodType(warScriptReplacement, self.cf)


def onGameStart(self, argsList):
	self.cf.warScript = types.MethodType(warScriptReplacement, self.cf)
