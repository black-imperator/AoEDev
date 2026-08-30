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
	// Written immediately after CvGame's uiFlag. Only for saves at
	// SAVE_FORMAT_VERSION_MANIFEST or later.
	void write(FDataStreamBase* pStream);

	// Reads the manifest and compares it against the content this build has loaded.
	// Any difference is reported to CvGameCoreDLL_corrupt_save.log, the engine log and
	// the debugger. Returns true when the save's content matches this build exactly.
	bool readAndCheck(FDataStreamBase* pStream);
}

#endif // CIV4_SAVE_MANIFEST_H
