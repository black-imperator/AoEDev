#pragma once

#ifndef CIV4_SNARKOPROFILER_H
#define CIV4_SNARKOPROFILER_H

class CvPlot;

class CvSnarkoProfiler
{
public:
	CvSnarkoProfiler();
	virtual ~CvSnarkoProfiler();

	void profile(CvString szFunc, bool bStopLogging = false);								// Exposed to Python

protected:
	CvString szLastFunc;
	int iLastTime;
};
#endif