#include "CvGameCoreDLL.h"
#include "CvSaveSizeProbe.h"
#include "CvGlobals.h"
#include "CvDLLUtilityIFaceBase.h"

#include <map>
#include <string>

namespace
{
	int g_iLevel = -1;

	struct Entry
	{
		Entry() : iBytes(0), iCount(0) {}
		int iBytes;
		int iCount;
	};

	std::map<std::string, Entry> g_totals;

	int level()
	{
		if (g_iLevel < 0)
		{
			g_iLevel = GC.getDefineINT("SAVE_SIZE_PROBE", 0);
			if (g_iLevel < 0)
			{
				g_iLevel = 0;
			}
		}
		return g_iLevel;
	}
}

bool CvSaveSizeProbe::isEnabled()
{
	return level() > 0;
}

void CvSaveSizeProbe::begin()
{
	g_totals.clear();
}

void CvSaveSizeProbe::add(const char* szClass, int iBytes)
{
	if (iBytes < 0)
	{
		return;		// stream position went backwards; nothing useful to record
	}

	Entry& kEntry = g_totals[std::string(szClass)];
	kEntry.iBytes += iBytes;
	kEntry.iCount++;
}

void CvSaveSizeProbe::report()
{
	if (!isEnabled() || g_totals.empty())
	{
		return;
	}

	char szPath[MAX_PATH];
	szPath[0] = '\0';
	if (GetModuleFileNameA(GetModuleHandleA("CvGameCoreDLL.dll"), szPath, MAX_PATH) > 0)
	{
		char* pSlash = strrchr(szPath, '\\');
		if (pSlash != NULL)
		{
			*(pSlash + 1) = '\0';
		}
		else
		{
			szPath[0] = '\0';
		}
	}
	strncat(szPath, "CvGameCoreDLL_save_size.log", MAX_PATH - strlen(szPath) - 1);

	FILE* fp = fopen(szPath[0] ? szPath : "CvGameCoreDLL_save_size.log", "a");
	if (fp == NULL)
	{
		return;
	}

	int iTotal = 0;
	for (std::map<std::string, Entry>::const_iterator it = g_totals.begin();
		it != g_totals.end(); ++it)
	{
		iTotal += it->second.iBytes;
	}

	fprintf(fp, "---- save, %d bytes accounted for across %d classes ----\n",
		iTotal, (int)g_totals.size());

	for (std::map<std::string, Entry>::const_iterator it = g_totals.begin();
		it != g_totals.end(); ++it)
	{
		const int iBytes = it->second.iBytes;
		const int iCount = it->second.iCount;
		fprintf(fp, "  %-22s %10d bytes  %7d objects  %6d each  %5.1f%%\n",
			it->first.c_str(), iBytes, iCount,
			iCount > 0 ? iBytes / iCount : 0,
			iTotal > 0 ? (iBytes * 100.0) / iTotal : 0.0);
	}
	fprintf(fp, "\n");
	fclose(fp);

	if (gDLL != NULL)
	{
		gDLL->logMsg("save_size.log", "save size table written", false, true);
	}
}
