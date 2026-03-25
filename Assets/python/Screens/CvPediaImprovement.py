## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvPediaImprovement:
	"Civilopedia Screen for tile Improvements"

	def __init__(self, main):
		self.iImprovement = -1
		self.top = main

		self.X_UPPER_PANE = 20
		self.Y_UPPER_PANE = 65
		self.W_UPPER_PANE = 433
		self.H_UPPER_PANE = 210

		self.X_IMPROVEMENT_ANIMATION = 475
		self.Y_IMPROVEMENT_ANIMATION = 73
		self.W_IMPROVEMENT_ANIMATION = 303
		self.H_IMPROVEMENT_ANIMATION = 200
		self.X_ROTATION_IMPROVEMENT_ANIMATION = -20
		self.Z_ROTATION_IMPROVEMENT_ANIMATION = 30
		self.SCALE_ANIMATION = 0.8

		self.X_ICON = 48
		self.Y_ICON = 105
		self.W_ICON = 150
		self.H_ICON = 150
		self.ICON_SIZE = 64

		self.X_COST = 225
		self.Y_COST = 115

		self.X_IMPROVEMENTS_PANE = self.X_UPPER_PANE
		self.Y_IMPROVEMENTS_PANE = self.Y_UPPER_PANE + self.H_UPPER_PANE + 20
		self.W_IMPROVEMENTS_PANE = 500
		self.H_IMPROVEMENTS_PANE = 250

		self.X_BONUS_YIELDS_PANE = self.X_IMPROVEMENTS_PANE + self.W_IMPROVEMENTS_PANE + 25
		self.Y_BONUS_YIELDS_PANE = self.Y_UPPER_PANE + self.H_UPPER_PANE + 20
		self.W_BONUS_YIELDS_PANE = 230
		self.H_BONUS_YIELDS_PANE = 402

		self.X_REQUIRES = self.X_UPPER_PANE
		self.Y_REQUIRES = self.Y_IMPROVEMENTS_PANE + self.H_IMPROVEMENTS_PANE + 20
		self.W_REQUIRES = 500
		self.H_REQUIRES = 110

		self.X_HISTORY = self.X_UPPER_PANE
		self.Y_HISTORY = self.Y_REQUIRES + self.H_REQUIRES + 20
		self.W_HISTORY = 500
		self.H_HISTORY = 120

		self.FILTERS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_UNFILTERED", ())',		# Name of the filter as it appears in dropdown menu.  Needs to be unique for this screen
				"Purpose" : "Clears all currently active filters",		# Description for the sanity of those who modify this file, appears and is used nowhere else
				"Hardcoded" : False,		# If this is True, then only those items in the HardcodeList will pass the check
				"HardcodeList" : [],
				"Value to Check" : 'None',	# Note that eImprovement is the ImprovementInfo object being tested
				"Desired Result" : 'None',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_IMPROVEMENT_REGULAR", ())',
				"Purpose" : "Shows only regular improvements",
				"Hardcoded" : True,
				"HardcodeList" : ['IMPROVEMENT_CAMP', 'IMPROVEMENT_COTTAGE', 'IMPROVEMENT_FARM', 'IMPROVEMENT_FISHING_BOATS', 'IMPROVEMENT_FORT', 'IMPROVEMENT_HAMLET', 'IMPROVEMENT_LUMBERMILL', 'IMPROVEMENT_MINE', 'IMPROVEMENT_PASTURE', 'IMPROVEMENT_PLANTATION', 'IMPROVEMENT_QUARRY', 'IMPROVEMENT_TOWN', 'IMPROVEMENT_VILLAGE', 'IMPROVEMENT_WATERMILL', 'IMPROVEMENT_WINDMILL', 'IMPROVEMENT_WORKSHOP', 'IMPROVEMENT_YARANGA'],
				"Value to Check" : 'None',
				"Desired Result" : 'None',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_IMPROVEMENT_UNIQUE", ())',
				"Purpose" : "Clears all currently active filters",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eImprovement.isUnique()',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_IMPROVEMENT_LAIRS", ())',
				"Purpose" : "Clears all currently active filters",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eImprovement.getSpawnUnitType() > -1 or eImprovement.getSpawnGroupType() > -1 or eImprovement.getImmediateSpawnUnitType() > -1 or eImprovement.getImmediateSpawnGroupType() > -1',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_IMPROVEMENT_CULTURE", ())',
				"Purpose" : "Clears all currently active filters",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eImprovement.getCultureCenterBonus() > 0',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_IMPROVEMENT_SPECIFIC", ())',
				"Purpose" : "Clears all currently active filters",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eImprovement.getPrereqCivilization() > -1',
				"Desired Result" : 'True',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_IMPROVEMENT_CONVERSION", ())',
				"Purpose" : "Clears all currently active filters",
				"Hardcoded" : False,
				"HardcodeList" : [],
				"Value to Check" : 'eImprovement.getBonusConvert() != -1',
				"Desired Result" : 'True',
			},
			]

		# List the filters which you want to be available initially, or self.FILTERS to have all of them available from the start
		self.ALLOWED_FILTERS = self.FILTERS
		self.CURRENT_FILTER = self.FILTERS[0]

		self.SORTS =	[
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_ALPHABETICAL", ())',
				"Purpose" : "Default Sorting Method",
				"Value to Sort" : 'eImprovement.getDescription()',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_FOOD", ())',
				"Purpose" : "Enhancement Sorting FTW",
				"Value to Sort" : '-eImprovement.getYieldChange(YieldTypes.YIELD_FOOD)',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_PRODUCTION_BONUS", ())',
				"Purpose" : "Enhancement Sorting FTW",
				"Value to Sort" : '-eImprovement.getYieldChange(YieldTypes.YIELD_PRODUCTION)',
			},
			{
				"name" : 'localText.getText("TXT_KEY_PEDIA_FILTER_COMMERCE", ())',
				"Purpose" : "Enhancement Sorting FTW",
				"Value to Sort" : '-eImprovement.getYieldChange(YieldTypes.YIELD_COMMERCE)',
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
	def interfaceScreen(self, iImprovement):

		self.iImprovement = iImprovement

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
		sImpDesc = gc.getImprovementInfo(self.iImprovement).getDescription()
		sImpDescCaps = CvUtil.repairedUpper(sImpDesc)
		szHeader = u"<font=4b>" + sImpDescCaps + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "Background", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.X_SCREEN, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Title (upper-right corner, above the list)
		szHeader = u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()).upper() + u"</font>"
		szHeaderId = self.top.getNextWidgetName()
		screen.setLabel(szHeaderId, "", szHeader, CvUtil.FONT_CENTER_JUSTIFY, self.top.W_SCREEN -self.top.W_LINKS/2, self.top.Y_TITLE, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT, -1)

		# Top
		link = CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT
		screen.setText(self.top.getNextWidgetName(), "Background", self.top.MENU_TEXT, CvUtil.FONT_LEFT_JUSTIFY, self.top.X_MENU, self.top.Y_MENU, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_MAIN, link, -1)

		if self.top.iLastScreen	!= CvScreenEnums.PEDIA_IMPROVEMENT or bNotActive:
			self.placeLinks(true)
			self.top.iLastScreen = CvScreenEnums.PEDIA_IMPROVEMENT
		else:
			self.placeLinks(false)

		szCostText = ""
		iBuild = -1
		iCost = 0
		iInst = 0
		for iBuildInfo in xrange(gc.getNumBuildInfos()):
			if gc.getImprovementInfo(self.iImprovement).getImprovementClass() == gc.getBuildInfo(iBuildInfo).getImprovementClass():
				iCost		= gc.getBuildInfo(iBuildInfo).getTime()
				if iCost == 0: continue
				iBuild		= iBuildInfo
				szImpInfo	= gc.getImprovementInfo(self.iImprovement).getType()[12:]
				szBuildInfo	= gc.getBuildInfo(iBuildInfo).getType()[6:]
				iInst += 1
				if szImpInfo == szBuildInfo:
					iInst = 1
					break
		if iInst != 1:
			iCost = 0
		if iCost > 0:
			szCostText = localText.getText("TXT_KEY_PEDIA_COST", ( iCost, ) ).upper() + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())

		# Icon
		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False,
			self.X_UPPER_PANE, self.Y_UPPER_PANE, self.W_UPPER_PANE, self.H_UPPER_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", false, false,
			self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getImprovementInfo(self.iImprovement).getButton(),
			self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		if iCost > 0:
			screen.setLabel(self.top.getNextWidgetName(), "Background", u"<font=4>" + szCostText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_COST, self.Y_COST, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			Y_DISCOUNT = self.Y_COST
			for iTech in xrange(gc.getNumTechInfos()):
				iDiscount = gc.getBuildInfo(iBuild).getTechDiscount(iTech)
				if iDiscount > 0:
					Y_DISCOUNT += 30
					szButton = gc.getTechInfo(iTech).getButton()
					szDicountText = "DISCOUNT: %d" % (iDiscount) + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar())
					screen.setLabel(self.top.getNextWidgetName(), "Background", u"<font=4>" + szDicountText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_COST, Y_DISCOUNT, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					screen.addDDSGFC(self.top.getNextWidgetName(), szButton, self.X_COST + 190, Y_DISCOUNT + 5, 22, 22, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, i, -1 )

		# Bonus animation
		screen.addImprovementGraphicGFC(self.top.getNextWidgetName(), self.iImprovement, self.X_IMPROVEMENT_ANIMATION, self.Y_IMPROVEMENT_ANIMATION, self.W_IMPROVEMENT_ANIMATION, self.H_IMPROVEMENT_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_IMPROVEMENT_ANIMATION, self.Z_ROTATION_IMPROVEMENT_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeRequires()
		self.placeImprovements()
		self.placeBonusYield()
		self.placeHistory()

	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		self.Y_REQUIRES = self.Y_UPPER_PANE + self.H_UPPER_PANE
		self.H_REQUIRES = self.top.H_BLUE50_PANEL
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", false, true,
				 self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )

		screen.attachLabel(panelName, "", "  ")

		iTech = -1
		iInst = 0
		for iBuildInfo in xrange(gc.getNumBuildInfos()):
			if gc.getImprovementInfo(self.iImprovement).getImprovementClass() == gc.getBuildInfo(iBuildInfo).getImprovementClass():
				iTech = gc.getBuildInfo(iBuildInfo).getTechPrereq()
				szImpInfo	= gc.getImprovementInfo(self.iImprovement).getType()[12:]
				szBuildInfo	= gc.getBuildInfo(iBuildInfo).getType()[6:]
				iInst += 1
				if szImpInfo == szBuildInfo:
					iInst = 1
					break

		if iInst != 1:
			iTech = -1
		if iTech > -1:
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )

	def placeImprovements(self):
		screen = self.top.getScreen()

		panelName = self.top.getNextWidgetName()
		self.Y_IMPROVEMENTS_PANE = self.Y_REQUIRES + self.H_REQUIRES
		self.H_IMPROVEMENTS_PANE = self.top.H_SCREEN - self.top.H_BOT_BAR - self.top.EXT_SPACING - self.Y_IMPROVEMENTS_PANE
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), "", true, true,
				 self.X_IMPROVEMENTS_PANE, self.Y_IMPROVEMENTS_PANE, self.W_IMPROVEMENTS_PANE, self.H_IMPROVEMENTS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		info = gc.getImprovementInfo(self.iImprovement)

		szYield = u""

#FfH: Added by Kael 09/27/2007
		szYield += CyGameTextMgr().getImprovementHelp(self.iImprovement, True) + u"\n"
#FfH: End Add

		for k in range(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = gc.getImprovementInfo(self.iImprovement).getYieldChange(k)
			if (iYieldChange != 0):
				if (iYieldChange > 0):
					sign = "+"
				else:
					sign = ""

				szYield += (u"%s: %s%i%c\n" % (gc.getYieldInfo(k).getDescription(), sign, iYieldChange, gc.getYieldInfo(k).getChar()))

		for k in range(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = gc.getImprovementInfo(self.iImprovement).getIrrigatedYieldChange(k)
			if (iYieldChange != 0):
				szYield += localText.getText("TXT_KEY_PEDIA_IRRIGATED_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar())) + u"\n"

		for k in range(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = gc.getImprovementInfo(self.iImprovement).getHillsYieldChange(k)
			if (iYieldChange != 0):
				szYield += localText.getText("TXT_KEY_PEDIA_HILLS_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar())) + u"\n"

		for k in range(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = gc.getImprovementInfo(self.iImprovement).getRiverSideYieldChange(k)
			if (iYieldChange != 0):
				szYield += localText.getText("TXT_KEY_PEDIA_RIVER_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar())) + u"\n"

		for iTech in range(gc.getNumTechInfos()):
			for k in range(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = gc.getImprovementInfo(self.iImprovement).getTechYieldChanges(iTech, k)
				if (iYieldChange != 0):
					szYield += localText.getText("TXT_KEY_PEDIA_TECH_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar(), gc.getTechInfo(iTech).getTextKey())) + u"\n"

		for iCivic in range(gc.getNumCivicInfos()):
			for k in range(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = gc.getCivicInfo(iCivic).getImprovementYieldChanges(self.iImprovement, k)
				if (iYieldChange != 0):
					szYield += localText.getText("TXT_KEY_PEDIA_TECH_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar(), gc.getCivicInfo(iCivic).getTextKey())) + u"\n"

		for iRoute in range(gc.getNumRouteInfos()):
			for k in range(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = gc.getImprovementInfo(self.iImprovement).getRouteYieldChanges(iRoute, k)
				if (iYieldChange != 0):
					szYield += localText.getText("TXT_KEY_PEDIA_ROUTE_YIELD", (gc.getYieldInfo(k).getTextKey(), iYieldChange, gc.getYieldInfo(k).getChar(), gc.getRouteInfo(iRoute).getTextKey())) + u"\n"

		listName = self.top.getNextWidgetName()

		screen.addMultilineText(listName, szYield, self.X_IMPROVEMENTS_PANE+5, self.Y_IMPROVEMENTS_PANE+10, self.W_IMPROVEMENTS_PANE-10, self.H_IMPROVEMENTS_PANE-15, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeBonusYield(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		self.Y_BONUS_YIELDS_PANE = self.Y_REQUIRES
		self.H_BONUS_YIELDS_PANE = self.top.H_SCREEN - self.top.H_BOT_BAR - self.top.EXT_SPACING - self.Y_BONUS_YIELDS_PANE
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_BONUS_YIELDS", ()), "", True, True,
				 self.X_BONUS_YIELDS_PANE, self.Y_BONUS_YIELDS_PANE, self.W_BONUS_YIELDS_PANE, self.H_BONUS_YIELDS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		info = gc.getImprovementInfo(self.iImprovement)

		for j in range(gc.getNumBonusInfos()):
			bFirst = True
			szYield = u""
			bEffect = False
			for k in range(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = info.getImprovementBonusYield(j, k)
				if (iYieldChange != 0):
					bEffect = True
					if (bFirst):
						bFirst = False
					else:
						szYield += u", "

					if (iYieldChange > 0):
						sign = u"+"
					else:
						sign = u""

					szYield += (u"%s%i%c" % (sign, iYieldChange, gc.getYieldInfo(k).getChar()))
			if (bEffect):
				childPanelName = self.top.getNextWidgetName()
				screen.attachPanel(panelName, childPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)

				screen.attachLabel(childPanelName, "", "  ")
				screen.attachImageButton( childPanelName, "", gc.getBonusInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, j, 1, False )
				screen.attachLabel(childPanelName, "", u"<font=4>" + szYield + u"</font>")



	def placeHistory(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		self.X_HISTORY = self.X_IMPROVEMENT_ANIMATION + self.W_IMPROVEMENT_ANIMATION + self.top.INT_SPACING
		self.Y_HISTORY = self.top.H_TOP_BAR + self.top.INT_SPACING
		self.W_HISTORY = self.top.X_LINKS - self.X_HISTORY - self.top.EXT_SPACING
		self.H_HISTORY = self.top.H_SCREEN - self.top.H_BOT_BAR - self.top.EXT_SPACING - self.Y_HISTORY

		screen.addPanel( panelName, localText.getText("TXT_KEY_CIVILOPEDIA_HISTORY", ()), "", true, false,
				 self.X_HISTORY, self.Y_HISTORY, self.W_HISTORY, self.H_HISTORY, PanelStyles.PANEL_STYLE_BLUE50 )
		if len(gc.getImprovementInfo(self.iImprovement).getCivilopedia()) > 0:
			listName = self.top.getNextWidgetName()
			szSpecialText = gc.getImprovementInfo(self.iImprovement).getCivilopedia()
			screen.addMultilineText(listName, szSpecialText, self.X_HISTORY+5, self.Y_HISTORY+25, self.W_HISTORY-10, self.H_HISTORY-30, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def placeLinks(self, bRedraw):
		screen = self.top.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)

		listSorted = self.getSortedList()

		i = 0
		iSelected = 0
		for iI in range(len(listSorted)):
			iImprovement = listSorted[iI][2]
			szName = listSorted[iI][3]
			if bRedraw:
				screen.appendListBoxString(self.top.LIST_ID, szName, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, iImprovement, -1, CvUtil.FONT_LEFT_JUSTIFY)
			if iImprovement == self.iImprovement:
				iSelected = i
			i += 1

		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)

	def getImprovementSortedList(self):
		listImprovements = []
		iCount = 0
		for iImprovement in range(gc.getNumImprovementInfos()):
			if (not gc.getImprovementInfo(iImprovement).isGraphicalOnly()):
				listImprovements.append(iImprovement)
				iCount += 1

		listSorted = [(0,0)] * iCount
		iI = 0
		for iImprovement in listImprovements:
			listSorted[iI] = (gc.getImprovementInfo(iImprovement).getDescription(), iImprovement)
			iI += 1
		listSorted.sort()
		return listSorted

	def getSortedList(self):
		listImprovements = []
		iCount = 0
		for iImprovement in range(gc.getNumImprovementInfos()):
			eImprovement = gc.getImprovementInfo(iImprovement)
			if not eImprovement.isGraphicalOnly():
				if self.CURRENT_FILTER["Hardcoded"]:
					for improvement in self.CURRENT_FILTER["HardcodeList"]:
						if iImprovement == gc.getInfoTypeForString(improvement):
							listImprovements.append(iImprovement)
							iCount += 1
				elif eval(self.CURRENT_FILTER["Value to Check"]) == eval(self.CURRENT_FILTER["Desired Result"]):
					listImprovements.append(iImprovement)
					iCount += 1

		listSorted = [(0,0,0,0,0,0)] * iCount
		iI = 0
		for iImprovement in listImprovements:
			eImprovement = gc.getImprovementInfo(iImprovement)
			sort1 = 0
			sort2 = 0
			if not self.CURRENT_SORT["Value to Sort"] == None:
				sort1 = eval(self.CURRENT_SORT["Value to Sort"])
				sort1 = CvUtil.removeAccent(self,sort1) # alphabetical sorting in the Pedia for languages using accents/diacritics
				if not self.SUB_SORT["Value to Sort"] == None:
					sort2 = eval(self.SUB_SORT["Value to Sort"])
			listSorted[iI] = (sort1, sort2, iImprovement, eImprovement.getDescription(), eImprovement.getButton(), 1)
			iI += 1
		listSorted.sort()

		return listSorted

	def applyFilterSort(self, filter, sort):
		if not self.CURRENT_SORT == sort:
			self.SUB_SORT = self.CURRENT_SORT
			self.CURRENT_SORT = sort
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT, True)

		if not self.CURRENT_FILTER == filter:
			self.CURRENT_FILTER = filter
			self.top.pediaJump(CvScreenEnums.PEDIA_MAIN, CivilopediaPageTypes.CIVILOPEDIA_PAGE_IMPROVEMENT, True)

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.top.getScreen()
			iFilterIndex = screen.getSelectedPullDownID(self.top.FILTER_DROPDOWN_ID)
			iSortIndex = screen.getSelectedPullDownID(self.top.SORT_DROPDOWN_ID)
			self.applyFilterSort(self.ALLOWED_FILTERS[iFilterIndex], self.ALLOWED_SORTS[iSortIndex])
			return 1

		return 0