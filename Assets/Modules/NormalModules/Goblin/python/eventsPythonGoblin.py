## ArcticNightWolf 29-may-2010
## ArcticNightWolf@gmail.com

import PyHelpers

import FoxDebug
import FoxTools
import time
from BasicFunctions import *
import CustomFunctions

cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
getInfoType = gc.getInfoTypeForString

def canTriggerLukosGames(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	return pCity.getCityClass()==getInfoType("CITYCLASS_LUKOS")
	
def doLukosGames3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	(pLoopCity, iter) = pPlayer.firstCity(false)
	while(pLoopCity):
		if (pLoopCity!=pCity):
			if (pLoopCity.getCityClass()==getInfoType("CITYCLASS_LUKOS")):
				pLoopCity.changeHurryAngerTimer(2)
			else:
				pLoopCity.changeHappinessTimer(10)
		(pLoopCity, iter) = pPlayer.nextCity(iter, false)
			
def canTriggerScorpionSabotage(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	return pCity.getCityClass()==getInfoType("CITYCLASS_SCORPION")
	
def doScorpionSabotage3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	(pLoopCity, iter) = pPlayer.firstCity(false)
	while(pLoopCity):
		if (pLoopCity!=pCity):
			if (pLoopCity.getCityClass()==getInfoType("CITYCLASS_SCORPION")):
				pLoopCity.changeHurryAngerTimer(2)
			else:
				pLoopCity.changeHappinessTimer(10)
		(pLoopCity, iter) = pPlayer.nextCity(iter, false)
	
def canTriggerMurisYouth(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iCity = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pCity = pPlayer.getCity(iCity)
	return pCity.getCityClass()==getInfoType("CITYCLASS_MURIS")
	
def doMurisYouth3(argsList):
	iEvent         = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer        = gc.getPlayer(kTriggeredData.ePlayer)
	pCity          = pPlayer.getCity(kTriggeredData.iCityId)
	(pLoopCity, iter) = pPlayer.firstCity(false)
	while(pLoopCity):
		if (pLoopCity!=pCity):
			if (pLoopCity.getCityClass()==getInfoType("CITYCLASS_MURIS")):
				pLoopCity.changeHurryAngerTimer(2)
			else:
				pLoopCity.changeHappinessTimer(10)
		(pLoopCity, iter) = pPlayer.nextCity(iter, false)