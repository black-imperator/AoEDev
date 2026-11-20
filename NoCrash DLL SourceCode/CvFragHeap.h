#pragma once
#ifndef CV_FRAG_HEAP_H
#define CV_FRAG_HEAP_H

#include <windows.h>

//
// CvFragHeap
//   Private Low-Fragmentation Heap for CvGameCoreDLL's internal object allocations
//   (FFreeListTrashArray<T> nodes and T objects). Bypasses gDLL->newMem so we do
//   not pollute the EXE's process heap, which on long sessions fragments to
//   ~13 MB largest free block and triggers std::bad_alloc in the EXE.
//
//   Only use for allocations whose pointers never cross the DLL/EXE boundary.
//   Cross-boundary objects MUST keep using gDLL->newMem to stay free-compatible
//   with the EXE.
//
class CvFragHeap
{
public:
	static CvFragHeap& get();

	void* alloc(size_t bytes);
	void  free(void* p);
	void* realloc(void* p, size_t bytes);

	// HeapCompact: returns the size (bytes) of the largest committed free block
	// after coalescing. Useful as a telemetry signal between turns.
	size_t compact();

	// Returns false if HeapCreate failed (caller falls back to gDLL->newMem).
	bool   ok() const { return m_heap != NULL; }

private:
	CvFragHeap();
	~CvFragHeap();
	CvFragHeap(const CvFragHeap&);
	CvFragHeap& operator=(const CvFragHeap&);

	HANDLE m_heap;
};

#endif // CV_FRAG_HEAP_H
