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
//
const unsigned int SAVE_FORMAT_VERSION = 4;

// First version that carries a manifest. Saves below this are read exactly as before.
// Deliberately NOT raised with SAVE_FORMAT_VERSION: a version 3 save has a manifest
// and positional CvGame fields, and must keep being read that way.
const unsigned int SAVE_FORMAT_VERSION_MANIFEST = 3;

// First version whose CvGame fields are tagged.
const unsigned int SAVE_FORMAT_VERSION_TAGGED = 4;

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
	void beginRead();

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

	template <class T>
	void readArray(FDataStreamBase* pStream, ContentType eType, T* pDest)
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
			}

			delete [] pTemp;
		}
	}
}

#endif // CIV4_SAVE_MANIFEST_H
