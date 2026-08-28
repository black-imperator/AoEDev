## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
import CvMainInterface
import CvDomesticAdvisor
import CvTechChooser
import CvForeignAdvisor
import CvExoticForeignAdvisor
import CvMilitaryAdvisor
import CvFinanceAdvisor
import CvReligionScreen
import CvCorporationScreen
import CvCivicsScreen
import CvVictoryScreen
import CvEspionageAdvisor
import CvScreenEnums

import CvOptionsScreen
import CvReplayScreen
import CvHallOfFameScreen
import CvDanQuayle
import CvUnVictoryScreen

import CvDawnOfMan
import CvTechSplashScreen
import CvTopCivs
import CvInfoScreen

import CvIntroMovieScreen
import CvVictoryMovieScreen
import CvWonderMovieScreen
import CvEraMovieScreen
import CvSpaceShipScreen
import CvBootlegSOScreen

import CvPediaMain
import CvPediaLore
import CvPediaHistory

import CvWorldBuilderScreen

import CvDebugTools
import CvDebugInfoScreen
#import CvDiplomacy
# DynTraits Start
import CvTraitScreen
# DynTraits End
import CvUtil
import CvEventInterface
import CvPopupInterface
import CvScreenUtilsInterface
import ScreenInput as PyScreenInput
from CvScreenEnums import *
from CvPythonExtensions import *

import CvGuildScreen
#FfH: Added by Talchas 05/19/2007
import CvTrophyHall
#FfH: End Add
# < Unit Statistics Mod Start >
import CvStatisticsScreen
# < Unit Statistics Mod En
#Begin Mercenaries
import CvMercenaryManager
#End Mercenaries 
import CvCivSelectScreen

### GameFont Display
import GameFontDisplay
### GameFont Display
import CustomFunctions
import PyHelpers
## World Builder ##
import CvPlatyBuilderScreen
import WBPlotScreen
import WBEventScreen
import WBBuildingScreen
import WBCityDataScreen
import WBCityEditScreen
import WBTechScreen
import WBProjectScreen
import WBTeamScreen
import WBPlayerScreen
import WBUnitScreen
import WBPromotionScreen
import WBDiplomacyScreen
import WBGameDataScreen
import WBPlayerUnits
import WBReligionScreen
import WBCorporationScreen
import WBInfoScreen
import WBTradeScreen

g_bIsScreenActive = -1

def toggleSetNoScreens():
	global g_bIsScreenActive
	print "SCREEN OFF"
	g_bIsScreenActive = -1

def toggleSetScreenOn(argsList):
	global g_bIsScreenActive
	print "%s SCREEN TURNED ON" %(argsList[0],)
	g_bIsScreenActive = argsList[0]

#diplomacyScreen = CvDiplomacy.CvDiplomacy()

mainInterface = CvMainInterface.CvMainInterface()
def showMainInterface():
	mainInterface.interfaceScreen()

def numPlotListButtons():
	return mainInterface.numPlotListButtons()

CivSelectScreen = CvCivSelectScreen.CvCivSelectScreen()
def showCivSelectScreen():
	CivSelectScreen.interfaceScreen()

def sendCivSelectMessage(argsList):
	CivSelectScreen.sendMessage(argsList)

#FfH: Added by Talchas 05/19/2007
trophyHall = CvTrophyHall.CvTrophyHall()
def showTrophyHall():
	if (-1 != CyGame().getActivePlayer()):
		#infoScreen.showScreen(-1, 1, 1)
		trophyHall.interfaceScreen()
#FfH: End Add

guildScreen = CvGuildScreen.CvGuildScreen()
def showGuildScreen():
	guildScreen.interfaceScreen()

techChooser = CvTechChooser.CvTechChooser()
def showTechChooser():
	if (-1 != CyGame().getActivePlayer()):
		techChooser.interfaceScreen()

hallOfFameScreen = CvHallOfFameScreen.CvHallOfFameScreen(HALL_OF_FAME)
def showHallOfFame(argsList):
	hallOfFameScreen.interfaceScreen(argsList[0])

civicScreen = CvCivicsScreen.CvCivicsScreen()
def showCivicsScreen():
	if (-1 != CyGame().getActivePlayer()):
		civicScreen.interfaceScreen()

religionScreen = CvReligionScreen.CvReligionScreen()
def showReligionScreen():
	if (-1 != CyGame().getActivePlayer()):
		religionScreen.interfaceScreen()

corporationScreen = CvCorporationScreen.CvCorporationScreen()
def showCorporationScreen():
	if (-1 != CyGame().getActivePlayer()):
		corporationScreen.interfaceScreen()

## FfH Card Game: begin
def updateCorporationElement(part, argsList = None):
		corporationScreen.updateElement(part, argsList)
## FfH Card Game: end

optionsScreen = CvOptionsScreen.CvOptionsScreen()
def showOptionsScreen():
	optionsScreen.interfaceScreen()

#foreignAdvisor = CvForeignAdvisor.CvForeignAdvisor()
foreignAdvisor = CvExoticForeignAdvisor.CvExoticForeignAdvisor()
def showForeignAdvisorScreen(argsList):
	if (-1 != CyGame().getActivePlayer()):
		foreignAdvisor.interfaceScreen(argsList[0])

financeAdvisor = CvFinanceAdvisor.CvFinanceAdvisor()
def showFinanceAdvisor():
	if (-1 != CyGame().getActivePlayer()):
		financeAdvisor.interfaceScreen()

domesticAdvisor = CvDomesticAdvisor.CvDomesticAdvisor()
def showDomesticAdvisor(argsList):
	if (-1 != CyGame().getActivePlayer()):
		domesticAdvisor.interfaceScreen()

militaryAdvisor = CvMilitaryAdvisor.CvMilitaryAdvisor(MILITARY_ADVISOR)
def showMilitaryAdvisor():
	if (-1 != CyGame().getActivePlayer()):
		militaryAdvisor.interfaceScreen()

espionageAdvisor = CvEspionageAdvisor.CvEspionageAdvisor()
def showEspionageAdvisor():
#	if (-1 != CyGame().getActivePlayer()):
	espionageAdvisor.interfaceScreen()

dawnOfMan = CvDawnOfMan.CvDawnOfMan(DAWN_OF_MAN)
def showDawnOfMan(argsList):
	dawnOfMan.interfaceScreen()

introMovie = CvIntroMovieScreen.CvIntroMovieScreen()
def showIntroMovie(argsList):
	introMovie.interfaceScreen()

victoryMovie = CvVictoryMovieScreen.CvVictoryMovieScreen()
def showVictoryMovie(argsList):
	victoryMovie.interfaceScreen(argsList[0])

wonderMovie = CvWonderMovieScreen.CvWonderMovieScreen()
def showWonderMovie(argsList):
	wonderMovie.interfaceScreen(argsList[0], argsList[1], argsList[2])

eraMovie = CvEraMovieScreen.CvEraMovieScreen()
def showEraMovie(argsList):
	return
#	eraMovie.interfaceScreen(argsList[0])

spaceShip = CvSpaceShipScreen.CvSpaceShipScreen()
def showSpaceShip(argsList):
	if (-1 != CyGame().getActivePlayer()):
		spaceShip.interfaceScreen(argsList[0])

replayScreen = CvReplayScreen.CvReplayScreen(REPLAY_SCREEN)
def showReplay(argsList):
	if argsList[0] > -1:
		CyGame().saveReplay(argsList[0])
	replayScreen.showScreen(argsList[4])

danQuayleScreen = CvDanQuayle.CvDanQuayle()
def showDanQuayleScreen(argsList):
	danQuayleScreen.interfaceScreen()

unVictoryScreen = CvUnVictoryScreen.CvUnVictoryScreen()
def showUnVictoryScreen(argsList):
	unVictoryScreen.interfaceScreen()
	
# DynTraits Start
dynTraitsScreen = CvTraitScreen.CvTraitScreen()
def showTraitsScreen():
	dynTraitsScreen.interfaceScreen(argsList[0])
	
def showTraitPopup(argsList):
	CvTraitScreen.showTraitPopup(argsList)
# DynTraits End

topCivs = CvTopCivs.CvTopCivs()
def showTopCivs():
	topCivs.showScreen()

infoScreen = CvInfoScreen.CvInfoScreen(INFO_SCREEN)
def showInfoScreen(argsList):
	if (-1 != CyGame().getActivePlayer()):
		iTabID = argsList[0]
		iEndGame = argsList[1]
		infoScreen.showScreen(-1, iTabID, iEndGame)

debugInfoScreen = CvDebugInfoScreen.CvDebugInfoScreen()
def showDebugInfoScreen():
	debugInfoScreen.interfaceScreen()

techSplashScreen = CvTechSplashScreen.CvTechSplashScreen(TECH_SPLASH)
def showTechSplash(argsList):
	techSplashScreen.interfaceScreen(argsList[0])

victoryScreen = CvVictoryScreen.CvVictoryScreen(VICTORY_SCREEN)
def showVictoryScreen():
	if (-1 != CyGame().getActivePlayer()):
		victoryScreen.interfaceScreen()

bootlegSOScreen = CvBootlegSOScreen.CvBootlegSOScreen()
def showBootlegSO():
	if CyGInterfaceScreen("BootlegSOScreen", CvScreenEnums.BOOTLEG_SO_SCREEN).isActive():
		bootlegSOScreen.hideScreen()
	else:
		bootlegSOScreen.interfaceScreen()

def changeBootlegSORadius():
	if CyGInterfaceScreen("BootlegSOScreen", CvScreenEnums.BOOTLEG_SO_SCREEN).isActive():
		bootlegSOScreen.changeRadius()

def changeBootlegSODraw():
	bootlegSOScreen.changeDraw()

# < Unit Statistics Mod Start >
statisticsScreen = CvStatisticsScreen.CvStatisticsScreen()
# < Unit Statistics Mod End   >
#Begin Mercenaries
mercenaryManager = CvMercenaryManager.CvMercenaryManager(CvScreenEnums.MERCENARY_MANAGER)
#End Mercenaries
#################################################
## Civilopedia
#################################################
pediaMainScreen = CvPediaMain.CvPediaMain()

def linkToPedia(argsList): # This function is used for all links in the pedia
	pediaMainScreen.link(argsList[0])

def pediaShow():
	return pediaMainScreen.pediaShow()

def pediaBack():
	return pediaMainScreen.back()

def pediaForward():
	pediaMainScreen.forward()

def pediaMain(argsList):
	pediaMainScreen.pediaJump(PEDIA_MAIN, argsList[0], True)

def pediaJumpToTech(argsList):
	pediaMainScreen.pediaJump(PEDIA_TECH, argsList[0], True)

def pediaJumpToUnit(argsList):
	pediaMainScreen.pediaJump(PEDIA_UNIT, argsList[0], True)

def pediaJumpToBuilding(argsList):
	pediaMainScreen.pediaJump(PEDIA_BUILDING, argsList[0], True)

def pediaJumpToProject(argsList):
	pediaMainScreen.pediaJump(PEDIA_PROJECT, argsList[0], True)

def pediaJumpToReligion(argsList):
	pediaMainScreen.pediaJump(PEDIA_RELIGION, argsList[0], True)

def pediaJumpToCorporation(argsList):
	pediaMainScreen.pediaJump(PEDIA_CORPORATION, argsList[0], True)

def pediaJumpToPromotion(argsList):
	pediaMainScreen.pediaJump(PEDIA_PROMOTION, argsList[0], True)

def pediaJumpToSpell(argsList):
	pediaMainScreen.pediaJump(PEDIA_SPELL, argsList[0], True)

def pediaJumpToUnitChart(argsList):
	pediaMainScreen.pediaJump(PEDIA_UNIT_CHART, argsList[0], True)

def pediaJumpToBonus(argsList):
	pediaMainScreen.pediaJump(PEDIA_BONUS, argsList[0], True)

def pediaJumpToTerrain(argsList):
	pediaMainScreen.pediaJump(PEDIA_TERRAIN, argsList[0], True)

def pediaJumpToFeature(argsList):
	pediaMainScreen.pediaJump(PEDIA_FEATURE, argsList[0], True)

def pediaJumpToPlotEffect(argsList):
	pediaMainScreen.pediaJump(PEDIA_PLOT_EFFECT, argsList[0], True)

def pediaJumpToImprovement(argsList):
	pediaMainScreen.pediaJump(PEDIA_IMPROVEMENT, argsList[0], True)

def pediaJumpToCivic(argsList):
	pediaMainScreen.pediaJump(PEDIA_CIVIC, argsList[0], True)

def pediaJumpToCiv(argsList):
	pediaMainScreen.pediaJump(PEDIA_CIVILIZATION, argsList[0], True)

def pediaJumpToCityClass(argsList):
	pediaMainScreen.pediaJump(PEDIA_CITYCLASS, argsList[0], True)

def pediaJumpToRoute(argsList):
	pediaMainScreen.pediaJump(PEDIA_ROUTE, argsList[0], True)

def pediaJumpToLeader(argsList):
	pediaMainScreen.pediaJump(PEDIA_LEADER, argsList[0], True)

def pediaJumpToTrait(argsList):
	pediaMainScreen.pediaJump(PEDIA_TRAIT, argsList[0], True)

def pediaJumpToSpawnGroup(argsList):
	pediaMainScreen.pediaJump(PEDIA_SPAWNGROUP, argsList[0], True)

def pediaJumpToAffinity(argsList):
	pediaMainScreen.pediaJump(PEDIA_AFFINITY, argsList[0], True)

def pediaJumpToSpecialist(argsList):
	pediaMainScreen.pediaJump(PEDIA_SPECIALIST, argsList[0], True)

def pediaShowLore(argsList):
	iEntryId = pediaMainScreen.pediaLore.getIdFromEntryInfo(argsList[0], argsList[1])
	pediaMainScreen.pediaJump(PEDIA_LORE, iEntryId, True)
	return

def pediaShowHistorical(argsList):
	iEntryId = pediaMainScreen.pediaHistorical.getIdFromEntryInfo(argsList[0], argsList[1])
	pediaMainScreen.pediaJump(PEDIA_HISTORY, iEntryId, True)
	return

#################################################
## Worldbuilder
#################################################
worldBuilderScreen = CvPlatyBuilderScreen.CvWorldBuilderScreen()
def getWorldBuilderScreen():
	return worldBuilderScreen

def showWorldBuilderScreen():
	worldBuilderScreen.interfaceScreen()

def hideWorldBuilderScreen():
	worldBuilderScreen.killScreen()

def WorldBuilderToggleUnitEditCB():
	worldBuilderScreen.toggleUnitEditCB()

def WorldBuilderEraseCB():
	worldBuilderScreen.eraseCB()

def WorldBuilderLandmarkCB():
	worldBuilderScreen.landmarkModeCB()

def WorldBuilderExitCB():
	worldBuilderScreen.Exit()

def WorldBuilderToggleCityEditCB():
	worldBuilderScreen.toggleCityEditCB()

def WorldBuilderNormalPlayerTabModeCB():
	worldBuilderScreen.normalPlayerTabModeCB()

def WorldBuilderNormalMapTabModeCB():
	worldBuilderScreen.normalMapTabModeCB()

def WorldBuilderRevealTabModeCB():
	worldBuilderScreen.revealTabModeCB()

def WorldBuilderRevealAllCB():
	worldBuilderScreen.revealAll(True)

def WorldBuilderUnRevealAllCB():
	worldBuilderScreen.revealAll(False)

def WorldBuilderGetHighlightPlot(argsList):
	return worldBuilderScreen.getHighlightPlot(argsList)

def WorldBuilderOnAdvancedStartBrushSelected(argsList):
	iList,iIndex,iTab = argsList;
	print("WB Advanced Start brush selected, iList=%d, iIndex=%d, type=%d" %(iList,iIndex,iTab))
	if (iTab == worldBuilderScreen.m_iASTechTabID):
		showTechChooser()
	elif (iTab == worldBuilderScreen.m_iASCityTabID and iList == worldBuilderScreen.m_iASAutomateListID):
		CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_AUTOMATE, worldBuilderScreen.m_iCurrentPlayer, -1, -1, -1, true)

	if (worldBuilderScreen.setCurrentAdvancedStartIndex(iIndex)):
		if (worldBuilderScreen.setCurrentAdvancedStartList(iList)):
			return 1
	return 0

def WorldBuilderGetASUnitTabID():
	return worldBuilderScreen.getASUnitTabID()

def WorldBuilderGetASCityTabID():
	return worldBuilderScreen.getASCityTabID()

def WorldBuilderGetASCityListID():
	return worldBuilderScreen.getASCityListID()

def WorldBuilderGetASBuildingsListID():
	return worldBuilderScreen.getASBuildingsListID()

def WorldBuilderGetASAutomateListID():
	return worldBuilderScreen.getASAutomateListID()

def WorldBuilderGetASImprovementsTabID():
	return worldBuilderScreen.getASImprovementsTabID()

def WorldBuilderGetASRoutesListID():
	return worldBuilderScreen.getASRoutesListID()

def WorldBuilderGetASImprovementsListID():
	return worldBuilderScreen.getASImprovementsListID()

def WorldBuilderGetASVisibilityTabID():
	return worldBuilderScreen.getASVisibilityTabID()

def WorldBuilderGetASTechTabID():
	return worldBuilderScreen.getASTechTabID()

#################################################
## Utility Functions (can be overridden by CvScreenUtilsInterface
#################################################

def movieDone(argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().movieDone(argsList)):
		return

	if (argsList[0] == INTRO_MOVIE_SCREEN):
		introMovie.hideScreen()

	if (argsList[0] == VICTORY_MOVIE_SCREEN):
		victoryMovie.hideScreen()

def leftMouseDown (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().leftMouseDown(argsList)):
		return

	if ( argsList[0] == WORLDBUILDER_SCREEN ):
		worldBuilderScreen.leftMouseDown(argsList[1:])
		return 1
	return 0

def rightMouseDown (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().rightMouseDown(argsList)):
		return

	if ( argsList[0] == WORLDBUILDER_SCREEN ):
		worldBuilderScreen.rightMouseDown(argsList)
		return 1
	return 0

def mouseOverPlot (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().mouseOverPlot(argsList)):
		return

	if ( argsList[0] == BOOTLEG_SO_SCREEN ):
		bootlegSOScreen.mouseOverPlot(argsList)

	if (WORLDBUILDER_SCREEN == argsList[0]):
		worldBuilderScreen.mouseOverPlot(argsList)

def handleInput (argsList):
	' handle input is called when a screen is up '
	inputClass = PyScreenInput.ScreenInput(argsList)

	# allows overides for mods
	ret = CvScreenUtilsInterface.getScreenUtils().handleInput( (inputClass.getPythonFile(),inputClass) )

	# get the screen that is active from the HandleInputMap Dictionary
	screen = HandleInputMap.get( inputClass.getPythonFile() )

	# call handle input on that screen
	if ( screen and not ret):
		return screen.handleInput(inputClass)
	return 0

def update (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().update(argsList)):
		return

	if (HandleInputMap.has_key(argsList[0])):
		screen = HandleInputMap.get(argsList[0])
		screen.update(argsList[1])

def onClose (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().onClose(argsList)):
		return

	if (HandleCloseMap.has_key(argsList[0])):
		screen = HandleCloseMap.get(argsList[0])
		screen.onClose()

# Forced screen update
def forceScreenUpdate (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().forceScreenUpdate(argsList)):
		return

	# Tech chooser update (forced from net message)
	if ( argsList[0] == TECH_CHOOSER ):
		techChooser.updateTechRecords(false)
	# Main interface Screen
	elif ( argsList[0] == MAIN_INTERFACE ):
		mainInterface.updateScreen()
	# world builder Screen
	elif ( argsList[0] == WORLDBUILDER_SCREEN ):
		worldBuilderScreen.updateScreen()

# Forced redraw
def forceScreenRedraw (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().forceScreenRedraw(argsList)):
		return

	# Main Interface Screen
	if ( argsList[0] == MAIN_INTERFACE ):
		mainInterface.redraw()
	elif ( argsList[0] == TECH_CHOOSER ):
		techChooser.updateTechRecords(true)


def minimapClicked (argsList):
	# allows overides for mods
	if (CvScreenUtilsInterface.getScreenUtils().minimapClicked(argsList)):
		return

	if (MILITARY_ADVISOR == argsList[0]):
		militaryAdvisor.minimapClicked()
	# < Unit Statistics Mod Start >
	if (HIGHSCORES_SCREEN == argsList[0] or TOP10_SCREEN1 == argsList[0] or TOP10_SCREEN2 == argsList[0]):
		statisticsScreen.minimapClicked()
	# < Unit Statistics Mod End   >
	return

############################################################################
## Misc Functions
############################################################################

def handleBack(screens):
	for iScreen in screens:
		if (HandleNavigationMap.has_key(iScreen)):
			screen = HandleNavigationMap.get( iScreen )
			screen.back()
	print "Mouse BACK"
	return 0

def handleForward(screens):
	for iScreen in screens:
		if (HandleNavigationMap.has_key(iScreen)):
			screen = HandleNavigationMap.get( iScreen )
			screen.forward()
	print "Mouse FWD"
	return 0

def refreshMilitaryAdvisor (argsList):
	if (1 == argsList[0]):
		militaryAdvisor.refreshSelectedGroup(argsList[1])
	elif (2 == argsList[0]):
		militaryAdvisor.refreshSelectedLeader(argsList[1])
	elif (argsList[0] <= 0):
		militaryAdvisor.refreshSelectedUnit(-argsList[0], argsList[1])

def updateMusicPath (argsList):
	szPathName = argsList[0]
	optionsScreen.updateMusicPath(szPathName)

def refreshOptionsScreen():
	optionsScreen.refreshScreen()

def cityWarningOnClickedCallback(argsList):
	iButtonId = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]
	city = CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
	if (not city.isNone()):
		if (iButtonId == 0):
			if (city.isProductionProcess()):
				CyMessageControl().sendPushOrder(iData1, iData2, iData3, False, False, False)
			else:
				CyMessageControl().sendPushOrder(iData1, iData2, iData3, False, True, False)
		elif (iButtonId == 2):
			CyInterface().selectCity(city, False)

def cityWarningOnFocusCallback(argsList):
	CyInterface().playGeneralSound("AS2D_ADVISOR_SUGGEST")
	CyInterface().lookAtCityOffset(argsList[0])
	return 0

def liberateOnClickedCallback(argsList):
	iButtonId = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]
	city = CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
	if (not city.isNone()):
		if (iButtonId == 0):
			# Issue #334: iData2 is the civ the popup promised the city to.
			# TASK_LIBERATE re-derives that civ and silently does nothing when the
			# answer has changed, so send TASK_GIFT instead: it still calls
			# liberate() while getLiberationPlayer() agrees, and falls back to
			# acquireCity() when it no longer does.
			if (iData2 >= 0 and CyGlobalContext().getPlayer(iData2).isAlive()):
				CyMessageControl().sendDoTask(iData1, TaskTypes.TASK_GIFT, iData2, -1, False, False, False, False)
			else:
				CyMessageControl().sendDoTask(iData1, TaskTypes.TASK_LIBERATE, 0, -1, False, False, False, False)
		elif (iButtonId == 2):
			CyInterface().selectCity(city, False)

def colonyOnClickedCallback(argsList):
	iButtonId = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]
	city = CyGlobalContext().getPlayer(CyGlobalContext().getGame().getActivePlayer()).getCity(iData1)
	if (not city.isNone()):
		if (iButtonId == 0):
			CyMessageControl().sendEmpireSplit(CyGlobalContext().getGame().getActivePlayer(), city.area().getID())
		elif (iButtonId == 2):
			CyInterface().selectCity(city, False)

def featAccomplishedOnClickedCallback(argsList):
	iButtonId = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]

	if (iButtonId == 1):
		if (iData1 == FeatTypes.FEAT_TRADE_ROUTE):
			showDomesticAdvisor(())
		elif ((iData1 >= FeatTypes.FEAT_UNITCOMBAT_ARCHER) and (iData1 <= FeatTypes.FEAT_UNIT_SPY)):
			showMilitaryAdvisor()
		elif ((iData1 >= FeatTypes.FEAT_COPPER_CONNECTED) and (iData1 <= FeatTypes.FEAT_FOOD_CONNECTED)):
			showForeignAdvisorScreen([0])
		elif ((iData1 == FeatTypes.FEAT_NATIONAL_WONDER)):
		  # 2 is for the wonder tab...
			showInfoScreen([2, 0])
#		elif ((iData1 >= FeatTypes.FEAT_POPULATION_HALF_MILLION) and (iData1 <= FeatTypes.FEAT_POPULATION_2_BILLION)):
#		  # 1 is for the demographics tab...
#			showInfoScreen([1, 0])
		elif iData1 == FeatTypes.FEAT_CORPORATION_ENABLED:
			showCorporationScreen()

def featAccomplishedOnFocusCallback(argsList):
	iData1 = argsList[0]
	iData2 = argsList[1]
	iData3 = argsList[2]
	iData4 = argsList[3]
	szText = argsList[4]
	bOption1 = argsList[5]
	bOption2 = argsList[6]

	CyInterface().playGeneralSound("AS2D_FEAT_ACCOMPLISHED")
	if ((iData1 >= FeatTypes.FEAT_UNITCOMBAT_ARCHER) and (iData1 <= FeatTypes.FEAT_FOOD_CONNECTED)):
		CyInterface().lookAtCityOffset(iData2)

	return 0

def reassignPlayer(argsList):
	iButtonId = argsList[0]
	iOldPlayer = argsList[1]
	iNewPlayer = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]

	if iButtonId == 0:
		CyMessageControl().sendModNetMessage(CvUtil.reassignPlayer, iOldPlayer, iNewPlayer, 0, 0)
		#CyGame().reassignPlayerAdvanced(iOldPlayer, iNewPlayer, -1)

def applyCheatEvents2(argsList):
	gc				= CyGlobalContext()
	iButtonId		= argsList[0]
	iPlayer			= argsList[1]
	pPlayer			= gc.getPlayer(iPlayer)
	szText			= argsList[5]
	lEvents			= []
	if "[" in szText:
		i = szText.index("[")
		szText = szText[i:]
		szText = szText.replace("[","").replace("]","")
		lEvents = map(int,szText.split(","))
	if lEvents:
		pPlayer.trigger(lEvents[iButtonId])

def applyRemoveAIUnits(argsList):
	gc				= CyGlobalContext()
	iButtonId		= argsList[0]
	lUC				= []
	if iButtonId == 0:
		return
	for i in xrange(gc.getNumUnitCombatInfos()):
		lUC.append(i)
	for iPlayer in xrange(gc.getMAX_PLAYERS()):
		if not gc.getPlayer(iPlayer).isHuman():
			pyPlayer = PyHelpers.PyPlayer(iPlayer)
			apUnitList = pyPlayer.getUnitList()
			for pUnit in apUnitList:
				if iButtonId == 1:
					pUnit.kill(True, PlayerTypes.NO_PLAYER)
				if iButtonId == 2:
					killRoll = CyGame().getSorenRandNum(100, "debug RemoveAIUnits 50%")
					if killRoll < 50:
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
				if iButtonId > 2:
					iRemoveUC = iButtonId - 3
					if pUnit.getUnitCombatType() == iRemoveUC:
						pUnit.kill(True, PlayerTypes.NO_PLAYER)

def effectRepublic(argsList):
	iButtonId	= argsList[0]
	iPlayer		= argsList[1]
	iElection	= argsList[2]
	gc			= CyGlobalContext()
	git			= gc.getInfoTypeForString
	pPlayer		= gc.getPlayer(iPlayer)
	iRnd		= CyGame().getSorenRandNum(100, "Republic Election")
	iShift		= iButtonId
	if iRnd < 20 and iButtonId != 2: # 20% to fail if someone is supported
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_REPUBLIC_ELECTION_OPPOSITION_PARTY_WINS", ()),'',3,'Art/Interface/Buttons/Civics/Republic.dds',git("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		return
	lRepublicTraits		= [git("TRAIT_AGGRESSIVE_REPUBLIC"),git("TRAIT_DEFENDER_REPUBLIC"),git("TRAIT_FINANCIAL_REPUBLIC"),git("TRAIT_EXPANSIVE_REPUBLIC"),git("TRAIT_SPIRITUAL_REPUBLIC"),git("TRAIT_ORGANIZED_REPUBLIC"),git("TRAIT_INDUSTRIOUS_REPUBLIC"),git("TRAIT_PHILOSOPHICAL_REPUBLIC")]
	lTraits				= [git("TRAIT_AGGRESSIVE"),git("TRAIT_DEFENDER"),git("TRAIT_FINANCIAL"),git("TRAIT_EXPANSIVE"),git("TRAIT_SPIRITUAL"),git("TRAIT_ORGANIZED"),git("TRAIT_INDUSTRIOUS"),git("TRAIT_PHILOSOPHICAL")]
	lRepublicTraitsText = ["TXT_KEY_EVENT_REPUBLIC_ELECTION_HAWK_WINS","TXT_KEY_EVENT_REPUBLIC_ELECTION_DOVE_WINS","TXT_KEY_EVENT_REPUBLIC_ELECTION_LANDOWNER_WINS","TXT_KEY_EVENT_REPUBLIC_ELECTION_PEASANT_WINS","TXT_KEY_EVENT_REPUBLIC_ELECTION_CHURCH_WINS","TXT_KEY_EVENT_REPUBLIC_ELECTION_STATE_WINS","TXT_KEY_EVENT_REPUBLIC_ELECTION_LABOR_WINS","TXT_KEY_EVENT_REPUBLIC_ELECTION_ACADEMIA_WINS"]
	lRepublicAltText	= ["TXT_KEY_EVENT_REPUBLIC_ELECTION_HAWK_WINS_ALREADY_AGGRESSIVE","TXT_KEY_EVENT_REPUBLIC_ELECTION_DOVE_WINS_ALREADY_DEFENSIVE","TXT_KEY_EVENT_REPUBLIC_ELECTION_LANDOWNER_WINS_ALREADY_FINANCIAL","TXT_KEY_EVENT_REPUBLIC_ELECTION_PEASANT_WINS_ALREADY_EXPANSIVE","TXT_KEY_EVENT_REPUBLIC_ELECTION_CHURCH_WINS_ALREADY_SPIRITUAL","TXT_KEY_EVENT_REPUBLIC_ELECTION_STATE_WINS_ALREADY_ORGANIZED","TXT_KEY_EVENT_REPUBLIC_ELECTION_LABOR_WINS_ALREADY_INDUSTRIOUS","TXT_KEY_EVENT_REPUBLIC_ELECTION_ACADEMIA_WINS_ALREADY_PHILOSOPHICAL"]
	if iRnd < 50 and iButtonId == 2: # 50/50 for every party to win if no one is supported
		iShift = 0
	elif iButtonId == 2:
		iShift = 1
	iElectionIndex = iElection * 2 + iShift # Based on Election Type and Button pressed: Hawk = 0, Dove = 1, Landowner = 2, Pesants = 3, Church = 4, State = 5, Labor = 6, Academia = 7
	bRepeatTrait = 0
	iTrait = lTraits[iElectionIndex]
	iRepublicTrait= lRepublicTraits[iElectionIndex]
	if pPlayer.hasTrait(iTrait) or pPlayer.hasTrait(iRepublicTrait):
		bRepeatTrait = 1
	if bRepeatTrait == 0: # Trait Rewards
		if not gc.isNoCrash():
			pPlayer.setHasTrait((iRepublicTrait),True,-1,True,True)
		else:
			pPlayer.setHasTrait((iRepublicTrait),True)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(lRepublicTraitsText[iElectionIndex], ()),'',3,'Art/Interface/Buttons/Civics/Republic.dds',git("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
	else: # Alt Rewards
		if iElectionIndex == 0: # Hawk wins
			pPlayer.initUnit(git('UNIT_COMMANDER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iElectionIndex == 1: # Dove wins
			for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
				loopPlayer = gc.getPlayer(iLoopPlayer)
				if loopPlayer.isAlive():
					if loopPlayer.getTeam() != pPlayer.getTeam():
						loopPlayer.AI_changeAttitudeExtra(iPlayer, 3)
						pPlayer.AI_changeAttitudeExtra(iLoopPlayer, 3)
		if iElectionIndex == 2: # Landowner wins
			pPlayer.initUnit(git('UNIT_MERCHANT'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iElectionIndex == 3: # Pesants win
			(loopCity, iter) = pPlayer.firstCity(False)
			while(loopCity):
				loopCity.changeHappinessTimer(30)
				pCity.changeEspionageHealthCounter(-5)
				(loopCity, iter) = pPlayer.nextCity(iter, False)
		if iElectionIndex == 4: # Church wins
			pPlayer.initUnit(git('UNIT_PROPHET'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iElectionIndex == 5: # State wins
			pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())
		if iElectionIndex == 6: # Labor wins
			pPlayer.initUnit(git('UNIT_ENGINEER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iElectionIndex == 7: # Academia wins
			pPlayer.initUnit(git('UNIT_SCIENTIST'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(lRepublicAltText[iElectionIndex], ()),'',3,'Art/Interface/Buttons/Civics/Republic.dds',git("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)

def passToModNetMessage(argsList):
	iData2	= argsList[0]
	iData3	= argsList[1]
	iData4	= argsList[2]
	iData1	= argsList[3]
	CyMessageControl().sendModNetMessage(iData1,iData2,iData3,iData4,-1)

#######################################################################################
## Handle Close Map
#######################################################################################
HandleCloseMap = {  DAWN_OF_MAN : dawnOfMan,
					SPACE_SHIP_SCREEN : spaceShip,
					TECH_CHOOSER : techChooser,
				# add new screens here
				}

#######################################################################################
## Handle Input Map
#######################################################################################
HandleInputMap = {  MAIN_INTERFACE : mainInterface,
					DOMESTIC_ADVISOR : domesticAdvisor,
					RELIGION_SCREEN : religionScreen,
					CORPORATION_SCREEN : corporationScreen,
					CIVICS_SCREEN : civicScreen,
					TECH_CHOOSER : techChooser,
					FOREIGN_ADVISOR : foreignAdvisor,
					FINANCE_ADVISOR : financeAdvisor,
					MILITARY_ADVISOR : militaryAdvisor,
					DAWN_OF_MAN : dawnOfMan,
					WONDER_MOVIE_SCREEN : wonderMovie,
					ERA_MOVIE_SCREEN : eraMovie,
					SPACE_SHIP_SCREEN : spaceShip,
					INTRO_MOVIE_SCREEN : introMovie,
					OPTIONS_SCREEN : optionsScreen,
					INFO_SCREEN : infoScreen,
					TECH_SPLASH : techSplashScreen,
					REPLAY_SCREEN : replayScreen,
					VICTORY_SCREEN : victoryScreen,
					TOP_CIVS : topCivs,
					HALL_OF_FAME : hallOfFameScreen,
					VICTORY_MOVIE_SCREEN : victoryMovie,
					ESPIONAGE_ADVISOR : espionageAdvisor,
					DAN_QUAYLE_SCREEN : danQuayleScreen,

#FfH: Added by Talchas 05/19/2007
					101:trophyHall,
#FfH: End Add

					PEDIA_MAIN : pediaMainScreen,
					PEDIA_TECH : pediaMainScreen,
					PEDIA_UNIT : pediaMainScreen,
					PEDIA_BUILDING : pediaMainScreen,
					PEDIA_PROMOTION : pediaMainScreen,
					PEDIA_PROJECT : pediaMainScreen,
					PEDIA_UNIT_CHART : pediaMainScreen,
					PEDIA_BONUS : pediaMainScreen,
					PEDIA_IMPROVEMENT : pediaMainScreen,
					PEDIA_TERRAIN : pediaMainScreen,
					PEDIA_FEATURE : pediaMainScreen,
					PEDIA_PLOT_EFFECT : pediaMainScreen,
					PEDIA_CIVIC : pediaMainScreen,
					PEDIA_CIVILIZATION : pediaMainScreen,
					PEDIA_CITYCLASS : pediaMainScreen,
					PEDIA_ROUTE : pediaMainScreen,
					PEDIA_LEADER : pediaMainScreen,
					PEDIA_TRAIT : pediaMainScreen,
					PEDIA_SPAWNGROUP : pediaMainScreen,
					PEDIA_AFFINITY : pediaMainScreen,
					PEDIA_RELIGION : pediaMainScreen,
					PEDIA_CORPORATION : pediaMainScreen,
					PEDIA_LORE : pediaMainScreen,
					PEDIA_HISTORY : pediaMainScreen,
					WORLDBUILDER_SCREEN : worldBuilderScreen,

					DEBUG_INFO_SCREEN : debugInfoScreen,

				# add new screens here
					PEDIA_SPELL : pediaMainScreen,
					# < Unit Statistics Mod Start >
					CIVSELECT_SCREEN : CivSelectScreen,
					UNITSTATS_SCREEN: statisticsScreen,
					HIGHSCORES_SCREEN: statisticsScreen,
					PLAYERSTATS_SCREEN: statisticsScreen,
					GRAVEYARD_SCREEN: statisticsScreen,
					HALLOFFAME_SCREEN: statisticsScreen,
					TOP10_SCREEN1: statisticsScreen,
					TOP10_SCREEN2: statisticsScreen,
					# < Unit Statistics Mod End   >

					GUILD_SCREEN: guildScreen,
					# < Mercenaries Mod Start > 
					MERCENARY_MANAGER: mercenaryManager,
					# < Mercenaries Mod End   >
# DynTraits Start
					TRAITS_SCREEN: dynTraitsScreen,
# DynTraits End
				
### GameFont Display
					GAMEFONT_DISPLAY_SCREEN : GameFontDisplay.GameFontDisplay(),
### GameFont Display

## Platy World Builder ##
					WB_PLOT : WBPlotScreen.WBPlotScreen(),
					WB_EVENT: WBEventScreen.WBEventScreen(),
					WB_BUILDING : WBBuildingScreen.WBBuildingScreen(),
					WB_CITYDATA : WBCityDataScreen.WBCityDataScreen(),
					WB_CITYEDIT : WBCityEditScreen.WBCityEditScreen(worldBuilderScreen),
					WB_TECH : WBTechScreen.WBTechScreen(),
					WB_PROJECT : WBProjectScreen.WBProjectScreen(),
					WB_TEAM : WBTeamScreen.WBTeamScreen(),
					WB_PLAYER : WBPlayerScreen.WBPlayerScreen(),
					WB_UNIT : WBUnitScreen.WBUnitScreen(worldBuilderScreen),
					WB_PROMOTION : WBPromotionScreen.WBPromotionScreen(),
					WB_DIPLOMACY : WBDiplomacyScreen.WBDiplomacyScreen(),
					WB_GAMEDATA : WBGameDataScreen.WBGameDataScreen(worldBuilderScreen),
					WB_UNITLIST : WBPlayerUnits.WBPlayerUnits(),
					WB_RELIGION : WBReligionScreen.WBReligionScreen(),
					WB_CORPORATION : WBCorporationScreen.WBCorporationScreen(),
					WB_INFO : WBInfoScreen.WBInfoScreen(),
					WB_TRADE : WBTradeScreen.WBTradeScreen(),

					BOOTLEG_SO_SCREEN : bootlegSOScreen,

				}

#######################################################################################
## Handle Navigation Map
#######################################################################################
HandleNavigationMap = {
					PEDIA_MAIN : pediaMainScreen,
					PEDIA_TECH : pediaMainScreen,
					PEDIA_UNIT : pediaMainScreen,
					PEDIA_BUILDING : pediaMainScreen,
					PEDIA_PROMOTION : pediaMainScreen,
					PEDIA_PROJECT : pediaMainScreen,
					PEDIA_UNIT_CHART : pediaMainScreen,
					PEDIA_BONUS : pediaMainScreen,
					PEDIA_IMPROVEMENT : pediaMainScreen,
					PEDIA_TERRAIN : pediaMainScreen,
					PEDIA_FEATURE : pediaMainScreen,
					PEDIA_PLOT_EFFECT : pediaMainScreen,
					PEDIA_CIVIC : pediaMainScreen,
					PEDIA_CIVILIZATION : pediaMainScreen,
					PEDIA_CITYCLASS : pediaMainScreen,
					PEDIA_ROUTE : pediaMainScreen,
					PEDIA_LEADER : pediaMainScreen,
					PEDIA_TRAIT : pediaMainScreen,
					PEDIA_SPAWNGROUP : pediaMainScreen,
					PEDIA_AFFINITY : pediaMainScreen,
					PEDIA_LORE : pediaMainScreen,
					PEDIA_HISTORY : pediaMainScreen,
					PEDIA_RELIGION : pediaMainScreen,
					PEDIA_CORPORATION : pediaMainScreen,

				# add new screens here
					PEDIA_SPELL : pediaMainScreen
				}