#pragma once

#ifndef CIV4_TAGGED_STREAM_H
#define CIV4_TAGGED_STREAM_H

#include "FDataStreamBase.h"
#include <vector>

//
// Self-describing field encoding for read()/write().
//
// The positional format has no room for change: every field is identified purely by
// how many bytes precede it, so adding, removing or reordering one shifts everything
// after it and the reader decodes garbage. Every uiFlag ladder in this codebase exists
// to work around that, one field at a time, by hand.
//
// Here each field carries its own tag and is self-delimiting, so:
//
//   - a field the reader does not know is skipped, not fatal. An older build can read
//     a newer save as long as it only needs the fields it already understands.
//   - a field the writer did not emit keeps whatever reset() gave it. Removing a field
//     costs nothing.
//   - order stops mattering. Fields can be written in any order and regrouped freely.
//
// Wire format, protobuf's, because it is small and proven:
//
//   record  := varint byteLength, then that many bytes of fields
//   field   := varint key, payload
//   key     := (tag << 1) | wiretype
//   payload := wiretype 0 -> one varint (self-delimiting)
//              wiretype 1 -> varint byteLength, then that many bytes
//
// Signed values are zigzagged so small negatives stay one byte. A typical small int
// costs one byte of key plus one of value, against four for a raw int today -- so a
// tagged save is expected to be SMALLER than a positional one, not larger.
//
// The whole record is length-prefixed and buffered in memory: one bulk stream call per
// object instead of a virtual call per byte, and a record that fails to parse can be
// stepped over without taking the rest of the stream with it.
//
// Tag numbers are per class and MUST be append-only. Renumbering an existing tag makes
// every save written before the change decode that field as something else, silently.
// Retiring a field means leaving its tag unused, never reusing the number.
//

class CvTagWriter
{
public:
	explicit CvTagWriter(FDataStreamBase* pStream);
	~CvTagWriter();

	void write(int iTag, int iValue);
	void write(int iTag, short iValue);
	void write(int iTag, char iValue);
	void write(int iTag, bool bValue);
	void write(int iTag, unsigned int uiValue);

	// Omits the field entirely when it still holds the value reset() gave it. Absent
	// means "unchanged from the default", and the reader's own reset() has already put
	// it there, so nothing is lost.
	//
	// This is not a micro-optimisation, it is what makes the format viable. The save
	// body is zlib-compressed, and a positional zero is part of a long run of 0x00 that
	// compresses to almost nothing, while a varint key is entropy that does not compress
	// at all. Tagging every field shrank the RAW bytes by about 30% and grew the
	// COMPRESSED save by about the same -- measured, on a real save, not predicted.
	// Skipping defaults drops both the key and the value and brings it back to parity.
	//
	// Only correct where reset() sets the field to zero or false. Where it does not,
	// write() unconditionally: omitting a field whose default is non-zero would have the
	// reader keep that non-zero default instead of the zero that was meant.
	void writeIfNonZero(int iTag, int iValue);
	void writeIfNonZero(int iTag, short iValue);
	void writeIfNonZero(int iTag, char iValue);
	void writeIfNonZero(int iTag, bool bValue);

	// Raw block, for anything without a scalar form yet.
	void writeBytes(int iTag, const void* pData, int iLength);

	// Flushes the record. Called by the destructor if you forget, but call it.
	void end();

private:
	void putVarint(unsigned int uiValue);
	void putKey(int iTag, int iWireType);
	void putSigned(int iTag, int iValue);

	FDataStreamBase* m_pStream;
	std::vector<unsigned char> m_buffer;
	bool m_bEnded;

	CvTagWriter(const CvTagWriter&);
	CvTagWriter& operator=(const CvTagWriter&);
};


class CvTagReader
{
public:
	explicit CvTagReader(FDataStreamBase* pStream);

	// Advance to the next field. False when the record is exhausted.
	bool next();

	int tag() const { return m_iTag; }

	int  asInt();
	bool asBool();

	// Copies at most iLength bytes of a wiretype 1 payload; returns bytes copied.
	int  asBytes(void* pDest, int iLength);

	// Step over the current payload. The default arm of every dispatch switch.
	void skip();

	// True if the record ran short or malformed. The stream position is still correct
	// -- the record was length-prefixed and consumed whole -- so a damaged object costs
	// its own contents and nothing else.
	bool bad() const { return m_bBad; }

private:
	unsigned int getVarint();

	std::vector<unsigned char> m_buffer;
	int m_iPos;
	int m_iTag;
	int m_iWireType;
	bool m_bBad;

	CvTagReader(const CvTagReader&);
	CvTagReader& operator=(const CvTagReader&);
};

#endif // CIV4_TAGGED_STREAM_H
