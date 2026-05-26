//
// init/cleanup XML functions
//
#include "CvGameCoreDLL.h"
#include "CvXMLLoadUtility.h"
#include "CvGlobals.h"
#include "CvArtFileMgr.h"
#include "CvGameTextMgr.h"
#include "CvInfoWater.h"
#include "FProfiler.h"

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   InitStringList(CvString **ppszList, int iListLen, CvString szString = "")
//
//  PURPOSE :   allocate and initialize a CvString pointer list of iListLen size to "", or
//				to szString if it is supplied
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::InitStringList(CvString **ppszList, int iListLen, CvString szString)
{
	PROFILE_FUNC();
	int i;	// loop counter
	CvString* pszList;

	FAssertMsg(*ppszList == NULL,"memory leak?");
	FAssertMsg((0 < iListLen),"list size to allocate is less than 1");
	// allocate memory for the boolean pointer based on the list length parameter
	*ppszList = new CvString[iListLen];
	// set the local pointer to the memory we just allocated
	pszList = *ppszList;

	// loop through all the booleans
	for (int i=0;i<iListLen;i++)
	{
		// set the current boolean to false
		pszList[i] = szString;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   void Init2DFloatList(float*** pppfList, int iSizeX, int iSizeY)
//
//  PURPOSE :   allocate and initialize a 2d array of float data
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::Init2DFloatList(float*** pppfList, int iSizeX, int iSizeY)
{
	// SPEEDUP
	PROFILE_FUNC();
	int i,j;	// loop counters
	float** ppfList;

	FAssertMsg(*pppfList == NULL,"memory leak?");
	FAssertMsg(((0 < iSizeX) && (0 < iSizeY)), "list size to allocate is less than 1");
	// allocate the memory for the array of pointers to arrays of floats
	*pppfList = new float *[iSizeX];
	// set the local pointer to the newly allocated memory
	ppfList = *pppfList;

	// loop through each of the pointers
	for (int i=0;i<iSizeX;i++)
	{
		// allocate a list of floats for the current pointer
		ppfList[i] = new float[iSizeY];
		// loop through all of the current pointer's floats
		for (int j=0;j<iSizeY;j++)
		{
			// set the current float to zero
			ppfList[i][j] = 0.0f;
		}
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   void Init2DIntList(int*** pppiList, int iSizeX, int iSizeY)
//
//  PURPOSE :   allocate and initialize a 2d array of int data
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::Init2DIntList(int*** pppiList, int iSizeX, int iSizeY)
{
	// SPEEDUP
	PROFILE_FUNC();
	int i,j;	// loop counters
	int** ppiList;

	FAssertMsg(*pppiList == NULL,"memory leak?");
	FAssertMsg(((0 < iSizeX) && (0 < iSizeY)), "list size to allocate is less than 1");
	// allocate the memory for the array of pointers to arrays of ints
	*pppiList = new int *[iSizeX];
	// set the local pointer to the newly allocated memory
	ppiList = *pppiList;

	// loop through each of the pointers
	for (int i=0;i<iSizeX;i++)
	{
		// allocate a list of ints for the current pointer
		ppiList[i] = new int[iSizeY];
		// loop through all of the current pointer's ints
		for (int j=0;j<iSizeY;j++)
		{
			// set the current int to zero
			ppiList[i][j] = 0;
		}
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   void InitPointerFloatList(float*** pppfList, int iSizeX)
//
//  PURPOSE :   allocate and initialize a 2d array of float data
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::InitPointerFloatList(float*** pppfList, int iSizeX)
{
	// SPEEDUP
	PROFILE_FUNC();
	int i;	// loop counters
	float** ppfList;

	FAssertMsg(*pppfList == NULL,"memory leak?");
	FAssertMsg((0 < iSizeX), "list size to allocate is less than 1");
	// allocate the memory for the array of pointers to arrays of floats
	*pppfList = new float *[iSizeX];
	// set the local pointer to the newly allocated memory
	ppfList = *pppfList;

	// loop through each of the pointers
	for (int i=0;i<iSizeX;i++)
	{
		// Null each pointer
		ppfList[i] = NULL;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   void InitPointerIntList(int*** pppiList, int iSizeX)
//
//  PURPOSE :   allocate and initialize a 2d array of int data
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::InitPointerIntList(int*** pppiList, int iSizeX)
{
	// SPEEDUP
	PROFILE_FUNC();
	int i;	// loop counters
	int** ppiList;

	FAssertMsg(*pppiList == NULL,"memory leak?");
	FAssertMsg((0 < iSizeX), "list size to allocate is less than 1");
	// allocate the memory for the array of pointers to arrays of ints
	*pppiList = new int *[iSizeX];
	// set the local pointer to the newly allocated memory
	ppiList = *pppiList;

	// loop through each of the pointers
	for (int i=0;i<iSizeX;i++)
	{
		// Null each pointer
		ppiList[i] = NULL;
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   void Init2DDirectionTypesList(DirectionTypes*** pppiList, int iSizeX, int iSizeY)
//
//  PURPOSE :   allocate and initialize a 2d array of DirectionTypes data
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::Init2DDirectionTypesList(DirectionTypes*** pppiList, int iSizeX, int iSizeY)
{
	// SPEEDUP
	PROFILE_FUNC();
	int i,j;	// loop counters
	DirectionTypes** ppiList;

	FAssertMsg(*pppiList == NULL,"memory leak?");
	FAssertMsg(((0 < iSizeX) && (0 < iSizeY)), "list size to allocate is less than 1");
	// allocate the memory for the array of pointers to arrays of DirectionTypes
	*pppiList = new DirectionTypes *[iSizeX];
	// set the local pointer to the newly allocated memory
	ppiList = *pppiList;

	// loop through each of the pointers
	for (int i=0;i<iSizeX;i++)
	{
		// allocate a list of DirectionTypes for the current pointer
		ppiList[i] = new DirectionTypes[iSizeY];
		// loop through all of the current pointer's DirectionTypes
		for (int j=0;j<iSizeY;j++)
		{
			// set the current DirectionTypes to NO_DIRECTION
			ppiList[i][j] = NO_DIRECTION;
		}
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   InitImprovementBonusList(CvImprovementBonusInfo** ppImprovementBonus, int iListLen)
//
//  PURPOSE :   allocate a improvement bonus struct list of iListLen size and initialize it's members
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::InitImprovementBonusList(CvImprovementBonusInfo** ppImprovementBonus, int iListLen)
{
	// SPEEDUP
	PROFILE_FUNC();
	int i;	// loop counter
	CvImprovementBonusInfo* paImprovementBonus;

	FAssertMsg(*ppImprovementBonus == NULL,"memory leak?");
	FAssertMsg((0 < iListLen),"list size to allocate is less than 1");
	// allocate memory for the bonus type pointer based on the list length parameter
	*ppImprovementBonus = new CvImprovementBonusInfo[iListLen];
	// set the local pointer to the memory we just allocated
	paImprovementBonus = *ppImprovementBonus;

	// loop through all the bonus structs
	for (int i=0;i<iListLen;i++)
	{
		paImprovementBonus[i].m_bBonusMakesValid = false;
		paImprovementBonus[i].m_bBonusTrade = false;

#if 1
		FAssertMsg(paImprovementBonus[i].m_piYieldChange==NULL, "mem leak");
		paImprovementBonus[i].m_piYieldChange = new int[NUM_YIELD_TYPES];
		for (int j = 0; j < NUM_YIELD_TYPES; j++)
		{
			paImprovementBonus[i].m_piYieldChange[j] = 0;
		}
#endif

		paImprovementBonus[i].m_iDiscoverRand = 0;
/*************************************************************************************************/
/** SpreadBonus                 Opera                   28/08/09                                **/
/*************************************************************************************************/
		paImprovementBonus[i].m_iSpreadRand = 0;
/*************************************************************************************************/
/** SpreadBonus                 END                                                             **/
/*************************************************************************************************/
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   InitBuildingDefaults(int **ppiDefaults)
//
//  PURPOSE :   allocate and initialize the civilization's default buildings
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::InitBuildingDefaults(int **ppiDefaults)
{
	// SPEEDUP
	PROFILE_FUNC();

	int i;
	int* piDefaults;

	FAssertMsg(*ppiDefaults == NULL,"memory leak?");
	// allocate memory based on the number of building classes
	*ppiDefaults = new int[GC.getNumBuildingClassInfos()];
	// set the local pointer to the new memory
	piDefaults = *ppiDefaults;

	// loop through all the pointers and set their default values
	for (int i=0;i<GC.getNumBuildingClassInfos();i++)
	{
/*************************************************************************************************/
/**	Streamline							10/18/08									Xienwolf	**/
/**																								**/
/**				Initializes the UnitClass to default as NONE if flagged to be Unique			**/
/*************************************************************************************************/
		if (GC.getBuildingClassInfo((BuildingClassTypes)i).isUnique())
		{
			piDefaults[i] = -1;
		}
		else
/*************************************************************************************************/
/**	Streamline									END												**/
/*************************************************************************************************/
		piDefaults[i] = GC.getBuildingClassInfo((BuildingClassTypes) i).getDefaultBuildingIndex();
	}

}

void CvXMLLoadUtility::InitImprovementDefaults(int** ppiDefaults)
{
	// SPEEDUP
	PROFILE_FUNC();

	int i;
	int* piDefaults;

	FAssertMsg(*ppiDefaults == NULL, "memory leak?");
	// allocate memory based on the number of Improvement classes
	*ppiDefaults = new int[GC.getNumImprovementClassInfos()];
	// set the local pointer to the new memory
	piDefaults = *ppiDefaults;

	// loop through all the pointers and set their default values
	for (int i = 0; i < GC.getNumImprovementClassInfos(); i++)
	{
		/*************************************************************************************************/
		/**	Streamline							10/18/08									Xienwolf	**/
		/**																								**/
		/**				Initializes the UnitClass to default as NONE if flagged to be Unique			**/
		/*************************************************************************************************/
		if (GC.getImprovementClassInfo((ImprovementClassTypes)i).isUnique())
		{
			piDefaults[i] = -1;
		}
		else
			/*************************************************************************************************/
			/**	Streamline									END												**/
			/*************************************************************************************************/
			piDefaults[i] = GC.getImprovementClassInfo((ImprovementClassTypes)i).getDefaultImprovementIndex();
	}

}

void CvXMLLoadUtility::InitBuildingArtDefineDefaults(CvString** ppiDefaults)
{
	// SPEEDUP
	PROFILE_FUNC();

	int i;
	CvString* piDefaults;

	FAssertMsg(*ppiDefaults == NULL, "memory leak?");
	// allocate memory based on the number of building classes
	*ppiDefaults = new CvString[GC.getNumBuildingInfos()];
	// set the local pointer to the new memory
	piDefaults = *ppiDefaults;
	CvString cDefault = CvString::format("").GetCString();

	// loop through all the pointers and set their default values
	for (int i = 0; i < GC.getNumBuildingInfos(); i++)
	{

		piDefaults[i] = cDefault;
	}
}
void CvXMLLoadUtility::InitFeatureGraphicsDefaults(int** ppiDefaults)
{
	// SPEEDUP
	PROFILE_FUNC();

	int i;
	int* piDefaults;

	FAssertMsg(*ppiDefaults == NULL, "memory leak?");
	// allocate memory based on the number of building classes
	*ppiDefaults = new int[GC.getNumFeatureInfos()];
	// set the local pointer to the new memory
	piDefaults = *ppiDefaults;
	CvString cDefault = CvString::format("").GetCString();

	// loop through all the pointers and set their default values
	for (int i = 0; i < GC.getNumFeatureInfos(); i++)
	{

		piDefaults[i] = -1;
	}
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   InitUnitDefaults(int **ppiDefaults)
//
//  PURPOSE :   allocate and initialize the civilization's default Units
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::InitUnitDefaults(int **ppiDefaults)
{
	// SPEEDUP
	PROFILE_FUNC();

	int i;
	int* piDefaults;

	FAssertMsg(*ppiDefaults == NULL,"memory leak?");
	// allocate memory based on the number of uniting classes
	*ppiDefaults = new int[GC.getNumUnitClassInfos()];
	// set the local pointer to the new memory
	piDefaults = *ppiDefaults;

	// loop through all the pointers and set their default values
	for (int i=0;i<GC.getNumUnitClassInfos();i++)
	{
/*************************************************************************************************/
/**	Streamline							10/18/08									Xienwolf	**/
/**																								**/
/**			Initializes the BuildingClass to default as NONE if flagged to be Unique			**/
/*************************************************************************************************/
		if (GC.getUnitClassInfo((UnitClassTypes)i).isUnique())
		{
			piDefaults[i] = -1;
		}
		else
/*************************************************************************************************/
/**	Streamline									END												**/
/*************************************************************************************************/
		piDefaults[i] = GC.getUnitClassInfo((UnitClassTypes) i).getDefaultUnitIndex();
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   InitSpecialistDefaults(int **ppiDefaults)
//
//  PURPOSE :   allocate and initialize the civilization's default Specialists
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::InitSpecialistDefaults(int** ppiDefaults)
{
	// SPEEDUP
	PROFILE_FUNC();

	int i;
	int* piDefaults;

	FAssertMsg(*ppiDefaults == NULL, "memory leak?");
	// allocate memory based on the number of Specialisting classes
	*ppiDefaults = new int[GC.getNumSpecialistClassInfos()];
	// set the local pointer to the new memory
	piDefaults = *ppiDefaults;

	// loop through all the pointers and set their default values
	for (i = 0; i < GC.getNumSpecialistClassInfos(); i++)
	{
		/*************************************************************************************************/
		/**	Streamline							10/18/08									Xienwolf	**/
		/**																								**/
		/**			Initializes the SpecialistClass to default as NONE if flagged to be Unique			**/
		/*************************************************************************************************/
		if (GC.getSpecialistClassInfo((SpecialistClassTypes)i).isUnique())
		{
			piDefaults[i] = -1;
		}
		else
			/*************************************************************************************************/
			/**	Streamline									END												**/
			/*************************************************************************************************/
			piDefaults[i] = GC.getSpecialistClassInfo((SpecialistClassTypes)i).getDefaultSpecialistIndex();
	}
}


//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   CleanUpGlobals()
//
//  PURPOSE :   free the variables that are in globals.cpp/h
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::CleanUpGlobalVariables()
{
	GC.deleteInfoArrays();
}

/*************************************************************************************************/
/** AlignmentAttitudeModifier                   Opera                   13.09.09                **/
/*************************************************************************************************/
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   InitAlignmentAttitudeModifiersList(CvAlignmentAttitudeModifierInfo** ppAlignmentAttitudeModifier, int iListLen)
//
//  PURPOSE :   allocate a alignment attitude modifier struct list of iListLen size and initialize it's members
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::InitAlignmentAttitudeModifierList(CvAlignmentAttitudeModifierInfo** ppAlignmentAttitudeModifier, int iListLen)
{
	// SPEEDUP
	PROFILE_FUNC();
	int i;	// loop counter
	CvAlignmentAttitudeModifierInfo* paAlignmentAttitudeModifier;

	FAssertMsg(*ppAlignmentAttitudeModifier == NULL,"memory leak?");
	FAssertMsg((0 < iListLen),"list size to allocate is less than 1");
	// allocate memory for the bonus type pointer based on the list length parameter
	*ppAlignmentAttitudeModifier = new CvAlignmentAttitudeModifierInfo[iListLen];
	// set the local pointer to the memory we just allocated
	paAlignmentAttitudeModifier = *ppAlignmentAttitudeModifier;

	// loop through all the bonus structs
	for (int i=0;i<iListLen;i++)
	{
		paAlignmentAttitudeModifier[i].m_iToGood = -100;
		paAlignmentAttitudeModifier[i].m_iToNeutral = -100;
		paAlignmentAttitudeModifier[i].m_iToEvil = -100;
	}
}
/*************************************************************************************************/
/** AlignmentAttitudeModifier                   END                                             **/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   InitEthicalAlignmentAttitudeModifiersList(CvEthicalAlignmentAttitudeModifierInfo** ppEthicalAlignmentAttitudeModifier, int iListLen)
//
//  PURPOSE :   allocate a Ethical alignment attitude modifier struct list of iListLen size and initialize it's members
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::InitEthicalAlignmentAttitudeModifierList(CvEthicalAlignmentAttitudeModifierInfo** ppEthicalAlignmentAttitudeModifier, int iListLen)
{
	// SPEEDUP
	PROFILE_FUNC();
	int i;	// loop counter
	CvEthicalAlignmentAttitudeModifierInfo* paEthicalAlignmentAttitudeModifier;

	FAssertMsg(*ppEthicalAlignmentAttitudeModifier == NULL,"memory leak?");
	FAssertMsg((0 < iListLen),"list size to allocate is less than 1");
	// allocate memory for the bonus type pointer based on the list length parameter
	*ppEthicalAlignmentAttitudeModifier = new CvEthicalAlignmentAttitudeModifierInfo[iListLen];
	// set the local pointer to the memory we just allocated
	paEthicalAlignmentAttitudeModifier = *ppEthicalAlignmentAttitudeModifier;

	// loop through all the bonus structs
	for (int i=0;i<iListLen;i++)
	{
		paEthicalAlignmentAttitudeModifier[i].m_iToLawful = -100;
		paEthicalAlignmentAttitudeModifier[i].m_iToEthicalNeutral = -100;
		paEthicalAlignmentAttitudeModifier[i].m_iToChaotic = -100;
	}
}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
