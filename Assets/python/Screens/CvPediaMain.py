## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
## 2013-08 Modified by Ronkhar
from CvPythonExtensions import *
import string
import CvUtil
import ScreenInput
import CvScreenEnums
import CvPediaScreen      # base class
import CvPediaUnit
import CvPediaTech
import CvPediaBuilding
import CvPediaPromotion
import CvPediaUnitChart
import CvPediaBonus
import CvPediaTerrain
import CvPediaFeature
import CvPediaPlotEffect
import CvPediaImprovement
import CvPediaCivic
import CvPediaCivilization
import CvPediaCityClass
import CvPediaRoute
import CvPediaLeader
import CvPediaTrait
import CvPediaSpecialist
import CvPediaLore
import CvPediaHistory
import CvPediaProject
import CvPediaSpawnGroup
import CvPediaAffinity
import CvPediaReligion
import CvPediaSpell
import CvPediaCorporation

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaMain( CvPediaScreen.CvPediaScreen ):
	"Civilopedia Main Screen"

	def __init__(self):
		self.PEDIA_MAIN_SCREEN_NAME = "PediaMainScreen"
		self.INTERFACE_ART_INFO     = "SCREEN_BG"

		self.WIDGET_ID              = "PediaMainWidget"
		self.EXIT_ID                = "PediaMainExitWidget"
		self.BACKGROUND_ID          = "PediaMainBackground"
		self.TOP_PANEL_ID           = "PediaMainTopPanel"
		self.BOTTOM_PANEL_ID        = "PediaMainBottomPanel"
		self.BACK_ID                = "PediaMainBack"
		self.NEXT_ID                = "PediaMainForward"
		self.TOP_ID                 = "PediaMainTop"
		self.LIST_ID                = "PediaMainList"

		self.FILTER_DROPDOWN_ID     = 0
		self.SORT_DROPDOWN_ID       = 0
		self.nWidgetCount           = 0

		# screen instances
		self.pediaTechScreen        = CvPediaTech.CvPediaTech(self)
		self.pediaUnitScreen        = CvPediaUnit.CvPediaUnit(self)
		self.pediaBuildingScreen    = CvPediaBuilding.CvPediaBuilding(self)
		self.pediaPromotionScreen   = CvPediaPromotion.CvPediaPromotion(self)
		self.pediaSpellScreen       = CvPediaSpell.CvPediaSpell(self)
		self.pediaUnitChart         = CvPediaUnitChart.CvPediaUnitChart(self)
		self.pediaBonus             = CvPediaBonus.CvPediaBonus(self)
		self.pediaTerrain           = CvPediaTerrain.CvPediaTerrain(self)
		self.pediaFeature           = CvPediaFeature.CvPediaFeature(self)
		self.pediaPlotEffect        = CvPediaPlotEffect.CvPediaPlotEffect(self)
		self.pediaImprovement       = CvPediaImprovement.CvPediaImprovement(self)
		self.pediaCivic             = CvPediaCivic.CvPediaCivic(self)
		self.pediaCivilization      = CvPediaCivilization.CvPediaCivilization(self)
		self.pediaCityClass         = CvPediaCityClass.CvPediaCityClass(self)
		self.pediaRoute             = CvPediaRoute.CvPediaRoute(self)
		self.pediaLeader            = CvPediaLeader.CvPediaLeader(self)
		self.pediaTrait             = CvPediaTrait.CvPediaTrait(self)
		self.pediaSpecialist        = CvPediaSpecialist.CvPediaSpecialist(self)
		self.pediaProjectScreen     = CvPediaProject.CvPediaProject(self)
		self.pediaReligion          = CvPediaReligion.CvPediaReligion(self)
		self.pediaCorporation       = CvPediaCorporation.CvPediaCorporation(self)
		self.pediaSpawnGroupScreen  = CvPediaSpawnGroup.CvPediaSpawnGroup(self)
		self.pediaAffinityScreen    = CvPediaAffinity.CvPediaAffinity(self)
		self.pediaLore              = CvPediaLore.CvPediaLore(self)
		self.pediaHistorical        = CvPediaHistory.CvPediaHistory(self)

		# used for navigating "forward" and "back" in civilopedia
		self.pediaHistory           = []
		self.pediaFuture            = []

		self.listCategories         = []

		self.iCategory              = -1
		self.iLastScreen            = -1
		self.iActivePlayer          = -1

		self.mapCategories = {
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH       : self.placeTechs,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT       : self.placeUnits,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING   : self.placeBuildings,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN    : self.placeTerrains,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE    : self.placeFeatures,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_PLOT_EFFECT: self.placePlotEffects,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_ROUTE      : self.placeRoutes,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS      : self.placeBoni,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT: self.placeImprovements,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST : self.placeSpecialists,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION  : self.placePromotions,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPELL      : self.placeSpells,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP : self.placeUnitGroups,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV        : self.placeCivs,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER     : self.placeLeaders,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CITYCLASS  : self.placeCityClasses,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_TRAIT      : self.placeTraits,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION   : self.placeReligions,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CORPORATION: self.placeCorporations,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC      : self.placeCivics,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT    : self.placeProjects,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPAWNGROUP : self.placeSpawnGroups,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_AFFINITY   : self.placeAffinities,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_LORE       : self.placeLore,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT    : self.placeConcepts,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_HINTS      : self.placeHints,
			CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPELL      : self.placeSpells,
			}

	def getScreen(self):
		# Find out the game resolution and give the same to pedia (full screen pedia)
		Screen_Ronkhar = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		self.W_SCREEN = Screen_Ronkhar.getXResolution() #HD example: 1920
		self.H_SCREEN = Screen_Ronkhar.getYResolution() #HD example: 1200

		# "back", "next", "top" and "exit" buttons: horizontal position
		self.X_BACK = 50
		self.X_FORWARD = 200
		self.X_MENU = int(self.W_SCREEN/2) # "TOP" button, center of screen
		self.X_EXIT = self.W_SCREEN - 30

		# and vertical position (bottom line of the pedia)
		h_bottom_line = self.H_SCREEN - 38 #HD example: 1162
		self.Y_BACK    = h_bottom_line
		self.Y_FORWARD = h_bottom_line
		self.Y_MENU    = h_bottom_line
		self.Y_EXIT    = h_bottom_line

		self.H_TOP_BAR = 50 # height of top bar
		self.H_BOT_BAR = 50 # height of bottom bar

		# Right menu
		self.W_LINKS = 270 # width (and width of central list of 1 column too)
		self.X_LINKS = self.W_SCREEN - self.W_LINKS # horizontal position (of upper-left corner) HD example: 1675
		self.Y_LINKS = self.H_TOP_BAR # vertical position (of upper-left corner)
		self.H_LINKS = self.H_SCREEN - self.H_TOP_BAR - self.H_BOT_BAR # height of right menu HD example: 1102

		# title positions
		self.X_SCREEN = max((self.W_SCREEN - self.W_LINKS)/2,800) # horizontal position of (center of) title (the max is used for low resolutions. 540 is just right of the 2 sorting bars)
		self.Y_TITLE = 11 # vertical position of title (+unknown constant, prob 5px)

		# size of filter and sort dropdown for other screens (top left of almost all screens)
		self.Y_DROPDOWN = 12
		self.W_DROPDOWN = 260
		self.X_FILTER_DROPDOWN = 0
		self.X_SORT_DROPDOWN = self.X_FILTER_DROPDOWN + self.W_DROPDOWN

		# Panel height for other screens (for example in the civilization screen, for unique/blocked units/buildings)
		self.H_BLUE50_PANEL = 105 # 77 for the panel and 21 for the title, 7 for BLUE50 offset

		# Text margin for other screens (for example in the civilization screen, for history and strategy)
		self.HM_TEXT = 10 # horizontal margin
		self.VM_TEXT = 26 # vertical margin

		# Central pane
		self.EXT_SPACING  = 28
		self.INT_SPACING  = self.EXT_SPACING/2
		self.X_ITEMS_PANE = self.EXT_SPACING  # horizontal position (of upper-left corner)
		self.Y_ITEMS_PANE = self.H_TOP_BAR + self.EXT_SPACING # vertical position (of upper-left corner)
		self.W_ITEMS_PANE = self.X_LINKS - 2 * self.EXT_SPACING # width of central pane    HD example: 1615
		self.H_ITEMS_PANE = self.H_LINKS - 2 * self.EXT_SPACING # height of central pane   HD example: 1042

		Screen_Pedia_Main_Ronkhar = CyGInterfaceScreen(self.PEDIA_MAIN_SCREEN_NAME, CvScreenEnums.PEDIA_MAIN)
		Screen_Pedia_Main_Ronkhar.setDimensions(0,0, self.W_SCREEN, self.H_SCREEN)
		return Screen_Pedia_Main_Ronkhar

	def setPediaCommonWidgets(self):
		self.EXIT_TEXT    = u"<font=4>" + localText.getText("TXT_KEY_EXIT_PEDIA"          , ()).upper() + "</font>"
		self.BACK_TEXT    = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_BACK"   , ()).upper() + "</font>"
		self.FORWARD_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_FORWARD", ()).upper() + "</font>"
		self.MENU_TEXT    = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_TOP"    , ()).upper() + "</font>"

		self.listCategories = [
			localText.getText("TXT_KEY_PEDIA_CATEGORY_TECH"       , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT"       , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_BUILDING"   , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_TERRAIN"    , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_FEATURE"    , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_PLOT_EFFECT", ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_ROUTE"      , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_BONUS"      , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_SPECIALIST" , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION"  , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_SPELL"      , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_UNIT_COMBAT", ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_CIV"        , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_LEADER"     , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_CITYCLASS"  , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_TRAIT"      , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_RELIGION"   , ()),
			localText.getText("TXT_KEY_CONCEPT_CORPORATIONS"      , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_CIVIC"      , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_PROJECT"    , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_SPAWNGROUP" , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_AFFINITY"   , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_LORE"       , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT"    , ()),
			localText.getText("TXT_KEY_PEDIA_CATEGORY_HINTS"      , ()),
		]
		# self.listCategories.sort() # Test of alphabetical sorting. Problem = it changes only the titles in the right menu. But clicking still show the former category (1st line links to techs, even if sorting puts affinities)
		# The order of entries is defined in python::enum_<CivilopediaPageTypes>("CivilopediaPageTypes"), line 2041 in CyEnumsInterface.cpp, which cannot be changed unless the dll is recompiled 

		# Create a new screen
		screen = self.getScreen()
		screen.setRenderInterfaceOnly(True);
		screen.setScreenGroup(1)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		# Set background image
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo(self.INTERFACE_ART_INFO).getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		#If the top panel Y is 0 and the height is H, you get 2 black lines, then H-9 brown lines, then a white one, then a grey gradient --> Y=-2 removes the black lines, H=58 puts the white line on line 50
		screen.addPanel(self.TOP_PANEL_ID, u"", u"", True, False, 0, -2, self.W_SCREEN, 58, PanelStyles.PANEL_STYLE_TOPBAR )
		#If the bottom panel Y is screenheight - H and the height is H, you get H-9 brown lines, then a white one, then a grey one (possibly with gradient on more lines, but can't see it on current background)
		screen.addPanel(self.BOTTOM_PANEL_ID, u"", u"", True, False, 0, self.H_SCREEN-58, self.W_SCREEN, 58, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)

		# Exit button
		screen.setText(self.EXIT_ID, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)

		# Back
		screen.setText(self.BACK_ID, "Background", self.BACK_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_BACK, self.Y_BACK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_BACK, 1, -1)

		# Forward
		screen.setText(self.NEXT_ID, "Background", self.FORWARD_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.X_FORWARD, self.Y_FORWARD, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_FORWARD, 1, -1)

		# List of items on the right
		screen.addListBoxGFC(self.LIST_ID, "", self.X_LINKS, self.Y_LINKS, self.W_LINKS, self.H_LINKS, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(self.LIST_ID, True)
		screen.setStyle(self.LIST_ID, "Table_StandardCiv_Style")

	# Screen construction function
	def showScreen(self, iCategory):
		self.iCategory = iCategory

		self.deleteAllWidgets()

		screen = self.getScreen()

		bNotActive = (not screen.isActive())
		if bNotActive:
			self.setPediaCommonWidgets()

		# Header...
		szHeader = u"<font=4b>" +localText.getText("TXT_KEY_WIDGET_HELP", ()).upper() + u"</font>"
		szHeaderId = self.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_DESCRIPTION, -1, -1)

		self.panelName = self.getNextWidgetName()
		screen.addPanel(self.panelName, "", "", false, false,self.X_ITEMS_PANE, self.Y_ITEMS_PANE, self.W_ITEMS_PANE, self.H_ITEMS_PANE, PanelStyles. PANEL_STYLE_MAIN_BLACK50)

		if self.iLastScreen != CvScreenEnums.PEDIA_MAIN or bNotActive:
			self.placeLinks(true)
			self.iLastScreen = CvScreenEnums.PEDIA_MAIN
		else:
			self.placeLinks(false)

		if (self.mapCategories.has_key(iCategory)):
			self.mapCategories.get(iCategory)()

	def placeTechs(self): # pediaXXXScreen is the list of names, while WIDGET_PEDIA_JUMP_TO_XXX is the list of popups on hover
		self.placeFilterSort(self.pediaTechScreen, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH)

	def placeUnits(self):
		self.placeFilterSort(self.pediaUnitScreen, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT)

	def placeBuildings(self):
		self.placeFilterSort(self.pediaBuildingScreen, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING)

	def placeBoni(self):
		self.placeFilterSort(self.pediaBonus, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS)

	def placeImprovements(self):
		self.placeFilterSort(self.pediaImprovement, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT)

	def placePromotions(self):
		self.placeFilterSort(self.pediaPromotionScreen, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION)

	def placeSpells(self):
		self.placeFilterSort(self.pediaSpellScreen, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPELL)

	def placeCivs(self):
		self.placeFilterSort(self.pediaCivilization, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV)

	def placeCityClasses(self):
		self.placeFilterSort(self.pediaCityClass, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CITYCLASS)

	def placeRoutes(self):
		self.placeFilterSort(self.pediaRoute, WidgetTypes.WIDGET_PEDIA_JUMP_TO_ROUTE)

	def placeLeaders(self):
		self.placeFilterSort(self.pediaLeader, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER)

	def placeTraits(self):
	##Modular update 
		# Runs once per session: without the flag every visit to this category appended the module filters again
		if self.pediaTrait.modular_update==False:
			if gc.getInfoTypeForString("MODULE_DYNAMIC_RELIGION")!=-1:
				self.pediaTrait.FILTERS.append({
					"name" : 'localText.getText("TXT_KEY_TRAITCLASS_RELIGION", ())',
					"Purpose" : "Religious Paths",
					"Hardcoded" : False,
					"HardcodeList" : [],
					"Value to Check" : 'eTrait.getTraitClass()',
					"Desired Result" : 'gc.getInfoTypeForString("TRAITCLASS_RELIGION")',
				})
			if gc.getInfoTypeForString("MODULE_CHISLEV_EXPANSION")!=-1:
				self.pediaTrait.FILTERS.append({
					"name" : 'localText.getText("TXT_KEY_TRAITCLASS_TRIBAL", ())',
					"Purpose" : "Religious Paths",
					"Hardcoded" : False,
					"HardcodeList" : [],
					"Value to Check" : 'eTrait.getTraitClass()',
					"Desired Result" : 'gc.getInfoTypeForString("TRAITCLASS_TRIBAL")',
				})
			self.pediaTrait.modular_update=True
		# List the filters which you want to be available initially, or self.FILTERS to have all of them available from the start
			self.pediaTrait.ALLOWED_FILTERS = self.pediaTrait.FILTERS
			self.pediaTrait.CURRENT_FILTER = self.pediaTrait.FILTERS[0]

	## End Modular update

		self.placeFilterSort(self.pediaTrait, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TRAIT)

	def placeCivics(self):
		self.placeFilterSort(self.pediaCivic, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC)

	def placeProjects(self):
		self.placeFilterSort(self.pediaProjectScreen, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROJECT)

	def placeSpawnGroups(self):
		# 1) same as RifE 1.41 --> affichage de la liste impossible, err à screen.setTableText(...)
		# self.placeFilterSort(self.pediaSpawnGroupScreen, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPAWNGROUP)
		# 2) trying another way, see placeFilterSort function, and specific case "elif widget == ...spawn..."
		self.placeFilterSort(self.pediaSpawnGroupScreen, WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPAWNGROUP,getNumInfos=gc.getNumSpawnGroupInfos(),getInfo=gc.getSpawnGroupInfo)

	def placeAffinities(self):
		self.placeFilterSort(self.pediaAffinityScreen, WidgetTypes.WIDGET_PEDIA_JUMP_TO_AFFINITY)

	def placeTerrains(self):
		self.placeFilterSort(self.pediaTerrain, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TERRAIN)

	def placeFeatures(self):
		self.placeFilterSort(self.pediaFeature, WidgetTypes.WIDGET_PEDIA_JUMP_TO_FEATURE)

	def placePlotEffects(self):
		self.placeFilterSort(self.pediaPlotEffect, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PLOT_EFFECT)

	def placeReligions(self):
		self.placeFilterSort(self.pediaReligion , WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION , getNumInfos=gc.getNumReligionInfos() , getInfo=gc.getReligionInfo)

	def placeCorporations(self):
		self.placeFilterSort(self.pediaCorporation , WidgetTypes.WIDGET_PEDIA_JUMP_TO_CORPORATION , getNumInfos=gc.getNumCorporationInfos() , getInfo=gc.getCorporationInfo)

	def placeSpecialists(self):
		self.placeFilterSort(self.pediaSpecialist , WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPECIALIST , getNumInfos=gc.getNumSpecialistInfos() , getInfo=gc.getSpecialistInfo)

	def placeUnitGroups(self):
		self.placeFilterSort(self.pediaUnitChart , WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT , getNumInfos=gc.getNumUnitCombatInfos() , getInfo=gc.getUnitCombatInfo)

	def placeLore(self):
		self.placeFilterSort(None , WidgetTypes.WIDGET_PEDIA_DESCRIPTION , getNumInfos=gc.getNumLoreInfos() , getInfo=gc.getLoreInfo)

	def placeConcepts(self):
		self.placeFilterSort(None , WidgetTypes.WIDGET_PEDIA_DESCRIPTION , getNumInfos=gc.getNumConceptInfos() , getInfo=gc.getConceptInfo)

	def placeFilterSort(self, pediaScreen, widget,getNumInfos=None,getInfo=None):
		screen = self.getScreen()
		if getNumInfos is None:
			list = pediaScreen.getSortedList()
		else:
			list = self.getSortedList(getNumInfos, getInfo )
		nEntries = len(list)
		stupid_offset = 2 # +2 prevents the useless scrollbar on the right
		stupid_offset2 = 7 # +7 puts tables on the correct height.
		hEntry = 24 # 24px/line
		hEntries = nEntries * hEntry + stupid_offset
		if hEntries < self.H_ITEMS_PANE: # little list -> all elements in one column centered
			nColumns = 1
			nRows = nEntries
			tableName = self.getNextWidgetName()
			screen.addTableControlGFC(tableName, 1, int((self.X_LINKS-self.W_LINKS)/2), self.Y_ITEMS_PANE+stupid_offset2, self.W_LINKS, hEntries, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
			screen.enableSelect(tableName, False)
		else: # big list
			# adapt column number to Resolution (original = 3 columns for ~740px --> ~245px/col)
			w_central_pane_Ronkhar = self.W_ITEMS_PANE
			nColumns = int(w_central_pane_Ronkhar/245)
			nRows = nEntries // nColumns
			if (nEntries % nColumns):
				nRows += 1
			tableName = self.getNextWidgetName()
			screen.addTableControlGFC(tableName, nColumns, self.X_ITEMS_PANE, self.Y_ITEMS_PANE+stupid_offset2, self.W_ITEMS_PANE, self.H_ITEMS_PANE-5, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
			screen.enableSelect(tableName, False)

		for i in range(nColumns):
			screen.setTableColumnHeader(tableName, i, "", self.W_ITEMS_PANE/nColumns)

		iCounter = 0
		iNumRows = 0
		for item in list:
			iRow = iCounter % nRows
			iColumn = iCounter // nRows
			if iRow >= iNumRows:
				iNumRows += 1
				screen.appendTableRow(tableName)
			if getNumInfos is None:
				iItem = item[2]
				szName = item[3]
				szButton = item[4]
				iAltLinker = item[5] # Seems to normally determine if there should be mouseover help offered
				screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + szName + u"</font>", szButton, widget, iItem, iAltLinker, CvUtil.FONT_LEFT_JUSTIFY)
			elif widget == WidgetTypes.WIDGET_PEDIA_DESCRIPTION: # IF Concepts OK
				if getNumInfos ==gc.getNumLoreInfos():
					screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", getInfo(item[1]).getButton(), widget, CivilopediaPageTypes.CIVILOPEDIA_PAGE_LORE, item[1], CvUtil.FONT_LEFT_JUSTIFY)
				else:
					screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", getInfo(item[1]).getButton(), widget, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, item[1], CvUtil.FONT_LEFT_JUSTIFY)

			elif widget == WidgetTypes.WIDGET_PEDIA_JUMP_TO_SPAWNGROUP: # IF spawngroups
				# API
				# VOID setTableText (STRING szName, INT iColumn, INT iRow, STRING text, STRING szIcon, WidgetType eWidgetType, INT iData1, INT iData2, INT iJustify)
				# void ( string szName, int iColumn, int iRow, wstring text, string szIcon, WidgetTypes eWidgetType, int iData1, int iData2, int iJustify )
				
				# 1) affichage de la liste OK, popup toujours "chariots", clic sur article --> err l.239 de spawngroup
				# screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", getInfo(item[1]).getButton(), widget, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPAWNGROUP, item[1],  CvUtil.FONT_LEFT_JUSTIFY)
				# screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", getInfo(item[1]).getButton(), widget, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPAWNGROUP, -1,  CvUtil.FONT_LEFT_JUSTIFY)
				# screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", getInfo(item[1]).getButton(), widget, CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPAWNGROUP, 1, CvUtil.FONT_LEFT_JUSTIFY)
				
				# 2) affichage de la liste impossible, err à la ligne ci-dessous
				#screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", getInfo(item[1]).getButton(), widget, item[1], 1,  CvUtil.FONT_LEFT_JUSTIFY)
				screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", "", widget, item[1], 1,  CvUtil.FONT_LEFT_JUSTIFY)
				# screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", getInfo(item[1]).getButton(), widget, item[1], item[1],  CvUtil.FONT_LEFT_JUSTIFY)

			else: # IF religions, corporations, specialists, categories   OK
			
				screen.setTableText(tableName, iColumn, iRow, u"<font=3>" + item[0] + u"</font>", getInfo(item[1]).getButton(), widget, item[1], 1, CvUtil.FONT_LEFT_JUSTIFY)
			iCounter += 1

		if getNumInfos is None:
			self.FILTER_DROPDOWN_ID = self.getNextWidgetName()
			screen.addDropDownBoxGFC(self.FILTER_DROPDOWN_ID, 2, 12, 260, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for i, filter in enumerate(pediaScreen.ALLOWED_FILTERS):
				screen.addPullDownString(self.FILTER_DROPDOWN_ID, eval(filter["name"]), i, i, filter == pediaScreen.CURRENT_FILTER )

			self.SORT_DROPDOWN_ID = self.getNextWidgetName()
			screen.addDropDownBoxGFC(self.SORT_DROPDOWN_ID, 260, 12, 250, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for i, sort in enumerate(pediaScreen.ALLOWED_SORTS):
				screen.addPullDownString(self.SORT_DROPDOWN_ID, eval(sort["name"]), i, i, sort == pediaScreen.CURRENT_SORT )

	def placeHints(self):
		screen = self.getScreen()

		self.szAreaId = self.getNextWidgetName()
		screen.addListBoxGFC( self.szAreaId, "", self.X_ITEMS_PANE, self.Y_ITEMS_PANE, self.W_ITEMS_PANE, self.H_ITEMS_PANE, TableStyles.TABLE_STYLE_STANDARD )

		szHintsText = CyGameTextMgr().buildHintsList()
		hintText = string.split( szHintsText, "\n" )
		for hint in hintText:
			if len( hint ) != 0:
				screen.appendListBoxStringNoUpdate( self.szAreaId, hint, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

		screen.updateListBox(self.szAreaId)

	def placeLinks(self, bRedraw): # creates the right menu
		screen = self.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.LIST_ID)

		i = 0
		for szCategory in self.listCategories:
			if bRedraw:
				screen.appendListBoxStringNoUpdate(self.LIST_ID, szCategory, WidgetTypes.WIDGET_PEDIA_MAIN, i, 0, CvUtil.FONT_LEFT_JUSTIFY )
			i += 1

		if bRedraw:
			screen.updateListBox(self.LIST_ID)

		screen.setSelectedListBoxStringGFC(self.LIST_ID, self.iCategory)

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def pediaJump(self, iScreen, iEntry, bRemoveFwdList):

		if (iEntry < 0):
			return

		self.iLastEntry = iEntry
		self.iActivePlayer = gc.getGame().getActivePlayer()

		self.pediaHistory.append((iScreen, iEntry))
		if (bRemoveFwdList):
			self.pediaFuture = []

		if (iScreen == CvScreenEnums.PEDIA_MAIN):
			self.showScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_TECH):
			self.pediaTechScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_UNIT):
			self.pediaUnitScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_BUILDING):
			self.pediaBuildingScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_PROMOTION):
			self.pediaPromotionScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_SPELL):
			self.pediaSpellScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_UNIT_CHART):
			self.pediaUnitChart.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_BONUS):
			self.pediaBonus.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_TERRAIN):
			self.pediaTerrain.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_FEATURE):
			self.pediaFeature.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_PLOT_EFFECT):
			self.pediaPlotEffect.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_IMPROVEMENT):
			self.pediaImprovement.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_CIVIC):
			self.pediaCivic.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_CIVILIZATION):
			self.pediaCivilization.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_CITYCLASS):
			self.pediaCityClass.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_ROUTE):
			self.pediaRoute.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_LEADER):
			self.pediaLeader.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_TRAIT):
			self.pediaTrait.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_SPECIALIST):
			self.pediaSpecialist.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_PROJECT):
			self.pediaProjectScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_RELIGION):
			self.pediaReligion.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_CORPORATION):
			self.pediaCorporation.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_SPAWNGROUP):
			self.pediaSpawnGroupScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_AFFINITY):
			self.pediaAffinityScreen.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_LORE):
			self.pediaLore.interfaceScreen(iEntry)
		elif (iScreen == CvScreenEnums.PEDIA_HISTORY):
			self.pediaHistorical.interfaceScreen(iEntry)

	def back(self):
		if (len(self.pediaHistory) > 1):
			self.pediaFuture.append(self.pediaHistory.pop())
			current = self.pediaHistory.pop()
			self.pediaJump(current[0], current[1], False)
		return 1

	def forward(self):
		if (self.pediaFuture):
			current = self.pediaFuture.pop()
			self.pediaJump(current[0], current[1], False)
		return 1

	def pediaShow(self):
		if (not self.pediaHistory):
			self.pediaHistory.append((CvScreenEnums.PEDIA_MAIN, 0))

		current = self.pediaHistory.pop()

		# erase history so it doesn't grow too large during the game
		self.pediaFuture = []
		self.pediaHistory = []

		# jump to the last screen that was up
		self.pediaJump(current[0], current[1], False)

	def link(self, szLink): # This function is used for all links in the pedia
		if (szLink == "PEDIA_MAIN_TECH"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH), True)
		if (szLink == "PEDIA_MAIN_UNIT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT), True)
		if (szLink == "PEDIA_MAIN_BUILDING"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING), True)
		if (szLink == "PEDIA_MAIN_TERRAIN"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN), True)
		if (szLink == "PEDIA_MAIN_FEATURE"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE), True)
		if (szLink == "PEDIA_MAIN_PLOT_EFFECT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PLOT_EFFECT), True)
		if (szLink == "PEDIA_MAIN_BONUS"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS), True)
		if (szLink == "PEDIA_MAIN_IMPROVEMENT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT), True)
		if (szLink == "PEDIA_MAIN_SPECIALIST"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST), True)
		if (szLink == "PEDIA_MAIN_PROMOTION"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION), True)
		if (szLink == "PEDIA_MAIN_SPELL"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPELL), True)
		if (szLink == "PEDIA_MAIN_UNIT_GROUP"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP), True)
		if (szLink == "PEDIA_MAIN_CIV"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV), True)
		if (szLink == "PEDIA_MAIN_CITYCLASS"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CITYCLASS), True)
		if (szLink == "PEDIA_MAIN_ROUTE"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_ROUTE), True)
		if (szLink == "PEDIA_MAIN_LEADER"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER), True)
		if (szLink == "PEDIA_MAIN_TRAIT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TRAIT), True)
		if (szLink == "PEDIA_MAIN_RELIGION"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION), True)
		if (szLink == "PEDIA_MAIN_CORPORATION"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CORPORATION), True)
		if (szLink == "PEDIA_MAIN_CIVIC"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC), True)
		if (szLink == "PEDIA_MAIN_PROJECT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT), True)
		if (szLink == "PEDIA_MAIN_SPAWNGROUP"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPAWNGROUP), True)
		if (szLink == "PEDIA_MAIN_AFFINITY"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_AFFINITY), True)
		if (szLink == "PEDIA_MAIN_LORE"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_LORE), True)
		if (szLink == "PEDIA_MAIN_CONCEPT"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT), True)
		if (szLink == "PEDIA_MAIN_HINTS"):
			return self.pediaJump(CvScreenEnums.PEDIA_MAIN, int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_HINTS), True)

		for i in range(gc.getNumLoreInfos()):
			if (gc.getLoreInfo(i).isMatchForLink(szLink, False)):
				iEntryId = self.pediaLore.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_LORE, i)
				return self.pediaJump(CvScreenEnums.PEDIA_LORE, iEntryId, True)
		for i in range(gc.getNumConceptInfos()):
			if (gc.getConceptInfo(i).isMatchForLink(szLink, False)):
				iEntryId = self.pediaHistorical.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, i)
				return self.pediaJump(CvScreenEnums.PEDIA_HISTORY, iEntryId, True)
		for i in range(gc.getNumTechInfos()):
			if (gc.getTechInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_TECH, i, True)
		for i in range(gc.getNumUnitInfos()):
			if (gc.getUnitInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_UNIT, i, True)
		for i in range(gc.getNumCorporationInfos()):
			if (gc.getCorporationInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CORPORATION, i, True)
		for i in range(gc.getNumBuildingInfos()):
			if (gc.getBuildingInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_BUILDING, i, True)
		for i in range(gc.getNumPromotionInfos()):
			if (gc.getPromotionInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_PROMOTION, i, True)
		for i in range(gc.getNumSpellInfos()):
			if (gc.getSpellInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_SPELL, i, True)
		for i in range(gc.getNumUnitCombatInfos()):
			if (gc.getUnitCombatInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_UNIT_CHART, i, True)
		for i in range(gc.getNumBonusInfos()):
			if (gc.getBonusInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_BONUS, i, True)
		for i in range(gc.getNumTerrainInfos()):
			if (gc.getTerrainInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_TERRAIN, i, True)
		for i in range(gc.getNumFeatureInfos()):
			if (gc.getFeatureInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_FEATURE, i, True)
		for i in range(gc.getNumPlotEffectInfos()):
			if (gc.getPlotEffectInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_PLOT_EFFECT, i, True)
		for i in range(gc.getNumImprovementInfos()):
			if (gc.getImprovementInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_IMPROVEMENT, i, True)
		for i in range(gc.getNumCivicInfos()):
			if (gc.getCivicInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CIVIC, i, True)
		for i in range(gc.getNumCivilizationInfos()):
			if (gc.getCivilizationInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CIVILIZATION, i, True)
		for i in range(gc.getNumCityClassInfos()):
			if (gc.getCityClassInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_CITYCLASS, i, True)
		for i in range(gc.getNumRouteInfos()):
			if (gc.getRouteInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_ROUTE, i, True)
		for i in range(gc.getNumLeaderHeadInfos()):
			if (gc.getLeaderHeadInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_LEADER, i, True)
		for i in range(gc.getNumTraitInfos()):
			if (gc.getTraitInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_TRAIT, i, True)
		for i in range(gc.getNumSpecialistInfos()):
			if (gc.getSpecialistInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_SPECIALIST, i, True)
		for i in range(gc.getNumProjectInfos()):
			if (gc.getProjectInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_PROJECT, i, True)
		for i in range(gc.getNumSpawnGroupInfos()):
			if (gc.getSpawnGroupInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_SPAWNGROUP, i, True)
		for i in range(gc.getNumAffinityInfos()):
			if (gc.getAffinityInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_AFFINITY, i, True)
		for i in range(gc.getNumReligionInfos()):
			if (gc.getReligionInfo(i).isMatchForLink(szLink, False)):
				return self.pediaJump(CvScreenEnums.PEDIA_RELIGION, i, True)

	def deleteAllWidgets(self):
		screen = self.getScreen()
		iNumWidgets = self.nWidgetCount
		self.nWidgetCount = 0
		for i in range(iNumWidgets):
			screen.deleteWidget(self.getNextWidgetName())
		self.nWidgetCount = 0

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		# redirect to proper screen if necessary
		if (self.iLastScreen == CvScreenEnums.PEDIA_UNIT or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaUnitScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_TECH or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TECH) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaTechScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_BUILDING or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_BUILDING) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaBuildingScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_PROMOTION or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROMOTION) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaPromotionScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_SPELL or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPELL) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaSpellScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_UNIT_CHART or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_UNIT_GROUP) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaUnitChart.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_BONUS or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_BONUS) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaBonus.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_TERRAIN or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TERRAIN) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaTerrain.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_FEATURE or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_FEATURE) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaFeature.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_PLOT_EFFECT or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PLOT_EFFECT) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaPlotEffect.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_IMPROVEMENT or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaImprovement.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_CIVIC or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIVIC) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaCivic.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_CIVILIZATION or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaCivilization.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_CITYCLASS or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CITYCLASS) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaCityClass.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_ROUTE or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_ROUTE) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaRoute.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_LEADER or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_LEADER) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaLeader.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_TRAIT or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_TRAIT) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaTrait.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_SPECIALIST or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPECIALIST) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaSpecialist.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_PROJECT or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_PROJECT) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaProjectScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_RELIGION or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_RELIGION) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaReligion.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_CORPORATION or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CORPORATION) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaCorporation.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_SPAWNGROUP or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_SPAWNGROUP) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaSpawnGroupScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_AFFINITY or (self.iLastEntry == int(CivilopediaPageTypes.CIVILOPEDIA_PAGE_AFFINITY) and self.iLastScreen == CvScreenEnums.PEDIA_MAIN)):
			return self.pediaAffinityScreen.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_LORE):
			return self.pediaLore.handleInput(inputClass)
		if (self.iLastScreen == CvScreenEnums.PEDIA_HISTORY):
			return self.pediaHistorical.handleInput(inputClass)

		return 0