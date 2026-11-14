from CvPythonExtensions import *
import FoxTools
from BasicFunctions import *

def onBeginGameTurn(self, argsList):
		'Called at the beginning of the end of each turn'
		iGameTurn = argsList[0]
	
		gc = CyGlobalContext() 
		cf			= self.cf
		game 		= CyGame()
		map 		= CyMap()
		isOption 	= game.isOption
		getPlayer 	= gc.getPlayer
		iOrcPlayer 	= gc.getORC_PLAYER()
		
		iSailaTurn = 1
		isMaxedOut	= game.isUnitClassMaxedOut
		eSpeed		= game.getGameSpeedType()
		Speed		= self.GameSpeeds
		if not isMaxedOut(gc.getInfoTypeForString('UNITCLASS_SAILA'), 0):
			bSaila = False
			if eSpeed == Speed["Quick"]:
				if iGameTurn >= iSailaTurn / 3 * 2: bSaila = True
			elif eSpeed == Speed["Normal"]:
				if iGameTurn >= iSailaTurn: 		 bSaila = True
			elif eSpeed == Speed["Epic"]:
				if iGameTurn >= iSailaTurn * 3 / 2: bSaila = True
			elif eSpeed == Speed["Marathon"]:
				if iGameTurn >= iSailaTurn * 3: 	 bSaila = True
			if bSaila:
				addUnit(gc.getInfoTypeForString('UNIT_SAILA'), iOrcPlayer)