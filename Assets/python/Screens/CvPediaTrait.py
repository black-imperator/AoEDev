## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import random

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaTrait:
	"Civilopedia Screen for Traits"

	def __init__(self, main):
		self.iTrait = -1
		self.top = main
		self.modular_update=False
		
		self.FILTERS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_UNFILTERED", ())',		# Name of the filter as it appears in dropdown menu.  Needs to be unique for this screen
				"Purpose" : "Clears all currently active filters",		# Description for the sanity of those who modify this file, appears and is used nowhere else
				"Hardcoded" : False,		# If this is True, then only those items in the HardcodeList will pass the check
				"HardcodeList" : [],
				"Value to Check" : 'None',	# Note that eTrait is the TraitInfo object being tested
				"Desired Result" : 'None',
			},
			{
				"name" : 'localText.getText("TXT_KEY_TRAIT_ADAPTIVE", ())',
				"Purpose" : "Traits available to Adaptive Leaders",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTrait.isSelectable()',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_TRAITCLASS_CIVILIZATION", ())',
				"Purpose" : "Civilization Traits",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTrait.getTraitClass()',
				"Desired Result" : 'gc.getInfoTypeForString("TRAITCLASS_CIVILIZATION")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_TRAITCLASS_PERSONALITY", ())',
				"Purpose" : "Civilization Traits",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTrait.getTraitClass()',
				"Desired Result" : 'gc.getInfoTypeForString("TRAITCLASS_PERSONALITY")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_TRAITCLASS_EMERGENT", ())',
				"Purpose" : "Civilization Traits",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTrait.getTraitClass()',
				"Desired Result" : 'gc.getInfoTypeForString("TRAITCLASS_EMERGENT")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_TRAITCLASS_KEEPERS", ())',
				"Purpose" : "Civilization Traits",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTrait.getTraitClass()',
				"Desired Result" : 'gc.getInfoTypeForString("TRAITCLASS_KEEPERS")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_TRAITCLASS_SAVAGE", ())',
				"Purpose" : "Civilization Traits",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTrait.getTraitClass()',
				"Desired Result" : 'gc.getInfoTypeForString("TRAITCLASS_SAVAGE")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_TRAITCLASS_REPUBLIC", ())',
				"Purpose" : "Civilization Traits",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTrait.getTraitClass()',
				"Desired Result" : 'gc.getInfoTypeForString("TRAITCLASS_REPUBLIC")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_TRAITCLASS_KAHD", ())',
				"Purpose" : "Civilization Traits",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTrait.getTraitClass()',
				"Desired Result" : 'gc.getInfoTypeForString("TRAITCLASS_KAHD")',
			},
			{
				"name" : 'localText.getText("TXT_KEY_TRAITCLASS_DEMON_PACT", ())',
				"Purpose" : "Demon Pacts",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eTrait.getTraitClass()',
				"Desired Result" : 'gc.getInfoTypeForString("TRAITCLASS_DEMON_PACT")',
			},
			]

			# List the filters which you want to be available initially, or self.FILTERS to have all of them available from the start
		self.ALLOWED_FILTERS = self.FILTERS
		self.CURRENT_FILTER = self.FILTERS[0]

		self.SORTS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_ALPHABETICAL", ())',
				"Purpose" : "Default Sorting Method",
				"Value to Sort" : 'eTrait.getDescription()',
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
	def interfaceScreen(self, iTrait):
	
		
		self.iTrait = iTrait

		self.top.deleteAllWidgets()

		screen = self.top.getScreen()

		bNotActive = (not screen.isActive())
		if bNotActive:
			self.top.setPediaCommonWidgets()

		#Filter/Sort dropdowns
		self.top.FILTER_DROPDOWN_ID = self.top.getNextWidgetName()
		screen.addDropDownBoxGFC(self.top.FILTER_DROPDOWN_ID,self.top.X_FILTER_DROPDOWN, self.top.Y_DROPDOWN, self.top.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i, filter in enumerate(self.ALLOWED_FILTERS):
			screen.addPullDownString(self.top.FILTER_DROPDOWN_ID, eval(filter["name"]), i, i, filter == self.CURRENT_FILTER )

		self.top.SORT_DROPDOWN_ID = self.top.getNextWidgetName()
		screen.addDropDownBoxGFC(self.top.SORT_DROPDOWN_ID, self.top.X_SORT_DROPDOWN, self.top.Y_DROPDOWN, self.top.W_DROPDOWN, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		for i, sort in enumerate(self.ALLOWED_SORTS):
			screen.addPullDownString(self.top.SORT_DROPDOWN_ID, eval(sort["name"]), 1, 1, sort == self.CURRENT_SORT )

		# Header...
		if gc.getTraitInfo(self.iTrait).getLevel()>0:
			szHeader = u"<font=4b>" + gc.getTraitInfo(self.iTrait).getDescription().upper()+ localText.getText("INTERFACE_PANE_LEVEL", ()).upper() +" "+  str(gc.getTraitInfo(self.iTrait).getLevel()) + u"</font>"
		else:
			szHeader = u"<font=4b>" + gc.getTraitInfo(self.iTrait).getDescription().upper() + u"</font>"
		
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Title (upper-right corner, above the list)
		szHeader = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_CATEGORY_TRAIT", ()).upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.W_SCREEN -self.top.W_LINKS/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TRAIT, -1)

		# Top
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TRAIT, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_TRAIT or bNotActive:
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_TRAIT
		else:
			self.placeLinks(false)

		self.placeLeaders()
		self.placeDetails()
		self.placeHistory()
		self.placeStrategy()

	def placeLeaders(self):
		screen = self.top.getScreen()
		self.X_LEADERS = self.top.EXT_SPACING
		self.Y_LEADERS = self.top.H_TOP_BAR + self.top.INT_SPACING
		self.W_LEADERS = 300
		self.H_LEADERS = 300
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, "", "", false, false,self.X_LEADERS, self.Y_LEADERS, self.W_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_MAIN_BLACK50)
		tableName = self.top.getNextWidgetName()
		stupid_offset2 = 7 # +7 puts tables on the correct height.
		screen.addTableControlGFC(tableName, 1, self.X_LEADERS, self.Y_LEADERS+stupid_offset2, self.W_LEADERS, self.H_LEADERS-stupid_offset2, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD);
		screen.enableSelect(tableName, False)
		screen.setTableColumnHeader(tableName, 0, "", self.W_LEADERS)

		iRow = 0
		iNumRows = 0
		for iLeader in range(gc.getNumLeaderHeadInfos()):
			eLeader = gc.getLeaderHeadInfo(iLeader)
			if eLeader.hasTrait(self.iTrait) and not eLeader.isGraphicalOnly():
				if iRow >= iNumRows:
					iNumRows += 1
					screen.appendTableRow(tableName)

				iBestCiv = -1 # test Ronkhar 2013-12-03 to avoid a bug with leaders without civilizations (Kahd) --> instead of "iBestCiv not assigned", we see Kahd but no info popup or link
				for iCiv in range(gc.getNumCivilizationInfos()):
					eCiv = gc.getCivilizationInfo(iCiv)
					if eCiv.isPediaLeaders(iLeader):
						iBestCiv = iCiv
						break

				screen.setTableText(tableName, 0, iRow, u"<font=3>" + eLeader.getDescription() + u"</font>", eLeader.getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_LEADER, iLeader, iBestCiv, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1
		for iCiv in range(gc.getNumCivilizationInfos()):
			eCiv = gc.getCivilizationInfo(iCiv)
			if eCiv.getCivTrait() == self.iTrait:
				if iRow >= iNumRows:
					iNumRows += 1
					screen.appendTableRow(tableName)
				screen.setTableText(tableName, 0, iRow, u"<font=3>" + eCiv.getDescription() + u"</font>", eCiv.getButton(), WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, iCiv, 1, CvUtil.FONT_LEFT_JUSTIFY)
				iRow += 1

	def placeDetails(self):
		screen = self.top.getScreen()
		self.X_DETAILS = self.X_LEADERS + self.W_LEADERS + self.top.INT_SPACING
		self.Y_DETAILS = self.Y_LEADERS
		self.W_DETAILS = self.top.X_LINKS - self.X_DETAILS - self.top.EXT_SPACING
		self.H_DETAILS = self.H_LEADERS
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, "", "", true, true,
			self.X_DETAILS, self.Y_DETAILS, self.W_DETAILS, self.H_DETAILS, PanelStyles.PANEL_STYLE_BLUE50 )

		detailsTextName = self.top.getNextWidgetName()
		DetailsText = CyGameTextMgr().parseTraits(self.iTrait, -1, false)
		DetailsText = u"<font=2>" + DetailsText + u"</font>"
		screen.attachMultilineText( panelName, detailsTextName, DetailsText,
			WidgetTypes.WIDGET_GENERAL,-1,-1, CvUtil.FONT_LEFT_JUSTIFY )

	def placeHistory(self):
		screen = self.top.getScreen()
		self.X_HISTORY = self.X_LEADERS
		self.Y_HISTORY = self.Y_LEADERS + self.H_LEADERS
		# the remaining horizontal space is split in 2. left --> History ; right --> Strategy
		self.W_HISTORY = int(0.5*(self.top.X_LINKS - self.top.EXT_SPACING*2 - self.top.INT_SPACING))
		self.H_HISTORY = self.top.H_SCREEN - self.top.H_BOT_BAR - self.top.EXT_SPACING - self.Y_HISTORY
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", True, True,
						self.X_HISTORY, self.Y_HISTORY,self.W_HISTORY, self.H_HISTORY,
						PanelStyles.PANEL_STYLE_BLUE50 )
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, "", "", true, true,self.X_HISTORY+self.top.HM_TEXT, self.Y_HISTORY+self.top.VM_TEXT, self.W_HISTORY - 2 * self.top.HM_TEXT, self.H_HISTORY - self.top.VM_TEXT, PanelStyles.PANEL_STYLE_EMPTY)
		HistoryText = gc.getTraitInfo(self.iTrait).getCivilopedia()
		screen.attachMultilineText( panelName, "", HistoryText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeStrategy(self):
		screen = self.top.getScreen()
		self.X_STRATEGY = self.X_HISTORY + self.W_HISTORY + self.top.INT_SPACING
		self.Y_STRATEGY = self.Y_HISTORY
		# the remaining horizontal space is split in 2. left --> History ; right --> Strategy
		self.W_STRATEGY = self.W_HISTORY
		self.H_STRATEGY = self.H_HISTORY
		StrategyPanel = self.top.getNextWidgetName()
		screen.addPanel( StrategyPanel, localText.getText("TXT_KEY_STRATEGY", ()), "", True, True,
						self.X_STRATEGY, self.Y_STRATEGY,self.W_STRATEGY, self.H_STRATEGY,
						PanelStyles.PANEL_STYLE_BLUE50 )
		StrategyTextPanel = self.top.getNextWidgetName()
		screen.addPanel( StrategyTextPanel, "", "", true, true,self.X_STRATEGY+self.top.HM_TEXT, self.Y_STRATEGY+self.top.VM_TEXT, self.W_STRATEGY - 2 * self.top.HM_TEXT, self.H_STRATEGY - self.top.VM_TEXT, PanelStyles.PANEL_STYLE_EMPTY)
		StrategyText = gc.getTraitInfo(self.iTrait).getStrategy()
		screen.attachMultilineText( StrategyTextPanel, "", StrategyText, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.attachMultilineText( StrategyTextPanel,  "" , u"<font=2>"+   CyGameTextMgr().parseTraitReqs(self.iTrait)+ u"</font>", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()
		
		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)

		listSorted = self.getSortedList()

		i = 0
		iSelected = 0
		for iI in range(len(listSorted)):
			iTrait = listSorted[iI][2]
			szName = listSorted[iI][3]
			if bRedraw:
				screen.appendListBoxString(self.top.LIST_ID, szName, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TRAIT, iTrait, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if iTrait == self.iTrait:
				iSelected = i
			i += 1

		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

	def getSortedList(self):
		listTraits = []
		iCount = 0
		for iTrait in range(gc.getNumTraitInfos()):
			eTrait = gc.getTraitInfo(iTrait)
			if not eTrait.isGraphicalOnly():
				if self.CURRENT_FILTER["Hardcoded"]:
					for trait in self.CURRENT_FILTER["HardcodeList"]:
						if iTrait == gc.getInfoTypeForString(trait):
							listTraits.append(iTrait)
							iCount += 1
				elif eval(self.CURRENT_FILTER["Value to Check"]) == eval(self.CURRENT_FILTER["Desired Result"]):
					listTraits.append(iTrait)
					iCount += 1

		listSorted = [(0,0,0,0,0,0)] * iCount
		iI = 0
		for iTrait in listTraits:
			eTrait = gc.getTraitInfo(iTrait)
			sort1 = 0
			sort2 = 0
			if not self.CURRENT_SORT["Value to Sort"] == None:
				sort1 = eval(self.CURRENT_SORT["Value to Sort"])
				if self.CURRENT_SORT["Value to Sort"] == 'eTrait.getDescription()':
					sort1 = CvUtil.removeAccent(self,sort1) # alphabetical sorting in the Pedia for languages using accents/diacritics
				if not self.SUB_SORT["Value to Sort"] == None:
					sort2 = eval(self.SUB_SORT["Value to Sort"])
					
			if eTrait.getLevel()>0:
				listSorted[iI] = (sort1, sort2, iTrait, eTrait.getDescription() + " " + localText.getText("INTERFACE_PANE_LEVEL", ()) + " " + str(eTrait.getLevel()) , eTrait.getButton(), 1)
			else:
				listSorted[iI] = (sort1, sort2, iTrait, eTrait.getDescription(), eTrait.getButton(), 1)
				
			iI += 1
		listSorted.sort()

		return listSorted

	def applyFilterSort(self, filter, sort):
		if not self.CURRENT_SORT == sort:
			self.SUB_SORT = self.CURRENT_SORT
			self.CURRENT_SORT = sort
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TRAIT, True)

		if not self.CURRENT_FILTER == filter:
			self.CURRENT_FILTER = filter
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_TRAIT, True)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.top.getScreen()
			iFilterIndex = screen.getSelectedPullDownID(self.top.FILTER_DROPDOWN_ID)
			iSortIndex = screen.getSelectedPullDownID(self.top.SORT_DROPDOWN_ID)
			self.applyFilterSort(self.ALLOWED_FILTERS[iFilterIndex], self.ALLOWED_SORTS[iSortIndex])
			return 1

		return 0