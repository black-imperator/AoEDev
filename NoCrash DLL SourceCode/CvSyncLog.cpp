#include "CvGameCoreDLL.h"
#include "CvSyncLog.h"
#include "CvGlobals.h"
#include "CvGame.h"
#include "CvGameAI.h"
#include "CvPlayerAI.h"
#include "CvUnit.h"
#include "CvMap.h"
#include "CvRandom.h"
#include "CvInfos.h"
#include "CvDLLUtilityIFaceBase.h"

namespace
{
	// -1 = not looked up yet. Read once: getDefineINT does a string lookup and this is
	// consulted every turn.
	int g_iLevel = -1;

	int level()
	{
		if (g_iLevel < 0)
		{
			g_iLevel = GC.getDefineINT("SYNC_LOG", 0);
			if (g_iLevel < 0)
			{
				g_iLevel = 0;
			}
		}
		return g_iLevel;
	}

	// One file per client. The active player differs between clients, so two players
	// can hand over their logs without the names colliding.
	FILE* openLog()
	{
		char szPath[MAX_PATH];
		szPath[0] = '\0';

		if (GetModuleFileNameA(GetModuleHandleA("CvGameCoreDLL.dll"), szPath, MAX_PATH) > 0)
		{
			char* pSlash = strrchr(szPath, '\\');
			if (pSlash != NULL)
			{
				*(pSlash + 1) = '\0';
			}
			else
			{
				szPath[0] = '\0';
			}
		}

		char szName[64];
		_snprintf(szName, sizeof(szName) - 1, "synclog_P%02d.txt",
			(int)GC.getGameINLINE().getActivePlayer());
		szName[sizeof(szName) - 1] = '\0';

		strncat(szPath, szName, MAX_PATH - strlen(szPath) - 1);

		// Append, and close again each turn: a client that crashes mid-game is exactly
		// the one whose tail you need.
		return fopen(szPath, "a");
	}
}

bool CvSyncLog::isEnabled()
{
	return level() > 0;
}

void CvSyncLog::logTurn()
{
	if (!isEnabled())
	{
		return;
	}

	FILE* fp = openLog();
	if (fp == NULL)
	{
		return;
	}

	CvGame& kGame = GC.getGameINLINE();
	const int iTurn = kGame.getGameTurn();

	// Game-wide state. The two RNG seeds come first on purpose: if they diverge,
	// everything below is a consequence and there is no point reading further.
	fprintf(fp, "T%05d GAME maprand=%d sorenrand=%d cities=%d pop=%d deals=%d plots=%d areas=%d\n",
		iTurn,
		kGame.getMapRand().getSeed(),
		kGame.getSorenRand().getSeed(),
		kGame.getNumCities(),
		kGame.getTotalPopulation(),
		kGame.getNumDeals(),
		GC.getMapINLINE().getOwnedPlots(),
		GC.getMapINLINE().getNumAreas());

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		CvPlayerAI& kPlayer = GET_PLAYER((PlayerTypes)iI);
		if (!kPlayer.isEverAlive())
		{
			continue;
		}

		// Category 0 -- the headline numbers.
		fprintf(fp, "T%05d P%02d core score=%d pop=%d land=%d gold=%d assets=%d power=%d cities=%d units=%d groups=%d\n",
			iTurn, iI,
			kGame.getPlayerScore((PlayerTypes)iI),
			kPlayer.getTotalPopulation(),
			kPlayer.getTotalLand(),
			kPlayer.getGold(),
			kPlayer.getAssets(),
			kPlayer.getPower(),
			kPlayer.getNumCities(),
			kPlayer.getNumUnits(),
			kPlayer.getNumSelectionGroups());

		// Category 1 -- economy.
		{
			int iYield = 0;
			for (int iJ = 0; iJ < NUM_YIELD_TYPES; iJ++)
			{
				iYield += kPlayer.calculateTotalYield((YieldTypes)iJ);
			}

			int iCommerce = 0;
			for (int iJ = 0; iJ < NUM_COMMERCE_TYPES; iJ++)
			{
				iCommerce += kPlayer.getCommerceRate((CommerceTypes)iJ);
			}

			fprintf(fp, "T%05d P%02d econ yield=%d commerce=%d\n",
				iTurn, iI, iYield, iCommerce);
		}

		// Category 2 -- content-indexed tallies. Summed per type rather than per entry:
		// a per-entry dump would be enormous, and once the sum differs the deep mode
		// below is what narrows it down.
		{
			int iBonus = 0;
			for (int iJ = 0; iJ < GC.getNumBonusInfos(); iJ++)
			{
				iBonus += kPlayer.getNumAvailableBonuses((BonusTypes)iJ);
				iBonus += kPlayer.getBonusImport((BonusTypes)iJ);
				iBonus += kPlayer.getBonusExport((BonusTypes)iJ);
			}

			int iImprovement = 0;
			for (int iJ = 0; iJ < GC.getNumImprovementInfos(); iJ++)
			{
				iImprovement += kPlayer.getImprovementCount((ImprovementTypes)iJ);
			}

			int iBuildingClass = 0;
			for (int iJ = 0; iJ < GC.getNumBuildingClassInfos(); iJ++)
			{
				iBuildingClass += kPlayer.getBuildingClassCountPlusMaking((BuildingClassTypes)iJ);
			}

			int iUnitClass = 0;
			for (int iJ = 0; iJ < GC.getNumUnitClassInfos(); iJ++)
			{
				iUnitClass += kPlayer.getUnitClassCountPlusMaking((UnitClassTypes)iJ);
			}

			int iUnitAI = 0;
			for (int iJ = 0; iJ < NUM_UNITAI_TYPES; iJ++)
			{
				iUnitAI += kPlayer.AI_totalUnitAIs((UnitAITypes)iJ);
			}

			fprintf(fp, "T%05d P%02d tally bonus=%d improvement=%d buildingclass=%d unitclass=%d unitai=%d\n",
				iTurn, iI, iBonus, iImprovement, iBuildingClass, iUnitClass, iUnitAI);
		}

		// Category 3 -- units. The summary is order-independent on purpose: iteration
		// order is itself a thing that can differ between clients, and a sum that does
		// not depend on it separates "different units" from "same units, different
		// order". Deep mode prints them individually, in id order, to tell them apart.
		{
			int iLoop = 0;
			int iCount = 0;
			int iSum = 0;

			for (CvUnit* pLoopUnit = kPlayer.firstUnit(&iLoop); pLoopUnit != NULL;
				pLoopUnit = kPlayer.nextUnit(&iLoop))
			{
				iCount++;
				iSum += pLoopUnit->getX_INLINE();
				iSum += pLoopUnit->getY_INLINE() * 3;
				iSum += pLoopUnit->getDamageReal() * 7;
				iSum += pLoopUnit->getExperience() * 11;
				iSum += pLoopUnit->getLevel() * 13;
			}

			fprintf(fp, "T%05d P%02d units count=%d sum=%d\n", iTurn, iI, iCount, iSum);

			if (level() >= 2)
			{
				for (CvUnit* pLoopUnit = kPlayer.firstUnit(&iLoop); pLoopUnit != NULL;
					pLoopUnit = kPlayer.nextUnit(&iLoop))
				{
					fprintf(fp, "T%05d P%02d unit id=%d type=%d x=%d y=%d dmg=%d xp=%d lvl=%d\n",
						iTurn, iI,
						pLoopUnit->getID(),
						(int)pLoopUnit->getUnitType(),
						pLoopUnit->getX_INLINE(),
						pLoopUnit->getY_INLINE(),
						pLoopUnit->getDamageReal(),
						pLoopUnit->getExperience(),
						pLoopUnit->getLevel());
				}
			}
		}
	}

	fclose(fp);
}
