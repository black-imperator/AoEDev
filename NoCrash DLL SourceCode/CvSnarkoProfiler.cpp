#include "CvGameCoreDLL.h"

#include "time.h"
#include "CvSnarkoProfiler.h"
#include "CvGlobals.h"	// for gDLL

CvSnarkoProfiler::CvSnarkoProfiler()
{
	szLastFunc = NULL;
	iLastTime = 0;
}

CvSnarkoProfiler::~CvSnarkoProfiler()
{
}

void CvSnarkoProfiler::profile(CvString szFunc, bool bStopLogging)
{
	int iNewTime = clock();
	if (szLastFunc != NULL)
	{
		int iTimeDiff = iNewTime - iLastTime;
		if (iTimeDiff > 0 && iLastTime !=0)
		{
			CvString szTimer;
			CvString szTemp;
			szTimer.append(CvString("Now Profiling:"));
			szTimer.append(szLastFunc);
			szTemp.Format(" Time elapsed: %i", iTimeDiff);
			szTimer.append(szTemp);
			gDLL->logMsg("Profilenew.log", szTimer);
		}
	}
	if (bStopLogging)
	{
		szLastFunc = NULL;
		iLastTime = 0;
	}
	else
	{
		szLastFunc = szFunc;
		iLastTime = clock();
	}
}