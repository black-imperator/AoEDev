from CvPythonExtensions import *
from BasicFunctions import *

def onBeginGameTurn(self, argsList):
	'Called at the beginning of the end of each turn'
	iGameTurn	= argsList[0]
	gc			= CyGlobalContext() 
	git			= gc.getInfoTypeForString
	NoggormothaPreviewTurn = 9
	NoggormothaArrivalTurn = 13
	NoggormothaPreview = False
	NoggormothaArrival = False
	if iGameTurn < 45:													# Part of code similar to Orthus spawn in Base game
		if CyGame().getGameSpeedType() == git('GAMESPEED_QUICK'):
			if iGameTurn == NoggormothaPreviewTurn / 3 * 2: NoggormothaPreview = True
			if iGameTurn == NoggormothaArrivalTurn / 3 * 2: NoggormothaArrival = True
		if CyGame().getGameSpeedType() == git('GAMESPEED_NORMAL'):
			if iGameTurn == NoggormothaPreviewTurn: NoggormothaPreview = True
			if iGameTurn == NoggormothaArrivalTurn: NoggormothaArrival = True
		if CyGame().getGameSpeedType() == git('GAMESPEED_EPIC'):
			if iGameTurn == NoggormothaPreviewTurn * 3 / 2: NoggormothaPreview = True
			if iGameTurn == NoggormothaArrivalTurn * 3 / 2: NoggormothaArrival = True
		if CyGame().getGameSpeedType() == git('GAMESPEED_MARATHON'):
			if iGameTurn == NoggormothaPreviewTurn * 3: NoggormothaPreview = True
			if iGameTurn == NoggormothaArrivalTurn * 3: NoggormothaArrival = True
		if NoggormothaPreview:
			for iPlayer in range(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				pCity = pPlayer.getCapitalCity()
				if not pCity.isNone():
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_KEEPER_START_MESSAGE", ()),'',2,'Art/Modules/Noggormotha/Buttons/Keeper_Locate.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
		if NoggormothaArrival:
			addPopup(CyTranslator().getText("TXT_KEY_NKEEPERN_ARRIVAL",()), 'Art/Modules/Noggormotha/Popups/Monastery_banner.dds')
			for iPlayer in range(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				pCity = pPlayer.getCapitalCity()
				if not pCity.isNone():
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_KEEPER_SPAWN_MESSAGE", ()),'',2,'Art/Modules/Noggormotha/Buttons/Toco_Button.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)	
					newUnit = pPlayer.initUnit(git('UNIT_KEEPER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)