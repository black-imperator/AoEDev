#include "CvGameCoreDLL.h"
#include "CvSaveManifest.h"
#include "CvGlobals.h"
#include "CvInfos.h"
#include "FDataStreamBase.h"
#include "CvDLLUtilityIFaceBase.h"

#include <string>
#include <vector>
#include <map>
#include <set>

namespace
{
	// 'AOEM'. Cheap guard against reading a manifest out of a save that has none --
	// which would otherwise consume bytes belonging to CvGame and desync the stream.
	const unsigned int MANIFEST_MAGIC   = 0x4D454F41;
	const unsigned int MANIFEST_VERSION = 1;

	// Gross upper bounds. Only reject obvious garbage, never a legitimately large mod.
	const int MAX_MANIFEST_TYPES   = 4096;
	const int MAX_ENTRIES_PER_TYPE = 1000000;

	// How many names to spell out per line before collapsing to "+N more".
	const int MAX_NAMES_LOGGED = 6;

	typedef int         (*ManifestCountFn)();
	typedef const char* (*ManifestNameFn)(int);

	struct ManifestType
	{
		const char*     szTypeName;
		ManifestCountFn pfnCount;
		ManifestNameFn  pfnName;
	};

	// One pair of accessors per content type, generated from every getNumXInfos() /
	// getXInfo() pair CvGlobals exposes -- from the engine itself, not from a list
	// someone maintains, so it cannot fall behind. Deriving this from the vanilla BtS
	// schema instead silently missed AoE's own content: SpecialistClass alone is read
	// by 21 sites.
	//
	// Enums with a fixed NUM_X_TYPES count (YieldTypes, DomainTypes, CommerceTypes,
	// ...) have no getNumXInfos() and are therefore absent, which is correct: their
	// width is compiled into the DLL and cannot change with content.
#define MANIFEST_ACCESSORS(Label, CountCall, InfoCall, EnumType)                       \
	int mfCount_##Label() { return GC.CountCall(); }                                   \
	const char* mfName_##Label(int i) { return GC.InfoCall((EnumType)i).getType(); }

	MANIFEST_ACCESSORS(Action, getNumActionInfos, getActionInfo, int)
	MANIFEST_ACCESSORS(Advisor, getNumAdvisorInfos, getAdvisorInfo, AdvisorTypes)
	MANIFEST_ACCESSORS(Affinity, getNumAffinityInfos, getAffinityInfo, AffinityTypes)
	MANIFEST_ACCESSORS(Alignment, getNumAlignmentInfos, getAlignmentInfo, AlignmentTypes)
	MANIFEST_ACCESSORS(AnimationCategory, getNumAnimationCategoryInfos, getAnimationCategoryInfo, AnimationCategoryTypes)
	MANIFEST_ACCESSORS(AnimationPath, getNumAnimationPathInfos, getAnimationPathInfo, AnimationPathTypes)
	MANIFEST_ACCESSORS(Attachable, getNumAttachableInfos, getAttachableInfo, int)
	MANIFEST_ACCESSORS(Automate, getNumAutomateInfos, getAutomateInfo, int)
	MANIFEST_ACCESSORS(Bonus, getNumBonusInfos, getBonusInfo, BonusTypes)
	MANIFEST_ACCESSORS(BonusClass, getNumBonusClassInfos, getBonusClassInfo, BonusClassTypes)
	MANIFEST_ACCESSORS(Build, getNumBuildInfos, getBuildInfo, BuildTypes)
	MANIFEST_ACCESSORS(Building, getNumBuildingInfos, getBuildingInfo, BuildingTypes)
	MANIFEST_ACCESSORS(BuildingClass, getNumBuildingClassInfos, getBuildingClassInfo, BuildingClassTypes)
	MANIFEST_ACCESSORS(Calendar, getNumCalendarInfos, getCalendarInfo, CalendarTypes)
	MANIFEST_ACCESSORS(Camera, getNumCameraInfos, getCameraInfo, CameraAnimationTypes)
	MANIFEST_ACCESSORS(CityClass, getNumCityClassInfos, getCityClassInfo, CityClassTypes)
	MANIFEST_ACCESSORS(CityTab, getNumCityTabInfos, getCityTabInfo, CityTabTypes)
	MANIFEST_ACCESSORS(Civic, getNumCivicInfos, getCivicInfo, CivicTypes)
	MANIFEST_ACCESSORS(CivicOption, getNumCivicOptionInfos, getCivicOptionInfo, CivicOptionTypes)
	MANIFEST_ACCESSORS(Civilization, getNumCivilizationInfos, getCivilizationInfo, CivilizationTypes)
	MANIFEST_ACCESSORS(Climate, getNumClimateInfos, getClimateInfo, ClimateTypes)
	MANIFEST_ACCESSORS(ClimateZone, getNumClimateZoneInfos, getClimateZoneInfo, ClimateZoneTypes)
	MANIFEST_ACCESSORS(Color, getNumColorInfos, getColorInfo, ColorTypes)
	MANIFEST_ACCESSORS(Command, getNumCommandInfos, getCommandInfo, CommandTypes)
	MANIFEST_ACCESSORS(Concept, getNumConceptInfos, getConceptInfo, ConceptTypes)
	MANIFEST_ACCESSORS(Control, getNumControlInfos, getControlInfo, ControlTypes)
	MANIFEST_ACCESSORS(Corporation, getNumCorporationInfos, getCorporationInfo, CorporationTypes)
	MANIFEST_ACCESSORS(CultureLevel, getNumCultureLevelInfos, getCultureLevelInfo, CultureLevelTypes)
	MANIFEST_ACCESSORS(Cursor, getNumCursorInfos, getCursorInfo, CursorTypes)
	MANIFEST_ACCESSORS(DamageType, getNumDamageTypeInfos, getDamageTypeInfo, DamageTypes)
	MANIFEST_ACCESSORS(DeathList, getNumDeathListInfos, getDeathListInfo, DeathListTypes)
	MANIFEST_ACCESSORS(Denial, getNumDenialInfos, getDenialInfo, DenialTypes)
	MANIFEST_ACCESSORS(Diplomacy, getNumDiplomacyInfos, getDiplomacyInfo, int)
	MANIFEST_ACCESSORS(Effect, getNumEffectInfos, getEffectInfo, int)
	MANIFEST_ACCESSORS(Emphasize, getNumEmphasizeInfos, getEmphasizeInfo, EmphasizeTypes)
	MANIFEST_ACCESSORS(EntityEvent, getNumEntityEventInfos, getEntityEventInfo, EntityEventTypes)
	MANIFEST_ACCESSORS(Era, getNumEraInfos, getEraInfo, EraTypes)
	MANIFEST_ACCESSORS(EspionageMission, getNumEspionageMissionInfos, getEspionageMissionInfo, EspionageMissionTypes)
	MANIFEST_ACCESSORS(EthicalAlignment, getNumEthicalAlignmentInfos, getEthicalAlignmentInfo, EthicalAlignmentTypes)
	MANIFEST_ACCESSORS(Event, getNumEventInfos, getEventInfo, EventTypes)
	MANIFEST_ACCESSORS(EventTrigger, getNumEventTriggerInfos, getEventTriggerInfo, EventTriggerTypes)
	MANIFEST_ACCESSORS(Feat, getNumFeatInfos, getFeatInfo, FeatTypes)
	MANIFEST_ACCESSORS(Feature, getNumFeatureInfos, getFeatureInfo, FeatureTypes)
	MANIFEST_ACCESSORS(Flag, getNumFlagInfos, getFlagInfo, FlagTypes)
	MANIFEST_ACCESSORS(ForceControl, getNumForceControlInfos, getForceControlInfo, ForceControlTypes)
	MANIFEST_ACCESSORS(GameOption, getNumGameOptionInfos, getGameOptionInfo, GameOptionTypes)
	MANIFEST_ACCESSORS(GameSpeed, getNumGameSpeedInfos, getGameSpeedInfo, GameSpeedTypes)
	MANIFEST_ACCESSORS(Goody, getNumGoodyInfos, getGoodyInfo, GoodyTypes)
	MANIFEST_ACCESSORS(Handicap, getNumHandicapInfos, getHandicapInfo, HandicapTypes)
	MANIFEST_ACCESSORS(Hurry, getNumHurryInfos, getHurryInfo, HurryTypes)
	MANIFEST_ACCESSORS(Improvement, getNumImprovementInfos, getImprovementInfo, ImprovementTypes)
	MANIFEST_ACCESSORS(ImprovementClass, getNumImprovementClassInfos, getImprovementClassInfo, ImprovementClassTypes)
	MANIFEST_ACCESSORS(Invisible, getNumInvisibleInfos, getInvisibleInfo, InvisibleTypes)
	MANIFEST_ACCESSORS(Landscape, getNumLandscapeInfos, getLandscapeInfo, int)
	MANIFEST_ACCESSORS(LeaderClass, getNumLeaderClassInfos, getLeaderClassInfo, LeaderClassTypes)
	MANIFEST_ACCESSORS(LeaderHead, getNumLeaderHeadInfos, getLeaderHeadInfo, LeaderHeadTypes)
	MANIFEST_ACCESSORS(LeaderRelation, getNumLeaderRelationInfos, getLeaderRelationInfo, LeaderRelationTypes)
	MANIFEST_ACCESSORS(LeaderStatus, getNumLeaderStatusInfos, getLeaderStatusInfo, LeaderStatusTypes)
	MANIFEST_ACCESSORS(Lore, getNumLoreInfos, getLoreInfo, LoreTypes)
	MANIFEST_ACCESSORS(MPOption, getNumMPOptionInfos, getMPOptionInfo, MultiplayerOptionTypes)
	MANIFEST_ACCESSORS(Mission, getNumMissionInfos, getMissionInfo, MissionTypes)
	MANIFEST_ACCESSORS(ModuleId, getNumModuleIdInfos, getModuleIdInfo, ModuleIds)
	MANIFEST_ACCESSORS(Month, getNumMonthInfos, getMonthInfo, MonthTypes)
	MANIFEST_ACCESSORS(NewConcept, getNumNewConceptInfos, getNewConceptInfo, NewConceptTypes)
	MANIFEST_ACCESSORS(PlayerColor, getNumPlayerColorInfos, getPlayerColorInfo, PlayerColorTypes)
	MANIFEST_ACCESSORS(PlayerOption, getNumPlayerOptionInfos, getPlayerOptionInfo, PlayerOptionTypes)
	MANIFEST_ACCESSORS(PlotEffect, getNumPlotEffectInfos, getPlotEffectInfo, PlotEffectTypes)
	MANIFEST_ACCESSORS(Process, getNumProcessInfos, getProcessInfo, ProcessTypes)
	MANIFEST_ACCESSORS(Project, getNumProjectInfos, getProjectInfo, ProjectTypes)
	MANIFEST_ACCESSORS(Promotion, getNumPromotionInfos, getPromotionInfo, PromotionTypes)
	MANIFEST_ACCESSORS(PromotionClass, getNumPromotionClassInfos, getPromotionClassInfo, PromotionClassTypes)
	MANIFEST_ACCESSORS(PythonModules, getNumPythonModulesInfos, getPythonModulesInfo, int)
	MANIFEST_ACCESSORS(Quest, getNumQuestInfos, getQuestInfo, int)
	MANIFEST_ACCESSORS(Religion, getNumReligionInfos, getReligionInfo, ReligionTypes)
	MANIFEST_ACCESSORS(River, getNumRiverInfos, getRiverInfo, RiverTypes)
	MANIFEST_ACCESSORS(RiverModel, getNumRiverModelInfos, getRiverModelInfo, int)
	MANIFEST_ACCESSORS(Route, getNumRouteInfos, getRouteInfo, RouteTypes)
	MANIFEST_ACCESSORS(RouteModel, getNumRouteModelInfos, getRouteModelInfo, int)
	MANIFEST_ACCESSORS(SeaLevel, getNumSeaLevelInfos, getSeaLevelInfo, SeaLevelTypes)
	MANIFEST_ACCESSORS(Season, getNumSeasonInfos, getSeasonInfo, SeasonTypes)
	MANIFEST_ACCESSORS(SlideShow, getNumSlideShowInfos, getSlideShowInfo, int)
	MANIFEST_ACCESSORS(SlideShowRandom, getNumSlideShowRandomInfos, getSlideShowRandomInfo, int)
	MANIFEST_ACCESSORS(SpaceShip, getNumSpaceShipInfos, getSpaceShipInfo, int)
	MANIFEST_ACCESSORS(SpawnGroup, getNumSpawnGroupInfos, getSpawnGroupInfo, SpawnGroupTypes)
	MANIFEST_ACCESSORS(SpecialBuilding, getNumSpecialBuildingInfos, getSpecialBuildingInfo, SpecialBuildingTypes)
	MANIFEST_ACCESSORS(SpecialUnit, getNumSpecialUnitInfos, getSpecialUnitInfo, SpecialUnitTypes)
	MANIFEST_ACCESSORS(Specialist, getNumSpecialistInfos, getSpecialistInfo, SpecialistTypes)
	MANIFEST_ACCESSORS(SpecialistArtstyle, getNumSpecialistArtstyleInfos, getSpecialistArtstyleInfo, SpecialistArtstyleTypes)
	MANIFEST_ACCESSORS(SpecialistClass, getNumSpecialistClassInfos, getSpecialistClassInfo, SpecialistClassTypes)
	MANIFEST_ACCESSORS(Spell, getNumSpellInfos, getSpellInfo, SpellTypes)
	MANIFEST_ACCESSORS(SpellClass, getNumSpellClassInfos, getSpellClassInfo, SpellClassTypes)
	MANIFEST_ACCESSORS(StateName, getNumStateNameInfos, getStateNameInfo, StateNameTypes)
	MANIFEST_ACCESSORS(Tech, getNumTechInfos, getTechInfo, TechTypes)
	MANIFEST_ACCESSORS(Terrain, getNumTerrainInfos, getTerrainInfo, TerrainTypes)
	MANIFEST_ACCESSORS(TerrainClass, getNumTerrainClassInfos, getTerrainClassInfo, TerrainClassTypes)
	MANIFEST_ACCESSORS(ThroneRoom, getNumThroneRoomInfos, getThroneRoomInfo, int)
	MANIFEST_ACCESSORS(ThroneRoomStyle, getNumThroneRoomStyleInfos, getThroneRoomStyleInfo, int)
	MANIFEST_ACCESSORS(Trait, getNumTraitInfos, getTraitInfo, TraitTypes)
	MANIFEST_ACCESSORS(TraitClass, getNumTraitClassInfos, getTraitClassInfo, TraitClassTypes)
	MANIFEST_ACCESSORS(TraitTrigger, getNumTraitTriggerInfos, getTraitTriggerInfo, TraitTriggerTypes)
	MANIFEST_ACCESSORS(TurnTimer, getNumTurnTimerInfos, getTurnTimerInfo, TurnTimerTypes)
	MANIFEST_ACCESSORS(Tutorial, getNumTutorialInfos, getTutorialInfo, int)
	MANIFEST_ACCESSORS(Unit, getNumUnitInfos, getUnitInfo, UnitTypes)
	MANIFEST_ACCESSORS(UnitArtStyleType, getNumUnitArtStyleTypeInfos, getUnitArtStyleTypeInfo, UnitArtStyleTypes)
	MANIFEST_ACCESSORS(UnitClass, getNumUnitClassInfos, getUnitClassInfo, UnitClassTypes)
	MANIFEST_ACCESSORS(UnitCombat, getNumUnitCombatInfos, getUnitCombatInfo, UnitCombatTypes)
	MANIFEST_ACCESSORS(UnitFormation, getNumUnitFormationInfos, getUnitFormationInfo, int)
	MANIFEST_ACCESSORS(Upkeep, getNumUpkeepInfos, getUpkeepInfo, UpkeepTypes)
	MANIFEST_ACCESSORS(Victory, getNumVictoryInfos, getVictoryInfo, VictoryTypes)
	MANIFEST_ACCESSORS(Vote, getNumVoteInfos, getVoteInfo, VoteTypes)
	MANIFEST_ACCESSORS(VoteSource, getNumVoteSourceInfos, getVoteSourceInfo, VoteSourceTypes)
	MANIFEST_ACCESSORS(World, getNumWorldInfos, getWorldInfo, WorldSizeTypes)
	MANIFEST_ACCESSORS(WorldPicker, getNumWorldPickerInfos, getWorldPickerInfo, int)

#undef MANIFEST_ACCESSORS

	const ManifestType MANIFEST_TYPES[] =
	{
		{ "ActionTypes", mfCount_Action, mfName_Action },
		{ "AdvisorTypes", mfCount_Advisor, mfName_Advisor },
		{ "AffinityTypes", mfCount_Affinity, mfName_Affinity },
		{ "AlignmentTypes", mfCount_Alignment, mfName_Alignment },
		{ "AnimationCategoryTypes", mfCount_AnimationCategory, mfName_AnimationCategory },
		{ "AnimationPathTypes", mfCount_AnimationPath, mfName_AnimationPath },
		{ "AttachableTypes", mfCount_Attachable, mfName_Attachable },
		{ "AutomateTypes", mfCount_Automate, mfName_Automate },
		{ "BonusTypes", mfCount_Bonus, mfName_Bonus },
		{ "BonusClassTypes", mfCount_BonusClass, mfName_BonusClass },
		{ "BuildTypes", mfCount_Build, mfName_Build },
		{ "BuildingTypes", mfCount_Building, mfName_Building },
		{ "BuildingClassTypes", mfCount_BuildingClass, mfName_BuildingClass },
		{ "CalendarTypes", mfCount_Calendar, mfName_Calendar },
		{ "CameraTypes", mfCount_Camera, mfName_Camera },
		{ "CityClassTypes", mfCount_CityClass, mfName_CityClass },
		{ "CityTabTypes", mfCount_CityTab, mfName_CityTab },
		{ "CivicTypes", mfCount_Civic, mfName_Civic },
		{ "CivicOptionTypes", mfCount_CivicOption, mfName_CivicOption },
		{ "CivilizationTypes", mfCount_Civilization, mfName_Civilization },
		{ "ClimateTypes", mfCount_Climate, mfName_Climate },
		{ "ClimateZoneTypes", mfCount_ClimateZone, mfName_ClimateZone },
		{ "ColorTypes", mfCount_Color, mfName_Color },
		{ "CommandTypes", mfCount_Command, mfName_Command },
		{ "ConceptTypes", mfCount_Concept, mfName_Concept },
		{ "ControlTypes", mfCount_Control, mfName_Control },
		{ "CorporationTypes", mfCount_Corporation, mfName_Corporation },
		{ "CultureLevelTypes", mfCount_CultureLevel, mfName_CultureLevel },
		{ "CursorTypes", mfCount_Cursor, mfName_Cursor },
		{ "DamageTypeTypes", mfCount_DamageType, mfName_DamageType },
		{ "DeathListTypes", mfCount_DeathList, mfName_DeathList },
		{ "DenialTypes", mfCount_Denial, mfName_Denial },
		{ "DiplomacyTypes", mfCount_Diplomacy, mfName_Diplomacy },
		{ "EffectTypes", mfCount_Effect, mfName_Effect },
		{ "EmphasizeTypes", mfCount_Emphasize, mfName_Emphasize },
		{ "EntityEventTypes", mfCount_EntityEvent, mfName_EntityEvent },
		{ "EraTypes", mfCount_Era, mfName_Era },
		{ "EspionageMissionTypes", mfCount_EspionageMission, mfName_EspionageMission },
		{ "EthicalAlignmentTypes", mfCount_EthicalAlignment, mfName_EthicalAlignment },
		{ "EventTypes", mfCount_Event, mfName_Event },
		{ "EventTriggerTypes", mfCount_EventTrigger, mfName_EventTrigger },
		{ "FeatTypes", mfCount_Feat, mfName_Feat },
		{ "FeatureTypes", mfCount_Feature, mfName_Feature },
		{ "FlagTypes", mfCount_Flag, mfName_Flag },
		{ "ForceControlTypes", mfCount_ForceControl, mfName_ForceControl },
		{ "GameOptionTypes", mfCount_GameOption, mfName_GameOption },
		{ "GameSpeedTypes", mfCount_GameSpeed, mfName_GameSpeed },
		{ "GoodyTypes", mfCount_Goody, mfName_Goody },
		{ "HandicapTypes", mfCount_Handicap, mfName_Handicap },
		{ "HurryTypes", mfCount_Hurry, mfName_Hurry },
		{ "ImprovementTypes", mfCount_Improvement, mfName_Improvement },
		{ "ImprovementClassTypes", mfCount_ImprovementClass, mfName_ImprovementClass },
		{ "InvisibleTypes", mfCount_Invisible, mfName_Invisible },
		{ "LandscapeTypes", mfCount_Landscape, mfName_Landscape },
		{ "LeaderClassTypes", mfCount_LeaderClass, mfName_LeaderClass },
		{ "LeaderHeadTypes", mfCount_LeaderHead, mfName_LeaderHead },
		{ "LeaderRelationTypes", mfCount_LeaderRelation, mfName_LeaderRelation },
		{ "LeaderStatusTypes", mfCount_LeaderStatus, mfName_LeaderStatus },
		{ "LoreTypes", mfCount_Lore, mfName_Lore },
		{ "MPOptionTypes", mfCount_MPOption, mfName_MPOption },
		{ "MissionTypes", mfCount_Mission, mfName_Mission },
		{ "ModuleIdTypes", mfCount_ModuleId, mfName_ModuleId },
		{ "MonthTypes", mfCount_Month, mfName_Month },
		{ "NewConceptTypes", mfCount_NewConcept, mfName_NewConcept },
		{ "PlayerColorTypes", mfCount_PlayerColor, mfName_PlayerColor },
		{ "PlayerOptionTypes", mfCount_PlayerOption, mfName_PlayerOption },
		{ "PlotEffectTypes", mfCount_PlotEffect, mfName_PlotEffect },
		{ "ProcessTypes", mfCount_Process, mfName_Process },
		{ "ProjectTypes", mfCount_Project, mfName_Project },
		{ "PromotionTypes", mfCount_Promotion, mfName_Promotion },
		{ "PromotionClassTypes", mfCount_PromotionClass, mfName_PromotionClass },
		{ "PythonModulesTypes", mfCount_PythonModules, mfName_PythonModules },
		{ "QuestTypes", mfCount_Quest, mfName_Quest },
		{ "ReligionTypes", mfCount_Religion, mfName_Religion },
		{ "RiverTypes", mfCount_River, mfName_River },
		{ "RiverModelTypes", mfCount_RiverModel, mfName_RiverModel },
		{ "RouteTypes", mfCount_Route, mfName_Route },
		{ "RouteModelTypes", mfCount_RouteModel, mfName_RouteModel },
		{ "SeaLevelTypes", mfCount_SeaLevel, mfName_SeaLevel },
		{ "SeasonTypes", mfCount_Season, mfName_Season },
		{ "SlideShowTypes", mfCount_SlideShow, mfName_SlideShow },
		{ "SlideShowRandomTypes", mfCount_SlideShowRandom, mfName_SlideShowRandom },
		{ "SpaceShipTypes", mfCount_SpaceShip, mfName_SpaceShip },
		{ "SpawnGroupTypes", mfCount_SpawnGroup, mfName_SpawnGroup },
		{ "SpecialBuildingTypes", mfCount_SpecialBuilding, mfName_SpecialBuilding },
		{ "SpecialUnitTypes", mfCount_SpecialUnit, mfName_SpecialUnit },
		{ "SpecialistTypes", mfCount_Specialist, mfName_Specialist },
		{ "SpecialistArtstyleTypes", mfCount_SpecialistArtstyle, mfName_SpecialistArtstyle },
		{ "SpecialistClassTypes", mfCount_SpecialistClass, mfName_SpecialistClass },
		{ "SpellTypes", mfCount_Spell, mfName_Spell },
		{ "SpellClassTypes", mfCount_SpellClass, mfName_SpellClass },
		{ "StateNameTypes", mfCount_StateName, mfName_StateName },
		{ "TechTypes", mfCount_Tech, mfName_Tech },
		{ "TerrainTypes", mfCount_Terrain, mfName_Terrain },
		{ "TerrainClassTypes", mfCount_TerrainClass, mfName_TerrainClass },
		{ "ThroneRoomTypes", mfCount_ThroneRoom, mfName_ThroneRoom },
		{ "ThroneRoomStyleTypes", mfCount_ThroneRoomStyle, mfName_ThroneRoomStyle },
		{ "TraitTypes", mfCount_Trait, mfName_Trait },
		{ "TraitClassTypes", mfCount_TraitClass, mfName_TraitClass },
		{ "TraitTriggerTypes", mfCount_TraitTrigger, mfName_TraitTrigger },
		{ "TurnTimerTypes", mfCount_TurnTimer, mfName_TurnTimer },
		{ "TutorialTypes", mfCount_Tutorial, mfName_Tutorial },
		{ "UnitTypes", mfCount_Unit, mfName_Unit },
		{ "UnitArtStyleTypeTypes", mfCount_UnitArtStyleType, mfName_UnitArtStyleType },
		{ "UnitClassTypes", mfCount_UnitClass, mfName_UnitClass },
		{ "UnitCombatTypes", mfCount_UnitCombat, mfName_UnitCombat },
		{ "UnitFormationTypes", mfCount_UnitFormation, mfName_UnitFormation },
		{ "UpkeepTypes", mfCount_Upkeep, mfName_Upkeep },
		{ "VictoryTypes", mfCount_Victory, mfName_Victory },
		{ "VoteTypes", mfCount_Vote, mfName_Vote },
		{ "VoteSourceTypes", mfCount_VoteSource, mfName_VoteSource },
		{ "WorldTypes", mfCount_World, mfName_World },
		{ "WorldPickerTypes", mfCount_WorldPicker, mfName_WorldPicker },
	};

	const int NUM_MANIFEST_TYPES = sizeof(MANIFEST_TYPES) / sizeof(MANIFEST_TYPES[0]);

	// The table and the ContentType enum are generated from one list and indexed by
	// each other. If they ever diverge this fails to compile rather than silently
	// remapping content through the wrong type.
	typedef char ManifestTableMatchesEnum[
		(sizeof(MANIFEST_TYPES) / sizeof(MANIFEST_TYPES[0]) == CvSaveManifest::NUM_CONTENT_TYPES) ? 1 : -1];

	// ---------------------------------------------------------------------------
	// Logging. Same three channels as logCorruptSave() in CvGame.cpp, and the same
	// file, so everything about a failed load lands in one place: the engine log
	// (ini-gated), a file next to the DLL (not gated), and the debugger.
	// ---------------------------------------------------------------------------
	void logManifest(const char* szLine)
	{
		if (gDLL != NULL)
		{
			gDLL->logMsg("save_corrupt.log", szLine, false, true);
		}

		char szPath[MAX_PATH];
		szPath[0] = '\0';
		if (GetModuleFileNameA(GetModuleHandleA("CvGameCoreDLL.dll"), szPath, MAX_PATH) > 0)
		{
			char* pSlash = strrchr(szPath, '\\');
			if (pSlash != NULL)
			{
				*(pSlash + 1) = '\0';
				strncat(szPath, "CvGameCoreDLL_corrupt_save.log", MAX_PATH - strlen(szPath) - 1);
			}
		}

		FILE* fp = fopen(szPath[0] ? szPath : "CvGameCoreDLL_corrupt_save.log", "a");
		if (fp != NULL)
		{
			fprintf(fp, "%s\n", szLine);
			fclose(fp);
		}

		OutputDebugStringA(szLine);
		OutputDebugStringA("\n");
	}

	// Non-variadic on purpose, matching logCorruptSave() in CvGame.cpp: a va_list
	// version there mis-passed %u/%d under clang -O2. szFormat MUST consume exactly
	// (const char*, int, int) in that order -- pass "" or 0 for the ones it does not
	// need, and keep %s ahead of the %d's.
	void logManifestf(const char* szFormat, const char* szA, int iB, int iC)
	{
		char szLine[1152];
		_snprintf(szLine, sizeof(szLine) - 1, szFormat, szA, iB, iC);
		szLine[sizeof(szLine) - 1] = '\0';
		logManifest(szLine);
	}

	// Names present in a but not in b, capped for legibility.
	std::string diffNames(const std::vector<std::string>& a, const std::set<std::string>& b)
	{
		std::string szOut;
		int iShown = 0;
		int iTotal = 0;

		for (int i = 0; i < (int)a.size(); i++)
		{
			if (b.find(a[i]) != b.end())
			{
				continue;
			}
			iTotal++;
			if (iShown < MAX_NAMES_LOGGED)
			{
				if (iShown > 0)
				{
					szOut += ", ";
				}
				szOut += a[i];
				iShown++;
			}
		}

		if (iTotal > iShown)
		{
			char szTail[64];
			_snprintf(szTail, sizeof(szTail) - 1, ", +%d more", iTotal - iShown);
			szTail[sizeof(szTail) - 1] = '\0';
			szOut += szTail;
		}

		return szOut;
	}

	std::vector<std::string> currentNames(const ManifestType& kType)
	{
		std::vector<std::string> out;
		const int iCount = kType.pfnCount();
		out.reserve(iCount > 0 ? iCount : 0);

		for (int i = 0; i < iCount; i++)
		{
			const char* szName = kType.pfnName(i);
			out.push_back(std::string(szName != NULL ? szName : ""));
		}

		return out;
	}
}

// ---------------------------------------------------------------------------

void CvSaveManifest::write(FDataStreamBase* pStream)
{
	pStream->Write(MANIFEST_MAGIC);
	pStream->Write(MANIFEST_VERSION);
	pStream->Write(NUM_MANIFEST_TYPES);

	for (int iType = 0; iType < NUM_MANIFEST_TYPES; iType++)
	{
		const ManifestType& kType = MANIFEST_TYPES[iType];
		const int iCount = kType.pfnCount();

		pStream->WriteString(std::string(kType.szTypeName));
		pStream->Write(iCount);

		for (int i = 0; i < iCount; i++)
		{
			const char* szName = kType.pfnName(i);
			pStream->WriteString(std::string(szName != NULL ? szName : ""));
		}
	}
}

bool CvSaveManifest::readAndCheck(FDataStreamBase* pStream)
{
	unsigned int uiMagic = 0;
	pStream->Read(&uiMagic);

	if (uiMagic != MANIFEST_MAGIC)
	{
		// The stream is already off. Say so and stop -- reading further would only
		// consume bytes that belong to CvGame and make the damage worse.
		logManifest("[MANIFEST] manifest block missing or malformed; this save's content cannot be checked");
		return false;
	}

	unsigned int uiVersion = 0;
	pStream->Read(&uiVersion);

	if (uiVersion > MANIFEST_VERSION)
	{
		// A newer manifest layout. We cannot parse it, and guessing would consume the
		// wrong number of bytes and take CvGame's stream down with it. There is nothing
		// useful to do but say so and leave the rest alone.
		logManifestf("[MANIFEST] manifest layout v%s%d is newer than this build understands (v%d)", "", (int)uiVersion, (int)MANIFEST_VERSION);
		return false;
	}

	int iNumTypes = 0;
	pStream->Read(&iNumTypes);

	if (iNumTypes < 0 || iNumTypes > MAX_MANIFEST_TYPES)
	{
		logManifestf("[MANIFEST] implausible content type count in manifest:%s %d (cap %d); manifest ignored", "", iNumTypes, MAX_MANIFEST_TYPES);
		return false;
	}

	std::map<std::string, std::vector<std::string> > saved;

	for (int iType = 0; iType < iNumTypes; iType++)
	{
		std::string szTypeName;
		pStream->ReadString(szTypeName);

		int iCount = 0;
		pStream->Read(&iCount);

		if (iCount < 0 || iCount > MAX_ENTRIES_PER_TYPE)
		{
			logManifestf("[MANIFEST] implausible entry count for %s: %d (cap %d); manifest abandoned", szTypeName.c_str(), iCount, MAX_ENTRIES_PER_TYPE);
			return false;
		}

		std::vector<std::string>& kNames = saved[szTypeName];
		kNames.reserve(iCount);

		for (int i = 0; i < iCount; i++)
		{
			std::string szName;
			pStream->ReadString(szName);
			kNames.push_back(szName);
		}
	}

	// -----------------------------------------------------------------------
	// Compare against what this build has loaded.
	// -----------------------------------------------------------------------
	int iDiffering = 0;
	bool bHeaderWritten = false;

	for (int iType = 0; iType < NUM_MANIFEST_TYPES; iType++)
	{
		const ManifestType& kType = MANIFEST_TYPES[iType];
		const std::map<std::string, std::vector<std::string> >::const_iterator it =
			saved.find(std::string(kType.szTypeName));

		const std::vector<std::string> kBuild = currentNames(kType);

		if (it == saved.end())
		{
			// This build knows a content type the save never recorded -- the save
			// predates it. Not itself a mismatch worth failing over.
			continue;
		}

		const std::vector<std::string>& kSave = it->second;

		if (kSave == kBuild)
		{
			continue;
		}

		if (!bHeaderWritten)
		{
			logManifest("[MANIFEST] ----------------------------------------------------------------");
			logManifest("[MANIFEST] this save was written with different content than this build has");
			bHeaderWritten = true;
		}
		iDiffering++;

		logManifestf("[MANIFEST] %-22s save %6d   build %6d", kType.szTypeName, (int)kSave.size(), (int)kBuild.size());

		const std::set<std::string> kSaveSet(kSave.begin(), kSave.end());
		const std::set<std::string> kBuildSet(kBuild.begin(), kBuild.end());

		const std::string szOnlyInBuild = diffNames(kBuild, kSaveSet);
		const std::string szOnlyInSave  = diffNames(kSave, kBuildSet);

		if (!szOnlyInBuild.empty())
		{
			logManifestf("[MANIFEST]   in build, not in save: %s", szOnlyInBuild.c_str(), 0, 0);
		}
		if (!szOnlyInSave.empty())
		{
			// The line that usually matters: named content the player is missing,
			// which in practice means a module that is turned off.
			logManifestf("[MANIFEST]   in save, not in build: %s", szOnlyInSave.c_str(), 0, 0);
		}

		if (szOnlyInBuild.empty() && szOnlyInSave.empty())
		{
			// Same names, different order. Counts match, so nothing desyncs -- but
			// every stored ID of this type now points at the wrong entry, which is
			// the failure mode where content silently loads as something else.
			for (int i = 0; i < (int)kSave.size() && i < (int)kBuild.size(); i++)
			{
				if (kSave[i] != kBuild[i])
				{
					char szLine[1152];
					_snprintf(szLine, sizeof(szLine) - 1,
						"[MANIFEST]   same content, reordered: index %d is %s in the save, %s here",
						i, kSave[i].c_str(), kBuild[i].c_str());
					szLine[sizeof(szLine) - 1] = '\0';
					logManifest(szLine);
					break;
				}
			}
		}
	}

	// Content types the save recorded that this build has never heard of: the save
	// comes from a newer build than this one.
	for (std::map<std::string, std::vector<std::string> >::const_iterator it = saved.begin();
		it != saved.end(); ++it)
	{
		bool bKnown = false;
		for (int iType = 0; iType < NUM_MANIFEST_TYPES; iType++)
		{
			if (it->first == MANIFEST_TYPES[iType].szTypeName)
			{
				bKnown = true;
				break;
			}
		}

		if (!bKnown)
		{
			if (!bHeaderWritten)
			{
				logManifest("[MANIFEST] ----------------------------------------------------------------");
				logManifest("[MANIFEST] this save was written with different content than this build has");
				bHeaderWritten = true;
			}
			iDiffering++;
			logManifestf("[MANIFEST] %-22s is in the save but unknown to this build (save is newer)", it->first.c_str(), 0, 0);
		}
	}

	if (iDiffering == 0)
	{
		return true;
	}

	logManifestf("[MANIFEST] %s%d content type(s) differ.", "", iDiffering, 0);
	logManifest("[MANIFEST] Re-enable the modules that supply the missing content, or convert");
	logManifest("[MANIFEST] the save with aoe_save_migrator.");
	logManifest("[MANIFEST] The rest of this load will desync: content arrays are written with");
	logManifest("[MANIFEST] no element count, so the reader uses this build's counts and every");
	logManifest("[MANIFEST] field after the first differing array decodes from the wrong offset.");
	logManifest("[MANIFEST] Anything logged below this point is a consequence, not a new fault.");
	logManifest("[MANIFEST] ----------------------------------------------------------------");

	return false;
}
