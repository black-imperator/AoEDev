#pragma once
#ifndef CV_RESERVE_POOL_H
#define CV_RESERVE_POOL_H

#include <windows.h>

//
// CvReservePool
//   At DLL load, reserve a 64 MB contiguous virtual-address range with
//   MEM_RESERVE (no physical commit, so no real memory cost). The reserved
//   range cannot be allocated by anyone — including the EXE's heap — so it
//   stays untouched as the EXE fragments the rest of the address space.
//
//   When a std::bad_alloc fires inside the EXE (typical signature on long
//   sessions: 11k+ small fragments, < 16 MB largest free block), we release
//   our reservation. The EXE's next allocation attempt sees a fresh
//   contiguous 64 MB hole and succeeds.
//
//   This is a one-shot rescue per session by default. After release, we try
//   to re-acquire smaller fallbacks (16/4/1 MB). On next quiet turn we may
//   attempt to grab a bigger reserve again if VA permits.
//
class CvReservePool
{
public:
	static CvReservePool& get();

	// Release reserved VA back to the OS. Returns true if we held a reserve.
	bool release();

	// Attempt to reserve a fresh range. Tries 64/16/4/1 MB in order.
	// Returns true if any reservation succeeded.
	bool reacquire();

	bool   isReserved() const { return m_reserved != NULL; }
	size_t size()       const { return m_size; }

private:
	CvReservePool();
	~CvReservePool();
	CvReservePool(const CvReservePool&);
	CvReservePool& operator=(const CvReservePool&);

	void*  m_reserved;
	size_t m_size;
};

// Helper for catch (std::bad_alloc&) blocks at DLL export boundaries.
// Releases the reserve and returns true if anything was freed (caller should
// then retry the failing operation once).
bool CvOnBadAllocReleaseReserve();

#endif // CV_RESERVE_POOL_H
