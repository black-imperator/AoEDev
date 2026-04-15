#include "CvGameCoreDLL.h"
#include "CvInfos.h"

//
// Python interface for info classes (formerly structs)
// These are simple enough to be exposed directly - no wrappers
//

void CyInfoPythonInterface1()
{
	OutputDebugString("Python Extension Module - CyInfoPythonInterface1\n");

	python::class_<CvInfoBase>("CvInfoBase")

		.def("isGraphicalOnly", &CvInfoBase::isGraphicalOnly, "bool ()")

		.def("getType", &CvInfoBase::getType, "string ()")
		.def("getButton", &CvInfoBase::getButton, "string ()")

		.def("getTextKey", &CvInfoBase::pyGetTextKey, "wstring ()")
		.def("getText", &CvInfoBase::pyGetText, "wstring ()")
		.def("getDescription", &CvInfoBase::pyGetDescription, "wstring ()")
		.def("getDescriptionForm", &CvInfoBase::pyGetDescriptionForm, "wstring ()")
		.def("getCivilopedia", &CvInfoBase::pyGetCivilopedia, "wstring ()")
		.def("getStrategy", &CvInfoBase::pyGetStrategy, "wstring ()")
		.def("getHelp", &CvInfoBase::pyGetHelp, "wstring ()")
		.def("isMatchForLink", &CvInfoBase::isMatchForLink, "bool (string)")
		;

	python::class_<CvScalableInfo>("CvScalableInfo")
		.def("setScale", &CvScalableInfo::setScale, "void (float fScale)")
		.def("getScale", &CvScalableInfo::getScale, "float  ()")
		;

	python::class_<CvSpecialistInfo, python::bases<CvInfoBase> >("CvSpecialistInfo")
		.def("getGreatPeopleUnitClass", &CvSpecialistInfo::getGreatPeopleUnitClass, "int ()")
		.def("getGreatPeopleRateChange", &CvSpecialistInfo::getGreatPeopleRateChange, "int ()")

		.def("isVisible", &CvSpecialistInfo::isVisible, "bool ()")

		.def("getYieldChange", &CvSpecialistInfo::getYieldChange, "int (int i)")
		.def("getCommerceChange", &CvSpecialistInfo::getCommerceChange, "int (int i)")
		.def("getExperience", &CvSpecialistInfo::getExperience, "int ()")
		.def("getFlavorValue", &CvSpecialistInfo::getFlavorValue, "int (int i)")

		.def("getTexture", &CvSpecialistInfo::getTexture, "string ()")
		;

	python::class_<CvTechInfo, python::bases<CvInfoBase> >("CvTechInfo")
		.def("getAdvisorType", &CvTechInfo::getAdvisorType, "int ()")
		.def("getAIWeight", &CvTechInfo::getAIWeight, "int ()")
		.def("getAITradeModifier", &CvTechInfo::getAITradeModifier, "int ()")
		.def("getResearchCost", &CvTechInfo::getResearchCost, "int ()")
		.def("getEra", &CvTechInfo::getEra, "int ()")
		.def("getTradeRoutes", &CvTechInfo::getTradeRoutes, "int ()")
		.def("getFeatureProductionModifier", &CvTechInfo::getFeatureProductionModifier, "int ()")
		.def("getWorkerSpeedModifier", &CvTechInfo::getWorkerSpeedModifier, "int ()")
		.def("getFirstFreeUnitClass", &CvTechInfo::getFirstFreeUnitClass, "int ()")
		.def("getHealth", &CvTechInfo::getHealth, "int ()")
		.def("getHappiness", &CvTechInfo::getHappiness, "int ()")
		.def("getFirstFreeTechs", &CvTechInfo::getFirstFreeTechs, "int ()")
		.def("getAssetValue", &CvTechInfo::getAssetValue, "int ()")
		.def("getPowerValue", &CvTechInfo::getPowerValue, "int ()")

		.def("getGridX", &CvTechInfo::getGridX, "int ()")
		.def("getGridY", &CvTechInfo::getGridY, "int ()")

		.def("isRepeat", &CvTechInfo::isRepeat, "bool ()")
		.def("isTrade", &CvTechInfo::isTrade, "bool ()")
		.def("isDisable", &CvTechInfo::isDisable, "bool ()")
		.def("isGoodyTech", &CvTechInfo::isGoodyTech, "bool ()")
		.def("isExtraWaterSeeFrom", &CvTechInfo::isExtraWaterSeeFrom, "bool ()")
		.def("isMapCentering", &CvTechInfo::isMapCentering, "bool ()")
		.def("isMapVisible", &CvTechInfo::isMapVisible, "bool ()")
		.def("isMapTrading", &CvTechInfo::isMapTrading, "bool ()")
		.def("isTechTrading", &CvTechInfo::isTechTrading, "bool ()")
		.def("isGoldTrading", &CvTechInfo::isGoldTrading, "bool ()")
		.def("isOpenBordersTrading", &CvTechInfo::isOpenBordersTrading, "bool ()")
		.def("isDefensivePactTrading", &CvTechInfo::isDefensivePactTrading, "bool ()")
		.def("isPermanentAllianceTrading", &CvTechInfo::isPermanentAllianceTrading, "bool ()")
		.def("isVassalStateTrading", &CvTechInfo::isVassalStateTrading, "bool ()")
		.def("isBridgeBuilding", &CvTechInfo::isBridgeBuilding, "bool ()")
		.def("isIrrigation", &CvTechInfo::isIrrigation, "bool ()")
		.def("isIgnoreIrrigation", &CvTechInfo::isIgnoreIrrigation, "bool ()")
		.def("isWaterWork", &CvTechInfo::isWaterWork, "bool ()")
		.def("isRiverTrade", &CvTechInfo::isRiverTrade, "bool ()")

		.def("getQuote", &CvTechInfo::getQuote, "wstring ()")
		.def("getSound", &CvTechInfo::getSound, "string ()")
		.def("getSoundMP", &CvTechInfo::getSoundMP, "string ()")

		.def("getDomainExtraMoves", &CvTechInfo::getDomainExtraMoves, "int (int i)")
		.def("getFlavorValue", &CvTechInfo::getFlavorValue, "int (int i)")
		.def("getPrereqOrTechs", &CvTechInfo::getPrereqOrTechs, "int (int i)")
		.def("getPrereqAndTechs", &CvTechInfo::getPrereqAndTechs, "int (int i)")

		.def("isCommerceFlexible", &CvTechInfo::isCommerceFlexible, "bool (int i)")
		.def("isTerrainTrade", &CvTechInfo::isTerrainTrade, "bool (int i)")
		/*************************************************************************************************/
		/**	New Tag Defs	(TechInfos)				05/15/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("getPrereqBroadAlignment", &CvTechInfo::getPrereqBroadAlignment, "int ()")
		.def("getAlignmentModifier", &CvTechInfo::getAlignmentModifier, "int ()")
		.def("getFirstToTechAlignmentModifier", &CvTechInfo::getFirstToTechAlignmentModifier, "int ()")
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
		/**																								**/
		/**							Adds a new alignment axis to the game								**/
		/*************************************************************************************************/
		.def("getPrereqBroadEthicalAlignment", &CvTechInfo::getPrereqBroadEthicalAlignment, "int ()")
		.def("getEthicalAlignmentModifier", &CvTechInfo::getEthicalAlignmentModifier, "int ()")
		.def("getFirstToTechEthicalAlignmentModifier", &CvTechInfo::getFirstToTechEthicalAlignmentModifier, "int ()")
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments					END												**/
		/*************************************************************************************************/
		.def("getBonusPrereq", &CvTechInfo::getBonusPrereq, "int ()")
		.def("getTechCostShift", &CvTechInfo::getTechCostShift, "int (int i)")
		.def("getBonusCostShift", &CvTechInfo::getBonusCostShift, "int (int i)")
		.def("getTechCostMod", &CvTechInfo::getTechCostMod, "int (int i)")
		.def("getBonusCostMod", &CvTechInfo::getBonusCostMod, "int (int i)")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		/************************************************************************************************/
		/* Influence Driven War                   06/07/10                                 Valkrionn    */
		/*                                                                                              */
		/*						Prevents IDW effects within specific borders                            */
		/************************************************************************************************/
		.def("isInfluenceAllowed", &CvTechInfo::isInfluenceAllowed, "bool ()")
		.def("getVictoryInfluenceModifier", &CvTechInfo::getVictoryInfluenceModifier, "int ()")
		.def("getPillageInfluenceModifier", &CvTechInfo::getPillageInfluenceModifier, "int ()")
		.def("getDefeatInfluenceModifier", &CvTechInfo::getDefeatInfluenceModifier, "int ()")
		/*************************************************************************************************/
		/**	END																							**/
		/*************************************************************************************************/

		;

	python::class_<CvPromotionInfo, python::bases<CvInfoBase> >("CvPromotionInfo")

		.def("getPrereqPromotion", &CvPromotionInfo::getPrereqPromotion, "int ()")
		.def("getPrereqOrPromotion1", &CvPromotionInfo::getPrereqOrPromotion1, "int ()")
		.def("getPrereqOrPromotion2", &CvPromotionInfo::getPrereqOrPromotion2, "int ()")
		.def("getActionInfoIndex", &CvPromotionInfo::getActionInfoIndex, "int ()")
		.def("getAIWeight", &CvPromotionInfo::getAIWeight, "int ()")

		.def("getTechPrereq", &CvPromotionInfo::getTechPrereq, "int ()")
		.def("getStateReligionPrereq", &CvPromotionInfo::getStateReligionPrereq, "int ()")
		.def("getVisibilityChange", &CvPromotionInfo::getVisibilityChange, "int ()")
		.def("getMovesChange", &CvPromotionInfo::getMovesChange, "int ()")
		.def("getMoveDiscountChange", &CvPromotionInfo::getMoveDiscountChange, "int ()")
		.def("getAirRangeChange", &CvPromotionInfo::getAirRangeChange, "int ()")
		.def("getInterceptChange", &CvPromotionInfo::getInterceptChange, "int ()")
		.def("getEvasionChange", &CvPromotionInfo::getEvasionChange, "int ()")
		.def("getWithdrawalChange", &CvPromotionInfo::getWithdrawalChange, "int ()")
		.def("getEnemyWithdrawalChange", &CvPromotionInfo::getEnemyWithdrawalChange, "int ()")
		.def("getCargoChange", &CvPromotionInfo::getCargoChange, "int ()")
		.def("getCollateralDamageChange", &CvPromotionInfo::getCollateralDamageChange, "int ()")
		.def("getBombardRateChange", &CvPromotionInfo::getBombardRateChange, "int ()")
		.def("getFirstStrikesChange", &CvPromotionInfo::getFirstStrikesChange, "int ()")
		.def("getChanceFirstStrikesChange", &CvPromotionInfo::getChanceFirstStrikesChange, "int ()")
		.def("getEnemyHealChange", &CvPromotionInfo::getEnemyHealChange, "int ()")
		.def("getNeutralHealChange", &CvPromotionInfo::getNeutralHealChange, "int ()")
		.def("getFriendlyHealChange", &CvPromotionInfo::getFriendlyHealChange, "int ()")
		.def("getSameTileHealChange", &CvPromotionInfo::getSameTileHealChange, "int ()")
		.def("getAdjacentTileHealChange", &CvPromotionInfo::getAdjacentTileHealChange, "int ()")
		.def("getCombatPercent", &CvPromotionInfo::getCombatPercent, "int ()")
		.def("getCityAttackPercent", &CvPromotionInfo::getCityAttackPercent, "int ()")
		.def("getCityDefensePercent", &CvPromotionInfo::getCityDefensePercent, "int ()")
		.def("getHillsAttackPercent", &CvPromotionInfo::getHillsAttackPercent, "int ()")
		.def("getHillsDefensePercent", &CvPromotionInfo::getHillsDefensePercent, "int ()")
		.def("getCommandType", &CvPromotionInfo::getCommandType, "int ()")
		.def("getRevoltProtection", &CvPromotionInfo::getRevoltProtection, "int ()")
		.def("getCollateralDamageProtection", &CvPromotionInfo::getCollateralDamageProtection, "int ()")
		.def("getPillageChange", &CvPromotionInfo::getPillageChange, "int ()")
		.def("getUpgradeDiscount", &CvPromotionInfo::getUpgradeDiscount, "int ()")
		.def("getExperiencePercent", &CvPromotionInfo::getExperiencePercent, "int ()")
		.def("getKamikazePercent", &CvPromotionInfo::getKamikazePercent, "int ()")

		.def("isLeader", &CvPromotionInfo::isLeader, "bool ()")
		.def("isBlitz", &CvPromotionInfo::isBlitz, "bool ()")
		.def("isAmphib", &CvPromotionInfo::isAmphib, "bool ()")
		.def("isRiver", &CvPromotionInfo::isRiver, "bool ()")
		.def("isEnemyRoute", &CvPromotionInfo::isEnemyRoute, "bool ()")
		.def("isAlwaysHeal", &CvPromotionInfo::isAlwaysHeal, "bool ()")
		.def("isHillsDoubleMove", &CvPromotionInfo::isHillsDoubleMove, "bool ()")
		.def("isImmuneToFirstStrikes", &CvPromotionInfo::isImmuneToFirstStrikes, "bool ()")
		.def("isDispellable", &CvPromotionInfo::isDispellable, "bool ()")

		.def("getSound", &CvPromotionInfo::getSound, "string ()")
		/*************************************************************************************************/
		/**	MobileCage								01/28/2010								Valkrionn	**/
		/**																								**/
		/**										Leashes	a unit to a plot								**/
		/*************************************************************************************************/
		.def("getLeashRange", &CvPromotionInfo::getLeashRange, "int ()")
		.def("getLeashChance", &CvPromotionInfo::getLeashChance, "int ()")
		.def("isLeashed", &CvPromotionInfo::isLeashed, "bool ()")
		/*************************************************************************************************/
		/**	MobileCage									END												**/
		/*************************************************************************************************/
		/*************************************************************************************************/
		/** Shades					  				07/30/10								Valkrionn	**/
		/**																								**/
		/*************************************************************************************************/
		.def("isLeveledImmortality", &CvPromotionInfo::isLeveledImmortality, "bool ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		/*************************************************************************************************/
		/**	New Tag Defs	(PromotionInfos)		05/15/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		/************************************************************************************************/
		/* Influence Driven War                   06/08/10                                 Valkrionn    */
		/*                                                                                              */
		/*						Prevents IDW effects within specific borders                            */
		/************************************************************************************************/
		.def("isNonInfluence", &CvPromotionInfo::isNonInfluence, "bool ()")
		.def("isInfluence", &CvPromotionInfo::isInfluence, "bool ()")
		.def("getVictoryInfluenceModifier", &CvPromotionInfo::getVictoryInfluenceModifier, "int ()")
		.def("getDefeatInfluenceModifier", &CvPromotionInfo::getDefeatInfluenceModifier, "int ()")
		.def("getPillageInfluenceModifier", &CvPromotionInfo::getPillageInfluenceModifier, "int ()")
		/*************************************************************************************************/
		/**	END																							**/
		/*************************************************************************************************/
		.def("getCommandLimit", &CvPromotionInfo::getCommandLimit, "int ()")
		.def("getCommandRange", &CvPromotionInfo::getCommandRange, "int ()")
		.def("getCommandXPShareRate", &CvPromotionInfo::getCommandXPShareRate, "int ()")
		.def("getNumMinionPromotions", &CvPromotionInfo::getNumMinionPromotions, "int ()")
		.def("getMinionPromotion", &CvPromotionInfo::getMinionPromotion, "int (int iI)")
		.def("getNumCommanderPromotions", &CvPromotionInfo::getNumCommanderPromotions, "int ()")
		.def("getCommanderPromotion", &CvPromotionInfo::getCommanderPromotion, "int (int iI)")
		.def("getNumSlavePromotions", &CvPromotionInfo::getNumSlavePromotions, "int ()")
		.def("getSlavePromotion", &CvPromotionInfo::getSlavePromotion, "int (int iI)")
		.def("getNumMasterPromotions", &CvPromotionInfo::getNumMasterPromotions, "int ()")
		.def("getMasterPromotion", &CvPromotionInfo::getMasterPromotion, "int (int iI)")
		.def("getPyPostCombatLost", &CvPromotionInfo::getPyPostCombatLost, "string ()")
		.def("getPyPostCombatWon", &CvPromotionInfo::getPyPostCombatWon, "string ()")
		/*************************************************************************************************/
		/**	PyOnPromoTaken							   08/28/10								Valkrionn	**/
		/*************************************************************************************************/
		.def("getPyOnPromoTaken", &CvPromotionInfo::getPyOnPromoTaken, "string ()")
		/*************************************************************************************************/
		/**	END                                                                   						**/
		/*************************************************************************************************/
		.def("getPyOnRemove", &CvPromotionInfo::getPyOnRemove, "string ()")
		.def("isCommunalProperty", &CvPromotionInfo::isCommunalProperty, "bool ()")
		.def("isNeverHostile", &CvPromotionInfo::isNeverHostile, "bool ()")
		.def("isBlind", &CvPromotionInfo::isBlind, "bool ()")
		.def("isOverrideHelpText", &CvPromotionInfo::isOverrideHelpText, "bool ()")
		.def("isCannotCast", &CvPromotionInfo::isCannotCast, "bool ()")
		.def("isFreeUnit", &CvPromotionInfo::isFreeUnit, "bool ()")
		.def("isNoSupply", &CvPromotionInfo::isNoSupply, "bool ()")
		.def("isTerritorial", &CvPromotionInfo::isTerritorial, "bool ()")
		.def("isRivalTerritoryExplore", &CvPromotionInfo::isRivalTerritoryExplore, "bool ()")
		.def("isRivalTerritoryBlock", &CvPromotionInfo::isRivalTerritoryBlock, "bool ()")
		.def("isPillageOnMove", &CvPromotionInfo::isPillageOnMove, "bool ()")
		.def("isSelfPillage", &CvPromotionInfo::isSelfPillage, "bool ()")
		.def("isGetCasterXP", &CvPromotionInfo::isGetCasterXP, "bool ()")
		.def("isNonWarWeariness", &CvPromotionInfo::isNonWarWeariness, "bool ()")
		.def("isNoMapReveal", &CvPromotionInfo::isNoMapReveal, "bool ()")
		.def("isCannotCapture", &CvPromotionInfo::isCannotCapture, "bool ()")
		.def("isCityHappy", &CvPromotionInfo::isCityHappy, "bool ()")
		.def("isCityNoHappy", &CvPromotionInfo::isCityNoHappy, "bool ()")
		.def("isNoSupport", &CvPromotionInfo::isNoSupport, "bool ()")
		.def("isCanPillage", &CvPromotionInfo::isCanPillage, "bool ()")
		.def("isCannotPillage", &CvPromotionInfo::isCannotPillage, "bool ()")
		.def("isCitySpy", &CvPromotionInfo::isCitySpy, "bool ()")
		.def("isStartGoldenAge", &CvPromotionInfo::isStartGoldenAge, "bool ()")
		.def("isNoDefenseBonus", &CvPromotionInfo::isNoDefenseBonus, "bool ()")
		.def("isMoveImpassable", &CvPromotionInfo::isMoveImpassable, "bool ()")
		.def("isClimbPeaks", &CvPromotionInfo::isClimbPeaks, "bool ()")
		.def("isFlatMoveCost", &CvPromotionInfo::isFlatMoveCost, "bool ()")
		.def("isIgnoreTerrainCosts", &CvPromotionInfo::isIgnoreTerrainCosts, "bool ()")
		.def("isAttackNoWar", &CvPromotionInfo::isAttackNoWar, "bool ()")
		.def("isAllowAttacks", &CvPromotionInfo::isAllowAttacks, "bool ()")
		.def("isFirstStrikeVulnerable", &CvPromotionInfo::isFirstStrikeVulnerable, "bool ()")
		.def("isAllowDefenseBonuses", &CvPromotionInfo::isAllowDefenseBonuses, "bool ()")
		.def("isNonAbandon", &CvPromotionInfo::isNonAbandon, "bool ()")
		.def("isIndependant", &CvPromotionInfo::isIndependant, "bool ()")
		.def("isReligiousCommander", &CvPromotionInfo::isReligiousCommanderPromo, "bool ()") // ReligiousCommander by BI 07/24/11
		.def("isEffectProm", &CvPromotionInfo::isEffectProm, "bool ()")
		.def("isStackEffect", &CvPromotionInfo::isStackEffect, "bool ()")
		/*************************************************************************************************/
		/**	1.4										03/28/11								Valkrionn	**/
		/**																								**/
		/**									New tags required for 1.4									**/
		/*************************************************************************************************/
		.def("getMaxApplications", &CvPromotionInfo::getMaxApplications, "int ()")
		.def("getUnitCombatMaxApplications", &CvPromotionInfo::getUnitCombatMaxApplications, "int (int i)")
		.def("getAntiWithdrawal", &CvPromotionInfo::getAntiWithdrawal, "int ()")
		.def("getAntiFirstStrikes", &CvPromotionInfo::getAntiFirstStrikes, "int ()")
		.def("getPrereqPromotionORs", &CvPromotionInfo::getPrereqPromotionORs, "int (int i, bool bValue)")
		.def("getPrereqPromotionANDs", &CvPromotionInfo::getPrereqPromotionANDs, "int (int i, bool bValue)")
		.def("getNumPrereqPromotionORs", &CvPromotionInfo::getNumPrereqPromotionORs, "int ()")
		.def("getNumPrereqPromotionANDs", &CvPromotionInfo::getNumPrereqPromotionANDs, "int ()")
		.def("getRangedCombatPercent", &CvPromotionInfo::getCombatPercent, "int ()")
		.def("getRangedCombatPercentGlobalCounter", &CvPromotionInfo::getRangedCombatPercentGlobalCounter, "int ()")
		.def("getRangedCombatPercentInBorders", &CvPromotionInfo::getRangedCombatPercentInBorders, "int ()")
		/*************************************************************************************************/
		/**												END												**/
		/*************************************************************************************************/
		.def("isAutoAcquire", &CvPromotionInfo::isAutoAcquire, "bool ()")
		.def("isMustMaintain", &CvPromotionInfo::isMustMaintain, "bool ()")
		.def("isPrereqInCity", &CvPromotionInfo::isPrereqInCity, "bool ()")
		.def("isNoXP", &CvPromotionInfo::isNoXP, "bool ()")
		.def("isPrereqInBorderEnemy", &CvPromotionInfo::isPrereqInBorderEnemy, "bool ()")
		.def("isPrereqInBorderRival", &CvPromotionInfo::isPrereqInBorderRival, "bool ()")
		.def("isPrereqInBorderTeam", &CvPromotionInfo::isPrereqInBorderTeam, "bool ()")
		.def("isPrereqInBorderSelf", &CvPromotionInfo::isPrereqInBorderSelf, "bool ()")
		.def("isPrereqInBorderNone", &CvPromotionInfo::isPrereqInBorderNone, "bool ()")
		.def("isAllowNULLUnitCombat", &CvPromotionInfo::isAllowNULLUnitCombat, "bool ()")
		.def("getRandomApplyChance", &CvPromotionInfo::getRandomApplyChance, "int ()")
		.def("getAssetValue", &CvPromotionInfo::getAssetValue, "int ()")
		/*************************************************************************************************/
		/**	Unit power						17/02/12										Snarko		**/
		/**																								**/
		/**							Rewriting unit power system											**/
		/*************************************************************************************************/
		/**								---- Start Original Code ----									**
				.def("getPowerValue", &CvPromotionInfo::getPowerValue, "int ()")
		/**								----  End Original Code  ----									**/
		.def("getPowerAdd", &CvPromotionInfo::getPowerAdd, "int ()")
		.def("getPowerMult", &CvPromotionInfo::getPowerMult, "int ()")
		/*************************************************************************************************/
		/**	Unit power						END															**/
		/*************************************************************************************************/
		.def("getTempUnitCombat", &CvPromotionInfo::getTempUnitCombat, "int ()")
		.def("getDamageOnRemove", &CvPromotionInfo::getDamageOnRemove, "int ()")
		.def("getFreeXPCap", &CvPromotionInfo::getFreeXPCap, "int ()")
		.def("getCasterXPRate", &CvPromotionInfo::getCasterXPRate, "float ()")
		.def("getDuration", &CvPromotionInfo::getDuration, "int ()")
		.def("getAirCombat", &CvPromotionInfo::getAirCombat, "int ()")
		.def("getAirCombatLimitBoost", &CvPromotionInfo::getAirCombatLimitBoost, "int ()")
		.def("getExtraDropRange", &CvPromotionInfo::getExtraDropRange, "int ()")
		.def("getCombatConversionChance", &CvPromotionInfo::getCombatConversionChance, "int ()")
		.def("getCombatUnitGenerationChance", &CvPromotionInfo::getCombatUnitGenerationChance, "int ()")
		.def("getSlaveGenerationChance", &CvPromotionInfo::getSlaveGenerationChance, "int ()")
		.def("getGiftableXP", &CvPromotionInfo::getGiftableXP, "int ()")
		.def("getCombatExtraDuration", &CvPromotionInfo::getCombatExtraDuration, "int ()")
		.def("getDurationPerTurn", &CvPromotionInfo::getDurationPerTurn, "int ()")
		.def("getDurationAlter", &CvPromotionInfo::getDurationAlter, "int ()")
		.def("getChangeDuration", &CvPromotionInfo::getChangeDuration, "int ()")
		.def("getExtraSupport", &CvPromotionInfo::getExtraSupport, "int ()")
		.def("getChanceMiscast", &CvPromotionInfo::getChanceMiscast, "int ()")
		.def("getCombatDmgCapBoost", &CvPromotionInfo::getCombatDmgCapBoost, "int ()")
		.def("getCollateralLimitCap", &CvPromotionInfo::getCollateralLimitCap, "int ()")
		.def("getCollateralLimitBoost", &CvPromotionInfo::getCollateralLimitBoost, "int ()")
		.def("getCollateralTargetsLimit", &CvPromotionInfo::getCollateralTargetsLimit, "int ()")
		.def("getCollateralExtraTargets", &CvPromotionInfo::getCollateralExtraTargets, "int ()")

		/*************************************************************************************************/
		/**	Updated Flanking						2011-10-30									Jheral	**/
		/**																								**/
		/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
		/*************************************************************************************************/
		.def("getFlankingLimitBoost", &CvPromotionInfo::getFlankingLimitBoost, "int ()")
		.def("getFlankingExtraTargets", &CvPromotionInfo::getFlankingExtraTargets, "int ()")
		/*************************************************************************************************/
		/**	Updated Flanking						END													**/
		/*************************************************************************************************/

		.def("getHammerSacrifice", &CvPromotionInfo::getHammerSacrifice, "int ()")
		.def("getExtraHammerPerPop", &CvPromotionInfo::getExtraHammerPerPop, "int ()")
		.def("getFoodSacrifice", &CvPromotionInfo::getFoodSacrifice, "int ()")
		.def("getPopulationAdd", &CvPromotionInfo::getPopulationAdd, "int ()")
		.def("getBeakerSacrifice", &CvPromotionInfo::getBeakerSacrifice, "int ()")
		.def("getExtraBeakerPerPop", &CvPromotionInfo::getExtraBeakerPerPop, "int ()")
		.def("getGoldSacrifice", &CvPromotionInfo::getGoldSacrifice, "int ()")
		.def("getExtraGoldPerPop", &CvPromotionInfo::getExtraGoldPerPop, "int ()")
		.def("getCultureSacrifice", &CvPromotionInfo::getCultureSacrifice, "int ()")
		.def("getExtraCulturePerPop", &CvPromotionInfo::getExtraCulturePerPop, "int ()")
		.def("getPrereqWeaponTier", &CvPromotionInfo::getPrereqWeaponTier, "int ()")
		.def("getPrereqTier", &CvPromotionInfo::getPrereqTier, "int ()")
		.def("getPrereqMinAge", &CvPromotionInfo::getPrereqMinAge, "int ()")
		.def("getPrereqMaxAge", &CvPromotionInfo::getPrereqMaxAge, "int ()")
		.def("getGoldCost", &CvPromotionInfo::getGoldCost, "int ()")
		.def("getXPTranserRate", &CvPromotionInfo::getXPTranserRate, "int ()")
		.def("getExpireChance", &CvPromotionInfo::getExpireChance, "int ()")
		.def("getNumCityBonuses", &CvPromotionInfo::getNumCityBonuses, "int ()")
		.def("getCityBonus", &CvPromotionInfo::getCityBonus, "CityBonuses (int iI)")
		.def("getYieldFromWin", &CvPromotionInfo::getYieldFromWin, "int (int iI)")
		.def("getYieldForLoss", &CvPromotionInfo::getYieldForLoss, "int (int iI)")
		.def("getCommerceFromWin", &CvPromotionInfo::getCommerceFromWin, "int (int iI)")
		.def("getCommerceForLoss", &CvPromotionInfo::getCommerceForLoss, "int (int iI)")
		.def("getNumPromotionExcludes", &CvPromotionInfo::getNumPromotionExcludes, "int ()")
		.def("getPromotionExcludes", &CvPromotionInfo::getPromotionExcludes, "int (int iI)")
		.def("getNumPromotionOverwrites", &CvPromotionInfo::getNumPromotionOverwrites, "int ()")
		.def("getPromotionOverwrites", &CvPromotionInfo::getPromotionOverwrites, "int (int iI)")
		.def("getNumPromotionReplacedBy", &CvPromotionInfo::getNumPromotionReplacedBy, "int ()")
		.def("getPromotionReplacedBy", &CvPromotionInfo::getPromotionReplacedBy, "int (int iI)")
		.def("getNumPromotionDegradesTo", &CvPromotionInfo::getNumPromotionDegradesTo, "int ()")
		.def("getPromotionDegradesTo", &CvPromotionInfo::getPromotionDegradesTo, "int (int iI)")
		.def("getNumPrereqUnits", &CvPromotionInfo::getNumPrereqUnits, "int ()")
		.def("getPrereqUnit", &CvPromotionInfo::getPrereqUnit, "int (int iI)")
		.def("getNumPrereqReligions", &CvPromotionInfo::getNumPrereqReligions, "int ()")
		.def("getPrereqReligion", &CvPromotionInfo::getPrereqReligion, "int (int iI)")
		.def("getNumPrereqTechANDs", &CvPromotionInfo::getNumPrereqTechANDs, "int ()")
		.def("getPrereqTechAND", &CvPromotionInfo::getPrereqTechAND, "int (int iI)")
		.def("getNumPrereqTechORs", &CvPromotionInfo::getNumPrereqTechORs, "int ()")
		.def("getPrereqTechOR", &CvPromotionInfo::getPrereqTechOR, "int (int iI)")
		.def("getNumPrereqAlignments", &CvPromotionInfo::getNumPrereqAlignments, "int ()")
		.def("getPrereqAlignment", &CvPromotionInfo::getPrereqAlignment, "int (int iI)")
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
		/**																								**/
		/**							Adds a new alignment axis to the game								**/
		/*************************************************************************************************/
		.def("getNumPrereqEthicalAlignments", &CvPromotionInfo::getNumPrereqEthicalAlignments, "int ()")
		.def("getPrereqEthicalAlignment", &CvPromotionInfo::getPrereqEthicalAlignment, "int (int iI)")
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments					END												**/
		/*************************************************************************************************/
		.def("getNumPrereqFeatures", &CvPromotionInfo::getNumPrereqFeatures, "int ()")
		.def("getPrereqFeature", &CvPromotionInfo::getPrereqFeature, "int (int iI)")
		/*************************************************************************************************/
		/**	Second Job							08/28/10									Valkrionn	**/
		/**				Allows units to qualify for the promotions of other UnitCombats					**/
		/*************************************************************************************************/
		.def("getNumSecondaryUnitCombats", &CvPromotionInfo::getNumSecondaryUnitCombats, "int ()")
		.def("getSecondaryUnitCombats", &CvPromotionInfo::getSecondaryUnitCombats, "int (int iI)")
		/*************************************************************************************************/
		/**	TempCombat									END												**/
		/*************************************************************************************************/
		/*************************************************************************************************/
		/**	Better Affinity						01/30/11									Valkrionn	**/
		/**																								**/
		/**					Vastly improved Affinity system, open to many tags							**/
		/*************************************************************************************************/
		.def("getNumAffinities", &CvPromotionInfo::getNumAffinities, "int ()")
		.def("getAffinities", &CvPromotionInfo::getAffinities, "int (int iI)")
		/*************************************************************************************************/
		/**	Better Affinity							END													**/
		/*************************************************************************************************/
		.def("getNumPrereqTerrains", &CvPromotionInfo::getNumPrereqTerrains, "int ()")
		.def("getPrereqTerrain", &CvPromotionInfo::getPrereqTerrain, "int (int iI)")
		.def("getNumPrereqBonusANDs", &CvPromotionInfo::getNumPrereqBonusANDs, "int ()")
		.def("getPrereqBonusAND", &CvPromotionInfo::getPrereqBonusAND, "int (int iI)")
		.def("getNumPrereqBonusORs", &CvPromotionInfo::getNumPrereqBonusORs, "int ()")
		.def("getPrereqBonusOR", &CvPromotionInfo::getPrereqBonusOR, "int (int iI)")
		.def("getNumPrereqCivilizations", &CvPromotionInfo::getNumPrereqCivilizations, "int ()")
		.def("getPrereqCivilization", &CvPromotionInfo::getPrereqCivilization, "int (int iI)")
		.def("getNumPrereqCivics", &CvPromotionInfo::getNumPrereqCivics, "int ()")
		.def("getPrereqCivic", &CvPromotionInfo::getPrereqCivic, "int (int iI)")
		.def("getNumPrereqImprovements", &CvPromotionInfo::getNumPrereqImprovements, "int ()")
		.def("getPrereqImprovement", &CvPromotionInfo::getPrereqImprovement, "int (int iI)")
		.def("getNumPrereqCorporations", &CvPromotionInfo::getNumPrereqCorporations, "int ()")
		.def("getPrereqCorporation", &CvPromotionInfo::getPrereqCorporation, "int (int iI)")
		.def("getNumPrereqTraits", &CvPromotionInfo::getNumPrereqTraits, "int ()")
		.def("getPrereqTrait", &CvPromotionInfo::getPrereqTrait, "int (int iI)")
		.def("getNumPrereqBuildingANDs", &CvPromotionInfo::getNumPrereqBuildingANDs, "int ()")
		.def("getPrereqBuildingAND", &CvPromotionInfo::getPrereqBuildingAND, "int (int iI)")
		.def("getNumPrereqBuildingORs", &CvPromotionInfo::getNumPrereqBuildingORs, "int ()")
		.def("getPrereqBuildingOR", &CvPromotionInfo::getPrereqBuildingOR, "int (int iI)")
		.def("getNumPrereqEventANDs", &CvPromotionInfo::getNumPrereqEventANDs, "int ()")
		.def("getPrereqEventAND", &CvPromotionInfo::getPrereqEventAND, "int (int iI)")
		.def("getNumPrereqEventORs", &CvPromotionInfo::getNumPrereqEventORs, "int ()")
		.def("getPrereqEventOR", &CvPromotionInfo::getPrereqEventOR, "int (int iI)")
		.def("getNumPrereqFeatANDs", &CvPromotionInfo::getNumPrereqFeatANDs, "int ()")
		.def("getPrereqFeatAND", &CvPromotionInfo::getPrereqFeatAND, "int (int iI)")
		.def("getNumPrereqFeatORs", &CvPromotionInfo::getNumPrereqFeatORs, "int ()")
		.def("getPrereqFeatOR", &CvPromotionInfo::getPrereqFeatOR, "int (int iI)")
		.def("getNumPrereqFeatNOTs", &CvPromotionInfo::getNumPrereqFeatNOTs, "int ()")
		.def("getPrereqFeatNOT", &CvPromotionInfo::getPrereqFeatNOT, "int (int iI)")
		.def("getNumInvisibleTypes", &CvPromotionInfo::getNumSeeInvisibleTypes, "int ()")
		.def("getInvisibleType", &CvPromotionInfo::getSeeInvisibleType, "int (int iI)")
		.def("getNumSeeInvisibleTypes", &CvPromotionInfo::getNumSeeInvisibleTypes, "int ()")
		.def("getSeeInvisibleType", &CvPromotionInfo::getSeeInvisibleType, "int (int iI)")
		.def("isRequirePermission", &CvPromotionInfo::isRequirePermission, "bool ()")
		.def("getNumPromotionAllows", &CvPromotionInfo::getNumPromotionAllows, "int ()")
		.def("getPromotionAllows", &CvPromotionInfo::getPromotionAllows, "int (int iI)")
		.def("getNumPrereqUnitTypesOnTile", &CvPromotionInfo::getNumPrereqUnitTypesOnTile, "int ()")
		.def("getPrereqUnitTypeOnTile", &CvPromotionInfo::getPrereqUnitTypeOnTile, "int (int iI)")
		.def("getNumPrereqUnitClassesOnTile", &CvPromotionInfo::getNumPrereqUnitClassesOnTile, "int ()")
		.def("getPrereqUnitClassOnTile", &CvPromotionInfo::getPrereqUnitClassOnTile, "int (int iI)")
		.def("getNumPrereqPromotionsOnTile", &CvPromotionInfo::getNumPrereqPromotionsOnTile, "int ()")
		.def("getPrereqPromotionOnTile", &CvPromotionInfo::getPrereqPromotionOnTile, "int (int iI)")
		.def("getNumPrereqUnitTypesNOTOnTile", &CvPromotionInfo::getNumPrereqUnitTypesNOTOnTile, "int ()")
		/*************************************************************************************************/
		/**	Workers Paradise						01/08/10											**/
		/**																								**/
		/**							Allows promotions to affect build orders							**/
		/*************************************************************************************************/
		.def("getNumPromotionBuilds", &CvPromotionInfo::getNumPromotionBuilds, "int ()")
		.def("getNumPromotionCannotBuilds", &CvPromotionInfo::getNumPromotionCannotBuilds, "int ()")
		/*************************************************************************************************/
		/**	Workers Paradise						END													**/
		/*************************************************************************************************/
		.def("getPrereqUnitTypeNOTOnTile", &CvPromotionInfo::getPrereqUnitTypeNOTOnTile, "int (int iI)")
		.def("getNumPrereqUnitClassesNOTOnTile", &CvPromotionInfo::getNumPrereqUnitClassesNOTOnTile, "int ()")
		.def("getPrereqUnitClassNOTOnTile", &CvPromotionInfo::getPrereqUnitClassNOTOnTile, "int (int iI)")
		.def("getNumPrereqPromotionsNOTOnTile", &CvPromotionInfo::getNumPrereqPromotionsNOTOnTile, "int ()")
		.def("getPrereqPromotionNOTOnTile", &CvPromotionInfo::getPrereqPromotionNOTOnTile, "int (int iI)")
		.def("getNoBadExplore", &CvPromotionInfo::getNoBadExplore, "int ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		// FfH: Added by Kael 08/17/2007
		.def("getBonusPrereq", &CvPromotionInfo::getBonusPrereq, "int ()")
		.def("getMinLevel", &CvPromotionInfo::getMinLevel, "int ()")
		/*************************************************************************************************/
		/**	PrereqStrBoostSize						10/16/09								Valkrionn	**/
		/**																								**/
		/**					Allows a units StrBoost to be used as a promotion prereq					**/
		/*************************************************************************************************/
		.def("getPrereqStrBoostSize", &CvPromotionInfo::getPrereqStrBoostSize, "int ()")
		/*************************************************************************************************/
		/**	PrereqStrBoostSize							END												**/
		/*************************************************************************************************/

		.def("getUnitReligionPrereq", &CvPromotionInfo::getUnitReligionPrereq, "int ()") // PrereqUnitReligion by BI 07/24/11
		.def("getPromotionPrereqAnd", &CvPromotionInfo::getPromotionPrereqAnd, "int ()")
		.def("getPromotionPrereqOr3", &CvPromotionInfo::getPromotionPrereqOr3, "int ()")
		.def("getPromotionPrereqOr4", &CvPromotionInfo::getPromotionPrereqOr4, "int ()")
		.def("getPromotionNextLevel", &CvPromotionInfo::getPromotionNextLevel, "int ()")
		.def("getPyPerTurn", &CvPromotionInfo::getPyPerTurn, "string ()")
		.def("getUnitArtStyleType", &CvPromotionInfo::getUnitArtStyleType, "int ()")
		.def("isEquipment", &CvPromotionInfo::isEquipment, "bool ()")
		.def("isRace", &CvPromotionInfo::isRace, "bool ()")
		// FfH: End Add

		// Arrays

		.def("getTerrainAttackPercent", &CvPromotionInfo::getTerrainAttackPercent, "int (int i)")
		.def("getTerrainDefensePercent", &CvPromotionInfo::getTerrainDefensePercent, "int (int i)")
		.def("getFeatureAttackPercent", &CvPromotionInfo::getFeatureAttackPercent, "int (int i)")
		.def("getFeatureDefensePercent", &CvPromotionInfo::getFeatureDefensePercent, "int (int i)")
		/*************************************************************************************************/
		/**	GWS										2010-08-23									Milaga	**/
		/**																								**/
		/**					Units can have movement modifiers for different terrain						**/
		/*************************************************************************************************/
		.def("getPromotionPeakCost", &CvPromotionInfo::getPromotionPeakCost, "int ()")
		.def("getPromotionHillCost", &CvPromotionInfo::getPromotionHillCost, "int ()")
		.def("getPromotionTerrainCost", &CvPromotionInfo::getPromotionTerrainCost, "int (int i)")
		.def("getPromotionFeatureCost", &CvPromotionInfo::getPromotionFeatureCost, "int (int i)")
		/*************************************************************************************************/
		/**	GWS										END													**/
		/*************************************************************************************************/
		.def("getPromotionClass", &CvPromotionInfo::getPromotionClass, "int()")
		.def("getUnitCombatModifierPercent", &CvPromotionInfo::getUnitCombatModifierPercent, "int (int i)")
		.def("getUnitCombatCaptureRatePercent", &CvPromotionInfo::getUnitCombatCaptureRatePercent, "int (int i)") // Upgraded Capture Rate by BI 08/16/11
		.def("getDomainModifierPercent", &CvPromotionInfo::getDomainModifierPercent, "int (int i)")

		.def("getTerrainDoubleMove", &CvPromotionInfo::getTerrainDoubleMove, "bool (int i)")
		.def("getFeatureDoubleMove", &CvPromotionInfo::getFeatureDoubleMove, "bool (int i)")
		.def("getUnitCombat", &CvPromotionInfo::getUnitCombat, "bool (int i)")
		;

	python::class_<CvMissionInfo, python::bases<CvInfoBase> >("CvMissionInfo")
		.def("getTime", &CvMissionInfo::getTime, "int ()")

		.def("isSound", &CvMissionInfo::isSound, "bool ()")
		.def("isTarget", &CvMissionInfo::isTarget, "bool ()")
		.def("isBuild", &CvMissionInfo::isBuild, "bool ()")
		.def("getVisible", &CvMissionInfo::getVisible, "bool ()")

		.def("getWaypoint", &CvMissionInfo::getWaypoint, "string ()")
		;

	python::class_<CvActionInfo>("CvActionInfo")
		.def("getMissionData", &CvActionInfo::getMissionData, "int ()")
		.def("getCommandData", &CvActionInfo::getCommandData, "int ()")
		.def("getAutomateType", &CvActionInfo::getAutomateType, "int ()")

		.def("getInterfaceModeType", &CvActionInfo::getInterfaceModeType, "int ()")
		.def("getMissionType", &CvActionInfo::getMissionType, "int ()")
		.def("getCommandType", &CvActionInfo::getCommandType, "int ()")
		.def("getControlType", &CvActionInfo::getControlType, "int ()")

		.def("isConfirmCommand", &CvActionInfo::isConfirmCommand, "bool ()")
		.def("isVisible", &CvActionInfo::isVisible, "bool ()")

		.def("getHotKey", &CvActionInfo::getHotKey, "string ()")
		.def("getButton", &CvActionInfo::getButton, "string ()")
		;

	python::class_<CvUnitInfo, python::bases<CvInfoBase, CvScalableInfo> >("CvUnitInfo")

		.def("getAIWeight", &CvUnitInfo::getAIWeight, "int ()")
		.def("getProductionCost", &CvUnitInfo::getProductionCost, "int ()")
		/*************************************************************************************************/
		/**	WeightedCost							 1/30/2010								Valkrionn	**/
		/**																								**/
		/**								Modifies Cost based on Population								**/
		/*************************************************************************************************/
		.def("getCityPopCostModifier", &CvUnitInfo::getCityPopCostModifier, "int ()")
		.def("getEmpirePopCostModifier", &CvUnitInfo::getEmpirePopCostModifier, "int ()")
		.def("getNumCityCostModifier", &CvUnitInfo::getNumCityCostModifier, "int ()")
		/*************************************************************************************************/
		/**	WeightedCost								END												**/
		/*************************************************************************************************/
		.def("getHurryCostModifier", &CvUnitInfo::getHurryCostModifier, "int ()")
		.def("getMinAreaSize", &CvUnitInfo::getMinAreaSize, "int ()")
		.def("getMoves", &CvUnitInfo::getMoves, "int ()")
		.def("getExtraPerception", &CvUnitInfo::getExtraPerception, "int ()")
		.def("getAirRange", &CvUnitInfo::getAirRange, "int ()")
		.def("getAirUnitCap", &CvUnitInfo::getAirUnitCap, "int ()")
		.def("getDropRange", &CvUnitInfo::getDropRange, "int ()")
		.def("getNukeRange", &CvUnitInfo::getNukeRange, "int ()")
		.def("getWorkRate", &CvUnitInfo::getWorkRate, "int ()")
		.def("getBaseDiscover", &CvUnitInfo::getBaseDiscover, "int ()")
		.def("getDiscoverMultiplier", &CvUnitInfo::getDiscoverMultiplier, "int ()")
		.def("getBaseHurry", &CvUnitInfo::getBaseHurry, "int ()")
		.def("getHurryMultiplier", &CvUnitInfo::getHurryMultiplier, "int ()")
		.def("getBaseTrade", &CvUnitInfo::getBaseTrade, "int ()")
		.def("getTradeMultiplier", &CvUnitInfo::getTradeMultiplier, "int ()")
		.def("getGreatWorkCulture", &CvUnitInfo::getGreatWorkCulture, "int ()")
		.def("getEspionagePoints", &CvUnitInfo::getEspionagePoints, "int ()")
		.def("getCombat", &CvUnitInfo::getCombat, "int ()")
		.def("setCombat", &CvUnitInfo::setCombat, "void (int)")
		.def("getCombatLimit", &CvUnitInfo::getCombatLimit, "int ()")
		.def("getAirCombat", &CvUnitInfo::getAirCombat, "int ()")
		.def("getAirCombatLimit", &CvUnitInfo::getAirCombatLimit, "int ()")
		.def("getXPValueAttack", &CvUnitInfo::getXPValueAttack, "int ()")
		.def("getXPValueDefense", &CvUnitInfo::getXPValueDefense, "int ()")
		.def("getFirstStrikes", &CvUnitInfo::getFirstStrikes, "int ()")
		.def("getChanceFirstStrikes", &CvUnitInfo::getChanceFirstStrikes, "int ()")
		.def("getInterceptionProbability", &CvUnitInfo::getInterceptionProbability, "int ()")
		.def("getEvasionProbability", &CvUnitInfo::getEvasionProbability, "int ()")
		.def("getWithdrawalProbability", &CvUnitInfo::getWithdrawalProbability, "int ()")
		.def("getEnemyWithdrawalProbability", &CvUnitInfo::getEnemyWithdrawalProbability, "int ()")
		.def("getCollateralDamage", &CvUnitInfo::getCollateralDamage, "int ()")
		.def("getCollateralDamageLimit", &CvUnitInfo::getCollateralDamageLimit, "int ()")
		.def("getCollateralDamageMaxUnits", &CvUnitInfo::getCollateralDamageMaxUnits, "int ()")

		/*************************************************************************************************/
		/**	Updated Flanking						2011-10-30									Jheral	**/
		/**																								**/
		/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
		/*************************************************************************************************/
		.def("getFlankingDamage", &CvUnitInfo::getFlankingDamage, "int ()")
		.def("getFlankingDamageLimit", &CvUnitInfo::getFlankingDamageLimit, "int ()")
		.def("getFlankingDamageMaxUnits", &CvUnitInfo::getFlankingDamageMaxUnits, "int ()")
		/*************************************************************************************************/
		/**	Updated Flanking						END													**/
		/*************************************************************************************************/

		.def("getCityAttackModifier", &CvUnitInfo::getCityAttackModifier, "int ()")
		.def("getCityDefenseModifier", &CvUnitInfo::getCityDefenseModifier, "int ()")
		.def("getAnimalCombatModifier", &CvUnitInfo::getAnimalCombatModifier, "int ()")
		.def("getHillsAttackModifier", &CvUnitInfo::getHillsAttackModifier, "int ()")
		.def("getHillsDefenseModifier", &CvUnitInfo::getHillsDefenseModifier, "int ()")
		.def("getBombRate", &CvUnitInfo::getBombRate, "int ()")
		.def("getBombardRate", &CvUnitInfo::getBombardRate, "int ()")
		.def("getSpecialCargo", &CvUnitInfo::getSpecialCargo, "int ()")
		.def("getDomainCargo", &CvUnitInfo::getDomainCargo, "int ()")

		.def("getCargoSpace", &CvUnitInfo::getCargoSpace, "int ()")
		.def("getConscriptionValue", &CvUnitInfo::getConscriptionValue, "int ()")
		.def("getCultureGarrisonValue", &CvUnitInfo::getCultureGarrisonValue, "int ()")
		.def("getExtraCost", &CvUnitInfo::getExtraCost, "int ()")
		.def("getAssetValue", &CvUnitInfo::getAssetValue, "int ()")
		/*************************************************************************************************/
		/**	Unit power						17/02/12										Snarko		**/
		/**																								**/
		/**							Rewriting unit power system											**/
		/*************************************************************************************************/
		/**								---- Start Original Code ----									**
				.def("getPowerValue", &CvUnitInfo::getPowerValue, "int ()")
		/**								----  End Original Code  ----									**/
		.def("getPowerAdd", &CvUnitInfo::getPowerAdd, "int ()")
		.def("getPowerMult", &CvUnitInfo::getPowerMult, "int ()")
		/*************************************************************************************************/
		/**	Unit power						END															**/
		/*************************************************************************************************/

		.def("getMagicalPower", &CvUnitInfo::getMagicalPower, "int ()")

		.def("getUnitClassType", &CvUnitInfo::getUnitClassType, "int ()")
		.def("getSpecialUnitType", &CvUnitInfo::getSpecialUnitType, "int ()")
		.def("getUnitCaptureClassType", &CvUnitInfo::getUnitCaptureClassType, "int ()")
		.def("getUnitCombatType", &CvUnitInfo::getUnitCombatType, "int ()")
		.def("getDomainType", &CvUnitInfo::getDomainType, "int ()")
		.def("getDefaultUnitAIType", &CvUnitInfo::getDefaultUnitAIType, "int ()")
		/*************************************************************************************************/
		/**	CandyMan								04/04/09								Xienwolf	**/
		/**																								**/
		/**							Allows Multiple Invisible types on a Unit							**/
		/*************************************************************************************************/
		/**								---- Start Original Code ----									**
				.def("getInvisibleType", &CvUnitInfo::getInvisibleType, "int ()")
		/**								----  End Original Code  ----									**/
		.def("getNumInvisibleTypes", &CvUnitInfo::getNumSeeInvisibleTypes, "int ()")
		.def("getInvisibleType", &CvUnitInfo::getSeeInvisibleType, "int (int)")
		/*************************************************************************************************/
		/**	CandyMan								END													**/
		/*************************************************************************************************/
		.def("getNumSeeInvisibleTypes", &CvUnitInfo::getNumSeeInvisibleTypes, "int ()")
		.def("getSeeInvisibleType", &CvUnitInfo::getSeeInvisibleType, "int (int)")
		.def("getAdvisorType", &CvUnitInfo::getAdvisorType, "int ()")
		.def("getHolyCity", &CvUnitInfo::getHolyCity, "int ()")
		.def("getReligionType", &CvUnitInfo::getReligionType, "int ()")
		.def("getStateReligion", &CvUnitInfo::getStateReligion, "int ()")
		.def("getPrereqReligion", &CvUnitInfo::getPrereqReligion, "int ()")
		.def("getPrereqCorporation", &CvUnitInfo::getPrereqCorporation, "int ()")
		.def("getPrereqBuilding", &CvUnitInfo::getPrereqBuilding, "int ()")
		.def("getPrereqAndTech", &CvUnitInfo::getPrereqAndTech, "int ()")
		.def("getPrereqAndBonus", &CvUnitInfo::getPrereqAndBonus, "int ()")
		.def("getGroupSize", &CvUnitInfo::getGroupSize, "int ()")
		.def("getGroupDefinitions", &CvUnitInfo::getGroupDefinitions, "int ()")
		.def("getMeleeWaveSize", &CvUnitInfo::getMeleeWaveSize, "int ()")
		.def("getRangedWaveSize", &CvUnitInfo::getRangedWaveSize, "int ()")
		.def("getNumUnitNames", &CvUnitInfo::getNumUnitNames, "int ()")
		.def("getCommandType", &CvUnitInfo::getCommandType, "int ()")

		.def("isAnimal", &CvUnitInfo::isAnimal, "bool ()")
		.def("isFoodProduction", &CvUnitInfo::isFoodProduction, "bool ()")
		.def("isNoBadGoodies", &CvUnitInfo::isNoBadGoodies, "bool ()")
		/************************************************************************************************/
		/* UNOFFICIAL_PATCH                       03/20/10                       Afforess & jdog5000    */
		/*                                                                                              */
		/* Bugfix                                                                                       */
		/************************************************************************************************/
		.def("isOnlyDefensive", &CvUnitInfo::isOnlyDefensive, "bool ()")
		/************************************************************************************************/
		/* UNOFFICIAL_PATCH                        END                                                  */
		/************************************************************************************************/
		.def("isCannotCapture", &CvUnitInfo::isCannotCapture, "bool ()")
		.def("isImmuneToCapture", &CvUnitInfo::isImmuneToCapture, "bool ()")
		.def("isRivalTerritory", &CvUnitInfo::isRivalTerritory, "bool ()")
		.def("isMilitaryHappiness", &CvUnitInfo::isMilitaryHappiness, "bool ()")
		.def("isMilitarySupport", &CvUnitInfo::isMilitarySupport, "bool ()")
		.def("isMilitaryProduction", &CvUnitInfo::isMilitaryProduction, "bool ()")
		.def("isPillage", &CvUnitInfo::isPillage, "bool ()")
		.def("isReligiousCommander", &CvUnitInfo::isReligiousCommander, "bool ()") // ReligiousCommander by BI 07/24/11
		.def("isSpy", &CvUnitInfo::isSpy, "bool ()")
		.def("isSabotage", &CvUnitInfo::isSabotage, "bool ()")
		.def("isDestroy", &CvUnitInfo::isDestroy, "bool ()")
		.def("isStealPlans", &CvUnitInfo::isStealPlans, "bool ()")
		.def("isInvestigate", &CvUnitInfo::isInvestigate, "bool ()")
		.def("isCounterSpy", &CvUnitInfo::isCounterSpy, "bool ()")
		.def("isFound", &CvUnitInfo::isFound, "bool ()")
		.def("isGoldenAge", &CvUnitInfo::isGoldenAge, "bool ()")
		.def("isInvisible", &CvUnitInfo::isInvisible, "bool ()")
		.def("setInvisible", &CvUnitInfo::setInvisible, "void (bool bEnable)")
		.def("isFirstStrikeImmune", &CvUnitInfo::isFirstStrikeImmune, "bool ()")
		.def("isNoDefensiveBonus", &CvUnitInfo::isNoDefensiveBonus, "bool ()")
		.def("isIgnoreBuildingDefense", &CvUnitInfo::isIgnoreBuildingDefense, "bool ()")
		.def("isCanMoveImpassable", &CvUnitInfo::isCanMoveImpassable, "bool ()")
		.def("isCanMoveAllTerrain", &CvUnitInfo::isCanMoveAllTerrain, "bool ()")
		.def("isFlatMovementCost", &CvUnitInfo::isFlatMovementCost, "bool ()")
		.def("isIgnoreTerrainCost", &CvUnitInfo::isIgnoreTerrainCost, "bool ()")
		.def("isNukeImmune", &CvUnitInfo::isNukeImmune, "bool ()")
		.def("isPrereqBonuses", &CvUnitInfo::isPrereqBonuses, "bool ()")
		.def("isPrereqReligion", &CvUnitInfo::isPrereqReligion, "bool ()")
		.def("isMechUnit", &CvUnitInfo::isMechUnit, "bool ()")
		.def("isRenderBelowWater", &CvUnitInfo::isRenderBelowWater, "bool ()")
		.def("isSuicide", &CvUnitInfo::isSuicide, "bool ()")
		.def("isHiddenNationality", &CvUnitInfo::isHiddenNationality, "bool ()")
		.def("isAlwaysHostile", &CvUnitInfo::isAlwaysHostile, "bool ()")

		.def("getUnitMaxSpeed", &CvUnitInfo::getUnitMaxSpeed, "float ()")
		.def("getUnitPadTime", &CvUnitInfo::getUnitPadTime, "float ()")

		/*************************************************************************************************/
		/**	New Tag Defs	(UnitInfos)				05/15/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("getMinLevel", &CvUnitInfo::getMinLevel, "int ()")
		/************************************************************************************************/
		/* Influence Driven War                   06/08/10                                 Valkrionn    */
		/*                                                                                              */
		/*						Prevents IDW effects within specific borders                            */
		/************************************************************************************************/
		.def("isNonInfluence", &CvUnitInfo::isNonInfluence, "bool ()")
		.def("isInfluence", &CvUnitInfo::isInfluence, "bool ()")
		.def("getVictoryInfluenceModifier", &CvUnitInfo::getVictoryInfluenceModifier, "int ()")
		.def("getDefeatInfluenceModifier", &CvUnitInfo::getDefeatInfluenceModifier, "int ()")
		.def("getPillageInfluenceModifier", &CvUnitInfo::getPillageInfluenceModifier, "int ()")
		/*************************************************************************************************/
		/**	END																							**/
		/*************************************************************************************************/
		.def("getCommandLimit", &CvUnitInfo::getCommandLimit, "int ()")
		.def("getCommandRange", &CvUnitInfo::getCommandRange, "int ()")
		.def("isFreeUnit", &CvUnitInfo::isFreeUnit, "bool ()")
		/*************************************************************************************************/
		/**	Workers Paradise						01/08/10											**/
		/**																								**/
		/**							Allows promotions to affect build orders							**/
		/*************************************************************************************************/
		.def("isPromotionBuild", &CvUnitInfo::isPromotionBuild, "bool ()")
		/*************************************************************************************************/
		/**	Workers Paradise						END													**/
		/*************************************************************************************************/
		.def("isNoSupply", &CvUnitInfo::isNoSupply, "bool ()")
		.def("getUnitCreateFromCombat", &CvUnitInfo::getUnitCreateFromCombat, "int ()")
		.def("isCommunalProperty", &CvUnitInfo::isCommunalProperty, "bool ()")
		.def("isNeverHostile", &CvUnitInfo::isNeverHostile, "bool ()")
		.def("isBlind", &CvUnitInfo::isBlind, "bool ()")
		.def("getPrereqBroadAlignment", &CvUnitInfo::getPrereqBroadAlignment, "int ()")
		.def("getAlignmentModifier", &CvUnitInfo::getAlignmentModifier, "int ()")
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
		/**																								**/
		/**							Adds a new alignment axis to the game								**/
		/*************************************************************************************************/
		.def("getPrereqBroadEthicalAlignment", &CvUnitInfo::getPrereqBroadEthicalAlignment, "int ()")
		.def("getEthicalAlignmentModifier", &CvUnitInfo::getEthicalAlignmentModifier, "int ()")
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments					END												**/
		/*************************************************************************************************/
		.def("getPyPerTurn", &CvUnitInfo::getPyPerTurn, "string ()")
		.def("isAllowPromotion", &CvUnitInfo::isAllowPromotion, "bool (int /*PromotionTypes*/ ePromotion)")
		.def("isDenyPromotion", &CvUnitInfo::isDenyPromotion, "bool (int /*PromotionTypes*/ ePromotion)")
		.def("getPyDeath", &CvUnitInfo::getPyDeath, "string ()")
		.def("getQuote", &CvUnitInfo::getQuote, "string ()")
		.def("getNumQuotes", &CvUnitInfo::getNumQuotes, "int ()")
		.def("getQuotes", &CvUnitInfo::getQuotes, "string (int i)")
		.def("getNumImages", &CvUnitInfo::getNumImages, "int ()")
		.def("getImages", &CvUnitInfo::getImages, "string (int i)")
		.def("isCanClimbPeaks", &CvUnitInfo::isCanClimbPeaks, "bool ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		/*************************************************************************************************/
		/** Feral Animals			  				10/19/09								Valkrionn	**/
		/**																								**/
		/*************************************************************************************************/
		.def("getAppearanceProb", &CvUnitInfo::getAppearanceProb, "int ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		// FfH: Added by Kael 03/01/2008
		.def("getCombatDefense", &CvUnitInfo::getCombatDefense, "int ()")
		.def("getEquipmentPromotion", &CvUnitInfo::getEquipmentPromotion, "int ()")
		.def("getImage", &CvUnitInfo::getImage, "wstring ()")
		.def("getPrereqBuildingClass", &CvUnitInfo::getPrereqBuildingClass, "int ()")
		.def("getPrereqCivic", &CvUnitInfo::getPrereqCivic, "int ()")
		// PyPreCombat by BI 07/24/11
		.def("getPyPreCombat", &CvUnitInfo::getPyPreCombat, "string ()")

		.def("getPyPostCombatLost", &CvUnitInfo::getPyPostCombatLost, "string ()")
		.def("getPyPostCombatWon", &CvUnitInfo::getPyPostCombatWon, "string ()")
		.def("getTier", &CvUnitInfo::getTier, "int ()")
		/*************************************************************************************************/
		/**	Tierable								04/04/09								Xienwolf	**/
		/**																								**/
		/**							Allows for Multiple sets of WeaponTiers								**/
		/*************************************************************************************************/
		/**								---- Start Original Code ----									**
				.def("getWeaponTier", &CvUnitInfo::getWeaponTier, "int ()")
		/**								----  End Original Code  ----									**/
		.def("getWeaponTierMax", &CvUnitInfo::getWeaponTierMax, "int ()")
		.def("getWeaponTierMin", &CvUnitInfo::getWeaponTierMin, "int ()")
		/*************************************************************************************************/
		/**	Tierable								END													**/
		/*************************************************************************************************/
		.def("isAbandon", &CvUnitInfo::isAbandon, "bool ()")
		.def("isDisableUpgradeTo", &CvUnitInfo::isDisableUpgradeTo, "bool ()")
		// FfH: End Add

		// Arrays

		.def("getPrereqAndTechs", &CvUnitInfo::getPrereqAndTechs, "int (int i)")
		.def("getPrereqOrBonuses", &CvUnitInfo::getPrereqOrBonuses, "int (int i)")
		.def("getProductionTraits", &CvUnitInfo::getProductionTraits, "int (int i)")
		/*************************************************************************************************/
		/** Feral Animals			  				10/19/09								Valkrionn	**/
		/**																								**/
		/*************************************************************************************************/
		.def("getAppearanceTechs", &CvUnitInfo::getAppearanceTechs, "int (int i)")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		.def("getFlavorValue", &CvUnitInfo::getFlavorValue, "int (int i)")
		.def("getTerrainAttackModifier", &CvUnitInfo::getTerrainAttackModifier, "int (int i)")
		.def("getTerrainDefenseModifier", &CvUnitInfo::getTerrainDefenseModifier, "int (int i)")
		.def("getFeatureAttackModifier", &CvUnitInfo::getFeatureAttackModifier, "int (int i)")
		.def("getFeatureDefenseModifier", &CvUnitInfo::getFeatureDefenseModifier, "int (int i)")
		/*************************************************************************************************/
		/**	GWS										2010-08-23									Milaga	**/
		/**																								**/
		/**					Units can have movement modifiers for different terrain						**/
		/*************************************************************************************************/
		.def("getUnitPeakCost", &CvUnitInfo::getUnitPeakCost, "int ()")
		.def("getUnitHillCost", &CvUnitInfo::getUnitHillCost, "int ()")
		.def("getUnitTerrainCost", &CvUnitInfo::getUnitTerrainCost, "int (int i)")
		.def("getUnitFeatureCost", &CvUnitInfo::getUnitFeatureCost, "int (int i)")
		/*************************************************************************************************/
		/**	GWS										END													**/
		/*************************************************************************************************/
		.def("getUnitClassAttackModifier", &CvUnitInfo::getUnitClassAttackModifier, "int (int i)")
		.def("getUnitClassDefenseModifier", &CvUnitInfo::getUnitClassDefenseModifier, "int (int i)")
		.def("getUnitCombatModifier", &CvUnitInfo::getUnitCombatModifier, "int (int i)")
		.def("getDomainModifier", &CvUnitInfo::getDomainModifier, "int (int i)")
		.def("getBonusProductionModifier", &CvUnitInfo::getBonusProductionModifier, "int (int i)")
		.def("getUnitGroupRequired", &CvUnitInfo::getUnitGroupRequired, "int (int i)")
		/*************************************************************************************************/
		/**	Speedup								12/02/12										Snarko	**/
		/**																								**/
		/**			Only store the unitclasses we upgrade to, for faster looping						**/
		/*************************************************************************************************/
		.def("getNumUpgradeUnitClass", &CvUnitInfo::getNumUpgradeUnitClass, "int ()")
		/*************************************************************************************************/
		/**	Speedup									END													**/
		/*************************************************************************************************/
		.def("getUpgradeUnitClass", &CvUnitInfo::getUpgradeUnitClass, "bool (int i)")
		.def("getTargetUnitClass", &CvUnitInfo::getTargetUnitClass, "bool (int i)")
		.def("getTargetUnitCombat", &CvUnitInfo::getTargetUnitCombat, "bool (int i)")
		.def("getDefenderUnitClass", &CvUnitInfo::getDefenderUnitClass, "bool (int i)")
		.def("getDefenderUnitCombat", &CvUnitInfo::getDefenderUnitCombat, "bool (int i)")
		.def("getUnitAIType", &CvUnitInfo::getUnitAIType, "bool (int i)")
		.def("getNotUnitAIType", &CvUnitInfo::getNotUnitAIType, "bool (int i)")
		.def("getBuilds", &CvUnitInfo::getBuilds, "bool (int i)")
		.def("getReligionSpreads", &CvUnitInfo::getReligionSpreads, "int (int i)")
		.def("getCorporationSpreads", &CvUnitInfo::getCorporationSpreads, "int (int i)")
		.def("getTerrainPassableTech", &CvUnitInfo::getTerrainPassableTech, "int (int i)")
		.def("getFeaturePassableTech", &CvUnitInfo::getFeaturePassableTech, "int (int i)")
		/*************************************************************************************************/
		/**	Updated Flanking						2011-10-30									Jheral	**/
		/**																								**/
		/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
		/*************************************************************************************************/
		// Old: .def("getFlankingStrikeUnitClass", &CvUnitInfo::getFlankingStrikeUnitClass, "int (int i)")
		.def("getFlankingStrikeUnitCombat", &CvUnitInfo::getFlankingStrikeUnitCombat, "int (int i)")
		/*************************************************************************************************/
		/**	Updated Flanking						END													**/
		/*************************************************************************************************/
		.def("getGreatPeoples", &CvUnitInfo::getGreatPeoples, "bool (int i)")
		.def("getBuildings", &CvUnitInfo::getBuildings, "bool (int i)")
		.def("getTerrainImpassable", &CvUnitInfo::getTerrainImpassable, "bool (int i)")
		.def("getFeatureImpassable", &CvUnitInfo::getFeatureImpassable, "bool (int i)")
		.def("getTerrainNative", &CvUnitInfo::getTerrainNative, "bool (int i)")
		.def("getFeatureNative", &CvUnitInfo::getFeatureNative, "bool (int i)")
		/*************************************************************************************************/
		/**	JRouteNative by Jeckel		imported by Valkrionn	09.28.09                        		**/
		/*************************************************************************************************/
		.def("getRouteNative", &CvUnitInfo::getRouteNative, "bool (int iRouteType)")
		.def("getRouteImpassable", &CvUnitInfo::getRouteImpassable, "bool (int iRouteType)")
		.def("getRouteIgnore", &CvUnitInfo::getRouteIgnore, "bool (int iRouteType)")
		.def("getRouteSubstitute", &CvUnitInfo::getRouteSubstitute, "int (int iRouteType)")
		/*************************************************************************************************/
		/**	JRouteNative    END                                                                   		**/
		/*************************************************************************************************/
		.def("getFreePromotions", &CvUnitInfo::getFreePromotions, "bool (int i)")
		/*************************************************************************************************/
		/**	1.4										03/28/11								Valkrionn	**/
		/**																								**/
		/**									New tags required for 1.4									**/
		/*************************************************************************************************/
		.def("getNumFreePromotions", &CvUnitInfo::getNumFreePromotions, "int (int i)")
		/*************************************************************************************************/
		/**												END												**/
		/*************************************************************************************************/
		.def("getLeaderPromotion", &CvUnitInfo::getLeaderPromotion, "int ()")
		.def("getLeaderExperience", &CvUnitInfo::getLeaderExperience, "int ()")

		.def("getEarlyArtDefineTag", &CvUnitInfo::getEarlyArtDefineTag, "string (int i, UnitArtStyleTypes eStyle)")
		.def("getLateArtDefineTag", &CvUnitInfo::getLateArtDefineTag, "string (int i, UnitArtStyleTypes eStyle)")
		.def("getMiddleArtDefineTag", &CvUnitInfo::getMiddleArtDefineTag, "string (int i, UnitArtStyleTypes eStyle)")

		// FfH: Added by Kael 02/06/2009
		.def("getUnitStyleButton", &CvUnitInfo::getUnitStyleButton, "string (int iProm)")
		// FfH: End Add

		.def("getUnitNames", &CvUnitInfo::getUnitNames, "string (int i)")
		.def("getArtInfo", &CvUnitInfo::getArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoUnit* (int i, bool bLate)")
		;

	python::class_<CvSpecialUnitInfo, python::bases<CvInfoBase> >("CvSpecialUnitInfo")
		.def("isValid", &CvSpecialUnitInfo::isValid, "bool ()")
		.def("isCityLoad", &CvSpecialUnitInfo::isCityLoad, "bool ()")

		.def("isCarrierUnitAIType", &CvSpecialUnitInfo::isCarrierUnitAIType, "bool (int i)")
		.def("getProductionTraits", &CvSpecialUnitInfo::getProductionTraits, "int (int i)")
		/*************************************************************************************************/
		/** Feral Animals			  				10/19/09								Valkrionn	**/
		/**																								**/
		/*************************************************************************************************/
		.def("getAppearanceTechs", &CvSpecialUnitInfo::getAppearanceTechs, "int (int i)")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		;

	python::class_<CvCivicOptionInfo, python::bases<CvInfoBase> >("CvCivicOptionInfo")
		.def("getTraitNoUpkeep", &CvCivicOptionInfo::getTraitNoUpkeep, "bool (int i)")
		;

	python::class_<CvCivicInfo, python::bases<CvInfoBase> >("CvCivicInfo")

		.def("getCivicOptionType", &CvCivicInfo::getCivicOptionType, "int ()")
		.def("getAnarchyLength", &CvCivicInfo::getAnarchyLength, "int ()")
		.def("getUpkeep", &CvCivicInfo::getUpkeep, "int ()")
		.def("getAIWeight", &CvCivicInfo::getAIWeight, "int ()")
		.def("getGreatPeopleRateModifier", &CvCivicInfo::getGreatPeopleRateModifier, "int ()")
		.def("getGreatGeneralRateModifier", &CvCivicInfo::getGreatGeneralRateModifier, "int ()")
		.def("getDomesticGreatGeneralRateModifier", &CvCivicInfo::getDomesticGreatGeneralRateModifier, "int ()")
		.def("getStateReligionGreatPeopleRateModifier", &CvCivicInfo::getStateReligionGreatPeopleRateModifier, "int ()")
		.def("getDistanceMaintenanceModifier", &CvCivicInfo::getDistanceMaintenanceModifier, "int ()")
		.def("getNumCitiesMaintenanceModifier", &CvCivicInfo::getNumCitiesMaintenanceModifier, "int ()")
		.def("getCorporationMaintenanceModifier", &CvCivicInfo::getCorporationMaintenanceModifier, "int ()")
		.def("getExtraHealth", &CvCivicInfo::getExtraHealth, "int ()")
		.def("getFreeExperience", &CvCivicInfo::getFreeExperience, "int ()")
		.def("getWorkerSpeedModifier", &CvCivicInfo::getWorkerSpeedModifier, "int ()")
		.def("getImprovementUpgradeRateModifier", &CvCivicInfo::getImprovementUpgradeRateModifier, "int ()")
		.def("getMilitaryProductionModifier", &CvCivicInfo::getMilitaryProductionModifier, "int ()")
		.def("getBaseFreeUnits", &CvCivicInfo::getBaseFreeUnits, "int ()")
		.def("getBaseFreeMilitaryUnits", &CvCivicInfo::getBaseFreeMilitaryUnits, "int ()")
		.def("getFreeUnitsPopulationPercent", &CvCivicInfo::getFreeUnitsPopulationPercent, "int ()")
		.def("getFreeMilitaryUnitsPopulationPercent", &CvCivicInfo::getFreeMilitaryUnitsPopulationPercent, "int ()")
		.def("getGoldPerUnit", &CvCivicInfo::getGoldPerUnit, "int ()")
		.def("getGoldPerMilitaryUnit", &CvCivicInfo::getGoldPerMilitaryUnit, "int ()")
		.def("getHappyPerMilitaryUnit", &CvCivicInfo::getHappyPerMilitaryUnit, "int ()")
		.def("getLargestCityHappiness", &CvCivicInfo::getLargestCityHappiness, "int ()")
		.def("getWarWearinessModifier", &CvCivicInfo::getWarWearinessModifier, "int ()")
		.def("getFreeSpecialist", &CvCivicInfo::getFreeSpecialist, "int ()")
		.def("getTradeRoutes", &CvCivicInfo::getTradeRoutes, "int ()")
		.def("getTechPrereq", &CvCivicInfo::getTechPrereq, "int ()")
		.def("getCivicPercentAnger", &CvCivicInfo::getCivicPercentAnger, "int ()")
		.def("getMaxConscript", &CvCivicInfo::getMaxConscript, "int ()")
		.def("getStateReligionHappiness", &CvCivicInfo::getStateReligionHappiness, "int ()")
		.def("getNonStateReligionHappiness", &CvCivicInfo::getNonStateReligionHappiness, "int ()")
		.def("getStateReligionUnitProductionModifier", &CvCivicInfo::getStateReligionUnitProductionModifier, "int ()")
		.def("getStateReligionBuildingProductionModifier", &CvCivicInfo::getStateReligionBuildingProductionModifier, "int ()")
		.def("getStateReligionFreeExperience", &CvCivicInfo::getStateReligionFreeExperience, "int ()")
		.def("getExpInBorderModifier", &CvCivicInfo::getExpInBorderModifier, "bool ()")

		.def("isMilitaryFoodProduction", &CvCivicInfo::isMilitaryFoodProduction, "bool ()")
		/************************************************************************************************/
		/* Influence Driven War                   06/07/10                                 Valkrionn    */
		/*                                                                                              */
		/*						Prevents IDW effects within specific borders                            */
		/************************************************************************************************/
		.def("isFixedBorders", &CvCivicInfo::isFixedBorders, "bool ()")
		.def("isInfluenceAllowed", &CvCivicInfo::isInfluenceAllowed, "bool ()")
		.def("getVictoryInfluenceModifier", &CvCivicInfo::getVictoryInfluenceModifier, "int ()")
		.def("getPillageInfluenceModifier", &CvCivicInfo::getPillageInfluenceModifier, "int ()")
		.def("getDefeatInfluenceModifier", &CvCivicInfo::getDefeatInfluenceModifier, "int ()")
		/*************************************************************************************************/
		/**	END																							**/
		/*************************************************************************************************/
		.def("isNoUnhealthyPopulation", &CvCivicInfo::isNoUnhealthyPopulation, "bool ()")
		.def("isBuildingOnlyHealthy", &CvCivicInfo::isBuildingOnlyHealthy, "bool ()")
		.def("isNoForeignTrade", &CvCivicInfo::isNoForeignTrade, "bool ()")
		.def("isNoCorporations", &CvCivicInfo::isNoCorporations, "bool ()")
		.def("isNoForeignCorporations", &CvCivicInfo::isNoForeignCorporations, "bool ()")
		.def("isStateReligion", &CvCivicInfo::isStateReligion, "bool ()")
		.def("isNoNonStateReligionSpread", &CvCivicInfo::isNoNonStateReligionSpread, "bool ()")

		.def("pyGetWeLoveTheKing", &CvCivicInfo::pyGetWeLoveTheKing, "wstring ()")

		/*************************************************************************************************/
		/**	New Tag Defs	(CivicInfos)			05/15/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("getAlignmentModifier", &CvCivicInfo::getAlignmentModifier, "int ()")
		.def("isCompassionHigh", &CvCivicInfo::isCompassionHigh, "bool ()")
		.def("isCompassionLow", &CvCivicInfo::isCompassionLow, "bool ()")
		.def("isHidden", &CvCivicInfo::isHidden, "bool ()")
		.def("isNoDiplomacyWithEnemies", &CvCivicInfo::isNoDiplomacyWithEnemies, "bool ()")
		.def("isPrereqWar", &CvCivicInfo::isPrereqWar, "bool ()")
		.def("getAttitudeShareMod", &CvCivicInfo::getAttitudeShareMod, "int ()")
		.def("getCoastalTradeRoutes", &CvCivicInfo::getCoastalTradeRoutes, "int ()")
		.def("getEnslavementChance", &CvCivicInfo::getEnslavementChance, "int ()")
		.def("getFoodConsumptionPerPopulation", &CvCivicInfo::getFoodConsumptionPerPopulation, "int ()")
		.def("getBlockAlignment", &CvCivicInfo::getBlockAlignment, "int ()")
		.def("getPrereqAlignment", &CvCivicInfo::getPrereqAlignment, "int ()")
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
		/**																								**/
		/**							Adds a new alignment axis to the game								**/
		/*************************************************************************************************/
		.def("getBlockEthicalAlignment", &CvCivicInfo::getBlockEthicalAlignment, "int ()")
		.def("getPrereqEthicalAlignment", &CvCivicInfo::getPrereqEthicalAlignment, "int ()")
		.def("getEthicalAlignmentModifier", &CvCivicInfo::getEthicalAlignmentModifier, "int ()")
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments					END												**/
		/*************************************************************************************************/
		.def("getPrereqReligion", &CvCivicInfo::getPrereqReligion, "int ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		// Arrays

		.def("getYieldModifier", &CvCivicInfo::getYieldModifier, "int (int i)")
		.def("getCapitalYieldModifier", &CvCivicInfo::getCapitalYieldModifier, "int (int i)")
		.def("getTradeYieldModifier", &CvCivicInfo::getTradeYieldModifier, "int (int i)")
		.def("getForeignTradeYieldModifier", &CvCivicInfo::getForeignTradeYieldModifier, "int (int i)")
		/*************************************************************************************************/
		/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
		/**																								**/
		/**									Allows trade to grant culture								**/
		/*************************************************************************************************/
		.def("getTradeCommerceModifier", &CvCivicInfo::getTradeCommerceModifier, "int (int i)")
		.def("getForeignTradeCommerceModifier", &CvCivicInfo::getForeignTradeCommerceModifier, "int (int i)")
		/*************************************************************************************************/
		/**	END																							**/
		/*************************************************************************************************/
		.def("getCommerceChange", &CvCivicInfo::getCommerceChange, "int (int i)")
		.def("getCommerceModifier", &CvCivicInfo::getCommerceModifier, "int (int i)")
		.def("getCapitalCommerceModifier", &CvCivicInfo::getCapitalCommerceModifier, "int (int i)")
		.def("getSpecialistExtraCommerce", &CvCivicInfo::getSpecialistExtraCommerce, "int (int i)")
		.def("getBuildingHappinessChanges", &CvCivicInfo::getBuildingHappinessChanges, "int (int i)")
		.def("getBuildingHealthChanges", &CvCivicInfo::getBuildingHealthChanges, "int (int i)")
		.def("getFeatureHappinessChanges", &CvCivicInfo::getFeatureHappinessChanges, "int (int i)")

		.def("isHurry", &CvCivicInfo::isHurry, "bool (int i)")
		.def("isSpecialBuildingNotRequired", &CvCivicInfo::isSpecialBuildingNotRequired, "bool (int i)")
		.def("isSpecialistClassValid", &CvCivicInfo::isSpecialistClassValid, "bool (int i)")

		.def("getImprovementYieldChanges", &CvCivicInfo::getImprovementYieldChanges, "int (int i, int j)")

		// FfH: Added by Kael 07/03/2009
		.def("getPrereqCivilization", &CvCivicInfo::getPrereqCivilization, "int ()")
		// FfH: End Add

		;

	python::class_<CvUnitClassInfo, python::bases<CvInfoBase> >("CvUnitClassInfo")
		.def("getMaxGlobalInstances", &CvUnitClassInfo::getMaxGlobalInstances, "int ()")
		.def("getMaxTeamInstances", &CvUnitClassInfo::getMaxTeamInstances, "int ()")
		.def("getMaxPlayerInstances", &CvUnitClassInfo::getMaxPlayerInstances, "int ()")
		/*************************************************************************************************/
		/**	WeightedCost							 1/30/2010								Valkrionn	**/
		/**																								**/
		/**						Modifies Cost based on Population and number of Cities					**/
		/*************************************************************************************************/
		.def("isCountCitiesAsUnit", &CvUnitClassInfo::isCountCitiesAsUnit, "bool ()")
		/*************************************************************************************************/
		/**	WeightedCost								END												**/
		/*************************************************************************************************/
		.def("getInstanceCostModifier", &CvUnitClassInfo::getInstanceCostModifier, "int ()")
		.def("getDefaultUnitIndex", &CvUnitClassInfo::getDefaultUnitIndex, "int ()")
		/*************************************************************************************************/
		/**	New Tag Defs	(UnitClassInfos)		10/18/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("isUnique", &CvUnitClassInfo::isUnique, "bool ()")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/
		;

	python::class_<CvBuildingInfo, python::bases<CvInfoBase, CvScalableInfo> >("CvBuildingInfo")

		.def("getBuildingClassType", &CvBuildingInfo::getBuildingClassType, "int ()")
		.def("getVictoryPrereq", &CvBuildingInfo::getVictoryPrereq, "int ()")
		.def("getFreeStartEra", &CvBuildingInfo::getFreeStartEra, "int ()")
		.def("getMaxStartEra", &CvBuildingInfo::getMaxStartEra, "int ()")
		.def("getObsoleteTech", &CvBuildingInfo::getObsoleteTech, "int ()")
		.def("getPrereqAndTech", &CvBuildingInfo::getPrereqAndTech, "int ()")
		.def("getNoBonus", &CvBuildingInfo::getNoBonus, "int ()")
		.def("getPowerBonus", &CvBuildingInfo::getPowerBonus, "int ()")
		.def("getFreeBonus", &CvBuildingInfo::getFreeBonus, "int ()")
		.def("getFreeBonus2", &CvBuildingInfo::getFreeBonus2, "int ()") // used to show palace free bonuses
		.def("getFreeBonus3", &CvBuildingInfo::getFreeBonus3, "int ()") // used to show palace free bonuses
		.def("getNumFreeBonuses", &CvBuildingInfo::getNumFreeBonuses, "int ()")
		.def("getFreeBuildingClass", &CvBuildingInfo::getFreeBuildingClass, "int ()")
		.def("getParentBuildingClass", &CvBuildingInfo::getParentBuildingClass, "int ()")
		.def("getFreePromotion", &CvBuildingInfo::getFreePromotion, "int ()")
		.def("getCivic", &CvBuildingInfo::getCivicOption, "int ()")
		.def("getAIWeight", &CvBuildingInfo::getAIWeight, "int ()")
		.def("getProductionCost", &CvBuildingInfo::getProductionCost, "int ()")
		.def("getHurryCostModifier", &CvBuildingInfo::getHurryCostModifier, "int ()")
		.def("getHurryAngerModifier", &CvBuildingInfo::getHurryAngerModifier, "int ()")
		.def("getMinAreaSize", &CvBuildingInfo::getMinAreaSize, "int ()")
		.def("getNumCitiesPrereq", &CvBuildingInfo::getNumCitiesPrereq, "int ()")
		.def("getNumTeamsPrereq", &CvBuildingInfo::getNumTeamsPrereq, "int ()")
		.def("getUnitLevelPrereq", &CvBuildingInfo::getUnitLevelPrereq, "int ()")
		.def("getMinLatitude", &CvBuildingInfo::getMinLatitude, "int ()")
		.def("getMaxLatitude", &CvBuildingInfo::getMaxLatitude, "int ()")
		.def("getGreatPeopleRateModifier", &CvBuildingInfo::getGreatPeopleRateModifier, "int ()")
		.def("getGreatGeneralRateModifier", &CvBuildingInfo::getGreatGeneralRateModifier, "int ()")
		.def("getDomesticGreatGeneralRateModifier", &CvBuildingInfo::getDomesticGreatGeneralRateModifier, "int ()")
		.def("getGlobalGreatPeopleRateModifier", &CvBuildingInfo::getGlobalGreatPeopleRateModifier, "int ()")
		.def("getAnarchyModifier", &CvBuildingInfo::getAnarchyModifier, "int ()")
		.def("getGoldenAgeModifier", &CvBuildingInfo::getGoldenAgeModifier, "int ()")
		.def("getGlobalHurryModifier", &CvBuildingInfo::getGlobalHurryModifier, "int ()")
		.def("getFreeExperience", &CvBuildingInfo::getFreeExperience, "int ()")
		.def("getGlobalFreeExperience", &CvBuildingInfo::getGlobalFreeExperience, "int ()")
		.def("getFoodKept", &CvBuildingInfo::getFoodKept, "int ()")
		.def("getAirlift", &CvBuildingInfo::getAirlift, "int ()")
		.def("getAirModifier", &CvBuildingInfo::getAirModifier, "int ()")
		.def("getAirUnitCapacity", &CvBuildingInfo::getAirUnitCapacity, "int ()")
		.def("getNukeModifier", &CvBuildingInfo::getNukeModifier, "int ()")
		.def("getNukeExplosionRand", &CvBuildingInfo::getNukeExplosionRand, "int ()")
		.def("getFreeSpecialist", &CvBuildingInfo::getFreeSpecialist, "int ()")
		.def("getAreaFreeSpecialist", &CvBuildingInfo::getAreaFreeSpecialist, "int ()")
		.def("getGlobalFreeSpecialist", &CvBuildingInfo::getGlobalFreeSpecialist, "int ()")
		.def("getHappiness", &CvBuildingInfo::getHappiness, "int ()")
		.def("getAreaHappiness", &CvBuildingInfo::getAreaHappiness, "int ()")
		.def("getGlobalHappiness", &CvBuildingInfo::getGlobalHappiness, "int ()")
		.def("getStateReligionHappiness", &CvBuildingInfo::getStateReligionHappiness, "int ()")
		.def("getWorkerSpeedModifier", &CvBuildingInfo::getWorkerSpeedModifier, "int ()")
		.def("getMilitaryProductionModifier", &CvBuildingInfo::getMilitaryProductionModifier, "int ()")
		.def("getSpaceProductionModifier", &CvBuildingInfo::getRitualProductionModifier, "int ()")
		.def("getGlobalSpaceProductionModifier", &CvBuildingInfo::getGlobalRitualProductionModifier, "int ()")
		.def("getTradeRoutes", &CvBuildingInfo::getTradeRoutes, "int ()")
		.def("getCoastalTradeRoutes", &CvBuildingInfo::getCoastalTradeRoutes, "int ()")
		.def("getGlobalTradeRoutes", &CvBuildingInfo::getGlobalTradeRoutes, "int ()")
		.def("getTradeRouteModifier", &CvBuildingInfo::getTradeRouteModifier, "int ()")
		.def("getForeignTradeRouteModifier", &CvBuildingInfo::getForeignTradeRouteModifier, "int ()")
		.def("getAssetValue", &CvBuildingInfo::getAssetValue, "int ()")
		.def("getPowerValue", &CvBuildingInfo::getPowerValue, "int ()")
		.def("getSpecialBuildingType", &CvBuildingInfo::getSpecialBuildingType, "int ()")
		.def("getAdvisorType", &CvBuildingInfo::getAdvisorType, "int ()")
		.def("getHolyCity", &CvBuildingInfo::getHolyCity, "int ()")
		.def("getReligionType", &CvBuildingInfo::getReligionType, "int ()")
		.def("getStateReligion", &CvBuildingInfo::getStateReligion, "int ()")
		.def("getPrereqReligion", &CvBuildingInfo::getPrereqReligion, "int ()")
		.def("getPrereqCorporation", &CvBuildingInfo::getPrereqCorporation, "int ()")
		.def("getFoundsCorporation", &CvBuildingInfo::getFoundsCorporation, "int ()")
		.def("getGlobalReligionCommerce", &CvBuildingInfo::getGlobalReligionCommerce, "int ()")
		.def("getGlobalCorporationCommerce", &CvBuildingInfo::getGlobalCorporationCommerce, "int ()")
		.def("getPrereqAndBonus", &CvBuildingInfo::getPrereqAndBonus, "int ()")
		.def("getGreatPeopleUnitClass", &CvBuildingInfo::getGreatPeopleUnitClass, "int ()")
		.def("getGreatPeopleRateChange", &CvBuildingInfo::getGreatPeopleRateChange, "int ()")
		.def("getConquestProbability", &CvBuildingInfo::getConquestProbability, "int ()")
		.def("getMaintenanceModifier", &CvBuildingInfo::getMaintenanceModifier, "int ()")
		.def("getWarWearinessModifier", &CvBuildingInfo::getWarWearinessModifier, "int ()")
		.def("getGlobalWarWearinessModifier", &CvBuildingInfo::getGlobalWarWearinessModifier, "int ()")
		.def("getEnemyWarWearinessModifier", &CvBuildingInfo::getEnemyWarWearinessModifier, "int ()")
		.def("getHealRateChange", &CvBuildingInfo::getHealRateChange, "int ()")
		.def("getHealth", &CvBuildingInfo::getHealth, "int ()")
		.def("getAreaHealth", &CvBuildingInfo::getAreaHealth, "int ()")
		.def("getGlobalHealth", &CvBuildingInfo::getGlobalHealth, "int ()")
		.def("getGlobalPopulationChange", &CvBuildingInfo::getGlobalPopulationChange, "int ()")
		.def("getFreeTechs", &CvBuildingInfo::getFreeTechs, "int ()")
		.def("getDefenseModifier", &CvBuildingInfo::getDefenseModifier, "int ()")
		.def("getBombardDefenseModifier", &CvBuildingInfo::getBombardDefenseModifier, "int ()")
		.def("getAllCityDefenseModifier", &CvBuildingInfo::getAllCityDefenseModifier, "int ()")
		.def("getEspionageDefenseModifier", &CvBuildingInfo::getEspionageDefenseModifier, "int ()")
		.def("getMissionType", &CvBuildingInfo::getMissionType, "int ()")
		.def("getVoteSourceType", &CvBuildingInfo::getVoteSourceType, "int ()")

		.def("isTeamShare", &CvBuildingInfo::isTeamShare, "bool ()")
		.def("isWater", &CvBuildingInfo::isWater, "bool ()")
		.def("isRiver", &CvBuildingInfo::isRiver, "bool ()")
		.def("isPower", &CvBuildingInfo::isPower, "bool ()")
		.def("isDirtyPower", &CvBuildingInfo::isDirtyPower, "bool ()")
		.def("isAreaCleanPower", &CvBuildingInfo::isAreaCleanPower, "bool ()")
		.def("isAreaBorderObstacle", &CvBuildingInfo::isAreaBorderObstacle, "bool ()")
		.def("isForceTeamVoteEligible", &CvBuildingInfo::isForceTeamVoteEligible, "bool ()")
		.def("isCapital", &CvBuildingInfo::isCapital, "bool ()")
		.def("isGovernmentCenter", &CvBuildingInfo::isGovernmentCenter, "bool ()")
		.def("isGoldenAge", &CvBuildingInfo::isGoldenAge, "bool ()")
		.def("isMapCentering", &CvBuildingInfo::isMapCentering, "bool ()")
		.def("isNoUnhappiness", &CvBuildingInfo::isNoUnhappiness, "bool ()")
		/************************************************************************************************/
		/* Influence Driven War                   06/08/10                                 Valkrionn    */
		/*                                                                                              */
		/*						Prevents IDW effects within specific borders                            */
		/************************************************************************************************/
		.def("isFixedBorders", &CvBuildingInfo::isFixedBorders, "bool ()")
		/*************************************************************************************************/
		/**	END																							**/
		/*************************************************************************************************/
		.def("isNoUnhealthyPopulation", &CvBuildingInfo::isNoUnhealthyPopulation, "bool ()")
		.def("isBuildingOnlyHealthy", &CvBuildingInfo::isBuildingOnlyHealthy, "bool ()")
		.def("isNeverCapture", &CvBuildingInfo::isNeverCapture, "bool ()")
		.def("isNukeImmune", &CvBuildingInfo::isNukeImmune, "bool ()")
		.def("isPrereqReligion", &CvBuildingInfo::isPrereqReligion, "bool ()")
		.def("isCenterInCity", &CvBuildingInfo::isCenterInCity, "bool ()")
		.def("isStateReligion", &CvBuildingInfo::isStateReligion, "bool ()")
		.def("isAllowsNukes", &CvBuildingInfo::isAllowsNukes, "bool ()")

		.def("getConstructSound", &CvBuildingInfo::getConstructSound, "string ()")
		.def("getHotKey", &CvBuildingInfo::getHotKey, "string ()")
		.def("getHotKeyDescription", &CvBuildingInfo::getHotKeyDescription, "string ()")
		.def("getArtDefineTag", &CvBuildingInfo::getArtDefineTag, "string ()")
		.def("getMovie", &CvBuildingInfo::getMovie, "string ()")
		.def("getMovieDefineTag", &CvBuildingInfo::getMovieDefineTag, "string ()")
		/*************************************************************************************************/
		/**	New Tag Defs	(BuildingInfos)			05/15/08								Xienwolf	**/
		/**																								**/
		/**								Exposes the Functions to Python									**/
		/*************************************************************************************************/
		.def("getEquipmentPromotion", &CvBuildingInfo::getEquipmentPromotion, "int ()")
		.def("getPrereqBroadAlignment", &CvBuildingInfo::getPrereqBroadAlignment, "int ()")
		/*************************************************************************************************/
		/**	Building prereq Alignments				07/04/10								Snarko		**/
		/**																								**/
		/**							Allows buildings to require alignments								**/
		/*************************************************************************************************/
		.def("getNumPrereqAlignments", &CvBuildingInfo::getNumPrereqAlignments, "int ()")
		.def("getPrereqAlignment", &CvBuildingInfo::getPrereqAlignment, "int (int iI)")
		.def("getNumPrereqEthicalAlignments", &CvBuildingInfo::getNumPrereqEthicalAlignments, "int ()")
		.def("getPrereqEthicalAlignment", &CvBuildingInfo::getPrereqEthicalAlignment, "int (int iI)")
		/*************************************************************************************************/
		/**	Building prereq Alignments					END												**/
		/*************************************************************************************************/
		.def("getAlignmentModifier", &CvBuildingInfo::getAlignmentModifier, "int ()")
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
		/**																								**/
		/**							Adds a new alignment axis to the game								**/
		/*************************************************************************************************/
		.def("getPrereqBroadEthicalAlignment", &CvBuildingInfo::getPrereqBroadEthicalAlignment, "int ()")
		.def("getEthicalAlignmentModifier", &CvBuildingInfo::getEthicalAlignmentModifier, "int ()")
		/*************************************************************************************************/
		/**	Lawful-Chaotic Alignments					END												**/
		/*************************************************************************************************/
		// Crime
			.def("getPrereqPopulation", &CvBuildingInfo::getPrereqPopulation, "int ()")
			.def("getPrereqCrime", &CvBuildingInfo::getPrereqCrime, "int ()")
		.def("getMinCrime", &CvBuildingInfo::getMinCrime, "int ()")
		.def("isAutoBuild", &CvBuildingInfo::isAutoBuild, "bool ()")
		.def("isMustMaintain", &CvBuildingInfo::isMustMaintain, "bool ()")
		.def("isCrimeEffect", &CvBuildingInfo::isCrimeEffect, "bool ()")
			.def("isEffect", &CvBuildingInfo::isEffect, "bool ()")
			.def("getPerCrimeEffectCommerceChange", &CvBuildingInfo::getPerCrimeEffectCommerceChange, "int (int i)")
		.def("getPerCrimeEffectYieldChange", &CvBuildingInfo::getPerCrimeEffectYieldChange, "int (int i)")

		.def("getPotency", &CvBuildingInfo::getPotency, "int ()")
		.def("getPotencyAffinity", &CvBuildingInfo::getPotencyAffinity, "float (int iI)")
		.def("getPotencyBonusPrereq", &CvBuildingInfo::getPotencyBonusPrereq, "int (int iI)")
		.def("getShielding", &CvBuildingInfo::getShielding, "int ()")
		.def("getShieldingAffinity", &CvBuildingInfo::getShieldingAffinity, "float (int iI)")
		.def("getShieldingBonusPrereq", &CvBuildingInfo::getShieldingBonusPrereq, "int (int iI)")
		.def("getTrainXPCap", &CvBuildingInfo::getTrainXPCap, "int (int iI)")
		.def("getTrainXPRate", &CvBuildingInfo::getTrainXPRate, "float (int iI)")

		.def("getGlobalPotency", &CvBuildingInfo::getGlobalPotency, "int ()")
		.def("getGlobalPotencyAffinity", &CvBuildingInfo::getGlobalPotencyAffinity, "float (int iI)")
		.def("getGlobalPotencyBonusPrereq", &CvBuildingInfo::getGlobalPotencyBonusPrereq, "int (int iI)")
		.def("getGlobalShielding", &CvBuildingInfo::getGlobalShielding, "int ()")
		.def("getGlobalShieldingAffinity", &CvBuildingInfo::getGlobalShieldingAffinity, "float (int iI)")
		.def("getGlobalShieldingBonusPrereq", &CvBuildingInfo::getGlobalShieldingBonusPrereq, "int (int iI)")
		.def("getGlobalTrainXPCap", &CvBuildingInfo::getGlobalTrainXPCap, "int (int iI)")
		.def("getGlobalTrainXPRate", &CvBuildingInfo::getGlobalTrainXPRate, "float (int iI)")

		.def("getNumPrereqTeamBuildingClassANDs", &CvBuildingInfo::getNumPrereqTeamBuildingClassANDs, "int ()")
		.def("getPrereqTeamBuildingClassAND", &CvBuildingInfo::getPrereqTeamBuildingClassAND, "int (int iI)")
		.def("getNumPrereqTeamBuildingClassNOTs", &CvBuildingInfo::getNumPrereqTeamBuildingClassNOTs, "int ()")
		.def("getPrereqTeamBuildingClassNOT", &CvBuildingInfo::getPrereqTeamBuildingClassNOT, "int (int iI)")
		.def("getNumPrereqTeamBuildingClassORs", &CvBuildingInfo::getNumPrereqTeamBuildingClassORs, "int ()")
		.def("getPrereqTeamBuildingClassOR", &CvBuildingInfo::getPrereqTeamBuildingClassOR, "int (int iI)")
		.def("getNumPrereqGlobalBuildingClassANDs", &CvBuildingInfo::getNumPrereqGlobalBuildingClassANDs, "int ()")
		.def("getPrereqGlobalBuildingClassAND", &CvBuildingInfo::getPrereqGlobalBuildingClassAND, "int (int iI)")
		.def("getNumPrereqGlobalBuildingClassNOTs", &CvBuildingInfo::getNumPrereqGlobalBuildingClassNOTs, "int ()")
		.def("getPrereqGlobalBuildingClassNOT", &CvBuildingInfo::getPrereqGlobalBuildingClassNOT, "int (int iI)")
		.def("getNumPrereqGlobalBuildingClassORs", &CvBuildingInfo::getNumPrereqGlobalBuildingClassORs, "int ()")
		.def("getPrereqGlobalBuildingClassOR", &CvBuildingInfo::getPrereqGlobalBuildingClassOR, "int (int iI)")
		/*************************************************************************************************/
		/**	New Tag Defs							END													**/
		/*************************************************************************************************/

		// FfH: Added by Kael 12/18/2007
		.def("isEquipment", &CvBuildingInfo::isEquipment, "bool ()")
		// FfH: End Add

		// Arrays

		.def("getYieldChange", &CvBuildingInfo::getYieldChange, "int (int i)")
		.def("getYieldModifier", &CvBuildingInfo::getYieldModifier, "int (int i)")
		.def("getPowerYieldModifier", &CvBuildingInfo::getPowerYieldModifier, "int (int i)")
		.def("getGlobalYieldModifier", &CvBuildingInfo::getGlobalYieldModifier, "int (int i)")
		/*************************************************************************************************/
		/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
		/**																								**/
		/**						Allows buildings to modify trade Yield and Commerces					**/
		/*************************************************************************************************/
		.def("getTradeYieldModifier", &CvBuildingInfo::getTradeYieldModifier, "int (int i)")
		.def("getTradeCommerceModifier", &CvBuildingInfo::getTradeCommerceModifier, "int (int i)")
		/*************************************************************************************************/
		/**	END																							**/
		/*************************************************************************************************/
		.def("getSeaPlotYieldChange", &CvBuildingInfo::getSeaPlotYieldChange, "int (int i)")
		.def("getRiverPlotYieldChange", &CvBuildingInfo::getRiverPlotYieldChange, "int (int i)")
		.def("getGlobalSeaPlotYieldChange", &CvBuildingInfo::getGlobalSeaPlotYieldChange, "int (int i)")
		.def("getCommerceChange", &CvBuildingInfo::getCommerceChange, "int (int i)")
		.def("getObsoleteSafeCommerceChange", &CvBuildingInfo::getObsoleteSafeCommerceChange, "int (int i)")
		.def("getCommerceChangeDoubleTime", &CvBuildingInfo::getCommerceChangeDoubleTime, "int (int i)")
		.def("getCommerceModifier", &CvBuildingInfo::getCommerceModifier, "int (int i)")
		.def("getGlobalCommerceModifier", &CvBuildingInfo::getGlobalCommerceModifier, "int (int i)")
		.def("getStateReligionCommerce", &CvBuildingInfo::getStateReligionCommerce, "int (int i)")
		.def("getCommerceHappiness", &CvBuildingInfo::getCommerceHappiness, "int (int i)")
		.def("getReligionChange", &CvBuildingInfo::getReligionChange, "int (int i)")
		/*************************************************************************************************/
		/**	GWSLocalSpecialist																	Milaga	**/
		/** Buildings can change give bonuses to specialists in only one city							**/
		/*************************************************************************************************/
		.def("getLocalSpecialistClassCommerceChange", &CvBuildingInfo::getLocalSpecialistClassCommerceChange, "int (int iSpecialistClass, int iCommerce)")
		.def("getLocalSpecialistClassYieldChange", &CvBuildingInfo::getLocalSpecialistClassYieldChange, "int (int iSpecialistClass, int iYield)")
		.def("getLocalSpecialistClassHappinessChange", &CvBuildingInfo::getLocalSpecialistClassHappinessChange, "int (int iSpecialistClass)")
		.def("getLocalSpecialistClassHealthChange", &CvBuildingInfo::getLocalSpecialistClassHealthChange, "int (int iSpecialistClass)")
		.def("getLocalSpecialistClassGPPChange", &CvBuildingInfo::getLocalSpecialistClassGPPChange, "int (int iSpecialistClass)")
		/*************************************************************************************************/
		/**	GWSLocalSpecialist																		END	**/
		/*************************************************************************************************/
		.def("getSpecialistClassCount", &CvBuildingInfo::getSpecialistClassCount, "int (int i)")
		.def("getFreeSpecialistClassCount", &CvBuildingInfo::getFreeSpecialistClassCount, "int (int i)")
		.def("getBonusHealthChanges", &CvBuildingInfo::getBonusHealthChanges, "int (int i)")
		.def("getBonusHappinessChanges", &CvBuildingInfo::getBonusHappinessChanges, "int (int i)")
		.def("getBonusProductionModifier", &CvBuildingInfo::getBonusProductionModifier, "int (int i)")
		.def("getUnitCombatFreeExperience", &CvBuildingInfo::getUnitCombatFreeExperience, "int (int i)")
		.def("getDomainFreeExperience", &CvBuildingInfo::getDomainFreeExperience, "int (int i)")
		.def("getDomainProductionModifier", &CvBuildingInfo::getDomainProductionModifier, "int (int i)")
		.def("getPrereqAndTechs", &CvBuildingInfo::getPrereqAndTechs, "int (int i)")
		.def("getPrereqOrBonuses", &CvBuildingInfo::getPrereqOrBonuses, "int (int i)")
		.def("getProductionTraits", &CvBuildingInfo::getProductionTraits, "int (int i)")
		.def("getHappinessTraits", &CvBuildingInfo::getHappinessTraits, "int (int i)")
		.def("getBuildingHappinessChanges", &CvBuildingInfo::getBuildingHappinessChanges, "int (int i)")
		.def("getPrereqNumOfBuildingClass", &CvBuildingInfo::getPrereqNumOfBuildingClass, "int (int i)")
		.def("getPrereqAtRangeBuildingClass", &CvBuildingInfo::getPrereqBuildingClassAtRange, "int (int i)")
		.def("getBuildingExclude", &CvBuildingInfo::getBuildingExclude, "int (int i)")
		.def("getFlavorValue", &CvBuildingInfo::getFlavorValue, "int (int i)")
		.def("getImprovementFreeSpecialistClass", &CvBuildingInfo::getImprovementFreeSpecialistClass, "int (int i)")

		.def("isCommerceFlexible", &CvBuildingInfo::isCommerceFlexible, "bool (int i)")
		.def("isCommerceChangeOriginalOwner", &CvBuildingInfo::isCommerceChangeOriginalOwner, "bool (int i)")
		.def("isBuildingClassNeededInCity", &CvBuildingInfo::isBuildingClassNeededInCity, "bool (int i)")

		.def("getSpecialistClassYieldChange", &CvBuildingInfo::getSpecialistClassYieldChange, "int (int i, int j)")
		.def("getBonusYieldModifier", &CvBuildingInfo::getBonusYieldModifier, "int (int i, int j)")
		.def("getBonusCommerceModifier", &CvBuildingInfo::getBonusCommerceModifier, "int (int i, int j)")

		.def("getArtInfo", &CvBuildingInfo::getArtInfo, python::return_value_policy<python::reference_existing_object>())
		;

	python::class_<CvSpecialBuildingInfo, python::bases<CvInfoBase> >("CvSpecialBuildingInfo")
		.def("getObsoleteTech", &CvSpecialBuildingInfo::getObsoleteTech, "int ()")
		.def("getTechPrereq", &CvSpecialBuildingInfo::getTechPrereq, "int ()")
		.def("isValid", &CvSpecialBuildingInfo::isValid, "bool ()")

		// Arrays

		.def("getProductionTraits", &CvSpecialBuildingInfo::getProductionTraits, "int (int i)")
		;
}
