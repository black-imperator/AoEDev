#pragma once

#ifndef CIV4_SAVE_MANIFEST_H
#define CIV4_SAVE_MANIFEST_H

//
// Records, inside the savegame, which content the save was written with.
//
// Civ4 serializes content-indexed arrays as pStream->Read(GC.getNumXInfos(), array) --
// the element count is never stored, so the reader takes it from the CURRENT XML. Add,
// remove or reorder any content and every array sized by it shifts, the stream desyncs
// at that point, and everything after it decodes from the wrong offset. Stored content
// IDs have the same problem: they are bare indices into XML order, so inserting content
// mid-list silently renumbers everything after it.
//
// Nothing in the format can detect either case, which is why the symptom is a hang, an
// allocation failure, or quietly wrong content rather than a clean error.
//
// The manifest does not fix that. It makes it *explainable*: the save carries the names
// and counts of every content type it was written with, so on load we can say exactly
// which content differs and, by implication, which module the player is missing.
//
// It lives at the very top of the compressed body (CvGame::read/write, reached first
// through CvGameAI) because that is the only slot that is both DLL-controlled and ahead
// of all game state. It cannot go in the header -- the EXE navigates that region by
// relativeOffsetToCompressedData and checksums it.
//
// The names recorded here are also what a later stage needs in order to remap content
// old->new by name, so the format is written once and does not change again for that.
//
#include "FDataStreamBase.h"

// The save format this build WRITES, carried in CvGame's uiFlag -- which is the first
// value in the compressed body, so it version-stamps the save as a whole.
//
// This is a DLL build constant on purpose. The format is a property of the code that
// reads and writes it, so putting the selector in GlobalDefinesAlt.xml would have made
// it *content* -- the very thing the manifest exists to decouple from -- and would let
// any module change the save format by shipping a define override. Nothing outside this
// DLL can reach it.
//
// The reader accepts every version this build has ever written, indefinitely, so raising
// this never strands an existing campaign.
//
//   0, 1  original Firaxis / FfH layout
//   2     NoBonus bans stored per vote source
//   3     a content manifest follows the flag
//   4     CvGame's own fields are a tagged record
//   5     CvCity's science floats and CityBonuses::fScience are present
//
const unsigned int SAVE_FORMAT_VERSION = 5;

// First version that carries a manifest. Saves below this are read exactly as before.
// Deliberately NOT raised with SAVE_FORMAT_VERSION: a version 3 save has a manifest
// and positional CvGame fields, and must keep being read that way.
const unsigned int SAVE_FORMAT_VERSION_MANIFEST = 3;

// First version whose CvGame fields are tagged.
const unsigned int SAVE_FORMAT_VERSION_TAGGED = 4;

// First version carrying CvCity::m_fProximityScience, CvCity::m_fPerPopScience and
// CityBonuses::fScience.
//
// Those three were added to POSITIONAL runs with no gate and no flag bump, so every
// save written before them is 8 bytes short per city and 4 short per CityBonuses
// record. The reader consumed them anyway and walked off the end of the first city,
// which surfaces much later as a null-array write in a freelist load. Reads of these
// fields are gated on this; writes are unconditional, because a write is always at
// SAVE_FORMAT_VERSION.
const unsigned int SAVE_FORMAT_VERSION_SCIENCE = 5;

namespace CvSaveManifest
{
	// Every XML-backed content type the engine exposes -- derived from CvGlobals'
	// getNumXInfos()/getXInfo() pairs, not from a hand-kept list, so it cannot fall
	// behind the engine. The order here IS the order of the table in the .cpp and the
	// index space the remap tables use; a compile-time check keeps the two in step.
	enum ContentType
	{
		CONTENT_ACTION,
		CONTENT_ADVISOR,
		CONTENT_AFFINITY,
		CONTENT_ALIGNMENT,
		CONTENT_ANIMATION_CATEGORY,
		CONTENT_ANIMATION_PATH,
		CONTENT_ATTACHABLE,
		CONTENT_AUTOMATE,
		CONTENT_BONUS,
		CONTENT_BONUS_CLASS,
		CONTENT_BUILD,
		CONTENT_BUILDING,
		CONTENT_BUILDING_CLASS,
		CONTENT_CALENDAR,
		CONTENT_CAMERA,
		CONTENT_CITY_CLASS,
		CONTENT_CITY_TAB,
		CONTENT_CIVIC,
		CONTENT_CIVIC_OPTION,
		CONTENT_CIVILIZATION,
		CONTENT_CLIMATE,
		CONTENT_CLIMATE_ZONE,
		CONTENT_COLOR,
		CONTENT_COMMAND,
		CONTENT_CONCEPT,
		CONTENT_CONTROL,
		CONTENT_CORPORATION,
		CONTENT_CULTURE_LEVEL,
		CONTENT_CURSOR,
		CONTENT_DAMAGE_TYPE,
		CONTENT_DEATH_LIST,
		CONTENT_DENIAL,
		CONTENT_DIPLOMACY,
		CONTENT_EFFECT,
		CONTENT_EMPHASIZE,
		CONTENT_ENTITY_EVENT,
		CONTENT_ERA,
		CONTENT_ESPIONAGE_MISSION,
		CONTENT_ETHICAL_ALIGNMENT,
		CONTENT_EVENT,
		CONTENT_EVENT_TRIGGER,
		CONTENT_FEAT,
		CONTENT_FEATURE,
		CONTENT_FLAG,
		CONTENT_FORCE_CONTROL,
		CONTENT_GAME_OPTION,
		CONTENT_GAME_SPEED,
		CONTENT_GOODY,
		CONTENT_HANDICAP,
		CONTENT_HURRY,
		CONTENT_IMPROVEMENT,
		CONTENT_IMPROVEMENT_CLASS,
		CONTENT_INVISIBLE,
		CONTENT_LANDSCAPE,
		CONTENT_LEADER_CLASS,
		CONTENT_LEADER_HEAD,
		CONTENT_LEADER_RELATION,
		CONTENT_LEADER_STATUS,
		CONTENT_LORE,
		CONTENT_MPOPTION,
		CONTENT_MISSION,
		CONTENT_MODULE_ID,
		CONTENT_MONTH,
		CONTENT_NEW_CONCEPT,
		CONTENT_PLAYER_COLOR,
		CONTENT_PLAYER_OPTION,
		CONTENT_PLOT_EFFECT,
		CONTENT_PROCESS,
		CONTENT_PROJECT,
		CONTENT_PROMOTION,
		CONTENT_PROMOTION_CLASS,
		CONTENT_PYTHON_MODULES,
		CONTENT_QUEST,
		CONTENT_RELIGION,
		CONTENT_RIVER,
		CONTENT_RIVER_MODEL,
		CONTENT_ROUTE,
		CONTENT_ROUTE_MODEL,
		CONTENT_SEA_LEVEL,
		CONTENT_SEASON,
		CONTENT_SLIDE_SHOW,
		CONTENT_SLIDE_SHOW_RANDOM,
		CONTENT_SPACE_SHIP,
		CONTENT_SPAWN_GROUP,
		CONTENT_SPECIAL_BUILDING,
		CONTENT_SPECIAL_UNIT,
		CONTENT_SPECIALIST,
		CONTENT_SPECIALIST_ARTSTYLE,
		CONTENT_SPECIALIST_CLASS,
		CONTENT_SPELL,
		CONTENT_SPELL_CLASS,
		CONTENT_STATE_NAME,
		CONTENT_TECH,
		CONTENT_TERRAIN,
		CONTENT_TERRAIN_CLASS,
		CONTENT_THRONE_ROOM,
		CONTENT_THRONE_ROOM_STYLE,
		CONTENT_TRAIT,
		CONTENT_TRAIT_CLASS,
		CONTENT_TRAIT_TRIGGER,
		CONTENT_TURN_TIMER,
		CONTENT_TUTORIAL,
		CONTENT_UNIT,
		CONTENT_UNIT_ART_STYLE_TYPE,
		CONTENT_UNIT_CLASS,
		CONTENT_UNIT_COMBAT,
		CONTENT_UNIT_FORMATION,
		CONTENT_UPKEEP,
		CONTENT_VICTORY,
		CONTENT_VOTE,
		CONTENT_VOTE_SOURCE,
		CONTENT_WORLD,
		CONTENT_WORLD_PICKER,

		NUM_CONTENT_TYPES
	};

	// Written immediately after CvGame's uiFlag. Only for saves at
	// SAVE_FORMAT_VERSION_MANIFEST or later.
	void write(FDataStreamBase* pStream);

	// Reads the manifest and compares it against the content this build has loaded.
	// Any difference is reported to CvGameCoreDLL_corrupt_save.log, the engine log and
	// the debugger. Returns true when the save's content matches this build exactly.
	bool readAndCheck(FDataStreamBase* pStream);

	// -----------------------------------------------------------------------------
	// Name-based content remapping.
	//
	// Content arrays are written with the count the writing build had, and the reader
	// has always used its OWN count. That mismatch is the desync. With the manifest we
	// know both the width the save used and, by name, where each of its entries lives
	// now -- so an array can be read at the save's width and scattered into today's
	// layout instead of being read at the wrong width.
	//
	// Content the build no longer has is dropped. Content the save never had is left
	// at zero, which is what reset() would have given it.
	// -----------------------------------------------------------------------------

	// Call at the top of CvGame::read, UNCONDITIONALLY -- including for saves with no
	// manifest -- so remap state cannot leak from an earlier load in the same session.
	// uiSaveVersion is CvGame's own flag, which IS the save format version.
	void beginRead(unsigned int uiSaveVersion);

	// The format version of the save being read, for gating a field that has not always
	// existed. Zero outside a load, which reads as "older than everything" and so takes
	// the conservative branch.
	unsigned int saveVersion();

	// Logged after the engine's LAST call into the DLL for a load, so the log always
	// says whether our half of the load finished.
	//
	// Without it a save that dies in the engine's own container handling -- a truncated
	// or mis-framed file, which the DLL cannot see or defend against because the chunk
	// framing, the header and the footer all belong to the EXE -- is indistinguishable
	// in the log from a save the DLL itself choked on. That ambiguity cost six
	// reproduction cycles on PC Turn_0295, which turned out to be a damaged file that
	// this DLL had read correctly and completely.
	//
	// Present: every byte the DLL is responsible for was read; look at the engine.
	// Absent:  the DLL did not finish; the manifest lines above say how far it got.
	void endRead();

	// Remap one stored content index from the save's numbering to this build's.
	// NO_X (-1) and anything outside the save's own range pass through untouched.
	// Content the build no longer has maps to -1, which is NO_X -- the right answer.
	int remapId(ContentType eType, int iValue);

	// Some content ids are stored in a short, not an int. The template below would
	// read four bytes into a two byte field and take the next field with it, so this
	// non-template overload -- which wins for short* -- reads the native width.
	inline void readId(FDataStreamBase* pStream, ContentType eType, short* pDest)
	{
		short sValue = 0;
		pStream->Read(&sValue);
		*pDest = (short)remapId(eType, (int)sValue);
	}

	template <class T>
	void readId(FDataStreamBase* pStream, ContentType eType, T* pDest)
	{
		int iValue = 0;
		pStream->Read(&iValue);
		*pDest = (T)remapId(eType, iValue);
	}

	int savedCount(ContentType eType);         // width the save used
	int currentCount(ContentType eType);       // width this build uses
	const int* remapTable(ContentType eType);  // old->new index, NULL when identity

	// pSavedOrder, when given, also receives the values in the SAVE's own ordering and
	// at the save's width. Only needed where a LATER part of the stream is framed by
	// these values AND is itself written in the save's order, so the remapped copy is
	// not enough to walk it. CvTeam's project art types are the only such case.
	template <class T>
	void readArray(FDataStreamBase* pStream, ContentType eType, T* pDest, T* pSavedOrder = NULL)
	{
		const int iOld = savedCount(eType);
		const int iNew = currentCount(eType);
		const int* piRemap = remapTable(eType);

		// iOld comes out of the manifest, so it is only as trustworthy as the manifest.
		// No content type has ever had anything like this many entries, so a count past
		// it means the manifest itself is damaged; leave the destination at its reset()
		// value rather than issue an absurd read.
		//
		// This is a plausibility bound, not a bounds check against the file. The stream
		// cannot be asked how many bytes remain -- GetSizeLeft() reports INT_MAX here --
		// so a read that is plausible but still longer than the save is not detectable
		// from inside the DLL.
		const int iMaxPlausibleCount = 1000000;
		if (iOld > iMaxPlausibleCount)
		{
			for (int i = 0; i < iNew; i++)
			{
				pDest[i] = T();
			}
			return;
		}

		if (piRemap == NULL && iOld == iNew)
		{
			// Nothing moved: byte-for-byte what the old code did. This is the path
			// every save without a manifest takes, and every save whose content
			// matches, so the common case carries no cost and no new risk.
			pStream->Read(iNew, pDest);

			if (pSavedOrder != NULL)
			{
				for (int i = 0; i < iNew; i++)
				{
					pSavedOrder[i] = pDest[i];
				}
			}
			return;
		}

		for (int i = 0; i < iNew; i++)
		{
			pDest[i] = T();
		}

		if (iOld > 0)
		{
			T* pTemp = new T[iOld];
			pStream->Read(iOld, pTemp);

			for (int i = 0; i < iOld; i++)
			{
				const int iTo = (piRemap != NULL) ? piRemap[i] : i;
				if (iTo >= 0 && iTo < iNew)
				{
					pDest[iTo] = pTemp[i];
				}
				if (pSavedOrder != NULL)
				{
					pSavedOrder[i] = pTemp[i];
				}
			}

			delete [] pTemp;
		}
	}

	// -----------------------------------------------------------------------------
	// Two-dimensional content arrays.
	//
	// readArray covers the one-dimensional form. The other shape the serialization
	// uses is a loop over a content count with a row read inside it:
	//
	//     for (int i = 0; i < GC.getNumFeatureInfos(); i++)
	//         pStream->Read(NUM_YIELD_TYPES, m_ppaaiFeatureYieldChange[i]);
	//
	// The bound is this build's count, so it is the same mismatch readArray exists to
	// fix -- but applied once per row, so it is off by the row width TIMES the
	// difference, and it carries the whole rest of the save with it. Five features
	// added to a mod costs 60 bytes here, and the wreckage surfaces in the freelists
	// a few lines later as a zero slot count meeting a live entry count in a null
	// array, which reads as a crash in code that is not at fault.
	//
	// These read the save's row count and place each row where its content lives now.
	// A row whose content this build no longer has is still read -- it is in the
	// stream either way -- and discarded.
	// -----------------------------------------------------------------------------

	// Rows of iRowLen values each, one row per entry of eRowType. The row width is a
	// fixed engine constant (NUM_YIELD_TYPES, NUM_COMMERCE_TYPES, the project cap),
	// not content, so it cannot move between builds.
	template <class T>
	void readRows(FDataStreamBase* pStream, ContentType eRowType, T** ppDest, int iRowLen)
	{
		const int iOld = savedCount(eRowType);
		const int iNew = currentCount(eRowType);
		const int* piRemap = remapTable(eRowType);

		if (iRowLen <= 0)
		{
			return;
		}

		// Same plausibility bound, and the same reasoning, as readArray.
		const int iMaxPlausibleCount = 1000000;
		if (iOld > iMaxPlausibleCount)
		{
			for (int i = 0; i < iNew; i++)
			{
				for (int j = 0; j < iRowLen; j++)
				{
					ppDest[i][j] = T();
				}
			}
			return;
		}

		if (piRemap == NULL && iOld == iNew)
		{
			// Nothing moved: exactly the loop this replaced.
			for (int i = 0; i < iNew; i++)
			{
				pStream->Read(iRowLen, ppDest[i]);
			}
			return;
		}

		for (int i = 0; i < iNew; i++)
		{
			for (int j = 0; j < iRowLen; j++)
			{
				ppDest[i][j] = T();
			}
		}

		T* pDiscard = new T[iRowLen];

		for (int i = 0; i < iOld; i++)
		{
			const int iTo = (piRemap != NULL) ? piRemap[i] : i;
			pStream->Read(iRowLen, (iTo >= 0 && iTo < iNew) ? ppDest[iTo] : pDiscard);
		}

		delete [] pDiscard;
	}

	// Rows that are themselves content arrays, so both axes move.
	template <class T>
	void readRows(FDataStreamBase* pStream, ContentType eRowType, ContentType eColType, T** ppDest)
	{
		const int iOld = savedCount(eRowType);
		const int iNew = currentCount(eRowType);
		const int* piRemap = remapTable(eRowType);
		const int iCols = currentCount(eColType);

		for (int i = 0; i < iNew; i++)
		{
			for (int j = 0; j < iCols; j++)
			{
				ppDest[i][j] = T();
			}
		}

		const int iMaxPlausibleCount = 1000000;
		if (iOld > iMaxPlausibleCount)
		{
			return;
		}

		// readArray always writes currentCount(eColType) entries, so the row handed
		// to it for dropped content has to be that wide.
		T* pDiscard = new T[(iCols > 0) ? iCols : 1];

		for (int i = 0; i < iOld; i++)
		{
			const int iTo = (piRemap != NULL) ? piRemap[i] : i;
			readArray(pStream, eColType, (iTo >= 0 && iTo < iNew) ? ppDest[iTo] : pDiscard);
		}

		delete [] pDiscard;
	}

	// One stored content id per entry of eRowType -- CvPlayer's civics, a CivicTypes
	// indexed by CivicOptionTypes. Both axes move: the row is placed by eRowType and
	// the value is remapped by eValueType.
	//
	// Absent rows are left at NO_X, not at zero. Zero is a real content index, and a
	// player silently running the first civic of an option they never had is worse
	// than one running none.
	template <class T>
	void readIdArray(FDataStreamBase* pStream, ContentType eRowType, ContentType eValueType, T* pDest)
	{
		const int iOld = savedCount(eRowType);
		const int iNew = currentCount(eRowType);
		const int* piRemap = remapTable(eRowType);

		for (int i = 0; i < iNew; i++)
		{
			pDest[i] = (T)-1;
		}

		const int iMaxPlausibleCount = 1000000;
		if (iOld > iMaxPlausibleCount)
		{
			return;
		}

		for (int i = 0; i < iOld; i++)
		{
			int iValue = 0;
			pStream->Read(&iValue);

			const int iTo = (piRemap != NULL) ? piRemap[i] : i;
			if (iTo >= 0 && iTo < iNew)
			{
				pDest[iTo] = (T)remapId(eValueType, iValue);
			}
		}
	}
}

#endif // CIV4_SAVE_MANIFEST_H
