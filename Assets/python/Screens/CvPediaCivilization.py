## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import string

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaCivilization:
	"Civilopedia Screen for Civilizations"

	def __init__(self, main):
		self.iCivilization = -1
		self.top = main

		self.FILTERS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_UNFILTERED", ())',		# Name of the filter as it appears in dropdown menu.  Needs to be unique for this screen
				"Purpose" : "Clears all currently active filters",		# Description for the sanity of those who modify this file, appears and is used nowhere else
				"Hardcoded" : False,		# If this is True, then only those items in the HardcodeList will pass the check
				"HardcodeList" : [],
				"Value to Check" : 'None',	# Note that eCiv is the CivilizationInfo object being tested
				"Desired Result" : 'None',
			},
			]

		# List the filters which you want to be available initially, or self.FILTERS to have all of them available from the start
		self.ALLOWED_FILTERS = self.FILTERS
		self.CURRENT_FILTER = self.FILTERS[0]

		self.SORTS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_ALPHABETICAL", ())',
				"Purpose" : "Default Sorting Method",
				"Value to Sort" : 'eCiv.getDescription()',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_XML_ORDER", ())',
				"Purpose" : "Default, unsorted method",
				"Value to Sort" : None,
			},
			]

		# List the sorts which you want to be available initially, or self.SORTS to have all of them available from the start
		self.ALLOWED_SORTS = self.SORTS
		self.CURRENT_SORT = self.SORTS[0]
		self.SUB_SORT = self.SORTS[0]

	# Screen construction function
	def interfaceScreen(self, iCivilization):
		self.iCivilization = iCivilization

		self.top.deleteAllWidgets()

		screen = self.top.getScreen()

		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		#Filter/Sort dropdowns
		self.top.FILTER_DROPDOWN_ID = self.top.getNextWidgetName()
		screen.addDropDownBoxGFC(self.top.FILTER_DROPDOWN_ID, self.top.X_FILTER_DROPDOWN, self.top.Y_DROPDOWN, self.top.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i, filter in enumerate(self.ALLOWED_FILTERS):
			screen.addPullDownString(self.top.FILTER_DROPDOWN_ID, eval(filter["name"]), i, i, filter == self.CURRENT_FILTER )

		self.top.SORT_DROPDOWN_ID = self.top.getNextWidgetName()
		screen.addDropDownBoxGFC(self.top.SORT_DROPDOWN_ID, self.top.X_SORT_DROPDOWN, self.top.Y_DROPDOWN, self.top.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i, sort in enumerate(self.ALLOWED_SORTS):
			screen.addPullDownString(self.top.SORT_DROPDOWN_ID, eval(sort["name"]), 1, 1, sort == self.CURRENT_SORT )

		# Header...
		szHeader = u"<font=4b>" + gc.getCivilizationInfo(self.iCivilization).getDescription().upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_CIVILIZATION or bNotActive:
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_CIVILIZATION
		else:
			self.placeLinks(false)

		self.placeBanner()
		self.placeBuilding()
		self.placeIcon()
		self.placeTech()
		self.placeUnit()
		self.placeImprovement()
		self.placeLeader()
		self.placeBlockedBuilding()
		self.placeBlockedUnit()
		self.placeBlockedImprovement()
		self.placeEffects()
		self.placeHistory()
		self.placeStrategy()
		return

	def placeBanner(self):
		# Horizontally Centred Banner (512x128)
		screen = self.top.getScreen()
		self.W_LOGO        = 512
		self.stupid_offset = 6 # the panel style creates an offset (different for each type of panel). The height we ask here is not the one we measure on the screen
		self.H_LOGO        = 128
		self.X_LOGO        = (self.top.X_LINKS - self.W_LOGO)/2 # HD example: 581.5 --> 581
		self.Y_LOGO        = 55

		if gc.getCivilizationInfo(self.iCivilization).getImage() != None:
			screen.addDDSGFC(self.top.getNextWidgetName(), gc.getCivilizationInfo(self.iCivilization).getImage(),
				self.X_LOGO , self.Y_LOGO , self.W_LOGO, self.H_LOGO, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def placeBuilding(self):
		screen = self.top.getScreen()
		self.X_BUILDING = self.top.EXT_SPACING
		self.Y_BUILDING = self.top.H_TOP_BAR + self.top.INT_SPACING
		self.W_BUILDING = self.X_LOGO - self.X_BUILDING - self.top.INT_SPACING
		self.H_BUILDING = self.top.H_BLUE50_PANEL
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_CIV_MENU_UNIQUE_BUILDINGS", ()), "", false, true,
				self.X_BUILDING, self.Y_BUILDING, self.W_BUILDING, self.H_BUILDING, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.setPanelColor(panelName, 0, 100, 0)

		# palace
		iPalace = gc.getCivilizationInfo(self.iCivilization).getCivilizationBuildings(gc.getInfoTypeForString('BUILDINGCLASS_PALACE'))
		if iPalace >0: # if not (animal or barbarian or demon) since they have no palaces
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iPalace).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iPalace, 1, False )
			screen.attachLabel(panelName, "", "|")
		# other buildings
		for iBuildingClass in range(gc.getNumBuildingClassInfos()):
			iUniqueBuilding = gc.getCivilizationInfo(self.iCivilization).getCivilizationBuildings(iBuildingClass);
			iDefaultBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex();
			if (iDefaultBuilding > -1 and iUniqueBuilding > -1 and iDefaultBuilding != iUniqueBuilding) or (iUniqueBuilding > -1 and gc.getBuildingClassInfo(iBuildingClass).isUnique()):
				if not gc.getBuildingInfo(iUniqueBuilding).isGraphicalOnly(): # hide graphical only buildings
					if iUniqueBuilding != iPalace: # We don't want a duplicate palace
						screen.attachImageButton( panelName, "", gc.getBuildingInfo(iUniqueBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iUniqueBuilding, 1, False )

	def placeIcon(self):
		# Icons
		screen = self.top.getScreen()
		self.S_ICON = 64 # icon size
		self.H_ICON_FRAME = 77 + 6 # same as techs (77 pixels visually + 6 pixels offset)
		self.W_ICON_FRAME = 82 # I guess
		self.X_ICON_FRAME = self.top.X_LINKS - self.W_ICON_FRAME - self.top.EXT_SPACING # HD example: 1594
		self.X_ICON = self.X_ICON_FRAME + 10 # HD example
		self.Y_ICON_FRAME = self.Y_BUILDING + 22 # same as techs (no title here --> offset 22)
		self.Y_ICON = self.Y_ICON_FRAME + 12 # HD example

		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
				self.X_ICON_FRAME, self.Y_ICON_FRAME,self.W_ICON_FRAME, self.H_ICON_FRAME, PanelStyles.PANEL_STYLE_BLUE50)
		civ_icon = ArtFileMgr.getCivilizationArtInfo(gc.getCivilizationInfo(self.iCivilization).getArtDefineTag()).getButton()
		screen.addDDSGFC(self.top.getNextWidgetName() , civ_icon, self.X_ICON , self.Y_ICON , self.S_ICON , self.S_ICON , WidgetTypes.WIDGET_GENERAL, -1, -1 )


	def placeTech(self):
		screen = self.top.getScreen()
		self.X_TECH = self.X_LOGO + self.W_LOGO + self.top.INT_SPACING
		self.Y_TECH = self.Y_BUILDING
		self.W_TECH = self.X_ICON_FRAME - self.X_TECH - self.top.INT_SPACING
		self.H_TECH = self.top.H_BLUE50_PANEL

		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_FREE_TECHS", ()), "", false, true,
				 self.X_TECH, self.Y_TECH, self.W_TECH, self.H_TECH, PanelStyles.PANEL_STYLE_BLUE50 )
		#screen.attachLabel(panelName, "", "  ")

		for iTech in range(gc.getNumTechInfos()):
			if (gc.getCivilizationInfo(self.iCivilization).isCivilizationFreeTechs(iTech)):
				screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )


	def placeUnit(self):
		screen = self.top.getScreen()
		self.X_UNIT = self.top.EXT_SPACING
		self.Y_UNIT = self.Y_BUILDING + self.H_BUILDING
		self.W_UNIT = self.X_TECH - self.X_UNIT - self.top.INT_SPACING
		self.H_UNIT = self.top.H_BLUE50_PANEL
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_FREE_UNITS", ()), "", false, true,
				 self.X_UNIT, self.Y_UNIT, self.W_UNIT, self.H_UNIT, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.setPanelColor(panelName, 0, 100, 0)

		# List all UnitCombats
		git = gc.getInfoTypeForString
		iRecon     = git('UNITCOMBAT_RECON')
		iArcher    = git('UNITCOMBAT_ARCHER')
		iMounted   = git('UNITCOMBAT_MOUNTED')
		iMelee     = git('UNITCOMBAT_MELEE')
		iSiege     = git('UNITCOMBAT_SIEGE')
		iAdept     = git('UNITCOMBAT_ADEPT')
		iDisciple  = git('UNITCOMBAT_DISCIPLE')
		iAnimal    = git('UNITCOMBAT_ANIMAL')
		iNaval     = git('UNITCOMBAT_NAVAL')
		iBeast     = git('UNITCOMBAT_BEAST')
		iWorker    = git('UNITCOMBAT_WORKER')
		iCommander = git('UNITCOMBAT_COMMANDER')
		iRogue     = git('UNITCOMBAT_ROGUE')
		iDefense   = git('UNITCOMBAT_DEFENSIVE_MELEE')
		
		# Create a dictionary to store Unique Units
		dictUnique = {
			"WorldUnit"   : {1:[],2:[],3:[],4:[]},
			iRecon        : {1:[],2:[],3:[],4:[]},
			iArcher       : {1:[],2:[],3:[],4:[]},
			iMounted      : {1:[],2:[],3:[],4:[]},
			iMelee        : {1:[],2:[],3:[],4:[]},
			iSiege        : {1:[],2:[],3:[],4:[]},
			iAdept        : {1:[],2:[],3:[],4:[]},
			iDisciple     : {1:[],2:[],3:[],4:[]},
			iAnimal       : {1:[],2:[],3:[],4:[]},
			iNaval        : {1:[],2:[],3:[],4:[]},
			iBeast        : {1:[],2:[],3:[],4:[]},
			iWorker       : {1:[],2:[],3:[],4:[]},
			iCommander    : {1:[],2:[],3:[],4:[]},
			iRogue        : {1:[],2:[],3:[],4:[]},
			iDefense      : {1:[],2:[],3:[],4:[]},
			"noUnitCombat": {1:[],2:[],3:[],4:[]},
			"noTier"      : {1:[]}
		}
		
		# World units 1st, then normal UnitCombats, then units missing either UnitCombat or Tier
		listOrdered = ["WorldUnit", iMelee, iDefense, iRecon, iRogue, iMounted, iArcher, iSiege, iAdept, iDisciple, iCommander, iWorker, iNaval, iAnimal, iBeast, "noUnitCombat","noTier"]
		bPipe = False
		listUnique = []
		
		# Find and sort Unique Units
		for iUnit in range(gc.getNumUnitClassInfos()):
			iUniqueUnit = gc.getCivilizationInfo(self.iCivilization).getCivilizationUnits(iUnit);
			iDefaultUnit = gc.getUnitClassInfo(iUnit).getDefaultUnitIndex();
			if (iDefaultUnit > -1 and iUniqueUnit > -1 and iDefaultUnit != iUniqueUnit) or (iUniqueUnit > -1 and gc.getUnitClassInfo(iUnit).isUnique()):
				if not iUniqueUnit in listUnique:# If there is a duplicate unit, we ignore it
					listUnique.append(iUniqueUnit)
					info = gc.getUnitInfo(iUniqueUnit)
					iTier = info.getTier()
					if iTier in [1,2,3,4]:
						if isWorldUnitClass(info.getUnitClassType()):
							dictUnique["WorldUnit"][iTier].append(iUniqueUnit)
						else:#if not a World Unit
							iUnitCombat = info.getUnitCombatType()
							if iUnitCombat in listOrdered:
								dictUnique[iUnitCombat][iTier].append(iUniqueUnit)
							else:#if noUnitCombat (golems...)
								dictUnique["noUnitCombat"][iTier].append(iUniqueUnit)
					else:#if noTier (fort commanders and forgotten units: Mother, baby spider...)
							dictUnique["noTier"][1].append(iUniqueUnit)
		
		# Show Unique Units in the specified order
		for keyUnitCombat in listOrdered:
			dictUnitCombat = dictUnique[keyUnitCombat]
			for keyTier in dictUnitCombat:
				listTier = dictUnitCombat[keyTier]
				if listTier:
					if bPipe:
						screen.attachLabel(panelName, "", "|")
						bPipe = False
					for iUniqueUnit in listTier:
						szButton = gc.getUnitInfo(iUniqueUnit).getButton()
						if self.top.iActivePlayer != -1:
							szButton = gc.getPlayer(self.top.iActivePlayer).getUnitButton(iUniqueUnit)
						screen.attachImageButton( panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iUniqueUnit, 1, False )
			bPipe = True

	def placeImprovement(self):
		screen = self.top.getScreen()
		self.X_IMP = self.top.EXT_SPACING
		self.Y_IMP = self.Y_UNIT + self.H_UNIT
		self.W_IMP = self.W_BUILDING
		self.H_IMP = self.top.H_BLUE50_PANEL
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_CIV_MENU_UNIQUE_IMPROVEMENTS", ()), "", false, true,
				self.X_IMP, self.Y_IMP, self.W_IMP, self.H_IMP, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.setPanelColor(panelName, 0, 100, 0)
		
		for iImprovementClass in range(gc.getNumImprovementClassInfos()):
			iUniqueImprovement = gc.getCivilizationInfo(self.iCivilization).getCivilizationImprovements(iImprovementClass);
			iDefaultImprovement = gc.getImprovementClassInfo(iImprovementClass).getDefaultImprovementIndex();
			if (iDefaultImprovement > -1 and iUniqueImprovement > -1 and iDefaultImprovement != iUniqueImprovement) or (iUniqueImprovement > -1 and gc.getImprovementClassInfo(iImprovementClass).isUnique()):
				if not gc.getImprovementInfo(iUniqueImprovement).isGraphicalOnly():
					screen.attachImageButton( panelName, "", gc.getImprovementInfo(iUniqueImprovement).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iUniqueImprovement, 1, False )

	def placeLeader(self):
		screen = self.top.getScreen()
		self.X_LEADER = self.X_TECH
		self.Y_LEADER = self.Y_UNIT
		self.W_LEADER = self.top.X_LINKS - self.X_LEADER - self.top.EXT_SPACING
		self.H_LEADER = self.top.H_BLUE50_PANEL
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_LEADER", ()), "", false, true,
				 self.X_LEADER, self.Y_LEADER, self.W_LEADER, self.H_LEADER, PanelStyles.PANEL_STYLE_BLUE50 )

		# sort leaders by status : historical, important, emergent
		for iLeader in range(gc.getNumLeaderHeadInfos()):
			civ = gc.getCivilizationInfo(self.iCivilization)
			if civ.isPediaLeaders(iLeader):
				eLeader = gc.getLeaderHeadInfo(iLeader)
			#	if eLeader.getLeaderStatus() == gc.getInfoTypeForString("HISTORICAL_STATUS"):
				if gc.getLeaderClassInfo(eLeader.getLeaderClass()).getLeaderStatus() == gc.getInfoTypeForString("HISTORICAL_STATUS"):
					screen.attachImageButton( panelName, "", gc.getLeaderHeadInfo(iLeader).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, self.iCivilization, False )

		first = true
		for iLeader in range(gc.getNumLeaderHeadInfos()):
			civ = gc.getCivilizationInfo(self.iCivilization)
			if civ.isPediaLeaders(iLeader):
				eLeader = gc.getLeaderHeadInfo(iLeader)
			#	if eLeader.getLeaderStatus() == gc.getInfoTypeForString("IMPORTANT_STATUS"):
				if gc.getLeaderClassInfo(eLeader.getLeaderClass()).getLeaderStatus() == gc.getInfoTypeForString("IMPORTANT_STATUS"):
					if first == true:
						screen.attachLabel(panelName, "", "|")
						first = false
					screen.attachImageButton( panelName, "", gc.getLeaderHeadInfo(iLeader).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, self.iCivilization, False )

		first = true
		for iLeader in range(gc.getNumLeaderHeadInfos()):
			civ = gc.getCivilizationInfo(self.iCivilization)
			if civ.isPediaLeaders(iLeader):
				eLeader = gc.getLeaderHeadInfo(iLeader)
			#	if eLeader.getLeaderStatus() == gc.getInfoTypeForString("EMERGENT_STATUS"):
				if gc.getLeaderClassInfo(eLeader.getLeaderClass()).getLeaderStatus() == gc.getInfoTypeForString("EMERGENT_STATUS"):
					if first == true:
						screen.attachLabel(panelName, "", "|")
						first = false
					screen.attachImageButton( panelName, "", gc.getLeaderHeadInfo(iLeader).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, self.iCivilization, False )

	def placeBlockedBuilding(self):
		screen = self.top.getScreen()
		self.X_XBUILDING = self.top.EXT_SPACING
		self.Y_XBUILDING = self.Y_IMP + self.H_IMP
		self.W_XBUILDING = self.W_BUILDING
		self.H_XBUILDING = self.top.H_BLUE50_PANEL
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CIV_MENU_BLOCKED_BUILDINGS", ()), "", False, True, self.X_XBUILDING, self.Y_XBUILDING, self.W_XBUILDING, self.H_XBUILDING, PanelStyles.PANEL_STYLE_BLUE50)
		screen.setPanelColor(panelName, 206, 65, 69)
		#screen.attachLabel(panelName, "", "  ")

		for iBuildingClass in range(gc.getNumBuildingClassInfos()):
			iUniqueBuilding = gc.getCivilizationInfo(self.iCivilization).getCivilizationBuildings(iBuildingClass);
			iDefaultBuilding = gc.getBuildingClassInfo(iBuildingClass).getDefaultBuildingIndex();
			if iDefaultBuilding != BuildingTypes.NO_BUILDING and not gc.getBuildingClassInfo(iBuildingClass).isUnique() and not gc.getBuildingInfo(iDefaultBuilding).isGraphicalOnly():
				if iUniqueBuilding == BuildingTypes.NO_BUILDING:
					szButton = gc.getBuildingInfo(iDefaultBuilding).getButton()
					screen.attachImageButton(panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iDefaultBuilding, 1, False)

	def placeBlockedUnit(self):
		screen = self.top.getScreen()
		self.X_XUNIT = self.top.EXT_SPACING
		self.Y_XUNIT = self.Y_XBUILDING + self.H_XBUILDING
		self.W_XUNIT = self.W_BUILDING
		self.H_XUNIT = self.top.H_BLUE50_PANEL
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CIV_MENU_BLOCKED_UNITS", ()), "", False, True, self.X_XUNIT, self.Y_XUNIT, self.W_XUNIT, self.H_XUNIT, PanelStyles.PANEL_STYLE_BLUE50)
		screen.setPanelColor(panelName, 206, 65, 69)
		#screen.attachLabel(panelName, "", "  ")

		for iUnitClass in range(gc.getNumUnitClassInfos()):
			iUniqueUnit = gc.getCivilizationInfo(self.iCivilization).getCivilizationUnits(iUnitClass);
			iDefaultUnit = gc.getUnitClassInfo(iUnitClass).getDefaultUnitIndex();
			if iDefaultUnit != UnitTypes.NO_UNIT and not gc.getUnitClassInfo(iUnitClass).isUnique():
				if iUniqueUnit == UnitTypes.NO_UNIT:
					szButton = gc.getUnitInfo(iDefaultUnit).getButton()
					screen.attachImageButton(panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, iDefaultUnit, 1, False)

	def placeBlockedImprovement(self):
		screen = self.top.getScreen()
		self.X_XIMP = self.top.EXT_SPACING
		self.Y_XIMP = self.Y_XUNIT + self.H_XUNIT
		self.W_XIMP = self.W_BUILDING
		self.H_XIMP = self.top.H_BLUE50_PANEL
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CIV_MENU_BLOCKED_IMPROVEMENTS", ()), "", False, True, self.X_XIMP, self.Y_XIMP, self.W_XIMP, self.H_XIMP, PanelStyles.PANEL_STYLE_BLUE50)
		screen.setPanelColor(panelName, 206, 65, 69)
		
		for iImprovementClass in range(gc.getNumImprovementClassInfos()):
			iUniqueImprovement = gc.getCivilizationInfo(self.iCivilization).getCivilizationImprovements(iImprovementClass);
			iDefaultImprovement = gc.getImprovementClassInfo(iImprovementClass).getDefaultImprovementIndex();
			if iDefaultImprovement != ImprovementTypes.NO_IMPROVEMENT and not gc.getImprovementClassInfo(iImprovementClass).isUnique():
				if iUniqueImprovement == ImprovementTypes.NO_IMPROVEMENT:
					szButton = gc.getImprovementInfo(iDefaultImprovement).getButton()
					screen.attachImageButton(panelName, "", szButton, GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iDefaultImprovement, 1, False)

	def placeEffects(self):
		screen = self.top.getScreen()
		self.X_EFFECTS = self.top.EXT_SPACING
		self.Y_EFFECTS = self.Y_XIMP + self.H_XIMP
		self.H_EFFECTS = self.top.H_SCREEN - self.top.H_BOT_BAR - self.top.EXT_SPACING - self.Y_EFFECTS
		self.W_EFFECTS = self.W_BUILDING
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_EFFECTS", ()), "", true, false,
				 self.X_EFFECTS, self.Y_EFFECTS, self.W_EFFECTS, self.H_EFFECTS, PanelStyles.PANEL_STYLE_BLUE50 )
		#screen.attachLabel(panelName, "", " ")

		szName = self.top.getNextWidgetName()
		szText = CyGameTextMgr().parseMoreCivInfos(self.iCivilization, False, True, True)

		lMaintainedFeatures = []
		for iFeature in range(gc.getNumFeatureInfos()):
			if gc.getCivilizationInfo(self.iCivilization).isMaintainFeatures(iFeature):
				lMaintainedFeatures.append(iFeature)
		if lMaintainedFeatures:
			szText += "\n\n" + localText.getText("TXT_KEY_PEDIA_CIV_MENU_MAINTAINED_FEATURES", ()) + " "
			iLastFeature = lMaintainedFeatures[-1]
			for iFeature in lMaintainedFeatures:
				szText += gc.getFeatureInfo(iFeature).getDescription()
				if iFeature != iLastFeature:
					szText += ", "

		lUniqueSpecialists = []
		lBlockedSpecialists = []
		for iSpecialistClass in range(gc.getNumSpecialistClassInfos()):
			iUniqueSpecialist = gc.getCivilizationInfo(self.iCivilization).getCivilizationSpecialists(iSpecialistClass)
			iDefaultSpecialist = gc.getSpecialistClassInfo(iSpecialistClass).getDefaultSpecialistIndex()
			bUniqueClass = gc.getSpecialistClassInfo(iSpecialistClass).isUnique()
			if iUniqueSpecialist > -1:
				if (iDefaultSpecialist > -1 and iDefaultSpecialist != iUniqueSpecialist) or bUniqueClass:
					if not gc.getSpecialistInfo(iUniqueSpecialist).isGraphicalOnly():
						lUniqueSpecialists.append(iUniqueSpecialist)
			else:
				if iDefaultSpecialist > -1 and not bUniqueClass:
					if not gc.getSpecialistInfo(iDefaultSpecialist).isGraphicalOnly():
						lBlockedSpecialists.append(iDefaultSpecialist)

		if lUniqueSpecialists:
			szText += "\n\n" + localText.getText("TXT_KEY_PEDIA_CIV_MENU_UNIQUE_SPECIALISTS", ()) + " "
			for iIndex in range(len(lUniqueSpecialists)):
				if iIndex > 0:
					szText += ", "
				szText += gc.getSpecialistInfo(lUniqueSpecialists[iIndex]).getDescription()

		if lBlockedSpecialists:
			szText += "\n\n" + localText.getText("TXT_KEY_PEDIA_CIV_MENU_BLOCKED_SPECIALISTS", ()) + " "
			for iIndex in range(len(lBlockedSpecialists)):
				if iIndex > 0:
					szText += ", "
				szText += gc.getSpecialistInfo(lBlockedSpecialists[iIndex]).getDescription()

		screen.attachMultilineText( panelName, szName, szText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeHistory(self):
		screen = self.top.getScreen()

		self.X_HISTORY = self.X_LOGO
		self.Y_HISTORY = self.Y_IMP
		self.W_HISTORY = self.top.X_LINKS - self.X_HISTORY - self.top.EXT_SPACING
		# the remaining vertical space under the logo is split in 2. upper-half --> History ; bottom-half --> Strategy
		self.H_HISTORY = int(0.5 * (self.top.H_SCREEN-self.top.H_BOT_BAR-self.top.EXT_SPACING-self.Y_HISTORY))
		HistoryPanel = self.top.getNextWidgetName()
		screen.addPanel( HistoryPanel, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True, self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )
		# InterfaceUpgrade: Better Pedia - Added by Grey Fox 04/18/2008
		HistoryTextPanel = self.top.getNextWidgetName()
		screen.addPanel( HistoryTextPanel, "", "", true, true,self.X_HISTORY+self.top.HM_TEXT, self.Y_HISTORY+self.top.VM_TEXT, self.W_HISTORY - 2 * self.top.HM_TEXT, self.H_HISTORY - self.top.VM_TEXT, PanelStyles.PANEL_STYLE_EMPTY)
		# InterfaceUpgrade: Better Pedia - End Add
		HistoryText = gc.getCivilizationInfo(self.iCivilization).getCivilopedia()
		screen.attachMultilineText( HistoryTextPanel, "", HistoryText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeStrategy(self):
		screen = self.top.getScreen()
		self.X_STRATEGY = self.X_HISTORY
		self.Y_STRATEGY = self.Y_HISTORY + self.H_HISTORY
		self.W_STRATEGY = self.W_HISTORY
		self.H_STRATEGY = self.H_HISTORY
		StrategyPanel = self.top.getNextWidgetName()
		screen.addPanel( StrategyPanel, localText.getText("TXT_KEY_STRATEGY", ()), "", true, true,self.X_STRATEGY, self.Y_STRATEGY, self.W_STRATEGY, self.H_STRATEGY, PanelStyles.PANEL_STYLE_BLUE50 )
		StrategyTextPanel = self.top.getNextWidgetName()
		screen.addPanel( StrategyTextPanel, "", "", true, true,self.X_STRATEGY+self.top.HM_TEXT, self.Y_STRATEGY+self.top.VM_TEXT, self.W_STRATEGY - 2 * self.top.HM_TEXT, self.H_STRATEGY - self.top.VM_TEXT, PanelStyles.PANEL_STYLE_EMPTY)
		StrategyText = gc.getCivilizationInfo(self.iCivilization).getStrategy()
		screen.attachMultilineText( StrategyTextPanel, "", StrategyText,WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)

		listSorted = self.getSortedList()

		i = 0
		iSelected = 0
		for iI in range(len(listSorted)):
			iCiv = listSorted[iI][2]
			szName = listSorted[iI][3]
			if bRedraw:
				screen.appendListBoxString(self.top.LIST_ID, szName, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if iCiv == self.iCivilization:
				iSelected = i
			i += 1

		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

	def getSortedList(self):
		listCivs = []
		iCount = 0
		for iCiv in range(gc.getNumCivilizationInfos()):
			eCiv = gc.getCivilizationInfo(iCiv)
			if not eCiv.isGraphicalOnly():
				if self.CURRENT_FILTER["Hardcoded"]:
					for civ in self.CURRENT_FILTER["HardcodeList"]:
						if iCiv == gc.getInfoTypeForString(civ):
							listCivs.append(iCiv)
							iCount += 1
				elif eval(self.CURRENT_FILTER["Value to Check"]) == eval(self.CURRENT_FILTER["Desired Result"]):
					listCivs.append(iCiv)
					iCount += 1

		listSorted = [(0,0,0,0,0,0)] * iCount
		iI = 0
		for iCiv in listCivs:
			eCiv = gc.getCivilizationInfo(iCiv)
			sort1 = 0
			sort2 = 0
			if not self.CURRENT_SORT["Value to Sort"] == None:
				sort1 = eval(self.CURRENT_SORT["Value to Sort"])
				if not self.SUB_SORT["Value to Sort"] == None:
					sort2 = eval(self.SUB_SORT["Value to Sort"])
			listSorted[iI] = (sort1, sort2, iCiv, eCiv.getDescription(), eCiv.getButton(), 1)
			iI += 1
		listSorted.sort()

		return listSorted

	def applyFilterSort(self, filter, sort):
		if not self.CURRENT_SORT == sort:
			self.SUB_SORT = self.CURRENT_SORT
			self.CURRENT_SORT = sort
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV, True)

		if not self.CURRENT_FILTER == filter:
			self.CURRENT_FILTER = filter
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_CIV, True)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.top.getScreen()
			iFilterIndex = screen.getSelectedPullDownID(self.top.FILTER_DROPDOWN_ID)
			iSortIndex = screen.getSelectedPullDownID(self.top.SORT_DROPDOWN_ID)
			self.applyFilterSort(self.ALLOWED_FILTERS[iFilterIndex], self.ALLOWED_SORTS[iSortIndex])
			return 1

		return 0