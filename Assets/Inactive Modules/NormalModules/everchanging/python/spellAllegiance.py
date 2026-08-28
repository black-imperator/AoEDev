
from CvPythonExtensions import *
gc = CyGlobalContext()

def postCombatAllegiance(pCaster, pOpponent):
	player = pOpponent.getOwner()
	pPlayer = gc.getPlayer(player)
	pCity = pPlayer.getCapitalCity()
	iMoreStrength = pCaster.getStrBoost()
	if pCity.isNone():
		iX = pOpponent.getX()
		iY = pOpponent.getY()
	else:
		iX = pCity.getX()
		iY = pCity.getY()
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SAILA'), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.changeStrBoost(iMoreStrength+1)
	# Level and XP must be restored BEFORE copying promotions so that <iMinLevel>
	# gates are evaluated against the level the reborn Saila actually has.
	newUnit.setLevel(pCaster.getLevel())
	newUnit.setExperienceTimes100(pCaster.getExperienceTimes100(), -1)
	# Only ADD promotions the new unit is legally allowed to hold. setHasPromotion()
	# is the raw, unvalidated setter, so blind-copying used to force promotions such
	# as PROMOTION_SPIDER_RHAGODESSA (PrereqUnits = spiders only, and it carries a
	# <NewName>/<UnitArtStyleType>) onto Saila. Nothing is removed here, so the
	# promotions the fresh unit legitimately gained at creation are kept.
	for i in range(gc.getNumPromotionInfos()):
		if not pCaster.isHasPromotion(i):
			continue
		kPromo = gc.getPromotionInfo(i)
		if kPromo.isEquipment():
			continue
		if kPromo.isMustMaintain():
			continue
		if newUnit.isHasPromotion(i):
			continue
		if not newUnit.canAcquirePromotion(i):
			continue
		newUnit.setHasPromotion(i, True)
	newUnit.finishMoves()
	for iPlayer in range(gc.getMAX_PLAYERS()):
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SAILA_FIRST", ()),'',1,'Art/Modules/Everchanging/Buttons/saila.dds',ColorTypes(8),pOpponent.getX(),pOpponent.getY(),True,True)
