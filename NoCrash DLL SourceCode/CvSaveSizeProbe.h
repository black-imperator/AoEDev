#pragma once

#ifndef CIV4_SAVE_SIZE_PROBE_H
#define CIV4_SAVE_SIZE_PROBE_H

//
// Per-class accounting for a save, so where the bytes go is measured rather than
// reasoned about.
//
// This exists because reasoning about it kept being wrong. Tagging was predicted to
// shrink saves by 30% on a raw-byte model; the first real save grew 23%. Eliding
// defaults was predicted to recover that; it recovered 168 bytes. Converting the two
// largest classes was predicted to pull it back; it added another 3%. Three models,
// three wrong answers.
//
// Bytes are counted where they are produced. The first attempt read the stream position
// before and after each write() and measured every class as zero:
// FDataStreamBase::GetPosition() reports nothing useful on the save stream. CvTagWriter,
// on the other hand, knows exactly how many bytes it emitted.
//
// Off unless SAVE_SIZE_PROBE is set in GlobalDefinesAlt.xml.
//
namespace CvSaveSizeProbe
{
	bool isEnabled();

	// One object of this class was written.
	void countObject(const char* szClass);

	// A tagged record of this many bytes was written for this class.
	void countTagged(const char* szClass, int iBytes);

	// Dumps whatever has accumulated and starts again.
	//
	// There is no end-of-save hook in the DLL: the EXE drives the body and CvGame is
	// written FIRST, not last, so a report placed after it sees only itself -- which is
	// exactly what the first attempt produced. The table for one save is therefore
	// written out when the NEXT save or load begins.
	void flush();
}

#endif // CIV4_SAVE_SIZE_PROBE_H
