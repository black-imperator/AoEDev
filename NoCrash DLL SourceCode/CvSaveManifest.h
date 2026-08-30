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
class FDataStreamBase;

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
//
const unsigned int SAVE_FORMAT_VERSION = 3;

// First version that carries a manifest. Saves below this are read exactly as before.
const unsigned int SAVE_FORMAT_VERSION_MANIFEST = 3;

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
}

#endif // CIV4_SAVE_MANIFEST_H
