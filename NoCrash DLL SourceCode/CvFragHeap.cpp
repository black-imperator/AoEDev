#include "CvGameCoreDLL.h"
#include "CvGameCoreDLLUndefNew.h"
#include "CvFragHeap.h"

#include <new>

// Initial heap reserve. Picked to absorb a full game's FFreeListTrashArray<T>
// load (units + cities + selection groups + plot groups across all civs)
// without growing into a second segment. Tunable.
static const SIZE_T CV_FRAG_HEAP_INITIAL = 16 * 1024 * 1024;  // 16 MB

CvFragHeap::CvFragHeap()
	: m_heap(NULL)
{
	m_heap = HeapCreate(0 /*flags*/, CV_FRAG_HEAP_INITIAL, 0 /*growable*/);
	if (m_heap)
	{
		// Enable Low Fragmentation Heap. Size-bucketed allocs prevent the
		// fine-grained external fragmentation that the EXE's heap exhibits.
		ULONG info = 2;  // HEAP_LFH
		HeapSetInformation(m_heap, (HEAP_INFORMATION_CLASS)0 /*HeapCompatibilityInformation*/,
		                   &info, sizeof(info));
	}
}

CvFragHeap::~CvFragHeap()
{
	if (m_heap)
	{
		HeapDestroy(m_heap);
		m_heap = NULL;
	}
}

CvFragHeap& CvFragHeap::get()
{
	static CvFragHeap g;
	return g;
}

void* CvFragHeap::alloc(size_t bytes)
{
	if (!m_heap)
	{
		throw std::bad_alloc();
	}
	void* p = HeapAlloc(m_heap, 0, bytes);
	if (!p)
	{
		throw std::bad_alloc();
	}
	return p;
}

void CvFragHeap::free(void* p)
{
	if (p && m_heap)
	{
		HeapFree(m_heap, 0, p);
	}
}

void* CvFragHeap::realloc(void* p, size_t bytes)
{
	if (!m_heap)
	{
		throw std::bad_alloc();
	}
	if (!p)
	{
		return alloc(bytes);
	}
	void* r = HeapReAlloc(m_heap, 0, p, bytes);
	if (!r)
	{
		throw std::bad_alloc();
	}
	return r;
}

size_t CvFragHeap::compact()
{
	if (!m_heap)
	{
		return 0;
	}
	return (size_t)HeapCompact(m_heap, 0);
}
