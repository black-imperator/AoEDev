#pragma once

#ifndef CVDEFINES_H
#define CVDEFINES_H

// defines.h

// The following #defines should not be moddable...

#define MOVE_IGNORE_DANGER										(0x00000001)
#define MOVE_SAFE_TERRITORY										(0x00000002)
#define MOVE_NO_ENEMY_TERRITORY								(0x00000004)
#define MOVE_DECLARE_WAR											(0x00000008)
#define MOVE_DIRECT_ATTACK										(0x00000010)
#define MOVE_THROUGH_ENEMY										(0x00000020)
#define MOVE_MAX_MOVES											(0x00000040)
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      01/01/09                                jdog5000      */
/*                                                                                              */
/* General AI                                                                                   */
/************************************************************************************************/
// These two flags signal to weight the cost of moving through or adjacent to enemy territory higher
// Used to reduce exposure to attack for approaching enemy cities
#define MOVE_AVOID_ENEMY_WEIGHT_2								(0x00000080)
#define MOVE_AVOID_ENEMY_WEIGHT_3								(0x00000100)
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
/*************************************************************************************************/
/**	AITweak							14/07/10								Snarko				**/
/**																								**/
/**			Teaching AI to sometimes ignore if the other unit has attacked this turn			**/
/*************************************************************************************************/
#define MOVE_IGNORE_HAS_ATTACKED											(0x00000200)
/*************************************************************************************************/
/**	AITweak									END													**/
/*************************************************************************************************/

#define RANDPLOT_LAND													(0x00000001)
#define RANDPLOT_UNOWNED											(0x00000002)
#define RANDPLOT_ADJACENT_UNOWNED							(0x00000004)
#define RANDPLOT_ADJACENT_LAND								(0x00000008)
#define RANDPLOT_PASSIBLE											(0x00000010)
#define RANDPLOT_NOT_VISIBLE_TO_CIV						(0x00000020)
#define RANDPLOT_NOT_CITY											(0x00000040)
#define RANDPLOT_PEAK											(0x00000080)
#define RANDPLOT_NOT_PEAK										(0x00000100)
#define RANDPLOT_EVIL												(0x00000200)
#define RANDPLOT_ORC_ALLY											(0x00000400)
#define RANDPLOT_ANIMAL_ALLY										(0x00000800)
#define RANDPLOT_DEMON_ALLY											(0x00001000)
#define RANDPLOT_NOT_IMPROVED										(0x00002000)
#define RANDPLOT_WATER												(0x00004000)
#define RANDPLOT_UNOCCUPIED											(0x00008000)
/*************************************************************************************************/
/**	LakeBarbFix								2026									 Issue #161 **/
/**																								**/
/**		Excludes lakes and dead-end water pockets from random plot selection					**/
/*************************************************************************************************/
#define RANDPLOT_NOT_ENCLOSED_WATER									(0x00010000)
/*************************************************************************************************/
/**	LakeBarbFix								END													**/
/*************************************************************************************************/


/*************************************************************************************************/
/**	MultiBarb							12/23/08									Xienwolf	**/
/**																								**/
/**							Adds extra Barbarian Civilizations									**/
/*************************************************************************************************/
/**								---- Start Original Code ----									**
#ifdef _USRDLL

//FfH: Modified by Kael 09/27/2007
//#define MAX_CIV_PLAYERS												(18)
#define MAX_CIV_PLAYERS												(35)
//FfH: End Modify

#else
#define MAX_CIV_PLAYERS												(CvGlobals::getInstance().getMaxCivPlayers())
#endif

#define MAX_CIV_TEAMS													(MAX_CIV_PLAYERS)
#define MAX_PLAYERS														(MAX_CIV_PLAYERS + 1)
#define MAX_TEAMS															(MAX_PLAYERS)
#define BARBARIAN_PLAYER											((PlayerTypes)MAX_CIV_PLAYERS)
#define BARBARIAN_TEAM												((TeamTypes)MAX_CIV_TEAMS)
/**								----  End Original Code  ----									**/
#ifdef _USRDLL
#define MAX_CIV_PLAYERS											(50)
#else
#define MAX_CIV_PLAYERS											(CvGlobals::getInstance().getMaxCivPlayers())
#endif

#define MAX_CIV_TEAMS											(MAX_CIV_PLAYERS)
#define MAX_PLAYERS												(MAX_CIV_PLAYERS + 3)
#define MAX_TEAMS												(MAX_PLAYERS)
#define BARBARIAN_PLAYER										((PlayerTypes)(MAX_CIV_PLAYERS))
#define BARBARIAN_TEAM											((TeamTypes)(MAX_CIV_TEAMS))
#define ORC_PLAYER												((PlayerTypes)(MAX_CIV_PLAYERS))
#define ORC_TEAM												((TeamTypes)(MAX_CIV_TEAMS))
#define ANIMAL_PLAYER											((PlayerTypes)(MAX_CIV_PLAYERS + 1))
#define ANIMAL_TEAM												((TeamTypes)(MAX_CIV_TEAMS + 1))
#define DEMON_PLAYER											((PlayerTypes)(MAX_CIV_PLAYERS + 2))
#define DEMON_TEAM												((TeamTypes)(MAX_CIV_TEAMS + 2))
#define OWNERSHIP_INFO_WIP										1
#define DEBUG_TGA_INDEX											1
/*************************************************************************************************/
/**	MultiBarb								END													**/
/*************************************************************************************************/

// Char Count limit for edit boxes
#define PREFERRED_EDIT_CHAR_COUNT							(15)
#define MAX_GAMENAME_CHAR_COUNT								(32)
#define MAX_PLAYERINFO_CHAR_COUNT							(32)
#define MAX_PLAYEREMAIL_CHAR_COUNT						(64)
#define MAX_PASSWORD_CHAR_COUNT								(32)
#define MAX_GSLOGIN_CHAR_COUNT								(17)
#define MAX_GSEMAIL_CHAR_COUNT								(50)
#define MAX_GSPASSWORD_CHAR_COUNT							(30)
#define MAX_CHAT_CHAR_COUNT										(256)
#define MAX_ADDRESS_CHAR_COUNT								(64)

#define INVALID_PLOT_COORD										(-(MAX_INT))	// don't use -1 since that is a valid wrap coordinate
#define DIRECTION_RADIUS											(1)
#define DIRECTION_DIAMETER										((DIRECTION_RADIUS * 2) + 1)

//FfH: Modified by Kael 11/18/2007
//#define NUM_CITY_PLOTS												(21)
//#define CITY_HOME_PLOT												(0)
//#define CITY_PLOTS_RADIUS											(2)
#define NUM_CITY_PLOTS												(37)
#define CITY_HOME_PLOT												(0)
#define CITY_PLOTS_RADIUS											(3)
//FfH: End Modify

#define CITY_PLOTS_DIAMETER										((CITY_PLOTS_RADIUS*2) + 1)

#define GAME_NAME															("Game")

#define LANDSCAPE_FOW_RESOLUTION							(4)

#define Z_ORDER_LAYER													(-0.1f)
#define Z_ORDER_LEVEL													(-0.3f)

#define CIV4_GUID															"civ4bts"
#define CIV4_PRODUCT_ID												11081
#define CIV4_NAMESPACE_ID											17
#define CIV4_NAMESPACE_EXT										"-tk"

#define MAP_TRANSFER_EXT											"_t"

#define USER_CHANNEL_PREFIX										"#civ4buser!"

#define SETCOLR																L"<color=%d,%d,%d,%d>"
#define ENDCOLR																L"</color>"
#define NEWLINE																L"\n"
#define SEPARATOR															L"\n-----------------------"
#define TEXT_COLOR(szColor)										((int)(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString(szColor)).getColor().r * 255)), ((int)(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString(szColor)).getColor().g * 255)), ((int)(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString(szColor)).getColor().b * 255)), ((int)(GC.getColorInfo((ColorTypes)GC.getInfoTypeForString(szColor)).getColor().a * 255))

// Version Verification files and folders
#ifdef _DEBUG
#define CIV4_EXE_FILE													".\\Civ4BeyondSword_DEBUG.exe"
#define CIV4_DLL_FILE													".\\Assets\\CvGameCoreDLL_DEBUG.dll"
#else
#define CIV4_EXE_FILE													".\\Civ4BeyondSword.exe"
#define CIV4_DLL_FILE													".\\Assets\\CvGameCoreDLL.dll"
#endif
#define CIV4_SHADERS													".\\Shaders\\FXO"
#define CIV4_ASSETS_PYTHON										".\\Assets\\Python"
#define CIV4_ASSETS_XML												".\\Assets\\XML"

#define MAX_PLAYER_NAME_LEN										(64)
#define MAX_VOTE_CHOICES											(8)
#define VOTE_TIMEOUT													(600000)	// 10 minute vote timeout - temporary

#define ANIMATION_DEFAULT											(1)			// Default idle animation

// python module names
#define PYDebugToolModule			"CvDebugInterface"					//Not Used
#define PYScreensModule				"CvScreensInterface"
#define PYCivModule						"CvAppInterface"				//Not Used
#define PYWorldBuilderModule	"CvWBInterface"							//Not Used
#define PYPopupModule					"CvPopupInterface"				//Not Used
#define PYDiplomacyModule			"CvDiplomacyInterface"				//Not Used
#define PYUnitControlModule		"CvUnitControlInterface"				//Not Used
#define PYTextMgrModule				"CvTextMgrInterface"				//Not Used
#define PYPerfTestModule			"CvPerfTest"						//Not Used
#define PYDebugScriptsModule	"DebugScripts"							//Not Used
#define PYPitBossModule				"PbMain"
#define PYTranslatorModule		"CvTranslator"							//Not Used
#define PYGameModule					"CvGameInterface"
#define PYEventModule					"CvEventInterface"
#define PYRandomEventModule					"CvRandomEventInterface"

//FfH: Added by Kael 07/23/2007 (PYSomniumModule and PyDataStorageModule are for Somnium)
#define PYSpellModule					"CvSpellInterface"
#define PYSomniumModule					"CvSomniumInterface"
#define PYDataStorageModule					"CvDataStorageInterface"
//FfH: End Add

/*************************************************************************************************/
/**	Flavour Mod								06/23/08								Jean Elcard **/
/**																								**/
/**								Adds a Python File Reference									**/
/*************************************************************************************************/
#define PYFlavourModule					"CvFlavourInterface"
/*************************************************************************************************/
/**	Flavour Mod								END													**/
/*************************************************************************************************/
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      08/21/09                                jdog5000      */
/*                                                                                              */
/* Efficiency                                                                                   */
/************************************************************************************************/
// Plot danger cache
#define DANGER_RANGE						(4)
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
#endif	// CVDEFINES_H
