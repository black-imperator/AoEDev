#include "CvGameCoreDLL.h"
#include "CvGameCoreDLLUndefNew.h"
#include "CvReservePool.h"

// Target reserve. Picked from the observed VA budget (LAA 32-bit, ~4 GB),
// fragmentation-induced bad_alloc happens when largest free block falls
// under ~16 MB. A 64 MB hole gives the EXE one comfortable contiguous slot
// to recover any reasonable allocation.
static const SIZE_T CV_RESERVE_SIZES[] = {
	64 * 1024 * 1024,
	16 * 1024 * 1024,
	 4 * 1024 * 1024,
	 1 * 1024 * 1024,
};
static const int CV_RESERVE_TIERS =
	sizeof(CV_RESERVE_SIZES) / sizeof(CV_RESERVE_SIZES[0]);

CvReservePool::CvReservePool()
	: m_reserved(NULL)
	, m_size(0)
{
	reacquire();
}

CvReservePool::~CvReservePool()
{
	release();
}

CvReservePool& CvReservePool::get()
{
	static CvReservePool g;
	return g;
}

bool CvReservePool::release()
{
	if (!m_reserved)
	{
		return false;
	}
	VirtualFree(m_reserved, 0, MEM_RELEASE);
	m_reserved = NULL;
	m_size = 0;
	return true;
}

bool CvReservePool::reacquire()
{
	if (m_reserved)
	{
		return true;
	}
	for (int i = 0; i < CV_RESERVE_TIERS; ++i)
	{
		void* p = VirtualAlloc(NULL, CV_RESERVE_SIZES[i],
		                       MEM_RESERVE, PAGE_NOACCESS);
		if (p)
		{
			m_reserved = p;
			m_size = CV_RESERVE_SIZES[i];
			return true;
		}
	}
	return false;
}

bool CvOnBadAllocReleaseReserve()
{
	return CvReservePool::get().release();
}
