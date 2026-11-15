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

def canTriggerCondatisDreaming(argsList):
	eTrigger = argsList[0]
	ePlayer = argsList[1]
	iUnit = argsList[2]
	pPlayer = gc.getPlayer(ePlayer)
	pUnit = pPlayer.getUnit(iUnit)
	if pUnit.isHasPromotion(getInfoType('PROMOTION_MASK_OF_THE_COVEN_OF_THE_BLACK_CANDLE_ESUS')):
		return True
	if pUnit.isHasPromotion(getInfoType('PROMOTION_MASK_OF_THE_COVEN_OF_THE_BLACK_CANDLE_BARBATOS')):
		return True
	if pUnit.isHasPromotion(getInfoType('PROMOTION_MASK_OF_THE_COVEN_OF_THE_BLACK_CANDLE_ALEXIS')):
		return True
	if pUnit.isHasPromotion(getInfoType('PROMOTION_MASK_OF_THE_COVEN_OF_THE_BLACK_CANDLE_ASMODAY')):
		return True
	if pUnit.isHasPromotion(getInfoType('PROMOTION_MASK_OF_THE_COVEN_OF_THE_BLACK_CANDLE_FAERYL')):
		return True
	if pUnit.isHasPromotion(getInfoType('PROMOTION_MASK_OF_THE_COVEN_OF_THE_BLACK_CANDLE_GABELLA')):
		return True
	if pUnit.isHasPromotion(getInfoType('PROMOTION_MASK_OF_THE_COVEN_OF_THE_BLACK_CANDLE_KYLORIN')):
		return True
	return False

def doChangeLeaderCondatis1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = CyGlobalContext().getPlayer(iPlayer)
	pPlayer.changeLeader(CyGlobalContext().getInfoTypeForString("LEADER_DREAM_CONDATIS"))

def doChangeLeaderCondatis2(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	iPlayer = kTriggeredData.ePlayer
	pPlayer = CyGlobalContext().getPlayer(iPlayer)
	pPlayer.changeLeader(CyGlobalContext().getInfoTypeForString("LEADER_DREAM_CONDATIS"))

	pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	pUnit.kill(False, -1)

	iCondatis = getInfoType('UNIT_CONDATIS')
	iPromotionMerged = getInfoType('PROMOTION_MERGED_VS')

	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		py = PyPlayer(iPlayer)
		if (pPlayer.isAlive()):
			for pUnit in py.getUnitList():
				if pUnit.getUnitType() == iCondatis:
					pUnit.setHasPromotion(iPromotionMerged, True)
