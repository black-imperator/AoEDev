//
// CvEngineMemoryPatch.cpp
//
// In-memory binary patches to the host engine EXE (Civ4BeyondSword 3.19).
// See CvEngineMemoryPatch.h for the contract.
//
// -----------------------------------------------------------------------------
// PATCH #1 -- "Exit to Main Menu" teardown crash (engine AV at EXE +0x27fd04)
// -----------------------------------------------------------------------------
//
// Symptom
//   Intermittent first-chance access violation when leaving a game to the main
//   menu (and, less visibly, on other popup dispatch). Faulting instruction:
//       Civ4BeyondSword+0x27fd04:  cmp dword ptr [ecx],edi      ; ecx unmapped
//
// What crashes
//   +0x27fcf0 is a generic "find index by key" over a small container:
//       data  = *(this + 0x18);   if (!data)            return -1;
//       count = *(this + 0x1C);   if ((signed)count<=0) return -1;
//       for (i=0; i<count; i++)  if (data[i].key == searchKey) return i;  // 12-byte stride
//   The faulting read at +0x27fd04 is the first element compare.
//
// Root cause  (proven live via WinDbg, 2026-05-31)
//   The container lives at offset +0x308 of the engine's GUI/interface-manager
//   singleton (vtable at EXE 0x00aca7c8; lazily built in +0x27f670 via
//   operator new(0x6A0) + ctor at +0x26bec0; stored at global [0x00b84f78]).
//   The constructor zero-initializes many members -- the +0x340 container, the
//   +0x3A4 sub-objects, +0x544.., etc. -- but it never initializes the +0x308
//   container's data pointer (+0x320) or count (+0x324). operator new does not
//   zero memory, so those two fields retain recycled heap garbage for the whole
//   process lifetime.
//
//   The search therefore crashes iff the garbage data pointer is non-null AND
//   the garbage count is a positive signed int. That value is decided once, the
//   moment the singleton is allocated -- which is exactly why the crash is
//   intermittent across launches but deterministic within one launch (and why
//   it is unrelated to turns played, AI auto-play, or which screen is open).
//   Confirmed by writing {data=0xF0000000, count=0x53554245} into the live
//   field and reproducing the exact +0x27fd04 fault on demand.
//
// Fix
//   Supply the initialization the engine constructor forgot: zero the +0x308
//   container's data/count at construction. The container becomes a clean,
//   empty {NULL, 0}; the search always bails safely, and the engine's normal
//   "add element" path is still free to populate it later -- so no legitimate
//   use is broken. We install this as a 5-byte detour at the ctor entry into a
//   small code cave that replicates the displaced prologue, zeroes the two
//   fields (the object's `this` is in EAX at ctor entry), and jumps back.
//
// All EXE offsets below are RVAs from the image's preferred base 0x00400000;
// we resolve them against GetModuleHandle(NULL) so a relocated EXE still works.
//

#include "CvGameCoreDLL.h"          // pulls in <windows.h>
#include "CvEngineMemoryPatch.h"

namespace {

// ---- engine layout constants (Civ4BeyondSword 3.19) ----
const unsigned int RVA_MGR_CTOR = 0x0026bec0; // ctor of the GUI/interface-manager singleton
const unsigned int OFF_M_DATA   = 0x00000320; // uninitialized container data pointer
const unsigned int OFF_M_COUNT  = 0x00000324; // uninitialized container element count

// First bytes of the ctor, used as a safety signature so we never patch the
// wrong executable/version. These opcodes are image-base independent:
//   0066bec0  51            push ecx
//   0066bec1  53            push ebx
//   0066bec2  55            push ebp
//   0066bec3  56            push esi
//   0066bec4  57            push edi
//   0066bec5  8B F8         mov  edi,eax           ; edi = this (this arrives in EAX)
//   0066bec7  B8 ...        mov  eax, <vtable ptr>
//   0066becc  C7 07 ...     mov  dword ptr [edi], <vtable>
//   0066bed2  89 47 0C      mov  dword ptr [edi+0Ch], eax
bool ctorSignatureMatches(const unsigned char* p)
{
	static const unsigned char kPrologue[7] =
		{ 0x51, 0x53, 0x55, 0x56, 0x57, 0x8B, 0xF8 };
	for (int i = 0; i < 7; ++i)
	{
		if (p[i] != kPrologue[i]) return false;
	}
	// distinctive vtable store + first member store
	if (p[0x0C] != 0xC7 || p[0x0D] != 0x07) return false;            // mov [edi], imm32
	if (p[0x12] != 0x89 || p[0x13] != 0x47 || p[0x14] != 0x0C) return false; // mov [edi+0xC], eax
	return true;
}

bool installExitToMenuCtorFix()
{
	unsigned char* base = reinterpret_cast<unsigned char*>(GetModuleHandle(NULL));
	if (base == NULL) return false;

	unsigned char* ctor = base + RVA_MGR_CTOR;
	if (IsBadReadPtr(ctor, 0x16)) return false;
	if (!ctorSignatureMatches(ctor))
	{
		OutputDebugString("CvEngineMemoryPatch: ctor signature mismatch; "
						   "exit-to-menu fix NOT applied (unexpected EXE build)\n");
		return false;
	}

	// Allocate an executable code cave for the trampoline.
	unsigned char* cave = reinterpret_cast<unsigned char*>(
		VirtualAlloc(NULL, 64, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE));
	if (cave == NULL) return false;

	int n = 0;
	// Replicate the 5 push instructions we are about to overwrite.
	cave[n++] = 0x51;   // push ecx
	cave[n++] = 0x53;   // push ebx
	cave[n++] = 0x55;   // push ebp
	cave[n++] = 0x56;   // push esi
	cave[n++] = 0x57;   // push edi
	// mov dword ptr [eax+OFF_M_DATA], 0    -> C7 80 <disp32> <imm32>   (eax == this)
	cave[n++] = 0xC7; cave[n++] = 0x80;
	*reinterpret_cast<unsigned int*>(cave + n) = OFF_M_DATA;  n += 4;
	*reinterpret_cast<unsigned int*>(cave + n) = 0;          n += 4;
	// mov dword ptr [eax+OFF_M_COUNT], 0
	cave[n++] = 0xC7; cave[n++] = 0x80;
	*reinterpret_cast<unsigned int*>(cave + n) = OFF_M_COUNT; n += 4;
	*reinterpret_cast<unsigned int*>(cave + n) = 0;          n += 4;
	// jmp back to ctor+5 (the original 'mov edi,eax')
	cave[n++] = 0xE9;
	unsigned char* jmpBackTarget = ctor + 5;
	*reinterpret_cast<int*>(cave + n) =
		static_cast<int>(jmpBackTarget - (cave + n + 4));
	n += 4;
	FlushInstructionCache(GetCurrentProcess(), cave, n);

	// Overwrite the 5 prologue push bytes with `jmp cave`.
	DWORD oldProtect = 0;
	if (!VirtualProtect(ctor, 5, PAGE_EXECUTE_READWRITE, &oldProtect))
	{
		return false;
	}
	ctor[0] = 0xE9; // jmp rel32
	*reinterpret_cast<int*>(ctor + 1) =
		static_cast<int>(cave - (ctor + 5));
	VirtualProtect(ctor, 5, oldProtect, &oldProtect);
	FlushInstructionCache(GetCurrentProcess(), ctor, 5);

	OutputDebugString("CvEngineMemoryPatch: exit-to-main-menu ctor fix installed\n");
	return true;
}

} // anonymous namespace

void installEngineMemoryPatches()
{
	installExitToMenuCtorFix();
}
