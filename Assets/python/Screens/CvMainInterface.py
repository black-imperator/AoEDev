## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvEventInterface
import time
# < Mercenaries Start >
import CvMercenaryManager

import CvGameInterface

gameUtils = CvGameInterface.gameUtils()
# < Mercenaries End   >

# DynTraits Start
import CvTraitScreen
# DynTraits End

import CustomFunctions
cf = CustomFunctions.CustomFunctions()
import ScenarioFunctions
sf = ScenarioFunctions.ScenarioFunctions()

# MPL ArcticNightWolf - 27-Nov-2010
import os
import imp
import CvPath
## MPL end
import math

#---unitstats addition 1/4-----------------------
import CvStatisticsScreen
import UnitStatisticsTools
gg = UnitStatisticsTools.UnitStatisticsTools()
g_UnitStatistics = "placeHolder"
#/---unitstats addition 1/4-----------------------

# FF: StateNames
import CvConfigParser
config = CvConfigParser.CvConfigParser("Ashes of Erebus Options.ini")
g_bScoreShowStateName = config.getboolean("Score Board", "UseStateName", False)
# FF: End

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()


# High Res stuff - Added by Grey Fox 03/29/2010
g_iMediumRez	= 1280
g_iHighRez 		= 1600
g_iVeryHighRez 	= 1600
g_iVeryHighY 	= 134
# High Res stuff - End Add

manaTypes1 = [ 'BONUS_MANA_AIR','BONUS_MANA_BODY','BONUS_MANA_CHAOS','BONUS_MANA_DEATH','BONUS_MANA_EARTH','BONUS_MANA_ENCHANTMENT','BONUS_MANA_ENTROPY','BONUS_MANA_FIRE','BONUS_MANA_LAW','BONUS_MANA_CREATION','BONUS_MANA_FORCE' ]
manaTypes2 = [ 'BONUS_MANA_LIFE','BONUS_MANA_METAMAGIC','BONUS_MANA_MIND','BONUS_MANA_NATURE','BONUS_MANA_SHADOW','BONUS_MANA_SPIRIT','BONUS_MANA_SUN','BONUS_MANA_WATER','BONUS_MANA_ICE','BONUS_MANA_DIMENSIONAL','BONUS_REFINED_MANA' ]

luxuryTypes1 = [ 'BONUS_ALE','BONUS_BLEEDING_GOD_WINE','BONUS_COTTON','BONUS_DYE','BONUS_MANA_ENCHANTMENT','BONUS_FINE_CLOTHES','BONUS_FRUIT_OF_YGGDRASIL','BONUS_FUR','BONUS_GEMS','BONUS_GOLD','BONUS_GULAGARM' ]
luxuryTypes2 = [ 'BONUS_HARE','BONUS_IVORY','BONUS_JETEYE','BONUS_JEWELS','BONUS_MARBLE','BONUS_OBSIDIAN','BONUS_PATRIAN_ARTIFACTS','BONUS_PEARL','BONUS_SILK','BONUS_SUGAR','BONUS_WINE' ]

healthTypes1 = [ 'BONUS_BANANA','BONUS_BISON','BONUS_CAMEL','BONUS_CLAM','BONUS_CORN','BONUS_COW','BONUS_CRAB','BONUS_DEER','BONUS_DEER_ARCTIC','BONUS_FISH' ]
healthTypes2 = [ 'BONUS_FRUIT_OF_YGGDRASIL','BONUS_MANA_LIFE','BONUS_MUSHROOMS','BONUS_PIG','BONUS_RICE','BONUS_SALT','BONUS_SHEEP','BONUS_SHRIMP','BONUS_TOAD','BONUS_WHALE','BONUS_WHEAT' ]

strategicTypes1 = [ 'BONUS_ASH','BONUS_CAMEL','BONUS_COPPER','BONUS_DESERT_ROSE','BONUS_GUNPOWDER','BONUS_HORSE','BONUS_HYAPON','BONUS_INCENSE','BONUS_IRON' ]
strategicTypes2 = [ 'BONUS_MITHRIL','BONUS_NIGHTMARE','BONUS_RAZORWEED','BONUS_REAGENTS','BONUS_SHEUT_STONE','BONUS_STONE' ]

RelInterfaces = [ 'Ashen','Overlords','Esus','Fellowship','Runes','Empyrean','Order' ]
CurrentHUD = ''
#Added for HUD Modification by seZereth
#####################################   CITY SECTION ##############################################
#Top Bar, stretching from Treasury to Clock
HUD_City_Top_Panel_Height = 41

#Behind Mini-Map & Advisor Buttons
HUD_City_Bottom_Right_Width = 243
HUD_City_Bottom_Right_Height = 186

#Behind Build Order Queue
HUD_City_Bottom_Left_Width = 243
HUD_City_Bottom_Left_Height = 186

#Behind Build Options, Width is automatically defined to stretch between the above 2 Panels
HUD_City_Bottom_Center_Height = 149

#Width for Background of 3 Sections, City Status (Science/Culture/Gold Sliders, Maintenance Costs - Fixed Height), Trade Routes Panel (fixed Height) and Buildings Panel (Stretches to connect Trade Routes Panel to the Bottom Left Panel)  --  Background will extend slightly into the Minimap Panel (City Bottom Right)
HUD_City_Left_Panel_Width = 258

#Label for Buildings Section
HUD_City_Buildings_Label_Height = 30
HUD_City_Buildings_Label_Width = 238

#Label for Trade Routes Section
HUD_City_TradeRoute_Label_Height = 30
HUD_City_TradeRoute_Label_Width = 238

#Panel for City Status Section
HUD_City_Status_Panel_Height = 120#105
HUD_City_Status_Panel_Width = 238

#Width for Background of 3 Sections, Religions/Corporations Panel (Fixed Height), Resources Panel (Stretches to Connect Religions/Corporations Panel to Specialists Panel) and Specialists Panel (Fixed Height)  --  Background will extend slightly into the Minimap Panel (City Bottom Right)
HUD_City_Right_Panel_Width = 258

#Behind the Food/Production Progress Bars.    Defined as a Width Exclusion since it is a centered item, so this number is how far it is from each edge of the screen.
HUD_City_Growth_Panel_Width_Exclusion = 260
HUD_City_Growth_Panel_Height = 60

#Background for above 2 sections is automatically defined: Stretches to connect City Left Panel and City Right Panel and Stretches from the Top bar to the Bottom Center bar  -- City_Top_Center_Background_Panel.tga

#Extra Panel to place anywhere you desire
HUD_City_Extra_1_Location_X = 10
HUD_City_Extra_1_Location_Y = 10
HUD_City_Extra_1_Height = 10
HUD_City_Extra_1_Width = 10

#Behind the City Name, Arrows to Cycle through Multiple Cities, and Defense Percentage.    Defined as a Width Exclusion since it is a centered item, so this number is how far it is from each edge of the screen.
HUD_City_Name_Panel_Width_Exclusion = 260
HUD_City_Name_Panel_Height = 38

#####################################   MAIN SECTION ##############################################
ishowManaBar = 1
isformershowManaBar = 1
#Behind Mini-Map
HUD_Main_Bottom_Right_Width = 243
HUD_Main_Bottom_Right_Height = 186

#Main Panel Behind Unit Stats
HUD_Main_Bottom_Left_Width = 291
HUD_Main_Bottom_Left_Height = 210

#Behind Action Buttons (Stretches to connect Bottom Right to Bottom Left)
HUD_Main_Bottom_Center_Height = 149

#Behind Treasury and Log Button
HUD_Main_Top_Left_Width = 286
HUD_Main_Top_Left_Height = 60

#Behind  GameClock and Advisor Buttons
HUD_Main_Top_Right_Width = 286
HUD_Main_Top_Right_Height = 60

#Behind Tech Progress Bar (Stretches to Connect Top Right and Top Left)
HUD_Main_Top_Center_Height = 60

#Extra Panel to place anywhere you desire
HUD_Main_Extra_1_Location_X = 10
HUD_Main_Extra_1_Location_Y = 10
HUD_Main_Extra_1_Height = 10
HUD_Main_Extra_1_Width = 10

# Great Person Bar
import GPUtil
GP_BAR_WIDTH = 320
###
g_iSlaveRowLength = 1
g_iSlaveColumnHeight = 6
g_NumEmphasizeInfos = 0
g_NumCityTabTypes = 0
g_NumHurryInfos = 0
g_NumUnitClassInfos = 0
g_NumBuildingClassInfos = 0
g_NumProjectInfos = 0
g_NumProcessInfos = 0
g_NumActionInfos = 0
g_eEndTurnButtonState = -1

MAX_SELECTED_TEXT = 5
MAX_DISPLAYABLE_BUILDINGS = 15
MAX_DISPLAYABLE_TRADE_ROUTES = 4
MAX_BONUS_ROWS = 10
MAX_CITIZEN_BUTTONS = 8

SELECTION_BUTTON_COLUMNS = 8
SELECTION_BUTTON_ROWS = 2
NUM_SELECTION_BUTTONS = SELECTION_BUTTON_ROWS * SELECTION_BUTTON_COLUMNS

g_iNumBuildingWidgets = MAX_DISPLAYABLE_BUILDINGS
g_iNumTradeRouteWidgets = MAX_DISPLAYABLE_TRADE_ROUTES

# END OF TURN BUTTON POSITIONS
######################
iEndOfTurnButtonSize = 64

#FfH: Modified by Kael 07/18/2008
#iEndOfTurnPosX = 296 # distance from right
iEndOfTurnPosX = 238 # distance from right
#FfH: End Modify

iEndOfTurnPosY = 147 # distance from bottom

# MINIMAP BUTTON POSITIONS
######################
iMinimapButtonsExtent = 228
iMinimapButtonsX = 227
iMinimapButtonsY_Regular = 160
iMinimapButtonsY_Minimal = 32
iMinimapButtonWidth = 24
iMinimapButtonHeight = 24

# Globe button
iGlobeButtonX = 48
iGlobeButtonY_Regular = 168
iGlobeButtonY_Minimal = 40
iGlobeToggleWidth = 48
iGlobeToggleHeight = 48

# GLOBE LAYER OPTION POSITIONING
######################
iGlobeLayerOptionsX  = 235
iGlobeLayerOptionsY_Regular  = 170# distance from bottom edge
iGlobeLayerOptionsY_Minimal  = 38 # distance from bottom edge
iGlobeLayerOptionsWidth = 400
iGlobeLayerOptionHeight = 24

# STACK BAR (Research bar, Great Person bar...)
#####################
# iStackBarCoordX = 287 + (xResolution - 1024) / 2 # this has to be defined later since we don't know xResolution here
iStackBarCoordY = 2
iStackBarDeltaY = 25
iStackBarHeight = 27
iStackBarWidth = 450

iXPBarCoordX = 5
iXPBarCoordY = 90
iXPLblCoordX = iXPBarCoordX + iStackBarWidth/2
iXPLblCoordY = iXPBarCoordY + 5

# MULTI LIST
#####################
iMultiListXL = 298
iMultiListXR = 236

# TOP CENTER TITLE
#####################
iCityCenterRow1X = 398
iCityCenterRow1Y = 78
iCityCenterRow2X = 398
iCityCenterRow2Y = 104

iCityCenterRow1Xa = 347
iCityCenterRow2Xa = 482


g_iNumTradeRoutes = 0
g_iNumBuildings = 0
g_iNumLeftBonus = 0
g_iNumCenterBonus = 0
g_iNumRightBonus = 0

g_szTimeText = ""
g_iTimeTextCounter = 0

g_pSelectedUnit = 0
#Toggle Manabar Start
ishowManaBar = 1
isformershowManaBar = 1
#Toggle Manabar End

#FfH: Added by Kael 07/17/2008
iHelpX = 140
#FfH: End Add
# < Mercenaries Start >

mercenaryManager = CvMercenaryManager.CvMercenaryManager(CvScreenEnums.MERCENARY_MANAGER)
# < Mercenaries End >

iBuildingsList = 0

iPromotionsPerPage = 30
iPromotionPage = 1
iNumUnitPromotions = 0

iScoreState = 0

class CvMainInterface:
	"Main Interface Screen"
# < Mercenaries Start >
	repainting = false
	# < Mercenaries End   >

	def numPlotListButtons(self):
		return self.m_iNumPlotListButtons # could be the source of a bug (at gamestart)

	def interfaceScreen (self):

		# Global variables being set here
		global g_NumEmphasizeInfos
		global g_NumCityTabTypes
		global g_NumHurryInfos
		global g_NumUnitClassInfos
		global g_NumBuildingClassInfos
		global g_NumProjectInfos
		global g_NumProcessInfos
		global g_NumActionInfos

		global MAX_SELECTED_TEXT
		global MAX_DISPLAYABLE_BUILDINGS
		global MAX_DISPLAYABLE_TRADE_ROUTES
		global MAX_BONUS_ROWS
		global MAX_CITIZEN_BUTTONS
		# < Mercenaries Start >
		self.repainting=false
		# < Mercenaries End   >
		global HUD_City_Bottom_Right_Width
		global HUD_City_Bottom_Right_Height
		global HUD_City_Bottom_Left_Width
		global HUD_City_Bottom_Left_Height
		global HUD_City_Bottom_Center_Height
		global HUD_City_Left_Panel_Width
		global HUD_City_Buildings_Label_Height
		global HUD_City_Buildings_Label_Width
		global HUD_City_TradeRoute_Label_Height
		global HUD_City_TradeRoute_Label_Width
		global HUD_City_Status_Panel_Height
		global HUD_City_Status_Panel_Width
		global HUD_City_Right_Panel_Width
		global HUD_City_Growth_Panel_Width_Exclusion
		global HUD_City_Growth_Panel_Height
		global HUD_City_Name_Panel_Width_Exclusion
		global HUD_City_Name_Panel_Height
		global HUD_City_Top_Center_Background_Panel_Height
		global HUD_City_Top_Panel_Height
		global HUD_City_Extra_1_Location_X
		global HUD_City_Extra_1_Location_Y
		global HUD_City_Extra_1_Height
		global HUD_City_Extra_1_Width
		global HUD_Main_Bottom_Right_Width
		global HUD_Main_Bottom_Right_Height
		global HUD_Main_Bottom_Left_Width
		global HUD_Main_Bottom_Left_Height
		global HUD_Main_Bottom_Center_Height
		global HUD_Main_Top_Left_Width
		global HUD_Main_Top_Left_Height
		global HUD_Main_Top_Right_Width
		global HUD_Main_Top_Right_Height
		global HUD_Main_Top_Center_Height
		global HUD_Main_Extra_1_Location_X
		global HUD_Main_Extra_1_Location_Y
		global HUD_Main_Extra_1_Height
		global HUD_Main_Extra_1_Width
		global g_iSlaveColumnHeight
		global g_iSlaveRowLength

		if ( CyGame().isPitbossHost() ):
			return

		pPlayer = gc.getPlayer( gc.getGame().getActivePlayer() )
		pCivilization = pPlayer.getCivilizationType()

		# This is the main interface screen, create it as such
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.setForcedRedraw(True)

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34

		screen.setDimensions(0, 0, xResolution, yResolution)

#---unitstats addition 2/4-----------------------



		InfoPaneX = 123
		InfoPaneY = yResolution - 200
		InfoPaneWidth = 270
		InfoPaneHeight = 30

		screen.addPanel( "UNIT_INFO_PANE", u"", u"", True, True, InfoPaneX, InfoPaneY, InfoPaneWidth, InfoPaneHeight, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "UNIT_INFO_PANE" )
		szText = "<font=2>" + localText.getText("TXT_KEY_UNIT_STATISTICS_SMALL", ()) + "</font=2>"
		szTextBlack = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_BLACK"))
		screen.addMultilineText( "UNIT_INFO_TEXT", szText, InfoPaneX +2, InfoPaneY +5, InfoPaneWidth -3, InfoPaneHeight- 3, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.hide( "UNIT_INFO_TEXT" )

		screen.setImageButton("RawManaButton1", "Art/Interface/Screens/RawManaButton.dds", 80, 118, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "RawManaButton1" )
		for szBonus in strategicTypes1:
			szName = "StrategicText" + szBonus
			screen.hide( szName )
		for szBonus in strategicTypes2:
			szName = "StrategicText" + szBonus
			screen.hide( szName )
		for szBonus in manaTypes1:
			szName = "ManaText" + szBonus
			screen.hide( szName )
		for szBonus in manaTypes2:
			szName = "ManaText" + szBonus
			screen.hide( szName )
		for szBonus in luxuryTypes1:
			szName = "LuxuryText" + szBonus
			screen.hide( szName )
		for szBonus in luxuryTypes2:
			szName = "LuxuryText" + szBonus
			screen.hide( szName )
		for szBonus in healthTypes1:
			szName = "HealthText" + szBonus
			screen.hide( szName )
		for szBonus in healthTypes2:
			szName = "HealthText" + szBonus
			screen.hide( szName )
		screen.addPanel( "ManaToggleHelpTextPanel", u"", u"", True, True, 100, 118, 170, 30, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "ManaToggleHelpTextPanel" )
		szText = "<font=2>" + localText.getText("TXT_KEY_MANA_TOGGLE_HELP", ()) + "</font=2>"
		screen.addMultilineText( "ManaToggleHelpText", szText, 102, 123, 167, 27, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.hide( "ManaToggleHelpText" )

		screen.setImageButton("xUPTButton", "Art/Interface/Screens/xUPT.dds", xResolution - 58, 52, iEndOfTurnButtonSize, iEndOfTurnButtonSize, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "xUPTButton" )

		screen.addPanel( "SpawnOddsHelpTextPanel", u"", u"", True, True, 100, 88, 170, 30, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "SpawnOddsHelpTextPanel" )
		szText = "<font=2>" + localText.getText("[COLOR_HIGHLIGHT_TEXT]Awakened Spawn Chance[COLOR_REVERT]", ()) + "</font=2>"
		screen.addMultilineText( "SpawnOddsHelpText", szText, 102, 93, 167, 27, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.hide( "SpawnOddsHelpText" )
#/---unitstats addition 2/4-----------------------
		# Set up our global variables...
		g_NumEmphasizeInfos = gc.getNumEmphasizeInfos()
		g_NumCityTabTypes = CityTabTypes.NUM_CITYTAB_TYPES
		g_NumHurryInfos = gc.getNumHurryInfos()
		g_NumUnitClassInfos = gc.getNumUnitClassInfos()
		g_NumBuildingClassInfos = gc.getNumBuildingClassInfos()
		g_NumProjectInfos = gc.getNumProjectInfos()
		g_NumProcessInfos = gc.getNumProcessInfos()
		g_NumActionInfos = gc.getNumActionInfos()


		if self.isHighResolution():
			HUD_City_Left_Panel_Width = 358
			HUD_City_Buildings_Label_Width = 338



		screen.addDDSGFC( "InterfaceCenterLeftBackgroundWidget", 'Art/Interface/Screens/Default/City_Left_Panel.tga', 0, HUD_City_Top_Panel_Height, HUD_City_Left_Panel_Width, yResolution - HUD_City_Bottom_Center_Height - HUD_City_Top_Panel_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceCenterLeftBackgroundWidget" )

		screen.addDDSGFC( "CityScreenAdjustPanel", 'Art/Interface/Screens/Default/City_Status_Panel.tga', 10, 44, HUD_City_Status_Panel_Width, HUD_City_Status_Panel_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "CityScreenAdjustPanel" )

#		screen.addDDSGFC( "TradeRouteListBackground", 'Art/Interface/Screens/Default/City_TradeRoute_Label.tga', 10, 157, HUD_City_TradeRoute_Label_Width, HUD_City_TradeRoute_Label_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#		screen.hide( "TradeRouteListBackground" )
#		screen.setLabel( "TradeRouteListLabel", "Background", localText.getText("TXT_KEY_HEADING_TRADEROUTE_LIST", ()), CvUtil.FONT_CENTER_JUSTIFY, 129, 165, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#		screen.hide( "TradeRouteListLabel" )

		screen.addDDSGFC( "BuildingListBackground", 'Art/Interface/Screens/Default/City_Buildings_Label.tga', 10, 202, HUD_City_Buildings_Label_Width, HUD_City_Buildings_Label_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "BuildingListBackground" )

		screen.addDDSGFC( "InterfaceTopLeftBackgroundWidget", 'Art/Interface/Screens/Default/City_Top_Center_Background_Panel.tga', HUD_City_Left_Panel_Width, HUD_City_Top_Panel_Height, xResolution - HUD_City_Left_Panel_Width - HUD_City_Right_Panel_Width, yResolution - HUD_City_Bottom_Center_Height - HUD_City_Top_Panel_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest( "InterfaceTopLeftBackgroundWidget", HitTestTypes.HITTEST_NOHIT )
		screen.hide( "InterfaceTopLeftBackgroundWidget" )

		screen.addDDSGFC( "TopCityPanelLeft", 'Art/Interface/Screens/Default/City_Growth_Panel.tga', HUD_City_Growth_Panel_Width_Exclusion, 70, xResolution - (2 * HUD_City_Growth_Panel_Width_Exclusion), HUD_City_Growth_Panel_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "TopCityPanelLeft" )

		screen.addDDSGFC( "CityNameBackground", 'Art/Interface/Screens/Default/City_Name_Panel.tga', HUD_City_Name_Panel_Width_Exclusion, 31, xResolution - (2 * HUD_City_Name_Panel_Width_Exclusion), HUD_City_Name_Panel_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "CityNameBackground" )

		screen.addDDSGFC( "InterfaceCenterRightBackgroundWidget", 'Art/Interface/Screens/Default/City_Right_Panel.tga', xResolution - HUD_City_Right_Panel_Width, HUD_City_Top_Panel_Height, HUD_City_Right_Panel_Width, yResolution - HUD_City_Bottom_Center_Height - HUD_City_Top_Panel_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceCenterRightBackgroundWidget" )

		screen.addDDSGFC( "CityExtra1", 'Art/Interface/Screens/Default/City_Extra_1.tga', HUD_City_Extra_1_Location_X, HUD_City_Extra_1_Location_Y, HUD_City_Extra_1_Width, HUD_City_Extra_1_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest( "CityExtra1", HitTestTypes.HITTEST_NOHIT )
		screen.hide( "CityExtra1" )

		screen.addDDSGFC( "CityScreenTopWidget", 'Art/Interface/Screens/Default/City_Top_Panel.tga', 0, 0, xResolution, HUD_City_Top_Panel_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "CityScreenTopWidget" )

		screen.addDDSGFC( "InterfaceCityCenterBackgroundWidget", 'Art/Interface/Screens/Default/City_Bottom_Center.tga', HUD_City_Bottom_Left_Width, yResolution - HUD_City_Bottom_Center_Height, xResolution - HUD_City_Bottom_Left_Width - HUD_City_Bottom_Right_Width, HUD_City_Bottom_Center_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceCityCenterBackgroundWidget" )

		screen.addDDSGFC( "InterfaceCityLeftBackgroundWidget", 'Art/Interface/Screens/Default/City_Bottom_Left.tga', 0, yResolution - HUD_City_Bottom_Left_Height, HUD_City_Bottom_Left_Width, HUD_City_Bottom_Left_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceCityLeftBackgroundWidget" )

		screen.addDDSGFC( "InterfaceCityRightBackgroundWidget", 'Art/Interface/Screens/Default/City_Bottom_Right.tga', xResolution - HUD_City_Bottom_Right_Width, yResolution - HUD_City_Bottom_Right_Height, HUD_City_Bottom_Right_Width, HUD_City_Bottom_Right_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceCityRightBackgroundWidget" )

		screen.addDDSGFC( "InterfaceCenterBackgroundWidget", 'Art/Interface/Screens/Default/Main_Bottom_Center.tga', HUD_Main_Bottom_Left_Width, yResolution - HUD_Main_Bottom_Center_Height, xResolution - HUD_Main_Bottom_Left_Width - HUD_Main_Bottom_Right_Width, HUD_Main_Bottom_Center_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest( "InterfaceCenterBackgroundWidget", HitTestTypes.HITTEST_NOHIT )
		screen.hide( "InterfaceCenterBackgroundWidget" )

		screen.addDDSGFC( "InterfaceLeftBackgroundWidget", 'Art/Interface/Screens/Default/Main_Bottom_Left.tga', 0, yResolution - HUD_Main_Bottom_Left_Height, HUD_Main_Bottom_Left_Width, HUD_Main_Bottom_Left_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceLeftBackgroundWidget" )

		screen.addDDSGFC( "InterfaceRightBackgroundWidget", 'Art/Interface/Screens/Default/Main_Bottom_Right.tga', xResolution - HUD_Main_Bottom_Right_Width, yResolution - HUD_Main_Bottom_Right_Height, HUD_Main_Bottom_Right_Width, HUD_Main_Bottom_Right_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceRightBackgroundWidget" )

		screen.addDDSGFC( "InterfaceTopCenter", 'Art/Interface/Screens/Default/Main_Top_Center.tga', xResolution - HUD_Main_Top_Left_Width, 0, xResolution - HUD_Main_Top_Left_Width - HUD_Main_Top_Right_Width, HUD_Main_Top_Center_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceTopCenter" )

		screen.addDDSGFC( "InterfaceTopLeft", 'Art/Interface/Screens/Default/Main_Top_Left.tga', 0, 0, HUD_Main_Top_Left_Width, HUD_Main_Top_Left_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceTopLeft" )

		screen.addDDSGFC( "InterfaceTopRight", 'Art/Interface/Screens/Default/Main_Top_Right.tga', xResolution - HUD_Main_Top_Left_Width, 0, HUD_Main_Top_Right_Width, HUD_Main_Top_Right_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "InterfaceTopRight" )

		screen.addDDSGFC( "MainExtra1", 'Art/Interface/Screens/Default/Main_Extra_1.tga', HUD_Main_Extra_1_Location_X, HUD_Main_Extra_1_Location_Y, HUD_Main_Extra_1_Width, HUD_Main_Extra_1_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest( "MainExtra1", HitTestTypes.HITTEST_NOHIT )
		screen.hide( "MainExtra1" )

		#Xienwolf Religious HUDs Add Begin
		if yResolution == 768:
			Fudge = 104
		elif yResolution == 800:
			Fudge = 110
		else:
			Fudge = 128


		global CurrentHUD
		for Religion in RelInterfaces:

			screen.addDDSGFC( str(Religion)+"InterfaceTopLeftBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/City_Center.tga', HUD_City_Left_Panel_Width, 34, xResolution - HUD_City_Left_Panel_Width - HUD_City_Right_Panel_Width, Fudge, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceCenterLeftBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/City_Left.tga', 0, HUD_City_Top_Panel_Height, HUD_City_Left_Panel_Width, yResolution - HUD_City_Bottom_Center_Height - HUD_City_Top_Panel_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceCenterRightBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/City_Right.tga', xResolution - 258, 34, 258, yResolution-180, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"CityScreenTopWidget", 'Art/Interface/Screens/'+str(Religion)+'/City_TopBar.tga', 0, 0, xResolution, 34, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"CityNameBackground", 'Art/Interface/Screens/'+str(Religion)+'/City_Title.tga', 262, 34, xResolution - (262 * 2), 32, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#			screen.addDDSGFC( str(Religion)+"InterfaceCityCenterBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/Common_Center.tga', 243, yResolution - 124, xResolution - (243*2), 124, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceCityCenterBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/Common_Center.tga', 243, yResolution - HUD_Main_Bottom_Center_Height, xResolution - (243*2), HUD_Main_Bottom_Center_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#			screen.addDDSGFC( str(Religion)+"InterfaceCenterBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/Common_Center.tga', 244, yResolution - 124, xResolution - (244*2-8), 124, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceCenterBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/Common_Center.tga', HUD_Main_Bottom_Left_Width, yResolution - HUD_Main_Bottom_Center_Height, xResolution - HUD_Main_Bottom_Right_Width, HUD_Main_Bottom_Center_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setHitTest( str(Religion)+"InterfaceCenterBackgroundWidget", HitTestTypes.HITTEST_NOHIT )
#			screen.addDDSGFC( str(Religion)+"InterfaceCityLeftBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/Common_Left.tga', 0, yResolution - 186, 243, 186, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceCityLeftBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/Common_Left.tga', 0, yResolution - HUD_City_Bottom_Left_Height + 20, 243, HUD_City_Bottom_Left_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#			screen.addDDSGFC( str(Religion)+"InterfaceLeftBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/Common_Left.tga', 0, yResolution - 157, 244, 157, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceLeftBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/Common_Left.tga', 0, yResolution - HUD_Main_Bottom_Left_Height + 20, HUD_Main_Bottom_Left_Width, HUD_Main_Bottom_Left_Height, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceCityRightBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/Common_Right.tga', xResolution - 243, yResolution - 186, 243, 186, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceRightBackgroundWidget", 'Art/Interface/Screens/'+str(Religion)+'/Common_Right.tga', xResolution - 236, yResolution - 159, 236, 159, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceTopCenter", 'Art/Interface/Screens/'+str(Religion)+'/Main_Center.tga', 259, 0, xResolution-(259*2), 41, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceTopLeft", 'Art/Interface/Screens/'+str(Religion)+'/Main_Left.tga', 0, 0, 259, 51, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.addDDSGFC( str(Religion)+"InterfaceTopRight", 'Art/Interface/Screens/'+str(Religion)+'/Main_Right.tga', xResolution - 259, 0, 259, 51, WidgetTypes.WIDGET_GENERAL, -1, -1 )

			CurrentHUD = Religion
			self.ClearHUD()
		#Xienwolf Religious HUDs Add End
		iBtnWidth	= 28
		iBtnAdvance = 25
		iBtnY = 27
		iBtnX = 27

		# Turn log Button

#FfH: Modified by Kael 08/13/2008
#		screen.setImageButton( "TurnLogButton", "", iBtnX, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TURN_LOG).getActionInfoIndex(), -1 )
		screen.setImageButton( "TurnLogButton", "", iBtnX + 60, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TURN_LOG).getActionInfoIndex(), -1 )
#FfH: End Modify

		screen.setStyle( "TurnLogButton", "Button_HUDLog_Style" )
		screen.hide( "TurnLogButton" )

		screen.setImageButton("UnitStatsButton1", "Art/Interface/Buttons/Highscores/UnitStatsButton.dds", xResolution - 285, yResolution - 150, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "UnitStatsButton1" )

#FfH: Added by Kael 09/24/2008
		screen.setImageButton( "TrophyButton", "", iBtnX + 86, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TROPHY).getActionInfoIndex(), -1 )
		screen.setStyle( "TrophyButton", "Button_HUDTrophy_Style" )
		screen.hide( "TrophyButton" )

		screen.setImageButton( "SomniumButton", "", iBtnX + 112, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CORPORATION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "SomniumButton", "Button_HUDAdvisorSomnium_Style" )
		screen.hide( "SomniumButton" )
#FfH: End Add
# < Mercenaries Start >
		#iBtnX += iBtnAdvance
		# Set the mercenary manager button in the interface
		screen.setImageButton( "MercenaryManagerButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_MERCENARIES_MANAGER").getPath(), iBtnX+138, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_PYTHON, 7100, 1 )
		# Hide the mercenary manager button 
		screen.hide( "MercenaryManagerButton" )
# < Mercenaries End >
# DynTraits Start
		#iBtnX += iBtnAdvance
	#	if (not gc.isNoCrash()):
		screen.setImageButton( "TraitButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_DYNAMIC_TRAITS").getPath(), iBtnX+164, iBtnY - 2, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_PYTHON, 8001, -1 )
		screen.hide( "TraitButton" )
# DynTraits End
		iBtnX = xResolution - 277

		# Advisor Buttons...
		screen.setImageButton( "DomesticAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_DOMESTIC_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "DomesticAdvisorButton", "Button_HUDAdvisorDomestic_Style" )
		screen.hide( "DomesticAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "FinanceAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FINANCIAL_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "FinanceAdvisorButton", "Button_HUDAdvisorFinance_Style" )
		screen.hide( "FinanceAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "CivicsAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVICS_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "CivicsAdvisorButton", "Button_HUDAdvisorCivics_Style" )
		screen.hide( "CivicsAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "ForeignAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FOREIGN_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ForeignAdvisorButton", "Button_HUDAdvisorForeign_Style" )
		screen.hide( "ForeignAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "MilitaryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "MilitaryAdvisorButton", "Button_HUDAdvisorMilitary_Style" )
		screen.hide( "MilitaryAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "TechAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TECH_CHOOSER).getActionInfoIndex(), -1 )
		screen.setStyle( "TechAdvisorButton", "Button_HUDAdvisorTechnology_Style" )
		screen.hide( "TechAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "ReligiousAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RELIGION_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "ReligiousAdvisorButton", "Button_HUDAdvisorReligious_Style" )
		screen.hide( "ReligiousAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "GuildButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GUILD_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "GuildButton", "Button_HUDAdvisorGuild_Style" )
		screen.hide( "GuildButton" )
		iBtnX += iBtnAdvance
		screen.setImageButton( "VictoryAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_VICTORY_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "VictoryAdvisorButton", "Button_HUDAdvisorVictory_Style" )
		screen.hide( "VictoryAdvisorButton" )

		iBtnX += iBtnAdvance
		screen.setImageButton( "InfoAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_INFO).getActionInfoIndex(), -1 )
		screen.setStyle( "InfoAdvisorButton", "Button_HUDAdvisorRecord_Style" )
		screen.hide( "InfoAdvisorButton" )

#FfH: Modified by Kael 07/25/2008
#		if not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ESPIONAGE):
#			iBtnX += iBtnAdvance
#			screen.setImageButton( "EspionageAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_ESPIONAGE_SCREEN).getActionInfoIndex(), -1 )
#			screen.setStyle( "EspionageAdvisorButton", "Button_HUDAdvisorEspionage_Style" )
#			screen.hide( "EspionageAdvisorButton" )
		iBtnX += iBtnAdvance
		screen.setImageButton( "EspionageAdvisorButton", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_ESPIONAGE_SCREEN).getActionInfoIndex(), -1 )
		screen.setStyle( "EspionageAdvisorButton", "Button_HUDAdvisorEspionage_Style" )
		screen.hide( "EspionageAdvisorButton" )
#FfH: End Modify

		# City Tabs
		iBtnX = xResolution - 324
		iBtnY = yResolution - 94
		iBtnWidth = 24
		iBtnAdvance = 24

		screen.setButtonGFC( "CityTab0", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab0", "Button_HUDJumpUnit_Style" )
		screen.hide( "CityTab0" )

		iBtnY += iBtnAdvance
		screen.setButtonGFC( "CityTab1", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab1", "Button_HUDJumpBuilding_Style" )
		screen.hide( "CityTab1" )

		iBtnY += iBtnAdvance
		screen.setButtonGFC( "CityTab2", "", "", iBtnX, iBtnY, iBtnWidth, iBtnWidth, WidgetTypes.WIDGET_CITY_TAB, 2, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
		screen.setStyle( "CityTab2", "Button_HUDJumpWonder_Style" )
		screen.hide( "CityTab2" )

		# Minimap initialization
		screen.setMainInterface(True)

#FfH: Modified by Kael 07/18/2008
#		screen.addPanel( "MiniMapPanel", u"", u"", True, False, xResolution - 214, yResolution - 151, 208, 151, PanelStyles.PANEL_STYLE_STANDARD )
		screen.addPanel( "MiniMapPanel", u"", u"", True, False, xResolution - 236, yResolution - 151, 240, 155, PanelStyles.PANEL_STYLE_STANDARD )
#FfH: End Modify

		screen.setStyle( "MiniMapPanel", "Panel_Game_HudMap_Style" )
		screen.hide( "MiniMapPanel" )

#FfH: Modified by Kael 07/18/2008
#		screen.initMinimap( xResolution - 210, xResolution - 9, yResolution - 131, yResolution - 9, -0.1 )
		screen.initMinimap( xResolution - 232, xResolution, yResolution - 131, yResolution, -0.1 )
#FfH: End Modify

		gc.getMap().updateMinimapColor()

		self.createMinimapButtons()

		# Help button (always visible)
		screen.setImageButton( "InterfaceHelpButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), xResolution - 28, 2, 24, 24, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVILOPEDIA).getActionInfoIndex(), -1 )
		screen.hide( "InterfaceHelpButton" )

		screen.setImageButton( "MainMenuButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_MENU_ICON").getPath(), xResolution - 54, 2, 24, 24, WidgetTypes.WIDGET_MENU_ICON, -1, -1 )
		screen.hide( "MainMenuButton" )

		# Globeview buttons
		self.createGlobeviewButtons( )

# High Res stuff - Modified by Grey Fox 03/29/2010
		iBtn 		= 48
		iY			= yResolution - 113
		iHeight		= 100
		if self.isHighResolution():
			iBtn	= 64
			iY		= yResolution - g_iVeryHighY
			iHeight	= 132
		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, iY, xResolution - (iMultiListXL+iMultiListXR), iHeight, 4, iBtn, iBtn, TableStyles.TABLE_STYLE_STANDARD )
		screen.hide( "BottomButtonContainer" )

		screen.hide( "BottomButtonContainer2" )
		screen.hide( "BottomButtonContainer3" )
		screen.hide( "BottomButtonContainer_Label" )
		screen.hide( "BottomButtonContainer2_Label" )
		screen.hide( "BottomButtonContainer3_Label" )
# High Res stuff - End Modify


		# *********************************************************************************
		# PLOT LIST BUTTONS
		# *********************************************************************************

		for j in xrange(gc.getMAX_PLOT_LIST_ROWS()):
			yRow = (j - gc.getMAX_PLOT_LIST_ROWS() + 1) * 34

#FfH: Modified by Kael 07/18/2008
#			yPixel = yResolution - 169 + yRow - 3
#			xPixel = 315 - 3
			yPixel = yResolution - 174 + yRow - 3
#			xPixel = 249 - 3 Changed r364
			xPixel = 297 - 3
#FfH: End Modify

			xWidth = self.numPlotListButtons() * 34 + 3
			yHeight = 32 + 3

			szStringPanel = "PlotListPanel" + str(j)
			screen.addPanel(szStringPanel, u"", u"", True, False, xPixel, yPixel, xWidth, yHeight, PanelStyles.PANEL_STYLE_EMPTY)

			for i in xrange(self.numPlotListButtons()):
				k = j*self.numPlotListButtons()+i

				xOffset = i * 34

				szString = "PlotListButton" + str(k)
				screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
				screen.hide( szString )

				szStringHealth = szString + "Health"
				screen.addStackedBarGFCAt( szStringHealth, szStringPanel, xOffset + 3, 22, 32, 22, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1 )
				screen.setHitTest( szStringHealth, HitTestTypes.HITTEST_NOHIT )
				screen.hide( szStringHealth )

				szStringStealth = szString + "Stealth"
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED").getPath()
				screen.addDDSGFCAt( szStringStealth, szStringPanel, szFileName, xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
				screen.setHitTest( szStringStealth, HitTestTypes.HITTEST_NOHIT )
				screen.hide( szStringStealth )

				szStringIcon = szString + "Icon"
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
				screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, xOffset, 0, 12, 12, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
				screen.hide( szStringIcon )

		# *********************************************************************************
		# SLAVE LIST BUTTONS
		# *********************************************************************************


		for u in xrange(2):
			if (u == 0):
				Add = ""
				Adjust = 0
			else:	#Second pass is to set up the panel lower on the screen for a minimized GUI view
				Add = "Bottom"
				Adjust = 138

			for j in xrange(g_iSlaveColumnHeight):
				yRow = j * 34
#				yPixel = yResolution - 172 - yRow + Adjust	Changed r364
				yPixel = yResolution - 208 - yRow + Adjust
				xPixel = 3
				xWidth = 32 + 3
				yHeight = 32 + 3
				xMinionShift = xWidth * g_iSlaveRowLength

				szStringPanel = str(Add) + "SlaveListPanel" + str(j)
				screen.addPanel(szStringPanel, u"", u"", True, False, xPixel, yPixel, xWidth, yHeight, PanelStyles.PANEL_STYLE_EMPTY)

				szMinionStringPanel = str(Add) + "MinionListPanel" + str(j)
				screen.addPanel(szMinionStringPanel, u"", u"", True, False, xPixel+xMinionShift, yPixel, xWidth, yHeight, PanelStyles.PANEL_STYLE_EMPTY)

				for i in xrange(g_iSlaveRowLength):
					k = j*g_iSlaveRowLength+i

					xOffset = i * 34

					szString = str(Add) + "SlaveListButton" + str(k)
					screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_SLAVE_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
					screen.hide( szString )

					szStringHealth = szString + "Health"
					screen.addStackedBarGFCAt( szStringHealth, szStringPanel, xOffset + 3, 22, 32, 22, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( szStringHealth, HitTestTypes.HITTEST_NOHIT )
					screen.hide( szStringHealth )

					szStringStealth = szString + "Stealth"
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED").getPath()
					screen.addDDSGFCAt( szStringStealth, szStringPanel, szFileName, xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
					screen.hide( szStringStealth )

					szStringIcon = szString + "Icon"
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
					screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, xOffset, 0, 12, 12, WidgetTypes.WIDGET_SLAVE_LIST, k, -1, False )
					screen.hide( szStringIcon )

					szString = str(Add) + "MinionListButton" + str(k)
					screen.addCheckBoxGFCAt(szMinionStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_MINION_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
					screen.hide( szString )

					szStringHealth = szString + "Health"
					screen.addStackedBarGFCAt( szStringHealth, szMinionStringPanel, xOffset + 3, 22, 32, 22, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( szStringHealth, HitTestTypes.HITTEST_NOHIT )
					screen.hide( szStringHealth )

					szStringStealth = szString + "Stealth"
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED").getPath()
					screen.addDDSGFCAt( szStringStealth, szMinionStringPanel, szFileName, xOffset + 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
					screen.hide( szStringStealth )

					szStringIcon = szString + "Icon"
					szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
					screen.addDDSGFCAt( szStringIcon, szMinionStringPanel, szFileName, xOffset, 0, 12, 12, WidgetTypes.WIDGET_MINION_LIST, k, -1, False )
					screen.hide( szStringIcon )

			szStringPanel = str(Add) + "MasterUnitPanel"
#			screen.addPanel(szStringPanel, u"", u"", True, False, 139, yResolution - 172 + Adjust, 37, 35, PanelStyles.PANEL_STYLE_EMPTY)	Changed r364
			screen.addPanel(szStringPanel, u"", u"", True, False, 139, yResolution - 208 + Adjust, 37, 35, PanelStyles.PANEL_STYLE_EMPTY)
			szString = str(Add) + "MasterUnitButton"
			screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 3, 3, 32, 32, WidgetTypes.WIDGET_MASTER_UNIT, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
			screen.hide( szString )

			szStringHealth = szString + "Health"
			screen.addStackedBarGFCAt( szStringHealth, szStringPanel, 3, 22, 32, 22, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setHitTest( szStringHealth, HitTestTypes.HITTEST_NOHIT )
			screen.hide( szStringHealth )

			szStringStealth = szString + "Stealth"
			szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED").getPath()
			screen.addDDSGFCAt( szStringStealth, szStringPanel, szFileName, 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
			screen.hide( szStringStealth )

			szStringIcon = szString + "Icon"
			szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
			screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, 0, 0, 12, 12, WidgetTypes.WIDGET_MASTER_UNIT, k, -1, False )
			screen.hide( szStringIcon )

			szStringPanel = str(Add) + "CommanderUnitPanel"
#			screen.addPanel(szStringPanel, u"", u"", True, False, 171, yResolution - 172 + Adjust, 37, 35, PanelStyles.PANEL_STYLE_EMPTY)	Changed r364
			screen.addPanel(szStringPanel, u"", u"", True, False, 171, yResolution - 208 + Adjust, 37, 35, PanelStyles.PANEL_STYLE_EMPTY)
			szString = str(Add) + "CommanderUnitButton"
			screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), 3, 3, 32, 32, WidgetTypes.WIDGET_COMMANDER_UNIT, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL, True )
			screen.hide( szString )

			szStringHealth = szString + "Health"
			screen.addStackedBarGFCAt( szStringHealth, szStringPanel, 3, 22, 32, 22, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setHitTest( szStringHealth, HitTestTypes.HITTEST_NOHIT )
			screen.hide( szStringHealth )

			szStringStealth = szString + "Stealth"
			szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED").getPath()
			screen.addDDSGFCAt( szStringStealth, szStringPanel, szFileName, 3, 3, 32, 32, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
			screen.hide( szStringStealth )

			szStringIcon = szString + "Icon"
			szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
			screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, 0, 0, 12, 12, WidgetTypes.WIDGET_COMMANDER_UNIT, k, -1, False )
			screen.hide( szStringIcon )

		# End Turn Text
		screen.setLabel( "EndTurnText", "Background", u"", CvUtil.FONT_CENTER_JUSTIFY, 0, yResolution - 188, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest( "EndTurnText", HitTestTypes.HITTEST_NOHIT )

		# Three states for end turn button...
		screen.addDDSGFC( "ACIcon", 'Art/Interface/Screens/armageddon.dds', xResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosX, yResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosY, iEndOfTurnButtonSize, iEndOfTurnButtonSize, WidgetTypes.WIDGET_ARMAGEDDON_COUNTER, -1, -1 )
		screen.hide( "ACIcon" )
		screen.setImageButton( "EndTurnButton", "", xResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosX, yResolution - (iEndOfTurnButtonSize/2) - iEndOfTurnPosY, iEndOfTurnButtonSize, iEndOfTurnButtonSize, WidgetTypes.WIDGET_ARMAGEDDON_COUNTER, -1, -1 )
		screen.setStyle( "EndTurnButton", "Button_HUDEndTurn_Style" )
		screen.setEndTurnState( "EndTurnButton", "Red" )
		screen.hide( "EndTurnButton" )

		# *********************************************************************************
		# RESEARCH BUTTONS
		# *********************************************************************************

		i = 0
		for i in xrange( gc.getNumTechInfos() ):
			szName = "ResearchButton" + str(i)
			screen.setImageButton( szName, gc.getTechInfo(i).getButton(), 0, 0, 32, 32, WidgetTypes.WIDGET_RESEARCH, i, -1 )
			screen.hide( szName )

		i = 0
		for i in xrange(gc.getNumReligionInfos()):
			szName = "ReligionButton" + str(i)
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_PICK_RELIGION):
				szButton = gc.getReligionInfo(i).getGenericTechButton()
			else:
				szButton = gc.getReligionInfo(i).getTechButton()
			screen.setImageButton( szName, szButton, 0, 0, 32, 32, WidgetTypes.WIDGET_RESEARCH, gc.getReligionInfo(i).getTechPrereq(), -1 )
			screen.hide( szName )

		# *********************************************************************************
		# CITIZEN BUTTONS
		# *********************************************************************************

		szHideCitizenList = []

		# Angry Citizens
		i = 0
		for i in xrange(MAX_CITIZEN_BUTTONS):
			szName = "AngryCitizen" + str(i)
			screen.setImageButton( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_ANGRYCITIZEN_TEXTURE").getPath(), xResolution - 74 - (26 * i), yResolution - 238, 24, 24, WidgetTypes.WIDGET_ANGRY_CITIZEN, -1, -1 )
			screen.hide( szName )

		iCount = 0

		# **********************************************************
		# GAME DATA STRINGS
		# **********************************************************

		szGameDataList = []
		iStackBarCoordX = 287 + (xResolution - 1024) / 2
		screen.addStackedBarGFC( "ResearchBar", iStackBarCoordX, iStackBarCoordY, iStackBarWidth, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RESEARCH_STORED") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_RESEARCH_RATE") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ResearchBar" )
# Great Person Bar

		
		screen.addStackedBarGFC( "GreatPersonBar", iStackBarCoordX, iStackBarCoordY+iStackBarDeltaY, iStackBarWidth, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPersonBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPersonBar" )


		screen.addStackedBarGFC("EmergentLeaderXPBar", iXPBarCoordX, iXPBarCoordY, iStackBarWidth, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setStackedBarColors("EmergentLeaderXPBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED"))
		screen.setStackedBarColors("EmergentLeaderXPBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE"))
		screen.setStackedBarColors("EmergentLeaderXPBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY"))
		screen.setStackedBarColors("EmergentLeaderXPBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY"))
		screen.hide( "EmergentLeaderXPBar" )
		# *********************************************************************************
		# SELECTION DATA BUTTONS/STRINGS
		# *********************************************************************************

		szHideSelectionDataList = []

		screen.addStackedBarGFC( "PopulationBar", iCityCenterRow1X, iCityCenterRow1Y-4, xResolution - (iCityCenterRow1X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_POPULATION, -1, -1 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColorsAlpha( "PopulationBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType(), 0.8 )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_NEGATIVE_RATE") )
		screen.setStackedBarColors( "PopulationBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "PopulationBar" )

		screen.addStackedBarGFC( "ProductionBar", iCityCenterRow2X, iCityCenterRow2Y-4, xResolution - (iCityCenterRow2X*2), iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_PRODUCTION, -1, -1 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_STORED, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType() )
		screen.setStackedBarColorsAlpha( "ProductionBar", InfoBarTypes.INFOBAR_RATE, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getColorType(), 0.8 )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getColorType() )
		screen.setStackedBarColors( "ProductionBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "ProductionBar" )

		screen.addStackedBarGFC( "GreatPeopleBar", xResolution - 246, yResolution - 180, 194, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_GREAT_PEOPLE, -1, -1 )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_STORED") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_GREAT_PEOPLE_RATE") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "GreatPeopleBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "GreatPeopleBar" )

		screen.addStackedBarGFC( "CultureBar", 16, yResolution - 188, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_CULTURE, -1, -1 )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_CULTURE_STORED") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString("COLOR_CULTURE_RATE") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_RATE_EXTRA, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.setStackedBarColors( "CultureBar", InfoBarTypes.INFOBAR_EMPTY, gc.getInfoTypeForString("COLOR_EMPTY") )
		screen.hide( "CultureBar" )

		# Holy City Overlay
		for i in xrange( gc.getNumReligionInfos() ):
			xCoord = xResolution - 242 + (i * 26)
			yCoord = 42
			szName = "ReligionHolyCityDDS" + str(i)
			screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
			screen.hide( szName )

		for i in xrange( gc.getNumCorporationInfos() ):
			xCoord = xResolution - 248 + (i * 23)
			yCoord = 70
			szName = "CorporationHeadquarterDDS" + str(i)
			screen.addDDSGFC( szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HOLYCITY_OVERLAY").getPath(), xCoord, yCoord, 21, 21, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
			screen.hide( szName )

		screen.addStackedBarGFC( "NationalityBar", 16, yResolution - 214, 220, iStackBarHeight, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_NATIONALITY, -1, -1 )
		screen.hide( "NationalityBar" )

		screen.setButtonGFC( "CityScrollMinus", u"", "", 274, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "CityScrollMinus" )

		screen.setButtonGFC( "CityScrollPlus", u"", "", 288, 32, 32, 32, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "CityScrollPlus" )

		screen.setButtonGFC( "PlotListMinus", u"", "", 315 + ( xResolution - (iMultiListXL+iMultiListXR) - 68 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "PlotListMinus" )

		screen.setButtonGFC( "PlotListPlus", u"", "", 298 + ( xResolution - (iMultiListXL+iMultiListXR) - 34 ), yResolution - 171, 32, 32, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, 1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "PlotListPlus" )

		# *********************************************************************************
		# UNIT INFO ELEMENTS
		# *********************************************************************************

		# Promotions

		for i in xrange(iPromotionsPerPage):
			szName	= "PromotionButton" + str(i)
			szName2	= szName + "Duration"
			szName3	= szName + "Quantity"
			screen.addDDSGFC( szName,"", 1, 1, 26, 26, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setText( szName2, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 1, 1, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setHitTest( szName2, HitTestTypes.HITTEST_NOHIT )
			screen.setText( szName3, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 1, 1, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setHitTest( szName3, HitTestTypes.HITTEST_NOHIT )
			screen.hide( szName )
			screen.hide( szName2 )
			screen.hide( szName3 )

		screen.setButtonGFC( "PromotionScrollPlus", u"", "", 264, yResolution - 58, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_RIGHT )
		screen.hide( "PromotionScrollPlus" )
		screen.setButtonGFC( "PromotionScrollMinus", u"", "", 2, yResolution - 58, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_ARROW_LEFT )
		screen.hide( "PromotionScrollMinus" )

		# *********************************************************************************
		# SCORES
		# *********************************************************************************

		screen.addPanel( "ScoreBackground", u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_MAIN )
		screen.hide( "ScoreBackground" )

#FfH: Added by Kael 10/29/2007
		screen.addPanel( "ManaBackground", u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "ManaBackground" )
#FfH: End Add

#AoE: Added by LeastCraft 09/04/2025
		screen.addPanel( "ArchosBroodActivityBackground", u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP )
		screen.hide( "ArchosBroodActivityBackground" )
#AoE: End Add

		for i in xrange( gc.getMAX_PLAYERS() ):
			szName = "ScoreText" + str(i)
			screen.setText( szName, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 996, 622, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_CONTACT_CIV, i, -1 )
			screen.hide( szName )

		# This should be a forced redraw screen
		screen.setForcedRedraw( True )

		# This should show the screen immidiately and pass input to the game
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)

		szHideList = []

		szHideList.append( "CreateGroup" )
		szHideList.append( "DeleteGroup" )

		# City Tabs
		for i in xrange( g_NumCityTabTypes ):
			szButtonID = "CityTab" + str(i)
			szHideList.append( szButtonID )

		for i in xrange( g_NumHurryInfos ):
			szButtonID = "Hurry" + str(i)
			szHideList.append( szButtonID )

		screen.registerHideList( szHideList, len(szHideList), 0 )

		#Xienwolf Religious HUDs Add Begin
		screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
		self.ClearHUD()
		#Xienwolf Religious HUDs Add End
		return 0

		screen.setButtonGFC( "ScoreToggle", u"", "", 0, 0, 18,18, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
		screen.hide("ScoreToggle")

	# Will update the screen (every 250 MS)
	def updateScreen(self):

		global g_szTimeText
		global g_iTimeTextCounter

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		self.m_iNumPlotListButtons = (xResolution - (iMultiListXL+iMultiListXR) - 68) / 34

		# This should recreate the minimap on load games and returns if already exists -JW
		screen.initMinimap( xResolution - 232, xResolution, yResolution - 131, yResolution, -0.1 )

		messageControl = CyMessageControl()

		bShow = False

		# Hide all interface widgets
		#screen.hide( "EndTurnText" )
		iPlayer = gc.getGame().getActivePlayer()
		pPlayer = gc.getPlayer(iPlayer)

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			if (gc.getGame().isPaused()):
				# Pause overrides other messages
				acOutput = localText.getText("SYSTEM_GAME_PAUSED", (gc.getPlayer(gc.getGame().getPausePlayer()).getNameKey(), ))
				#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
				screen.setEndTurnState( "EndTurnText", acOutput )
				bShow = True
			elif (messageControl.GetFirstBadConnection() != -1):
				# Waiting on a bad connection to resolve
				if (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 1):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 2):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
			else:
				# Flash select messages if no popups are present
				if ( CyInterface().shouldDisplayReturn() ):
					acOutput = localText.getText("SYSTEM_RETURN", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingOthers() ):
					acOutput = localText.getText("SYSTEM_WAITING", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayEndTurn() ):
					acOutput = localText.getText("SYSTEM_END_TURN", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingYou() ):
					acOutput = localText.getText("SYSTEM_WAITING_FOR_YOU", ())
					#screen.modifyLabel( "EndTurnText", acOutput, CvUtil.FONT_CENTER_JUSTIFY )
					screen.setEndTurnState( "EndTurnText", acOutput )
					bShow = True

		if ( bShow ):
			screen.showEndTurn( "EndTurnText" )
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isCityScreenUp() ):
				screen.moveItem( "EndTurnText", 0, yResolution - 194, -0.1 )
			else:
				screen.moveItem( "EndTurnText", 0, yResolution - 86, -0.1 )
		else:
			screen.hideEndTurn( "EndTurnText" )

		screen.hide( "ACText" )
		if (not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
			if (pPlayer != None):
				ACstr = u"<font=2i><color=%d,%d,%d,%d>%s</color></font>" %(pPlayer.getPlayerTextColorR(),pPlayer.getPlayerTextColorG(),pPlayer.getPlayerTextColorB(),pPlayer.getPlayerTextColorA(),str(CyGame().getGlobalCounter()) + str(" "))
				screen.setText( "ACText", "Background", ACstr, CvUtil.FONT_CENTER_JUSTIFY, xResolution - 239, yResolution - 157, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.setHitTest( "ACText", HitTestTypes.HITTEST_NOHIT )

		self.updateEndTurnButton()
		self.updatexUPT()
		if (CyGame().isUPTLock()):
			screen.setHitTest( "xUPTButton", HitTestTypes.HITTEST_NOHIT )

		screen.hide( "AIText" )
		if (not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
			if (CyGame().getAIAutoPlay() > 0):
				AIstr = u"<font=2>%d Turns AutoPlay Left</font>" %(CyGame().getAIAutoPlay())
				screen.setText( "AIText", "Background", AIstr, CvUtil.FONT_LEFT_JUSTIFY, 257, 3, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.setHitTest( "AIText", HitTestTypes.HITTEST_NOHIT )
#Awakened display
		screen.hide( "SRText" )
		screen.hide( "Awakenedchance" )
		screen.hide( "ScorpText" )
		screen.hide( "Scorpchance" )
		if (not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
			#*************************************************************************************************#
			#** Spawn Probability - Scions - Awakened                                                       **#
			#*************************************************************************************************#
			if (pPlayer!=None):
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SCIONS') and pPlayer.getNumCities() > 0:
					tScionCap	= cf.calculateScionCap(iPlayer)
					iCurPop		= ""
					iMaxPop		= ""
					if tScionCap != -1:
						iCurPop		= tScionCap[0]
						iMaxPop		= tScionCap[1]
					iSpawnOdds  = pPlayer.getCivCounter() # spawn chance, rounded to 2 digits from the decimal point
					iInteger    = iSpawnOdds / 100
					iDecimal    = iSpawnOdds % 100
					if iInteger + iDecimal > 0: # if the value is high enough (min 0.01%)
						SRstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(".") + str(iDecimal) + str("% ") + "  " + str(iCurPop) + "/" + str(iMaxPop) + "  " )
						screen.setImageButton("Awakenedchance", "Art/Interface/Buttons/Units/Scions/awake.dds", 177, 7, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setText( "SRText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 189, 5, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
					else:
						screen.hide( "Awakenedchance" )
						screen.hide( "SRText" )
			#*************************************************************************************************#
			#** Spawn Probability - Scions - Awakened                                                   END **#
			#*************************************************************************************************#
			#*************************************************************************************************#
			#** Spawn Probability - Mekara - Aspirant                                                       **#
			#*************************************************************************************************#
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MEKARA_V2') and pPlayer.getNumCities() > 0 and pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_IRAM'):
					iSpawnOdds  = pPlayer.getCivCounter() # spawn chance, rounded to 2 digits from the decimal point
					iInteger    = iSpawnOdds / 100
					iDecimal    = iSpawnOdds % 100
					if iInteger + iDecimal > 0: # if the value is high enough (min 0.01%)
						SRstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(".") + str(iDecimal) + str("% "))
						screen.setImageButton("Awakenedchance", "Art/Interface/Buttons/Units/Adventurer.dds", 177, 7, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setText( "SRText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 189, 5, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
					else:
						screen.hide( "Awakenedchance" )
						screen.hide( "SRText" )
			#*************************************************************************************************#
			#** Spawn Probability - Mekara - Aspirant                                                   END **#
			#*************************************************************************************************#
			#*************************************************************************************************#
			#** Spawn Probability - Grigori - Adventurers                                                   **#
			#*************************************************************************************************#
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_GRIGORI') and pPlayer.getNumCities() > 0:
					iSpawnOdds  = pPlayer.getCivCounter() # spawn chance, rounded to 2 digits from the decimal point
					iInteger    = iSpawnOdds / 100
					iDecimal    = iSpawnOdds % 100
					fGrigoriMod = (pPlayer.getCivCounterMod() / 100)
					fSecondPart = iSpawnOdds - (iInteger * 100)
					if iInteger + iDecimal > 0: # if the value is high enough (min 0.01%)
						SRstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(".") + str(iDecimal) + str(" / ") + str(fGrigoriMod) + str(" "))
						screen.setImageButton("Awakenedchance", "Art/Interface/Buttons/Units/Adventurer.dds", 177, 7, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setText( "SRText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 189, 5, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
					else:
						screen.hide( "Awakenedchance" )
						screen.hide( "SRText" )
			#*************************************************************************************************#
			#** Spawn Probability - Grigori - Adventurers                                               END **#
			#*************************************************************************************************#
			#*************************************************************************************************#
			#** Soul Counter - Court of Misrak - Souls  (DrackAosNiSira Module)                             **#
			#*************************************************************************************************#
				elif gc.getInfoTypeForString('MODULE_DRACKAOSNISIRA')!=-1 and pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_COURTOFMISRAK'):
					iSoulCounter  = pPlayer.getCivCounter() # Souls in Storage
					iInteger    = iSoulCounter
					SRstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(" "))
					screen.setImageButton("SoulCounter", "Modules\NormalModules\DrackAosNiSira\Art\Other\Souls.dds", 177, 7, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setText( "SRText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 189, 5, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
			#*************************************************************************************************#
			#** Soul Counter - Court of Misrak - Souls  (DrackAosNiSira Module)                         END **#
			#*************************************************************************************************#
			#*************************************************************************************************#
			#** Spawn Probability - Doviello - Animals                                                      **#
			#*************************************************************************************************#
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO') and pPlayer.getNumCities() > 0:
					pDen = pPlayer.getCapitalCity()
					iSpawnOdds = pDen.getCityCounter() # spawn chance of capital, not civ
					iInteger    = iSpawnOdds / 100
					iDecimal    = iSpawnOdds % 100
					if iInteger + iDecimal > 0: # if the value is high enough (min 0.01%)
						SRstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(".") + str(iDecimal) + str("% "))
						screen.setImageButton("Awakenedchance", "Art/Interface/Buttons/Units/Wolf.dds", 177, 7, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setText( "SRText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 189, 5, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
					else:
						screen.hide( "Awakenedchance" )
						screen.hide( "SRText" )
			#*************************************************************************************************#
			#** Spawn Probability - Doviello - Animals                                                  END **#
			#*************************************************************************************************#
			#*************************************************************************************************#
			#** Spawn Probability - Archos - Spiders                                                        **#
			#*************************************************************************************************#
				elif gc.getInfoTypeForString('MODULE_ARACHNOPHOBIA')==-1 and pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ARCHOS') and pPlayer.getNumCities() > 0:
					iSpawnOdds  = pPlayer.getCivCounter() # spawn chance, rounded to 2 digits from the decimal point
					iInteger    = iSpawnOdds / 100
					iDecimal    = iSpawnOdds % 100
					if (iInteger + iDecimal > 0): # if the value is high enough (min 0.01%)
						SRstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(".") + str(iDecimal) + str("% "))
						screen.setImageButton("Awakenedchance", "Art/Interface/Buttons/Units/Spider.dds", 177, 7, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setText( "SRText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 189, 5, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
					else:
						screen.hide( "Awakenedchance" )
						screen.hide( "SRText" )
			#*************************************************************************************************#
			#** Spawn Probability - Archos - Spiders                                                    END **#
			#*************************************************************************************************#
			#*************************************************************************************************#
			#** Spawn Probability - Archos - Scorpions                                                      **#
			#*************************************************************************************************#
					iSpawnOdds  = pPlayer.getCivCounterMod() # spawn chance, rounded to 2 digits from the decimal point
					iInteger    = iSpawnOdds / 100
					iDecimal    = iSpawnOdds % 100
					if (iInteger + iDecimal > 0): # if the value is high enough (min 0.01%)
						SRstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(".") + str(iDecimal) + str("% "))
						screen.setImageButton("Scorpchance", "Art/Interface/Buttons/Units/Scorpion.dds", 177, 27, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setText( "ScorpText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 189, 25, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "ScorpText", HitTestTypes.HITTEST_NOHIT )
					else:
						screen.hide( "Scorpchance" )
						screen.hide( "ScorpText" )
			#*************************************************************************************************#
			#** Spawn Probability - Archos - Scorpions                                                  END **#
			#*************************************************************************************************#
			#*************************************************************************************************#
			#** Spawn Probability - Archos - Brood Activity                                                 **#
			#*************************************************************************************************#
				elif gc.getInfoTypeForString('MODULE_ARACHNOPHOBIA')!=-1 and pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ARCHOS') and pPlayer.getNumCities() > 0:
					iBroodActivity = pPlayer.getCivCounter() # brood activity, rounded to 2 digits from the decimal point
					iBAInteger     = iBroodActivity / 100
					iBADecimal     = iBroodActivity % 100
					iSpawnOdds     = pPlayer.getCivCounterMod() # spawn chance, rounded to 2 digits from the decimal point
					iSpawnInteger  = iSpawnOdds / 100
					iSpawnDecimal  = iSpawnOdds % 100

					if iBAInteger >= 800:
						BAstr = u"<font=2i>%s</font>" %(str(" ") + str(localText.getText("TXT_KEY_MISC_BROOD_ACTIVITY_4", ())) + str(" "))
					elif iBAInteger >= 400:
						BAstr = u"<font=2i>%s</font>" %(str(" ") + str(localText.getText("TXT_KEY_MISC_BROOD_ACTIVITY_3", ())) + str(" "))
					elif iBAInteger >= 200:
						BAstr = u"<font=2i>%s</font>" %(str(" ") + str(localText.getText("TXT_KEY_MISC_BROOD_ACTIVITY_2", ())) + str(" "))
					else:
						BAstr = u"<font=2i>%s</font>" %(str(" ") + str(localText.getText("TXT_KEY_MISC_BROOD_ACTIVITY_1", ())) + str(" "))
					screen.setImageButton("Awakenedchance", "Art/Interface/Buttons/Units/Spider.dds", 6, 331, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setText( "SRText", "Background", BAstr, CvUtil.FONT_LEFT_JUSTIFY, 18, 329, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )

					SRstr = u"<font=2i>%s</font>" %(str(" ") + str(iBAInteger) + str(".") + str(iBADecimal) + str(" + ") + str(iSpawnInteger) + str(".") + str(iSpawnDecimal) + str(" "))
					screen.setText( "ScorpText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 18, 349, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "ScorpText", HitTestTypes.HITTEST_NOHIT )
			#*************************************************************************************************#
			#** Spawn Probability - Archos - Brood Activity                                             END **#
			#*************************************************************************************************#
			#*************************************************************************************************#
			#** Spawn Probability - Jotnar - MOVE TO MODULE                                                 **#
			#*************************************************************************************************#
				elif gc.getInfoTypeForString('MODULE_JOTNAR')!=-1 and pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_JOTNAR') and pPlayer.getNumCities() > 0:
	
					pCity = pPlayer.getCapitalCity()
					fSpawnOdds = pCity.getCityCounter()
					fFirstPart = fSpawnOdds / 100
					fSecondPart = fSpawnOdds - (fFirstPart * 100)

					if fFirstPart + fSecondPart > 0:
	
						SRstr = u"<font=2i>%s</font>" %(str(" ") + str(fFirstPart) + str(".") + str(fSecondPart) + str("% "))
						screen.setImageButton("Awakenedchance", "Art/Civs/Jotnar/buttons/jot_era1.dds", 177, 7, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setText( "SRText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 189, 5, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
					else:
						screen.hide( "Awakenedchance" )
						screen.hide( "SRText" )
			#*************************************************************************************************#
			#** Spawn Probability - Jotnar - MOVE TO MODULE                                             END **#
			#*************************************************************************************************#
			#*************************************************************************************************#
			#** Spawn Probability - Sheaim - Planar creatures                                               **#
			#*************************************************************************************************#
				elif pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM') and pPlayer.getNumCities() > 0:
					pCity = pPlayer.getCapitalCity()
					if pCity.getCityCounter() > 0:
						iSpawnOdds = pCity.getCityCounter()
						iInteger    = iSpawnOdds / 100
						iDecimal    = iSpawnOdds % 100
						if (iInteger + iDecimal > 0): # if the value is high enough (min 0.01%)
							SRstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(".") + str(iDecimal) + str("% "))
							screen.setImageButton("Awakenedchance", "Art/Interface/Buttons/Buildings/PlanarGate.dds", 177, 7, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
							screen.setText( "SRText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 189, 5, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
							screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
						else:
							screen.hide( "Awakenedchance" )
							screen.hide( "SRText" )
			#*************************************************************************************************#
			#** Spawn Probability - Sheaim - Planar creatures                                           END **#
			#*************************************************************************************************#
			#*************************************************************************************************#
			#** Free Promos - Anscarca                                                                        **#
			#*************************************************************************************************#
				elif gc.getInfoTypeForString("MODULE_ANSCARCA")!=-1 and pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ANSCARCA') and pPlayer.getNumCities() > 0:
					anscarcaGlobalExp = pPlayer.getCivCounterMod()
					anscarcaGeneTier = int(math.floor(math.sqrt(anscarcaGlobalExp / 100)))
				
					SRstr = u"<font=2i>%s(%s)</font>" % (str(anscarcaGlobalExp),str(anscarcaGeneTier))
					screen.setImageButton("GeneTier", "Art/Interface/Buttons/Projects/Natures Revolt.dds", 177, 7, 16, 16, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setText( "SRText", "Background", SRstr, CvUtil.FONT_LEFT_JUSTIFY, 189, 5, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
			#*************************************************************************************************#
			#** Free Promos - Anscarca                                                                    END **#
			#*************************************************************************************************#		if (CyInterface().isCityScreenUp()):
				pHeadSelectedCity = CyInterface().getHeadSelectedCity()
				if (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
				#*************************************************************************************************#
				#** Spawn Probability - Doviello - Animals                                                      **#
				#*************************************************************************************************#
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
						iSpawnOdds = pHeadSelectedCity.getCityCounter()
						iInteger    = iSpawnOdds / 100
						iDecimal    = iSpawnOdds % 100
						if iInteger + iDecimal > 0: # if the value is high enough (min 0.01%)
							DAstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(".") + str(iDecimal) + str("% "))
							screen.setImageButton("Awakenedchance", "Art/Interface/Buttons/Units/Wolf.dds", 256, 166, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1 )
							screen.setText( "SRText", "Background", DAstr, CvUtil.FONT_LEFT_JUSTIFY, 275, 164, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
							screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
						else:
							screen.hide( "Awakenedchance" )
							screen.hide( "SRText" )
				#*************************************************************************************************#
				#** Spawn Probability - Doviello - Animals                                                  END **#
				#*************************************************************************************************#
				#*************************************************************************************************#
				#** Spawn Probability - Sheaim - Planar creatures                                               **#
				#*************************************************************************************************#
					elif pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
						if pHeadSelectedCity.getCityCounter() > 0:
							iSpawnOdds = pHeadSelectedCity.getCityCounter()
							iInteger    = iSpawnOdds / 100
							iDecimal    = iSpawnOdds % 100
							if iInteger + iDecimal > 0: # if the value is high enough (min 0.01%)
								DAstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(".") + str(iDecimal) + str("% "))
								screen.setImageButton("Awakenedchance", "Art/Interface/Buttons/Buildings/PlanarGate.dds", 256, 166, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1 )
								screen.setText( "SRText", "Background", DAstr, CvUtil.FONT_LEFT_JUSTIFY, 275, 164, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
								screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
							else:
								screen.hide( "Awakenedchance" )
								screen.hide( "SRText" )
				#*************************************************************************************************#
				#** Spawn Probability - Sheaim - Planar creatures                                           END **#
				#*************************************************************************************************#
				#*************************************************************************************************#
				#** Spawn Probability - Grigori - Adventurers                                                   **#
				#*************************************************************************************************#
					elif pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):

						if pHeadSelectedCity.getCityCounter() > 0:
							iSpawnOdds = pHeadSelectedCity.getCityCounter()
							iInteger    = iSpawnOdds / 100
							iDecimal    = iSpawnOdds % 100
							if iInteger + iDecimal > 0: # if the value is high enough (min 0.01%)
								DAstr = u"<font=2i>%s</font>" %(str(" ") + str(iInteger) + str(".") + str(iDecimal) + str("% "))
								screen.setImageButton("Awakenedchance", "Art/Interface/Buttons/Units/Settler.dds", 256, 166, 24, 24, WidgetTypes.WIDGET_GENERAL, -1, -1 )
								screen.setText( "SRText", "Background", DAstr, CvUtil.FONT_LEFT_JUSTIFY, 275, 164, 0.5, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
								screen.setHitTest( "SRText", HitTestTypes.HITTEST_NOHIT )
							else:
								screen.hide( "Awakenedchance" )
								screen.hide( "SRText" )
				#*************************************************************************************************#
				#** Spawn Probability - Grigori - Adventurers                                               END **#
				#*************************************************************************************************#

		if (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
			self.updateTimeText()
			screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( "TimeText" )
		else:
			screen.hide( "TimeText" )

		return 0

	# Will redraw the interface
	def redraw( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Check Dirty Bits, see what we need to redraw...
		if (CyInterface().isDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT) == True):
			# Percent Buttons
			self.updatePercentButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PercentButtons_DIRTY_BIT, False)
		if (CyInterface().isDirty(InterfaceDirtyBits.Flag_DIRTY_BIT) == True):
			# Percent Buttons
			self.updateFlag()
			CyInterface().setDirty(InterfaceDirtyBits.Flag_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT) == True ):
			# Miscellaneous buttons (civics screen, etc)
			self.updateMiscButtons()
			CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT) == True ):
			# Info Pane Dirty Bit
			# This must come before updatePlotListButtons so that the entity widget appears in front of the stats
			self.updateInfoPaneStrings()
			CyInterface().setDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT) == True ):
			# Plot List Buttons Dirty
			self.updatePlotListButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT) == True ):
			# Selection Buttons Dirty
			self.updateSelectionButtons()
			CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT) == True ):
			# Research Buttons Dirty
			self.updateResearchButtons()
			CyInterface().setDirty(InterfaceDirtyBits.ResearchButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT) == True ):
			# Citizen Buttons Dirty
			self.updateCitizenButtons()
			CyInterface().setDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GameData_DIRTY_BIT) == True ):
			# Game Data Strings Dirty
			self.updateGameDataStrings()
			CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Help_DIRTY_BIT) == True ):
			# Help Dirty bit
			self.updateHelpStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Help_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT) == True ):
			# Selection Data Dirty Bit
			self.updateCityScreen()
			CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Score_DIRTY_BIT) == True or CyInterface().checkFlashUpdate() ):
			# Scores!
			self.updateScoreStrings()

#FfH: Added by Kael 04/30/2007
			self.updateManaStrings()
			self.updatexUPT()
#FfH: End Add

			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT) == True ):
			# Globeview and Globelayer buttons
			CyInterface().setDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT, False)
			self.updateGlobeviewButtons()

		return 0

	# Will update the percent buttons
	def updatePercentButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		for iI in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
			szString = "IncreasePercent" + str(iI)
			screen.hide( szString )
			szString = "DecreasePercent" + str(iI)
			screen.hide( szString )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if ( not CyInterface().isCityScreenUp() or ( pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() ) or gc.getGame().isDebugMode() ):
			iCount = 0

			if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
				for iI in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
					# Intentional offset...
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES

					iShift = 60
					if (CyInterface().isCityScreenUp()):
						iShift = 0

					if (gc.getActivePlayer().isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
						szString1 = "IncreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString1, u"", "", 70 + iShift, 50 + (19 * iCount), 20, 20, WidgetTypes.WIDGET_PYTHON, 5001, eCommerce, ButtonStyles.BUTTON_STYLE_CITY_PLUS ) #gc.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS")
						screen.show( szString1 )
						szString2 = "DecreasePercent" + str(eCommerce)
						screen.setButtonGFC( szString2, u"", "", 90 + iShift, 50 + (19 * iCount), 20, 20, WidgetTypes.WIDGET_PYTHON, 5002, eCommerce, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
						screen.show( szString2 )

						iCount = iCount + 1

						if (gc.getActivePlayer().isCommerceFlexible(eCommerce)):
							screen.enable( szString1, True )
							screen.enable( szString2, True )
						else:
							screen.enable( szString1, False )
							screen.enable( szString2, False )

		return 0

	# Will update the end Turn Button
	def updateEndTurnButton( self ):

		global g_eEndTurnButtonState

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().shouldDisplayEndTurnButton() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):

			eState = CyInterface().getEndTurnState()

			bShow = False

			if ( eState == EndTurnButtonStates.END_TURN_OVER_HIGHLIGHT ):
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				bShow = True
			elif ( eState == EndTurnButtonStates.END_TURN_OVER_DARK ):
				screen.setEndTurnState( "EndTurnButton", u"Red" )
				bShow = True
			elif ( eState == EndTurnButtonStates.END_TURN_GO ):
				screen.setEndTurnState( "EndTurnButton", u"Green" )
				bShow = True

			if ( bShow ):
				screen.showEndTurn( "EndTurnButton" )
			else:
				screen.hideEndTurn( "EndTurnButton" )

			if ( g_eEndTurnButtonState == eState ):
				return

			g_eEndTurnButtonState = eState

		else:
			screen.hideEndTurn( "EndTurnButton" )

		return 0

	# Update the miscellaneous buttons
	def updateMiscButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		xResolution = screen.getXResolution()

# FFHBUG
# Great Person Bar
		self.updateGreatPersonBar(screen)
		if not gc.isNoCrash():
			self.updateEmergentLeaderXPBar(screen)
###

		if ( CyInterface().shouldDisplayFlag() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			screen.show( "CivilizationFlag" )
			screen.show( "InterfaceHelpButton" )
			screen.show( "MainMenuButton" )
		else:
			screen.hide( "CivilizationFlag" )
			screen.hide( "InterfaceHelpButton" )
			screen.hide( "MainMenuButton" )

		#Xienwolf Religious HUDs Add Begin  (Original Omitted)

		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())

		iCurrentReligion = pPlayer.getStateReligion()

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_RELIGIOUS_HUD):
			if  iCurrentReligion== gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				Religion = 'Ashen'
			elif iCurrentReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
				Religion = 'Overlords'
			elif iCurrentReligion == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
				Religion = 'Esus'
			elif iCurrentReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				Religion = 'Fellowship'
			elif iCurrentReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
				Religion = 'Runes'
			elif iCurrentReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				Religion = 'Empyrean'
			elif iCurrentReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
				Religion = 'Order'
			else:
#				Religion = 'Default'
				Religion = ''
		else:
			Religion = ''

		global CurrentHUD
		if Religion != CurrentHUD:
			self.ClearHUD()
			CurrentHUD = Religion

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			self.ClearHUD()
			# < Mercenaries Start >
			screen.hide( "MercenaryManagerButton" )
			# < Mercenaries End >
		elif ( CyInterface().isCityScreenUp() ):
			self.ClearHUD()
			# < Mercenaries Start >
			screen.hide( "MercenaryManagerButton" )
			# < Mercenaries End >
			self.CityHUD()
		elif ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE):
			self.ClearHUD()
			# < Mercenaries Start >
			# Show the mercenary manager button if the player has at least one city and mercenaries are unlocked.
			if (not gc.isNoCrash()):
				if(gc.getActivePlayer().getNumCities() > 0 and gc.getGame().isUnlockMercenaries()):
						screen.show( "MercenaryManagerButton" )
			# < Mercenaries End >
			self.PartialHUD()
			# < Mercenaries Start >
			# move the mercenary manager button to the front if the player has at least one city and mercenaries are unlocked.
			if (not gc.isNoCrash()):
				if(gc.getActivePlayer().getNumCities() > 0 and gc.getGame().isUnlockMercenaries()):
						screen.moveToFront( "MercenaryManagerButton" )
			# < Mercenaries End >

		elif (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_ADVANCED_START):
			self.ClearHUD()
			self.AdvancedStartHUD()

		elif ( CyEngine().isGlobeviewUp() ):
			self.ClearHUD()
			# < Mercenaries Start >
			# Show the mercenary manager button if the player has at least one city and mercenaries are unlocked.
			if (not gc.isNoCrash()):
				if(gc.getActivePlayer().getNumCities() > 0 and gc.getGame().isUnlockMercenaries()):
					screen.show( "MercenaryManagerButton" )
			# < Mercenaries End >
			self.GlobeView()
			# < Mercenaries Start >
			# Move the mercenary manager button to the front if the player has at least one city and they are in the
			# correct era.
			if (not gc.isNoCrash()):
				if(gc.getActivePlayer().getNumCities() > 0 and gc.getGame().isUnlockMercenaries()):
					screen.moveToFront( "MercenaryManagerButton" )
			# < Mercenaries End >

		else:
			self.ClearHUD()
			# < Mercenaries Start >
			# Show the mercenary manager button if the player has at least one city and they are in the
			# correct era.
			if( (not gc.isNoCrash()) and gc.getActivePlayer().getNumCities() > 0 and gc.getGame().isUnlockMercenaries()):
				screen.show( "MercenaryManagerButton" )
			# < Mercenaries End >
			self.MainHUD()
			# < Mercenaries Start >
			# Move the mercenary manager button to the front if the player has at least one city and they are in the
			# correct era.
			if((not gc.isNoCrash()) and gc.getActivePlayer().getNumCities() > 0 and gc.getGame().isUnlockMercenaries()):
				screen.moveToFront( "MercenaryManagerButton" )
			# < Mercenaries End >

		screen.updateMinimapVisibility()

		return 0
	#Xienwolf Religious HUDs Add Begin
	def ClearHUD( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		global CurrentHUD
		

		screen.hide( str(CurrentHUD)+"CityNameBackground" )
		screen.hide( str(CurrentHUD)+"CityScreenTopWidget" )
		screen.hide( str(CurrentHUD)+"InterfaceTopLeftBackgroundWidget" )
		screen.hide( str(CurrentHUD)+"InterfaceTopRightBackgroundWidget" )
		screen.hide( str(CurrentHUD)+"InterfaceCenterLeftBackgroundWidget" )
		screen.hide( str(CurrentHUD)+"InterfaceCenterRightBackgroundWidget" )
		screen.hide( str(CurrentHUD)+"TopCityPanelLeft" )
		screen.hide( str(CurrentHUD)+"TopCityPanelRight" )
		screen.hide( str(CurrentHUD)+"CityScreenAdjustPanel" )
		screen.hide( str(CurrentHUD)+"InterfaceCityLeftBackgroundWidget" )
		screen.hide( str(CurrentHUD)+"InterfaceLeftBackgroundWidget" )
		screen.hide( str(CurrentHUD)+"InterfaceCityCenterBackgroundWidget" )
		screen.hide( str(CurrentHUD)+"InterfaceCenterBackgroundWidget" )
		screen.hide( str(CurrentHUD)+"InterfaceCityRightBackgroundWidget" )
		screen.hide( str(CurrentHUD)+"InterfaceRightBackgroundWidget" )
		screen.hide( str(CurrentHUD)+"InterfaceTopLeft" )
		screen.hide( str(CurrentHUD)+"InterfaceTopCenter" )
		screen.hide( str(CurrentHUD)+"InterfaceTopRight" )
		screen.hide( str(CurrentHUD) + "MainExtra1" )
		screen.hide( str(CurrentHUD) + "CityExtra1" )

		screen.hide( "GreatPersonBar" )
		screen.hide( "GreatPersonBarText" )
		screen.hide( "EmergentLeaderXPBar" )
		screen.hide( "EmergentLeaderXPLbl" )
		screen.hide( "RawManaButton1" )
		for szBonus in strategicTypes1:
			szName = "StrategicText" + szBonus
			screen.hide( szName )
		for szBonus in strategicTypes2:
			szName = "StrategicText" + szBonus
			screen.hide( szName )
		for szBonus in manaTypes1:
			szName = "ManaText" + szBonus
			screen.hide( szName )
		for szBonus in manaTypes2:
			szName = "ManaText" + szBonus
			screen.hide( szName )
		for szBonus in luxuryTypes1:
			szName = "LuxuryText" + szBonus
			screen.hide( szName )
		for szBonus in luxuryTypes2:
			szName = "LuxuryText" + szBonus
			screen.hide( szName )
		for szBonus in healthTypes1:
			szName = "HealthText" + szBonus
			screen.hide( szName )
		for szBonus in healthTypes2:
			szName = "HealthText" + szBonus
			screen.hide( szName )
		screen.hide( "xUPTButton" )
		screen.hide( "GuildButton" )
		screen.hide( "UnitStatsButton1" )
		screen.hide( "TurnLogButton" )
		screen.hide( "EspionageAdvisorButton" )
		screen.hide( "DomesticAdvisorButton" )
		screen.hide( "ForeignAdvisorButton" )
		screen.hide( "TechAdvisorButton" )
		screen.hide( "CivicsAdvisorButton" )
		screen.hide( "ReligiousAdvisorButton" )
		screen.hide( "SomniumButton" )
		screen.hide( "FinanceAdvisorButton" )
		screen.hide( "MilitaryAdvisorButton" )
		screen.hide( "VictoryAdvisorButton" )
		screen.hide( "InfoAdvisorButton" )
# DynTraits Start
		#if (not gc.isNoCrash()):
		screen.hide( "TraitButton" )
# DynTraits End
		screen.hide( "MiniMapPanel" )
		screen.hide( "Bob" )
		screen.hide( "ACIcon" )
		screen.hide( "TrophyButton" )

		screen.moveToFront( "TurnLogButton" )
		screen.moveToFront( "EspionageAdvisorButton" )
		screen.moveToFront( "DomesticAdvisorButton" )
		screen.moveToFront( "ForeignAdvisorButton" )
		screen.moveToFront( "TechAdvisorButton" )
		screen.moveToFront( "CivicsAdvisorButton" )
		screen.moveToFront( "ReligiousAdvisorButton" )
		screen.moveToFront( "SomniumButton" )
		screen.moveToFront( "FinanceAdvisorButton" )
		screen.moveToFront( "MilitaryAdvisorButton" )
		screen.moveToFront( "VictoryAdvisorButton" )
		screen.moveToFront( "InfoAdvisorButton" )
		screen.moveToFront( "TrophyButton" )
		screen.moveToFront( "GuildButton" )

	def CityHUD( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		global CurrentHUD
		screen.show( str(CurrentHUD) + "InterfaceTopRightBackgroundWidget" )
		screen.show( str(CurrentHUD) + "CityNameBackground" )
		screen.show( str(CurrentHUD) + "CityScreenTopWidget" )
		screen.show( str(CurrentHUD) + "InterfaceCenterRightBackgroundWidget" )
		screen.show( str(CurrentHUD) + "InterfaceCenterLeftBackgroundWidget" )
		screen.show( str(CurrentHUD) + "InterfaceTopLeftBackgroundWidget" )
		screen.show( str(CurrentHUD) + "TopCityPanelRight" )
		screen.show( str(CurrentHUD) + "TopCityPanelLeft" )
		screen.show( str(CurrentHUD) + "CityScreenAdjustPanel" )
		screen.show( str(CurrentHUD) + "InterfaceCityLeftBackgroundWidget" )
		screen.show( str(CurrentHUD) + "InterfaceTopBackgroundWidget" )
		screen.show( str(CurrentHUD) + "InterfaceCityCenterBackgroundWidget" )
		screen.show( str(CurrentHUD) + "InterfaceCityRightBackgroundWidget" )
		screen.show( str(CurrentHUD) + "CityExtra1" )
		screen.show( "MiniMapPanel" )
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		pTeam = gc.getTeam(pPlayer.getTeam())
		global ishowManaBar
		global isformershowManaBar 
		if ishowManaBar !=0 :
			isformershowManaBar = ishowManaBar
		ishowManaBar = 0
		self.updateManaStrings()
		screen.hide("ManaBackground")
		
	def MainHUD( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		global CurrentHUD
		if (CyInterface().getHeadSelectedCity()):
			screen.show( str(CurrentHUD) + "InterfaceCityLeftBackgroundWidget" )
			screen.show( str(CurrentHUD) + "InterfaceCityCenterBackgroundWidget" )
			screen.show( str(CurrentHUD) + "InterfaceCityRightBackgroundWidget" )
		else:
			screen.show( str(CurrentHUD) + "InterfaceLeftBackgroundWidget" )
			screen.show( str(CurrentHUD) + "InterfaceCenterBackgroundWidget" )
			screen.show( str(CurrentHUD) + "InterfaceRightBackgroundWidget" )
		screen.show( str(CurrentHUD) + "InterfaceTopBackgroundWidget" )
		screen.show( str(CurrentHUD) + "InterfaceTopLeft" )
		screen.show( str(CurrentHUD) + "InterfaceTopCenter" )
		screen.show( str(CurrentHUD) + "InterfaceTopRight" )
		screen.show( str(CurrentHUD) + "MainExtra1" )
		screen.show( "MiniMapPanel" )
		screen.show( "ACIcon" )
	##	screen.show( "ManaBackground" )
	##  self.showArchosBroodActivityBackground()
		global ishowManaBar
		global isformershowManaBar
		ishowManaBar = isformershowManaBar
		self.updateManaStrings()

		self.ShowButtons()
		if gg.isModOption(g_UnitStatistics):
			screen.show( "UnitStatsButton1" )
		#if (not gc.isNoCrash()):
		screen.show( "TraitButton" ) # DynTraits interface - anw 7th/X/2011
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		pTeam = gc.getTeam(pPlayer.getTeam())

	def PartialHUD( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		global CurrentHUD
		screen.show( str(CurrentHUD) + "InterfaceTopBackgroundWidget" )
		screen.show( str(CurrentHUD) + "InterfaceTopCenter" )
		self.ShowButtons()

	def GlobeView( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		global CurrentHUD
		screen.show( str(CurrentHUD) + "InterfaceRightBackgroundWidget" )
		screen.show( str(CurrentHUD) + "InterfaceTopLeft" )
		screen.show( str(CurrentHUD) + "InterfaceTopCenter" )
		screen.show( str(CurrentHUD) + "InterfaceTopRight" )
		screen.show( "MiniMapPanel" )
		screen.show( "ACIcon" )
		self.ShowButtons()

	def AdvancedStartHUD( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.show( "MiniMapPanel" )

	def ShowButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.show( "TurnLogButton" )
		screen.show( "EspionageAdvisorButton" )
		screen.show( "DomesticAdvisorButton" )
		screen.show( "ForeignAdvisorButton" )
		screen.show( "TechAdvisorButton" )
		screen.show( "CivicsAdvisorButton" )
		screen.show( "ReligiousAdvisorButton" )
		screen.show( "SomniumButton" )
		screen.show( "GuildButton" )
		screen.show( "FinanceAdvisorButton" )
		screen.show( "MilitaryAdvisorButton" )
		screen.show( "VictoryAdvisorButton" )
		screen.show( "InfoAdvisorButton" )
# DynTraits Start
		#if (not gc.isNoCrash()):
		screen.show( "TraitButton" )
# DynTraits End
		screen.show( "RawManaButton1" )
		screen.show( "xUPTButton" )
		screen.show( "TrophyButton" )
		self.updateGreatPersonBar(screen)
		if not gc.isNoCrash():
	
			self.updateEmergentLeaderXPBar(screen)
	#Xienwolf Religious HUDs Add End

	# Update plot List Buttons
	def updatePlotListButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		global g_iSlaveColumnHeight
		global g_iSlaveRowLength

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bHandled = False
		if ( CyInterface().shouldDisplayUnitModel() and CyEngine().isGlobeviewUp() == false and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL ):
			if ( CyInterface().isCitySelection() ):

				iOrders = CyInterface().getNumOrdersQueued()

				for i in xrange( iOrders ):
					if ( bHandled == False ):
						eOrderNodeType = CyInterface().getOrderNodeType(i)
						if (eOrderNodeType  == OrderTypes.ORDER_TRAIN ):

#FfH: Modified by Kael 07/18/2008
#							screen.addUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 1, False )
							screen.addUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 115, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 1, False )
#FfH: End Modify

							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_CONSTRUCT ):

#FfH: Modified by Kael 07/18/2008
#							screen.addBuildingGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 0.8, False )
							screen.addBuildingGraphicGFC( "InterfaceUnitModel", CyInterface().getOrderNodeData1(i), 115, yResolution - 138, 123, 132, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1,  -20, 30, 0.8, False )
#FfH: End Modify

							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_CREATE ):
							if(gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).isSpaceship()):
								modelType = 0

#FfH: Modified by Kael 07/18/2008
#								screen.addSpaceShipWidgetGFC("InterfaceUnitModel", 175, yResolution - 138, 123, 132, CyInterface().getOrderNodeData1(i), modelType, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1)
								screen.addSpaceShipWidgetGFC("InterfaceUnitModel", 115, yResolution - 138, 123, 132, CyInterface().getOrderNodeData1(i), modelType, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1)
#FfH: End Modify

							else:
								screen.hide( "InterfaceUnitModel" )
							bHandled = True
						elif ( eOrderNodeType == OrderTypes.ORDER_MAINTAIN ):
							screen.hide( "InterfaceUnitModel" )
							bHandled = True

				if ( not bHandled ):
					screen.hide( "InterfaceUnitModel" )
					bHandled = True

				screen.moveToFront("SelectedCityText")

			elif ( CyInterface().getHeadSelectedUnit() ):
				if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
#FfH: Modified by Kael 07/17/2008
#				screen.addSpecificUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit(), 175, yResolution - 138, 123, 132, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )
#					screen.addSpecificUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit(), -20, yResolution - 350, 160, 198, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )	Changed r364
					screen.addSpecificUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit(), -20, yResolution - 374, 160, 198, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )
#FfH: End Modify
				else:
					screen.addSpecificUnitGraphicGFC( "InterfaceUnitModel", CyInterface().getHeadSelectedUnit(), -20, yResolution - 200, 160, 198, WidgetTypes.WIDGET_UNIT_MODEL, CyInterface().getHeadSelectedUnit().getUnitType(), -1,  -20, 30, 1, False )
				screen.moveToFront("SelectedUnitText")
				screen.moveToFront("PromotionScrollMinus")
				screen.moveToFront("PromotionScrollPlus")
				for i in xrange(iPromotionsPerPage):
					szName	= "PromotionButton" + str(i)
					szName2 = szName + "Duration"
					szName3 = szName + "Quantity"
					screen.moveToFront(szName)
					screen.moveToFront(szName2)
					screen.moveToFront(szName3)
				screen.moveToBack( "InterfaceUnitModel" )
			else:
				screen.hide( "InterfaceUnitModel" )
		else:
			screen.hide( "InterfaceUnitModel" )

		pPlot = CyInterface().getSelectionPlot()

#	Movement lag fix, caught by Snarko
#
#		for i in xrange(gc.getNumPromotionInfos()):
#			szName = "PromotionButton" + str(i)
#			szName2 = szName + "Duration"
#			szName3 = szName + "Quantity"
#			screen.moveToFront( szName )
#			screen.moveToFront( szName2 )
#			screen.moveToFront( szName3 )

		screen.hide( "PlotListMinus" )
		screen.hide( "PlotListPlus" )

		for j in xrange(gc.getMAX_PLOT_LIST_ROWS()):
			#szStringPanel = "PlotListPanel" + str(j)
			#screen.hide(szStringPanel)

			for i in xrange(self.numPlotListButtons()):
				szString = "PlotListButton" + str(j*self.numPlotListButtons()+i)
				screen.hide( szString )

				szStringHealth = szString + "Health"
				screen.hide( szStringHealth )

				szStringStealth = szString + "Stealth"
				screen.hide( szStringStealth )

				szStringIcon = szString + "Icon"
				screen.hide( szStringIcon )

#Slave/Master List Buttons Begin
		for u in xrange(2):
			if (u == 0):
				Add = ""
			else:
				Add = "Bottom"

			for j in xrange(g_iSlaveColumnHeight):
				#szStringPanel = "PlotListPanel" + str(j)
				#screen.hide(szStringPanel)

				for i in xrange(g_iSlaveRowLength):
					szString = str(Add) + "SlaveListButton" + str(j*g_iSlaveRowLength+i)
					screen.hide( szString )

					szStringHealth = szString + "Health"
					screen.hide( szStringHealth )

					szStringStealth = szString + "Stealth"
					screen.hide( szStringStealth )

					szStringIcon = szString + "Icon"
					screen.hide( szStringIcon )

					szString = str(Add) + "MinionListButton" + str(j*g_iSlaveRowLength+i)
					screen.hide( szString )

					szStringHealth = szString + "Health"
					screen.hide( szStringHealth )

					szStringStealth = szString + "Stealth"
					screen.hide( szStringStealth )

					szStringIcon = szString + "Icon"
					screen.hide( szStringIcon )

			szString = str(Add) + "MasterUnitButton"
			screen.hide( szString )

			szStringHealth = szString + "Health"
			screen.hide( szStringHealth )

			szStringStealth = szString + "Stealth"
			screen.hide( szStringStealth )

			szStringIcon = szString + "Icon"
			screen.hide( szStringIcon )

			szString = str(Add) + "CommanderUnitButton"
			screen.hide( szString )

			szStringHealth = szString + "Health"
			screen.hide( szStringHealth )

			szStringStealth = szString + "Stealth"
			screen.hide( szStringStealth )

			szStringIcon = szString + "Icon"
			screen.hide( szStringIcon )
#Slave/Master List Buttons End
		if ( pPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyEngine().isGlobeviewUp() == False):

			iVisibleUnits = CyInterface().getNumVisibleUnits()
			iCount = -(CyInterface().getPlotListColumn())

			bLeftArrow = False
			bRightArrow = False

			if (CyInterface().isCityScreenUp()):
				iMaxRows = 1
				iSkipped = (gc.getMAX_PLOT_LIST_ROWS() - 1) * self.numPlotListButtons()
				iCount += iSkipped
			else:
#Slave/Master List Buttons Begin
				if ( CyInterface().getHeadSelectedUnit() ):
					self.updateSlaveButtons()
#Slave/Master List Buttons End
				iMaxRows = gc.getMAX_PLOT_LIST_ROWS()
				iCount += CyInterface().getPlotListOffset()
				iSkipped = 0

			CyInterface().cacheInterfacePlotUnits(pPlot)
			for i in xrange(CyInterface().getNumCachedInterfacePlotUnits()):
				pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
				if (pLoopUnit):

					if ((iCount == 0) and (CyInterface().getPlotListColumn() > 0)):
						bLeftArrow = True
					elif ((iCount == (gc.getMAX_PLOT_LIST_ROWS() * self.numPlotListButtons() - 1)) and ((iVisibleUnits - iCount - CyInterface().getPlotListColumn() + iSkipped) > 1)):
						bRightArrow = True

					if ((iCount >= 0) and (iCount <  self.numPlotListButtons() * gc.getMAX_PLOT_LIST_ROWS())):
						if ((pLoopUnit.getTeam() != gc.getGame().getActiveTeam()) or pLoopUnit.isWaiting()):
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()

						elif (pLoopUnit.canMove()):
							if (pLoopUnit.hasMoved()):
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
							else:
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
						else:
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

						szString = "PlotListButton" + str(iCount)
						screen.changeImageButton( szString, pLoopUnit.getButton() )
						if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
							bEnable = True
						else:
							bEnable = False
						screen.enable(szString, bEnable)

						if (pLoopUnit.IsSelected()):
							screen.setState(szString, True)
						else:
							screen.setState(szString, False)
						screen.show( szString )

						# place the health bar
						if (pLoopUnit.isFighting()):
							bShowHealth = False
						elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
							bShowHealth = pLoopUnit.canAirAttack()
						else:
							bShowHealth = pLoopUnit.canFight()

						if bShowHealth:
							szStringHealth = szString + "Health"
							screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
							if (pLoopUnit.getDamageReal() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_RED"))
							elif (pLoopUnit.getDamageReal() >= (pLoopUnit.maxHitPoints() / 3)):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_YELLOW"))
							else:
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString("COLOR_GREEN"))
							screen.show( szStringHealth )

						if pLoopUnit.isRevealed():
							szStringStealth = szString + "Stealth"
							if pLoopUnit.IsSelected():
								szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED_SELECTED").getPath()
								screen.changeDDSGFC( szStringStealth, szPromoFileName )
							screen.show( szStringStealth )
						elif pLoopUnit.isPromotionReady():
#						if pLoopUnit.isPromotionReady(): # Swap with 4 lines above
							szStringStealth = szString + "Stealth"
							szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION").getPath()
							screen.changeDDSGFC( szStringStealth, szPromoFileName )
							if pLoopUnit.IsSelected():
								szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_SELECTED").getPath()
								screen.changeDDSGFC( szStringStealth, szPromoFileName )
							screen.show( szStringStealth )

						# Adds the overlay first
						szStringIcon = szString + "Icon"
						screen.changeDDSGFC( szStringIcon, szFileName )
						screen.show( szStringIcon )

					iCount = iCount + 1

			if (iVisibleUnits > self.numPlotListButtons() * iMaxRows):
				screen.enable("PlotListMinus", bLeftArrow)
				screen.show( "PlotListMinus" )

				screen.enable("PlotListPlus", bRightArrow)
				screen.show( "PlotListPlus" )

		return 0

	# This will update the flag widget for SP hotseat and dbeugging
	def updateFlag( self ):

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START ):
			screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
			xResolution = screen.getXResolution()
			yResolution = screen.getYResolution()

#FfH: Modified by Kael 07/17/2008
#			screen.addFlagWidgetGFC( "CivilizationFlag", xResolution - 288, yResolution - 138, 68, 250, gc.getGame().getActivePlayer(), WidgetTypes.WIDGET_FLAG, gc.getGame().getActivePlayer(), -1)
			screen.addFlagWidgetGFC( "CivilizationFlag", 0, -20, 68, 250, gc.getGame().getActivePlayer(), WidgetTypes.WIDGET_FLAG, gc.getGame().getActivePlayer(), -1)
#FfH: End Modify

	# Will hide and show the selection buttons and their associated buttons
	def updateSelectionButtons( self ):

		global SELECTION_BUTTON_COLUMNS
		global MAX_SELECTION_BUTTONS
		global g_pSelectedUnit

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()

		global g_NumEmphasizeInfos
		global g_NumCityTabTypes
		global g_NumHurryInfos
		global g_NumUnitClassInfos
		global g_NumBuildingClassInfos
		global g_NumProjectInfos
		global g_NumProcessInfos
		global g_NumActionInfos

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

#FfH: Modified by Kael 07/18/2008
#		screen.addMultiListControlGFC( "BottomButtonContainer", u"", iMultiListXL, yResolution - 113, xResolution - (iMultiListXL+iMultiListXR), 100, 4, 48, 48, TableStyles.TABLE_STYLE_STANDARD )
#		screen.clearMultiList( "BottomButtonContainer" )
#		screen.hide( "BottomButtonContainer" )

# High Res stuff - Modified by Grey Fox 03/29/2010

# City Actions - START: Added by Grey Fox 03/28/2010
		iCityActionWidth = 124
# City Actions - END
		if (not CyEngine().isGlobeviewUp() and pHeadSelectedCity):
			iDefaultWidth 	= xResolution - (iMultiListXL+iMultiListXR) -90
			iMultiListW 	= iDefaultWidth-(iCityActionWidth+5)

		else:
			iDefaultWidth 	= xResolution - (iMultiListXL+iMultiListXR)
			iMultiListW		= iDefaultWidth

		iBtn 		= 48
		iY			= yResolution - 113
		iHeight		= 100
		if self.isHighResolution():
			iBtn	= 64
			iY		= yResolution - g_iVeryHighY
			iHeight	= 132
		szName1			= "BottomButtonContainer"
		szName2			= "BottomButtonContainer2"
		szName3			= "BottomButtonContainer3"
		szlabl1			= "BottomButtonContainer_Label"
		szlabl2			= "BottomButtonContainer2_Label"
		szlabl3			= "BottomButtonContainer3_Label"
		eFont			= FontTypes.SMALL_FONT
		eFontJustify	= CvUtil.FONT_CENTER_JUSTIFY
		eTableStyle		= TableStyles.TABLE_STYLE_STANDARD
		eWidget			= WidgetTypes.WIDGET_GENERAL
		iFirstX 		= iMultiListXL + 5
		iFontY			= yResolution - 130
		iWidth  		= iDefaultWidth / 120
		iFirstWidth 	= iWidth * 40 -5
		iThirdWidth 	= 148
		iSecndWidth 	= iDefaultWidth - (iFirstWidth + iThirdWidth + iCityActionWidth + 25)
		iSecndX			= iFirstX + iFirstWidth + 5
		iThirdX			= iSecndX + iSecndWidth + 5
		szFirst			= "Units"
		szSecnd			= "Buildings"
		szThird			= "Wonders & Projects"
		addMultiList	= screen.addMultiListControlGFC
		setLabel		= screen.setLabel

		if self.isHighResolution():
			# First
			addMultiList( szName1, u"", iFirstX, iY, 	iFirstWidth, 	iHeight, 4, iBtn, iBtn, eTableStyle )
			#setLabel	( szlabl1, "Background", szFirst, 	eFontJustify, iFirstX + 24, iFontY, -0.1, eFont, eWidget, -1, -1 )
			# Second
			addMultiList( szName2, u"", iSecndX, iY, 	iSecndWidth, 	iHeight, 4, iBtn, iBtn, eTableStyle )
			#setLabel	( szlabl2, "Background", szSecnd, 	eFontJustify, iSecndX + 29, iFontY, -0.1, eFont, eWidget, -1, -1 )
			# Third
			addMultiList( szName3, u"", iThirdX, iY,	iThirdWidth, 	iHeight, 4, iBtn, iBtn, eTableStyle )
			#setLabel	( szlabl3, "Background", szThird, 	eFontJustify, iThirdX + 29, iFontY, -0.1, eFont, eWidget, -1, -1 )
		else:
			addMultiList( szName1, u"", iFirstX, iY, 	iMultiListW, 	iHeight, 4, iBtn, iBtn, eTableStyle )
# High Res stuff - End Modify

# City Actions - START: Added by Grey Fox 03/28/2010
		iCityActionX = xResolution - 445
		screen.addMultiListControlGFC( "CityActionsButtonContainer", u"", iCityActionX, yResolution - 113, iCityActionWidth, 100, 4, 48, 48, TableStyles.TABLE_STYLE_STANDARD )
		screen.setLabel( "CityActionsLabel", "Background", localText.getText("TXT_KEY_CITY_ACTIONS", ()), CvUtil.FONT_CENTER_JUSTIFY, iCityActionX +48, yResolution - 130, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.clearMultiList( "CityActionsButtonContainer" )
		screen.hide( "CityActionsButtonContainer" )
		screen.hide( "CityActionsLabel" )
# City Actions - END

		screen.clearMultiList( "BottomButtonContainer" )
		screen.hide( "BottomButtonContainer" )

# High Res stuff - Added by Grey Fox 03/29/2010
		screen.hide( "BottomButtonContainer2" )
		screen.hide( "BottomButtonContainer3" )
		screen.hide( "BottomButtonContainer_Label" )
		screen.hide( "BottomButtonContainer2_Label" )
		screen.hide( "BottomButtonContainer3_Label" )
# High Res stuff - End Add

#FfH: End Modify

		# All of the hides...
		self.setMinimapButtonVisibility(False)

		screen.hideList( 0 )

		for i in xrange (g_NumEmphasizeInfos):
			szButtonID = "Emphasize" + str(i)
			screen.hide( szButtonID )

		# Hurry button show...
		for i in xrange( g_NumHurryInfos ):
			szButtonID = "Hurry" + str(i)
			screen.hide( szButtonID )

		# Conscript Button Show
		screen.hide( "Conscript" )
		#screen.hide( "Liberate" )
		screen.hide( "AutomateProduction" )
		screen.hide( "AutomateCitizens" )

		if (not CyEngine().isGlobeviewUp() and pHeadSelectedCity):

			self.setMinimapButtonVisibility(True)

			if ((pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer()) or gc.getGame().isDebugMode()):

				iBtnX = xResolution - 284
				iBtnY = yResolution - 177
				iBtnW = 64
				iBtnH = 30

				# Liberate button
				#szText = "<font=1>" + localText.getText("TXT_KEY_LIBERATE_CITY", ()) + "</font>"
				#screen.setButtonGFC( "Liberate", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_LIBERATE_CITY, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				#screen.setStyle( "Liberate", "Button_CityT1_Style" )
				#screen.hide( "Liberate" )

#FfH: Modified by Kael 07/18/2008
#				iBtnSX = xResolution - 284
				iBtnSX = xResolution - 296
#FfH: End Modify

				iBtnX = iBtnSX
				iBtnY = yResolution - 140
				iBtnW = 64
				iBtnH = 30

				# Conscript button
				szText = "<font=1>" + localText.getText("TXT_KEY_DRAFT", ()) + "</font>"
				screen.setButtonGFC( "Conscript", szText, "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_CONSCRIPT, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Conscript", "Button_CityT1_Style" )
				screen.hide( "Conscript" )

				iBtnY += iBtnH
				iBtnW = 21
				iBtnH = 24

				# Hurry Buttons
				screen.setButtonGFC( "Hurry0", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 0, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry0", "Button_CityC1_Style" )
				screen.hide( "Hurry0" )

				iBtnX += iBtnW

				screen.setButtonGFC( "Hurry1", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry1", "Button_CityC2_Style" )
				screen.hide( "Hurry1" )

				iBtnX += iBtnW

				screen.setButtonGFC( "Hurry2", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_HURRY, 2, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "Hurry2", "Button_CityC1_Style" )
				screen.hide( "Hurry2" )

				iBtnX = iBtnSX
				iBtnY += iBtnH
				iBtnW = 32
				iBtnH = 28

				# Automate Production Button
				screen.addCheckBoxGFC( "AutomateProduction", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_PRODUCTION, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "AutomateProduction", "Button_CityC3_Style" )

				iBtnX += iBtnW

				# Automate Citizens Button
				screen.addCheckBoxGFC( "AutomateCitizens", "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_AUTOMATE_CITIZENS, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
				screen.setStyle( "AutomateCitizens", "Button_CityC4_Style" )

				iBtnY += iBtnH
				iBtnX = iBtnSX

				iBtnW	= 22
				iBtnWa	= 20
				iBtnH	= 24
				iBtnHa	= 27

				# Set Emphasize buttons
				i = 0
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnH, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				iBtnY += iBtnH

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW, iBtnY, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", iBtnX+iBtnW+iBtnWa, iBtnY, iBtnW, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i+1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				# FF: Added by Jean Elcard 11/15/2008 (set up growth control buttons)
				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", xResolution - HUD_City_Growth_Panel_Width_Exclusion - iBtnWa, iCityCenterRow2Y, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )

				i+=1
				szButtonID = "Emphasize" + str(i)
				screen.addCheckBoxGFC( szButtonID, "", "", xResolution - HUD_City_Growth_Panel_Width_Exclusion - iBtnWa, iCityCenterRow1Y, iBtnWa, iBtnHa, WidgetTypes.WIDGET_EMPHASIZE, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				szStyle = "Button_CityB" + str(i-1) + "_Style"
				screen.setStyle( szButtonID, szStyle )
				screen.hide( szButtonID )
				# FF: End Add

				g_pSelectedUnit = 0
				screen.setState( "AutomateCitizens", pHeadSelectedCity.isCitizensAutomated() )
				screen.setState( "AutomateProduction", pHeadSelectedCity.isProductionAutomated() )

				# FF: Added by Jean Elcard 11/15/2008
				iNumCustomEmphasizeInfos = 2
				# FF: End Add

				for i in xrange (g_NumEmphasizeInfos):
					# FF: Added by Jean Elcard 11/15/2008 (don't show buttons if city screen isn't up)
					if (i < g_NumEmphasizeInfos - iNumCustomEmphasizeInfos or CyInterface().isCityScreenUp()) and not (i >= g_NumEmphasizeInfos - iNumCustomEmphasizeInfos and gc.getPlayer(pHeadSelectedCity.getOwner()).isIgnoreFood()):
						# FF: End Add
						szButtonID = "Emphasize" + str(i)
						screen.show( szButtonID )
						if ( pHeadSelectedCity.AI_isEmphasize(i) ):
							screen.setState( szButtonID, True )
						else:
							screen.setState( szButtonID, False )

				# City Tabs
				for i in xrange( g_NumCityTabTypes ):
					szButtonID = "CityTab" + str(i)
					screen.show( szButtonID )

				# Hurry button show...
				for i in xrange( g_NumHurryInfos ):
					szButtonID = "Hurry" + str(i)
					screen.show( szButtonID )
					screen.enable( szButtonID, pHeadSelectedCity.canHurry(i, False) )

				# Conscript Button Show
				screen.show( "Conscript" )
				if (pHeadSelectedCity.canConscript()):
					screen.enable( "Conscript", True )
				else:
					screen.enable( "Conscript", False )

				# Liberate Button Show
				#screen.show( "Liberate" )
				#if (-1 != pHeadSelectedCity.getLiberationPlayer()):
				#	screen.enable( "Liberate", True )
				#else:
				#	screen.enable( "Liberate", False )

# City Actions - START: Added by Grey Fox 03/28/2010

				iCount = 0
				# City Actions (Spells) available
				iSelectedCount = 0
				pPlayer = gc.getPlayer(pHeadSelectedCity.getOwner())
				(loopCity,iter)= pPlayer.firstCity(False)
				while(loopCity):
					if CyInterface().isCitySelected(loopCity):
						iSelectedCount+=1
					(loopCity,iter)=pPlayer.nextCity(iter,False)
		#		for iCity in xrange (pPlayer.getNumCities()):
		#			pCity = pPlayer.getCity(iCity)
		#			if CyInterface().isCitySelected(pCity):
		#				iSelectedCount += 1
				if iSelectedCount == 1:
					for i in xrange ( gc.getNumSpellInfos() ):

						if pHeadSelectedCity.canCast(i, True):
							szButton = gc.getSpellInfo(i).getButton()

							screen.appendMultiListButton( "CityActionsButtonContainer", szButton, 0, WidgetTypes.WIDGET_CITY_ACTION, i, -1, False )
							screen.show( "CityActionsButtonContainer" )
							screen.show( "CityActionsLabel" )

							if not pHeadSelectedCity.canCast(i, False):
								screen.disableMultiListButton( "CityActionsButtonContainer", 0, iCount, szButton)

							iCount = iCount + 1

# City Actions - END

				iCount = 0
				iRow = 0
				bFound = False

				# Units to construct
				addedunitlist=[]
				for i in xrange ( g_NumUnitClassInfos ):
					eLoopUnit = pHeadSelectedCity.getCityUnits(i)

#FfH: Added by Kael 10/05/2007
					if (eLoopUnit != -1) and(eLoopUnit not in addedunitlist):
#FfH: End Add			
						
						if (pHeadSelectedCity.canTrain(eLoopUnit, False, True)):
							szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)
							addedunitlist.append(eLoopUnit)
#FfH: Added by Kael 02/06/2009
							iProm = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getDefaultRace()
							if iProm != -1:
								szButton = gc.getUnitInfo(eLoopUnit).getUnitStyleButton(iProm)
#FfH: End Add

							screen.appendMultiListButton( "BottomButtonContainer", szButton, iRow, WidgetTypes.WIDGET_TRAIN, i, -1, False )
							screen.show( "BottomButtonContainer" )

							if ( not pHeadSelectedCity.canTrain(eLoopUnit, False, False) ):
								screen.disableMultiListButton( "BottomButtonContainer", iRow, iCount, szButton)

							iCount = iCount + 1
							bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

# High Res stuff - Added by Grey Fox 03/29/2010
				eMultiList = "BottomButtonContainer"
				if self.isHighResolution():
					iRow = 0
					eMultiList = "BottomButtonContainer2"
# High Res stuff - End Add

				# Buildings to construct
				for i in xrange ( g_NumBuildingClassInfos ):
					if (not isLimitedWonderClass(i)):
						eLoopBuilding = pHeadSelectedCity.getCityBuildings(i)

						if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
# High Res stuff - Modified by Grey Fox 03/29/2010
							screen.appendMultiListButton( eMultiList, gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
							screen.show( eMultiList )

							if ( not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False) ):
								screen.disableMultiListButton( eMultiList, iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton() )
# High Res stuff - End Modify
							iCount = iCount + 1
							bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

# High Res stuff - Added by Grey Fox 03/29/2010
				eMultiList = "BottomButtonContainer"
				if self.isHighResolution():
					iRow = 0
					eMultiList = "BottomButtonContainer3"
# High Res stuff - End Add

				# Wonders to construct
				i = 0
				for i in xrange( g_NumBuildingClassInfos ):
					if (isLimitedWonderClass(i)):
						eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)

						if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
# High Res stuff - Modified by Grey Fox 03/29/2010
							screen.appendMultiListButton( eMultiList, gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
							screen.show( eMultiList )

							if ( not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False) ):
								screen.disableMultiListButton( eMultiList, iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton() )
# High Res stuff - End Modify
							iCount = iCount + 1
							bFound = True

				iCount = 0
				if (bFound):
					iRow = iRow + 1
				bFound = False

				# Projects
				i = 0
				for i in xrange( g_NumProjectInfos ):
					if (pHeadSelectedCity.canCreate(i, False, True)):
# High Res stuff - Modified by Grey Fox 03/29/2010
						screen.appendMultiListButton( eMultiList, gc.getProjectInfo(i).getButton(), iRow, WidgetTypes.WIDGET_CREATE, i, -1, False )
						screen.show( eMultiList )

						if ( not pHeadSelectedCity.canCreate(i, False, False) ):
							screen.disableMultiListButton( eMultiList, iRow, iCount, gc.getProjectInfo(i).getButton() )
# High Res stuff - End Modify
						iCount = iCount + 1
						bFound = True

				# Processes
				i = 0
				for i in xrange( g_NumProcessInfos ):
					if (pHeadSelectedCity.canMaintain(i, False)):
# High Res stuff - Modified by Grey Fox 03/29/2010
						screen.appendMultiListButton( eMultiList, gc.getProcessInfo(i).getButton(), iRow, WidgetTypes.WIDGET_MAINTAIN, i, -1, False )
						screen.show( eMultiList )

						iCount = iCount + 1
						bFound = True

				screen.selectMultiList( eMultiList, CyInterface().getCityTabSelectionRow() )
# High Res stuff - End Modify

		elif (not CyEngine().isGlobeviewUp() and pHeadSelectedUnit and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):

			self.setMinimapButtonVisibility(True)

			if (CyInterface().getInterfaceMode() == InterfaceModeTypes.INTERFACEMODE_SELECTION):

				if ( pHeadSelectedUnit.getOwner() == gc.getGame().getActivePlayer() and g_pSelectedUnit != pHeadSelectedUnit ):

					g_pSelectedUnit = pHeadSelectedUnit

					iCount = 0

# High Res stuff - Modified by Grey Fox 03/29/2010
					iCount1 = 0
					iCount2 = 0
					iCount3 = 0
					eMultiList = "BottomButtonContainer"
					getAction	= gc.getActionInfo
					iRow = 0
					bHighRezButtons = False
					if self.isHighResolution():
						bHighRezButtons = True

					actions = CyInterface().getActionsToShow()
					for i in actions:
						eCommandType = getAction(i).getCommandType()
						eMissionType = getAction(i).getMissionType()
#FfH: Modified by Kael 02/07/2009
#						screen.appendMultiListButton( "BottomButtonContainer", gc.getActionInfo(i).getButton(), 0, WidgetTypes.WIDGET_ACTION, i, -1, False )
						szButton = getAction(i).getButton()
						if eCommandType	== CommandTypes.COMMAND_UPGRADE:
							iProm = gc.getCivilizationInfo(gc.getPlayer(pHeadSelectedUnit.getOwner()).getCivilizationType()).getDefaultRace()
							if iProm != -1:
								szButton = gc.getUnitInfo(getAction(i).getCommandData()).getUnitStyleButton(iProm)

						if bHighRezButtons:
							if   eCommandType	== CommandTypes.COMMAND_PROMOTION:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_PILLAGE_ROUTE:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_SENTRY:
								eMultiList = "BottomButtonContainer"
							elif eMissionType	== MissionTypes.MISSION_AIRSTRIKE:
								eMultiList = "BottomButtonContainer2"
							elif eCommandType	== CommandTypes.COMMAND_UPGRADE:
								eMultiList = "BottomButtonContainer2"
							elif eCommandType	== CommandTypes.COMMAND_AUTOMATE:
								eMultiList = "BottomButtonContainer"
							elif eCommandType	== CommandTypes.COMMAND_WAKE:
								eMultiList = "BottomButtonContainer"
							elif eCommandType	== CommandTypes.COMMAND_CANCEL:
								eMultiList = "BottomButtonContainer3"
						#	elif "Bombard" in szButton:
						#		eMultiList = "BottomButtonContainer2"
							elif eCommandType	== CommandTypes.COMMAND_CANCEL_ALL:
								eMultiList = "BottomButtonContainer3"
							elif eCommandType	== CommandTypes.COMMAND_STOP_AUTOMATION:
								eMultiList = "BottomButtonContainer"
							elif eCommandType	== CommandTypes.COMMAND_DELETE:
								eMultiList = "BottomButtonContainer"
							elif eCommandType	== CommandTypes.COMMAND_GIFT:
								eMultiList = "BottomButtonContainer3"
							elif eCommandType	== CommandTypes.COMMAND_LOAD:
								eMultiList = "BottomButtonContainer3"
							elif eCommandType	== CommandTypes.COMMAND_LOAD_UNIT:
								eMultiList = "BottomButtonContainer3"
							elif eCommandType	== CommandTypes.COMMAND_UNLOAD:
								eMultiList = "BottomButtonContainer3"
							elif eCommandType	== CommandTypes.COMMAND_UNLOAD_ALL:
								eMultiList = "BottomButtonContainer3"
							elif eCommandType	== CommandTypes.COMMAND_CAST:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_MOVE_TO:
								eMultiList = "BottomButtonContainer"
							elif eMissionType	== MissionTypes.MISSION_ROUTE_TO:
								eMultiList = "BottomButtonContainer"
							elif eMissionType	== MissionTypes.MISSION_SKIP:
								eMultiList = "BottomButtonContainer"
							elif eMissionType	== MissionTypes.MISSION_SLEEP:
								eMultiList = "BottomButtonContainer"
							elif eMissionType	== MissionTypes.MISSION_FORTIFY:
								eMultiList = "BottomButtonContainer"
							elif eMissionType	== MissionTypes.MISSION_PLUNDER:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_AIRPATROL:
								eMultiList = "BottomButtonContainer"
							elif eMissionType	== MissionTypes.MISSION_SEAPATROL:
								eMultiList = "BottomButtonContainer"
							elif eMissionType	== MissionTypes.MISSION_MULTI_DESELECT:
								eMultiList = "BottomButtonContainer"
							elif eMissionType	== MissionTypes.MISSION_HEAL:
								eMultiList = "BottomButtonContainer"
							elif eMissionType	== MissionTypes.MISSION_AIRLIFT:
								eMultiList = "BottomButtonContainer3"
							elif eMissionType	== MissionTypes.MISSION_NUKE:
								eMultiList = "BottomButtonContainer3"
							elif eMissionType	== MissionTypes.MISSION_RECON:
								eMultiList = "BottomButtonContainer3"
							elif eMissionType	== MissionTypes.MISSION_PARADROP:
								eMultiList = "BottomButtonContainer3"
							elif eMissionType	== MissionTypes.MISSION_BOMBARD:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_RANGE_ATTACK:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_PILLAGE:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_SABOTAGE:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_DESTROY:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_STEAL_PLANS:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_FOUND:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_SPREAD:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_SPREAD_CORPORATION:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_JOIN:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_CONSTRUCT:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_DISCOVER:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_HURRY:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_TRADE:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_GREAT_WORK:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_INFILTRATE:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_GOLDEN_AGE:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_BUILD:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_LEAD:
								eMultiList = "BottomButtonContainer2"
							elif eMissionType	== MissionTypes.MISSION_ESPIONAGE:
								eMultiList = "BottomButtonContainer2"
							else:
								eMultiList = "BottomButtonContainer"

						screen.appendMultiListButton( eMultiList, szButton, iRow, WidgetTypes.WIDGET_ACTION, i, -1, False )
#FfH: End Modify

						if eMultiList == "BottomButtonContainer":
							screen.show( "BottomButtonContainer" )
							iTheCount = iCount1
							iCount1 += 1
						elif eMultiList == "BottomButtonContainer2":
							screen.show( "BottomButtonContainer2" )
							iTheCount = iCount2
							iCount2 += 1
						elif eMultiList == "BottomButtonContainer3":
							screen.show( "BottomButtonContainer3" )
							iTheCount = iCount3
							iCount3 += 1

						if ( not CyInterface().canHandleAction(i, False) ):
							if bHighRezButtons:
								screen.disableMultiListButton( eMultiList, iRow, iTheCount, gc.getActionInfo(i).getButton() )
							else:
								screen.disableMultiListButton( eMultiList, iRow, iCount, gc.getActionInfo(i).getButton() )

						if ( pHeadSelectedUnit.isActionRecommended(i) ):#or gc.getActionInfo(i).getCommandType() == CommandTypes.COMMAND_PROMOTION ):

							if bHighRezButtons:
								screen.enableMultiListPulse( eMultiList, True, 0, iTheCount )
							else:
								screen.enableMultiListPulse( eMultiList, True, 0, iCount )
						else:
							if bHighRezButtons:
								screen.enableMultiListPulse( eMultiList, False, 0, iTheCount )
							else:
								screen.enableMultiListPulse( eMultiList, False, 0, iCount )

						iCount = iCount + 1

					if bHighRezButtons:
						eMultiList = "BottomButtonContainer3"
					if (CyInterface().canCreateGroup()):
						screen.appendMultiListButton( eMultiList, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CREATEGROUP").getPath(), 0, WidgetTypes.WIDGET_CREATE_GROUP, -1, -1, False )
						screen.show( eMultiList )

						iCount = iCount + 1

					if (CyInterface().canDeleteGroup()):
						screen.appendMultiListButton( eMultiList, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_SPLITGROUP").getPath(), 0, WidgetTypes.WIDGET_DELETE_GROUP, -1, -1, False )
						screen.show( eMultiList )

						iCount = iCount + 1
# < Mercenaries Start >	
					if (not gc.isNoCrash()):
						if(not self.repainting):
							self.repainting=true

							b=false

							
							# Show the contract out unit and fire mercenary buttons only if the player has at least one city and
							# and the current player era is at or beyond the configured starting era.
							if(gc.getActivePlayer().getNumCities() > 0 and gc.getGame().isUnlockMercenaries()):
								bCreateContract = true
										
							# If the require city unit contract creation and the unit is not in a city then
										# don't show the create contract button for the unit
							if(not g_pSelectedUnit.plot().isCity()):
								bCreateContract = false
								
							# Show the contract out unit button only if the selected unit can be contracted out and if the 
							# selected unit isn't already a mercenary.
							if(gc.getGame().isUnlockMercenaries() and g_pSelectedUnit.canContractOut() and bCreateContract):
								screen.appendMultiListButton( "BottomButtonContainer", "Art/Interface/Buttons/Actions/ContractOutUnit.dds", 0, WidgetTypes.WIDGET_CONTRACT_OUT, -1, -1, False )
								screen.show( "BottomButtonContainer" )
								iCount = iCount + 1
										
							# Show the fire mercenary button only if the selected unit information is a mercenary.
							if(gc.getGame().isUnlockMercenaries() and g_pSelectedUnit.isMercenary()):
								screen.appendMultiListButton( "BottomButtonContainer", "Art/Interface/Buttons/Actions/FireMercenary.dds", 0, WidgetTypes.WIDGET_FIRE_MERCENARY, -1, -1, False )
								screen.show( "BottomButtonContainer" )
								iCount = iCount + 1
								

							self.repainting=false						

						# < Mercenaries End >

# High Res stuff - End Modify

		elif (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):

			self.setMinimapButtonVisibility(True)

		return 0

	# Will update the research buttons
	def updateResearchButtons( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		for i in xrange( gc.getNumTechInfos() ):
			szName = "ResearchButton" + str(i)
			screen.hide( szName )

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		#screen.hide( "InterfaceOrnamentLeftLow" )
		#screen.hide( "InterfaceOrnamentRightLow" )

		for i in xrange(gc.getNumReligionInfos()):
			szName = "ReligionButton" + str(i)
			screen.hide( szName )

		i = 0
		if ( CyInterface().shouldShowResearchButtons() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			iCount = 0

			for i in xrange( gc.getNumTechInfos() ):
				if (gc.getActivePlayer().canResearch(i, False)):

#FfH: Modified by Karl 08/24/2007
#					if (iCount < 20):
					if (iCount < 30):
#FfH: End Modify

						szName = "ResearchButton" + str(i)

						bDone = False
						for j in xrange( gc.getNumReligionInfos() ):
							if ( not bDone ):
								if (gc.getReligionInfo(j).getTechPrereq() == i):
									if not (gc.getGame().isReligionSlotTaken(j)):
										szName = "ReligionButton" + str(j)
										bDone = True

						screen.show( szName )
						self.setResearchButtonPosition(szName, iCount)

					iCount = iCount + 1

		return 0

	# Will update the citizen buttons
	def updateCitizenButtons(self):

		global MAX_CITIZEN_BUTTONS

		bHandled = False

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		for i in xrange(MAX_CITIZEN_BUTTONS):
			szName = "FreeSpecialist" + str(i)
			screen.hide(szName)
			szName = "AngryCitizen" + str(i)
			screen.hide(szName)

		for i in xrange(gc.getNumSpecialistClassInfos()):
			szName = "IncreaseSpecialist" + str(i)
			screen.hide(szName)
			szName = "DecreaseSpecialist" + str(i)
			screen.hide(szName)
			szName = "CitizenDisabledButton" + str(i)
			screen.hide(szName)
			for j in xrange(MAX_CITIZEN_BUTTONS):
				szName = "CitizenButton" + str((i * 100) + j)
				screen.hide(szName)
				szName = "CitizenButtonHighlight" + str((i * 100) + j)
				screen.hide(szName)
			szName = "CitizenButtonBlock" + str(i)
			screen.hide(szName)

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if (CyInterface().isCityScreenUp()):
			if (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
				if (pHeadSelectedCity.angryPopulation(0) < MAX_CITIZEN_BUTTONS):
					iCount = pHeadSelectedCity.angryPopulation(0)
				else:
					iCount = MAX_CITIZEN_BUTTONS

				for i in xrange(iCount):
					bHandled = True
					szName = "AngryCitizen" + str(i)
					screen.show(szName)

				iFreeSpecialistCount = 0
				for i in xrange(gc.getNumSpecialistClassInfos()):
					iFreeSpecialistCount += pHeadSelectedCity.getFreeSpecialistClassCount(i)

				iCount = 0

				bHandled = False

				if (iFreeSpecialistCount > MAX_CITIZEN_BUTTONS):
					for i in xrange(gc.getNumSpecialistClassInfos()):
						if (pHeadSelectedCity.getFreeSpecialistClassCount(i) > 0):
							iSpecialist = pHeadSelectedCity.getSpecialistTypeFromClass(i)
							if (iCount < MAX_CITIZEN_BUTTONS):
								szName = "FreeSpecialist" + str(iCount)
								screen.setImageButton(szName, gc.getSpecialistInfo(iSpecialist).getTexture(),
													  (xResolution - 74 - (26 * iCount)), yResolution - 206, 24, 24,
													  WidgetTypes.WIDGET_FREE_CITIZEN, i, 1)
								screen.show(szName)
								bHandled = true
							iCount += 1

				else:
					for i in xrange(gc.getNumSpecialistClassInfos()):
						for j in xrange(pHeadSelectedCity.getFreeSpecialistClassCount(i)):
							iSpecialist = pHeadSelectedCity.getSpecialistTypeFromClass(i)
							if (iCount < MAX_CITIZEN_BUTTONS):
								szName = "FreeSpecialist" + str(iCount)
								screen.setImageButton(szName, gc.getSpecialistInfo(iSpecialist).getTexture(),
													  (xResolution - 74 - (26 * iCount)), yResolution - 206, 24, 24,
													  WidgetTypes.WIDGET_FREE_CITIZEN, i, -1)
								screen.show(szName)
								bHandled = true

							iCount = iCount + 1

				iButtonOffset = 0
				for i in xrange(gc.getNumSpecialistClassInfos()):
					iSpecialist = pHeadSelectedCity.getSpecialistTypeFromClass(i)
					bHandled = False
					if iSpecialist == -1:
						continue
					if not gc.getSpecialistInfo(iSpecialist).isVisible():
						continue
					if (pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer() or gc.getGame().isDebugMode()):

						if (pHeadSelectedCity.isCitizensAutomated()):
							iSpecialistCount = max(pHeadSelectedCity.getSpecialistClassCount(i),
												   pHeadSelectedCity.getForceSpecialistClassCount(i))
						else:
							iSpecialistCount = pHeadSelectedCity.getSpecialistClassCount(i)

						if ((pHeadSelectedCity.isSpecialistClassValid(i,1)
							 or pHeadSelectedCity.isSpecialistClassBlocked(i))
								and (pHeadSelectedCity.isCitizensAutomated() or iSpecialistCount < (
								pHeadSelectedCity.getPopulation() + pHeadSelectedCity.totalFreeSpecialists()))):
							szName = "IncreaseSpecialist" + str(i)
							screen.setButtonGFC(szName, u"", "", xResolution - 46,
												(yResolution - 270 - (26 * iButtonOffset)),
												20, 20, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, 1,
												ButtonStyles.BUTTON_STYLE_CITY_PLUS)
							screen.show(szName)
							szName = "CitizenDisabledButton" + str(i)
							screen.setImageButton(szName, gc.getSpecialistInfo(iSpecialist).getTexture(),
												  xResolution - 74,
												  (yResolution - 272 - (26 * iButtonOffset)), 24, 24,
												  WidgetTypes.WIDGET_DISABLED_CITIZEN, i, -1)
							screen.enable(szName, False)
							screen.show(szName)

						if iSpecialistCount > 0:
							szName = "CitizenDisabledButton" + str(i)
							screen.hide(szName)
						if iSpecialistCount > 0 or (
								not pHeadSelectedCity.isSpecialistClassBlocked(i) and i != gc.getInfoTypeForString(
								"SPECIALISTCLASS_CITIZEN")):
							szName = "DecreaseSpecialist" + str(i)
							screen.setButtonGFC(szName, u"", "", xResolution - 24,
												(yResolution - 270 - (26 * iButtonOffset)),
												20, 20, WidgetTypes.WIDGET_CHANGE_SPECIALIST, i, -1,
												ButtonStyles.BUTTON_STYLE_CITY_MINUS)
							screen.show(szName)

					if (pHeadSelectedCity.getSpecialistClassCount(i) < MAX_CITIZEN_BUTTONS):
						iCount = pHeadSelectedCity.getSpecialistClassCount(i)
					else:
						iCount = MAX_CITIZEN_BUTTONS

					j = 0
					for j in xrange(iCount):
						bHandled = True
						szName = "CitizenButton" + str((i * 100) + j)
						screen.addCheckBoxGFC(szName, gc.getSpecialistInfo(iSpecialist).getTexture(), "",
											  xResolution - 74 - (26 * j), (yResolution - 272 - (26 * iButtonOffset)),
											  24, 24, WidgetTypes.WIDGET_CITIZEN, i, j, ButtonStyles.BUTTON_STYLE_LABEL)
						screen.show(szName)
						szName = "CitizenButtonHighlight" + str((i * 100) + j)
						screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(),
										 xResolution - 74 - (26 * j), (yResolution - 272 - (26 * iButtonOffset)), 24,
										 24, WidgetTypes.WIDGET_CITIZEN, i, j)
						if (pHeadSelectedCity.getForceSpecialistClassCount(i) > j):
							screen.show(szName)
						else:
							screen.hide(szName)
					if pHeadSelectedCity.isSpecialistClassBlocked(i):
						szName = "CitizenButtonBlock" + str(i)
						screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED").getPath(),
										 xResolution - 74, (yResolution - 272 - (26 * iButtonOffset)), 24, 24,
										 WidgetTypes.WIDGET_CITIZEN, i, j)
						screen.show(szName)
					else:
						szName = "CitizenButtonBlock" + str(i)
						screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED").getPath(),
										 xResolution - 74, (yResolution - 272 - (26 * iButtonOffset)), 24, 24,
										 WidgetTypes.WIDGET_CITIZEN, i, j)
						screen.hide(szName)

					if (not bHandled):
						szName = "CitizenDisabledButton" + str(i)
						screen.setImageButton(szName, gc.getSpecialistInfo(iSpecialist).getTexture(), xResolution - 74,
											  (yResolution - 272 - (26 * iButtonOffset)), 24, 24,
											  WidgetTypes.WIDGET_DISABLED_CITIZEN, i, -1)
						screen.enable(szName, False)
						screen.show(szName)
					iButtonOffset = iButtonOffset + 1

		return 0

	# Will update the game data strings
	def updateGameDataStrings( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		screen.hide( "ResearchText" )
		screen.hide( "GoldText" )
		screen.hide( "TimeText" )
		screen.hide( "ResearchBar" )

		bShift = CyInterface().shiftKey()

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if (pHeadSelectedCity):
			ePlayer = pHeadSelectedCity.getOwner()
		else:
			ePlayer = gc.getGame().getActivePlayer()

		if ( ePlayer < 0 or ePlayer >= gc.getMAX_PLAYERS() ):
			return 0

		for iI in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			szString = "PercentText" + str(iI)
			screen.hide(szString)
			szString = "RateText" + str(iI)
			screen.hide(szString)

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):

			# Percent of commerce
			if (gc.getPlayer(ePlayer).isAlive()):
				iCount = 0
				for iI in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
					eCommerce = (iI + 1) % CommerceTypes.NUM_COMMERCE_TYPES
					if (gc.getPlayer(ePlayer).isCommerceFlexible(eCommerce) or (CyInterface().isCityScreenUp() and (eCommerce == CommerceTypes.COMMERCE_GOLD))):
						iShift = 60
						if (CyInterface().isCityScreenUp()):
							iShift = 0
						szOutText = u"<font=2>%c:%d%%</font>" %(gc.getCommerceInfo(eCommerce).getChar(), gc.getPlayer(ePlayer).getCommercePercent(eCommerce))
						szString = "PercentText" + str(iI)
						screen.setLabel( szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 14 + iShift, 50 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.show( szString )

						if not CyInterface().isCityScreenUp():
							szOutText = u"<font=2>" + localText.getText("TXT_KEY_MISC_POS_GOLD_PER_TURN", (gc.getPlayer(ePlayer).getCommerceRate(CommerceTypes(eCommerce)), )) + u"</font>"
							szString = "RateText" + str(iI)
							screen.setLabel( szString, "Background", szOutText, CvUtil.FONT_LEFT_JUSTIFY, 112 + iShift, 50 + (iCount * 19), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
							screen.show( szString )

						iCount = iCount + 1;

			self.updateTimeText()
			screen.setLabel( "TimeText", "Background", g_szTimeText, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 56, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( "TimeText" )

			if (gc.getPlayer(ePlayer).isAlive()):

				szText = CyGameTextMgr().getGoldStr(ePlayer)

#FfH: Added by Kael 12/08/2007, upgraded by Ronkhar 2025-01
				if (gc.getPlayer(ePlayer).getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KHAZAD') and gc.getPlayer(ePlayer).getNumCities() > 0):
					iCities = gc.getPlayer(ePlayer).getNumCities()
					iGold = gc.getPlayer(ePlayer).getGold() / iCities
					if iGold <= 49:
						szText = szText + " ("                    + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_1EMPTY"      , ()) + str( 50*iCities) + ")"
					elif iGold <= 99:
						szText = szText + " ("+str( 50*iCities-1) + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_2LOW"        , ()) + str(100*iCities) + ")"
					elif iGold <= 149:
						szText = szText + " ("+str(100*iCities-1) + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_3AVERAGE"    , ()) + str(150*iCities) + ")"
					elif iGold <= 199:
						szText = szText + " ("+str(150*iCities-1) + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_4STOCKED"    , ()) + str(200*iCities) + ")"
					elif iGold <= 299:
						szText = szText + " ("+str(200*iCities-1) + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_5ABUNDANT"   , ()) + str(300*iCities) + ")"
					elif iGold <= 499:
						szText = szText + " ("+str(300*iCities-1) + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_6FULL"       , ()) + str(500*iCities) + ")"
					else: # iGold > 499
						szText = szText + " ("+str(500*iCities-1) + localText.getText("TXT_KEY_MISC_DWARVEN_VAULT_7OVERFLOWING", ())                    + ")"
#FfH: End Add

				iShift = 60
				if (CyInterface().isCityScreenUp()):
					iShift = 0

				screen.setLabel( "GoldText", "Background", szText, CvUtil.FONT_LEFT_JUSTIFY, 12 + iShift, 6, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show( "GoldText" )

				if (((gc.getPlayer(ePlayer).calculateGoldRate() != 0) and not (gc.getPlayer(ePlayer).isAnarchy())) or (gc.getPlayer(ePlayer).getGold() != 0)):
					screen.show( "GoldText" )

				if (gc.getPlayer(ePlayer).isAnarchy()):

					szText = localText.getText("INTERFACE_ANARCHY", (gc.getPlayer(ePlayer).getAnarchyTurns(), ))
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 3, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					if ( gc.getPlayer(ePlayer).getCurrentResearch() != -1 ):
						screen.show( "ResearchText" )
					else:
						screen.hide( "ResearchText" )

				elif (gc.getPlayer(ePlayer).getCurrentResearch() != -1):

					#Xienwolf Religious HUDs Add Begin
					pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())

					if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_RELIGIOUS_HUD):
						if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
							TechStored = 'COLOR_NEGATIVE_RATE'
							TechRate = 'COLOR_FONT_RED'
						elif pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
							TechStored = 'COLOR_CITY_BLUE'
							TechRate = 'COLOR_TECH_BLUE'
						elif pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
							TechStored = 'COLOR_TECH_WORKING'
							TechRate = 'COLOR_TECH_BLACK'
						elif pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
							TechStored = 'COLOR_BROWN_TEXT'
							TechRate = 'COLOR_CITY_BROWN'
						elif pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
							TechStored = 'COLOR_DAWN_OF_MAN_TEXT'
							TechRate = 'COLOR_PLAYER_DARK_PURPLE'
						elif pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
							TechStored = 'COLOR_YELLOW'
							TechRate = 'COLOR_GREAT_PEOPLE_RATE'
						elif pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
							TechStored = 'COLOR_WHITE'
							TechRate = 'COLOR_GREY'
						else:
							TechStored = 'COLOR_RESEARCH_STORED'
							TechRate = 'COLOR_RESEARCH_RATE'
					else:
						TechStored = 'COLOR_RESEARCH_STORED'
						TechRate = 'COLOR_RESEARCH_RATE'
					screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_STORED, gc.getInfoTypeForString(str(TechStored)) )
					screen.setStackedBarColors( "ResearchBar", InfoBarTypes.INFOBAR_RATE, gc.getInfoTypeForString(str(TechRate)) )
					#Xienwolf Religious HUDs Add End
					szText = CyGameTextMgr().getResearchStr(ePlayer)

					xCoord = screen.centerX(512)
					yCoord = 3
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					screen.show( "ResearchText" )
###
					screen.setText( "ResearchText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 3, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RESEARCH, -1, -1 )
					screen.show( "ResearchText" )

					researchProgress = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchProgress(gc.getPlayer(ePlayer).getCurrentResearch())
					overflowResearch = (gc.getPlayer(ePlayer).getOverflowResearch() * gc.getPlayer(ePlayer).calculateResearchModifier(gc.getPlayer(ePlayer).getCurrentResearch()))/100
					researchCost = gc.getTeam(gc.getPlayer(ePlayer).getTeam()).getResearchCost(gc.getPlayer(ePlayer).getCurrentResearch())
					researchRate = gc.getPlayer(ePlayer).calculateResearchRate(-1)

					iFirst = float(researchProgress + overflowResearch) / float(researchCost)
					screen.setBarPercentage( "ResearchBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "ResearchBar", InfoBarTypes.INFOBAR_RATE, ( float(researchRate) / float(researchCost) ) )
					else:
						screen.setBarPercentage( "ResearchBar", InfoBarTypes.INFOBAR_RATE, ( ( float(researchRate) / float(researchCost) ) ) / ( 1 - iFirst ) )

					screen.show( "ResearchBar" )
# BUG
# Great Person Bar
				self.updateGreatPersonBar(screen)
				if not gc.isNoCrash():
					self.updateEmergentLeaderXPBar(screen)


		return 0

# BUG - Great Person Bar - start
	def updateGreatPersonBar(self, screen):
		screen.hide( "GreatPersonBar" )
		screen.hide( "GreatPersonBarText" )
		if (not CyInterface().isCityScreenUp()):
			pHeadSelectedCity = CyInterface().getHeadSelectedCity()
			if (pHeadSelectedCity and pHeadSelectedCity.getOwner() == gc.getGame().getActivePlayer()):
				pGPCity = pHeadSelectedCity
				iGPTurns = GPUtil.getCityTurns(pGPCity)
			else:
				pGPCity, iGPTurns = GPUtil.findNextCity()
				if (not pGPCity):
					pGPCity, iGPP = GPUtil.findMaxCity()
			szText = GPUtil.getGreatPeopleText(pGPCity, iGPTurns, GP_BAR_WIDTH, False, False, True)
			szText = u"<font=2>%s</font>" % (szText)
			if (pGPCity):
				iCityID = pGPCity.getID()
			else:
				iCityID = -1

# BUG - Bars on single line for higher resolution screens - start
			xResolution = screen.getXResolution()
			xCoord = 321 + (xResolution - 1024) / 2 + 380 / 2
			yCoord = 30

			screen.setText( "GreatPersonBarText", "Background", szText, CvUtil.FONT_CENTER_JUSTIFY, xCoord, yCoord, -0.4, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, iCityID, -1 )
			if (not pGPCity):
				screen.setHitTest( "GreatPersonBarText", HitTestTypes.HITTEST_NOHIT )
			screen.hide( "GreatPersonBarText" )
# BUG - Bars on single line for higher resolution screens - end

			if (pGPCity):
				fThreshold = float(gc.getPlayer( pGPCity.getOwner() ).greatPeopleThreshold(False))
				fRate = float(pGPCity.getGreatPeopleRate())
				fFirst = float(pGPCity.getGreatPeopleProgress()) / fThreshold

				screen.setBarPercentage( "GreatPersonBar", InfoBarTypes.INFOBAR_STORED, fFirst )
				if ( fFirst == 1 ):
					screen.setBarPercentage( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE, fRate / fThreshold )
				else:
					screen.setBarPercentage( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE, fRate / fThreshold / ( 1 - fFirst ) )
				screen.show( "GreatPersonBar" )
				screen.show( "GreatPersonBarText" )
			else:
				screen.setBarPercentage( "GreatPersonBar", InfoBarTypes.INFOBAR_STORED, 0 )
				screen.setBarPercentage( "GreatPersonBar", InfoBarTypes.INFOBAR_RATE, 0 )

# BUG - Great Person Bar - end

#*************************************************************************************************#
#** Emergent Leaders - XP bar widget                                                            **#
#*************************************************************************************************#
	def updateEmergentLeaderXPBar(self, screen):
		Manager = CvEventInterface.getEventManager() # to import foxtools dictionaries
		Status = Manager.LeaderStatus
		#screen.hide( "EmergentLeaderXPBar" )
		#screen.hide( "EmergentLeaderXPLbl" )
		pPlayer = gc.getPlayer( gc.getGame().getActivePlayer() )

		if pPlayer.getLeaderStatus() == Status["Emergent"]:
			# Check the experience value for all traits. If the leader has xp for the trait, show the xp bar for the trait.
			for iTrait in range(gc.getNumTraitInfos()):
				iTraitCounter = pPlayer.getTraitCounter(iTrait) # get the xp obtained for the trait
				if iTraitCounter != 0 and pPlayer.hasTrait(iTrait): # We are looking for traits with an experience counter and owned by the leader
					iTraitCounter = iTraitCounter - pPlayer.getTraitSpecificThreshold(iTrait)#*gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent())/100 # an emergent leader starts with xp = getTraitSpecificThreshold. We want the xp bar to start at 0.
					pTrait = gc.getTraitInfo(iTrait)
					if pTrait.getNextTrait() != TraitTypes.NO_TRAIT and not (CyInterface().isCityScreenUp()): # We will show an xp bar if the trait is not complete yet
						iLevel = pPlayer.getLevelforLastTraitGainedInChain(iTrait) # find current level
						# case 1 : leader level is 1, next level is 2 -> the xp bar shows current xp/ getTraitSpecificThreshold(N+1)
						# case 2 : leader level is N, next level is N+1 -> # the xp bar shows (current xp - getTraitSpecificThreshold(N))/ getTraitSpecificThreshold(N+1)
						if iLevel != 1:
							iTraitCounter = iTraitCounter - pPlayer.getTraitSpecificThreshold(iTrait+iLevel-1)# XP obtained since the beginning of this level
						iNextLevelXP = pPlayer.getTraitSpecificThreshold(iTrait+iLevel) # XP needed from level N to level N+1
						iRemainingXP = iNextLevelXP - iTraitCounter # XP the leader needs to levelup
						fLvlAdvancement = iTraitCounter/float(iNextLevelXP) # percentage of advancement to next level
						screen.setBarPercentage("EmergentLeaderXPBar", InfoBarTypes.INFOBAR_STORED, fLvlAdvancement)
						if iRemainingXP > 0:
							screen.setLabel("EmergentLeaderXPLbl", "", localText.getText("TXT_KEY_MISC_LEADER_EXPERIENCE", (iTraitCounter,iNextLevelXP,int(100*fLvlAdvancement),iRemainingXP,pTrait.getDescription(),iLevel+1)), CvUtil.FONT_CENTER_JUSTIFY, iXPLblCoordX, iXPLblCoordY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						else:
							screen.setLabel("EmergentLeaderXPLbl", "", localText.getText("TXT_KEY_MISC_LEADER_LEVELUP", (iTraitCounter,iNextLevelXP,pTrait.getDescription(),iLevel+1)), CvUtil.FONT_CENTER_JUSTIFY, iXPLblCoordX, iXPLblCoordY, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
						screen.show( "EmergentLeaderXPBar" )
						screen.show( "EmergentLeaderXPLbl" )
						break
#*************************************************************************************************#
#** Emergent Leaders - XP bar widget                                                        END **#
#*************************************************************************************************#

	def updateTimeText( self ):

		global g_szTimeText

		ePlayer = gc.getGame().getActivePlayer()
		pPlayer = gc.getPlayer(ePlayer)

		g_szTimeText = unicode(CyGameTextMgr().getInterfaceTimeStr(ePlayer))
		if (CyUserProfile().isClockOn()):
			g_szTimeText = getClockText() + u" - " + g_szTimeText
		if (pPlayer!=None):
			if pPlayer.getCivics(gc.getInfoTypeForString("CIVICOPTION_GOVERNMENT")) == gc.getInfoTypeForString("CIVIC_REPUBLIC"):
				# onBeginPlayerTurn iCycle counterpart
				iCycle				= gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent() / 10 * 4
				iRepublicCounter	= pPlayer.getFlagValue(gc.getInfoTypeForString("FLAG_REPUBLIC_TIMER"))
				iElection			= ( ( iCycle - iRepublicCounter + 1 ) % iCycle ) + gc.getGame().getGameTurn() + 1
				if iElection == gc.getGame().getGameTurn() + 1:
					iElection += iCycle
				szElection	= localText.getText("TXT_KEY_NEXT_ELECTION", (iElection, ))
				g_szTimeText = g_szTimeText + u" - " + szElection
			
	# Will update the selection Data Strings
	def updateCityScreen( self ):

		global MAX_DISPLAYABLE_BUILDINGS
		global MAX_DISPLAYABLE_TRADE_ROUTES
		global MAX_BONUS_ROWS

		global g_iNumTradeRoutes
		global g_iNumBuildings
		global g_iNumLeftBonus
		global g_iNumCenterBonus
		global g_iNumRightBonus
		
		global iBuildingsList

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bShift = CyInterface().shiftKey()

		lBuildingLines0		= []			# Not Wonders, not Effects
		lBuildingLines1		= []			# Wonders
		lBuildingLines2		= []			# Effects (0 costs)
		lChildBuildingLines	= []			# Buildings with a parent building

		screen.hide( "PopulationBar" )
		screen.hide( "ProductionBar" )
		screen.hide( "GreatPeopleBar" )
		screen.hide( "CultureBar" )
		screen.hide( "MaintenanceText" )
		screen.hide( "MaintenanceAmountText" )
		screen.hide( "CrimeText" )
		screen.hide( "CrimeAmountText" )
		screen.hide( "NationalityText" )
		screen.hide( "NationalityBar" )
		screen.hide( "DefenseText" )
		screen.hide( "CityScrollMinus" )
		screen.hide( "CityScrollPlus" )
		screen.hide( "CityNameText" )
		screen.hide( "PopulationText" )
		screen.hide( "PopulationInputText" )
		screen.hide( "HealthText" )
		screen.hide( "ProductionText" )
		screen.hide( "ProductionInputText" )
		screen.hide( "HappinessText" )
		screen.hide( "CultureText" )
		screen.hide( "GreatPeopleText" )

		for i in xrange( gc.getNumReligionInfos() ):
			szName = "ReligionHolyCityDDS" + str(i)
			screen.hide( szName )
			szName = "ReligionDDS" + str(i)
			screen.hide( szName )

		for i in xrange( gc.getNumCorporationInfos() ):
			szName = "CorporationHeadquarterDDS" + str(i)
			screen.hide( szName )
			szName = "CorporationDDS" + str(i)
			screen.hide( szName )

		for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
			szName = "CityPercentText" + str(i)
			screen.hide( szName )

#FfH: Added by Kael 07/18/2007
#		screen.setPanelSize( "InterfaceCenterBackgroundWidget", 296, yResolution - 133, xResolution - (296*2), 133)
#		screen.setPanelSize( "InterfaceLeftBackgroundWidget", 0, yResolution - 168, 304, 168)
#		screen.setPanelSize( "InterfaceRightBackgroundWidget", xResolution - 304, yResolution - 168, 304, 168)
#		screen.setPanelSize( "MiniMapPanel", xResolution - 214, yResolution - 151, 208, 151)
		iMultiListXR = 332
#FfH: End Add

		screen.addPanel( "BonusPane0", u"", u"", True, False, xResolution - 244, 94, 57, yResolution - 560, PanelStyles.PANEL_STYLE_CITY_COLUMNL )
		screen.hide( "BonusPane0" )
		screen.addScrollPanel( "BonusBack0", u"", xResolution - 242, 94, 157, yResolution - 576, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack0" )

		screen.addPanel( "BonusPane1", u"", u"", True, False, xResolution - 187, 94, 68, yResolution - 560, PanelStyles.PANEL_STYLE_CITY_COLUMNC )
		screen.hide( "BonusPane1" )
		screen.addScrollPanel( "BonusBack1", u"", xResolution - 191, 94, 184, yResolution - 576, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack1" )

		screen.addPanel( "BonusPane2", u"", u"", True, False, xResolution - 119, 94, 107, yResolution - 560, PanelStyles.PANEL_STYLE_CITY_COLUMNR )
		screen.hide( "BonusPane2" )
		screen.addScrollPanel( "BonusBack2", u"", xResolution - 125, 94, 205, yResolution - 576, PanelStyles.PANEL_STYLE_EXTERNAL )
		screen.hide( "BonusBack2" )

		screen.hide( "TradeRouteTable" )
		screen.hide( "BuildingListTable" )
		screen.hide( "TrainingTable" )

		szPathBuildingType0	= "Art/Interface/Screens/Building_Icon_Common_Dark.dds"
		szPathBuildingType1	= "Art/Interface/Screens/Building_Icon_Wonder_Dark.dds"
		szPathBuildingType2	= "Art/Interface/Screens/Building_Icon_Effect_Dark.dds"
		szPathTradeRoutes	= "Art/Interface/Screens/Trade_Routes_Dark.dds"
#		szPathSpecialistL	= "Art/Interface/Screens/Specialist_Left_Dark.dds"
		szPathTrainingTable	= "Art/Interface/Screens/Training_Table_Dark.dds"

#		if iBuildingsList == 5:
#			szBuildingsLabel = localText.getText("TXT_KEY_CONCEPT_SPECIALISTS", ())
#			szPathSpecialistL = "Art/Interface/Screens/Specialist_Left.dds"
		if iBuildingsList == 4:
			szBuildingsLabel = localText.getText("TXT_KEY_TRAINING_LABEL", ())
			szPathTrainingTable = "Art/Interface/Screens/Training_Table.dds"
		elif iBuildingsList == 3:
			szBuildingsLabel = localText.getText("TXT_KEY_HEADING_TRADEROUTE_LIST", ())
			szPathTradeRoutes = "Art/Interface/Screens/Trade_Routes.dds"
		elif iBuildingsList == 2:
			szBuildingsLabel = localText.getText("TXT_KEY_PEDIA_EFFECTS", ())
			szPathBuildingType2 = "Art/Interface/Screens/Building_Icon_Effect.dds"
		elif iBuildingsList == 1:
			szBuildingsLabel = localText.getText("TXT_KEY_CONCEPT_WONDERS", ())
			szPathBuildingType1 = "Art/Interface/Screens/Building_Icon_Wonder.dds"
		else:
			szBuildingsLabel = localText.getText("TXT_KEY_CONCEPT_BUILDINGS", ())
			szPathBuildingType0 = "Art/Interface/Screens/Building_Icon_Common.dds"

		screen.setLabel( "BuildingListLabel", "Background", szBuildingsLabel, CvUtil.FONT_CENTER_JUSTIFY, HUD_City_Left_Panel_Width / 2 - 5, 210, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide( "BuildingListLabel" )

		screen.setImageButton("BuildingsCommon", szPathBuildingType0, 15, 165, 40, 40, WidgetTypes.WIDGET_PYTHON, 1001, -1 )
		screen.hide( "BuildingsCommon" )

		screen.setImageButton("BuildingsWonder", szPathBuildingType1, 60, 165, 40, 40, WidgetTypes.WIDGET_PYTHON, 1002, -1 )
		screen.hide( "BuildingsWonder" )

		screen.setImageButton("BuildingsEffects", szPathBuildingType2, 105, 165, 40, 40, WidgetTypes.WIDGET_PYTHON, 1003, -1 )
		screen.hide( "BuildingsEffects" )

		screen.setImageButton("TradeRoutesButton", szPathTradeRoutes, 150, 165, 40, 40, WidgetTypes.WIDGET_PYTHON, 1004, -1 )
		screen.hide( "TradeRoutesButton" )

		screen.setImageButton("TrainingTableButton", szPathTrainingTable, 195, 165, 40, 40, WidgetTypes.WIDGET_PYTHON, 1005, -1 )
		screen.hide( "TrainingTableButton" )

#		screen.setImageButton("SpecialistLeft", szPathSpecialistL, 195, 165, 40, 40, WidgetTypes.WIDGET_GENERAL, -1, -1 )
#		screen.hide( "SpecialistLeft" )

		screen.hide( "BuildingListBackground" )
		screen.hide( "TradeRouteListBackground" )
		screen.hide( "TradeRouteListLabel" )

		i = 0
		for i in xrange( g_iNumLeftBonus ):
			szName = "LeftBonusItem" + str(i)
			screen.hide( szName )

		i = 0
		for i in xrange( g_iNumCenterBonus ):
			szName = "CenterBonusItemLeft" + str(i)
			screen.hide( szName )
			szName = "CenterBonusItemRight" + str(i)
			screen.hide( szName )

		i = 0
		for i in xrange( g_iNumRightBonus ):
			szName = "RightBonusItemLeft" + str(i)
			screen.hide( szName )
			szName = "RightBonusItemRight" + str(i)
			screen.hide( szName )

		i = 0
		for i in xrange( 3 ):
			szName = "BonusPane" + str(i)
			screen.hide( szName )
			szName = "BonusBack" + str(i)
			screen.hide( szName )

		i = 0
		if ( CyInterface().isCityScreenUp() ):
			if ( pHeadSelectedCity ):

				#Xienwolf Religious HUDs Add Begin
				#screen.show( "InterfaceTopLeftBackgroundWidget" )
				#screen.show( "InterfaceTopRightBackgroundWidget" )
				#screen.show( "InterfaceCenterLeftBackgroundWidget" )
				#screen.show( "CityScreenTopWidget" )
				#screen.show( "CityNameBackground" )
				#screen.show( "TopCityPanelLeft" )
				#screen.show( "TopCityPanelRight" )
				#screen.show( "CityScreenAdjustPanel" )
				#screen.show( "InterfaceCenterRightBackgroundWidget" )
				#Xienwolf Religious HUDs Add End

				if ( pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam() ):
					if ( gc.getActivePlayer().getNumCities() > 1 ):
						screen.show( "CityScrollMinus" )
						screen.show( "CityScrollPlus" )

				# Help Text Area
				screen.setHelpTextArea( 390, FontTypes.SMALL_FONT, 0, 0, -2.2, True, ArtFileMgr.getInterfaceArtInfo("POPUPS_BACKGROUND_TRANSPARENT").getPath(), True, True, CvUtil.FONT_LEFT_JUSTIFY, 0 )

				iFoodDifference = pHeadSelectedCity.foodDifference(True)
				iProductionDiffNoFood = pHeadSelectedCity.getCurrentProductionDifference(True, True)
				iProductionDiffJustFood = (pHeadSelectedCity.getCurrentProductionDifference(False, True) - iProductionDiffNoFood)

				szBuffer = u"<font=4>"

				if (pHeadSelectedCity.isCapital()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR))
				elif (pHeadSelectedCity.isGovernmentCenter()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR))
				if pHeadSelectedCity.getCityClass()!=-1:
					szBuffer += localText.getText(gc.getCityClassInfo(pHeadSelectedCity.getCityClass()).getShortDescription(),())
		
				if (pHeadSelectedCity.isPower()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.POWER_CHAR))

				szBuffer += u"%s: %d" %(pHeadSelectedCity.getName(), pHeadSelectedCity.getPopulation())
				if (pHeadSelectedCity.getCityPopulationCap()>0):
					szBuffer+=u"/%d"%(pHeadSelectedCity.getCityPopulationCap())
				if (pHeadSelectedCity.isOccupation()):
					szBuffer += u" (%c:%d)" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR), pHeadSelectedCity.getOccupationTimer())

				szBuffer += u"</font>"

				screen.setText( "CityNameText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), 32, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )
				screen.setStyle( "CityNameText", "Button_Stone_Style" )
				screen.show( "CityNameText" )

				if not (gc.getPlayer(pHeadSelectedCity.getOwner()).isIgnoreFood()):
					if ( (iFoodDifference != 0) or not (pHeadSelectedCity.isFoodProduction() )):
# FF: Changed by Jean Elcard 09/03/2009 (growth control buttons)
						'''
						if (iFoodDifference > 0):
						'''
						if pHeadSelectedCity.AI_stopGrowth():
							szBuffer = localText.getText("INTERFACE_CITY_STAGNANT_GROWTH_CONTROL", ())
						elif (iFoodDifference > 0):
# FF: End Change
							szBuffer = localText.getText("INTERFACE_CITY_GROWING", (pHeadSelectedCity.getFoodTurnsLeft(), ))
						elif (iFoodDifference < 0):
							szBuffer = localText.getText("INTERFACE_CITY_STARVING", ())
						else:
							szBuffer = localText.getText("INTERFACE_CITY_STAGNANT", ())

						screen.setLabel( "PopulationText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow1Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.setHitTest( "PopulationText", HitTestTypes.HITTEST_NOHIT )
						screen.show( "PopulationText" )

					if (not pHeadSelectedCity.isDisorder() and not pHeadSelectedCity.isFoodProduction()):

						FoodGain = iFoodDifference + pHeadSelectedCity.foodConsumption(False, 0)
						szBuffer = u"%d%c - %d%c" %(FoodGain, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), pHeadSelectedCity.foodConsumption(False, 0), CyGame().getSymbolID(FontSymbols.EATEN_FOOD_CHAR))
						screen.setLabel( "PopulationInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.show( "PopulationInputText" )

					else:

						szBuffer = u"%d%c" %(iFoodDifference, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar())
						screen.setLabel( "PopulationInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
						screen.show( "PopulationInputText" )

				if ((pHeadSelectedCity.badHealth(False) > 0) or (pHeadSelectedCity.goodHealth() >= 0)):
					if (pHeadSelectedCity.healthRate(False, 0) < 0):
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_BAD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False), pHeadSelectedCity.healthRate(False, 0)))
					elif (pHeadSelectedCity.badHealth(False) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD", (pHeadSelectedCity.goodHealth(), pHeadSelectedCity.badHealth(False)))
					else:
						szBuffer = localText.getText("INTERFACE_CITY_HEALTH_GOOD_NO_BAD", (pHeadSelectedCity.goodHealth(), ))

					screen.setLabel( "HealthText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow1Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HEALTH, -1, -1 )
					screen.show( "HealthText" )

				if (iFoodDifference < 0):

					if ( pHeadSelectedCity.getFood() + iFoodDifference > 0 ):
						iDeltaFood = pHeadSelectedCity.getFood() + iFoodDifference
					else:
						iDeltaFood = 0
					if ( -iFoodDifference < pHeadSelectedCity.getFood() ):
						iExtraFood = -iFoodDifference
					else:
						iExtraFood = pHeadSelectedCity.getFood()
					iFirst = float(iDeltaFood) / float(pHeadSelectedCity.growthThreshold())
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, 0.0 )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ( float(iExtraFood) / float(pHeadSelectedCity.growthThreshold()) ) )
					else:
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ( ( float(iExtraFood) / float(pHeadSelectedCity.growthThreshold()) ) ) / ( 1 - iFirst ) )

				else:

					iFirst = float(pHeadSelectedCity.getFood()) / float(pHeadSelectedCity.growthThreshold())
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, ( float(iFoodDifference) / float(pHeadSelectedCity.growthThreshold()) ) )
					else:
						screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE, ( ( float(iFoodDifference) / float(pHeadSelectedCity.growthThreshold()) ) ) / ( 1 - iFirst ) )
					screen.setBarPercentage( "PopulationBar", InfoBarTypes.INFOBAR_RATE_EXTRA, 0.0 )

				if not (gc.getPlayer(pHeadSelectedCity.getOwner()).isIgnoreFood()):
					screen.show( "PopulationBar" )

				if (pHeadSelectedCity.getOrderQueueLength() > 0):
					if (pHeadSelectedCity.isProductionProcess()):
						szBuffer = pHeadSelectedCity.getProductionName()
					else:
						szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft()))

					screen.setLabel( "ProductionText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, screen.centerX(512), iCityCenterRow2Y, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "ProductionText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "ProductionText" )

				if (pHeadSelectedCity.isProductionProcess()):
					szBuffer = u"%d%c" %(pHeadSelectedCity.getYieldRate(YieldTypes.YIELD_PRODUCTION), gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				elif (pHeadSelectedCity.isFoodProduction() and (iProductionDiffJustFood > 0)):
					szBuffer = u"%d%c + %d%c" %(iProductionDiffJustFood, gc.getYieldInfo(YieldTypes.YIELD_FOOD).getChar(), iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
				else:
					szBuffer = u"%d%c" %(iProductionDiffNoFood, gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())

				screen.setLabel( "ProductionInputText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iCityCenterRow1X - 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_PRODUCTION_MOD_HELP, -1, -1 )
				screen.show( "ProductionInputText" )

				if ((pHeadSelectedCity.happyLevel() >= 0) or (pHeadSelectedCity.unhappyLevel(0) > 0)):
					if (pHeadSelectedCity.isDisorder()):
						szBuffer = u"%d%c" %(pHeadSelectedCity.angryPopulation(0), CyGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR))
					elif (pHeadSelectedCity.angryPopulation(0) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_UNHAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0), pHeadSelectedCity.angryPopulation(0)))
					elif (pHeadSelectedCity.unhappyLevel(0) > 0):
						szBuffer = localText.getText("INTERFACE_CITY_HAPPY", (pHeadSelectedCity.happyLevel(), pHeadSelectedCity.unhappyLevel(0)))
					else:
						szBuffer = localText.getText("INTERFACE_CITY_HAPPY_NO_UNHAPPY", (pHeadSelectedCity.happyLevel(), ))

					screen.setLabel( "HappinessText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - iCityCenterRow1X + 6, iCityCenterRow2Y, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_HAPPINESS, -1, -1 )
					screen.show( "HappinessText" )

				if (not(pHeadSelectedCity.isProductionProcess())):

					iFirst = ((float(pHeadSelectedCity.getProduction())) / (float(pHeadSelectedCity.getProductionNeeded())))
					screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						iSecond = ( ((float(iProductionDiffNoFood)) / (float(pHeadSelectedCity.getProductionNeeded()))) )
					else:
						iSecond = ( ((float(iProductionDiffNoFood)) / (float(pHeadSelectedCity.getProductionNeeded()))) ) / ( 1 - iFirst )
					screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE, iSecond )
					if ( iFirst + iSecond == 1 ):
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ( ((float(iProductionDiffJustFood)) / (float(pHeadSelectedCity.getProductionNeeded()))) ) )
					else:
						screen.setBarPercentage( "ProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ( ( ((float(iProductionDiffJustFood)) / (float(pHeadSelectedCity.getProductionNeeded()))) ) ) / ( 1 - ( iFirst + iSecond ) ) )

					screen.show( "ProductionBar" )

				iCount = 0

				for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
					eCommerce = (i + 1) % CommerceTypes.NUM_COMMERCE_TYPES

					if ((gc.getPlayer(pHeadSelectedCity.getOwner()).isCommerceFlexible(eCommerce)) or (eCommerce == CommerceTypes.COMMERCE_GOLD)):
						szBuffer = u"%d.%02d %c" %(pHeadSelectedCity.getCommerceRate(eCommerce), pHeadSelectedCity.getCommerceRateTimes100(eCommerce)%100, gc.getCommerceInfo(eCommerce).getChar())

						iHappiness = pHeadSelectedCity.getCommerceHappinessByType(eCommerce)

						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u", %d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR))
							else:
								szTempBuffer = u", %d%c" %(-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))
							szBuffer = szBuffer + szTempBuffer

						szName = "CityPercentText" + str(iCount)
						screen.setLabel( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 45 + (19 * iCount) + 4, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_COMMERCE_MOD_HELP, eCommerce, -1 )
						screen.show( szName )
						iCount = iCount + 1

				iCount = 0

				# Adds a little bit of space for the char column of the TradeRouteTable for every Yield and Commerce type city gaining through trade routes.
				xTradeRouteOffset = 10
				iNumYield = 0
				# 3rd empty column (spacing for the scrollbar) is looking bad if grid is drawn
				bDrawGridTrade = False

				for j in xrange (YieldTypes.NUM_YIELD_TYPES):
					iTotalYield = pHeadSelectedCity.getTradeYield(j)
					if (iTotalYield != 0):
						iNumYield += 1

				for j in xrange (CommerceTypes.NUM_COMMERCE_TYPES):
					iTotalCommerce = pHeadSelectedCity.getTradeCommerce(j)
					if (iTotalCommerce != 0):
						iNumYield += 1

				# Height of the building/routes list = yResolution - Starting Height (232) - NationalityBar Starting Height (214) - few px of spacing
				screen.addTableControlGFC( "TradeRouteTable", 3, 10, 232, HUD_City_Left_Panel_Width - 20, yResolution - 450, False, bDrawGridTrade, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
				screen.setStyle( "TradeRouteTable", "Table_City_Style" )
				screen.addTableControlGFC( "BuildingListTable", 3, 10, 232, HUD_City_Left_Panel_Width - 20, yResolution - 450, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
				screen.setStyle( "BuildingListTable", "Table_City_Style" )
				screen.addTableControlGFC( "TrainingTable", 4, 10, 232, HUD_City_Left_Panel_Width - 20, yResolution - 450, True, True, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
				screen.setStyle( "TrainingTable", "Table_City_Style" )


				screen.setTableColumnHeader( "TradeRouteTable", 0, u"", ( HUD_City_Left_Panel_Width - 20 ) / 2 - xTradeRouteOffset * iNumYield - 10)
				screen.setTableColumnHeader( "TradeRouteTable", 1, u"", ( HUD_City_Left_Panel_Width - 20 ) / 2 + xTradeRouteOffset * iNumYield )
				screen.setTableColumnHeader( "TradeRouteTable", 2, u"", 10 )
				screen.setTableColumnRightJustify( "TradeRouteTable", 1 )

				iBuildingListTableColumnWidth0 = ( ( HUD_City_Left_Panel_Width - 20 ) * 2 / 3 ) - 10
				iBuildingListTableColumnWidth1 = ( ( HUD_City_Left_Panel_Width - 20 ) / 3 )
				# More space for the 2nd column (Happiness, Health, Yield, etc) on high res.
				if self.isHighResolution():
					iBuildingListTableColumnWidth0 = ( ( HUD_City_Left_Panel_Width - 20 ) / 2 ) - 10
					iBuildingListTableColumnWidth1 = ( ( HUD_City_Left_Panel_Width - 20 ) / 2 )

				screen.setTableColumnHeader( "BuildingListTable", 0, u"", iBuildingListTableColumnWidth0 )
				screen.setTableColumnHeader( "BuildingListTable", 1, u"", iBuildingListTableColumnWidth1 )
				screen.setTableColumnHeader( "BuildingListTable", 2, u"", 10 )
				screen.setTableColumnRightJustify( "BuildingListTable", 1 )

				screen.setTableColumnHeader( "TrainingTable", 0, "<font=2>" + localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ()) + "</font>", ( HUD_City_Left_Panel_Width - 20 ) * 2 / 5 )
				screen.setTableColumnHeader( "TrainingTable", 1, "<font=2>" + localText.getText("TXT_KEY_XP_CAP", ()) + "</font>", ( HUD_City_Left_Panel_Width - 20 ) / 5 )
				screen.setTableColumnHeader( "TrainingTable", 2, "<font=2>" + localText.getText("TXT_KEY_XP_RATE", ()) + "</font>", ( HUD_City_Left_Panel_Width - 20 ) / 5 )
				screen.setTableColumnHeader( "TrainingTable", 3, "<font=2>" + localText.getText("TXT_KEY_FREE_XP", ()) + "</font>", ( HUD_City_Left_Panel_Width - 20 ) / 5 )

				screen.show( "BuildingListBackground" )
				screen.show( "TradeRouteListBackground" )
				screen.show( "BuildingListLabel" )
				screen.show( "TradeRouteListLabel" )

				screen.show( "BuildingsCommon" )
				screen.show( "BuildingsWonder" )
				screen.show( "BuildingsEffects" )
				screen.show( "TradeRoutesButton" )
				screen.show( "TrainingTableButton" )
#				screen.show( "SpecialistLeft" )

				for i in xrange( 3 ):
					szName = "BonusPane" + str(i)
					screen.show( szName )
					szName = "BonusBack" + str(i)
					screen.show( szName )


## BuildingListTable Start
				i = 0
				iNumBuildings = 0

				for i in xrange(gc.getNumBuildingInfos()):
					if pHeadSelectedCity.getNumBuilding(i) > 0:

						for k in xrange(pHeadSelectedCity.getNumBuilding(i)):

							iParent = -1
							szLeftBuffer = gc.getBuildingInfo(i).getDescription()
							szRightBuffer = u""
							bFirst = True


							if (pHeadSelectedCity.getNumActiveBuilding(i) > 0):

## Building Health
								iHealth = pHeadSelectedCity.getBuildingHealth(i)

								if (iHealth != 0):
									if not bFirst:
										szRightBuffer += ", "
									else:
										bFirst = False

									if ( iHealth > 0 ):
										szRightBuffer += u"%d%c" %( iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR) )

									else:
										szRightBuffer += u"%d%c" % (-iHealth, CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR))

## Building Happiness
								iHappiness = pHeadSelectedCity.getBuildingHappiness(i)

								if (iHappiness != 0):
									if not bFirst:
										szRightBuffer += ", "
									else:
										bFirst = False

									if ( iHappiness > 0 ):
										szRightBuffer += u"%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )

									else:
										szRightBuffer += u"%d%c" % (-iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR))

## Building Yield
								for j in xrange(YieldTypes.NUM_YIELD_TYPES):
									iYield = (gc.getBuildingInfo(i).getYieldChange(j) + pHeadSelectedCity.getNumBuilding(i) * pHeadSelectedCity.getBuildingYieldChange(gc.getBuildingInfo(i).getBuildingClassType(), j))

									if (iYield != 0):
										if not bFirst:
											szRightBuffer += ", "
										else:
											bFirst = False

										szRightBuffer += u"%s%d%c" %( "", iYield, gc.getYieldInfo(j).getChar() )

## Building Yield %
									iYieldModifier = gc.getBuildingInfo(i).getYieldModifier(j) * pHeadSelectedCity.getNumBuilding(i)

									if iYieldModifier != 0:
										if not bFirst:
											szRightBuffer += ", "
										else:
											bFirst = False

										szRightBuffer += str(iYieldModifier) + "%" + u"%c" %(gc.getYieldInfo(j).getChar())

## Building Commerce
								for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
									iCommerce = pHeadSelectedCity.getBuildingCommerceByBuilding(j, i) / pHeadSelectedCity.getNumBuilding(i)

									if (iCommerce != 0):
										if not bFirst:
											szRightBuffer += ", "
										else:
											bFirst = False

										szRightBuffer += u"%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )

## Building Commerce %
									iCommerceModifier = gc.getBuildingInfo(i).getCommerceModifier(j) * pHeadSelectedCity.getNumBuilding(i)
									if iCommerceModifier != 0:
										if not bFirst:
											szRightBuffer += ", "
										else:
											bFirst = False

										szRightBuffer += str(iCommerceModifier) + "%" + u"%c" %(gc.getCommerceInfo(j).getChar())

## Building GP
								iGPRate = gc.getBuildingInfo(i).getGreatPeopleRateChange()
								if iGPRate != 0:
									if not bFirst:
										szRightBuffer += ", "
									else:
										bFirst = False

									szRightBuffer += str(iGPRate) + CyTranslator().getText("[ICON_GREATPEOPLE]", ())

## Trade Routes
								iTradeRoute = gc.getBuildingInfo(i).getTradeRoutes()
								if iTradeRoute != 0:
									if not bFirst:
										szRightBuffer += ", "
									else:
										bFirst = False

									szRightBuffer +=  u"%d%c" %(iTradeRoute, CyGame().getSymbolID(FontSymbols.TRADE_CHAR) )

## Parent check
								if not gc.getBuildingInfo(i).getParentBuildingClass() == -1:
									szLeftBuffer = "	" + szLeftBuffer
									iParent = gc.getBuildingInfo(i).getParentBuildingClass()

## Pick Category
							buildingListItem = [szLeftBuffer, szRightBuffer, i, iParent]

							if not gc.getBuildingInfo(i).getParentBuildingClass() == -1:
								buildingLines = lChildBuildingLines
							elif gc.getBuildingInfo(i).isCrimeEffect():
								buildingLines = lBuildingLines2
							elif isLimitedWonderClass(gc.getBuildingInfo(i).getBuildingClassType()):
								buildingLines = lBuildingLines1
							else:
								buildingLines = lBuildingLines0

							buildingLines.append(buildingListItem)

							iNumBuildings +=  1

## Sort alphabetically, szLeftBuffer is a building name
				lBuildingLines0.sort()
				lBuildingLines1.sort()
				lBuildingLines2.sort()

## Insert Child Buildings after Parent one
				lCopyBuildingLines0 = list(lBuildingLines0)
				lCopyBuildingLines1 = list(lBuildingLines1)
				lCopyBuildingLines2 = list(lBuildingLines2)

				for iChildItem in lChildBuildingLines:
					for iParentItem in lCopyBuildingLines0:
						if iChildItem[3] == gc.getBuildingInfo(iParentItem[2]).getBuildingClassType():
							lBuildingLines0.insert(lBuildingLines0.index(iParentItem) + 1, iChildItem)
					for iParentItem in lCopyBuildingLines1:
						if iChildItem[3] == gc.getBuildingInfo(iParentItem[2]).getBuildingClassType():
							lBuildingLines1.insert(lBuildingLines1.index(iParentItem) + 1, iChildItem)
					for iParentItem in lCopyBuildingLines2:
						if iChildItem[3] == gc.getBuildingInfo(iParentItem[2]).getBuildingClassType():
							lBuildingLines2.insert(lBuildingLines2.index(iParentItem) + 1, iChildItem)

## Pick list to draw
				if iBuildingsList == 2:
					lBuildings = lBuildingLines2
				elif iBuildingsList == 1:
					lBuildings = lBuildingLines1
				else:
					lBuildings = lBuildingLines0

## Draw Table
				ix = 0
				for iBuildingLineToDraw in lBuildings:
					screen.appendTableRow( "BuildingListTable" )
					screen.setTableText( "BuildingListTable", 0, ix, "<font=1>" + iBuildingLineToDraw[0] + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, iBuildingLineToDraw[2], -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.setTableText( "BuildingListTable", 1, ix, "<font=1>" + iBuildingLineToDraw[1] + "</font>", "", WidgetTypes.WIDGET_HELP_BUILDING, iBuildingLineToDraw[2], -1, CvUtil.FONT_RIGHT_JUSTIFY )
					ix += 1

				if ( iNumBuildings > g_iNumBuildings ):
					g_iNumBuildings = iNumBuildings

				screen.hide( "BuildingListTable" )
## BuildingListTable End

## TrainingTable Start
				iNumTrainingRows = 0
				for iUC in xrange(gc.getNumUnitCombatInfos()):
					fUCXPRate = pHeadSelectedCity.getTrainXPRate(iUC)
					iUCXPCap = pHeadSelectedCity.getTrainXPCap(iUC)
					iFreeXP = pHeadSelectedCity.getUnitCombatFreeExperience(iUC)
					iFreeXP += pHeadSelectedCity.getSpecialistFreeExperience()
					szUCDecription = gc.getUnitCombatInfo(iUC).getDescription()
					szUCXPRate = u"%.2f" %(fUCXPRate)
					szUCXPCap = str(iUCXPCap / 100)
					szUCXPFree = str(iFreeXP / 100)
					if fUCXPRate > 0 or iUCXPCap > 0 or iFreeXP >0:
						screen.appendTableRow( "TrainingTable" )
						screen.setTableText( "TrainingTable", 0, iNumTrainingRows, "<font=1>" + szUCDecription + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "TrainingTable", 1, iNumTrainingRows, "<font=1>" + szUCXPCap + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "TrainingTable", 2, iNumTrainingRows, "<font=1>" + szUCXPRate + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "TrainingTable", 3, iNumTrainingRows, "<font=1>" + szUCXPFree + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
						iNumTrainingRows += 1
				if iNumTrainingRows == 0:
					screen.appendTableRow( "TrainingTable" )
					screen.setTableText( "TrainingTable", 0, iNumTrainingRows, "<font=1>" + localText.getText("TXT_KEY_NO_XP_BONUSES", ()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

				screen.hide( "TrainingTable" )
## TrainingTable End

## TradeRouteTable Start
				iNumTradeRoutes = 0

				for i in xrange(gc.getDefineINT("MAX_TRADE_ROUTES")):
					pLoopCity = pHeadSelectedCity.getTradeCity(i)

					if (pLoopCity and pLoopCity.getOwner() >= 0):
						player = gc.getPlayer(pLoopCity.getOwner())
						szLeftBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(player.getPlayerTextColorR(), player.getPlayerTextColorG(), player.getPlayerTextColorB(), player.getPlayerTextColorA(), pLoopCity.getName() )
						szRightBuffer = u""

						iTradeProfit100 = pHeadSelectedCity.calculateTradeProfitTimes100(pLoopCity)

						for j in xrange( YieldTypes.NUM_YIELD_TYPES ):
							iTradeYield = pHeadSelectedCity.calculateCityTradeYield(j, pLoopCity, iTradeProfit100)

							if (iTradeYield != 0):
								if ( iTradeYield > 999):
									szTempBuffer = u"%d%s%01d%c" %( int(iTradeYield / 100), ".", int(iTradeYield % 100) // 10, gc.getYieldInfo(j).getChar() )
									szRightBuffer = szRightBuffer + szTempBuffer
								else:
									szTempBuffer = u"%d%s%02d%c" %( int(iTradeYield / 100), ".", int(iTradeYield % 100), gc.getYieldInfo(j).getChar() )
									szRightBuffer = szRightBuffer + szTempBuffer

						for j in xrange( CommerceTypes.NUM_COMMERCE_TYPES ):
							iTradeCommerce = pHeadSelectedCity.calculateCityTradeCommerce(j, pLoopCity, iTradeProfit100)

							if (iTradeCommerce != 0):
								if ( iTradeCommerce > 999 ):
									szTempBuffer = u"%d%s%01d%c" %( int(iTradeCommerce / 100), ".", int(iTradeCommerce % 100) // 10, gc.getCommerceInfo(j).getChar() )
									szRightBuffer = szRightBuffer + szTempBuffer
								else:
									szTempBuffer = u"%d%s%02d%c" %( int(iTradeCommerce / 100), ".", int(iTradeCommerce % 100), gc.getCommerceInfo(j).getChar() )
									szRightBuffer = szRightBuffer + szTempBuffer

						screen.appendTableRow( "TradeRouteTable" )
						screen.setTableText( "TradeRouteTable", 0, iNumTradeRoutes, "<font=1>" + szLeftBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "TradeRouteTable", 1, iNumTradeRoutes, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_HELP_TRADE_ROUTE_CITY, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )

						iNumTradeRoutes = iNumTradeRoutes + 1

				if iNumTradeRoutes > 1:
					iNumYield = 0
					szRightBuffer = u""
					for j in xrange (YieldTypes.NUM_YIELD_TYPES):
						iTotalYield = pHeadSelectedCity.getTradeYield(j)
						if (iTotalYield != 0):
							szTempBuffer = u"%d%c" %( iTotalYield, gc.getYieldInfo(j).getChar() )
							szRightBuffer = szRightBuffer + szTempBuffer
							iNumYield += 1

					for j in xrange (CommerceTypes.NUM_COMMERCE_TYPES):
						iTotalCommerce = pHeadSelectedCity.getTradeCommerce(j)
						if (iTotalCommerce != 0):
							szTempBuffer = u"%d%c" %( iTotalCommerce, gc.getCommerceInfo(j).getChar() )
							szRightBuffer = szRightBuffer + szTempBuffer
							iNumYield += 1

					screen.appendTableRow( "TradeRouteTable" )
					screen.setTableText( "TradeRouteTable", 0, iNumTradeRoutes, "<font=1>" + localText.getText("TXT_KEY_TRADE_ROUTE_TOTAL",()) + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.setTableText( "TradeRouteTable", 1, iNumTradeRoutes, "<font=1>" + szRightBuffer + "</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )

				if ( iNumTradeRoutes > g_iNumTradeRoutes ):
					g_iNumTradeRoutes = iNumTradeRoutes

				screen.hide( "TradeRouteTable" )
## TradeRouteTable End

				if iBuildingsList == 4:
					screen.show( "TrainingTable" )
				elif iBuildingsList == 3:
					screen.show( "TradeRouteTable" )
				else:
					screen.show( "BuildingListTable" )

				i = 0
				iLeftCount = 0
				iCenterCount = 0
				iRightCount = 0

				for i in xrange( gc.getNumBonusInfos() ):
					bHandled = False
					if ( pHeadSelectedCity.hasBonus(i) ):

						iHealth = pHeadSelectedCity.getBonusHealth(i)
						iHappiness = pHeadSelectedCity.getBonusHappiness(i)

						szBuffer = u""
						szLeadBuffer = u""

						szTempBuffer = u"<font=1>%c" %( gc.getBonusInfo(i).getChar() )
						szLeadBuffer = szLeadBuffer + szTempBuffer

						if (pHeadSelectedCity.getNumBonuses(i) > 1):
							szTempBuffer = u"(%d)" %( pHeadSelectedCity.getNumBonuses(i) )
							szLeadBuffer = szLeadBuffer + szTempBuffer

						szLeadBuffer = szLeadBuffer + "</font>"

						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u"<font=1>+%d%c</font>" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
							else:
								szTempBuffer = u"<font=1>+%d%c</font>" %( -iHappiness, CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )

							if ( iHealth > 0 ):
								szTempBuffer += u"<font=1>, +%d%c</font>" %( iHealth, CyGame().getSymbolID( FontSymbols.HEALTHY_CHAR ) )

							szName = "RightBonusItemLeft" + str(iRightCount)
							screen.setLabelAt( szName, "BonusBack2", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							szName = "RightBonusItemRight" + str(iRightCount)
							screen.setLabelAt( szName, "BonusBack2", szTempBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 102, (iRightCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )

							iRightCount = iRightCount + 1

							bHandled = True

						if (iHealth != 0 and bHandled == False):
							if ( iHealth > 0 ):
								szTempBuffer = u"<font=1>+%d%c</font>" %( iHealth, CyGame().getSymbolID( FontSymbols.HEALTHY_CHAR ) )
							else:
								szTempBuffer = u"<font=1>+%d%c</font>" %( -iHealth, CyGame().getSymbolID(FontSymbols.UNHEALTHY_CHAR) )

							szName = "CenterBonusItemLeft" + str(iCenterCount)
							screen.setLabelAt( szName, "BonusBack1", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )
							szName = "CenterBonusItemRight" + str(iCenterCount)
							screen.setLabelAt( szName, "BonusBack1", szTempBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 62, (iCenterCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )

							iCenterCount = iCenterCount + 1

							bHandled = True

						szBuffer = u""
						if ( not bHandled ):

							szName = "LeftBonusItem" + str(iLeftCount)
							screen.setLabelAt( szName, "BonusBack0", szLeadBuffer, CvUtil.FONT_LEFT_JUSTIFY, 0, (iLeftCount * 20) + 4, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, i, -1 )

							iLeftCount = iLeftCount + 1

							bHandled = True

				g_iNumLeftBonus = iLeftCount
				g_iNumCenterBonus = iCenterCount
				g_iNumRightBonus = iRightCount

				iMaintenance = pHeadSelectedCity.getMaintenanceTimes100() - int(pHeadSelectedCity.getProximityGold() * 100)

				szBuffer = localText.getText("INTERFACE_CITY_MAINTENANCE", ())

				screen.setLabel( "MaintenanceText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 116, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				screen.show( "MaintenanceText" )

				szBuffer = u"%d.%02d %c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())
				screen.setLabel( "MaintenanceAmountText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 220, 115, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_MAINTENANCE, -1, -1 )
				screen.show( "MaintenanceAmountText" )

				if not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_CRIME):
					szBuffer = u""
					iCrime = pHeadSelectedCity.getCrime()
					szBuffer = localText.getText("TXT_KEY_CITY_BAR_CRIME", (iCrime, pHeadSelectedCity.getCrimePerTurn()))
	
					screen.setLabel( "CrimeText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, 15, 136, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_CRIME, -1, -1 )
					screen.show( "CrimeText" )

			#	szBuffer = u"%d (%d /turn)" %(iCrime)
			#	screen.setLabel( "CrimeAmountText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 200, 145, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			#	screen.show( "CrimeAmountText" )

				szBuffer = u""

				for i in xrange(gc.getNumReligionInfos()):
					xCoord = xResolution - 242 + (i * 26)
					yCoord = 42

					bEnable = True

					if (pHeadSelectedCity.isHasReligion(i)):

#FfH: Added by Kael 11/03/2007
						if (gc.getPlayer(gc.getGame().getActivePlayer()).canSeeReligion(i)):
#FfH: End Add

							if (pHeadSelectedCity.isHolyCityByType(i)):
								szTempBuffer = u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
								szName = "ReligionHolyCityDDS" + str(i)
								screen.show( szName )
							else:
								szTempBuffer = u"%c" %(gc.getReligionInfo(i).getChar())
							szBuffer = szBuffer + szTempBuffer

						j = 0
						for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
							iCommerce = pHeadSelectedCity.getReligionCommerceByReligion(j, i)

							if (iCommerce != 0):
								if ( iCommerce > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer

						iHappiness = pHeadSelectedCity.getReligionHappiness(i)

						if (iHappiness != 0):
							if ( iHappiness > 0 ):
								szTempBuffer = u",+%d%c" %(iHappiness, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR) )
								szBuffer = szBuffer + szTempBuffer
							else:
								szTempBuffer = u",+%d%c" %(-(iHappiness), CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR) )
								szBuffer = szBuffer + szTempBuffer

						szBuffer = szBuffer + " "

						szButton = gc.getReligionInfo(i).getButton()

					else:

						bEnable = False
						szButton = gc.getReligionInfo(i).getButton()

					szName = "ReligionDDS" + str(i)
					screen.setImageButton( szName, szButton, xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_RELIGION_CITY, i, -1 )
					screen.enable( szName, bEnable )
					screen.show( szName )

				for i in xrange(gc.getNumCorporationInfos()):
					xCoord = xResolution - 248 + (i * 23)
					yCoord = 70

					bEnable = True

					if (pHeadSelectedCity.isHasCorporation(i)):
						if (pHeadSelectedCity.isHeadquartersByType(i)):
							szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
							szName = "CorporationHeadquarterDDS" + str(i)
							screen.show( szName )
						else:
							szTempBuffer = u"%c" %(gc.getCorporationInfo(i).getChar())
						szBuffer = szBuffer + szTempBuffer

						for j in xrange(YieldTypes.NUM_YIELD_TYPES):
							iYield = pHeadSelectedCity.getCorporationYieldByCorporation(j, i)

							if (iYield != 0):
								if ( iYield > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iYield, gc.getYieldInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iYield, gc.getYieldInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer

						for j in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
							iCommerce = pHeadSelectedCity.getCorporationCommerceByCorporation(j, i)

							if (iCommerce != 0):
								if ( iCommerce > 0 ):
									szTempBuffer = u",%s%d%c" %("+", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer
								else:
									szTempBuffer = u",%s%d%c" %( "", iCommerce, gc.getCommerceInfo(j).getChar() )
									szBuffer = szBuffer + szTempBuffer

						szBuffer += " "

						szButton = gc.getCorporationInfo(i).getButton()

					else:

						bEnable = False
						szButton = gc.getCorporationInfo(i).getButton()

					szName = "CorporationDDS" + str(i)
					screen.setImageButton( szName, szButton, xCoord, yCoord, 24, 24, WidgetTypes.WIDGET_HELP_CORPORATION_CITY, i, -1 )
					screen.enable( szName, bEnable )
					screen.show( szName )

				szBuffer = u"%d%% %s" %(pHeadSelectedCity.plot().calculateCulturePercent(pHeadSelectedCity.getOwner()), gc.getPlayer(pHeadSelectedCity.getOwner()).getCivilizationAdjective(0) )
				screen.setLabel( "NationalityText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 210, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.setHitTest( "NationalityText", HitTestTypes.HITTEST_NOHIT )
				screen.show( "NationalityText" )
				iRemainder = 0
				iWhichBar = 0
				for h in xrange( gc.getMAX_PLAYERS() ):
					if ( gc.getPlayer(h).isAlive() ):
						fPercent = pHeadSelectedCity.plot().calculateCulturePercent(h)
						if ( fPercent != 0 ):
							fPercent = fPercent / 100.0
							screen.setStackedBarColorsRGB( "NationalityBar", iWhichBar, gc.getPlayer(h).getPlayerTextColorR(), gc.getPlayer(h).getPlayerTextColorG(), gc.getPlayer(h).getPlayerTextColorB(), gc.getPlayer(h).getPlayerTextColorA() )
							if ( iRemainder == 1 ):
								screen.setBarPercentage( "NationalityBar", iWhichBar, fPercent )
							else:
								screen.setBarPercentage( "NationalityBar", iWhichBar, fPercent / ( 1 - iRemainder ) )
							iRemainder += fPercent
							iWhichBar += 1
				screen.show( "NationalityBar" )

				iDefenseModifier = pHeadSelectedCity.getDefenseModifier(False)

				if (iDefenseModifier != 0):
					szBuffer = localText.getText("TXT_KEY_MAIN_CITY_DEFENSE", (CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR), iDefenseModifier))

					if (pHeadSelectedCity.getDefenseDamage() > 0):
						szTempBuffer = u" (%d%%)" %( ( ( gc.getMAX_CITY_DEFENSE_DAMAGE() - pHeadSelectedCity.getDefenseDamage() ) * 100 ) / gc.getMAX_CITY_DEFENSE_DAMAGE() )
						szBuffer = szBuffer + szTempBuffer
					szNewBuffer = "<font=4>"
					szNewBuffer = szNewBuffer + szBuffer
					szNewBuffer = szNewBuffer + "</font>"
					screen.setLabel( "DefenseText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 270, 40, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_DEFENSE, -1, -1 )
					screen.show( "DefenseText" )

				if ( pHeadSelectedCity.getCultureLevel != CultureLevelTypes.NO_CULTURELEVEL ):
					iRate = pHeadSelectedCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
					if (iRate%100 == 0):
						szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), iRate/100))
					else:
						szRate = u"+%d.%02d" % (iRate/100, iRate%100)
						szBuffer = localText.getText("INTERFACE_CITY_COMMERCE_RATE_FLOAT", (gc.getCommerceInfo(CommerceTypes.COMMERCE_CULTURE).getChar(), gc.getCultureLevelInfo(pHeadSelectedCity.getCultureLevel()).getTextKey(), szRate))
					screen.setLabel( "CultureText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, 125, yResolution - 184, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "CultureText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "CultureText" )

				if ((pHeadSelectedCity.getGreatPeopleProgress() > 0) or (pHeadSelectedCity.getGreatPeopleRate() > 0)):
					szBuffer = localText.getText("INTERFACE_CITY_GREATPEOPLE_RATE", (CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR), pHeadSelectedCity.getGreatPeopleRate()))

					screen.setLabel( "GreatPeopleText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution - 146, yResolution - 176, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.setHitTest( "GreatPeopleText", HitTestTypes.HITTEST_NOHIT )
					screen.show( "GreatPeopleText" )

					iFirst = float(pHeadSelectedCity.getGreatPeopleProgress()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) )
					screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) )
					else:
						screen.setBarPercentage( "GreatPeopleBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pHeadSelectedCity.getGreatPeopleRate()) / float( gc.getPlayer( pHeadSelectedCity.getOwner() ).greatPeopleThreshold(false) ) ) ) / ( 1 - iFirst ) )
					screen.show( "GreatPeopleBar" )

				iFirst = float(pHeadSelectedCity.getCultureTimes100(pHeadSelectedCity.getOwner())) / float(100 * pHeadSelectedCity.getCultureThreshold())
				screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_STORED, iFirst )
				if ( iFirst == 1 ):
					screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_RATE, ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) )
				else:
					screen.setBarPercentage( "CultureBar", InfoBarTypes.INFOBAR_RATE, ( ( float(pHeadSelectedCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE)) / float(pHeadSelectedCity.getCultureThreshold()) ) ) / ( 1 - iFirst ) )
				screen.show( "CultureBar" )

		else:

			# Help Text Area
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ): #TODO Ronkhar augment width
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
			else:
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )

			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				self.setMinimapButtonVisibility(True)

		return 0
	# Will update the info pane strings
	def updateInfoPaneStrings( self ):

		global iNumUnitPromotions
		iNumUnitPromotions = 0
		iRow = 0

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.addPanel( "SelectedUnitPanel", u"", u"", True, False, 8, yResolution - 164, 200, 80, PanelStyles.PANEL_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitPanel", "Panel_Game_HudStat_Style" )
		screen.hide( "SelectedUnitPanel" )
		screen.addTableControlGFC( "SelectedUnitText", 3, 5, yResolution - 135, 280, 102, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
		screen.setStyle( "SelectedUnitText", "Table_EmptyScroll_Style" )
		screen.hide( "SelectedUnitText" )
		screen.hide( "SelectedUnitLabel" )
		screen.hide( "Stealth Icon" )
		screen.hide( "Unit UC" )
		screen.hide( "Unit HN" )
		screen.addTableControlGFC( "SelectedCityText", 3, 10, yResolution - 139, 220, 128, False, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD )
		screen.setStyle( "SelectedCityText", "Table_EmptyScroll_Style" )
		screen.hide( "SelectedCityText" )

		for i in xrange(iPromotionsPerPage):
			szName = "PromotionButton" + str(i)
			szName2 = szName + "Duration"
			szName3 = szName + "Quantity"
			screen.hide( szName )
			screen.hide( szName2 )
			screen.hide( szName3 )
		
		screen.hide( "PromotionScrollPlus" )
		screen.hide( "PromotionScrollMinus" )

		if CyEngine().isGlobeviewUp():
			return

		if (pHeadSelectedCity):

			iOrders = CyInterface().getNumOrdersQueued()
			iWidthMax = 0

			screen.setTableColumnHeader( "SelectedCityText", 0, u"", 10 )
			screen.setTableColumnHeader( "SelectedCityText", 1, u"", 200 )
			screen.setTableColumnHeader( "SelectedCityText", 2, u"", 10 )

			for i in xrange( iOrders ):

				szBuffer0 = u""
				szBuffer1 = u""

				if ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_TRAIN ):
					szBuffer0 += "(" + str(pHeadSelectedCity.getUnitProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"
					if (CyInterface().getOrderNodeSave(i)):
						szBuffer1 += u"*"
					szBuffer1 += gc.getUnitInfo(CyInterface().getOrderNodeData1(i)).getDescription()


				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONSTRUCT ):
					szBuffer0 += "(" + str(pHeadSelectedCity.getBuildingProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"
					szBuffer1 += gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getDescription()

				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CREATE ):
					szBuffer0 += "(" + str(pHeadSelectedCity.getProjectProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i)) + ")"
					szBuffer1 += gc.getProjectInfo(CyInterface().getOrderNodeData1(i)).getDescription()


				elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_MAINTAIN ):
					szBuffer1 += gc.getProcessInfo(CyInterface().getOrderNodeData1(i)).getDescription()

				iWidth0 = CyInterface().determineWidth(szBuffer0)
				if iWidth0 > iWidthMax:
					iWidthMax = iWidth0

				screen.appendTableRow( "SelectedCityText" )
				screen.setTableText( "SelectedCityText", 0, iRow, szBuffer0, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
				screen.setTableText( "SelectedCityText", 1, iRow, szBuffer1, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.show( "SelectedCityText" )
				iRow += 1

			screen.setTableColumnHeader( "SelectedCityText", 0, u"", iWidthMax + 15 )
			screen.setTableColumnHeader( "SelectedCityText", 1, u"", 195 - iWidthMax )

		elif (pHeadSelectedUnit and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):

			screen.setTableColumnHeader( "SelectedUnitText", 0, u"", 290 )
			screen.setTableColumnHeader( "SelectedUnitText", 1, u"", 5 )
			screen.setTableColumnHeader( "SelectedUnitText", 2, u"", 5 )
			screen.setTableColumnRightJustify( "SelectedUnitText", 1 )

			if (CyInterface().mirrorsSelectionGroup()):
				pSelectedGroup = pHeadSelectedUnit.getGroup()
			else:
				pSelectedGroup = 0

			if (CyInterface().getLengthSelectionList() > 1):

				screen.setText( "SelectedUnitLabel", "Background", localText.getText("TXT_KEY_UNIT_STACK", (CyInterface().getLengthSelectionList(), )), CvUtil.FONT_LEFT_JUSTIFY, 18, yResolution - 161, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )

				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					if (pHeadSelectedUnit):
						for i in xrange(gc.getNumUnitInfos()):
							iCount = CyInterface().countEntities(i)

							if (iCount > 0):
								szRightBuffer = u""

								szLeftBuffer = gc.getUnitInfo(i).getDescription()

								if (iCount > 1):
									szRightBuffer = u"(" + str(iCount) + u")"

								szBuffer = szLeftBuffer + u"  " + szRightBuffer
								screen.appendTableRow( "SelectedUnitText" )
								screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
								screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
								screen.show( "SelectedUnitText" )
								screen.show( "SelectedUnitPanel" )
								iRow += 1
			else:
				szBuffer	= ""
				xPos		= 12
				yPos		= yResolution - 161
				xOffset		= 24

				iUC = pHeadSelectedUnit.getUnitCombatType()
				if iUC != -1:
					szButton = gc.getUnitCombatInfo(iUC).getButton()

					screen.addDDSGFC( "Unit UC", szButton, xPos, yPos, 24, 24, WidgetTypes.WIDGET_PYTHON, 1008, -1 )

					screen.show( "Unit UC" )
					xPos += xOffset

				if pHeadSelectedUnit.getNumInvisibleTypes() > 0:
					if pHeadSelectedUnit.isRevealed():
						szButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_UNIT_REVEALED").getPath()
					else:
						szButton = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HIDDEN").getPath()

					screen.addDDSGFC( "Stealth Icon", szButton, xPos, yPos, 24, 24, WidgetTypes.WIDGET_PYTHON, 1006, -1 )

					screen.show( "Stealth Icon" )
					xPos += xOffset

				if pHeadSelectedUnit.isHiddenNationality():
					szButton = gc.getPromotionInfo(gc.getInfoTypeForString("PROMOTION_HIDDEN_NATIONALITY")).getButton()

					screen.addDDSGFC( "Unit HN", szButton, xPos, yPos, 24, 24, WidgetTypes.WIDGET_GENERAL, 1007, -1 )

					screen.show( "Unit HN" )
					xPos += xOffset

				iRel = pHeadSelectedUnit.getReligion()
				if iRel != -1:
					cRel = gc.getReligionInfo(iRel).getChar()
					szTempBuffer = u"%c" %(cRel)
					szBuffer += szTempBuffer

				if pHeadSelectedUnit.isRivalTerritory():
					cRT = CyGame().getSymbolID(FontSymbols.OPEN_BORDERS_CHAR)
					szTempBuffer = u"%c" %(cRT)
					szBuffer += szTempBuffer

				if (pHeadSelectedUnit.getHotKeyNumber() == -1):
					szBuffer += localText.getText("INTERFACE_PANE_UNIT_NAME", (pHeadSelectedUnit.getName(), ))
				else:
					szBuffer += localText.getText("INTERFACE_PANE_UNIT_NAME_HOT_KEY", (pHeadSelectedUnit.getHotKeyNumber(), pHeadSelectedUnit.getName()))
				if (len(szBuffer) > 50):
					print "len"
					print szBuffer
					print len(szBuffer)
					szBuffer = "<font=2>" + szBuffer + "</font>"

				screen.setText( "SelectedUnitLabel", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xPos, yPos - 2, -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )

				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					screen.show( "SelectedUnitText" )
					screen.show( "SelectedUnitPanel" )

					# [Level] [XP] [Movement] [Fortify]
					# [Combat] [HP] [Ranged] [MP] [Work Rate]

					szBuffer		= u""
					szColorStart	= ''
					szColorEnd		= ''
					bShortStr		= False
					bHurt			= pHeadSelectedUnit.isHurt()
					szSeparator		= "  |  "
					lRow1			= []
					lRow2			= []
					if bHurt:
						szColorStart = localText.getText('[COLOR_RED]',())
						szColorEnd = localText.getText('[COLOR_REVERT]',())

					# Combat Str
					if (pHeadSelectedUnit.canFight()):
						szHP = ''
						if not pHeadSelectedUnit.isFighting():
							iStrength = pHeadSelectedUnit.baseCombatStr()
							iDefStrength = pHeadSelectedUnit.baseCombatStrDefense()
							if iStrength == iDefStrength:
								bShortStr = True
							if bHurt:
								fCurrentHP = float(pHeadSelectedUnit.currHitPoints())
								fMaxHP = float(pHeadSelectedUnit.maxHitPoints())
								iStrength = float(iStrength) * (fCurrentHP / fMaxHP)
								iStrength = round(iStrength, 1)
								iDefStrength = float(iDefStrength) * (fCurrentHP / fMaxHP)
								iDefStrength = round(iDefStrength, 1)
							cStrength = CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR)
							if bShortStr:
								szCombat = szColorStart + u"%c%g" %(cStrength,iStrength) + szColorEnd
							else:
								szCombat = szColorStart + u"%c%g/%g" %(cStrength,iStrength,iDefStrength) + szColorEnd
							lRow2.append(szCombat)
					
					# HP + Regen
					iRegen = pHeadSelectedUnit.calcTurnHealthChangeReal()

					if (bHurt or iRegen < 0) and not pHeadSelectedUnit.isFighting():

						fCurrentHP = float(pHeadSelectedUnit.currHitPoints())
						fMaxHP = float(pHeadSelectedUnit.maxHitPoints())
						fHP = (fCurrentHP / fMaxHP) * 100
						fHP = round(fHP, 1)
						szHP = u" %g" %(fHP) + "%"
						szHP = szColorStart + szHP + szColorEnd
						
						iRegen = pHeadSelectedUnit.calcTurnHealthChangeReal()
						fRegen = (iRegen / fMaxHP) * 100
						fRegen = int(fRegen)
						szRegen = ""
						if fRegen < 0:
							szColorRegenStart = localText.getText('[COLOR_RED]',())
							szColorRegenEnd = localText.getText('[COLOR_REVERT]',())
							szRegen = szColorRegenStart + " (" + str(fRegen) + "%)" + szColorRegenEnd
						elif fRegen > 0:
							szColorRegenStart = localText.getText('[COLOR_POSITIVE_TEXT]',())
							szColorRegenEnd = localText.getText('[COLOR_REVERT]',())
							szRegen = szColorRegenStart + " (+" + str(fRegen) + "%)" + szColorRegenEnd
						szHP += szRegen
						lRow2.append(szHP)

					# Ranged Str
					if (pHeadSelectedUnit.airBaseCombatStr() > 0) and not pHeadSelectedUnit.isFighting():
						iRangedStrength = pHeadSelectedUnit.airBaseCombatStr()
						iRangedLimit = pHeadSelectedUnit.airCombatLimit()
						if bHurt:
							fCurrentHP = float(pHeadSelectedUnit.currHitPoints())
							fMaxHP = float(pHeadSelectedUnit.maxHitPoints())
							iRangedStrength = float(iRangedStrength) * (fCurrentHP / fMaxHP)
							iRangedStrength = round(iRangedStrength, 1)
						cRanged = CyGame().getSymbolID(FontSymbols.RANGED_CHAR)
						szRanged = szColorStart + u"%c%g" %(cRanged,iRangedStrength) + szColorEnd + u", %d%%" %(iRangedLimit)
						lRow2.append(szRanged)

					# Magical Power
					iMP = pHeadSelectedUnit.getMagicalPower()
					if iMP > 0:
						cMP = gc.getBonusInfo(gc.getInfoTypeForString("BONUS_MANA")).getChar()
						szMP = u"%c%d" %(cMP,iMP)
						lRow2.append(szMP)

					# Work Rate
					iWorkRate = pHeadSelectedUnit.workRate(True, -1, -1)
					if iWorkRate > 0:
						cWork = gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()
						szWorkRate = u"%c%d" %(cWork,iWorkRate)
						lRow2.append(szWorkRate)

					# Level
					iLevel = pHeadSelectedUnit.getLevel()
					szLevel = localText.getText("TXT_KEY_INTERFACE_LEVEL", (iLevel,))
					lRow1.append(szLevel)

					# XP
					fCurrentXP = pHeadSelectedUnit.getExperience()
					fNeededXP = pHeadSelectedUnit.experienceNeeded()
					szXP = localText.getText("TXT_KEY_INTERFACE_XP", ()) + u" %g/%g" %(fCurrentXP,fNeededXP)
					lRow1.append(szXP)

					# Movement
					fMoves = float(pHeadSelectedUnit.movesLeft())
					fCurrMoves = (fMoves / gc.getMOVE_DENOMINATOR())
					fCurrMoves = round(fCurrMoves, 2)
					iBase = pHeadSelectedUnit.baseMoves()
					cMoves = CyGame().getSymbolID(FontSymbols.MOVES_CHAR)
					if (pHeadSelectedUnit.baseMoves() == fCurrMoves):
						szMovement = u"%c%d" %(cMoves,iBase)
					else:
						szMovement = u"%c%g/%d" %(cMoves,fCurrMoves,iBase)
					lRow1.append(szMovement)

					# Fortify
					if pHeadSelectedUnit.fortifyModifier() > 0:
						iFort = pHeadSelectedUnit.fortifyModifier()
						cFort = CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR)
						szFortify = u"%c%d" %(cFort,iFort) + "%"
						lRow1.append(szFortify)

					for string in lRow1:
						if lRow1.index(string) != len(lRow1) - 1:
							szBuffer += string + szSeparator
						else:
							szBuffer += string

					iWidth = CyInterface().determineWidth(szBuffer)
					if iWidth > 260:
						szBuffer = "<font=1>" + szBuffer + "</font>"

					screen.appendTableRow( "SelectedUnitText" )
					screen.setTableText( "SelectedUnitText", 0, iRow, szBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, 0, -1, CvUtil.FONT_LEFT_JUSTIFY )
					iRow += 1
					szBuffer = u""

					for string in lRow2:
						if lRow2.index(string) != len(lRow2) - 1:
							szBuffer += string + szSeparator
						else:
							szBuffer += string

					iWidth = CyInterface().determineWidth(szBuffer)
					if iWidth > 260:
						szBuffer = "<font=1>" + szBuffer + "</font>"

					screen.appendTableRow( "SelectedUnitText" )
					screen.setTableText( "SelectedUnitText", 0, iRow, szBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, 0, -1, CvUtil.FONT_LEFT_JUSTIFY )
					iRow += 1
					szBuffer = u""

				iPromotionCount = 0
				lPromotionList = []
				for iPromotion in xrange(gc.getNumPromotionInfos()):
					iPromotionNext = gc.getPromotionInfo(iPromotion).getPromotionNextLevel()
					if not pHeadSelectedUnit.isHasPromotion(iPromotion):
						continue
					if gc.getPromotionInfo(iPromotion).isEffectProm():
						continue
					if iPromotionNext != -1 and pHeadSelectedUnit.isHasPromotion(iPromotionNext):
						continue

					lPromotionList.append(iPromotion)
					iPromotionCount += 1

				iNumUnitPromotions = iPromotionCount

				if lPromotionList:
					self.setPromotionButtons(lPromotionList, pHeadSelectedUnit)

			if (pSelectedGroup):

				iNodeCount = pSelectedGroup.getLengthMissionQueue()

				if (iNodeCount > 1):
					for i in xrange( iNodeCount ):
						szLeftBuffer = u""
						szRightBuffer = u""

						if (gc.getMissionInfo(pSelectedGroup.getMissionType(i)).isBuild()):
							if (i == 0):
								szLeftBuffer = gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription()
								szRightBuffer = localText.getText("INTERFACE_CITY_TURNS", (pSelectedGroup.plot().getBuildTurnsLeft(pSelectedGroup.getMissionData1(i), 0, 0), ))
							else:
								szLeftBuffer = u"%s..." %(gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription())
						else:
							szLeftBuffer = u"%s..." %(gc.getMissionInfo(pSelectedGroup.getMissionType(i)).getDescription())

						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow( "SelectedUnitText" )
						screen.setTableText( "SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText( "SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show( "SelectedUnitText" )
						screen.show( "SelectedUnitPanel" )
						iRow += 1

		return 0

	# Will update the scores
	def updateScoreStrings( self ):
		global iScoreState
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		screen.hide( "ScoreBackground" )
		screen.hide( "ScoreToggle" )
		screen.hide( "CutLosersTag" )
		screen.hide( "DifficultyTag" )
		screen.hide( "HighToLowTag" )
		screen.hide( "DisableProductionTag" )
		screen.hide( "DisableResearchTag" )
#StasisRework Addition by Klauros
		screen.hide( "StasisTag" )
#End StasisRework Addition
		screen.hide( "DisableSpellcastingTag" )
		for i in xrange( gc.getMAX_PLAYERS() ):
			screen.hide( "ScoreText" + str(i) )
		if CyGame().getWBMapScript():
			screen.hide( "GoalTag" )

		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL: return
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY: return
		if not CyInterface().isScoresVisible(): return
		if CyInterface().isCityScreenUp(): return
		if CyEngine().isGlobeviewUp(): return

		xResolution		= screen.getXResolution()
		yResolution		= screen.getYResolution()
		git				= gc.getInfoTypeForString
		iWidth			= 0
		iRow			= 0
		iRowSpecial		= 0
		iBtnHeight		= 22
		iY				= yResolution - 206
		iX				= xResolution - 18
		iActiveTeam		= gc.getGame().getActiveTeam()
		iActivePlayer	= gc.getGame().getActivePlayer()
		pActivePlayer	= gc.getPlayer(iActivePlayer)
		bDebug = False
		if CyGame().isDebugMode():
			bDebug = True
		bEyesEars = False
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			iLoopTeam = pLoopPlayer.getTeam()
			if iLoopTeam == iActiveTeam and pLoopPlayer.getNumBuilding(git('BUILDING_EYES_AND_EARS_NETWORK')) > 0:
				bEyesEars = True

		lMasters = []
		lVassals = []
		lPlayers = []
		if iScoreState == 2:
			lPlayers.append(iActivePlayer)
		else:
			for iPlayerX in xrange(gc.getMAX_CIV_PLAYERS()):
				pPlayerX = gc.getPlayer(iPlayerX)
				if pPlayerX.isAlive() and not pPlayerX.isMinorCiv():
					iTeamX = pPlayerX.getTeam()
					pTeamX = gc.getTeam(iTeamX)
					if pTeamX.isHasMet(iActiveTeam) or bDebug:
						if pTeamX.isAVassal():
							for iTeamY in xrange(gc.getMAX_CIV_TEAMS()):
								if pTeamX.isVassal(iTeamY):
									lVassals.append([CyGame().getTeamRank(iTeamY), CyGame().getTeamRank(iTeamX), CyGame().getPlayerRank(iPlayerX), iPlayerX])
									break
						else:
							lMasters.append([CyGame().getTeamRank(iTeamX), CyGame().getPlayerRank(iPlayerX), iPlayerX])
		lMasters.sort()
		lVassals.sort()
		for i in xrange(len(lMasters)):
			lPlayers.append(lMasters[i][2])
			if i < len(lMasters) - 1 and lMasters[i][0] == lMasters[i + 1][0]: continue
			for j in lVassals:
				if j[0] == lMasters[i][0]:
					lPlayers.append(j[3])
				elif j[0] > lMasters[i][0]:
					break
		lPlayers.reverse()

		screen.setButtonGFC( "ScoreToggle", u"", "", iX, iY, 18,18, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
		screen.show("ScoreToggle")

		for iPlayer in lPlayers:
			pPlayer	= gc.getPlayer(iPlayer)
			iTeam	= pPlayer.getTeam()
			pTeam	= gc.getTeam(iTeam)
			szName	= "ScoreText" + str(iPlayer)
			szColorStart	= u"<color=%d,%d,%d,%d>" %(pPlayer.getPlayerTextColorR(), pPlayer.getPlayerTextColorG(), pPlayer.getPlayerTextColorB(), pPlayer.getPlayerTextColorA())
			szColorEnd		= u"</color>"
			if iPlayer == iActivePlayer:
				szColorStart	= u"[" + szColorStart
				szColorEnd		+= u"]"
			szPlayerString	= u"<font=2>"
			szScore			= str(gc.getGame().getPlayerScore(iPlayer)) + ": "
			if g_bScoreShowStateName and iScoreState != 1:
				szPlayerName = pPlayer.getStateName()
				# Reminder to change to Secondary Leader when they are added
				if pPlayer.getLeaderType() == git('LEADER_KOUN'):
					szPlayerName += u" %c" %(CyGame().getSymbolID(FontSymbols.GREAT_PEOPLE_CHAR))
			else:
				szPlayerName = pPlayer.getName()

			if gc.getGame().isNetworkMultiPlayer() and not pPlayer.isTurnActive():
				szPlayerString += "*"
			elif gc.getGame().isHotSeat and iPlayer < iActivePlayer:
				szPlayerString += "*"
			szPlayerString += szScore
			szPlayerString += szColorStart
			szPlayerString += szPlayerName
			szPlayerString += szColorEnd
			if not pTeam.isHasMet(iActiveTeam):
				szPlayerString += " ?"
			elif not pPlayer.isHuman():
				szAttitudeChar = ""
				iAttitude = pPlayer.AI_getAttitude(iActivePlayer)
				if iAttitude == AttitudeTypes.ATTITUDE_FURIOUS:
					szAttitudeChar = u"%c" %(CyGame().getSymbolID(FontSymbols.FURIOUS_CHAR))
				elif iAttitude == AttitudeTypes.ATTITUDE_ANNOYED:
					szAttitudeChar = u"%c" %(CyGame().getSymbolID(FontSymbols.ANNOYED_CHAR))
				elif iAttitude == AttitudeTypes.ATTITUDE_CAUTIOUS:
					szAttitudeChar = u"%c" %(CyGame().getSymbolID(FontSymbols.CAUTIOUS_CHAR))
				elif iAttitude == AttitudeTypes.ATTITUDE_PLEASED:
					szAttitudeChar = u"%c" %(CyGame().getSymbolID(FontSymbols.PLEASED_CHAR))
				elif iAttitude == AttitudeTypes.ATTITUDE_FRIENDLY:
					szAttitudeChar = u"%c" %(CyGame().getSymbolID(FontSymbols.FRIENDLY_CHAR))
				szPlayerString += szAttitudeChar
			if pTeam.isAtWar(iActiveTeam):
				szPlayerString += "("  + localText.getColorText("TXT_KEY_CONCEPT_WAR", (), git("COLOR_NEGATIVE_TEXT")).upper() + ")"
			if pPlayer.canTradeNetworkWith(iActivePlayer) and (iPlayer != iActivePlayer):
				szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
				szPlayerString += szTempBuffer
			if pTeam.isOpenBorders(iActiveTeam):
				szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.OPEN_BORDERS_CHAR))
				szPlayerString += szTempBuffer
			if pTeam.isDefensivePact(iActiveTeam):
				szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR))
				szPlayerString += szTempBuffer
			if not (pTeam.isAtWar(gc.getORC_TEAM())):
				szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.ORC_CHAR))
				szPlayerString += szTempBuffer
			if not (pTeam.isAtWar(gc.getDEMON_TEAM())):
				szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.DEMON_CHAR))
				szPlayerString += szTempBuffer
			if not (pTeam.isAtWar(gc.getANIMAL_TEAM())):
				szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.ANIMAL_CHAR))
				szPlayerString += szTempBuffer
			if pTeam.getBlockBonuses() > 0:
				if iTeam == iActiveTeam or bDebug:
					szTempBuffer = u"%c(%d)" %(CyGame().getSymbolID(FontSymbols.BAD_FOOD_CHAR), pTeam.getBlockBonuses())
				else:
					szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.BAD_FOOD_CHAR))
				szPlayerString += szTempBuffer
			if pTeam.getRevealAllBonuses() > 0:
				if iTeam == iActiveTeam or bDebug:
					szTempBuffer = u"%c(%d)" %(gc.getBonusInfo(git('BONUS_MANA_NATURE')).getChar(), pTeam.getRevealAllBonuses())
				else:
					szTempBuffer = u"%c" %(gc.getBonusInfo(git('BONUS_MANA_NATURE')).getChar())
				szPlayerString += szTempBuffer
			if pPlayer.isHideUnits():
				if (iTeam == iActiveTeam or bDebug) and pTeam.getHideUnits() > 0:
					szTempBuffer = u"%c(%d)" %(gc.getBonusInfo(git('BONUS_MANA_SHADOW')).getChar(), pTeam.getHideUnits())
				else:
					szTempBuffer = u"%c" %(gc.getBonusInfo(git('BONUS_MANA_SHADOW')).getChar())
				szPlayerString += szTempBuffer
			if pPlayer.isSeeInvisible():
				if (iTeam == iActiveTeam or bDebug) and pTeam.getSeeInvisible() > 0:
					szTempBuffer = u"%c(%d)" %(gc.getBonusInfo(git('BONUS_MANA_SUN')).getChar(), pTeam.getSeeInvisible())
				else:
					szTempBuffer = u"%c" %(gc.getBonusInfo(git('BONUS_MANA_SUN')).getChar())
				szPlayerString += szTempBuffer
			if pPlayer.getStateReligion() != -1 and (pActivePlayer.canSeeReligion(pPlayer.getStateReligion()) or bDebug):
				if pPlayer.hasHolyCity(pPlayer.getStateReligion()):
					szTempBuffer = u"%c" %(gc.getReligionInfo(pPlayer.getStateReligion()).getHolyCityChar())
				else:
					szTempBuffer = u"%c" %(gc.getReligionInfo(pPlayer.getStateReligion()).getChar())
				szPlayerString += szTempBuffer
			if iScoreState != 1:
				iAlignment	= pPlayer.getAlignment()
				iEAlignment	= pPlayer.getEthicalAlignment()
				lAlignment	= [git("ALIGNMENT_EVIL"), git("ALIGNMENT_GOOD"), git("ALIGNMENT_NEUTRAL")]
				lEAlignment	= [git("ETHICAL_ALIGNMENT_CHAOTIC"), git("ETHICAL_ALIGNMENT_LAWFUL"), git("ETHICAL_ALIGNMENT_NEUTRAL")]
				lColor		= [git("COLOR_RED"), git("COLOR_YELLOW"), git("COLOR_GREY")]
				lStrAlignment	= [	"TXT_KEY_ALIGNMENT_CHAOTIC_EVIL",	"TXT_KEY_ALIGNMENT_CHAOTIC_GOOD",	"TXT_KEY_ALIGNMENT_CHAOTIC_NEUTRAL",
									"TXT_KEY_ALIGNMENT_LAWFUL_EVIL",	"TXT_KEY_ALIGNMENT_LAWFUL_GOOD",	"TXT_KEY_ALIGNMENT_LAWFUL_NEUTRAL",
									"TXT_KEY_ALIGNMENT_NEUTRAL_EVIL",	"TXT_KEY_ALIGNMENT_NEUTRAL_GOOD",	"TXT_KEY_ALIGNMENT_NEUTRAL_NEUTRAL"]
				for i in lAlignment:
					if iAlignment == i:
						for j in lEAlignment:
							if iEAlignment == j:
								index = lAlignment.index(i) + lEAlignment.index(j) * 3
								szTempBuffer = " (" + localText.getColorText(lStrAlignment[index], (), lColor[lAlignment.index(i)]) + ")"
								szPlayerString += szTempBuffer
			szTempBuffer = u""
			if pPlayer.getLeaderStatus() == git('HISTORICAL_STATUS'):
				szTempBuffer = u" %c" %(CyGame().getSymbolID(FontSymbols.HISTORICAL_CHAR))
			elif pPlayer.getLeaderStatus() == git('IMPORTANT_STATUS'):
				szTempBuffer = u" %c" %(CyGame().getSymbolID(FontSymbols.IMPORTANT_CHAR))
			elif pPlayer.getLeaderStatus() == git('EMERGENT_STATUS'):
				szTempBuffer = u" %c" %(CyGame().getSymbolID(FontSymbols.EMERGENT_CHAR))
			szPlayerString += szTempBuffer
			if bEyesEars or bDebug or (iTeam == iActiveTeam and gc.getTeam(iActiveTeam).getNumMembers() > 1) or pTeam.isVassal(iActiveTeam):
				if pPlayer.getCurrentResearch() != -1:
					szPlayerString += u"-%s (%d)" %(gc.getTechInfo(pPlayer.getCurrentResearch()).getDescription(), pPlayer.getResearchTurnsLeft(pPlayer.getCurrentResearch(), True))
			if CyGame().isNetworkMultiPlayer():
				szPlayerString += CyGameTextMgr().getNetStats(iPlayer)
			if pPlayer.isHuman() and CyInterface().isOOSVisible():
				szPlayerString += u" <color=255,0,0>* %s *</color>" %(CyGameTextMgr().getOOSSeeds(iPlayer))

			if CyInterface().determineWidth(szPlayerString) > iWidth:
				iWidth = CyInterface().determineWidth(szPlayerString)

			screen.setText( szName, "Background", szPlayerString, CvUtil.FONT_RIGHT_JUSTIFY, iX, iY - (iRow * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_CONTACT_CIV, iPlayer, -1 )
			screen.show( szName )
			iRow += 1

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_INCREASING_DIFFICULTY) or gc.getGame().isOption(GameOptionTypes.GAMEOPTION_FLEXIBLE_DIFFICULTY):
			iRowSpecial += 1
			szName = "DifficultyTag"
			szBuffer = u"<font=2>" + localText.getColorText("TXT_KEY_MESSAGE_DIFFICULTY", (gc.getHandicapInfo(pActivePlayer.getHandicapType()).getDescription(), ()), gc.getInfoTypeForString("COLOR_RED")) + "</font>"
			screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iX, iY - ((iRow + iRowSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( szName )
		if (gc.getGame().isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_CUT_LOSERS) or gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT)) and gc.getGame().countCivPlayersAlive() > 5:
			iRowSpecial += 1
			szName = "CutLosersTag"
			szBuffer = u"<font=2>" + localText.getColorText("TXT_KEY_MESSAGE_CUT_LOSERS", (50 * gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent() - gc.getGame().getCutLosersCounter(), ()), gc.getInfoTypeForString("COLOR_RED")) + "</font>"
			screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iX, iY - ((iRow + iRowSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( szName )
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_HIGH_TO_LOW):
			iRowSpecial += 1
			szName = "HighToLowTag"
			szBuffer = u"<font=2>"
			if gc.getGame().getHighToLowCounter() == 0:
				szBuffer += localText.getColorText("TXT_KEY_MESSAGE_HIGH_TO_LOW_GOAL_0", (), gc.getInfoTypeForString("COLOR_RED"))
			elif gc.getGame().getHighToLowCounter() == 1:
				szBuffer += localText.getColorText("TXT_KEY_MESSAGE_HIGH_TO_LOW_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			elif gc.getGame().getHighToLowCounter() > 1:
				szBuffer += localText.getColorText("TXT_KEY_MESSAGE_HIGH_TO_LOW_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))
			szBuffer += "</font>"
			screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iX, iY - ((iRow + iRowSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( szName )
		if CyGame().getWBMapScript():
			iRowSpecial += 1
			szName = "GoalTag"
			szBuffer = sf.getGoalTag(pActivePlayer)
			screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iX, iY - ((iRow + iRowSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( szName )
		if pActivePlayer.getDisableProduction() > 0:
			iRowSpecial += 1
			szName = "DisableProductionTag"
			szBuffer = u"<font=2>" + localText.getColorText("TXT_KEY_MESSAGE_DISABLE_PRODUCTION", (pActivePlayer.getDisableProduction(), ()), gc.getInfoTypeForString("COLOR_RED")) + "</font>"
			screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iX, iY - ((iRow + iRowSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( szName )
		if pActivePlayer.getDisableResearch() > 0:
			iRowSpecial += 1
			szName = "DisableResearchTag"
			szBuffer = u"<font=2>" + localText.getColorText("TXT_KEY_MESSAGE_DISABLE_RESEARCH", (pActivePlayer.getDisableResearch(), ()), gc.getInfoTypeForString("COLOR_RED")) + "</font>"
			screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iX, iY - ((iRow + iRowSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( szName )
#StasisRework Addition by Klauros
		if pActivePlayer.getRemainingStasisTurns() > 0:
			iRowSpecial += 1
			szName = "StasisTag"
			szBuffer = u"<font=2>" + localText.getColorText("TXT_KEY_MESSAGE_STASIS_TURNS_REMAINING", (pActivePlayer.getRemainingStasisTurns(), ()), gc.getInfoTypeForString("COLOR_RED")) + "</font>"
			screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iX, iY - ((iRow + iRowSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( szName )
#End StasisRework Addition
		if pActivePlayer.getDisableSpellcasting() > 0:
			iRowSpecial += 1
			szName = "DisableSpellcastingTag"
			szBuffer = u"<font=2>" + localText.getColorText("TXT_KEY_MESSAGE_DISABLE_SPELLCASTING", (pActivePlayer.getDisableSpellcasting(), ()), gc.getInfoTypeForString("COLOR_RED")) + "</font>"
			screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, iX, iY - ((iRow + iRowSpecial) * iBtnHeight), -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.show( szName )

		screen.setPanelSize( "ScoreBackground", iX - iWidth - 10, iY - (iBtnHeight * (iRow - 1)) - 4, iWidth + 22, (iBtnHeight * iRow) + 8 )
		screen.show( "ScoreBackground" )

#FfH: Added by Kael 10/29/2007
	def updateManaStrings( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		global ishowManaBar

		screen.hide( "ManaBackground" )
		screen.hide( "ArchosBroodActivityBackground" )

		iWidth = 0
		iCount = 0
		iBtnHeight = 18
		
		yCoord = 93

		if (ishowManaBar == 0):
			for szBonus in strategicTypes1:
				szName = "StrategicText" + szBonus
				screen.hide( szName )
			for szBonus in strategicTypes2:
				szName = "StrategicText" + szBonus
				screen.hide( szName )
			for szBonus in manaTypes1:
				szName = "ManaText" + szBonus
				screen.hide( szName )
			for szBonus in manaTypes2:
				szName = "ManaText" + szBonus
				screen.hide( szName )
			for szBonus in luxuryTypes1:
				szName = "LuxuryText" + szBonus
				screen.hide( szName )
			for szBonus in luxuryTypes2:
				szName = "LuxuryText" + szBonus
				screen.hide( szName )
			for szBonus in healthTypes1:
				szName = "HealthText" + szBonus
				screen.hide( szName )
			for szBonus in healthTypes2:
				szName = "HealthText" + szBonus
				screen.hide( szName )

		if (ishowManaBar == 1):
			if (CyInterface().isScoresVisible() and not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyEngine().isGlobeviewUp() == false and ishowManaBar == 1) and not CyGame().GetWorldBuilderMode():
				for szBonus in manaTypes1:
					iBonus = gc.getInfoTypeForString(szBonus)
					szBuffer = u"<font=2>"
					szTempBuffer = u"%c: %d" %(gc.getBonusInfo(iBonus).getChar(), pPlayer.getNumAvailableBonuses(iBonus))
					szBuffer = szBuffer + szTempBuffer
					szBuffer = szBuffer + "</font>"
					if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
						iWidth = CyInterface().determineWidth( szBuffer )
					szName = "ManaText" + szBonus
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 40, yCoord + (iCount * iBtnHeight) + 24, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1 )
					screen.show( szName )
					iCount = iCount + 1
				iCount = 0
				for szBonus in manaTypes2:
					iBonus = gc.getInfoTypeForString(szBonus)
					szBuffer = u"<font=2>"
					szTempBuffer = u"%c: %d" %(gc.getBonusInfo(iBonus).getChar(), pPlayer.getNumAvailableBonuses(iBonus))
					szBuffer = szBuffer + szTempBuffer
					szBuffer = szBuffer + "</font>"
					if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
						iWidth = CyInterface().determineWidth( szBuffer )
					szName = "ManaText" + szBonus
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 80, yCoord + (iCount * iBtnHeight) + 24, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1 )
					screen.show( szName )
					iCount = iCount + 1
				screen.setPanelSize( "ManaBackground", 6, yCoord + 18, (iWidth * 2) + 12, (iBtnHeight * 11) + 12 )
				screen.show( "ManaBackground" )
				self.showArchosBroodActivityBackground()
		if (ishowManaBar == 2):
			for szBonus in manaTypes1:
				szName = "ManaText" + szBonus
				screen.hide( szName )
			for szBonus in manaTypes2:
				szName = "ManaText" + szBonus
				screen.hide( szName )

			if (CyInterface().isScoresVisible() and not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyEngine().isGlobeviewUp() == false and ishowManaBar == 2) and not CyGame().GetWorldBuilderMode():
				for szBonus in luxuryTypes1:
					iBonus = gc.getInfoTypeForString(szBonus)
					szBuffer = u"<font=2>"
					szTempBuffer = u"%c: %d" %(gc.getBonusInfo(iBonus).getChar(), pPlayer.getNumAvailableBonuses(iBonus))
					szBuffer = szBuffer + szTempBuffer
					szBuffer = szBuffer + "</font>"
					if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
						iWidth = CyInterface().determineWidth( szBuffer )
					szName = "LuxuryText" + szBonus
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 40, yCoord + (iCount * iBtnHeight) + 24, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1 )
					screen.show( szName )
					iCount = iCount + 1
				iCount = 0
				for szBonus in luxuryTypes2:
					iBonus = gc.getInfoTypeForString(szBonus)
					szBuffer = u"<font=2>"
					szTempBuffer = u"%c: %d" %(gc.getBonusInfo(iBonus).getChar(), pPlayer.getNumAvailableBonuses(iBonus))
					szBuffer = szBuffer + szTempBuffer
					szBuffer = szBuffer + "</font>"
					if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
						iWidth = CyInterface().determineWidth( szBuffer )
					szName = "LuxuryText" + szBonus
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 80, yCoord + (iCount * iBtnHeight) + 24, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1 )
					screen.show( szName )
					iCount = iCount + 1
				screen.setPanelSize( "ManaBackground", 6, yCoord + 18, (iWidth * 2) + 12, (iBtnHeight * 11) + 12 )
				screen.show( "ManaBackground" )
				self.showArchosBroodActivityBackground()
		if (ishowManaBar == 3):
			for szBonus in luxuryTypes1:
				szName = "LuxuryText" + szBonus
				screen.hide( szName )
			for szBonus in luxuryTypes2:
				szName = "LuxuryText" + szBonus
				screen.hide( szName )

			if (CyInterface().isScoresVisible() and not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyEngine().isGlobeviewUp() == false and ishowManaBar == 3) and not CyGame().GetWorldBuilderMode():
				for szBonus in healthTypes1:
					iBonus = gc.getInfoTypeForString(szBonus)
					szBuffer = u"<font=2>"
					szTempBuffer = u"%c: %d" %(gc.getBonusInfo(iBonus).getChar(), pPlayer.getNumAvailableBonuses(iBonus))
					szBuffer = szBuffer + szTempBuffer
					szBuffer = szBuffer + "</font>"
					if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
						iWidth = CyInterface().determineWidth( szBuffer )
					szName = "HealthText" + szBonus
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 40, yCoord + (iCount * iBtnHeight) + 24, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1 )
					screen.show( szName )
					iCount = iCount + 1
				iCount = 0
				for szBonus in healthTypes2:
					iBonus = gc.getInfoTypeForString(szBonus)
					szBuffer = u"<font=2>"
					szTempBuffer = u"%c: %d" %(gc.getBonusInfo(iBonus).getChar(), pPlayer.getNumAvailableBonuses(iBonus))
					szBuffer = szBuffer + szTempBuffer
					szBuffer = szBuffer + "</font>"
					if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
						iWidth = CyInterface().determineWidth( szBuffer )
					szName = "HealthText" + szBonus
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 80, yCoord + (iCount * iBtnHeight) + 24, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1 )
					screen.show( szName )
					iCount = iCount + 1
				screen.setPanelSize( "ManaBackground", 6, yCoord + 18, (iWidth * 2) + 12, (iBtnHeight * 11) + 12 )
				screen.show( "ManaBackground" )
				self.showArchosBroodActivityBackground()
		if (ishowManaBar == 4):
			for szBonus in healthTypes1:
				szName = "HealthText" + szBonus
				screen.hide( szName )
			for szBonus in healthTypes2:
				szName = "HealthText" + szBonus
				screen.hide( szName )

			if (CyInterface().isScoresVisible() and not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyEngine().isGlobeviewUp() == false and ishowManaBar == 4) and not CyGame().GetWorldBuilderMode():
				for szBonus in strategicTypes1:
					iBonus = gc.getInfoTypeForString(szBonus)
					szBuffer = u"<font=2>"
					szTempBuffer = u"%c: %d" %(gc.getBonusInfo(iBonus).getChar(), pPlayer.getNumAvailableBonuses(iBonus))
					szBuffer = szBuffer + szTempBuffer
					szBuffer = szBuffer + "</font>"
					if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
						iWidth = CyInterface().determineWidth( szBuffer )
					szName = "StrategicText" + szBonus
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 40, yCoord + (iCount * iBtnHeight) + 24, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1 )
					screen.show( szName )
					iCount = iCount + 1
				iCount = 0
				for szBonus in strategicTypes2:
					iBonus = gc.getInfoTypeForString(szBonus)
					szBuffer = u"<font=2>"
					szTempBuffer = u"%c: %d" %(gc.getBonusInfo(iBonus).getChar(), pPlayer.getNumAvailableBonuses(iBonus))
					szBuffer = szBuffer + szTempBuffer
					szBuffer = szBuffer + "</font>"
					if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
						iWidth = CyInterface().determineWidth( szBuffer )
					szName = "StrategicText" + szBonus
					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, 80, yCoord + (iCount * iBtnHeight) + 24, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iBonus, -1 )
					screen.show( szName )
					iCount = iCount + 1
				screen.setPanelSize( "ManaBackground", 6, yCoord + 18, (iWidth * 2) + 12, (iBtnHeight * 11) + 12 )
				screen.show( "ManaBackground" )
				self.showArchosBroodActivityBackground()
	
	def showArchosBroodActivityBackground( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		if gc.getInfoTypeForString('MODULE_ARACHNOPHOBIA')!=-1 and pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ARCHOS') and pPlayer.getNumCities() > 0:
			screen.setPanelSize( "ArchosBroodActivityBackground", 6, 321, 100, 52 )
			screen.show( "ArchosBroodActivityBackground" )

	def updatexUPT( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())

		iWidth = 0
		iCount = 0
		iBtnHeight = 18

		yCoord = 63
		if (not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyEngine().isGlobeviewUp() == false):
			szBuffer = u"<font=2>"
			szTempBuffer = u"%d" %(CyGame().getUPT())
			szBuffer = szBuffer + szTempBuffer
			szBuffer = szBuffer + "</font>"
			if ( CyInterface().determineWidth( szBuffer ) > iWidth ):
				iWidth = CyInterface().determineWidth( szBuffer )
			szName = "xUPT"
			screen.setText( szName, "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution - (24 - (iWidth / 2)), 76, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setHitTest( szName, HitTestTypes.HITTEST_NOHIT )
			screen.show( szName )
#FfH: End Add

	# Will update the help Strings
	def updateHelpStrings( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL ):
			screen.setHelpTextString( "" )
		else:
			screen.setHelpTextString( CyInterface().getHelpString() )

		return 0

	# Will set the promotion button position
	def setPromotionButtons( self, lPromotionList, pHeadSelectedUnit):
		global iPromotionPage
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		yResolution = screen.getYResolution()

		if len(lPromotionList) > iPromotionsPerPage:
			screen.show( "PromotionScrollPlus" )
			screen.moveToFront( "PromotionScrollPlus" )
			screen.show( "PromotionScrollMinus" )
			screen.moveToFront( "PromotionScrollMinus" )

		if len(lPromotionList) < (iPromotionPage - 1) * iPromotionsPerPage:
			iPromotionPage = 1

		offset			= 24
		xStartingPos	= 25
		yStartingPos	= yResolution - 80
		iPromotionCount = 0
		iNumPromColumn	= 10
		iNumPromRow		= 3

		if iPromotionPage == 1 and len(lPromotionList) <= iPromotionsPerPage:
			xStartingPos	= 4
			iNumPromColumn	= 11

		iPromotionCount = 0
		for iPromotion in lPromotionList:
			if ((iPromotionPage - 1) * iPromotionsPerPage) <= iPromotionCount < (iPromotionPage * iPromotionsPerPage):
				xPos	= iPromotionCount % iNumPromColumn * offset + xStartingPos
				yPos	= ( iPromotionCount / iNumPromColumn ) % iNumPromRow * offset + yStartingPos
				szName		= "PromotionButton" + str(iPromotionCount % iPromotionsPerPage)
				szName2		= szName + "Duration"
				szName3		= szName + "Quantity"
				szArtPath	= gc.getPromotionInfo(iPromotion).getButton()
				iDuration	= pHeadSelectedUnit.getPromotionDuration(iPromotion)
				iQuantity	= pHeadSelectedUnit.countHasPromotion(iPromotion)

				screen.addDDSGFC( szName, szArtPath, xPos, yPos, 26, 26, WidgetTypes.WIDGET_ACTION, gc.getPromotionInfo(iPromotion).getActionInfoIndex(), -1 )
				screen.moveToFront( szName )

				if iDuration > 0:
					screen.setText( szName2, "Background", str(iDuration), CvUtil.FONT_RIGHT_JUSTIFY, xPos + 12, yPos + 3, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.moveToFront( szName2 )
					screen.show( szName2 )

				if iQuantity > 1:
					screen.setText( szName3, "Background", str(iQuantity), CvUtil.FONT_RIGHT_JUSTIFY, xPos + 12, yPos + 6, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.moveToFront( szName3 )
					screen.show( szName3 )

			iPromotionCount += 1

	# Will set the selection button position
	def setResearchButtonPosition( self, szButtonID, iCount ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()

#FfH: Modified by Kael 07/17/2008
#		screen.moveItem( szButtonID, 287 + ( ( xResolution - 1024 ) / 2 ) + ( 34 * ( iCount % 15 ) ), 0 + ( 34 * ( iCount / 15 ) ), -0.3 )
		iTechIcons = (xResolution - 574) / 32
		screen.moveItem( szButtonID, 282 + ( 32 * ( iCount % iTechIcons ) ), 0 + ( 32 * ( iCount / iTechIcons ) ), -0.3 )
#FfH: End Modify

	# Will set the selection button position
	def setScoreTextPosition( self, szButtonID, iWhichLine ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		yResolution = screen.getYResolution()
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			yCoord = yResolution - 180
		else:
			yCoord = yResolution - 88
		screen.moveItem( szButtonID, 996, yCoord - (iWhichLine * 18), -0.3 )

	# Will build the globeview UI
	def updateGlobeviewButtons( self ):
		kInterface = CyInterface()
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()
		iCurrentLayerID = kGLM.getCurrentLayerID()

		# Positioning things based on the visibility of the globe
		if kEngine.isGlobeviewUp():
			screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
		else:
			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 172, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )
			else:
				screen.setHelpTextArea( 350, FontTypes.SMALL_FONT, iHelpX, yResolution - 50, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, 150 )


		# Set base Y position for the LayerOptions, if we find them
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iGlobeLayerOptionsY_Minimal
		else:
			iY = yResolution - iGlobeLayerOptionsY_Regular

		# Hide the layer options ... all of them
		for i in xrange (20):
			szName = "GlobeLayerOption" + str(i)
			screen.hide(szName)

		# Setup the GlobeLayer panel
		iNumLayers = kGLM.getNumLayers()
		if kEngine.isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL:
			# set up panel
			if iCurrentLayerID != -1 and kGLM.getLayer(iCurrentLayerID).getNumOptions() != 0:
				bHasOptions = True
			else:
				bHasOptions = False
				screen.hide( "ScoreBackground" )
				screen.hide( "ScoreToggle" )

#FfH: Added by Kael 10/29/2007
				screen.hide( "ManaBackground" )
#FfH: End Add

#AoE: Added by LeastCraft 09/04/2025
				screen.hide( "ArchosBroodActivityBackground" )
#AoE: End Add

			# set up toggle button
			screen.setState("GlobeToggle", True)

			# Set GlobeLayer indicators correctly
			for i in xrange(kGLM.getNumLayers()):
				szButtonID = "GlobeLayer" + str(i)
				screen.setState( szButtonID, iCurrentLayerID == i )

			# Set up options pane
			if bHasOptions:
				kLayer = kGLM.getLayer(iCurrentLayerID)

				iCurY = iY
				iNumOptions = kLayer.getNumOptions()
				iCurOption = kLayer.getCurrentOption()
				iMaxTextWidth = -1
				for iTmp in xrange(iNumOptions):
					iOption = iTmp # iNumOptions - iTmp - 1
					szName = "GlobeLayerOption" + str(iOption)
					szCaption = kLayer.getOptionName(iOption)
					if(iOption == iCurOption):
						szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
					else:
						szBuffer = "  %s  " % (szCaption)
					iTextWidth = CyInterface().determineWidth( szBuffer )

					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - 9 - iTextWidth, iCurY-iGlobeLayerOptionHeight-10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GLOBELAYER_OPTION, iOption, -1 )
					screen.show( szName )

					iCurY -= iGlobeLayerOptionHeight

					if iTextWidth > iMaxTextWidth:
						iMaxTextWidth = iTextWidth

				#make extra space
				iCurY -= iGlobeLayerOptionHeight;
				iPanelWidth = iMaxTextWidth + 32
				iPanelHeight = iY - iCurY
				iPanelX = xResolution - 14 - iPanelWidth
				iPanelY = iCurY
				screen.setPanelSize( "ScoreBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight )
				screen.show( "ScoreBackground" )

#FfH: Added by Kael 10/29/2007
				screen.setPanelSize( "ManaBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight )
				screen.show( "ManaBackground" )
#FfH: End Add

#AoE: Added by LeastCraft 09/04/2025
				self.showArchosBroodActivityBackground()
#AoE: End Add

		else:
			if iCurrentLayerID != -1:
				kLayer = kGLM.getLayer(iCurrentLayerID)
				if kLayer.getName() == "RESOURCES":
					screen.setState("ResourceIcons", True)
				else:
					screen.setState("ResourceIcons", False)

				if kLayer.getName() == "UNITS":
					screen.setState("UnitIcons", True)
				else:
					screen.setState("UnitIcons", False)
			else:
				screen.setState("ResourceIcons", False)
				screen.setState("UnitIcons", False)

			screen.setState("Grid", CyUserProfile().getGrid())
			screen.setState("BareMap", CyUserProfile().getMap())
			screen.setState("Yields", CyUserProfile().getYields())
			screen.setState("ScoresVisible", CyUserProfile().getScores())

			screen.hide( "InterfaceGlobeLayerPanel" )
			screen.setState("GlobeToggle", False )

	# Update minimap buttons
	def setMinimapButtonVisibility( self, bVisible):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		kInterface = CyInterface()
		kGLM = CyGlobeLayerManager()
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		if ( CyInterface().isCityScreenUp() ):
			bVisible = False

		kMainButtons = ["UnitIcons", "Grid", "BareMap", "Yields", "ScoresVisible", "ResourceIcons"]
		kGlobeButtons = []
		for i in xrange(kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)
			kGlobeButtons.append(szButtonID)

		if bVisible:
			if CyEngine().isGlobeviewUp():
				kHide = kMainButtons
				kShow = kGlobeButtons
			else:
				kHide = kGlobeButtons
				kShow = kMainButtons
			screen.show( "GlobeToggle" )

		else:
			kHide = kMainButtons + kGlobeButtons
			kShow = []
			screen.hide( "GlobeToggle" )

		for szButton in kHide:
			screen.hide(szButton)

		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iMinimapButtonsY_Minimal
			iGlobeY = yResolution - iGlobeButtonY_Minimal
		else:
			iY = yResolution - iMinimapButtonsY_Regular
			iGlobeY = yResolution - iGlobeButtonY_Regular

		iBtnX = xResolution - 39
		screen.moveItem("GlobeToggle", iBtnX, iGlobeY, 0.0)

		iBtnAdvance = 28
		iBtnX = iBtnX - len(kShow)*iBtnAdvance - 10
		if len(kShow) > 0:
			i = 0
			for szButton in kShow:
				screen.moveItem(szButton, iBtnX, iY, 0.0)
				screen.moveToFront(szButton)
				screen.show(szButton)
				iBtnX += iBtnAdvance
				i += 1


	def createGlobeviewButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iNumLayers = kGLM.getNumLayers()

		for i in xrange(kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)

			kLayer = kGLM.getLayer(i)
			szStyle = kLayer.getButtonStyle()

			if szStyle == 0 or szStyle == "":
				szStyle = "Button_HUDSmall_Style"

			screen.addCheckBoxGFC( szButtonID, "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_GLOBELAYER, i, -1, ButtonStyles.BUTTON_STYLE_LABEL )
			screen.setStyle( szButtonID, szStyle )
			screen.hide( szButtonID )


	def createMinimapButtons( self ):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.addCheckBoxGFC( "UnitIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_UNIT_ICONS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "UnitIcons", "Button_HUDGlobeUnit_Style" )
		screen.setState( "UnitIcons", False )
		screen.hide( "UnitIcons" )

		screen.addCheckBoxGFC( "Grid", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GRID).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Grid", "Button_HUDBtnGrid_Style" )
		screen.setState( "Grid", False )
		screen.hide( "Grid" )

		screen.addCheckBoxGFC( "BareMap", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_BARE_MAP).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "BareMap", "Button_HUDBtnClearMap_Style" )
		screen.setState( "BareMap", False )
		screen.hide( "BareMap" )

		screen.addCheckBoxGFC( "Yields", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_YIELDS).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "Yields", "Button_HUDBtnTileAssets_Style" )
		screen.setState( "Yields", False )
		screen.hide( "Yields" )

		screen.addCheckBoxGFC( "ScoresVisible", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_SCORES).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ScoresVisible", "Button_HUDBtnRank_Style" )
		screen.setState( "ScoresVisible", True )
		screen.hide( "ScoresVisible" )

		screen.addCheckBoxGFC( "ResourceIcons", "", "", 0, 0, 28, 28, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_RESOURCE_ALL).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "ResourceIcons", "Button_HUDBtnResources_Style" )
		screen.setState( "ResourceIcons", False )
		screen.hide( "ResourceIcons" )

		screen.addCheckBoxGFC( "GlobeToggle", "", "", -1, -1, 36, 36, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_GLOBELAYER).getActionInfoIndex(), -1, ButtonStyles.BUTTON_STYLE_LABEL )
		screen.setStyle( "GlobeToggle", "Button_HUDZoom_Style" )
		screen.setState( "GlobeToggle", False )
		screen.hide( "GlobeToggle" )

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
#---unitstats addition 4/4-----------------------
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		global ishowManaBar
		global isformershowManaBar
		global iBuildingsList
		global iPromotionPage
		global iScoreState

		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON and inputClass.getFunctionName() == "UnitStatsButton"):
			screen.show("UNIT_INFO_TEXT")
			screen.show("UNIT_INFO_PANE")
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF and inputClass.getFunctionName() == "UnitStatsButton"):
			screen.hide("UNIT_INFO_TEXT")
			screen.hide("UNIT_INFO_PANE")

		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON and inputClass.getFunctionName() == "RawManaButton"):
			screen.show("ManaToggleHelpText")
			screen.show("ManaToggleHelpTextPanel")
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF and inputClass.getFunctionName() == "RawManaButton"):
			screen.hide("ManaToggleHelpText")
			screen.hide("ManaToggleHelpTextPanel")

		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON and (inputClass.getFunctionName() == "Awakenedchance" or inputClass.getFunctionName() == "SRText")):
			screen.show("SpawnOddsHelpText")
			screen.show("SpawnOddsHelpTextPanel")
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF and (inputClass.getFunctionName() == "Awakenedchance" or inputClass.getFunctionName() == "SRText")):
			screen.hide("SpawnOddsHelpText")
			screen.hide("SpawnOddsHelpTextPanel")
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON and (inputClass.getFunctionName() == "Scorpchance" or inputClass.getFunctionName() == "ScorpText")):
			screen.show("SpawnOddsHelpText")
			screen.show("SpawnOddsHelpTextPanel")
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF and (inputClass.getFunctionName() == "Scorpchance" or inputClass.getFunctionName() == "ScorpText")):
			screen.hide("SpawnOddsHelpText")
			screen.hide("SpawnOddsHelpTextPanel")

# DynTraits Start
		#if (not gc.isNoCrash()):
		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "TraitButton"):
			CvTraitScreen.CvTraitScreen().interfaceScreen()
# DynTraits End
		

		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "UnitStatsButton"):
			# Try to get the selected unit
			objUnit = CyInterface().getSelectionUnit(0)
			statisticsScreen = CvStatisticsScreen.CvStatisticsScreen()
			screen.hide("UNIT_INFO_TEXT")
			screen.hide("UNIT_INFO_PANE")
			if (objUnit != None):
				statisticsScreen.startScreen(objUnit, "unit")
				return 1
			elif (objUnit == None):
				statisticsScreen.startScreen(objUnit, "player")
				return 1


		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "RawManaButton"):
			if (ishowManaBar == 4):
				ishowManaBar = 0
				isformershowManaBar = 0
				self.updateManaStrings()
				return 1
			else:
				ishowManaBar += 1
				isformershowManaBar +=1
				self.updateManaStrings()
				return 1

		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "xUPTButton"):
			cf.showUnitPerTilePopup()
			self.updatexUPT()
			return 1

		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "BuildingsCommon"):
			iBuildingsList = 0
			self.updateCityScreen()
			return 1

		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "BuildingsWonder"):
			iBuildingsList = 1
			self.updateCityScreen()
			return 1

		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "BuildingsEffects"):
			iBuildingsList = 2
			self.updateCityScreen()
			return 1

		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "TradeRoutesButton"):
			iBuildingsList = 3
			self.updateCityScreen()
			return 1

		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "TrainingTableButton"):
			iBuildingsList = 4
			self.updateCityScreen()
			return 1

		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and (inputClass.getFunctionName() == "PromotionScrollMinus" or inputClass.getFunctionName() == "PromotionScrollPlus")):
			iMaxPromotionPages = (iNumUnitPromotions - 1) / iPromotionsPerPage + 1
			if inputClass.getFunctionName() == "PromotionScrollPlus":
				if iPromotionPage < iMaxPromotionPages:
					iPromotionPage += 1
				else:
					iPromotionPage = 1
			else:
				if iPromotionPage > 1:
					iPromotionPage -= 1
				else:
					iPromotionPage = iMaxPromotionPages
			self.updateInfoPaneStrings()
			return 1

		if(inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == "ScoreToggle"):
			iScoreState += 1
			if iScoreState > 2:
				iScoreState = 0
			self.updateScoreStrings()
			return 1

		if inputClass.getFunctionName().find("IncreasePercent") > -1:
			iPlayer		= gc.getGame().getActivePlayer()
			iCommerce	= CommerceTypes(inputClass.getData2())
			iChange		= 10
			if CyInterface().shiftKey():
				iChange = 5
			# I wish Civ4 worked
			elif inputClass.isCtrlKeyDown():
				iChange = 1
			CyMessageControl().sendModNetMessage(5001, iPlayer, iChange, iCommerce, -1)
			return 1

		if inputClass.getFunctionName().find("DecreasePercent") > -1:
			iPlayer		= gc.getGame().getActivePlayer()
			iCommerce	= CommerceTypes(inputClass.getData2())
			iChange		= 10
			if CyInterface().shiftKey():
				iChange = 5
			# I wish Civ4 worked
			elif inputClass.isCtrlKeyDown():
				iChange = 1
			CyMessageControl().sendModNetMessage(5002, iPlayer, iChange, iCommerce, -1)
			return 1

#/---unitstats addition 4/4-----------------------

# BUG - Great Person Bar - start
		if (inputClass.getFunctionName() == "GreatPersonBar" or inputClass.getFunctionName() == "GreatPersonBarText"):
			# Zoom to next GP city
			iCity = inputClass.getData1()
			if (iCity == -1):
				pCity, _ = GPUtil.findNextCity()
			else:
				pCity = gc.getActivePlayer().getCity(iCity)
				CyInterface().selectCity(pCity, False)
			return 1

		# < Mercenaries Start >
		# Handle the case where the "Mercenary Manager" button is pressed. 
		if(inputClass.getFunctionName() == "MercenaryManagerButton"):
			mercenaryManager.interfaceScreen()
		# < Mercenaries End   >
		return 0

	def update(self, fDelta):
		return

	def updateSlaveButtons (self):
		gc 			= CyGlobalContext()
		getInfoType	= gc.getInfoTypeForString
		screen 		= CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		interface	= CyInterface()
		getHeadSelectedUnit = interface.getHeadSelectedUnit()
		NumSlaves 	= getHeadSelectedUnit.getNumSlaves()
		NumMinions 	= getHeadSelectedUnit.getNumMinions()
		getInterfaceArtInfo = ArtFileMgr.getInterfaceArtInfo
		iCount = 0
		global g_iSlaveColumnHeight
		global g_iSlaveRowLength

		if ( interface.getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			Add = ""
		else:
			Add = "Bottom"

		if (not getHeadSelectedUnit.getMasterUnit().isNone()):
			pLoopUnit = getHeadSelectedUnit.getMasterUnit()
			if (pLoopUnit.isWaiting()):
				szFileName = getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()
			elif (pLoopUnit.canMove()):
				if (pLoopUnit.hasMoved()):
					szFileName = getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
				else:
					szFileName = getInterfaceArtInfo("OVERLAY_MOVE").getPath()
			else:
				szFileName = getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

			szString = str(Add) + "MasterUnitButton"
			screen.changeImageButton( szString, pLoopUnit.getButton() )
			screen.enable(szString, True)
			screen.setState(szString, False)
			screen.show( szString )

			# place the health bar
			if (pLoopUnit.isFighting()):
				bShowHealth = False
			elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
				bShowHealth = pLoopUnit.canAirAttack()
			else:
				bShowHealth = pLoopUnit.canFight()

			if bShowHealth:
				szStringHealth = szString + "Health"
				screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
				if (pLoopUnit.getDamageReal() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
					screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_RED"))
				elif (pLoopUnit.getDamageReal() >= (pLoopUnit.maxHitPoints() / 3)):
					screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_YELLOW"))
				else:
					screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_GREEN"))
				screen.show( szStringHealth )

			if pLoopUnit.isRevealed():
				szStringStealth = szString + "Stealth"
				if pLoopUnit.IsSelected():
					szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED_SELECTED").getPath()
					screen.changeDDSGFC( szStringStealth, szPromoFileName )
				screen.show( szStringStealth )
			elif pLoopUnit.isPromotionReady():
#			if pLoopUnit.isPromotionReady(): # Swap with 4 lines above
				szStringStealth = szString + "Stealth"
				szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION").getPath()
				screen.changeDDSGFC( szStringStealth, szPromoFileName )
				if pLoopUnit.IsSelected():
					szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_SELECTED").getPath()
					screen.changeDDSGFC( szStringStealth, szPromoFileName )
				screen.show( szStringStealth )

			# Adds the overlay first
			szStringIcon = szString + "Icon"
			screen.changeDDSGFC( szStringIcon, szFileName )
			screen.show( szStringIcon )

		if (not getHeadSelectedUnit.getCommanderUnit().isNone()):
			pLoopUnit = getHeadSelectedUnit.getCommanderUnit()
			if (pLoopUnit.isWaiting()):
				szFileName = getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()
			elif (pLoopUnit.canMove()):
				if (pLoopUnit.hasMoved()):
					szFileName = getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
				else:
					szFileName = getInterfaceArtInfo("OVERLAY_MOVE").getPath()
			else:
				szFileName = getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

			szString = str(Add) + "CommanderUnitButton"
			screen.changeImageButton( szString, pLoopUnit.getButton() )
			screen.enable(szString, True)
			screen.setState(szString, False)
			screen.show( szString )

			# place the health bar
			if (pLoopUnit.isFighting()):
				bShowHealth = False
			elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
				bShowHealth = pLoopUnit.canAirAttack()
			else:
				bShowHealth = pLoopUnit.canFight()

			if bShowHealth:
				szStringHealth = szString + "Health"
				screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
				if (pLoopUnit.getDamageReal() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
					screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_RED"))
				elif (pLoopUnit.getDamageReal() >= (pLoopUnit.maxHitPoints() / 3)):
					screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_YELLOW"))
				else:
					screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_GREEN"))
				screen.show( szStringHealth )

			if pLoopUnit.isRevealed():
				szStringStealth = szString + "Stealth"
				if pLoopUnit.IsSelected():
					szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED_SELECTED").getPath()
					screen.changeDDSGFC( szStringStealth, szPromoFileName )
				screen.show( szStringStealth )
			elif pLoopUnit.isPromotionReady():
#			if pLoopUnit.isPromotionReady(): # Swap with 4 lines above
				szStringStealth = szString + "Stealth"
				szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION").getPath()
				screen.changeDDSGFC( szStringStealth, szPromoFileName )
				if pLoopUnit.IsSelected():
					szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_SELECTED").getPath()
					screen.changeDDSGFC( szStringStealth, szPromoFileName )
				screen.show( szStringStealth )

			# Adds the overlay first
			szStringIcon = szString + "Icon"
			screen.changeDDSGFC( szStringIcon, szFileName )
			screen.show( szStringIcon )

		for i in xrange(NumSlaves):
			pLoopUnit = getHeadSelectedUnit.getSlaveUnit(i)
			if (pLoopUnit):

				if (iCount <  g_iSlaveColumnHeight*g_iSlaveRowLength):
					if (pLoopUnit.isWaiting()):
						szFileName = getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()
					elif (pLoopUnit.canMove()):
						if (pLoopUnit.hasMoved()):
							szFileName = getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
						else:
							szFileName = getInterfaceArtInfo("OVERLAY_MOVE").getPath()
					else:
						szFileName = getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

					szString = str(Add) + "SlaveListButton" + str(iCount)
					screen.changeImageButton( szString, pLoopUnit.getButton() )
					screen.enable(szString, True)
					screen.setState(szString, False)
					screen.show( szString )

					# place the health bar
					if (pLoopUnit.isFighting()):
						bShowHealth = False
					elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
						bShowHealth = pLoopUnit.canAirAttack()
					else:
						bShowHealth = pLoopUnit.canFight()

					if bShowHealth:
						szStringHealth = szString + "Health"
						screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
						if (pLoopUnit.getDamageReal() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
							screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_RED"))
						elif (pLoopUnit.getDamageReal() >= (pLoopUnit.maxHitPoints() / 3)):
							screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_YELLOW"))
						else:
							screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_GREEN"))
						screen.show( szStringHealth )

					if pLoopUnit.isRevealed():
						szStringStealth = szString + "Stealth"
						if pLoopUnit.IsSelected():
							szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED_SELECTED").getPath()
							screen.changeDDSGFC( szStringStealth, szPromoFileName )
						screen.show( szStringStealth )
					elif pLoopUnit.isPromotionReady():
#					if pLoopUnit.isPromotionReady(): # Swap with 4 lines above
						szStringStealth = szString + "Stealth"
						szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION").getPath()
						screen.changeDDSGFC( szStringStealth, szPromoFileName )
						if pLoopUnit.IsSelected():
							szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_SELECTED").getPath()
							screen.changeDDSGFC( szStringStealth, szPromoFileName )
						screen.show( szStringStealth )

					# Adds the overlay first
					szStringIcon = szString + "Icon"
					screen.changeDDSGFC( szStringIcon, szFileName )
					screen.show( szStringIcon )

				iCount = iCount + 1

		iCount = 0
		for i in xrange(NumMinions):
			pLoopUnit = getHeadSelectedUnit.getMinionUnit(i)
			if (pLoopUnit):

				if (iCount <  g_iSlaveColumnHeight*g_iSlaveRowLength):
					if (pLoopUnit.isWaiting()):
						szFileName = getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()
					elif (pLoopUnit.canMove()):
						if (pLoopUnit.hasMoved()):
							szFileName = getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
						else:
							szFileName = getInterfaceArtInfo("OVERLAY_MOVE").getPath()
					else:
						szFileName = getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

					szString = str(Add) + "MinionListButton" + str(iCount)
					screen.changeImageButton( szString, pLoopUnit.getButton() )
					screen.enable(szString, True)
					screen.setState(szString, False)
					screen.show( szString )

					# place the health bar
					if (pLoopUnit.isFighting()):
						bShowHealth = False
					elif (pLoopUnit.getDomainType() == DomainTypes.DOMAIN_AIR):
						bShowHealth = pLoopUnit.canAirAttack()
					else:
						bShowHealth = pLoopUnit.canFight()

					if bShowHealth:
						szStringHealth = szString + "Health"
						screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
						if (pLoopUnit.getDamageReal() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
							screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_RED"))
						elif (pLoopUnit.getDamageReal() >= (pLoopUnit.maxHitPoints() / 3)):
							screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_YELLOW"))
						else:
							screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, getInfoType("COLOR_GREEN"))
						screen.show( szStringHealth )

					if pLoopUnit.isRevealed():
						szStringStealth = szString + "Stealth"
						if pLoopUnit.IsSelected():
							szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_BUSTED_SELECTED").getPath()
							screen.changeDDSGFC( szStringStealth, szPromoFileName )
						screen.show( szStringStealth )
					elif pLoopUnit.isPromotionReady():
#					if pLoopUnit.isPromotionReady(): # Swap with 4 lines above
						szStringStealth = szString + "Stealth"
						szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION").getPath()
						screen.changeDDSGFC( szStringStealth, szPromoFileName )
						if pLoopUnit.IsSelected():
							szPromoFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_PROMOTION_SELECTED").getPath()
							screen.changeDDSGFC( szStringStealth, szPromoFileName )
						screen.show( szStringStealth )

					# Adds the overlay first
					szStringIcon = szString + "Icon"
					screen.changeDDSGFC( szStringIcon, szFileName )
					screen.show( szStringIcon )

				iCount = iCount + 1

	def isHighResolution(self):
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		if CyUserProfile().getPlayerOption(PlayerOptionTypes.PLAYEROPTION_MODDER_2): return False
		if xResolution < g_iVeryHighRez: return False
		return True

def RecursiveSearch(pfilename, ppath, pexact):
		##
		##  Recursive search
		##  -- arcticnightwolf, 26-Nov-2010
		##
		## note: search is case insensitive
		##       pexact: true   -- will search only for exact matches                       ( "c:/somefolder/somefile.txt" )
		##       pexact: false  -- will search only for files ending with specified string  ( "c:/somefolder/*somefile.txt" )
		##
		if (os.path.isdir(ppath)):
				fnlength = len(pfilename)
				for subitem in os.listdir(ppath):
						if (pexact or len(subitem) >= fnlength):
								if ((pexact and subitem.lower() == pfilename.lower()) or ((not pexact) and (subitem.lower()[-fnlength:] == pfilename.lower()))):
										yield os.path.join(ppath, subitem)
						if (os.path.isdir(ppath)):
								for subsubitem in RecursiveSearch(pfilename, os.path.join(ppath, subitem), pexact):
										yield subsubitem

def getSpecialistList( iCivilization ):
	   # edit:
		# * MPL ( modular python loading )
		#     - all modules are searched for files "*SpecialistList.py"
		#     - in these files there have to be exactly one function called "getSpecialistList"
		#        - civSpecialist dictionary is passed to this function as parameter
		#        - function may add/modify/remove data in this dictionary
		#            - civSpecialists[getInfoType(CIV)] = [citizen, priest, bard, sage, merch, eng, heal, statesman, greatpriest, greatbard, greatsage, greatmerch, greateng, greatheal]
		#        - function is expected to return this dictionary
		# -- arcticnightwolf 27-Nov-2010
	global baseSpecialistList
	global civSpecialists

	if baseSpecialistList is None:
		gc 			= CyGlobalContext()
		getInfoType	= gc.getInfoTypeForString
		baseSpecialistList = ['Art/Civs/CivSpecialists/Human/Citizen.dds', 'Art/Civs/CivSpecialists/Human/Priest.dds', 'Art/Civs/CivSpecialists/Human/Bard.dds', 'Art/Civs/CivSpecialists/Human/Sage.dds', 'Art/Civs/CivSpecialists/Human/Merchant.dds', 'Art/Civs/CivSpecialists/Human/Engineer.dds', 'Art/Civs/CivSpecialists/Human/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Human/GreatPriest.dds', 'Art/Civs/CivSpecialists/Human/GreatBard.dds', 'Art/Civs/CivSpecialists/Human/GreatSage.dds', 'Art/Civs/CivSpecialists/Human/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Human/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Human/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']
		civSpecialists = dict()
		civSpecialists[getInfoType('CIVILIZATION_KHAZAD')] = ['Art/Civs/CivSpecialists/Dwarves/Citizen.dds', 'Art/Civs/CivSpecialists/Dwarves/Priest.dds', 'Art/Civs/CivSpecialists/Dwarves/Bard.dds', 'Art/Civs/CivSpecialists/Dwarves/Sage.dds', 'Art/Civs/CivSpecialists/Dwarves/Merchant.dds', 'Art/Civs/CivSpecialists/Dwarves/Engineer.dds', 'Art/Civs/CivSpecialists/Dwarves/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatPriest.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatBard.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatSage.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']
		civSpecialists[getInfoType('CIVILIZATION_LUCHUIRP')] = ['Art/Civs/CivSpecialists/Dwarves/Citizen.dds', 'Art/Civs/CivSpecialists/Dwarves/Priest.dds', 'Art/Civs/CivSpecialists/Dwarves/Bard.dds', 'Art/Civs/CivSpecialists/Dwarves/Sage.dds', 'Art/Civs/CivSpecialists/Dwarves/Merchant.dds', 'Art/Civs/CivSpecialists/Dwarves/Engineer.dds', 'Art/Civs/CivSpecialists/Dwarves/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatPriest.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatBard.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatSage.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Dwarves/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']
		civSpecialists[getInfoType('CIVILIZATION_LJOSALFAR')] = ['Art/Civs/CivSpecialists/Elves/Citizen.dds', 'Art/Civs/CivSpecialists/Elves/Priest.dds', 'Art/Civs/CivSpecialists/Elves/Bard.dds', 'Art/Civs/CivSpecialists/Elves/Sage.dds', 'Art/Civs/CivSpecialists/Elves/Merchant.dds', 'Art/Civs/CivSpecialists/Elves/Engineer.dds', 'Art/Civs/CivSpecialists/Elves/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Elves/GreatPriest.dds', 'Art/Civs/CivSpecialists/Elves/GreatBard.dds', 'Art/Civs/CivSpecialists/Elves/GreatSage.dds', 'Art/Civs/CivSpecialists/Elves/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Elves/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Elves/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']
		civSpecialists[getInfoType('CIVILIZATION_SVARTALFAR')] = ['Art/Civs/CivSpecialists/Elves/Citizen.dds', 'Art/Civs/CivSpecialists/Elves/Priest.dds', 'Art/Civs/CivSpecialists/Elves/Bard.dds', 'Art/Civs/CivSpecialists/Elves/Sage.dds', 'Art/Civs/CivSpecialists/Elves/Merchant.dds', 'Art/Civs/CivSpecialists/Elves/Engineer.dds', 'Art/Civs/CivSpecialists/Elves/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Elves/GreatPriest.dds', 'Art/Civs/CivSpecialists/Elves/GreatBard.dds', 'Art/Civs/CivSpecialists/Elves/GreatSage.dds', 'Art/Civs/CivSpecialists/Elves/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Elves/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Elves/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']
		civSpecialists[getInfoType('CIVILIZATION_MAZATL')] = ['Art/Civs/CivSpecialists/Lizardmen/Citizen.dds', 'Art/Civs/CivSpecialists/Lizardmen/Priest.dds', 'Art/Civs/CivSpecialists/Lizardmen/Bard.dds', 'Art/Civs/CivSpecialists/Lizardmen/Sage.dds', 'Art/Civs/CivSpecialists/Lizardmen/Merchant.dds', 'Art/Civs/CivSpecialists/Lizardmen/Engineer.dds', 'Art/Civs/CivSpecialists/Lizardmen/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatPriest.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatBard.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatSage.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']
		civSpecialists[getInfoType('CIVILIZATION_CUALLI')] = ['Art/Civs/CivSpecialists/Lizardmen/Citizen.dds', 'Art/Civs/CivSpecialists/Lizardmen/Priest.dds', 'Art/Civs/CivSpecialists/Lizardmen/Bard.dds', 'Art/Civs/CivSpecialists/Lizardmen/Sage.dds', 'Art/Civs/CivSpecialists/Lizardmen/Merchant.dds', 'Art/Civs/CivSpecialists/Lizardmen/Engineer.dds', 'Art/Civs/CivSpecialists/Lizardmen/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatPriest.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatBard.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatSage.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Lizardmen/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']
		civSpecialists[getInfoType('CIVILIZATION_INFERNAL')] = ['Art/Civs/CivSpecialists/Demons/Citizen.dds', 'Art/Civs/CivSpecialists/Demons/Priest.dds', 'Art/Civs/CivSpecialists/Demons/Bard.dds', 'Art/Civs/CivSpecialists/Demons/Sage.dds', 'Art/Civs/CivSpecialists/Demons/Merchant.dds', 'Art/Civs/CivSpecialists/Demons/Engineer.dds', 'Art/Civs/CivSpecialists/Demons/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Demons/GreatPriest.dds', 'Art/Civs/CivSpecialists/Demons/GreatBard.dds', 'Art/Civs/CivSpecialists/Demons/GreatSage.dds', 'Art/Civs/CivSpecialists/Demons/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Demons/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Demons/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']
		civSpecialists[getInfoType('CIVILIZATION_DTESH')] = ['Art/Civs/CivSpecialists/Undead/Citizen.dds', 'Art/Civs/CivSpecialists/Undead/Priest.dds', 'Art/Civs/CivSpecialists/Undead/Bard.dds', 'Art/Civs/CivSpecialists/Undead/Sage.dds', 'Art/Civs/CivSpecialists/Undead/Merchant.dds', 'Art/Civs/CivSpecialists/Undead/Engineer.dds', 'Art/Civs/CivSpecialists/Undead/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Undead/GreatPriest.dds', 'Art/Civs/CivSpecialists/Undead/GreatBard.dds', 'Art/Civs/CivSpecialists/Undead/GreatSage.dds', 'Art/Civs/CivSpecialists/Undead/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Undead/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Undead/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']
		# Nafshahim slaves
		#if getInfoType("CIVILIZATION_NAFSHAHIM") != -1:
		#	civSpecialists[getInfoType('CIVILIZATION_NAFSHAHIM')] = ['Art/Civs/CivSpecialists/Human/Citizen.dds', 'Art/Civs/CivSpecialists/Human/Priest.dds', 'Art/Civs/CivSpecialists/Human/Bard.dds', 'Art/Civs/CivSpecialists/Human/Sage.dds', 'Art/Civs/CivSpecialists/Human/Merchant.dds', 'Art/Civs/CivSpecialists/Human/Engineer.dds', 'Art/Civs/CivSpecialists/Human/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Human/GreatPriest.dds', 'Art/Civs/CivSpecialists/Human/GreatBard.dds', 'Art/Civs/CivSpecialists/Human/GreatSage.dds', 'Art/Civs/CivSpecialists/Human/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Human/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Human/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']

		# And the same for the Mekaran Order
		if getInfoType("CIVILIZATION_MEKARA") != -1:
			civSpecialists[getInfoType('CIVILIZATION_MEKARA')] = ['Art/Civs/CivSpecialists/Human/Citizen.dds', 'Art/Civs/CivSpecialists/Human/Priest.dds', 'Art/Civs/CivSpecialists/Human/Bard.dds', 'Art/Civs/CivSpecialists/Human/Sage.dds', 'Art/Civs/CivSpecialists/Human/Merchant.dds', 'Art/Civs/CivSpecialists/Human/Engineer.dds', 'Art/Civs/CivSpecialists/Human/Healer.dds', 'Art/Civs/CivSpecialists/Human/Statesman.dds', 'Art/Civs/CivSpecialists/Human/GreatPriest.dds', 'Art/Civs/CivSpecialists/Human/GreatBard.dds', 'Art/Civs/CivSpecialists/Human/GreatSage.dds', 'Art/Civs/CivSpecialists/Human/GreatMerchant.dds', 'Art/Civs/CivSpecialists/Human/GreatEngineer.dds', 'Art/Civs/CivSpecialists/Human/GreatHealer.dds', 'Art/Civs/CivSpecialists/Human/Citizen.dds']

		folderlist = []
		folderlist.append(CvPath.assetsPath[2] + "\\Modules\\NormalModules\\")
		folderlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FirstLoad\\")
		folderlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\SecondLoad\\")
		folderlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\ThirdLoad\\")
		folderlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FourthLoad\\")

		for folderpath in folderlist:
				if os.path.exists(folderpath):
						for module in os.listdir(folderpath):
								for listfile in RecursiveSearch("SpecialistList.py", os.path.join(folderpath, module), False):
										if os.path.exists(listfile):
												tempFileName = file(listfile)
												tempModuleName = listfile.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ]
												module = imp.load_module( tempModuleName, tempFileName, tempModuleName+".py", ("","",1))
												civSpecialists = module.getSpecialistList( civSpecialists )
												tempFileName.close()

	return civSpecialists.get( iCivilization, baseSpecialistList )
