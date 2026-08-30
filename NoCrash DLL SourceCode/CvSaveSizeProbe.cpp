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

void CvSaveSizeProbe::countObject(const char* szClass)
{
	if (isEnabled())
	{
		g_totals[std::string(szClass)].iCount++;
	}
}

void CvSaveSizeProbe::countTagged(const char* szClass, int iBytes)
{
	if (isEnabled() && iBytes > 0)
	{
		g_totals[std::string(szClass)].iBytes += iBytes;
	}
}

void CvSaveSizeProbe::flush()
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
	if (fp != NULL)
	{
		int iObjects = 0;
		int iTagged = 0;
		for (std::map<std::string, Entry>::const_iterator it = g_totals.begin();
			it != g_totals.end(); ++it)
		{
			iObjects += it->second.iCount;
			iTagged += it->second.iBytes;
		}

		fprintf(fp, "---- %d objects, %d bytes in tagged records ----\n", iObjects, iTagged);
		fprintf(fp, "  %-22s %9s %13s %11s\n", "class", "objects", "taggedBytes", "perObject");

		for (std::map<std::string, Entry>::const_iterator it = g_totals.begin();
			it != g_totals.end(); ++it)
		{
			const int n = it->second.iCount;
			const int b = it->second.iBytes;
			fprintf(fp, "  %-22s %9d %13d %11d\n",
				it->first.c_str(), n, b, (n > 0) ? (b / n) : 0);
		}
		fprintf(fp, "\n");
		fclose(fp);
	}

	g_totals.clear();
}
