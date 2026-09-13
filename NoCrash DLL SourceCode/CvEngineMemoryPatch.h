#ifndef CvEngineMemoryPatch_h
#define CvEngineMemoryPatch_h

//
// CvEngineMemoryPatch
//
// In-memory binary patches applied to the host engine executable
// (Civ4BeyondSword.exe) at DLL load time, to repair engine-side defects that
// we cannot fix in the engine source (it is not ours to recompile).
//
// Call installEngineMemoryPatches() exactly once, from DllMain
// (DLL_PROCESS_ATTACH), before the engine has had a chance to construct any of
// the objects being patched. Each individual patch validates a byte signature
// at its target and silently no-ops if the running EXE does not match the
// build it was authored against, so it is safe to ship.
//
void installEngineMemoryPatches();

#endif // CvEngineMemoryPatch_h
