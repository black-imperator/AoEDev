# Sid Meier's Civilization 4
# Copyright Firaxis Games 2006
#
# CvEventManager
# This class is passed an argsList from CvAppInterface.onEvent
# The argsList can contain anything from mouse location to key info
# The EVENTLIST that are being notified can be found

from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvDebugTools
import CvWBPopups
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import CvWorldBuilderScreen
import CvAdvisorUtils
import pickle
import CvIntroMovieScreen
import CustomFunctions
import ScenarioFunctions
import CvCorporationScreen
import GameFontDisplay
#FfH: Added by Kael 10/15/2008 for OOS Logging
import OOSLogger
#FfH: End Add
import Blizzards		#Added in Frozen: Blizzards: TC01
# Platy WB
import WBCityEditScreen
import WBUnitScreen
import WBPlayerScreen
import WBGameDataScreen
import WBPlotScreen
import CvPlatyBuilderScreen

## *******************
## Modular Python: ANW 16-feb-2010
##                     29-may-2010
##                     20-aug-2010
## ArcticNightWolf on CivFanatics
## ArcticNightWolf@gmail.com

# For dynamic plugin loading
import imp    # dynamic importing of libraries
#import glob   # Unix style pathname pattern expansion
import os     # Windows style pathname
import CvPath # path to current assets
import inspect

# Maps modules to the function name
# Syntax: {'functionName': [module1, module2]}
command = {}

# functionList is a list of strings of functions we will directly map
functionList = ['onMouseEvent', 'onKbdEvent', 'onModNetMessage', 'onInit', 'onUpdate', 'onUnInit', 'onSaveGame', 'onPreSave', 'onLoadGame', 'onBeginGameTurn',
 'onEndGameTurn', 'onBeginPlayerTurn', 'onEndPlayerTurn', 'onEndTurnReady', 'onCombatResult', 'onCombatLogCalc', 'onCombatLogHit',
 'onImprovementBuilt', 'onImprovementDestroyed', 'onRouteBuilt', 'onFirstContact', 'onCityBuilt', 'onCityRazed', 'onCityAcquired',
 'onCityAcquiredAndKept', 'onCityLost', 'onCultureExpansion', 'onCityGrowth', 'onCityDoTurn', 'onCityBuildingUnit', 'onCityBuildingBuilding',
 'onCityRename', 'onCityHurry', 'onSelectionGroupPushMission', 'onUnitMove', 'onUnitSetXY', 'onUnitCreated', 'onUnitBuilt', 'onUnitKilled',
 'onUnitLost', 'onUnitPromoted', 'onUnitSelected', 'onUnitRename', 'onUnitPillage', 'onUnitSpreadReligionAttempt', 'onUnitGifted',
 'onUnitBuildImprovement', 'onGoodyReceived', 'onGreatPersonBorn', 'onBuildingBuilt', 'onProjectBuilt', 'onTechAcquired', 'onTechSelected','onTraitGained','onTraitLost',
 'onReligionFounded', 'onReligionSpread', 'onReligionRemove', 'onCorporationFounded', 'onCorporationSpread', 'onCorporationRemove', 'onGoldenAge',
 'onEndGoldenAge', 'onChat', 'onVictory', 'onVassalState', 'onChangeWar', 'onSetPlayerAlive', 'onPlayerChangeStateReligion', 'onPlayerGoldTrade',
 'onWindowActivation', 'onGameUpdate', 'onGameStart', 'onGameEnd', 'onPlotRevealed', 'onPlotFeatureRemoved', 'onPlotPicked', 'onNukeExplosion', 'onGotoPlotSet']

## Modular Python End
## *******************

# globals
sf = ScenarioFunctions.ScenarioFunctions()

#FfH: Card Game: begin
cs = CvCorporationScreen.cs
#FfH: Card Game: end

Blizzards = Blizzards.Blizzards()		#Added in Frozen: Blizzards: TC01

#import GreyFoxCustom
import FoxDebug
import FoxTools
import time
from BasicFunctions import *
import SdToolKitAdvanced

FoxGlobals = {
	"USE_DEBUG_WINDOW" 		: False,
	"USE_AIAUTOPLAY_SOUND" 	: True,
}
SoundSettings = {
	"SOUND_MASTER_VOLUME" 	: 0,
	"SOUND_SPEECH_VOLUME" 	: 0,
	"SOUND_MASTER_NO_SOUND" : False,
}


	# Import from BugUtil.py

# Import/hack from BugUtil.py. Maybe should be moved to a dedicated util file, but eh
deferredCallQueue = []
def deferCall(function, delay=0.0):
	"""
	Calls the given function during a future gameUpdate event after at least <delay> seconds.
	"""
	CvUtil.pyPrint('defer call start')
	global deferredCallQueue
	if delay < 0.0:
		delay = 0.0
	when = time.clock() + delay
	entry = (when, function)
	if deferredCallQueue:
		for i in range(len(deferredCallQueue)):
			if when < deferredCallQueue[i][0]:
				deferredCallQueue.insert(i, entry)
				return
	deferredCallQueue.append(entry)

def doDeferredCalls(argsList=None):
	"""
	Calls deferred calls whose timers have expired.
	"""
	global deferredCallQueue
	if deferredCallQueue:
		# insert a marker so that items added during this round of calls will be processed on the next round
		deferCall(None)
		while deferredCallQueue:
			when, func = deferredCallQueue[0]
			if func is None:
				del deferredCallQueue[0]
				break
			if when > time.clock():
				for i, (when, func) in enumerate(deferredCallQueue):
					if func is None:
						del deferredCallQueue[i]
						break
				break
			del deferredCallQueue[0]
			func()
			CvUtil.pyPrint('defer call EXECUTE')

# globals
###################################################
class CvEventManager:
	def __init__(self):
		#################### ON EVENT MAP ######################
		#print "EVENTMANAGER INIT"
		self.bCtrl = False
		self.bShift = False
		self.bAlt = False
		self.bAllowCheats = False
		self.pluginScan()

		# Dictionaries
		self.Defines			= {}
		self.Eras				= {}
		self.Techs				= {}
		self.Victories			= {}
		self.GameSpeeds			= {}
		self.GameOptions		= {}
		self.EventTriggers		= {}

		# Civs, etc
		self.Civilizations		= {}
		self.Leaders 			= {}
		self.LeaderStatus		= {}
		self.Traits 			= {}
		self.Civics 			= {}
		self.Religions			= {}
		self.Corporations		= {}
		self.Alignments			= {}

		# Buildings, etc
		self.Projects 			= {}
		self.Buildings 			= {}
		self.Specialists		= {}
		self.BuildingClasses	= {}
		self.Processes			= {}

		# Improvements, etc
		self.Builds				= {}
		self.Lairs 				= {}
		self.ManaNodes			= {}
		self.Improvements 		= {}
		self.CivImprovements	= {}
		self.UniqueImprovements	= {}

		# Terrain, etc
		self.Mana	 			= {}
		self.Terrain 			= {}
		self.Feature 			= {}
		self.Resources 			= {}
		self.WorldSizes			= {}
		self.Goodies			= {}

		# Units, etc
		self.Units 				= {}
		self.Heroes				= {}
		self.UnitAI				= {}
		self.Promotions 		= {}
		self.UnitClasses		= {}
		self.UnitCombats 		= {}
		self.GreatPeople 		= {}
		self.DamageTypes		= {}

		self.cf					= None
		self.Tools 				= None
		self.DbgWnd				= None
		self.LoadedData			= False

		# OnEvent Enums
		self.EventLButtonDown=1
		self.EventLcButtonDblClick=2
		self.EventRButtonDown=3
		self.EventBack=4
		self.EventForward=5
		self.EventKeyDown=6
		self.EventKeyUp=7

		self.__LOG_MOVEMENT = 0
		self.__LOG_BUILDING = 0
		self.__LOG_COMBAT = 0
		self.__LOG_CONTACT = 0
		self.__LOG_IMPROVEMENT =0
		self.__LOG_CITYLOST = 0
		self.__LOG_CITYBUILDING = 0
		self.__LOG_TECH = 0
		self.__LOG_UNITBUILD = 0
		self.__LOG_UNITKILLED = 0
		self.__LOG_UNITLOST = 0
		self.__LOG_UNITPROMOTED = 0
		self.__LOG_UNITSELECTED = 0
		self.__LOG_UNITPILLAGE = 0
		self.__LOG_GOODYRECEIVED = 0
		self.__LOG_GREATPERSON = 0
		self.__LOG_RELIGION = 0
		self.__LOG_RELIGIONSPREAD = 0
		self.__LOG_GOLDENAGE = 0
		self.__LOG_ENDGOLDENAGE = 0
		self.__LOG_WARPEACE = 0
		self.__LOG_PUSH_MISSION = 0

		## EVENTLIST
		self.EventHandlerMap = {
			'mouseEvent'					: self.onMouseEvent,
			'kbdEvent' 						: self.onKbdEvent,
			'ModNetMessage'					: self.onModNetMessage,
			'Init'							: self.onInit,
			'Update'						: self.onUpdate,
			'UnInit'						: self.onUnInit,
			'OnSave'						: self.onSaveGame,
			'OnPreSave'						: self.onPreSave,
			'OnLoad'						: self.onLoadGame,
			'GameStart'						: self.onGameStart,
			'GameEnd'						: self.onGameEnd,
			'plotRevealed' 					: self.onPlotRevealed,
			'plotFeatureRemoved' 			: self.onPlotFeatureRemoved,
			'plotPicked'					: self.onPlotPicked,
			'nukeExplosion'					: self.onNukeExplosion,
			'gotoPlotSet'					: self.onGotoPlotSet,
			'BeginGameTurn'					: self.onBeginGameTurn,
			'EndGameTurn'					: self.onEndGameTurn,
			'BeginPlayerTurn'				: self.onBeginPlayerTurn,
			'EndPlayerTurn'					: self.onEndPlayerTurn,
			'endTurnReady'					: self.onEndTurnReady,
			'combatResult' 					: self.onCombatResult,
			'combatLogCalc'	 				: self.onCombatLogCalc,
			'combatLogHit'					: self.onCombatLogHit,
			'improvementBuilt' 				: self.onImprovementBuilt,
			'improvementDestroyed' 			: self.onImprovementDestroyed,
			'routeBuilt' 					: self.onRouteBuilt,
			'firstContact' 					: self.onFirstContact,
			'cityBuilt' 					: self.onCityBuilt,
			'cityRazed'						: self.onCityRazed,
			'cityAcquired' 					: self.onCityAcquired,
			'cityAcquiredAndKept' 			: self.onCityAcquiredAndKept,
			'cityLost'						: self.onCityLost,
			'cultureExpansion' 				: self.onCultureExpansion,
			'cityGrowth' 					: self.onCityGrowth,
			'cityDoTurn' 					: self.onCityDoTurn,
			'cityBuildingUnit'				: self.onCityBuildingUnit,
			'cityBuildingBuilding'			: self.onCityBuildingBuilding,
			'cityRename'					: self.onCityRename,
			'cityHurry'						: self.onCityHurry,
			'selectionGroupPushMission'		: self.onSelectionGroupPushMission,
			'unitMove' 						: self.onUnitMove,
			'unitSetXY' 					: self.onUnitSetXY,
			'unitCreated' 					: self.onUnitCreated,
			'unitBuilt' 					: self.onUnitBuilt,
			'unitKilled'					: self.onUnitKilled,
			'unitLost'						: self.onUnitLost,
			'unitPromoted'					: self.onUnitPromoted,
			'unitSelected'					: self.onUnitSelected,
			'UnitRename'					: self.onUnitRename,
			'unitPillage'					: self.onUnitPillage,
			'unitSpreadReligionAttempt'		: self.onUnitSpreadReligionAttempt,
			'unitGifted'					: self.onUnitGifted,
			'unitBuildImprovement'			: self.onUnitBuildImprovement,
			'goodyReceived'					: self.onGoodyReceived,
			'greatPersonBorn'	  			: self.onGreatPersonBorn,
			'buildingBuilt' 				: self.onBuildingBuilt,
			'projectBuilt' 					: self.onProjectBuilt,
			'techAcquired'					: self.onTechAcquired,
			'techSelected'					: self.onTechSelected,
			'traitGained'					: self.onTraitGained,
			'traitLost'						: self.onTraitLost,
			'religionFounded'				: self.onReligionFounded,
			'religionSpread'				: self.onReligionSpread,
			'religionRemove'				: self.onReligionRemove,
			'corporationFounded'			: self.onCorporationFounded,
			'corporationSpread'				: self.onCorporationSpread,
			'corporationRemove'				: self.onCorporationRemove,
			'goldenAge'						: self.onGoldenAge,
			'endGoldenAge'					: self.onEndGoldenAge,
			'chat' 							: self.onChat,
			'victory'						: self.onVictory,
			'vassalState'					: self.onVassalState,
			'changeWar'						: self.onChangeWar,
			'setPlayerAlive'				: self.onSetPlayerAlive,
			'playerChangeStateReligion'		: self.onPlayerChangeStateReligion,
			'playerGoldTrade'				: self.onPlayerGoldTrade,
			'windowActivation'				: self.onWindowActivation,
			'gameUpdate'					: self.onGameUpdate,		# sample generic event
			'combatHit'					: '', #These are used by UnitStatistics.
			'airIntercept'					: '',
			'combatBegin'					: '',
			'combatWithdrawal'					: '',
			'airStrikeHit'					: '',
			'unitUpgraded'					: '',
			'spellCast'					: '',
			'unitConverted'					: '',
			'combatHit'					: '',
		}

		################## Events List ###############################
		#
		# Dictionary of Events, indexed by EventID (also used at popup context id)
		#   entries have name, beginFunction, applyFunction [, randomization weight...]
		#
		# Normal events first, random events after
		#
		################## Events List ###############################
		self.Events={
			CvUtil.EventEditCityName : ('EditCityName', self.__eventEditCityNameApply, self.__eventEditCityNameBegin),
			CvUtil.EventEditCity : ('EditCity', self.__eventEditCityApply, self.__eventEditCityBegin),
			CvUtil.EventPlaceObject : ('PlaceObject', self.__eventPlaceObjectApply, self.__eventPlaceObjectBegin),
			CvUtil.EventAwardTechsAndGold: ('AwardTechsAndGold', self.__eventAwardTechsAndGoldApply, self.__eventAwardTechsAndGoldBegin),
			CvUtil.EventEditUnitName : ('EditUnitName', self.__eventEditUnitNameApply, self.__eventEditUnitNameBegin),
			CvUtil.EventWBAllPlotsPopup : ('WBAllPlotsPopup', self.__eventWBAllPlotsPopupApply, self.__eventWBAllPlotsPopupBegin),
			CvUtil.EventWBLandmarkPopup : ('WBLandmarkPopup', self.__eventWBLandmarkPopupApply, self.__eventWBLandmarkPopupBegin),
			CvUtil.EventWBScriptPopup : ('WBScriptPopup', self.__eventWBScriptPopupApply, self.__eventWBScriptPopupBegin),
			CvUtil.EventWBStartYearPopup : ('WBStartYearPopup', self.__eventWBStartYearPopupApply, self.__eventWBStartYearPopupBegin),
			CvUtil.EventShowWonder: ('ShowWonder', self.__eventShowWonderApply, self.__eventShowWonderBegin),
			CvUtil.EventSetTurnsAutoPlayPopup : ('SetTurnsAutoPlayPopup', self.__eventSetTurnsAutoPlayApply, self.__eventSetTurnsAutoPlayBegin),
			CvUtil.EventSetUnitPerTilePopup : ('SetUnitPerTilePopup', self.__eventSetUnitPerTileApply, self.__eventSetUnitPerTileBegin),
			CvUtil.EventCheat: ('TriggerRandEvent', self.__eventCheatEventApply, self.__eventCheatEventBegin),
		
## Platy Builder ##
			CvUtil.EventWBLandmarkPopup : ('WBLandmarkPopup', self.__eventWBLandmarkPopupApply, self.__eventWBScriptPopupBegin),
			CvUtil.EventShowWonder: ('ShowWonder', self.__eventShowWonderApply, self.__eventShowWonderBegin),
			1111 : ('WBPlayerScript', self.__eventWBPlayerScriptPopupApply, self.__eventWBScriptPopupBegin),
			2222 : ('WBCityScript', self.__eventWBCityScriptPopupApply, self.__eventWBScriptPopupBegin),
			3333 : ('WBUnitScript', self.__eventWBUnitScriptPopupApply, self.__eventWBScriptPopupBegin),
			4444 : ('WBGameScript', self.__eventWBGameScriptPopupApply, self.__eventWBScriptPopupBegin),
			5555 : ('WBPlotScript', self.__eventWBPlotScriptPopupApply, self.__eventWBScriptPopupBegin),
## Platy Builder ##
			CvUtil.EventReminder : ('Reminder', self.__eventReminderApply, self.__eventReminderBegin),
		}
## FfH Card Game: begin
		self.Events[CvUtil.EventSelectSolmniumPlayer] = ('selectSolmniumPlayer', self.__EventSelectSolmniumPlayerApply, self.__EventSelectSolmniumPlayerBegin)
		self.Events[CvUtil.EventSolmniumAcceptGame] = ('solmniumAcceptGame', self.__EventSolmniumAcceptGameApply, self.__EventSolmniumAcceptGameBegin)
		self.Events[CvUtil.EventSolmniumConcedeGame] = ('solmniumConcedeGame', self.__EventSolmniumConcedeGameApply, self.__EventSolmniumConcedeGameBegin)
## FfH Card Game: end

		self.reminders = []

#################### EVENT STARTERS ######################
	def handleEvent(self, argsList):
		'EventMgr entry point'
		# extract the last 6 args in the list, the first arg has already been consumed
		self.origArgsList = argsList	# point to original
		tag = argsList[0]				# event type string
		idx = len(argsList)-6
		bDummy = False
		self.bDbg, bDummy, self.bAlt, self.bCtrl, self.bShift, self.bAllowCheats = argsList[idx:]
		ret = 0
		if self.EventHandlerMap.has_key(tag):
			fxn = self.EventHandlerMap[tag]
			ret = fxn(argsList[1:idx])
		return ret

#################### EVENT APPLY ######################
	def beginEvent( self, context, argsList=-1 ):
		'Begin Event'
		entry = self.Events[context]
		return entry[2]( argsList )

	def applyEvent( self, argsList ):
		'Apply the effects of an event '
		context, playerID, netUserData, popupReturn = argsList

		if context == CvUtil.PopupTypeEffectViewer:
			return CvDebugTools.g_CvDebugTools.applyEffectViewer( playerID, netUserData, popupReturn )

		entry = self.Events[context]

		if ( context not in CvUtil.SilentEvents ):
			self.reportEvent(entry, context, (playerID, netUserData, popupReturn) )
		return entry[1]( playerID, netUserData, popupReturn )   # the apply function

	def reportEvent(self, entry, context, argsList):
		'Report an Event to Events.log '
		if (CyGame().getActivePlayer() != -1):
			message = "DEBUG Event: %s (%s)" %(entry[0], CyGlobalContext().getActivePlayer().getName())
			CyInterface().addImmediateMessage(message,"")
			CvUtil.pyPrint(message)
		return 0

################# MODULAR PYTHON HANDLER ############
## Modular Python: ANW 16-feb-2010
##                     29-may-2010
##                     20-aug-2010
##                     02-sep-2010

	def pluginScan(self):
		#print ("PluginScan called")
		for function in functionList:
			command[function] = []

		# Load modules
		MLFlist = []
		MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\NormalModules\\")
		MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FirstLoad\\")
		MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\SecondLoad\\")
		MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\ThirdLoad\\")
		MLFlist.append(CvPath.assetsPath[2] + "\\Modules\\LoadOrderVitalModules\\FourthLoad\\")

		print "Module List:"
		for pathToMLF in MLFlist:
			for modules in os.listdir(pathToMLF):
				pathToModuleRoot = pathToMLF+modules+"\\"
				# Ignore all xml files
				if modules.lower()[-4:] != ".xml":
					print "%s" % (modules)
					# Check whether path exists // whether current directory isn't actually a file
					if os.path.exists(pathToModuleRoot):
						# Check whether python folder is present
						if "python" in os.listdir(pathToModuleRoot):
							pathToModulePython = pathToModuleRoot+"python\\"
							# For every file in that folder
							for pythonFileSourceName in os.listdir(pathToModulePython):
								pythonFileSource = pathToModulePython+pythonFileSourceName
								# Is it non-python file ?
								if (pythonFileSource.lower()[-3:] != ".py"):
									continue
								# Is it spell file ?
								if pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ].upper()[0:5] == "SPELL":
									continue
								# Is it event file ?
								if pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ].upper()[0:5] == "EVENT":
									continue
								tempFileName = file(pythonFileSource)
								tempModuleName = pythonFileSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ -1 ]
								module = imp.load_module( tempModuleName, tempFileName, tempModuleName+".py", ("","",1))
								# List all the functions the plugin has.
								functs = inspect.getmembers(module, inspect.isfunction)
								#each function is returned as a tuple (or maybe a list) 0, being the name, and 1 being the function itself
								for tuple in functs:
									for possFuncts in functionList:
										#since we only need the name of the function to match up, we only use the name in [0]
										if tuple[0] == possFuncts:
											#add it to our list of the applicable functions.
											command[possFuncts].append(module)
								tempFileName.close()

## Modular Python end
#################### ON EVENTS ######################
	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'

		eventType,key,mx,my,px,py = argsList
		game 		= CyGame()
		map 		= CyMap()
		cf			= self.cf

		if (self.bAllowCheats):
			# notify debug tools of input to allow it to override the control
			argsList = (eventType,key,self.bCtrl,self.bShift,self.bAlt,mx,my,px,py,game.isNetworkMultiPlayer())
			if ( CvDebugTools.g_CvDebugTools.notifyInput(argsList) ):
				return 0

		if ( eventType == self.EventKeyDown ):
			theKey=int(key)
						
### GameFont Display
			if theKey == int(InputTypes.KB_F1) and self.bShift and self.bCtrl:
				GameFontDisplay.GameFontDisplay().interfaceScreen()
				return 1
### GameFont Display

#FfH: Added by Kael 07/05/2008
			if (theKey == int(InputTypes.KB_LEFT)):
				if self.bCtrl:
						CyCamera().SetBaseTurn(CyCamera().GetBaseTurn() - 45.0)
						return 1
				elif self.bShift:
						CyCamera().SetBaseTurn(CyCamera().GetBaseTurn() - 10.0)
						return 1

			if (theKey == int(InputTypes.KB_RIGHT)):
					if self.bCtrl:
							CyCamera().SetBaseTurn(CyCamera().GetBaseTurn() + 45.0)
							return 1
					elif self.bShift:
							CyCamera().SetBaseTurn(CyCamera().GetBaseTurn() + 10.0)
							return 1
#FfH: End Add
			if (self.bAllowCheats):
				# Shift E (Debug - Trigger an Event)
				if (theKey== int(InputTypes.KB_E)):
					if(self.bShift):
						CvDebugTools.CvDebugTools().cheatEvents2()
						return 1

			if (self.bAllowCheats):
				# Shift Y (Debug - Remove AI Units)
				if (theKey== int(InputTypes.KB_Y)):
					if(self.bShift):
						CvDebugTools.CvDebugTools().debugRemoveAIUnits()
						return 1

			CvCameraControls.g_CameraControls.handleInput( theKey )

			if (self.bAllowCheats):
				# Shift - T (Debug - No MP)
				if (theKey == int(InputTypes.KB_T)):
					if ( self.bShift ):
						self.beginEvent(CvUtil.EventAwardTechsAndGold)
						#self.beginEvent(CvUtil.EventCameraControlPopup)
						return 1

				elif (theKey == int(InputTypes.KB_W)):
					if ( self.bShift and self.bCtrl):
						self.beginEvent(CvUtil.EventShowWonder)
						return 1

				# Shift - ] (Debug - currently mouse-overd unit, health += 10
				elif (theKey == int(InputTypes.KB_LBRACKET) and self.bShift ):
					unit = map.plot(px, py).getUnit(0)
					if ( not unit.isNone() ):
						d = min( unit.maxHitPoints()-1, unit.getDamage() + 10 )
						unit.setDamage( d, PlayerTypes.NO_PLAYER )

				# Shift - [ (Debug - currently mouse-overd unit, health -= 10
				elif (theKey == int(InputTypes.KB_RBRACKET) and self.bShift ):
					unit = map.plot(px, py).getUnit(0)
					if ( not unit.isNone() ):
						d = max( 0, unit.getDamage() - 10 )
						unit.setDamage( d, PlayerTypes.NO_PLAYER )

				elif (theKey == int(InputTypes.KB_F1)):
					if ( self.bShift ):
						CvScreensInterface.replayScreen.showScreen(False)
						return 1
					# don't return 1 unless you want the input consumed

				elif (theKey == int(InputTypes.KB_F2)):
					if ( self.bShift ):
						import CvDebugInfoScreen
						CvScreensInterface.showDebugInfoScreen()
						return 1

				elif (theKey == int(InputTypes.KB_F3)):
					if ( self.bShift ):
						CvScreensInterface.showDanQuayleScreen(())
						return 1

				elif (theKey == int(InputTypes.KB_F4)):
					if ( self.bShift ):
						CvScreensInterface.showUnVictoryScreen(())
						return 1


			if (self.bAllowCheats or game.isMPOption(MultiplayerOptionTypes.MPOPTION_ENABLE_AUTOPLAY)):
				if (theKey == int(InputTypes.KB_X) and self.bShift and self.bCtrl):
					CyMessageControl().sendModNetMessage(CvUtil.AutoPlay, 1, -1, -1, -1)
				elif (theKey == int(InputTypes.KB_Z) and self.bShift and self.bCtrl):
					if game.getAIAutoPlay() > 0:
						CyMessageControl().sendModNetMessage(CvUtil.AutoPlay, 0, -1, -1, -1)
					else:
						cf.showAutoPlayPopup()

			if (theKey == int(InputTypes.KB_U) and self.bShift):
				if (not game.isUPTLock() or self.bAllowCheats):
					cf.showUnitPerTilePopup()

			# Alt+R creates a reminder
			if (theKey == int(InputTypes.KB_R) and self.bAlt and self.bShift):
				self.beginEvent(CvUtil.EventReminder)
				return 1

			if theKey == int(InputTypes.KB_X) and self.bAlt:
				CvScreensInterface.showBootlegSO()
				return 1

			if theKey == int(InputTypes.KB_X) and self.bShift:
				CvScreensInterface.changeBootlegSORadius()
				return 1

			if theKey == int(InputTypes.KB_X) and self.bCtrl:
				CvScreensInterface.changeBootlegSODraw()
				return 1

# Grey Fox Speed Tweaks: START
			if ( self.bShift ):
				if (theKey == int(InputTypes.KB_C)):
					if FoxGlobals["USE_DEBUG_WINDOW"]:
						self.DbgWnd.updateDebugPanel()
						
# END

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onKbdEvent']:
			module.onKbdEvent(self, argsList)

		## Modular Python End
		## *******************

		return 0
		
		
	def __eventCheatEventApply(self, playerID, netUserData, popupReturn):
		'Cheat Event Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyCheatEvent( (popupReturn) )
			
			
	def onModNetMessage(self, argsList):
		'Called whenever CyMessageControl().sendModNetMessage() is called - this is all for you modders!'
		gc = CyGlobalContext()
		cf = self.cf
		game = CyGame()
		iData1, iData2, iData3, iData4, iData5 = argsList

#FfH Card Game: begin
#		print("Modder's net message!")
#		CvUtil.pyPrint( 'onModNetMessage' )
		if iData1 == CvUtil.Somnium : # iData1 == 0 : Somnium message, iData2 = function, iData3 to iData5 = parameters
			if iData2 == 0:
				if (iData3 == game.getActivePlayer()):
					self.__EventSelectSolmniumPlayerBegin()
			elif iData2 == 1:
				if (iData4 == game.getActivePlayer()):
					self.__EventSolmniumConcedeGameBegin((iData3, iData4))
			else :
				cs.applyAction(iData2, iData3, iData4, iData5)
# FfH Card Game: end
		elif iData1 == CvUtil.CivSelector:  #iData1==1 : CivSelect message,  iData2 = iCiv, iData3 = bAIPlayable, iData4 = bPlayable
			gc.getCivilizationInfo(iData2).setAIPlayable(iData3)
			gc.getCivilizationInfo(iData2).setPlayable(iData4)

		elif iData1 == CvUtil.AutoPlay:	#iData1 == 2: AutoPlay Config, iData2 = SetTurns
			game.setAIAutoPlay(iData2)

		elif iData1 == CvUtil.UPT: #iData1 == 3: UPT Config, iData2 = SetUPT, iData3 = bLock
			game.setUPT(iData2)
			if (iData3):
				game.setUPTLock(True)

		elif iData1 == CvUtil.reassignPlayer:
						game.reassignPlayerAdvanced(iData2, iData3, -1)

		elif iData1 == 100:
			iButtonId		= iData2
			iPlayer			= iData3
			gc				= CyGlobalContext()
			git				= gc.getInfoTypeForString
			pPlayer			= gc.getPlayer(iPlayer)
			# List should be the same as lTraits in CvEventManager, onBeginPlayerTurn, Trait Adaptive part.
			lDirtyTraits = [git("TRAIT_AGGRESSIVE"),git("TRAIT_ARCANE"),git("TRAIT_CHARISMATIC"),git("TRAIT_CREATIVE"),git("TRAIT_EXPANSIVE"),git("TRAIT_FINANCIAL"),git("TRAIT_INDUSTRIOUS"),git("TRAIT_ORGANIZED"),git("TRAIT_PHILOSOPHICAL"),git("TRAIT_RAIDERS"),git("TRAIT_SPIRITUAL")]
			lTraits = []
			for i in lDirtyTraits:
				if not pPlayer.hasTrait(i):
					lTraits.append(i)
			iTrait = lTraits[iButtonId]
			if not gc.isNoCrash():
				pPlayer.setHasTrait((iTrait),True,-1,True,True)
			else:
				pPlayer.setHasTrait((iTrait),True)

		elif iData1 == 101:
			iButtonId	= iData2
			iPlayer		= iData3
			iElection	= iData4
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
			iRepublicTrait = lRepublicTraits[iElectionIndex]
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
						loopCity.changeEspionageHealthCounter(-5)
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

		elif iData1 == 102:
			iPlayer = iData2
			pPlayer = gc.getPlayer(iPlayer)
			git				= gc.getInfoTypeForString
			pBestPlot = -1
			iBestPlot = -1
			for i in range (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				iPlot = -1
				if not pPlot.isWater():
					if pPlot.getNumUnits() == 0:
						if not pPlot.isCity():
							if not pPlot.isImpassable():
								iPlot = CyGame().getSorenRandNum(1000, "Add Unit")
								if pPlot.area().getNumTiles() < 8:
									iPlot += 1000
								if not pPlot.isOwned():
									iPlot += 1000
								if iPlot > iBestPlot:
									iBestPlot = iPlot
									pBestPlot = pPlot
			if iBestPlot != -1:
				containerUnit = -1
				for i in range(pBestPlot.getNumUnits()):
					if pBestPlot.getUnit(i).getUnitType() == git('EQUIPMENT_CONTAINER'):
						containerUnit = pBestPlot.getUnit(i)
				if containerUnit == -1:
					containerUnit = gc.getPlayer(gc.getORC_PLAYER()).initUnit(git('EQUIPMENT_CONTAINER'), pBestPlot.getX(), pBestPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				containerUnit.setHasPromotion(git('PROMOTION_GODSLAYER'), True)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_TREASURE",()),'',1,'Art/Interface/Buttons/Equipment/Treasure.dds',ColorTypes(8),containerUnit.getX(),containerUnit.getY(),True,True)
				iTeam = pPlayer.getTeam()
				signText = CvUtil.convertToStr(CyTranslator().getText("TXT_KEY_EQUIPMENT_GODSLAYER", ()))
				pBestPlot.setRevealed(iTeam, True, False, TeamTypes.NO_TEAM)
				CyCamera().JustLookAtPlot(pBestPlot)
				CyEngine().addSign(pBestPlot, iPlayer, signText)

		elif iData1 == 103:
			iButtonId		= iData2
			iPlayer			= iData3
			gc				= CyGlobalContext()
			git				= gc.getInfoTypeForString
			cf				= CustomFunctions.CustomFunctions()
			pPlayer = gc.getPlayer(iPlayer)
			lDemonLordsList= [git("LEADER_HYBOREM")]
			lDemonLordsTraitList=["TRAIT_PACT_HYBOREM"]
			if (git("MODULE_IMPORTANT_LEADERS")!=-1):
				lDemonLordsList=lDemonLordsList+[git("LEADER_MERESIN"),git("LEADER_OUZZA"),git("LEADER_STATIUS"),git("LEADER_SALLOS"),git("LEADER_LETHE"),git("LEADER_JUDECCA")]
				lDemonLordsTraitList=lDemonLordsTraitList+["TRAIT_PACT_MERESIN","TRAIT_PACT_OUZZA","TRAIT_PACT_STATIUS","TRAIT_PACT_SALLOS","TRAIT_PACT_LETHE","TRAIT_PACT_JUDECCA"]
					
			lDemonLordsToSpawn = []
			lDemonLordsTraitToSpawn = []
			for iDemonLord in range(len(lDemonLordsList)):
				if not CyGame().isLeaderEverActive(lDemonLordsList[iDemonLord]):
					lDemonLordsToSpawn.append(lDemonLordsList[iDemonLord])
					lDemonLordsTraitToSpawn.append(lDemonLordsTraitList[iDemonLord])
			iCounter	= 0
			iCounterTrait=0
			iLeader		= -1
			bSwap		= False
			for i in lDemonLordsToSpawn:
				if iButtonId == iCounter:
					iLeader = i
					cf.spawnDemonLord(iLeader,iPlayer)
					pPlayer.setHasTrait(git(lDemonLordsTraitToSpawn[iCounterTrait]),True)
					return
				else:
					iCounter += 1
				if iButtonId == iCounter:
					iLeader = i
					cf.spawnDemonLord(iLeader,iPlayer,True)
					pPlayer.setHasTrait(git(lDemonLordsTraitToSpawn[iCounterTrait]),True)
					return
				else:
					iCounter += 1
				iCounterTrait+=1
		elif iData1 == 104:
			iButtonId	= iData2
			iPlayer		= iData3
			pPlayer		= gc.getPlayer(iPlayer)
			iCity		= iButtonId + 1
			pCity		= cf.getAshenVeilCity(iCity)
			pPlayer.acquireCity(pCity,False,False)

		elif iData1 == 105:
			iButtonId	= iData2
			iPlayer		= iData3
			pPlayer		= gc.getPlayer(iPlayer)
			git			= gc.getInfoTypeForString
			pCapital	= pPlayer.getCapitalCity()
			if iButtonId == 0:
				pPlayer.setFeatAccomplished(FeatTypes.FEAT_VISIT_MIRROR_OF_HEAVEN, False)
				return
			if iButtonId == 1:
				newUnit = pPlayer.initUnit(git('UNIT_LIGHTBRINGER'), pCapital.getX(), pCapital.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setName(CyTranslator().getText("TXT_KEY_EVENT_MALAKIM_MIRROR_2_HERMIT_NAME",()))
				newUnit.setHasPromotion(git('PROMOTION_HERO'), True)
				newUnit.setHasPromotion(git('PROMOTION_MOBILITY1'), True)
			if iButtonId == 2:
				pCapital.setNumRealBuilding(git('BUILDING_MALAKIM_TEMPLE_MIRROR'), 1)

		elif iData1 == 106:
			iButtonId	= iData2
			iCaster		= iData3
			iPlayer		= iData4
			pPlayer		= gc.getPlayer(iPlayer)
			pCaster		= pPlayer.getUnit(iCaster)
			pPlot		= pCaster.plot()
			git			= gc.getInfoTypeForString
			if iButtonId == 2:
				gc.getGame().setGlobalFlag(git("FLAG_FOXFORD_FIRST_TIME"),False)
				return
			iRnd		= CyGame().getSorenRandNum(100, "Foxford General Roll")
			if iButtonId == 0:
				pCaster.setHasPromotion(git('PROMOTION_ADVENTURER'), True)
				pCaster.changeExperienceTimes100(500, -1, False, False, False)
				iGold = 20 + CyGame().getSorenRandNum(10, "Foxford Gold Roll")
				pPlayer.changeGold(iGold)
				if iRnd < 15:
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_FOXFORD_WOLFKILLED", ()),'',3,'Art/Interface/Buttons/Promotions/Werewolf.dds',git("COLOR_RED"),pPlot.getX(),pPlot.getY(),True,True)
					pCaster.kill(False,-1)
				return
			if iButtonId == 1:
				pCaster.setHasPromotion(git('PROMOTION_WEREWOLF'), True)
				CyGame().setPlotExtraYield (pPlot.getX(),pPlot.getY(), git("YIELD_COMMERCE"), -3)
				pPlayer.setHasFlag(git("FLAG_FOXFORD_RAZED"),True)
				CyEngine().removeLandmark(pPlot)
				if iRnd < 33:
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_FOXFORD_LYNCHED", ()),'',3,'Art/Interface/Buttons/Actions/Pillage.dds',git("COLOR_RED"),pPlot.getX(),pPlot.getY(),True,True)
					pCaster.kill(False,-1)

		elif iData1 == 107:
			iButtonId	= iData2
			iUnit		= iData3
			iPlayer		= iData4
			pUnit		= gc.getPlayer(iPlayer).getUnit(iUnit)
			if iButtonId == 0:
				iBestValue = 0
				pBestPlot = -1
				for i in xrange (CyMap().numPlots()):
					iValue = 0
					pPlot = CyMap().plotByIndex(i)
					if not pPlot.isWater() and not pPlot.isPeak() and pPlot.getNumUnits() == 0:
						iValue = CyGame().getSorenRandNum(1000, "Portal")
						if not pPlot.isOwned():
							iValue += 1000
						if iValue > iBestValue:
							iBestValue = iValue
							pBestPlot = pPlot
				if pBestPlot != -1:
					pUnit.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True,False)
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_PORTAL",()),'',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pBestPlot.getX(),pBestPlot.getY(),True,True)

		elif iData1 == 108:
			iButtonId		= iData2
			iUnit			= iData3
			iPlayer			= iData4
			pType			= iData5
			git				= gc.getInfoTypeForString
			pPlayer			= gc.getPlayer(iPlayer)
			pUnit			= pPlayer.getUnit(iUnit)
			pPlot			= pUnit.plot()
			pNewPlot		= findClearPlot(-1, pPlot)
			bPlayer			= gc.getPlayer(gc.getORC_PLAYER())
			pPlayer1		= bPlayer
			pPlayer2		= bPlayer
			iCount1			= 3
			iCount2			= 3
			pPlot1			= pNewPlot
			pPlot2			= pNewPlot
			bBronze			= False
			bPoison			= False
			if pType == 1:		# DwarfVsLizard
				pUnitType1	= git("UNIT_AXEMAN")
				pUnitType2	= git("UNIT_LIZARDMAN")
			elif pType == 2:	# RedVsYellow
				pUnitType1	= git("UNIT_ARCHER_SCORPION_CLAN")
				pUnitType2	= git("UNIT_GOBLIN_MURIS_CLAN")
			if bPlayer.isHasTech(git('TECH_BRONZE_WORKING')):
				bBronze = True
			if bPlayer.isHasTech(git('TECH_HUNTING')):
				bPoison = True
			if iButtonId == 0:
				pPlayer1	= pPlayer
				iCount1		= 2
				pPlot1		= pPlot
			elif iButtonId == 1:
				pPlayer2	= pPlayer
				iCount2		= 2
				pPlot2		= pPlot
			if pNewPlot != -1:
				for i in xrange(iCount1):
					newUnitFirst = pPlayer1.initUnit(pUnitType1, pPlot1.getX(), pPlot1.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					if pType == 1:
						newUnitFirst.setHasPromotion(git('PROMOTION_DWARF'), True)
						if bBronze == True:
							newUnitFirst.setHasPromotion(git('PROMOTION_BRONZE_WEAPONS'), True)
					elif bPoison == True and pType == 2:
						newUnitFirst.setHasPromotion(git('PROMOTION_POISONED_WEAPON'), True) # Poisoned Blade switched for Poisoned Weapon
				for j in xrange(iCount2):
					newUnitSecond = pPlayer2.initUnit(pUnitType2, pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					if bPoison == True:
						newUnitSecond.setHasPromotion(git('PROMOTION_POISONED_BLADE'), True)

		elif iData1 == 109:
			iButtonId	= iData2
			iUnit		= iData3
			iPlayer		= iData4
			pPlayer		= gc.getPlayer(iPlayer)
			pUnit		= pPlayer.getUnit(iUnit)
			git			= gc.getInfoTypeForString
			if iButtonId == 0:
				possibleGoodies = []
				iRnd = CyGame().getSorenRandNum(2, "Lair Depth, Roll Class")
				if iRnd == 0:
					eGoodyClass = git("GOODYCLASS_GENERIC_MODERATE")
				else:
					eGoodyClass = git("GOODYCLASS_GENERIC_MAJOR")
				for i in xrange(gc.getNumGoodyInfos()):
					if gc.getGoodyInfo(i).isGoodyClassType(eGoodyClass):
						if (pPlayer.canReceiveGoody(pUnit.plot(), i, pUnit)):
							possibleGoodies.append(i)
				if possibleGoodies:
					eGoody = possibleGoodies[CyGame().getSorenRandNum(len(possibleGoodies), "Lair Depth, Roll Goody")]
					pPlayer.receiveGoody(pUnit.plot(), eGoody, pUnit)

		elif iData1 == 110:
			iButtonId	= iData2
			iPlayer		= iData3
			pPlayer		= gc.getPlayer(iPlayer)
			iChange = 0
			if iButtonId == 2:
				return
			if iButtonId == 0:
				iChange	= -5
			if iButtonId == 1:
				iChange = 5
			pPlayer.changeGlobalCounterContrib(iChange)
			CyGame().changeGlobalCounter(iChange)

		elif iData1 == 111:
			iButtonId	= iData2
			iPlayer		= iData3
			pPlayer		= gc.getPlayer(iPlayer)
			git			= gc.getInfoTypeForString
			bOption2	= False
			pCapital	= pPlayer.getCapitalCity()
			lReqBonus = [git("BONUS_COW"),git("BONUS_DEER"),git("BONUS_PIG"),git("BONUS_DEER_ARCTIC"),git("BONUS_BANANA"),git("BONUS_RICE"),git("BONUS_WHEAT"),git("BONUS_WINE"),git("BONUS_CORN")]
			for i in range (CyMap().numPlots()):
				iPlot = CyMap().plotByIndex(i)
				if iPlot.getBonusType(-1) in lReqBonus and iPlot.getOwner() == iPlayer:
					bOption2 = True
			if pPlayer.getGold() < 350 and iButtonId >= 0: # I don't know how else to simulate option shift caused by reqs in popup
				iButtonId += 1
			if bOption2 != True and iButtonId >= 1: # Option shift
				iButtonId += 1
			if pPlayer.getCivilizationType() != git("CIVILIZATION_KURIOTATES") or pCapital == -1 or pCapital.isNone(): # Option shift
				if iButtonId >= 2:
					iButtonId += 1
			if iButtonId == 3:
				return
			if iButtonId == 0:
				pPlayer.changeGold(-350)
			if iButtonId == 1:
				iRemovedBonus = 0
				for i in range (CyMap().numPlots()):
					if iRemovedBonus == 0:
						iPlot = CyMap().plotByIndex(i)
						if iPlot.getBonusType(-1) in lReqBonus and iPlot.getOwner() == iPlayer:
							iPlot.setBonusType(-1)
							iRemovedBonus += 1
			if iButtonId == 2:
				pCapital = pPlayer.getCapitalCity()
				pCapital.changePopulation(1)
			pPlayer.setHasFlag(git('FLAG_DEAL_WITH_CENTAURS_TRIBE'), True)
			# TODO Remove comment when setFreePromotion is exposed to python
			# pPlayer.setFreePromotion(git("UNITCOMBAT_MOUNTED"),git("PROMOTION_SHOCK"),true)

		elif iData1 == 112:
			iButtonId	= iData2
			iPlayer		= iData3
			iUnit		= iData4
			pPlayer		= gc.getPlayer(iPlayer)
			pUnit		= pPlayer.getUnit(iUnit)
			git			= gc.getInfoTypeForString
			pPlot		= pUnit.plot()
			if pPlayer.getCivilizationType() != git('CIVILIZATION_MAZATL') and pPlayer.getCivilizationType() !=  git('CIVILIZATION_CUALLI') and iButtonId >= 2: # I don't know how else to simulate option shift caused by reqs in popup
				iButtonId += 1
			if iButtonId == 3:
				return
			iGold = 250 + CyGame().getSorenRandNum(100, "CityOfGold Gold")
			if iButtonId == 2:
				pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())
				pPlayer.changeGold(iGold)
				return
			if iButtonId == 0:
				pPlayer.changeGold(iGold)
			iRnd = CyGame().getSorenRandNum(100, "CityOfGold Guards")
			if iButtonId == 1 or iRnd < 34: # Spawn Guards
				pOrcPlayer	= gc.getPlayer(gc.getORC_PLAYER())
				pNewPlot	= findClearPlot(-1, pPlot)
				newUnit1		= pOrcPlayer.initUnit(git('UNIT_LIZARD_PRIEST_OF_AGRUONN'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
				newUnit1.setHasPromotion(git('PROMOTION_COMBAT1'),True)
				newUnit1.setHasPromotion(git('PROMOTION_COMBAT2'),True)
				newUnit2		= pOrcPlayer.initUnit(git('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
				newUnit2.setHasPromotion(git('PROMOTION_COMBAT1'),True)
				newUnit3		= pOrcPlayer.initUnit(git('UNIT_LIZARD_BLOWPIPE'), pNewPlot.getX(), pNewPlot.getY(), UnitAITypes.UNITAI_EXPLORE, DirectionTypes.DIRECTION_SOUTH)
				newUnit3.setHasPromotion(git('PROMOTION_COMBAT1'),True)
				if iButtonId == 1:
					pUnit.changeImmobileTimer(3)
					pUnit.setHasPromotion(git('PROMOTION_PILLAGED_GOLD'),True)

		elif iData1 == 113:
			iButtonId		= iData2
			iData1			= iData3
			iData2			= iData4
			gc				= CyGlobalContext()
			git				= gc.getInfoTypeForString
			pPlayer			= gc.getPlayer(iData2)
			pCaster			= pPlayer.getUnit(iData1)
			pPlot			= pCaster.plot()
			iPlayer			= gc.getGame().getActivePlayer()
			listCommander	= []
			pCommander		= -1
			for i in range(pPlot.getNumUnits()): # forming the list identical to findCommanderHuman
				pUnit = pPlot.getUnit(i)
				if pUnit.getOwner() == pCaster.getOwner():
					if not pUnit.getID() == pCaster.getID():	
						if pCaster.getDomainType() == pUnit.getDomainType():
							bvalid=True
							pLoopCommander=pUnit.getCommanderUnit()
							while( not pLoopCommander.isNone()):
								if (pLoopCommander.getID()==pCaster.getID()):
									bvalid=False
									break
								pLoopCommander=pLoopCommander.getCommanderUnit()
							if (not bvalid):
								continue
							if not pUnit.getID() == pCaster.getCommanderUnit().getID() and not pUnit.getCommanderUnit().getID() == pCaster.getID():
								if pUnit.getNumMinions() < pUnit.getCommandLimit():
									if pCaster.getUnitClassType() == git("UNITCLASS_SLUGA") or pCaster.getUnitClassType() == git("UNITCLASS_BATTLE_SLUGA") or pCaster.getUnitClassType() == git("UNITCLASS_WAR_SLUGA") or pCaster.getUnitClassType() == git("UNITCLASS_BEHEMOTH_SLUGA"):
										if pUnit.getUnitClassType() == git("UNITCLASS_OVERSEER") or pUnit.getUnitClassType() == git("UNITCLASS_COMBAT_OVERSEER") or pUnit.getUnitClassType() == git("UNITCLASS_SLUGA_COMMANDER") or pUnit.getUnitClassType() == git("UNITCLASS_KARAS"):
											listCommander.append(pUnit)
									else:
										iMinionRank = 0
										if pCaster.isHasPromotion(git('PROMOTION_GENERAL')):
											iMinionRank = 5
										elif pCaster.isHasPromotion(git('PROMOTION_CAPTAIN')):
											iMinionRank = 4
										elif pCaster.isHasPromotion(git('PROMOTION_MASTER_SEARGENT')):
											iMinionRank = 3
										elif pCaster.isHasPromotion(git('PROMOTION_SEARGENT')):
											iMinionRank = 2
										elif pCaster.isHasPromotion(git('PROMOTION_CORPORAL')):
											iMinionRank = 1
										elif pCaster.getCommandLimit() > 0:
											iMinionRank = 6
										iCommanderRank = 6
										if pUnit.isHasPromotion(git('PROMOTION_GENERAL')):
											iCommanderRank = 5
										elif pUnit.isHasPromotion(git('PROMOTION_CAPTAIN')):
											iCommanderRank = 4
										elif pUnit.isHasPromotion(git('PROMOTION_MASTER_SEARGENT')):
											iCommanderRank = 3
										elif pUnit.isHasPromotion(git('PROMOTION_SEARGENT')):
											iCommanderRank = 2
										elif pUnit.isHasPromotion(git('PROMOTION_CORPORAL')):
											iCommanderRank = 1
										if iCommanderRank > iMinionRank:
											listCommander.append(pUnit)
			if iButtonId != 0:
				pCommander = listCommander[iButtonId-1] # First button is used to cancel action
			if pCommander != -1:
				pCommander.addMinion(pCaster)
				pCaster.DeselectUnit()
				pCaster.SelectUnit()

		elif iData1 == 114:
			iButtonId		= iData2
			iPlayer			= iData3
			gc				= CyGlobalContext()
			pPlayer			= gc.getPlayer(iPlayer)
			git				= gc.getInfoTypeForString
			lTribeLeaders	= [git("LEADER_SHIMASANI"),git("LEADER_SOYALA"),git("LEADER_MOTSQUEH"),git("LEADER_OSYKA"),git("LEADER_ALOSAKA")]
			lLeaderText		= ["TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SHIMASANI_WINS","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SOYALA_WINS","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_MOTSQUEH_WINS","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_OSYKA_WINS","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_ALOSAKA_WINS"]
			lAltPassText	= ["TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SHIMASANI_WINS_ALREADY_SHIMASANI_SUCCESS","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SOYALA_WINS_ALREADY_SOYALA_SUCCESS","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_MOTSQUEH_WINS_ALREADY_MOTSQUEH_SUCCESS","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_OSYKA_WINS_ALREADY_OSYKA_SUCCESS","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_ALOSAKA_WINS_ALREADY_ALOSAKA_SUCCESS"]
			lAltFailText	= ["TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SHIMASANI_WINS_ALREADY_SHIMASANI_FAIL","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SOYALA_WINS_ALREADY_SOYALA_FAIL","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_MOTSQUEH_WINS_ALREADY_MOTSQUEH_FAIL","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_OSYKA_WINS_ALREADY_OSYKA_FAIL","TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_ALOSAKA_WINS_ALREADY_ALOSAKA_FAIL"]
			bAnarchy		= True
			iLeader			= iButtonId
			iRnd			= CyGame().getSorenRandNum(100, "TribalLaw, Bonus")
			if iButtonId == 5:										# Fair, No Anarchy, Happy city timer
				bAnarchy = False
				iHappyTurns = 1
				pPlayer.changeCivCounter(1)
				if pPlayer.getCivCounter() == 3:
					pPlayer.setCivCounter(0)
					iHappyTurns = 6
				(loopCity, iter) = pPlayer.firstCity(False)
				while(loopCity):
					loopCity.changeHappinessTimer(iHappyTurns)
					(loopCity, iter) = pPlayer.nextCity(iter, False)
				iLeader = CyGame().getSorenRandNum(len(lTribeLeaders), "TribalLaw, Fair Pick")
			else:
				pPlayer.setCivCounter(0)
			if iButtonId == 6:										# No Elections
				pPlayer.changeAnarchyTurns(1)
				return
			if bAnarchy == True and iLeader != 0:					# Anarchy Check
				pPlayer.changeAnarchyTurns(1)
			if pPlayer.getLeaderType() != lTribeLeaders[iLeader]:	# Leader Change
				pPlayer.changeLeader(lTribeLeaders[iLeader])
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(lLeaderText[iLeader], ()),'',3,'art/Modules/ChislevExpansion/Buttons/Tribal_Law_Button.dds',git("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			elif iRnd < 50:											# Same Leader, Failed 50/50, no Bonus
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(lAltFailText[iLeader], ()),'',3,'art/Modules/ChislevExpansion/Buttons/Tribal_Law_Button.dds',git("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
			elif iRnd >= 50:										# Same Leader, Passed 50/50, do Bonus
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(lAltPassText[iLeader], ()),'',3,'art/Modules/ChislevExpansion/Buttons/Tribal_Law_Button.dds',git("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
				if iLeader == 0: # Eagle
					for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
						loopPlayer = gc.getPlayer(iLoopPlayer)
						if loopPlayer.isAlive():
							if loopPlayer.getTeam() != pPlayer.getTeam():
								loopPlayer.AI_changeAttitudeExtra(iPlayer, 3)
								pPlayer.AI_changeAttitudeExtra(iLoopPlayer, 3)
				elif iLeader == 1: # Coyote
					pPlayer.initUnit(git('UNIT_ARTIST'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				elif iLeader == 2: # Bear
					pPlayer.initUnit(git('UNIT_ENGINEER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				elif iLeader == 3: # Serpent
					pPlayer.initUnit(git('UNIT_COMMANDER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				elif iLeader == 4: # Tortoise
					pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())

		elif iData1 == 115:
			iButtonId		= iData2
			iPlayer			= iData3
			pPlayer			= CyGlobalContext().getPlayer(iPlayer)
			lLeaders		= [CyGlobalContext().getInfoTypeForString("LEADER_CHISLEV"),CyGlobalContext().getInfoTypeForString("LEADER_NATANE")]
			pPlayer.changeLeader(lLeaders[iButtonId])

		elif iData1 == 116:
			iButtonId		= iData2
			iUnitID			= iData3
			iPlayer			= iData4
			pUnit			= CyGlobalContext().getPlayer(iPlayer).getUnit(iUnitID)
			git				= CyGlobalContext().getInfoTypeForString
			lPromotion1		= [git("PROMOTION_MENAWA_EAGLE_TRIBE"),git("PROMOTION_MENAWA_COYOTE_TRIBE"),git("PROMOTION_MENAWA_BEAR_TRIBE"),git("PROMOTION_MENAWA_SERPENT_TRIBE"),git("PROMOTION_MENAWA_TORTOISE_TRIBE")]
			lPromotion2		= [git("PROMOTION_MOBILITY1"),git("PROMOTION_DRILL1"),git("PROMOTION_COMBAT1"),git("PROMOTION_CITY_RAIDER1"),git("PROMOTION_CITY_GARRISON1")]
			lPromotion3		= [git("PROMOTION_MOBILITY2"),git("PROMOTION_DRILL2"),git("PROMOTION_COMBAT2"),git("PROMOTION_CITY_RAIDER2"),git("PROMOTION_CITY_GARRISON2")]
			pUnit.setHasPromotion(lPromotion1[iButtonId],True)
			if pUnit.isHasPromotion(lPromotion2[iButtonId]):
				pUnit.setHasPromotion(lPromotion3[iButtonId],True)
			pUnit.setHasPromotion(lPromotion2[iButtonId],True)

		elif iData1 == 117:
			iButtonId		= iData2
			iCaster			= iData3
			iPlayer			= iData4
			git				= gc.getInfoTypeForString
			pPlayer			= gc.getPlayer(iPlayer)
			pCaster			= pPlayer.getUnit(iCaster)
			pPlot			= pCaster.plot()
			lSpell			= [[git("SPELL_SUMMON_FROSTLING_WARRIOR_GREATOR"),git("SPELL_SUMMON_FROSTLING_ARCHER_GREATOR")],[git("SPELL_SUMMON_WINTER_WOLF_GREATOR")],[git("SPELL_SUMMON_KOCRACHON_GREATOR")],[git("SPELL_SUMMON_ICE_ELEMENTAL_GREATOR")],[git("SPELL_SUMMON_AQUILAN_GREATOR")],[git("SPELL_SUMMON_FROST_GIANT_GREATER")]]
			for iSpell in lSpell[iButtonId]:
				pCaster.cast(iSpell)

		elif iData1 == 118:
			iButtonId		= iData2
			iUnit			= iData3
			iPlayer			= iData4
			git				= gc.getInfoTypeForString
			pPlayer			= gc.getPlayer(iPlayer)
			pUnit			= pPlayer.getUnit(iUnit)
			if iButtonId == 1:
				return
			pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
			CyGame().changeGlobalCounter(-10)
			pPlayer.changeGlobalCounterContrib(-10)
			newUnit = pPlayer.initUnit(git('UNIT_ANGEL'), pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.setHasPromotion(git('PROMOTION_HERO'), True)
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_BASIUM_GELA",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Units/Basium.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer	= gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.getCivilizationType() == git('CIVILIZATION_MERCURIANS'):
					pLoopPlayer.AI_changeAttitudeExtra(3,1)

		elif iData1 == 119:
			iButtonId		= iData2
			iUnit			= iData3
			iPlayer			= iData4
			iImprovement	= iData5
			git				= gc.getInfoTypeForString
			pPlayer			= gc.getPlayer(iPlayer)
			pUnit			= pPlayer.getUnit(iUnit)
			pPlot			= pUnit.plot()
			if iButtonId == 1:
				return
			if iImprovement == git("IMPROVEMENT_BROKEN_SEPULCHER"):
				pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
				for iCity in xrange(pPlayer.getNumCities()):
					pCity = pPlayer.getCity(iCity)
					if CyGame().getSorenRandNum(100,"effect Gela, Broken Sepulcher") <= 60:
						newUnit = pPlayer.initUnit(git('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					if pCity.getPopulation() > 2:
						pCity.changePopulation(-2)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_GELA_BROKEN",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/brokensepulcher.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
			elif iImprovement == git("IMPROVEMENT_MIRROR_OF_HEAVEN"):
				pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
				pUnit.setHasPromotion(git('PROMOTION_TEMP_HELD'), True)
				pUnit.setHasPromotion(git('PROMOTION_SOL'), True)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_GELA_MIRROR",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/mirrorofheaven.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
				pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
				for iPlayer2 in range(gc.getMAX_PLAYERS()):
					pPlayer2 = gc.getPlayer(iPlayer2)
					if (pPlayer2.isAlive()):
						if pPlayer2.getCivilizationType() == git('CIVILIZATION_INFERNAL'):
							pDemonPlayer = pPlayer2
							enemyTeam = pDemonPlayer.getTeam()
							pTeam = gc.getTeam(pPlayer.getTeam())
							pTeam.declareWar(enemyTeam, True, WarPlanTypes.WARPLAN_TOTAL)
				for iiX in range(pUnit.getX()-2, pUnit.getX()+3, 1):
					for iiY in range(pUnit.getY()-2, pUnit.getY()+3, 1):
						pPlot2 = CyMap().plot(iiX,iiY)
						if not pPlot2.isWater() and not pPlot2.isCity() and pPlot2.getNumUnits() == 0 and pPlot2.isFlatlands():
							if CyGame().getSorenRandNum(500, "effect Gela, Hellfire") <= 400:
								iImprovement = pPlot2.getImprovementType()
								bValid = True
								if iImprovement != -1 :
									if gc.getImprovementInfo(iImprovement).isPermanent():
										bValid = False
								if bValid :
									pPlot2.setImprovementType(git('IMPROVEMENT_HELLFIRE'))
									newUnit = pDemonPlayer.initUnit(git('UNIT_SECT_OF_FLIES'), pPlot2.getX(), pPlot2.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
									newUnit.setHasPromotion(git('PROMOTION_DEMON'), True)
			elif iImprovement == git("IMPROVEMENT_POOL_OF_TEARS"):
				pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
				pUnit.setHasPromotion(git('PROMOTION_PIKE_OF_TEARS'), True)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/pooloftears.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
				iRnd = CyGame().getSorenRandNum(100, "effect Gela, Pool of Tears, Plague") <= 20
				if iRnd <= 20 or (pPlayer.getStateReligion() != git('RELIGION_FELLOWSHIP_OF_LEAVES') and iRnd <= 50):
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA_PLAGUE",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/pooloftears.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
					for iPlayer2 in range(gc.getMAX_PLAYERS()):
						pPlayer2 = gc.getPlayer(iPlayer2)
						if pPlayer2.getCivilizationType() != git('CIVILIZATION_INFERNAL'):
							for iCity in xrange(pPlayer2.getNumCities()):
								pCity = pPlayer.getCity(iCity)
								i = CyGame().getSorenRandNum(5, "Blight")
								i += pCity.getPopulation() - 2
								i -= pCity.totalGoodBuildingHealth()
								pCity.changeEspionageHealthCounter(i)
							for iUnit in xrange(pPlayer2.getNumUnits()):
								pUnit2 = pPlayer.getUnit(iUnit)
								pUnit2.doDamageNoCaster(40, 100, git('DAMAGE_DEATH'), False)
			elif iImprovement == git("IMPROVEMENT_PYRE_OF_THE_SERAPHIC"):
				pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
				pPlot.setImprovementType(-1)
				if CyGame().getSorenRandNum(100,"effect Gela, Pyre") <= 40:
					pUnit.setHasPromotion(git('PROMOTION_FROZEN_FLAME'), True)
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA_PYRE_1",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/pyreoftheseraphic.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
				else:
					mapSize = CyMap().getWorldSize()
					# i from 1 (duel) to 9 (huger)
					i = 1 + mapSize + int(mapSize/5) + int(mapSize/6)
					addBonus('BONUS_MANA',i,'Art/Interface/Buttons/WorldBuilder/mana_button.dds')
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TEARS_GELA_PYRE_2",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/pyreoftheseraphic.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
			elif iImprovement == git("IMPROVEMENT_MAELSTROM"):
				pUnit.setHasPromotion(git('PROMOTION_GELA'), False)
				pUnit.kill(True, PlayerTypes.NO_PLAYER)
				if  pPlayer.getStateReligion() == git('RELIGION_OCTOPUS_OVERLORDS'):
					newUnit1 = pPlayer.initUnit(git('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit1.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
					newUnit2 = pPlayer.initUnit(git('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit2.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
					newUnit3 = pPlayer.initUnit(git('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit3.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
					newUnit4 = pPlayer.initUnit(git('UNIT_STYGIAN_GUARD'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit4.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
					newUnit5 = pPlayer.initUnit(git('UNIT_DISCIPLE_OCTOPUS_OVERLORDS'), pUnit.getX()+1, pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit5.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
					newUnit5.setHasPromotion(git('PROMOTION_HERO'), True)
					CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_GELA_1",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
				else:
					iStygianChance = 300
					pDemonPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
					for i in range (CyMap().numPlots()):
						pPlot = CyMap().plotByIndex(i)
						if pPlot.isWater() and pPlot.getNumUnits() == 0:
							if CyGame().getSorenRandNum(10000, "effect Gela, Stygian") <= iStygianChance:
								newUnit = pDemonPlayer.initUnit(git('UNIT_STYGIAN_GUARD'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.setUnitAIType(git('UNITAI_ANIMAL'))
								newUnit.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
							elif CyGame().getSorenRandNum(10000, "effect Gela, SeaSerpent") <= iStygianChance:
								newUnit = pDemonPlayer.initUnit(git('UNIT_SEA_SERPENT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.setUnitAIType(git('UNITAI_ANIMAL'))
								newUnit.setHasPromotion(git('PROMOTION_WATER_WALKING'), True)
					CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_GELA_2",()),'AS2D_FEATUREGROWTH',3,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)

		elif iData1 == 120:
			iButtonId		= iData2
			iPlayer			= iData3
			iUnit			= iData4
			git				= gc.getInfoTypeForString
			pPlayer			= gc.getPlayer(iPlayer)
			pUnit			= pPlayer.getUnit(iUnit)
			pPlot			= pUnit.plot()
			iRnd			= CyGame().getSorenRandNum(100,"OrphanedGoblin effect")
			if iButtonId == 0:
				pUnit.setHasPromotion(git('PROMOTION_ORC_SLAYING'), True)
				pUnit.setHasPromotion(git('PROMOTION_CRAZED'), True)
				pPlayer.changeBroadAlignment(-5)
			elif iButtonId == 1:
				pUnit.setHasPromotion(git('PROMOTION_GOBLIN'), True)
			elif iButtonId == 2:
				pNewPlot = findClearPlot(-1, pPlot)
				if pNewPlot != -1:
					if iRnd < 50:
						pGoblinPlayer = gc.getPlayer(gc.getORC_PLAYER())
					else:
						pGoblinPlayer = pPlayer
					newUnit = pGoblinPlayer.initUnit(git('UNIT_GOBLIN'), pNewPlot.getX(),pNewPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					newUnit.setHasPromotion(git('PROMOTION_WEAK'), True)
			else:
				pUnit.changeExperience(-1,-1,False,False,False)
				newUnit = pPlayer.initUnit(git('UNIT_GOBLIN'), pPlot.getX(),pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		elif iData1 == 121:
			gc = CyGlobalContext()
			val_answer = iData2
			iCity = iData3
			iOwner = iData4
			pPlayer = gc.getPlayer(iOwner)
			pCity = pPlayer.getCity(iCity)
			pPlot = pCity.plot()
			if val_answer == 0:
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_NIGHTMARE'))
			if val_answer == 1:
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_ASH'))

		elif iData1 == 122:
			gc = CyGlobalContext()
			val_answer = iData2
			iCity = iData3
			iOwner = iData4
			pPlayer = gc.getPlayer(iOwner)
			if val_answer == 1:
				pCity = pPlayer.getCity(iCity)
				pPlot = pCity.plot()
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_ASH'))

		elif iData1 == 123: # Take Equipment
			iButtonId		= iData2
			iCaster			= iData3
			iPlayer			= iData4
			cf				= CustomFunctions.CustomFunctions()
			pPlayer			= gc.getPlayer(iPlayer)
			pCaster			= pPlayer.getUnit(iCaster)
			pPlot			= pCaster.plot()
			lEquipmentList	= []
			if iButtonId == 0:	# Cancel
				return
			for iUnit in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(iUnit)
				if pUnit.isCommunalProperty():
					for iPromotion in xrange(gc.getNumPromotionInfos()):
						if pUnit.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
							if not pCaster.isHasPromotion(iPromotion):
								if not iPromotion in lEquipmentList:
									if cf.canRemoveEquipment(-1,pCaster,iPromotion) == True:
										lEquipmentList.append(iPromotion)
			iEquipment		= lEquipmentList[iButtonId - 1] 
			for iUnit in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(iUnit)
				if pUnit.isCommunalProperty() and pUnit.isHasPromotion(iEquipment):
					pUnit.setHasPromotion(iEquipment, False)
					pCaster.setHasPromotion(iEquipment, True)

		elif iData1 == 124: # Drop Equipment
			iButtonId		= iData2
			iCaster			= iData3
			iPlayer			= iData4
			cf				= CustomFunctions.CustomFunctions()
			git				= gc.getInfoTypeForString
			pPlayer			= gc.getPlayer(iPlayer)
			pCaster			= pPlayer.getUnit(iCaster)
			pPlot			= pCaster.plot()
			lEquipmentList	= []
			containerUnit = -1
			if iButtonId == 0: # Cancel
				return
			for iUnit in xrange(pPlot.getNumUnits()):
				if pPlot.getUnit(iUnit).getUnitType() == git('EQUIPMENT_CONTAINER'):
					containerUnit = pPlot.getUnit(iUnit)
			if containerUnit == -1:
				containerUnit = gc.getPlayer(gc.getORC_PLAYER()).initUnit(git('EQUIPMENT_CONTAINER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			for iPromotion in xrange(gc.getNumPromotionInfos()):
				if pCaster.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
					if cf.canRemoveEquipment(pCaster,-1,iPromotion) == True:
						lEquipmentList.append(iPromotion)
			if iButtonId == 1: # All
				for iPromotion in lEquipmentList:
					containerUnit.setHasPromotion(iPromotion,True)
					pCaster.setHasPromotion(iPromotion,False)
			elif iButtonId > 1:
				containerUnit.setHasPromotion(lEquipmentList[iButtonId - 2],True)
				pCaster.setHasPromotion(lEquipmentList[iButtonId - 2],False)

		elif iData1 == 125: # Swap Equipment
			iButtonId		= iData2
			iCaster			= iData3
			iPlayer			= iData4
			cf				= CustomFunctions.CustomFunctions()
			pPlayer			= gc.getPlayer(iPlayer)
			pCaster			= pPlayer.getUnit(iCaster)
			pPlot			= pCaster.plot()
			lEquipmentUnitPairs = []
			if iButtonId == 0: # Cancel
				return
			for iUnit in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(iUnit)
				if not pUnit.isCommunalProperty() and pUnit.getOwner() == iPlayer:
					for iPromotion in xrange(gc.getNumPromotionInfos()):
						if pUnit.isHasPromotion(iPromotion) and gc.getPromotionInfo(iPromotion).isEquipment():
							if not pCaster.isHasPromotion(iPromotion):
								if cf.canRemoveEquipment(pUnit,pCaster,iPromotion) == True:
									lPair = [iPromotion,pUnit]
									lEquipmentUnitPairs.append(lPair)
			lPair		= lEquipmentUnitPairs[iButtonId - 1]
			iPromotion	= lPair[0]
			pHolder		= lPair[1]
			pCaster.setHasPromotion(iPromotion,True)
			pHolder.setHasPromotion(iPromotion,False)

		elif iData1 == 20 : # Goblin CityClass Choice iData1=20, iData2=CityID, iData3=CityClassId, iData4=PlayerId
			pPlayer = gc.getPlayer(iData4)
			pCity = pPlayer.getCity(iData2)
			pCity.setCityClass(iData3)
		elif iData1 == 21 : # Kurio Settlement choice iData1=21, iData2=CityID, iData3 = 1(True) or 0(False) , iData4=PlayerId
			pPlayer = gc.getPlayer(iData4)
			pCity = pPlayer.getCity(iData2)
			if(iData3==1):
				pCity.setSettlement(True)
			else:
				pCity.setSettlement(False)
		elif iData1==22 : # Important Trait choice  iData1=22 , iData2=TraitId, iData3= 1(True) or 0(False), iData4=PlayerId
			pPlayer = gc.getPlayer(iData4)
			if (iData3==1):
				pPlayer.setHasTrait(iData2,True)
				pPlayer.initValidTraitTriggers()
				pPlayer.setGainingTrait(False)
			else:
				pPlayer.setTraitPoints(iData2,0)
				pPlayer.setGainingTrait(False)
		elif iData1 == 5001 or iData1 == 5002: # Commerce Change from MainInterface
			iPlayer		= iData2
			iChange		= iData3
			iCommerce	= CommerceTypes(iData4)
			pPlayer = gc.getPlayer(iPlayer)
			if iData1 == 5001:
				pPlayer.changeCommercePercent(iCommerce, iChange)
			else:
				pPlayer.changeCommercePercent(iCommerce, - min(iChange, pPlayer.getCommercePercent(iCommerce)))

		## *******************
		## Modular Python: ANW 29-may-2010
		for module in command['onModNetMessage']:
			module.onModNetMessage(self, argsList)

		## Modular Python End
		## *******************

	def onInit(self, argsList):
		'Called when Civ starts up'
		CvUtil.pyPrint( 'OnInit' )

		## *******************
		## Modular Python: ANW 29-may-2010

		self.pluginScan()

		## Modular Python End
		## *******************

	def onUpdate(self, argsList):
		'Called every frame'
		fDeltaTime = argsList[0]

		# allow camera to be updated
		CvCameraControls.g_CameraControls.onUpdate( fDeltaTime )

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUpdate']:
			module.onUpdate(self, argsList)

		## Modular Python End
		## *******************

	def onWindowActivation(self, argsList):
		'Called when the game window activates or deactivates'
		bActive = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onWindowActivation']:
			module.onWindowActivation(self, argsList)

		## Modular Python End
		## *******************

	def onUnInit(self, argsList):
		'Called when Civ shuts down'
		CvUtil.pyPrint('OnUnInit')

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnInit']:
			module.onUnInit(self, argsList)

		## Modular Python End
		## *******************

	def onPreSave(self, argsList):
		"called before a game is actually saved"
		CvUtil.pyPrint('OnPreSave')

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onPreSave']:
			module.onPreSave(self, argsList)

		## Modular Python End
		## *******************

		if self.DbgWnd != None:
			CyGame().setScriptData(pickle.dumps(self.DbgWnd.saveData()))

	def onSaveGame(self, argsList):
		"return the string to be saved - Must be a string"

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onSaveGame']:
			module.onSaveGame(self, argsList)

		## Modular Python End
		## *******************

		return ""

	def verifyLoaded(self, bLoad = False):
		if self.LoadedData == False:
			self.loadData(bLoad)

	def loadData(self, bLoad = False):
		' Loading data and initializing variables '
		self.Tools 			= FoxTools.FoxTools()
		self.Tools.initialize()

		self.Defines			= self.Tools.getDefineDict()
		self.Eras				= self.Tools.getEraDict()
		self.Techs				= self.Tools.getTechDict()
		self.Victories			= self.Tools.getVictoryDict()
		self.GameSpeeds			= self.Tools.getGameSpeedDict()
		self.GameOptions		= self.Tools.getGameOptionDict()
		self.EventTriggers		= self.Tools.getEventTriggerDict()

		self.Civilizations		= self.Tools.getCivilizationDict()
		self.Leaders			= self.Tools.getLeaderDict()
		self.LeaderStatus		= self.Tools.getLeaderStatusDict()
		self.Traits				= self.Tools.getTraitDict()
		self.Civics				= self.Tools.getCivicDict()
		self.Religions			= self.Tools.getReligionDict()
		self.Corporations		= self.Tools.getCorporationDict()
		self.Alignments			= self.Tools.getAlignmentDict()

		self.Projects			= self.Tools.getProjectDict()
		self.Buildings			= self.Tools.getBuildingDict()
		self.Specialists		= self.Tools.getSpecialistDict()
		self.BuildingClasses	= self.Tools.getBuildingClassDict()
		self.Processes			= self.Tools.getProcessesDict()

		self.Resources			= self.Tools.getResourcesDict()
		self.WorldSizes			= self.Tools.getWorldSizesDict()
		self.Terrain			= self.Tools.getTerrainDict()
		self.Feature			= self.Tools.getFeatureDict()
		self.Mana				= self.Tools.getManaDict()
		self.Goodies			= self.Tools.getGoodyDict()

		self.Builds				= self.Tools.getBuildDict()
		self.Lairs				= self.Tools.getLairDict()
		self.ManaNodes			= self.Tools.getManaNodeDict()
		self.Improvements		= self.Tools.getImprovementDict()
		self.CivImprovements	= self.Tools.getCivImprovementDict()
		self.UniqueImprovements	= self.Tools.getUniqueImprovementDict()

		self.Units				= self.Tools.getUnitDict()
		self.Heroes				= self.Tools.getHeroesDict()
		self.UnitAI				= self.Tools.getUnitAIDict()
		self.UnitClasses		= self.Tools.getUnitClassDict()
		self.UnitCombats		= self.Tools.getUnitCombatDict()
		self.GreatPeople		= self.Tools.getGreatPeopleDict()
		self.Promotions			= self.Tools.getPromotionDict()
		self.DamageTypes		= self.Tools.getDamageTypesDict()

		self.cf					= CustomFunctions.CustomFunctions()
		self.cf.initialize()

		if bLoad:
			if FoxGlobals["USE_DEBUG_WINDOW"]:
				self.DbgWnd 		= FoxDebug.FoxDebug()
				self.DbgWnd.loadData(pickle.loads(CyGame().getScriptData()))

		self.LoadedData = True

	def onLoadGame(self, argsList):
		CvAdvisorUtils.resetNoLiberateCities()
		self.verifyLoaded(True)
		gc = CyGlobalContext()
		# Reminders
		self.reminders = []
		if not gc.getGame().isGameMultiPlayer():
			lReminders = SdToolKitAdvanced.sdGetGlobal("reminders","list")
			if lReminders:
				self.reminders = lReminders

		CyGame().setAIAutoPlay(0)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onLoadGame']:
			module.onLoadGame(self, argsList)

		## Modular Python End
		## *******************

		return 0

	def onGameStart(self, argsList):
		'Called at the start of the game'
		# Loading Debug data and Initializing dictionaries
		self.verifyLoaded()
		gc	= CyGlobalContext()
		cf	= self.cf

		if CyGame().getWBMapScript():
			sf.gameStart()
		else:
			introMovie = CvIntroMovieScreen.CvIntroMovieScreen()
			introMovie.interfaceScreen()

		cf.doAoEGameStart()

		if (CyGame().getGameTurnYear() == self.Defines["Start Year"] and not self.GameOptions["Advanced Start"]):
			if not CyGame().getWBMapScript():
				for iPlayer in xrange(gc.getMAX_PLAYERS()):
					player = gc.getPlayer(iPlayer)
					if (player.isAlive() and player.isHuman()):
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
						popupInfo.setText(u"showDawnOfMan")
						popupInfo.addPopup(iPlayer)
		else:
			CyInterface().setSoundSelectionReady(True)

		if CyGame().isPbem():
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iPlayer)
				if (player.isAlive() and player.isHuman()):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_DETAILS)
					popupInfo.setOption1(True)
					popupInfo.addPopup(iPlayer)

		CvAdvisorUtils.resetNoLiberateCities()

		# Reminders
		self.reminders = []

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onGameStart']:
			module.onGameStart(self, argsList)

		## Modular Python End
		## *******************

# FF: Added by Jean Elcard 14/01/2009 (speed tweak)
		rebuildGraphics()
# FF: End Add

	def onGameEnd(self, argsList):
		'Called at the End of the game'
		print("Game is ending")

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onGameEnd']:
			module.onGameEnd(self, argsList)

		## Modular Python End
		## *******************

		return

	def onBeginGameTurn(self, argsList):
		'Called at the beginning of the end of each turn'
		iGameTurn = argsList[0]
		cf	= self.cf

		cs.doTurn()
		cf.doFFTurn(iGameTurn)
		if CyGame().getWBMapScript():
			sf.doTurn()

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onBeginGameTurn']:
			module.onBeginGameTurn(self, argsList)

		## Modular Python End
		## *******************

#Added in Frozen: TC01 (Blizzard Utils)
		Blizzards.doBlizzardTurn()
#End of Frozen

		if CyGame().getAIAutoPlay() == 0:
			CvTopCivs.CvTopCivs().turnChecker(iGameTurn)

	def onEndGameTurn(self, argsList):
		'Called at the end of the end of each turn'
		iGameTurn = argsList[0]

		gc			= CyGlobalContext()
		iDemonTeam	= gc.getDEMON_TEAM()

# FF: Added by Jean Elcard 14/01/2009 (speed tweak)
		rebuildGraphics()
# FF: End Add

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onEndGameTurn']:
			module.onEndGameTurn(self, argsList)

		## Modular Python End
		## *******************


		if CyGame().isVictoryValid(self.Victories["Gone to Hell"]):
			iTotalTiles = CyMap().numPlots()
			iEvilTiles = 0

			for iLoop in xrange(CyMap().getNumAreas()):
				iEvilTiles += CyMap().getArea(iLoop).getNumEvilTiles()


			if (100.0 * iEvilTiles) / iTotalTiles > self.Defines["Gone to Hell"]:

				pMostEvilPlayer = -1
				iMostEvilTotalContrib = 0

				for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if not pLoopPlayer.isAlive():										continue
					if pLoopPlayer.getGlobalCounterContrib() <= iMostEvilTotalContrib:	continue
					pMostEvilPlayer			= pLoopPlayer
					iMostEvilTotalContrib	= pLoopPlayer.getGlobalCounterContrib()

				if pMostEvilPlayer != -1:
					pMostEvilPlayer.setTeam(iDemonTeam)

				CyGame().setWinner(iDemonTeam, self.Victories["Gone to Hell"])

		if FoxGlobals["USE_AIAUTOPLAY_SOUND"]:
			if CyGame().getAIAutoPlay() == 1:
				pCapital = gc.getPlayer(0).getCapitalCity().plot()
				if pCapital != None :
					CyCamera().JustLookAtPlot(pCapital)
					point 			= pCapital.getPoint()
					profile			= CyUserProfile()
					Play3DSound		= CyAudioGame().Play3DSound
					profile.setMasterNoSound(False)
					profile.setMasterVolume(50)
					profile.setSpeechVolume(50)
					Play3DSound("AS3D_ENGLAND_SELECT",point.x,point.y,point.z)
					profile.setMasterVolume(SoundSettings["SOUND_MASTER_VOLUME"])
					profile.setSpeechVolume(SoundSettings["SOUND_SPEECH_VOLUME"])
					profile.setMasterNoSound(SoundSettings["SOUND_MASTER_NO_SOUND"])

	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer	= argsList
		gc					= CyGlobalContext()
		cf					= self.cf
		pPlayer				= gc.getPlayer(iPlayer)
		bAI					= self.Tools.isAI(iPlayer)
		eCiv				= pPlayer.getCivilizationType()

		print ("GameTurn: "+str(iGameTurn))

		if bAI and not CyGame().getWBMapScript():			cf.warScript(iPlayer)
		if pPlayer.isCivic(self.Civics["Crusade"]):			cf.doCrusade(iPlayer)
		if pPlayer.isCivic(self.Civics["Republic"]):		cf.doRepublic(iPlayer, iGameTurn)

		if   eCiv == self.Civilizations["Khazad"]:			cf.doTurnKhazad(iPlayer)
		elif eCiv == self.Civilizations["Luchuirp"]:		cf.doTurnLuchuirp(iPlayer)
		elif eCiv == self.Civilizations["Archos"]:			cf.doTurnArchos(iPlayer)
		elif eCiv == self.Civilizations["Scions"]:			cf.doTurnScions(iPlayer)
#		elif eCiv == self.Civilizations["Grigori"]:			cf.doTurnGrigori(iPlayer)
#		elif eCiv == self.Civilizations["Mekara Order"]:	cf.doTurnMekara(iPlayer)
		elif eCiv == self.Civilizations["Infernal"]:		cf.doTurnInfernal(iPlayer)
		elif eCiv == self.Civilizations["Mercurians"]:		cf.doTurnMercurians(iPlayer)

		if pPlayer.hasTrait(self.Traits["Insane"]):			cf.doInsane(iPlayer)
		if pPlayer.hasTrait(self.Traits["Adaptive"]):		cf.doAdaptive(iPlayer, iGameTurn)

		## Reminders
		if (gc.getPlayer(iPlayer).isHuman()):
			thisTurn = gc.getGame().getGameTurn() + 1
			for i in xrange(len(self.reminders) -1, -1, -1):
				if self.reminders[i][0] != thisTurn: continue
				message = self.reminders[i][1]
				CyInterface().addMessage(iPlayer, True, 30, message, 'AS2D_SOMNIUM_DISCARD', 0, None, ColorTypes(11), 0, 0, False, False)
				popupInfo = CyPopupInfo()
				popupInfo.setText(message)
				popupInfo.addPopup(iPlayer)
				del self.reminders[i]
				if gc.getGame().isGameMultiPlayer(): continue
				SdToolKitAdvanced.sdSetGlobal("reminders", "list", self.reminders)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onBeginPlayerTurn']:
			module.onBeginPlayerTurn(self, argsList)

		## Modular Python End
		## *******************

		if pPlayer.isHuman():
			self.Tools.showTraitPopup()

	def onEndPlayerTurn(self, argsList):
		'Called at the end of a players turn'
		iGameTurn, iPlayer = argsList
		gc			= CyGlobalContext()
		cf			= self.cf
		game		= CyGame()
		getPlayer	= gc.getPlayer
		pPlayer		= getPlayer(iPlayer)

		if (game.getElapsedGameTurns() == 1):
			if (pPlayer.isHuman()):
				if (pPlayer.canRevolution(0)):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_CHANGECIVIC)
					popupInfo.addPopup(iPlayer)

		CvAdvisorUtils.resetAdvisorNags()
		CvAdvisorUtils.endTurnFeats(iPlayer)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onEndPlayerTurn']:
			module.onEndPlayerTurn(self, argsList)

		## Modular Python End
		## *******************

# FF: Added by Jean Elcard 14/01/2009 (speed tweak)
		rebuildGraphics()
# FF: End Add

	def onEndTurnReady(self, argsList):
		iGameTurn = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onEndTurnReady']:
			module.onEndTurnReady(self, argsList)

		## Modular Python End
		## *******************

	def onFirstContact(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##				
		'Contact'
		iTeamX,iHasMetTeamY = argsList
		if (not self.__LOG_CONTACT):
			return
		CvUtil.pyPrint('Team %d has met Team %d' %(iTeamX, iHasMetTeamY))

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onFirstContact']:
			module.onFirstContact(self, argsList)

		## Modular Python End
		## *******************

	def onCombatResult(self, argsList):
		'Combat Result'
		pWinner,pLoser	= argsList
		gc				= CyGlobalContext()
		cf				= self.cf
		iWinner			= pWinner.getOwner()
		iLoser			= pLoser.getOwner()

		### NOW DONE IN POSTCOMBAT METHODS ON PROMOTIONS

		iGodslayer		= self.Promotions["Equipment"]["Godslayer"]
		iAvatar			= self.Promotions["Race"]["Avatar"]
		iClava			= gc.getInfoTypeForString('PROMOTION_CLAVA_VINDEX')
		iNetherblade	= gc.getInfoTypeForString('PROMOTION_NETHER_BLADE')
		
		if pWinner.isHasPromotion(iGodslayer):
			if pLoser.isHasPromotion(iAvatar):
				pLoser.setHasPromotion(iAvatar, False)
				pLoser.kill(False, iWinner)
		elif pLoser.isHasPromotion(iGodslayer):
			if pWinner.isHasPromotion(iAvatar):
				pWinner.setHasPromotion(iAvatar, False)
				pWinner.kill(False, iLoser)
		
		elif pWinner.isHasPromotion(iNetherblade) and not gc.isNoCrash():
			gc.getGame().addtoDeathList(gc.getInfoTypeForString('DEATHLIST_NETHERBLADE'),pLoser)
			pLoser.kill(False, iWinner)
		elif pLoser.isHasPromotion(iNetherblade) and not gc.isNoCrash():
			gc.getGame().addtoDeathList(gc.getInfoTypeForString('DEATHLIST_NETHERBLADE'),pWinner)
			pWinner.kill(False, iLoser)
			
		elif pWinner.isHasPromotion(iClava):
			
			CvUtil.pyPrint('someone was killed with a clava')
			if pLoser.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON')) and not gc.isNoCrash():
				gc.getGame().addtoDeathList(gc.getInfoTypeForString('DEATHLIST_BASIUM_DEMON'),pLoser)
				pLoser.kill(False, iWinner)
				CvUtil.pyPrint('a demon was killed with a clava')
				
			if cf.angelorMane(pLoser) == gc.getInfoTypeForString('UNIT_MANES') and not gc.isNoCrash():
				gc.getGame().addtoDeathList(gc.getInfoTypeForString('DEATHLIST_BASIUM'),pLoser)
				pLoser.kill(False, iWinner)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCombatResult']:
			module.onCombatResult(self, argsList)

		## Modular Python End
		## *******************
		
		if (not self.__LOG_COMBAT):
			return
		
	def onCombatLogCalc(self, argsList):
		'Combat Result'
		genericArgs	= argsList[0][0]
		cdAttacker	= genericArgs[0]
		cdDefender	= genericArgs[1]
		iCombatOdds	= genericArgs[2]
		CvUtil.combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCombatLogCalc']:
			module.onCombatLogCalc(self, argsList)

		## Modular Python End
		## *******************

	def onCombatLogHit(self, argsList):
		'Combat Message'
		global gCombatMessages, gCombatLog
		gc			= CyGlobalContext()
		genericArgs	= argsList[0][0]
		cdAttacker	= genericArgs[0]
		cdDefender	= genericArgs[1]
		iIsAttacker	= genericArgs[2]
		iDamage		= genericArgs[3]
		localText	= CyTranslator()

		if cdDefender.eOwner == cdDefender.eVisualOwner:
			szDefenderName = gc.getPlayer(cdDefender.eOwner).getNameKey()
		else:
			szDefenderName = localText.getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN", ())
		if cdAttacker.eOwner == cdAttacker.eVisualOwner:
			szAttackerName = gc.getPlayer(cdAttacker.eOwner).getNameKey()
		else:
			szAttackerName = localText.getText("TXT_KEY_TRAIT_PLAYER_UNKNOWN", ())

		if (iIsAttacker == 0):
			combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_HIT", (szDefenderName, cdDefender.sUnitName, iDamage, cdDefender.iCurrHitPoints, cdDefender.iMaxHitPoints))
			CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
			CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
			if (cdDefender.iCurrHitPoints <= 0):
				combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_DEFEATED", (szAttackerName, cdAttacker.sUnitName, szDefenderName, cdDefender.sUnitName))
				CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
				CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
		elif (iIsAttacker == 1):
			combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_HIT", (szAttackerName, cdAttacker.sUnitName, iDamage, cdAttacker.iCurrHitPoints, cdAttacker.iMaxHitPoints))
			CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
			CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
			if (cdAttacker.iCurrHitPoints <= 0):
				combatMessage = localText.getText("TXT_KEY_COMBAT_MESSAGE_DEFEATED", (szDefenderName, cdDefender.sUnitName, szAttackerName, cdAttacker.sUnitName))
				CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
				CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCombatLogHit']:
			module.onCombatLogHit(self, argsList)

		## Modular Python End
		## *******************

	def onImprovementBuilt(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Improvement Built'
		iImprovement, iX, iY = argsList
		self.verifyLoaded()
		gc		= CyGlobalContext()
		pPlot	= CyMap().plot(iX, iY)
		if gc.getImprovementInfo(iImprovement).isUnique():
			# This CyEngine call, for whatever godsdangnabit reason, fails to trigger when
			# a landmark has been removed from the same tile before the player has a chance to input anything.
			# So, delay a fraction of a second. Hell if I know why.
			# Defer also doesn't update until WB is exited which can cause confusion, so check for that and game init
			if (CyGame().GetWorldBuilderMode() or CyGame().getGameTurn() < 1):
				CyEngine().addLandmark(pPlot, CvUtil.convertToStrLatin(gc.getImprovementInfo(iImprovement).getDescription()))
			else:
				deferCall(lambda: CyEngine().addLandmark(pPlot, CvUtil.convertToStrLatin(gc.getImprovementInfo(iImprovement).getDescription())), delay=0.05)

			if   iImprovement == self.UniqueImprovements["Ring of Carcer"]:
				pPlot.setMinLevel(15)

			elif iImprovement == self.UniqueImprovements["Bair of Lacuna"]:
				pPlot.setMinLevel(6)
				pPlot.setRouteType(self.Improvements["Road"])

			elif iImprovement == self.UniqueImprovements["Seven Pines"]:
				for iiX, iiY in aoeByMapSize(pPlot):
					pLoopPlot = CyMap().plot(iiX, iiY)
					pLoopPlot.setPlotEffectType(gc.getInfoTypeForString("PLOT_EFFECT_BLESSED_LANDS"))

			elif gc.getInfoTypeForString("MODULE_MAGISTER_ASHES")!=-1 and iImprovement == gc.getInfoTypeForString("IMPROVEMENT_WHISPERING_WOOD"):
				pPlot.setFeatureType(self.Feature["Ancient Forest"], 0)
				for iiX, iiY in aoeByMapSize(pPlot):
					pLoopPlot = CyMap().plot(iiX, iiY)
					pLoopPlot.setPlotEffectType(gc.getInfoTypeForString("PLOT_EFFECT_MIST"))

			elif iImprovement == self.UniqueImprovements["Well of Souls"]:
				for iiX, iiY in aoeByMapSize(pPlot):
					pLoopPlot = CyMap().plot(iiX, iiY)
					if pLoopPlot.isWater(): continue
					pLoopPlot.setTerrainType(self.Terrain["Wasteland"], True, True)

		elif iImprovement == self.CivImprovements["D'Tesh"]["Aquatic Pyre"]:
			if pPlot.getFeatureType != -1:
				pPlot.setFeatureType(-1, -1)
			if pPlot.getBonusType(-1) != -1:
				pPlot.setBonusType(-1)
		elif iImprovement == self.Improvements["HellGate"]:
			CyGame().changeGlobalCounter(2)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onImprovementBuilt']:
			module.onImprovementBuilt(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Improvement %s was built at %d, %d'
			%(gc.getImprovementInfo(iImprovement).getDescription(), iX, iY))

	def onImprovementDestroyed(self, argsList):
		## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
		## Platy Builder ##
		'Improvement Destroyed'
		iImprovement, iOwner, iX, iY = argsList
		gc = CyGlobalContext()

		if iImprovement != -1:
			if gc.getImprovementInfo(iImprovement).isUnique():
				pPlot = CyMap().plot(iX, iY)
				CyEngine().removeLandmark(pPlot)
				rebuildPlots([pPlot])

				if   iImprovement == self.UniqueImprovements["Ring of Carcer"]:
					pPlot.setMinLevel(-1)

				elif iImprovement == self.UniqueImprovements["Bair of Lacuna"]:
					pPlot.setMinLevel(-1)
					pPlot.setRouteType(-1)

				elif iImprovement == self.UniqueImprovements["Seven Pines"]:
					for iiX, iiY in aoeByMapSize(pPlot):
						pLoopPlot = CyMap().plot(iiX, iiY)
						pLoopPlot.setPlotEffectType(gc.getInfoTypeForString("NO_PLOT_EFFECT"))

				elif gc.getInfoTypeForString("MODULE_MAGISTER_ASHES")!=-1 and iImprovement == gc.getInfoTypeForString("IMPROVEMENT_WHISPERING_WOOD"):
					for iiX, iiY in aoeByMapSize(pPlot):
						pLoopPlot = CyMap().plot(iiX, iiY)
						pLoopPlot.setPlotEffectType(gc.getInfoTypeForString("NO_PLOT_EFFECT"))

			elif iImprovement == self.Improvements["HellGate"]:
				CyGame().changeGlobalCounter(-2)

			elif iImprovement == self.Improvements["Necrototem"]:
				CyGame().changeGlobalCounter(-2)

		if CyGame().getWBMapScript():
			sf.onImprovementDestroyed(iImprovement, iOwner, iX, iY)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onImprovementDestroyed']:
			module.onImprovementDestroyed(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Improvement %s was Destroyed at %d, %d'
			%(gc.getImprovementInfo(iImprovement).getDescription(), iX, iY))

	def onRouteBuilt(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Route Built'
		iRoute, iX, iY = argsList
		gc = CyGlobalContext()

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onRouteBuilt']:
			module.onRouteBuilt(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_IMPROVEMENT):
			return
		CvUtil.pyPrint('Route %s was built at %d, %d'
			%(gc.getRouteInfo(iRoute).getDescription(), iX, iY))

	def onPlotRevealed(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##					
		'Plot Revealed'
		pPlot = argsList[0]
		iTeam = argsList[1]

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onPlotRevealed']:
			module.onPlotRevealed(self, argsList)

		## Modular Python End
		## *******************

	def onPlotFeatureRemoved(self, argsList):
		'Plot Revealed'
		pPlot			= argsList[0]
		iFeatureType	= argsList[1]
		pCity			= argsList[2] # This can be null

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onPlotFeatureRemoved']:
			module.onPlotFeatureRemoved(self, argsList)

		## Modular Python End
		## *******************

	def onPlotPicked(self, argsList):
		'Plot Picked'
		pPlot = argsList[0]
		CvUtil.pyPrint('Plot was picked at %d, %d'
			%(pPlot.getX(), pPlot.getY()))

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onPlotPicked']:
			module.onPlotPicked(self, argsList)

		## Modular Python End
		## *******************

	def onNukeExplosion(self, argsList):
		'Nuke Explosion'
		pPlot, pNukeUnit = argsList
		CvUtil.pyPrint('Nuke detonated at %d, %d'
			%(pPlot.getX(), pPlot.getY()))

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onNukeExplosion']:
			module.onNukeExplosion(self, argsList)

		## Modular Python End
		## *******************

	def onGotoPlotSet(self, argsList):
		'Nuke Explosion'
		pPlot, iPlayer = argsList

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onGotoPlotSet']:
			module.onGotoPlotSet(self, argsList)

		## Modular Python End
		## *******************

	def onBuildingBuilt(self, argsList):
		'Building Completed'
		pCity, iBuildingType = argsList
		iPlayer			= pCity.getOwner()
		gc				= CyGlobalContext()
		cf				= self.cf
		pPlayer			= gc.getPlayer(iPlayer)
		pBuilding		= gc.getBuildingInfo(iBuildingType)
		iBuildingClass	= pBuilding.getBuildingClassType()

		if ((not CyGame().isNetworkMultiPlayer()) and (pCity.getOwner() == CyGame().getActivePlayer()) and isWorldWonderClass(iBuildingClass)):
			if pBuilding.getMovie():
				## Platy Builder ##
				if not CyGame().GetWorldBuilderMode():
					# If this is a wonder...
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setData1(iBuildingType)
					popupInfo.setData2(pCity.getID())
					popupInfo.setData3(0)
					popupInfo.setText(u"showWonderMovie")
					popupInfo.addPopup(pCity.getOwner())

		if   iBuildingType == self.Buildings["Infernal Grimoire"]:
			iNoAI	= UnitAITypes.NO_UNITAI
			iSouth	= DirectionTypes.DIRECTION_SOUTH
			pPlot	= pCity.plot()
			if CyGame().getSorenRandNum(100, "Grimoire Effect") <= 20:
				pPlot2 = findClearPlot(-1, pPlot)
				if pPlot2 != -1:
					bPlayer = gc.getPlayer(gc.getDEMON_PLAYER())
					newUnit = bPlayer.initUnit(self.Units["Infernal"]["Balor"], pPlot2.getX(), pPlot2.getY(), iNoAI, iSouth)
					CyInterface().addMessage(pCity.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_INFERNAL_GRIMOIRE_BALOR",()),'AS2D_BALOR',1,'Art/Interface/Buttons/Units/Balor.dds',ColorTypes(7),newUnit.getX(),newUnit.getY(),True,True)
					if pCity.getOwner() == CyGame().getActivePlayer():
						addPopup(CyTranslator().getText("TXT_KEY_POPUP_INFERNAL_GRIMOIRE_BALOR",()), 'art/interface/popups/Balor.dds')

		elif iBuildingType == self.Buildings["Pact of the Nilhorn"]:
			lName = ["Larry", "Curly", "Moe"]
			iNoAI		= UnitAITypes.NO_UNITAI
			iSouth		= DirectionTypes.DIRECTION_SOUTH
			iX			= pCity.getX()
			iY			= pCity.getY()
			for i in xrange(3):
				newUnit = pPlayer.initUnit(self.Units["Savage"]["Hill Giant"], iX, iY, iNoAI, iSouth)
				newUnit.setHasPromotion(self.Promotions["Effects"]["Hidden Nationality"], True)
				newUnit.setHasPromotion(self.Promotions["Race"]["Undead"], False)
				if newUnit.getRace() != -1:
					newUnit.setHasPromotion(newUnit.getRace(), False)
				newUnit.setHasPromotion(self.Promotions["Race"]["Giantkin"], True)
				newUnit.setName(lName[i])

		elif iBuildingType == self.Buildings["Mercurian Gate"]:
			iNoAI		= UnitAITypes.NO_UNITAI
			iSouth		= DirectionTypes.DIRECTION_SOUTH
			iMercurians	= self.Civilizations["Mercurians"]
			pPlot		= pCity.plot()
			if not CyGame().isCivEverActive(iMercurians):
				iMercurianPlayer	= getOpenPlayer()
				pMercurians			= gc.getPlayer(iMercurianPlayer)
				iTeam				= pPlayer.getTeam()
				pPlot2				= findClearPlot(-1, pCity.plot())
				if (iMercurianPlayer != -1 and pPlot2 != -1):
					iX = pPlot.getX(); iY = pPlot.getY();
					for i in xrange(pPlot.getNumUnits(), -1, -1):
						pUnit = pPlot.getUnit(i)
						pUnit.setXY(pPlot2.getX(), pPlot2.getY(), True, True, True, False)
					CyGame().addPlayerAdvanced(iMercurianPlayer, iTeam, self.Leaders["Basium"], iMercurians, pPlayer.getID())
					basiumUnit = pMercurians.initUnit(self.Heroes["Basium"], iX, iY, iNoAI, iSouth)
					basiumUnit.setExperienceTimes100(2500, -1)
					pMercurians.initUnit(self.Units["Generic"]["Settler"], iX, iY, iNoAI, iSouth)
					pMercurians.initUnit(self.Units["Mercurian"]["Angel"], iX, iY, iNoAI, iSouth)
					pMercurians.initUnit(self.Units["Mercurian"]["Angel"], iX, iY, iNoAI, iSouth)
					pMercurians.initUnit(self.Units["Mercurian"]["Angel"], iX, iY, iNoAI, iSouth)
					pMercurians.initUnit(self.Units["Mercurian"]["Angel"], iX, iY, iNoAI, iSouth)
					pMercurians.initUnit(self.Units["Mercurian"]["Angel"], iX, iY, iNoAI, iSouth)
					pMercurians.initUnit(self.Units["Mercurian"]["Angel"], iX, iY, iNoAI, iSouth)
					if pPlayer.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_POPUP_CONTROL_MERCURIANS",()))
						popupInfo.setData1(iPlayer)
						popupInfo.setData2(iMercurianPlayer)
						popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_YES", ()), "")
						popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_POPUP_NO", ()), "")
						popupInfo.setOnClickedPythonCallback("reassignPlayer")
						popupInfo.addPopup(iPlayer)
			elif not CyGame().isUnitClassMaxedOut(self.UnitClasses["Basium"], 0) and CyGame().getNumCivActive(iMercurians) > 0:
				pMercurians		= gc.getPlayer(CyGame().getCivActivePlayer(iMercurians, 0))
				pCapitalPlot	= pMercurians.getCapitalCity()
				basiumUnit		= pMercurians.initUnit(self.Heroes["Basium"], pCapitalPlot.getX(), pCapitalPlot.getY(), iNoAI, iSouth)
				basiumUnit.setExperienceTimes100(2500, -1)

		elif iBuildingType == self.Buildings["Tower of Elements"]:
			iNoAI		= UnitAITypes.NO_UNITAI
			iSouth		= DirectionTypes.DIRECTION_SOUTH
			iX			= pCity.getX()
			iY			= pCity.getY()
			lList		= [self.Units["Summons"]["Air Elemental"], self.Units["Summons"]["Earth Elemental"], self.Units["Summons"]["Fire Elemental"],self.Units["Summons"]["Ice Elemental"], self.Units["Summons"]["Water Elemental"]]
			iUnit		= lList[CyGame().getSorenRandNum(len(lList), "ToE Pick Elemental")]
			newUnit		= pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)
			newUnit.setHasPromotion(self.Promotions["Effects"]["Held"], True)
			iElemental	= self.Promotions["Race"]["Elemental"]
			iStrong		= self.Promotions["Effects"]["Strong"]

			iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
			iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
			szText		= CyTranslator().getText("TXT_KEY_MESSAGE_TOWER_OF_THE_ELEMENTS_SPAWN",())
			szSound		= ""
			CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, gc.getUnitInfo(iUnit).getButton(), iGreen, iX, iY, True, True)
			for iLoopUnit in xrange(pPlayer.getNumUnits()):
				pLoopUnit = pPlayer.getUnit(iLoopUnit)
				if not pLoopUnit.isHasPromotion(iElemental): continue
				pLoopUnit.setHasPromotion(iStrong, True)

		elif iBuildingType == self.Buildings["Tower of Necromancy"]:
			iCiv	= pPlayer.getCivilizationType()
			iScions	= self.Civilizations["Scions"]
			iUndead	= self.Promotions["Race"]["Undead"]
			iSkele	= self.Units["Summons"]["Skeleton"]
			iHorde	= self.Units["Scions"]["Bone Horde"]
			iCorpse	= self.Units["Veil"]["Diseased Corpse"]
			iStrong	= self.Promotions["Effects"]["Strong"]
			for iLoopUnit in xrange(pPlayer.getNumUnits()):
				pLoopUnit = pPlayer.getUnit(iLoopUnit)
				if iCiv != iScions:
					if pLoopUnit.isHasPromotion(iUndead):	pLoopUnit.setHasPromotion(iStrong, True)
				else: # if Scions, limit the benefits (game balance)
					iUnitType = pLoopUnit.getUnitType()
					if   iUnitType == iSkele:				pLoopUnit.setHasPromotion(iStrong, True)
					elif iUnitType == iHorde:				pLoopUnit.setHasPromotion(iStrong, True)
					elif iUnitType == iCorpse:				pLoopUnit.setHasPromotion(iStrong, True)

		elif iBuildingType == self.Buildings["Temple of the Gift"]:
			pCity.setNumRealBuilding(self.Buildings["Emperors Mark"], 0)

		elif iBuildingType == self.Buildings["Grand Menagerie"]:
			if pPlayer.isHuman() and not CyGame().getWBMapScript():
				t = "TROPHY_FEAT_GRAND_MENAGERIE"
				if not CyGame().isHasTrophy(t): CyGame().changeTrophyValue(t, 1)

		elif iBuildingType == self.Buildings["Fisher Guild"]:
			pCity.setHasCorporation( self.Corporations["Fishermans"], True, True, False)
		elif iBuildingType == self.Buildings["Masquerade Troupe Camp"]:
			pCity.setHasCorporation( self.Corporations["Masquerade"], True, True, False)
		elif iBuildingType == self.Buildings["Fabricaforma"]:
			pCity.setHasCorporation( self.Corporations["Fabricaforma"], True, True, False)
		elif iBuildingType == self.Buildings["Farmers Guild"]:
			pCity.setHasCorporation( self.Corporations["Farmers"], True, True, False)
		elif iBuildingType == self.Buildings["Stonefire Guild"]:
			pCity.setHasCorporation( self.Corporations["Stonefire"], True, True, False)
		elif iBuildingType == self.Buildings["Mokkas Cauldron"]:
			gc.getGame().setGlobalFlag(gc.getInfoTypeForString("FLAG_MOKKA_LOST"), False)

		CvAdvisorUtils.buildingBuiltFeats(pCity, iBuildingType)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onBuildingBuilt']:
			module.onBuildingBuilt(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_BUILDING):
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s'
			%(gc.getBuildingInfo(iBuildingType).getDescription(), pCity.getOwner(), gc.getPlayer(pCity.getOwner()).getCivilizationDescription(0)))

	def onProjectBuilt(self, argsList):
		'Project Completed'
		pCity, iProjectType = argsList

		gc				= CyGlobalContext()
		cf				= self.cf
		iPlayer 		= pCity.getOwner()

		if ((not CyGame().isNetworkMultiPlayer()) and (iPlayer == CyGame().getActivePlayer())) or not CyGame().GetWorldBuilderMode():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
			popupInfo.setData1(iProjectType)
			popupInfo.setData2(pCity.getID())
			popupInfo.setData3(2)
			popupInfo.setText(u"showWonderMovie")
			popupInfo.addPopup(iPlayer)

		if   iProjectType == self.Projects["Bane Divine"]:			cf.doBaneDivine(iPlayer)
		elif iProjectType == self.Projects["Genesis"]:				cf.genesis(iPlayer)
		elif iProjectType == self.Projects["Glory Everlasting"]:	cf.doGlory(iPlayer)
		elif iProjectType == self.Projects["Rites of Oghma"]:		cf.doRoO()
		elif iProjectType == self.Projects["Nature's Revolt"]:		cf.doNatureRevolt()
		elif iProjectType == self.Projects["Blood of the Phoenix"]:	cf.doBloodOfThePhoenix(iPlayer)
		elif iProjectType == self.Projects["Purge the Unfaithful"]:	cf.doPurge(iPlayer)
		elif iProjectType == self.Projects["Samhain"]:				cf.doSamhain(iPlayer)
		elif iProjectType == self.Projects["The White Hand"]:		cf.doProjectWH(pCity)
		elif iProjectType == self.Projects["The Deepening"]:		cf.doDeepening()
		elif iProjectType == self.Projects["Stir From Slumber"]:	cf.stirFromSlumber(pCity)
		elif iProjectType == self.Projects["The Draw"]:				cf.doDraw(iPlayer)
		elif iProjectType == self.Projects["Ascension"]:			cf.doAscension(iPlayer)
		elif iProjectType == self.Projects["Birthright Regained"]:
			pPlayer	= gc.getPlayer(iPlayer)
			pPlayer.setFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL, False)
		elif iProjectType == self.Projects["Prepare Expedition"]:
			pPlayer	= gc.getPlayer(iPlayer)
			pPlayer.setFeatAccomplished(FeatTypes.FEAT_EXPEDITION_READY, True)
		elif iProjectType == self.Projects["Pax Diabolis"]:
			pCity.setNumRealBuilding( self.Buildings["Pax Diabolis"], 1)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onProjectBuilt']:
			module.onProjectBuilt(self, argsList)

		## Modular Python End
		## *******************


	def onSelectionGroupPushMission(self, argsList):
		'selection group mission'
		eOwner		= argsList[0]
		eMission	= argsList[1]
		iNumUnits	= argsList[2]
		listUnitIds	= argsList[3]

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onSelectionGroupPushMission']:
			module.onSelectionGroupPushMission(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_PUSH_MISSION):
			return
		##if pHeadUnit:
		CvUtil.pyPrint("Selection Group pushed mission %d" %(eMission))

	def onUnitMove(self, argsList):
		'unit move'
		pPlot, pUnit, pOldPlot = argsList
		gc			= CyGlobalContext()
		iPlayer		= pUnit.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)
		szDesc		= gc.getUnitInfo(pUnit.getUnitType()).getDescription()

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitMove']:
			module.onUnitMove(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_MOVEMENT):
			return
		if pPlayer and szDesc:
			CvUtil.pyPrint('Player %d Civilization %s unit %s is moving to %d, %d'
				%(pPlayer.getID(), pPlayer.getCivilizationName(), szDesc,
				pUnit.getX(), pUnit.getY()))

	def onUnitSetXY(self, argsList):
		'units xy coords set manually'
		pPlot, pUnit = argsList

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitSetXY']:
			module.onUnitSetXY(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_MOVEMENT):
			return

	def onUnitCreated(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Unit Completed'
		pUnit = argsList[0]
		self.verifyLoaded()
		gc			= CyGlobalContext()
		cf			= self.cf
		iPlayer		= pUnit.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)
		iUnitType	= pUnit.getUnitType()
		iUnitCombat	= pUnit.getUnitCombatType()

		if CyGame().getAIAutoPlay() == 0:
			if (pUnit.isImage()):
				activePlayer = gc.getPlayer(CyGame().getActivePlayer())
				sPlayerName = pPlayer.getName()
				sUnitName = pUnit.getName()
				sQuote = pUnit.getQuote()
				if gc.getTeam(pUnit.getTeam()).isHasMet(activePlayer.getTeam()):
					sPopupText = CyTranslator().getText('TXT_KEY_MISC_UNIT_POPUP',(sPlayerName, sUnitName, sQuote))
				else:
					sPopupText = CyTranslator().getText('TXT_KEY_MISC_UNIT_POPUP_UNKNOWN',(sUnitName, sQuote))
				addPopup(sPopupText, str(pUnit.getImage()))

		cf.unitCreatedTraits(pUnit)

		if iUnitType == self.Units["Scorpion Clan"]["Whelp"]: pUnit =	cf.unitCreatedWelp(pUnit)
		if iUnitCombat == self.UnitCombats["Adept"]:					cf.unitCreatedAdept(pUnit)

		if pUnit.isHasPromotion(self.Promotions["Race"]["Elemental"]):
			if pPlayer.getNumBuilding(self.Buildings["Tower of Elements"]) > 0:
				pUnit.setHasPromotion(self.Promotions["Effects"]["Strong"], True)

		if pUnit.isHasPromotion(self.Promotions["Race"]["Undead"]):
			if pPlayer.getNumBuilding(self.Buildings["Tower of Necromancy"]) > 0:
				if pPlayer.getCivilizationType() != self.Civilizations["Scions"]:
					pUnit.setHasPromotion(self.Promotions["Effects"]["Strong"], True)
				else: #scions specifics
					if   iUnitType == self.Units["Summons"]["Skeleton"]:		pUnit.setHasPromotion(self.Promotions["Effects"]["Strong"], True)
					elif iUnitType == self.Units["Summons"]["Spectre"]:			pUnit.setHasPromotion(self.Promotions["Effects"]["Strong"], True)
					elif iUnitType == self.Units["Summons"]["Wraith"]:			pUnit.setHasPromotion(self.Promotions["Effects"]["Strong"], True)
					elif iUnitType == self.Units["Veil"]["Diseased Corpse"]:	pUnit.setHasPromotion(self.Promotions["Effects"]["Strong"], True)
					elif iUnitType == self.Units["Scions"]["Bone Horde"]:		pUnit.setHasPromotion(self.Promotions["Effects"]["Strong"], True)

		if pUnit.isAlive() and pUnit.baseCombatStr() > 0:				cf.unitCreatedAspect(pUnit)
		if iUnitCombat == self.UnitCombats["Mounted"]:					cf.unitCreatedMounted(pUnit)
		if pUnit.isSecondaryUnitCombat(self.UnitCombats["Mounted"]):	cf.unitCreatedMounted(pUnit)

		if iUnitType == gc.getInfoTypeForString('UNIT_CARNIVEAN'):
			pUnit.setLevel(15)
			pUnit.setExperienceTimes100(10000, 10000)
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_MUTATED"),True)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitCreated']:
			module.onUnitCreated(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_UNITBUILD):
			return

	def onUnitBuilt(self, argsList):
		'Unit Completed'
		pCity = argsList[0]
		pUnit = argsList[1]

		gc			= CyGlobalContext()
		cf			= self.cf
		iPlayer		= pUnit.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)
		iUnitType	= pUnit.getUnitType()
		iCombatType	= pUnit.getUnitCombatType()
		iCiv		= pPlayer.getCivilizationType()

		if pUnit.isAlive():												cf.doHalfMortal(pUnit)
		if iUnitType == self.Units["Veil"]["Beast of Agares"]:			cf.doBeastOfAgares(pCity)
		if pCity.getNumBuilding(self.Buildings["Chancel of Guardians"]) > 0:
			if CyGame().getSorenRandNum(100, "Chancel of Guardians") < 20:
				pUnit.setHasPromotion( self.Promotions["Generic"]["Defensive"], True)

	#	if pPlayer.hasTrait(self.Traits["Instructor3"]):
	#		if not iCombatType in (self.UnitCombats["Siege"], self.UnitCombats["Naval"])
	#			pUnit.changeFreePromotionPick(3)
	#	elif pPlayer.hasTrait(self.Traits["Instructor2"]):
	#		if not iCombatType in (self.UnitCombats["Siege"], self.UnitCombats["Naval"])
	#			pUnit.changeFreePromotionPick(2)
		if pPlayer.hasTrait(self.Traits["Instructor"]):
			if not iCombatType in (self.UnitCombats["Siege"], self.UnitCombats["Naval"]):
				pUnit.changeFreePromotionPick(1)

		if pCity.getNumBuilding(self.Buildings["Wizards Hall"]) > 0:	cf.unitBuiltAmurites(pUnit, pCity)
	#	if iCiv == self.Civilizations["Luchuirp"]:						cf.unitBuiltLuchuirp(pUnit, pCity)
	#       Done by XML now.

		if pCity.getNumBuilding( self.Buildings["Asylum"]) > 0:
			if pUnit.isAlive():
				if isWorldUnitClass(pUnit.getUnitClassType()) == False:
					if CyGame().getSorenRandNum(100, "Asylum Crazed Application") <= 10:
						pUnit.setHasPromotion( self.Promotions["Generic"]["Crazed"], True)
						pUnit.setHasPromotion( self.Promotions["Generic"]["Enraged"], True)

		if iUnitType == self.Heroes["Acheron"]:
			pCity.setNumRealBuilding(self.Buildings["Dragons Hoard"], 1)
			pUnit.setHasPromotion(self.Promotions["Effects"]["Acheron Leashed"], True)
			iX			= pCity.getX()
			iY			= pCity.getY()
			for dX, dY in RANGE1:
				pPlot		= CyMap().plot(iX+dX, iY+dY)
				iFeature	= pPlot.getFeatureType()
				if iFeature != self.Feature["Forest"] and iFeature != self.Feature["Jungle"]: continue
				pPlot.setFeatureType(self.Feature["Flames"], 0)

		if pUnit.isHasPromotion(self.Promotions["Race"]["Dwarven"]):
			if pCity.getNumBuilding(self.Buildings["Brewery"]) > 0:
				pUnit.changeExperience(2, -1, False, False, False)

		if pUnit.isHasPromotion(self.Promotions["Race"]["Demon"]):
			if pCity.getNumBuilding(self.Buildings["Demons Altar"]) > 0:
				pUnit.changeExperience(2, -1, False, False, False)

		if iCiv == self.Civilizations["Austrin"]:
			if iCombatType == self.UnitCombats["Naval"]:
				pUnit.setHasPromotion( self.Promotions["Generic"]["Eastwinds"], True)

# Mekara Start - Makes sure sluga start without XP or promotions
#		if pPlayer.getCivilizationType() == self.Civilizations["Mekara Order"]:
#			if iUnitType == gc.getInfoTypeForString('UNIT_SLUGA') or iUnitType == gc.getInfoTypeForString('UNIT_BATTLE_SLUGA'):
#				newUnit = pPlayer.initUnit(iUnitType, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
#				pUnit.kill(True, 0)
#Disabled for now

		if iUnitType == gc.getInfoTypeForString("UNIT_KAHD"):
			if(pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_KAHD_MAMMON"))):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND1'), True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND2'), True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND3'), True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AMBITION'), True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('COMPELLING_JEWEL'), True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HERO'), True)
			else:
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC1'), True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC2'), True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC3'), True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MAGIC_RESISTANCE'), True)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_KAHD_REDEEMED'), True)
			

		CvAdvisorUtils.unitBuiltFeats(pCity, pUnit)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitBuilt']:
			module.onUnitBuilt(self, argsList)

		## Modular Python End
		## *******************


		if (not self.__LOG_UNITBUILD):
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s'
			%(gc.getUnitInfo(pUnit.getUnitType()).getDescription(), pPlayer.getID(), pPlayer.getCivilizationName()))

	def onUnitKilled(self, argsList):
		'Unit Killed'
		pUnit, iKillerPlayer = argsList
		gc				= CyGlobalContext()
		cf				= self.cf
		iLoserPlayer	= pUnit.getOwner()
		pLoserPlayer	= gc.getPlayer(iLoserPlayer)
		pKillerPlayer	= gc.getPlayer(iKillerPlayer)
		bConverted		= False
		iUnitType		= pUnit.getUnitType()

		if pUnit.isAlive() and not pUnit.isImmortal() and (gc.isNoCrash() or not(pUnit.isOnDeathList())):
			cf.unitKilledCity(pUnit)
			cf.unitKilledAoM(pUnit)
			if pUnit.isHasPromotion(self.Promotions["Effects"]["Spirit Guide"]): cf.unitKilledGuide(pUnit)

		if iUnitType == self.Heroes["Acheron"]:
			pUnit.setHasPromotion(self.Promotions["Effects"]["Acheron Leashed"], False)

		if CyGame().getWBMapScript():
			sf.onUnitKilled(pUnit, iKillerPlayer)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitKilled']:
			module.onUnitKilled(self, argsList)

		## Modular Python End
		## *******************

		if not pUnit.isImmortal() and not bConverted: cf.resetAspects(pUnit)

		if not self.__LOG_UNITKILLED: return
		CvUtil.pyPrint('Player %d Civilization %s Unit %s was killed by Player %d'
			%(pLoserPlayer.getID(), pLoserPlayer.getCivilizationDescription(0), gc.getUnitInfo(iUnitType).getDescription(), pKillerPlayer.getID()))

	def onUnitLost(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Unit Lost'
		pUnit	= argsList[0]
		gc		= CyGlobalContext()
		iPlayer	= pUnit.getOwner()
		pPlayer	= gc.getPlayer(iPlayer)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitLost']:
			module.onUnitLost(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_UNITLOST):
			return
		CvUtil.pyPrint('%s was lost by Player %d Civilization %s'
			%(gc.getUnitInfo(pUnit.getUnitType()).getDescription(), pPlayer.getID(), pPlayer.getCivilizationName()))

	def onUnitPromoted(self, argsList):
		'Unit Promoted'
		self.verifyLoaded(True)
		pUnit, iPromotion = argsList
		gc			= CyGlobalContext()
		iPlayer		= pUnit.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)
		iUnitType	= pUnit.getUnitType()

# Trying to get high experienced units out of City Defense Notque 03/10/09
		if pUnit.isHasPromotion(self.Promotions["Effects"]["Hero"]):
			if pUnit.getExperience() > 25:
				if pUnit.getUnitAIType() != self.UnitAI["Counter"]:
					pUnit.setUnitAIType(self.UnitAI["Counter"])

		# Change to see if I can get Pyre Zombies to stop City Defense Notque 03/10/09
		if iUnitType == self.Units["Sheaim"]["Pyre Zombie"]:
			if pUnit.getUnitAIType() == self.UnitAI["City Defense"]:
				if CyGame().getSorenRandNum(100, "PYRE_UNITAI") >= 50:
					pUnit.setUnitAIType(self.UnitAI["Collateral"])
				else:
					pUnit.setUnitAIType(self.UnitAI["Counter"])

#scions start - Handles Centeni promotions, makes sure they lose Undead status and get Chosen promotion when upgraded to another unit type
		if pUnit.isHasPromotion(self.Promotions["Effects"]["Unreliable"]):
			if iUnitType != self.Units["Scions"]["Centeni"] or pUnit.isHasPromotion(self.Promotions["Generic"]["Headless"]):
				pUnit.setHasPromotion(self.Promotions["Effects"]["Alive"], False)
				pUnit.setHasPromotion(self.Promotions["Race"]["Undead"], True)
				pUnit.setHasPromotion(self.Promotions["Effects"]["Chosen"], True)
				pUnit.setHasPromotion(self.Promotions["Effects"]["Unreliable"], False)

# scions end


		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitPromoted']:
			module.onUnitPromoted(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_UNITPROMOTED):
			return
		CvUtil.pyPrint('Unit Promotion Event: %s - %s' %(pPlayer.getCivilizationName(), pUnit.getName(),))

	def onUnitSelected(self, argsList):
		'Unit Selected'
		pUnit	= argsList[0]
		gc		= CyGlobalContext()
		iPlayer	= pUnit.getOwner()
		pPlayer	= gc.getPlayer(iPlayer)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitSelected']:
			module.onUnitSelected(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_UNITSELECTED):
			return
		CvUtil.pyPrint('%s was selected by Player %d Civilization %s'
			%(gc.getUnitInfo(pUnit.getUnitType()).getDescription(), pPlayer.getID(), pPlayer.getCivilizationName()))

	def onUnitRename(self, argsList):
		'Unit is renamed'
		pUnit = argsList[0]
		if (pUnit.getOwner() == CyGame().getActivePlayer()):
			self.__eventEditUnitNameBegin(pUnit)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitRename']:
			module.onUnitRename(self, argsList)

		## Modular Python End
		## *******************

	def onUnitPillage(self, argsList):
		'Unit pillages a plot'
		pUnit, iImprovement, iRoute, iOwner = argsList
		cf			= self.cf
		gc			= CyGlobalContext()
		iPlotX		= pUnit.getX()
		iPlotY		= pUnit.getY()
		iUnitType	= pUnit.getUnitType()

		if iUnitType in (gc.getInfoTypeForString('UNIT_BOUNTY_HUNTER'), gc.getInfoTypeForString('UNIT_SLAVE_HUNTER'), gc.getInfoTypeForString('UNIT_RAIDER')): cf.pillageSlave(pUnit, iImprovement)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitPillage']:
			module.onUnitPillage(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_UNITPILLAGE):
			return
		CvUtil.pyPrint("Player %d's %s pillaged improvement %d and route %d at plot at (%d, %d)"
			%(iOwner, gc.getUnitInfo(iUnitType).getDescription(), iImprovement, iRoute, iPlotX, iPlotY))

	def onUnitSpreadReligionAttempt(self, argsList):
		'Unit tries to spread religion to a city'

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitSpreadReligionAttempt']:
			module.onUnitSpreadReligionAttempt(self, argsList)

		## Modular Python End
		## *******************

	def onUnitGifted(self, argsList):
		'Unit is gifted from one player to another'
		pUnit, iGiftingPlayer, pPlotLocation = argsList

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitGifted']:
			module.onUnitGifted(self, argsList)

		## Modular Python End
		## *******************

	def onUnitBuildImprovement(self, argsList):
		'Unit begins enacting a Build (building an Improvement or Route)'
		pUnit, iBuild, bFinished = argsList

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onUnitBuildImprovement']:
			module.onUnitBuildImprovement(self, argsList)

		## Modular Python End
		## *******************

	def onGoodyReceived(self, argsList):
		'Goody received'
		iPlayer, pPlot, pUnit, iGoodyType = argsList
		gc = CyGlobalContext()

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onGoodyReceived']:
			module.onGoodyReceived(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_GOODYRECEIVED):
			return
		CvUtil.pyPrint('%s received a goody' %(gc.getPlayer(iPlayer).getCivilizationDescription(0)),)

	def onGreatPersonBorn(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Unit Promoted'
		pUnit, iPlayer, pCity = argsList
		gc 		= CyGlobalContext() 
		pPlayer	= gc.getPlayer(iPlayer)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onGreatPersonBorn']:
			module.onGreatPersonBorn(self, argsList)

		## Modular Python End
		## *******************

		if pUnit.isNone() or pCity.isNone():
			return
		if (not self.__LOG_GREATPERSON):
			return
		CvUtil.pyPrint('A %s was born for %s in %s' %(pUnit.getName(), pPlayer.getCivilizationName(), pCity.getName()))

	def onTechAcquired(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Tech Acquired'
		iTechType, iTeam, iPlayer, bAnnounce = argsList
		# Note that iPlayer may be NULL (-1) and not a refer to a player object
		self.verifyLoaded()
		gc			= CyGlobalContext()
		cf			= self.cf
		bBarb		= True
		if iPlayer > -1:
			pPlayer = gc.getPlayer(iPlayer)
			bBarb	= pPlayer.isBarbarian()

		# Show tech splash when applicable
		if (iPlayer > -1 and bAnnounce and not CyInterface().noTechSplash()):
			if (CyGame().isFinalInitialized() and not CyGame().GetWorldBuilderMode()):
				if ((not CyGame().isNetworkMultiPlayer()) and (iPlayer == CyGame().getActivePlayer())):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
					popupInfo.setData1(iTechType)
					popupInfo.setText(u"showTechSplash")
					popupInfo.addPopup(iPlayer)

		if not bBarb:												cf.techRel(iTechType, iPlayer)
		if iTechType == self.Techs["Infernal Pact"] and not bBarb:	cf.infernalPact(iTechType, iPlayer)

		if CyGame().getWBMapScript():
			sf.onTechAcquired(iTechType, iTeam, iPlayer, bAnnounce)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onTechAcquired']:
			module.onTechAcquired(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_TECH):
			return
		CvUtil.pyPrint('%s was finished by Team %d'
			%(gc.getTechInfo.TechnologyInfo(iTechType).getDescription(), iTeam))

	def onTechSelected(self, argsList):
		'Tech Selected'
		iTechType, iPlayer = argsList
		gc = CyGlobalContext()

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onTechSelected']:
			module.onTechSelected(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_TECH):
			return
		CvUtil.pyPrint('%s was selected by Player %d' %(gc.getTechInfo(iTechType).getDescription(), iPlayer))

	def onTraitGained(self, argsList):
		'Trait Gained'
		iTrait, iPlayer = argsList
		self.verifyLoaded()
		gc	= CyGlobalContext()

		if iTrait == self.Traits["Civilized"]: # Barbarians declare war on the Clan if it becomes too strong; re-added by Azatote
			pPlayer	= gc.getPlayer(iPlayer)
			eTeam	= gc.getTeam(gc.getPlayer(gc.getORC_PLAYER()).getTeam())
			iTeam	= pPlayer.getTeam()
			if eTeam.isAtWar(iTeam) == False:
				eTeam.declareWar(iTeam, False, WarPlanTypes.WARPLAN_LIMITED)
				if iPlayer == CyGame().getActivePlayer() and pPlayer.isHuman():
					addPopup(CyTranslator().getText("TXT_KEY_POPUP_BARBARIAN_DECLARE_WAR",()), 'art/interface/popups/Barbarian.dds')
	
		if (iTrait == gc.getInfoTypeForString("TRAIT_KAHD_OGHMA")):
			pPlayer	= gc.getPlayer(iPlayer)
			pPlayer.setHasTrait(self.Traits["Intolerant"], False)
			pPlayer.setHasTrait(self.Traits["Spiritual"], True)
			addPopup(CyTranslator().getText("TXT_KEY_POPUP_KAHDI_STRENGTH_OF_WILL",()), 'art/interface/popups/kahdpop.dds')
			addPopup(CyTranslator().getText("TXT_KEY_POPUP_KAHDI_ENLIGHTENMENT",()), 'art/interface/popups/enlightenment.dds')
		
		if (iTrait == gc.getInfoTypeForString("TRAIT_KAHD_MAMMON")):
			addPopup(CyTranslator().getText("TXT_KEY_POPUP_KAHDI_STRENGTH_OF_WILL",()), 'art/interface/popups/kahdpop.dds')
			addPopup(CyTranslator().getText("TXT_KEY_POPUP_KAHDI_CORRUPTION",()), 'art/interface/popups/corruption.dds')

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onTraitGained']:
			module.onTraitGained(self, argsList)

		## Modular Python End
		## *******************

	def onTraitLost(self, argsList):
		'Trait Lost'
		iTrait, iPlayer = argsList

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onTraitLost']:
			module.onTraitLost(self, argsList)

		## Modular Python End
		## *******************

	def onReligionFounded(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Religion Founded'
		iReligion, iFounder = argsList
		gc			= CyGlobalContext() #Cause local variables are faster
		pPlayer		= gc.getPlayer(iFounder)
		iCityId		= CyGame().getHolyCity(iReligion).getID()
		if CyGame().isFinalInitialized() and not CyGame().GetWorldBuilderMode():
			if not CyGame().isNetworkMultiPlayer() and iFounder == CyGame().getActivePlayer():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iReligion)
				popupInfo.setData2(iCityId)
				if iReligion in (self.Religions["Empyrean"], self.Religions["Council of Esus"]):
					popupInfo.setData3(3)
				else:
					popupInfo.setData3(1)
				popupInfo.setText(u"showWonderMovie")
				popupInfo.addPopup(iFounder)

		if CyGame().getWBMapScript():
			sf.onReligionFounded(iReligion, iFounder)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onReligionFounded']:
			module.onReligionFounded(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_RELIGION):
			return
		CvUtil.pyPrint('Player %d Civilization %s has founded %s'
			%(iFounder, pPlayer.getCivilizationName(), gc.getReligionInfo(iReligion).getDescription()))

	def onReligionSpread(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Religion Has Spread to a City'
		iReligion, iOwner, pSpreadCity = argsList
		gc			= CyGlobalContext()
		cf			= self.cf
		pPlayer		= gc.getPlayer(iOwner)

		if iReligion == self.Religions["Order"] and CyGame().getGameTurn() != CyGame().getStartTurn(): cf.spreadOrder(iOwner, pSpreadCity)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onReligionSpread']:
			module.onReligionSpread(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has spread to Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, pPlayer.getCivilizationName(), pSpreadCity.getName()))

	def onReligionRemove(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Religion Has been removed from a City'
		iReligion, iOwner, pRemoveCity = argsList
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(iOwner)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onReligionRemove']:
			module.onReligionRemove(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has been removed from Player %d Civilization %s city of %s'
			%(gc.getReligionInfo(iReligion).getDescription(), iOwner, pPlayer.getCivilizationName(), pRemoveCity.getName()))

	def onCorporationFounded(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Corporation Founded'
		iCorporation, iFounder = argsList
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(iFounder)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCorporationFounded']:
			module.onCorporationFounded(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_RELIGION):
			return
		CvUtil.pyPrint('Player %d Civilization %s has founded %s'
			%(iFounder, pPlayer.getCivilizationName(), gc.getCorporationInfo(iCorporation).getDescription()))

	def onCorporationSpread(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Corporation Has Spread to a City'
		iCorporation, iOwner, pSpreadCity = argsList
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(iOwner)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCorporationSpread']:
			module.onCorporationSpread(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has spread to Player %d Civilization %s city of %s'
			%(gc.getCorporationInfo(iCorporation).getDescription(), iOwner, pPlayer.getCivilizationName(), pSpreadCity.getName()))

	def onCorporationRemove(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Corporation Has been removed from a City'
		iCorporation, iOwner, pRemoveCity = argsList
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(iOwner)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCorporationRemove']:
			module.onCorporationRemove(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_RELIGIONSPREAD):
			return
		CvUtil.pyPrint('%s has been removed from Player %d Civilization %s city of %s'
			%(gc.getCorporationInfo(iCorporation).getDescription(), iOwner, pPlayer.getCivilizationName(), pRemoveCity.getName()))

	def onGoldenAge(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Golden Age'
		iPlayer = argsList[0]
		gc = CyGlobalContext() #Cause local variables are faster
		pPlayer 	= gc.getPlayer(iPlayer)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onGoldenAge']:
			module.onGoldenAge(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_GOLDENAGE):
			return
		CvUtil.pyPrint('Player %d Civilization %s has begun a golden age'
			%(iPlayer, pPlayer.getCivilizationName()))

	def onEndGoldenAge(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'End Golden Age'
		iPlayer	= argsList[0]
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(iPlayer)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onEndGoldenAge']:
			module.onEndGoldenAge(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_ENDGOLDENAGE):
			return
		CvUtil.pyPrint('Player %d Civilization %s golden age has ended'
			%(iPlayer, pPlayer.getCivilizationName()))

	def onChangeWar(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'War Status Changes'
		gc				= CyGlobalContext()
		cf				= self.cf
		bIsWar			= argsList[0]
		iTeam			= argsList[1]
		iRivalTeam		= argsList[2]

		if bIsWar:		cf.resetPactTraits(iTeam, iRivalTeam)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onChangeWar']:
			module.onChangeWar(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_WARPEACE):
			return
		if (bIsWar):
			strStatus = "declared war"
		else:
			strStatus = "declared peace"
		CvUtil.pyPrint('Team %d has %s on Team %d'
			%(iTeam, strStatus, iRivalTeam))

	def onChat(self, argsList):
		'Chat Message Event'
		chatMessage = "%s" %(argsList[0],)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onChat']:
			module.onChat(self, argsList)

		## Modular Python End
		## *******************

	def onSetPlayerAlive(self, argsList):
		'Set Player Alive Event'
		iPlayerID = argsList[0]
		bNewValue = argsList[1]
		gc 			= CyGlobalContext() #Cause local variables are faster
		cf			= self.cf
		CvUtil.pyPrint("Player %d's alive status set to: %d" %(iPlayerID, int(bNewValue)))

		if (bNewValue == False and CyGame().getGameTurnYear() >= 5):
			pPlayer = gc.getPlayer(iPlayerID)
			if pPlayer.getAlignment() == self.Alignments["Good"]:
				CyGame().changeGlobalCounter(5)
			if pPlayer.getAlignment() == self.Alignments["Evil"]:
				CyGame().changeGlobalCounter(-5)
			if CyGame().getWBMapScript():
				sf.playerDefeated(pPlayer)
			else:
				if CyGame().getAIAutoPlay() == 0:
					sPlayerName = pPlayer.getName()
					sQuote = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getDefeatQuote()
					sPopupText = CyTranslator().getText('TXT_KEY_MISC_DEFEAT_POPUP',(sPlayerName, sQuote))
					addPopup(sPopupText, str(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getImage()))

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onSetPlayerAlive']:
			module.onSetPlayerAlive(self, argsList)

		## Modular Python End
		## *******************

	def onPlayerChangeStateReligion(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'Player changes his state religion'
		iPlayer, iNewReligion, iOldReligion = argsList
		gc = CyGlobalContext() #Cause local variables are faster
		pPlayer 	= gc.getPlayer(iPlayer)
		iCiv 		= pPlayer.getCivilizationType()

		if iOldReligion == self.Religions["Ashen Veil"] and iNewReligion != self.Religions["Ashen Veil"]:
			eDemonTeam = gc.getTeam(gc.getPlayer(gc.getDEMON_PLAYER()).getTeam())
			iTeam = pPlayer.getTeam()
			if eDemonTeam.isAtWar(iTeam) == False:
				eDemonTeam.declareWar(iTeam, False, WarPlanTypes.WARPLAN_TOTAL)

		if iNewReligion == self.Religions["Ashen Veil"] and iCiv in (self.Civilizations["Sheaim"], self.Civilizations["Infernal"]):
			iDemonTeam = gc.getDEMON_TEAM()
			pTeam = gc.getTeam(pPlayer.getTeam())
			pTeam.makePeace(iDemonTeam)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onPlayerChangeStateReligion']:
			module.onPlayerChangeStateReligion(self, argsList)

		## Modular Python End
		## *******************

#FF: Added by Jean Elcard 03/01/2009 (State Names)
		pPlayer.updateStateNameType()
#FF: End Add

	def onPlayerGoldTrade(self, argsList):
		'Player Trades gold to another player'
		iFromPlayer, iToPlayer, iGoldAmount = argsList

	def onCityBuilt(self, argsList):
		'City Built'
		pCity		= argsList[0]
		gc			= CyGlobalContext()
		cf			= self.cf
		pPlot		= pCity.plot()
		iOwner		= pCity.getOwner()
		pPlayer		= gc.getPlayer(iOwner)

		if pPlot.getBonusType(-1) == self.Mana["Mana"]:
			pPlot.setBonusType(-1)

		cf.cityTraitCheck(pCity)
		cf.cityLeaderCheck(pCity)
		cf.cityCivCheck(pCity)

#FF: Added by Jean Elcard 03/01/2009 (State Names)
		pPlayer.updateStateNameType()
#FF: End Add

		if CyGame().getWBMapScript():
			sf.onCityBuilt(pCity)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityBuilt']:
			module.onCityBuilt(self, argsList)

		## Modular Python End
		## *******************

		if pCity.getOwner() == CyGame().getActivePlayer() and CyGame().getAIAutoPlay() == 0:
			self.__eventEditCityNameBegin(pCity, False)
	##	CvUtil.pyPrint('City Built Event: %s' %(pCity.getName()))

	def onCityRazed(self, argsList):
		'City Razed'
		pCity, iPlayer 	= argsList
		gc 				= CyGlobalContext()
		cf				= self.cf
		iOriginalOwner	= pCity.getOriginalOwner()
		pPlayer 		= gc.getPlayer(iPlayer) # conqueror
		iPopulation 	= pCity.getPopulation()
		iOriginalAlignment = gc.getPlayer(iOriginalOwner).getAlignment()
		pPlot = pCity.plot()
		iX = pCity.getX(); iY = pCity.getY()
		eCiv 			= gc.getPlayer(iOriginalOwner).getCivilizationType()
		eNewOwnerCiv	= gc.getPlayer(iPlayer).getCivilizationType()

		cf.razeAoM(pCity)
		if (pPlayer.hasTrait(self.Traits["Scorched Earth"])):	cf.razeScorcedEarth(pCity)
		if   eNewOwnerCiv == self.Civilizations["Scions"]:		cf.razeScions(pCity)
		elif eNewOwnerCiv == self.Civilizations["D'Tesh"]:		cf.razeDtesh(pCity)

		if CyGame().getWBMapScript():
			sf.onCityRazed(pCity, iPlayer)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityRazed']:
			module.onCityRazed(self, argsList)

		## Modular Python End
		## *******************

		CvUtil.pyPrint("City Razed Event: %s" %(pCity.getName(),))

	def onCityAcquired(self, argsList): # triggered whenever a city is captured (before the player chooses to keep or raze)
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'City Acquired'
		iPreviousOwner, iNewOwner, pCity, bConquest, bTrade = argsList
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iNewOwner)
		pOldOwner	= gc.getPlayer(iPreviousOwner)
		eLeader		= pPlayer.getLeaderType()
		iCiv		= pPlayer.getCivilizationType()
		iPop		= pCity.getPopulation()

		if eLeader == gc.getInfoTypeForString("LEADER_SAUROS"):
			if   iCiv == self.Civilizations["Clan of Embers"]:
				pCity.setCityClass(gc.getInfoTypeForString("CITYCLASS_SAUROS_CLAN"))
			elif iCiv == self.Civilizations["Cualli"]:
				pCity.setCityClass(gc.getInfoTypeForString("CITYCLASS_SAUROS_CUALLI"))

		if pPlayer.hasTrait(self.Traits["Slaver"]):
			iSlave 		= self.Units["Generic"]["Slave"]
			iSlavePop 	= iPop / 2
			pCity.changePopulation(-iSlavePop)
			iPop		= pCity.getPopulation()
			iX			= pCity.getX()
			iY			= pCity.getY()
			iAI			= UnitAITypes.NO_UNITAI
			iDirection	= DirectionTypes.DIRECTION_SOUTH
			for i in xrange(iSlavePop):
				pPlayer.initUnit(iSlave, iX, iY, iAI, iDirection)

		if   iCiv == self.Civilizations["Scions"]:
			if   pOldOwner.getCivilizationType() == self.Civilizations["Scions"]:
				pass
			elif pPlayer.isCivic(self.Civics["God King"]):
				iPopReduction = iPop * 10 / 16
				pCity.changePopulation(-iPopReduction)
			else:
				iPopReduction = iPop * 10 / 12
				pCity.changePopulation(-iPopReduction)

		elif iCiv == self.Civilizations["D'Tesh"]:
			iPopReduction = iPop / 3
			pCity.changePopulation(-iPopReduction)

		elif pOldOwner.getCivilizationType() == self.Civilizations["Scions"]:
			iPopReduction = iPop * 10 / 12
			pCity.changePopulation(-iPopReduction)

		if iCiv == self.Civilizations["Infernal"]:
			pCity.setNumRealBuilding(self.Buildings["Demonic Citizens"], 1)
			pCity.setHasReligion(self.Religions["Order"], False, True, True)
			if CyGame().countKnownTechNumTeams(self.Techs["Infernal Pact"]) > 0:
				pCity.setHasReligion(self.Religions["Ashen Veil"], True, True, True)
				pCity.setNumRealBuilding(self.Buildings["Elder Council"], 1)
				pCity.setNumRealBuilding(self.Buildings["Barracks"], 1)
				pCity.setNumRealBuilding(self.Buildings["Obsidian Gate"], 1)
				pCity.setNumRealBuilding(self.Buildings["Forge"], 1)
				pCity.setNumRealBuilding(self.Buildings["Mage Guild"], 1)

		if iCiv == self.Civilizations["Austrin"]:
			pCity.setNumRealBuilding(self.Buildings["Austrin Settlement"], 1)

		if pCity.getNumBuilding(self.Buildings["Dragons Hoard"])>0:
			iX			= pCity.getX()
			iY			= pCity.getY()
			for dX in range(-5,6):
				for dY in range(-5,6):
					pPlot		= CyMap().plot(iX+dX, iY+dY)
					if pPlot.isNone():
						continue
					for i in range(pPlot.getNumUnits()):
						pUnit=pPlot.getUnit(i)
						if(pUnit.getUnitType()==self.Heroes["Acheron"]):
							pUnit.setHasPromotion(self.Promotions["Effects"]["Acheron Leashed"], False)
		if CyGame().getWBMapScript():
			sf.onCityAcquired(iPreviousOwner, iNewOwner, pCity, bConquest, bTrade)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityAcquired']:
			module.onCityAcquired(self, argsList)

		## Modular Python End
		## *******************


		CvUtil.pyPrint('City Acquired Event: %s' %(pCity.getName()))

	def onCityAcquiredAndKept(self, argsList):
		'City Acquired and Kept'
		iOwner, pCity= argsList
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iOwner)
		#Functions added here tend to cause OOS issues

#FF: Added by Jean Elcard 03/01/2009 (State Names)
		pPlayer.updateStateNameType()
#FF: End Add

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityAcquiredAndKept']:
			module.onCityAcquiredAndKept(self, argsList)

		## Modular Python End
		## *******************

		CvUtil.pyPrint('City Acquired and Kept Event: %s' %(pCity.getName()))

	def onCityLost(self, argsList):
		'City Lost'
		pCity	= argsList[0]
		gc		= CyGlobalContext()
		iPlayer	= pCity.getOwner()
		pPlayer	= gc.getPlayer(iPlayer)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityLost']:
			module.onCityLost(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_CITYLOST):
			return
		CvUtil.pyPrint('City %s was lost by Player %d Civilization %s'
			%(pCity.getName(), pPlayer.getID(), pPlayer.getCivilizationName()))

	def onCultureExpansion(self, argsList):
	## Platy Builder ##
		if CyGame().GetWorldBuilderMode() and not CvPlatyBuilderScreen.bPython: return
	## Platy Builder ##
		'City Culture Expansion'
		pCity	= argsList[0]
		iPlayer	= argsList[1]
	##	CvUtil.pyPrint("City %s's culture has expanded" %(pCity.getName(),))

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCultureExpansion']:
			module.onCultureExpansion(self, argsList)

		## Modular Python End
		## *******************

	def onCityGrowth(self, argsList):
		'City Population Growth'
		pCity = argsList[0]
		iPlayer = argsList[1]
		##CvUtil.pyPrint("%s has grown" %(pCity.getName(),))

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityGrowth']:
			module.onCityGrowth(self, argsList)

		## Modular Python End
		## *******************

	def onCityDoTurn(self, argsList):
		'City Production'
		pCity	= argsList[0]
		iPlayer	= argsList[1]
		gc		= CyGlobalContext()
		cf		= self.cf
		pPlayer	= gc.getPlayer(iPlayer)
		iCiv	= pPlayer.getCivilizationType()

		if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_PIXIE_GARDEN") > 0):	cf.doCityTurnPixieGarden(pCity, iPlayer)

		if pCity.getNumBuilding(self.Buildings["Riot and Sedition"]) > 0:
			if CyGame().getSorenRandNum(100, "Spell expiration RaS") < 16:				pCity.setNumRealBuilding( self.Buildings["Riot and Sedition"], 0)

		if pCity.getNumBuilding(self.Buildings["Poison Words"]) > 0:
			if CyGame().getSorenRandNum(100, "Spell expiration PW") < 5:				pCity.setNumRealBuilding( self.Buildings["Poison Words"], 0)

		if pCity.getNumBuilding(self.Buildings["Eyes and Ears"]) > 0:					cf.doCityTurnEAE(pCity, iPlayer)

		if pCity.getNumBuilding(self.Buildings["Hall of Mirrors"]) > 0:					cf.doCityTurnHallOfMirrors(pCity, iPlayer)

		if pCity.getNumBuilding(self.Buildings["Planar Gate"]) > 0:						cf.doCityTurnPlanarGate(iPlayer, pCity)

		if pCity.getNumBuilding(self.Buildings["Memorial Refugee"]) > 0 or pCity.getNumBuilding(self.Buildings["Dwelling of Refuge"]) > 0:
			cf.doCityTurnMemorial(iPlayer, pCity)
	
		if pCity.getNumBuilding(self.Buildings["Kahdi Vault Gate"]) > 0:				cf.doCityTurnKahdiVault(pCity, iPlayer)

		elif iCiv == self.Civilizations["Doviello"]:									cf.doCityTurnDoviello(iPlayer, pCity)

		elif iCiv == self.Civilizations["Infernal"]:
			if pCity.isHasReligion(self.Religions["Order"]):
				pCity.setHasReligion(self.Religions["Order"], False, True, True)
			if CyGame().countKnownTechNumTeams(gc.getInfoTypeForString('TECH_INFERNAL_PACT')) > 0:
				if pCity.isHasReligion(self.Religions["Ashen Veil"]) == False:
					pCity.setHasReligion(self.Religions["Ashen Veil"], True, True, True)

		elif iCiv == self.Civilizations["Mercurians"]:
			if pCity.isHasReligion(self.Religions["Ashen Veil"]):
				pCity.setHasReligion(self.Religions["Ashen Veil"], False, True, True)

		if pCity.getNumBuilding(self.Buildings["Shrine of Sirona"]) > 0:
			pPlayer.setFeatAccomplished(FeatTypes.FEAT_HEAL_UNIT_PER_TURN, True)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityDoTurn']:
			module.onCityDoTurn(self, argsList)

		## Modular Python End
		## *******************

		CvAdvisorUtils.cityAdvise(pCity, iPlayer)

	def onCityBuildingUnit(self, argsList):
		'City begins building a unit'
		pCity = argsList[0]
		iUnitType = argsList[1]
		gc = CyGlobalContext()

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityBuildingUnit']:
			module.onCityBuildingUnit(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_CITYBUILDING):
			return
		CvUtil.pyPrint("%s has begun building a %s" %(pCity.getName(),gc.getUnitInfo(iUnitType).getDescription()))

	def onCityBuildingBuilding(self, argsList):
		'City begins building a Building'
		pCity = argsList[0]
		iBuildingType = argsList[1]
		gc = CyGlobalContext()

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityBuildingBuilding']:
			module.onCityBuildingBuilding(self, argsList)

		## Modular Python End
		## *******************

		if (not self.__LOG_CITYBUILDING):
			return
		CvUtil.pyPrint("%s has begun building a %s" %(pCity.getName(),gc.getBuildingInfo(iBuildingType).getDescription()))

	def onCityRename(self, argsList):
		'City is renamed'
		pCity = argsList[0]
		game = CyGame()
		if (pCity.getOwner() == game.getActivePlayer()):
			self.__eventEditCityNameBegin(pCity, True)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityRename']:
			module.onCityRename(self, argsList)

		## Modular Python End
		## *******************

	def onCityHurry(self, argsList):
		'City is renamed'
		pCity = argsList[0]
		iHurryType = argsList[1]

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onCityHurry']:
			module.onCityHurry(self, argsList)

		## Modular Python End
		## *******************

	def onVictory(self, argsList):
		'Victory'
		iTeam, iVic = argsList
		gc = CyGlobalContext()

		if (iVic >= 0 and iVic < gc.getNumVictoryInfos()):
			trophy 		= CyGame().changeTrophyValue
			Option		= self.GameOptions
			Civ 		= self.Civilizations
			Victory		= self.Victories
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive() and pPlayer.isHuman() and pPlayer.getTeam() == iTeam:
					if CyGame().getWBMapScript():
						sf.onVictory(iPlayer, iVic)
					else:
						iCiv = pPlayer.getCivilizationType()
						if   iCiv == Civ["Amurites"]:       trophy("TROPHY_VICTORY_AMURITES", 1)
						elif iCiv == Civ["Archos"]:         trophy("TROPHY_VICTORY_ARCHOS", 1)
						elif iCiv == Civ["Austrin"]:        trophy("TROPHY_VICTORY_AUSTRIN", 1)
						elif iCiv == Civ["Balseraphs"]:     trophy("TROPHY_VICTORY_BALSERAPHS", 1)
						elif iCiv == Civ["Bannor"]:         trophy("TROPHY_VICTORY_BANNOR", 1)
						elif iCiv == Civ["Calabim"]:        trophy("TROPHY_VICTORY_CALABIM", 1)
						elif iCiv == Civ["Chislev"]:        trophy("TROPHY_VICTORY_CHISLEV", 1)
						elif iCiv == Civ["Clan of Embers"]: trophy("TROPHY_VICTORY_CLAN_OF_EMBERS", 1)
						elif iCiv == Civ["Cualli"]:         trophy("TROPHY_VICTORY_CUALLI", 1)
						elif iCiv == Civ["Doviello"]:       trophy("TROPHY_VICTORY_DOVIELLO", 1)
						elif iCiv == Civ["D'Tesh"]:         trophy("TROPHY_VICTORY_DTESH", 1)
						elif iCiv == Civ["Dural"]:          trophy("TROPHY_VICTORY_DURAL", 1)
						elif iCiv == Civ["Elohim"]:         trophy("TROPHY_VICTORY_ELOHIM", 1)
						elif iCiv == Civ["Grigori"]:        trophy("TROPHY_VICTORY_GRIGORI", 1)
						elif iCiv == Civ["Hippus"]:         trophy("TROPHY_VICTORY_HIPPUS", 1)
						elif iCiv == Civ["Illians"]:        trophy("TROPHY_VICTORY_ILLIANS", 1)
						elif iCiv == Civ["Infernal"]:       trophy("TROPHY_VICTORY_INFERNAL", 1)
						elif iCiv == Civ["Jotnar"]:         trophy("TROPHY_VICTORY_JOTNAR", 1)
						elif iCiv == Civ["Khazad"]:         trophy("TROPHY_VICTORY_KHAZAD", 1)
						elif iCiv == Civ["Kuriotates"]:     trophy("TROPHY_VICTORY_KURIOTATES", 1)
						elif iCiv == Civ["Lanun"]:          trophy("TROPHY_VICTORY_LANUN", 1)
						elif iCiv == Civ["Ljosalfar"]:      trophy("TROPHY_VICTORY_LJOSALFAR", 1)
						elif iCiv == Civ["Luchuirp"]:       trophy("TROPHY_VICTORY_LUCHUIRP", 1)
						elif iCiv == Civ["Malakim"]:        trophy("TROPHY_VICTORY_MALAKIM", 1)
						elif iCiv == Civ["Mazatl"]:         trophy("TROPHY_VICTORY_MAZATL", 1)
						elif iCiv == Civ["Mechanos"]:       trophy("TROPHY_VICTORY_MECHANOS", 1)
						elif iCiv == Civ["Mercurians"]:     trophy("TROPHY_VICTORY_MERCURIANS", 1)
						elif iCiv == Civ["Scions"]:         trophy("TROPHY_VICTORY_SCIONS", 1)
						elif iCiv == Civ["Sheaim"]:         trophy("TROPHY_VICTORY_SHEAIM", 1)
						elif iCiv == Civ["Sidar"]:          trophy("TROPHY_VICTORY_SIDAR", 1)
						elif iCiv == Civ["Svartalfar"]:     trophy("TROPHY_VICTORY_SVARTALFAR", 1)

						if   iVic == Victory["Altar"]: 		trophy("TROPHY_VICTORY_ALTAR_OF_THE_LUONNOTAR", 1)
						elif iVic == Victory["Conquest"]:	trophy("TROPHY_VICTORY_CONQUEST", 1)
						elif iVic == Victory["Cultural"]:	trophy("TROPHY_VICTORY_CULTURAL", 1)
						elif iVic == Victory["Domination"]:	trophy("TROPHY_VICTORY_DOMINATION", 1)
						elif iVic == Victory["Religious"]:	trophy("TROPHY_VICTORY_RELIGIOUS", 1)
						elif iVic == Victory["Score"]:		trophy("TROPHY_VICTORY_SCORE", 1)
						elif iVic == Victory["Time"]:		trophy("TROPHY_VICTORY_TIME", 1)
						elif iVic == Victory["Tower"]:		trophy("TROPHY_VICTORY_TOWER_OF_MASTERY", 1)

						if Option["Barbarian World"]: 		trophy("TROPHY_VICTORY_BARBARIAN_WORLD", 1)
						if Option["Cut Losers"]:			trophy("TROPHY_VICTORY_FINAL_FIVE", 1)
						if Option["High to Low"]:			trophy("TROPHY_VICTORY_HIGH_TO_LOW", 1)
						if Option["Increasing Difficulty"]:	trophy("TROPHY_VICTORY_INCREASING_DIFFICULTY", 1)

			victoryInfo = gc.getVictoryInfo(int(iVic))
			CvUtil.pyPrint("Victory!  Team %d achieves a %s victory"
				%(iTeam, victoryInfo.getDescription()))

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onVictory']:
			module.onVictory(self, argsList)

		## Modular Python End
		## *******************

	def onVassalState(self, argsList):
		'Vassal State'
		iMaster, iVassal, bVassal = argsList
		gc = CyGlobalContext()

		if (bVassal):
			CvUtil.pyPrint("Team %d becomes a Vassal State of Team %d"
				%(iVassal, iMaster))
		else:
			CvUtil.pyPrint("Team %d revolts and is no longer a Vassal State of Team %d"
				%(iVassal, iMaster))
		getPlayer = gc.getPlayer
#FF: Added by Jean Elcard 03/01/2009 (State Names)
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pPlayer = getPlayer(iPlayer)
			if pPlayer.isAlive():
				if (pPlayer.getTeam() == iMaster) or (pPlayer.getTeam() == iVassal):
					print "Update State Name for %d." % iPlayer
					print "Vassal: %s" % gc.getTeam(pPlayer.getTeam()).isAVassal()
					pPlayer.updateStateNameType()
#FF: End Add

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onVassalState']:
			module.onVassalState(self, argsList)

		## Modular Python End
		## *******************

	def onGameUpdate(self, argsList):
		'sample generic event, called on each game turn slice'
		genericArgs = argsList[0][0]	# tuple of tuple of my args
		turnSlice = genericArgs[0]

		doDeferredCalls()

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onGameUpdate']:
			module.onGameUpdate(self, argsList)

		## Modular Python End
		## *******************

		# Added by Gerikes for OOS logging.
		if CyInterface().isOOSVisible():
			CyMessageControl().sendModNetMessage(CvUtil.AutoPlay, 0, -1, -1, -1)
			OOSLogger.doGameUpdate()
		# End added by Gerikes for OOS logging.

	def onMouseEvent(self, argsList):
		'mouse handler - returns 1 if the event was consumed'
		eventType,mx,my,px,py,interfaceConsumed,screens = argsList
		if ( px!=-1 and py!=-1 ):
			if ( eventType == self.EventLButtonDown ):
				if (self.bAllowCheats and self.bCtrl and self.bAlt and CyMap().plot(px,py).isCity() and not interfaceConsumed):
					# Launch Edit City Event
					self.beginEvent( CvUtil.EventEditCity, (px,py) )
					return 1

				elif (self.bAllowCheats and self.bCtrl and self.bShift and not interfaceConsumed):
					# Launch Place Object Event
					self.beginEvent( CvUtil.EventPlaceObject, (px, py) )
					return 1

		if ( eventType == self.EventBack ):
			return CvScreensInterface.handleBack(screens)
		elif ( eventType == self.EventForward ):
			return CvScreensInterface.handleForward(screens)

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['onMouseEvent']:
			module.onMouseEvent(self, argsList)

		## Modular Python End
		## *******************

		return 0


#################### TRIGGERED EVENTS ##################

	def __eventEditCityNameBegin(self, city, bRename):
		popup = PyPopup.PyPopup(CvUtil.EventEditCityName, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((city.getID(), bRename))
		popup.setHeaderString(CyTranslator().getText("TXT_KEY_NAME_CITY", ()))
		popup.setBodyString(CyTranslator().getText("TXT_KEY_SETTLE_NEW_CITY_NAME", ()))
		popup.createEditBox(city.getName())
		popup.setEditBoxMaxCharCount( 15 )
		popup.launch()

	def __eventEditCityNameApply(self, playerID, userData, popupReturn):
		'Edit City Name Event'
		iCityID = userData[0]
		bRename = userData[1]
		player = CyGlobalContext().getPlayer(playerID)
		city = player.getCity(iCityID)
		cityName = popupReturn.getEditBoxString(0)
		if (len(cityName) > 30):
			cityName = cityName[:30]
		city.setName(cityName, not bRename)

	def __eventEditCityBegin(self, argsList):
		'Edit City Event'
		px,py = argsList
		CvWBPopups.CvWBPopups().initEditCity(argsList)

	def __eventEditCityApply(self, playerID, userData, popupReturn):
		'Edit City Event Apply'
		if (getChtLvl() > 0):
			CvWBPopups.CvWBPopups().applyEditCity( (popupReturn, userData) )

	def __eventPlaceObjectBegin(self, argsList):
		'Place Object Event'
		CvDebugTools.CvDebugTools().initUnitPicker(argsList)

	def __eventPlaceObjectApply(self, playerID, userData, popupReturn):
		'Place Object Event Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyUnitPicker( (popupReturn, userData) )

	def __eventAwardTechsAndGoldBegin(self, argsList):
		'Award Techs & Gold Event'
		CvDebugTools.CvDebugTools().cheatTechs()

	def __eventAwardTechsAndGoldApply(self, playerID, netUserData, popupReturn):
		'Award Techs & Gold Event Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyTechCheat( (popupReturn) )

	def __eventShowWonderBegin(self, argsList):
		'Show Wonder Event'
		CvDebugTools.CvDebugTools().wonderMovie()

	def __eventShowWonderApply(self, playerID, netUserData, popupReturn):
		'Wonder Movie Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyWonderMovie( (popupReturn) )

	def __eventEditUnitNameBegin(self, argsList):
		pUnit = argsList
		popup = PyPopup.PyPopup(CvUtil.EventEditUnitName, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setUserData((pUnit.getID(),))
		popup.setBodyString(CyTranslator().getText("TXT_KEY_RENAME_UNIT", ()))
		popup.createEditBox(pUnit.getNameNoDesc())
		popup.launch()

	def __eventEditUnitNameApply(self, playerID, userData, popupReturn):
		'Edit Unit Name Event'
		iUnitID = userData[0]
		unit = CyGlobalContext().getPlayer(playerID).getUnit(iUnitID)
		newName = popupReturn.getEditBoxString(0)
		if (len(newName) > 25):
			newName = newName[:25]
		unit.setName(newName)
		if CyGame().GetWorldBuilderMode():
			WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeStats()
			WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeCurrentUnit()	

	def __eventWBAllPlotsPopupBegin(self, argsList):
		CvScreensInterface.getWorldBuilderScreen().allPlotsCB()
		return

	def __eventWBAllPlotsPopupApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() >= 0):
			CvScreensInterface.getWorldBuilderScreen().handleAllPlotsCB(popupReturn)
		return

	def __eventWBLandmarkPopupBegin(self, argsList):
		CvScreensInterface.getWorldBuilderScreen().setLandmarkCB("")
		#popup = PyPopup.PyPopup(CvUtil.EventWBLandmarkPopup, EventContextTypes.EVENTCONTEXT_ALL)
		#popup.createEditBox(CyTranslator().getText("TXT_KEY_WB_LANDMARK_START", ()))
		#popup.launch()
		return

#	def __eventWBLandmarkPopupApply(self, playerID, userData, popupReturn):
#		if (popupReturn.getEditBoxString(0)):
#			szLandmark = popupReturn.getEditBoxString(0)
#			if (len(szLandmark)):
#				CvScreensInterface.getWorldBuilderScreen().setLandmarkCB(szLandmark)
#		return

#	def __eventWBScriptPopupBegin(self, argsList):
#		popup = PyPopup.PyPopup(CvUtil.EventWBScriptPopup, EventContextTypes.EVENTCONTEXT_ALL)
#		popup.setHeaderString(CyTranslator().getText("TXT_KEY_WB_SCRIPT", ()))
#		popup.createEditBox(CvScreensInterface.getWorldBuilderScreen().getCurrentScript())
#		popup.launch()
#		return

	def __eventWBScriptPopupApply(self, playerID, userData, popupReturn):
		if (popupReturn.getEditBoxString(0)):
			szScriptName = popupReturn.getEditBoxString(0)
			CvScreensInterface.getWorldBuilderScreen().setScriptCB(szScriptName)
		return

	def __eventWBStartYearPopupBegin(self, argsList):
		popup = PyPopup.PyPopup(CvUtil.EventWBStartYearPopup, EventContextTypes.EVENTCONTEXT_ALL)
		popup.createSpinBox(0, "", CyGame().getStartYear(), 1, 5000, -5000)
		popup.launch()
		return

	def __eventWBStartYearPopupApply(self, playerID, userData, popupReturn):
		iStartYear = popupReturn.getSpinnerWidgetValue(int(0))
		CvScreensInterface.getWorldBuilderScreen().setStartYearCB(iStartYear)
		return

	def __eventSetHasTraitBegin(self, argslist):
		return 0

	def __eventSetHasTraitApply(self, playerID, userData, popupReturn):
		iPlayer, iTrait, bHas = userData
		gc		= CyGlobalContext()
		pPlayer	= CyGlobalContext().getPlayer(iPlayer)
		if not gc.isNoCrash():
			pPlayer.setHasTrait(iTrait, bHas,-1,True,True)
		else:
			pPlayer.setHasTrait(iTrait, bHas)
		return 0

	def __eventSetTurnsAutoPlayBegin(self, argslist):
		return 0

	def __eventSetTurnsAutoPlayApply(self, playerID, userData, popupReturn):
		if popupReturn.getButtonClicked() == 0: # ok button
			sEditBoxContent = popupReturn.getEditBoxString(0)
			if sEditBoxContent.isdigit():
				iNumTurns = int(sEditBoxContent)
				# AI Autoplay Sounds by Grey Fox
				profile = CyUserProfile()
				SoundSettings["SOUND_MASTER_VOLUME"] 	= profile.getMasterVolume()
				SoundSettings["SOUND_SPEECH_VOLUME"] 	= profile.getSpeechVolume()
				SoundSettings["SOUND_MASTER_NO_SOUND"] 	= profile.isMasterNoSound()
				profile.setMasterNoSound(True)
				# End
				CyMessageControl().sendModNetMessage(CvUtil.AutoPlay, iNumTurns, -1, -1, -1)
		return 0

	def __eventSetUnitPerTileBegin(self, argslist):
		return 0

	def __eventSetUnitPerTileApply(self, playerID, userData, popupReturn):
		if (popupReturn.getButtonClicked() == 0 or popupReturn.getButtonClicked() == 1): # Okay/Lock buttons
			sEditBoxContent = popupReturn.getEditBoxString(0)
			if sEditBoxContent.isdigit():
				iNumUPT = int(sEditBoxContent)
				bLock = False
				if popupReturn.getButtonClicked() == 1:
					bLock = True
				CyMessageControl().sendModNetMessage(CvUtil.UPT, iNumUPT, bLock, -1, -1)
		return 0

## FfH Card Game: begin
	def __EventSelectSolmniumPlayerBegin(self):
		gc = CyGlobalContext()
		game = CyGame()
		iHUPlayer = game.getActivePlayer()
		getPlayer = gc.getPlayer
		getLeaderHeadInfo = gc.getLeaderHeadInfo
		localText = CyTranslator()

		if iHUPlayer == -1 : return 0
		if not cs.canStartGame(iHUPlayer) : return 0

		popup = PyPopup.PyPopup(CvUtil.EventSelectSolmniumPlayer, EventContextTypes.EVENTCONTEXT_ALL)

		sResText = CyUserProfile().getResolutionString(CyUserProfile().getResolution())
		sX, sY = sResText.split("x")
		iXRes = int(sX)
		iYRes = int(sY)

		iW = 620
		iH = 650

		popup.setSize(iW, iH)
		popup.setPosition((iXRes - iW) / 2, 30)

		lStates = []
		startMPGame = cs.getStartGameMPWith
		startAIGame = cs.getStartGameAIWith
		for iPlayer in xrange(gc.getMAX_CIV_PLAYERS()) :
			pPlayer = getPlayer(iPlayer)

			if pPlayer.isNone() : continue

			if pPlayer.isHuman() :
				lPlayerState = startMPGame(iHUPlayer, iPlayer)
				if lPlayerState[0][0] in ["No", "notMet"] : continue
				lStates.append([iPlayer, lPlayerState])
			else :
				lPlayerState = startAIGame(iHUPlayer, iPlayer)
				if lPlayerState[0][0] in ["No", "notMet"] : continue
				lStates.append([iPlayer, lPlayerState])

		lPlayerButtons = []

		popup.addDDS(CyArtFileMgr().getInterfaceArtInfo("SOMNIUM_POPUP_INTRO").getPath(), 0, 0, 512, 128)
		popup.addSeparator()
		#popup.setHeaderString(localText.getText("TXT_KEY_SOMNIUM_START", ()), CvUtil.FONT_CENTER_JUSTIFY)
		if len(lStates) == 0 :
			popup.setBodyString(localText.getText("TXT_KEY_SOMNIUM_NOONE_MET", ()))
			sText = u""
		else :
			#popup.setBodyString(localText.getText("TXT_KEY_SOMNIUM_PLAY_WITH", ()))
			popup.addSeparator()
			popup.addSeparator()

			sText = u""
			for iPlayer, lPlayerState in lStates :
				pPlayer 		= getPlayer(iPlayer)
				sPlayerName 	= pPlayer.getName()
				eType 			= pPlayer.getLeaderType()
				getMemory 		= getLeaderHeadInfo(eType).getMemoryAttitudePercent
				iPositiveChange = getMemory(MemoryTypes.MEMORY_SOMNIUM_POSITIVE) / 100
				iNegativeChange = getMemory(MemoryTypes.MEMORY_SOMNIUM_NEGATIVE) / 100
				bShift = True

				for item in lPlayerState :

					sTag = item[0]
					if (sTag == "atWar") :
						if len(sText) > 0 : sText += localText.getText("[NEWLINE]", ())
						sText += localText.getText("TXT_KEY_SOMNIUM_AT_WAR", (sPlayerName, ))

					elif (sTag == "InGame") :
						if len(sText) > 0 : sText += localText.getText("[NEWLINE]", ())
						sText += localText.getText("TXT_KEY_SOMNIUM_IN_GAME", (sPlayerName, ))

					elif (sTag == "relation") :
						delay = item[1]
						if (delay > 0) :
								if len(sText) > 0 : sText += localText.getText("[NEWLINE]", ())
								sText += localText.getText("TXT_KEY_SOMNIUM_GAME_DELAYED", (sPlayerName, delay))
						else :
								if bShift :
										bShift = False
										popup.addSeparator()
								popup.addButton(localText.getText("TXT_KEY_SOMNIUM_GAME_RELATION", (sPlayerName, iPositiveChange, iNegativeChange)))
								lPlayerButtons.append((iPlayer, -1))

					elif (sTag == "gold") :
						for iGold in item[1] :
							if bShift :
								bShift = False
								popup.addSeparator()
							if iGold == 0 :
								popup.addButton(localText.getText("TXT_KEY_SOMNIUM_GAME_FUN", (sPlayerName, )))
								lPlayerButtons.append((iPlayer, iGold))
							else :
								popup.addButton(localText.getText("TXT_KEY_SOMNIUM_GAME_GOLD", (sPlayerName, iGold)))
								lPlayerButtons.append((iPlayer, iGold))

		if len(sText) > 0 :
			popup.addSeparator()
			popup.addSeparator()
			popup.setBodyString(sText)

		popup.setUserData(tuple(lPlayerButtons))
		popup.launch()

	def __EventSelectSolmniumPlayerApply(self, playerID, userData, popupReturn):
		gc = CyGlobalContext()
		game = CyGame()
		if userData :
			idButtonCliked = popupReturn.getButtonClicked()
			if idButtonCliked in xrange(len(userData)) :
				iOpponent, iGold = userData[idButtonCliked]
				gc = CyGlobalContext()
				pLeftPlayer = gc.getPlayer(playerID)
				pRightPlayer = gc.getPlayer(iOpponent)

				if not pRightPlayer.isHuman() :
					if (cs.canStartGame(playerID)) and (pLeftPlayer.isAlive()) and (pRightPlayer.isAlive()) :
						cs.startGame(playerID, iOpponent, iGold)
					else :
						CyInterface().addMessage(playerID, True, 25, CyTranslator().getText("TXT_KEY_SOMNIUM_CANT_START_GAME", (gc.getPlayer(iOpponent).getName(), )), '', 1, '', ColorTypes(7), -1, -1, False, False)
				else :
					if (cs.canStartGame(playerID)) and (cs.canStartGame(iOpponent)) and (pLeftPlayer.isAlive()) and (pRightPlayer.isAlive()) :
						if (iOpponent == game.getActivePlayer()):
							self.__EventSolmniumAcceptGameBegin((playerID, iOpponent, iGold))
					else :
						CyInterface().addMessage(playerID, True, 25, CyTranslator().getText("TXT_KEY_SOMNIUM_CANT_START_GAME", (gc.getPlayer(iOpponent).getName(), )), '', 1, '', ColorTypes(7), -1, -1, False, False)

	def __EventSolmniumAcceptGameBegin(self, argslist):
		iPlayer, iOpponent, iGold = argslist
		gc = CyGlobalContext()
		if not gc.getPlayer(iOpponent).isAlive() : return 0

		popup = PyPopup.PyPopup(CvUtil.EventSolmniumAcceptGame, EventContextTypes.EVENTCONTEXT_ALL)

		popup.setUserData(argslist)

		popup.setHeaderString(CyTranslator().getText("TXT_KEY_SOMNIUM_START", ()))
		if iGold > 0 :
			popup.setBodyString(CyTranslator().getText("TXT_KEY_SOMNIUM_ACCEPT_GAME", (gc.getPlayer(iPlayer).getName(), iGold)))
		else :
			popup.setBodyString(CyTranslator().getText("TXT_KEY_SOMNIUM_ACCEPT_GAME_FUN", (gc.getPlayer(iPlayer).getName(), )))

		popup.addButton( CyTranslator().getText("AI_DIPLO_ACCEPT_1", ()) )
		popup.addButton( CyTranslator().getText("AI_DIPLO_NO_PEACE_3", ()) )

		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __EventSolmniumAcceptGameApply(self, playerID, userData, popupReturn):
		gc = CyGlobalContext()
		if userData :
			iPlayer, iOpponent, iGold = userData
			idButtonCliked = popupReturn.getButtonClicked()
			if idButtonCliked == 0 :
				if (cs.canStartGame(iPlayer)) and (cs.canStartGame(iOpponent)) and (gc.getPlayer(iPlayer).isAlive()) and (gc.getPlayer(iOpponent).isAlive()) :
					cs.startGame(iPlayer, iOpponent, iGold)
				else :
					CyInterface().addMessage(iPlayer, True, 25, CyTranslator().getText("TXT_KEY_SOMNIUM_CANT_START_GAME", (gc.getPlayer(iOpponent).getName(), )), '', 1, '', ColorTypes(7), -1, -1, False, False)
					CyInterface().addMessage(iOpponent, True, 25, CyTranslator().getText("TXT_KEY_SOMNIUM_CANT_START_GAME", (gc.getPlayer(iPlayer).getName(), )), '', 1, '', ColorTypes(7), -1, -1, False, False)
			else :
				CyInterface().addMessage(iPlayer, True, 25, CyTranslator().getText("TXT_KEY_SOMNIUM_REFUSE_GAME", (gc.getPlayer(iOpponent).getName(), iGold)), '', 1, '', ColorTypes(7), -1, -1, False, False)

	def __EventSolmniumConcedeGameBegin(self, argslist):
		popup = PyPopup.PyPopup(CvUtil.EventSolmniumConcedeGame, EventContextTypes.EVENTCONTEXT_ALL)

		popup.setUserData(argslist)

		popup.setHeaderString( CyTranslator().getText("TXT_KEY_SOMNIUM_START", ()))
		popup.setBodyString( CyTranslator().getText("TXT_KEY_SOMNIUM_CONCEDE_GAME", ()))

		popup.addButton( CyTranslator().getText("AI_DIPLO_ACCEPT_1", ()) )
		popup.addButton( CyTranslator().getText("AI_DIPLO_NO_PEACE_3", ()) )

		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __EventSolmniumConcedeGameApply(self, playerID, userData, popupReturn):
		if userData :
			idButtonCliked = popupReturn.getButtonClicked()
			if idButtonCliked == 0 :
				cs.endGame(userData[0], userData[1])
## FfH Card Game: end
	def __eventCheatEventBegin(self, argsList):
		'Cheat Event'
		CvDebugTools.CvDebugTools().cheatEvents()
    
	def __eventCheatEventApply(self, playerID, netUserData, popupReturn):
		'Cheat Event Apply'
		if (getChtLvl() > 0):
			CvDebugTools.CvDebugTools().applyCheatEvent( (popupReturn) )

## Platy Builder ##

	def __eventWBPlayerScriptPopupApply(self, playerID, userData, popupReturn):
		gc = CyGlobalContext()
		sScript = popupReturn.getEditBoxString(0)
		gc.getPlayer(userData[0]).setScriptData(CvUtil.convertToStr(sScript))
		WBPlayerScreen.WBPlayerScreen().placeScript()
		return

	def __eventWBCityScriptPopupApply(self, playerID, userData, popupReturn):
		gc = CyGlobalContext()
		sScript = popupReturn.getEditBoxString(0)
		pCity = gc.getPlayer(userData[0]).getCity(userData[1])
		pCity.setScriptData(CvUtil.convertToStr(sScript))
		WBCityEditScreen.WBCityEditScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
		return

	def __eventWBUnitScriptPopupApply(self, playerID, userData, popupReturn):
		gc = CyGlobalContext()
		sScript = popupReturn.getEditBoxString(0)
		pUnit = gc.getPlayer(userData[0]).getUnit(userData[1])
		pUnit.setScriptData(CvUtil.convertToStr(sScript))
		WBUnitScreen.WBUnitScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
		return

	def __eventWBScriptPopupBegin(self):
		return

	def __eventWBGameScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		CyGame().setScriptData(CvUtil.convertToStr(sScript))
		WBGameDataScreen.WBGameDataScreen(CvPlatyBuilderScreen.CvWorldBuilderScreen()).placeScript()
		return

	def __eventWBPlotScriptPopupApply(self, playerID, userData, popupReturn):
		sScript = popupReturn.getEditBoxString(0)
		pPlot = CyMap().plot(userData[0], userData[1])
		pPlot.setScriptData(CvUtil.convertToStr(sScript))
		WBPlotScreen.WBPlotScreen().placeScript()
		return

	def __eventWBLandmarkPopupApply(self, playerID, userData, popupReturn):
		gc = CyGlobalContext()
		sScript = popupReturn.getEditBoxString(0)
		pPlot = CyMap().plot(userData[0], userData[1])
		iPlayer = userData[2]
		if userData[3] > -1:
			pSign = CyEngine().getSignByIndex(userData[3])
			iPlayer = pSign.getPlayerType()
			CyEngine().removeSign(pPlot, iPlayer)
		if len(sScript):
			if iPlayer == gc.getBARBARIAN_PLAYER():
				CyEngine().addLandmark(pPlot, CvUtil.convertToStr(sScript))
			else:
				CyEngine().addSign(pPlot, iPlayer, CvUtil.convertToStr(sScript))
		WBPlotScreen.iCounter = 10
		return
## Platy Builder ##

	def __eventReminderBegin(self, argsList):
		popup = PyPopup.PyPopup(CvUtil.EventReminder, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(CyTranslator().getText("TXT_KEY_REMINDER_HEADER", ()))
		popup.createSpinBox(0, "", 0, 1, 100, 0)
		popup.createEditBox("", 1)
		szText = ""
		if self.reminders:
			szText = CyTranslator().getText("TXT_KEY_REMINDER_ACTIVE", ()) + "\n"
		for i in range(len(self.reminders)):
			szText += CyTranslator().getText("TXT_KEY_UNITSTATS_TURN", ()) + " %d: " % (self.reminders[i][0] + 1)
			szText += self.reminders[i][1] + "\n"
		popup.setBodyString(szText)
		popup.addButton(CyTranslator().getText("TXT_KEY_REMINDER_CLEAR_LIST", ()))
		popup.launch()

	def __eventReminderApply(self, playerID, userData, popupReturn):
		gc = CyGlobalContext()
		if popupReturn.getSpinnerWidgetValue(0) > 0:
			reminderTurn = popupReturn.getSpinnerWidgetValue(0) + gc.getGame().getGameTurn()
			reminderText = popupReturn.getEditBoxString(1)
			newEntry = (reminderTurn, reminderText)
			if gc.getGame().isGameMultiPlayer():
				self.reminders.append(newEntry)
			else:
				lReminders = SdToolKitAdvanced.sdGetGlobal("reminders","list")
				if lReminders:
					lReminders.append(newEntry)
				else:
					lReminders = [newEntry]
				SdToolKitAdvanced.sdSetGlobal("reminders", "list", lReminders)
				self.reminders = lReminders
		if popupReturn.getButtonClicked() == 0:
			del self.reminders[:]
			if not gc.getGame().isGameMultiPlayer():
				SdToolKitAdvanced.sdDelGlobal("reminders","list")
