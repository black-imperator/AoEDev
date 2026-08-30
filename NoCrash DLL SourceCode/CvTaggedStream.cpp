// Deliberately free of CvGameCoreDLL.h: this is the one piece of the save format
// that can be exercised without the game, and a standalone test of it is worth more
// than the convenience of the umbrella header.
#include "CvTaggedStream.h"
#include <string.h>

namespace
{
	const int WIRE_VARINT = 0;
	const int WIRE_BYTES  = 1;

	// A record larger than this is not a record, it is a misread length. Refuse it
	// rather than trying to allocate it.
	const unsigned int MAX_RECORD_BYTES = 64u * 1024u * 1024u;

	// Small negatives should cost one byte, not five, so map signed onto unsigned by
	// alternating: 0, -1, 1, -2, 2 -> 0, 1, 2, 3, 4.
	inline unsigned int zigzag(int iValue)
	{
		return (unsigned int)((iValue << 1) ^ (iValue >> 31));
	}

	inline int unzigzag(unsigned int uiValue)
	{
		return (int)(uiValue >> 1) ^ -(int)(uiValue & 1);
	}
}

// ---------------------------------------------------------------------------
// Writer
// ---------------------------------------------------------------------------

CvTagWriter::CvTagWriter(FDataStreamBase* pStream)
	: m_pStream(pStream)
	, m_bEnded(false)
{
	// Most records are small; save the early reallocations.
	m_buffer.reserve(256);
}

void CvTagWriter::putVarint(unsigned int uiValue)
{
	while (uiValue >= 0x80u)
	{
		m_buffer.push_back((unsigned char)(uiValue | 0x80u));
		uiValue >>= 7;
	}
	m_buffer.push_back((unsigned char)uiValue);
}

void CvTagWriter::putKey(int iTag, int iWireType)
{
	putVarint(((unsigned int)iTag << 1) | (unsigned int)iWireType);
}

void CvTagWriter::putSigned(int iTag, int iValue)
{
	putKey(iTag, WIRE_VARINT);
	putVarint(zigzag(iValue));
}

void CvTagWriter::write(int iTag, int iValue)          { putSigned(iTag, iValue); }
void CvTagWriter::write(int iTag, short iValue)        { putSigned(iTag, (int)iValue); }
void CvTagWriter::write(int iTag, char iValue)         { putSigned(iTag, (int)iValue); }
void CvTagWriter::write(int iTag, bool bValue)         { putSigned(iTag, bValue ? 1 : 0); }

void CvTagWriter::writeIfNonZero(int iTag, int iValue)   { if (iValue != 0) putSigned(iTag, iValue); }
void CvTagWriter::writeIfNonZero(int iTag, short iValue) { if (iValue != 0) putSigned(iTag, (int)iValue); }
void CvTagWriter::writeIfNonZero(int iTag, char iValue)  { if (iValue != 0) putSigned(iTag, (int)iValue); }
void CvTagWriter::writeIfNonZero(int iTag, bool bValue)  { if (bValue) putSigned(iTag, 1); }

void CvTagWriter::write(int iTag, unsigned int uiValue)
{
	// Not zigzagged: an unsigned field has no small negatives to protect, and
	// zigzagging would double the cost of large values like a random seed.
	putKey(iTag, WIRE_VARINT);
	putVarint(uiValue);
}

void CvTagWriter::writeBytes(int iTag, const void* pData, int iLength)
{
	if (iLength < 0)
	{
		iLength = 0;
	}

	putKey(iTag, WIRE_BYTES);
	putVarint((unsigned int)iLength);

	const unsigned char* p = (const unsigned char*)pData;
	for (int i = 0; i < iLength; i++)
	{
		m_buffer.push_back(p[i]);
	}
}

CvTagWriter::~CvTagWriter()
{
	end();
}

void CvTagWriter::end()
{
	if (m_bEnded)
	{
		return;
	}
	m_bEnded = true;

	const unsigned int uiLength = (unsigned int)m_buffer.size();
	m_pStream->Write(uiLength);

	if (uiLength > 0)
	{
		m_pStream->Write((int)uiLength, (const unsigned char*)&m_buffer[0]);
	}
}

// ---------------------------------------------------------------------------
// Reader
// ---------------------------------------------------------------------------

CvTagReader::CvTagReader(FDataStreamBase* pStream)
	: m_iPos(0)
	, m_iTag(0)
	, m_iWireType(0)
	, m_bBad(false)
{
	unsigned int uiLength = 0;
	pStream->Read(&uiLength);

	if (uiLength > MAX_RECORD_BYTES)
	{
		// Do not trust it enough to allocate it. Nothing is consumed beyond the length
		// itself, so the caller still knows where it stands.
		m_bBad = true;
		return;
	}

	if (uiLength > 0)
	{
		m_buffer.resize(uiLength);
		pStream->Read((int)uiLength, (unsigned char*)&m_buffer[0]);
	}
}

unsigned int CvTagReader::getVarint()
{
	unsigned int uiValue = 0;
	int iShift = 0;

	while (m_iPos < (int)m_buffer.size())
	{
		const unsigned char c = m_buffer[m_iPos++];
		uiValue |= ((unsigned int)(c & 0x7F)) << iShift;

		if ((c & 0x80) == 0)
		{
			return uiValue;
		}

		iShift += 7;
		if (iShift > 28)
		{
			break;	// more continuation bytes than a 32 bit value can hold
		}
	}

	m_bBad = true;
	return 0;
}

bool CvTagReader::next()
{
	if (m_bBad || m_iPos >= (int)m_buffer.size())
	{
		return false;
	}

	const unsigned int uiKey = getVarint();
	if (m_bBad)
	{
		return false;
	}

	m_iTag = (int)(uiKey >> 1);
	m_iWireType = (int)(uiKey & 1);
	return true;
}

int CvTagReader::asInt()
{
	if (m_iWireType != WIRE_VARINT)
	{
		// Tag reused for a different shape than this build expects. Skipping keeps the
		// rest of the record readable instead of misparsing from here on.
		skip();
		m_bBad = true;
		return 0;
	}
	return unzigzag(getVarint());
}

bool CvTagReader::asBool()
{
	return asInt() != 0;
}

int CvTagReader::asBytes(void* pDest, int iLength)
{
	if (m_iWireType != WIRE_BYTES)
	{
		skip();
		m_bBad = true;
		return 0;
	}

	const unsigned int uiAvail = getVarint();
	if (m_bBad || (int)(m_iPos + uiAvail) > (int)m_buffer.size())
	{
		m_bBad = true;
		return 0;
	}

	const int iCopy = ((int)uiAvail < iLength) ? (int)uiAvail : iLength;
	if (iCopy > 0)
	{
		memcpy(pDest, &m_buffer[m_iPos], iCopy);
	}

	m_iPos += (int)uiAvail;
	return iCopy;
}

void CvTagReader::skip()
{
	if (m_iWireType == WIRE_VARINT)
	{
		getVarint();
		return;
	}

	const unsigned int uiLength = getVarint();
	if (m_bBad || (int)(m_iPos + uiLength) > (int)m_buffer.size())
	{
		m_bBad = true;
		return;
	}
	m_iPos += (int)uiLength;
}
