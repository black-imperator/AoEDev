## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

## Victory Screen shell used to build Military Advisor multi-tab display

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import PyHelpers
import time
import re

import IconGrid_BUG
import BugUtil
import UnitGrouper

# BUG - Options - start
import BugScreensOptions
BugScreens = BugScreensOptions.getOptions()
# BUG - Options - end

PyPlayer = PyHelpers.PyPlayer

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

UNIT_LOCATION_SCREEN = 0
SITUATION_REPORT_SCREEN = 1
#PLACE_HOLDER = 2

def BUGPrint (stuff):
#	stuff = "BUG_MAdv: " + stuff
#	print stuff
	return

class CvMilitaryAdvisor:
	"Shows the BUG Version of the Military Advisor"

	def __init__(self, screenId):
		self.screenId = screenId
		self.SCREEN_NAME = "MilitaryScreen-BUG"

		self.UNIT_LOC_TAB_ID = "MilitaryUnitLocTabWidget-BUG"
		self.SIT_REP_TAB_ID = "MilitarySitRepTabWidget-BUG"
#		self.PLACE_HOLDER_TAB = "placeholder"

		self.X_MAP = 20
		self.Y_MAP = 190
		self.W_MAP = 580
		self.H_MAP_MAX = 500
		self.MAP_MARGIN = 20

		self.X_TEXT = 625
		self.Y_TEXT = 190
		self.W_TEXT = 380
		self.H_TEXT = 500

		self.X_LEADERS = 20
		self.Y_LEADERS = 80
		self.W_LEADERS = 985
		self.H_LEADERS = 90
		self.LEADER_BUTTON_SIZE = 64
		self.LEADER_MARGIN = 12

		self.LEADER_COLUMNS = int(self.W_LEADERS / (self.LEADER_BUTTON_SIZE + self.LEADER_MARGIN))

		self.selectedLeaderList = []
		self.selectedGroupList = []
		self.selectedUnitList = []
		self.bUnitDetails = False
		self.iShiftKeyDown = 0

		self.X_GREAT_GENERAL_BAR = 0
		self.Y_GREAT_GENERAL_BAR = 0
		self.W_GREAT_GENERAL_BAR = 0
		self.H_GREAT_GENERAL_BAR = 0

		self.UNIT_BUTTON_ID = "MilitaryAdvisorUnitButton-BUG"
		self.UNIT_LIST_ID = "MilitaryAdvisorUnitList-BUG"
		self.UNIT_BUTTON_LABEL_ID = "MilitaryAdvisorUnitButtonLabel-BUG"
		self.LEADER_BUTTON_ID = "MilitaryAdvisorLeaderButton-BUG"
		self.MINIMAP_PANEL = "MilitaryMiniMapPanel-BUG"

#		self.SitRep_Y = 55
#		self.SitRep_Y_Offset = 10
#		self.SitRep_X1 = 90
#		self.SitRep_X2 = self.SitRep_X1 + 100
#		self.SitRep_X3 = self.SitRep_X2 + 100
#		self.SitRep_X4 = self.SitRep_X3 + 100
#		self.SitRep_X5 = self.SitRep_X4 + 100
#		self.SitRep_X6 = self.SitRep_X5 + 100


		self.iPlayerPower = 0
		self.iDemographicsMission = -1

		# dict for upgrade units
		self.FutureUnitsByUnitClass = {}







#		self.DEBUG_DROPDOWN_ID =  "MilitaryScreenDropdownWidget"
#		self.INTERFACE_ART_INFO = "TECH_BG"
#		self.EXIT_AREA = "EXIT"
		self.EXIT_ID = "MilitaryScreenExit-BUG"
		self.BACKGROUND_ID = "MilitaryScreenBackground-BUG"
		self.HEADER_ID = "MilitaryScreenHeader-BUG"
		self.WIDGET_ID = "MilitaryScreenWidget-BUG"
#		self.VC_TAB_ID = "VictoryTabWidget"
#		self.SETTINGS_TAB_ID = "SettingsTabWidget"
#		self.SPACESHIP_SCREEN_BUTTON = 1234

		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
#		self.DZ = -0.2

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 12

		self.X_EXIT = 994
		self.Y_EXIT = 726

#		self.X_AREA = 10
#		self.Y_AREA = 60
#		self.W_AREA = 1010
#		self.H_AREA = 650

#		self.TABLE_WIDTH_0 = 350
#		self.TABLE_WIDTH_1 = 80
#		self.TABLE_WIDTH_2 = 180
#		self.TABLE_WIDTH_3 = 100
#		self.TABLE_WIDTH_4 = 180
#		self.TABLE_WIDTH_5 = 100

#		self.TABLE2_WIDTH_0 = 740
#		self.TABLE2_WIDTH_1 = 265

		self.X_LINK = 100
		self.DX_LINK = 220
		self.Y_LINK = 726
		self.MARGIN = 20

		self.SETTINGS_PANEL_X1 = 50
		self.SETTINGS_PANEL_X2 = 355
		self.SETTINGS_PANEL_X3 = 660
		self.SETTINGS_PANEL_Y = 150
		self.SETTINGS_PANEL_WIDTH = 300
		self.SETTINGS_PANEL_HEIGHT = 500

		self.nWidgetCount = 0
		self.iActivePlayer = -1
#		self.bVoteTab = False

		self.minimapInitialized = False
		self.iScreen = UNIT_LOCATION_SCREEN

		# icongrid constants
		self.IconGridActive = False

		self.SHOW_LEADER_NAMES = False
		self.SHOW_ROW_BORDERS = True
		self.MIN_TOP_BOTTOM_SPACE = 30
		self.MIN_LEFT_RIGHT_SPACE = 10
		self.GROUP_BORDER = 8
		self.GROUP_LABEL_OFFSET = "   "
		self.MIN_COLUMN_SPACE = 5
		self.MIN_ROW_SPACE = 1

		# sit rep constants
		self.SITREP_PANEL_SPACE = 50
		self.TITLE_HEIGHT = 0
		self.TABLE_CONTROL_HEIGHT = 0
#		self.RESOURCE_ICON_SIZE = 34
		self.SCROLL_TABLE_UP = 1
		self.SCROLL_TABLE_DOWN = 2

		self.bWHEOOH = False
		self.bCurrentWar = False


	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, self.screenId)

	def hideScreen(self):
		self.IconGridActive = False
		screen = self.getScreen()
		screen.hideScreen()

	def interfaceScreen(self):

		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return

		# over-ride screen width, height
		self.W_SCREEN = screen.getXResolution() - 40
		self.X_EXIT = self.W_SCREEN - 30
		#self.Y_EXIT = 726
		#self.H_SCREEN = screen.getYResolution()

		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.iActivePlayer = CyGame().getActivePlayer()
		if self.iScreen == -1:
			self.iScreen = UNIT_LOCATION_SCREEN

		# Set the background widget and exit button
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MILITARY").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground( False )
		#screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setDimensions(20, screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setText(self.EXIT_ID, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		# Header...
		screen.setLabel(self.HEADER_ID, "Background", u"<font=4b>" + localText.getText("TXT_KEY_MILITARY_ADVISOR_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.unitLocationInitDone = False
		if self.iScreen == UNIT_LOCATION_SCREEN:
			self.showUnitLocation()
		elif self.iScreen == SITUATION_REPORT_SCREEN:
			self.showSituationReport()
#		elif self.iScreen == PLACE_HOLDER:
#			self.showGameSettingsScreen()

	def drawTabs(self):

		screen = self.getScreen()

		xLink = self.X_LINK
		if (self.iScreen != UNIT_LOCATION_SCREEN):
			screen.setText(self.UNIT_LOC_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_MILITARY_UNIT_LOCATION", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setText(self.UNIT_LOC_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_MILITARY_UNIT_LOCATION", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += self.DX_LINK

		if (self.iScreen != SITUATION_REPORT_SCREEN):
			screen.setText(self.SIT_REP_TAB_ID, "", u"<font=4>" + localText.getText("TXT_KEY_MILITARY_SITUATION_REPORT", ()).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setText(self.SIT_REP_TAB_ID, "", u"<font=4>" + localText.getColorText("TXT_KEY_MILITARY_SITUATION_REPORT", (), gc.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", CvUtil.FONT_CENTER_JUSTIFY, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += self.DX_LINK

# dev using icongrid
	def showSituationReport(self):

		self.deleteAllWidgets()
		screen = self.getScreen()

		#self.PrintUpgrades()
		# build the future upgrade path array / list / dict - whatever!
		if len(self.FutureUnitsByUnitClass) == 0:
			self.buildFutureUnitsByUnitClass()


		# get Player arrays
		iVassals = [[]] * gc.getMAX_PLAYERS()
		iDefPacts = [[]] * gc.getMAX_PLAYERS()
		bVassals = False
		bDefPacts = False
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iLoopPlayer)

			if (pPlayer.isAlive()
			and (gc.getTeam(pPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and iLoopPlayer != self.iActivePlayer
			and not pPlayer.isBarbarian()
			and not pPlayer.isMinorCiv()):
				iVassals[iLoopPlayer] = self.getVassals(iLoopPlayer)
				iDefPacts[iLoopPlayer] = self.getDefPacts(iLoopPlayer)

				if len(iVassals[iLoopPlayer]) > 0:
					bVassals = True

				if len(iDefPacts[iLoopPlayer]) > 0:
					bDefPacts = True

		self.initGrid(screen, bVassals, bDefPacts)
		self.initPower()

		activePlayer = gc.getPlayer(self.iActivePlayer)


		# Assemble the panel
		iPANEL_X = 5
		iPANEL_Y = 60
		iPANEL_WIDTH = self.W_SCREEN - 20
		iPANEL_HEIGHT = self.H_SCREEN - 120

		self.tradePanel = self.getNextWidgetName()
		screen.addPanel(self.tradePanel, "", "", True, True, iPANEL_X, iPANEL_Y, iPANEL_WIDTH, iPANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN )

		self.SitRepGrid.createGrid()
		self.SitRepGrid.clearData()

		iRow = 0
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iLoopPlayer)

			if (pPlayer.isAlive()
			and (gc.getTeam(pPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and iLoopPlayer != self.iActivePlayer
			and not pPlayer.isBarbarian()
			and not pPlayer.isMinorCiv()):


#				szPlayerName = pPlayer.getName() + "/" + pPlayer.getCivilizationShortDescription(0)
#				BUGPrint("Grid_ThreatIndex - Start %i %s" % (iLoopPlayer, szPlayerName))
#				BUGPrint("Grid_ThreatIndex - Start %i" % (iLoopPlayer))

				self.SitRepGrid.appendRow(pPlayer.getName(), "", 3)

				# add leaderhead icon
				self.SitRepGrid.addIcon(iRow, self.Col_Leader,
										gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton(), 64,
										WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer)

				# add worst enemy
				self.Grid_WorstEnemy(iRow, iLoopPlayer)

				# add strategic differences
				self.Grid_Strategic_Resources(iRow, iLoopPlayer)

				# add current war opponents
				self.bCurrentWar = False
				iActiveWars = self.GetActiveWars(iRow, iLoopPlayer)
				if len(iActiveWars) > 0:
					self.bCurrentWar = True

				for iLoopPlayer2 in iActiveWars:
					self.SitRepGrid.addIcon(iRow, self.Col_Curr_Wars,
											gc.getLeaderHeadInfo (gc.getPlayer(iLoopPlayer2).getLeaderType()).getButton(), 32,
											WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer2)

				# show vassals
				if bVassals:
					for iLoopPlayer2 in iVassals[iLoopPlayer]:
						self.SitRepGrid.addIcon(iRow, self.Col_Vassals,
												gc.getLeaderHeadInfo (gc.getPlayer(iLoopPlayer2).getLeaderType()).getButton(), 32,
												WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer2)

				# show defensive packs
				if bDefPacts:
					for iLoopPlayer2 in iDefPacts[iLoopPlayer]:
						self.SitRepGrid.addIcon(iRow, self.Col_DefPacts,
												gc.getLeaderHeadInfo (gc.getPlayer(iLoopPlayer2).getLeaderType()).getButton(), 32,
												WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer2)

				# show players that the current player will declare on
				self.bWHEOOH = False
				iActiveWars = self.GetDeclareWar(iRow, iLoopPlayer)
				for iLoopPlayer2 in iActiveWars:
					self.SitRepGrid.addIcon(iRow, self.Col_WillDeclareOn,
											gc.getLeaderHeadInfo (gc.getPlayer(iLoopPlayer2).getLeaderType()).getButton(), 32,
											WidgetTypes.WIDGET_LEADERHEAD, iLoopPlayer2)
				# WHEOOH
				if self.bWHEOOH:
					sWHEOOH = u" %c" % CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR)
				else:
					sWHEOOH = ""

				self.SitRepGrid.addText(iRow, self.Col_WHEOOH, sWHEOOH, 3)

				# add the threat index
				self.Grid_ThreatIndex(iRow, iLoopPlayer)

				iRow += 1

		self.SitRepGrid.refresh()

		self.drawTabs()

		return

	def initGrid(self, screen, bVassals, bDefPacts):

		self.Col_Leader = 0
		self.Col_WHEOOH = 1
		self.Col_WEnemy = 2
		self.Col_Threat = 3
		self.Col_StratResPos = 4
		self.Col_StratResNeg = 5
		self.Col_WillDeclareOn = 7
		self.Col_Curr_Wars = 6
		self.Col_Vassals = 8
		self.Col_DefPacts = 9

		if (not bVassals and not bDefPacts):
			columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_TEXT_COLUMN,
						IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_STACKEDBAR_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN)
		if (bVassals and bDefPacts):
			columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_TEXT_COLUMN,
						IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_STACKEDBAR_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN)
		else:
			columns = ( IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_TEXT_COLUMN,
						IconGrid_BUG.GRID_ICON_COLUMN,
						IconGrid_BUG.GRID_STACKEDBAR_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN,
						IconGrid_BUG.GRID_MULTI_LIST_COLUMN)

		gridX = self.MIN_LEFT_RIGHT_SPACE + 10
		gridY = self.MIN_TOP_BOTTOM_SPACE + self.SITREP_PANEL_SPACE + self.TABLE_CONTROL_HEIGHT + self.TITLE_HEIGHT + 10
		gridWidth = self.W_SCREEN - 10 # - self.MIN_LEFT_RIGHT_SPACE * 2 - 20
		gridHeight = self.H_SCREEN - self.MIN_TOP_BOTTOM_SPACE * 2 - self.SITREP_PANEL_SPACE - self.TITLE_HEIGHT - 20

#		self.resIconGridName = self.getNextWidgetName()
#class IconGrid:  def __init__(self, sWidgetId, screen, iX, iY, iWidth, iHeight, columns, bUseSmallIcons, bShowRowHeader, bShowRowBorder):


		self.SitRepGrid = IconGrid_BUG.IconGrid_BUG(self.getNextWidgetName(), screen, gridX, gridY, gridWidth, gridHeight,
													columns, True, self.SHOW_LEADER_NAMES, self.SHOW_ROW_BORDERS)

		# set constants
		self.SitRepGrid.setGroupBorder(self.GROUP_BORDER)
		self.SitRepGrid.setGroupLabelOffset(self.GROUP_LABEL_OFFSET)
		self.SitRepGrid.setMinColumnSpace(self.MIN_COLUMN_SPACE)
		self.SitRepGrid.setMinRowSpace(self.MIN_ROW_SPACE)

		# set headings
		self.SitRepGrid.setHeader(self.Col_Leader, "", 3)
		self.SitRepGrid.setHeader(self.Col_WHEOOH, "", 3)
		self.SitRepGrid.setHeader(self.Col_WEnemy, localText.getText("TXT_KEY_MILITARY_SITREP_ENEMY", ()), 3)
		self.SitRepGrid.setHeader(self.Col_Threat, localText.getText("TXT_KEY_MILITARY_SITREP_THREAT_INDEX", ()), 3)
		self.SitRepGrid.setHeader(self.Col_Curr_Wars, localText.getText("TXT_KEY_MILITARY_SITREP_WARS_ACTIVE", ()), 3)
		self.SitRepGrid.setHeader(self.Col_StratResPos, localText.getText("TXT_KEY_MILITARY_SITREP_STRAT_RES_OURS", ()), 3)
		self.SitRepGrid.setHeader(self.Col_StratResNeg, localText.getText("TXT_KEY_MILITARY_SITREP_STRAT_RES_THEIRS", ()), 3)
		self.SitRepGrid.setHeader(self.Col_WillDeclareOn, localText.getText("TXT_KEY_MILITARY_SITREP_WARS_OPTIONAL", ()), 3)

		if bVassals:
			self.SitRepGrid.setHeader(self.Col_Vassals, localText.getText("TXT_KEY_MILITARY_SITREP_VASSALS", ()), 3)

		if bDefPacts:
			self.SitRepGrid.setHeader(self.Col_DefPacts, localText.getText("TXT_KEY_MILITARY_SITREP_DEFPACTS", ()), 3)

		self.SitRepGrid.createColumnGroup("", 1)
		self.SitRepGrid.createColumnGroup("", 1)
		self.SitRepGrid.createColumnGroup(localText.getText("TXT_KEY_MILITARY_SITREP_WORST", ()), 1)
		self.SitRepGrid.createColumnGroup("", 1)
		self.SitRepGrid.createColumnGroup(localText.getText("TXT_KEY_MILITARY_SITREP_STRATEGIC_RESOURCES", ()), 2)
		self.SitRepGrid.createColumnGroup(localText.getText("TXT_KEY_MILITARY_SITREP_WARS", ()), 2)

		self.SitRepGrid.setTextColWidth(self.Col_WHEOOH, 25)
		self.SitRepGrid.setStackedBarColWidth(self.Col_Threat, 120)

		gridWidth = self.SitRepGrid.getPrefferedWidth()
		gridHeight = self.SitRepGrid.getPrefferedHeight()
		self.SITREP_LEFT_RIGHT_SPACE = (self.W_SCREEN - gridWidth - 20) / 2
		self.SITREP_TOP_BOTTOM_SPACE = (self.H_SCREEN - gridHeight - 20) / 2
		gridX = self.SITREP_LEFT_RIGHT_SPACE + 10
		gridY = self.SITREP_TOP_BOTTOM_SPACE + 10

		self.SitRepGrid.setPosition(gridX, gridY)
		self.SitRepGrid.setSize(gridWidth, gridHeight)

		self.IconGridActive = True


	def initPower(self):
		# active player power
		self.iPlayerPower = gc.getActivePlayer().getPower()

		# see demographics?
		self.iDemographicsMission = -1
		for iMissionLoop in range(gc.getNumEspionageMissionInfos()):
			if (gc.getEspionageMissionInfo(iMissionLoop).isSeeDemographics()):
				self.iDemographicsMission = iMissionLoop
				break

		return

	def Grid_ThreatIndex(self, iRow, iPlayer):

		pPlayer = gc.getPlayer(iPlayer)

#		BUGPrint("Grid_ThreatIndex - Start")

		if gc.getTeam(pPlayer.getTeam()).isAVassal():
			self.SitRepGrid.addStackedBar(iRow, self.Col_Threat, -1, "", localText.getText("TXT_KEY_MILITARY_SITREP_VASSAL", ()), 3)
#			BUGPrint("Grid_ThreatIndex - is vassal")
			return

		# initialize threat index
		iThreat = 0

		# add attitude threat value
		iRel = self.calculateRelations(iPlayer, self.iActivePlayer)
		fRel_Threat = float(38) * float(15 - iRel) / float(30)
		if fRel_Threat < 0:
			fRel_Threat = 0.0
		elif fRel_Threat > 38:
			fRel_Threat = 38.0

#		BUGPrint("Grid_ThreatIndex - relationships")

		# calculate the power threat value
		fPwr_Threat = 0
		iPower = pPlayer.getPower()
		if (iPower > 0): # avoid divide by zero
			fPowerRatio = float(self.iPlayerPower) / float(iPower)
			fPwr_Threat = float(38) * float(1.5 - fPowerRatio)
			if fPwr_Threat < 0:
				fPwr_Threat = 0.0
			elif fPwr_Threat > 38:
				fPwr_Threat = 38.0

		# set power thread to 75% of max if active player cannot see the demographics
		bCannotSeeDemographics = False
		if not gc.getActivePlayer().canDoEspionageMission(self.iDemographicsMission, iPlayer, None, -1):
			bCannotSeeDemographics = True
			fPwr_Threat = 38.0 * 0.75
#			self.SitRepGrid.addStackedBar(iRow, self.Col_Threat, -1, "", "n/a", 3)
#			BUGPrint("Grid_ThreatIndex - not enough spy points")
#			return


#		BUGPrint("Grid_ThreatIndex - power")

		# total threat, pre WHEOOH adjustment
		fThreat = fRel_Threat + fPwr_Threat

		# WHEOOH adjustment
		if (self.bWHEOOH
		and not self.bCurrentWar):
			fThreat = fThreat * 1.3

		# reduce the threat if the current player is in a defensive pact with the active player
		if gc.getTeam(pPlayer.getTeam()).isDefensivePact(gc.getPlayer(self.iActivePlayer).getTeam()):
			fThreat = fThreat * 0.2

		BUGPrint("Grid_ThreatIndex - thread adjustments - thread index %i" % int(fThreat))

		if fThreat < 15:
			sColour = "COLOR_PLAYER_GREEN"
			sThreat = localText.getText("TXT_KEY_MILITARY_THREAT_INDEX_LOW", ())
		elif  fThreat < 35:
			sColour = "COLOR_PLAYER_BLUE"
			sThreat = localText.getText("TXT_KEY_MILITARY_THREAT_INDEX_GUARDED", ())
		elif  fThreat < 55:
			sColour = "COLOR_PLAYER_YELLOW"
			sThreat = localText.getText("TXT_KEY_MILITARY_THREAT_INDEX_ELEVATED", ())
		elif  fThreat < 75:
			sColour = "COLOR_PLAYER_ORANGE"
			sThreat = localText.getText("TXT_KEY_MILITARY_THREAT_INDEX_HIGH", ())
		else:
			sColour = "COLOR_PLAYER_RED"
			sThreat = localText.getText("TXT_KEY_MILITARY_THREAT_INDEX_SEVERE", ())

		if bCannotSeeDemographics:
			sThreat += " (est)"

		self.SitRepGrid.addStackedBar(iRow, self.Col_Threat, fThreat, sColour, sThreat, 3)
#		BUGPrint("Grid_ThreatIndex - bar placed")
		return

	def calculateRelations (self, nPlayer, nTarget):
		if (nPlayer != nTarget
		and gc.getTeam(gc.getPlayer(nPlayer).getTeam()).isHasMet(gc.getPlayer(nTarget).getTeam())):
			nAttitude = 0
			szAttitude = CyGameTextMgr().getAttitudeString(nPlayer, nTarget)
#			print szAttitude
			ltPlusAndMinuses = re.findall ("[-+][0-9]+", szAttitude)
			for i in range (len (ltPlusAndMinuses)):
				nAttitude += int (ltPlusAndMinuses[i])
		else:
			return None
		return nAttitude


	def Grid_WorstEnemy(self, iRow, iLeader):
		szWEnemyName = gc.getPlayer(iLeader).getWorstEnemyName()

		if szWEnemyName == "":
			self.SitRepGrid.addIcon(iRow, self.Col_WEnemy,
									ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), 45,
									WidgetTypes.WIDGET_LEADERHEAD, -1)
		else:
			for iLoopEnemy in range(gc.getMAX_PLAYERS()):
				if gc.getPlayer(iLoopEnemy).getName() == szWEnemyName:
					iWEnemy = iLoopEnemy
					break

			pWEPlayer = gc.getPlayer(iWEnemy)
			if (pWEPlayer.isAlive()
			and (gc.getTeam(pWEPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and not pWEPlayer.isBarbarian()
			and not pWEPlayer.isMinorCiv()):
				self.SitRepGrid.addIcon(iRow, self.Col_WEnemy,
										gc.getLeaderHeadInfo(pWEPlayer.getLeaderType()).getButton(), 32,
										WidgetTypes.WIDGET_LEADERHEAD, iLoopEnemy)
		return

	def GetActiveWars(self, iRow, iLeader):
		iWars = []

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive()
			and (gc.getTeam(pLoopPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and not pLoopPlayer.isBarbarian()
			and not pLoopPlayer.isMinorCiv()):
				if gc.getTeam(gc.getPlayer(iLeader).getTeam()).isAtWar(pLoopPlayer.getTeam()):
					iWars.append(iLoopPlayer)

		return iWars

	def getVassals(self, iPlayer):
		iVassals = []
		pPlayer = gc.getPlayer(iPlayer)

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive()
			and (gc.getTeam(pLoopPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and not pLoopPlayer.isBarbarian()
			and not pLoopPlayer.isMinorCiv()
			and iPlayer != iLoopPlayer):
				if gc.getTeam(pLoopPlayer.getTeam()).isVassal(pPlayer.getTeam()):
					iVassals.append(iLoopPlayer)
		return iVassals

	def getDefPacts(self, iPlayer):
		iDefPacts = []
		pPlayer = gc.getPlayer(iPlayer)

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if (pLoopPlayer.isAlive()
			and (gc.getTeam(pLoopPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			or gc.getGame().isDebugMode())
			and not pLoopPlayer.isBarbarian()
			and not pLoopPlayer.isMinorCiv()
			and iPlayer != iLoopPlayer):
				if gc.getTeam(pLoopPlayer.getTeam()).isDefensivePact(pPlayer.getTeam()):
					iDefPacts.append(iLoopPlayer)
		return iDefPacts



	def PrintUpgrades(self):

		for u in (self.FutureUnitsByUnitClass):
			sDummy = "Unit Upgrade (%s): " % (gc.getUnitInfo(u).getDescription())

			upgrades = self.FutureUnitsByUnitClass[u]
			for k in upgrades:
				sDummy += " %s" % (gc.getUnitInfo(k).getDescription())

			print sDummy
		return

	def Grid_Strategic_Resources(self, iRow, iPlayer):

		pPlayer = gc.getPlayer(iPlayer)
		pActivePlayer = gc.getPlayer(self.iActivePlayer)

		if (not pActivePlayer.canTradeNetworkWith(iPlayer)
		or (not gc.getTeam(pActivePlayer.getTeam()).isTechTrading()
		and not gc.getTeam(pPlayer.getTeam()).isTechTrading())):
			szButton = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
			self.SitRepGrid.addIcon(iRow, self.Col_StratResPos, szButton, 32, WidgetTypes.WIDGET_GENERAL, -1)
			self.SitRepGrid.addIcon(iRow, self.Col_StratResNeg, szButton, 32, WidgetTypes.WIDGET_GENERAL, -1)
			return

		iAIUnits = self.getCanTrainUnits(iPlayer)
		iHumanUnits = self.getCanTrainUnits(self.iActivePlayer)

		# remove units that the human does not know about
		iUnitsToRemove = set()
		for iUnit in iAIUnits:
			iDiscoverTech = gc.getUnitInfo(iUnit).getPrereqAndTech()
			if not (gc.getTeam(pActivePlayer.getTeam()).isHasTech(iDiscoverTech)
			or  pActivePlayer.canResearch(iDiscoverTech, False)):
				iUnitsToRemove.add(iUnit)
		iAIUnits -= iUnitsToRemove

		# determine units that human can build that the AI cannot
		for iUnit in iHumanUnits:
			if self.isUnitUnique(iUnit, iAIUnits):
				szButton = gc.getUnitInfo(iUnit).getButton()
				self.SitRepGrid.addIcon(iRow, self.Col_StratResPos, szButton, 32, WidgetTypes.WIDGET_GENERAL, -1)

		# determine units that AI can build that the human cannot
		for iUnit in iAIUnits:
			if self.isUnitUnique(iUnit, iHumanUnits):
				szButton = gc.getUnitInfo(iUnit).getButton()
				self.SitRepGrid.addIcon(iRow, self.Col_StratResNeg, szButton, 32, WidgetTypes.WIDGET_GENERAL, -1)







#				if (PlayerHasTech != ""):



#				szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)
#						screen.appendMultiListButton( "BottomButtonContainer", szButton, iRow, WidgetTypes.WIDGET_TRAIN, i, -1, False )
#		self.SitRepGrid.addIcon( iRow, self.Col_StratResPos
#								, gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton()
#								, WidgetTypes.WIDGET_LEADERHEAD, iPlayer)


#units.getDiscoveryTech()
#						elif currentPlayer.canResearch(iLoopTech, False):

		# Go through all the techs
#		for i in range(gc.getNumTechInfos()):

#			abChanged.append(0)

#			if ( gc.getTeam(gc.getPlayer(self.iCivSelected).getTeam()).isHasTech(i) ):








#		self.SitRepGrid.addIcon( iRow, self.Col_StratResPos
#								, gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton()
#								, WidgetTypes.WIDGET_LEADERHEAD, iPlayer)

#		self.SitRepGrid.addIcon( iRow, self.Col_StratResNeg
#								, gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getButton()
#								, WidgetTypes.WIDGET_LEADERHEAD, iPlayer)



		return


	def getCanTrainUnits(self, iPlayer):
		pPlayer = gc.getPlayer(iPlayer)
		civInfo = gc.getCivilizationInfo(pPlayer.getCivilizationType())

		iUnits = set()
		for i in range (gc.getNumUnitClassInfos()):
			iUnit = civInfo.getCivilizationUnits(i)
			if gc.getUnitInfo(iUnit).getUnitCombatType() > 0: # ie, not settler, worker, missionary, etc
				(pLoopCity, iter) = pPlayer.firstCity(False)
				while(pLoopCity):
					if pLoopCity.canTrain(iUnit, False, False):
						iUnits.add(iUnit)
						break
					(pLoopCity, iter) = pPlayer.nextCity(iter, False)

		return iUnits

	def buildFutureUnitsByUnitClass(self):
		NUM_UNITS = gc.getNumUnitInfos()

		# Create graph of single-step upgrades (Swordsman to Maceman)
		self.FutureUnitsByUnitClass = {}
		self.UnitsAlreadyMapped = set()
		for iUnitA in xrange(NUM_UNITS):
			infoA = gc.getUnitInfo(iUnitA)
			upgrades = set()
			self.FutureUnitsByUnitClass[iUnitA] = upgrades  # <-- creates a link between these two items
			for iUnitB in xrange(NUM_UNITS):
				infoB = gc.getUnitInfo(iUnitB)
				for iUnitClass in xrange(infoA.getNumUpgradeUnitClass()):
					if infoA.getUpgradeUnitClass(iUnitClass) == infoB.getUnitClassType():
						upgrades.add(iUnitB)   # also adds iUnitB to FutureUnitsByUnitClass array

		# Now add all transitive upgrades (Swordsman to Rifleman)
		for iUnit in self.FutureUnitsByUnitClass.iterkeys():
			self.buildFutureArray_Closure(iUnit)   # just starting the recursive call

	def buildFutureArray_Closure(self, iUnit):
		upgrades = self.FutureUnitsByUnitClass[iUnit]
		if iUnit not in self.UnitsAlreadyMapped:
			nextUpgrades = set()
			for iNextUnit in upgrades:
				nextUpgrades |= self.buildFutureArray_Closure(iNextUnit)  # note recursive call
			upgrades |= nextUpgrades
			self.UnitsAlreadyMapped.add(iUnit)
		return upgrades

	def isUnitUnique(self, iUnit, enemyUnits):
		# check if the unit is in the array of enemyunts
		if (iUnit in enemyUnits):
			return False

		# check if the enemy has any of the upgrades to this unit
		upgrades = self.FutureUnitsByUnitClass[iUnit]
		return len(upgrades & enemyUnits) == 0


























	def GetDeclareWar(self, iRow, iPlayer):
		# this module will check if the iPlayer will declare war
		# on the other leaders.  We cannot check if the iPlayer, the iActivePlayer
		# and the iTargetPlayer don't all know each other.
		# However, the code wouldn't have got this far if the iPlayer didn't know the iActivePlayer
		# so we only need to check if the iPlayer and the iActivePlayer both know the iTargetPlayer.

		# also need to check on vassal state - will do that later

		iLeaderWars = []
		szWarDenial = ""

		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_WAR

		pPlayer = gc.getPlayer(iPlayer)

		szPlayerName = gc.getPlayer(iPlayer).getName() + "/" + gc.getPlayer(iPlayer).getCivilizationShortDescription(0)

		for iTargetPlayer in range(gc.getMAX_PLAYERS()):
			pTargetPlayer = gc.getPlayer(iTargetPlayer)

			if (pTargetPlayer.isAlive()
			and (gc.getTeam(pTargetPlayer.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam())
			and  gc.getTeam(pTargetPlayer.getTeam()).isHasMet(gc.getPlayer(iPlayer).getTeam())
			or   gc.getGame().isDebugMode())
			and not iTargetPlayer == self.iActivePlayer
			and not iTargetPlayer == iPlayer
			and not gc.getTeam(pPlayer.getTeam()).isAtWar(pTargetPlayer.getTeam())
			and not pTargetPlayer.isBarbarian()
			and not pTargetPlayer.isMinorCiv()):

				szPlayerName = gc.getPlayer(iTargetPlayer).getName() + "/" + gc.getPlayer(iTargetPlayer).getCivilizationShortDescription(0)

				tradeData.iData = iTargetPlayer
				if (pPlayer.canTradeItem(self.iActivePlayer, tradeData, False)):
					WarDenial = pPlayer.getTradeDenial(self.iActivePlayer, tradeData)
					if WarDenial == DenialTypes.NO_DENIAL:
						iLeaderWars.append(iTargetPlayer)
					elif szWarDenial == "":
						szWarDenial = gc.getDenialInfo(WarDenial).getDescription()

					if WarDenial == DenialTypes.DENIAL_TOO_MANY_WARS:
						self.bWHEOOH = True

		return iLeaderWars

	def getWarDeclarationTrades(self, activePlayer, activeTeam):
		iActivePlayerID = activePlayer.getID()
		iActiveTeamID = activeTeam.getID()
		tradeData = TradeData()
		tradeData.ItemType = TradeableItems.TRADE_WAR
		currentTrades = set()

		for iLoopPlayerID in range(gc.getMAX_PLAYERS()):
			loopPlayer = gc.getPlayer(iLoopPlayerID)
			iLoopTeamID = loopPlayer.getTeam()
			loopTeam = gc.getTeam(iLoopTeamID)
			if (loopPlayer.isBarbarian() or loopPlayer.isMinorCiv() or not loopPlayer.isAlive()):
				continue
			if (iLoopPlayerID != iActivePlayerID and loopTeam.isHasMet(iActiveTeamID)):
				if (loopPlayer.canTradeItem(iActivePlayerID, tradeData, False)):
					if (loopPlayer.getTradeDenial(iActivePlayerID, tradeData) == DenialTypes.NO_DENIAL): # will trade
						currentTrades.add(iLoopPlayerID)
		return currentTrades




























	def showUnitLocation(self):

		self.deleteAllWidgets()
		screen = self.getScreen()

		activePlayer = PyHelpers.PyPlayer(self.iActivePlayer)
		iActiveTeam = gc.getPlayer(self.iActivePlayer).getTeam()

		if not self.unitLocationInitDone:
			self.unitsList = [(0, 0, [], 0)] * gc.getNumUnitInfos() * 2
			self.selectedUnitList = []
			self.selectedLeaderList = [self.iActivePlayer]
			self.UL_initMinimap(screen)
			self.unitLocationInitDone = True
			self.UL_refresh(True, True)
		else:
			self.UL_refresh(False, True)

		self.drawTabs()




	def UL_initMinimap(self, screen):
		# Minimap initialization
		iMap_W = CyMap().getGridWidth()
		iMap_H = CyMap().getGridHeight()
		self.H_MAP = (self.W_MAP * iMap_H) / iMap_W
		if (self.H_MAP > self.H_MAP_MAX):
			self.W_MAP = (self.H_MAP_MAX * iMap_W) / iMap_H
			self.H_MAP = self.H_MAP_MAX

		szPanel_ID = self.MINIMAP_PANEL
		screen.addPanel(szPanel_ID, u"", "", False, False, self.X_MAP, self.Y_MAP, self.W_MAP, self.H_MAP, PanelStyles.PANEL_STYLE_MAIN)
		screen.initMinimap(self.X_MAP + self.MAP_MARGIN, self.X_MAP + self.W_MAP - self.MAP_MARGIN, self.Y_MAP + self.MAP_MARGIN, self.Y_MAP + self.H_MAP - self.MAP_MARGIN, self.Z_CONTROLS)
		screen.updateMinimapSection(False, False)
		screen.updateMinimapColorFromMap(MinimapModeTypes.MINIMAPMODE_TERRITORY, 0.3)
		screen.setMinimapMode(MinimapModeTypes.MINIMAPMODE_MILITARY)

		self.UL_SetMinimapVisibility(screen, True)
		screen.bringMinimapToFront()

	def UL_SetMinimapVisibility(self, screen, bVisibile):
		iOldMode = CyInterface().getShowInterface()

		if bVisibile:
			CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_MINIMAP_ONLY)
		else:
			CyInterface().setShowInterface(InterfaceVisibility.INTERFACE_HIDE)

		screen.updateMinimapVisibility()
		CyInterface().setShowInterface(iOldMode)

	def UL_refresh(self, bReload, bRedraw):

		if (self.iActivePlayer < 0):
			return

		screen = self.getScreen()

		if bRedraw:
			# Set scrollable area for unit buttons
			szPanel_ID = self.getNextWidgetName()
			screen.addPanel(szPanel_ID, "", "", True, True, self.X_TEXT, self.Y_TEXT, self.W_TEXT, self.H_TEXT, PanelStyles.PANEL_STYLE_MAIN)

			# Set scrollable area for leaders
			szPanel_ID = self.getNextWidgetName()
			screen.addPanel(szPanel_ID, "", "", False, True, self.X_LEADERS, self.Y_LEADERS, self.W_LEADERS, self.H_LEADERS, PanelStyles.PANEL_STYLE_MAIN)

			listLeaders = []
			for iLoopPlayer in range(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iLoopPlayer)
				if (player.isAlive() and (gc.getTeam(player.getTeam()).isHasMet(gc.getPlayer(self.iActivePlayer).getTeam()) or gc.getGame().isDebugMode())):
					listLeaders.append(iLoopPlayer)

			iNumLeaders = len(listLeaders)
			if iNumLeaders >= self.LEADER_COLUMNS:
				iButtonSize = self.LEADER_BUTTON_SIZE / 2
			else:
				iButtonSize = self.LEADER_BUTTON_SIZE

			iColumns = int(self.W_LEADERS / (iButtonSize + self.LEADER_MARGIN))

			# loop through all players and display leaderheads
			for iIndex in range(iNumLeaders):
				iLoopPlayer = listLeaders[iIndex]
				player = gc.getPlayer(iLoopPlayer)

				x = self.X_LEADERS + self.LEADER_MARGIN + (iIndex % iColumns) * (iButtonSize + self.LEADER_MARGIN)
				y = self.Y_LEADERS + self.LEADER_MARGIN + (iIndex // iColumns) * (iButtonSize + self.LEADER_MARGIN)

				if iLoopPlayer == gc.getORC_PLAYER():
					szButton = "Art/Interface/Buttons/Civilizations/Orc.dds"
				elif iLoopPlayer == gc.getANIMAL_PLAYER():
					szButton = "Art/Interface/Buttons/Civilizations/Animal.dds"
				elif iLoopPlayer == gc.getDEMON_PLAYER():
					szButton = "Art/Interface/Buttons/Civilizations/Barbarian.dds"
				else:
					szButton = gc.getLeaderHeadInfo(gc.getPlayer(iLoopPlayer).getLeaderType()).getButton()

				szLeaderButton = self.getLeaderButtonWidget(iLoopPlayer)              #self.getNextWidgetName()
				screen.addCheckBoxGFC(szLeaderButton, szButton, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), x, y, iButtonSize, iButtonSize, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 2, iLoopPlayer, ButtonStyles.BUTTON_STYLE_LABEL)
				screen.setState(szLeaderButton, (iLoopPlayer in self.selectedLeaderList))

		self.UL_refreshUnitSelection(bReload, bRedraw)

	def UL_refreshUnitSelection(self, bReload, bRedraw):
		screen = self.getScreen()

		screen.minimapClearAllFlashingTiles()

		if (bRedraw):
			iBtn_X = self.X_TEXT + self.MAP_MARGIN
			iBtn_Y = self.Y_TEXT + self.MAP_MARGIN/2
			iTxt_X = iBtn_X + 22
			iTxt_Y = iBtn_Y + 2
			if (self.bUnitDetails):
				szText = localText.getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_OFF", ())
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", iBtn_X, iBtn_Y, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_MINUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", szText, CvUtil.FONT_LEFT_JUSTIFY, iTxt_X, iTxt_Y, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				szText = localText.getText("TXT_KEY_MILITARY_ADVISOR_UNIT_TOGGLE_ON", ())
				screen.setButtonGFC(self.UNIT_BUTTON_ID, u"", "", iBtn_X, iBtn_Y, 20, 20, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_CITY_PLUS )
				screen.setLabel(self.UNIT_BUTTON_LABEL_ID, "", szText, CvUtil.FONT_LEFT_JUSTIFY, iTxt_X, iTxt_Y, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if bReload:
			activePlayer = gc.getPlayer(self.iActivePlayer)
			iActiveTeam = activePlayer.getTeam()
			activeTeam = gc.getTeam(iActiveTeam)
			self.grouper = UnitGrouper.StandardGrouper()
			self.stats = UnitGrouper.GrouperStats(self.grouper)
			for iPlayer in range(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iPlayer)
				if player.isAlive():
					team = gc.getTeam(player.getTeam())
					for iUnit in range(player.getNumUnits()):
						unit = player.getUnit(iUnit)
						if unit.isNone():
							continue
						plot = unit.plot()
						if plot.isNone():
							continue
						bVisible = plot.isVisible(iActiveTeam, False) and not unit.isInvisible(iActiveTeam, False)
						if not bVisible:
							continue
						if unit.getVisualOwner() in self.selectedLeaderList:
							self.stats.processUnit(activePlayer, activeTeam, unit)

		szText = localText.getText("TXT_KEY_PEDIA_ALL_UNITS", ()).upper()
		bAllSelected = self.isSelectedGroup(None)
		if (bAllSelected):
			szText = localText.changeTextColor(u"<u>" + szText + u"</u>", gc.getInfoTypeForString("COLOR_YELLOW"))
		if (bRedraw):
			screen.addListBoxGFC(self.UNIT_LIST_ID, "", self.X_TEXT+self.MAP_MARGIN, self.Y_TEXT+self.MAP_MARGIN+15, self.W_TEXT-2*self.MAP_MARGIN, self.H_TEXT-2*self.MAP_MARGIN-15, TableStyles.TABLE_STYLE_STANDARD)
			screen.enableSelect(self.UNIT_LIST_ID, False)
			screen.setStyle(self.UNIT_LIST_ID, "Table_StandardCiv_Style")
			screen.appendListBoxString(self.UNIT_LIST_ID, szText, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		else:
			screen.setListBoxStringGFC(self.UNIT_LIST_ID, 0, szText, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, -1, CvUtil.FONT_LEFT_JUSTIFY)

#		for grouping in self.stats.itergroupings():
#			for group in grouping.itergroups():
#				BugUtil.debug("%s / %s : %d (%d)" % (grouping.grouping.title, group.group.title, group.size(), group.isEmpty()))

		grouping1 = self.stats.getGrouping("loc")
		grouping2 = self.stats.getGrouping("type")
		iItem = 1
		for group1 in grouping1.itergroups():
			if (group1.isEmpty()):
				continue
			units1 = group1.units
			bGroup1Selected = self.isSelectedGroup(group1)
			szDescription = group1.group.title.upper() + u" (%d)" % len(units1)
			if (bGroup1Selected):
				szDescription = u"   <u>" + szDescription + u"</u>"
			else:
				szDescription = u"   " + szDescription
			if (bGroup1Selected or bAllSelected):
				szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))
			if (bRedraw):
				screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, group1.group.key, CvUtil.FONT_LEFT_JUSTIFY)
			else:
				screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, group1.group.key, CvUtil.FONT_LEFT_JUSTIFY)
			iItem += 1
			bGroup1Selected = bGroup1Selected or bAllSelected
			for group2 in grouping2.itergroups():
				units2 = group2.units & units1
				if (not units2):
					continue
				bGroup2Selected = self.isSelectedGroup(group2)
				szDescription = group2.group.title + u" (%d)" % len(units2)
				if (bGroup2Selected):
					szDescription = u"      <u>" + szDescription + u"</u>"
				else:
					szDescription = u"      " + szDescription
				if (bGroup2Selected or bGroup1Selected):
					szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))
				if (bRedraw):
					screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, group2.group.key, CvUtil.FONT_LEFT_JUSTIFY)
				else:
					screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, 1, group2.group.key, CvUtil.FONT_LEFT_JUSTIFY)
				iItem += 1

				bGroup2Selected = bGroup2Selected or bGroup1Selected
				for unit in units2:
					loopUnit = unit.unit
					bUnitSelected = self.isSelectedUnit(loopUnit.getOwner(), loopUnit.getID())
					if (self.bUnitDetails):
						szDescription = CyGameTextMgr().getSpecificUnitHelp(loopUnit, true, false)

						listMatches = re.findall("<.*?color.*?>", szDescription)
						for szMatch in listMatches:
							szDescription = szDescription.replace(szMatch, u"")

						if (loopUnit.isWaiting()):
							szDescription = '*' + szDescription

						if (bUnitSelected):
							szDescription = u"         <u>" + szDescription + u"</u>"
						else:
							szDescription = u"         " + szDescription

						if (bUnitSelected or bGroup2Selected):
							szDescription = localText.changeTextColor(szDescription, gc.getInfoTypeForString("COLOR_YELLOW"))

						if (bRedraw):
							screen.appendListBoxString(self.UNIT_LIST_ID, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, -loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						else:
							screen.setListBoxStringGFC(self.UNIT_LIST_ID, iItem, szDescription, WidgetTypes.WIDGET_MINIMAP_HIGHLIGHT, -loopUnit.getOwner(), loopUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY)
						iItem += 1

					iPlayer = loopUnit.getVisualOwner()
					player = PyPlayer(iPlayer)
					iColor = gc.getPlayerColorInfo(gc.getPlayer(iPlayer).getPlayerColor()).getColorTypePrimary()
					screen.setMinimapColor(MinimapModeTypes.MINIMAPMODE_MILITARY, loopUnit.getX(), loopUnit.getY(), iColor, 0.6)
					if (bUnitSelected or bGroup2Selected) and iPlayer in self.selectedLeaderList:

						if (player.getTeam().isAtWar(gc.getPlayer(self.iActivePlayer).getTeam())):
							iColor = gc.getInfoTypeForString("COLOR_RED")
						elif (gc.getPlayer(iPlayer).getTeam() != gc.getPlayer(self.iActivePlayer).getTeam()):
							iColor = gc.getInfoTypeForString("COLOR_YELLOW")
						else:
							iColor = gc.getInfoTypeForString("COLOR_WHITE")
						screen.minimapFlashPlot(loopUnit.getX(), loopUnit.getY(), iColor, -1)

	def refreshSelectedGroup(self, iSelected):
		if (iSelected in self.selectedGroupList):
			self.selectedGroupList.remove(iSelected)
		else:
			self.selectedGroupList.append(iSelected)
		self.UL_refreshUnitSelection(False, False)

	def refreshSelectedUnit(self, iPlayer, iUnitId):
		selectedUnit = (iPlayer, iUnitId)
		if (selectedUnit in self.selectedUnitList):
			self.selectedUnitList.remove(selectedUnit)
		else:
			self.selectedUnitList.append(selectedUnit)
		self.UL_refreshUnitSelection(False, False)

	def refreshSelectedLeader(self, iPlayer):
		if self.iShiftKeyDown == 1:
			if (iPlayer in self.selectedLeaderList):
				self.selectedLeaderList.remove(iPlayer)
			else:
				self.selectedLeaderList.append(iPlayer)
		else:
			self.selectedLeaderList = [iPlayer]

		self.UL_refresh(True, True)

	def isSelectedGroup(self, group):
		if not group:
			return -1 in self.selectedGroupList
		return group.group.key in self.selectedGroupList

	def isSelectedUnit(self, iPlayer, iUnitId):
		return (iPlayer, iUnitId) in self.selectedUnitList








	def minimapClicked(self):
		self.hideScreen()




	def getLeaderButtonWidget(self, iPlayer):
		szName = self.LEADER_BUTTON_ID + str(iPlayer)
		return szName


	def scrollGrid_Up(self):
		if self.iScreen == SITUATION_REPORT_SCREEN:
			self.SitRepGrid.scrollUp()

	def scrollGrid_Down(self):
		if self.iScreen == SITUATION_REPORT_SCREEN:
			self.SitRepGrid.scrollDown()



	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0

		# delete widgets with pre-defined names
		screen.deleteWidget(self.UNIT_BUTTON_ID)
		screen.deleteWidget(self.UNIT_LIST_ID)
		screen.deleteWidget(self.UNIT_BUTTON_LABEL_ID)
		#screen.hide(self.MINIMAP_PANEL)

		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			screen.deleteWidget(self.getLeaderButtonWidget(iLoopPlayer))

		# hide the mini-map
		#self.UL_SetMinimapVisibility(screen, false)

		# clear the grid
		if self.IconGridActive:
			self.SitRepGrid.hideGrid()
			self.IconGridActive = False



	# handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getFunctionName() == self.UNIT_LOC_TAB_ID):
				self.iScreen = UNIT_LOCATION_SCREEN
				self.showUnitLocation()

			elif (inputClass.getFunctionName() == self.SIT_REP_TAB_ID):
				self.iScreen = SITUATION_REPORT_SCREEN
				self.showSituationReport()

#			elif (inputClass.getFunctionName() == self.PLACE_HOLDER_TAB):
#				self.iScreen = PLACE_HOLDER
#				self.showGameSettingsScreen()

			elif (inputClass.getFunctionName() == self.UNIT_BUTTON_ID):
				self.bUnitDetails = not self.bUnitDetails
				self.UL_refreshUnitSelection(True, True)

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL):
				if (inputClass.getData1() == self.SCROLL_TABLE_UP):
					self.scrollGrid_Up()
				elif (inputClass.getData1() == self.SCROLL_TABLE_DOWN):
					self.scrollGrid_Down()

		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
			if (inputClass.getData() == int(InputTypes.KB_LSHIFT)
			or  inputClass.getData() == int(InputTypes.KB_RSHIFT)):
				self.iShiftKeyDown = inputClass.getID()

#		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED and inputClass.getFunctionName() == self.UNIT_BUTTON_ID) :
#			self.bUnitDetails = not self.bUnitDetails
#			self.refreshUnitSelection(True)
#		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER):
#			if (inputClass.getData() == int(InputTypes.KB_LSHIFT) or inputClass.getData() == int(InputTypes.KB_RSHIFT)):
#				self.iShiftKeyDown = inputClass.getID()

		return 0


	def update(self, fDelta):
		return
