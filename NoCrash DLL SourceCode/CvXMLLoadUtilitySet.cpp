//
// XML Set functions
//

#include "CvGameCoreDLL.h"
#include "CvDLLXMLIFaceBase.h"
#include "CvXMLLoadUtility.h"
#include "CvGlobals.h"
#include "CvArtFileMgr.h"
#include "CvGameTextMgr.h"
#include <algorithm>
#include "CvInfoWater.h"
#include "FProfiler.h"
#include "FVariableSystem.h"
#include "CvGameCoreUtils.h"
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**					Need to include this for a few function calls later on						**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
#include "CvXMLLoadUtilitySetMod.h"
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

// Macro for Setting Global Art Defines
#define INIT_XML_GLOBAL_LOAD(xmlInfoPath, infoArray, numInfos)  SetGlobalClassInfo(infoArray, xmlInfoPath, numInfos);

bool CvXMLLoadUtility::ReadGlobalDefines(const TCHAR* szXMLFileName, CvCacheObject* cache)
{
	bool bLoaded = false;	// used to make sure that the xml file was loaded correctly

	if (!gDLL->cacheRead(cache, szXMLFileName))			// src data file name
	{
		// load normally
		if (!CreateFXml())
		{
			return false;
		}

		// load the new FXml variable with the szXMLFileName file
		bLoaded = LoadCivXml(m_pFXml, szXMLFileName);
		if (!bLoaded)
		{
			char	szMessage[1024];
			sprintf( szMessage, "LoadXML call failed for %s \n Current XML file is: %s", szXMLFileName, GC.getCurrentXMLFile().GetCString());
			gDLL->MessageBox(szMessage, "XML Load Error");
		}

		// if the load succeeded we will continue
		if (bLoaded)
		{
			// locate the first define tag in the xml
			if (gDLL->getXMLIFace()->LocateNode(m_pFXml,"Civ4Defines/Define"))
			{
				int i;	// loop counter
				// get the number of other Define tags in the xml file
				int iNumDefines = gDLL->getXMLIFace()->GetNumSiblings(m_pFXml);
				// add one to the total in order to include the current Define tag
				iNumDefines++;

				// loop through all the Define tags
				for (int i=0;i<iNumDefines;i++)
				{
					char szNodeType[256];	// holds the type of the current node
					char szName[256];

					// Skip any comments and stop at the next value we might want
					if (SkipToNextVal())
					{
						// call the function that sets the FXml pointer to the first non-comment child of
						// the current tag and gets the value of that new node
						if (GetChildXmlVal(szName))
						{
							// set the FXml pointer to the next sibling of the current tag``
							if (gDLL->getXMLIFace()->NextSibling(GetXML()))
							{
								// Skip any comments and stop at the next value we might want
								if (SkipToNextVal())
								{
									// if we successfuly get the node type for the current tag
									if (gDLL->getXMLIFace()->GetLastLocatedNodeType(GetXML(),szNodeType))
									{
										// if the node type of the current tag isn't null
										if (strcmp(szNodeType,"")!=0)
										{
											// if the node type of the current tag is a float then
											if (strcmp(szNodeType,"float")==0)
											{
												// get the float value for the define
												float fVal;
												GetXmlVal(&fVal);
												GC.getDefinesVarSystem()->SetValue(szName, fVal);
											}
											// else if the node type of the current tag is an int then
											else if (strcmp(szNodeType,"int")==0)
											{
												// get the int value for the define
												int iVal;
												GetXmlVal(&iVal);
												GC.getDefinesVarSystem()->SetValue(szName, iVal);
											}
											// else if the node type of the current tag is a boolean then
											else if (strcmp(szNodeType,"boolean")==0)
											{
												// get the boolean value for the define
												bool bVal;
												GetXmlVal(&bVal);
												GC.getDefinesVarSystem()->SetValue(szName, bVal);
											}
											// otherwise we will assume it is a string/text value
											else
											{
												char szVal[256];
												// get the string/text value for the define
												GetXmlVal(szVal);
												GC.getDefinesVarSystem()->SetValue(szName, szVal);
											}
										}
										// otherwise we will default to getting the string/text value for the define
										else
										{
											char szVal[256];
											// get the string/text value for the define
											GetXmlVal(szVal);
											GC.getDefinesVarSystem()->SetValue(szName, szVal);
										}
									}
								}
							}

							// since we are looking at the children of a Define tag we will need to go up
							// one level so that we can go to the next Define tag.
							// Set the FXml pointer to the parent of the current tag
							gDLL->getXMLIFace()->SetToParent(GetXML());
						}
					}

					// now we set the FXml pointer to the sibling of the current tag, which should be the next
					// Define tag
					if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
					{
						break;
					}
				}

				// write global defines info to cache
				bool bOk = gDLL->cacheWrite(cache);
				if (!bOk)
				{
					char	szMessage[1024];
					sprintf( szMessage, "Failed writing to global defines cache. \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Caching Error");
				}
				else
				{
					logMsg("Wrote GlobalDefines to cache");
				}
			}
		}

		// delete the pointer to the FXml variable
		gDLL->getXMLIFace()->DestroyFXml(m_pFXml);
	}
	else
	{
		logMsg("Read GobalDefines from cache");
	}

	return true;
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetGlobalDefines()
//
//  PURPOSE :   Initialize the variables located in globaldefines.cpp/h with the values in
//				GlobalDefines.xml
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::SetGlobalDefines()
{
	UpdateProgressCB("GlobalDefines");

	/////////////////////////////////
	//
	// use disk cache if possible.
	// if no cache or cache is older than xml file, use xml file like normal, else read from cache
	//

	CvCacheObject* cache = gDLL->createGlobalDefinesCacheObject("GlobalDefines.dat");	// cache file name

	if (!ReadGlobalDefines("xml\\GlobalDefines.xml", cache))
	{
		return false;
	}

	if (!ReadGlobalDefines("xml\\GlobalDefinesAlt.xml", cache))
	{
		return false;
	}

	if (!ReadGlobalDefines("xml\\PythonCallbackDefines.xml", cache))
	{
		return false;
	}

/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
/*                                                                                              */
/* XML Options                                                                                  */
/************************************************************************************************/
	if (!ReadGlobalDefines("xml\\BBAI_Game_Options_GlobalDefines.xml", cache))
	{
		//return false;
	}

	if (!ReadGlobalDefines("xml\\BBAI_AI_Variables_GlobalDefines.xml", cache))
	{
		//return false;
	}

	if (!ReadGlobalDefines("xml\\TechDiffusion_GlobalDefines.xml", cache))
	{
		//return false;
	}

	if (!ReadGlobalDefines("xml\\LeadFromBehind_GlobalDefines.xml", cache))
	{
		//return false;
	}
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/

	if (gDLL->isModularXMLLoading())
	{
		std::vector<CvString> aszFiles;
		gDLL->enumerateFiles(aszFiles, "modules\\*_GlobalDefines.xml");

		for (std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
		{
			if (!ReadGlobalDefines(*it, cache))
			{
				return false;
			}
		}

		std::vector<CvString> aszModularFiles;
		gDLL->enumerateFiles(aszModularFiles, "modules\\*_PythonCallbackDefines.xml");

		for (std::vector<CvString>::iterator it = aszModularFiles.begin(); it != aszModularFiles.end(); ++it)
		{
			if (!ReadGlobalDefines(*it, cache))
			{
				return false;
			}
		}
	}
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**			Seems that this is allowing Modules to load even if disabled in the ini...			**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	else
	{
		std::vector<CvString> aszFiles;
		CvXMLLoadUtilitySetMod* pModEnumVector = new CvXMLLoadUtilitySetMod;
		aszFiles.reserve(10000);
		pModEnumVector->loadModControlArray(aszFiles, "globaldefines");

		for (std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
		{
			if (!ReadGlobalDefines(*it, cache))
			{
				return false;
			}
		}

		std::vector<CvString> aszModularFiles;
		aszModularFiles.reserve(10000);
		pModEnumVector->loadModControlArray(aszModularFiles, "pythoncallbackdefines");

		for (std::vector<CvString>::iterator it = aszModularFiles.begin(); it != aszModularFiles.end(); ++it)
		{
			if (!ReadGlobalDefines(*it, cache))
			{
				return false;
			}
		}
		aszFiles.clear();
		aszModularFiles.clear();
		SAFE_DELETE(pModEnumVector);
	}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/


	gDLL->destroyCache(cache);
	////////////////////////////////////////////////////////////////////////

	GC.cacheGlobals();

	return true;
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetPostGlobalsGlobalDefines()
//
//  PURPOSE :   This function assumes that the SetGlobalDefines function has already been called
//							it then loads the few global defines that needed to reference a global variable that
//							hadn't been loaded in prior to the SetGlobalDefines call
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::SetPostGlobalsGlobalDefines()
{
	const char* szVal=NULL;		// holds the string value from the define queue
	int idx;

	if (GC.getDefinesVarSystem()->GetSize() > 0)
	{
		SetGlobalDefine("LAND_TERRAIN", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("LAND_TERRAIN", idx);

		SetGlobalDefine("DEEP_WATER_TERRAIN", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("DEEP_WATER_TERRAIN", idx);

		SetGlobalDefine("SHALLOW_WATER_TERRAIN", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("SHALLOW_WATER_TERRAIN", idx);

		SetGlobalDefine("LAND_IMPROVEMENT", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("LAND_IMPROVEMENT", idx);

		SetGlobalDefine("WATER_IMPROVEMENT", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("WATER_IMPROVEMENT", idx);

		SetGlobalDefine("RUINS_IMPROVEMENT", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("RUINS_IMPROVEMENT", idx);

		SetGlobalDefine("NUKE_FEATURE", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("NUKE_FEATURE", idx);

		SetGlobalDefine("GLOBAL_WARMING_TERRAIN", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("GLOBAL_WARMING_TERRAIN", idx);

		SetGlobalDefine("CAPITAL_BUILDINGCLASS", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("CAPITAL_BUILDINGCLASS", idx);

		SetGlobalDefine("DEFAULT_SPECIALISTCLASS", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("DEFAULT_SPECIALISTCLASS", idx);

		SetGlobalDefine("INITIAL_CITY_ROUTE_TYPE", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("INITIAL_CITY_ROUTE_TYPE", idx);

		SetGlobalDefine("STANDARD_HANDICAP", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("STANDARD_HANDICAP", idx);

		SetGlobalDefine("STANDARD_HANDICAP_QUICK", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("STANDARD_HANDICAP_QUICK", idx);

		SetGlobalDefine("STANDARD_GAMESPEED", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("STANDARD_GAMESPEED", idx);

		SetGlobalDefine("STANDARD_TURNTIMER", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("STANDARD_TURNTIMER", idx);

		SetGlobalDefine("STANDARD_CLIMATE", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("STANDARD_CLIMATE", idx);

		SetGlobalDefine("STANDARD_SEALEVEL", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("STANDARD_SEALEVEL", idx);

		SetGlobalDefine("STANDARD_ERA", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("STANDARD_ERA", idx);

		SetGlobalDefine("STANDARD_CALENDAR", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("STANDARD_CALENDAR", idx);

		SetGlobalDefine("AI_HANDICAP", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("AI_HANDICAP", idx);

		SetGlobalDefine("BARBARIAN_HANDICAP", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("BARBARIAN_HANDICAP", idx);

		SetGlobalDefine("BARBARIAN_CIVILIZATION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("BARBARIAN_CIVILIZATION", idx);

		SetGlobalDefine("BARBARIAN_LEADER", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("BARBARIAN_LEADER", idx);

//FfH Units: Added by Kael 08/07/2007
		SetGlobalDefine("BONUS_MANA", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("BONUS_MANA", idx);

		SetGlobalDefine("BONUSCLASS_MANA", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("BONUSCLASS_MANA", idx);

		SetGlobalDefine("INVISIBLE_TYPE", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("INVISIBLE_TYPE", idx);

		SetGlobalDefine("FLAMES_EXPIRE_EFFECT", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("FLAMES_EXPIRE_EFFECT", idx);

		SetGlobalDefine("FLAMES_FEATURE", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("FLAMES_FEATURE", idx);

		SetGlobalDefine("FLAMES_SPREAD_EFFECT", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("FLAMES_SPREAD_EFFECT", idx);

		SetGlobalDefine("GREAT_COMMANDER_PROMOTION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("GREAT_COMMANDER_PROMOTION", idx);

		SetGlobalDefine("HIDDEN_NATIONALITY_PROMOTION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("HIDDEN_NATIONALITY_PROMOTION", idx);

		SetGlobalDefine("MUTATED_PROMOTION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("MUTATED_PROMOTION", idx);

		SetGlobalDefine("POISONED_PROMOTION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("POISONED_PROMOTION", idx);

		SetGlobalDefine("RANDOM_CIVILIZATION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("RANDOM_CIVILIZATION", idx);

		SetGlobalDefine("SPECIALUNIT_SPELL", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("SPECIALUNIT_SPELL", idx);
		
		SetGlobalDefine("SPECIALUNIT_BIRD", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("SPECIALUNIT_BIRD", idx);

		SetGlobalDefine("STARTING_SETTLER_PROMOTION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("STARTING_SETTLER_PROMOTION", idx);

		SetGlobalDefine("SLAVE_UNITCLASS", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("SLAVE_UNITCLASS", idx);

/*************************************************************************************************/
/**	Tierable								04/04/09								Xienwolf	**/
/**																								**/
/**						No longer need the DLL to directly handle Weapon upgrades				**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		SetGlobalDefine("WEAPON_PROMOTION_TIER1", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("WEAPON_PROMOTION_TIER1", idx);

		SetGlobalDefine("WEAPON_PROMOTION_TIER2", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("WEAPON_PROMOTION_TIER2", idx);

		SetGlobalDefine("WEAPON_PROMOTION_TIER3", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("WEAPON_PROMOTION_TIER3", idx);

		SetGlobalDefine("WEAPON_REQ_BONUS_TIER1", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("WEAPON_REQ_BONUS_TIER1", idx);

		SetGlobalDefine("WEAPON_REQ_BONUS_TIER2", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("WEAPON_REQ_BONUS_TIER2", idx);

		SetGlobalDefine("WEAPON_REQ_BONUS_TIER3", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("WEAPON_REQ_BONUS_TIER3", idx);
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Tierable								END													**/
/*************************************************************************************************/
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(GlobalInfos)			09/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in Globals								**/
/*************************************************************************************************/
		SetGlobalDefine("WORKER_UNITCOMBAT", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("WORKER_UNITCOMBAT", idx);

		SetGlobalDefine("PROMOTION_INVISIBLE_SHROUD", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("PROMOTION_INVISIBLE_SHROUD", idx);

		SetGlobalDefine("WITHDRAW_PROMOTION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("WITHDRAW_PROMOTION", idx);

		SetGlobalDefine("NULL_PROMOTION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("NULL_PROMOTION", idx);

		SetGlobalDefine("MISCAST_PROMOTION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("MISCAST_PROMOTION", idx);

		SetGlobalDefine("ORC_CIVILIZATION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("ORC_CIVILIZATION", idx);

		SetGlobalDefine("ORC_LEADER", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("ORC_LEADER", idx);

		SetGlobalDefine("ANIMAL_CIVILIZATION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("ANIMAL_CIVILIZATION", idx);

		SetGlobalDefine("ANIMAL_LEADER", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("ANIMAL_LEADER", idx);

		SetGlobalDefine("DEMON_CIVILIZATION", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("DEMON_CIVILIZATION", idx);

		SetGlobalDefine("DEMON_LEADER", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("DEMON_LEADER", idx);

		SetGlobalDefine("EQUIPMENT_HOLDER", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("EQUIPMENT_HOLDER", idx);

		SetGlobalDefine("COMMANDER_UNITCLASS", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("COMMANDER_UNITCLASS", idx);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	MISSION_CLAIM_FORT						11/06/10									Snarko	**/
/**																								**/
/**						Adding a mission for the claim_fort action...							**/
/*************************************************************************************************/
		SetGlobalDefine("FORT_COMMANDER_UNITCLASS", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("FORT_COMMANDER_UNITCLASS", idx);
/*************************************************************************************************/
/**	MISSION_CLAIM_FORT									END										**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
		SetGlobalDefine("MIST_FEATURE", szVal);
		idx = FindInInfoClass(szVal);
		GC.getDefinesVarSystem()->SetValue("MIST_FEATURE", idx);
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

		return true;
	}

	char	szMessage[1024];
	sprintf( szMessage, "Size of Global Defines is not greater than 0. \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
	gDLL->MessageBox(szMessage, "XML Load Error");

	return false;
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetGlobalTypes()
//
//  PURPOSE :   Initialize the variables located in globaltypes.cpp/h with the values in
//				GlobalTypes.xml
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::SetGlobalTypes()
{
	UpdateProgressCB("GlobalTypes");

	bool bLoaded = false;	// used to make sure that the xml file was loaded correctly
	if (!CreateFXml())
	{
		return false;
	}

	// load the new FXml variable with the GlobalTypes.xml file
	bLoaded = LoadCivXml(m_pFXml, "xml/GlobalTypes.xml");
	if (!bLoaded)
	{
		char	szMessage[1024];
		sprintf( szMessage, "LoadXML call failed for GlobalTypes.xml. \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Load Error");
	}

	// if the load succeeded we will continue
	if (bLoaded)
	{
		SetGlobalStringArray(&GC.getAnimationOperatorTypes(), "Civ4Types/AnimationOperatorTypes/AnimationOperatorType", &GC.getNumAnimationOperatorTypes());
		int iEnumVal = NUM_FUNC_TYPES;
		SetGlobalStringArray(&GC.getFunctionTypes(), "Civ4Types/FunctionTypes/FunctionType", &iEnumVal, true);
		SetGlobalStringArray(&GC.getFlavorTypes(), "Civ4Types/FlavorTypes/FlavorType", &GC.getNumFlavorTypes());
		SetGlobalStringArray(&GC.getArtStyleTypes(), "Civ4Types/ArtStyleTypes/ArtStyleType", &GC.getNumArtStyleTypes());
		SetGlobalStringArray(&GC.getCitySizeTypes(), "Civ4Types/CitySizeTypes/CitySizeType", &GC.getNumCitySizeTypes());
		iEnumVal = NUM_CONTACT_TYPES;
		SetGlobalStringArray(&GC.getContactTypes(), "Civ4Types/ContactTypes/ContactType", &iEnumVal, true);
		iEnumVal = NUM_DIPLOMACYPOWER_TYPES;
		SetGlobalStringArray(&GC.getDiplomacyPowerTypes(), "Civ4Types/DiplomacyPowerTypes/DiplomacyPowerType", &iEnumVal, true);
		iEnumVal = NUM_AUTOMATE_TYPES;
		SetGlobalStringArray(&GC.getAutomateTypes(), "Civ4Types/AutomateTypes/AutomateType", &iEnumVal, true);
		iEnumVal = NUM_DIRECTION_TYPES;
		SetGlobalStringArray(&GC.getDirectionTypes(), "Civ4Types/DirectionTypes/DirectionType", &iEnumVal, true);
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR				20/06/10										Snarko	**/
/**																								**/
/**							Moving explore lair results into SDK								**/
/*************************************************************************************************/
		SetGlobalStringArray(&GC.getGoodyClassTypes(), "Civ4Types/GoodyClassTypes/GoodyClassType", &GC.getNumGoodyClassTypes());
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR					END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Civilization Flavors				07/07/10										Snarko	**/
/**																								**/
/**							Making civilization flavors,										**/
/**			for helping AI with things we can't really add in a non-hardcoded way				**/
/*************************************************************************************************/
		SetGlobalStringArray(&GC.getCivFlavorTypes(), "Civ4Types/CivFlavorTypes/CivFlavorType", &GC.getNumCivFlavorTypes());
/*************************************************************************************************/
/**	Civilization Flavors					END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Improved AI								18/01/12								Snarko		**/
/**							Teaching the AI to go for victories.								**/
/*************************************************************************************************/
		SetGlobalStringArray(&GC.getAIVictoryTypes(), "Civ4Types/AIVictoryTypes/AIVictoryType", &GC.getNumAIVictoryTypes());
/*************************************************************************************************/
/**	Improved AI								END													**/
/*************************************************************************************************/
		SetGlobalStringArray(&GC.getFootstepAudioTypes(), "Civ4Types/FootstepAudioTypes/FootstepAudioType", &GC.getNumFootstepAudioTypes());
		iEnumVal = NUM_TRAITHOOK_TYPES;
		SetGlobalStringArray(&GC.getTraitHookTypes(), "Civ4Types/TraitHookTypes/TraitHookType", &iEnumVal, true);
		iEnumVal = NUM_TRADEABLE_ITEMS;
		SetGlobalStringArray(&GC.getTradeableItems(), "Civ4Types/TradeableItems/TradeableItem", &iEnumVal, true);

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
		gDLL->getXMLIFace()->SetToParent(m_pFXml);
		SetVariableListTagPair(&GC.getFootstepAudioTags(), "FootstepAudioTags", GC.getFootstepAudioTypes(), GC.getNumFootstepAudioTypes(), "");
	}

	// delete the pointer to the FXml variable
	DestroyFXml();

	return true;
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetDiplomacyCommentTypes()
//
//  PURPOSE :   Creates a full list of Diplomacy Comments
//
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetDiplomacyCommentTypes(CvString** ppszString, int* iNumVals)
{
	FAssertMsg(false, "should never get here");
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetupGlobalLandscapeInfos()
//
//  PURPOSE :   Initialize the appropriate variables located in globals.cpp/h with the values in
//				Terrain\Civ4TerrainSettings.xml
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::SetupGlobalLandscapeInfo()
{
	if (!CreateFXml())
	{
		return false;
	}

	LoadGlobalClassInfo(GC.getLandscapeInfo(), "CIV4TerrainSettings", "Terrain", "Civ4TerrainSettings/LandscapeInfos/LandscapeInfo", false);

	// delete the pointer to the FXml variable
	DestroyFXml();

	return true;
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetGlobalArtDefines()
//
//  PURPOSE :   Initialize the appropriate variables located in globals.cpp/h with the values in
//				Civ4ArtDefines.xml
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::SetGlobalArtDefines()
{
	if (!CreateFXml())
	{
		return false;
	}

	LoadGlobalClassInfo(ARTFILEMGR.getInterfaceArtInfo(), "CIV4ArtDefines_Interface", "Art", "Civ4ArtDefines/InterfaceArtInfos/InterfaceArtInfo", false);
	LoadGlobalClassInfo(ARTFILEMGR.getMovieArtInfo(), "CIV4ArtDefines_Movie", "Art", "Civ4ArtDefines/MovieArtInfos/MovieArtInfo", false);
	LoadGlobalClassInfo(ARTFILEMGR.getMiscArtInfo(), "CIV4ArtDefines_Misc", "Art", "Civ4ArtDefines/MiscArtInfos/MiscArtInfo", false);
	LoadGlobalClassInfo(ARTFILEMGR.getUnitArtInfo(), "CIV4ArtDefines_Unit", "Art", "Civ4ArtDefines/UnitArtInfos/UnitArtInfo", false);
	LoadGlobalClassInfo(ARTFILEMGR.getBuildingArtInfo(), "CIV4ArtDefines_Building", "Art", "Civ4ArtDefines/BuildingArtInfos/BuildingArtInfo", false);
	LoadGlobalClassInfo(ARTFILEMGR.getCivilizationArtInfo(), "CIV4ArtDefines_Civilization", "Art", "Civ4ArtDefines/CivilizationArtInfos/CivilizationArtInfo", false);
	LoadGlobalClassInfo(ARTFILEMGR.getLeaderheadArtInfo(), "CIV4ArtDefines_Leaderhead", "Art", "Civ4ArtDefines/LeaderheadArtInfos/LeaderheadArtInfo", false);
	LoadGlobalClassInfo(ARTFILEMGR.getBonusArtInfo(), "CIV4ArtDefines_Bonus", "Art", "Civ4ArtDefines/BonusArtInfos/BonusArtInfo", false);
	LoadGlobalClassInfo(ARTFILEMGR.getImprovementArtInfo(), "CIV4ArtDefines_Improvement", "Art", "Civ4ArtDefines/ImprovementArtInfos/ImprovementArtInfo", false);
	LoadGlobalClassInfo(ARTFILEMGR.getTerrainArtInfo(), "CIV4ArtDefines_Terrain", "Art", "Civ4ArtDefines/TerrainArtInfos/TerrainArtInfo", false);
	LoadGlobalClassInfo(ARTFILEMGR.getFeatureArtInfo(), "CIV4ArtDefines_Feature", "Art", "Civ4ArtDefines/FeatureArtInfos/FeatureArtInfo", false);

	DestroyFXml();

	return true;
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetGlobalText()
//
//  PURPOSE :   Handles all Global Text Infos
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::LoadGlobalText()
{
	CvCacheObject* cache = gDLL->createGlobalTextCacheObject("GlobalText.dat");	// cache file name
	if (!gDLL->cacheRead(cache))
	{
		bool bLoaded = false;

		if (!CreateFXml())
		{
			return false;
		}

		//
		// load all files in the xml text directory
		//
		std::vector<CvString> aszFiles;
		std::vector<CvString> aszModfiles;

		gDLL->enumerateFiles(aszFiles, "xml\\text\\*.xml");

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**			Yeah, looks like you can't turn off modules anymore, handy though					**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
		if (gDLL->isModularXMLLoading())
		{
			gDLL->enumerateFiles(aszModfiles, "modules\\*_CIV4GameText.xml");
			aszFiles.insert(aszFiles.end(), aszModfiles.begin(), aszModfiles.end());
		}
/**								----  End Original Code  ----									**/
		gDLL->enumerateFiles(aszModfiles, "modules\\*_CIV4GameText*.xml");
		aszFiles.insert(aszFiles.end(), aszModfiles.begin(), aszModfiles.end());
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

		for(std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
		{
			bLoaded = LoadCivXml(m_pFXml, *it); // Load the XML
			if (!bLoaded)
			{
				char	szMessage[1024];
				sprintf( szMessage, "LoadXML call failed for %s. \n Current XML file is: %s", (*it).c_str(), GC.getCurrentXMLFile().GetCString());
				gDLL->MessageBox(szMessage, "XML Load Error");
			}
			if (bLoaded)
			{
				// if the xml is successfully validated
				SetGameText("Civ4GameText", "Civ4GameText/TEXT");
			}
		}

		DestroyFXml();

		// write global text info to cache
		bool bOk = gDLL->cacheWrite(cache);
		if (!bLoaded)
		{
			char	szMessage[1024];
			sprintf( szMessage, "Failed writing to Global Text cache. \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
			gDLL->MessageBox(szMessage, "XML Caching Error");
		}
		if (bOk)
		{
			logMsg("Wrote GlobalText to cache");
		}
	}	// didn't read from cache
	else
	{
		logMsg("Read GlobalText from cache");
	}

	gDLL->destroyCache(cache);

	return true;
}

bool CvXMLLoadUtility::LoadBasicInfos()
{
	if (!CreateFXml())
	{
		return false;
	}
	LoadGlobalClassInfo(GC.getLoreInfo(), "CIV4BasicInfos", "BasicInfos", "Civ4BasicInfos/LoreInfos/LoreInfo", false);
	LoadGlobalClassInfo(GC.getConceptInfo(), "CIV4BasicInfos", "BasicInfos", "Civ4BasicInfos/ConceptInfos/ConceptInfo", false);
	LoadGlobalClassInfo(GC.getNewConceptInfo(), "CIV4NewConceptInfos", "BasicInfos", "Civ4NewConceptInfos/NewConceptInfos/NewConceptInfo", false);
	LoadGlobalClassInfo(GC.getCityTabInfo(), "CIV4CityTabInfos", "BasicInfos", "Civ4CityTabInfos/CityTabInfos/CityTabInfo", false);
	LoadGlobalClassInfo(GC.getCalendarInfo(), "CIV4CalendarInfos", "BasicInfos", "Civ4CalendarInfos/CalendarInfos/CalendarInfo", false);
	LoadGlobalClassInfo(GC.getSeasonInfo(), "CIV4SeasonInfos", "BasicInfos", "Civ4SeasonInfos/SeasonInfos/SeasonInfo", false);
	LoadGlobalClassInfo(GC.getMonthInfo(), "CIV4MonthInfos", "BasicInfos", "Civ4MonthInfos/MonthInfos/MonthInfo", false);
	LoadGlobalClassInfo(GC.getDenialInfo(), "CIV4DenialInfos", "BasicInfos", "Civ4DenialInfos/DenialInfos/DenialInfo", false);
	LoadGlobalClassInfo(GC.getInvisibleInfo(), "CIV4InvisibleInfos", "BasicInfos", "Civ4InvisibleInfos/InvisibleInfos/InvisibleInfo", false);
	LoadGlobalClassInfo(GC.getUnitCombatInfo(), "CIV4UnitCombatInfos", "BasicInfos", "Civ4UnitCombatInfos/UnitCombatInfos/UnitCombatInfo", false);
	LoadGlobalClassInfo(GC.getDomainInfo(), "CIV4DomainInfos", "BasicInfos", "Civ4DomainInfos/DomainInfos/DomainInfo", false);
	LoadGlobalClassInfo(GC.getUnitAIInfo(), "CIV4UnitAIInfos", "BasicInfos", "Civ4UnitAIInfos/UnitAIInfos/UnitAIInfo", false);
	LoadGlobalClassInfo(GC.getAttitudeInfo(), "CIV4AttitudeInfos", "BasicInfos", "Civ4AttitudeInfos/AttitudeInfos/AttitudeInfo", false);
	LoadGlobalClassInfo(GC.getMemoryInfo(), "CIV4MemoryInfos", "BasicInfos", "Civ4MemoryInfos/MemoryInfos/MemoryInfo", false);

//FfH: Added by Kael 08/07/2007
	LoadGlobalClassInfo(GC.getAlignmentInfo(), "CIV4AlignmentInfos", "BasicInfos", "Civ4AlignmentInfos/AlignmentInfos/AlignmentInfo", false);
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	LoadGlobalClassInfo(GC.getEthicalAlignmentInfo(), "CIV4EthicalAlignmentInfos", "BasicInfos", "Civ4EthicalAlignmentInfos/EthicalAlignmentInfos/EthicalAlignmentInfo", false);
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	LeaderStatus Infos      				10/01/09								Valkrionn	**/
/*************************************************************************************************/
	LoadGlobalClassInfo(GC.getLeaderStatusInfo(), "CIV4LeaderStatusInfos", "BasicInfos", "Civ4LeaderStatusInfos/LeaderStatusInfos/LeaderStatusInfo", false);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	LoadGlobalClassInfo(GC.getDamageTypeInfo(), "CIV4DamageInfos", "BasicInfos", "Civ4DamageInfos/DamageInfos/DamageInfo", false);
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(BasicInfos)			12/22/08								Xienwolf	**/
/**																								**/
/**									Loads Information from XML									**/
/*************************************************************************************************/
	LoadGlobalClassInfo(GC.getFeatInfo(), "CIV4FeatInfos", "BasicInfos", "Civ4FeatInfos/FeatInfos/FeatInfo", false);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	DestroyFXml();
	return true;
}

//
// Globals which must be loaded before the main menus.
// Don't put anything in here unless it has to be loaded before the main menus,
// instead try to load things in LoadPostMenuGlobals()
//
bool CvXMLLoadUtility::LoadPreMenuGlobals()
{
	if (!CreateFXml())
	{
		return false;
	}

	// ModuleId Start
	LoadGlobalClassInfo(GC.getModuleIdInfo(), "CIV4ModuleIdInfos", "GameInfo", "Civ4ModuleIdInfos/ModuleIdInfos/ModuleIdInfo", false);
	LoadGlobalClassInfo(GC.getGameSpeedInfo(), "CIV4GameSpeedInfo", "GameInfo", "Civ4GameSpeedInfo/GameSpeedInfos/GameSpeedInfo", false);
	LoadGlobalClassInfo(GC.getTurnTimerInfo(), "CIV4TurnTimerInfo", "GameInfo", "Civ4TurnTimerInfo/TurnTimerInfos/TurnTimerInfo", false);
	LoadGlobalClassInfo(GC.getWorldInfo(), "CIV4WorldInfo", "GameInfo", "Civ4WorldInfo/WorldInfos/WorldInfo", false);
	LoadGlobalClassInfo(GC.getClimateInfo(), "CIV4ClimateInfo", "GameInfo", "Civ4ClimateInfo/ClimateInfos/ClimateInfo", false);
	LoadGlobalClassInfo(GC.getSeaLevelInfo(), "CIV4SeaLevelInfo", "GameInfo", "Civ4SeaLevelInfo/SeaLevelInfos/SeaLevelInfo", false);
	LoadGlobalClassInfo(GC.getAdvisorInfo(), "CIV4AdvisorInfos", "Interface", "Civ4AdvisorInfos/AdvisorInfos/AdvisorInfo", false);

//FlavourMod: Addded by Jean Elcard (ClimateSystem)
	LoadGlobalClassInfo(GC.getTerrainClassInfo(), "CIV4TerrainClassInfos", "Terrain", "Civ4TerrainClassInfos/TerrainClassInfos/TerrainClassInfo", false);
//FlavourMod: End Add

	LoadGlobalClassInfo(GC.getTerrainInfo(), "CIV4TerrainInfos", "Terrain", "Civ4TerrainInfos/TerrainInfos/TerrainInfo", false);

//FlavourMod: Addded by Jean Elcard (ClimateSystem)
	for (int i=0; i < GC.getNumTerrainClassInfos(); ++i)
	{
		GC.getTerrainClassInfo((TerrainClassTypes)i).readPass3();
	}

	LoadGlobalClassInfo(GC.getClimateZoneInfo(), "CIV4ClimateZoneInfos", "Terrain", "Civ4ClimateZoneInfos/ClimateZoneInfos/ClimateZoneInfo", false);
//FlavourMod: End Add

	LoadGlobalClassInfo(GC.getEraInfo(), "CIV4EraInfos", "GameInfo", "Civ4EraInfos/EraInfos/EraInfo", false);
	LoadGlobalClassInfo(GC.getUnitClassInfo(), "CIV4UnitClassInfos", "Units", "Civ4UnitClassInfos/UnitClassInfos/UnitClassInfo", false);
	LoadGlobalClassInfo(GC.getSpecialistClassInfo(), "CIV4SpecialistClassInfos", "GameInfo", "Civ4SpecialistClassInfos/SpecialistClassInfos/SpecialistClassInfo", false);
	LoadGlobalClassInfo(GC.getSpecialistInfo(), "CIV4SpecialistInfos", "GameInfo", "Civ4SpecialistInfos/SpecialistInfos/SpecialistInfo", false);
	for (int i = 0; i < GC.getNumSpecialistClassInfos(); ++i)
	{
		GC.getSpecialistClassInfo((SpecialistClassTypes)i).readPass3();
	}
	LoadGlobalClassInfo(GC.getVoteSourceInfo(), "CIV4VoteSourceInfos", "GameInfo", "Civ4VoteSourceInfos/VoteSourceInfos/VoteSourceInfo", false);
	LoadGlobalClassInfo(GC.getTechInfo(), "CIV4TechInfos", "Technologies", "Civ4TechInfos/TechInfos/TechInfo", true, &CvDLLUtilityIFaceBase::createTechInfoCacheObject);

//FfH: Modified by Kael 08/26/2007
//	LoadGlobalClassInfo(GC.getFeatureInfo(), "Civ4FeatureInfos", "Terrain", "Civ4FeatureInfos/FeatureInfos/FeatureInfo", false);
//	LoadGlobalClassInfo(GC.getReligionInfo(), "CIV4ReligionInfo", "GameInfo", "Civ4ReligionInfo/ReligionInfos/ReligionInfo", false);
	LoadGlobalClassInfo(GC.getReligionInfo(), "CIV4ReligionInfo", "GameInfo", "Civ4ReligionInfo/ReligionInfos/ReligionInfo", false);
	LoadGlobalClassInfo(GC.getFeatureInfo(), "Civ4FeatureInfos", "Terrain", "Civ4FeatureInfos/FeatureInfos/FeatureInfo", true);
	// ModuleId Start
	LoadGlobalClassInfo(GC.getPlotEffectInfo(), "CIV4PlotEffectInfos", "Terrain", "Civ4PlotEffectInfos/PlotEffectInfos/PlotEffectInfo", false);
	//FfH: End Modify

	LoadGlobalClassInfo(GC.getAnimationCategoryInfo(), "CIV4AnimationInfos", "Units", "Civ4AnimationInfos/AnimationCategories/AnimationCategory", false);
	LoadGlobalClassInfo(GC.getAnimationPathInfo(), "CIV4AnimationPathInfos", "Units", "Civ4AnimationPathInfos/AnimationPaths/AnimationPath", false);

//FfH Damage Types: Modified by Kael 08/23/2007 (to move bonuses before promotions in the load order)
//	LoadGlobalClassInfo(GC.getPromotionInfo(), "CIV4PromotionInfos", "Units", "Civ4PromotionInfos/PromotionInfos/PromotionInfo", true, &CvDLLUtilityIFaceBase::createPromotionInfoCacheObject);
//	LoadGlobalClassInfo(GC.getTraitInfo(), "CIV4TraitInfos", "Civilizations", "Civ4TraitInfos/TraitInfos/TraitInfo", false);
//	LoadGlobalClassInfo(GC.getGoodyInfo(), "CIV4GoodyInfo", "GameInfo", "Civ4GoodyInfo/GoodyInfos/GoodyInfo", false);
//	LoadGlobalClassInfo(GC.getHandicapInfo(), "CIV4HandicapInfo", "GameInfo", "Civ4HandicapInfo/HandicapInfos/HandicapInfo", false, &CvDLLUtilityIFaceBase::createHandicapInfoCacheObject);
//	LoadGlobalClassInfo(GC.getCursorInfo(), "CIV4CursorInfo", "GameInfo", "Civ4CursorInfo/CursorInfos/CursorInfo", false);
//	LoadGlobalClassInfo(GC.getCivicOptionInfo(), "CIV4CivicOptionInfos", "GameInfo", "Civ4CivicOptionInfos/CivicOptionInfos/CivicOptionInfo", false);
//	LoadGlobalClassInfo(GC.getUpkeepInfo(), "CIV4UpkeepInfo", "GameInfo", "Civ4UpkeepInfo/UpkeepInfos/UpkeepInfo", false);
//	LoadGlobalClassInfo(GC.getHurryInfo(), "CIV4HurryInfo", "GameInfo", "Civ4HurryInfo/HurryInfos/HurryInfo", false);
//	LoadGlobalClassInfo(GC.getSpecialBuildingInfo(), "CIV4SpecialBuildingInfos", "Buildings", "Civ4SpecialBuildingInfos/SpecialBuildingInfos/SpecialBuildingInfo", false);
//	LoadGlobalClassInfo(GC.getCultureLevelInfo(), "CIV4CultureLevelInfo", "GameInfo", "Civ4CultureLevelInfo/CultureLevelInfos/CultureLevelInfo", false);
//	LoadGlobalClassInfo(GC.getBonusClassInfo(), "CIV4BonusClassInfos", "Terrain", "Civ4BonusClassInfos/BonusClassInfos/BonusClassInfo", false);
//	LoadGlobalClassInfo(GC.getVictoryInfo(), "CIV4VictoryInfo", "GameInfo", "Civ4VictoryInfo/VictoryInfos/VictoryInfo", false);
//	LoadGlobalClassInfo(GC.getBonusInfo(), "CIV4BonusInfos", "Terrain", "Civ4BonusInfos/BonusInfos/BonusInfo", false, &CvDLLUtilityIFaceBase::createBonusInfoCacheObject);
	LoadGlobalClassInfo(GC.getBonusClassInfo(), "CIV4BonusClassInfos", "Terrain", "Civ4BonusClassInfos/BonusClassInfos/BonusClassInfo", false);
	LoadGlobalClassInfo(GC.getBonusInfo(), "CIV4BonusInfos", "Terrain", "Civ4BonusInfos/BonusInfos/BonusInfo", false, &CvDLLUtilityIFaceBase::createBonusInfoCacheObject);
	
	// FlagSystem Start
	LoadGlobalClassInfo(GC.getFlagInfo(), "CIV4FlagInfos", "GameInfo", "Civ4FlagInfos/FlagInfos/FlagInfo", false);
	//PromotionClass
	LoadGlobalClassInfo(GC.getPromotionClassInfo(), "CIV4PromotionClassInfos", "Units", "Civ4PromotionClassInfos/PromotionClassInfos/PromotionClassInfo", false);
	
	LoadGlobalClassInfo(GC.getTraitClassInfo(), "CIV4TraitClassInfos", "Civilizations", "Civ4TraitClassInfos/TraitClassInfos/TraitClassInfo", false);
	LoadGlobalClassInfo(GC.getLeaderClassInfo(), "CIV4LeaderClassInfos", "Civilizations", "Civ4LeaderClassInfos/LeaderClassInfos/LeaderClassInfo", false);

	LoadGlobalClassInfo(GC.getSpecialUnitInfo(), "CIV4SpecialUnitInfos", "Units", "Civ4SpecialUnitInfos/SpecialUnitInfos/SpecialUnitInfo", false);
	LoadGlobalClassInfo(GC.getSpellClassInfo(), "CIV4SpellClassInfos", "Units", "Civ4SpellClassInfos/SpellClassInfos/SpellClassInfo", false);

	LoadGlobalClassInfo(GC.getPromotionInfo(), "CIV4PromotionInfos", "Units", "Civ4PromotionInfos/PromotionInfos/PromotionInfo", true, &CvDLLUtilityIFaceBase::createPromotionInfoCacheObject);
	LoadGlobalClassInfo(GC.getTraitInfo(), "CIV4TraitInfos", "Civilizations", "Civ4TraitInfos/TraitInfos/TraitInfo", true);
	LoadGlobalClassInfo(GC.getGoodyInfo(), "CIV4GoodyInfo", "GameInfo", "Civ4GoodyInfo/GoodyInfos/GoodyInfo", false);
	LoadGlobalClassInfo(GC.getHandicapInfo(), "CIV4HandicapInfo", "GameInfo", "Civ4HandicapInfo/HandicapInfos/HandicapInfo", false, &CvDLLUtilityIFaceBase::createHandicapInfoCacheObject);
	LoadGlobalClassInfo(GC.getCursorInfo(), "CIV4CursorInfo", "GameInfo", "Civ4CursorInfo/CursorInfos/CursorInfo", false);
	LoadGlobalClassInfo(GC.getCivicOptionInfo(), "CIV4CivicOptionInfos", "GameInfo", "Civ4CivicOptionInfos/CivicOptionInfos/CivicOptionInfo", false);
	LoadGlobalClassInfo(GC.getUpkeepInfo(), "CIV4UpkeepInfo", "GameInfo", "Civ4UpkeepInfo/UpkeepInfos/UpkeepInfo", false);
	LoadGlobalClassInfo(GC.getHurryInfo(), "CIV4HurryInfo", "GameInfo", "Civ4HurryInfo/HurryInfos/HurryInfo", false);
	LoadGlobalClassInfo(GC.getSpecialBuildingInfo(), "CIV4SpecialBuildingInfos", "Buildings", "Civ4SpecialBuildingInfos/SpecialBuildingInfos/SpecialBuildingInfo", false);
	LoadGlobalClassInfo(GC.getCultureLevelInfo(), "CIV4CultureLevelInfo", "GameInfo", "Civ4CultureLevelInfo/CultureLevelInfos/CultureLevelInfo", false);
/*************************************************************************************************/
/**	Reload									04/04/09								Xienwolf	**/
/**																								**/
/**					Second Pass to reference information within the same file					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	LoadGlobalClassInfo(GC.getVictoryInfo(), "CIV4VictoryInfo", "GameInfo", "Civ4VictoryInfo/VictoryInfos/VictoryInfo", false);
/**								----  End Original Code  ----									**/
	LoadGlobalClassInfo(GC.getVictoryInfo(), "CIV4VictoryInfo", "GameInfo", "Civ4VictoryInfo/VictoryInfos/VictoryInfo", true);
/*************************************************************************************************/
/**	Reload									END													**/
/*************************************************************************************************/
//FfH: End Modify

	LoadGlobalClassInfo(GC.getCorporationInfo(), "CIV4CorporationInfo", "GameInfo", "Civ4CorporationInfo/CorporationInfos/CorporationInfo", false);
	LoadGlobalClassInfo(GC.getRouteInfo(), "Civ4RouteInfos", "Misc", "Civ4RouteInfos/RouteInfos/RouteInfo", false);
	LoadGlobalClassInfo(GC.getImprovementClassInfo(), "CIV4ImprovementClassInfos", "Terrain", "Civ4ImprovementClassInfos/ImprovementClassInfos/ImprovementClassInfo", false);
	LoadGlobalClassInfo(GC.getImprovementInfo(), "CIV4ImprovementInfos", "Terrain", "Civ4ImprovementInfos/ImprovementInfos/ImprovementInfo", true, &CvDLLUtilityIFaceBase::createImprovementInfoCacheObject);
	for (int i = 0; i < GC.getNumImprovementClassInfos(); ++i)
	{
		GC.getImprovementClassInfo((ImprovementClassTypes)i).readPass3();
	}
	LoadGlobalClassInfo(GC.getBuildingClassInfo(), "CIV4BuildingClassInfos", "Buildings", "Civ4BuildingClassInfos/BuildingClassInfos/BuildingClassInfo", false);
	LoadGlobalClassInfo(GC.getCivicInfo(), "CIV4CivicInfos", "GameInfo", "Civ4CivicInfos/CivicInfos/CivicInfo", false, &CvDLLUtilityIFaceBase::createCivicInfoCacheObject);
	LoadGlobalClassInfo(GC.getBuildingInfo(), "CIV4BuildingInfos", "Buildings", "Civ4BuildingInfos/BuildingInfos/BuildingInfo", false, &CvDLLUtilityIFaceBase::createBuildingInfoCacheObject);
	for (int i=0; i < GC.getNumBuildingClassInfos(); ++i)
	{
		GC.getBuildingClassInfo((BuildingClassTypes)i).readPass3();
	}
	LoadGlobalClassInfo(GC.getProjectInfo(), "CIV4ProjectInfo", "GameInfo", "Civ4ProjectInfo/ProjectInfos/ProjectInfo", true);
	for (int i=0; i < GC.getNumVoteSourceInfos(); ++i)
	{
		GC.getVoteSourceInfo((VoteSourceTypes)i).readPass3();
	}
	LoadGlobalClassInfo(GC.getLeaderHeadInfo(), "CIV4LeaderHeadInfos", "Civilizations", "Civ4LeaderHeadInfos/LeaderHeadInfos/LeaderHeadInfo", false, &CvDLLUtilityIFaceBase::createLeaderHeadInfoCacheObject);
	LoadGlobalClassInfo(GC.getColorInfo(), "CIV4ColorVals", "Interface", "Civ4ColorVals/ColorVals/ColorVal", false);
	LoadGlobalClassInfo(GC.getPlayerColorInfo(), "CIV4PlayerColorInfos", "Interface", "Civ4PlayerColorInfos/PlayerColorInfos/PlayerColorInfo", false);
	LoadGlobalClassInfo(GC.getEffectInfo(), "CIV4EffectInfos", "Misc", "Civ4EffectInfos/EffectInfos/EffectInfo", false);

	LoadGlobalClassInfo(GC.getEntityEventInfo(), "CIV4EntityEventInfos", "Units", "Civ4EntityEventInfos/EntityEventInfos/EntityEventInfo", false);
/*************************************************************************************************/
/**	LinkedBuilds							7/18/10									Valkrionn	**/
/**																								**/
/**		Creates a list of Builds, which are executed before the main build if reqs are met		**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	LoadGlobalClassInfo(GC.getBuildInfo(), "CIV4BuildInfos", "Units", "Civ4BuildInfos/BuildInfos/BuildInfo", false);
/**								----  End Original Code  ----									**/
	LoadGlobalClassInfo(GC.getBuildInfo(), "CIV4BuildInfos", "Units", "Civ4BuildInfos/BuildInfos/BuildInfo", true);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	LoadGlobalClassInfo(GC.getAffinityInfo(), "CIV4AffinityInfos", "Units", "Civ4AffinityInfos/AffinityInfos/AffinityInfo", false);
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/

//FfH Units: Modified by Kael 08/07/2007
//	LoadGlobalClassInfo(GC.getUnitInfo(), "CIV4UnitInfos", "Units", "Civ4UnitInfos/UnitInfos/UnitInfo", false, &CvDLLUtilityIFaceBase::createUnitInfoCacheObject);
	LoadGlobalClassInfo(GC.getUnitInfo(), "CIV4UnitInfos", "Units", "Civ4UnitInfos/UnitInfos/UnitInfo", true, &CvDLLUtilityIFaceBase::createUnitInfoCacheObject);
//FfH: End Add

	for (int i=0; i < GC.getNumUnitClassInfos(); ++i)
	{
		GC.getUnitClassInfo((UnitClassTypes)i).readPass3();
	}
	for (int i = 0; i < GC.getNumTraitInfos(); ++i)
	{
		GC.getTraitInfo((TraitTypes)i).readPass3();
	}

	LoadGlobalClassInfo(GC.getUnitArtStyleTypeInfo(), "CIV4UnitArtStyleTypeInfos", "Civilizations", "Civ4UnitArtStyleTypeInfos/UnitArtStyleTypeInfos/UnitArtStyleTypeInfo", false);
	LoadGlobalClassInfo(GC.getCivilizationInfo(), "CIV4CivilizationInfos", "Civilizations", "Civ4CivilizationInfos/CivilizationInfos/CivilizationInfo", true, &CvDLLUtilityIFaceBase::createCivilizationInfoCacheObject);
/*************************************************************************************************/
/**	StateNames								12/12/08								Jean Elcard	**/
/**																								**/
/**						Load the new XML file with the State Names Infos.						**/
/*************************************************************************************************/
	LoadGlobalClassInfo(GC.getStateNameInfo(), "CIV4StateNameInfos", "GameInfo", "Civ4StateNameInfos/StateNameInfos/StateNameInfo", false);
/*************************************************************************************************/
/**	StateNames								END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
	LoadGlobalClassInfo(GC.getSpawnGroupInfo(), "CIV4SpawnGroupInfos", "GameInfo", "Civ4SpawnGroupInfos/SpawnGroupInfos/SpawnGroupInfo", false);
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/
	LoadGlobalClassInfo(GC.getHints(), "CIV4Hints", "GameInfo", "Civ4Hints/HintInfos/HintInfo", false);
	LoadGlobalClassInfo(GC.getMainMenus(), "CIV4MainMenus", "Art", "Civ4MainMenus/MainMenus/MainMenu", false);
	LoadGlobalClassInfo(GC.getSlideShowInfo(), "CIV4SlideShowInfos", "Interface", "Civ4SlideShowInfos/SlideShowInfos/SlideShowInfo", false);
	LoadGlobalClassInfo(GC.getSlideShowRandomInfo(), "CIV4SlideShowRandomInfos", "Interface", "Civ4SlideShowRandomInfos/SlideShowRandomInfos/SlideShowRandomInfo", false);
	LoadGlobalClassInfo(GC.getWorldPickerInfo(), "CIV4WorldPickerInfos", "Interface", "Civ4WorldPickerInfos/WorldPickerInfos/WorldPickerInfo", false);
	LoadGlobalClassInfo(GC.getSpaceShipInfo(), "Civ4SpaceShipInfos", "Interface", "Civ4SpaceShipInfos/SpaceShipInfos/SpaceShipInfo", false);

	LoadGlobalClassInfo(GC.getYieldInfo(), "CIV4YieldInfos", "Terrain", "Civ4YieldInfos/YieldInfos/YieldInfo", false);
	LoadGlobalClassInfo(GC.getCommerceInfo(), "CIV4CommerceInfo", "GameInfo", "Civ4CommerceInfo/CommerceInfos/CommerceInfo", false);
	LoadGlobalClassInfo(GC.getGameOptionInfo(), "CIV4GameOptionInfos", "GameInfo", "Civ4GameOptionInfos/GameOptionInfos/GameOptionInfo", false);
	LoadGlobalClassInfo(GC.getMPOptionInfo(), "CIV4MPOptionInfos", "GameInfo", "Civ4MPOptionInfos/MPOptionInfos/MPOptionInfo", false);
	LoadGlobalClassInfo(GC.getForceControlInfo(), "CIV4ForceControlInfos", "GameInfo", "Civ4ForceControlInfos/ForceControlInfos/ForceControlInfo", false);

//FfH Spell System: Added by Kael 04/17/2008
	LoadGlobalClassInfo(GC.getEventInfo(), "CIV4EventInfos", "Events", "Civ4EventInfos/EventInfos/EventInfo", true, &CvDLLUtilityIFaceBase::createEventInfoCacheObject);
	LoadGlobalClassInfo(GC.getEventTriggerInfo(), "CIV4EventTriggerInfos", "Events", "Civ4EventTriggerInfos/EventTriggerInfos/EventTriggerInfo", false, &CvDLLUtilityIFaceBase::createEventTriggerInfoCacheObject);
	LoadGlobalClassInfo(GC.getSpellInfo(), "CIV4SpellInfos", "Units", "Civ4SpellInfos/SpellInfos/SpellInfo", false);
	LoadGlobalClassInfo(GC.getCityClassInfo(), "CIV4CityClassInfos", "Buildings", "Civ4CityClassInfos/CityClassInfos/CityClassInfo", false);
	for (int i=0; i < GC.getNumBonusInfos(); ++i)
	{
		GC.getBonusInfo((BonusTypes)i).readPass3();
	}
	for (int i=0; i < GC.getNumImprovementInfos(); ++i)
	{
		GC.getImprovementInfo((ImprovementTypes)i).readPass3();
	}
	for (int i=0; i < GC.getNumTechInfos(); ++i)
	{
		GC.getTechInfo((TechTypes)i).readPass3();
	}
	for (int i=0; i < GC.getNumCivicInfos(); ++i)
	{
		GC.getCivicInfo((CivicTypes)i).readPass3();
	}
	for (int i=0; i < GC.getNumPromotionInfos(); ++i)
	{
		GC.getPromotionInfo((PromotionTypes)i).readPass3();
	}
	for (int i = 0; i < GC.getNumSpellInfos(); ++i)
	{
		GC.getSpellInfo((SpellTypes)i).readPass3();
	}
	for (int i=0; i < GC.getNumUnitInfos(); ++i)
	{
		GC.getUnitInfo((UnitTypes)i).readPass3();
	}
	for (int i=0; i < GC.getNumProjectInfos(); ++i)
	{
		GC.getProjectInfo((ProjectTypes)i).readPass3();
	}
/*************************************************************************************************/
/**	CivPlotMods								03/23/09								Jean Elcard	**/
/**																								**/
/**			Obsolete FfH Code. Replaced with TerrainYieldChanges in CvCivilizationInfo.			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	for (int i=0; i < GC.getNumTerrainInfos(); ++i)
	{
		GC.getTerrainInfo((TerrainTypes)i).readPass3();
	}
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/
//FfH: End Add
/*************************************************************************************************/
/**	LeaderRelations		Opera (from poyuzhe)		31.05.09									**/
/*************************************************************************************************/
	LoadGlobalClassInfo(GC.getLeaderRelationInfo(), "CIV4LeaderRelationInfos", "Civilizations", "Civ4LeaderRelationInfos/LeaderRelationInfos/LeaderRelationInfo", false);
	LoadGlobalClassInfo(GC.getTraitTriggerInfo(), "CIV4TraitTriggerInfos", "Civilizations", "Civ4TraitTriggerInfos/TraitTriggerInfos/TraitTriggerInfo", false);
	/*************************************************************************************************/
/**	End																							**/
/*************************************************************************************************/

/**	New Tag Defs	(General)				12/31/08								Xienwolf	**/
/**																								**/
/**					Third Pass to reference information which didn't exist before				**/
/*************************************************************************************************/
	for (int i=0; i < GC.getNumGoodyInfos(); ++i)		GC.getGoodyInfo((GoodyTypes)i).readPass3();
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	// add types to global var system
	for (int i = 0; i < GC.getNumCursorInfos(); ++i)
	{
		int iVal;
		CvString szType = GC.getCursorInfo((CursorTypes)i).getType();
		if (GC.getDefinesVarSystem()->GetValue(szType, iVal))
		{
			char szMessage[1024];
			sprintf(szMessage, "cursor type already set? \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
			gDLL->MessageBox(szMessage, "XML Error");
		}
		GC.getDefinesVarSystem()->SetValue(szType, i);
	}

	// Check Playables
	for (int i=0; i < GC.getNumCivilizationInfos(); ++i)
	{
		// if the civilization is playable we will increment the playable var
		if (GC.getCivilizationInfo((CivilizationTypes) i).isPlayable())
		{
			GC.getNumPlayableCivilizationInfos() += 1;
		}

		// if the civilization is playable by AI increments num playable
		if (GC.getCivilizationInfo((CivilizationTypes) i).isAIPlayable())
		{
			GC.getNumAIPlayableCivilizationInfos() += 1;
		}
	}
/*************************************************************************************************/
/**	LoadedTGA								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Modifies how the TGA is handled to allow many more religions/corporations/resources easily	**/
/*************************************************************************************************/
	AddTGABogus(GC.getCorporationInfo(), "CIV4CorporationInfo");
	AddTGABogus(GC.getReligionInfo(), "CIV4ReligionInfo");
/*************************************************************************************************/
/**	LoadedTGA								END													**/
/*************************************************************************************************/

	UpdateProgressCB("GlobalOther");

	DestroyFXml();

	return true;
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   LoadPostMenuGlobals()
//
//  PURPOSE :   loads global xml data which isn't needed for the main menus
//		this data is loaded as a secodn stage, when the game is launched
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::LoadPostMenuGlobals()
{
	PROFILE_FUNC();
	if (!CreateFXml())
	{
		return false;
	}

	//throne room disabled
	UpdateProgressCB("Global Throne Room");

	LoadGlobalClassInfo(GC.getThroneRoomCamera(), "CIV4ThroneRoomCameraInfos", "Interface", "Civ4ThroneRoomCameraInfos/ThroneRoomCameraInfos/ThroneRoomCamera", false);
	LoadGlobalClassInfo(GC.getThroneRoomInfo(), "CIV4ThroneRoomInfos", "Interface", "Civ4ThroneRoomInfos/ThroneRoomInfos/ThroneRoomInfo", false);
	LoadGlobalClassInfo(GC.getThroneRoomStyleInfo(), "CIV4ThroneRoomStyleInfos", "Interface", "Civ4ThroneRoomStyleInfos/ThroneRoomStyleInfos/ThroneRoomStyleInfo", false);

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**								Moved to LoadPreMenuGlobals										**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	UpdateProgressCB("Global Events");
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

//FfH: Modified by Kael 04/17/2008 (moved to the normal xml load process)
//	LoadGlobalClassInfo(GC.getEventInfo(), "CIV4EventInfos", "Events", "Civ4EventInfos/EventInfos/EventInfo", true, &CvDLLUtilityIFaceBase::createEventInfoCacheObject);
//	LoadGlobalClassInfo(GC.getEventTriggerInfo(), "CIV4EventTriggerInfos", "Events", "Civ4EventTriggerInfos/EventTriggerInfos/EventTriggerInfo", false, &CvDLLUtilityIFaceBase::createEventTriggerInfoCacheObject);
//FfH: End Modify

	UpdateProgressCB("Global Routes");

	LoadGlobalClassInfo(GC.getRouteModelInfo(), "Civ4RouteModelInfos", "Art", "Civ4RouteModelInfos/RouteModelInfos/RouteModelInfo", false);

	UpdateProgressCB("Global Rivers");

	LoadGlobalClassInfo(GC.getRiverInfo(), "CIV4RiverInfos", "Misc", "Civ4RiverInfos/RiverInfos/RiverInfo", false);
	LoadGlobalClassInfo(GC.getRiverModelInfo(), "CIV4RiverModelInfos", "Art", "Civ4RiverModelInfos/RiverModelInfos/RiverModelInfo", false);

	UpdateProgressCB("Global Other");

	LoadGlobalClassInfo(GC.getWaterPlaneInfo(), "CIV4WaterPlaneInfos", "Misc", "Civ4WaterPlaneInfos/WaterPlaneInfos/WaterPlaneInfo", false);
	LoadGlobalClassInfo(GC.getTerrainPlaneInfo(), "CIV4TerrainPlaneInfos", "Misc", "Civ4TerrainPlaneInfos/TerrainPlaneInfos/TerrainPlaneInfo", false);
	LoadGlobalClassInfo(GC.getCameraOverlayInfo(), "CIV4CameraOverlayInfos", "Misc", "Civ4CameraOverlayInfos/CameraOverlayInfos/CameraOverlayInfo", false);


	UpdateProgressCB("Global Process");

	LoadGlobalClassInfo(GC.getProcessInfo(), "CIV4ProcessInfo", "GameInfo", "Civ4ProcessInfo/ProcessInfos/ProcessInfo", false);

	UpdateProgressCB("Global Emphasize");

	LoadGlobalClassInfo(GC.getEmphasizeInfo(), "CIV4EmphasizeInfo", "GameInfo", "Civ4EmphasizeInfo/EmphasizeInfos/EmphasizeInfo", false);

	UpdateProgressCB("Global Other");

	LoadGlobalClassInfo(GC.getMissionInfo(), "CIV4MissionInfos", "Units", "Civ4MissionInfos/MissionInfos/MissionInfo", false);
	LoadGlobalClassInfo(GC.getControlInfo(), "CIV4ControlInfos", "Units", "Civ4ControlInfos/ControlInfos/ControlInfo", false);
	LoadGlobalClassInfo(GC.getCommandInfo(), "CIV4CommandInfos", "Units", "Civ4CommandInfos/CommandInfos/CommandInfo", false);
	LoadGlobalClassInfo(GC.getAutomateInfo(), "CIV4AutomateInfos", "Units", "Civ4AutomateInfos/AutomateInfos/AutomateInfo", false);

	UpdateProgressCB("Global Vote");

	LoadGlobalClassInfo(GC.getVoteInfo(), "CIV4VoteInfo", "GameInfo", "Civ4VoteInfo/VoteInfos/VoteInfo", false);

	UpdateProgressCB("Global Interface");

	LoadGlobalClassInfo(GC.getCameraInfo(), "CIV4CameraInfos", "Interface", "Civ4CameraInfos/CameraInfos/CameraInfo", false);
	LoadGlobalClassInfo(GC.getInterfaceModeInfo(), "CIV4InterfaceModeInfos", "Interface", "Civ4InterfaceModeInfos/InterfaceModeInfos/InterfaceModeInfo", false);

	SetGlobalActionInfo();


	// Load the formation info
	LoadGlobalClassInfo(GC.getUnitFormationInfo(), "CIV4FormationInfos", "Units", "UnitFormations/UnitFormation", false);

	// Load the attachable infos
	LoadGlobalClassInfo(GC.getAttachableInfo(), "CIV4AttachableInfos", "Misc", "Civ4AttachableInfos/AttachableInfos/AttachableInfo", false);

	// Specail Case Diplomacy Info due to double vectored nature and appending of Responses
	LoadDiplomacyInfo(GC.getDiplomacyInfo(), "CIV4DiplomacyInfos", "GameInfo", "Civ4DiplomacyInfos/DiplomacyInfos/DiplomacyInfo", &CvDLLUtilityIFaceBase::createDiplomacyInfoCacheObject);

	LoadGlobalClassInfo(GC.getQuestInfo(), "Civ4QuestInfos", "Misc", "Civ4QuestInfos/QuestInfo", false);
	LoadGlobalClassInfo(GC.getTutorialInfo(), "Civ4TutorialInfos", "Misc", "Civ4TutorialInfos/TutorialInfo", false);

	LoadGlobalClassInfo(GC.getEspionageMissionInfo(), "CIV4EspionageMissionInfo", "GameInfo", "Civ4EspionageMissionInfo/EspionageMissionInfos/EspionageMissionInfo", false);

	DestroyFXml();
	return true;
}


//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetGlobalStringArray(TCHAR (**ppszString)[256], char* szTagName, int* iNumVals)
//
//  PURPOSE :   takes the szTagName parameter and if it finds it in the m_pFXml member variable
//				then it loads the ppszString parameter with the string values under it and the
//				iNumVals with the total number of tags with the szTagName in the xml file
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetGlobalStringArray(CvString **ppszString, char* szTagName, int* iNumVals, bool bUseEnum)
{
	PROFILE_FUNC();
	logMsg("SetGlobalStringArray %s\n", szTagName);

	int i=0;					//loop counter
	CvString *pszString;	// hold the local pointer to the newly allocated string memory
	pszString = NULL;			// null out the local string pointer so that it can be checked at the
	// end of the function in an FAssert

	// if we locate the szTagName, the current node is set to the first instance of the tag name in the xml file
	if (gDLL->getXMLIFace()->LocateNode(m_pFXml,szTagName))
	{
		if (!bUseEnum)
		{
			// get the total number of times this tag appears in the xml
			*iNumVals = gDLL->getXMLIFace()->NumOfElementsByTagName(m_pFXml,szTagName);
		}
		// initialize the memory based on the total number of tags in the xml and the 256 character length we selected
		*ppszString = new CvString[*iNumVals];
		// set the local pointer to the memory just allocated
		pszString = *ppszString;

		// loop through each of the tags
		for (int i=0;i<*iNumVals;i++)
		{
			// get the string value at the current node
			GetXmlVal(pszString[i]);
			GC.setTypesEnum(pszString[i], i);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
			GC.setInfoTypeFromString(pszString[i], i, true);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

			// if can't set the current node to a sibling node we will break out of the for loop
			// otherwise we will keep looping
			if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
			{
				break;
			}
		}
	}

	// if the local string pointer is null then we weren't able to find the szTagName in the xml
	// so we will FAssert to let whoever know it
	if (!pszString)
	{
		char	szMessage[1024];
		sprintf( szMessage, "Error locating tag node in SetGlobalStringArray function \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
}




//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetGlobalActionInfo(CvActionInfo** ppActionInfo, int* iNumVals)
//
//  PURPOSE :   Takes the szTagName parameter and if it exists in the xml it loads the ppActionInfo
//				with the value under it and sets the value of the iNumVals parameter to the total number
//				of occurances of the szTagName tag in the xml.
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetGlobalActionInfo()
{
	PROFILE_FUNC();
	logMsg("SetGlobalActionInfo\n");
	int i=0;					//loop counter

	if(!(NUM_INTERFACEMODE_TYPES > 0))
	{
		char	szMessage[1024];
		sprintf( szMessage, "NUM_INTERFACE_TYPES is not greater than zero in CvXMLLoadUtility::SetGlobalActionInfo \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	if(!(GC.getNumBuildInfos() > 0))
	{
		char	szMessage[1024];
		sprintf( szMessage, "GC.getNumBuildInfos() is not greater than zero in CvXMLLoadUtility::SetGlobalActionInfo \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	if(!(GC.getNumPromotionInfos() > 0))
	{
		char	szMessage[1024];
		sprintf( szMessage, "GC.getNumPromotionInfos() is not greater than zero in CvXMLLoadUtility::SetGlobalActionInfo \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	if(!(GC.getNumUnitClassInfos() > 0) )
	{
		char	szMessage[1024];
		sprintf( szMessage, "GC.getNumUnitClassInfos() is not greater than zero in CvXMLLoadUtility::SetGlobalActionInfo \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	if(!(GC.getNumSpecialistClassInfos() > 0) )
	{
		char	szMessage[1024];
		sprintf( szMessage, "GC.getNumSpecialistClassInfos() is not greater than zero in CvXMLLoadUtility::SetGlobalActionInfo \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	if(!(GC.getNumBuildingInfos() > 0) )
	{
		char	szMessage[1024];
		sprintf( szMessage, "GC.getNumBuildingInfos() is not greater than zero in CvXMLLoadUtility::SetGlobalActionInfo \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	if(!(NUM_CONTROL_TYPES > 0) )
	{
		char	szMessage[1024];
		sprintf( szMessage, "NUM_CONTROL_TYPES is not greater than zero in CvXMLLoadUtility::SetGlobalActionInfo \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	if(!(GC.getNumAutomateInfos() > 0) )
	{
		char	szMessage[1024];
		sprintf( szMessage, "GC.getNumAutomateInfos() is not greater than zero in CvXMLLoadUtility::SetGlobalActionInfo \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	if(!(NUM_COMMAND_TYPES > 0) )
	{
		char	szMessage[1024];
		sprintf( szMessage, "NUM_COMMAND_TYPES is not greater than zero in CvXMLLoadUtility::SetGlobalActionInfo \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	if(!(NUM_MISSION_TYPES > 0) )
	{
		char	szMessage[1024];
		sprintf( szMessage, "NUM_MISSION_TYPES is not greater than zero in CvXMLLoadUtility::SetGlobalActionInfo \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}

	int* piOrderedIndex=NULL;

	int iNumOrigVals = GC.getNumActionInfos();

	int iNumActionInfos = iNumOrigVals +
		NUM_INTERFACEMODE_TYPES +
		GC.getNumBuildInfos() +
		GC.getNumPromotionInfos() +
		GC.getNumReligionInfos() +
		GC.getNumCorporationInfos() +
		GC.getNumUnitInfos() +
		GC.getNumSpecialistClassInfos() +
		GC.getNumBuildingInfos() +
		NUM_CONTROL_TYPES +
		NUM_COMMAND_TYPES +
		GC.getNumAutomateInfos() +

//FfH Spell System: Added by Kael 07/23/2007
		GC.getNumSpellInfos() +
//FfH: End Add

		NUM_MISSION_TYPES;

	int* piIndexList = new int[iNumActionInfos];
	int* piPriorityList = new int[iNumActionInfos];
	int* piActionInfoTypeList = new int[iNumActionInfos];

	int iTotalActionInfoCount = 0;

	// loop through control info
	for (int i=0;i<NUM_COMMAND_TYPES;i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getCommandInfo((CommandTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_COMMAND;
		iTotalActionInfoCount++;
	}

	for (int i=0;i<NUM_INTERFACEMODE_TYPES;i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getInterfaceModeInfo((InterfaceModeTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_INTERFACEMODE;
		iTotalActionInfoCount++;
	}

	for (int i=0;i<GC.getNumBuildInfos();i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getBuildInfo((BuildTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_BUILD;
		iTotalActionInfoCount++;
	}

	for (int i=0;i<GC.getNumPromotionInfos();i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getPromotionInfo((PromotionTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_PROMOTION;
		iTotalActionInfoCount++;
	}

	for (int i=0;i<GC.getNumUnitInfos();i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getUnitInfo((UnitTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_UNIT;
		iTotalActionInfoCount++;
	}

	for (int i=0;i<GC.getNumReligionInfos();i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getReligionInfo((ReligionTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_RELIGION;
		iTotalActionInfoCount++;
	}

	for (int i=0;i<GC.getNumCorporationInfos();i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getCorporationInfo((CorporationTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_CORPORATION;
		iTotalActionInfoCount++;
	}

	for (int i = 0;i<GC.getNumSpecialistClassInfos();i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getSpecialistClassInfo((SpecialistClassTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_SPECIALIST;
		iTotalActionInfoCount++;
	}

	for (int i=0;i<GC.getNumBuildingInfos();i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getBuildingInfo((BuildingTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_BUILDING;
		iTotalActionInfoCount++;
	}

	for (int i=0;i<NUM_CONTROL_TYPES;i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getControlInfo((ControlTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_CONTROL;
		iTotalActionInfoCount++;
	}

	for (int i=0;i<GC.getNumAutomateInfos();i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getAutomateInfo(i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_AUTOMATE;
		iTotalActionInfoCount++;
	}

	for (int i=0;i<NUM_MISSION_TYPES;i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getMissionInfo((MissionTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_MISSION;
		iTotalActionInfoCount++;
	}

//FfH Spell System: Added by Kael 07/23/2007
	for (int i=0;i<GC.getNumSpellInfos();i++)
	{
		piIndexList[iTotalActionInfoCount] = i;
		piPriorityList[iTotalActionInfoCount] = GC.getSpellInfo((SpellTypes)i).getOrderPriority();
		piActionInfoTypeList[iTotalActionInfoCount] = ACTIONSUBTYPE_SPELL;
		iTotalActionInfoCount++;
	}
//FfH: End Add

	SAFE_DELETE_ARRAY(piOrderedIndex);
	piOrderedIndex = new int[iNumActionInfos];

	orderHotkeyInfo(&piOrderedIndex, piPriorityList, iNumActionInfos);
	for (int i=0;i<iNumActionInfos;i++)
	{
		CvActionInfo* pActionInfo = new CvActionInfo;
		pActionInfo->setOriginalIndex(piIndexList[piOrderedIndex[i]]);
		pActionInfo->setSubType((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]]);
		if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_COMMAND)
		{
			GC.getCommandInfo((CommandTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
		}
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_INTERFACEMODE)
		{
			GC.getInterfaceModeInfo((InterfaceModeTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
		}
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_BUILD)
		{
			GC.getBuildInfo((BuildTypes)piIndexList[piOrderedIndex[i]]).setMissionType(FindInInfoClass("MISSION_BUILD"));
			GC.getBuildInfo((BuildTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
		}
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_PROMOTION)
		{
			GC.getPromotionInfo((PromotionTypes)piIndexList[piOrderedIndex[i]]).setCommandType(FindInInfoClass("COMMAND_PROMOTION"));
			GC.getPromotionInfo((PromotionTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
			GC.getPromotionInfo((PromotionTypes)piIndexList[piOrderedIndex[i]]).setHotKeyDescription(GC.getPromotionInfo((PromotionTypes)piIndexList[piOrderedIndex[i]]).getTextKeyWide(), GC.getCommandInfo((CommandTypes)(GC.getPromotionInfo((PromotionTypes)piIndexList[piOrderedIndex[i]]).getCommandType())).getTextKeyWide(), CreateHotKeyFromDescription(GC.getPromotionInfo((PromotionTypes)piIndexList[piOrderedIndex[i]]).getHotKey(), GC.getPromotionInfo((PromotionTypes)piIndexList[piOrderedIndex[i]]).isShiftDown(), GC.getPromotionInfo((PromotionTypes)piIndexList[piOrderedIndex[i]]).isAltDown(), GC.getPromotionInfo((PromotionTypes)piIndexList[piOrderedIndex[i]]).isCtrlDown()));
		}

//FfH Spell System: Added by Kael 07/23/2007
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_SPELL)
		{
			GC.getSpellInfo((SpellTypes)piIndexList[piOrderedIndex[i]]).setCommandType(FindInInfoClass("COMMAND_CAST"));
			GC.getSpellInfo((SpellTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
			GC.getSpellInfo((SpellTypes)piIndexList[piOrderedIndex[i]]).setHotKeyDescription(GC.getSpellInfo((SpellTypes)piIndexList[piOrderedIndex[i]]).getTextKeyWide(), GC.getCommandInfo((CommandTypes)(GC.getSpellInfo((SpellTypes)piIndexList[piOrderedIndex[i]]).getCommandType())).getTextKeyWide(), CreateHotKeyFromDescription(GC.getSpellInfo((SpellTypes)piIndexList[piOrderedIndex[i]]).getHotKey(), GC.getSpellInfo((SpellTypes)piIndexList[piOrderedIndex[i]]).isShiftDown(), GC.getSpellInfo((SpellTypes)piIndexList[piOrderedIndex[i]]).isAltDown(), GC.getSpellInfo((SpellTypes)piIndexList[piOrderedIndex[i]]).isCtrlDown()));
		}
//FfH: End Add

		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_UNIT)
		{
			GC.getUnitInfo((UnitTypes)piIndexList[piOrderedIndex[i]]).setCommandType(FindInInfoClass("COMMAND_UPGRADE"));
			GC.getUnitInfo((UnitTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
			GC.getUnitInfo((UnitTypes)piIndexList[piOrderedIndex[i]]).setHotKeyDescription(GC.getUnitInfo((UnitTypes)piIndexList[piOrderedIndex[i]]).getTextKeyWide(), GC.getCommandInfo((CommandTypes)(GC.getUnitInfo((UnitTypes)piIndexList[piOrderedIndex[i]]).getCommandType())).getTextKeyWide(), CreateHotKeyFromDescription(GC.getUnitInfo((UnitTypes)piIndexList[piOrderedIndex[i]]).getHotKey(), GC.getUnitInfo((UnitTypes)piIndexList[piOrderedIndex[i]]).isShiftDown(), GC.getUnitInfo((UnitTypes)piIndexList[piOrderedIndex[i]]).isAltDown(), GC.getUnitInfo((UnitTypes)piIndexList[piOrderedIndex[i]]).isCtrlDown()));
		}
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_RELIGION)
		{
			GC.getReligionInfo((ReligionTypes)piIndexList[piOrderedIndex[i]]).setMissionType(FindInInfoClass("MISSION_SPREAD"));
			GC.getReligionInfo((ReligionTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
			GC.getReligionInfo((ReligionTypes)piIndexList[piOrderedIndex[i]]).setHotKeyDescription(GC.getReligionInfo((ReligionTypes)piIndexList[piOrderedIndex[i]]).getTextKeyWide(), GC.getMissionInfo((MissionTypes)(GC.getReligionInfo((ReligionTypes)piIndexList[piOrderedIndex[i]]).getMissionType())).getTextKeyWide(), CreateHotKeyFromDescription(GC.getReligionInfo((ReligionTypes)piIndexList[piOrderedIndex[i]]).getHotKey(), GC.getReligionInfo((ReligionTypes)piIndexList[piOrderedIndex[i]]).isShiftDown(), GC.getReligionInfo((ReligionTypes)piIndexList[piOrderedIndex[i]]).isAltDown(), GC.getReligionInfo((ReligionTypes)piIndexList[piOrderedIndex[i]]).isCtrlDown()));
		}
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_CORPORATION)
		{
			GC.getCorporationInfo((CorporationTypes)piIndexList[piOrderedIndex[i]]).setMissionType(FindInInfoClass("MISSION_SPREAD_CORPORATION"));
			GC.getCorporationInfo((CorporationTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
			GC.getCorporationInfo((CorporationTypes)piIndexList[piOrderedIndex[i]]).setHotKeyDescription(GC.getCorporationInfo((CorporationTypes)piIndexList[piOrderedIndex[i]]).getTextKeyWide(), GC.getMissionInfo((MissionTypes)(GC.getCorporationInfo((CorporationTypes)piIndexList[piOrderedIndex[i]]).getMissionType())).getTextKeyWide(), CreateHotKeyFromDescription(GC.getCorporationInfo((CorporationTypes)piIndexList[piOrderedIndex[i]]).getHotKey(), GC.getCorporationInfo((CorporationTypes)piIndexList[piOrderedIndex[i]]).isShiftDown(), GC.getCorporationInfo((CorporationTypes)piIndexList[piOrderedIndex[i]]).isAltDown(), GC.getCorporationInfo((CorporationTypes)piIndexList[piOrderedIndex[i]]).isCtrlDown()));
		}
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_SPECIALIST)
		{
			GC.getSpecialistClassInfo((SpecialistClassTypes)piIndexList[piOrderedIndex[i]]).setMissionType(FindInInfoClass("MISSION_JOIN"));
			GC.getSpecialistClassInfo((SpecialistClassTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
			GC.getSpecialistClassInfo((SpecialistClassTypes)piIndexList[piOrderedIndex[i]]).setHotKeyDescription(GC.getSpecialistClassInfo((SpecialistClassTypes)piIndexList[piOrderedIndex[i]]).getTextKeyWide(), GC.getMissionInfo((MissionTypes)(GC.getSpecialistClassInfo((SpecialistClassTypes)piIndexList[piOrderedIndex[i]]).getMissionType())).getTextKeyWide(), CreateHotKeyFromDescription(GC.getSpecialistClassInfo((SpecialistClassTypes)piIndexList[piOrderedIndex[i]]).getHotKey(), GC.getSpecialistClassInfo((SpecialistClassTypes)piIndexList[piOrderedIndex[i]]).isShiftDown(), GC.getSpecialistClassInfo((SpecialistClassTypes)piIndexList[piOrderedIndex[i]]).isAltDown(), GC.getSpecialistClassInfo((SpecialistClassTypes)piIndexList[piOrderedIndex[i]]).isCtrlDown()));
		}
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_BUILDING)
		{
			GC.getBuildingInfo((BuildingTypes)piIndexList[piOrderedIndex[i]]).setMissionType(FindInInfoClass("MISSION_CONSTRUCT"));
			GC.getBuildingInfo((BuildingTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
			GC.getBuildingInfo((BuildingTypes)piIndexList[piOrderedIndex[i]]).setHotKeyDescription(GC.getBuildingInfo((BuildingTypes)piIndexList[piOrderedIndex[i]]).getTextKeyWide(), GC.getMissionInfo((MissionTypes)(GC.getBuildingInfo((BuildingTypes)piIndexList[piOrderedIndex[i]]).getMissionType())).getTextKeyWide(), CreateHotKeyFromDescription(GC.getBuildingInfo((BuildingTypes)piIndexList[piOrderedIndex[i]]).getHotKey(), GC.getBuildingInfo((BuildingTypes)piIndexList[piOrderedIndex[i]]).isShiftDown(), GC.getBuildingInfo((BuildingTypes)piIndexList[piOrderedIndex[i]]).isAltDown(), GC.getBuildingInfo((BuildingTypes)piIndexList[piOrderedIndex[i]]).isCtrlDown()));
		}
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_CONTROL)
		{
			GC.getControlInfo((ControlTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
		}
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_AUTOMATE)
		{
			GC.getAutomateInfo(piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i);
		}
		else if ((ActionSubTypes)piActionInfoTypeList[piOrderedIndex[i]] == ACTIONSUBTYPE_MISSION)
		{
			GC.getMissionInfo((MissionTypes)piIndexList[piOrderedIndex[i]]).setActionInfoIndex(i + iNumOrigVals);
		}

		GC.getActionInfo().push_back(pActionInfo);
	}

	SAFE_DELETE_ARRAY(piOrderedIndex);
	SAFE_DELETE_ARRAY(piIndexList);
	SAFE_DELETE_ARRAY(piPriorityList);
	SAFE_DELETE_ARRAY(piActionInfoTypeList);
}


//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetGlobalAnimationPathInfo(CvAnimationPathInfo** ppAnimationPathInfo, char* szTagName, int* iNumVals)
//
//  PURPOSE :   Takes the szTagName parameter and if it exists in the xml it loads the ppAnimationPathInfo
//				with the value under it and sets the value of the iNumVals parameter to the total number
//				of occurances of the szTagName tag in the xml.
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetGlobalAnimationPathInfo(CvAnimationPathInfo** ppAnimationPathInfo, char* szTagName, int* iNumVals)
{
	PROFILE_FUNC();
	logMsg( "SetGlobalAnimationPathInfo %s\n", szTagName );

	int		i;						// Loop counters
	CvAnimationPathInfo * pAnimPathInfo = NULL;	// local pointer to the domain info memory

	if ( gDLL->getXMLIFace()->LocateNode(m_pFXml, szTagName ))
	{
		// get the number of times the szTagName tag appears in the xml file
		*iNumVals = gDLL->getXMLIFace()->NumOfElementsByTagName(m_pFXml,szTagName);

		// allocate memory for the domain info based on the number above
		*ppAnimationPathInfo = new CvAnimationPathInfo[*iNumVals];
		pAnimPathInfo = *ppAnimationPathInfo;

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
		gDLL->getXMLIFace()->SetToChild(m_pFXml);
		gDLL->getXMLIFace()->SetToChild(m_pFXml);


		// Loop through each tag.
		for (int i=0;i<*iNumVals;i++)
		{
			SkipToNextVal();	// skip to the next non-comment node

			if (!pAnimPathInfo[i].read(this))
				break;
			GC.setInfoTypeFromString(pAnimPathInfo[i].getType(), i);	// add type to global info type hash map
			if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
			{
				break;
			}
		}
	}

	// if we didn't find the tag name in the xml then we never set the local pointer to the
	// newly allocated memory and there for we will FAssert to let people know this most
	// interesting fact
	if(!pAnimPathInfo )
	{
		char	szMessage[1024];
		sprintf( szMessage, "Error finding tag node in SetGlobalAnimationPathInfo function \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetGlobalUnitScales(float* pfLargeScale, float* pfSmallScale, char* szTagName)
//
//  PURPOSE :   Takes the szTagName parameter and if it exists in the xml it loads the ppPromotionInfo
//				with the value under it and sets the value of the iNumVals parameter to the total number
//				of occurances of the szTagName tag in the xml.
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetGlobalUnitScales(float* pfLargeScale, float* pfSmallScale, char* szTagName)
{
	PROFILE_FUNC();
	logMsg("SetGlobalUnitScales %s\n", szTagName);
	// if we successfully locate the szTagName node
	if (gDLL->getXMLIFace()->LocateNode(m_pFXml,szTagName))
	{
		// call the function that sets the FXml pointer to the first non-comment child of
		// the current tag and gets the value of that new node
		if (GetChildXmlVal(pfLargeScale))
		{
			// set the current xml node to it's next sibling and then
			// get the sibling's TCHAR value
			GetNextXmlVal(pfSmallScale);

			// set the current xml node to it's parent node
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
		}
	}
	else
	{
		// if we didn't find the tag name in the xml then we never set the local pointer to the
		// newly allocated memory and there for we will FAssert to let people know this most
		// interesting fact
		char	szMessage[1024];
		sprintf( szMessage, "Error finding tag node in SetGlobalUnitScales function \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
}


//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetGameText()
//
//  PURPOSE :   Reads game text info from XML and adds it to the translation manager
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetGameText(const char* szTextGroup, const char* szTagName)
{
	PROFILE_FUNC();
	logMsg("SetGameText %s\n", szTagName);
	int i=0;		//loop counter - Index into pTextInfo

	if (gDLL->getXMLIFace()->LocateNode(m_pFXml, szTextGroup)) // Get the Text Group 1st
	{
		int iNumVals = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);	// Get the number of Children that the Text Group has
		gDLL->getXMLIFace()->LocateNode(m_pFXml, szTagName); // Now switch to the TEXT Tag
		gDLL->getXMLIFace()->SetToParent(m_pFXml);
		gDLL->getXMLIFace()->SetToChild(m_pFXml);

		// loop through each tag
		for (int i=0; i < iNumVals; i++)
		{
			CvGameText textInfo;
			textInfo.read(this);

			gDLL->addText(textInfo.getType() /*id*/, textInfo.getText(), textInfo.getGender(), textInfo.getPlural());
			if (!gDLL->getXMLIFace()->NextSibling(m_pFXml) && i!=iNumVals-1)
			{
				char	szMessage[1024];
				sprintf( szMessage, "failed to find sibling \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
				gDLL->MessageBox(szMessage, "XML Error");
				break;
			}
		}
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetGlobalClassInfo - This is a template function that is USED FOR ALMOST ALL INFO CLASSES.
//		Each info class should have a read(CvXMLLoadUtility*) function that is responsible for initializing
//		the class from xml data.
//
//  PURPOSE :   takes the szTagName parameter and loads the ppszString with the text values
//				under the tags.  This will be the hints displayed during game initialization and load
//
//------------------------------------------------------------------------------------------------------
template <class T>
void CvXMLLoadUtility::SetGlobalClassInfo(std::vector<T*>& aInfos, const char* szTagName, bool bTwoPass)
{
	char szLog[256];
	sprintf(szLog, "SetGlobalClassInfo (%s)", szTagName);
	PROFILE(szLog);
	logMsg(szLog);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**		Tracking method I wrote myself so that you know what tag was loaded last in Asserts		**/
/**	Really the only way to get the assert is an empty XML container, which shouldn't load or by	**/
/** a comment after the last XML item, because the NextSibling check doesn't ignore comments	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	CvString mszLastType = "No XML Loaded Successfully";
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	// if we successfully locate the tag name in the xml file
	if (gDLL->getXMLIFace()->LocateNode(m_pFXml, szTagName))
	{
		// loop through each tag
		do
		{
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/** If a Type is dependent on it's existence(i.e. a modder adds something to an existing		**/
/** Type but doesn't want to actual initialize it in case the Type didn't exist previously)		**/
/** this check here makes sure that the file will be skipped then and not used to create the	**/
/** object																						**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			SkipToNextVal();	// skip to the next non-comment node

				T* pClassInfo = new T;

				FAssert(NULL != pClassInfo);
				if (NULL == pClassInfo)
				{
					break;
				}

				bool bSuccess = pClassInfo->read(this);

				FAssert(bSuccess);
				if (!bSuccess)
				{
					delete pClassInfo;
					break;
				}
/**								----  End Original Code  ----									**/
			if (!SkipToNextVal())	// skip to the next non-comment node
			{
				sprintf(szLog, "Empty XML File (%s), last Type loaded was %s", szTagName, mszLastType.GetCString());
				FAssertMsg(false, szLog);
				break;
			}

			T* pClassInfo = new T;

			FAssert(NULL != pClassInfo);
			if (NULL == pClassInfo)
			{
				break;
			}

			//This is where we call CvInfos::read(XML) functions
			bool bSuccess = pClassInfo->read(this);
			mszLastType = pClassInfo->getType();

			if ( !GC.isAnyDependency() )
			{
				CvString szAssertBuffer;
				szAssertBuffer.Format("OWN TYPE - dependency not found: %s, in file: \"%s\"", pClassInfo->getType(), GC.getModDir().c_str());
				FAssertMsg(bSuccess, szAssertBuffer.c_str());
				if (!bSuccess)
				{
					delete pClassInfo;
					break;
				}
			}
			else
			{
				int iTypeIndex = -1;
				if (NULL != pClassInfo->getType())
				{
					iTypeIndex = GC.getInfoTypeForString(pClassInfo->getType(), true);
				}

				// TYPE dependency? (Condition 1)
				if ( GC.getTypeDependency() && (-1 == iTypeIndex))
				{
					delete pClassInfo;
					GC.resetDependencies();		// make sure we always reset once anydependency was true!
					continue;
				}

				// OR Dependencies (Condition 2)
				GC.setTypeDependency(false);
				if ( GC.getOrNumDependencyTypes() > 0 )
				{
					// if we have Or dependencies, set to dependend by default(this will prevent loading)
					// the moment ANY condition is met, we can safely load the ClassInfo and set the
					// dependency to false
					GC.setTypeDependency(true);
				}
				for ( int iI = 0; iI < GC.getOrNumDependencyTypes(); iI++ )
				{
					iTypeIndex = GC.getInfoTypeForString( GC.getOrDependencyTypes(iI), true );
					if ( iTypeIndex == -1 )
					{
					}
					else
					{
						// we found a OR dependent Type, so we can load safely!
						// dependency will be set disabled(false)
						GC.setTypeDependency(false);
					}
				}

				// AND Dependencies (Condition 3)
				if (GC.getAndNumDependencyTypes() > 0)
				{
					bool bAllAndDepsFound = true;
					for ( int iI = 0; iI < GC.getAndNumDependencyTypes(); iI++ )
					{
						iTypeIndex = GC.getInfoTypeForString( GC.getAndDependencyTypes(iI), true );
						if ( iTypeIndex == -1 )
						{
							// if any AND condition is not met, we disable the loading of the Class Info!
							GC.setTypeDependency(true);
							bAllAndDepsFound = false;
						}
					}
				}

				//This covers both the bTypeDependency and the And/Or-DependencyTypes tags!
				if ( GC.getTypeDependency() )
				{
					// We found that any of the 3! conditions NOT to load this class info has been met!
					delete pClassInfo;
					GC.resetDependencies();		// make sure we always reset once anydependency was true!
					continue;
				}
				else
				{
					bool bSuccess = pClassInfo->read(this);
					GC.resetDependencies();		// make sure we always reset once anydependency was true!
					FAssert(bSuccess);
					if (!bSuccess)
					{
						delete pClassInfo;
						break;
					}
				}
			}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

			int iIndex = -1;
			//Check if we already have an index assigned for this type (ie - it is a repeat/module)
			if (NULL != pClassInfo->getType())
			{
				iIndex = GC.getInfoTypeForString(pClassInfo->getType(), true);
			}

			if (-1 == iIndex)
			//If this is new, create a new entry for it
			{
				aInfos.push_back(pClassInfo);
				if (NULL != pClassInfo->getType())
				{
					GC.setInfoTypeFromString(pClassInfo->getType(), (int)aInfos.size() - 1);	// add type to global info type hash map
				}
			}
			else	//Here we become modular!  (Warning, this also means having a double entry gets a LITTLE MORE CONFUSING as now you get data from both of them
			{
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Special Method to disable overwriting of defaults like 0, NO_TECH, NULL, false, etc			**/
/**	over non default values. Added myself, has to be handled strange for pass 2 unfortunately	**/
/**																								**/
/**																								**/
/**	If a Variable has been initialized by any previous Module, we don't want to reset it by a	**/
/**			default value just because the 2nd Module doesn't know about it's existance			**/
/**			(assuming in the previous XML there was a reason for a non-default value)			**/
/** Arrays forming a list like Uniqueunitnames will be extended and appended so we don't loose  **/
/** functionality of the Modules using the same Type(iIndex) of the same classinfo				**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
				//Copy information out of the previous entry where this new entry is boring...
				if(!pClassInfo->isForceOverwrite())
					pClassInfo->copyNonDefaults(aInfos[iIndex], this);

				//New information (just loaded) is running this function to pull information out of the old stuff
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
				//Delete the old entry data, but keep the spot reserved
				SAFE_DELETE(aInfos[iIndex]);
				//Now put this new data (which holds some of the old data) into that spot instead
				aInfos[iIndex] = pClassInfo;
				//So looks like all of this is done during the first readpass, since we haven't tried to call readpass2 CopyNonDefaults yet.  That means we need to ensure that anything bound for readpass3 is appended, and then it should sort itself out quite nicely for us.  Also means that unless I append information, anything from the original XML load doesn't exist anymore, as we deleted the memory container it was in
			}


		} while (gDLL->getXMLIFace()->NextSibling(m_pFXml));
//This ends readpass1, above loop keeps going till you reach the end of the XML file (or more correctly, go up one parent element from those which contain Types).
		if (bTwoPass)
		{
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
			// if we successfully locate the szTagName node
			if (gDLL->getXMLIFace()->LocateNode(m_pFXml, szTagName))
			{
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
				gDLL->getXMLIFace()->SetToChild(m_pFXml);

				// loop through each tag
				for (std::vector<T*>::iterator it = aInfos.begin(); it != aInfos.end(); ++it)
				{
					SkipToNextVal();	// skip to the next non-comment node

					(*it)->readPass2(this);

					if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
					{
						break;
					}
				}
			}
/**								----  End Original Code  ----									**/
			if (gDLL->getXMLIFace()->LocateNode(m_pFXml, szTagName))
			{
				// loop through each tag
				do
				{
					if (!SkipToNextVal())	// skip to the next non-comment node
					{
						sprintf(szLog, "Empty XML File (%s), last Type loaded was %s", szTagName, mszLastType.GetCString());
						FAssertMsg(false, szLog);
						break;
					}

					T* pClassInfo = new T;

					FAssert(NULL != pClassInfo);

					//Second readpass information is loaded into a completely new set of data
					bool bSuccess = pClassInfo->readPass2(this);
/*************************************************************************************************/
/** If a Type is dependent on it's existence(i.e. a modder adds something to an existing		**/
/** Type but doesn't want to actual initialize it in case the Type didn't exist previously)		**/
/** this check here makes sure that the file will be skipped then and not used to create the	**/
/** object																						**/
/*************************************************************************************************/
					//Need a new dependency check because we are loading this as a completely new item, so we know nothing about readpass 1 and what may have been checked there
					if ( !GC.isAnyDependency() )
					{
						FAssert(bSuccess);
					}
					else
					{
						int iTypeIndex = -1;
						if (NULL != pClassInfo->getType())
						{
							iTypeIndex = GC.getInfoTypeForString(pClassInfo->getType(), true);
						}

						// TYPE dependency? (Condition 1)
						if ( GC.getTypeDependency() && -1 == iTypeIndex)
						{
							delete pClassInfo;
							GC.resetDependencies();		// make sure we always reset once anydependency was true!
							continue;
						}

						// OR Dependencies (Condition 2)
						GC.setTypeDependency(false);
						if ( GC.getOrNumDependencyTypes() > 0 )
						{
							// if we have Or dependencies, set to dependend by default(this will prevent loading)
							// the moment ANY condition is met, we can safely load the ClassInfo and set the
							// dependency to false
							GC.setTypeDependency(true);
						}
						for ( int iI = 0; iI < GC.getOrNumDependencyTypes(); iI++ )
						{
							iTypeIndex = GC.getInfoTypeForString( GC.getOrDependencyTypes(iI), true );
							if ( !(iTypeIndex == -1) )
							{
								// we found a OR dependent Type, so we can load safely!
								// dependency will be set disabled(false)
								GC.setTypeDependency(false);
							}
						}

						for ( int iI = 0; iI < GC.getAndNumDependencyTypes(); iI++ )
						{
							iTypeIndex = GC.getInfoTypeForString( GC.getAndDependencyTypes(iI), true );
							if ( iTypeIndex == -1 )
							{
								// if any AND condition is not met, we disable the loading of the Class Info!
								GC.setTypeDependency(true);
							}
						}

						//This covers both the bTypeDependency and the And/Or-DependencyTypes tags!
						if ( GC.getTypeDependency() )
						{
							// We found that any of the 3! conditions NOT to load this class info has been met!
							delete pClassInfo;
							GC.resetDependencies();		// make sure we always reset once anydependency was true!
							continue;
						}
						else
						{
							bool bSuccess = pClassInfo->read(this);
							GC.resetDependencies();		// make sure we always reset once anydependency was true!
							FAssert(bSuccess);
							if (!bSuccess)
							{
								delete pClassInfo;
								break;
							}
						}
					}

					int iIndex = -1;
					//At this point, the type MUST already exist, so we don't offer the chance to setInfoType
					if (NULL != pClassInfo->getType())
					{
						iIndex = GC.getInfoTypeForString(pClassInfo->getType(), true);
					}

					//As before, keep what was set before if it is boring this time around
					//But backward this time, we are discarding anything not specifically included, so having this function be blank is now a BAD THING
					aInfos[iIndex]->copyNonDefaultsReadPass2(pClassInfo, this);
					//Old information is running this function to pull data out of the new stuff

					SAFE_DELETE(pClassInfo);

				} while (gDLL->getXMLIFace()->NextSibling(m_pFXml));
			}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
		}
	}
}

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/** This method is a replacement for the bTwoPass, if stuff that is depending on each other in  **/
/** a loop, the bTwoPass would fail since it doesn't look first in the other Modules!			**/
/** Translation:  If Module1 had a promotion which refers to a promotion in Module2, things blow up
/*************************************************************************************************/
template <class T>
void CvXMLLoadUtility::SetGlobalClassInfoTwoPassReplacement(std::vector<T*>& aInfos, const char* szTagName)
{
	char szLog[256];
	sprintf(szLog, "SetGlobalClassInfo (%s)", szTagName);
	PROFILE(szLog);
	logMsg(szLog);
	CvString mszLastType = "No XML Loaded Successfully";

	if (gDLL->getXMLIFace()->LocateNode(m_pFXml, szTagName))
	{
		// loop through each tag
		do
		{
			if (!SkipToNextVal())	// skip to the next non-comment node
			{
				sprintf(szLog, "Empty XML File (%s), last Type loaded was %s", szTagName, mszLastType.GetCString());
				FAssertMsg(false, szLog);
				break;
			}

			T* pClassInfo = new T;

			FAssert(NULL != pClassInfo);

			bool bSuccess = pClassInfo->readPass2(this);

			if ( !GC.isAnyDependency() )
			{
				FAssert(bSuccess);
			}
			else
			{
				int iTypeIndex = -1;
				if (NULL != pClassInfo->getType())
				{
					iTypeIndex = GC.getInfoTypeForString(pClassInfo->getType(), true);
				}

				// TYPE dependency? (Condition 1)
				if ( GC.getTypeDependency() && -1 == iTypeIndex)
				{
					delete pClassInfo;
					GC.resetDependencies();		// make sure we always reset once anydependency was true!
					continue;
				}

				// OR Dependencies (Condition 2)
				GC.setTypeDependency(false);
				if ( GC.getOrNumDependencyTypes() > 0 )
				{
					// if we have Or dependencies, set to dependend by default(this will prevent loading)
					// the moment ANY condition is met, we can safely load the ClassInfo and set the
					// dependency to false
					GC.setTypeDependency(true);
				}
				for ( int iI = 0; iI < GC.getOrNumDependencyTypes(); iI++ )
				{
					iTypeIndex = GC.getInfoTypeForString( GC.getOrDependencyTypes(iI), true );
					if ( !(iTypeIndex == -1) )
					{
						// we found a OR dependent Type, so we can load safely!
						// dependency will be set disabled(false)
						GC.setTypeDependency(false);
					}
				}

				for ( int iI = 0; iI < GC.getAndNumDependencyTypes(); iI++ )
				{
					iTypeIndex = GC.getInfoTypeForString( GC.getAndDependencyTypes(iI), true );
					if ( iTypeIndex == -1 )
					{
						// if any AND condition is not met, we disable the loading of the Class Info!
						GC.setTypeDependency(true);
					}
				}

				//This covers both the bTypeDependency and the And/Or-DependencyTypes tags!
				if ( GC.getTypeDependency() )
				{
					// We found that any of the 3! conditions NOT to load this class info has been met!
					delete pClassInfo;
					GC.resetDependencies();		// make sure we always reset once anydependency was true!
					continue;
				}
				else
				{
					bool bSuccess = pClassInfo->read(this);
					GC.resetDependencies();		// make sure we always reset once anydependency was true!
					FAssert(bSuccess);
					if (!bSuccess)
					{
						delete pClassInfo;
						break;
					}
				}
			}

			int iIndex = -1;
			if (NULL != pClassInfo->getType())
			{
				iIndex = GC.getInfoTypeForString(pClassInfo->getType(), true);
			}

			aInfos[iIndex]->copyNonDefaultsReadPass2(pClassInfo, this);
			SAFE_DELETE(pClassInfo);

		} while (gDLL->getXMLIFace()->NextSibling(m_pFXml));
	}
}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
void CvXMLLoadUtility::SetDiplomacyInfo(std::vector<CvDiplomacyInfo*>& DiploInfos, const char* szTagName)
{
	char szLog[256];
	sprintf(szLog, "SetDiplomacyInfo (%s)", szTagName);
	PROFILE(szLog);
	logMsg(szLog);

	// if we successfully locate the tag name in the xml file
	if (gDLL->getXMLIFace()->LocateNode(m_pFXml, szTagName))
	{
		// loop through each tag
		do
		{
			SkipToNextVal();	// skip to the next non-comment node

			CvString szType;
			GetChildXmlValByName(szType, "Type");
			int iIndex = GC.getInfoTypeForString(szType, true);

			if (-1 == iIndex)
			{
				CvDiplomacyInfo* pClassInfo = new CvDiplomacyInfo;

				if (NULL == pClassInfo)
				{
					FAssert(false);
					break;
				}

				pClassInfo->read(this);
				if (NULL != pClassInfo->getType())
				{
					GC.setInfoTypeFromString(pClassInfo->getType(), (int)DiploInfos.size());	// add type to global info type hash map
				}
				DiploInfos.push_back(pClassInfo);
			}
			else
			{
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
				DiploInfos[iIndex]->read(this);
/**								----  End Original Code  ----									**/
				if(!DiploInfos[iIndex]->isForceOverwrite())
					DiploInfos[iIndex]->copyNonDefaults(this);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
			}

		} while (gDLL->getXMLIFace()->NextSibling(m_pFXml));
	}
}

template <class T>
void CvXMLLoadUtility::LoadGlobalClassInfo(std::vector<T*>& aInfos, const char* szFileRoot, const char* szFileDirectory, const char* szXmlPath, bool bTwoPass, CvCacheObject* (CvDLLUtilityIFaceBase::*pArgFunction) (const TCHAR*))
{
	bool bLoaded = false;
	bool bWriteCache = true;
	CvCacheObject* pCache = NULL;
	GC.addToInfosVectors(&aInfos);

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**		Basically this first bit here allows you to turn off WoC's Readpass2 statements			**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	bool bTwoPassReplacement = true; // Use this if you wanna use the regular Firaxis bTwoPass
	if ( bTwoPassReplacement )
	{
		if (!bTwoPass )
		{
			bTwoPassReplacement = false;
		}
		bTwoPass = false;
	}

	CvXMLLoadUtilitySetMod* pModEnumVector = new CvXMLLoadUtilitySetMod;
	CvXMLLoadUtilityModTools* p_szDirName = new CvXMLLoadUtilityModTools;
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
	if (NULL != pArgFunction)
	{
		pCache = (gDLL->*pArgFunction)(CvString::format("%s.dat", szFileRoot));	// cache file name

		if (gDLL->cacheRead(pCache, CvString::format("xml\\\\%s\\\\%s.xml", szFileDirectory, szFileRoot)))
		{
			logMsg("Read %s from cache", szFileDirectory);
			bLoaded = true;
			bWriteCache = false;
		}
	}

	if (!bLoaded)
	{
		bLoaded = LoadCivXml(m_pFXml, CvString::format("xml\\%s/%s.xml", szFileDirectory, szFileRoot));

		if (!bLoaded)
		{
			char szMessage[1024];
			sprintf(szMessage, "LoadXML call failed for %s.", CvString::format("%s/%s.xml", szFileDirectory, szFileRoot).GetCString());
			gDLL->MessageBox(szMessage, "XML Load Error");
		}
		else
		{
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**	Clears previous entry in the "Currently Loading" tracker, will be set to new value soon		**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
			GC.setModDir("NONE");
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
			SetGlobalClassInfo(aInfos, szXmlPath, bTwoPass);

			if (gDLL->isModularXMLLoading())
			{
				std::vector<CvString> aszFiles;
				gDLL->enumerateFiles(aszFiles, CvString::format("modules\\*_%s.xml", szFileRoot));  // search for the modular files

				for (std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
				{
					bLoaded = LoadCivXml(m_pFXml, *it);

					if (!bLoaded)
					{
						char szMessage[1024];
						sprintf(szMessage, "LoadXML call failed for %s.", (*it).GetCString());
						gDLL->MessageBox(szMessage, "XML Load Error");
					}
					else
					{
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
						CvString szDirName = (*it).GetCString();
						szDirName = p_szDirName->deleteFileName(szDirName, '\\');
						GC.setModDir(szDirName);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
						SetGlobalClassInfo(aInfos, szXmlPath, bTwoPass);
					}
				}
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
				if ( bTwoPassReplacement )
				{
					bLoaded = LoadCivXml(m_pFXml, CvString::format("xml\\%s/%s.xml", szFileDirectory, szFileRoot));
					if (!bLoaded)
					{
						char szMessage[1024];
						sprintf(szMessage, "LoadXML call failed for %s.", CvString::format("%s/%s.xml", szFileDirectory, szFileRoot).GetCString());
						gDLL->MessageBox(szMessage, "XML Load Error");
					}
					else
					{
						SetGlobalClassInfoTwoPassReplacement(aInfos, szXmlPath);
					}
				}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
				if ( bTwoPassReplacement )	// reloop through the modules!
				{
					for (std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
					{
						bLoaded = LoadCivXml(m_pFXml, *it);

						if (!bLoaded)
						{
							char szMessage[1024];
							sprintf(szMessage, "LoadXML call failed for %s.", (*it).GetCString());
							gDLL->MessageBox(szMessage, "XML Load Error");
						}
						else
						{

							CvString szDirName = (*it).GetCString();
							szDirName = p_szDirName->deleteFileName(szDirName, '\\');
							GC.setModDir(szDirName);
							SetGlobalClassInfoTwoPassReplacement(aInfos, szXmlPath);

						}
					}
				}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
			}

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
			else		//Not Modular Loading...
			{
				std::vector<CvString> aszFiles;
				aszFiles.reserve(10000);
				pModEnumVector->loadModControlArray(aszFiles, szFileRoot);

				for (std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
				{

					bLoaded = LoadCivXml(m_pFXml, *it);

					if (!bLoaded)
					{
						char szMessage[1024];
						sprintf(szMessage, "LoadXML call failed for %s.", (*it).GetCString());
						gDLL->MessageBox(szMessage, "XML Load Error");
					}
					else
					{
						CvString szDirName = (*it).GetCString();
						szDirName = p_szDirName->deleteFileName(szDirName, '\\');
						GC.setModDir(szDirName);
						SetGlobalClassInfo(aInfos, szXmlPath, bTwoPass);
					}
				}
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
				if ( bTwoPassReplacement )
				{
					bLoaded = LoadCivXml(m_pFXml, CvString::format("xml\\%s/%s.xml", szFileDirectory, szFileRoot));
					if (!bLoaded)
					{
						char szMessage[1024];
						sprintf(szMessage, "LoadXML call failed for %s.", CvString::format("%s/%s.xml", szFileDirectory, szFileRoot).GetCString());
						gDLL->MessageBox(szMessage, "XML Load Error");
					}
					else
					{
						SetGlobalClassInfoTwoPassReplacement(aInfos, szXmlPath);
					}
				}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
				if ( bTwoPassReplacement )	// reloop through the modules!
				{
					for (std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
					{
						bLoaded = LoadCivXml(m_pFXml, *it);

						if (!bLoaded)
						{
							char szMessage[1024];
							sprintf(szMessage, "LoadXML call failed for %s.", (*it).GetCString());
							gDLL->MessageBox(szMessage, "XML Load Error");
						}
						else
						{

							CvString szDirName = (*it).GetCString();
							szDirName = p_szDirName->deleteFileName(szDirName, '\\');
							GC.setModDir(szDirName);
							SetGlobalClassInfoTwoPassReplacement(aInfos, szXmlPath);

						}
					}
				}
			}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
			if (NULL != pArgFunction && bWriteCache)
			{
				// write info to cache
				bool bOk = gDLL->cacheWrite(pCache);
				if (!bOk)
				{
					char szMessage[1024];
					sprintf(szMessage, "Failed writing to %s cache. \n Current XML file is: %s", szFileDirectory, GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Caching Error");
				}
				if (bOk)
				{
					logMsg("Wrote %s to cache", szFileDirectory);
				}
			}
		}
	}

	if (NULL != pArgFunction)
	{
		gDLL->destroyCache(pCache);
	}
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	SAFE_DELETE(pModEnumVector);
	SAFE_DELETE(p_szDirName);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
}

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**					we use this for xml's that should only be loaded as a module				**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
template <class T>
void CvXMLLoadUtility::LoadGlobalClassInfoModular(std::vector<T*>& aInfos, const char* szFileRoot, const char* szFileDirectory, const char* szXmlPath, bool bTwoPass)
{
	// we don't wanna use cache for modular loading, could do that, but safer just to load modules from scratch..
	bool bLoaded = false;
	GC.addToInfosVectors(&aInfos);

	CvXMLLoadUtilitySetMod* pModEnumVector = new CvXMLLoadUtilitySetMod;
	CvXMLLoadUtilityModTools* p_szDirName = new CvXMLLoadUtilityModTools;

	std::vector<CvString> aszFiles;
	aszFiles.reserve(10000);
	pModEnumVector->loadModControlArray(aszFiles, szFileRoot);

	for (std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
	{

		bLoaded = LoadCivXml(m_pFXml, *it);

		if (!bLoaded)
		{
			char szMessage[1024];
			sprintf(szMessage, "LoadXML call failed for %s.", (*it).GetCString());
			gDLL->MessageBox(szMessage, "XML Load Error");
		}
		else
		{
			CvString szDirName = (*it).GetCString();
			szDirName = p_szDirName->deleteFileName(szDirName, '\\');
			GC.setModDir(szDirName);
			SetGlobalClassInfo(aInfos, szXmlPath, bTwoPass);
		}
	}

	SAFE_DELETE(pModEnumVector);
	SAFE_DELETE(p_szDirName);
}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

void CvXMLLoadUtility::LoadDiplomacyInfo(std::vector<CvDiplomacyInfo*>& DiploInfos, const char* szFileRoot, const char* szFileDirectory, const char* szXmlPath, CvCacheObject* (CvDLLUtilityIFaceBase::*pArgFunction) (const TCHAR*))
{
	bool bLoaded = false;
	bool bWriteCache = true;
	CvCacheObject* pCache = NULL;

	if (NULL != pArgFunction)
	{
		pCache = (gDLL->*pArgFunction)(CvString::format("%s.dat", szFileRoot));	// cache file name

		if (gDLL->cacheRead(pCache, CvString::format("xml\\\\%s\\\\%s.xml", szFileDirectory, szFileRoot)))
		{
			logMsg("Read %s from cache", szFileDirectory);
			bLoaded = true;
			bWriteCache = false;
		}
	}

	if (!bLoaded)
	{
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
		CvXMLLoadUtilityModTools* p_szDirName = new CvXMLLoadUtilityModTools;
		CvXMLLoadUtilitySetMod* pModEnumVector = new CvXMLLoadUtilitySetMod;
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
		bLoaded = LoadCivXml(m_pFXml, CvString::format("xml\\%s/%s.xml", szFileDirectory, szFileRoot));

		if (!bLoaded)
		{
			char szMessage[1024];
			sprintf(szMessage, "LoadXML call failed for %s.", CvString::format("%s/%s.xml", szFileDirectory, szFileRoot).GetCString());
			gDLL->MessageBox(szMessage, "XML Load Error");
		}
		else
		{
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
			GC.setModDir("NONE");
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
			SetDiplomacyInfo(DiploInfos, szXmlPath);

			if (gDLL->isModularXMLLoading())
			{
				std::vector<CvString> aszFiles;
				gDLL->enumerateFiles(aszFiles, CvString::format("modules\\*_%s.xml", szFileRoot));  // search for the modular files

				for (std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
				{
					bLoaded = LoadCivXml(m_pFXml, *it);

					if (!bLoaded)
					{
						char szMessage[1024];
						sprintf(szMessage, "LoadXML call failed for %s.", (*it).GetCString());
						gDLL->MessageBox(szMessage, "XML Load Error");
					}
					else
					{
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
						CvString szDirName = (*it).GetCString();
						szDirName = p_szDirName->deleteFileName(szDirName, '\\');
						GC.setModDir(szDirName);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
						SetDiplomacyInfo(DiploInfos, szXmlPath);
					}
				}
			}

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
			else
			{
				std::vector<CvString> aszFiles;
				aszFiles.reserve(10000);
				pModEnumVector->loadModControlArray(aszFiles, szFileRoot);

				for (std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
				{
					bLoaded = LoadCivXml(m_pFXml, *it);

					if (!bLoaded)
					{
						char szMessage[1024];
						sprintf(szMessage, "LoadXML call failed for %s.", (*it).GetCString());
						gDLL->MessageBox(szMessage, "XML Load Error");
					}
					else
					{
						CvString szDirName = (*it).GetCString();
						szDirName = p_szDirName->deleteFileName(szDirName, '\\');
						GC.setModDir(szDirName);
						SetDiplomacyInfo(DiploInfos, szXmlPath);
					}
				}
			}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
			if (NULL != pArgFunction && bWriteCache)
			{
				// write info to cache
				bool bOk = gDLL->cacheWrite(pCache);
				if (!bOk)
				{
					char szMessage[1024];
					sprintf(szMessage, "Failed writing to %s cache. \n Current XML file is: %s", szFileDirectory, GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Caching Error");
				}
				if (bOk)
				{
					logMsg("Wrote %s to cache", szFileDirectory);
				}
			}
		}
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
		SAFE_DELETE(pModEnumVector);
		SAFE_DELETE(p_szDirName);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
	}

	if (NULL != pArgFunction)
	{
		gDLL->destroyCache(pCache);
	}
}

//
// helper sort predicate
//

struct OrderIndex {int m_iPriority; int m_iIndex;};
bool sortHotkeyPriority(const OrderIndex orderIndex1, const OrderIndex orderIndex2)
{
	return (orderIndex1.m_iPriority > orderIndex2.m_iPriority);
}

void CvXMLLoadUtility::orderHotkeyInfo(int** ppiSortedIndex, int* pHotkeyIndex, int iLength)
{
	int iI;
	int* piSortedIndex;
	std::vector<OrderIndex> viOrderPriority;

	viOrderPriority.resize(iLength);
	piSortedIndex = *ppiSortedIndex;

	// set up vector
	for (int iI=0;iI<iLength;iI++)
	{
		viOrderPriority[iI].m_iPriority = pHotkeyIndex[iI];
		viOrderPriority[iI].m_iIndex = iI;
	}

	// sort the array
	std::sort(viOrderPriority.begin(), viOrderPriority.end(), sortHotkeyPriority);

	// insert new order into the array to return
	for (int iI=0;iI<iLength;iI++)
	{
		piSortedIndex[iI] = viOrderPriority[iI].m_iIndex;
	}
}

//
// helper sort predicate
//
/*
bool sortHotkeyPriorityOld(const CvHotkeyInfo* hotkey1, const CvHotkeyInfo* hotkey2)
{
return (hotkey1->getOrderPriority() < hotkey2->getOrderPriority());
}
*/

//------------------------------------------------------------------------------------------------
// FUNCTION:    void CvXMLLoadUtility::orderHotkeyInfoOld(T **ppHotkeyInfos, int iLength)
//! \brief      order a hotkey info derived class
//! \param      ppHotkeyInfos is a hotkey info derived class
//!							iLength is the length of the hotkey info derived class array
//! \retval
//------------------------------------------------------------------------------------------------
/*
template <class T>
void CvXMLLoadUtility::orderHotkeyInfoOld(T **ppHotkeyInfos, int iLength)
{
int iI;
std::vector<T*> vHotkeyInfo;
T* pHotkeyInfo;	// local pointer to the hotkey info memory

for (int iI=0;iI<iLength;iI++)
{
pHotkeyInfo = new T;
*pHotkeyInfo = (*ppHotkeyInfos)[iI];
vHotkeyInfo.push_back(pHotkeyInfo);
}

std::sort(vHotkeyInfo.begin(), vHotkeyInfo.end(), sortHotkeyPriority);

for (int iI=0;iI<iLength;iI++)
{
(*ppHotkeyInfos)[iI] = *vHotkeyInfo[iI];
}

for (int iI=0;iI<(int)vHotkeyInfo.size();iI++)
{
vHotkeyInfo[iI]->reset();
SAFE_DELETE(vHotkeyInfo[iI]);
}
vHotkeyInfo.clear();
}
*/

/*************************************************************************************************/
/**	New Tag Defs	(XMLInfos)				08/09/08								Xienwolf	**/
/**																								**/
/**									Loads Information from XML									**/
/*************************************************************************************************/
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetChildList(int** ppiYield)
//
//  PURPOSE :   Generates a Vector String containing all data from single entry children fields
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetStringWithChildList(int* iNumEntries, std::vector<CvString>* aszXMLLoad)
{
	std::vector<CvString> paszXMLLoad;
	CvString szTextVal;

	if (SkipToNextVal())
	{
		int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
		if (0 < iNumSibs)
		{
			if (GetChildXmlVal(szTextVal))
			{
				for (int iI = 0; iI < iNumSibs; iI++)
				{
					bool bLoad = true;
					int iSize = paszXMLLoad.size();
					for (int iJ = 0; iJ < iSize; ++iJ)
					{
						if(szTextVal == paszXMLLoad[iJ])
						{
							bLoad = false;
						}
					}
					if (bLoad)
					{
						paszXMLLoad.push_back(szTextVal);
					}
					if (!GetNextXmlVal(szTextVal))
					{
						break;
					}
				}

				gDLL->getXMLIFace()->SetToParent(m_pFXml);
			}
		}
	}
	gDLL->getXMLIFace()->SetToParent(m_pFXml);

	*iNumEntries = paszXMLLoad.size();
	*aszXMLLoad = paszXMLLoad;
	paszXMLLoad.clear();
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetIntWithChildList(int* iNumEntries, int** piXMLLoad)
//
//  PURPOSE :   Generates an Int Array containing all data from single entry children fields
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetIntWithChildList(int* iNumEntries, int** piXMLLoad)
{
	int* ppiXMLLoad;
	CvString szTextVal;
	std::vector<int> szTemp;

	if (SkipToNextVal())
	{
		int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
		if (iNumSibs > 0)
		{
			if (GetChildXmlVal(szTextVal))
			{
				for (int iI = 0; iI < iNumSibs; iI++)
				{
					int iNew = FindInInfoClass(szTextVal);
					if(iNew == -1)
					{
						char szMessage[1024];
						sprintf( szMessage, "Index is -1 inside function \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
						gDLL->MessageBox(szMessage, "XML Error");
					}
					else
					{
						bool bLoad = true;
						int iSize = szTemp.size();
						for (int iJ = 0; iJ < iSize; ++iJ)
						{
							if(iNew == szTemp[iJ])
							{
								bLoad = false;
							}
						}
						if (bLoad)
						{
							szTemp.push_back(iNew);
						}
					}
					if (!GetNextXmlVal(szTextVal))
					{
						break;
					}
				}

				gDLL->getXMLIFace()->SetToParent(m_pFXml);
			}
		}
	}
	gDLL->getXMLIFace()->SetToParent(m_pFXml);

	int iSize = szTemp.size();
	*iNumEntries = iSize;
	//Redo function to use and return a list, then build the array from that list
	ppiXMLLoad = new int[iSize];
	*piXMLLoad = new int[iSize];
	ppiXMLLoad = *piXMLLoad;
	for (int i = 0; i < iSize; ++i)
	{
		ppiXMLLoad[i] = szTemp[i];
	}
	szTemp.clear();
}
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetBoolFromChildList(int iNumEntries, bool** pbXMLLoad)
//
//  PURPOSE :   Generates an Bool Array containing True in any listed field
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetBoolFromChildList(int iNumEntries, bool** pbXMLLoad)
{
	bool* ppbXMLLoad = NULL;
	ppbXMLLoad = *pbXMLLoad;
	CvString szTextVal;
	if (SkipToNextVal())
	{
		int iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
		if (iNumEntries < iNumSibs)
		{
			char	szMessage[1024];
			sprintf( szMessage, "Too many Children values \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
			gDLL->MessageBox(szMessage, "XML Error");
		}
		if (iNumSibs > 0)
		{
			if (GetChildXmlVal(szTextVal))
			{
				for (int iI = 0; iI < iNumSibs; iI++)
				{
					int eLoad = FindInInfoClass(szTextVal);
					if(eLoad == -1)
					{
						char	szMessage[1024];
						sprintf( szMessage, "Index is -1 inside function \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
						gDLL->MessageBox(szMessage, "XML Error");
					}
					ppbXMLLoad[eLoad] = true;
					if (!GetNextXmlVal(szTextVal))
					{
						break;
					}
				}

				gDLL->getXMLIFace()->SetToParent(m_pFXml);
			}
		}
	}

	gDLL->getXMLIFace()->SetToParent(m_pFXml);
}
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetYields(int** ppiYield)
//
//  PURPOSE :   Allocate memory for the yield parameter and set it to the values
//				in the xml file.  The current/last located node must be the first child of the
//				yield changes node
//
//------------------------------------------------------------------------------------------------------
int CvXMLLoadUtility::SetYields(int** ppiYield)
{
	int i=0;			//loop counter
	int iNumSibs=0;		// the number of siblings the current xml node has
	int *piYield;	// local pointer for the yield memory

	// Skip any comments and stop at the next value we might want
	if (SkipToNextVal())
	{
		// get the total number of children the current xml node has
		iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);

		InitList(ppiYield, NUM_YIELD_TYPES);

		// set the local pointer to the memory we just allocated
		piYield = *ppiYield;

		if (0 < iNumSibs)
		{
			// if the call to the function that sets the current xml node to it's first non-comment
			// child and sets the parameter with the new node's value succeeds
			if (GetChildXmlVal(&piYield[0]))
			{
				if(!(iNumSibs <= NUM_YIELD_TYPES))
				{
					char	szMessage[1024];
					sprintf( szMessage, "For loop iterator is greater than array size \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				// loop through all the siblings, we start at 1 since we already have the first value
				for (int i=1;i<iNumSibs;i++)
				{
					// if the call to the function that sets the current xml node to it's first non-comment
					// sibling and sets the parameter with the new node's value does not succeed
					// we will break out of this for loop
					if (!GetNextXmlVal(&piYield[i]))
					{
						break;
					}
				}
				// set the current xml node to it's parent node
				gDLL->getXMLIFace()->SetToParent(m_pFXml);
			}
		}
	}

	return iNumSibs;
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetFeatureStruct(int** ppiFeatureTech, int** ppiFeatureTime, int** ppiFeatureProduction, bool** ppbFeatureRemove)
//
//  PURPOSE :   allocate and set the feature struct variables for the CvBuildInfo class
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetFeatureStruct(int** ppiFeatureTech, int** ppiFeatureTime, int** ppiFeatureProduction, bool** ppbFeatureRemove)
{
	int i=0;				//loop counter
	int iNumSibs;					// the number of siblings the current xml node has
	int iFeatureIndex;
	TCHAR szTextVal[256];	// temporarily hold the text value of the current xml node
	int* paiFeatureTech = NULL;
	int* paiFeatureTime = NULL;
	int* paiFeatureProduction = NULL;
	bool* pabFeatureRemove = NULL;

	if(GC.getNumFeatureInfos() < 1)
	{
		char	szMessage[1024];
		sprintf( szMessage, "no feature infos set yet! \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	InitList(ppiFeatureTech, GC.getNumFeatureInfos(), -1);
	InitList(ppiFeatureTime, GC.getNumFeatureInfos());
	InitList(ppiFeatureProduction, GC.getNumFeatureInfos());
	InitList(ppbFeatureRemove, GC.getNumFeatureInfos());

	paiFeatureTech = *ppiFeatureTech;
	paiFeatureTime = *ppiFeatureTime;
	paiFeatureProduction = *ppiFeatureProduction;
	pabFeatureRemove = *ppbFeatureRemove;

	if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,"FeatureStructs"))
	{
		iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);

		if (0 < iNumSibs)
		{
			if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,"FeatureStruct"))
			{
				if(!(iNumSibs <= GC.getNumFeatureInfos()))
				{
					char	szMessage[1024];
					sprintf( szMessage, "iNumSibs is greater than GC.getNumFeatureInfos in SetFeatureStruct function \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				for (int i=0;i<iNumSibs;i++)
				{
					GetChildXmlValByName(szTextVal, "FeatureType");
					iFeatureIndex = FindInInfoClass(szTextVal);
					if(!(iFeatureIndex != -1))
					{
						char	szMessage[1024];
						sprintf( szMessage, "iFeatureIndex is -1 inside SetFeatureStruct function \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
						gDLL->MessageBox(szMessage, "XML Error");
					}
					GetChildXmlValByName(szTextVal, "PrereqTech");
					paiFeatureTech[iFeatureIndex] = FindInInfoClass(szTextVal);
					GetChildXmlValByName(&paiFeatureTime[iFeatureIndex], "iTime");
					GetChildXmlValByName(&paiFeatureProduction[iFeatureIndex], "iProduction");
					GetChildXmlValByName(&pabFeatureRemove[iFeatureIndex], "bRemove");

					if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
					{
						break;
					}
				}

				gDLL->getXMLIFace()->SetToParent(m_pFXml);
			}
		}

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetImprovementBonuses(CvImprovementBonusInfo** ppImprovementBonus)
//
//  PURPOSE :   Allocate memory for the improvement bonus pointer and fill it based on the
//				values in the xml.
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetImprovementBonuses(CvImprovementBonusInfo** ppImprovementBonus)
{
	int i=0;				//loop counter
	int iNumSibs;			// the number of siblings the current xml node has
	TCHAR szNodeVal[256];	// temporarily holds the string value of the current xml node
	CvImprovementBonusInfo* paImprovementBonus;	// local pointer to the bonus type struct in memory

	// Skip any comments and stop at the next value we might want
	if (SkipToNextVal())
	{
		// initialize the boolean list to the correct size and all the booleans to false
		InitImprovementBonusList(ppImprovementBonus, GC.getNumBonusInfos());
		// set the local pointer to the memory we just allocated
		paImprovementBonus = *ppImprovementBonus;

		// get the total number of children the current xml node has
		iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
		// if we can set the current xml node to the child of the one it is at now
		if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
		{
			if(!(iNumSibs <= GC.getNumBonusInfos()))
			{
				char	szMessage[1024];
				sprintf( szMessage, "For loop iterator is greater than array size \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
				gDLL->MessageBox(szMessage, "XML Error");
			}
			// loop through all the siblings
			for (int i=0;i<iNumSibs;i++)
			{
				// skip to the next non-comment node
				if (SkipToNextVal())
				{
					// call the function that sets the FXml pointer to the first non-comment child of
					// the current tag and gets the value of that new node
					if (GetChildXmlVal(szNodeVal))
					{
						int iBonusIndex;	// index of the match in the bonus types list
						// call the find in list function to return either -1 if no value is found
						// or the index in the list the match is found at
						iBonusIndex = FindInInfoClass(szNodeVal);
						// if we found a match we will get the next sibling's boolean value at that match's index
						if (iBonusIndex >= 0)
						{
							GetNextXmlVal(&paImprovementBonus[iBonusIndex].m_bBonusMakesValid);
							GetNextXmlVal(&paImprovementBonus[iBonusIndex].m_bBonusTrade);
							GetNextXmlVal(&paImprovementBonus[iBonusIndex].m_iDiscoverRand);

/*************************************************************************************************/
/** SpreadBonus                 Opera                   28/08/09                                **/
/*************************************************************************************************/
							GetNextXmlVal(&paImprovementBonus[iBonusIndex].m_iSpreadRand);
/*************************************************************************************************/
/** SpreadBonus                 END                                                             **/
/*************************************************************************************************/
							gDLL->getXMLIFace()->SetToParent(m_pFXml);

							SAFE_DELETE_ARRAY(paImprovementBonus[iBonusIndex].m_piYieldChange);	// free memory - MT, since we are about to reallocate
							if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,"YieldChanges"))
							{
								SetYields(&paImprovementBonus[iBonusIndex].m_piYieldChange);
								gDLL->getXMLIFace()->SetToParent(m_pFXml);
							}
							else
							{
								InitList(&paImprovementBonus[iBonusIndex].m_piYieldChange, NUM_YIELD_TYPES);
							}
						}
						else
						{
							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						// set the current xml node to it's parent node
					}

					// if we cannot set the current xml node to it's next sibling then we will break out of the for loop
					// otherwise we will continue looping
					if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
					{
						break;
					}
				}
			}
			// set the current xml node to it's parent node
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
		}
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetAndLoadVar(int** ppiVar, int iDefault)
//
//  PURPOSE :   set the variable to a default and load it from the xml if there are any children
//
//------------------------------------------------------------------------------------------------------
bool CvXMLLoadUtility::SetAndLoadVar(int** ppiVar, int iDefault)
{
	int iNumSibs;
	int* piVar;
	bool bReturn = false;
	int i; // loop counter

	// Skip any comments and stop at the next value we might want
	if (SkipToNextVal())
	{
		bReturn = true;

		// get the total number of children the current xml node has
		iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);

		// allocate memory
		InitList(ppiVar, iNumSibs, iDefault);

		// set the a local pointer to the newly allocated memory
		piVar = *ppiVar;

		// if the call to the function that sets the current xml node to it's first non-comment
		// child and sets the parameter with the new node's value succeeds
		if (GetChildXmlVal(&piVar[0]))
		{
			// loop through all the siblings, we start at 1 since we already got the first sibling
			for (int i=1;i<iNumSibs;i++)
			{
				// if the call to the function that sets the current xml node to it's next non-comment
				// sibling and sets the parameter with the new node's value does not succeed
				// we will break out of this for loop
				if (!GetNextXmlVal(&piVar[i]))
				{
					break;
				}
			}

			// set the current xml node to it's parent node
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
		}
	}

	return bReturn;
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetVariableListTagPair(	int **ppiList, const TCHAR* szRootTagName,
//										int iInfoBaseSize, int iInfoBaseLength, int iDefaultListVal)
//
//  PURPOSE :   allocate and initialize a list from a tag pair in the xml
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetVariableListTagPair(int **ppiList, const TCHAR* szRootTagName,
											  int iInfoBaseSize, int iInfoBaseLength, int iDefaultListVal)
{
	int i;
	int iIndexVal;
	int iNumSibs;
	TCHAR szTextVal[256];
	int* piList;

	if (0 > iInfoBaseLength)
	{
		char	szMessage[1024];
		sprintf( szMessage, "Allocating zero or less memory in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	InitList(ppiList, iInfoBaseLength, iDefaultListVal);
	if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szRootTagName))
	{
		if (SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
			piList = *ppiList;
			if (0 < iNumSibs)
			{
				if(!(iNumSibs <= iInfoBaseLength))
				{
					char	szMessage[1024];
					sprintf( szMessage, "There are more siblings than memory allocated for them in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
				{
					for (int i=0;i<iNumSibs;i++)
					{
						if (GetChildXmlVal(szTextVal))
						{
							iIndexVal = FindInInfoClass(szTextVal);

							if (iIndexVal != -1)
							{
								GetNextXmlVal(&piList[iIndexVal]);
							}

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
						{
							break;
						}
					}

					gDLL->getXMLIFace()->SetToParent(m_pFXml);
				}
			}
		}

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetVariableListTagPair(	bool **ppbList, const TCHAR* szRootTagName,
//										int iInfoBaseSize, int iInfoBaseLength, bool bDefaultListVal)
//
//  PURPOSE :   allocate and initialize a list from a tag pair in the xml
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetVariableListTagPair(bool **ppbList, const TCHAR* szRootTagName,
											  int iInfoBaseSize, int iInfoBaseLength, bool bDefaultListVal)
{
	int i;
	int iIndexVal;
	int iNumSibs;
	TCHAR szTextVal[256];
	bool* pbList;

	if(!(0 < iInfoBaseLength))
	{
		char	szMessage[1024];
		sprintf( szMessage, "Allocating zero or less memory in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	InitList(ppbList, iInfoBaseLength, bDefaultListVal);
	if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szRootTagName))
	{
		if (SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
			pbList = *ppbList;
			if (0 < iNumSibs)
			{
				if(!(iNumSibs <= iInfoBaseLength))
				{
					char	szMessage[1024];
					sprintf( szMessage, "There are more siblings than memory allocated for them in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
				{
					for (int i=0;i<iNumSibs;i++)
					{
						if (GetChildXmlVal(szTextVal))
						{
							iIndexVal = FindInInfoClass(szTextVal);
							if (iIndexVal != -1)
							{
								GetNextXmlVal(&pbList[iIndexVal]);
							}

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
						{
							break;
						}
					}

					gDLL->getXMLIFace()->SetToParent(m_pFXml);
				}
			}
		}

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetVariableListTagPair(	float **ppfList, const TCHAR* szRootTagName,
//										int iInfoBaseSize, int iInfoBaseLength, float fDefaultListVal)
//
//  PURPOSE :   allocate and initialize a list from a tag pair in the xml
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetVariableListTagPair(float **ppfList, const TCHAR* szRootTagName,
											  int iInfoBaseSize, int iInfoBaseLength, float fDefaultListVal)
{
	int i;
	int iIndexVal;
	int iNumSibs;
	TCHAR szTextVal[256];
	float* pfList;

	if(!(0 < iInfoBaseLength))
	{
		char	szMessage[1024];
		sprintf( szMessage, "Allocating zero or less memory in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	InitList(ppfList, iInfoBaseLength, fDefaultListVal);
	if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szRootTagName))
	{
		if (SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
			pfList = *ppfList;
			if (0 < iNumSibs)
			{
				if(!(iNumSibs <= iInfoBaseLength))
				{
					char	szMessage[1024];
					sprintf( szMessage, "There are more siblings than memory allocated for them in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
				{
					for (int i=0;i<iNumSibs;i++)
					{
						if (GetChildXmlVal(szTextVal))
						{
							iIndexVal = FindInInfoClass(szTextVal);
							if (iIndexVal != -1)
							{
								GetNextXmlVal(&pfList[iIndexVal]);
							}

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
						{
							break;
						}
					}

					gDLL->getXMLIFace()->SetToParent(m_pFXml);
				}
			}
		}

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetVariableListTagPair(	CvString **ppfList, const TCHAR* szRootTagName,
//										int iInfoBaseSize, int iInfoBaseLength, CvString szDefaultListVal)
//
//  PURPOSE :   allocate and initialize a list from a tag pair in the xml
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetVariableListTagPair(CvString **ppszList, const TCHAR* szRootTagName,
											  int iInfoBaseSize, int iInfoBaseLength, CvString szDefaultListVal)
{
	int i;
	int iIndexVal;
	int iNumSibs;
	TCHAR szTextVal[256];
	CvString* pszList;

	if(!(0 < iInfoBaseLength))
	{
		char	szMessage[1024];
		sprintf( szMessage, "Allocating zero or less memory in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	InitStringList(ppszList, iInfoBaseLength, szDefaultListVal);
	if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szRootTagName))
	{
		if (SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
			pszList = *ppszList;
			if (0 < iNumSibs)
			{
				if(!(iNumSibs <= iInfoBaseLength))
				{
					char	szMessage[1024];
					sprintf( szMessage, "There are more siblings than memory allocated for them in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
				{
					for (int i=0;i<iNumSibs;i++)
					{
						if (GetChildXmlVal(szTextVal))
						{
							iIndexVal = FindInInfoClass(szTextVal);
							if (iIndexVal != -1)
							{
								GetNextXmlVal(pszList[iIndexVal]);
							}

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
						{
							break;
						}
					}

					gDLL->getXMLIFace()->SetToParent(m_pFXml);
				}
			}
		}

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetVariableListTagPair(int **ppiList, const TCHAR* szRootTagName,
//										CvString* m_paszTagList, int iTagListLength, int iDefaultListVal)
//
//  PURPOSE :   allocate and initialize a list from a tag pair in the xml
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetVariableListTagPair(int **ppiList, const TCHAR* szRootTagName,
											  CvString* m_paszTagList, int iTagListLength, int iDefaultListVal)
{
	int i;
	int iIndexVal;
	int iNumSibs;
	TCHAR szTextVal[256];
	int* piList;

	if(!(0 < iTagListLength))
	{
		char	szMessage[1024];
		sprintf( szMessage, "Allocating zero or less memory in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	InitList(ppiList, iTagListLength, iDefaultListVal);
	if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szRootTagName))
	{
		if (SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
			piList = *ppiList;
			if (0 < iNumSibs)
			{
				if(!(iNumSibs <= iTagListLength))
				{
					char	szMessage[1024];
					sprintf( szMessage, "There are more siblings than memory allocated for them in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
				{
					for (int i=0;i<iNumSibs;i++)
					{
						if (GetChildXmlVal(szTextVal))
						{
							iIndexVal = GC.getTypesEnum(szTextVal);
							if (iIndexVal != -1)
							{
								GetNextXmlVal(&piList[iIndexVal]);
							}

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
						{
							break;
						}
					}

					gDLL->getXMLIFace()->SetToParent(m_pFXml);
				}
			}
		}

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
	}
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetVariableListTagPair(int **ppiList, const TCHAR* szRootTagName,
//										CvString* m_paszTagList, int iTagListLength, int iDefaultListVal)
//
//  PURPOSE :   allocate and initialize a list from a tag pair in the xml for audio scripts
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetVariableListTagPairForAudioScripts(int **ppiList, const TCHAR* szRootTagName,
															 CvString* m_paszTagList, int iTagListLength, int iDefaultListVal)
{
	int i;
	int iIndexVal;
	int iNumSibs;
	TCHAR szTextVal[256];
	int* piList;
	CvString szTemp;

	if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szRootTagName))
	{
		if (SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
			if(!(0 < iTagListLength))
			{
				char	szMessage[1024];
				sprintf( szMessage, "Allocating zero or less memory in CvXMLLoadUtility::SetVariableListTagPairForAudio \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
				gDLL->MessageBox(szMessage, "XML Error");
			}
			InitList(ppiList, iTagListLength, iDefaultListVal);
			piList = *ppiList;
			if (0 < iNumSibs)
			{
				if(!(iNumSibs <= iTagListLength))
				{
					char	szMessage[1024];
					sprintf( szMessage, "There are more siblings than memory allocated for them in CvXMLLoadUtility::SetVariableListTagPairForAudio \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
				{
					for (int i=0;i<iNumSibs;i++)
					{
						if (GetChildXmlVal(szTextVal))
						{
							iIndexVal =	GC.getTypesEnum(szTextVal);
							if (iIndexVal != -1)
							{
								GetNextXmlVal(szTemp);
								if ( szTemp.GetLength() > 0 )
									piList[iIndexVal] = gDLL->getAudioTagIndex(szTemp);
								else
									piList[iIndexVal] = -1;
							}

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
						{
							break;
						}
					}

					gDLL->getXMLIFace()->SetToParent(m_pFXml);
				}
			}
		}

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
	}
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**	Need to ensure that after this function runs the list DOES exist, so we can compare later	**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	else
	{
		InitList(ppiList, iTagListLength, iDefaultListVal);
	}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetVariableListTagPairForAudioScripts(int **ppiList, const TCHAR* szRootTagName,
//										int iInfoBaseLength, int iDefaultListVal)
//
//  PURPOSE :   allocate and initialize a list from a tag pair in the xml for audio scripts
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetVariableListTagPairForAudioScripts(int **ppiList, const TCHAR* szRootTagName, int iInfoBaseLength, int iDefaultListVal)
{
	int i;
	int iIndexVal;
	int iNumSibs;
	TCHAR szTextVal[256];
	int* piList;
	CvString szTemp;

	if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szRootTagName))
	{
		if (SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
			if(!(0 < iInfoBaseLength))
			{
				char	szMessage[1024];
				sprintf( szMessage, "Allocating zero or less memory in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
				gDLL->MessageBox(szMessage, "XML Error");
			}
			InitList(ppiList, iInfoBaseLength, iDefaultListVal);
			piList = *ppiList;
			if (0 < iNumSibs)
			{
				if(!(iNumSibs <= iInfoBaseLength))
				{
					char	szMessage[1024];
					sprintf( szMessage, "There are more siblings than memory allocated for them in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
				{
					for (int i=0;i<iNumSibs;i++)
					{
						if (GetChildXmlVal(szTextVal))
						{
							iIndexVal = FindInInfoClass(szTextVal);
							if (iIndexVal != -1)
							{
								GetNextXmlVal(szTemp);
								if ( szTemp.GetLength() > 0 )
									piList[iIndexVal] = gDLL->getAudioTagIndex(szTemp);
								else
									piList[iIndexVal] = -1;
							}

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
						{
							break;
						}
					}

					gDLL->getXMLIFace()->SetToParent(m_pFXml);
				}
			}
		}

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
	}
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	else
	{
		InitList(ppiList, iInfoBaseLength, iDefaultListVal);
	}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
}

//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetVariableListTagPair(bool **ppbList, const TCHAR* szRootTagName,
//										CvString* m_paszTagList, int iTagListLength, int iDefaultListVal)
//
//  PURPOSE :   allocate and initialize a list from a tag pair in the xml
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetVariableListTagPair(bool **ppbList, const TCHAR* szRootTagName,
											  CvString* m_paszTagList, int iTagListLength, bool bDefaultListVal)
{
	int i;
	int iIndexVal;
	int iNumSibs;
	TCHAR szTextVal[256];
	bool* pbList;

	if(!(0 < iTagListLength))
	{
		char	szMessage[1024];
		sprintf( szMessage, "Allocating zero or less memory in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	InitList(ppbList, iTagListLength, bDefaultListVal);
	if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szRootTagName))
	{
		if (SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
			pbList = *ppbList;
			if (0 < iNumSibs)
			{
				if(!(iNumSibs <= iTagListLength))
				{
					char	szMessage[1024];
					sprintf( szMessage, "There are more siblings than memory allocated for them in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
				{
					for (int i=0;i<iNumSibs;i++)
					{
						if (GetChildXmlVal(szTextVal))
						{
							iIndexVal =	GC.getTypesEnum(szTextVal);
							if (iIndexVal != -1)
							{
								GetNextXmlVal(&pbList[iIndexVal]);
							}

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
						{
							break;
						}
					}

					gDLL->getXMLIFace()->SetToParent(m_pFXml);
				}
			}
		}

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
	}
}

//------------------------------------------------------------------------------------------------------
//
//	FUNCTION:	SetVariableListTagPair(CvString **ppszList, const TCHAR* szRootTagName,
//							CvString* m_paszTagList, int iTagListLength, CvString szDefaultListVal = "")
//
//  PURPOSE :   allocate and initialize a list from a tag pair in the xml
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetVariableListTagPair(CvString **ppszList, const TCHAR* szRootTagName,
											  CvString* m_paszTagList, int iTagListLength, CvString szDefaultListVal)
{
	int i;
	int iIndexVal;
	int iNumSibs;
	TCHAR szTextVal[256];
	CvString* pszList;

	if(!(0 < iTagListLength))
	{
		char	szMessage[1024];
		sprintf( szMessage, "Allocating zero or less memory in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
		gDLL->MessageBox(szMessage, "XML Error");
	}
	InitStringList(ppszList, iTagListLength, szDefaultListVal);
	if (gDLL->getXMLIFace()->SetToChildByTagName(m_pFXml,szRootTagName))
	{
		if (SkipToNextVal())
		{
			iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
			pszList = *ppszList;
			if (0 < iNumSibs)
			{
				if(!(iNumSibs <= iTagListLength))
				{
					char	szMessage[1024];
					sprintf( szMessage, "There are more siblings than memory allocated for them in CvXMLLoadUtility::SetVariableListTagPair \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
					gDLL->MessageBox(szMessage, "XML Error");
				}
				if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
				{
					for (int i=0;i<iNumSibs;i++)
					{
						if (GetChildXmlVal(szTextVal))
						{
							iIndexVal =	GC.getTypesEnum(szTextVal);
							if (iIndexVal != -1)
							{
								GetNextXmlVal(pszList[iIndexVal]);
							}

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
						{
							break;
						}
					}

					gDLL->getXMLIFace()->SetToParent(m_pFXml);
				}
			}
		}

		gDLL->getXMLIFace()->SetToParent(m_pFXml);
	}
}

DllExport bool CvXMLLoadUtility::LoadPlayerOptions()
{
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	// Python Modular Loading
	if (!CreateFXml())
		return false;
	LoadPythonModulesInfo(GC.getPythonModulesInfo(), "CIV4PythonModulesInfos", "Civ4PythonModulesInfos/PythonModulesInfos/PythonModulesInfo", false);
	DestroyFXml();

	// MLF loading
	if (!gDLL->isModularXMLLoading())
	{
		if (!CreateFXml())
			return false;

		ModularLoadingControlXML();

		DestroyFXml();
	}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
	if (!CreateFXml())
		return false;

	LoadGlobalClassInfo(GC.getPlayerOptionInfo(), "CIV4PlayerOptionInfos", "GameInfo", "Civ4PlayerOptionInfos/PlayerOptionInfos/PlayerOptionInfo", false);
	FAssert(GC.getNumPlayerOptionInfos() == NUM_PLAYEROPTION_TYPES);

	DestroyFXml();
	return true;
}

DllExport bool CvXMLLoadUtility::LoadGraphicOptions()
{
	if (!CreateFXml())
		return false;

	LoadGlobalClassInfo(GC.getGraphicOptionInfo(), "CIV4GraphicOptionInfos", "GameInfo", "Civ4GraphicOptionInfos/GraphicOptionInfos/GraphicOptionInfo", false);
	FAssert(GC.getNumGraphicOptions() == NUM_GRAPHICOPTION_TYPES);

	DestroyFXml();
	return true;
}


/*************************************************************************************************/
/** AlignmentAttitudeModifier                   Opera                   13.09.09                **/
/*************************************************************************************************/
//------------------------------------------------------------------------------------------------------
//
//  FUNCTION:   SetAlignmentAttitudeModifiers(CvAlignmentAttitudeModifierInfo** ppAlignmentAttitudeModifier)
//
//  PURPOSE :   Allocate memory for the alignment attitude modifier pointer and fill it based on the
//				values in the xml.
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetAlignmentAttitudeModifiers(CvAlignmentAttitudeModifierInfo** ppAlignmentAttitudeModifier)
{
	int i=0;				//loop counter
	int iNumSibs;			// the number of siblings the current xml node has
	TCHAR szNodeVal[256];	// temporarily holds the string value of the current xml node
	CvAlignmentAttitudeModifierInfo* paAlignmentAttitudeModifier;	// local pointer to the bonus type struct in memory

	// Skip any comments and stop at the next value we might want
	if (SkipToNextVal())
	{
		// initialize the boolean list to the correct size and all the booleans to false
		InitAlignmentAttitudeModifierList(ppAlignmentAttitudeModifier, GC.getNumAlignmentInfos());
		// set the local pointer to the memory we just allocated
		paAlignmentAttitudeModifier = *ppAlignmentAttitudeModifier;

		// get the total number of children the current xml node has
		iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
		// if we can set the current xml node to the child of the one it is at now
		if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
		{
			if(!(iNumSibs <= GC.getNumAlignmentInfos()))
			{
				char	szMessage[1024];
				sprintf( szMessage, "For loop iterator is greater than array size \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
				gDLL->MessageBox(szMessage, "XML Error");
			}
			// loop through all the siblings
			for (int i=0;i<iNumSibs;i++)
			{
				// skip to the next non-comment node
				if (SkipToNextVal())
				{
					// call the function that sets the FXml pointer to the first non-comment child of
					// the current tag and gets the value of that new node
					if (GetChildXmlVal(szNodeVal))
					{
						int iAlignmentIndex;	// index of the match in the bonus types list
						// call the find in list function to return either -1 if no value is found
						// or the index in the list the match is found at
						iAlignmentIndex = FindInInfoClass(szNodeVal);
						// if we found a match we will get the next sibling's boolean value at that match's index
						if (iAlignmentIndex >= 0)
						{
							GetNextXmlVal(&paAlignmentAttitudeModifier[iAlignmentIndex].m_iToGood, -100);
							GetNextXmlVal(&paAlignmentAttitudeModifier[iAlignmentIndex].m_iToNeutral, -100);
							GetNextXmlVal(&paAlignmentAttitudeModifier[iAlignmentIndex].m_iToEvil, -100);

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}
						else
						{
							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						// set the current xml node to it's parent node
					}

					// if we cannot set the current xml node to it's next sibling then we will break out of the for loop
					// otherwise we will continue looping
					if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
					{
						break;
					}
				}
			}
			// set the current xml node to it's parent node
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
		}
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
//  FUNCTION:   SetEthicalAlignmentAttitudeModifiers(CvEthicalAlignmentAttitudeModifierInfo** ppEthicalAlignmentAttitudeModifier)
//
//  PURPOSE :   Allocate memory for the Ethical alignment attitude modifier pointer and fill it based on the
//				values in the xml.
//
//------------------------------------------------------------------------------------------------------
void CvXMLLoadUtility::SetEthicalAlignmentAttitudeModifiers(CvEthicalAlignmentAttitudeModifierInfo** ppEthicalAlignmentAttitudeModifier)
{
	int i=0;				//loop counter
	int iNumSibs;			// the number of siblings the current xml node has
	TCHAR szNodeVal[256];	// temporarily holds the string value of the current xml node
	CvEthicalAlignmentAttitudeModifierInfo* paEthicalAlignmentAttitudeModifier;	// local pointer to the bonus type struct in memory

	// Skip any comments and stop at the next value we might want
	if (SkipToNextVal())
	{
		// initialize the boolean list to the correct size and all the booleans to false
		InitEthicalAlignmentAttitudeModifierList(ppEthicalAlignmentAttitudeModifier, GC.getNumEthicalAlignmentInfos());
		// set the local pointer to the memory we just allocated
		paEthicalAlignmentAttitudeModifier = *ppEthicalAlignmentAttitudeModifier;

		// get the total number of children the current xml node has
		iNumSibs = gDLL->getXMLIFace()->GetNumChildren(m_pFXml);
		// if we can set the current xml node to the child of the one it is at now
		if (gDLL->getXMLIFace()->SetToChild(m_pFXml))
		{
			if(!(iNumSibs <= GC.getNumEthicalAlignmentInfos()))
			{
				char	szMessage[1024];
				sprintf( szMessage, "For loop iterator is greater than array size \n Current XML file is: %s", GC.getCurrentXMLFile().GetCString());
				gDLL->MessageBox(szMessage, "XML Error");
			}
			// loop through all the siblings
			for (int i=0;i<iNumSibs;i++)
			{
				// skip to the next non-comment node
				if (SkipToNextVal())
				{
					// call the function that sets the FXml pointer to the first non-comment child of
					// the current tag and gets the value of that new node
					if (GetChildXmlVal(szNodeVal))
					{
						int iEthicalAlignmentIndex;	// index of the match in the bonus types list
						// call the find in list function to return either -1 if no value is found
						// or the index in the list the match is found at
						iEthicalAlignmentIndex = FindInInfoClass(szNodeVal);
						// if we found a match we will get the next sibling's boolean value at that match's index
						if (iEthicalAlignmentIndex >= 0)
						{
							GetNextXmlVal(&paEthicalAlignmentAttitudeModifier[iEthicalAlignmentIndex].m_iToLawful, -100);
							GetNextXmlVal(&paEthicalAlignmentAttitudeModifier[iEthicalAlignmentIndex].m_iToEthicalNeutral, -100);
							GetNextXmlVal(&paEthicalAlignmentAttitudeModifier[iEthicalAlignmentIndex].m_iToChaotic, -100);

							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}
						else
						{
							gDLL->getXMLIFace()->SetToParent(m_pFXml);
						}

						// set the current xml node to it's parent node
					}

					// if we cannot set the current xml node to it's next sibling then we will break out of the for loop
					// otherwise we will continue looping
					if (!gDLL->getXMLIFace()->NextSibling(m_pFXml))
					{
						break;
					}
				}
			}
			// set the current xml node to it's parent node
			gDLL->getXMLIFace()->SetToParent(m_pFXml);
		}
	}
}
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/


/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/** Initialize the list of Module Directories to be loaded										**/
/*************************************************************************************************/
// Python Modular Loading
template <class T>
void CvXMLLoadUtility::LoadPythonModulesInfo(std::vector<T*>& aInfos, const char* szFileRoot, const char* szXmlPath, bool bTwoPass)
{
	bool bLoaded = false;
	GC.addToInfosVectors(&aInfos);

	GC.setModDir("NONE");

	std::vector<CvString> aszFiles;
	gDLL->enumerateFiles(aszFiles, CvString::format("Python Config\\*_%s.xml", szFileRoot));  // search for the modular files

	for (std::vector<CvString>::iterator it = aszFiles.begin(); it != aszFiles.end(); ++it)
	{
		bLoaded = LoadCivXml(m_pFXml, *it);

		if (!bLoaded)
		{
			char szMessage[1024];
			sprintf(szMessage, "LoadXML call failed for %s.", (*it).GetCString());
			gDLL->MessageBox(szMessage, "XML Load Error");
		}
		else
		{
			SetGlobalClassInfo(aInfos, szXmlPath, bTwoPass);
		}
	}
}
// Main control of the MLF feature
void CvXMLLoadUtility::ModularLoadingControlXML()
{
	CvXMLLoadUtilitySetMod* pSetMod = new CvXMLLoadUtilitySetMod;
	pSetMod->setModLoadControlDirArray(LoadModLoadControlInfo(GC.getModLoadControlInfos(), "CIV4ModularLoadingControls", "Type"));
	SAFE_DELETE(pSetMod);
}


// In the next 2 methods we load the MLF classes
template <class T>
bool CvXMLLoadUtility::LoadModLoadControlInfo(std::vector<T*>& aInfos, const char* szFileRoot, const char* szXmlPath)
{
	GC.addToInfosVectors(&aInfos);
	logMLF("Entering MLF");		//logging

	bool bLoaded = false;
	bool bContinue = true;
	int m_iDirDepth = 0;

	CvXMLLoadUtilityModTools* pProgramDir = new CvXMLLoadUtilityModTools;

	std::string szDirDepth = "modules\\";
	std::string szModDirectory = "modules";
	std::string szConfigString;

	bLoaded = LoadCivXml(m_pFXml, CvString::format("%s\\MLF_%s.xml", szModDirectory.c_str(), szFileRoot));

	if (!bLoaded)
	{
		logMLF("MLF not found, you will now load the modules without Modular Loading Control");  //logging
		return false;
	}
	else
	{
		if ( gDLL->getXMLIFace()->LocateNode(m_pFXml,"Civ4ModularLoadControls/DefaultConfiguration"))
		{
			// call the function that sets the FXml pointer to the first non-comment child of
			// the current tag and gets the value of that new node
			GetChildXmlVal(szConfigString, "NONE");
			if (szConfigString == "NONE")
			{
				logMLF("The default configuration in \"%s\\MLF_%s.xml\" was set to \"NONE\", you will continue loading the regular Firaxian method", szModDirectory.c_str(), szFileRoot);
				return false;   // abort without enumerating anything
			}
		}
		else
		{
			logMLF("The default configuration in \"%s\\MLF_%s.xml\" couldn't be found, you will continue loading using the regular Firaxian method", szModDirectory.c_str(), szFileRoot);
			return false;
		}

		if (!SetModLoadControlInfo(aInfos, szXmlPath, szConfigString, szDirDepth, m_iDirDepth))
		{
			logMLF("The default configuration in \"%s\\MLF_%s.xml\" set by you could not be found, please check your XML settings!", szModDirectory.c_str(), szFileRoot);
			return false;
		}

		//	We want a top to bottom control mechanism. If in any new level there wasn't found a
		//	new MLF we don't want to loop further downwards into the directory hyrarchy
		while (bContinue)
		{
			m_iDirDepth++;
			bContinue = false;	//we want to stop the while loop, unless a new MLF will be found
			//loop through all MLF's so far loaded
			for ( int iInfos = 0; iInfos < GC.getNumModLoadControlInfos(); iInfos++)
			{
				//only loop through files in the actual depth
				if (GC.getModLoadControlInfos(iInfos).getDirDepth() + 1 == m_iDirDepth)
				{
					//loop through the modules of each MLF
					for ( int i = 0; i < GC.getModLoadControlInfos(iInfos).getNumModules(); i++ )
					{
						if ( GC.getModLoadControlInfos(iInfos).isLoad(i) )
						{

							//each new loop we load the previous dir, and check if a MLF file exist on a lower level
							szModDirectory = GC.getModLoadControlInfos(iInfos).getModuleFolder(i);

							//Check if this Modulefolder is parent to a child MLF
							if ( pProgramDir->isModularArt(CvString::format("%s\\MLF_%s.xml", szModDirectory.c_str(), szFileRoot)))
							{
								bLoaded = LoadCivXml(m_pFXml, CvString::format("%s\\MLF_%s.xml", szModDirectory.c_str(), szFileRoot));
							}
							else
							{
								bLoaded = false;
							}

							if (!bLoaded)
							{
								logMLF( "Found module: \"%s\\\"", szModDirectory.c_str() );
							}
							else
							{
								if ( gDLL->getXMLIFace()->LocateNode(m_pFXml,"Civ4ModularLoadControls/DefaultConfiguration"))
								{
									// call the function that sets the FXml pointer to the first non-comment child of
									// the current tag and gets the value of that new node
									GetChildXmlVal(szConfigString, "NONE");
									if (szConfigString == "NONE")
									{
										logMLF("The default configuration in \"%s\\MLF_%s.xml\" was set to \"NONE\", settings in this file will be disregarded", szModDirectory.c_str(), szFileRoot);
									}
									else
									{
										szDirDepth = CvString::format("%s\\", szModDirectory.c_str());
										SetModLoadControlInfo(aInfos, szXmlPath, szConfigString.c_str(), szDirDepth.c_str(), m_iDirDepth);
										bContinue = true; //found a new MLF in a subdir, continue the loop
									}
								}
							}
						}
					}
				}
			}
		}
	}
	SAFE_DELETE(pProgramDir);
	return true;
}

template <class T>
bool CvXMLLoadUtility::SetModLoadControlInfo(std::vector<T*>& aInfos, const char* szTagName, CvString szConfigString, CvString szDirDepth, int iDirDepth)
{
	std::string szCandidateConfig;

	if ( gDLL->getXMLIFace()->LocateNode(m_pFXml,"Civ4ModularLoadControls/ConfigurationInfos/ConfigurationInfo"))
	{
		// loop through each tag
		do
		{
			SkipToNextVal();	// skip to the next non-comment node

			szCandidateConfig = "NONE";
			GetChildXmlValByName(szCandidateConfig, szTagName);
			if (szCandidateConfig == szConfigString)
			{
				T* pClassInfo = new T;

				FAssert(NULL != pClassInfo);
				if (NULL == pClassInfo)
				{
					break;
				}

				bool bSuccess = pClassInfo->read(this, szDirDepth, iDirDepth);
				FAssert(bSuccess);
				if (!bSuccess)
				{
					delete pClassInfo;
					break;
				}

				int iIndex = -1;
				if (NULL != pClassInfo->getType())
				{
					iIndex = GC.getInfoTypeForString(pClassInfo->getType(), true);
					if ( iIndex != -1 )
					{
						logMLF("This type \"%s\" is double", pClassInfo->getType());
						//Catch dupes here, we don't want the overwrite or copy method for the MLF
						CvString szFAssertMsg = CvString::format("The <type>%s</type> of the \"MLF_CIV4ModularLoadingControls.xml\" in directory: \"%s\" is already in use, please use an alternative <type> -name",pClassInfo->getType(), szDirDepth.c_str());
						FAssertMsg(iIndex == -1, szFAssertMsg);
						return false;
					}
				}

				aInfos.push_back(pClassInfo);
				if (NULL != pClassInfo->getType())
				{
					GC.setInfoTypeFromString(pClassInfo->getType(), (int)aInfos.size() - 1);	// add type to global info type hash map
					return true;
				}
			}
		} while (gDLL->getXMLIFace()->NextSibling(m_pFXml));
	}
	return false;
}

bool CvXMLLoadUtility::doResetGlobalInfoClasses()
{
	// PlayerOptions reloaded seperatly because of the MLF Array initialization
	if (!CreateFXml())
		return false;

	LoadGlobalClassInfo(GC.getPlayerOptionInfo(), "CIV4PlayerOptionInfos", "GameInfo", "Civ4PlayerOptionInfos/PlayerOptionInfos/PlayerOptionInfo", false);
	FAssert(GC.getNumPlayerOptionInfos() == NUM_PLAYEROPTION_TYPES);

	DestroyFXml();

	LoadGraphicOptions();
	SetGlobalDefines();
//	LoadGlobalText();   //Thus far everything loaded anyway, it's just text
	SetGlobalTypes();

	return true;
}
bool CvXMLLoadUtility::doResetInfoClasses()
{
	LoadBasicInfos();
	LoadPreMenuGlobals();
	SetPostGlobalsGlobalDefines();
	SetupGlobalLandscapeInfo();
	LoadPostMenuGlobals();

	return true;
}
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	LoadedTGA								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Modifies how the TGA is handled to allow many more religions/corporations/resources easily	**/
/*************************************************************************************************/
template <class T>
void CvXMLLoadUtility::AddTGABogus(std::vector<T*>& aInfos, const char* szInfo)
{
	bool bTGAInfoTypeValid = false;

	T* pTempClassInfo = new T;	// Temp to store while swapping positions
	T* pClassInfo = new T;		// Bogus InfoType

	FAssert(NULL != pTempClassInfo);
	FAssert(NULL != pClassInfo);
	if (NULL == pClassInfo || NULL == pTempClassInfo)
	{
		return;
	}

	CvString verify = CvString::format("%s", szInfo).GetCString();  //string comparison

	if ( verify == "CIV4ReligionInfo" )
	{
		for ( int iI = 0; iI < GC.getDefineINT("GAMEFONT_TGA_RELIGIONS"); iI++ )
		{
			bTGAInfoTypeValid = false;
			// loop through the religions see what we've got
			for ( int iReligion = 0; iReligion < (int)aInfos.size(); iReligion++ )
			{
				// if we found the Religion with the proper TGAIndex, make sure it's on the right spot in the aInfos vector
				if ( GC.getReligionInfo((ReligionTypes)iReligion).getTGAIndex() == iI )
				{
					bTGAInfoTypeValid = true;
				}
			}
			if ( !bTGAInfoTypeValid)
			{
				aInfos.insert(aInfos.begin() + iI, pClassInfo);
			}
		}
	}

	if ( verify == "CIV4CorporationInfo" )
	{
		for ( int iI = 0; iI < GC.getDefineINT("GAMEFONT_TGA_CORPORATIONS"); iI++ )
		{
			bTGAInfoTypeValid = false;
			// loop through the religions see what we've got
			for ( int iCorporation = 0; iCorporation < (int)aInfos.size(); iCorporation++ )
			{
				// if we found the Religion with the proper TGAIndex, make sure it's on the right spot in the aInfos vector
				if ( GC.getCorporationInfo((CorporationTypes)iCorporation).getTGAIndex() == iI )
				{
					bTGAInfoTypeValid = true;
				}
			}
			if ( !bTGAInfoTypeValid)
			{
				aInfos.insert(aInfos.begin() + iI, pClassInfo);
			}
		}
	}
}

// Made an own little function for this one in case we have to clean up any further info vectors in future
// principly any one can be added here in future, if everything is ok, nothing will be done anyway
void CvXMLLoadUtility::cleanTGA()
{
	RemoveTGABogusReligion(GC.getReligionInfo());
	RemoveTGABogusCorporation(GC.getCorporationInfo());
}

template <class T>
void CvXMLLoadUtility::RemoveTGABogusReligion(std::vector<T*>& aInfos)
{
	std::vector <int> viDeletionVector;

	for ( int iI = 0; iI < GC.getNumReligionInfos(); iI++)
	{
		if ( NULL == GC.getReligionInfo((ReligionTypes)iI).getType() )
		{
			viDeletionVector.push_back(iI);
		}
	}

	for ( int iI = (int)viDeletionVector.size() - 1; iI >= 0; iI--)	// gotta do this backwards
	{
		aInfos.erase( aInfos.begin()+viDeletionVector.at(iI));
	}
}

template <class T>
void CvXMLLoadUtility::RemoveTGABogusCorporation(std::vector<T*>& aInfos)
{
	std::vector <int> viDeletionVector;

	for ( int iI = 0; iI < GC.getNumCorporationInfos(); iI++)
	{
		if ( NULL == GC.getCorporationInfo((CorporationTypes)iI).getType() )
		{
			viDeletionVector.push_back(iI);
		}
	}

	for ( int iI = (int)viDeletionVector.size() - 1; iI >= 0; iI--)	// gotta do this backwards
	{
		aInfos.erase( aInfos.begin()+viDeletionVector.at(iI));
	}
}
/*************************************************************************************************/
/**	LoadedTGA								END													**/
/*************************************************************************************************/
