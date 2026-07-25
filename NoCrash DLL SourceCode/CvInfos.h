#pragma once

//  $Header:
//------------------------------------------------------------------------------------------------
//
//  FILE:    CvInfos.h
//
//  PURPOSE: All Civ4 info classes and the base class for them
//
//------------------------------------------------------------------------------------------------
//  Copyright (c) 2003 Firaxis Games, Inc. All rights reserved.
//------------------------------------------------------------------------------------------------
#ifndef CV_INFO_H
#define CV_INFO_H

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**			Needs included since we make some calls to functions within it here					**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
#include "CvXMLLoadUtilityModTools.h"
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
#pragma warning( disable: 4251 )		// needs to have dll-interface to be used by clients of class
#pragma warning( disable: 4127 )

class CvXMLLoadUtility;

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvInfoBase
//
//  DESC:   The base class for all info classes to inherit from.  This gives us
//			the base description and type strings
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:
	DllExport CvInfoBase();
	DllExport virtual ~CvInfoBase();

	virtual void reset();

	DllExport bool isGraphicalOnly() const;										// Exposed to Python

	DllExport const TCHAR* getType() const;										// Exposed to Python
	virtual const TCHAR* getButton() const;					// Exposed to Python
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**		Need to have the Keys available for comparison with module data in CopyNonDefaults		**/
/**		Assert Message helps remind a modder to set up a readpass2 if needed and forgotten		**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	bool isForceOverwrite() const;
	const wchar* getCivilopediaKey() const;
	const wchar* getHelpKey() const;
	const wchar* getStrategyKey() const;
	void copyNonDefaults(CvInfoBase* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL );
	virtual void copyNonDefaultsReadPass2(CvInfoBase* pClassInfo = NULL , CvXMLLoadUtility* pXML = NULL){ pClassInfo; FAssertMsg(false, "Override this"); }
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	// for python wide string handling
	std::wstring pyGetTextKey() { return getTextKeyWide(); }						// Exposed to Python
	std::wstring pyGetDescription() { return getDescription(0); }					// Exposed to Python
	std::wstring pyGetDescriptionForm(uint uiForm) { return getDescription(uiForm); }	// Exposed to Python
	std::wstring pyGetText() { return getText(); }									// Exposed to Python
	std::wstring pyGetCivilopedia() { return getCivilopedia(); }					// Exposed to Python
	std::wstring pyGetHelp() { return getHelp(); }									// Exposed to Python
	std::wstring pyGetStrategy() { return getStrategy(); }							// Exposed to Python

	DllExport const wchar* getTextKeyWide() const;
	DllExport const wchar* getDescription(uint uiForm = 0) const;
	DllExport const wchar* getText() const;
	const wchar* getCivilopedia() const;
	DllExport const wchar* getHelp() const;
	const wchar* getStrategy() const;

	bool isMatchForLink(std::wstring szLink, bool bKeysOnly) const;

	virtual void read(FDataStreamBase* pStream);
	virtual void write(FDataStreamBase* pStream);

	virtual bool read(CvXMLLoadUtility* pXML);
	virtual bool readPass2(CvXMLLoadUtility* pXML) { pXML; FAssertMsg(false, "Override this"); return false; }
	virtual bool readPass3() { FAssertMsg(false, "Override this"); return false; }

protected:

	bool doneReadingXML(CvXMLLoadUtility* pXML);

	bool m_bGraphicalOnly;
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**		The other dependancy data is not saved, it is used during load and then discarded		**/
/**			Someday I'll look it over a bit closer and see if I can move to use the same		**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	bool m_bForceOverwrite;
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	CvString m_szType;
	CvString m_szButton;				// Used for Infos that don't require an ArtAssetInfo
	CvWString m_szTextKey;
	CvWString m_szCivilopediaKey;
	CvWString m_szHelpKey;
	CvWString m_szStrategyKey;

	// translated text
	std::vector<CvString> m_aszExtraXMLforPass3;
	mutable std::vector<CvWString> m_aCachedDescriptions;
	mutable CvWString m_szCachedText;
	mutable CvWString m_szCachedHelp;
	mutable CvWString m_szCachedStrategy;
	mutable CvWString m_szCachedCivilopedia;
};

//
// holds the scale for scalable objects
//
class CvScalableInfo
{
public:

	DllExport CvScalableInfo() : m_fScale(1.0f), m_fInterfaceScale(1.0f) { }

	DllExport float getScale() const;
	DllExport void setScale(float fScale);

	DllExport float getInterfaceScale() const;
	DllExport void setInterfaceScale(float fInterfaceScale);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	CopyNonDefault statements (readpass1) will carry data from the main mod into the Module.	**/
/**	So if a value is not accounted for, then whatever value was in the last module loaded is	**/
/**	what will be retained.  Readpass2 works in the opposite manner though, so must be handled	**/
/**	with greater care (you can forget a field in CopyNonDefaults without a HUGE issue, as most	**/
/**	modules will probably continue to carry full data for any type for a while longer still)	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvScalableInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	float m_fScale;			// Exposed to Python
	float m_fInterfaceScale;	//!< the scale of the unit appearing in the interface screens
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  CLASS:      CvHotkeyInfo
//!  \brief			holds the hotkey info for an info class
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvHotkeyInfo : public CvInfoBase
{
public:
	//constructor
	DllExport CvHotkeyInfo();
	//destructor
	DllExport virtual ~CvHotkeyInfo();

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvHotkeyInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	const WCHAR* getHotKeyDescriptionKey() const;
	const WCHAR* getHotKeyAltDescriptionKey() const;
	const WCHAR* getHotKeyString() const;
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	DllExport virtual void read(FDataStreamBase* pStream);
	DllExport virtual void write(FDataStreamBase* pStream);

	DllExport int getActionInfoIndex() const;
	DllExport void setActionInfoIndex(int i);

	DllExport int getHotKeyVal() const;
	DllExport void setHotKeyVal(int i);
	DllExport int getHotKeyPriority() const;
	DllExport void setHotKeyPriority(int i);
	DllExport int getHotKeyValAlt() const;
	DllExport void setHotKeyValAlt(int i);
	DllExport int getHotKeyPriorityAlt() const;
	DllExport void setHotKeyPriorityAlt(int i);
	DllExport int getOrderPriority() const;
	DllExport void setOrderPriority(int i);

	DllExport bool isAltDown() const;
	DllExport void setAltDown(bool b);
	DllExport bool isShiftDown() const;
	DllExport void setShiftDown(bool b);
	DllExport bool isCtrlDown() const;
	DllExport void setCtrlDown(bool b);
	DllExport bool isAltDownAlt() const;
	DllExport void setAltDownAlt(bool b);
	DllExport bool isShiftDownAlt() const;
	DllExport void setShiftDownAlt(bool b);
	DllExport bool isCtrlDownAlt() const;
	DllExport void setCtrlDownAlt(bool b);

	DllExport const TCHAR* getHotKey() const;			// Exposed to Python
	DllExport void setHotKey(const TCHAR* szVal);

	DllExport std::wstring getHotKeyDescription() const;
	DllExport void setHotKeyDescription(const wchar* szHotKeyDescKey, const wchar* szHotKeyAltDescKey, const wchar* szHotKeyString);

protected:

	int m_iActionInfoIndex;

	int m_iHotKeyVal;
	int m_iHotKeyPriority;
	int m_iHotKeyValAlt;
	int m_iHotKeyPriorityAlt;
	int m_iOrderPriority;

	bool m_bAltDown;
	bool m_bShiftDown;
	bool m_bCtrlDown;
	bool m_bAltDownAlt;
	bool m_bShiftDownAlt;
	bool m_bCtrlDownAlt;

	CvString m_szHotKey;
	CvWString m_szHotKeyDescriptionKey;
	CvWString m_szHotKeyAltDescriptionKey;
	CvWString m_szHotKeyString;

};

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**	Honestly not quite sure why this is needed or precisely what it does, but it links the two	**/
/**				in some manner which is pretty important to proper operations now				**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
class CvDiplomacyInfo;
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
class CvDiplomacyResponse
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvDiplomacyResponse();
	DllExport virtual ~CvDiplomacyResponse();

	DllExport int getNumDiplomacyText();
	DllExport void setNumDiplomacyText(int i);

	DllExport bool getCivilizationTypes(int i);
	DllExport bool* getCivilizationTypes() const;
	DllExport void setCivilizationTypes(int i, bool bVal);

	DllExport bool getLeaderHeadTypes(int i);
	DllExport bool* getLeaderHeadTypes() const;
	DllExport void setLeaderHeadTypes(int i, bool bVal);

	DllExport bool getAttitudeTypes(int i) const;
	DllExport bool* getAttitudeTypes() const;
	DllExport void setAttitudeTypes(int i, bool bVal);

	DllExport bool getDiplomacyPowerTypes(int i);
	DllExport bool* getDiplomacyPowerTypes() const;
	DllExport void setDiplomacyPowerTypes(int i, bool bVal);

	DllExport const TCHAR* getDiplomacyText(int i) const;
	DllExport const CvString* getDiplomacyText() const;
	DllExport void setDiplomacyText(int i, CvString szText);

	DllExport void read(FDataStreamBase* stream);
	DllExport void write(FDataStreamBase* stream);
	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**			Special function is required here because diplomacy data is handled funky			**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void UpdateDiplomacies(CvDiplomacyInfo* pDiplomacyInfo, int iIndex);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:
	int m_iNumDiplomacyText;
	bool* m_pbCivilizationTypes;
	bool* m_pbLeaderHeadTypes;
	bool* m_pbAttitudeTypes;
	bool* m_pbDiplomacyPowerTypes;
	CvString* m_paszDiplomacyText;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpecialistClassInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpecialistClassInfo :
	public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvSpecialistClassInfo();
	virtual ~CvSpecialistClassInfo();
	int getDefaultSpecialistIndex() const;				// Exposed to Python
	void setDefaultSpecialistIndex(int i);
	int getMissionType() const;							// Exposed to Python
	void setMissionType(int iNewType);
	bool isUnique() const;
	int getDefaultSpecialistIndexVector();
	CvString getDefaultSpecialistIndexVectorElement(int i);
	void copyNonDefaults(CvSpecialistClassInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:
	int m_iMissionType;

	int m_iDefaultSpecialistIndex;
	bool m_bUnique;
};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpecialistArtstyleInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpecialistArtstyleInfo :
	public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvSpecialistArtstyleInfo();
	virtual ~CvSpecialistArtstyleInfo();
	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpecialistInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpecialistInfo : public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvSpecialistInfo();
	virtual ~CvSpecialistInfo();

	int getSpecialistClassType() const;

	int getGreatPeopleUnitClass() const;		// Exposed to Python
	int getGreatPeopleRateChange() const;		// Exposed to Python
/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
	int getHealth() const;							// Exposed to Python
	int getHappiness() const;							// Exposed to Python
	int getCrime() const;							// Exposed to Python
	int getCityDefense() const;							// Exposed to Python
	int getExtraTradeRoutes() const;							// Exposed to Python
	/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/
	int getExperience() const;				// Exposed to Python
	int getUnitCombatFreeXP(int i) const;				// Exposed to Python
	int getTrainXPCap(int i) const;				// Exposed to Python
	float getTrainXPRate(int i) const;				// Exposed to Python


	bool isVisible() const;				// Exposed to Python

	// Arrays

	int getYieldChange(int i) const;		// Exposed to Python
	const int* getYieldChangeArray() const;		// Exposed to Python - For Moose - CvWidgetData
	int getCommerceChange(int i) const;		// Exposed to Python
	int getFlavorValue(int i) const;		// Exposed to Python

	int getSpecialistClassExtraYield(int i, int j) const;		// Exposed to Python
	const int* getSpecialistClassExtraYieldArray(int i) const;		// Exposed to Python
	int getSpecialistClassExtraCommerce(int i, int j) const;		// Exposed to Python
	const int* getSpecialistClassExtraCommerceArray(int i) const;		// Exposed to Python
	int getSpecialistClassExtraCrime(int i) const;		// Exposed to Python

	const TCHAR* getTexture() const;				// Exposed to Python
	void setTexture(const TCHAR* szVal);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvSpecialistInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
	int m_iSpecialistClassType;

	int m_iGreatPeopleUnitClass;		// Exposed to Python
	int m_iGreatPeopleRateChange;		// Exposed to Python
/*************************************************************************************************/
/** Specialists Enhancements, by Supercheese 10/9/09           Imported by Valkrionn   10/22/09  */
/**                                                                                              */
/**                                                                                              */
/*************************************************************************************************/
	int m_iHealth;
	int m_iHappiness;
	int m_iCrime;
	int m_iCityDefense;
	int m_iExtraTradeRoutes;
	/*************************************************************************************************/
/** Specialists Enhancements                          END                                        */
/*************************************************************************************************/
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
	float m_iExperience;
	float* m_piUnitCombatFreeXP;
	float* m_piTrainXPCap;
	float* m_piTrainXPRate;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int** m_ppiSpecialistClassExtraYield;
	int** m_ppiSpecialistClassExtraCommerce;
	int* m_piSpecialistClassExtraCrime;

	bool m_bVisible;				// Exposed to Python

	CvString m_szTexture;

	// Arrays

	int* m_piYieldChange;
	int* m_piCommerceChange;
	int* m_piFlavorValue;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTechInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTechInfo : public CvInfoBase
{

friend class CvXMLLoadUtility;

//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvTechInfo();
	virtual ~CvTechInfo();

	int getAdvisorType() const;						// Exposed to Python
	int getAIWeight() const;							// Exposed to Python
	int getAITradeModifier() const;				// Exposed to Python
	int getResearchCost() const;					// Exposed to Python
	int getAdvancedStartCost() const;				// Exposed to Python
	int getAdvancedStartCostIncrease() const;				// Exposed to Python
	int getEra() const;										// Exposed to Python
	int getTradeRoutes() const;						// Exposed to Python
	int getFeatureProductionModifier() const;	// Exposed to Python
	int getWorkerSpeedModifier() const;		// Exposed to Python
	int getFirstFreeUnitClass() const;		// Exposed to Python
	int getHealth() const;								// Exposed to Python
	int getHappiness() const;							// Exposed to Python
	int getFirstFreeTechs() const;				// Exposed to Python
	int getAssetValue() const;						// Exposed to Python
	int getPowerValue() const;						// Exposed to Python

	int getGridX() const;									// Exposed to Python
	int getGridY() const;									// Exposed to Python

	bool isRepeat() const;								// Exposed to Python
	bool isTrade() const;									// Exposed to Python
	bool isDisable() const;								// Exposed to Python
	bool isGoodyTech() const;							// Exposed to Python
	bool isExtraWaterSeeFrom() const;			// Exposed to Python
	bool isMapCentering() const;					// Exposed to Python
	bool isMapVisible() const;						// Exposed to Python
	bool isMapTrading() const;						// Exposed to Python
	bool isTechTrading() const;						// Exposed to Python
	bool isGoldTrading() const;						// Exposed to Python
	bool isOpenBordersTrading() const;		// Exposed to Python
	bool isDefensivePactTrading() const;	// Exposed to Python
	bool isPermanentAllianceTrading() const;	// Exposed to Python
	bool isVassalStateTrading() const;	// Exposed to Python
	bool isBridgeBuilding() const;				// Exposed to Python
	bool isIrrigation() const;						// Exposed to Python
	bool isIgnoreIrrigation() const;			// Exposed to Python
	bool isWaterWork() const;							// Exposed to Python
	bool isRiverTrade() const;							// Exposed to Python

	std::wstring getQuote() const;	// Exposed to Python
	void setQuoteKey(const TCHAR* szVal);
	const TCHAR* getSound() const;				// Exposed to Python
	void setSound(const TCHAR* szVal);
	const TCHAR* getSoundMP() const;			// Exposed to Python
	void setSoundMP(const TCHAR* szVal);

	// Arrays

	int getDomainExtraMoves(int i) const;	// Exposed to Python
	int getFlavorValue(int i) const;			// Exposed to Python
	int getPrereqOrTechs(int i) const;		// Exposed to Python
	int getPrereqAndTechs(int i) const;		// Exposed to Python

	bool isCommerceFlexible(int i) const;	// Exposed to Python
	bool isTerrainTrade(int i) const;			// Exposed to Python

//FfH Techs: Added by Kael 08/09/2007
	bool isWater() const;
	int getPrereqReligion() const;
	bool readPass3();
//FfH: End Add

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	int getCityCapModifier() const;
/*************************************************************************************************/
/** CityPopCap                      END                                                         **/
/*************************************************************************************************/
/************************************************************************************************/
/* Influence Driven War                   06/24/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool isInfluenceAllowed() const;
	int getVictoryInfluenceModifier() const;
	int getDefeatInfluenceModifier() const;
	int getPillageInfluenceModifier() const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(TechInfos) 			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getPrereqBroadAlignment() const;
	int getAlignmentModifier() const;
	int getFirstToTechAlignmentModifier() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getPrereqBroadEthicalAlignment() const;
	int getEthicalAlignmentModifier() const;
	int getFirstToTechEthicalAlignmentModifier() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int getBonusPrereq() const;
	int getTechCostShift(int i, bool bValue = false) const;
	int getNumTechCostShifts() const;
	int getTechCostMod(int i, bool bValue = false) const;
	int getNumTechCostMods() const;

	int getBonusCostShift(int i) const;
	int getBonusCostMod(int i) const;
	int getPrereqReligionVectorSize();
	CvString getPrereqReligionVectorElement(int i);
	int getBonusCostShiftsVectorSize();
	CvString getBonusCostShiftNamesVectorElement(int i);
	int getBonusCostShiftValuesVectorElement(int i);
	int getBonusCostModsVectorSize();
	CvString getBonusCostModNamesVectorElement(int i);
	int getBonusCostModValuesVectorElement(int i);

	int getSpecialistTypeYieldChange(int i, int j);
	const int* getSpecialistTypeYieldChangeArray(int i);
	int getSpecialistTypeCommerceChange(int i, int j);
	const int* getSpecialistTypeCommerceChangeArray(int i);
	int getSpecialistTypeHealthChange(int i);
	int getSpecialistTypeHappinessChange(int i);
	int getSpecialistTypeCrimeChange(int i);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	void read(FDataStreamBase* );
	void write(FDataStreamBase* );

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	const TCHAR* getQuoteKey();
	void copyNonDefaults(CvTechInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	void copyNonDefaultsReadPass2(CvTechInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iAdvisorType;
	int m_iAIWeight;
	int m_iAITradeModifier;
	int m_iResearchCost;
	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;
	int m_iEra;
	int m_iTradeRoutes;
	int m_iFeatureProductionModifier;
	int m_iWorkerSpeedModifier;
	int m_iFirstFreeUnitClass;
	int m_iHealth;
	int m_iHappiness;
	int m_iFirstFreeTechs;
	int m_iAssetValue;
	int m_iPowerValue;

	int m_iGridX;
	int m_iGridY;

	bool m_bRepeat;
	bool m_bTrade;
	bool m_bDisable;
	bool m_bGoodyTech;
	bool m_bExtraWaterSeeFrom;
	bool m_bMapCentering;
	bool m_bMapVisible;
	bool m_bMapTrading;
	bool m_bTechTrading;
	bool m_bGoldTrading;
	bool m_bOpenBordersTrading;
	bool m_bDefensivePactTrading;
	bool m_bPermanentAllianceTrading;
	bool m_bVassalStateTrading;
	bool m_bBridgeBuilding;
	bool m_bIrrigation;
	bool m_bIgnoreIrrigation;
	bool m_bWaterWork;
	bool m_bRiverTrade;

	CvString m_szQuoteKey;
	CvString m_szSound;
	CvString m_szSoundMP;

//FfH Techs: Added by Kael 08/09/2007
	bool m_bWater;
/*************************************************************************************************/
/**	Cutting								25/07/10										Snarko	**/
/**																								**/
/**				Removing rarely used/redundant stuff to improve speed.							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iPreferredAlignment;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Cutting									END													**/
/*************************************************************************************************/
	int m_iPrereqReligion;
//FfH: End Add

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	int m_iCityCapModifier;
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/
/************************************************************************************************/
/* Influence Driven War                   06/24/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool m_bInfluenceAllowed;
	int m_iVictoryInfluenceModifier;
	int m_iDefeatInfluenceModifier;
	int m_iPillageInfluenceModifier;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	// Arrays

	int* m_piDomainExtraMoves;
	int* m_piFlavorValue;

	int* m_piPrereqOrTechs;
	int* m_piPrereqAndTechs;

	bool* m_pbCommerceFlexible;
	bool* m_pbTerrainTrade;
/*************************************************************************************************/
/**	New Tag Defs	(TechInfos)				05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iPrereqBroadAlignment;
	int m_iAlignmentModifier;
	int m_iFirstToTechAlignmentModifier;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Cutting								25/07/10										Snarko	**/
/**																								**/
/**				Removing rarely used/redundant stuff to improve speed.							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iPreferredEthicalAlignment;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Cutting									END													**/
/*************************************************************************************************/
	int m_iPrereqBroadEthicalAlignment;
	int m_iEthicalAlignmentModifier;
	int m_iFirstToTechEthicalAlignmentModifier;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int m_iBonusPrereq;
	int** m_piiTechCostShifts;
	int m_iNumTechCostShifts;
	int** m_piiTechCostMods;
	int m_iNumTechCostMods;
	int* m_piBonusCostShift;

	int** m_ppiSpecialistTypeYieldChanges;
	int** m_ppiSpecialistTypeCommerceChanges;
	int* m_piSpecialistTypeHealthChanges;
	int* m_piSpecialistTypeHappinessChanges;
	int* m_piSpecialistTypeCrimeChanges;
	std::vector<CvString> m_aszBonusCostShiftsforPass3;
	std::vector<int> m_aiBonusCostShiftsforPass3;
	int* m_piBonusCostMod;
	std::vector<CvString> m_aszBonusCostModsforPass3;
	std::vector<int> m_aiBonusCostModsforPass3;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvPromotionInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvPromotionInfo :	public CvHotkeyInfo
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:
	CvPromotionInfo();
	virtual ~CvPromotionInfo();

	int getLayerAnimationPath() const;
	int getPrereqPromotion() const;				// Exposed to Python
	void setPrereqPromotion(int i);				// Exposed to Python
	int getPrereqOrPromotion1() const;				// Exposed to Python
	void setPrereqOrPromotion1(int i);				// Exposed to Python
	int getPrereqOrPromotion2() const;				// Exposed to Python
	void setPrereqOrPromotion2(int i);				// Exposed to Python

	int getTechPrereq() const;				// Exposed to Python
	int getStateReligionPrereq() const;				// Exposed to Python
	int getCaptureUnitClass() const;				// Exposed to Python
	int getVisibilityChange() const;				// Exposed to Python
	int getMovesChange() const;				// Exposed to Python
	int getMoveDiscountChange() const;				// Exposed to Python
	int getAirRangeChange() const;				// Exposed to Python
	int getInterceptChange() const;				// Exposed to Python
	int getEvasionChange() const;				// Exposed to Python
	int getWithdrawalChange() const;				// Exposed to Python
	int getEnemyWithdrawalChange() const;				// Exposed to Python
	int getCargoChange() const;				// Exposed to Python
	int getCollateralDamageChange() const;				// Exposed to Python
	int getBombardRateChange() const;				// Exposed to Python
	int getFirstStrikesChange() const;				// Exposed to Python
	int getChanceFirstStrikesChange() const;				// Exposed to Python
	int getEnemyHealChange() const;				// Exposed to Python
	int getNeutralHealChange() const;				// Exposed to Python
	int getFriendlyHealChange() const;				// Exposed to Python
	int getSameTileHealChange() const;				// Exposed to Python
	int getAdjacentTileHealChange() const;				// Exposed to Python
	int getCombatPercent() const;				// Exposed to Python
	int getCityAttackPercent() const;				// Exposed to Python
	int getCityDefensePercent() const;				// Exposed to Python
	int getHillsAttackPercent() const;				// Exposed to Python
	int getHillsDefensePercent() const;				// Exposed to Python
	int getCommandType() const;									// Exposed to Python
	void setCommandType(int iNewType);

	int getRevoltProtection() const;				// Exposed to Python
	int getCollateralDamageProtection() const;				// Exposed to Python
	int getPillageChange() const;				// Exposed to Python
	int getUpgradeDiscount() const;				// Exposed to Python
	int getExperiencePercent() const;				// Exposed to Python
	int getKamikazePercent() const;				// Exposed to Python

	bool isLeader() const;				// Exposed to Python
	bool isBlitz() const;				// Exposed to Python
	bool isAmphib() const;				// Exposed to Python
	bool isRiver() const;				// Exposed to Python
	bool isEnemyRoute() const;				// Exposed to Python
	bool isAlwaysHeal() const;				// Exposed to Python
	bool isHillsDoubleMove() const;				// Exposed to Python
	bool isImmuneToFirstStrikes() const;				// Exposed to Python
	bool isDurationDecreaseSpellpower() const;				// Exposed to Python

	bool isTradeDefender() const;

	const TCHAR* getSound() const;				// Exposed to Python
	void setSound(const TCHAR* szVal);

	// Arrays
	int getNoBadExploreImprovement(int i) const;
	int getNoBadExploreImprovementsVectorSize();
	CvString getNoBadExploreImprovementNamesVectorElement(int i);
	int getNoBadExploreImprovementValuesVectorElement(int i);

	int getTerrainAttackPercent(int i) const;				// Exposed to Python
	int getTerrainDefensePercent(int i) const;				// Exposed to Python
	int getFeatureAttackPercent(int i) const;				// Exposed to Python
	int getFeatureDefensePercent(int i) const;				// Exposed to Python
	int getPlotEffectAttackPercent(int i) const;				// Exposed to Python
	int getPlotEffectDefensePercent(int i) const;				// Exposed to Python
	/*************************************************************************************************/
/**	GWS										2010-08-23									Milaga	**/
/**																								**/
/**					Units can have movement modifiers for different terrain						**/
/*************************************************************************************************/
// CvPromotionInfo Public
	int getPromotionHillCost() const;
	int getPromotionPeakCost() const;
	int getPromotionTerrainCost(int i) const;
	int getPromotionFeatureCost(int i) const;
/*************************************************************************************************/
/**	GWS										END													**/
/*************************************************************************************************/
	int getUnitCombatModifierPercent(int i) const;				// Exposed to Python

	//Upgraded Capture Rate by BI 08/16/11
	int getUnitCombatCaptureRatePercent(int i) const;				// Exposed to Python
	bool isUnitCombatNonCapture(int i) const;				// Exposed to Python

	int getDomainModifierPercent(int i) const;				// Exposed to Python

	bool getTerrainDoubleMove(int i) const;				// Exposed to Python
	bool getFeatureDoubleMove(int i) const;				// Exposed to Python
	bool getPlotEffectDoubleMove(int i) const;				// Exposed to Python
	int getExtraSpellClassPower(int i) const;				// Exposed to Python
	bool getUnitCombat(int i) const;				// Exposed to Python
	int getMaxExpReward() const;
	/*************************************************************************************************/
/**	MobileCage								01/28/2010								Valkrionn	**/
/**																								**/
/**										Leashes	a unit to a plot								**/
/*************************************************************************************************/
	int getLeashRange() const;
	bool isLeashed() const;
	int getLeashChance() const;
	int getMaxLeash() const;
/*************************************************************************************************/
/**	MobileCage									END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/** Shades					  				07/30/10								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	bool isLeveledImmortality() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool isNonInfluence() const;							// Exposed to Python
	bool isInfluence() const;								// Exposed to Python
	int getVictoryInfluenceModifier() const;				// Exposed to Python
	int getDefeatInfluenceModifier() const;				// Exposed to Python
	int getPillageInfluenceModifier() const;			// Exposed to Python
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	int getExtraPerception() const;
	int getInvisibleLevel() const;
	bool isRevealed() const;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(PromotionInfos)		05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int getCommandLimit() const;
	int getCommandRange() const;
	int getCommandXPShareRate() const;
	int getNumMinionPromotions() const;
	PromotionTypes getMinionPromotion(int iI) const;
	int getNumCapturePromotions() const;
	PromotionTypes getCapturePromotion(int iI) const;
	int getNumCommanderPromotions() const;
	PromotionTypes getCommanderPromotion(int iI) const;
	int getNumSlavePromotions() const;
	PromotionTypes getSlavePromotion(int iI) const;
	int getNumMasterPromotions() const;
	PromotionTypes getMasterPromotion(int iI) const;
	CvString getPrereqUnitsVectorElement(int i);
	CvString getPrereqCivilizationsVectorElement(int i);
	CvString getPrereqCivicsVectorElement(int i);
	CvString getPrereqImprovementsVectorElement(int i);
	CvString getPrereqCorporationsVectorElement(int i);
	CvString getPrereqTraitsVectorElement(int i);
	CvString getPrereqBuildingANDsVectorElement(int i);
	CvString getPrereqBuildingORsVectorElement(int i);
	CvString getPrereqEventANDsVectorElement(int i);
	CvString getPrereqEventORsVectorElement(int i);
	CvString getPrereqUnitTypesOnTileVectorElement(int i);
	CvString getPrereqUnitTypesNOTOnTileVectorElement(int i);
/*************************************************************************************************/
/**	Workers Paradise						01/08/10											**/
/**																								**/
/**							Allows promotions to affect build orders							**/
/*************************************************************************************************/
	CvString getPromotionBuildsVectorElement(int i);
	CvString getPromotionCannotBuildsVectorElement(int i);
/*************************************************************************************************/
/**	Workers Paradise						END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	CvString getAffinitiesVectorElement(int i);
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
	int getUnitArtStyleTypeVectorSize();
	CvString getUnitArtStyleTypeVectorElement(int i);
	const TCHAR* getPyOnRemove() const;
/*************************************************************************************************/
/**	Promotion PyHelp		 				07/09/10								Valkrionn	**/
/**																								**/
/**							Allows promotions to have dynamic help								**/
/*************************************************************************************************/
	const char* getPythonHelp() const;
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/
	bool isCommunalProperty() const;
	bool isNeverHostile() const;
	bool isBlind() const;
	bool isOverrideHelpText() const;
	bool isRequirePermission() const;
	bool isCannotCast() const;
	bool isFreeUnit() const;
	bool isNoSupply() const;
	bool isTerritorial() const;
	bool isRivalTerritoryExplore() const;
	bool isRivalTerritoryBlock() const;
	bool isPillageOnMove() const;
	bool isSelfPillage() const;
	bool isGetCasterXP() const;
	bool isNonWarWeariness() const;
	bool isNoMapReveal() const;
	bool isCannotCapture() const;
	bool isCityHappy() const;
	bool isCityNoHappy() const;
	bool isNoSupport() const;
	bool isCanPillage() const;
	bool isCannotPillage() const;
	bool isCitySpy() const;
	bool isStartGoldenAge() const;
	bool isNoDefenseBonus() const;
	bool isMoveImpassable() const;
	bool isClimbPeaks() const;
	bool isFlatMoveCost() const;
	bool isIgnoreTerrainCosts() const;
	bool isAttackNoWar() const;
	bool isAllowAttacks() const;
	bool isFirstStrikeVulnerable() const;
	bool isAllowDefenseBonuses() const;
	bool isNonAbandon() const;
	bool isIndependant() const;
	bool isReligiousCommanderPromo() const; //Religious Commander by BI 07/24/11
	bool isEffectProm() const;
	bool isStackEffect() const;
	bool isAutoAcquire() const;
	bool isMustMaintain() const;
	bool isPrereqInCity() const;
	bool isNoXP() const;
	bool isPrereqInBorderEnemy() const;
	bool isPrereqInBorderRival() const;
	bool isPrereqInBorderTeam() const;
	bool isPrereqInBorderSelf() const;
	bool isPrereqInBorderNone() const;
	bool isAllowNULLUnitCombat() const;

	int getRandomApplyChance() const;
	int getAssetValue() const;
/*************************************************************************************************/
/**	Unit power						17/02/12										Snarko		**/
/**																								**/
/**							Rewriting unit power system											**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getPowerValue() const;
/**								----  End Original Code  ----									**/
	int getPowerAdd() const;
	int getPowerMult() const;
/*************************************************************************************************/
/**	Unit power						END															**/
/*************************************************************************************************/
	int getTempUnitCombat() const;
	int getDamageOnRemove() const;
	int getFreeXPCap() const;
	float getCasterXPRate() const;
	int getDuration() const;
	int getAirCombat() const;
	int getAirCombatLimitBoost() const;
	int getExtraDropRange() const;
	int getPrereqBroadAlignment() const;
	int getAlignmentModifier() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getPrereqBroadEthicalAlignment() const;
	int getEthicalAlignmentModifier() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int getSpellExtraRange() const;
	int getCombatConversionChance() const;
	int getCombatUnitGenerationChance() const;
	int getSlaveGenerationChance() const;
	int getGiftableXP() const;
	int getCombatExtraDuration() const;
	int getDurationPerTurn() const;
	int getDurationAlter() const;
	int getChangeDuration() const;
	int getExtraSupport() const;
	int getChanceMiscast() const;
	int getCombatDmgCapBoost() const;
	int getCollateralLimitCap() const;
	int getCollateralLimitBoost() const;
	int getCollateralTargetsLimit() const;
	int getCollateralExtraTargets() const;

/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	int getFlankingLimitBoost() const;
	int getFlankingExtraTargets() const;
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/

	int getHammerSacrifice() const;
	int getExtraHammerPerPop() const;
	int getFoodSacrifice() const;
	int getPopulationAdd() const;
	int getBeakerSacrifice() const;
	int getExtraBeakerPerPop() const;
	int getGoldSacrifice() const;
	int getExtraGoldPerPop() const;
	int getCultureSacrifice() const;
	int getExtraCulturePerPop() const;
	int getPrereqMinAge() const;
	int getPrereqMaxAge() const;
	int getGoldCost() const;
	int getXPTranserRate() const;
	int getYieldFromWin(int i) const;
	int getYieldForLoss(int i) const;
	int getCommerceFromWin(int i) const;
	int getCommerceForLoss(int i) const;
	int getPrereqTier() const;
	int getPrereqWeaponTier() const;
	int getNumPromotionExcludes() const;
	PromotionTypes getPromotionExcludes(int iI) const;
	int getNumPromotionAllows() const;
	PromotionTypes getPromotionAllows(int iI) const;
	int getNumPromotionReplacedBy() const;
	PromotionTypes getPromotionReplacedBy(int iI) const;
	int getNumPromotionOverwrites() const;
	PromotionTypes getPromotionOverwrites(int iI) const;
	int getNumPromotionDegradesTo() const;
	PromotionTypes getPromotionDegradesTo(int iI) const;
	int getNumPrereqUnits() const;
	int getPrereqUnit(int iI) const;
	int getNumPrereqReligions() const;
	int getPrereqReligion(int iI) const;
	int getNumPrereqTechANDs() const;
	int getPrereqTechAND(int iI) const;
	int getNumPrereqTechORs() const;
	int getPrereqTechOR(int iI) const;
	int getNumPrereqAlignments() const;
	int getPrereqAlignment(int iI) const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getNumPrereqEthicalAlignments() const;
	int getPrereqEthicalAlignment(int iI) const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int getNumPrereqFeatures() const;
	int getPrereqFeature(int iI) const;
	int getNumPrereqPlotEffects() const;
	int getPrereqPlotEffect(int iI) const;
	int getNumPrereqTerrains() const;
	int getPrereqTerrain(int iI) const;
	int getNumPrereqBonusANDs() const;
	int getPrereqBonusAND(int iI) const;
	int getNumPrereqBonusORs() const;
	int getPrereqBonusOR(int iI) const;
	int getNumPrereqCivilizations() const;
	int getPrereqCivilization(int iI) const;
	int getNumPrereqCivics() const;
	int getPrereqCivic(int iI) const;
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
	int getNumSecondaryUnitCombats() const;
	int getSecondaryUnitCombats(int iI) const;
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
	int getNumPrereqImprovements() const;
	int getPrereqImprovement(int iI) const;
	int getNumPrereqBuildingANDs() const;
	int getPrereqBuildingAND(int iI) const;
	int getNumPrereqBuildingORs() const;
	int getPrereqBuildingOR(int iI) const;
	int getNumPrereqCorporations() const;
	int getPrereqCorporation(int iI) const;
	int getNumPrereqTraits() const;
	int getPrereqTrait(int iI) const;
	int getNumPrereqEventANDs() const;
	int getPrereqEventAND(int iI) const;
	int getNumPrereqEventORs() const;
	int getPrereqEventOR(int iI) const;
	int getNumPrereqFeatANDs() const;
	int getPrereqFeatAND(int iI) const;
	int getNumPrereqFeatORs() const;
	int getPrereqFeatOR(int iI) const;
	int getNumPrereqFeatNOTs() const;
	int getPrereqFeatNOT(int iI) const;

	const TCHAR* getPyPostCombatLost() const;
	const TCHAR* getPyPostCombatWon() const;
/*************************************************************************************************/
/**	PyOnPromoTaken							   08/28/10								Valkrionn	**/
/*************************************************************************************************/
	const TCHAR* getPyOnPromoTaken() const;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
	const TCHAR* getNewName() const;

	int getInvisibleType(int i) const;
	int getNumInvisibleTypes() const;
	int getSeeInvisibleType(int i) const;
	int getNumSeeInvisibleTypes() const;

	int getNumCityBonuses() const;
	CityBonuses getCityBonus(int iI) const;
	std::list<CityBonuses> listCityBonuses();
	//Aura black_imp 24/09/15
	int getNumAuraBonuses() const;
	AuraBonuses getAuraBonus(int iI) const;
	std::list<AuraBonuses> listAuraBonuses();

	int getNumPrereqUnitTypesOnTile() const;
	int getPrereqUnitTypeOnTile(int iI) const;
	int getNumPrereqUnitTypesNOTOnTile() const;
	int getPrereqUnitTypeNOTOnTile(int iI) const;
/*************************************************************************************************/
/**	Workers Paradise						01/08/10											**/
/**																								**/
/**							Allows promotions to affect build orders							**/
/*************************************************************************************************/
	int getNumPromotionBuilds() const;
	int getPromotionBuilds(int iI) const;
	int getNumPromotionCannotBuilds() const;
	int getPromotionCannotBuilds(int iI) const;
/*************************************************************************************************/
/**	Workers Paradise						END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	int getNumAffinities() const;
	int getAffinities(int iI) const;
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
	int getNumPrereqUnitClassesOnTile() const;
	int getPrereqUnitClassOnTile(int iI) const;
	int getNumPrereqUnitClassesNOTOnTile() const;
	int getPrereqUnitClassNOTOnTile(int iI) const;
	int getNumPrereqPromotionsOnTile() const;
	int getPrereqPromotionOnTile(int iI) const;
	int getNumPrereqPromotionsNOTOnTile() const;
	int getPrereqPromotionNOTOnTile(int iI) const;
	int getNoBadExplore() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH: Added by Kael 07/30/2007
	bool isEnraged() const;
	bool isBoarding() const;
	bool isOnlyDefensive() const;
	bool isDispellable() const;
	int getPrereqDispelPower() const;
	bool isDoubleFortifyBonus() const;
	bool isEquipment() const;
	bool isFear() const;
	bool isFlying() const;
	bool isPrereqAliveCapture() const;
	bool isHeld() const;
	bool isHiddenNationality() const;
	bool isIgnoreBuildingDefense() const;
	bool isImmortal() const;
	bool isImmuneToCapture() const;
	bool isImmuneToDefensiveStrike() const;
	bool isImmuneToFear() const;
	bool isImmuneToMagic() const;
	bool isInvisible() const;
	bool isMutation() const;
/*************************************************************************************************/
/**	Dynamic Mutation						06/15/10								Valkrionn	**/
/**																								**/
/**							New tags used by the Dynamic Mutation system						**/
/*************************************************************************************************/
	int getMutationWeight() const;
	int getMutationMin() const;
	int getMutationMax() const;
	int getMutationMaxApplications() const;
	bool isBadEffect() const;
/*************************************************************************************************/
/**	DynamicMutation								END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	1.4										03/28/11								Valkrionn	**/
/**																								**/
/**									New tags required for 1.4									**/
/*************************************************************************************************/
	int getMaxApplications() const;
	int getUnitCombatMaxApplications(int i) const;
	int getPrereqPromotionORs(int i, bool bValue = false) const;
	int getPrereqPromotionANDs(int i, bool bValue = false) const;
	int getNumPrereqPromotionORs() const;
	int getNumPrereqPromotionANDs() const;
	
	int getPromotionCombatMods(int i, bool bValue = false) const;
	int getNumPromotionCombatMods() const;
	int getAntiWithdrawal() const;
	int getAntiFirstStrikes() const;
	int getRangedCombatPercent() const;
	int getRangedCombatPercentGlobalCounter() const;
	int getRangedCombatPercentInBorders() const;
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/
	bool isNotAlive() const;
	bool isPrereqAlive() const;
	bool isPrereqRevealed() const;				// Exposed to Python
	bool isPrereqHidden() const;				// Exposed to Python
	bool isRace() const;
	bool isMentalEffect() const;
	bool isCompanion() const;
	bool isGraphicalAddOnPromotion() const;
	bool isRemovedByCasting() const;
	bool isRemovedByCombat() const;
	bool isRemovedWhenHealed() const;
/*************************************************************************************************/
/**	BeenThereDoneThat						04/04/09								Xienwolf	**/
/**																								**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool isSeeInvisible() const;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	BeenThereDoneThat						END													**/
/*************************************************************************************************/
	bool isTargetWeakestUnit() const;
	bool isTargetWeakestUnitCounter() const;
	int getMulticast() const;
	bool isValidate() const;
	bool isWaterWalking() const;
	int getAIWeight() const;
	int getBetrayalChance() const;
	int getBetterDefenderThanPercent() const;
	int getCasterResistModify() const;
	int getCombatCapturePercent() const;
	int getCombatHealPercent() const;
	int getCombatLimit() const;
	int getCombatPercentDefense() const;
	int getCombatPercentGlobalCounter() const;
	int getCombatPercentInBorders() const;
	int getDefensiveStrikeChance() const;
	int getDefensiveStrikeDamage() const;
	int getExpireChance() const;
	int getExtraCombatStr() const;
	int getExtraCombatDefense() const;
	int getFreeXPPerTurn() const;
	int getFreeXPFromCombat() const;
/*************************************************************************************************/
/**	BeenThereDoneThat						04/04/09								Xienwolf	**/
/**																								**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getGoldFromCombat() const;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	BeenThereDoneThat						END													**/
/*************************************************************************************************/
	int getGroupSize() const;
	int getMinLevel() const;
/*************************************************************************************************/
/**	PrereqStrBoostSize						10/16/09								Valkrionn	**/
/**																								**/
/**					Allows a units StrBoost to be used as a promotion prereq					**/
/*************************************************************************************************/
	int getPrereqStrBoostSize() const;
/*************************************************************************************************/
/**	PrereqStrBoostSize							END												**/
/*************************************************************************************************/
	int getModifyGlobalCounter() const;
	int getModifyGlobalCounterOnCombat() const;
	int getResistMagic() const;
	int getSpellCasterXP() const;
	int getSpellDamageModify() const;
	int getWorkRateModify() const;
	int getWorkRateModifier() const;
	int getCaptureUnitCombat() const;
	int getBlockedSpellClass() const;
	int getPromotionCombatApply() const;
/*************************************************************************************************/
/**	Cutting								30/01/12										Snarko	**/
/**																								**/
/**				Removing rarely used/redundant stuff to improve speed.							**/
/**			Use PromotionExcludes instead, both faster and more flexible						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getPromotionImmune1() const;
	int getPromotionImmune2() const;
	int getPromotionImmune3() const;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Cutting									END													**/
/*************************************************************************************************/
	int getPromotionRandomApply() const;
	int getPromotionSummonPerk() const;
	int getBonusPrereq() const;
	int getPromotionPrereqOr3() const;
	int getPromotionPrereqOr4() const;
	int getPromotionPrereqAnd() const;
	int getUnitReligionPrereq() const; //PrereqUnitReligion by BI 07/24/11
	int getPromotionNextLevel() const;
	const TCHAR* getPyPerTurn() const;
	const TCHAR* getExtraArtType() const;
	const TCHAR* getReplaceArtType() const;
	int getUnitArtStyleType() const;
	int getPromotionCombatType() const;
	int getPromotionCombatMod() const;

	//ReligionCombatBonus by BI 07/25/11
	int getReligionCombatType() const;
	int getReligionCombatMod() const;
/*************************************************************************************************/
/**	MISSION_INQUISITION						13/01/12									Snarko	**/
/**																								**/
/**			Adding a mission for inquisition and teaching the AI proper use						**/
/*************************************************************************************************/
	bool isInquisition() const;
/*************************************************************************************************/
/**	MISSION_INQUISITION END																		**/
/*************************************************************************************************/


	int getBonusAffinity(int i) const;
	int getDamageTypeCombat(int i) const;
	int getDamageTypeResist(int i) const;
	//PromotionClass
	PromotionClassTypes getPromotionClass() const;
	PromotionClassTypes getPromotionClassOverwrite() const;
	SpecialUnitTypes getSpecialCargo() const;
	DomainTypes getDomainCargo() const;
	bool readPass3();
//FfH: End Add

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvPromotionInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	void copyNonDefaultsReadPass2(CvPromotionInfo* pClassInfo = NULL , CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
	//Magic Rework
	int getMagicalPower() const;
	int getMinMagicalPower() const;
	//	int getDominionCapacity() const;

protected:

	int m_iLayerAnimationPath;
	int m_iPrereqPromotion;
	int m_iPrereqOrPromotion1;
	int m_iPrereqOrPromotion2;

	int m_iTechPrereq;
	int m_iStateReligionPrereq;
	int m_iCaptureUnitClass;
	int m_iVisibilityChange;
	int m_iMovesChange;
	int m_iMoveDiscountChange;
	int m_iAirRangeChange;
	int m_iInterceptChange;
	int m_iEvasionChange;
	int m_iWithdrawalChange;
	int m_iEnemyWithdrawalChange;
	int m_iCargoChange;
	int m_iCollateralDamageChange;
	int m_iBombardRateChange;
	int m_iFirstStrikesChange;
	int m_iChanceFirstStrikesChange;
	int m_iEnemyHealChange;
	int m_iNeutralHealChange;
	int m_iFriendlyHealChange;
	int m_iSameTileHealChange;
	int m_iAdjacentTileHealChange;
	int m_iCombatPercent;
	int m_iCityAttackPercent;
	int m_iCityDefensePercent;
	int m_iHillsAttackPercent;
	int m_iHillsDefensePercent;
	int m_iCommandType;
	int m_iRevoltProtection;
	int m_iCollateralDamageProtection;
	int m_iPillageChange;
	int m_iUpgradeDiscount;
	int m_iExperiencePercent;
	int m_iKamikazePercent;
	//Magic Rework
	int m_iMagicalPower;
	int m_iMinMagicalPower;
	//	bool m_iDominionCapacity;

	bool m_bLeader;
	bool m_bBlitz;
	bool m_bAmphib;
	bool m_bRiver;
	bool m_bEnemyRoute;
	bool m_bAlwaysHeal;
	bool m_bHillsDoubleMove;
	bool m_bImmuneToFirstStrikes;
	bool m_bDurationDecreaseSpellpower;
	bool m_bTradeDefender;

	CvString m_szSound;
	int m_iMaxExpReward;
/*************************************************************************************************/
/**	MobileCage								01/28/2010								Valkrionn	**/
/**																								**/
/**										Leashes	a unit to a plot								**/
/*************************************************************************************************/
	int m_iLeashRange;
	int m_iLeashChance;
/*************************************************************************************************/
/**	MobileCage									END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/** Shades					  				07/30/10								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	bool m_bLeveledImmortality;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool m_bNonInfluence;
	bool m_bInfluence;
	int m_iVictoryInfluenceModifier;
	int m_iDefeatInfluenceModifier;
	int m_iPillageInfluenceModifier;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	int m_iExtraPerception;
	int m_iInvisibleLevel;
	bool m_bRevealed;
	/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(PromotionInfos)		05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iCommandLimit;
	int m_iCommandRange;
	int m_iCommandXPShareRate;
	int m_iNumMinionPromotions;
	int* m_piMinionPromotions;
	int m_iNumCapturePromotions;
	int* m_piCapturePromotions;
	int m_iNumCommanderPromotions;
	int* m_piCommanderPromotions;
	int m_iNumSlavePromotions;
	int* m_piSlavePromotions;
	int m_iNumMasterPromotions;
	int* m_piMasterPromotions;
	CvString m_szPyOnRemove;
/*************************************************************************************************/
/**	Promotion PyHelp		 				07/09/10								Valkrionn	**/
/**																								**/
/**							Allows promotions to have dynamic help								**/
/*************************************************************************************************/
	CvString m_szPyHelp;
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/
	bool m_bCommunalProperty;
	bool m_bNeverHostile;
	bool m_bBlind;
	bool m_bOverrideHelpText;
	bool m_bRequirePermission;
	bool m_bCannotCast;
	bool m_bFreeUnit;
	bool m_bNoSupply;
	bool m_bTerritorial;
	bool m_bRivalTerritoryExplore;
	bool m_bRivalTerritoryBlock;
	bool m_bPillageOnMove;
	bool m_bSelfPillage;
	bool m_bGetCasterXP;
	bool m_bNonWarWeariness;
	bool m_bNoMapReveal;
	bool m_bCannotCapture;
	bool m_bCityHappy;
	bool m_bCityNoHappy;
	bool m_bNoSupport;
	bool m_bCanPillage;
	bool m_bCannotPillage;
	bool m_bCitySpy;
	bool m_bStartGoldenAge;
	bool m_bNoDefenseBonus;
	bool m_bMoveImpassable;
	bool m_bClimbPeaks;
	bool m_bFlatMoveCost;
	bool m_bIgnoreTerrainCosts;
	bool m_bAttackNoWar;
	bool m_bAllowAttacks;
	bool m_bFirstStrikeVulnerable;
	bool m_bAllowDefenseBonuses;
	bool m_bNonAbandon;
	bool m_bIndependant;
	bool m_bReligiousCommanderPromo; //ReligiousCommander by BI 07/24/11
	bool m_bEffectProm;
	bool m_bStackEffect;
	bool m_bAutoAcquire;
	bool m_bMustMaintain;
	bool m_bPrereqInCity;
	bool m_bNoXP;
	bool m_bPrereqInBorderEnemy;
	bool m_bPrereqInBorderRival;
	bool m_bPrereqInBorderTeam;
	bool m_bPrereqInBorderSelf;
	bool m_bPrereqInBorderNone;
	bool m_bAllowNULLUnitCombat;

	int m_iRandomApplyChance;
	int m_iAssetValue;
/*************************************************************************************************/
/**	Unit power						17/02/12										Snarko		**/
/**																								**/
/**							Rewriting unit power system											**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iPowerValue;
/**								----  End Original Code  ----									**/
	int m_iPowerAdd;
	int m_iPowerMult;
/*************************************************************************************************/
/**	Unit power						END															**/
/*************************************************************************************************/
	int m_iTempUnitCombat;
	int m_iDamageOnRemove;
	int m_iFreeXPCap;
	float m_fCasterXPRate;
	int m_iDuration;
	int m_iAirCombat;
	int m_iAirCombatLimitBoost;
	int m_iExtraDropRange;
	int m_iPrereqBroadAlignment;
	int m_iAlignmentModifier;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iPrereqBroadEthicalAlignment;
	int m_iEthicalAlignmentModifier;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int m_iSpellExtraRange;
	int m_iCombatConversionChance;
	int m_iCombatUnitGenerationChance;
	int m_iSlaveGenerationChance;
	float m_iGiftableXP;
	int m_iCombatExtraDuration;
	int m_iDurationPerTurn;
	int m_iDurationAlter;
	int m_iChangeDuration;
	int m_iExtraSupport;
	int m_iChanceMiscast;
	int m_iCombatDmgCapBoost;
	int m_iCollateralLimitCap;
	int m_iCollateralLimitBoost;
	int m_iCollateralTargetsLimit;
	int m_iCollateralExtraTargets;

/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	int m_iFlankingLimitBoost;
	int m_iFlankingExtraTargets;
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/

	int m_iHammerSacrifice;
	int m_iExtraHammerPerPop;
	int m_iFoodSacrifice;
	int m_iPopulationAdd;
	int m_iBeakerSacrifice;
	int m_iExtraBeakerPerPop;
	int m_iGoldSacrifice;
	int m_iExtraGoldPerPop;
	int m_iCultureSacrifice;
	int m_iExtraCulturePerPop;
	int m_iPrereqMinAge;
	int m_iPrereqMaxAge;
	int m_iGoldCost;
	int m_iXPTranserRate;
	int m_iPrereqTier;
	int m_iPrereqWeaponTier;
	int m_iNumPromotionExcludes;
	int m_iNumPromotionAllows;
	int m_iNumPromotionReplacedBy;
	int m_iNumPromotionOverwrites;
	int m_iNumPromotionDegradesTo;
	int m_iNumPrereqUnits;
	int m_iNumPrereqReligions;
	int m_iNumPrereqTechANDs;
	int m_iNumPrereqTechORs;
	int m_iNumPrereqAlignments;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iNumPrereqEthicalAlignments;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int m_iNumPrereqFeatures;
	int m_iNumPrereqPlotEffects;
	int m_iNumPrereqTerrains;
	int m_iNumPrereqBonusANDs;
	int m_iNumPrereqBonusORs;
	int m_iNumPrereqCivilizations;
	int m_iNumPrereqCivics;
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
	int m_iNumSecondaryUnitCombats;
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
	int m_iNumPrereqImprovements;
	int m_iNumPrereqBuildingANDs;
	int m_iNumPrereqBuildingORs;
	int m_iNumPrereqCorporations;
	int m_iNumPrereqTraits;
	int m_iNumPrereqEventANDs;
	int m_iNumPrereqEventORs;
	int m_iNumPrereqFeatANDs;
	int m_iNumPrereqFeatORs;
	int m_iNumPrereqFeatNOTs;

	CvString m_szPyPostCombatLost;
	CvString m_szPyPostCombatWon;
/*************************************************************************************************/
/**	PyOnPromoTaken							   08/28/10								Valkrionn	**/
/*************************************************************************************************/
	CvString m_szPyOnPromoTaken;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
	CvString m_szNewName;

	int* m_piYieldFromWin;
	int* m_piYieldForLoss;
	int* m_piCommerceFromWin;
	int* m_piCommerceForLoss;
	int* m_piPromotionExcludes;
	int* m_piPromotionAllows;
	int* m_piPromotionReplacedBy;
	int* m_piPromotionOverwrites;
	int* m_piPromotionDegradesTo;
	int* m_piPrereqUnits;
	int* m_piPrereqReligions;
	int* m_piPrereqTechANDs;
	int* m_piPrereqTechORs;
	int* m_piPrereqAlignments;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int* m_piPrereqEthicalAlignments;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int* m_piPrereqFeatures;
	int* m_piPrereqPlotEffects;
	int* m_piPrereqTerrains;
	int* m_piPrereqBonusANDs;
	int* m_piPrereqBonusORs;
	int* m_piPrereqCivilizations;
	int* m_piPrereqCivics;
/*************************************************************************************************/
/**	Second Job							08/28/10									Valkrionn	**/
/**				Allows units to qualify for the promotions of other UnitCombats					**/
/*************************************************************************************************/
	int* m_piSecondaryUnitCombats;
/*************************************************************************************************/
/**	TempCombat									END												**/
/*************************************************************************************************/
	int* m_piPrereqImprovements;
	int* m_piPrereqBuildingANDs;
	int* m_piPrereqBuildingORs;
	int* m_piPrereqCorporations;
	int* m_piPrereqTraits;
	int* m_piPrereqEventANDs;
	int* m_piPrereqEventORs;
	int* m_piPrereqFeatANDs;
	int* m_piPrereqFeatORs;
	int* m_piPrereqFeatNOTs;

	std::vector<CvString> m_aszPrereqUnitsforPass3;
	std::vector<CvString> m_aszPrereqCivilizationsforPass3;
	std::vector<CvString> m_aszPrereqCivicsforPass3;
	std::vector<CvString> m_aszPrereqImprovementsforPass3;
	std::vector<CvString> m_aszPrereqBuildingANDsforPass3;
	std::vector<CvString> m_aszPrereqBuildingORsforPass3;
	std::vector<CvString> m_aszPrereqCorporationsforPass3;
	std::vector<CvString> m_aszPrereqTraitsforPass3;
	std::vector<CvString> m_aszPrereqEventANDsforPass3;
	std::vector<CvString> m_aszPrereqEventORsforPass3;

	std::vector<int> m_aiInvisibleTypes;
	std::vector<int> m_aiSeeInvisibleTypes;

	int m_iNumCityBonuses;
	std::list <CityBonuses> m_cbCityBonuses;

	int m_iNumAuraBonuses;
	std::list <AuraBonuses> m_cbAuraBonuses;


	int m_iNumPrereqUnitTypesOnTile;
	int* m_piPrereqUnitTypesOnTile;
	std::vector<CvString> m_aszPrereqUnitTypesOnTileforPass3;
	int m_iNumPrereqUnitTypesNOTOnTile;
	int* m_piPrereqUnitTypesNOTOnTile;
	std::vector<CvString> m_aszPrereqUnitTypesNOTOnTileforPass3;
/*************************************************************************************************/
/**	Workers Paradise						01/08/10											**/
/**																								**/
/**							Allows promotions to affect build orders							**/
/*************************************************************************************************/
	int m_iNumPromotionBuilds;
	int* m_piPromotionBuilds;
	std::vector<CvString> m_aszPromotionBuildsforPass3;
	int m_iNumPromotionCannotBuilds;
	int* m_piPromotionCannotBuilds;
	std::vector<CvString> m_aszPromotionCannotBuildsforPass3;
/*************************************************************************************************/
/**	Workers Paradise						END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	int m_iNumAffinities;
	int* m_piAffinities;
	std::vector<CvString> m_aszAffinitiesforPass3;
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
	int m_iNumPrereqUnitClassesOnTile;
	int* m_piPrereqUnitClassesOnTile;
	int m_iNumPrereqUnitClassesNOTOnTile;
	int* m_piPrereqUnitClassesNOTOnTile;
	int m_iNumPrereqPromotionsOnTile;
	int* m_piPrereqPromotionsOnTile;
	int m_iNumPrereqPromotionsNOTOnTile;
	int* m_piPrereqPromotionsNOTOnTile;
	int m_iNoBadExplore;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH: Added by Kael 07/30/2007
	bool m_bEnraged;
	bool m_bBoarding;
	bool m_bOnlyDefensive;
	bool m_bDispellable;
	int m_iPrereqDispelPower;
	bool m_bDoubleFortifyBonus;
	bool m_bEquipment;
	bool m_bFear;
	bool m_bFlying;
	bool m_bPrereqAliveCapture;
	bool m_bHeld;
	bool m_bHiddenNationality;
	bool m_bIgnoreBuildingDefense;
	bool m_bImmortal;
	bool m_bImmuneToCapture;
	bool m_bImmuneToDefensiveStrike;
	bool m_bImmuneToFear;
	bool m_bImmuneToMagic;
	bool m_bInvisible;
	bool m_bMutation;
/*************************************************************************************************/
/**	Dynamic Mutation						06/15/10								Valkrionn	**/
/**																								**/
/**							New tags used by the Dynamic Mutation system						**/
/*************************************************************************************************/
	int m_iMutationWeight;
	int m_iMutationMin;
	int m_iMutationMax;
	int m_iMutationMaxApplications;
	bool m_bBadEffect;
/*************************************************************************************************/
/**	DynamicMutation								END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	1.4										03/28/11								Valkrionn	**/
/**																								**/
/**									New tags required for 1.4									**/
/*************************************************************************************************/
	int m_iMaxApplications;
	int* m_piUnitCombat;
	int* m_piExtraSpellClassPower;
	int** m_piiPrereqPromotionORs;
	int** m_piiPrereqPromotionANDs;
	int m_iNumPrereqPromotionORs;
	int m_iNumPrereqPromotionANDs;
	int** m_piiPromotionCombatMods;
	int m_iNumPromotionCombatMods;
	int m_iAntiWithdrawal;
	int m_iAntiFirstStrikes;
	int m_iRangedCombatPercent;
	int m_iRangedCombatPercentGlobalCounter;
	int m_iRangedCombatPercentInBorders;
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/
	bool m_bNotAlive;
	bool m_bPrereqAlive;
	bool m_bPrereqRevealed;
	bool m_bPrereqHidden;
	bool m_bRace;
	bool m_bMentalEffect;
	bool m_bCompanion;
	bool m_bGraphicalAddOnPromotion;
	bool m_bRemovedByCasting;
	bool m_bRemovedByCombat;
	bool m_bRemovedWhenHealed;
/*************************************************************************************************/
/**	BeenThereDoneThat						04/04/09								Xienwolf	**/
/**																								**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	bool m_bSeeInvisible;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	BeenThereDoneThat						END													**/
/*************************************************************************************************/
	bool m_bTargetWeakestUnit;
	bool m_bTargetWeakestUnitCounter;
	int m_iMulticast;
	bool m_bValidate;
	bool m_bWaterWalking;
	int m_iAIWeight;
	int m_iBetrayalChance;
	int m_iBetterDefenderThanPercent;
	int m_iCasterResistModify;
	int m_iCombatCapturePercent;
	int m_iCombatHealPercent;
	int m_iCombatLimit;
	int m_iCombatPercentDefense;
	int m_iCombatPercentGlobalCounter;
	int m_iCombatPercentInBorders;
	int m_iDefensiveStrikeChance;
	int m_iDefensiveStrikeDamage;
	int m_iExpireChance;
	int m_iExtraCombatStr;
	int m_iExtraCombatDefense;
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/**									Useless field skipped										**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iFreeXPPerTurn;
	int m_iFreeXPFromCombat;
	int m_iGoldFromCombat;
/**								----  End Original Code  ----									**/
	float m_iFreeXPPerTurn;
	float m_iFreeXPFromCombat;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int m_iGroupSize;
	int m_iMinLevel;
/*************************************************************************************************/
/**	PrereqStrBoostSize						10/16/09								Valkrionn	**/
/**																								**/
/**					Allows a units StrBoost to be used as a promotion prereq					**/
/*************************************************************************************************/
	int m_iPrereqStrBoostSize;
/*************************************************************************************************/
/**	PrereqStrBoostSize							END												**/
/*************************************************************************************************/
	int m_iModifyGlobalCounter;
	int m_iModifyGlobalCounterOnCombat;
	int m_iResistMagic;
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
	float m_iSpellCasterXP;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int m_iSpellDamageModify;
	int m_iWorkRateModify;
	int m_iWorkRateModifier;
	int m_iCaptureUnitCombat;
	int m_iBlockedSpellClass;
	int m_iPromotionCombatApply;
/*************************************************************************************************/
/**	Cutting								30/01/12										Snarko	**/
/**																								**/
/**				Removing rarely used/redundant stuff to improve speed.							**/
/**			Use PromotionExcludes instead, both faster and more flexible						**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iPromotionImmune1;
	int m_iPromotionImmune2;
	int m_iPromotionImmune3;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Cutting									END													**/
/*************************************************************************************************/
	int m_iPromotionRandomApply;
	int m_iPromotionSummonPerk;
	int m_iBonusPrereq;
	int m_iPromotionPrereqOr3;
	int m_iPromotionPrereqOr4;
	int m_iPromotionPrereqAnd;
	int m_iUnitReligionPrereq; //PrereqUnitReligion by BI 07/24/11
	int m_iPromotionNextLevel;
	CvString m_szPyPerTurn;
	CvString m_szExtraArtType;
	CvString m_szReplaceArtType;
	int m_iUnitArtStyleType;
	int m_iPromotionCombatType;
	int m_iPromotionCombatMod;
	//ReligionCombatBonus by BI 07/25/11
	int m_iReligionCombatType;
	int m_iReligionCombatMod;
/*************************************************************************************************/
/**	MISSION_INQUISITION						13/01/12									Snarko	**/
/**																								**/
/**			Adding a mission for inquisition and teaching the AI proper use						**/
/*************************************************************************************************/
	bool m_bInquisition;
/*************************************************************************************************/
/**	MISSION_INQUISITION END																		**/
/*************************************************************************************************/



	int* m_piBonusAffinity;
	int* m_piDamageTypeCombat;
	int* m_piDamageTypeResist;
//FfH: End Add

	// Arrays
	int* m_piNoBadExploreImprovement;
	std::vector<CvString> m_aszNoBadExploreImprovementsforPass3;
	std::vector<int> m_aiNoBadExploreImprovementsforPass3;

	int* m_piTerrainAttackPercent;
	int* m_piTerrainDefensePercent;
	int* m_piFeatureAttackPercent;
	int* m_piFeatureDefensePercent;
	int* m_piPlotEffectAttackPercent;
	int* m_piPlotEffectDefensePercent;
/*************************************************************************************************/
/**	GWS										2010-08-23									Milaga	**/
/**																								**/
/**					Units can have movement modifiers for different terrain						**/
/*************************************************************************************************/
// CvPromotionInfo Protected
	int m_iPromotionHillCost;
	int m_iPromotionPeakCost;
	int* m_piPromotionTerrainCost;
	int* m_piPromotionFeatureCost;
/*************************************************************************************************/
/**	GWS										END													**/
/*************************************************************************************************/
	int* m_piUnitCombatModifierPercent;
	// Upgraded Capture rate  by BI 06/18/11
	int* m_piUnitCombatCaptureRatePercent;
	bool* m_pbUnitCombatNonCapture;

	int* m_piDomainModifierPercent;

	bool* m_pbTerrainDoubleMove;
	bool* m_pbFeatureDoubleMove;
	bool* m_pbPlotEffectDoubleMove;
	//PromotionClass
	PromotionClassTypes m_iPromotionClass;
	SpecialUnitTypes m_iSpecialCargo;
	DomainTypes m_iDomainCargo;
	PromotionClassTypes m_iPromotionClassOverwrite;

};

//FfH Spell System: Added by Kael 07/23/2007
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpellInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpellInfo :	public CvHotkeyInfo
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:
	DllExport CvSpellInfo();
	DllExport virtual ~CvSpellInfo();

/*************************************************************************************************/
/**	City Actions	(SpellInfos)			03/28/10								Grey Fox	**/
/*************************************************************************************************/
	bool isCityAction() const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	DllExport int getPromotionPrereq1() const;
	DllExport int getPromotionPrereq2() const;
	int getUnitPrereq() const;
	int getUnitCombatPrereq() const;
	int getUnitClassPrereq() const;
	int getUnitInStackPrereq() const;
	int getUnitInStackTargetPrereq() const;
	int getBuildingPrereq() const;
	int getBuildingTargetPrereq() const;
	int getBuildingClassPrereq() const;
	int getBuildingClassTargetPrereq() const;
	int getBuildingClassOwnedPrereq() const;
	int getCivilizationPrereq() const;
	int getCorporationPrereq() const;
	int getCorporationTargetPrereq() const;
	int getFeatureOrPrereq1() const;
	int getFeatureOrPrereq2() const;
	int getFeatureOrTargetPrereq1() const;
	int getFeatureOrTargetPrereq2() const;
	int getImprovementPrereq() const;
	int getImprovementTargetPrereq() const;
	int getPlotEffectPrereq() const;
	int getPlotEffectTargetPrereq() const;
	int getPromotionInStackPrereq() const;
	int getPromotionInStackTargetPrereq() const;
	int getReligionPrereq() const;
	int getStateReligionPrereq() const;
	int getTechPrereq() const;
	int getPrereqCivic() const;
	int getPrereqTrait(int iI) const;
	int getNumPrereqTraits() const;
	CvString getPrereqTraitsVectorElement(int i);
	int getNumPromotionsPrereq() const;
	int getPromotionPrereq(int iI) const;
	
	int getNumTargetPromotionsPrereq() const;
	int getTargetPromotionPrereq(int iI) const;

	int getNumAddPromotions() const;
	int getAddPromotion(int iI) const;
	CvString getAddPromotionsVectorElement(int i);

	int getNumRemovePromotions() const;
	int getRemovePromotion(int iI) const;
	CvString getRemovePromotionsVectorElement(int i);

	int getNumSpellBonuses() const;
	SpellBonuses getSpellBonus(int iI) const;
	std::list<SpellBonuses> listSpellBonuses();

/*************************************************************************************************/
/**	New Tag Defs	(SpellInfos)			05/15/08								Xienwolf	**/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	bool isPrereqNotAttacked() const;
	bool isSetHasAttacked() const;
	bool isRemoveHasAttacked() const;
	const char* getPythonHelp() const;
	bool isPrereqAvailableCommander() const;
	bool isPrereqIsNOTMinion() const;
	bool isPrereqIsMinion() const;
	int getPrereqBroadAlignment() const;
	int getAlignmentModifier() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getPrereqBroadEthicalAlignment() const;
	int getEthicalAlignmentModifier() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	bool isSummonMaster() const;
	int getPromotionDuration() const;
	const TCHAR* getQuote() const;
	void copyNonDefaults(CvSpellInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int getRange() const;
	int getTargetRange() const;
	int getEffect() const;
	int getAIWeight() const;
	int getCasterMinLevel() const;
	int getChangePopulation() const;
	int getCost() const;
	int getNumTargets() const;
	int getCrimePrereq() const;
	int getDamage() const;
	int getDamageLimit() const;
	int getDamageType() const;
	int getDelay() const;
	int getCreateUnitNum() const;
	int getCreateUnitDuration() const;
	int getAddPromotionType1() const;
	int getAddPromotionType2() const;
	int getAddPromotionType3() const;
	int getConvertUnitType() const;
	int getCreateBuildingType() const;
	int getCreateFeatureType() const;
	int getCreatePlotEffectType() const;
	int getRemovePlotEffectType() const;
	int getCreateImprovementType() const;
	int getSpreadReligion() const;
	int getImmobileTurns() const;
	int getFortifyTurns() const;
	int getMiscastChance() const;
	int getRemovePromotionType1() const;
	int getRemovePromotionType2() const;
	int getRemovePromotionType3() const;
	int getResistModify() const;
	int getCreateUnitPromotion() const;
	int getCreateUnitType() const;
	bool isAllowAI() const;
	bool isAdjacentToWaterOnly() const;
	bool isTargetAdjacentToWaterOnly() const;
	bool isCasterMustBeAlive() const;
	bool isCasterNoDuration() const;
	bool isCausesWar() const;
	bool isCopyCastersPromotions() const;
	bool isGlobal() const;
	bool isInBordersOnly() const;
	bool isInCityOnly() const;
	bool isTargetInBordersOnly() const;
	bool isTargetInCityOnly() const;
	bool isPrereqSlaveTrade() const;
	bool isBuffCasterOnly() const;
	bool isAbility() const;
	bool isDispel() const;
	bool isDisplayWhenDisabled() const;
	bool isHasCasted() const;
	bool isIgnoreHasCasted() const;
	bool isImmuneTeam() const;
	bool isImmuneNeutral() const;
	bool isImmuneEnemy() const;
	bool isImmuneFlying() const;
	bool isImmuneNotAlive() const;
	bool isTargetSummon() const;
	bool isPermanentUnitCreate() const;
	bool isPush() const;
	bool isRemoveHasCasted() const;
	bool isResistable() const;
	bool isSacrificeCaster() const;
/*************************************************************************************************/
/**	AutoCast								24/05/10									Snarko	**/
/**																								**/
/**						Making the human able to set units to autocast spells					**/
/*************************************************************************************************/
	bool isAutoCast() const;
/*************************************************************************************************/
/**	AutoCast								END													**/
/*************************************************************************************************/
	//TargetedSpell 0924 blackimp
	bool isTargeted() const;

	const TCHAR* getSound() const;
	DllExport const TCHAR* getPyMiscast() const;
	DllExport const TCHAR* getPyResult() const;
	DllExport const TCHAR* getPyRequirement() const;
	int getCommandType() const;
	void setCommandType(int iNewType);
	//Magic Rework
	int getMagicalPowerPrereq() const;
	bool isSpellClass(int i) const;

	DllExport void read(FDataStreamBase* stream);
	DllExport void write(FDataStreamBase* stream);
	DllExport bool read(CvXMLLoadUtility* pXML);
	DllExport bool readPass3();
//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iAIWeight;
	int m_iCasterMinLevel;

/*************************************************************************************************/
/**	City Actions	(SpellInfos)			03/28/10								Grey Fox	**/
/*************************************************************************************************/
	bool m_bCityAction;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/

	int m_iPromotionPrereq1;
	int m_iPromotionPrereq2;
	int m_iUnitPrereq;
	int m_iUnitCombatPrereq;
	int m_iUnitClassPrereq;
	int m_iUnitInStackPrereq;
	int m_iUnitInStackTargetPrereq;
	int m_iBuildingPrereq;
	int m_iBuildingTargetPrereq;
	int m_iBuildingClassPrereq;
	int m_iBuildingClassTargetPrereq;
	int m_iBuildingClassOwnedPrereq;
	int m_iCivilizationPrereq;
	int m_iCorporationPrereq;
	int m_iCorporationTargetPrereq;
	int m_iFeatureOrPrereq1;
	int m_iFeatureOrPrereq2;
	int m_iFeatureOrTargetPrereq1;
	int m_iFeatureOrTargetPrereq2;
	int m_iPlotEffectPrereq;
	int m_iPlotEffectTargetPrereq;
	int m_iImprovementPrereq;
	int m_iImprovementTargetPrereq;
	int m_iPromotionInStackPrereq;
	int m_iPromotionInStackTargetPrereq;
	int m_iReligionPrereq;
	int m_iStateReligionPrereq;
	int m_iTechPrereq;
	int m_iPrereqCivic;
	int m_iNumPrereqTraits;
	int* m_piPrereqTraits;
	std::vector<CvString> m_aszPrereqTraitsforPass3;
	int m_iNumPromotionsPrereq;
	int* m_piPromotionsPrereq;
	int m_iNumTargetPromotionsPrereq;
	int* m_piTargetPromotionsPrereq;
	int* m_piAddPromotions;
	int m_iNumAddPromotions;
	std::vector<CvString> m_aszAddPromotionsforPass3;
	int* m_piRemovePromotions;
	int m_iNumRemovePromotions;
	std::vector<CvString> m_aszRemovePromotionsforPass3;
	int m_iNumSpellBonuses;
	std::list <SpellBonuses> m_cbSpellBonuses;

/*************************************************************************************************/
/**	New Tag Defs	(SpellInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	bool m_bPrereqNotAttacked;
	bool m_bSetHasAttacked;
	bool m_bRemoveHasAttacked;
	CvString m_szPyHelp;
	int m_bPrereqAvailableCommander;
	int m_bPrereqIsNOTMinion;
	int m_bPrereqIsMinion;
	int m_iPrereqBroadAlignment;
	int m_iAlignmentModifier;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iPrereqBroadEthicalAlignment;
	int m_iEthicalAlignmentModifier;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int m_bSummonMaster;
	int m_iPromotionDuration;
	CvString m_szQuote;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	bool m_bAllowAI;
	bool m_bAdjacentToWaterOnly;
	bool m_bTargetAdjacentToWaterOnly;
	bool m_bCasterMustBeAlive;
	bool m_bCasterNoDuration;
	bool m_bCausesWar;
	bool m_bGlobal;
	bool m_bInBordersOnly;
	bool m_bInCityOnly;
	bool m_bTargetInBordersOnly;
	bool m_bTargetInCityOnly;
	bool m_bPrereqSlaveTrade;
	bool m_bResistable;
	bool m_bDisplayWhenDisabled;
	bool m_bHasCasted;
	bool m_bIgnoreHasCasted;
	int m_iDamage;
	int m_iDamageLimit;
	int m_iDamageType;
	int m_iDelay;
	int m_iRange;
	int m_iTargetRange;
	int m_iResistModify;
	int m_iAddPromotionType1;
	int m_iAddPromotionType2;
	int m_iAddPromotionType3;
	int m_iRemovePromotionType1;
	int m_iRemovePromotionType2;
	int m_iRemovePromotionType3;
	bool m_bBuffCasterOnly;
	int m_iConvertUnitType;
	int m_iCreateBuildingType;
	int m_iCreateFeatureType;
	int m_iCreatePlotEffectType;
	int m_iRemovePlotEffectType;
	int m_iCreateImprovementType;
	int m_iSpreadReligion;
	int m_iCreateUnitNum;
	int m_iCreateUnitDuration;
	int m_iCreateUnitPromotion;
	int m_iCreateUnitType;
	bool m_bCopyCastersPromotions;
	bool m_bPermanentUnitCreate;
	bool m_bImmuneTeam;
	bool m_bImmuneNeutral;
	bool m_bImmuneEnemy;
	bool m_bImmuneFlying;
	bool m_bImmuneNotAlive;
	bool m_bTargetSummon;
	bool m_bAbility;
	bool m_bDispel;
	bool m_bPush;
	bool m_bRemoveHasCasted;
	bool m_bSacrificeCaster;
	int m_iChangePopulation;
	int m_iCost;
	int m_iNumTargets;
	int m_iCrimePrereq;
	int m_iImmobileTurns;
	int m_iFortifyTurns;
	int m_iMiscastChance;
	int m_iEffect;
	int m_iCommandType;
/*************************************************************************************************/
/**	AutoCast								24/05/10									Snarko	**/
/**																								**/
/**						Making the human able to set units to autocast spells					**/
/*************************************************************************************************/
	bool m_bAutoCast;
/*************************************************************************************************/
/**	Autocast								END													**/
/*************************************************************************************************/
	//TargetedSpell 0924 blackimp
	bool m_bTargeted;
	CvString m_szPyMiscast;
	CvString m_szPyResult;
	CvString m_szPyRequirement;
	CvString m_szSound;
	//Magic Rework
	int m_iMagicalPowerPrereq;
	bool* m_pbSpellClass;

};
//FfH: End Add

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvMissionInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvMissionInfo : public CvHotkeyInfo
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvMissionInfo();
	DllExport virtual ~CvMissionInfo();

	DllExport int getTime() const;								// Exposed to Python
	DllExport int getGoldCost() const;							// Exposed to Python

	DllExport bool isSound() const;								// Exposed to Python
	DllExport bool isTarget() const;							// Exposed to Python
	DllExport bool isBuild() const;								// Exposed to Python
	DllExport bool getVisible() const;						// Exposed to Python
	DllExport EntityEventTypes getEntityEvent() const;

	DllExport const TCHAR* getWaypoint() const;		// effect type, Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvMissionInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iTime;
	int m_iGoldCost;

	bool m_bSound;
	bool m_bTarget;
	bool m_bBuild;
	bool m_bVisible;
	EntityEventTypes m_eEntityEvent;

	CvString m_szWaypoint;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvControlInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvControlInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvControlInfo();
	DllExport virtual ~CvControlInfo();

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvControlInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCommandInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCommandInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvCommandInfo();
	DllExport virtual ~CvCommandInfo();

	DllExport int getAutomate() const;
	DllExport void setAutomate(int i);

	DllExport bool getConfirmCommand() const;
	DllExport bool getVisible() const;
	DllExport bool getAll() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvCommandInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
	int m_iAutomate;

	bool m_bConfirmCommand;
	bool m_bVisible;
	bool m_bAll;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAutomateInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAutomateInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvAutomateInfo();
	DllExport virtual ~CvAutomateInfo();

	DllExport int getCommand() const;
	DllExport void setCommand(int i);
	DllExport int getAutomate() const;
	DllExport void setAutomate(int i);

	DllExport bool getConfirmCommand() const;
	DllExport void setConfirmCommand(bool bVal);
	DllExport bool getVisible() const;
	DllExport void setVisible(bool bVal);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvAutomateInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
	int m_iCommand;
	int m_iAutomate;

	bool m_bConfirmCommand;
	bool m_bVisible;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvActionInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvActionInfo
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvActionInfo();
	DllExport virtual ~CvActionInfo();

	DllExport int getMissionData() const;				// Exposed to Python
	DllExport int getCommandData() const;				// Exposed to Python

	DllExport int getAutomateType() const;
	DllExport int getInterfaceModeType() const;				// Exposed to Python
	DllExport int getMissionType() const;				// Exposed to Python
	DllExport int getCommandType() const;				// Exposed to Python
	DllExport int getControlType() const;				// Exposed to Python
	DllExport int getOriginalIndex() const;
	DllExport void setOriginalIndex(int i);

	DllExport bool isConfirmCommand() const;				// Exposed to Python
	DllExport bool isVisible() const;				// Exposed to Python
	DllExport ActionSubTypes getSubType() const;
	DllExport void setSubType(ActionSubTypes eSubType);

	// functions to replace the CvInfoBase calls
	DllExport const TCHAR* getType() const;
	DllExport const wchar* getDescription() const;
	DllExport const wchar* getCivilopedia() const;
	DllExport const wchar* getHelp() const;
	DllExport const wchar* getStrategy() const;
	DllExport virtual const TCHAR* getButton() const;
	DllExport const wchar* getTextKeyWide() const;

	// functions to replace the CvHotkey calls
	DllExport int getActionInfoIndex() const;
	DllExport int getHotKeyVal() const;
	DllExport int getHotKeyPriority() const;
	DllExport int getHotKeyValAlt() const;
	DllExport int getHotKeyPriorityAlt() const;
	DllExport int getOrderPriority() const;

	DllExport bool isAltDown() const;
	DllExport bool isShiftDown() const;
	DllExport bool isCtrlDown() const;
	DllExport bool isAltDownAlt() const;
	DllExport bool isShiftDownAlt() const;
	DllExport bool isCtrlDownAlt() const;

	DllExport const TCHAR* getHotKey() const;			// Exposed to Python

	DllExport std::wstring getHotKeyDescription() const;	// Exposed to Python

//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iOriginalIndex;
	ActionSubTypes m_eSubType;

private:
	CvHotkeyInfo* getHotkeyInfo() const;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvUnitInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoUnit;
class CvUnitInfo : public CvHotkeyInfo
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:
	CvUnitInfo();
	virtual ~CvUnitInfo();

	int getAIWeight() const;				// Exposed to Python
	int getProductionCost() const;				// Exposed to Python
/*************************************************************************************************/
/**	WeightedCost							 1/30/2010								Valkrionn	**/
/**																								**/
/**								Modifies Cost based on Population								**/
/*************************************************************************************************/
	int getCityPopCostModifier() const;				// Exposed to Python
	int getEmpirePopCostModifier() const;			// Exposed to Python
	int getNumCityCostModifier() const;				// Exposed to Python
	int getPlayerPopCostModifier() const;			// Exposed to Python
/*************************************************************************************************/
/**	WeightedCost								END												**/
/*************************************************************************************************/
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool isNonInfluence() const;						// Exposed to Python
	bool isInfluence() const;							// Exposed to Python
	int getVictoryInfluenceModifier() const;			// Exposed to Python
	int getDefeatInfluenceModifier() const;				// Exposed to Python
	int getPillageInfluenceModifier() const;			// Exposed to Python
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int getHurryCostModifier() const;				// Exposed to Python
	int getAdvancedStartCost() const;				// Exposed to Python
	int getAdvancedStartCostIncrease() const;				// Exposed to Python
	int getMinAreaSize() const;				// Exposed to Python
	int getMoves() const;				// Exposed to Python
	int getAirRange() const;				// Exposed to Python
	int getAirUnitCap() const;				// Exposed to Python
	int getDropRange() const;				// Exposed to Python
	int getNukeRange() const;				// Exposed to Python
	int getWorkRate() const;				// Exposed to Python
	int getBaseDiscover() const;		// Exposed to Python
	int getDiscoverMultiplier() const;		// Exposed to Python
	int getBaseHurry() const;				// Exposed to Python
	int getHurryMultiplier() const;				// Exposed to Python
	int getBaseTrade() const;				// Exposed to Python
	int getTradeMultiplier() const;				// Exposed to Python
	int getGreatWorkCulture() const;				// Exposed to Python
	int getEspionagePoints() const;				// Exposed to Python
	int getCombat() const;				// Exposed to Python
	void setCombat(int iNum);				// Exposed to Python
	int getCombatLimit() const;				// Exposed to Python
	int getAirCombat() const;				// Exposed to Python
	int getAirCombatLimit() const;				// Exposed to Python
	int getXPValueAttack() const;				// Exposed to Python
	int getXPValueDefense() const;				// Exposed to Python
	int getFirstStrikes() const;				// Exposed to Python
	int getChanceFirstStrikes() const;				// Exposed to Python
	int getInterceptionProbability() const;		// Exposed to Python
	int getEvasionProbability() const;				// Exposed to Python
	int getWithdrawalProbability() const;			// Exposed to Python
	int getEnemyWithdrawalProbability() const;			// Exposed to Python
	int getCollateralDamage() const;					// Exposed to Python
	int getCollateralDamageLimit() const;			// Exposed to Python
	int getCollateralDamageMaxUnits() const;	// Exposed to Python

/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	int getFlankingDamage() const;					// Exposed to Python
	int getFlankingDamageLimit() const;			// Exposed to Python
	int getFlankingDamageMaxUnits() const;	// Exposed to Python
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/
	int getCityAttackModifier() const;				// Exposed to Python
	int getCityDefenseModifier() const;				// Exposed to Python
	int getAnimalCombatModifier() const;			// Exposed to Python
	int getHillsAttackModifier() const;			// Exposed to Python
	int getHillsDefenseModifier() const;			// Exposed to Python
	int getBombRate() const;									// Exposed to Python
	int getBombardRate() const;								// Exposed to Python
	int getSpecialCargo() const;							// Exposed to Python
	int getDomainCargo() const;								// Exposed to Python

	int getCargoSpace() const;								// Exposed to Python
	int getConscriptionValue() const;					// Exposed to Python
	int getCultureGarrisonValue() const;			// Exposed to Python
	int getExtraCost() const;									// Exposed to Python
	int getAssetValue() const;								// Exposed to Python
/*************************************************************************************************/
/**	Unit power						17/02/12										Snarko		**/
/**																								**/
/**							Rewriting unit power system											**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getPowerValue() const;								// Exposed to Python
/**								----  End Original Code  ----									**/
	int getPowerAdd() const;								// Exposed to Python
	int getPowerMult() const;								// Exposed to Python
/*************************************************************************************************/
/**	Unit power						END															**/
/*************************************************************************************************/
	int getUnitClassType() const;							// Exposed to Python
	int getSecondaryUnitClassType() const;							// Exposed to Python
	int getSpecialUnitType() const;						// Exposed to Python
	int getUnitCaptureClassType() const;			// Exposed to Python
	int getUnitCombatType() const;						// Exposed to Python
	int getDomainType() const;								// Exposed to Python
	int getDefaultUnitAIType() const;					// Exposed to Python
/*************************************************************************************************/
/**	CandyMan								04/04/09								Xienwolf	**/
/**																								**/
/**							Allows Multiple Invisible types on a Unit							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getInvisibleType() const;							// Exposed to Python
/**								----  End Original Code  ----									**/
	int getInvisibleType(int i) const;					// Exposed to Python
	int getNumInvisibleTypes() const;					// Exposed to Python
/*************************************************************************************************/
/**	CandyMan								END													**/
/*************************************************************************************************/
	int getSeeInvisibleType(int i) const;					// Exposed to Python
	int getNumSeeInvisibleTypes() const;					// Exposed to Python
	int getAdvisorType() const;								// Exposed to Python
	int getHolyCity() const;									// Exposed to Python
	int getReligionType() const;							// Exposed to Python
	int getStateReligion() const;							// Exposed to Python
	int getPrereqReligion() const;						// Exposed to Python
	int getPrereqCorporation() const;						// Exposed to Python
	int getPrereqBuilding() const;						// Exposed to Python
	int getPrereqAndTech() const;							// Exposed to Python
	int getPrereqAndBonus() const;						// Exposed to Python
	int getGroupSize() const;									// Exposed to Python - the initial number of individuals in the unit group
	int getGroupDefinitions() const;					// Exposed to Python - the number of UnitMeshGroups for this unit
	int getMeleeWaveSize() const;							// Exposed to Python
	int getRangedWaveSize() const;						// Exposed to Python
	int getNumUnitNames() const;							// Exposed to Python
	int getCommandType() const;								// Exposed to Python
	void setCommandType(int iNewType);

	bool isAnimal() const;				// Exposed to Python
	bool isFoodProduction() const;				// Exposed to Python
	bool isNoBadGoodies() const;				// Exposed to Python
	bool isOnlyDefensive() const;				// Exposed to Python
	bool isCannotCapture() const;				// Exposed to Python
	bool isImmuneToCapture() const;				// Exposed to Python
	bool isQuickCombat() const;				// Exposed to Python
	bool isRivalTerritory() const;				// Exposed to Python
	bool isMilitaryHappiness() const;				// Exposed to Python
	bool isMilitarySupport() const;				// Exposed to Python
	bool isMilitaryProduction() const;				// Exposed to Python
	bool isPillage() const;				// Exposed to Python
	bool isReligiousCommander() const;				// Exposed to Python  ReligiousCommander by BI 07/24/11
	bool isSpy() const;				// Exposed to Python
	bool isSabotage() const;				// Exposed to Python
	bool isDestroy() const;				// Exposed to Python
	bool isStealPlans() const;				// Exposed to Python
	bool isInvestigate() const;				// Exposed to Python
	bool isCounterSpy() const;				// Exposed to Python
	bool isFound() const;				// Exposed to Python
	bool isGoldenAge() const;				// Exposed to Python
	bool isInvisible() const;				// Exposed to Python
	void setInvisible(bool bEnable) ;			// Exposed to Python
	bool isFirstStrikeImmune() const;				// Exposed to Python
	bool isNoDefensiveBonus() const;				// Exposed to Python
	bool isIgnoreBuildingDefense() const;				// Exposed to Python
	bool isCanMoveImpassable() const;				// Exposed to Python
	bool isCanMoveAllTerrain() const;				// Exposed to Python
	bool isFlatMovementCost() const;				// Exposed to Python
	bool isIgnoreTerrainCost() const;				// Exposed to Python
	bool isNukeImmune() const;				// Exposed to Python
	bool isPrereqBonuses() const;				// Exposed to Python
	bool isPrereqReligion() const;				// Exposed to Python
	bool isMechUnit() const;							// Exposed to Python
	bool isRenderBelowWater() const;			// Exposed to Python
	bool isRenderAlways() const;			// Exposed to Python
	bool isSuicide() const;			// Exposed to Python
	bool isHiddenNationality() const;			// Exposed to Python
	bool isAlwaysHostile() const;			// Exposed to Python
	bool isNoRevealMap() const;			// Exposed to Python

	float getUnitMaxSpeed() const;					// Exposed to Python
	float getUnitPadTime() const;					// Exposed to Python

/*************************************************************************************************/
/**	New Tag Defs	(UnitInfos)				05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getCommandLimit() const;
	int getCommandRange() const;
	bool isFreeUnit() const;
	bool isNoSupply() const;
	bool isNeverHostile() const;
	bool isCommunalProperty() const;
	bool isBlind() const;
	bool isJoinPop() const;
	int getPrereqBroadAlignment() const;
	int getAlignmentModifier() const;
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	int getAlignmentShift() const;
	int getAlignmentShiftModifier() const;
	int getAlignmentShiftTowardsNeutral() const;
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
	const TCHAR* getPyPerTurn() const;
	int getYieldFromKill(int i) const;
	int getCommerceFromKill(int i) const;
	bool isCanClimbPeaks() const;				// Exposed to Python
	bool isAllowPromotion(PromotionTypes eIndex) const;
	bool isDenyPromotion(PromotionTypes eIndex) const;
	const TCHAR* getPyDeath() const;
	int getNumQuotes() const;
	const TCHAR* getQuotes(int i) const;
	const TCHAR* getQuote() const;
	int getNumImages() const;
	const TCHAR* getImages(int i) const;
	int getUpgradeCivVectorSize();
	CvString getUpgradeCivVectorElement(int i);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/** Feral Animals			  				10/19/09								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	int getAppearanceProb() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Units: Added by Kael 08/04/2007
	bool isAbandon() const;
	bool isAutoRaze() const;
	bool isDisableUpgradeTo() const;
	bool isExplodeInCombat() const;
	bool isFreeXP() const;
	bool isImmortal() const;
	bool isImmuneToDefensiveStrike() const;
	bool isNeverObsolete() const;
	bool isNoWarWeariness() const;
/*************************************************************************************************/
/**	Workers Paradise						01/08/10											**/
/**																								**/
/**							Allows promotions to affect build orders							**/
/*************************************************************************************************/
	bool isPromotionBuild() const;
/*************************************************************************************************/
/**	Workers Paradise						END													**/
/*************************************************************************************************/
	int getBonusAffinity(int i) const;
	int getCombatDefense() const;
	int getDefensiveStrikeChance() const;
	int getDefensiveStrikeDamage() const;
	int getDamageTypeCombat(int i) const;
	int getSpellClassExtraPower(int i) const;
	int getDiploVoteType() const;
	int getDurationFromCombat() const;
	int getEnslavementChance() const;
	int getFreePromotionPick() const;
	int getGoldFromCombat() const;
	const TCHAR* getImage() const;
	int getMinLevel() const;
	///PopCost
	int getPopCost() const;
	int getMiscastChance() const;
	int getModifyGlobalCounter() const;
	int getEquipmentPromotion() const;
	int getPrereqAlignment() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getPrereqBroadEthicalAlignment() const;
	int getEthicalAlignmentModifier() const;
	int getEthicalAlignmentShift() const;
	int getEthicalAlignmentShiftModifier() const;
	int getEthicalAlignmentShiftTowardsNeutral() const;
	int getPrereqEthicalAlignment() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int getPrereqBuildingClass() const;
	int getPrereqCivic() const;
	int getPrereqTrait() const;
	int getPrereqGlobalCounter() const;
	int getPromotionFromCombat() const;
	const TCHAR* getPyPreCombat() const;//PyPreCombat by BI 07/24/11
	const TCHAR* getPyPostCombatLost() const;
	const TCHAR* getPyPostCombatWon() const;
	int getUnitConvertFromCombat() const;
	int getUnitConvertFromCombatChance() const;
	int getUnitCreateFromCombat() const;
	int getUnitCreateFromCombatChance() const;
	int getUpgradeCiv() const;
	int getTier() const;
/*************************************************************************************************/
/**	Tierable								04/04/09								Xienwolf	**/
/**																								**/
/**							Allows for Multiple sets of WeaponTiers								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getWeaponTier() const;
/**								----  End Original Code  ----									**/
	int getWeaponTierMax() const;
	int getWeaponTierMin() const;
/*************************************************************************************************/
/**	Tierable								END													**/
/*************************************************************************************************/
	int getWithdrawlProbDefensive() const;
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	int getNumAffinities() const;
	int getAffinities(int iI) const;
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/

	bool readPass2(CvXMLLoadUtility* pXML);
	bool readPass3();
//FfH: End Add

	// Arrays

	int getPrereqAndTechs(int i) const;				// Exposed to Python
	int getPrereqOrBonuses(int i) const;				// Exposed to Python
	int getProductionTraits(int i) const;				// Exposed to Python
/*************************************************************************************************/
/** Feral Animals			  				10/19/09								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	int getAppearanceTechs(int i) const;                // Exposed to Python
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int getFlavorValue(int i) const;				// Exposed to Python
	int getTerrainAttackModifier(int i) const;				// Exposed to Python
	int getTerrainDefenseModifier(int i) const;				// Exposed to Python
	int getFeatureAttackModifier(int i) const;				// Exposed to Python
	int getFeatureDefenseModifier(int i) const;				// Exposed to Python
/*************************************************************************************************/
/**	GWS										2010-08-23									Milaga	**/
/**																								**/
/**					Units can have movement modifiers for different terrain						**/
/*************************************************************************************************/
// CvUnitInfo Public
	int getUnitHillCost() const;
	int getUnitPeakCost() const;
	int getUnitTerrainCost(int i) const;
	int getUnitFeatureCost(int i) const;
/*************************************************************************************************/
/**	GWS										END													**/
/*************************************************************************************************/
	int getUnitClassAttackModifier(int i) const;				// Exposed to Python
	int getUnitClassDefenseModifier(int i) const;				// Exposed to Python
	int getUnitCombatModifier(int i) const;				// Exposed to Python
	int getUnitCombatCollateralImmune(int i) const;				// Exposed to Python
	int getDomainModifier(int i) const;				// Exposed to Python
	int getBonusProductionModifier(int i) const;				// Exposed to Python
	int getUnitGroupRequired(int i) const;				// Exposed to Python
	int getReligionSpreads(int i) const;		// Exposed to Python
	int getCorporationSpreads(int i) const;		// Exposed to Python
	int getTerrainPassableTech(int i) const;		// Exposed to Python
	int getFeaturePassableTech(int i) const;		// Exposed to Python
/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	// Old Code: int getFlankingStrikeUnitClass(int i) const;	// Exposed to Python
	int getFlankingStrikeUnitCombat(int i) const;	// Exposed to Python
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Speedup								12/02/12										Snarko	**/
/**																								**/
/**			Only store the unitclasses we upgrade to, for faster looping						**/
/*************************************************************************************************/
	int getNumUpgradeUnitClass() const;	//Exposed to Python
	int getUpgradeUnitClass(int i) const;	// Exposed to Python
/*************************************************************************************************/
/**	Speedup									END													**/
/*************************************************************************************************/
	bool getTargetUnitClass(int i) const;	// Exposed to Python
	bool getTargetUnitCombat(int i) const;	// Exposed to Python
	bool getDefenderUnitClass(int i) const;	// Exposed to Python
	bool getDefenderUnitCombat(int i) const;	// Exposed to Python
	bool getUnitAIType(int i) const;				// Exposed to Python
	bool getNotUnitAIType(int i) const;			// Exposed to Python
	bool getBuilds(int i) const;						// Exposed to Python
	bool getGreatPeoples(int i) const;			// Exposed to Python
	bool getBuildings(int i) const;					// Exposed to Python
	bool getTerrainImpassable(int i) const;				// Exposed to Python
	bool getFeatureImpassable(int i) const;				// Exposed to Python
	bool getTerrainNative(int i) const;			// Exposed to Python
	bool getFeatureNative(int i) const;			// Exposed to Python
/*************************************************************************************************/
/**	JRouteNative by Jeckel		imported by Valkrionn	09.28.09                        		**/
/*************************************************************************************************/
	bool getRouteNative(int iRouteType) const;			// Exposed to Python
	bool getRouteImpassable(int iRouteType) const;			// Exposed to Python
	bool getRouteIgnore(int iRouteType) const;			// Exposed to Python
	int getRouteSubstitute(int iRouteType) const;			// Exposed to Python
/*************************************************************************************************/
/**	JRouteNative    END                                                                   		**/
/*************************************************************************************************/
	bool getFreePromotions(int i) const;		// Exposed to Python
/*************************************************************************************************/
/**	1.4										03/28/11								Valkrionn	**/
/**																								**/
/**									New tags required for 1.4									**/
/*************************************************************************************************/
	int getNumFreePromotions(int i) const;
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/
	int getLeaderPromotion() const;   // Exposed to Python
	int getLeaderExperience() const;				// Exposed to Python

/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	int getExtraPerception() const;
	int getInvisibleLevel() const;
	/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

	const TCHAR* getEarlyArtDefineTag(int i, UnitArtStyleTypes eStyle, int iPromo=-1) const;				// Exposed to Python
	void setEarlyArtDefineTag(int i, const TCHAR* szVal);
	const TCHAR* getLateArtDefineTag(int i, UnitArtStyleTypes eStyle) const;				// Exposed to Python
	void setLateArtDefineTag(int i, const TCHAR* szVal);
	const TCHAR* getMiddleArtDefineTag(int i, UnitArtStyleTypes eStyle) const;				// Exposed to Python
	void setMiddleArtDefineTag(int i, const TCHAR* szVal);
	const TCHAR* getUnitNames(int i) const;
	const TCHAR* getFormationType() const;
	//Magic Rework
	int getMagicalPower() const;				// Exposed to Python
	//int getDominionCapacity() const;				// Exposed to Python
//	int getSpellClassExtraPower(int i) const;

	const TCHAR* getButton() const;

//FfH: Added by Kael 02/06/2009
	const TCHAR* getUnitStyleButton(int iProm) const;
//FfH: End Add

	void updateArtDefineButton();

	const CvArtInfoUnit* getArtInfo(int i, EraTypes eEra, UnitArtStyleTypes eStyle, int iPromo=-1) const;

	void read(FDataStreamBase* );
	void write(FDataStreamBase* );

	bool read(CvXMLLoadUtility* pXML);

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvUnitInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	void copyNonDefaultsReadPass2(CvUnitInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iAIWeight;
	int m_iProductionCost;
/*************************************************************************************************/
/**	WeightedCost							 1/30/2010								Valkrionn	**/
/**																								**/
/**								Modifies Cost based on Population								**/
/*************************************************************************************************/
	int m_iCityPopCostModifier;
	int m_iEmpirePopCostModifier;
	int m_iNumCityCostModifier;
	int m_iPlayerPopCostModifier;
/*************************************************************************************************/
/**	WeightedCost								END												**/
/*************************************************************************************************/
/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool m_bNonInfluence;
	bool m_bInfluence;
	int m_iVictoryInfluenceModifier;
	int m_iDefeatInfluenceModifier;
	int m_iPillageInfluenceModifier;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int m_iHurryCostModifier;
	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;
	int m_iMinAreaSize;
	int m_iMoves;
	int m_iAirRange;
	int m_iAirUnitCap;
	int m_iDropRange;
	int m_iNukeRange;
	int m_iWorkRate;
	int m_iBaseDiscover;
	int m_iDiscoverMultiplier;
	int m_iBaseHurry;
	int m_iHurryMultiplier;
	int m_iBaseTrade;
	int m_iTradeMultiplier;
	int m_iGreatWorkCulture;
	int m_iEspionagePoints;
	int m_iCombat;
	int m_iCombatLimit;
	int m_iAirCombat;
	int m_iAirCombatLimit;
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iXPValueAttack;
	int m_iXPValueDefense;
/**								----  End Original Code  ----									**/
	float m_iXPValueAttack;
	float m_iXPValueDefense;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int m_iFirstStrikes;
	int m_iChanceFirstStrikes;
	int m_iInterceptionProbability;
	int m_iEvasionProbability;
	int m_iWithdrawalProbability;
	int m_iEnemyWithdrawalProbability;
	int m_iCollateralDamage;
	int m_iCollateralDamageLimit;
	int m_iCollateralDamageMaxUnits;

/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	int m_iFlankingDamage;
	int m_iFlankingDamageLimit;
	int m_iFlankingDamageMaxUnits;
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/

	int m_iCityAttackModifier;
	int m_iCityDefenseModifier;
	int m_iAnimalCombatModifier;
	int m_iHillsAttackModifier;
	int m_iHillsDefenseModifier;
	int m_iBombRate;
	int m_iBombardRate;
	int m_iSpecialCargo;

	int m_iDomainCargo;
	int m_iCargoSpace;
	int m_iConscriptionValue;
	int m_iCultureGarrisonValue;
	int m_iExtraCost;
	int m_iAssetValue;
/*************************************************************************************************/
/**	Unit power						17/02/12										Snarko		**/
/**																								**/
/**							Rewriting unit power system											**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iPowerValue;
/**								----  End Original Code  ----									**/
	int m_iPowerAdd;
	int m_iPowerMult;
/*************************************************************************************************/
/**	Unit power						END															**/
/*************************************************************************************************/
	int m_iUnitClassType;
	int m_iSecondaryUnitClassType;
	int m_iSpecialUnitType;
	int m_iUnitCaptureClassType;
	int m_iUnitCombatType;
	int m_iDomainType;
	int m_iDefaultUnitAIType;
/*************************************************************************************************/
/**	CandyMan								04/04/09								Xienwolf	**/
/**																								**/
/**							Allows Multiple Invisible types on a Unit							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iInvisibleType;
/**								----  End Original Code  ----									**/
	std::vector<int> m_aiInvisibleTypes;
/*************************************************************************************************/
/**	CandyMan								END													**/
/*************************************************************************************************/
	int m_iAdvisorType;
	int m_iHolyCity;
	int m_iReligionType;
	int m_iStateReligion;
	int m_iPrereqReligion;
	int m_iPrereqCorporation;
	int m_iPrereqBuilding;
	int m_iPrereqAndTech;
	int m_iPrereqAndBonus;
	int m_iGroupSize;
	int m_iGroupDefinitions;
	int m_iUnitMeleeWaveSize;
	int m_iUnitRangedWaveSize;
	int m_iNumUnitNames;
	int m_iCommandType;
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iLeaderExperience;
/**								----  End Original Code  ----									**/
	float m_iLeaderExperience;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	//Magic Rework
	int m_iMagicalPower;
//	int m_iDominionCapacity;
//	int* m_piSpellClassExtraPower;

	bool m_bAnimal;
	bool m_bFoodProduction;
	bool m_bNoBadGoodies;
	bool m_bOnlyDefensive;
	bool m_bNoCapture;
	bool m_bImmuneToCapture;
	bool m_bQuickCombat;
	bool m_bRivalTerritory;
	bool m_bMilitaryHappiness;
	bool m_bMilitarySupport;
	bool m_bMilitaryProduction;
	bool m_bPillage;
	bool m_bReligiousCommander; //ReligiousCommander by BI 07/24/11
	bool m_bSpy;
	bool m_bSabotage;
	bool m_bDestroy;
	bool m_bStealPlans;
	bool m_bInvestigate;
	bool m_bCounterSpy;
	bool m_bFound;
	bool m_bGoldenAge;
	bool m_bInvisible;
	bool m_bFirstStrikeImmune;
	bool m_bNoDefensiveBonus;
	bool m_bIgnoreBuildingDefense;
	bool m_bCanMoveImpassable;
	bool m_bCanMoveAllTerrain;
	bool m_bFlatMovementCost;
	bool m_bIgnoreTerrainCost;
	bool m_bNukeImmune;
	bool m_bPrereqBonuses;
	bool m_bPrereqReligion;
	bool m_bMechanized;
	bool m_bRenderBelowWater;
	bool m_bRenderAlways;
	bool m_bSuicide;
	bool m_bHiddenNationality;
	bool m_bAlwaysHostile;
	bool m_bNoRevealMap;
	int m_iLeaderPromotion;

	float m_fUnitMaxSpeed;
	float m_fUnitPadTime;

/*************************************************************************************************/
/**	New Tag Defs	(UnitInfos)				05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iCommandLimit;
	int m_iCommandRange;
	bool m_bFreeUnit;
	bool m_bNoSupply;
	bool m_bCommunalProperty;
	bool m_bNeverHostile;
	bool m_bBlind;
	bool m_bJoinPop;
	int m_iPrereqBroadAlignment;
	int m_iAlignmentModifier;
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	int m_iAlignmentShift;
	int m_iAlignmentShiftModifier;
	int m_iAlignmentShiftTowardsNeutral;
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
	CvString m_szPyPerTurn;
	int* m_piYieldFromKill;
	int* m_piCommerceFromKill;
	bool m_bCanClimbPeaks;
	bool* m_pbAllowPromotion;
	bool* m_pbDenyPromotion;
	CvString* m_paszQuotes;
	int m_iNumQuotes;
	CvString m_szQuote;
	CvString* m_paszImages;
	int m_iNumImages;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/** Feral Animals			  				10/19/09								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	int m_iAppearanceProb;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Units: Added by Kael 08/04/2007
	bool m_bAbandon;
	bool m_bAutoRaze;
	bool m_bDisableUpgradeTo;
	bool m_bExplodeInCombat;
	bool m_bFreeXP;
	bool m_bImmortal;
	bool m_bImmuneToDefensiveStrike;
	bool m_bNeverObsolete;
	bool m_bNoWarWeariness;
/*************************************************************************************************/
/**	Workers Paradise						01/08/10											**/
/**																								**/
/**							Allows promotions to affect build orders							**/
/*************************************************************************************************/
	bool m_bPromotionBuild;
/*************************************************************************************************/
/**	Workers Paradise						END													**/
/*************************************************************************************************/
	int m_iCombatDefense;
	int m_iDefensiveStrikeChance;
	int m_iDefensiveStrikeDamage;
	int m_iDiploVoteType;
	int m_iDurationFromCombat;
	int m_iEnslavementChance;
	int m_iFreePromotionPick;
	int m_iGoldFromCombat;
	int m_iMinLevel;
	///PopCost
	int m_iPopCost;
	int m_iMiscastChance;
	int m_iModifyGlobalCounter;
	int m_iEquipmentPromotion;
	int m_iPrereqAlignment;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iPrereqBroadEthicalAlignment;
	int m_iEthicalAlignmentModifier;
	int m_iEthicalAlignmentShift;
	int m_iEthicalAlignmentShiftModifier;
	int m_iEthicalAlignmentShiftTowardsNeutral;
	int m_iPrereqEthicalAlignment;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int m_iPrereqBuildingClass;
	int m_iPrereqCivic;
	int m_iPrereqTrait;
	int m_iPrereqGlobalCounter;
	int m_iPromotionFromCombat;
	int m_iTier;
	int m_iUnitConvertFromCombat;
	int m_iUnitConvertFromCombatChance;
	int m_iUnitCreateFromCombat;
	int m_iUnitCreateFromCombatChance;
	int m_iUpgradeCiv;
/*************************************************************************************************/
/**	Tierable								04/04/09								Xienwolf	**/
/**																								**/
/**							Allows for Multiple sets of WeaponTiers								**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iWeaponTier;
/**								----  End Original Code  ----									**/
	int m_iWeaponTierMax;
	int m_iWeaponTierMin;
	CvString m_szPyDeath;
/*************************************************************************************************/
/**	Tierable								END													**/
/*************************************************************************************************/
	int m_iWithdrawlProbDefensive;
	int* m_piBonusAffinity;
	int* m_piDamageTypeCombat;
	int* m_piSpellClassExtraPower;
	CvString m_szPyPreCombat;//PyPrecombat by BI 07/24/11
	CvString m_szPyPostCombatLost;
	CvString m_szPyPostCombatWon;
	CvString m_szImage;
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	int m_iExtraPerception;
	int m_iInvisibleLevel;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
	int m_iNumAffinities;
	int* m_piAffinities;
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/
//FfH: End Add

	// Arrays

	int* m_piPrereqAndTechs;
	int* m_piPrereqOrBonuses;
	int* m_piProductionTraits;
/*************************************************************************************************/
/** Feral Animals			  				10/19/09								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	int* m_piAppearanceTechs;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int* m_piFlavorValue;
	int* m_piTerrainAttackModifier;
	int* m_piTerrainDefenseModifier;
	int* m_piFeatureAttackModifier;
	int* m_piFeatureDefenseModifier;
/*************************************************************************************************/
/**	GWS										2010-08-23									Milaga	**/
/**																								**/
/**					Units can have movement modifiers for different terrain						**/
/*************************************************************************************************/
// CvUnit Protected
	int m_iUnitHillCost;
	int m_iUnitPeakCost;
	int* m_piUnitTerrainCost;
	int* m_piUnitFeatureCost;
/*************************************************************************************************/
/**	GWS										END													**/
/*************************************************************************************************/
	int* m_piUnitClassAttackModifier;
	int* m_piUnitClassDefenseModifier;
	int* m_piUnitCombatModifier;
	int* m_piUnitCombatCollateralImmune;
	int* m_piDomainModifier;
	int* m_piBonusProductionModifier;
	int* m_piUnitGroupRequired;
	int* m_piReligionSpreads;
	int* m_piCorporationSpreads;
	int* m_piTerrainPassableTech;
	int* m_piFeaturePassableTech;
/*************************************************************************************************/
/**	Updated Flanking						2011-10-30									Jheral	**/
/**																								**/
/**					Flanking applies to UnitCombats, rather than UnitClasses					**/
/*************************************************************************************************/
	// Old Code: int* m_piFlankingStrikeUnitClass;
	int* m_piFlankingStrikeUnitCombat;
/*************************************************************************************************/
/**	Updated Flanking						END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Speedup								12/02/12										Snarko	**/
/**																								**/
/**			Only store the unitclasses we upgrade to, for faster looping						**/
/*************************************************************************************************/
	int m_iNumUpgradeUnitClass;
	int* m_piUpgradeUnitClass;
/*************************************************************************************************/
/**	Speedup									END													**/
/*************************************************************************************************/
	bool* m_pbTargetUnitClass;
	bool* m_pbTargetUnitCombat;
	bool* m_pbDefenderUnitClass;
	bool* m_pbDefenderUnitCombat;
	bool* m_pbUnitAIType;
	bool* m_pbNotUnitAIType;
	bool* m_pbBuilds;
	bool* m_pbGreatPeoples;
	bool* m_pbBuildings;
	bool* m_pbTerrainNative;
	bool* m_pbFeatureNative;
/*************************************************************************************************/
/**	JRouteNative by Jeckel		imported by Valkrionn	09.28.09                        		**/
/*************************************************************************************************/
	bool* m_pbRouteNative;
	bool* m_pbRouteImpassable;
	bool* m_pbRouteIgnore;
	int* m_piRouteSubstitute;
/*************************************************************************************************/
/**	JRouteNative    END                                                                   		**/
/*************************************************************************************************/
	bool* m_pbTerrainImpassable;
	bool* m_pbFeatureImpassable;
/*************************************************************************************************/
/**	1.4										03/28/11								Valkrionn	**/
/**																								**/
/**									New tags required for 1.4									**/
/*************************************************************************************************/
/**										Start Original Code										**
	bool* m_pbFreePromotions;
/**										End Original Code										**/
	int* m_piFreePromotions;
/*************************************************************************************************/
/**												END												**/
/*************************************************************************************************/

	CvString* m_paszEarlyArtDefineTags;
	CvString* m_paszLateArtDefineTags;
	CvString* m_paszMiddleArtDefineTags;
	CvString* m_paszUnitNames;
	CvString m_szFormationType;
	CvString m_szArtDefineButton;

	std::vector<int> m_aiSeeInvisibleTypes;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
// class	: CvUnitFormationInfo
//
// \brief	: Holds information relating to the formation of sub-units within a unit
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class CvUnitEntry
{
public:
	CvUnitEntry()
	{
	}

	CvUnitEntry(const NiPoint2 &position, float radius, float facingDirection, float facingVariance) :
	m_position(position),
	m_fRadius(radius),
	m_fFacingDirection(facingDirection),
	m_fFacingVariance(facingVariance)
	{
	}

	NiPoint2 m_position;
	float m_fRadius;
	float m_fFacingDirection;
	float m_fFacingVariance;
};

class CvUnitFormationInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvUnitFormationInfo();
	DllExport virtual ~CvUnitFormationInfo();

	DllExport const TCHAR* getFormationType() const;
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**			These functions are required so we can do an item-by-item comparison loop			**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	int getNumEventTypes() const;
	const EntityEventTypes &getEventType(int index) const;
	void copyNonDefaults(CvUnitFormationInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
	DllExport const std::vector<EntityEventTypes> & getEventTypes() const;

	DllExport int getNumUnitEntries() const;
	DllExport const CvUnitEntry &getUnitEntry(int index) const;
	DllExport void addUnitEntry(const CvUnitEntry &unitEntry);
	DllExport int getNumGreatUnitEntries() const;
	DllExport const CvUnitEntry &getGreatUnitEntry(int index) const;
	DllExport int getNumSiegeUnitEntries() const;
	DllExport const CvUnitEntry &getSiegeUnitEntry(int index) const;

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PUBLIC MEMBER VARIABLES---------------------------------

protected:

	CvString m_szFormationType;
	std::vector<EntityEventTypes>	m_vctEventTypes;		//!< The list of EntityEventTypes that this formation is intended for

	std::vector<CvUnitEntry> m_vctUnitEntries;
	std::vector<CvUnitEntry> m_vctGreatUnitEntries;
	std::vector<CvUnitEntry> m_vctSiegeUnitEntries;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpecialUnitInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpecialUnitInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvSpecialUnitInfo();
	virtual ~CvSpecialUnitInfo();

	bool isValid() const;
	bool isCityLoad() const;

	// Arrays

	bool isCarrierUnitAIType(int i) const; 		// Exposed to Python
	int getProductionTraits(int i) const;				// Exposed to Python
/*************************************************************************************************/
/** Feral Animals			  				10/19/09								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	int getAppearanceTechs(int i) const;                // Exposed to Python
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvSpecialUnitInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	bool m_bValid;
	bool m_bCityLoad;

	// Arrays
	bool* m_pbCarrierUnitAITypes;
	int* m_piProductionTraits;
/*************************************************************************************************/
/** Feral Animals			  				10/19/09								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	int* m_piAppearanceTechs;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCivicOptionInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCivicOptionInfo :
	public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvCivicOptionInfo();
	virtual ~CvCivicOptionInfo();

	bool getTraitNoUpkeep(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvCivicOptionInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	bool* m_pabTraitNoUpkeep;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCivicInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCivicInfo :
	public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvCivicInfo();
	virtual ~CvCivicInfo();

	int getCivicOptionType() const;				// Exposed to Python
	int getAnarchyLength() const;				// Exposed to Python
	int getCrimePerTurn() const;				// Exposed to Python
	int getUpkeep() const;				// Exposed to Python
	int getAIWeight() const;				// Exposed to Python
	int getGreatPeopleRateModifier() const;				// Exposed to Python
	int getGreatGeneralRateModifier() const;				// Exposed to Python
	int getDiscoverRandModifier() const;				// Exposed to Python
	int getSpreadRandModifier() const;				// Exposed to Python
	int getDomesticGreatGeneralRateModifier() const;				// Exposed to Python
	int getStateReligionGreatPeopleRateModifier() const;				// Exposed to Python
	int getDistanceMaintenanceModifier() const;				// Exposed to Python
	int getNumCitiesMaintenanceModifier() const;				// Exposed to Python
	int getCorporationMaintenanceModifier() const;				// Exposed to Python
	int getExtraHealth() const;						// Exposed to Python
	int getFreeExperience() const;				// Exposed to Python
	int getWorkerSpeedModifier() const;				// Exposed to Python
	int getImprovementUpgradeRateModifier() const;				// Exposed to Python
	int getMilitaryProductionModifier() const;				// Exposed to Python
	int getBaseFreeUnits() const;				// Exposed to Python
	int getBaseFreeMilitaryUnits() const;				// Exposed to Python
	int getFreeUnitsPopulationPercent() const;				// Exposed to Python
	int getFreeMilitaryUnitsPopulationPercent() const;				// Exposed to Python
	int getGoldPerUnit() const;				// Exposed to Python
	int getGoldPerMilitaryUnit() const;				// Exposed to Python
	int getHappyPerMilitaryUnit() const;				// Exposed to Python
	int getLargestCityHappiness() const;					// Exposed to Python
	int getWarWearinessModifier() const;					// Exposed to Python
	int getFreeSpecialist() const;				// Exposed to Python
	int getTradeRoutes() const;				// Exposed to Python
	int getTechPrereq() const;				// Exposed to Python
	int getCivicPercentAnger() const;				// Exposed to Python
	int getMaxConscript() const;				// Exposed to Python
	int getStateReligionHappiness() const;				// Exposed to Python
	int getNonStateReligionHappiness() const;				// Exposed to Python
	int getStateReligionUnitProductionModifier() const;				// Exposed to Python
	int getStateReligionBuildingProductionModifier() const;				// Exposed to Python
	int getStateReligionFreeExperience() const;								// Exposed to Python
	int getExpInBorderModifier() const;				// Exposed to Python

	bool isMilitaryFoodProduction() const;				// Exposed to Python
/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool isFixedBorders() const;
	bool isInfluenceAllowed() const;
	int getVictoryInfluenceModifier() const;
	int getDefeatInfluenceModifier() const;
	int getPillageInfluenceModifier() const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	bool isNoUnhealthyPopulation() const;				// Exposed to Python
	bool isBuildingOnlyHealthy() const;				// Exposed to Python
	bool isNoForeignTrade() const;				// Exposed to Python
	bool isNoCorporations() const;				// Exposed to Python
	bool isNoForeignCorporations() const;				// Exposed to Python
	bool isStateReligion() const;				// Exposed to Python
	bool isNoNonStateReligionSpread() const;				// Exposed to Python

	std::wstring pyGetWeLoveTheKing() { return getWeLoveTheKing(); }			// Exposed to Python
	const wchar* getWeLoveTheKing();
	void setWeLoveTheKingKey(const TCHAR* szVal);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvCivicInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	New Tag Defs	(CivicInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getAlignmentModifier() const;
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	int getAlignmentShift() const;
	int getAlignmentShiftModifier() const;
	int getAlignmentShiftTowardsNeutral() const;
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
	const wchar* getWeLoveTheKingKey();
	int getPrereqCivilizationVectorSize();
	CvString getPrereqCivilizationVectorElement(int i);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Civics: Added by Kael 08/11/2007
	bool isCompassionHigh() const;
	bool isCompassionLow() const;
	bool isHidden() const;
	bool isNoDiplomacyWithEnemies() const;
	bool isPrereqWar() const;
	int getAttitudeShareMod() const;
	int getCoastalTradeRoutes() const;
	int getEnslavementChance() const;
	int getFoodConsumptionPerPopulation() const;
	int getBlockAlignment() const;
	int getPrereqAlignment() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getEthicalAlignmentModifier() const;
	int getEthicalAlignmentShift() const;
	int getEthicalAlignmentShiftModifier() const;
	int getEthicalAlignmentShiftTowardsNeutral() const;
	int getBlockEthicalAlignment() const;
	int getPrereqEthicalAlignment() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int getPrereqCivilization() const;
	int getPrereqReligion() const;

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	int getCityCapModifier() const;
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/** MaxCulture					Opera															**/
/*************************************************************************************************/
	int getMaxCultureLevel() const;
	bool isExpandBeyondPlotRadius() const;
	bool isCapitalNoCultureCap() const;
	bool isGovCenterNoCultureCap() const;
/*************************************************************************************************/
/** MaxCulture					END																**/
/*************************************************************************************************/
	
	bool isOverflowProduction() const;

	bool readPass3();
//FfH: End Add

	// Arrays

	int getYieldModifier(int i) const;				// Exposed to Python
	int* getYieldModifierArray() const;
	int getCapitalYieldModifier(int i) const;				// Exposed to Python
	int* getCapitalYieldModifierArray() const;
	int getTradeYieldModifier(int i) const;				// Exposed to Python
	int* getTradeYieldModifierArray() const;
	int getForeignTradeYieldModifier(int i) const;				// Exposed to Python
	int* getForeignTradeYieldModifierArray() const;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	int getTradeCommerceModifier(int i) const;			// Exposed to Python
	int* getTradeCommerceModifierArray() const;
	int getForeignTradeCommerceModifier(int i) const;			// Exposed to Python
	int* getForeignTradeCommerceModifierArray() const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int getCommerceChange(int i) const;				// Exposed to Python
	int* getCommerceChangeArray() const;
	int getCommerceModifier(int i) const;				// Exposed to Python
	int* getCommerceModifierArray() const;
	int getCapitalCommerceModifier(int i) const;				// Exposed to Python
	int* getCapitalCommerceModifierArray() const;
	int getSpecialistExtraCommerce(int i) const;				// Exposed to Python
	int* getSpecialistExtraCommerceArray() const;
	int getBuildingHappinessChanges(int i) const;				// Exposed to Python
	int getBuildingHealthChanges(int i) const;				// Exposed to Python
	int getFeatureHappinessChanges(int i) const;				// Exposed to Python
	int getSpecialistClassCrimeChanges(int i) const;				// Exposed to Python
	int getSpecialistClassGPPChanges(int i) const;				// Exposed to Python

	bool isHurry(int i) const;													// Exposed to Python
	bool isSpecialBuildingNotRequired(int i) const;			// Exposed to Python
	bool isSpecialistClassValid(int i) const;								// Exposed to Python
	int getFreeSpecialistClassCount(int i) const;				// Exposed to Python
	int getSpecialistClassCount(int i) const;				// Exposed to Python
	bool isSpecialistClassUnlimited(int i) const;								// Exposed to Python

	int getImprovementYieldChanges(int i, int j) const;				// Exposed to Python
	int getSpecialistClassYieldChanges(int i, int j) const;				// Exposed to Python
	int* getSpecialistClassYieldChangeArray(int i) const;
	int getSpecialistClassCommerceChanges(int i, int j) const;				// Exposed to Python
	int* getSpecialistClassCommerceChangeArray(int i) const;

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	bool read(CvXMLLoadUtility* pXML);

//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iCivicOptionType;
	int m_iAnarchyLength;
	int m_iCrimePerTurn;
	int m_iUpkeep;
	int m_iAIWeight;
	int m_iGreatPeopleRateModifier;
	int m_iGreatGeneralRateModifier;
	int m_iDiscoverRandModifier;
	int	m_iSpreadRandModifier;
	int m_iDomesticGreatGeneralRateModifier;
	int m_iStateReligionGreatPeopleRateModifier;
	int m_iDistanceMaintenanceModifier;
	int m_iNumCitiesMaintenanceModifier;
	int m_iCorporationMaintenanceModifier;
	int m_iExtraHealth;
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iFreeExperience;
/**								----  End Original Code  ----									**/
	float m_iFreeExperience;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int m_iWorkerSpeedModifier;
	int m_iImprovementUpgradeRateModifier;
	int m_iMilitaryProductionModifier;
	int m_iBaseFreeUnits;
	int m_iBaseFreeMilitaryUnits;
	int m_iFreeUnitsPopulationPercent;
	int m_iFreeMilitaryUnitsPopulationPercent;
	int m_iGoldPerUnit;
	int m_iGoldPerMilitaryUnit;
	int m_iHappyPerMilitaryUnit;
	int m_iLargestCityHappiness;
	int m_iWarWearinessModifier;
	int m_iFreeSpecialist;
	int m_iTradeRoutes;
	int m_iTechPrereq;
	int m_iCivicPercentAnger;
	int m_iMaxConscript;
	int m_iStateReligionHappiness;
	int m_iNonStateReligionHappiness;
	int m_iStateReligionUnitProductionModifier;
	int m_iStateReligionBuildingProductionModifier;
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iStateReligionFreeExperience;
/**								----  End Original Code  ----									**/
	float m_iStateReligionFreeExperience;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int m_iExpInBorderModifier;

	bool m_bMilitaryFoodProduction;
/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool m_bFixedBorders;
	bool m_bInfluenceAllowed;
	int m_iVictoryInfluenceModifier;
	int m_iDefeatInfluenceModifier;
	int m_iPillageInfluenceModifier;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	bool m_bNoUnhealthyPopulation;
	bool m_bBuildingOnlyHealthy;
	bool m_bNoForeignTrade;
	bool m_bNoCorporations;
	bool m_bNoForeignCorporations;
	bool m_bStateReligion;
	bool m_bNoNonStateReligionSpread;

	CvWString m_szWeLoveTheKingKey;

/*************************************************************************************************/
/**	New Tag Defs	(CivicInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iAlignmentModifier;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	int m_iAlignmentShift;
	int m_iAlignmentShiftModifier;
	int m_iAlignmentShiftTowardsNeutral;
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
//FfH Civics: Added by Kael 08/11/2007
	bool m_bCompassionHigh;
	bool m_bCompassionLow;
	bool m_bHidden;
	bool m_bNoDiplomacyWithEnemies;
	bool m_bPrereqWar;
	int m_iAttitudeShareMod;
	int m_iCoastalTradeRoutes;
	int m_iEnslavementChance;
	int m_iFoodConsumptionPerPopulation;
	int m_iBlockAlignment;
	int m_iPrereqAlignment;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iEthicalAlignmentModifier;
	int m_iEthicalAlignmentShift;
	int m_iEthicalAlignmentShiftModifier;
	int m_iEthicalAlignmentShiftTowardsNeutral;
	int m_iBlockEthicalAlignment;
	int m_iPrereqEthicalAlignment;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int m_iPrereqCivilization;
	int m_iPrereqReligion;
//FfH: End Add

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	int m_iCityCapModifier;
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/** MaxCulture					Opera															**/
/*************************************************************************************************/
	int m_iMaxCultureLevel;
	bool m_bExpandBeyondPlotRadius;
	bool m_bCapitalNoCultureCap;
	bool m_bGovCenterNoCultureCap;
/*************************************************************************************************/
/** MaxCulture					END																**/
/*************************************************************************************************/
	
	bool m_bOverflowProduction;

	// Arrays

	int* m_piYieldModifier;
	int* m_piCapitalYieldModifier;
	int* m_piTradeYieldModifier;
	int* m_piForeignTradeYieldModifier;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	int* m_piTradeCommerceModifier;
	int* m_piForeignTradeCommerceModifier;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int* m_piCommerceChange;
	int* m_piCommerceModifier;
	int* m_piCapitalCommerceModifier;
	int* m_piSpecialistExtraCommerce;
	int* m_paiBuildingHappinessChanges;
	int* m_paiBuildingHealthChanges;
	int* m_paiFeatureHappinessChanges;
	int* m_paiSpecialistClassCrimeChanges;
	int* m_paiSpecialistClassGPPChanges;

	bool* m_pabHurry;
	bool* m_pabSpecialBuildingNotRequired;
	bool* m_pabSpecialistClassValid;
	bool* m_pabSpecialistClassUnlimited;
	int* m_piSpecialistClassCount;
	
	int* m_piFreeSpecialistClassCount;

	int** m_ppiImprovementYieldChanges;
	int** m_ppiSpecialistClassYieldChanges;
	int** m_ppiSpecialistClassCommerceChanges;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvDiplomacyInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvDiplomacyInfo :
	public CvInfoBase
{

	friend class CvXMLLoadUtility;		// so it can access private vars to initialize the class
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvDiplomacyInfo();
	DllExport virtual ~CvDiplomacyInfo();

	DllExport void uninit();

	DllExport const CvDiplomacyResponse& getResponse(int iNum) const;	// Exposed to Python
	DllExport int getNumResponses() const;															// Exposed to Python

	DllExport bool getCivilizationTypes(int i, int j) const;						// Exposed to Python
	DllExport bool getLeaderHeadTypes(int i, int j) const;							// Exposed to Python
	DllExport bool getAttitudeTypes(int i, int j) const;								// Exposed to Python
	DllExport bool getDiplomacyPowerTypes(int i, int j) const;					// Exposed to Python

	DllExport int getNumDiplomacyText(int i) const;											// Exposed to Python

	DllExport const TCHAR* getDiplomacyText(int i, int j) const;				// Exposed to Python

	DllExport void read(FDataStreamBase* stream);
	DllExport void write(FDataStreamBase* stream);
	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**		Another "Diplomacy is Wierd" function, haven't played with it either so far				**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvXMLLoadUtility* pXML);
	bool FindResponseIndex(CvDiplomacyResponse* pNewResponse, int iCase, int* iIndex);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	std::vector<CvDiplomacyResponse*> m_pResponses;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvUnitClassInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvUnitClassInfo :
	public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvUnitClassInfo();
	virtual ~CvUnitClassInfo();

	int getMaxGlobalInstances() const;				// Exposed to Python
	int getMaxTeamInstances() const;				// Exposed to Python
	int getMaxPlayerInstances() const;				// Exposed to Python
/*************************************************************************************************/
/**	WeightedCost							 1/30/2010								Valkrionn	**/
/**																								**/
/**						Modifies Cost based on Population and number of Cities					**/
/*************************************************************************************************/
	int isCountCitiesAsUnit() const;				// Exposed to Python
/*************************************************************************************************/
/**	WeightedCost								END												**/
/*************************************************************************************************/
	int getInstanceCostModifier() const;				// Exposed to Python
	int getDefaultUnitIndex() const;				// Exposed to Python
	void setDefaultUnitIndex(int i);
/*************************************************************************************************/
/**	New Tag Defs	(UnitClassInfos)		10/18/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	bool isUnique() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**	Extra functions to handle the fact that Readpass3 might contain more than 1 piece of data	**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	int getDefaultUnitIndexVector();
	CvString getDefaultUnitIndexVectorElement(int i);
	void copyNonDefaults(CvUnitClassInfo* pClassInfo = NULL , CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();

//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iMaxGlobalInstances;
	int m_iMaxTeamInstances;
	int m_iMaxPlayerInstances;
/*************************************************************************************************/
/**	WeightedCost							 1/30/2010								Valkrionn	**/
/**																								**/
/**						Modifies Cost based on Population and number of Cities					**/
/*************************************************************************************************/
	int m_bCountCitiesAsUnit;
/*************************************************************************************************/
/**	WeightedCost								END												**/
/*************************************************************************************************/
	int m_iInstanceCostModifier;
	int m_iDefaultUnitIndex;
/*************************************************************************************************/
/**	New Tag Defs	(UnitClassInfos)		10/18/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	bool m_bUnique;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/


};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvBuildingInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoBuilding;
class CvArtInfoMovie;
class CvBuildingInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvBuildingInfo();
	virtual ~CvBuildingInfo();

	int getBuildingClassType() const;				// Exposed to Python
	int getVictoryPrereq() const;				// Exposed to Python
	int getFreeStartEra() const;						// Exposed to Python
	int getMaxStartEra() const;				// Exposed to Python
	int getObsoleteTech() const;				// Exposed to Python
	int getPrereqAndTech() const;				// Exposed to Python
	int getNoBonus() const;				// Exposed to Python
	int getPowerBonus() const;				// Exposed to Python
	int getFreeBonus() const;				// Exposed to Python
	int getNumFreeBonuses() const;				// Exposed to Python
	int getMinLevelAccess() const;				// Exposed to Python
	int getFreeBuildingClass() const;				// Exposed to Python
	int getParentBuildingClass() const;				// Exposed to Python
	void setNumFreeBuildingClass(int i);
	int getFreePromotion() const;				// Exposed to Python
	int getCivicOption() const;				// Exposed to Python
	int getAIWeight() const;				// Exposed to Python
	int getProductionCost() const;				// Exposed to Python
	int getHurryCostModifier() const;				// Exposed to Python
	int getHurryAngerModifier() const;				// Exposed to Python
	int getAdvancedStartCost() const;				// Exposed to Python
	int getAdvancedStartCostIncrease() const;				// Exposed to Python
	int getMinAreaSize() const;				// Exposed to Python
	int getNumCitiesPrereq() const;				// Exposed to Python
	int getNumTeamsPrereq() const;				// Exposed to Python
	int getUnitLevelPrereq() const;				// Exposed to Python
	int getMinLatitude() const;				// Exposed to Python
	int getMaxLatitude() const;				// Exposed to Python
	int getGreatPeopleRateModifier() const;				// Exposed to Python
	int getGreatGeneralRateModifier() const;				// Exposed to Python
	int getDomesticGreatGeneralRateModifier() const;				// Exposed to Python
	int getGlobalGreatPeopleRateModifier() const;				// Exposed to Python
	int getAnarchyModifier() const;				// Exposed to Python
	int getGoldenAgeModifier() const;				// Exposed to Python
	int getGlobalHurryModifier() const;				// Exposed to Python
	int getFreeExperience() const;				// Exposed to Python
	int getGlobalFreeExperience() const;				// Exposed to Python
	int getFoodKept() const;				// Exposed to Python
	int getAirlift() const;				// Exposed to Python
	int getAirModifier() const;				// Exposed to Python
	int getAirUnitCapacity() const;				// Exposed to Python
	int getNukeModifier() const;				// Exposed to Python
	int getNukeExplosionRand() const;				// Exposed to Python
	int getFreeSpecialist() const;				// Exposed to Python
	int getAreaFreeSpecialist() const;				// Exposed to Python
	int getGlobalFreeSpecialist() const;				// Exposed to Python
	int getHappiness() const;				// Exposed to Python
	int getAreaHappiness() const;				// Exposed to Python
	int getGlobalHappiness() const;				// Exposed to Python
	int getStateReligionHappiness() const;				// Exposed to Python
	int getWorkerSpeedModifier() const;				// Exposed to Python
	int getMilitaryProductionModifier() const;				// Exposed to Python
	int getRitualProductionModifier() const;				// Exposed to Python
	int getGlobalRitualProductionModifier() const;				// Exposed to Python
	int getTradeRoutes() const;				// Exposed to Python
	int getCoastalTradeRoutes() const;				// Exposed to Python
	int getGlobalTradeRoutes() const;				// Exposed to Python
	int getTradeRouteModifier() const;				// Exposed to Python
	int getForeignTradeRouteModifier() const;				// Exposed to Python
	int getAssetValue() const;				// Exposed to Python
	int getPowerValue() const;				// Exposed to Python
	int getSpecialBuildingType() const;				// Exposed to Python
	int getAdvisorType() const;				// Exposed to Python
	int getHolyCity() const;				// Exposed to Python
	int getReligionType() const;				// Exposed to Python
	int getStateReligion() const;				// Exposed to Python
	int getPrereqReligion() const;				// Exposed to Python
	int getPrereqFlag() const;				// Exposed to Python
	int getPrereqCorporation() const;				// Exposed to Python
	int getPrereqCivic() const;				// Exposed to Python
	int getFoundsCorporation() const;				// Exposed to Python
	int getGlobalReligionCommerce() const;				// Exposed to Python
	int getGlobalCorporationCommerce() const;				// Exposed to Python
	int getPrereqAndBonus() const;				// Exposed to Python
	int getGreatPeopleUnitClass() const;				// Exposed to Python
	int getGreatPeopleRateChange() const;				// Exposed to Python
	int getConquestProbability() const;				// Exposed to Python
	int getMaintenanceModifier() const;				// Exposed to Python
	int getWarWearinessModifier() const;				// Exposed to Python
	int getGlobalWarWearinessModifier() const;				// Exposed to Python
	int getEnemyWarWearinessModifier() const;				// Exposed to Python
	int getHealRateChange() const;				// Exposed to Python
	int getHealth() const;				// Exposed to Python
	int getAreaHealth() const;				// Exposed to Python
	int getGlobalHealth() const;				// Exposed to Python
	int getGlobalPopulationChange() const;				// Exposed to Python
	int getFreeTechs() const;				// Exposed to Python
	int getDefenseModifier() const;					// Exposed to Python
	int getBombardDefenseModifier() const;					// Exposed to Python
	int getAllCityDefenseModifier() const;				// Exposed to Python
	int getEspionageDefenseModifier() const;					// Exposed to Python
	int getMissionType() const;											// Exposed to Python
	void setMissionType(int iNewType);
	int getVoteSourceType() const;				// Exposed to Python
	const char* getPythonHelp() const;

/*************************************************************************************************/
/**	Building prereq Alignments				07/04/10								Snarko		**/
/**																								**/
/**							Allows buildings to require alignments								**/
/*************************************************************************************************/
	int getNumPrereqAlignments() const;
	int getPrereqAlignment(int iI) const;
	int getNumPrereqEthicalAlignments() const;
	int getPrereqEthicalAlignment(int iI) const;
/*************************************************************************************************/
/**	Building prereq Alignments					END												**/
/*************************************************************************************************/

	float getVisibilityPriority() const;

	bool isTeamShare() const;				// Exposed to Python
	bool isWater() const;				// Exposed to Python
	bool isRiver() const;				// Exposed to Python
	bool isPower() const;				// Exposed to Python
	bool isDirtyPower() const;				// Exposed to Python
	bool isAreaCleanPower() const;		// Exposed to Python
	bool isAreaBorderObstacle() const;		// Exposed to Python
	bool isForceTeamVoteEligible() const;				// Exposed to Python
	bool isCapital() const;				// Exposed to Python
	bool isGovernmentCenter() const;				// Exposed to Python
	bool isGoldenAge() const;				// Exposed to Python
	bool isFoodProduction() const;				// Exposed to Python
	bool isMapCentering() const;				// Exposed to Python
	bool isNoUnhappiness() const;				// Exposed to Python
	bool isNoUnhealthiness() const;				// Exposed to Python
/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool isFixedBorders() const;				// Exposed to Python
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	bool isNoForeignTradeRoutes() const;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
/*************************************************************************************************/
/* MultiBonus							  06/08/10									Valkrionn    */
/*                                                                                               */
/*				Causes certain building tags to use each instance of a resource                  */
/*************************************************************************************************/
	bool isUseMultiBonuses() const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	bool isNoUnhealthyPopulation() const;				// Exposed to Python
	bool isBuildingOnlyHealthy() const;				// Exposed to Python
	bool isNeverCapture() const;				// Exposed to Python
	bool isNukeImmune() const;				// Exposed to Python
	bool isPrereqReligion() const;				// Exposed to Python
	bool isPrereqNoReligion() const;				// Exposed to Python
	bool isCenterInCity() const;				// Exposed to Python
	bool isStateReligion() const;				// Exposed to Python
	bool isAllowsNukes() const;				// Exposed to Python

	const TCHAR* getConstructSound() const;				// Exposed to Python
	void setConstructSound(const TCHAR* szVal);
	const TCHAR* getArtDefineTag() const;				// Exposed to Python
	void setArtDefineTag(const TCHAR* szVal);
	const TCHAR* getMovieDefineTag() const;				// Exposed to Python
	void setMovieDefineTag(const TCHAR* szVal);

/*************************************************************************************************/
/**	New Tag Defs	(BuildingInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getEquipmentPromotion() const;
	int getPrereqBroadAlignment() const;
	int getAlignmentModifier() const;


	//Crime
	int getPrereqPopulation() const;
	int getPrereqCrime() const;
	int getMinCrime() const;
	bool isAutoBuild() const;
	bool isMustMaintain() const;
	bool isCrimeEffect() const;
	bool isEffect() const;
	int getPerCrimeEffectHappyChange() const;
	int getPerCrimeEffectHealthChange() const;
	int getPerCrimeEffectCommerceChange(int i) const;				// Exposed to Python
	int getPerCrimeEffectYieldChange(int i) const;				// Exposed to Python
	int* getPerCrimeEffectCommerceChangeArray() const;
	int* getPerCrimeEffectYieldChangeArray() const;

	/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	int getAlignmentShift() const;
	int getAlignmentShiftModifier() const;
	int getAlignmentShiftTowardsNeutral() const;
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getPrereqBroadEthicalAlignment() const;
	int getEthicalAlignmentModifier() const;
	int getEthicalAlignmentShift() const;
	int getEthicalAlignmentShiftModifier() const;
	int getEthicalAlignmentShiftTowardsNeutral() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/

	int getPotency() const;
	float getPotencyAffinity(int iI) const;
	int getPotencyBonusPrereq(int iI) const;
	int getShielding() const;
	float getShieldingAffinity(int iI) const;
	int getShieldingBonusPrereq(int iI) const;
	int getTrainXPCap(int iI) const;
	float getTrainXPRate(int iI) const;
	float getPerCrimeTrainXPCap(int iI) const;
	float getPerCrimeTrainXPRate(int iI) const;

	int getGlobalPotency() const;
	float getGlobalPotencyAffinity(int iI) const;
	int getGlobalPotencyBonusPrereq(int iI) const;
	int getGlobalShielding() const;
	float getGlobalShieldingAffinity(int iI) const;
	int getGlobalShieldingBonusPrereq(int iI) const;
	int getGlobalTrainXPCap(int iI) const;
	float getGlobalTrainXPRate(int iI) const;

	int getNumPrereqTeamBuildingClassANDs() const;
	int getPrereqTeamBuildingClassAND(int iI) const;
	int getNumPrereqTeamBuildingClassNOTs() const;
	int getPrereqTeamBuildingClassNOT(int iI) const;
	int getNumPrereqTeamBuildingClassORs() const;
	int getPrereqTeamBuildingClassOR(int iI) const;

	int getNumPrereqGlobalBuildingClassANDs() const;
	int getPrereqGlobalBuildingClassAND(int iI) const;
	int getNumPrereqGlobalBuildingClassNOTs() const;
	int getPrereqGlobalBuildingClassNOT(int iI) const;
	int getNumPrereqGlobalBuildingClassORs() const;
	int getPrereqGlobalBuildingClassOR(int iI) const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Buildings: Added by Kael 08/04/2007
	bool isApplyFreePromotionOnMove() const;
	bool isEquipment() const;
	bool isHideUnits() const;
	bool isNoCivicAnger() const;
	bool isRequiresCaster() const;
/*************************************************************************************************/
/**	Aqueduct 	Orbis new tags 	 	Ahwaric		09/09/09	Ahwaric		**/
/*************************************************************************************************/
	bool isCarriesFreshWater() const;
	bool isPrereqNoFreshWater() const;
	/*************************************************************************************************/
/**	Aqueduct END 									**/
/*************************************************************************************************/
	bool isSeeInvisible() const;
	bool isOverflowProduction() const;
	bool isUnhappyProduction() const;
	int getCrime() const;
	int getCrimePerUnhappyModifier() const;
	int getCrimePerUnhealthModifier() const;
	int getFreePromotionPick() const;
	int getGlobalResistEnemyModify() const;
	int getGlobalResistModify() const;
	int getModifyGlobalCounter() const;
	int getPlotRadius() const;
	int getResistMagic() const;
	int getFreeBonus2() const;
	int getFreeBonus3() const;
	int getPrereqTrait() const;
	int getPrereqTrait2() const;
	int getRemovePromotion() const;

	int getSpecialistClassCommerceChange(int i, int j) const;
	int* getSpecialistClassCommerceChangeArray(int i) const;
//FfH: End Add

/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
	int getLocalSpecialistClassCommerceChange(int iSpecialist, int iYield) const;
	int* getLocalSpecialistClassCommerceChangeArray(int iSpecialist) const;
	int getLocalSpecialistClassYieldChange(int iSpecialist, int iYield) const;
	int* getLocalSpecialistClassYieldChangeArray(int iSpecialist) const;
	int getLocalSpecialistClassHappinessChange(int iSpecialist) const;
	int getLocalSpecialistClassHealthChange(int iSpecialist) const;
	int getLocalSpecialistClassCrimeChange(int iSpecialist) const;
	int getLocalSpecialistClassGPPChange(int iSpecialist) const;
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	int getCityCapModifier() const;
	int getGlobalCityCapModifier() const;
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/** MaxCulture					Opera															**/
/*************************************************************************************************/
	bool isNoCultureCap() const;
/*************************************************************************************************/
/** MaxCulture					END																**/
/*************************************************************************************************/

	// Arrays

	int getYieldChange(int i) const;				// Exposed to Python
	int* getYieldChangeArray() const;
	int getYieldModifier(int i) const;;				// Exposed to Python
	int* getYieldModifierArray() const;
	int getPowerYieldModifier(int i) const;				// Exposed to Python
	int* getPowerYieldModifierArray() const;
	int getAreaYieldModifier(int i) const;				// Exposed to Python
	int* getAreaYieldModifierArray() const;
	int getGlobalYieldModifier(int i) const;				// Exposed to Python
	int* getGlobalYieldModifierArray() const;
	int getSeaPlotYieldChange(int i) const;				// Exposed to Python
	int* getSeaPlotYieldChangeArray() const;
	int getRiverPlotYieldChange(int i) const;				// Exposed to Python
	int* getRiverPlotYieldChangeArray() const;
	int getTerrainYieldChange(int i, int j) const;			// Exposed to Python
	int* getTerrainYieldChangeArray(int i) const;
	int getFeatureYieldChange(int i, int j) const;			// Exposed to Python
	int* getFeatureYieldChangeArray(int i) const;
	int getGlobalSeaPlotYieldChange(int i) const;				// Exposed to Python
	int* getGlobalSeaPlotYieldChangeArray() const;


	int getCommerceChange(int i) const;				// Exposed to Python
	int* getCommerceChangeArray() const;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
	int getTradeYieldModifier(int i) const;			// Exposed to Python
	int* getTradeYieldModifierArray() const;
	int getTradeCommerceModifier(int i) const;		// Exposed to Python
	int* getTradeCommerceModifierArray() const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int getObsoleteSafeCommerceChange(int i) const;				// Exposed to Python
	int* getObsoleteSafeCommerceChangeArray() const;
	int getCommerceChangeDoubleTime(int i) const;				// Exposed to Python
	int getCommerceModifier(int i) const;				// Exposed to Python
	int* getCommerceModifierArray() const;
	int getGlobalCommerceModifier(int i) const;				// Exposed to Python
	int* getGlobalCommerceModifierArray() const;
	int getSpecialistExtraCommerce(int i) const;	// Exposed to Python
	int* getSpecialistExtraCommerceArray() const;
	int getStateReligionCommerce(int i) const;				// Exposed to Python
	int* getStateReligionCommerceArray() const;
	int getCommerceHappiness(int i) const;				// Exposed to Python
	int getReligionChange(int i) const;				// Exposed to Python
	int getSpecialistClassCount(int i) const;				// Exposed to Python
	int getFreeSpecialistClassCount(int i) const;				// Exposed to Python
	int getBonusHealthChanges(int i) const;				// Exposed to Python
	int getBonusHappinessChanges(int i) const;				// Exposed to Python
	int getBonusProductionModifier(int i) const;				// Exposed to Python
	int getUnitCombatFreeExperience(int i) const;				// Exposed to Python
	int getDomainFreeExperience(int i) const;						// Exposed to Python
	int getDomainProductionModifier(int i) const;				// Exposed to Python
	int getPrereqAndTechs(int i) const;				// Exposed to Python
	int getPrereqOrBonuses(int i) const;				// Exposed to Python
	int getProductionTraits(int i) const;				// Exposed to Python
	int getHappinessTraits(int i) const;				// Exposed to Python
	int getBuildingHappinessChanges(int i) const;				// Exposed to Python
	int getPrereqNumOfBuildingClass(int i) const;				// Exposed to Python
	int getPrereqBuildingClassAtRange(int i) const;				// Exposed to Python
	int getPrereqImprovementAtRange(int i) const;				// Exposed to Python
	int getPrereqFeatureAtRange(int i) const;				// Exposed to Python
	int getPrereqBonusAtRange(int i) const;				// Exposed to Python
	int getBuildingExclude(int i) const;				// Exposed to Python
	int getFlavorValue(int i) const;				// Exposed to Python
	int getImprovementFreeSpecialistClass(int i) const;				// Exposed to Python

	bool isCommerceFlexible(int i) const;				// Exposed to Python
	bool isCommerceChangeOriginalOwner(int i) const;				// Exposed to Python
	bool isBuildingClassNeededInCity(int i) const;				// Exposed to Python

	int getSpecialistClassYieldChange(int i, int j) const;			// Exposed to Python
	int* getSpecialistClassYieldChangeArray(int i) const;

	int getBonusYieldModifier(int i, int j) const;				// Exposed to Python
	int* getBonusYieldModifierArray(int i) const;
	
	int getBonusCommerceModifier(int i, int j) const;				// Exposed to Python
	int* getBonusCommerceModifierArray(int i) const;
	//PerPopEffect
	int getNumPerPopBonuses() const;
	CityBonuses getPerPopBonus(int iI) const;
	std::list<CityBonuses> listPerPopBonuses();

	// Other

	const CvArtInfoBuilding* getArtInfo() const;
	const CvArtInfoMovie* getMovieInfo() const;
	const TCHAR* getButton() const;
	const TCHAR* getMovie() const;

	// serialization
	void read(FDataStreamBase*);
	void write(FDataStreamBase*);
	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvBuildingInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PUBLIC MEMBER VARIABLES---------------------------------
protected:

	int m_iBuildingClassType;
	int m_iVictoryPrereq;
	int m_iFreeStartEra;
	int m_iMaxStartEra;
	int m_iObsoleteTech;
	int m_iPrereqAndTech;
	int m_iNoBonus;
	int m_iPowerBonus;
	int m_iFreeBonus;
	int m_iNumFreeBonuses;
	int m_iMinLevelAccess;
	int m_iFreeBuildingClass;
	int m_iParentBuildingClass;
	int m_iFreePromotion;
	int m_iCivicOption;
	int m_iAIWeight;
	int m_iProductionCost;
	int m_iHurryCostModifier;
	int m_iHurryAngerModifier;
	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;
	int m_iMinAreaSize;
	int m_iNumCitiesPrereq;
	int m_iNumTeamsPrereq;
	int m_iUnitLevelPrereq;
	int m_iMinLatitude;
	int m_iMaxLatitude;
	int m_iGreatPeopleRateModifier;
	int m_iGreatGeneralRateModifier;
	int m_iDomesticGreatGeneralRateModifier;
	int m_iGlobalGreatPeopleRateModifier;
	int m_iAnarchyModifier;
	int m_iGoldenAgeModifier;
	int m_iGlobalHurryModifier;
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iFreeExperience;
	int m_iGlobalFreeExperience;
/**								----  End Original Code  ----									**/
	float m_iFreeExperience;
	float m_iGlobalFreeExperience;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int m_iFoodKept;
	int m_iAirlift;
	int m_iAirModifier;
	int m_iAirUnitCapacity;
	int m_iNukeModifier;
	int m_iNukeExplosionRand;
	int m_iFreeSpecialist;
	int m_iAreaFreeSpecialist;
	int m_iGlobalFreeSpecialist;
	int m_iHappiness;
	int m_iAreaHappiness;
	int m_iGlobalHappiness;
	int m_iStateReligionHappiness;
	int m_iWorkerSpeedModifier;
	int m_iMilitaryProductionModifier;
	int m_iSpaceProductionModifier;
	int m_iGlobalSpaceProductionModifier;
	int m_iTradeRoutes;
	int m_iCoastalTradeRoutes;
	int m_iGlobalTradeRoutes;
	int m_iTradeRouteModifier;
	int m_iForeignTradeRouteModifier;
	int m_iAssetValue;
	int m_iPowerValue;
	int m_iSpecialBuildingType;
	int m_iAdvisorType;
	int m_iHolyCity;
	int m_iReligionType;
	int m_iStateReligion;
	int m_iPrereqReligion;
	int m_iPrereqFlag;
	int m_iPrereqCorporation;
	int m_iPrereqCivic;
	int m_iFoundsCorporation;
	int m_iGlobalReligionCommerce;
	int m_iGlobalCorporationCommerce;
	int m_iPrereqAndBonus;
	int m_iGreatPeopleUnitClass;
	int m_iGreatPeopleRateChange;
	int m_iConquestProbability;
	int m_iMaintenanceModifier;
	int m_iWarWearinessModifier;
	int m_iGlobalWarWearinessModifier;
	int m_iEnemyWarWearinessModifier;
	int m_iHealRateChange;
	int m_iHealth;
	int m_iAreaHealth;
	int m_iGlobalHealth;
	int m_iGlobalPopulationChange;
	int m_iFreeTechs;
	int m_iDefenseModifier;
	int m_iBombardDefenseModifier;
	int m_iAllCityDefenseModifier;
	int m_iEspionageDefenseModifier;
	int m_iMissionType;
	int m_iVoteSourceType;

	float m_fVisibilityPriority;

	bool m_bTeamShare;
	bool m_bWater;
	bool m_bRiver;
	bool m_bPower;
	bool m_bDirtyPower;
	bool m_bAreaCleanPower;
	bool m_bAreaBorderObstacle;
	bool m_bForceTeamVoteEligible;
	bool m_bCapital;
	bool m_bGovernmentCenter;
	bool m_bGoldenAge;
	bool m_bFoodProduction;
	bool m_bMapCentering;
	bool m_bNoUnhappiness;
	bool m_bNoUnhealthiness;
	CvString m_szPyHelp;

/************************************************************************************************/
/* Influence Driven War                   06/08/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool m_bFixedBorders;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	bool m_bNoForeignTradeRoutes;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
/*************************************************************************************************/
/* MultiBonus							  06/08/10									Valkrionn    */
/*                                                                                               */
/*				Causes certain building tags to use each instance of a resource                  */
/*************************************************************************************************/
	bool m_bUseMultiBonuses;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	bool m_bNoUnhealthyPopulation;
	bool m_bBuildingOnlyHealthy;
	bool m_bNeverCapture;
	bool m_bNukeImmune;
	bool m_bPrereqReligion;
	bool m_bPrereqNoReligion;
	bool m_bCenterInCity;
	bool m_bStateReligion;
	bool m_bAllowsNukes;

	CvString m_szConstructSound;
	CvString m_szArtDefineTag;
	CvString m_szMovieDefineTag;

/*************************************************************************************************/
/**	New Tag Defs	(BuildingInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iEquipmentPromotion;
	int m_iPrereqBroadAlignment;
	int m_iAlignmentModifier;

/*************************************************************************************************/
/**	Building prereq Alignments				07/04/10								Snarko		**/
/**																								**/
/**							Allows buildings to require alignments								**/
/*************************************************************************************************/
	int m_iNumPrereqAlignments;
	int m_iNumPrereqEthicalAlignments;
/*************************************************************************************************/
/**	Building prereq Alignments					END												**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	int m_iAlignmentShift;
	int m_iAlignmentShiftModifier;
	int m_iAlignmentShiftTowardsNeutral;
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iPrereqBroadEthicalAlignment;
	int m_iEthicalAlignmentModifier;
	int m_iEthicalAlignmentShift;
	int m_iEthicalAlignmentShiftModifier;
	int m_iEthicalAlignmentShiftTowardsNeutral;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	//Crime
	int m_iPrereqPopulation;
	int m_iPrereqCrime;
	int m_iMinCrime;
	bool m_bAutoBuild;
	bool m_bMustMaintain;
	bool m_bCrimeEffect;
	bool m_bEffect;
	int m_iPerCrimeEffectHappyChange;
	int m_iPerCrimeEffectHealthChange;
	int* m_piPerCrimeEffectYieldChange;
	int* m_piPerCrimeEffectCommerceChange;

	int m_iPotency;
	float* m_pafPotencyAffinity;
	int* m_paiPotencyBonusPrereq;
	int m_iShielding;
	float* m_pafShieldingAffinity;
	int* m_paiShieldingBonusPrereq;
	float* m_pafTrainXPCap;
	float* m_pafTrainXPRate;
	float* m_pafPerCrimeTrainXPCap;
	float* m_pafPerCrimeTrainXPRate;

	int m_iGlobalPotency;
	float* m_pafGlobalPotencyAffinity;
	int* m_paiGlobalPotencyBonusPrereq;
	int m_iGlobalShielding;
	float* m_pafGlobalShieldingAffinity;
	int* m_paiGlobalShieldingBonusPrereq;
	float* m_pafGlobalTrainXPCap;
	float* m_pafGlobalTrainXPRate;

	int m_iNumPrereqTeamBuildingClassANDs;
	int m_iNumPrereqTeamBuildingClassNOTs;
	int m_iNumPrereqTeamBuildingClassORs;
	int* m_piPrereqTeamBuildingClassANDs;
	int* m_piPrereqTeamBuildingClassNOTs;
	int* m_piPrereqTeamBuildingClassORs;

	int m_iNumPrereqGlobalBuildingClassANDs;
	int m_iNumPrereqGlobalBuildingClassNOTs;
	int m_iNumPrereqGlobalBuildingClassORs;
	int* m_piPrereqGlobalBuildingClassANDs;
	int* m_piPrereqGlobalBuildingClassNOTs;
	int* m_piPrereqGlobalBuildingClassORs;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Buildings: Added by Kael 08/04/2007
	bool m_bApplyFreePromotionOnMove;
	bool m_bEquipment;
	bool m_bHideUnits;
	bool m_bNoCivicAnger;
	bool m_bRequiresCaster;
/*************************************************************************************************/
/**	Aqueduct 	Orbis new tags 	 	Ahwaric		09/09/09	Ahwaric		**/
/*************************************************************************************************/
	bool m_bCarriesFreshWater;
	bool m_bPrereqNoFreshWater;
	/*************************************************************************************************/
/**	Aqueduct END 									**/
/*************************************************************************************************/
	bool m_bSeeInvisible;
	bool m_bOverflowProduction;
	bool m_bUnhappyProduction;
	int m_iCrime;
	int m_iCrimePerTurn;
	int m_iCrimePerUnhappyModifier;
	int m_iCrimePerUnhealthModifier;
	int m_iFreePromotionPick;
	int m_iFreeBonus2;
	int m_iFreeBonus3;
	int m_iGlobalResistEnemyModify;
	int m_iGlobalResistModify;
	int m_iModifyGlobalCounter;
	int m_iPlotRadius;
	int m_iPrereqTrait;
	int m_iPrereqTrait2;
	int m_iRemovePromotion;
	int m_iResistMagic;

	int** m_ppaiSpecialistClassCommerceChange;
//FfH: End Add

/*************************************************************************************************/
/**	GWSLocalSpecialist																	Milaga	**/
/** Buildings can change give bonuses to specialists in only one city							**/
/*************************************************************************************************/
	int **m_paaiLocalSpecialistClassYieldChange;
	int **m_paaiLocalSpecialistClassCommerceChange;
	int *m_paiLocalSpecialistClassHappinessChange;
	int *m_paiLocalSpecialistClassHealthChange;
	int* m_paiLocalSpecialistClassCrimeChange;
	int *m_paiLocalSpecialistClassGPPChange;
/*************************************************************************************************/
/**	GWSLocalSpecialist																		END	**/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	int m_iCityCapModifier;
	int m_iGlobalCityCapModifier;
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

/*************************************************************************************************/
/** MaxCulture					Opera															**/
/*************************************************************************************************/
	bool m_bNoCultureCap;
/*************************************************************************************************/
/** MaxCulture					END																**/
/*************************************************************************************************/

	// Arrays

	int* m_piPrereqAndTechs;
	int* m_piPrereqOrBonuses;
	int* m_piProductionTraits;
	int* m_piHappinessTraits;
	int* m_piSeaPlotYieldChange;
	int* m_piRiverPlotYieldChange;
	int** m_ppaiTerrainYieldChange;
	int** m_ppaiFeatureYieldChange;
	int* m_piGlobalSeaPlotYieldChange;
	int* m_piYieldChange;
	int* m_piYieldModifier;
	int* m_piPowerYieldModifier;
	int* m_piAreaYieldModifier;
	int* m_piGlobalYieldModifier;
	int* m_piCommerceChange;
	int* m_piObsoleteSafeCommerceChange;
	int* m_piCommerceChangeDoubleTime;
	int* m_piCommerceModifier;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**						Allows buildings to modify trade Yield and Commerces					**/
/*************************************************************************************************/
	int* m_piTradeYieldModifier;
	int* m_piTradeCommerceModifier;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int* m_piGlobalCommerceModifier;
	int* m_piSpecialistExtraCommerce;
	int* m_piStateReligionCommerce;
	int* m_piCommerceHappiness;
	int* m_piReligionChange;
	int* m_piSpecialistClassCount;
	int* m_piFreeSpecialistClassCount;
	int* m_piBonusHealthChanges;
	int* m_piBonusHappinessChanges;
	int* m_piBonusProductionModifier;
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int* m_piUnitCombatFreeExperience;
	int* m_piDomainFreeExperience;
/**								----  End Original Code  ----									**/
	float* m_piUnitCombatFreeExperience;
	float* m_piDomainFreeExperience;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int* m_piDomainProductionModifier;
	int* m_piBuildingHappinessChanges;
	int* m_piPrereqNumOfBuildingClass;
	int* m_piPrereqBuildingClassAtRange;
	int* m_piPrereqImprovementAtRange;
	int* m_piPrereqFeatureAtRange;
	int* m_piPrereqBonusAtRange;
	int* m_piBuildingExclude;
	int* m_piFlavorValue;
	int* m_piImprovementFreeSpecialistClass;

	bool* m_pbCommerceFlexible;
	bool* m_pbCommerceChangeOriginalOwner;
	bool* m_pbBuildingClassNeededInCity;

	int** m_ppaiSpecialistClassYieldChange;
	int** m_ppaiBonusYieldModifier;
	int** m_ppaiBonusCommerceModifier;

/*************************************************************************************************/
/**	Building prereq Alignments				07/04/10								Snarko		**/
/**																								**/
/**							Allows buildings to require alignments								**/
/*************************************************************************************************/
	int* m_piPrereqAlignments;
	int* m_piPrereqEthicalAlignments;
/*************************************************************************************************/
/**	Building prereq Alignments					END												**/
/*************************************************************************************************/
//PerPopEffect
	int m_iNumPerPopBonuses;
	std::list <CityBonuses> m_cbPerPopBonuses;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpecialBuildingInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpecialBuildingInfo :
	public CvInfoBase
{

	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvSpecialBuildingInfo();
	virtual ~CvSpecialBuildingInfo();

	int getObsoleteTech( void ) const;					// Exposed to Python
	int getTechPrereq( void ) const;						// Exposed to Python
	int getTechPrereqAnyone( void ) const;						// Exposed to Python

	bool isValid( void ) const;									// Exposed to Python

	// Arrays

	int getProductionTraits(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvSpecialBuildingInfo* pClassInfo = NULL , CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iObsoleteTech;
	int m_iTechPrereq;
	int m_iTechPrereqAnyone;

	bool m_bValid;

	// Arrays

	int* m_piProductionTraits;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvBuildingClassInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBuildingClassInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvBuildingClassInfo();
	virtual ~CvBuildingClassInfo();

	int getMaxGlobalInstances() const;				// Exposed to Python
	int getMaxTeamInstances() const;				// Exposed to Python
	int getMaxPlayerInstances() const;				// Exposed to Python
	int getExtraPlayerInstances() const;				// Exposed to Python
	int getDefaultBuildingIndex() const;				// Exposed to Python
	void setDefaultBuildingIndex(int i);

	bool isNoLimit() const;				// Exposed to Python
	bool isMonument() const;				// Exposed to Python

/*************************************************************************************************/
/**	New Tag Defs	(BuildingClassInfos)	10/18/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	bool isUnique() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	// Arrays

	int getVictoryThreshold(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvBuildingClassInfo* pClassInfo = NULL , CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iMaxGlobalInstances;
	int m_iMaxTeamInstances;
	int m_iMaxPlayerInstances;
	int m_iExtraPlayerInstances;
	int m_iDefaultBuildingIndex;

	bool m_bNoLimit;
	bool m_bMonument;
/*************************************************************************************************/
/**	New Tag Defs	(BuildingClassInfos)	10/18/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	bool m_bUnique;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	// Arrays

	int* m_piVictoryThreshold;

};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvRiverInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRiverInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvRiverInfo();
	virtual ~CvRiverInfo();

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvRiverModelInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRiverModelInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvRiverModelInfo();
	DllExport virtual ~CvRiverModelInfo();

	DllExport const TCHAR* getModelFile() const;				// Exposed to Python
	DllExport void setModelFile(const TCHAR* szVal);				// The model filename
	DllExport const TCHAR* getBorderFile() const;				// Exposed to Python
	DllExport void setBorderFile(const TCHAR* szVal);				// The model filename

	DllExport int getTextureIndex() const;
	DllExport const TCHAR* getDeltaString() const;				//Exposed to Python
	DllExport const TCHAR* getConnectString() const;				// Exposed to Python
	DllExport const TCHAR* getRotateString() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvRiverModelInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	CvString m_szModelFile;					// The model filename
	CvString m_szBorderFile;				// The border filename

	TCHAR		m_szDeltaString[32];		// The delta type
	TCHAR		m_szConnectString[32];		// The connections this cell makes ( N S E W NE NW SE SW )
	TCHAR		m_szRotateString[32];		// The possible rotations for this cell ( 0 90 180 270 )
	int			m_iTextureIndex;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvRouteModelInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRouteModelInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvRouteModelInfo();
	DllExport virtual ~CvRouteModelInfo();

	DllExport RouteTypes getRouteType() const;				// The route type

	DllExport const TCHAR* getModelFile() const;				// Exposed to Python
	DllExport void setModelFile(const TCHAR* szVal);				// The model filename
	DllExport const TCHAR* getLateModelFile() const;				// Exposed to Python
	DllExport void setLateModelFile(const TCHAR* szVal);				// The model filename
	DllExport const TCHAR* getModelFileKey() const;				// Exposed to Python
	DllExport void setModelFileKey(const TCHAR* szVal);				// The model filename Key

	DllExport bool isAnimated() const;

	DllExport const TCHAR* getConnectString() const;				// Exposed to Python
	DllExport const TCHAR* getModelConnectString() const;			// Exposed to Python
	DllExport const TCHAR* getRotateString() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvRouteModelInfo* pClassInfo = NULL , CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	RouteTypes	m_eRouteType;			// The route type

	CvString m_szModelFile;				// The model filename
	CvString m_szLateModelFile;				// The model filename
	CvString m_szModelFileKey;			// The model file key reference
	bool m_bAnimated;

	TCHAR		m_szConnectString[32];	// The connections this cell makes ( N S E W NE NW SE SW )
	TCHAR		m_szModelConnectString[32];	// The connections this model makes ( N S E W NE NW SE SW )
	TCHAR		m_szRotateString[32];	// The possible rotations for this cell ( 0 90 180 270 )
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCivilizationInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoCivilization;
class CvCivilizationInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvCivilizationInfo();
	DllExport virtual ~CvCivilizationInfo();
	DllExport virtual void reset();

	DllExport int getDefaultPlayerColor() const;				// Expose to Python
	DllExport int getArtStyleType() const;				// Expose to Python
	DllExport int getUnitArtStyleType() const;         // Expose to Python
	DllExport int getNumCityNames() const;				// Expose to Python
	DllExport int getNumLeaders() const;				// Exposed to Python - the number of leaders the Civ has, this is needed so that random leaders can be generated easily
	DllExport int getSelectionSoundScriptId() const;				// Expose to Python
	DllExport int getActionSoundScriptId() const;				// Expose to Python

	DllExport bool isAIPlayable() const;				// Expose to Python
	DllExport bool isPlayable() const;				// Expose to Python
	DllExport bool isNoCrimeCiv() const;				// Expose to Python
	/*************************************************************************************************/
/**	New Tag Defs	(CivilizationInfos)		01/12/09								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	void setAIPlayable(bool bPlayable);
	void setPlayable(bool bPlayable);
	bool isLimitedSelection() const;
	int getFeatureHealthPercentChange(int i) const;
	int getFeatureYieldChanges(int i, int j) const;
	int getImprovementYieldChanges(int i, int j) const;
	int getTerrainYieldChanges(int i, int j) const;
	int getPeakYieldChange(int i) const;

	//ClimateSystem:
	int getFormClimateZoneType() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	std::wstring pyGetShortDescription(uint uiForm) { return getShortDescription(uiForm); }				// Exposed to Python
	DllExport const wchar* getShortDescription(uint uiForm = 0);
	DllExport const wchar* getShortDescriptionKey() const;				// Exposed to Python
	std::wstring pyGetShortDescriptionKey() { return getShortDescriptionKey(); }				// Exposed to Python

	std::wstring pyGetAdjective(uint uiForm) { return getAdjective(uiForm);  }	// Exposed to Python
	DllExport const wchar* getAdjective(uint uiForm = 0);
	DllExport const wchar* getAdjectiveKey() const;				// Exposed to Python
	std::wstring pyGetAdjectiveKey() { return getAdjectiveKey(); }				// Exposed to Python

	DllExport const TCHAR* getFlagTexture() const;
	DllExport const TCHAR* getArtDefineTag() const;
	DllExport void setArtDefineTag(const TCHAR* szVal);
	// Arrays

	DllExport CvString getCivilizationBuildingArtDefines(int i) const;				// Exposed to Python
	DllExport int getCivilizationBuildings(int i) const;				// Exposed to Python
	DllExport int getCivilizationSpecialists(int i) const;				// Exposed to Python
	DllExport int getSpecialistArtstyle(int i) const;				// Exposed to Python
	DllExport int getCivilizationImprovements(int i) const;				// Exposed to Python
	DllExport int getCivilizationUnits(int i) const;				// Exposed to Python
	DllExport int getCivilizationFreeUnitsClass(int i) const;				// Exposed to Python
	DllExport int getCivilizationInitialCivics(int i) const;				// Exposed to Python

	DllExport bool isLeaders(int i) const;				// Exposed to Python
	DllExport bool isSecondaryLeaders(int i) const;				// Exposed to Python
	DllExport bool isPediaLeaders(int i) const;				// Exposed to Python
	DllExport bool isCivilizationFreeBuildingClass(int i) const;				// Exposed to Python
	DllExport bool isCivilizationFreeTechs(int i) const;				// Exposed to Python
	DllExport bool isCivilizationDisableTechs(int i) const;				// Exposed to Python

	DllExport std::string getCityNames(int i) const;				// Exposed to Python

	int getFlavorValue(int i) const;				// Exposed to Python

	DllExport const CvArtInfoCivilization* getArtInfo() const;
	DllExport const TCHAR* getButton() const;

	DllExport int getDerivativeCiv() const;																// Exposed to Python
	void setDerivativeCiv(int iCiv);

//InterfaceUpgrade: Better Pedia - Added by Grey Fox 04/18/2008
	DllExport const TCHAR* getImage() const;
	DllExport void setImage(const TCHAR* szVal);

//Interface Upgrade: Better Pedia - End Add

//FfH: Added by Kael 08/07/2007
	int getCivTrait() const;
	int getDefaultRace() const;
	int getHero() const;
	bool isMaintainFeatures(int i) const;
//FfH: End Add
/*************************************************************************************************/
/**	Civilization Flavors				07/07/10										Snarko	**/
/**																								**/
/**							Making civilization flavors,										**/
/**			for helping AI with things we can't really add in a non-hardcoded way				**/
/*************************************************************************************************/
	int getCivFlavorValue(int i) const;				// Exposed to Python
/*************************************************************************************************/
/**	Civilization Flavors					END													**/
/*************************************************************************************************/

	bool read(CvXMLLoadUtility* pXML);
	DllExport bool readPass2(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvCivilizationInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	void copyNonDefaultsReadPass2(CvCivilizationInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
	DllExport void read(FDataStreamBase* stream);
	DllExport void write(FDataStreamBase* stream);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iDefaultPlayerColor;
	int m_iArtStyleType;
	int m_iUnitArtStyleType;  // FlavorUnits by Impaler[WrG]
	int m_iNumCityNames;
	int m_iNumLeaders;				 // the number of leaders the Civ has, this is needed so that random leaders can be generated easily
	int m_iSelectionSoundScriptId;
	int m_iActionSoundScriptId;
	int m_iDerivativeCiv;

	bool m_bAIPlayable;
	bool m_bPlayable;
	bool m_bNoCrimeCiv;

	CvString m_szArtDefineTag;
	CvWString m_szShortDescriptionKey;
	CvWString m_szAdjectiveKey;
	// Arrays
	CvString* m_piCivilizationBuildingArtDefines;
	int* m_piCivilizationBuildings;
	int* m_piCivilizationSpecialists;
	int* m_piSpecialistArtstyles;
	int* m_piCivilizationImprovements;
	int* m_piCivilizationUnits;
	int* m_piCivilizationFreeUnitsClass;
	int* m_piCivilizationInitialCivics;

	bool* m_pbLeaders;
	bool* m_pbSecondaryLeaders;
	bool* m_pbCivilizationFreeBuildingClass;
	bool* m_pbCivilizationFreeTechs;
	bool* m_pbCivilizationDisableTechs;

	int* m_piFlavorValue;

//InterfaceUpgrade: Better Pedia - Added by Grey Fox 04/18/2008
	CvString m_szCivilizationImage;
//Interface Upgrade: Better Pedia - End Add

//FfH: Added by Kael 08/07/2007
	int m_iCivTrait;
	int m_iDefaultRace;
	int m_iHero;
	bool* m_pbMaintainFeatures;
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(CivilizationInfos)		01/12/09								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	bool m_bLimitedSelection;
	int* m_piFeatureHealthPercentChanges;
	int** m_ppiFeatureYieldChanges;
	int** m_ppiImprovementYieldChanges;
	int** m_ppiTerrainYieldChanges;
	int* m_paiPeakYieldChange;

	//ClimateSystem:
	int m_iFormClimateZoneType;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Civilization Flavors				07/07/10										Snarko	**/
/**																								**/
/**							Making civilization flavors,										**/
/**			for helping AI with things we can't really add in a non-hardcoded way				**/
/*************************************************************************************************/
	int* m_piCivFlavorValue;
/*************************************************************************************************/
/**	Civilization Flavors					END													**/
/*************************************************************************************************/

	CvString* m_paszCityNames;

	mutable std::vector<CvWString> m_aszShortDescription;
	mutable std::vector<CvWString> m_aszAdjective;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvVictoryInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvVictoryInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvVictoryInfo();
	virtual ~CvVictoryInfo();

	int getPopulationPercentLead() const;				// Exposed to Python
	int getLandPercent() const;				// Exposed to Python
	int getMinLandPercent() const;				// Exposed to Python
	int getReligionPercent() const;				// Exposed to Python
	int getCityCulture() const;				// Exposed to Python
	int getNumCultureCities() const;				// Exposed to Python
	int getTotalCultureRatio() const;				// Exposed to Python
	int getVictoryDelayTurns() const;				// Exposed to Python

	bool isTargetScore() const;				// Exposed to Python
	bool isEndScore() const;					// Exposed to Python
	bool isConquest() const;					// Exposed to Python
	bool isDiploVote() const;					// Exposed to Python
	DllExport bool isPermanent() const;					// Exposed to Python

	const char* getMovie() const;
/*************************************************************************************************/
/**	New Tag Defs	(VictoryInfos)			01/16/09								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getNumLinkedVictories() const;
	int getLinkedVictory(int iI) const;
	bool readPass2(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Improved AI								18/01/12								Snarko		**/
/**							Teaching the AI to go for victories.								**/
/*************************************************************************************************/
	int getAIVictoryWeight(int i) const;
/*************************************************************************************************/
/**	Improved AI								END													**/
/*************************************************************************************************/

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvVictoryInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	void copyNonDefaultsReadPass2(CvVictoryInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iPopulationPercentLead;
	int m_iLandPercent;
	int m_iMinLandPercent;
	int m_iReligionPercent;
	int m_iCityCulture;
	int m_iNumCultureCities;
	int m_iTotalCultureRatio;
	int m_iVictoryDelayTurns;

	bool m_bTargetScore;
	bool m_bEndScore;
	bool m_bConquest;
	bool m_bDiploVote;
	bool m_bPermanent;

	CvString m_szMovie;
/*************************************************************************************************/
/**	New Tag Defs	(VictoryInfos)			01/16/09								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int* m_piLinkedVictories;
	int m_iNumLinkedVictories;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Improved AI								18/01/12								Snarko		**/
/**							Teaching the AI to go for victories.								**/
/*************************************************************************************************/
	int* m_piAIVictoryTypes;
/*************************************************************************************************/
/**	Improved AI								END													**/
/*************************************************************************************************/

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvHurryInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvHurryInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
	public:

		CvHurryInfo();
		virtual ~CvHurryInfo();

		int getGoldPerProduction() const;					// Exposed to Python
		int getCulturePerProduction() const;					// Exposed to Python
		int getProductionPerPopulation() const;		// Exposed to Python

		bool isAnger() const;											// Exposed to Python

		bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
		void copyNonDefaults(CvHurryInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PUBLIC MEMBER VARIABLES---------------------------------
	protected:

		int m_iGoldPerProduction;
		int m_iCulturePerProduction;
		int m_iProductionPerPopulation;

		bool m_bAnger;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvHandicapInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvHandicapInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvHandicapInfo();
	virtual ~CvHandicapInfo();

	int getFreeWinsVsBarbs() const;				// Exposed to Python
	int getAnimalAttackProb() const;				// Exposed to Python
	int getStartingLocationPercent() const;				// Exposed to Python
	int getAdvancedStartPointsMod() const;				// Exposed to Python
	int getStartingGold() const;				// Exposed to Python
	int getFreeUnits() const;				// Exposed to Python
	int getUnitCostPercent() const;				// Exposed to Python
	int getResearchPercent() const;				// Exposed to Python
	int getDistanceMaintenancePercent() const;				// Exposed to Python
	int getNumCitiesMaintenancePercent() const;				// Exposed to Python
	int getMaxNumCitiesMaintenance() const;				// Exposed to Python
	int getColonyMaintenancePercent() const;				// Exposed to Python
	int getMaxColonyMaintenance() const;				// Exposed to Python
	int getCorporationMaintenancePercent() const;				// Exposed to Python
	int getCivicUpkeepPercent() const;				// Exposed to Python
	int getInflationPercent() const;				// Exposed to Python
	int getHealthBonus() const;				// Exposed to Python
	int getHappyBonus() const;				// Exposed to Python
	int getAttitudeChange() const;				// Exposed to Python
	int getNoTechTradeModifier() const;				// Exposed to Python
	int getTechTradeKnownModifier() const;				// Exposed to Python
	int getTilesPerAnimal() const;				// Exposed to Python
	int getTilesPerOrc() const;				// Exposed to Python
	int getWaterTilesPerOrc() const;				// Exposed to Python
	int getUnownedTilesPerBarbarianCity() const;				// Exposed to Python
	int getBarbarianCityCreationTurnsElapsed() const;				// Exposed to Python
	int getBarbarianCityCreationProb() const;				// Exposed to Python
	int getAnimalCombatModifier() const;				// Exposed to Python
	int getBarbarianCombatModifier() const;				// Exposed to Python
	int getAIAnimalCombatModifier() const;				// Exposed to Python
	int getAIBarbarianCombatModifier() const;				// Exposed to Python

	int getStartingDefenseUnits() const;						// Exposed to Python
	int getStartingWorkerUnits() const;							// Exposed to Python
	int getStartingExploreUnits() const;						// Exposed to Python
	int getAIStartingUnitMultiplier() const;				// Exposed to Python
	int getAIStartingDefenseUnits() const;				// Exposed to Python
	int getAIStartingWorkerUnits() const;				// Exposed to Python
	int getAIStartingExploreUnits() const;				// Exposed to Python
	int getBarbarianInitialDefenders() const;				// Exposed to Python
	int getAIDeclareWarProb() const;								// Exposed to Python
	int getAIWorkRateModifier() const;				// Exposed to Python
	int getAIGrowthPercent() const;				// Exposed to Python
	int getAITrainPercent() const;				// Exposed to Python
	int getAIWorldTrainPercent() const;				// Exposed to Python
	int getAIConstructPercent() const;				// Exposed to Python
	int getAIWorldConstructPercent() const;				// Exposed to Python
	int getAICreatePercent() const;				// Exposed to Python
	int getAIWorldCreatePercent() const;				// Exposed to Python
	int getAICivicUpkeepPercent() const;				// Exposed to Python
	int getAIUnitCostPercent() const;				// Exposed to Python
	int getAIUnitSupplyPercent() const;				// Exposed to Python
	int getAIUnitUpgradePercent() const;				// Exposed to Python
	int getAIInflationPercent() const;				// Exposed to Python
	int getAIWarWearinessPercent() const;				// Exposed to Python
	int getAIPerEraModifier() const;						// Exposed to Python
	int getAIAdvancedStartPercent() const;						// Exposed to Python
	int getNumGoodies() const;				// Exposed to Python

//FfH Improvements: Added by Kael 08/07/2007
	int getAIFreeXP() const;
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(HandicapInfos)			12/27/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getWaterTilesPerAnimal() const;
	int getAnimalEscalationTurnsElapsed() const;
	int getPercentDemonsPerEvilPlot() const;
	int getDemonPerTurnKnownTechsPercent() const;
	int getDemonGlobalCounterFreeXPPercent() const;
	int getPercentDemonsPerEvilPlotPerGlobalCounter() const;
	int getTilesPerLairDemon() const;
	int getDemonBonus() const;
	int getAIDemonBonus() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	// Arrays

	int getGoodies(int i) const;				// Exposed to Python
	int isFreeTechs(int i) const;				// Exposed to Python
	int isAIFreeTechs(int i) const;				// Exposed to Python

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvHandicapInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iFreeWinsVsBarbs;
	int m_iAnimalAttackProb;
	int m_iStartingLocationPercent;
	int m_iAdvancedStartPointsMod;
	int m_iStartingGold;
	int m_iFreeUnits;
	int m_iUnitCostPercent;
	int m_iResearchPercent;
	int m_iDistanceMaintenancePercent;
	int m_iNumCitiesMaintenancePercent;
	int m_iMaxNumCitiesMaintenance;
	int m_iColonyMaintenancePercent;
	int m_iMaxColonyMaintenance;
	int m_iCorporationMaintenancePercent;
	int m_iCivicUpkeepPercent;
	int m_iInflationPercent;
	int m_iHealthBonus;
	int m_iHappyBonus;
	int m_iAttitudeChange;
	int m_iNoTechTradeModifier;
	int m_iTechTradeKnownModifier;
	int m_iTilesPerAnimal;
	int m_iTilesPerOrc;
	int m_iWaterTilesPerOrc;
	int m_iUnownedTilesPerBarbarianCity;
	int m_iBarbarianCityCreationTurnsElapsed;
	int m_iBarbarianCityCreationProb;
	int m_iAnimalCombatModifier;
	int m_iBarbarianCombatModifier;
	int m_iAIAnimalCombatModifier;
	int m_iAIBarbarianCombatModifier;

	int m_iStartingDefenseUnits;
	int m_iStartingWorkerUnits;
	int m_iStartingExploreUnits;
	int m_iAIStartingUnitMultiplier;
	int m_iAIStartingDefenseUnits;
	int m_iAIStartingWorkerUnits;
	int m_iAIStartingExploreUnits;
	int m_iBarbarianInitialDefenders;
	int m_iAIDeclareWarProb;
	int m_iAIWorkRateModifier;
	int m_iAIGrowthPercent;
	int m_iAITrainPercent;
	int m_iAIWorldTrainPercent;
	int m_iAIConstructPercent;
	int m_iAIWorldConstructPercent;
	int m_iAICreatePercent;
	int m_iAIWorldCreatePercent;
	int m_iAICivicUpkeepPercent;
	int m_iAIUnitCostPercent;
	int m_iAIUnitSupplyPercent;
	int m_iAIUnitUpgradePercent;
	int m_iAIInflationPercent;
	int m_iAIWarWearinessPercent;
	int m_iAIPerEraModifier;
	int m_iAIAdvancedStartPercent;
	int m_iNumGoodies;

//FfH Improvements: Added by Kael 08/07/2007
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iAIFreeXP;
/**								----  End Original Code  ----									**/
	float m_iAIFreeXP;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(HandicapInfos)			12/27/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iWaterTilesPerAnimal;
	int m_iAnimalEscalationTurnsElapsed;
	int m_iPercentDemonsPerEvilPlot;
	int m_iPercentDemonsPerEvilPlotPerGlobalCounter;
	int m_iTilesPerLairDemon;
	int m_iDemonGlobalCounterFreeXPPercent;
	int m_iDemonPerTurnKnownTechsPercent;
	int m_iDemonBonus;
	int m_iAIDemonBonus;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	CvString m_szHandicapName;

	// Arrays

	int* m_piGoodies;

	bool* m_pbFreeTechs;
	bool* m_pbAIFreeTechs;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvGameSpeedInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGameSpeedInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvGameSpeedInfo();
	virtual ~CvGameSpeedInfo();

	int getGrowthPercent() const;						// Exposed to Python
	int getTrainPercent() const;						// Exposed to Python
	int getConstructPercent() const;				// Exposed to Python
	int getCreatePercent() const;						// Exposed to Python
	int getResearchPercent() const;					// Exposed to Python
	int getBuildPercent() const;						// Exposed to Python
	int getImprovementPercent() const;			// Exposed to Python
	int getGreatPeoplePercent() const;			// Exposed to Python
	int getAnarchyPercent() const;					// Exposed to Python
	int getBarbPercent() const;							// Exposed to Python
	int getFeatureProductionPercent() const;				// Exposed to Python
	int getUnitDiscoverPercent() const;			// Exposed to Python
	int getUnitHurryPercent() const;				// Exposed to Python
	int getUnitTradePercent() const;				// Exposed to Python
	int getUnitGreatWorkPercent() const;		// Exposed to Python
	int getGoldenAgePercent() const;				// Exposed to Python
	int getHurryPercent() const;						// Exposed to Python
	int getHurryConscriptAngerPercent() const;	// Exposed to Python
	int getInflationOffset() const;					// Exposed to Python
	int getInflationPercent() const;				// Exposed to Python
	int getVictoryDelayPercent() const;				// Exposed to Python
	int getNumTurnIncrements() const;				// Exposed to Python
/*************************************************************************************************/
/**	New Tag Defs	(GameSpeedInfos)		12/27/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getLairSpawnChance() const;
	int getTurnsPerLairCycle() const;
	int getBarbSpawnDelay() const;

	GameTurnInfo& getGameTurnInfo(int iIndex) const;				// Exposed to Python
	void allocateGameTurnInfos(const int iSize);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvGameSpeedInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iGrowthPercent;
	int m_iTrainPercent;
	int m_iConstructPercent;
	int m_iCreatePercent;
	int m_iResearchPercent;
	int m_iBuildPercent;
	int m_iImprovementPercent;
	int m_iGreatPeoplePercent;
	int m_iAnarchyPercent;
	int m_iBarbPercent;
	int m_iFeatureProductionPercent;
	int m_iUnitDiscoverPercent;
	int m_iUnitHurryPercent;
	int m_iUnitTradePercent;
	int m_iUnitGreatWorkPercent;
	int m_iGoldenAgePercent;
	int m_iHurryPercent;
	int m_iHurryConscriptAngerPercent;
	int m_iInflationOffset;
	int m_iInflationPercent;
	int m_iVictoryDelayPercent;
	int m_iNumTurnIncrements;
/*************************************************************************************************/
/**	New Tag Defs	(GameSpeedInfos)		12/27/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iLairSpawnChance;
	int m_iTurnsPerLairCycle;
	int m_iBarbSpawnDelay;

	CvString m_szGameSpeedName;
	GameTurnInfo* m_pGameTurnInfo;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTurnTimerInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTurnTimerInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvTurnTimerInfo();
	virtual ~CvTurnTimerInfo();

	int getBaseTime() const;				// Exposed to Python
	int getCityBonus() const;				// Exposed to Python
	int getUnitBonus() const;				// Exposed to Python
	int getFirstTurnMultiplier() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvTurnTimerInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iBaseTime;
	int m_iCityBonus;
	int m_iUnitBonus;
	int m_iFirstTurnMultiplier;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvBuildInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBuildInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvBuildInfo();
	virtual ~CvBuildInfo();

	int getTime() const;				// Exposed to Python
	int getCost() const;				// Exposed to Python
/*************************************************************************************************/
/**	BuildXP									7/17/10									Valkrionn	**/
/**																								**/
/**									Allows Builds to grant XP									**/
/*************************************************************************************************/
	int getXPValue() const;				// Exposed to Python
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	LinkedBuilds							7/18/10									Valkrionn	**/
/**																								**/
/**		Creates a list of Builds, which are executed before the main build if reqs are met		**/
/*************************************************************************************************/
	int getNumLinkedBuilds() const;
	BuildTypes getLinkedBuilds(int iI) const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int getTechPrereq() const;				// Exposed to Python
	int getImprovementClass() const;				// Exposed to Python
	int getRoute() const;				// Exposed to Python
	DllExport int getEntityEvent() const;				// Exposed to Python
	DllExport int getMissionType() const;				// Exposed to Python
	void setMissionType(int iNewType);

	bool isKill() const;				// Exposed to Python
	bool isStandard() const;				// Exposed to Python

	// Arrays

	int getFeatureTech(int i) const;				// Exposed to Python
	int getFeatureTime(int i) const;				// Exposed to Python
	int getFeatureProduction(int i) const;				// Exposed to Python

	bool isFeatureRemove(int i) const;				// Exposed to Python
/*************************************************************************************************/
/**	New Tag Defs	(BuildInfos)			12/07/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getTechDiscount(int iI) const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvBuildInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	void copyNonDefaultsReadPass2(CvBuildInfo* pClassInfo = NULL , CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iTime;
	int m_iCost;
	int m_iTechPrereq;
	int m_iImprovement;
	int m_iRoute;
	int m_iEntityEvent;
	int m_iMissionType;
/*************************************************************************************************/
/**	BuildXP									7/17/10									Valkrionn	**/
/**																								**/
/**									Allows Builds to grant XP									**/
/*************************************************************************************************/
	float m_iXPValue;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	LinkedBuilds							7/18/10									Valkrionn	**/
/**																								**/
/**		Creates a list of Builds, which are executed before the main build if reqs are met		**/
/*************************************************************************************************/
	int m_iNumLinkedBuilds;
	int* m_piLinkedBuilds;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	bool m_bKill;
	bool m_bStandard;

	// Arrays

	int* m_paiFeatureTech;
	int* m_paiFeatureTime;
	int* m_paiFeatureProduction;

	bool* m_pabFeatureRemove;
/*************************************************************************************************/
/**	New Tag Defs	(BuildInfos)			12/07/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int* m_paiTechDiscount;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvGoodyInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGoodyInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvGoodyInfo();
	virtual ~CvGoodyInfo();

/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR				20/06/10										Snarko	**/
/**																								**/
/**							Moving explore lair results into SDK								**/
/*************************************************************************************************/
	bool isGoodyClassType(int i) const;				// Exposed to Python
	int getWeight() const;				// Exposed to Python
	int getDamageType() const;				// Exposed to Python
	int getDamageLimit() const;				// Exposed to Python
	int getBonusType() const;				// Exposed to Python
	const char* getPythonCallback() const;
	const char* getPythonPrereq() const;
	int getPrereqAlignment() const;				// Exposed to Python
	int getDestroyLairChance() const;				// Exposed to Python
	bool isAnyPromotion() const;				// Exposed to Python
	bool isUnique() const;				// Exposed to Python
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR					END													**/
/*************************************************************************************************/

	int getGold() const;				// Exposed to Python
	int getGoldRand1() const;				// Exposed to Python
	int getGoldRand2() const;				// Exposed to Python
	int getMapOffset() const;				// Exposed to Python
	int getMapRange() const;				// Exposed to Python
	int getMapProb() const;				// Exposed to Python
	int getExperience() const;				// Exposed to Python
	int getHealing() const;				// Exposed to Python
	int getDamagePrereq() const;				// Exposed to Python
	int getBarbarianUnitProb() const;				// Exposed to Python
	int getMinBarbarians() const;				// Exposed to Python
	int getUnitClassType() const;				// Exposed to Python
	int getBarbarianUnitClass() const;				// Exposed to Python
/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
	int getBarbarianSpawnGroup() const;				// Exposed to Python
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(GoodyInfos)			07/29/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int getScience() const;
	int getScienceRand1() const;
	int getScienceRand2() const;
	int getBarbarianCivilization() const;
	bool readPass3();
	int getPromotionAdd(int iI) const;
	int getNumPromotionAdds() const;
	int getPromotionRemove(int iI) const;
	int getNumPromotionRemoves() const;
	int getMinTurnsElapsed() const;
	int getMaxTurnsElapsed() const;
	int getBarbarianCivilizationVectorSize();
	CvString getBarbarianCivilizationVectorElement(int i);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	bool isTech() const;				// Exposed to Python
	bool isBad() const;				// Exposed to Python
/*************************************************************************************************/
/**	Balancing							05/10/12										Snarko	**/
/**																								**/
/**					Making the more OP results require certain techs							**/
/*************************************************************************************************/
	int getPrereqTech() const;				// Exposed to Python
	int getPrereqEra() const;				// Exposed to Python
/*************************************************************************************************/
/**	Balancing								END													**/
/*************************************************************************************************/

	const TCHAR* getSound() const;				// Exposed to Python
	void setSound(const TCHAR* szVal);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvGoodyInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR				20/06/10										Snarko	**/
/**																								**/
/**							Moving explore lair results into SDK								**/
/*************************************************************************************************/
	bool* m_pbGoodyClassTypes;
	int m_iWeight;
	int m_iDamageType;
	int m_iDamageLimit;
	int m_iBonusType;
	CvString m_szPythonCallback;
	CvString m_szPythonPrereq;
	int m_iPrereqAlignment;
	int m_iDestroyLairChance;
	bool m_bAnyPromotion;
	bool m_bUnique;
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR					END													**/
/*************************************************************************************************/
	int m_iGold;
	int m_iGoldRand1;
	int m_iGoldRand2;
	int m_iMapOffset;
	int m_iMapRange;
	int m_iMapProb;
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iExperience;
/**								----  End Original Code  ----									**/
	float m_iExperience;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int m_iHealing;
	int m_iDamagePrereq;
	int m_iBarbarianUnitProb;
	int m_iMinBarbarians;
	int m_iUnitClassType;
	int m_iBarbarianUnitClass;
/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
	int m_iBarbarianSpawnGroup;
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/

	bool m_bTech;
/*************************************************************************************************/
/**	New Tag Defs	(GoodyInfos)			07/29/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iScience;
	int m_iScienceRand1;
	int m_iScienceRand2;
	int m_iBarbarianCivilization;
	int m_iNumPromotionAdds;
	int* m_piPromotionAdds;
	int m_iNumPromotionRemoves;
	int* m_piPromotionRemoves;
	int m_iMinTurnsElapsed;
	int m_iMaxTurnsElapsed;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Balancing							05/10/12										Snarko	**/
/**																								**/
/**					Making the more OP results require certain techs							**/
/*************************************************************************************************/
	int m_iTechPrereq;
	int m_iEraPrereq;
/*************************************************************************************************/
/**	Balancing								END													**/
/*************************************************************************************************/
	bool m_bBad;

	CvString m_szSound;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvRouteInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvRouteInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvRouteInfo();
	virtual ~CvRouteInfo();

	int getAdvancedStartCost() const;				// Exposed to Python
	int getAdvancedStartCostIncrease() const;				// Exposed to Python

	int getValue() const;								// Exposed to Python
	int getMovementCost() const;				// Exposed to Python
	int getFlatMovementCost() const;		// Exposed to Python
	int getPrereqBonus() const;					// Exposed to Python

	// Arrays

	int getYieldChange(int i) const;				// Exposed to Python
	int getTechMovementChange(int i) const;				// Exposed to Python
	int getPrereqOrBonus(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvRouteInfo* pClassInfo = NULL , CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;

	int m_iValue;
	int m_iMovementCost;
	int m_iFlatMovementCost;
	int m_iPrereqBonus;

	// Arrays

	int* m_piYieldChange;
	int* m_piTechMovementChange;
	int* m_piPrereqOrBonuses;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvImprovementBonusInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvImprovementBonusInfo :
	public CvInfoBase
{

friend class CvImprovementInfo;
friend class CvXMLLoadUtility;

	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvImprovementBonusInfo();
	virtual ~CvImprovementBonusInfo();

	int getDiscoverRand() const;				// Exposed to Python

	bool isBonusMakesValid() const;				// Exposed to Python
	bool isBonusTrade() const;				// Exposed to Python

	int getYieldChange(int i) const;				// Exposed to Python

/*************************************************************************************************/
/** SpreadBonus     Opera       28/08/09         imported by Valkrionn	09.26.09                **/
/*************************************************************************************************/
	int getSpreadRand() const;
/*************************************************************************************************/
/** SpreadBonus                 END                                                             **/
/*************************************************************************************************/

	// Serialize

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iDiscoverRand;

	bool m_bBonusMakesValid;
	bool m_bBonusTrade;

/*************************************************************************************************/
/** SpreadBonus     Opera       28/08/09        imported by Valkrionn	09.26.09                **/
/*************************************************************************************************/
	int m_iSpreadRand;
/*************************************************************************************************/
/** SpreadBonus                 END                                                             **/
/*************************************************************************************************/

	// Arrays

	int* m_piYieldChange;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvImprovementInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoImprovement;
class CvImprovementInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvImprovementInfo();
	virtual ~CvImprovementInfo();

	int getAdvancedStartCost() const;				// Exposed to Python
	int getAdvancedStartCostIncrease() const;				// Exposed to Python

	int getTilesPerGoody() const;				// Exposed to Python
	int getGoodyUniqueRange() const;				// Exposed to Python
	int getFeatureGrowthProbability() const;				// Exposed to Python
	int getUpgradeTime() const;				// Exposed to Python
	int getExploreDelay() const;				// Exposed to Python
	int getLairTier() const;                // Exposed to Python
	int getMaxAirlift() const;                // Exposed to Python
	int getMaxOutgoingAirlift() const;                // Exposed to Python

	int getAirBombDefense() const;				// Exposed to Python
	int getDefenseModifier() const;				// Exposed to Python
	int getHappiness() const;				// Exposed to Python
	int getPillageGold() const;				// Exposed to Python
	int getImprovementClassPillage() const;				// Exposed to Python
	void setImprovementPillage(int i);
	int getImprovementClassUpgrade() const;				// Exposed to Python
	void setImprovementUpgrade(int i);
	
	int getImprovementClass() const;				// Exposed to Python
	void setImprovementClass(int i);

	bool isActsAsCity() const;				// Exposed to Python
	bool isHillsMakesValid() const;				// Exposed to Python
/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
	bool isPeakMakesValid() const;				// Exposed to Python
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/
	bool isFreshWaterMakesValid() const;				// Exposed to Python
	bool isRiverSideMakesValid() const;				// Exposed to Python
	bool isNoFreshWater() const;				// Exposed to Python
	bool isRequiresFlatlands() const;				// Exposed to Python
	DllExport bool isRequiresRiverSide() const;				// Exposed to Python
	bool isRequiresIrrigation() const;				// Exposed to Python
	bool isCarriesIrrigation() const;				// Exposed to Python
	bool isRequiresFeature() const;				// Exposed to Python
	bool isWater() const;				// Exposed to Python
	DllExport bool isGoody() const;				// Exposed to Python
	bool isPermanent() const;				// Exposed to Python
	bool isOutsideBorders() const;				// Exposed to Python
/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	int getMinimumDistance() const;                // Exposed to Python
	int getCultureRange() const;				// Exposed to Python
	void setCultureRange(int i);
	int getCultureControlStrength() const;				// Exposed to Python
	void setCultureControlStrength(int i);
	int getCultureCenterBonus() const;				// Exposed to Python
	void setCultureCenterBonus(int i);
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/

	const TCHAR* getArtDefineTag() const;
	void setArtDefineTag(const TCHAR* szVal);

	int getWorldSoundscapeScriptId() const;
/*************************************************************************************************/
/**	New Tag Defs	(ImprovementInfos)		12/27/08								Xienwolf	**/
/**								Added to by Valkrionn, 1/15/10									**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getSpawnUnitCiv() const;
	int getSpawnAtOnceLimit() const;
	int getLairCreationWeight() const;
/*************************************************************************************************/
/** Hinterlands				  				07/11/09								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	int getLairCreationWeightTechs(int i) const;
	int getLairUpgradeTechs(int i) const;
/*************************************************************************************************/
/**											END													**/
/*************************************************************************************************/
	bool isExplorable() const;
	bool isFreshWater() const;
	/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR				20/06/10										Snarko	**/
/**																								**/
/**							Moving explore lair results into SDK								**/
/*************************************************************************************************/
	bool isGoodyClassType(int i) const;
	int getNoBadExplore() const;
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR					END													**/
/*************************************************************************************************/
	bool isFort() const;
	bool isSpawnOnlyForOwner() const;
	int getBasePlotCounterModify() const;
	int getSpawnUnitTypeVectorSize();
	CvString getSpawnUnitTypeVectorElement(int i);
/*************************************************************************************************/
/**	LairGuardians							7/17/10									Valkrionn	**/
/**																								**/
/**				Allows for lairs to spawn a unit on creation, but spawn others normally			**/
/*************************************************************************************************/
	int getImmediateSpawnUnitTypeVectorSize();
	CvString getImmediateSpawnUnitTypeVectorElement(int i);
	int getSpawnGroupTypeVectorSize();
	CvString getSpawnGroupTypeVectorElement(int i);
	int getImmediateSpawnGroupTypeVectorSize();
	CvString getImmediateSpawnGroupTypeVectorElement(int i);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int getPrereqCivilizationVectorSize();
	CvString getPrereqCivilizationVectorElement(int i);
	int getSpawnUnitCivVectorSize();
	CvString getSpawnUnitCivVectorElement(int i);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	// Arrays

	int getPrereqNatureYield(int i) const;				// Exposed to Python
	int* getPrereqNatureYieldArray();
	int getYieldChange(int i) const;				// Exposed to Python
	int* getYieldChangeArray();
	int getRiverSideYieldChange(int i) const;				// Exposed to Python
	int* getRiverSideYieldChangeArray();
	int getHillsYieldChange(int i) const;				// Exposed to Python
	int* getHillsYieldChangeArray();
	int getIrrigatedYieldChange(int i) const;				// Exposed to Python
	int* getIrrigatedYieldChangeArray();				// For Moose - CvWidgetData XXX

	bool getTerrainMakesValid(int i) const;				// Exposed to Python
	bool hasFeatureMakesValid() const;
	bool getFeatureMakesValid(int i) const;				// Exposed to Python
/*************************************************************************************************/
/**	Feature spread		 				Ahwaric	23.09.09		**/
/*************************************************************************************************/
	bool getAllowsFeature(int i) const;				// Exposed to Python
/*************************************************************************************************/
/**	Feature spread	END									**/
/*************************************************************************************************/

	int getTechYieldChanges(int i, int j) const;				// Exposed to Python
	int* getTechYieldChangesArray(int i);
	int getRouteYieldChanges(int i, int j) const;				// Exposed to Python
	int* getRouteYieldChangesArray(int i);				// For Moose - CvWidgetData XXX

	int getImprovementBonusYield(int i, int j) const;				// Exposed to Python
	bool isImprovementBonusMakesValid(int i) const;				// Exposed to Python
	bool isImprovementBonusTrade(int i) const;				// Exposed to Python
	int getImprovementBonusDiscoverRand(int i) const;				// Exposed to Python

/*************************************************************************************************/
/** SpreadBonus     Opera       28/08/09        imported by Valkrionn	09.26.09                **/
/*************************************************************************************************/
	int getImprovementBonusSpreadRand(int i) const;
/*************************************************************************************************/
/** SpreadBonus                 END                                                             **/
/*************************************************************************************************/

	// Other

	const TCHAR* getButton() const;
	DllExport const CvArtInfoImprovement* getArtInfo() const;

//FfH Improvements: Added by Kael 08/07/2007
	bool isRequiresPeak() const;
	bool isUnique() const;
	int getAppearanceProbability() const;
	int getSpawnUnitChancePercentMod() const;
	int getSpawnGroupChancePercentMod() const;
	int getHealRateChange() const;
	int getRange() const;
	int getRangeDefenseModifier() const;
	int getBonusConvert() const;
/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
	int getFreeSpecialistClass() const;					// Exposed to Python
	int getWorkingCityCrime() const;					// Exposed to Python
	/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/
	int getFeatureUpgrade() const;
	int getPrereqCivilization() const;
	const TCHAR* getPythonAtRange() const;
	const TCHAR* getPythonOnMove() const;
	int getSpawnUnitType() const;
/*************************************************************************************************/
/**	LairGuardians							7/17/10									Valkrionn	**/
/**																								**/
/**				Allows for lairs to spawn a unit on creation, but spawn others normally			**/
/*************************************************************************************************/
	int getImmediateSpawnUnitType() const;
	int getSpawnGroupType() const;
	int getImmediateSpawnGroupType() const;
	int getNumSpawnPromotions() const;							// Exposed to Python
	int getNumGuardianPromotions() const;						// Exposed to Python
	int getSpawnPromotions(int iI) const;						// Exposed to Python
	int getGuardianPromotions(int iI) const;					// Exposed to Python
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int getVisibilityChange() const;
	bool readPass3();
//FfH: End Add

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvImprovementInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	void copyNonDefaultsReadPass2(CvImprovementInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/




	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iAdvancedStartCost;
	int m_iAdvancedStartCostIncrease;

	int m_iTilesPerGoody;
	int m_iGoodyUniqueRange;
	int m_iFeatureGrowthProbability;
	int m_iUpgradeTime;
	int m_iExploreDelay;

	int m_iAirBombDefense;
	int m_iDefenseModifier;
	int m_iHappiness;
	int m_iPillageGold;
	int m_iImprovementPillage;
	int m_iImprovementUpgrade;
	int m_iImprovementClass;
	bool m_bActsAsCity;
	bool m_bHillsMakesValid;
/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
	bool m_bPeakMakesValid;
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/
	bool m_bFreshWaterMakesValid;
	bool m_bRiverSideMakesValid;
	bool m_bNoFreshWater;
	bool m_bRequiresFlatlands;
	bool m_bRequiresRiverSide;
	bool m_bRequiresIrrigation;
	bool m_bCarriesIrrigation;
	bool m_bRequiresFeature;
	bool m_bWater;
	bool m_bGoody;
	bool m_bPermanent;
	bool m_bOutsideBorders;
	int m_iLairTier;
	int m_iMaxAirlift;
	int m_iMaxOutgoingAirlift;
	/*************************************************************************************************/
/**	Improvements Mods by Jeckel		imported by Ahwaric	20.09.09 | Valkrionn	09.24.09		**/
/*************************************************************************************************/
	int m_iMinimumDistance;
	int m_iCultureRange;
	int m_iCultureControlStrength;
	int m_iCultureCenterBonus;
/*************************************************************************************************/
/**	Improvements Mods	END								**/
/*************************************************************************************************/

	CvString m_szArtDefineTag;


	int m_iWorldSoundscapeScriptId;

//FfH Improvements: Added by Kael 08/07/2007
	bool m_bRequiresPeak;
	bool m_bUnique;
	int m_iAppearanceProbability;
	int m_iSpawnUnitChancePercentMod;
	int m_iSpawnGroupChancePercentMod;
	int m_iHealRateChange;
	int m_iRange;
	int m_iRangeDefenseModifier;
	int m_iBonusConvert;
/*************************************************************************************************/
/**	Statesmen								02/05/10											**/
/**																								**/
/**						Allows improvements to grant specific specialists						**/
/*************************************************************************************************/
	int m_iFreeSpecialistClass;
	int m_iWorkingCityCrime;
/*************************************************************************************************/
/**	Statesmen								END													**/
/*************************************************************************************************/
	int m_iFeatureUpgrade;
	int m_iPrereqCivilization;
	CvString m_szPythonAtRange;
	CvString m_szPythonOnMove;
	int m_iSpawnUnitType;
/*************************************************************************************************/
/**	LairGuardians							7/17/10									Valkrionn	**/
/**																								**/
/**				Allows for lairs to spawn a unit on creation, but spawn others normally			**/
/*************************************************************************************************/
	int m_iImmediateSpawnUnitType;
	std::vector<CvString> m_aszExtraXML4forPass3;
	int m_iSpawnGroupType;
	std::vector<CvString> m_aszExtraXML5forPass3;
	int m_iImmediateSpawnGroupType;
	std::vector<CvString> m_aszExtraXML6forPass3;

	int m_iNumSpawnPromotions;
	int m_iNumGuardianPromotions;
	int* m_piSpawnPromotions;
	int* m_piGuardianPromotions;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int m_iVisibilityChange;

	std::vector<CvString> m_aszExtraXML2forPass3;
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(ImprovementInfos)		12/27/08								Xienwolf	**/
/**								Added to by Valkrionn, 1/15/10									**/
/**							ExtraXML field defined globally for use elsewhere in CvInfos		**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	std::vector<CvString> m_aszExtraXML3forPass3;
	int m_iSpawnUnitCiv;
	int m_iSpawnAtOnceLimit;
	int m_iLairCreationWeight;
/*************************************************************************************************/
/** Hinterlands				  				07/11/09								Valkrionn	**/
/**																								**/
/*************************************************************************************************/
	int* m_piLairCreationWeightTechs;
	int* m_piLairUpgradeTechs;
/*************************************************************************************************/
/**											END													**/
/*************************************************************************************************/
	int m_bExplorable;
	int m_bFreshWater;
	/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR				20/06/10										Snarko	**/
/**																								**/
/**							Moving explore lair results into SDK								**/
/*************************************************************************************************/
	bool* m_pbGoodyClassTypes;
	int m_iNoBadExplore;
/*************************************************************************************************/
/**	MISSION_EXPLORE_LAIR					END													**/
/*************************************************************************************************/
	int m_bFort;
	int m_bSpawnOnlyForOwner;
	int m_iBasePlotCounterModify;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	// Arrays

	int* m_piPrereqNatureYield;
	int* m_piYieldChange;
	int* m_piRiverSideYieldChange;
	int* m_piHillsYieldChange;
	int* m_piIrrigatedChange;

	bool* m_pbTerrainMakesValid;
	bool* m_pbFeatureMakesValid;
/*************************************************************************************************/
/**	Feature spread		 				Ahwaric	23.09.09		**/
/*************************************************************************************************/
	bool* m_pbAllowsFeature;
/*************************************************************************************************/
/**	Feature spread	END									**/
/*************************************************************************************************/

	int** m_ppiTechYieldChanges;
	int** m_ppiRouteYieldChanges;

	CvImprovementBonusInfo* m_paImprovementBonus;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvBonusClassInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvBonusClassInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvBonusClassInfo();
	virtual ~CvBonusClassInfo();

	int getUniqueRange() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvBonusClassInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iUniqueRange;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvBonusInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoBonus;
class CvBonusInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvBonusInfo();
	virtual ~CvBonusInfo();

	int getBonusClassType() const;			// Exposed to Python
	int getChar() const;								// Exposed to Python
	void setChar(int i);								// Exposed to Python
	int getTechReveal() const;					// Exposed to Python
	int getTechCityTrade() const;				// Exposed to Python
	int getTechObsolete() const;				// Exposed to Python
	int getAITradeModifier() const;			// Exposed to Python
	int getAIObjective() const;			// Exposed to Python
	int getHealth() const;							// Exposed to Python
	int getHappiness() const;						// Exposed to Python
	int getMinAreaSize() const;					// Exposed to Python
	int getMinLatitude() const;					// Exposed to Python
	int getMaxLatitude() const;					// Exposed to Python
	int getPlacementOrder() const;			// Exposed to Python
	int getConstAppearance() const;			// Exposed to Python
	int getRandAppearance1() const;			// Exposed to Python
	int getRandAppearance2() const;			// Exposed to Python
	int getRandAppearance3() const;			// Exposed to Python
	int getRandAppearance4() const;			// Exposed to Python
	int getPercentPerPlayer() const;		// Exposed to Python
	int getTilesPer() const;						// Exposed to Python
	int getMinLandPercent() const;			// Exposed to Python
	int getUniqueRange() const;					// Exposed to Python
	int getGroupRange() const;					// Exposed to Python
	int getGroupRand() const;						// Exposed to Python

	bool isOneArea() const;							// Exposed to Python
	bool isHills() const;								// Exposed to Python
/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
	bool isPeaks() const;								// Exposed to Python
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/
	bool isFlatlands() const;						// Exposed to Python
	bool isNoRiverSide() const;					// Exposed to Python
	bool isDiscoverable() const;					// Exposed to Python
	bool isNormalize() const;						// Exposed to Python

	const TCHAR* getArtDefineTag() const;
	void setArtDefineTag(const TCHAR* szVal);

//FfH: Added by Kael 08/16/2007
	bool isModifierPerBonus() const;
	int getBadAttitude() const;
	int getDamageType() const;
	int getDiscoverRandModifier() const;
	int getFreePromotion() const;
	int getGreatPeopleRateModifier() const;
	int getHealChange() const;
	int getHealChangeEnemy() const;
	int getMaintenanceModifier() const;
	int getMutateChance() const;
	int getResearchModifier() const;
	bool readPass3();
//FfH: End Add
/*************************************************************************************************/
/**	New Tag Defs	(BonusInfos)			05/31/09								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getFreePromotionVectorSize();
	CvString getFreePromotionVectorElement(int i);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

	// Arrays

	int getYieldChange(int i) const;				// Exposed to Python
	int* getYieldChangeArray();				// Exposed to Python
	
	int getYieldModifier(int i) const;				// Exposed to Python
	int* getYieldModifierArray();				// Exposed to Python

	int getCommerceModifier(int i) const;				// Exposed to Python
	int* getCommerceModifierArray();				// Exposed to Python

	int getImprovementChange(int i) const;

	bool isTerrain(int i) const;				// Exposed to Python
	bool isFeature(int i) const;				// Exposed to Python
	bool isFeatureTerrain(int i) const;				// Exposed to Python

	// Other

	const TCHAR* getButton() const; // Exposed to Python
	DllExport const CvArtInfoBonus* getArtInfo() const; // Exposed to Python

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvBonusInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PUBLIC MEMBER VARIABLES---------------------------------

protected:

	int m_iBonusClassType;
	int m_iChar;
	int m_iTechReveal;
	int m_iTechCityTrade;
	int m_iTechObsolete;
	int m_iAITradeModifier;
	int m_iAIObjective;
	int m_iHealth;
	int m_iHappiness;
	int m_iMinAreaSize;
	int m_iMinLatitude;
	int m_iMaxLatitude;
	int m_iPlacementOrder;
	int m_iConstAppearance;
	int m_iRandAppearance1;
	int m_iRandAppearance2;
	int m_iRandAppearance3;
	int m_iRandAppearance4;
	int m_iPercentPerPlayer;
	int m_iTilesPer;
	int m_iMinLandPercent;
	int m_iUniqueRange;
	int m_iGroupRange;
	int m_iGroupRand;

	bool m_bOneArea;
	bool m_bHills;
/*************************************************************************************************/
/**	Mountain Mod by NeverMind 		imported by Ahwaric	19.09.09		**/
/*************************************************************************************************/
	bool m_bPeaks;
/*************************************************************************************************/
/**	Mountain Mod	END									**/
/*************************************************************************************************/
	bool m_bFlatlands;
	bool m_bNoRiverSide;
	bool m_bDiscoverable;
	bool m_bNormalize;

	CvString m_szArtDefineTag;

//FfH: Added by Kael 08/16/2007
	bool m_bModifierPerBonus;
	int m_iBadAttitude;
	int m_iDamageType;
	int m_iDiscoverRandModifier;
	int m_iFreePromotion;
	int m_iGreatPeopleRateModifier;
	int m_iHealChange;
	int m_iHealChangeEnemy;
	int m_iMaintenanceModifier;
	int m_iMutateChance;
	int m_iResearchModifier;
//FfH: End Add

	// Arrays

	int* m_piYieldChange;
	int* m_piYieldModifier;
	int* m_piCommerceModifier;
	int* m_piImprovementChange;

	bool* m_pbTerrain;
	bool* m_pbFeature;
	bool* m_pbFeatureTerrain;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvFeatureInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoFeature;
class CvFeatureInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvFeatureInfo();
	virtual ~CvFeatureInfo();

/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	int isMist() const;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/

	int getMovementCost() const;							// Exposed to Python
	int getSeeThroughChange() const;					// Exposed to Python
	int getHealthPercent() const;							// Exposed to Python
	int getAppearanceProbability() const;			// Exposed to Python
	int getDisappearanceProbability() const;	// Exposed to Python
	int getGrowthProbability() const;					// Exposed to Python
	int getDefenseModifier() const;						// Exposed to Python
	int getAdvancedStartRemoveCost() const;						// Exposed to Python
	int getTurnDamage() const;						// Exposed to Python
	const int getDamageLimit() const;
	const int getDamageType() const;

	bool isNoCoast() const;						// Exposed to Python
	bool isNoRiver() const;						// Exposed to Python
	bool isNoAdjacent() const;				// Exposed to Python
	bool isRequiresFlatlands() const;	// Exposed to Python
	bool isRequiresRiver() const;			// Exposed to Python
/*************************************************************************************************/
/**	Features expanded						Ahwaric	04/10/09	**/
/*************************************************************************************************/
	bool isRequiresFreshwater() const;			// Exposed to Python
	int getTerrainConvert() const;
/*************************************************************************************************/
/**										END		**/
/*************************************************************************************************/
	bool isAddsFreshWater() const;		// Exposed to Python
	bool isImpassable() const;				// Exposed to Python
	bool isNoCity() const;						// Exposed to Python
	bool isNoImprovement() const;			// Exposed to Python
	bool isVisibleAlways() const;			// Exposed to Python
	bool isNukeImmune() const;			// Exposed to Python
	const TCHAR* getOnUnitChangeTo() const;

	const TCHAR* getArtDefineTag() const;
	void setArtDefineTag(const TCHAR* szTag);

	int getWorldSoundscapeScriptId() const;

	const TCHAR* getEffectType() const;
	int getEffectProbability() const;

//FfH: Added by Kael 08/26/2007
	bool isFlammable() const;
	int getFeatureUpgrade() const;
	int getPrereqStateReligion() const;
	const TCHAR* getPythonOnMove() const;
	int getRequireResist() const;
	bool readPass2(CvXMLLoadUtility* pXML);
//FfH: End Add

	// Arrays

	int getYieldChange(int i) const;						// Exposed to Python
	int getRiverYieldChange(int i) const;				// Exposed to Python
	int getHillsYieldChange(int i) const;				// Exposed to Python
	int get3DAudioScriptFootstepIndex(int i) const;

	bool isTerrain(int i) const;								// Exposed to Python
	int getNumVarieties() const;

	// Other

	DllExport const CvArtInfoFeature* getArtInfo() const;
	const TCHAR* getButton() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvFeatureInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	void copyNonDefaultsReadPass2(CvFeatureInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

/*************************************************************************************************/
/**	Sidar Mist 								25/06/10								Grey Fox	**/
/*************************************************************************************************/
	int m_bMist;
	int m_iFeatureMist;
/*************************************************************************************************/
/**	END                                                                   						**/
/*************************************************************************************************/
	int m_iMovementCost;
	int m_iSeeThroughChange;
	int m_iHealthPercent;
	int m_iAppearanceProbability;
	int m_iDisappearanceProbability;
	int m_iGrowthProbability;
	int m_iDefenseModifier;
	int m_iAdvancedStartRemoveCost;
	int m_iTurnDamage;
	int m_iDamageLimit;
	int m_iDamageType;

	bool m_bNoCoast;
	bool m_bNoRiver;
	bool m_bNoAdjacent;
	bool m_bRequiresFlatlands;
	bool m_bRequiresRiver;
/*************************************************************************************************/
/**	Features expanded						Ahwaric	04/10/09	**/
/*************************************************************************************************/
	bool m_bRequiresFreshwater;
	int m_iTerrainConvert;
/*************************************************************************************************/
/**										END		**/
/*************************************************************************************************/
	bool m_bAddsFreshWater;
	bool m_bImpassable;
	bool m_bNoCity;
	bool m_bNoImprovement;
	bool m_bVisibleAlways;
	bool m_bNukeImmune;
	CvString m_szOnUnitChangeTo;

	int m_iWorldSoundscapeScriptId;

	CvString m_szEffectType;
	int m_iEffectProbability;

//FfH: Added by Kael 08/26/2007
	bool m_bFlammable;
	int m_iFeatureUpgrade;
	int m_iPrereqStateReligion;
	int m_iRequireResist;
	CvString m_szPythonOnMove;
//FfH: End Add

	// Arrays

	int* m_piYieldChange;
	int* m_piRiverYieldChange;
	int* m_piHillsYieldChange;
	int* m_pi3DAudioScriptFootstepIndex;

	bool* m_pbTerrain;

private:

	CvString m_szArtDefineTag;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCommerceInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCommerceInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvCommerceInfo();
	virtual ~CvCommerceInfo();

	int getChar() const;				// Exposed to Python
	void setChar(int i);
	int getInitialPercent() const;				// Exposed to Python
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	int getTradeModifier() const;				// Exposed to Python
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int getInitialHappiness() const;				// Exposed to Python
	int getAIWeightPercent() const;				// Exposed to Python

	bool isFlexiblePercent() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvCommerceInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iChar;
	int m_iInitialPercent;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	int m_iTradeModifier;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
	int m_iInitialHappiness;
	int m_iAIWeightPercent;

	bool m_bFlexiblePercent;

};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvYieldInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvYieldInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvYieldInfo();
	virtual ~CvYieldInfo();

	int getChar() const;				// Exposed to Python
	void setChar(int i);
	int getHillsChange() const;				// Exposed to Python
	int getPeakChange() const;				// Exposed to Python
	int getLakeChange() const;				// Exposed to Python
	int getCityChange() const;				// Exposed to Python
	int getPopulationChangeOffset() const;				// Exposed to Python
	int getPopulationChangeDivisor() const;				// Exposed to Python
	int getMinCity() const;				// Exposed to Python
	int getTradeModifier() const;				// Exposed to Python
	int getGoldenAgeYield() const;				// Exposed to Python
	int getGoldenAgeYieldThreshold() const;				// Exposed to Python
	int getAIWeightPercent() const;				// Exposed to Python
	int getColorType() const;				// Exposed to Python

	// Arrays

	const TCHAR* getSymbolPath(int i) const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvYieldInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iChar;
	int m_iHillsChange;
	int m_iPeakChange;
	int m_iLakeChange;
	int m_iCityChange;
	int m_iPopulationChangeOffset;
	int m_iPopulationChangeDivisor;
	int m_iMinCity;
	int m_iTradeModifier;
	int m_iGoldenAgeYield;
	int m_iGoldenAgeYieldThreshold;
	int m_iAIWeightPercent;
	int m_iColorType;

	CvString* m_paszSymbolPath;

};

// FlavourMod: Added by Jean Elcard (ClimateSystem)
class CvTerrainClassInfo :
	public CvInfoBase
{
public:

	CvTerrainClassInfo();
	virtual ~CvTerrainClassInfo();

	int getDefaultTemperature() const;
	int getDefaultHumidity() const;
	int getNaturalTerrain() const;
	int getHellTerrain() const;

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();

protected:

	int m_iDefaultTemperature;
	int m_iDefaultHumidity;
	int m_iNaturalTerrain;
	int m_iHellTerrain;
};
// FlavourMod: End Add


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTerrainInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoTerrain;
class CvTerrainInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvTerrainInfo();
	virtual ~CvTerrainInfo();

	int getMovementCost() const;				// Exposed to Python
	int getSeeFromLevel() const;				// Exposed to Python
	int getSeeThroughLevel() const;			// Exposed to Python
	int getBuildModifier() const;				// Exposed to Python
	int getDefenseModifier() const;			// Exposed to Python

	bool isWater() const;								// Exposed to Python
	bool isImpassable() const;					// Exposed to Python
	bool isFound() const;								// Exposed to Python
	bool isFoundCoast() const;					// Exposed to Python
	bool isFoundFreshWater() const;			// Exposed to Python
	bool isHell() const;					// Exposed to Python

	//FfH: Added by Kael 08/02/2007
	void setArtDefineTag2(const TCHAR* szTag);
	bool isNormalize() const;
	//FfH: End Add

	DllExport const TCHAR* getArtDefineTag() const;
	void setArtDefineTag(const TCHAR* szTag);

	int getWorldSoundscapeScriptId() const;

	// Arrays

	int getYield(int i) const;				// Exposed to Python
	int getRiverYieldChange(int i) const;				// Exposed to Python
	int getHillsYieldChange(int i) const;				// Exposed to Python
	int get3DAudioScriptFootstepIndex(int i) const;

	// Other

	const CvArtInfoTerrain* getArtInfo() const;
	const TCHAR* getButton() const;

//FlavourMod: Added by Jean Elcard (ClimateSystem)
	int getTerrainClassType() const;
//FlavourMod: End Add

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvTerrainInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iMovementCost;
	int m_iSeeFromLevel;
	int m_iSeeThroughLevel;
	int m_iBuildModifier;
	int m_iDefenseModifier;

	bool m_bWater;
	bool m_bImpassable;
	bool m_bFound;
	bool m_bFoundCoast;
	bool m_bFoundFreshWater;
	bool m_bHell;

	int m_iWorldSoundscapeScriptId;

//FfH: Added by Kael 08/02/2007
	bool m_bNormalize;
/*************************************************************************************************/
/**	CivPlotMods								03/23/09								Jean Elcard	**/
/**																								**/
/**			Obsolete FfH Code. Replaced with TerrainYieldChanges in CvCivilizationInfo.			**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iCivilizationYieldType;
	int m_iPlotCounterDown;
	int m_iTerrainDown;
	int m_iPlotCounterUp;
	int m_iTerrainUp;
	int* m_piCivilizationYieldChange;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	CivPlotMods								END													**/
/*************************************************************************************************/
//FfH: End Add

	// Arrays

	int* m_piYields;
	int* m_piRiverYieldChange;
	int* m_piHillsYieldChange;
	int* m_pi3DAudioScriptFootstepIndex;

//FlavourMod: Added by Jean Elcard (ClimateSystem)
	int m_iTerrainClassType;
//FlavourMod: End Add


private:

	CvString m_szArtDefineTag;

//FfH: Added by Kael 12/20/2007
	CvString m_szArtDefineTag2;
//FfH: End Add

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvInterfaceModeInfo (ADD to Python)
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvInterfaceModeInfo :
	public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvInterfaceModeInfo();
	DllExport virtual ~CvInterfaceModeInfo();

	DllExport int getCursorIndex() const;
	DllExport int getMissionType() const;

	DllExport bool getVisible() const;
	DllExport bool getGotoPlot() const;
	DllExport bool getHighlightPlot() const;
	DllExport bool getSelectType() const;
	DllExport bool getSelectAll() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvInterfaceModeInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iCursorIndex;
	int m_iMissionType;

	bool m_bVisible;
	bool m_bGotoPlot;
	bool m_bHighlightPlot;
	bool m_bSelectType;
	bool m_bSelectAll;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAdvisorInfo (ADD to Python)
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAdvisorInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvAdvisorInfo();
	virtual ~CvAdvisorInfo();

	const TCHAR* getTexture() const;				// Exposed to Python
	void setTexture(const TCHAR* szVal);
	int getNumCodes() const;
	int getEnableCode(uint uiCode) const;
	int getDisableCode(uint uiCode) const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvAdvisorInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:
	CvString m_szTexture;
	std::vector< std::pair< int, int > > m_vctEnableDisableCodes;
};

/*************************************************************************************************/
/** AlignmentAttitudeModifier       Opera       13.09.09        imported by Valkrionn	09.26.09**/
/*************************************************************************************************/
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAlignmentAttitudeModifierInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAlignmentAttitudeModifierInfo :
	public CvInfoBase
{

friend class CvLeaderHeadInfo;
friend class CvXMLLoadUtility;

	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvAlignmentAttitudeModifierInfo();

	int getToGood() const;
	int getToNeutral() const;
	int getToEvil() const;

	// Serialize

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iToGood;
	int m_iToNeutral;
	int m_iToEvil;
};
/*************************************************************************************************/
/** AlignmentAttitudeModifier                   END                                             **/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEthicalAlignmentAttitudeModifierInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEthicalAlignmentAttitudeModifierInfo :
	public CvInfoBase
{

friend class CvLeaderHeadInfo;
friend class CvXMLLoadUtility;

	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvEthicalAlignmentAttitudeModifierInfo();

	int getToLawful() const;
	int getToEthicalNeutral() const;
	int getToChaotic() const;

	// Serialize

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iToLawful;
	int m_iToEthicalNeutral;
	int m_iToChaotic;
};
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvLeaderHeadInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvArtInfoLeaderhead;
class CvLeaderHeadInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvLeaderHeadInfo();
	virtual ~CvLeaderHeadInfo();

	int getWonderConstructRand() const;				// Exposed to Python
	int getBaseAttitude() const;				// Exposed to Python
	int getBasePeaceWeight() const;				// Exposed to Python
	int getPeaceWeightRand() const;				// Exposed to Python
	int getWarmongerRespect() const;				// Exposed to Python
	int getEspionageWeight() const;				// Exposed to Python
	int getRefuseToTalkWarThreshold() const;				// Exposed to Python
	int getNoTechTradeThreshold() const;				// Exposed to Python
	int getTechTradeKnownPercent() const;				// Exposed to Python
	int getMaxGoldTradePercent() const;				// Exposed to Python
	int getMaxGoldPerTurnTradePercent() const;				// Exposed to Python
/*************************************************************************************************/
/**	Improved AI								18/01/12								Snarko		**/
/**							Teaching the AI to go for victories.								**/
/*************************************************************************************************/
	int getAIVictoryWeight(int i) const;
/*************************************************************************************************/
/**	Improved AI								END													**/
/*************************************************************************************************/
	int getMaxWarRand() const;				// Exposed to Python
	int getMaxWarNearbyPowerRatio() const;				// Exposed to Python
	int getMaxWarDistantPowerRatio() const;				// Exposed to Python
	int getMaxWarMinAdjacentLandPercent() const;				// Exposed to Python
	int getLimitedWarRand() const;				// Exposed to Python
	int getLimitedWarPowerRatio() const;				// Exposed to Python
	int getDogpileWarRand() const;				// Exposed to Python
	int getMakePeaceRand() const;				// Exposed to Python
	int getDeclareWarTradeRand() const;				// Exposed to Python
	int getDemandRebukedSneakProb() const;				// Exposed to Python
	int getDemandRebukedWarProb() const;				// Exposed to Python
	int getRazeCityProb() const;				// Exposed to Python
	int getBuildUnitProb() const;				// Exposed to Python
	int getBaseAttackOddsChange() const;				// Exposed to Python
	int getAttackOddsChangeRand() const;				// Exposed to Python
	int getWorseRankDifferenceAttitudeChange() const;				// Exposed to Python
	int getBetterRankDifferenceAttitudeChange() const;				// Exposed to Python
	int getCloseBordersAttitudeChange() const;				// Exposed to Python
	int getLostWarAttitudeChange() const;				// Exposed to Python
	int getAtWarAttitudeDivisor() const;				// Exposed to Python
	int getAtWarAttitudeChangeLimit() const;				// Exposed to Python
	int getAtPeaceAttitudeDivisor() const;				// Exposed to Python
	int getAtPeaceAttitudeChangeLimit() const;				// Exposed to Python
	int getSameReligionAttitudeChange() const;				// Exposed to Python
	int getSameReligionAttitudeDivisor() const;				// Exposed to Python
	int getSameReligionAttitudeChangeLimit() const;				// Exposed to Python
	int getDifferentReligionAttitudeChange() const;				// Exposed to Python
	int getDifferentReligionAttitudeDivisor() const;				// Exposed to Python
	int getDifferentReligionAttitudeChangeLimit() const;				// Exposed to Python
	int getBonusTradeAttitudeDivisor() const;				// Exposed to Python
	int getBonusTradeAttitudeChangeLimit() const;				// Exposed to Python
	int getOpenBordersAttitudeDivisor() const;				// Exposed to Python
	int getOpenBordersAttitudeChangeLimit() const;				// Exposed to Python
	int getDefensivePactAttitudeDivisor() const;				// Exposed to Python
	int getDefensivePactAttitudeChangeLimit() const;				// Exposed to Python
	int getShareWarAttitudeChange() const;				// Exposed to Python
	int getShareWarAttitudeDivisor() const;				// Exposed to Python
	int getShareWarAttitudeChangeLimit() const;				// Exposed to Python
	int getFavoriteCivicAttitudeChange() const;				// Exposed to Python
	int getFavoriteCivicAttitudeDivisor() const;				// Exposed to Python
	int getFavoriteCivicAttitudeChangeLimit() const;				// Exposed to Python
	int getDemandTributeAttitudeThreshold() const;				// Exposed to Python
	int getNoGiveHelpAttitudeThreshold() const;				// Exposed to Python
	int getTechRefuseAttitudeThreshold() const;				// Exposed to Python
	int getStrategicBonusRefuseAttitudeThreshold() const;				// Exposed to Python
	int getHappinessBonusRefuseAttitudeThreshold() const;				// Exposed to Python
	int getHealthBonusRefuseAttitudeThreshold() const;					// Exposed to Python
	int getMapRefuseAttitudeThreshold() const;									// Exposed to Python
	int getDeclareWarRefuseAttitudeThreshold() const;						// Exposed to Python
	int getDeclareWarThemRefuseAttitudeThreshold() const;				// Exposed to Python
	int getStopTradingRefuseAttitudeThreshold() const;					// Exposed to Python
	int getStopTradingThemRefuseAttitudeThreshold() const;			// Exposed to Python
	int getAdoptCivicRefuseAttitudeThreshold() const;						// Exposed to Python
	int getConvertReligionRefuseAttitudeThreshold() const;			// Exposed to Python
	int getOpenBordersRefuseAttitudeThreshold() const;					// Exposed to Python
	int getDefensivePactRefuseAttitudeThreshold() const;				// Exposed to Python
	int getPermanentAllianceRefuseAttitudeThreshold() const;		// Exposed to Python
	int getVassalRefuseAttitudeThreshold() const;				// Exposed to Python
	int getVassalPowerModifier() const;				// Exposed to Python
	int getFavoriteCivic() const;																// Exposed to Python
/*************************************************************************************************/
/**	Cutting								25/07/10										Snarko	**/
/**																								**/
/**				Removing rarely used/redundant stuff to improve speed.							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getFavoriteReligion() const;																// Exposed to Python
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Cutting									END													**/
/*************************************************************************************************/
	int getFreedomAppreciation() const;																// Exposed to Python

	const TCHAR* getArtDefineTag() const;				// Exposed to Python
	void setArtDefineTag(const TCHAR* szVal);

	// Arrays

	bool hasTrait(int i) const;				// Exposed to Python

	int getFlavorValue(int i) const;				// Exposed to Python
	int getContactRand(int i) const;				// Exposed to Python
	int getContactDelay(int i) const;				// Exposed to Python
	int getMemoryDecayRand(int i) const;				// Exposed to Python
	int getMemoryAttitudePercent(int i) const;				// Exposed to Python
	int getNoWarAttitudeProb(int i) const;				// Exposed to Python
	int getUnitAIWeightModifier(int i) const;				// Exposed to Python
	int getImprovementWeightModifier(int i) const;				// Exposed to Python
	int getDiploPeaceIntroMusicScriptIds(int i) const;
	int getDiploPeaceMusicScriptIds(int i) const;
	int getDiploWarIntroMusicScriptIds(int i) const;
	int getDiploWarMusicScriptIds(int i) const;

/*************************************************************************************************/
/** BonusAttitudeModifier           Opera   30.07.09        imported by Valkrionn	09.26.09    **/
/*************************************************************************************************/
	int getBonusAttitudeModifier(int i) const;
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

/*************************************************************************************************/
/** AlignmentAttitudeModifier       Opera   13.09.09        imported by Valkrionn	09.26.09    **/
/*************************************************************************************************/
	int getAlignmentAttitudeModifierToGood(int i) const;
	int getAlignmentAttitudeModifierToNeutral(int i) const;
	int getAlignmentAttitudeModifierToEvil(int i) const;
/*************************************************************************************************/
/** AlignmentAttitudeModifier                       END                                         **/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getEthicalAlignmentAttitudeModifierToLawful(int i) const;
	int getEthicalAlignmentAttitudeModifierToEthicalNeutral(int i) const;
	int getEthicalAlignmentAttitudeModifierToChaotic(int i) const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/

	// Other

	DllExport const CvArtInfoLeaderhead* getArtInfo() const;
	const TCHAR* getLeaderHead() const;
	const TCHAR* getButton() const;

/*************************************************************************************************/
/**	New Tag Defs	(LeaderInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getAlignmentModifier() const;
	int getProximityMemoryDecayDelay() const;
	int getProximityMemoryDecayRand() const;
	int getProximityMemoryLimit() const;
	float getProximityMemoryDecaySpeed() const;
	const TCHAR* getDefeatQuote() const;
	const TCHAR* getImage() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH: Added by Kael 08/07/2007
	bool isFemale() const;
	bool isRandom() const;
	int getAlignment() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getEthicalAlignmentModifier() const;
	int getEthicalAlignment() const;
	bool isTrueNeutral() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	bool isLeaderVariant() const;
	LeaderHeadTypes getPrimaryLeader() const;
/*************************************************************************************************/
/**	LeaderStatus Infos      				10/01/09								Valkrionn	**/
/*************************************************************************************************/
	int getLeaderClass() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int getAttitudeBadBonus() const;
	int getAttitudeCompassionHigh() const;
	int getAttitudeCompassionLow() const;
	int getAttitudeFromFemales() const;
	int getAttitudeFromMales() const;
	int getAttitudeToFemales() const;
	int getAttitudeToMales() const;

//FfH Card Game: Added by Sto 08/08/2008
	int getSomniumAggressiveness() const;
//FfH: End Add
/*************************************************************************************************/
/**	Cutting								25/07/10										Snarko	**/
/**																								**/
/**				Removing rarely used/redundant stuff to improve speed.							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int getFavoriteTech() const;
	int getFavoriteUnitCombat() const;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Cutting									END													**/
/*************************************************************************************************/
	int getFavoriteWonder() const;
	int getPermanentTrait() const;
/*************************************************************************************************/
/** HatedCivic		Opera		31.05.09        imported by Valkrionn	09.26.09 				**/
/*************************************************************************************************/
	DllExport int getHatedCivicAttitudeChange() const;
	DllExport int getHatedCivicAttitudeDivisor() const;
	DllExport int getHatedCivicAttitudeChangeLimit() const;
	DllExport int getHatedCivic() const;
/*************************************************************************************************/
/** End																							**/
/*************************************************************************************************/

	int getReligionWeightModifier(int i) const;

//FfH: End Add

	void write(FDataStreamBase* stream);
	void read(FDataStreamBase* stream);
	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvLeaderHeadInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL );
	void copyNonDefaultsReadPass2(CvLeaderHeadInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iWonderConstructRand;
	int m_iBaseAttitude;
	int m_iBasePeaceWeight;
	int m_iPeaceWeightRand;
	int m_iWarmongerRespect;
	int m_iEspionageWeight;
	int m_iRefuseToTalkWarThreshold;
	int m_iNoTechTradeThreshold;
	int m_iTechTradeKnownPercent;
	int m_iMaxGoldTradePercent;
	int m_iMaxGoldPerTurnTradePercent;
/*************************************************************************************************/
/**	Improved AI								18/01/12								Snarko		**/
/**							Teaching the AI to go for victories.								**/
/*************************************************************************************************/
	int* m_piAIVictoryTypes;
/*************************************************************************************************/
/**	Improved AI								END													**/
/*************************************************************************************************/
	int m_iMaxWarRand;
	int m_iMaxWarNearbyPowerRatio;
	int m_iMaxWarDistantPowerRatio;
	int m_iMaxWarMinAdjacentLandPercent;
	int m_iLimitedWarRand;
	int m_iLimitedWarPowerRatio;
	int m_iDogpileWarRand;
	int m_iMakePeaceRand;
	int m_iDeclareWarTradeRand;
	int m_iDemandRebukedSneakProb;
	int m_iDemandRebukedWarProb;
	int m_iRazeCityProb;
	int m_iBuildUnitProb;
	int m_iBaseAttackOddsChange;
	int m_iAttackOddsChangeRand;
	int m_iWorseRankDifferenceAttitudeChange;
	int m_iBetterRankDifferenceAttitudeChange;
	int m_iCloseBordersAttitudeChange;
	int m_iLostWarAttitudeChange;
	int m_iAtWarAttitudeDivisor;
	int m_iAtWarAttitudeChangeLimit;
	int m_iAtPeaceAttitudeDivisor;
	int m_iAtPeaceAttitudeChangeLimit;
	int m_iSameReligionAttitudeChange;
	int m_iSameReligionAttitudeDivisor;
	int m_iSameReligionAttitudeChangeLimit;
	int m_iDifferentReligionAttitudeChange;
	int m_iDifferentReligionAttitudeDivisor;
	int m_iDifferentReligionAttitudeChangeLimit;
	int m_iBonusTradeAttitudeDivisor;
	int m_iBonusTradeAttitudeChangeLimit;
	int m_iOpenBordersAttitudeDivisor;
	int m_iOpenBordersAttitudeChangeLimit;
	int m_iDefensivePactAttitudeDivisor;
	int m_iDefensivePactAttitudeChangeLimit;
	int m_iShareWarAttitudeChange;
	int m_iShareWarAttitudeDivisor;
	int m_iShareWarAttitudeChangeLimit;
	int m_iFavoriteCivicAttitudeChange;
	int m_iFavoriteCivicAttitudeDivisor;
	int m_iFavoriteCivicAttitudeChangeLimit;
	int m_iDemandTributeAttitudeThreshold;
	int m_iNoGiveHelpAttitudeThreshold;
	int m_iTechRefuseAttitudeThreshold;
	int m_iStrategicBonusRefuseAttitudeThreshold;
	int m_iHappinessBonusRefuseAttitudeThreshold;
	int m_iHealthBonusRefuseAttitudeThreshold;
	int m_iMapRefuseAttitudeThreshold;
	int m_iDeclareWarRefuseAttitudeThreshold;
	int m_iDeclareWarThemRefuseAttitudeThreshold;
	int m_iStopTradingRefuseAttitudeThreshold;
	int m_iStopTradingThemRefuseAttitudeThreshold;
	int m_iAdoptCivicRefuseAttitudeThreshold;
	int m_iConvertReligionRefuseAttitudeThreshold;
	int m_iOpenBordersRefuseAttitudeThreshold;
	int m_iDefensivePactRefuseAttitudeThreshold;
	int m_iPermanentAllianceRefuseAttitudeThreshold;
	int m_iVassalRefuseAttitudeThreshold;
	int m_iVassalPowerModifier;
	int m_iFreedomAppreciation;
	int m_iFavoriteCivic;
/*************************************************************************************************/
/**	Cutting								25/07/10										Snarko	**/
/**																								**/
/**				Removing rarely used/redundant stuff to improve speed.							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iFavoriteReligion;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Cutting									END													**/
/*************************************************************************************************/
	CvString m_szArtDefineTag;

/*************************************************************************************************/
/**	New Tag Defs	(LeaderInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iAlignmentModifier;
	int m_iProximityMemoryDecayDelay;
	int m_iProximityMemoryDecayRand;
	int m_iProximityMemoryLimit;
	float m_fProximityMemoryDecaySpeed;
	CvString m_szDefeatQuote;
	CvString m_szImage;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH: Added by Kael 08/07/2007
	bool m_bFemale;
	bool m_bRandom;
	int m_iAlignment;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iEthicalAlignmentModifier;
	int m_iEthicalAlignment;
	bool m_bTrueNeutral;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	bool m_bLeaderVariant;
	int m_iPrimaryLeader;
/*************************************************************************************************/
/**	LeaderStatus Infos      				10/02/09								Valkrionn	**/
/*************************************************************************************************/
	int m_iLeaderClass;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int m_iAttitudeBadBonus;
	int m_iAttitudeCompassionHigh;
	int m_iAttitudeCompassionLow;
	int m_iAttitudeFromFemales;
	int m_iAttitudeFromMales;
	int m_iAttitudeToFemales;
	int m_iAttitudeToMales;

//FfH Card Game: Added by Sto 08/08/2008
	int m_iSomniumAggressiveness;
//FfH: End Add
/*************************************************************************************************/
/**	Cutting								25/07/10										Snarko	**/
/**																								**/
/**				Removing rarely used/redundant stuff to improve speed.							**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iFavoriteTech;
	int m_iFavoriteUnitCombat;
/**								----  End Original Code  ----									**/
/*************************************************************************************************/
/**	Cutting									END													**/
/*************************************************************************************************/
	int m_iFavoriteWonder;
	int m_iPermanentTrait;

/*************************************************************************************************/
/** HatedCivic		Opera		31.05.09        imported by Valkrionn	09.26.09    			**/
/*************************************************************************************************/
	int m_iHatedCivicAttitudeChange;
	int m_iHatedCivicAttitudeDivisor;
	int m_iHatedCivicAttitudeChangeLimit;
	int m_iHatedCivic;
/*************************************************************************************************/
/** End																							**/
/*************************************************************************************************/

	int* m_piReligionWeightModifier;
//FfH: End Add

	// Arrays

	bool* m_pbTraits;

	int* m_piFlavorValue;
	int* m_piContactRand;
	int* m_piContactDelay;
	int* m_piMemoryDecayRand;
	int* m_piMemoryAttitudePercent;
	int* m_piNoWarAttitudeProb;
	int* m_piUnitAIWeightModifier;
	int* m_piImprovementWeightModifier;
	int* m_piDiploPeaceIntroMusicScriptIds;
	int* m_piDiploPeaceMusicScriptIds;
	int* m_piDiploWarIntroMusicScriptIds;
	int* m_piDiploWarMusicScriptIds;

/*************************************************************************************************/
/** BonusAttitudeModifier           Opera   30.07.09        imported by Valkrionn	09.26.09    **/
/*************************************************************************************************/
	int* m_piBonusAttitudeModifier;
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

/*************************************************************************************************/
/** AlignmentAttitudeModifier       Opera   13.09.09        imported by Valkrionn	09.26.09    **/
/*************************************************************************************************/
	CvAlignmentAttitudeModifierInfo* m_paAlignmentAttitudeModifier;
/*************************************************************************************************/
/** AlignmentAttitudeModifier                   END                                             **/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	CvEthicalAlignmentAttitudeModifierInfo* m_paEthicalAlignmentAttitudeModifier;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvWorldInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvWorldInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvWorldInfo();
	virtual ~CvWorldInfo();

	DllExport int getDefaultPlayers() const;				// Exposed to Python
	int getUnitNameModifier() const;				// Exposed to Python
	int getTargetNumCities() const;				// Exposed to Python
	int getNumFreeBuildingBonuses() const;				// Exposed to Python
	int getBuildingClassPrereqModifier() const;				// Exposed to Python
	int getMaxConscriptModifier() const;				// Exposed to Python
	int getWarWearinessModifier() const;				// Exposed to Python
	int getGridWidth() const;				// Exposed to Python
	int getGridHeight() const;				// Exposed to Python
	int getTerrainGrainChange() const;				// Exposed to Python
	int getFeatureGrainChange() const;				// Exposed to Python
	int getResearchPercent() const;				// Exposed to Python
	int getTradeProfitPercent() const;				// Exposed to Python
	int getDistanceMaintenancePercent() const;				// Exposed to Python
	int getNumCitiesMaintenancePercent() const;				// Exposed to Python
	int getColonyMaintenancePercent() const;				// Exposed to Python
	int getCorporationMaintenancePercent() const;				// Exposed to Python
	int getNumCitiesAnarchyPercent() const;				// Exposed to Python
	int getAdvancedStartPointsMod() const;				// Exposed to Python

//FfH: Added by Kael 10/01/2007
	int getMaxCitiesMod() const;
	int getUniqueFeatureChance() const;
	int getMapsizePlotCounterAttenuation() const;
//FfH: End Add

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvWorldInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iDefaultPlayers;
	int m_iUnitNameModifier;
	int m_iTargetNumCities;
	int m_iNumFreeBuildingBonuses;
	int m_iBuildingClassPrereqModifier;
	int m_iMaxConscriptModifier;
	int m_iWarWearinessModifier;
	int m_iGridWidth;
	int m_iGridHeight;
	int m_iTerrainGrainChange;
	int m_iFeatureGrainChange;
	int m_iResearchPercent;
	int m_iTradeProfitPercent;
	int m_iDistanceMaintenancePercent;
	int m_iNumCitiesMaintenancePercent;
	int m_iColonyMaintenancePercent;
	int m_iCorporationMaintenancePercent;
	int m_iNumCitiesAnarchyPercent;
	int m_iAdvancedStartPointsMod;

//FfH: Added by Kael 10/01/2007
	int m_iMaxCitiesMod;
	int m_iUniqueFeatureChance;
//FfH: End Add
	int m_iMapsizePlotCounterAttenuation;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvClimateInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvClimateInfo :	public CvInfoBase
{
public:

	CvClimateInfo();
	virtual ~CvClimateInfo();

	int getDesertPercentChange() const;							// Exposed to Python
	int getJungleLatitude() const;									// Exposed to Python
	int getHillRange() const;												// Exposed to Python
	int getPeakPercent() const;											// Exposed to Python

	float getSnowLatitudeChange() const;						// Exposed to Python
	float getTundraLatitudeChange() const;					// Exposed to Python
	float getGrassLatitudeChange() const;						// Exposed to Python
	float getDesertBottomLatitudeChange() const;		// Exposed to Python
	float getDesertTopLatitudeChange() const;				// Exposed to Python
	float getIceLatitude() const;										// Exposed to Python
	float getRandIceLatitude() const;								// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvClimateInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	int m_iDesertPercentChange;
	int m_iJungleLatitude;
	int m_iHillRange;
	int m_iPeakPercent;

	float m_fSnowLatitudeChange;
	float m_fTundraLatitudeChange;
	float m_fGrassLatitudeChange;
	float m_fDesertBottomLatitudeChange;
	float m_fDesertTopLatitudeChange;
	float m_fIceLatitude;
	float m_fRandIceLatitude;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//  class : CvSeaLevelInfo
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSeaLevelInfo :	public CvInfoBase
{
public:

	CvSeaLevelInfo();
	virtual ~CvSeaLevelInfo();

	int getSeaLevelChange() const;		// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvSeaLevelInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	int m_iSeaLevelChange;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvProcessInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvProcessInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvProcessInfo();
	virtual ~CvProcessInfo();

	int getTechPrereq() const;				// Exposed to Python
	
	int getProductionToCrimeModifier() const;				// Exposed to Python

	// Arrays

	int getProductionToCommerceModifier(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvProcessInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iTechPrereq;

	// Arrays
	int m_iProductionToCrimeModifier;
	int* m_paiProductionToCommerceModifier;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvVoteInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvVoteInfo :	public CvInfoBase
{
public:
	CvVoteInfo();
	virtual ~CvVoteInfo();

	int getPopulationThreshold() const;	// Exposed to Python
	int getStateReligionVotePercent() const;	// Exposed to Python
	int getTradeRoutes() const;					// Exposed to Python
	int getMinVoters() const;					// Exposed to Python

	bool isSecretaryGeneral() const;		// Exposed to Python
	bool isVictory() const;							// Exposed to Python
	bool isFreeTrade() const;						// Exposed to Python
	bool isNoNukes() const;							// Exposed to Python
	bool isCityVoting() const;	// Exposed to Python
	bool isCivVoting() const;	// Exposed to Python
	bool isDefensivePact() const;	// Exposed to Python
	bool isOpenBorders() const;	// Exposed to Python
	bool isForcePeace() const;	// Exposed to Python
	bool isForceNoTrade() const;	// Exposed to Python
	bool isForceWar() const;	// Exposed to Python
	bool isAssignCity() const;	// Exposed to Python

//FfH: Added by Kael 11/14/2007
	bool isGamblingRing() const;
	bool isNoOutsideTechTrades() const;
	bool isSlaveTrade() const;
	bool isSmugglingRing() const;
	int getCost() const;
	int getCrime() const;
	int getFreeUnitClass() const;
	int getFreeUnits() const;
	int getNoBonus() const;
	const TCHAR* getPyResult() const;
//FfH: End Add

	// Arrays

	bool isForceCivic(int i) const;			// Exposed to Python
	bool isVoteSourceType(int i) const;			// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvVoteInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	int m_iPopulationThreshold;
	int m_iStateReligionVotePercent;
	int m_iTradeRoutes;
	int m_iMinVoters;

	bool m_bSecretaryGeneral;
	bool m_bVictory;
	bool m_bFreeTrade;
	bool m_bNoNukes;
	bool m_bCityVoting;
	bool m_bCivVoting;
	bool m_bDefensivePact;
	bool m_bOpenBorders;
	bool m_bForcePeace;
	bool m_bForceNoTrade;
	bool m_bForceWar;
	bool m_bAssignCity;

//FfH: Added by Kael 11/14/2007
	bool m_bGamblingRing;
	bool m_bNoOutsideTechTrades;
	bool m_bSlaveTrade;
	bool m_bSmugglingRing;
	int m_iCost;
	int m_iCrime;
	int m_iFreeUnits;
	int m_iFreeUnitClass;
	int m_iNoBonus;
	CvString m_szPyResult;
//FfH: End Add

	// Arrays

	bool* m_pbForceCivic;
	bool* m_abVoteSourceTypes;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvProjectInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvProjectInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvProjectInfo();
	virtual ~CvProjectInfo();

	int getVictoryPrereq() const;									// Exposed to Python
	int getTechPrereq() const;										// Exposed to Python
	int getAnyoneProjectPrereq() const;						// Exposed to Python
	void setAnyoneProjectPrereq(int i);
/*************************************************************************************************/
/**	New Tag Defs	(ProjectInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getNumPrereqAlignments() const;
	int getPrereqAlignment(int iI) const;
	bool isResetProjects() const;
	bool isPrereqWar() const;
	bool isPrereqBlockBonuses() const;
	int getPrereqBroadAlignment() const;
	int getAlignmentModifier() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getNumPrereqEthicalAlignments() const;
	int getPrereqEthicalAlignment(int iI) const;
	int getPrereqBroadEthicalAlignment() const;
	int getEthicalAlignmentModifier() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int getRevealAllBonuses() const;
	int getBlockBonuses() const;
	int getRestoreBonuses() const;
	int getHideUnits() const;
	int getSeeInvisible() const;
	int getCooldown() const;
	bool isResistable() const;
	int getResistBase() const;
	int getResistMax() const;
	int getResistMin() const;
	int getForcePeaceWithCivilization() const;
	int getPrereqCivilizationVectorSize();
	CvString getPrereqCivilizationVectorElement(int i);
	int getForcePeaceWithCivilizationVectorSize();
	CvString getForcePeaceWithCivilizationVectorElement(int i);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int getMaxGlobalInstances() const;						// Exposed to Python
	int getMaxTeamInstances() const;							// Exposed to Python
	int getProductionCost() const;								// Exposed to Python
	int getNukeInterception() const;							// Exposed to Python
	int getTechShare() const;											// Exposed to Python
	int getEveryoneSpecialUnit() const;						// Exposed to Python
	int getEveryoneSpecialBuilding() const;				// Exposed to Python
	int getVictoryDelayPercent() const;				// Exposed to Python
	int getSuccessRate() const;				// Exposed to Python

	bool isSpaceship() const;											// Exposed to Python
	bool isAllowsNukes() const;											// Exposed to Python
	const char* getMovieArtDef() const;						// Exposed to Python

	const TCHAR* getCreateSound() const;					// Exposed to Python
	void setCreateSound(const TCHAR* szVal);

//FfH: Added by Kael 08/26/2008
	int getAIWeight() const;
	int getModifyGlobalCounter() const;
	CvString getPrereqCivilizationsVectorElement(int i);
	int getNumPrereqCivilizations() const;
	int getPrereqCivilization(int iI) const;
	int getPrereqGlobalCounter() const;
//FfH: End Add

	// Arrays

	int getBonusProductionModifier(int i) const;	// Exposed to Python
	int getVictoryThreshold(int i) const;					// Exposed to Python
	int getVictoryMinThreshold(int i) const;					// Exposed to Python
	int getProjectsNeeded(int i) const;						// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvProjectInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	void copyNonDefaultsReadPass2(CvProjectInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

//FfH: Added by Kael 08/26/2008
	bool readPass3();
//FfH: End Add

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iVictoryPrereq;
	int m_iTechPrereq;
	int m_iAnyoneProjectPrereq;
/*************************************************************************************************/
/**	New Tag Defs	(ProjectInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iNumPrereqAlignments;
	int* m_piPrereqAlignments;
	bool m_bResetProjects;
	bool m_bPrereqWar;
	bool m_bPrereqBlockBonuses;
	int m_iPrereqBroadAlignment;
	int m_iAlignmentModifier;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iNumPrereqEthicalAlignments;
	int* m_piPrereqEthicalAlignments;
	int m_iPrereqBroadEthicalAlignment;
	int m_iEthicalAlignmentModifier;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int m_iRevealAllBonuses;
	int m_iBlockBonuses;
	int m_iRestoreBonuses;
	int m_iHideUnits;
	int m_iSeeInvisible;
	int m_iCooldown;
	bool m_bResistable;
	int m_iResistBase;
	int m_iResistMax;
	int m_iResistMin;
	int m_iForcePeaceWithCivilization;
	std::vector<CvString> m_aszExtraXML2forPass3;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int m_iMaxGlobalInstances;
	int m_iMaxTeamInstances;
	int m_iProductionCost;
	int m_iNukeInterception;
	int m_iTechShare;
	int m_iEveryoneSpecialUnit;
	int m_iEveryoneSpecialBuilding;
	int m_iVictoryDelayPercent;
	int m_iSuccessRate;

	bool m_bSpaceship;
	bool m_bAllowsNukes;

	CvString m_szCreateSound;
	CvString m_szMovieArtDef;

//FfH: Added by Kael 08/26/2008
	int m_iAIWeight;
	int m_iModifyGlobalCounter;
	int m_iNumPrereqCivilizations;
	int m_iPrereqGlobalCounter;
//FfH: End Add

	// Arrays

	int* m_piBonusProductionModifier;
	int* m_piVictoryThreshold;
	int* m_piVictoryMinThreshold;
	int* m_piProjectsNeeded;
	int* m_piPrereqCivilizations;
	std::vector<CvString> m_aszPrereqCivilizationsforPass3;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvReligionInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvReligionInfo : public CvHotkeyInfo
{
	//---------------------------------------PUBLIC INTERFACE----------------------------------------
public:

	CvReligionInfo();
	virtual ~CvReligionInfo();

	int getChar() const;								// Exposed to Python
	void setChar(int i,int j=8483);
	int getHolyCityChar() const;				// Exposed to Python
	void setHolyCityChar(int i,int j=8483);
	int getTechPrereq() const;					// Exposed to Python
	int getFreeUnitClass() const;				// Exposed to Python
	int getNumFreeUnits() const;				// Exposed to Python
	int getSpreadFactor() const;				// Exposed to Python
	int getMissionType() const;					// Exposed to Python
	void setMissionType(int iNewType);

	//ClimateSystem:
	int getFormClimateZoneType() const;

/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
	int getGlobalReligionYield(int i) const;		// Exposed to Python
	int* getGlobalReligionYieldArray() const;
	int getHolyCityYield(int i) const;					// Exposed to Python
	int* getHolyCityYieldArray() const;
	int getStateReligionYield(int i) const;		// Exposed to Python
	int* getStateReligionYieldArray() const;
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/

	const TCHAR* getTechButton() const;				// Exposed to Python
	void setTechButton(const TCHAR* szVal);
	const TCHAR* getGenericTechButton() const;				// Exposed to Python
	void setGenericTechButton(const TCHAR* szVal);
	const TCHAR* getMovieFile() const;				// Exposed to Python
	void setMovieFile(const TCHAR* szVal);
	const TCHAR* getMovieSound() const;				// Exposed to Python
	void setMovieSound(const TCHAR* szVal);
	const TCHAR* getSound() const;						// Exposed to Python
	void setSound(const TCHAR* szVal);

	const TCHAR* getButtonDisabled() const;		//	Exposed to Python

	void setAdjectiveKey(const TCHAR* szVal);
	const wchar* getAdjectiveKey() const;				// Exposed to Python
	std::wstring pyGetAdjectiveKey() { return getAdjectiveKey(); }				// Exposed to Python

	// Arrays

	int getGlobalReligionCommerce(int i) const;		// Exposed to Python
	int* getGlobalReligionCommerceArray() const;
	int getHolyCityCommerce(int i) const;					// Exposed to Python
	int* getHolyCityCommerceArray() const;
	int getStateReligionCommerce(int i) const;		// Exposed to Python
	int* getStateReligionCommerceArray() const;

/*************************************************************************************************/
/**	New Tag Defs	(ReligionInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getAlignmentModifier() const;
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	int getAlignmentShift() const;
	int getAlignmentShiftModifier() const;
	int getAlignmentShiftTowardsNeutral() const;
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
	int getTGAIndex() const;
	void setTGAIndex(int i);
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Religion: Added by Kael 08/09/2007
	bool isHidden() const;
	bool isNoCrimeUnhappy() const;
	bool isSneakAttack() const;
	bool isUpdateSight() const;
	int getACPlotAttenuationMod() const;
	int getGlobalCounterFound() const;
	int getGlobalCounterSpread() const;
	int getAlignment() const;
	int getAlignmentBest() const;
	int getAlignmentWorst() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getEthicalAlignmentModifier() const;
	int getEthicalAlignmentShift() const;
	int getEthicalAlignmentShiftModifier() const;
	int getEthicalAlignmentShiftTowardsNeutral() const;
	int getEthicalAlignment() const;
	int getEthicalAlignmentBest() const;
	int getEthicalAlignmentWorst() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Religion Based Music					02/09/10									Snarko	**/
/**				Changing music from eras to religions (or eras if no religion)					**/
/*************************************************************************************************/
	int getNumSoundtracks() const;				//	Exposed to Python
	int getSoundtracks(int i) const;				//	Exposed to Python
/*************************************************************************************************/
/**	Religion Based Music						END												**/
/*************************************************************************************************/
//FfH: End Add

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvReligionInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iChar;
	int m_iHolyCityChar;
	int m_iTechPrereq;
	int m_iFreeUnitClass;
	int m_iNumFreeUnits;
	int m_iSpreadFactor;
	int m_iMissionType;

	//ClimateSystem:
	int m_iFormClimateZoneType;

/*************************************************************************************************/
/**	Stasis									11/17/09								Valkrionn	**/
/**																								**/
/**			Adds new commerces to Religions			**/
/*************************************************************************************************/
	int* m_paiGlobalReligionYield;
	int* m_paiHolyCityYield;
	int* m_paiStateReligionYield;
/*************************************************************************************************/
/**	Stasis									END													**/
/*************************************************************************************************/

	CvString m_szTechButton;
	CvString m_szGenericTechButton;
	CvString m_szMovieFile;
	CvString m_szMovieSound;
	CvString m_szSound;
	CvWString m_szAdjectiveKey;

/*************************************************************************************************/
/**	New Tag Defs	(ReligionInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iAlignmentModifier;
/*************************************************************************************************/
/**	Expanded Broader Alignments 			11/03/09								Valkrionn	**/
/**																								**/
/**								Used to determine per turn shifts								**/
/*************************************************************************************************/
	int m_iAlignmentShift;
	int m_iAlignmentShiftModifier;
	int m_iAlignmentShiftTowardsNeutral;
/*************************************************************************************************/
/**	Broader Alignments Expansion				END												**/
/*************************************************************************************************/
	int m_iTGAIndex;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Religion: Added by Kael 08/09/2007
	bool m_bHidden;
	bool m_bNoCrimeUnhappy;
	bool m_bSneakAttack;
	bool m_bUpdateSight;
	int m_iACPlotAttenuationMod;
	int m_iGlobalCounterFound;
	int m_iGlobalCounterSpread;
	int m_iAlignment;
	int m_iAlignmentBest;
	int m_iAlignmentWorst;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iEthicalAlignmentModifier;
	int m_iEthicalAlignmentShift;
	int m_iEthicalAlignmentShiftModifier;
	int m_iEthicalAlignmentShiftTowardsNeutral;
	int m_iEthicalAlignment;
	int m_iEthicalAlignmentBest;
	int m_iEthicalAlignmentWorst;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Religion Based Music					02/09/10									Snarko	**/
/**				Changing music from eras to religions (or eras if no religion)					**/
/*************************************************************************************************/
	int m_iNumSoundtracks;
	int* m_paiSoundtracks;
/*************************************************************************************************/
/**	Religion Based Music						END												**/
/*************************************************************************************************/
//FfH: End Add

	// Arrays

	int* m_paiGlobalReligionCommerce;
	int* m_paiHolyCityCommerce;
	int* m_paiStateReligionCommerce;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCorporationInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCorporationInfo : public CvHotkeyInfo
{
/*************************************************************************************************/
/**	LoadedTGA								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Modifies how the TGA is handled to allow many more religions/corporations/resources easily	**/
/*************************************************************************************************/
	friend class CvXMLLoadUtility;
/*************************************************************************************************/
/**	LoadedTGA								END													**/
/*************************************************************************************************/
	//---------------------------------------PUBLIC INTERFACE----------------------------------------
public:

	CvCorporationInfo();
	virtual ~CvCorporationInfo();

	int getChar() const;								// Exposed to Python
/*************************************************************************************************/
/**	LoadedTGA								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Modifies how the TGA is handled to allow many more religions/corporations/resources easily	**/
/*************************************************************************************************/
	int getTGAIndex() const;
	void setTGAIndex(int i);
/*************************************************************************************************/
/**	LoadedTGA								END													**/
/*************************************************************************************************/
	void setChar(int i,int j=8483);
	int getHeadquarterChar() const;				// Exposed to Python
	void setHeadquarterChar(int i, int j=8483);
	int getTechPrereq() const;					// Exposed to Python
	int getFreeUnitClass() const;				// Exposed to Python
	int getSpreadFactor() const;				// Exposed to Python
	int getSpreadCost() const;				// Exposed to Python
	int getMaintenance() const;				// Exposed to Python
	int getMissionType() const;					// Exposed to Python
	void setMissionType(int iNewType);

	int getBonusProduced() const;					// Exposed to Python

	const TCHAR* getMovieFile() const;				// Exposed to Python
	void setMovieFile(const TCHAR* szVal);
	const TCHAR* getMovieSound() const;				// Exposed to Python
	void setMovieSound(const TCHAR* szVal);
	const TCHAR* getSound() const;						// Exposed to Python
	void setSound(const TCHAR* szVal);

	// Arrays

	int getPrereqBonus(int i) const;					// Exposed to Python
	int getHeadquarterCommerce(int i) const;					// Exposed to Python
	int* getHeadquarterCommerceArray() const;
	int getCommerceProduced(int i) const;					// Exposed to Python
	int* getCommerceProducedArray() const;
	int getYieldProduced(int i) const;					// Exposed to Python
	int* getYieldProducedArray() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvCorporationInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

/*************************************************************************************************/
/**	LoadedTGA								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Modifies how the TGA is handled to allow many more religions/corporations/resources easily	**/
/*************************************************************************************************/
	int m_iTGAIndex;
/*************************************************************************************************/
/**	LoadedTGA								END													**/
/*************************************************************************************************/
	int m_iChar;
	int m_iHeadquarterChar;
	int m_iTechPrereq;
	int m_iFreeUnitClass;
	int m_iSpreadFactor;
	int m_iSpreadCost;
	int m_iMaintenance;
	int m_iMissionType;
	int m_iBonusProduced;

	CvString m_szMovieFile;
	CvString m_szMovieSound;
	CvString m_szSound;

	// Arrays

	int* m_paiPrereqBonuses;
	int* m_paiHeadquarterCommerce;
	int* m_paiCommerceProduced;
	int* m_paiYieldProduced;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTraitInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTraitInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvTraitInfo();
	virtual ~CvTraitInfo();

	int getHealth() const;				// Exposed to Python
	int getHappiness() const;				// Exposed to Python
	int getHappyPerMilitaryUnit() const;				// Exposed to Python
	int getMaxAnarchy() const;				// Exposed to Python
	int getFreeBuildingClass() const;				// Exposed to Python
	int getUpkeepModifier() const;				// Exposed to Python
	int getDistanceMaintenanceModifier() const;				// Exposed to Python
	int getRitualProductionModifier() const;				// Exposed to Python
	int getMilitaryProductionModifier() const;				// Exposed to Python
	int getLevelExperienceModifier() const;				// Exposed to Python
	int getGreatPeopleRateModifier() const;				// Exposed to Python
	int getGreatGeneralRateModifier() const;				// Exposed to Python
	int getDiscoverRandModifier() const;				// Exposed to Python
	int getSpreadRandModifier() const;				// Exposed to Python
	int getExtraGrowthThreshold() const;				// Exposed to Python
	int getACGrowthThreshold() const;				// Exposed to Python
	int getDomesticGreatGeneralRateModifier() const;				// Exposed to Python
	int getMaxGlobalBuildingProductionModifier() const;				// Exposed to Python
	int getMaxTeamBuildingProductionModifier() const;				// Exposed to Python
	int getMaxPlayerBuildingProductionModifier() const;				// Exposed to Python

	int getLevel() const;
	int getMinRequiredPoints() const;
	bool isCanBeLost() const;
	int getTraitClass() const;
	int getNextTrait() const;
	int getParentTrait() const;
	void setNextTrait(int i);
	void setParentTrait(int i);
	const TCHAR* getShortDescription() const;				// Exposed to Python
	void setShortDescription(const TCHAR* szVal);

//FfH Traits: Added by Kael 08/02/2007
	bool isAdaptive() const;
	bool isAgnostic() const;
	bool isAmphibian() const;
	bool isAssimilation() const;
	bool isBarbarianAlly() const;
	bool isIgnoreFood() const;
	bool isIgnoreProduction() const;
	bool isIgnoreHealth() const;
	bool isIgnoreHappy() const;
	bool isInsane() const;
	bool isSelectable() const;
	bool isSprawling() const;
/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool isFixedBorders() const;
	bool isInfluenceAllowed() const;
	int getVictoryInfluenceModifier() const;
	int getDefeatInfluenceModifier() const;
	int getPillageInfluenceModifier() const;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	bool isOverflowProduction() const;
	bool isFoodUnitProduction() const;
	bool isFoodBuildingProduction() const;
	bool isFoodProjectProduction() const;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Nomadic								01/15/10									Valkrionn	**/
/**							Addition requested by Sylvain5477									**/
/**						   Allows you to bypass the city check									**/
/*************************************************************************************************/
	bool isNomadic() const;
/*************************************************************************************************/
/**	Nomadic									END													**/
/*************************************************************************************************/
	int getFreeXPFromCombat() const;
	int getMaxCities() const;
	int getPillagingGold() const;
	int getStartingGold() const;
	int getSummonDuration() const;
	int getUpgradeCostModifier() const;
//FfH: End Add

	// Arrays

	int getExtraYieldThreshold(int i) const;				// Exposed to Python
	int getTradeYieldModifier(int i) const;				// Exposed to Python
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	int getTradeCommerceModifier(int i) const;			// Exposed to Python
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(TraitInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getModReligionSpreadChance() const;
	int getBaseYieldFromUnit(int i) const;
	int getYieldFromUnitModifier(int i) const;
	int getBaseCommerceFromUnit(int i) const;
	int getCommerceFromUnitModifier(int i) const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int getCommerceChange(int i) const;				// Exposed to Python
	int getCommerceModifier(int i) const;				// Exposed to Python

	int isRevealBonus(int i) const;				// Exposed to Python
	int isFreeBonus(int i) const;				// Exposed to Python
	int isNoBonus(int i) const;				// Exposed to Python

	int isFreeSpecialistClassStateReligion(int i) const;				// Exposed to Python
	int isFreeSpecialistClassNonStateReligion(int i) const;				// Exposed to Python

	int getSpecialistClassHappinessChange(int i)const;
	int getSpecialistClassHealthChange(int i)const;
	int getSpecialistClassCrimeChange(int i)const;
	
	int getReligiousWeightModifier(int i)const;

	int getUnitClassPlayerInstancesChange(int i)const;

	int isFreePromotion(int i) const;				// Exposed to Python
	int isFreePromotionUnitCombat(int i) const;

/*************************************************************************************************/
/**	Miner Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
	int getSpecialistClassYieldChange(int i, int j) const;
	int* getSpecialistClassYieldChangeArray(int i) const;

	int getSpecialistClassCommerceChange(int i, int j) const;
	int* getSpecialistClassCommerceChangeArray(int i) const;

	int getPeaceCommerceModifier(int i) const;

	int getFeatureProductionChange(int i) const;       // Exposed to Python
	int getFeatureGrowthChange(int i) const;       // Exposed to Python
	int getPlotEffectSpawnChance(int i) const;       // Exposed to Python
	int getHurryPopulationModifier() const;				// Exposed to Python
	int getTerrainYieldChanges(int i, int j) const;
	int* getTerrainYieldChangesArray(int i) const;
	int getFeatureYieldChanges(int i, int j) const;
	int* getFeatureYieldChangesArray(int i) const;
	int getImprovementYieldChanges(int i, int j) const;
	int* getImprovementYieldChangesArray(int i) const;
	int getImprovementYieldChangesVectorSize();
	CvString getImprovementYieldChangesNamesVectorElement(int i);
	int* getImprovementYieldChangesValuesVectorElement(int i);
	int getUnitClassesVectorSize();
	int getUnitClassesUnitVectorSize();
	CvString getUnitClassesVectorElement(int i);
	CvString getUnitClassesUnitVectorElement(int i);
	int getExtraUnitClasses(int i) const;
	int getBuildingClassesVectorSize();
	int getBuildingClassesBuildingVectorSize();
	CvString getBuildingClassesVectorElement(int i);
	CvString getBuildingClassesBuildingVectorElement(int i);
	int getExtraBuildingClasses(int i) const;
	/*************************************************************************************************/
/**	Miner Trait							END			**/
/*************************************************************************************************/

/*************************************************************************************************/
/** bUniqueCult         Opera for LE/Orbis  06/07/09        imported by Valkrionn	09.26.09    **/
/*************************************************************************************************/
	bool isUniqueCult() const;
	bool isIntolerant() const;
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	int getInitialCityCap() const;
	int getMaxCityCap() const;
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

	bool read(CvXMLLoadUtility* pXML);	
	bool readPass2(CvXMLLoadUtility* pXML);
	bool readPass3();

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvTraitInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL );
	void copyNonDefaultsReadPass2(CvTraitInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);

/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iTraitClass;
	int m_iNextTrait;
	int m_iParentTrait;
	int m_iHealth;
	int m_iHappiness;
	int m_iHappyPerMilitaryUnit;
	int m_iMaxAnarchy;
	int m_iFreeBuildingClass;
	CvString m_iFreeBuildingClassforPass3;
	int m_iUpkeepModifier;
	int m_iDistanceMaintenanceModifier;
	int m_iRitualProductionModifier;
	int m_iMilitaryProductionModifier;
	int m_iLevelExperienceModifier;
	int m_iGreatPeopleRateModifier;
	int m_iGreatGeneralRateModifier;
	int m_iDiscoverRandModifier;
	int m_iSpreadRandModifier;
	int m_iExtraGrowthThreshold;
	int m_iACGrowthThreshold;
	int m_iDomesticGreatGeneralRateModifier;
	int m_iMaxGlobalBuildingProductionModifier;
	int m_iMaxTeamBuildingProductionModifier;
	int m_iMaxPlayerBuildingProductionModifier;
	int m_iLevel;
	
	int m_iMinRequiredPoints;
	bool m_bCanBeLost;

//FfH Traits: Added by Kael 08/02/2007
	bool m_bAdaptive;
	bool m_bAgnostic;
	bool m_bAmphibian;
	bool m_bAssimilation;
	bool m_bBarbarianAlly;
	bool m_bIgnoreFood;
	bool m_bIgnoreProduction;
	bool m_bIgnoreHealth;
	bool m_bIgnoreHappy;
	bool m_bInsane;
	bool m_bSelectable;
	bool m_bSprawling;
/************************************************************************************************/
/* Influence Driven War                   06/07/10                                 Valkrionn    */
/*                                                                                              */
/*						Prevents IDW effects within specific borders                            */
/************************************************************************************************/
	bool m_bFixedBorders;
	bool m_bInfluenceAllowed;
	int m_iVictoryInfluenceModifier;
	int m_iDefeatInfluenceModifier;
	int m_iPillageInfluenceModifier;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Multiple Production 					07/10/09									Denev	**/
/**							Merged by Valkrionn		13/01/2010									**/
/**					Allows overflow production to produce multiple units each turn				**/
/*************************************************************************************************/
	bool m_bOverflowProduction;
	bool m_bFoodUnitProduction;
	bool m_bFoodBuildingProduction;
	bool m_bFoodProjectProduction;
/*************************************************************************************************/
/**	Multiple Production							END												**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Nomadic								01/15/10									Valkrionn	**/
/**							Addition requested by Sylvain5477									**/
/**						   Allows you to bypass the city check									**/
/*************************************************************************************************/
	bool m_bNomadic;
/*************************************************************************************************/
/**	Nomadic									END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iFreeXPFromCombat;
/**								----  End Original Code  ----									**/
	float m_iFreeXPFromCombat;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int m_iMaxCities;
	int m_iPillagingGold;
	int m_iStartingGold;
	int m_iSummonDuration;
	int m_iUpgradeCostModifier;
//FfH: End Add

	CvString m_szShortDescription;

	// Arrays

	int* m_paiExtraYieldThreshold;
	int* m_paiTradeYieldModifier;
/*************************************************************************************************/
/**	TradeCommerceModifiers	 				09/05/10								Valkrionn	**/
/**																								**/
/**									Allows trade to grant culture								**/
/*************************************************************************************************/
	int* m_paiTradeCommerceModifier;
/*************************************************************************************************/
/**	END																							**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	New Tag Defs	(TraitInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iModReligionSpreadChance;
	int* m_paiBaseYieldFromUnit;
	int* m_paiYieldFromUnitModifier;
	int* m_paiBaseCommerceFromUnit;
	int* m_paiCommerceFromUnitModifier;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	int* m_paiCommerceChange;
	int* m_paiCommerceModifier;

	bool* m_pabRevealBonus;
	bool* m_pabFreeBonus;
	bool* m_pabNoBonus;

	bool* m_pabFreeSpecialistClassStateReligion;
	bool* m_pabFreeSpecialistClassNonStateReligion;

	int* m_paiSpecialistClassHealthChange;
	int* m_paiSpecialistClassHappinessChange;
	int* m_paiSpecialistClassCrimeChange;
	int* m_paiReligiousWeightModifier;

	int* m_paiUnitClassPlayerInstancesChange;

	bool* m_pabFreePromotion;
	bool* m_pabFreePromotionUnitCombat;

/*************************************************************************************************/
/**	Miner Trait 	 	Orbis from Sanguo Mod		18/02/09	Ahwaric		**/
/*************************************************************************************************/
	int** m_ppaiSpecialistClassYieldChange;
	int** m_ppaiSpecialistClassCommerceChange;
	int* m_paiPeaceCommerceModifier;
	int* m_paiFeatureProductionChange;
	int* m_paiFeatureGrowthChange;
	int* m_paiPlotEffectSpawnChance;
	int m_iHurryPopulationModifier;
	int** m_ppiTerrainYieldChanges;
	int** m_ppiFeatureYieldChanges;
	int** m_ppiImprovementYieldChanges;
	std::vector<CvString> m_aszImprovementYieldChanges;
	std::vector<int*> m_yiImprovementYieldChanges;
	std::vector<CvString> m_aszUnitClassesforPass3;
	std::vector<CvString> m_aszUnitClassesUnitforPass3;
	int* m_piExtraUnitClass;
	std::vector<CvString> m_aszBuildingClassesforPass3;
	std::vector<CvString> m_aszBuildingClassesBuildingforPass3;
	int* m_piExtraBuildingClass;
	/*************************************************************************************************/
/**	Miner Trait							END			**/
/*************************************************************************************************/

/*************************************************************************************************/
/** bUniqueCult         Opera for LE/Orbis  06/07/09         imported by Valkrionn	09.26.09    **/
/*************************************************************************************************/
	bool m_bUniqueCult;
	bool m_bIntolerant;
/*************************************************************************************************/
/** End                                                                                         **/
/*************************************************************************************************/

/*************************************************************************************************/
/** CityPopCap     Opera  9.8.09            imported by Valkrionn	09.26.09                    **/
/*************************************************************************************************/
	int m_iInitialCityCap;
	int m_iMaxCityCap;
/*************************************************************************************************/
/** CityPopCap                  END                                                             **/
/*************************************************************************************************/

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCursorInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCursorInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvCursorInfo();
	virtual ~CvCursorInfo();

	DllExport const TCHAR* getPath();				// Exposed to Python
	void setPath(const TCHAR* szVal);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvCursorInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szPath;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvThroneRoomCamera
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvThroneRoomCamera : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvThroneRoomCamera();
	virtual ~CvThroneRoomCamera();

	DllExport const TCHAR* getFileName();
	void setFileName(const TCHAR* szVal);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvThroneRoomCamera* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szFileName;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvThroneRoomInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvThroneRoomInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvThroneRoomInfo();
	DllExport virtual ~CvThroneRoomInfo();

	DllExport const TCHAR* getEvent();
	DllExport void setEvent(const TCHAR* szVal);
	DllExport const TCHAR* getNodeName();
	DllExport void setNodeName(const TCHAR* szVal);
	DllExport int getFromState();
	DllExport void setFromState(int iVal);
	DllExport int getToState();
	DllExport void setToState(int iVal);
	DllExport int getAnimation();
	DllExport void setAnimation(int iVal);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvThroneRoomInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iFromState;
	int m_iToState;
	int m_iAnimation;
	CvString m_szEvent;
	CvString m_szNodeName;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvThroneRoomStyleInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvThroneRoomStyleInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvThroneRoomStyleInfo();
	DllExport virtual ~CvThroneRoomStyleInfo();

	DllExport const TCHAR* getArtStyleType();
	DllExport void setArtStyleType(const TCHAR* szVal);
	DllExport const TCHAR* getEraType();
	DllExport void setEraType(const TCHAR* szVal);
	DllExport const TCHAR* getFileName();
	DllExport void setFileName(const TCHAR* szVal);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvThroneRoomStyleInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szArtStyleType;
	CvString m_szEraType;
	CvString m_szFileName;
	std::vector<CvString> m_aNodeNames;
	std::vector<CvString> m_aTextureNames;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSlideShowInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSlideShowInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvSlideShowInfo();
	DllExport virtual ~CvSlideShowInfo();

	DllExport const TCHAR* getPath();
	DllExport void setPath(const TCHAR* szVal);
	DllExport const TCHAR* getTransitionType();
	DllExport void setTransitionType(const TCHAR* szVal);
	DllExport float getStartTime();
	DllExport void setStartTime(float fVal);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvSlideShowInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	float m_fStartTime;
	CvString m_szPath;
	CvString m_szTransitionType;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSlideShowRandomInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSlideShowRandomInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvSlideShowRandomInfo();
	DllExport virtual ~CvSlideShowRandomInfo();

	DllExport const TCHAR* getPath();
	DllExport void setPath(const TCHAR* szVal);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvSlideShowRandomInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szPath;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvWorldPickerInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvWorldPickerInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvWorldPickerInfo();
	DllExport virtual ~CvWorldPickerInfo();

	DllExport const TCHAR* getMapName();
	DllExport void setMapName(const TCHAR* szVal);
	DllExport const TCHAR* getModelFile();
	DllExport void setModelFile(const TCHAR* szVal);
	DllExport int getNumSizes();
	DllExport float getSize(int index);
	DllExport int getNumClimates();
	DllExport const TCHAR* getClimatePath(int index);
	DllExport int getNumWaterLevelDecals();
	DllExport const TCHAR* getWaterLevelDecalPath(int index);
	DllExport int getNumWaterLevelGloss();
	DllExport const TCHAR* getWaterLevelGlossPath(int index);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvWorldPickerInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szMapName;
	CvString m_szModelFile;
	std::vector<float> m_aSizes;
	std::vector<CvString> m_aClimates;
	std::vector<CvString> m_aWaterLevelDecals;
	std::vector<CvString> m_aWaterLevelGloss;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpaceShipInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpaceShipInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvSpaceShipInfo();
	DllExport virtual ~CvSpaceShipInfo();

	DllExport const TCHAR* getNodeName();
	DllExport void setNodeName(const TCHAR* szVal);
	DllExport const TCHAR* getProjectName();
	DllExport void setProjectName(const TCHAR* szVal);
	DllExport ProjectTypes getProjectType();
	DllExport AxisTypes getCameraUpAxis();
	DllExport SpaceShipInfoTypes getSpaceShipInfoType();
	DllExport int getPartNumber();
	DllExport int getArtType();
	DllExport int getEventCode();

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvSpaceShipInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szNodeName;
	CvString m_szProjectName;
	ProjectTypes m_eProjectType;
	AxisTypes m_eCameraUpAxis;
	int m_iPartNumber;
	int m_iArtType;
	int m_iEventCode;
	SpaceShipInfoTypes m_eSpaceShipInfoType;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAnimationInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
typedef std::vector<std::pair<int,float> > CvAnimationPathDefinition;
typedef std::pair<int,int >			CvAnimationCategoryDefinition;

class CvAnimationPathInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
	public:

		DllExport CvAnimationPathInfo();
		DllExport virtual ~CvAnimationPathInfo();

		DllExport int getPathCategory( int i );
		DllExport float getPathParameter( int i );
		DllExport int getNumPathDefinitions();
		DllExport CvAnimationPathDefinition * getPath( );
		DllExport bool isMissionPath() const;

		bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
		void copyNonDefaults(CvAnimationPathInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PRIVATE MEMBER VARIABLES---------------------------------
	private:

		CvAnimationPathDefinition 	m_vctPathDefinition;	//!< Animation path definitions, pair(category,param).
		bool						m_bMissionPath;			//!< True if this animation is used in missions
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAnimationInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAnimationCategoryInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
	public:

		DllExport CvAnimationCategoryInfo();
		DllExport virtual ~CvAnimationCategoryInfo();

		DllExport int getCategoryBaseID( );
		DllExport int getCategoryDefaultTo( );

		bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
		void copyNonDefaults(CvAnimationCategoryInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PRIVATE MEMBER VARIABLES---------------------------------
	private:

		CvAnimationCategoryDefinition	m_kCategory;		//!< The pair(base IDs, default categories) defining the animation categories
		CvString						m_szDefaultTo;		//!< Holds the default to parameter, until all categories are read
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEntityEventInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEntityEventInfo : public CvInfoBase
{
		//---------------------------------------PUBLIC INTERFACE---------------------------------
	public:

		DllExport CvEntityEventInfo();
		DllExport virtual ~CvEntityEventInfo();

		bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
		void copyNonDefaults(CvEntityEventInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

		DllExport AnimationPathTypes getAnimationPathType(int iIndex = 0) const;
		DllExport EffectTypes getEffectType(int iIndex = 0) const;
		DllExport int getAnimationPathCount() const;
		DllExport int getEffectTypeCount() const;

		DllExport bool getUpdateFormation() const;

		//---------------------------------------PRIVATE MEMBER VARIABLES---------------------------------
	private:

		std::vector<AnimationPathTypes>	m_vctAnimationPathType;
		std::vector<EffectTypes>		m_vctEffectTypes;
		bool							m_bUpdateFormation;
};

// The below classes are for the ArtFile Management
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  classes : CvArtInfos
//
// This is also an abstract BASE class
//
//  DESC:  Used to store data from Art\Civ4ArtDefines.xml
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAssetInfoBase : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvAssetInfoBase()  {}
	DllExport virtual ~CvAssetInfoBase() {}

	DllExport const TCHAR* getTag() const;				// Exposed to Python
	DllExport void setTag(const TCHAR* szDesc);				// Exposed to Python

	DllExport const TCHAR* getPath() const;				// Exposed to Python
	DllExport void setPath(const TCHAR* szDesc);				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvAssetInfoBase* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szPath;

};

class CvArtInfoAsset : 	public CvAssetInfoBase
{
public:

	DllExport CvArtInfoAsset() {}
	DllExport virtual ~CvArtInfoAsset() {}

	DllExport const TCHAR* getNIF() const;				// Exposed to Python
	DllExport const TCHAR* getKFM() const;				// Exposed to Python

	DllExport void setNIF(const TCHAR* szDesc);				// Exposed to Python
	DllExport void setKFM(const TCHAR* szDesc);				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvArtInfoAsset* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	CvString m_szKFM;
	CvString m_szNIF;
};

//
//////////////////////////////////////////////////////////////////////////
// Another base class
//////////////////////////////////////////////////////////////////////////

class CvArtInfoScalableAsset :
	public CvArtInfoAsset,
	public CvScalableInfo
{
public:

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvArtInfoScalableAsset* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

};

// todoJS: Remove empty classes if additional items are not added

class CvArtInfoInterface : 	public CvArtInfoAsset
{
public:

	DllExport CvArtInfoInterface() {}
	DllExport virtual ~CvArtInfoInterface() {}

};

class CvArtInfoMisc : 	public CvArtInfoScalableAsset
{
public:

	DllExport CvArtInfoMisc() {}
	DllExport virtual ~CvArtInfoMisc() {}

};

class CvArtInfoMovie : 	public CvArtInfoAsset
{
public:

	DllExport CvArtInfoMovie() {}
	DllExport virtual ~CvArtInfoMovie() {}

};

class CvArtInfoUnit : public CvArtInfoScalableAsset
{
public:

	DllExport CvArtInfoUnit();
	DllExport virtual ~CvArtInfoUnit();

	DllExport bool getActAsRanged() const;
	DllExport bool getActAsLand() const;
	DllExport bool getActAsAir() const;

	DllExport const TCHAR* getShaderNIF() const;
	DllExport void setShaderNIF(const TCHAR* szDesc);

	DllExport const TCHAR* getShadowNIF() const;
	DllExport float getShadowScale() const;
	DllExport const TCHAR* getShadowAttachNode() const;
	DllExport int getDamageStates() const;

	DllExport const TCHAR* getTrailTexture() const;
	DllExport float getTrailWidth() const;
	DllExport float getTrailLength() const;
	DllExport float getTrailTaper() const;
	DllExport float getTrailFadeStarTime() const;
	DllExport float getTrailFadeFalloff() const;

	DllExport float getBattleDistance() const;
	DllExport float getRangedDeathTime() const;
	DllExport float getExchangeAngle() const;
	DllExport bool getCombatExempt() const;
	DllExport bool getSmoothMove() const;
	DllExport float getAngleInterpRate() const;
	DllExport float getBankRate() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvArtInfoUnit* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	DllExport const TCHAR* getTrainSound() const;
	DllExport void setTrainSound(const TCHAR* szVal);
	DllExport int getRunLoopSoundTag() const;
	DllExport int getRunEndSoundTag() const;
	DllExport int getPatrolSoundTag() const;
	DllExport int getSelectionSoundScriptId() const;
	DllExport int getActionSoundScriptId() const;

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:
	CvString m_szShaderNIF;		//!< The NIF used if the graphics card supports shaders
	CvString m_szShadowNIF;		//!< The shadow blob NIF to use for the unit
	CvString m_szShadowAttach;	//!< The name of the node to which the shadow takes its x,y position

	float m_fShadowScale;		//!< the scale of the unit's shadow.

	int m_iDamageStates;		//!< The maximum number of damage states this unit type supports
	bool m_bActAsRanged;		//!< true if the unit acts as a ranged unit in combat (but may or may not be actually a ranged unit)
	bool m_bActAsLand;
	bool m_bActAsAir;
	bool m_bCombatExempt;		//!< true if the unit is 'exempt' from combat - ie. it just flees instead of dying
	bool m_bSmoothMove;			//!< true if the unit should do non-linear interpolation for moves

	CvString m_szTrailTexture;	//!< The trail texture of the unit
	float m_fTrailWidth;		//!< The width of the trail
	float m_fTrailLength;		//!< The length of the trail
	float m_fTrailTaper;		//!< Tapering of the trail
	float m_fTrailFadeStartTime;//!< Time after which the trail starts to fade
	float m_fTrailFadeFalloff;	//!< Speed at which the fade happens

	float m_fBattleDistance;	//!< The preferred attack distance of this unit (1.0 == plot size)
	float m_fRangedDeathTime;	//!< The offset from firing in which an opponent should die
	float m_fExchangeAngle;		//!< The angle at which the unit does combat.
	float m_fAngleInterRate;	//!< The rate at which the units' angle interpolates
	float m_fBankRate;

	CvString m_szTrainSound;
	int m_iRunLoopSoundTag;
	int m_iRunEndSoundTag;
	int m_iPatrolSoundTag;
	int m_iSelectionSoundScriptId;
	int m_iActionSoundScriptId;
};

class CvArtInfoBuilding : public CvArtInfoScalableAsset
{
public:

	DllExport CvArtInfoBuilding();
	DllExport virtual ~CvArtInfoBuilding();

	DllExport bool isAnimated() const;				// Exposed to Python
	DllExport const TCHAR* getLSystemName() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvArtInfoBuilding* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	bool m_bAnimated;
	CvString m_szLSystemName;

};

class CvArtInfoCivilization : public CvArtInfoAsset
{
public:

	DllExport CvArtInfoCivilization();
	DllExport virtual ~CvArtInfoCivilization();

	DllExport bool isWhiteFlag() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvArtInfoCivilization* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	bool m_bWhiteFlag;

};

class CvArtInfoLeaderhead : public CvArtInfoAsset
{
public:

	DllExport CvArtInfoLeaderhead() {}
	DllExport virtual ~CvArtInfoLeaderhead() {}

	DllExport const TCHAR* getNoShaderNIF() const;
	DllExport void setNoShaderNIF(const TCHAR* szNIF);
	DllExport const TCHAR* getBackgroundKFM() const;
	DllExport void setBackgroundKFM( const TCHAR* szKFM);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvArtInfoLeaderhead* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	CvString m_szNoShaderNIF;
	CvString m_szBackgroundKFM;
};

class CvArtInfoBonus : public CvArtInfoScalableAsset
{
public:
	DllExport CvArtInfoBonus();
	DllExport virtual ~CvArtInfoBonus() {}

	DllExport int getFontButtonIndex() const;

	DllExport const TCHAR* getShaderNIF() const;
	DllExport void setShaderNIF(const TCHAR* szDesc);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvArtInfoBonus* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:
	CvString m_szShaderNIF;		//!< The NIF used if the graphics card supports shaders
	int m_iFontButtonIndex;
};

class CvArtInfoImprovement : public CvArtInfoScalableAsset
{
public:

	DllExport CvArtInfoImprovement();
	DllExport virtual ~CvArtInfoImprovement();

	DllExport const TCHAR* getShaderNIF() const;
	DllExport void setShaderNIF(const TCHAR* szDesc);

	DllExport bool isExtraAnimations() const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvArtInfoImprovement* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:
	CvString m_szShaderNIF;		//!< The NIF used if the graphics card supports shaders

	bool m_bExtraAnimations;

};

typedef std::vector<std::pair<int, int> > CvTextureBlendSlotList;

class CvArtInfoTerrain : public CvArtInfoAsset
{
public:

	DllExport CvArtInfoTerrain();
	DllExport virtual ~CvArtInfoTerrain();

	DllExport const TCHAR* getBaseTexture();
	DllExport void setBaseTexture(const TCHAR* szTmp );
	DllExport const TCHAR* getGridTexture();
	DllExport void setGridTexture(const TCHAR* szTmp );
	DllExport const TCHAR* getDetailTexture();
	DllExport void setDetailTexture(const TCHAR* szTmp);
	DllExport int getLayerOrder();
	DllExport bool useAlphaShader();
	DllExport CvTextureBlendSlotList &getBlendList(int blendMask);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvArtInfoTerrain* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	CvString m_szDetailTexture;				//!< Detail texture associated with the Terrain base texture
	CvString m_szGridTexture;

	int m_iLayerOrder;									//!< Layering order of texture
	bool m_bAlphaShader;
	int m_numTextureBlends;						//!< number to blend textures.
	CvTextureBlendSlotList  **m_pTextureSlots;	//!< Array of Textureslots per blend tile
};

class CvArtInfoFeature : public CvArtInfoScalableAsset
{
public:

	DllExport CvArtInfoFeature();
	DllExport virtual ~CvArtInfoFeature();

	DllExport bool isAnimated() const;				// Exposed to Python
	DllExport bool isRiverArt() const;				// Exposed to Python
	DllExport TileArtTypes getTileArtType() const;
	DllExport LightTypes getLightType() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvArtInfoFeature* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	class FeatureArtModel
	{
	public:
		FeatureArtModel(const CvString &modelFile, RotationTypes rotation)
		{
			m_szModelFile = modelFile;
			m_eRotation = rotation;
		}

		const CvString &getModelFile() const
		{
			return m_szModelFile;
		}

		RotationTypes getRotation() const
		{
			return m_eRotation;
		}

	private:
		CvString m_szModelFile;
		RotationTypes m_eRotation;
	};

	class FeatureArtPiece
	{
	public:
		FeatureArtPiece(int connectionMask)
		{
			m_iConnectionMask = connectionMask;
		}

		int getConnectionMask() const
		{
			return m_iConnectionMask;
		}

		int getNumArtModels() const
		{
			return m_aArtModels.size();
		}

		const FeatureArtModel &getArtModel(int index) const
		{
			FAssertMsg((index >= 0) && (index < (int) m_aArtModels.size()), "[Jason] Invalid feature model file index.");
			return m_aArtModels[index];
		}

	private:
		std::vector<FeatureArtModel> m_aArtModels;
		int m_iConnectionMask;

		friend CvArtInfoFeature;
	};

	class FeatureDummyNode
	{
	public:
		FeatureDummyNode(const CvString &tagName, const CvString &nodeName)
		{
			m_szTag = tagName;
			m_szName = nodeName;
		}

		const CvString getTagName() const
		{
			return m_szTag;
		}

		const CvString getNodeName() const
		{
			return m_szName;
		}

	private:
		CvString m_szTag;
		CvString m_szName;
	};

	class FeatureVariety
	{
	public:
		FeatureVariety()
		{
		}

		const CvString &getVarietyButton() const
		{
			return m_szVarietyButton;
		}

		const FeatureArtPiece &getFeatureArtPiece(int index) const
		{
			FAssertMsg((index >= 0) && (index < (int) m_aFeatureArtPieces.size()), "[Jason] Invalid feature art index.");
			return m_aFeatureArtPieces[index];
		}

		const FeatureArtPiece &getFeatureArtPieceFromConnectionMask(int connectionMask) const
		{
			for(int i=0;i<(int)m_aFeatureArtPieces.size();i++)
				if(m_aFeatureArtPieces[i].getConnectionMask() == connectionMask)
					return m_aFeatureArtPieces[i];

			FAssertMsg(false, "[Jason] Failed to find feature art piece with valid connection mask.");
			return m_aFeatureArtPieces[0];
		}

		const CvString getFeatureDummyNodeName(const CvString &tagName) const
		{
			for(int i=0;i<(int)m_aFeatureDummyNodes.size();i++)
			{
				if(m_aFeatureDummyNodes[i].getTagName().CompareNoCase(tagName) == 0)
					return m_aFeatureDummyNodes[i].getNodeName();
			}

			FAssertMsg(false, "[Jason] Failed to find dummy tag name.");
			return "";
		}

		const CvString getFeatureDummyTag(const CvString &nodeName) const
		{
			for(int i=0;i<(int)m_aFeatureDummyNodes.size();i++)
			{
				if(m_aFeatureDummyNodes[i].getNodeName().CompareNoCase(nodeName) == 0)
					return m_aFeatureDummyNodes[i].getTagName();
			}

			return "";
		}

		FeatureArtPiece &createFeatureArtPieceFromConnectionMask(int connectionMask)
		{
			for(int i=0;i<(int)m_aFeatureArtPieces.size();i++)
				if(m_aFeatureArtPieces[i].getConnectionMask() == connectionMask)
					return m_aFeatureArtPieces[i];

			m_aFeatureArtPieces.push_back(FeatureArtPiece(connectionMask));
			return m_aFeatureArtPieces.back();
		}

		void createFeatureDummyNode(const CvString &tagName, const CvString &nodeName)
		{
			m_aFeatureDummyNodes.push_back(FeatureDummyNode(tagName, nodeName));
		}

	private:
		std::vector<FeatureArtPiece> m_aFeatureArtPieces;
		std::vector<FeatureDummyNode> m_aFeatureDummyNodes;
		CvString m_szVarietyButton;

		friend CvArtInfoFeature;
	};

	DllExport const FeatureVariety &getVariety(int index) const;
	DllExport int getNumVarieties() const;
	DllExport std::string getFeatureDummyNodeName(int variety, std::string tagName);

protected:

	int getConnectionMaskFromString(const CvString &connectionString);
	int getRotatedConnectionMask(int connectionMask, RotationTypes rotation);

	bool m_bAnimated;
	bool m_bRiverArt;
	TileArtTypes m_eTileArtType;
	LightTypes m_eLightType;
	std::vector<FeatureVariety> m_aFeatureVarieties;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEmphasizeInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEmphasizeInfo :
	public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvEmphasizeInfo();
	virtual ~CvEmphasizeInfo();

	bool isAvoidGrowth() const;				// Exposed to Python
	bool isGreatPeople() const;				// Exposed to Python

/*************************************************************************************************/
/**	New Tag Defs	(CvEmphasizeInfo)		11/15/08								Jean Elcard	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	bool isAvoidAngryCitizens() const;		// Exposed to Python
	bool isAvoidUnhealthyCitizens() const;	// Exposed to Python
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	// Arrays

	int getYieldChange(int i) const;				// Exposed to Python
	int getCommerceChange(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvEmphasizeInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	bool m_bAvoidGrowth;
	bool m_bGreatPeople;

/*************************************************************************************************/
/**	New Tag Defs	(CvEmphasizeInfo)		11/15/08								Jean Elcard	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	bool m_bAvoidAngryCitizens;
	bool m_bAvoidUnhealthyCitizens;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
	// Arrays

	int* m_piYieldModifiers;
	int* m_piCommerceModifiers;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvUpkeepInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvUpkeepInfo :
	public CvInfoBase
{
//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvUpkeepInfo();
	virtual ~CvUpkeepInfo();

	int getPopulationPercent() const;			//	Exposed to Python
	int getCityPercent() const;						//	Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvUpkeepInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL );
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iPopulationPercent;
	int m_iCityPercent;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCultureLevelInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCultureLevelInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvCultureLevelInfo();
	virtual ~CvCultureLevelInfo();

	int getCityDefenseModifier() const;		//	Exposed to Python

	int getSpeedThreshold(int i) const;		//	Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvCultureLevelInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL );
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iCityDefenseModifier;

	int* m_paiSpeedThreshold;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEraInfo
//
//  DESC:   Used to manage different types of Art Styles
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEraInfo :
	public CvInfoBase
{
public:

	CvEraInfo();
	virtual ~CvEraInfo();

	int getStartingUnitMultiplier() const;		//	Exposed to Python
	int getStartingDefenseUnits() const;			//	Exposed to Python
	int getStartingWorkerUnits() const;				//	Exposed to Python
	int getStartingExploreUnits() const;			//	Exposed to Python
	int getAdvancedStartPoints() const;					//	Exposed to Python
	int getStartingGold() const;					//	Exposed to Python
	int getFreePopulation() const;				//	Exposed to Python
	int getStartPercent() const;					//	Exposed to Python
	int getGrowthPercent() const;					//	Exposed to Python
	int getTrainPercent() const;					//	Exposed to Python
	int getConstructPercent() const;			//	Exposed to Python
	int getCreatePercent() const;					//	Exposed to Python
	int getResearchPercent() const;				//	Exposed to Python
	int getBuildPercent() const;					//	Exposed to Python
	int getImprovementPercent() const;		//	Exposed to Python
	int getGreatPeoplePercent() const;		//	Exposed to Python
	int getAnarchyPercent() const;				//	Exposed to Python
	int getEventChancePerTurn() const;				//	Exposed to Python
	int getSoundtrackSpace() const;				//	Exposed to Python
	int getNumSoundtracks() const;				//	Exposed to Python
	const TCHAR* getAudioUnitVictoryScript() const;				//	Exposed to Python
	const TCHAR* getAudioUnitDefeatScript() const;				//	Exposed to Python

	bool isNoGoodies() const;					//	Exposed to Python
	bool isNoAnimals() const;					//	Exposed to Python
	bool isNoBarbUnits() const;				//	Exposed to Python
	bool isNoBarbCities() const;			//	Exposed to Python
	bool isFirstSoundtrackFirst() const;			//	Exposed to Python

	// Arrays

	int getSoundtracks(int i) const;
	int getCitySoundscapeSciptId(int i) const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvEraInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL );
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	int m_iStartingUnitMultiplier;
	int m_iStartingDefenseUnits;
	int m_iStartingWorkerUnits;
	int m_iStartingExploreUnits;
	int m_iAdvancedStartPoints;
	int m_iStartingGold;
	int m_iFreePopulation;
	int m_iStartPercent;
	int m_iGrowthPercent;
	int m_iTrainPercent;
	int m_iConstructPercent;
	int m_iCreatePercent;
	int m_iResearchPercent;
	int m_iBuildPercent;
	int m_iImprovementPercent;
	int m_iGreatPeoplePercent;
	int m_iAnarchyPercent;
	int m_iEventChancePerTurn;
	int m_iSoundtrackSpace;
	int m_iNumSoundtracks;
	CvString m_szAudioUnitVictoryScript;
	CvString m_szAudioUnitDefeatScript;

	bool m_bNoGoodies;
	bool m_bNoAnimals;
	bool m_bNoBarbUnits;
	bool m_bNoBarbCities;
	bool m_bFirstSoundtrackFirst;

	// Arrays

	int* m_paiSoundtracks;
	int* m_paiCitySoundscapeSciptIds;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvColorInfo
//
//  DESC:   Used to manage different types of Art Styles
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvColorInfo :
	public CvInfoBase
{
public:

	DllExport CvColorInfo();
	DllExport virtual ~CvColorInfo();

	DllExport const NiColorA& getColor() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvColorInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL );
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	NiColorA m_Color;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvPlayerColorInfo (ADD to Python)
//
//  DESC:   Used to manage different types of Art Styles
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvPlayerColorInfo :
	public CvInfoBase
{
public:

	DllExport CvPlayerColorInfo();
	DllExport virtual ~CvPlayerColorInfo();

	DllExport int getColorTypePrimary() const;
	DllExport int getColorTypeSecondary() const;
	DllExport int getTextColorType() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvPlayerColorInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL );
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:

	int m_iColorTypePrimary;
	int m_iColorTypeSecondary;
	int m_iTextColorType;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvLandscapeInfo
//
//  Purpose:	This info acts as the Civ4Terrain.ini and is initialize in CvXmlLoadUtility with the infos in
//					XML/Terrain/TerrainSettings.xml
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvLandscapeInfo :
	public CvInfoBase
{
	public:

		DllExport CvLandscapeInfo();
		DllExport virtual ~CvLandscapeInfo() {}

		DllExport int getFogR() const;
		DllExport int getFogG() const;
		DllExport int getFogB() const;
		DllExport int getHorizontalGameCell() const;
		DllExport int getVerticalGameCell() const;
		DllExport int getPlotsPerCellX() const;
		DllExport int getPlotsPerCellY() const;
		DllExport int getHorizontalVertCnt() const;
		DllExport int getVerticalVertCnt() const;
		DllExport int getWaterHeight() const;

		DllExport float getTextureScaleX() const;
		DllExport float getTextureScaleY() const;
		DllExport float getZScale() const;

		DllExport bool isUseTerrainShader() const;
		DllExport bool isUseLightmap() const;
		DllExport bool isRandomMap() const;
		DllExport float getPeakScale() const;
		DllExport float getHillScale() const;

		DllExport const TCHAR* getSkyArt();
		DllExport void setSkyArt(const TCHAR* szPath);
		DllExport const TCHAR* getHeightMap();
		DllExport void setHeightMap(const TCHAR* szPath);
		DllExport const TCHAR* getTerrainMap();
		DllExport void setTerrainMap(const TCHAR* szPath);
		DllExport const TCHAR* getNormalMap();
		DllExport void setNormalMap(const TCHAR* szPath);
		DllExport const TCHAR* getBlendMap();
		DllExport void setBlendMap(const TCHAR* szPath);

		bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
		void copyNonDefaults(CvLandscapeInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	protected:

		int m_iFogR;
		int m_iFogG;
		int m_iFogB;
		int m_iHorizontalGameCell;
		int m_iVerticalGameCell;
		int m_iPlotsPerCellX;
		int m_iPlotsPerCellY;
		int m_iHorizontalVertCnt;
		int m_iVerticalVertCnt;
		int m_iWaterHeight;

		float m_fTextureScaleX;
		float m_fTextureScaleY;
		float m_fZScale;

		float m_fPeakScale;
		float m_fHillScale;

		bool m_bUseTerrainShader;
		bool m_bUseLightmap;
		bool m_bRandomMap;

		CvString m_szSkyArt;
		CvString m_szHeightMap;
		CvString m_szTerrainMap;
		CvString m_szNormalMap;
		CvString m_szBlendMap;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvGameText
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGameText : public CvInfoBase
{
public:
	DllExport CvGameText();

	const wchar* getText() const;
	void setText(const wchar* szText);

	// for Python
	std::wstring pyGetText() const { return getText(); }

	void setGender(const wchar* szGender) { m_szGender = szGender;	}
	const wchar* getGender() const { return m_szGender; }

	void setPlural(const wchar* szPlural) { m_szPlural = szPlural; }
	const wchar* getPlural() const { return m_szPlural; }

	DllExport int getNumLanguages() const; // not static for Python access
	DllExport void setNumLanguages(int iNum); // not static for Python access

	bool read(CvXMLLoadUtility* pXML);

protected:

	CvWString m_szText;
	CvWString m_szGender;
	CvWString m_szPlural;

	static int NUM_LANGUAGES;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvDiplomacyTextInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvDiplomacyTextInfo :	public CvInfoBase
{
	friend class CvXMLLoadUtility;		// so it can access private vars to initialize the class
public:
	struct Response
	{
		DllExport Response() :
			m_iNumDiplomacyText(0),
			m_pbCivilizationTypes(NULL),
			m_pbLeaderHeadTypes(NULL),
			m_pbAttitudeTypes(NULL),
			m_pbDiplomacyPowerTypes(NULL),
			m_paszDiplomacyText(NULL)
		{
		}

		DllExport virtual ~Response ()
		{
			SAFE_DELETE_ARRAY(m_pbCivilizationTypes);
			SAFE_DELETE_ARRAY(m_pbLeaderHeadTypes);
			SAFE_DELETE_ARRAY(m_pbAttitudeTypes);
			SAFE_DELETE_ARRAY(m_pbDiplomacyPowerTypes);
			SAFE_DELETE_ARRAY(m_paszDiplomacyText);
		}

		void read(FDataStreamBase* stream);
		void write(FDataStreamBase* stream);

		int m_iNumDiplomacyText;
		bool* m_pbCivilizationTypes;
		bool* m_pbLeaderHeadTypes;
		bool* m_pbAttitudeTypes;
		bool* m_pbDiplomacyPowerTypes;
		CvString* m_paszDiplomacyText;	// needs to be public for xml load assignment
	};

	DllExport CvDiplomacyTextInfo();
	DllExport virtual ~CvDiplomacyTextInfo() { uninit(); }	// free memory - MT

	// note - Response member vars allocated by CvXmlLoadUtility
	DllExport void init(int iNum);
	DllExport void uninit();

	DllExport const Response& getResponse(int iNum) const { return m_pResponses[iNum]; }	// Exposed to Python
	DllExport int getNumResponses() const;															// Exposed to Python

	DllExport bool getCivilizationTypes(int i, int j) const;						// Exposed to Python
	DllExport bool getLeaderHeadTypes(int i, int j) const;							// Exposed to Python
	DllExport bool getAttitudeTypes(int i, int j) const;								// Exposed to Python
	DllExport bool getDiplomacyPowerTypes(int i, int j) const;					// Exposed to Python

	DllExport int getNumDiplomacyText(int i) const;											// Exposed to Python

	DllExport const TCHAR* getDiplomacyText(int i, int j) const;				// Exposed to Python

	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	bool read(CvXMLLoadUtility* pXML);

private:

	int m_iNumResponses;			// set by init
	Response* m_pResponses;

};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEffectInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEffectInfo :
	public CvInfoBase,
	public CvScalableInfo
{
public:

	DllExport CvEffectInfo();
	DllExport virtual ~CvEffectInfo();

	DllExport const TCHAR* getPath() const { return m_szPath; }
	DllExport void setPath(const TCHAR* szVal) { m_szPath = szVal; }
	DllExport float getUpdateRate( ) const { return m_fUpdateRate; };
	DllExport void setUpdateRate( float fUpdateRate ) { m_fUpdateRate = fUpdateRate; }
	DllExport bool isProjectile() const { return m_bProjectile; };
	DllExport float getProjectileSpeed() const { return m_fProjectileSpeed; };
	DllExport float getProjectileArc() const { return m_fProjectileArc; };
	DllExport bool isSticky() const { return m_bSticky; };
	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvEffectInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	CvString m_szPath;
	float m_fUpdateRate;
	bool m_bProjectile;
	bool m_bSticky;
	float m_fProjectileSpeed;
	float m_fProjectileArc;
};



//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvAttachableInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvAttachableInfo :
	public CvInfoBase,
	public CvScalableInfo
{
public:

	DllExport CvAttachableInfo();
	DllExport virtual ~CvAttachableInfo();

	DllExport const TCHAR* getPath() const { return m_szPath; }
	DllExport void setPath(const TCHAR* szVal) { m_szPath = szVal; }

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvAttachableInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	CvString m_szPath;
	float m_fUpdateRate;
};



//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCameraInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCameraInfo :
	public CvInfoBase
{
public:

	DllExport CvCameraInfo() {}
	DllExport virtual ~CvCameraInfo() {}

	DllExport const TCHAR* getPath() const { return m_szPath; }
	DllExport void setPath(const TCHAR* szVal) { m_szPath = szVal; }

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvCameraInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	CvString m_szPath;
};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvQuestInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvQuestInfo :
	public CvInfoBase
{
public:
	struct QuestLink
	{
		// Stores the QuestLinks Type and Name
		DllExport QuestLink() :
		m_szQuestLinkType("No Type"),
		m_szQuestLinkName("No Name")
		{
		}

	CvString m_szQuestLinkType;
	CvString m_szQuestLinkName;
	};

	DllExport CvQuestInfo();
	DllExport virtual ~CvQuestInfo();

	DllExport void reset();
	DllExport bool initQuestLinks(int iNum);

	DllExport int getNumQuestMessages() const;
	DllExport int getNumQuestLinks() const;
	DllExport int getNumQuestSounds() const;
	DllExport const TCHAR* getQuestObjective() const;
	DllExport const TCHAR* getQuestBodyText() const;
	DllExport const TCHAR* getQuestMessages(int iIndex) const;
	DllExport const TCHAR* getQuestLinkType(int iIndex) const;
	DllExport const TCHAR* getQuestLinkName(int iIndex) const;
	DllExport const TCHAR* getQuestSounds(int iIndex) const;
	DllExport const TCHAR* getQuestScript() const;

	DllExport void setNumQuestMessages(int iNum);
	DllExport void setNumQuestSounds(int iNum);
	DllExport void setQuestObjective(const TCHAR* szText);
	DllExport void setQuestBodyText(const TCHAR* szText);
	DllExport void setQuestMessages(int iIndex, const TCHAR* szText);
	DllExport void setQuestSounds(int iIndex, const TCHAR* szText);
	DllExport void setQuestScript(const TCHAR* szText);

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvQuestInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	int m_iNumQuestMessages;
	int m_iNumQuestLinks;
	int m_iNumQuestSounds;

	CvString m_szQuestObjective;
	CvString m_szQuestBodyText;
	CvString m_szQuestScript;

	CvString* m_paszQuestMessages;
	QuestLink* m_pQuestLinks;
	CvString* m_paszQuestSounds;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTutorialInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTutorialMessage
{
public:
	DllExport CvTutorialMessage();
	DllExport virtual ~CvTutorialMessage();

	DllExport const TCHAR* getText() const;
	DllExport const TCHAR* getImage() const;
	DllExport const TCHAR* getSound() const;

	DllExport void setText(const TCHAR* szText);
	DllExport void setImage(const TCHAR* szText);
	DllExport void setSound(const TCHAR* szText);
	DllExport void setScript(int iIndex, const TCHAR* szText);

	DllExport int getNumTutorialScripts() const;
	DllExport const TCHAR* getTutorialScriptByIndex(int i) const;
	bool read(CvXMLLoadUtility* pXML);

private:
	int m_iNumTutorialScripts;
	CvString m_szTutorialMessageText;
	CvString m_szTutorialMessageImage;
	CvString m_szTutorialMessageSound;
	CvString* m_paszTutorialScripts;
};

class CvTutorialMessage;
class CvTutorialInfo :
	public CvInfoBase
{
public:
	DllExport CvTutorialInfo();
	DllExport virtual ~CvTutorialInfo();

	DllExport const TCHAR* getNextTutorialInfoType();
	DllExport void setNextTutorialInfoType(const TCHAR* szVal);

	DllExport bool initTutorialMessages(int iNum);
	DllExport void resetMessages();

	DllExport int getNumTutorialMessages() const;
	DllExport const CvTutorialMessage* getTutorialMessage(int iIndex) const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvTutorialInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	CvString m_szNextTutorialInfoType;
	int m_iNumTutorialMessages;
	CvTutorialMessage* m_paTutorialMessages;
};


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvGameOptionInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGameOptionInfo :
	public CvInfoBase
{
public:
	DllExport CvGameOptionInfo();
	DllExport virtual ~CvGameOptionInfo();

	DllExport bool getDefault() const;
	DllExport bool getVisible() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvGameOptionInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	bool m_bDefault;
	bool m_bVisible;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvMPOptionInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvMPOptionInfo :
	public CvInfoBase
{
public:
	DllExport CvMPOptionInfo();
	DllExport virtual ~CvMPOptionInfo();

	DllExport bool getDefault() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvMPOptionInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	bool m_bDefault;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvForceControlInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvForceControlInfo :
	public CvInfoBase
{
public:
	DllExport CvForceControlInfo();
	DllExport virtual ~CvForceControlInfo();

	DllExport bool getDefault() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvForceControlInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	bool m_bDefault;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvPlayerOptionInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvPlayerOptionInfo :
	public CvInfoBase
{
public:
	DllExport CvPlayerOptionInfo();
	DllExport virtual ~CvPlayerOptionInfo();

	DllExport bool getDefault() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvPlayerOptionInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	bool m_bDefault;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvGraphicOptionInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvGraphicOptionInfo :
	public CvInfoBase
{
public:
	DllExport CvGraphicOptionInfo();
	DllExport virtual ~CvGraphicOptionInfo();

	DllExport bool getDefault() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvGraphicOptionInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	bool m_bDefault;

};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEventTriggerInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEventTriggerInfo : public CvInfoBase
{
	friend class CvXMLLoadUtility;

public:
	CvEventTriggerInfo();
	virtual ~CvEventTriggerInfo();

	int getPercentGamesActive() const;		// Exposed to Python
	int getProbability() const;				// Exposed to Python
	int getNumUnits() const;					// Exposed to Python
	int getNumBuildings() const;				// Exposed to Python
	int getNumUnitsGlobal() const;			// Exposed to Python
	int getNumBuildingsGlobal() const;		// Exposed to Python
	int getNumPlotsRequired() const;			// Exposed to Python
	int getPlotType() const;					// Exposed to Python
	int getNumReligions() const;				// Exposed to Python
	int getNumCorporations() const;			// Exposed to Python
	int getOtherPlayerShareBorders() const;	// Exposed to Python
	int getOtherPlayerHasTech() const;		// Exposed to Python
	int getCityFoodWeight() const;			// Exposed to Python
	int getCivic() const;						// Exposed to Python
	int getMinPopulation() const;				// Exposed to Python
	int getMaxPopulation() const;				// Exposed to Python
	int getMinMapLandmass() const;			// Exposed to Python
	int getMinOurLandmass() const;			// Exposed to Python
	int getMaxOurLandmass() const;			// Exposed to Python
	int getMinDifficulty() const;				// Exposed to Python
	int getAngry() const;						// Exposed to Python
	int getUnhealthy() const;					// Exposed to Python
	int getUnitDamagedWeight() const;			// Exposed to Python
	int getUnitDistanceWeight() const;		// Exposed to Python
	int getUnitExperienceWeight() const;		// Exposed to Python
	int getMinTreasury() const;				// Exposed to Python

	int getBuildingRequired(int i) const;		// Exposed to Python
	int getNumBuildingsRequired() const;		// Exposed to Python
	int getUnitRequired(int i) const;			// Exposed to Python
	int getNumUnitsRequired() const;			// Exposed to Python
	int getPrereqOrTechs(int i) const;		// Exposed to Python
	int getNumPrereqOrTechs() const;			// Exposed to Python
	int getPrereqAndTechs(int i) const;		// Exposed to Python
	int getNumPrereqAndTechs() const;			// Exposed to Python
	int getObsoleteTech(int i) const;				// Exposed to Python
	int getNumObsoleteTechs() const;				// Exposed to Python
	int getEvent(int i) const;				// Exposed to Python
	int getNumEvents() const;					// Exposed to Python
	int getPrereqEvent(int i) const;			// Exposed to Python
	int getNumPrereqEvents() const;			// Exposed to Python
	int getFeatureRequired(int i) const;		// Exposed to Python
	int getNumFeaturesRequired() const;		// Exposed to Python
	int getTerrainRequired(int i) const;		// Exposed to Python
	int getNumTerrainsRequired() const;		// Exposed to Python
	int getImprovementRequired(int i) const;	// Exposed to Python
	int getNumImprovementsRequired() const;	// Exposed to Python
	int getBonusRequired(int i) const;		// Exposed to Python
	int getNumBonusesRequired() const;		// Exposed to Python
	int getRouteRequired(int i) const;		// Exposed to Python
	int getNumRoutesRequired() const;			// Exposed to Python
	int getReligionRequired(int i) const;		// Exposed to Python
	int getNumReligionsRequired() const;		// Exposed to Python
	int getCorporationRequired(int i) const;	// Exposed to Python
	int getNumCorporationsRequired() const;	// Exposed to Python

	const CvWString& getText(int i) const;
	int getTextEra(int i) const;
	int getNumTexts() const;
	const CvWString& getWorldNews(int i) const;
	int getNumWorldNews() const;

	bool isSinglePlayer() const;				// Exposed to Python
	bool isTeam() const;						// Exposed to Python
	bool isRecurring() const;					// Exposed to Python
	bool isGlobal() const;					// Exposed to Python
	bool isPickPlayer() const;				// Exposed to Python
	bool isOtherPlayerWar() const;			// Exposed to Python
	bool isOtherPlayerHasReligion() const;	// Exposed to Python
	bool isOtherPlayerHasOtherReligion() const;	// Exposed to Python
	bool isOtherPlayerAI() const;				// Exposed to Python
	bool isPickCity() const;					// Exposed to Python
	bool isPickOtherPlayerCity() const;		// Exposed to Python
	bool isShowPlot() const;					// Exposed to Python
	bool isUnitsOnPlot() const;				// Exposed to Python
	bool isOwnPlot() const;					// Exposed to Python
	bool isPickReligion() const;				// Exposed to Python
	bool isStateReligion() const;				// Exposed to Python
	bool isHolyCity() const;					// Exposed to Python
	bool isPickCorporation() const;			// Exposed to Python
	bool isHeadquarters() const;				// Exposed to Python
	bool isProbabilityUnitMultiply() const;	// Exposed to Python
	bool isProbabilityBuildingMultiply() const;	// Exposed to Python
	bool isPrereqEventCity() const;			// Exposed to Python

	const char* getPythonCallback() const;
	const char* getPythonCanDo() const;
	const char* getPythonCanDoCity() const;
	const char* getPythonCanDoUnit() const;

/*************************************************************************************************/
/**	New Tag Defs	(EventTriggerInfos)		05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getPrereqBroadAlignment() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Events: Added by Kael 08/08/2007
	int getPrereqCrime() const;
	int getPrereqGlobalCounter() const;
	int getPrereqAlignment() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getPrereqBroadEthicalAlignment() const;
	int getPrereqEthicalAlignment() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int getPrereqCivilizationPleased() const;
	int getPrereqLeader() const;
	int getPrereqTrait() const;
//FfH: End Add
	//FlagSystem
	int getPrereqFlags(int i) const;		// Exposed to Python
	int getNumPrereqFlags() const;			// Exposed to Python
	int getPrereqNotFlags(int i) const;		// Exposed to Python
	int getNumPrereqNotFlags() const;			// Exposed to Python

	void read(FDataStreamBase* );
	void write(FDataStreamBase* );

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvEventTriggerInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	int m_iPercentGamesActive;
	int m_iProbability;
	int m_iNumUnits;
	int m_iNumBuildings;
	int m_iNumUnitsGlobal;
	int m_iNumBuildingsGlobal;
	int m_iNumPlotsRequired;
	int m_iPlotType;
	int m_iNumReligions;
	int m_iNumCorporations;
	int m_iOtherPlayerShareBorders;
	int m_iOtherPlayerHasTech;
	int m_iCityFoodWeight;
	int m_iCivic;
	int m_iMinPopulation;
	int m_iMaxPopulation;
	int m_iMinMapLandmass;
	int m_iMinOurLandmass;
	int m_iMaxOurLandmass;
	int m_iMinDifficulty;
	int m_iAngry;
	int m_iUnhealthy;
	int m_iUnitDamagedWeight;
	int m_iUnitDistanceWeight;
	int m_iUnitExperienceWeight;
	int m_iMinTreasury;

	std::vector<int> m_aiUnitsRequired;
	std::vector<int> m_aiBuildingsRequired;
	std::vector<int> m_aiPrereqOrTechs;
	std::vector<int> m_aiPrereqAndTechs;
	std::vector<int> m_aiObsoleteTechs;
	std::vector<int> m_aiEvents;
	std::vector<int> m_aiPrereqEvents;
	std::vector<int> m_aiFeaturesRequired;
	std::vector<int> m_aiTerrainsRequired;
	std::vector<int> m_aiImprovementsRequired;
	std::vector<int> m_aiBonusesRequired;
	std::vector<int> m_aiRoutesRequired;
	std::vector<int> m_aiReligionsRequired;
	std::vector<int> m_aiCorporationsRequired;

	std::vector<int> m_aiTextEra;
	std::vector<CvWString> m_aszText;
	std::vector<CvWString> m_aszWorldNews;

	bool m_bSinglePlayer;
	bool m_bTeam;
	bool m_bRecurring;
	bool m_bGlobal;
	bool m_bPickPlayer;
	bool m_bOtherPlayerWar;
	bool m_bOtherPlayerHasReligion;
	bool m_bOtherPlayerHasOtherReligion;
	bool m_bOtherPlayerAI;
	bool m_bPickCity;
	bool m_bPickOtherPlayerCity;
	bool m_bShowPlot;
	bool m_bUnitsOnPlot;
	bool m_bOwnPlot;
	bool m_bPickReligion;
	bool m_bStateReligion;
	bool m_bHolyCity;
	bool m_bPickCorporation;
	bool m_bHeadquarters;
	bool m_bProbabilityUnitMultiply;
	bool m_bProbabilityBuildingMultiply;
	bool m_bPrereqEventCity;

	CvString m_szPythonCallback;
	CvString m_szPythonCanDo;
	CvString m_szPythonCanDoCity;
	CvString m_szPythonCanDoUnit;

/*************************************************************************************************/
/**	New Tag Defs	(EventTriggerInfos)		05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iPrereqBroadAlignment;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH Events: Added by Kael 08/08/2007
	int m_iPrereqCrime;
	int m_iPrereqGlobalCounter;
	int m_iPrereqAlignment;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iPrereqBroadEthicalAlignment;
	int m_iPrereqEthicalAlignment;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int m_iPrereqCivilizationPleased;
	int m_iPrereqLeader;
	int m_iPrereqTrait;
//FfH: End Add
	//FlagSystem
	std::vector<int> m_aiPrereqFlags;
	std::vector<int> m_aiPrereqNotFlags;


};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEventInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEventInfo : public CvInfoBase
{
	friend class CvXMLLoadUtility;

public:
	CvEventInfo();
	virtual ~CvEventInfo();

	bool isQuest() const;						// Exposed to Python
	bool isGlobal() const;					// Exposed to Python
	bool isTeam() const;						// Exposed to Python
	bool isCityEffect() const;				// Exposed to Python
	bool isOtherPlayerCityEffect() const;		// Exposed to Python
	bool isGoldToPlayer() const;				// Exposed to Python
	bool isGoldenAge() const;					// Exposed to Python
	bool isDeclareWar() const;				// Exposed to Python
	bool isDisbandUnit() const;				// Exposed to Python

	int getGold() const;						// Exposed to Python
	int getRandomGold() const;				// Exposed to Python
	int getEspionagePoints() const;			// Exposed to Python
	int getCulture() const;					// Exposed to Python
	int getTech() const;						// Exposed to Python
	int getTechPercent() const;				// Exposed to Python
	int getTechCostPercent() const;			// Exposed to Python
	int getTechMinTurnsLeft() const;			// Exposed to Python
	int getPrereqTech() const;				// Exposed to Python
	int getUnitClass() const;					// Exposed to Python
	int getNumUnits() const;					// Exposed to Python
	int getBuildingClass() const;				// Exposed to Python
	int getBuildingChange() const;			// Exposed to Python
	int getHappy() const;						// Exposed to Python
	int getHealth() const;					// Exposed to Python
	int getHurryAnger() const;				// Exposed to Python
	int getHappyTurns() const;				// Exposed to Python
	int getFood() const;						// Exposed to Python
	int getFoodPercent() const;				// Exposed to Python
	int getProduction() const;				// Exposed to Python
	int getFeature() const;					// Exposed to Python
	int getFeatureChange() const;				// Exposed to Python
	int getImprovement() const;				// Exposed to Python
	int getImprovementChange() const;			// Exposed to Python
	int getBonus() const;						// Exposed to Python
	int getBonusChange() const;				// Exposed to Python
	int getRoute() const;						// Exposed to Python
	int getRouteChange() const;				// Exposed to Python
	int getBonusRevealed() const;				// Exposed to Python
	int getBonusGift() const;					// Exposed to Python
	int getUnitExperience() const;			// Exposed to Python
	int getUnitImmobileTurns() const;			// Exposed to Python
	int getConvertOwnCities() const;			// Exposed to Python
	int getConvertOtherCities() const;		// Exposed to Python
	int getMaxNumReligions() const;			// Exposed to Python
	int getOurAttitudeModifier() const;		// Exposed to Python
	int getAttitudeModifier() const;			// Exposed to Python
	int getTheirEnemyAttitudeModifier() const;// Exposed to Python
	int getPopulationChange() const;			// Exposed to Python
	int getRevoltTurns() const;				// Exposed to Python
	int getMinPillage() const;				// Exposed to Python
	int getMaxPillage() const;				// Exposed to Python
	int getUnitPromotion() const;				// Exposed to Python
	int getFreeUnitSupport() const;			// Exposed to Python
	int getInflationModifier() const;			// Exposed to Python
	int getSpaceProductionModifier() const;	// Exposed to Python
	int getAIValue() const;	// Exposed to Python

	int getAdditionalEventChance(int i) const;// Exposed to Python
	int getAdditionalEventTime(int i) const;	// Exposed to Python
	int getClearEventChance(int i) const;		// Exposed to Python
	int getTechFlavorValue(int i) const;		// Exposed to Python
	int getPlotExtraYield(int i) const;		// Exposed to Python
	int getFreeSpecialistClassCount(int i) const;	// Exposed to Python
	int getUnitCombatPromotion(int i) const;	// Exposed to Python
	int getUnitClassPromotion(int i) const;	// Exposed to Python
	const CvWString& getWorldNews(int i) const;
	int getNumWorldNews() const;

	int getBuildingYieldChange(int iBuildingClass, int iYield) const;
	int getNumBuildingYieldChanges() const;
	int getBuildingCommerceChange(int iBuildingClass, int iCommerce) const;
	int getNumBuildingCommerceChanges() const;
	int getBuildingHappyChange(int iBuildingClass) const;
	int getNumBuildingHappyChanges() const;
	int getBuildingHealthChange(int iBuildingClass) const;
	int getNumBuildingHealthChanges() const;

/*************************************************************************************************/
/**	New Tag Defs	(EventInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Function for Use in .cpp								**/
/*************************************************************************************************/
	int getAlignmentModifier() const;
	int getAlignmentModTowardsNeutral() const;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/
//FfH: Added by Kael 01/21/2008
	int getCrime() const;
	int getGlobalCounter() const;
	int getPrereqAlignment() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getEthicalAlignmentModifier() const;
	int getEthicalAlignmentModTowardsNeutral() const;
	int getPrereqEthicalAlignment() const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int getPrereqBonus() const;
	int getPrereqCivilization() const;
	int getPrereqCorporation() const;
	int getPrereqReligion() const;
	int getPrereqStateReligion() const;
//FfH: End Add

	const char* getPythonCallback() const;
	const char* getPythonExpireCheck() const;
	const char* getPythonCanDo() const;
	const char* getPythonHelp() const;
	const wchar* getUnitNameKey() const;
	const wchar* getQuestFailTextKey() const;
	const wchar* getOtherPlayerPopup() const;
	const wchar* getLocalInfoTextKey() const;

	void read(FDataStreamBase* );
	void write(FDataStreamBase* );

	bool read(CvXMLLoadUtility* pXML);
	bool readPass2(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvEventInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	void copyNonDefaultsReadPass2(CvEventInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

private:
	bool m_bQuest;
	bool m_bGlobal;
	bool m_bTeam;
	bool m_bCityEffect;
	bool m_bOtherPlayerCityEffect;
	bool m_bGoldToPlayer;
	bool m_bGoldenAge;
	bool m_bDeclareWar;
	bool m_bDisbandUnit;

	int m_iGold;
	int m_iRandomGold;
	int m_iCulture;
	int m_iEspionagePoints;
	int m_iTech;
	int m_iTechPercent;
	int m_iTechCostPercent;
	int m_iTechMinTurnsLeft;
	int m_iPrereqTech;
	int m_iUnitClass;
	int m_iNumUnits;
	int m_iBuildingClass;
	int m_iBuildingChange;
	int m_iHappy;
	int m_iHealth;
	int m_iHurryAnger;
	int m_iHappyTurns;
	int m_iFood;
	int m_iFoodPercent;
	int m_iProduction;
	int m_iFeature;
	int m_iFeatureChange;
	int m_iImprovement;
	int m_iImprovementChange;
	int m_iBonus;
	int m_iBonusChange;
	int m_iRoute;
	int m_iRouteChange;
	int m_iBonusRevealed;
	int m_iBonusGift;
/*************************************************************************************************/
/**	DecimalXP							11/21/08									Xienwolf	**/
/**																								**/
/**					XP Values carried as Floats now in XML, 100x value in DLL					**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
	int m_iUnitExperience;
/**								----  End Original Code  ----									**/
	float m_iUnitExperience;
/*************************************************************************************************/
/**	DecimalXP									END												**/
/*************************************************************************************************/
	int m_iUnitImmobileTurns;
	int m_iConvertOwnCities;
	int m_iConvertOtherCities;
	int m_iMaxNumReligions;
	int m_iOurAttitudeModifier;
	int m_iAttitudeModifier;
	int m_iTheirEnemyAttitudeModifier;
	int m_iPopulationChange;
	int m_iRevoltTurns;
	int m_iMinPillage;
	int m_iMaxPillage;
	int m_iUnitPromotion;
	int m_iFreeUnitSupport;
	int m_iInflationModifier;
	int m_iSpaceProductionModifier;
	int m_iAIValue;
/*************************************************************************************************/
/**	New Tag Defs	(EventInfos)			05/15/08								Xienwolf	**/
/**																								**/
/**								Defines Variable for Use in .cpp								**/
/*************************************************************************************************/
	int m_iAlignmentModifier;
	int m_iAlignmentModTowardsNeutral;
/*************************************************************************************************/
/**	New Tag Defs							END													**/
/*************************************************************************************************/

//FfH: Added by Kael 01/21/2008
	int m_iCrime;
	int m_iGlobalCounter;
	int m_iPrereqAlignment;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iPrereqEthicalAlignment;
	int m_iEthicalAlignmentModifier;
	int m_iEthicalAlignmentModTowardsNeutral;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int m_iPrereqBonus;
	int m_iPrereqCivilization;
	int m_iPrereqCorporation;
	int m_iPrereqReligion;
	int m_iPrereqStateReligion;
//FfH: End Add

	int* m_piTechFlavorValue;
	int* m_piPlotExtraYields;
	int* m_piFreeSpecialistClassCount;
	int* m_piAdditionalEventChance;
	int* m_piAdditionalEventTime;
	int* m_piClearEventChance;
	int* m_piUnitCombatPromotions;
	int* m_piUnitClassPromotions;

	std::vector<BuildingYieldChange> m_aBuildingYieldChanges;
	std::vector<BuildingCommerceChange> m_aBuildingCommerceChanges;
	BuildingChangeArray m_aBuildingHappyChanges;
	BuildingChangeArray m_aBuildingHealthChanges;

	CvString m_szPythonCallback;
	CvString m_szPythonExpireCheck;
	CvString m_szPythonCanDo;
	CvString m_szPythonHelp;
	CvWString m_szUnitName;
	CvWString m_szOtherPlayerPopup;
	CvWString m_szQuestFailText;
	CvWString m_szLocalInfoText;
	std::vector<CvWString> m_aszWorldNews;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvEspionageMissionInfo
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvEspionageMissionInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvEspionageMissionInfo();
	virtual ~CvEspionageMissionInfo();

	int getCost() const;
	bool isPassive() const;
	bool isTwoPhases() const;
	bool isTargetsCity() const;
	bool isSelectPlot() const;

	int getTechPrereq() const;
	int getVisibilityLevel() const;
	bool isInvestigateCity() const;
	bool isSeeDemographics() const;
	bool isNoActiveMissions() const;
	bool isSeeResearch() const;

	bool isDestroyImprovement() const;
	int getDestroyBuildingCostFactor() const;
	int getDestroyUnitCostFactor() const;
	int getDestroyProjectCostFactor() const;
	int getDestroyProductionCostFactor() const;
	int getBuyUnitCostFactor() const;
	int getBuyCityCostFactor() const;
	int getStealTreasuryTypes() const;
	int getCityInsertCultureAmountFactor() const;
	int getCityInsertCultureCostFactor() const;
	int getCityPoisonWaterCounter() const;
	int getCityUnhappinessCounter() const;
	int getCityRevoltCounter() const;
	int getBuyTechCostFactor() const;
	int getSwitchCivicCostFactor() const;
	int getSwitchReligionCostFactor() const;
	int getPlayerAnarchyCounter() const;
	int getCounterespionageNumTurns() const;
	int getCounterespionageMod() const;
	int getDifficultyMod() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvEspionageMissionInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------
protected:

	int m_iCost;
	bool m_bIsPassive;
	bool m_bIsTwoPhases;
	bool m_bTargetsCity;
	bool m_bSelectPlot;

	int m_iTechPrereq;
	int m_iVisibilityLevel;
	bool m_bInvestigateCity;
	bool m_bSeeDemographics;
	bool m_bNoActiveMissions;
	bool m_bSeeResearch;

	bool m_bDestroyImprovement;
	int m_iDestroyBuildingCostFactor;
	int m_iDestroyUnitCostFactor;
	int m_iDestroyProjectCostFactor;
	int m_iDestroyProductionCostFactor;
	int m_iBuyUnitCostFactor;
	int m_iBuyCityCostFactor;
	int m_iStealTreasuryTypes;
	int m_iCityInsertCultureAmountFactor;
	int m_iCityInsertCultureCostFactor;
	int m_iCityPoisonWaterCounter;
	int m_iCityUnhappinessCounter;
	int m_iCityRevoltCounter;
	int m_iBuyTechCostFactor;
	int m_iSwitchCivicCostFactor;
	int m_iSwitchReligionCostFactor;
	int m_iPlayerAnarchyCounter;
	int m_iCounterespionageNumTurns;
	int m_iCounterespionageMod;
	int m_iDifficultyMod;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvUnitArtStyleTypeInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvUnitArtStyleTypeInfo : public CvInfoBase
{
public:

	CvUnitArtStyleTypeInfo();
	virtual ~CvUnitArtStyleTypeInfo();

	const TCHAR* getEarlyArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j, int iPromo = -1, bool bbypassSecondaryCheck=false) const;
	void setEarlyArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j, const TCHAR* szVal, int iPromo=-1);
	const TCHAR* getLateArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j) const;
	void setLateArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j, const TCHAR* szVal);
	const TCHAR* getMiddleArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j) const;
	void setMiddleArtDefineTag(int /*Mesh Index*/ i, int /*UnitType*/ j, const TCHAR* szVal);
	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvUnitArtStyleTypeInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/
	int getEarlyArtDefineArraySize();
	int getEarlyArtDefineMesh(int i);
	int getEarlyArtDefineUnit(int i);
	int getEarlyArtDefinePromo(int i);
	CvString getEarlyArtDefineTag(int i);

protected:

	struct ArtDefneTag
	{
		int iMeshIndex;
		int iUnitType;
		int iPromoType;
		CvString szTag;
	};
	typedef std::vector<ArtDefneTag> ArtDefineArray;
	ArtDefineArray m_azEarlyArtDefineTags;
	ArtDefineArray m_azLateArtDefineTags;
	ArtDefineArray m_azMiddleArtDefineTags;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvVoteSourceInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvVoteSourceInfo : public CvInfoBase
{
public:

	CvVoteSourceInfo();
	virtual ~CvVoteSourceInfo();

	int getVoteInterval() const;					// Exposed to Python
	int getFreeSpecialistClass() const;					// Exposed to Python
	int getCivic() const;					// Exposed to Python
	const CvWString getPopupText() const;
	const CvWString getSecretaryGeneralText() const;
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	const CvString& getCopyPopupText() const;
	const CvString& getCopySecretaryGeneralText() const;
	int getCivicVectorSize();
	CvString getCivicVectorElement(int i);
	void copyNonDefaults(CvVoteSourceInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

	std::wstring pyGetSecretaryGeneralText() { return getSecretaryGeneralText(); }						// Exposed to Python

	int getReligionYield(int i) const;					// Exposed to Python
	int getReligionCommerce(int i) const;					// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();

protected:
	int m_iVoteInterval;
	int m_iFreeSpecialistClass;
	int m_iCivic;

	int* m_aiReligionYields;
	int* m_aiReligionCommerces;

	CvString m_szPopupText;
	CvString m_szSecretaryGeneralText;
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvMainMenuInfo
//
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvMainMenuInfo : public CvInfoBase
{
public:

	DllExport CvMainMenuInfo();
	DllExport virtual ~CvMainMenuInfo();

	DllExport std::string getScene() const;
	DllExport std::string getSceneNoShader() const;
	DllExport std::string getSoundtrack() const;
	DllExport std::string getLoading() const;
	DllExport std::string getLoadingSlideshow() const;

	bool read(CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**																								**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
	void copyNonDefaults(CvMainMenuInfo* pClassInfo, CvXMLLoadUtility* pXML);
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

protected:
	std::string m_szScene;
	std::string m_szSceneNoShader;
	std::string m_szSoundtrack;
	std::string m_szLoading;
	std::string m_szLoadingSlideshow;
};

// Official Belief, created by poyuzhe 12.01.08, added by Opera 31.05.09, added by Valkrionn 09.26.09
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvLeaderRelationInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvLeaderRelationInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvLeaderRelationInfo();
	DllExport virtual ~CvLeaderRelationInfo();

	int getLeaderType() const;
	int getLeaderAttitudeChange(int i) const; 		// Exposed to Python

	// Arrays


	DllExport bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iLeaderType;
	int* m_paiLeaderAttitudeChange;
	// Arrays


};
/*************************************************************************************************/
/** EndAdd																						**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	TrueModular								05/26/09	Written: Mr. Genie	Imported: Xienwolf	**/
/**Reasonably certain these are useless, but wanted to merge everything before trimming anything**/
/**	Properly links Modular modifications to previous elements, and allows partial overwriting	**/
/*************************************************************************************************/
// Python Modular Loading
class CvPythonModulesInfo : public CvInfoBase
{
public:
	CvPythonModulesInfo();
	virtual ~CvPythonModulesInfo();

	bool isMainInterfaceScreen();
	bool isCivicScreen();
	bool isCorporationScreen();
	bool isDomesticAdvisor();
	bool isEspionageAdvisor();
	bool isForeignAdvisor();
	bool isMilitaryAdvisor();
	bool isVictoryScreen();
	int getScreen();

	bool read(CvXMLLoadUtility* pXML);

protected:

	bool m_bMainInterfaceScreen;
	bool m_bCivicScreen;
	bool m_bCorporationScreen;
	bool m_bDomesticAdvisor;
	bool m_bEspionageAdvisor;
	bool m_bForeignAdvisor;
	bool m_bMilitaryAdvisor;
	bool m_bVictoryScreen;
	int m_iScreen;

};

// MLF loading
class CvModLoadControlInfo : public CvInfoBase
{
public:

	CvModLoadControlInfo();
	virtual ~CvModLoadControlInfo();

	bool isLoad(int i);
	void setLoad(int i, bool bLoad = true);
	std::string getModuleFolder(int i);
	std::string getParentFolder();
	int getNumModules();
	int getDirDepth();
	bool read(CvXMLLoadUtility* pXML, CvString szDirDepth, int iDirDepth);

protected:
	bool* m_bLoad;
	int m_iNumModules;
	int m_iDirDepth;
	std::string* m_paszModuleFolder;
	std::string m_paszParentFolder;
};
/*************************************************************************************************/
/**	TrueModular								END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	StateNames								12/12/08								Jean Elcard	**/
/**																								**/
/**								Declares a new class for State Names.							**/
/*************************************************************************************************/
class CvStateNameInfo : public CvInfoBase
{
public:

	CvStateNameInfo();
	virtual ~CvStateNameInfo();

	bool isFullCiv() const;
	bool isMinorCiv() const;
	bool isSovereign() const;
	bool isVassal() const;
	bool isColony() const;
	bool isFemaleLeader() const;

	int getMinNumCities() const;
	int getMaxNumCities() const;
	int getMinNumVassals() const;
	int getMinNumCitiesConquered() const;

	int getNumPrereqCivics() const;
	int getPrereqCivic(int iI) const;

	int getNumPrereqAlignments() const;
	int getPrereqAlignment(int iI) const;

/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int getNumPrereqEthicalAlignments() const;
	int getPrereqEthicalAlignment(int iI) const;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/

	int getPrereqCivilization() const;
	int getPrereqLeader() const;
	int getPrereqReligion() const;

	bool read(CvXMLLoadUtility* pXML);
	void copyNonDefaults(CvStateNameInfo* pClassInfo, CvXMLLoadUtility* pXML);

protected:

	int m_iMinNumCities;
	int m_iMaxNumCities;
	int m_iMinNumCitiesConquered;
	int m_iMinNumVassals;
	int m_iNumPrereqCivics;
	int m_iNumPrereqAlignments;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int m_iNumPrereqEthicalAlignments;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
	int m_iPrereqCivilization;
	int m_iPrereqLeader;
	int m_iPrereqReligion;

	bool m_bFullCiv;
	bool m_bMinorCiv;
	bool m_bSovereign;
	bool m_bVassal;
	bool m_bColony;
	bool m_bFemaleLeader;

	int* m_piPrereqCivics;
	int* m_piPrereqAlignments;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments 				11/06/09								Valkrionn	**/
/**																								**/
/**							Adds a new alignment axis to the game								**/
/*************************************************************************************************/
	int* m_piPrereqEthicalAlignments;
/*************************************************************************************************/
/**	Lawful-Chaotic Alignments					END												**/
/*************************************************************************************************/
};
/*************************************************************************************************/
/**	StateNames								END													**/
/*************************************************************************************************/
/*************************************************************************************************/
/**	Spawn Groups						08/05/10									Valkrionn	**/
/**																								**/
/**					New spawn mechanic, allowing us to customize stacks							**/
/*************************************************************************************************/
class CvSpawnGroupInfo : public CvInfoBase
{
public:

	CvSpawnGroupInfo();
	virtual ~CvSpawnGroupInfo();

	int getPrereqMinTurn() const;								// Exposed to Python
	int getPrereqMaxTurn() const;								// Exposed to Python
	int getPrereqMinAC() const;									// Exposed to Python
	int getPrereqMaxAC() const;									// Exposed to Python
	int getPrereqProject() const;								// Exposed to Python
	int getWeight() const;										// Exposed to Python
	int getNumCommanderUnits() const;							// Exposed to Python
	int getNumGroupPromotions() const;							// Exposed to Python
	int getNumCommanderPromotions() const;						// Exposed to Python
	int getNumSpawnTerrains() const;							// Exposed to Python
	int getNumSpawnFeatures() const;							// Exposed to Python
	int getNumPrereqTechANDs() const;							// Exposed to Python
	int getNumPrereqTechORs() const;							// Exposed to Python
	int getNumBlockTechANDs() const;							// Exposed to Python
	int getNumBlockTechORs() const;								// Exposed to Python

	bool isUnique() const;										// Exposed to Python
	bool isAlwaysSpawn() const;									// Exposed to Python
	bool isNeverSpawn() const;									// Exposed to Python
	bool isNaval() const;										// Exposed to Python

	int getCommanderUnits(int i) const;							// Exposed to Python
	int getGroupUnits(int i) const;								// Exposed to Python
	int getGroupUnitClasses(int i) const;						// Exposed to Python
	int getGroupPromotions(int iI) const;						// Exposed to Python
	int getCommanderPromotions(int iI) const;					// Exposed to Python
	int getSpawnTerrains(int iI) const;							// Exposed to Python
	int getSpawnFeatures(int iI) const;							// Exposed to Python
	int getPrereqTechANDs(int iI) const;						// Exposed to Python
	int getPrereqTechORs(int iI) const;							// Exposed to Python
	int getBlockTechANDs(int iI) const;							// Exposed to Python
	int getBlockTechORs(int iI) const;							// Exposed to Python

	DllExport const TCHAR* getPyRequirement() const;			// Exposed to Python
	DllExport const TCHAR* getPyOnSpawn() const;				// Exposed to Python
	DllExport const TCHAR* getBanner() const;					// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
	void copyNonDefaults(CvSpawnGroupInfo* pClassInfo, CvXMLLoadUtility* pXML);

protected:

	int m_iPrereqMinTurn;
	int m_iPrereqMaxTurn;
	int m_iPrereqMinAC;
	int m_iPrereqMaxAC;
	int m_iPrereqProject;
	int m_iWeight;
	int m_iNumCommanderUnits;
	int m_iNumGroupPromotions;
	int m_iNumCommanderPromotions;
	int m_iNumSpawnTerrains;
	int m_iNumSpawnFeatures;
	int m_iNumPrereqTechANDs;
	int m_iNumPrereqTechORs;
	int m_iNumBlockTechANDs;
	int m_iNumBlockTechORs;

	bool m_bUnique;
	bool m_bAlwaysSpawn;
	bool m_bNeverSpawn;
	bool m_bNaval;

	int* m_piCommanderUnits;
	int* m_piGroupUnits;
	int* m_piGroupUnitClasses;
	int* m_piGroupPromotions;
	int* m_piCommanderPromotions;
	int* m_piSpawnTerrains;
	int* m_piSpawnFeatures;
	int* m_piPrereqTechANDs;
	int* m_piPrereqTechORs;
	int* m_piBlockTechANDs;
	int* m_piBlockTechORs;

	CvString m_szPyRequirement;
	CvString m_szPyOnSpawn;
	CvString m_szBanner;
};
/*************************************************************************************************/
/**	Spawn Groups							END													**/
/*************************************************************************************************/

/*************************************************************************************************/
/**	Better Affinity						01/30/11									Valkrionn	**/
/**																								**/
/**					Vastly improved Affinity system, open to many tags							**/
/*************************************************************************************************/
class CvAffinityInfo : public CvInfoBase
{
public:

	CvAffinityInfo();
	virtual ~CvAffinityInfo();

// Bools
	bool isNumCitiesEffect() const;										// Exposed to Python
	bool isCapitalPopEffect() const;										// Exposed to Python
	bool isPopulationEffect() const;										// Exposed to Python
	bool isVassalEffect() const;										// Exposed to Python

// Floats
	float getStrength() const;								// Exposed to Python
	float getStrengthMod() const;								// Exposed to Python
	float getAttackStrength() const;								// Exposed to Python
	float getAttackStrengthMod() const;								// Exposed to Python
	float getDefenseStrength() const;								// Exposed to Python
	float getDefenseStrengthMod() const;								// Exposed to Python
	float getCityDefenseMod() const;								// Exposed to Python
	float getMovement() const;								// Exposed to Python
	float getMovementDiscount() const;								// Exposed to Python
	float getVisibility() const;								// Exposed to Python
	float getPerception() const;								// Exposed to Python
	float getRangedStrength() const;								// Exposed to Python
	float getRangedStrengthMod() const;								// Exposed to Python
	float getRange() const;								// Exposed to Python
	float getRangedLimit() const;								// Exposed to Python
	float getFirstStrikes() const;								// Exposed to Python
	float getFirstStrikeChance() const;								// Exposed to Python
	float getAntiFirstStrikes() const;								// Exposed to Python
	float getDefensiveStrikes() const;								// Exposed to Python
	float getAntiDefensiveStrikes() const;								// Exposed to Python
	float getCapacity() const;								// Exposed to Python
	float getWillpower() const;								// Exposed to Python
	float getWithdrawal() const;								// Exposed to Python
	float getAntiWithdrawal() const;								// Exposed to Python
	float getHealRate() const;								// Exposed to Python
	float getXPFromCombat() const;								// Exposed to Python
	float getXPRate() const;								// Exposed to Python
	float getCommandRange() const;								// Exposed to Python
	float getCommandLimit() const;								// Exposed to Python
	float getWorkRate() const;								// Exposed to Python
	float getCollateral() const;								// Exposed to Python
	float getCollateralProtection() const;								// Exposed to Python
	float getCollateralLimit() const;								// Exposed to Python
	float getCollateralTargets() const;								// Exposed to Python
	float getVictoryInfluenceModifier() const;								// Exposed to Python
	float getDefeatInfluenceModifier() const;								// Exposed to Python
	float getPillageInfluenceModifier() const;								// Exposed to Python
	float getSlaveChance() const;								// Exposed to Python
	float getCombatHealPercent() const;								// Exposed to Python
	float getEnemyHealChange() const;								// Exposed to Python
	float getNeutralHealChange() const;								// Exposed to Python
	float getFriendlyHealChange() const;								// Exposed to Python

// Lists
	int getNumBonusTypes() const;							// Exposed to Python
	int getBonusTypes(int iI) const;							// Exposed to Python
	int getNumAffinityPromotions() const;							// Exposed to Python
	int getAffinityPromotions(int iI) const;							// Exposed to Python

// Arrays
	float getDamageTypeCombats(int iI) const;								// Exposed to Python
	float getDamageTypeResists(int iI) const;								// Exposed to Python
	float getTerrainDefenseMods(int iI) const;								// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
	void copyNonDefaults(CvAffinityInfo* pClassInfo, CvXMLLoadUtility* pXML);

protected:

// Bools
	bool m_bNumCitiesEffect;
	bool m_bCapitalPopEffect;
	bool m_bPopulationEffect;
	bool m_bVassalEffect;

// Floats
	float m_fStrength;
	float m_fStrengthMod;
	float m_fAttackStrength;
	float m_fAttackStrengthMod;
	float m_fDefenseStrength;
	float m_fDefenseStrengthMod;
	float m_fCityDefenseMod;
	float m_fMovement;
	float m_fMovementDiscount;
	float m_fVisibility;
	float m_fPerception;
	float m_fRangedStrength;
	float m_fRangedStrengthMod;
	float m_fRange;
	float m_fRangedLimit;
	float m_fFirstStrikes;
	float m_fFirstStrikeChance;
	float m_fAntiFirstStrikes;
	float m_fDefensiveStrikes;
	float m_fAntiDefensiveStrikes;
	float m_fCapacity;
	float m_fWillpower;
	float m_fWithdrawal;
	float m_fAntiWithdrawal;
	float m_fHealRate;
	float m_fXPFromCombat;
	float m_fXPRate;
	float m_fCommandRange;
	float m_fCommandLimit;
	float m_fWorkRate;
	float m_fCollateral;
	float m_fCollateralProtection;
	float m_fCollateralLimit;
	float m_fCollateralTargets;
	float m_fVictoryInfluenceModifier;
	float m_fDefeatInfluenceModifier;
	float m_fPillageInfluenceModifier;
	float m_fSlaveChance;
	float m_fCombatHealPercent;
	float m_fEnemyHealChange;
	float m_fNeutralHealChange;
	float m_fFriendlyHealChange;

// Lists
	int m_iNumBonusTypes;
	int* m_piBonusTypes;
	int m_iNumAffinityPromotions;
	int* m_piAffinityPromotions;

// Arrays
	float* m_pafDamageTypeCombats;
	float* m_pafDamageTypeResists;
	float* m_pafTerrainDefenseMods;
};
/*************************************************************************************************/
/**	Better Affinity							END													**/
/*************************************************************************************************/


#endif

// FlavourMod: Added by Jean Elcard (ClimateSystem)
class CvClimateZoneInfo :
	public CvInfoBase
{
public:

	CvClimateZoneInfo();
	virtual ~CvClimateZoneInfo();

	bool isOceanicClimate() const;

	int getMinTemperature() const;
	int getMaxTemperature() const;
	int getMinHumidity() const;
	int getMaxHumidity() const;

	int getTerrainClass() const;

	bool read(CvXMLLoadUtility* pXML);

protected:

	bool m_bOceanicClimate;

	int m_iMinTemperature;
	int m_iMaxTemperature;
	int m_iMinHumidity;
	int m_iMaxHumidity;

	int m_iTerrainClass;
};
// FlavourMod: End Add

// FlagSystem Start
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvFlagInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvFlagInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvFlagInfo();
	DllExport virtual ~CvFlagInfo();

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
};
// ModuleIdSystem Start
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvModuleIdInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvModuleIdInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvModuleIdInfo();
	DllExport virtual ~CvModuleIdInfo();

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
};


// PlotEffectSystem Start
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvPlotEffectInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvPlotEffectInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvPlotEffectInfo();
	DllExport virtual ~CvPlotEffectInfo();

	const TCHAR* getPythonOnMove() const;
	const TCHAR* getPyPerTurn() const;
	const int getDefaultFeatureGraphics() const;
	const int getTurnDamage()const;
	const int getDamageLimit()const;
	const int getDamageType()const;
	const bool isDispellable()const;
	const int getPrereqDispelPower()const;
	const int getHealthPercent()const;
	const int getMaxPlotCounter()const;
	const int getSpawnChance()const;
	const int getSpreadChance()const;
	const int getDisappearChance()const;
	const int getMoveChance()const;
	const int getPerceptionCost()const;
	const int getSeeThroughChange()const;
	const int* getYieldChangeArray()const;
	int getYieldChange(int i)const;
	bool isTerrain(int i) const;				// Exposed to Python

	bool read(CvXMLLoadUtility* pXML);
	void copyNonDefaults(CvPlotEffectInfo* pClassInfo, CvXMLLoadUtility* pXML);
	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
	CvString m_szPythonOnMove;
	CvString m_szPyPerTurn;
	int m_iDefaultFeatureGraphics;
	int m_iTurnDamage;
	int m_iDamageLimit;
	int m_iDamageType;
	int m_iHealthPercent;
	bool m_bDispellable;
	bool m_iPrereqDispelPower;
	int m_iMaxPlotCounter;
	int m_iSpawnChance;
	int m_iSpreadChance;
	int m_iDisappearChance;
	int m_iMoveChance;
	int m_iPerceptionCost;
	int m_iSeeThroughChange;
	int* m_piYieldChange;
	bool* m_pbTerrain;


};

//PromotionClass
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvPromotionClassInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvPromotionClassInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvPromotionClassInfo();
	DllExport virtual ~CvPromotionClassInfo();

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvCityClassInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvCityClassInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvCityClassInfo();
	DllExport virtual ~CvCityClassInfo();
	DllExport virtual void reset();

	DllExport int getArtStyleType() const;				// Expose to Python
	DllExport int getUnitArtStyleType() const;         // Expose to Python
	bool isLimitedSelection() const;
	DllExport int getCityClassBuildings(int i) const;				// Exposed to Python
	DllExport int getCityClassUnits(int i) const;				// Exposed to Python
	DllExport bool isCityClassFreeBuildingClass(int i) const;				// Exposed to Python
	int getDefaultRace() const;
	const TCHAR* getShortDescription() const;				// Exposed to Python
	void setShortDescription(const TCHAR* szVal);
	bool read(CvXMLLoadUtility* pXML);
	void copyNonDefaults(CvCityClassInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
	DllExport void read(FDataStreamBase* stream);
	DllExport void write(FDataStreamBase* stream);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:

	int m_iArtStyleType;
	int m_iUnitArtStyleType;  // FlavorUnits by Impaler[WrG]
	int* m_piCityClassBuildings;
	int* m_piCityClassUnits;
	bool* m_pbCityClassFreeBuildingClass;
	int m_iDefaultRace;
	bool m_bLimitedSelection;
	CvString m_szShortDescription;

};

//TraitClass
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTraitClassInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTraitClassInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvTraitClassInfo();
	DllExport virtual ~CvTraitClassInfo();

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
};
//LeaderClass
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvLeaderClassInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvLeaderClassInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvLeaderClassInfo();
	DllExport virtual ~CvLeaderClassInfo();

	bool read(CvXMLLoadUtility* pXML);
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	void copyNonDefaults(CvLeaderClassInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);

	int getLeaderStatus() const;
	int getMaxTraitsPerClass(int i) const;
	bool isTraitClassEvolve(int i) const;

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
	/*************************************************************************************************/
/**	LeaderStatus Infos      				10/02/09								Valkrionn	**/
/*************************************************************************************************/
	int m_iLeaderStatus;
	int* m_piMaxTraitsPerClass;
	bool* m_pbTraitClassEvolve;

	/*************************************************************************************************/
	/**	New Tag Defs							END													**/
	/*************************************************************************************************/

};
//TraitTrigger
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvTraitTriggerInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvTraitTriggerInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvTraitTriggerInfo();
	DllExport virtual ~CvTraitTriggerInfo();

	bool read(CvXMLLoadUtility* pXML);
	void read(FDataStreamBase* stream);
	void write(FDataStreamBase* stream);
	void copyNonDefaults(CvTraitTriggerInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);

	int getTraitHookType() const;
	int getTraitClassType() const;
	int getPrereqReligionType() const;
	int getPrereqOldReligionType() const;
	int getPrereqCultureLevel() const;
	int getPrereqRace() const;
	int getPrereqKilledRace() const;
	int getPrereqTrade() const;
	int getPrereqImprovementType() const;
	int getPrereqRouteType() const;
	int getPrereqProjectType() const;
	int getPrereqTerrainType() const;
	int getPrereqFeatureType() const;
	int getPrereqBonusType() const;
	int getPrereqTechType() const;
	int getPrereqHurryType() const;
	int getPrereqUnitClassType() const;
	int getPrereqKilledUnitClassType() const;
	int getPrereqPromotionType() const;
	int getPrereqSpellType() const;
	int getPrereqBuildingClassType() const;
	int getPrereqUnitCombatType() const;
	int getPrereqKilledUnitCombatType() const;
	int getPrereqAlignment() const;
	int getPrereqKilledAlignment() const;
	int getPrereqEthicalAlignment() const;
	int getPrereqKilledEthicalAlignment() const;
	int getPrereqMinAlignment() const;
	int getPrereqMaxAlignment() const;
	int getPrereqThroughAlignment() const;
	int getPrereqThroughEthicalAlignment() const;
	int getPrereqMinKilledAlignment() const;
	int getPrereqMaxKilledAlignment() const;
	int getPrereqMinEthicalAlignment() const;
	int getPrereqMaxEthicalAlignment() const;
	int getPrereqMinKilledEthicalAlignment() const;
	int getPrereqMaxKilledEthicalAlignment() const;
	bool isFirst() const;
	bool isOncePerPlayer() const;
	bool isGameSpeedScale() const;
	bool isCoastal() const;
	bool isPrereqConquest() const;
	bool isPrereqTrade() const;
	bool isCityOwnHolyCity() const;
	bool isCityNotOwnHolyCity() const;
	bool isCityAnyHolyCity() const;
	bool isPrereqWerewolf() const;
	bool isPrereqUndead() const;
	bool isPrereqHero() const;
	bool isPrereqHiddenNationality() const;
	bool isPrereqInBorders() const;
	bool isPrereqOutsideBorders() const;
	bool isPrereqKilledWerewolf() const;
	bool isPrereqKilledUndead() const;
	bool isPrereqKilledHero() const;
	bool isPrereqKilledHiddenNationality() const;
	bool isPrereqKilledInBorders() const;
	bool isPrereqKilledOutsideBorders() const;

	int getBonusMultiplierType() const;
	bool isPrereqAtWar() const;
	bool isPrereqAtPeace() const;
	bool isPrereqOpposite() const;
	bool isPrereqOppositeEthical() const;
	bool isPrereqHill() const;
	bool isPrereqPeak() const;
	bool isPrereqHappy() const;
	bool isPrereqHealth() const;
	bool isOwnHolyCity() const;
	int getTraitCounterChange(int i) const;
	bool isTraitClassEvolve(int i) const;
	int getNumPrereqCivics() const;
	int getPrereqCivic(int iI) const;

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
	/*************************************************************************************************/
/**	LeaderStatus Infos      				10/02/09								Valkrionn	**/
/*************************************************************************************************/
	int m_iTraitHookType;
	int m_iTraitClassType;
	int m_iPrereqReligionType;
	int m_iPrereqOldReligionType;
	int m_iPrereqCultureLevel;
	int m_iPrereqRace;
	int m_iPrereqKilledRace;
	int m_iPrereqTrade;
	int m_iPrereqImprovementType;
	int m_iPrereqRouteType;
	int m_iPrereqProjectType;
	int m_iPrereqTerrainType;
	int m_iPrereqFeatureType;
	int m_iPrereqBonusType;
	int m_iPrereqTechType;
	int m_iPrereqHurryType;
	int m_iPrereqUnitClassType;
	int m_iPrereqKilledUnitClassType;
	int m_iPrereqPromotionType;
	int m_iPrereqSpellType;
	int m_iPrereqBuildingClassType;
	int m_iPrereqUnitCombatType;
	int m_iPrereqKilledUnitCombatType;
	int m_iPrereqAlignment;
	int m_iPrereqKilledAlignment;
	int m_iPrereqEthicalAlignment;
	int m_iPrereqKilledEthicalAlignment;
	int m_iPrereqMinAlignment;
	int m_iPrereqMaxAlignment;
	int m_iPrereqThroughAlignment;
	int m_iPrereqThroughEthicalAlignment;
	int m_iPrereqMinKilledAlignment;
	int m_iPrereqMaxKilledAlignment;
	int m_iPrereqMinEthicalAlignment;
	int m_iPrereqMaxEthicalAlignment;
	int m_iPrereqMinKilledEthicalAlignment;
	int m_iPrereqMaxKilledEthicalAlignment;

	bool m_bFirst;
	bool m_bOncePerPlayer;
	bool m_bGameSpeedScale;
	bool m_bCoastal;
	bool m_bConquest;
	bool m_bTrade;
	bool m_bOwnHolyCity;
	bool m_bNotOwnHolyCity;
	bool m_bAnyHolyCity;
	bool m_bWerewolf;
	bool m_bUndead;
	bool m_bHero;
	bool m_bHiddenNationality;
	bool m_bInBorders;
	bool m_bOutsideBorders;
	bool m_bKilledWerewolf;
	bool m_bKilledUndead;
	bool m_bKilledHero;
	bool m_bKilledHiddenNationality;
	bool m_bKilledInBorders;
	bool m_bKilledOutsideBorders;
	int m_iBonusMultiplierType;
	bool m_bPrereqAtWar;
	bool m_bPrereqAtPeace;
	bool m_bPrereqOpposite;
	bool m_bPrereqOppositeEthical;
	bool m_bPrereqHill;
	bool m_bPrereqPeak;
	bool m_bPrereqHappy;
	bool m_bPrereqHealth;
	bool m_bHolyCity;
	int* m_piTraitCounterChange;
	bool* m_pbTraitClassEvolve;
	int m_iNumPrereqCivics;
	int* m_piPrereqCivics;

	/*************************************************************************************************/
	/**	New Tag Defs							END													**/
	/*************************************************************************************************/

};

// Magic Rework
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvSpellClassInfo
//
//  DESC:   
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvSpellClassInfo : public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	DllExport CvSpellClassInfo();
	DllExport virtual ~CvSpellClassInfo();

	bool read(CvXMLLoadUtility* pXML);

	//---------------------------------------PROTECTED MEMBER VARIABLES---------------------------------

protected:
};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//  class : CvImprovementClassInfo
//
//  DESC:
//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CvImprovementClassInfo :
	public CvInfoBase
{
	//---------------------------------------PUBLIC INTERFACE---------------------------------
public:

	CvImprovementClassInfo();
	virtual ~CvImprovementClassInfo();

	int getDefaultImprovementIndex() const;				// Exposed to Python
	void setDefaultImprovementIndex(int i);


	bool isUnique() const;

	bool read(CvXMLLoadUtility* pXML);
	bool readPass3();
	void copyNonDefaults(CvImprovementClassInfo* pClassInfo = NULL, CvXMLLoadUtility* pXML = NULL);
protected:

	int m_iDefaultImprovementIndex;

	bool m_bUnique;

};

