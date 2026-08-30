// gameAI.cpp

#include "CvGameCoreDLL.h"
#include "CvGameAI.h"
#include "CvPlayerAI.h"
#include "CvTeamAI.h"
#include "CvGlobals.h"
#include "CvInfos.h"
#include "CvSaveSizeProbe.h"
#include "CvTaggedStream.h"

// Public Functions...

CvGameAI::CvGameAI()
{
	AI_reset();
}


CvGameAI::~CvGameAI()
{
	AI_uninit();
}


void CvGameAI::AI_init()
{
	AI_reset();

	//--------------------------------
	// Init other game data
/*************************************************************************************************/
/**	AI anti barb force				12/04/11											Snarko	**/
/**					Helping the AI take out barbs, one unit at the time...						**/
/*************************************************************************************************/
	AI_calcBarbWeight();
/*************************************************************************************************/
/**	AI anti barb force						END													**/
/*************************************************************************************************/
}


void CvGameAI::AI_uninit()
{
}


void CvGameAI::AI_reset()
{
	AI_uninit();

	m_iPad = 0;
}


void CvGameAI::AI_makeAssignWorkDirty()
{
	int iI;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		if (GET_PLAYER((PlayerTypes)iI).isAlive())
		{
			GET_PLAYER((PlayerTypes)iI).AI_makeAssignWorkDirty();
		}
	}
}


void CvGameAI::AI_updateAssignWork()
{
	int iI;

	for (int iI = 0; iI < MAX_PLAYERS; iI++)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER((PlayerTypes)iI);
		if (GET_TEAM(kLoopPlayer.getTeam()).isHuman() && kLoopPlayer.isAlive())
		{
			kLoopPlayer.AI_updateAssignWork();
		}
	}
}


//FfH: CvGameAI::AI_combatValue has been obsoleted by the FfH function CvPlayerAI::AI_combatValue(UnitTypes eUnit)
int CvGameAI::AI_combatValue(UnitTypes eUnit)
{
	int iValue;

	iValue = 100;

	if (GC.getUnitInfo(eUnit).getDomainType() == DOMAIN_AIR)
	{
		iValue *= GC.getUnitInfo(eUnit).getAirCombat();
	}
	else
	{
		iValue *= GC.getUnitInfo(eUnit).getCombat();

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
		// From Lead From Behind by UncutDragon
		// original
		//iValue *= ((((GC.getUnitInfo(eUnit).getFirstStrikes() * 2) + GC.getUnitInfo(eUnit).getChanceFirstStrikes()) * (GC.getDefineINT("COMBAT_DAMAGE") / 5)) + 100);
		// modified
		iValue *= ((((GC.getUnitInfo(eUnit).getFirstStrikes() * 2) + GC.getUnitInfo(eUnit).getChanceFirstStrikes()) * (GC.getCOMBAT_DAMAGE() / 5)) + 100);
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

		iValue /= 100;
	}

	iValue /= getBestLandUnitCombat();

	return iValue;
}


int CvGameAI::AI_turnsPercent(int iTurns, int iPercent)
{
	FAssert(iPercent > 0);
	if (iTurns != MAX_INT)
	{
		iTurns *= (iPercent);
		iTurns /= 100;
	}

	return std::max(1, iTurns);
}


// Tag numbers for this class's tagged record. APPEND ONLY: renumbering an existing
// tag makes every save written before the change decode that field as something
// else, silently. A retired field leaves its number unused rather than handing it on.
namespace
{
	enum GameAITag
	{
		TAG_PAD = 1,
	};
}
void CvGameAI::read(FDataStreamBase* pStream)
{
	CvGame::read(pStream);

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion
	if (uiFlag >= 1)
	{
		// Tagged. Order does not matter, an unknown tag is stepped over, and a field
		// the writer omitted keeps what reset() gave it.
		CvTagReader kReader(pStream);
		while (kReader.next())
		{
			switch (kReader.tag())
			{
			case TAG_PAD: m_iPad = kReader.asInt(); break;
			default: kReader.skip(); break;
			}
		}
	}
	else
	{
		// Positional, exactly as it always was. This branch is the compatibility
		// shim; it is not new code and must not be edited.
		pStream->Read(&m_iPad);
	}

/*************************************************************************************************/
/**	AI anti barb force				03/02/12											Snarko	**/
/**					Helping the AI take out barbs, one unit at the time...						**/
/*************************************************************************************************/
	pStream->Read(&iAIBarbWeight);
/*************************************************************************************************/
/**	AI anti barb force						END													**/
/*************************************************************************************************/
}


void CvGameAI::write(FDataStreamBase* pStream)
{
	CvGame::write(pStream);

	uint uiFlag=1;	// 1: tagged fields (CvTaggedStream)
	pStream->Write(uiFlag);		// flag for expansion
	{
		CvTagWriter kWriter(pStream);
		kWriter.write(TAG_PAD, m_iPad);
		kWriter.end();
	}

/*************************************************************************************************/
/**	AI anti barb force				03/02/12											Snarko	**/
/**					Helping the AI take out barbs, one unit at the time...						**/
/*************************************************************************************************/
	pStream->Write(iAIBarbWeight);
/*************************************************************************************************/
/**	AI anti barb force						END													**/
/*************************************************************************************************/
}

// Protected Functions...

// Private Functions...
/*************************************************************************************************/
/**	AI anti barb force				12/04/11											Snarko	**/
/**					Helping the AI take out barbs, one unit at the time...						**/
/*************************************************************************************************/
void CvGameAI::AI_calcBarbWeight()
{
	if (isOption(GAMEOPTION_NO_BARBARIANS) && isOption(GAMEOPTION_NO_ANIMALS) && isOption(GAMEOPTION_NO_DEMONS))
	{
		iAIBarbWeight = 0; //No barbarians, why bother? (barbarian world and events can still create barbs, but not enough to care)
	}
	else
	{
		iAIBarbWeight = 20;
		if (isOption(GAMEOPTION_NO_BARBARIANS))
		{
			iAIBarbWeight -= 8;
		}
		else if (isOption(GAMEOPTION_RAGING_BARBARIANS))
		{
			iAIBarbWeight += 4;
		}
		if (isOption(GAMEOPTION_NO_ANIMALS))
		{
			iAIBarbWeight -= 6;
		}
		else if (isOption(GAMEOPTION_DOUBLE_ANIMALS))
		{
			iAIBarbWeight += 2;
		}
		if (isOption(GAMEOPTION_NO_DEMONS))
		{
			iAIBarbWeight -= 4;
		}
		if (isOption(GAMEOPTION_BARBARIAN_WORLD))
		{
			iAIBarbWeight += 2;
		}
		if (isOption(GAMEOPTION_NO_SETTLERS))
		{
			iAIBarbWeight += 1; //Because we need to capture barb cities and because there will be more wilderness longer
		}
		if (isOption(GAMEOPTION_NO_LAIRS))
		{
			iAIBarbWeight -= 6;
		}
		if (isOption(GAMEOPTION_NO_ACHERON) && isOption(GAMEOPTION_NO_ORTHUS))
		{
			iAIBarbWeight -= 1;
		}
		iAIBarbWeight = std::max(0, iAIBarbWeight);
	}
}

//Public function
int CvGameAI::getAIBarbWeight()
{
	return iAIBarbWeight;
}
/*************************************************************************************************/
/**	AI anti barb force						END													**/
/*************************************************************************************************/