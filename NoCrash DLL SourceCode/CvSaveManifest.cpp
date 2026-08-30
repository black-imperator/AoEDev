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

	// One pair of accessors per content type. Generated mechanically from the set of
	// XML-backed enums, so the table cannot drift from what CvGlobals actually exposes.
	// Structural enums with a fixed NUM_X_TYPES count (YieldTypes, DomainTypes,
	// CommerceTypes, ...) are deliberately absent: they cannot change with content.
#define MANIFEST_ACCESSORS(Label, CountCall, InfoCall, EnumType)                       \
	int mfCount_##Label() { return GC.CountCall(); }                                   \
	const char* mfName_##Label(int i) { return GC.InfoCall((EnumType)i).getType(); }

	MANIFEST_ACCESSORS(Bonus, getNumBonusInfos, getBonusInfo, BonusTypes)
	MANIFEST_ACCESSORS(Build, getNumBuildInfos, getBuildInfo, BuildTypes)
	MANIFEST_ACCESSORS(BuildingClass, getNumBuildingClassInfos, getBuildingClassInfo, BuildingClassTypes)
	MANIFEST_ACCESSORS(Building, getNumBuildingInfos, getBuildingInfo, BuildingTypes)
	MANIFEST_ACCESSORS(Calendar, getNumCalendarInfos, getCalendarInfo, CalendarTypes)
	MANIFEST_ACCESSORS(CivicOption, getNumCivicOptionInfos, getCivicOptionInfo, CivicOptionTypes)
	MANIFEST_ACCESSORS(Civic, getNumCivicInfos, getCivicInfo, CivicTypes)
	MANIFEST_ACCESSORS(Civilization, getNumCivilizationInfos, getCivilizationInfo, CivilizationTypes)
	MANIFEST_ACCESSORS(Climate, getNumClimateInfos, getClimateInfo, ClimateTypes)
	MANIFEST_ACCESSORS(Color, getNumColorInfos, getColorInfo, ColorTypes)
	MANIFEST_ACCESSORS(Corporation, getNumCorporationInfos, getCorporationInfo, CorporationTypes)
	MANIFEST_ACCESSORS(CultureLevel, getNumCultureLevelInfos, getCultureLevelInfo, CultureLevelTypes)
	MANIFEST_ACCESSORS(Emphasize, getNumEmphasizeInfos, getEmphasizeInfo, EmphasizeTypes)
	MANIFEST_ACCESSORS(Era, getNumEraInfos, getEraInfo, EraTypes)
	MANIFEST_ACCESSORS(EventTrigger, getNumEventTriggerInfos, getEventTriggerInfo, EventTriggerTypes)
	MANIFEST_ACCESSORS(Event, getNumEventInfos, getEventInfo, EventTypes)
	MANIFEST_ACCESSORS(Feat, getNumFeatInfos, getFeatInfo, FeatTypes)
	MANIFEST_ACCESSORS(Feature, getNumFeatureInfos, getFeatureInfo, FeatureTypes)
	MANIFEST_ACCESSORS(Flag, getNumFlagInfos, getFlagInfo, FlagTypes)
	MANIFEST_ACCESSORS(GameOption, getNumGameOptionInfos, getGameOptionInfo, GameOptionTypes)
	MANIFEST_ACCESSORS(GameSpeed, getNumGameSpeedInfos, getGameSpeedInfo, GameSpeedTypes)
	MANIFEST_ACCESSORS(Goody, getNumGoodyInfos, getGoodyInfo, GoodyTypes)
	MANIFEST_ACCESSORS(Handicap, getNumHandicapInfos, getHandicapInfo, HandicapTypes)
	MANIFEST_ACCESSORS(Hurry, getNumHurryInfos, getHurryInfo, HurryTypes)
	MANIFEST_ACCESSORS(Improvement, getNumImprovementInfos, getImprovementInfo, ImprovementTypes)
	MANIFEST_ACCESSORS(LeaderHead, getNumLeaderHeadInfos, getLeaderHeadInfo, LeaderHeadTypes)
	MANIFEST_ACCESSORS(Mission, getNumMissionInfos, getMissionInfo, MissionTypes)
	MANIFEST_ACCESSORS(PlayerColor, getNumPlayerColorInfos, getPlayerColorInfo, PlayerColorTypes)
	MANIFEST_ACCESSORS(PlayerOption, getNumPlayerOptionInfos, getPlayerOptionInfo, PlayerOptionTypes)
	MANIFEST_ACCESSORS(PlotEffect, getNumPlotEffectInfos, getPlotEffectInfo, PlotEffectTypes)
	MANIFEST_ACCESSORS(Project, getNumProjectInfos, getProjectInfo, ProjectTypes)
	MANIFEST_ACCESSORS(Promotion, getNumPromotionInfos, getPromotionInfo, PromotionTypes)
	MANIFEST_ACCESSORS(Religion, getNumReligionInfos, getReligionInfo, ReligionTypes)
	MANIFEST_ACCESSORS(Route, getNumRouteInfos, getRouteInfo, RouteTypes)
	MANIFEST_ACCESSORS(SeaLevel, getNumSeaLevelInfos, getSeaLevelInfo, SeaLevelTypes)
	MANIFEST_ACCESSORS(SpawnGroup, getNumSpawnGroupInfos, getSpawnGroupInfo, SpawnGroupTypes)
	MANIFEST_ACCESSORS(SpecialBuilding, getNumSpecialBuildingInfos, getSpecialBuildingInfo, SpecialBuildingTypes)
	MANIFEST_ACCESSORS(SpecialUnit, getNumSpecialUnitInfos, getSpecialUnitInfo, SpecialUnitTypes)
	MANIFEST_ACCESSORS(Specialist, getNumSpecialistInfos, getSpecialistInfo, SpecialistTypes)
	MANIFEST_ACCESSORS(Tech, getNumTechInfos, getTechInfo, TechTypes)
	MANIFEST_ACCESSORS(Terrain, getNumTerrainInfos, getTerrainInfo, TerrainTypes)
	MANIFEST_ACCESSORS(TraitClass, getNumTraitClassInfos, getTraitClassInfo, TraitClassTypes)
	MANIFEST_ACCESSORS(TraitTrigger, getNumTraitTriggerInfos, getTraitTriggerInfo, TraitTriggerTypes)
	MANIFEST_ACCESSORS(Trait, getNumTraitInfos, getTraitInfo, TraitTypes)
	MANIFEST_ACCESSORS(TurnTimer, getNumTurnTimerInfos, getTurnTimerInfo, TurnTimerTypes)
	MANIFEST_ACCESSORS(UnitClass, getNumUnitClassInfos, getUnitClassInfo, UnitClassTypes)
	MANIFEST_ACCESSORS(UnitCombat, getNumUnitCombatInfos, getUnitCombatInfo, UnitCombatTypes)
	MANIFEST_ACCESSORS(Unit, getNumUnitInfos, getUnitInfo, UnitTypes)
	MANIFEST_ACCESSORS(Upkeep, getNumUpkeepInfos, getUpkeepInfo, UpkeepTypes)
	MANIFEST_ACCESSORS(Victory, getNumVictoryInfos, getVictoryInfo, VictoryTypes)
	MANIFEST_ACCESSORS(VoteSource, getNumVoteSourceInfos, getVoteSourceInfo, VoteSourceTypes)
	MANIFEST_ACCESSORS(Vote, getNumVoteInfos, getVoteInfo, VoteTypes)
	MANIFEST_ACCESSORS(World, getNumWorldInfos, getWorldInfo, WorldSizeTypes)

#undef MANIFEST_ACCESSORS

	const ManifestType MANIFEST_TYPES[] =
	{
	{ "BonusTypes", mfCount_Bonus, mfName_Bonus },
	{ "BuildTypes", mfCount_Build, mfName_Build },
	{ "BuildingClassTypes", mfCount_BuildingClass, mfName_BuildingClass },
	{ "BuildingTypes", mfCount_Building, mfName_Building },
	{ "CalendarTypes", mfCount_Calendar, mfName_Calendar },
	{ "CivicOptionTypes", mfCount_CivicOption, mfName_CivicOption },
	{ "CivicTypes", mfCount_Civic, mfName_Civic },
	{ "CivilizationTypes", mfCount_Civilization, mfName_Civilization },
	{ "ClimateTypes", mfCount_Climate, mfName_Climate },
	{ "ColorTypes", mfCount_Color, mfName_Color },
	{ "CorporationTypes", mfCount_Corporation, mfName_Corporation },
	{ "CultureLevelTypes", mfCount_CultureLevel, mfName_CultureLevel },
	{ "EmphasizeTypes", mfCount_Emphasize, mfName_Emphasize },
	{ "EraTypes", mfCount_Era, mfName_Era },
	{ "EventTriggerTypes", mfCount_EventTrigger, mfName_EventTrigger },
	{ "EventTypes", mfCount_Event, mfName_Event },
	{ "FeatTypes", mfCount_Feat, mfName_Feat },
	{ "FeatureTypes", mfCount_Feature, mfName_Feature },
	{ "FlagTypes", mfCount_Flag, mfName_Flag },
	{ "GameOptionTypes", mfCount_GameOption, mfName_GameOption },
	{ "GameSpeedTypes", mfCount_GameSpeed, mfName_GameSpeed },
	{ "GoodyTypes", mfCount_Goody, mfName_Goody },
	{ "HandicapTypes", mfCount_Handicap, mfName_Handicap },
	{ "HurryTypes", mfCount_Hurry, mfName_Hurry },
	{ "ImprovementTypes", mfCount_Improvement, mfName_Improvement },
	{ "LeaderHeadTypes", mfCount_LeaderHead, mfName_LeaderHead },
	{ "MissionTypes", mfCount_Mission, mfName_Mission },
	{ "PlayerColorTypes", mfCount_PlayerColor, mfName_PlayerColor },
	{ "PlayerOptionTypes", mfCount_PlayerOption, mfName_PlayerOption },
	{ "PlotEffectTypes", mfCount_PlotEffect, mfName_PlotEffect },
	{ "ProjectTypes", mfCount_Project, mfName_Project },
	{ "PromotionTypes", mfCount_Promotion, mfName_Promotion },
	{ "ReligionTypes", mfCount_Religion, mfName_Religion },
	{ "RouteTypes", mfCount_Route, mfName_Route },
	{ "SeaLevelTypes", mfCount_SeaLevel, mfName_SeaLevel },
	{ "SpawnGroupTypes", mfCount_SpawnGroup, mfName_SpawnGroup },
	{ "SpecialBuildingTypes", mfCount_SpecialBuilding, mfName_SpecialBuilding },
	{ "SpecialUnitTypes", mfCount_SpecialUnit, mfName_SpecialUnit },
	{ "SpecialistTypes", mfCount_Specialist, mfName_Specialist },
	{ "TechTypes", mfCount_Tech, mfName_Tech },
	{ "TerrainTypes", mfCount_Terrain, mfName_Terrain },
	{ "TraitClassTypes", mfCount_TraitClass, mfName_TraitClass },
	{ "TraitTriggerTypes", mfCount_TraitTrigger, mfName_TraitTrigger },
	{ "TraitTypes", mfCount_Trait, mfName_Trait },
	{ "TurnTimerTypes", mfCount_TurnTimer, mfName_TurnTimer },
	{ "UnitClassTypes", mfCount_UnitClass, mfName_UnitClass },
	{ "UnitCombatTypes", mfCount_UnitCombat, mfName_UnitCombat },
	{ "UnitTypes", mfCount_Unit, mfName_Unit },
	{ "UpkeepTypes", mfCount_Upkeep, mfName_Upkeep },
	{ "VictoryTypes", mfCount_Victory, mfName_Victory },
	{ "VoteSourceTypes", mfCount_VoteSource, mfName_VoteSource },
	{ "VoteTypes", mfCount_Vote, mfName_Vote },
	{ "WorldTypes", mfCount_World, mfName_World },
	};

	const int NUM_MANIFEST_TYPES = sizeof(MANIFEST_TYPES) / sizeof(MANIFEST_TYPES[0]);

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
