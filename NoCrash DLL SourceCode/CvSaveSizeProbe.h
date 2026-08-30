#pragma once

#ifndef CIV4_SAVE_SIZE_PROBE_H
#define CIV4_SAVE_SIZE_PROBE_H

#include "FDataStreamBase.h"

//
// Per-class byte accounting for a save, so where the bytes go is measured rather than
// reasoned about.
//
// This exists because reasoning about it kept being wrong. Tagging was predicted to
// shrink saves by 30% on a raw-byte model; the first real save grew 23%. Eliding
// defaults was predicted to recover that; it recovered 168 bytes. Converting the two
// largest classes was predicted to pull it back; it added another 3%. Three models,
// three wrong answers -- at which point the only useful thing to do is count.
//
// Scoped: construct at the top of a write(), and the destructor adds the bytes that
// function produced to that class's running total. Nested writes are attributed to the
// innermost probe, which is what you want -- a city's own bytes should not be charged
// to the player that owns it.
//
// Off unless SAVE_SIZE_PROBE is set in GlobalDefinesAlt.xml.
//
namespace CvSaveSizeProbe
{
	bool isEnabled();

	// Zero the totals. Called at the top of the outermost write.
	void begin();

	// Write the table to CvGameCoreDLL_save_size.log. Called when the save is complete.
	void report();

	void add(const char* szClass, int iBytes);
}


class CvSaveSizeScope
{
public:
	CvSaveSizeScope(FDataStreamBase* pStream, const char* szClass)
		: m_pStream(pStream)
		, m_szClass(szClass)
		, m_uiStart(0)
	{
		if (CvSaveSizeProbe::isEnabled())
		{
			m_uiStart = pStream->GetPosition();
		}
	}

	~CvSaveSizeScope()
	{
		if (CvSaveSizeProbe::isEnabled())
		{
			CvSaveSizeProbe::add(m_szClass, (int)(m_pStream->GetPosition() - m_uiStart));
		}
	}

private:
	FDataStreamBase* m_pStream;
	const char* m_szClass;
	unsigned int m_uiStart;

	CvSaveSizeScope(const CvSaveSizeScope&);
	CvSaveSizeScope& operator=(const CvSaveSizeScope&);
};

#endif // CIV4_SAVE_SIZE_PROBE_H
