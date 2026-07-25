## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Implementaion of miscellaneous game functions

import CvUtil
from CvPythonExtensions import *
from BasicFunctions import *
import CvEventInterface
import ScenarioFunctions

## *******************
## Modular Python: ANW 16-feb-2010
##                     29-may-2010
##                     20-aug-2010
## ArcticNightWolf on CivFanatics
## ArcticNightWolf@gmail.com

# For dynamic plugin loading
import imp    # dynamic importing of libraries
#import glob   # Unix style pathname pattern expansion
import os
import CvPath # path to current assets
import inspect

# Maps modules to the function name
# Syntax: {'functionName': [module1, module2]}
command = {}

# functionList is a list of strings of functions we will directly map
functionList = ['isVictoryTest', 'isVictory', 'isPlayerResearch', 'getExtraCost', 'createBarbarianCities', 'createBarbarianUnits', 'createBarbarianBosses',
 'skipResearchPopup', 'showTechChooserButton', 'getFirstRecommendedTech', 'getSecondRecommendedTech', 'canRazeCity', 'canDeclareWar', 'skipProductionPopup',
 'showExamineCityButton', 'getRecommendedUnit', 'getRecommendedBuilding', 'updateColoredPlots', 'isActionRecommended', 'unitCannotMoveInto', 'cannotHandleAction',
 'canBuild', 'cannotFoundCity', 'cannotSelectionListMove', 'cannotSelectionListGameNetMessage', 'cannotDoControl', 'canResearch', 'cannotResearch', 'canDoCivic',
 'cannotDoCivic', 'canTrain', 'cannotTrain', 'canConstruct', 'cannotConstruct', 'canCreate', 'cannotCreate', 'canMaintain', 'cannotMaintain', 'AI_chooseTech',
 'AI_chooseProduction', 'AI_unitUpdate', 'AI_doWar', 'AI_doDiplo', 'calculateScore', 'doHolyCity', 'doHolyCityTech', 'doGold', 'doResearch', 'doGoody', 'doGrowth',
 'cannotGrow', 'cannotStarve', 'cannotSpreadReligionHere', 'doProduction', 'doCulture', 'doPlotCulture', 'doReligion', 'cannotSpreadReligion', 'doGreatPeople',
 'doMeltdown', 'doReviveActivePlayer', 'doPillageGold', 'doCityCaptureGold', 'citiesDestroyFeatures', 'canFoundCitiesOnWater', 'doCombat', 'getConscriptUnitType',
 'getCityFoundValue', 'canPickPlot', 'getUnitCostMod', 'getBuildingCostMod', 'canUpgradeAnywhere', 'getWidgetHelp', 'getUpgradePriceOverride', 'getExperienceNeeded']

## Modular Python End
## *******************

class CvGameUtils:
	"Miscellaneous game functions"
	def __init__(self):

		## *******************
		## Modular Python: ANW 29-may-2010

		self.pluginScan()

		## Modular Python End
		## *******************

		pass

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

		for pathToMLF in MLFlist:
			for modules in os.listdir(pathToMLF):
				pathToModuleRoot = pathToMLF+modules+"\\"
				# Ignore all xml files
				if modules.lower()[-4:] != ".xml":
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

	def isVictoryTest(self):		#Return False to prevent testing for Victory
		## modified: estyles 25-Oct-2010 to allow this function to be modular

		if ( CyGame().getElapsedGameTurns() <= 10 ):
			return False

		## *******************
		## Modular Python: estyles 25-Oct-2010

		for module in command['isVictoryTest']:
			if not module.isVictoryTest(self):
				return False

		## Modular Python End
		## *******************

		return True

	def isVictory(self, argsList):		#Return True to grant the Tested Team a Victory.  If more than 1 team gains Victory in a single turn, a single winner is selected randomly
		eVictory = argsList[0]
		Manager	= CvEventInterface.getEventManager()
		if eVictory == Manager.Victories["Gone to Hell"]: return False

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['isVictory']:
			if not module.isVictory(self, argsList):
				return False

		## Modular Python End
		## *******************

		return True

	def isPlayerResearch(self, argsList):
		ePlayer = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['isPlayerResearch']:
			if not module.isPlayerResearch(self, argsList):
				return False

		## Modular Python End
		## *******************

		return True

	def getExtraCost(self, argsList):
		ePlayer = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		modularReturn = 0
		for module in command['getExtraCost']:
			modularReturn += module.getExtraCost(self, argsList)
		return modularReturn

		## Modular Python End
		## *******************

		#return 0

	def createBarbarianCities(self):

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['createBarbarianCities']:
			if module.createBarbarianCities(self):
				return True

		## Modular Python End
		## *******************

		return False

	def createBarbarianUnits(self):

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['createBarbarianUnits']:
			if module.createBarbarianUnits(self):
				return True

		## Modular Python End
		## *******************

		return False

	def createBarbarianBosses(self, argsList):
		pPlot = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['createBarbarianBosses']:
			if module.createBarbarianBosses(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def skipResearchPopup(self,argsList):
		ePlayer = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['skipResearchPopup']:
			if module.skipResearchPopup(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def showTechChooserButton(self,argsList):
		ePlayer = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['showTechChooserButton']:
			if not module.showTechChooserButton(self, argsList):
				return False

		## Modular Python End
		## *******************

		return True

	def getFirstRecommendedTech(self,argsList):
		ePlayer = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getFirstRecommendedTech']:
			modularReturn = module.getFirstRecommendedTech(self, argsList)
			if modularReturn != TechTypes.NO_TECH:
				return modularReturn

		## Modular Python End
		## *******************

		return TechTypes.NO_TECH

	def getSecondRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		eFirstTech = argsList[1]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getSecondRecommendedTech']:
			modularReturn = module.getSecondRecommendedTech(self, argsList)
			if modularReturn != TechTypes.NO_TECH:
				return modularReturn

		## Modular Python End
		## *******************

		return TechTypes.NO_TECH

	def canRazeCity(self,argsList):
		iRazingPlayer, pCity = argsList

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canRazeCity']:
			if not module.canRazeCity(self, argsList):
				return False

		## Modular Python End
		## *******************

		return True

	def canDeclareWar(self,argsList):
		iAttackingTeam, iDefendingTeam = argsList

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canDeclareWar']:
			if not module.canDeclareWar(self, argsList):
				return False

		## Modular Python End
		## *******************

		return True

	def skipProductionPopup(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['skipProductionPopup']:
			if module.skipProductionPopup(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def showExamineCityButton(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['showExamineCityButton']:
			if not module.showExamineCityButton(self, argsList):
				return False

		## Modular Python End
		## *******************

		return True

	def getRecommendedUnit(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getRecommendedUnit']:
			modularReturn = module.getRecommendedUnit(self, argsList)
			if modularReturn != UnitTypes.NO_UNIT:
				return modularReturn

		## Modular Python End
		## *******************

		return UnitTypes.NO_UNIT

	def getRecommendedBuilding(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getRecommendedBuilding']:
			modularReturn = module.getRecommendedBuilding(self, argsList)
			if modularReturn != BuildingTypes.NO_BUILDING:
				return modularReturn

		## Modular Python End
		## *******************

		return BuildingTypes.NO_BUILDING

	def updateColoredPlots(self):

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['updateColoredPlots']:
			if module.updateColoredPlots(self):
				return True

		## Modular Python End
		## *******************

		return False

	def isActionRecommended(self,argsList):
		pUnit = argsList[0]
		iAction = argsList[1]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['isActionRecommended']:
			if module.isActionRecommended(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def unitCannotMoveInto(self,argsList):
		ePlayer = argsList[0]
		iUnitId = argsList[1]
		iPlotX = argsList[2]
		iPlotY = argsList[3]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['unitCannotMoveInto']:
			if module.unitCannotMoveInto(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotHandleAction(self,argsList):
		pPlot = argsList[0]
		iAction = argsList[1]
		bTestVisible = argsList[2]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotHandleAction']:
			if module.cannotHandleAction(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def canBuild(self,argsList):
		iX, iY, iBuild, iPlayer = argsList
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		eCiv 		= pPlayer.getCivilizationType()
		Manager		= CvEventInterface.getEventManager()

		if eCiv == Manager.Civilizations["Scions"] and iBuild == Manager.Builds["Farm"]:
			pPlot = CyMap().plot(iX, iY)
			if pPlot.getBonusType(-1) in (Manager.Resources["Wheat"], Manager.Resources["Corn"], Manager.Resources["Rice"]): return -1
			else: return 0

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canBuild']:
			modularReturn = module.canBuild(self, argsList)
			if modularReturn != -1:
				return modularReturn

		## Modular Python End
		## *******************

		return -1	# Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can

	def cannotFoundCity(self,argsList):
		#This python call has been turned off.
		#Settling on mana will remove the mana, as it used to.
		#The No Settlers option is now handled in the DLL.
		iPlayer, iPlotX, iPlotY = argsList
		gc = CyGlobalContext()
		pPlot = CyMap().plot(iPlotX,iPlotY)
		Manager		= CvEventInterface.getEventManager()
		Civ			= Manager.Civilizations
		Option		= Manager.GameOptions
		Resource	= Manager.Resources

# scions start
		pPlayer = gc.getPlayer(iPlayer)

		if Option["No Settlers"]:
			if pPlayer.getCivilizationType() == Civ["Scions"]:
				if pPlayer.getNumCities() > 0:
					return True
# scions end

		if pPlot.getBonusType(-1) == Resource["Mana"]:
			return True

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotFoundCity']:
			if module.cannotFoundCity(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotSelectionListMove(self,argsList):
		pPlot	= argsList[0]
		bAlt	= argsList[1]
		bShift	= argsList[2]
		bCtrl	= argsList[3]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotSelectionListMove']:
			if module.cannotSelectionListMove(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotSelectionListGameNetMessage(self,argsList):
		eMessage	= argsList[0]
		iData2		= argsList[1]
		iData3		= argsList[2]
		iData4		= argsList[3]
		iFlags		= argsList[4]
		bAlt		= argsList[5]
		bShift		= argsList[6]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotSelectionListGameNetMessage']:
			if module.cannotSelectionListGameNetMessage(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotDoControl(self,argsList):
		eControl = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotDoControl']:
			if module.cannotDoControl(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def canResearch(self,argsList):
		ePlayer	= argsList[0]
		eTech	= argsList[1]
		bTrade	= argsList[2]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canResearch']:
			if module.canResearch(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotResearch(self,argsList):
		ePlayer		= argsList[0]
		eTech		= argsList[1]
		bTrade		= argsList[2]
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(ePlayer)
		sf			= ScenarioFunctions.ScenarioFunctions()
		Manager		= CvEventInterface.getEventManager()
		eCiv		= pPlayer.getCivilizationType()
		bAgnostic	= pPlayer.isAgnostic()

		if   eTech == Manager.Techs["Orders from Heaven"]:
			if Manager.GameOptions["No Order"]:				return True
			if bAgnostic:									return True

		elif eTech == Manager.Techs["White Hand"]:
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_7): return True
			if bAgnostic:									return True

		elif eTech == Manager.Techs["Way of the Earthmother"]:
			if Manager.GameOptions["No RoK"]:				return True
			if bAgnostic:									return True

		elif eTech == Manager.Techs["Way of the Forests"]:
			if Manager.GameOptions["No Leaves"]:			return True
			if bAgnostic:									return True

		elif eTech == Manager.Techs["Message from the Deep"]:
			if Manager.GameOptions["No OO"]:				return True
			if bAgnostic:									return True

		elif eTech == Manager.Techs["Corruption of Spirit"]:
			if Manager.GameOptions["No Veil"]:				return True
			if bAgnostic:									return True

		elif eTech == Manager.Techs["Honor"]:
			if Manager.GameOptions["No Empy"]:				return True
			if bAgnostic:									return True

		elif eTech == Manager.Techs["Deception"]:
			if Manager.GameOptions["No Esus"]:				return True
			if bAgnostic:									return True

		elif eTech == Manager.Techs["Seafaring"]:
			if eCiv != Manager.Civilizations["Lanun"]:		return True

		elif eTech == Manager.Techs["Steam Power"]:
			if eCiv != Manager.Civilizations["Mechanos"]:	return True

		elif eTech == Manager.Techs["Alchemy"]:
			if eCiv != Manager.Civilizations["Mechanos"] and gc.getInfoTypeForString("MODULE_SILVER_CIRCLE") == -1: return True

		elif eTech == Manager.Techs["Swampdwelling"]:		return True

		elif eTech == Manager.Techs["The Gift"]:			return True

		if CyGame().getWBMapScript():
			bBlock = sf.cannotResearch(ePlayer, eTech, bTrade)
			if bBlock:
				return True

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotResearch']:
			if module.cannotResearch(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def canDoCivic(self,argsList):
		ePlayer	= argsList[0]
		eCivic	= argsList[1]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canDoCivic']:
			if module.canDoCivic(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotDoCivic(self,argsList):
		ePlayer		= argsList[0]
		eCivic		= argsList[1]
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(ePlayer)
		eCiv		= pPlayer.getCivilizationType()
		Manager		= CvEventInterface.getEventManager()
		eCivicType	= gc.getCivicInfo(eCivic).getCivicOptionType()

		if eCiv == Manager.Civilizations["Jotnar"]:
			if eCivicType == Manager.Civics["Government"]:
				if eCivic != Manager.Civics["Traditions"]:	return True
		
		if eCiv == gc.getInfoTypeForString("CIVILIZATION_MECHANOS") and gc.getInfoTypeForString("MODULE_VCIVICS") != -1:
			if eCivic == gc.getInfoTypeForString("CIVIC_MAGOCRACY"): return True

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotDoCivic']:
			if module.cannotDoCivic(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def canTrain(self,argsList):
		pCity			= argsList[0]
		eUnit			= argsList[1]
		bContinue		= argsList[2]
		bTestVisible	= argsList[3]
		bIgnoreCost		= argsList[4]
		bIgnoreUpgrades	= argsList[5]
		gc				= CyGlobalContext()
		ePlayer			= pCity.getOwner()
		pPlayer			= gc.getPlayer(ePlayer)
		eUnitClass		= gc.getUnitInfo(eUnit).getUnitClassType()
		Manager			= CvEventInterface.getEventManager()

		if Manager.GameOptions["One City Challenge"]:
			if pPlayer.getCivilizationType() == Manager.Civilizations["Scions"]:
				if eUnitClass == Manager.UnitClasses["Awakened"]:
					if pCity.getNumRealBuilding(Manager.Buildings["Scions Palace"]) > 0:
						return True
				if eUnitClass == Manager.UnitClasses["Reborn"]:
					if pCity.getNumRealBuilding(Manager.Buildings["Cathedral of Rebirth"]) > 0:
						return True

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canTrain']:
			if module.canTrain(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotTrain(self,argsList):
		pCity			= argsList[0]
		eUnit			= argsList[1]
		bContinue		= argsList[2]
		bTestVisible	= argsList[3]
		bIgnoreCost		= argsList[4]
		bIgnoreUpgrades	= argsList[5]
		gc				= CyGlobalContext()
		pPlayer			= gc.getPlayer(pCity.getOwner())
		sf				= ScenarioFunctions.ScenarioFunctions()
		eCiv			= pPlayer.getCivilizationType()
		Manager			= CvEventInterface.getEventManager()

		if   eUnit == Manager.Units["Veil"]["Beast of Agares"]:
			if pCity.getPopulation() <= 5: return True

		elif eUnit in (Manager.Units["Generic"]["Worker"], Manager.Units["Generic"]["Settler"], Manager.Units["Generic"]["Workboat"]):
			if pPlayer.isCivic(Manager.Civics["Crusade"]): return True

		elif eUnit == Manager.Units["Cualli"]["Shadow Priest of Agruonn"]:
			if not CyGame().isUnitClassMaxedOut(Manager.Heroes["Class-Miquiztli"], 0): return True

		elif eUnit == Manager.Heroes["Acheron"]:
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ACHERON): return True

		elif eUnit == Manager.Heroes["Duin"]:
			if Manager.GameOptions["No Duin"]: return True
			for iPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iPlayer)
				if pLoopPlayer.getLeaderType() == Manager.Leaders["Duin"] and pLoopPlayer.isAlive(): return True

		elif eUnit == Manager.Heroes["Varulv"]:
			if pPlayer.getLeaderType() != Manager.Leaders["Duin"]: return True

		elif eUnit in (Manager.Units["Malakim"]["Horseman"], Manager.Units["Malakim"]["Knight"], Manager.Units["Malakim"]["Camel Archer"]):
			if eCiv == Manager.Civilizations["Malakim"]:
				if pCity.getNumRealBuilding(Manager.Buildings["Camel Stable"]) == 0 and pCity.getNumRealBuilding(Manager.Buildings["Stable"]) == 0: return True

		if CyGame().getWBMapScript():
			bBlock = sf.cannotTrain(pCity, eUnit, bContinue, bTestVisible, bIgnoreCost, bIgnoreUpgrades)
			if bBlock: return True

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['cannotTrain']:
			if module.cannotTrain(self, argsList) == True:
				return True

		## Modular Python End
		## *******************

		return False

	def canConstruct(self,argsList):
		pCity			= argsList[0]
		eBuilding		= argsList[1]
		bContinue		= argsList[2]
		bTestVisible	= argsList[3]
		bIgnoreCost		= argsList[4]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canConstruct']:
			if module.canConstruct(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotConstruct(self,argsList):
		pCity			= argsList[0]
		eBuilding		= argsList[1]
		bContinue		= argsList[2]
		bTestVisible	= argsList[3]
		bIgnoreCost		= argsList[4]
		gc				= CyGlobalContext()
		pPlayer			= gc.getPlayer(pCity.getOwner())
		bAI				= pPlayer.isHuman() == False
		eCiv			= pPlayer.getCivilizationType()
		Manager			= CvEventInterface.getEventManager()

		if   eBuilding in (	Manager.Buildings["Alchemy Lab"],		Manager.Buildings["Aqueduct"],		Manager.Buildings["Brewery"],
							Manager.Buildings["Carnival"],			Manager.Buildings["Courthouse"],	Manager.Buildings["Elder Council"],
							Manager.Buildings["Gambling House"],	Manager.Buildings["Granary"],		Manager.Buildings["Harbor"],
							Manager.Buildings["Herbalist"],			Manager.Buildings["Library"],		Manager.Buildings["Market"],
							Manager.Buildings["Moneychanger"],		Manager.Buildings["Public Baths"],	Manager.Buildings["Smokehouse"],
							Manager.Buildings["Theatre"] ):
			if pPlayer.isCivic(Manager.Civics["Crusade"]): return True

		elif eBuilding in (Manager.Buildings["Camel Stable"], Manager.Buildings["Stable"]):
			if eCiv == Manager.Civilizations["Malakim"]:
				if pCity.getNumBuilding(Manager.Buildings["Stable"]) > 0 or pCity.getNumBuilding(Manager.Buildings["Camel Stable"]) > 0: return True

		elif eBuilding == Manager.Buildings["Imperial Cenotaph"]:
			if pPlayer.getLeaderType() == Manager.Leaders["Risen Emperor"]: return True

		elif eBuilding == Manager.Buildings["Mercurian Gate"]:
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_HYBOREM_OR_BASIUM): return True
			if pPlayer.getStateReligion() == Manager.Religions["Ashen Veil"]: return True
			if pCity.isCapital() and not pCity.getCivilizationType() == Manager.Civilizations["Mercurians"]: return True

		elif eBuilding == Manager.Buildings["Monument to Avarice"]:
			if pPlayer.isFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL):
				if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_KAHD_MAMMON")): return False
			return True

		elif eBuilding == Manager.Buildings["Shrine of the Champion"]:
			iHero = Manager.cf.getHero(pPlayer)
			if iHero == -1: return True
			if CyGame().isUnitClassMaxedOut(iHero, 0) == False: return True
			if pPlayer.getUnitClassCount(iHero) > 0: return True

		elif eBuilding == Manager.Buildings["Siege Workshop"]:
			if eCiv in (Manager.Civilizations["Ljosalfar"], Manager.Civilizations["Svartalfar"]): return True
			if not pPlayer.isHasTech(Manager.Techs["Construction"]): return True

		elif eBuilding == Manager.Buildings["Smugglers Port"]:
			if pPlayer.isSmugglingRing() == False: return True

		elif eBuilding == Manager.Buildings["Temple of the Gift"]:
			if pPlayer.getLeaderType() == Manager.Leaders["Korrina"]: return True

		elif eBuilding == Manager.Buildings["Vacant Mausoleum"]:
			if pPlayer.getLeaderType() == Manager.Leaders["Risen Emperor"]: return True

		elif eBuilding == Manager.Buildings["Kahdi Vault Gate"]:
			if pPlayer.getLeaderType() != Manager.Leaders["Kahd"]: return True

		elif eBuilding == gc.getInfoTypeForString("BUILDING_RIDE_OF_THE_NINE_KINGS"):
			if not (pCity.hasBonus(gc.getInfoTypeForString("BONUS_HYAPON")) or pCity.hasBonus(gc.getInfoTypeForString("BONUS_HORSE")) or pCity.hasBonus(gc.getInfoTypeForString("BONUS_NIGHTMARE"))): return True

		if gc.getInfoTypeForString("MODULE_DAO") != -1:
			if   eBuilding==gc.getInfoTypeForString("BUILDING_SHRINE_AIR"):
				if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_SHRINE_EARTH"))>0:
					return True
			elif eBuilding==gc.getInfoTypeForString("BUILDING_SHRINE_EARTH"):
				if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_SHRINE_AIR"))>0:
					return True
			elif eBuilding==gc.getInfoTypeForString("BUILDING_SHRINE_WATER"):
				if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_SHRINE_FIRE"))>0:
					return True
			elif eBuilding==gc.getInfoTypeForString("BUILDING_SHRINE_FIRE"):
				if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_SHRINE_WATER"))>0:
					return True
					
		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotConstruct']:
			if module.cannotConstruct(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def canCreate(self,argsList):
		pCity			= argsList[0]
		eProject		= argsList[1]
		bContinue		= argsList[2]
		bTestVisible	= argsList[3]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canCreate']:
			if module.canCreate(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotCreate(self,argsList):
		pCity			= argsList[0]
		eProject		= argsList[1]
		bContinue		= argsList[2]
		bTestVisible	= argsList[3]
		gc				= CyGlobalContext()
		pPlayer			= gc.getPlayer(pCity.getOwner())
		pTeam			= gc.getTeam(pPlayer.getTeam())
		bAI				= not pPlayer.isHuman()
		eCiv			= pPlayer.getCivilizationType()
		iReligion		= pPlayer.getStateReligion()
		Manager			= CvEventInterface.getEventManager()

		if   eProject == Manager.Projects["Purge the Unfaithful"]:
			if bAI: return True # this means AIs never cast this ritual. (even if they're aiming for religious victory) TODO update AI
			if iReligion == -1: return True

		elif eProject == Manager.Projects["Birthright Regained"]:
			if not pPlayer.isFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL): return True

		elif eProject == Manager.Projects["Stir From Slumber"]:
			if (pPlayer.getPlayersKilled() == 0 or iReligion != Manager.Religions["White Hand"]): return True

		elif eProject == Manager.Projects["The Deepening"]:
			if iReligion != Manager.Religions["White Hand"]: return True

		elif eProject == Manager.Projects["The Draw"]:
			if pPlayer.getLeaderType() == Manager.Leaders["Raitlor"]: return True
			if bAI and pPlayer.getUnitClassCount(Manager.Heroes["Class-Auric"]) == 0 and pPlayer.getUnitClassCount(Manager.Heroes["Class-Auric Winter"]) == 0: return True

		elif eProject == Manager.Projects["Ascension"]:
			if pPlayer.getLeaderType() == Manager.Leaders["Raitlor"]: return True
			if eCiv == Manager.Civilizations["Illians"]:
				if pPlayer.getUnitClassCount(Manager.Heroes["Class-Auric"]) == 0 and pPlayer.getUnitClassCount(Manager.Heroes["Class-Auric Winter"]) == 0: return True 

# TODO Ronkhar: split and move to frozen module (here = if genesis and civ illians. In module = if genesis and civ frozen)
		elif eProject == Manager.Projects["Genesis"]:															#Changed in Frozen: TC01
			if eCiv in (Manager.Civilizations["Illians"], Manager.Civilizations["Frozen"]): return True

# TODO Ronkhar: move liberation to frozen module
		elif eProject == Manager.Projects["Liberation"]:
			if Manager.GameOptions["No Liberation"]: return True
			if pPlayer.getAlignment() == Manager.Alignments["Good"]: return True

		elif eProject == Manager.Projects["Pax Diabolis"]:
			if iReligion != Manager.Religions["Ashen Veil"] or not pTeam.isAtWar(gc.getDEMON_TEAM()): return True
			if bAI and (pCity.getPopulation() > 10 or pCity.isCapital() or pCity.isHolyCity()): return True

		elif eProject == Manager.Projects["Prepare Expedition"]:
			if pPlayer.isFeatAccomplished(FeatTypes.FEAT_EXPEDITION_READY): return True

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotCreate']:
			if module.cannotCreate(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def canMaintain(self,argsList):
		pCity		= argsList[0]
		eProcess	= argsList[1]
		bContinue	= argsList[2]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canMaintain']:
			if module.canMaintain(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotMaintain(self,argsList):
		pCity		= argsList[0]
		eProcess	= argsList[1]
		bContinue	= argsList[2]
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(pCity.getOwner())
		Manager		= CvEventInterface.getEventManager()

		# Caste System Requires the civic
		if eProcess == Manager.Processes["Caste System"] :
			if not pPlayer.isCivic(Manager.Civics["Caste System"]):			return True

		# Wealth is automatically upgraded with the Taxation technology
		if eProcess == Manager.Processes["Wealth"]:
			if pPlayer.isHasTech(Manager.Techs["Taxation"]):				return True

		# Culture rate improved by running Liberty
		if eProcess == Manager.Processes["Culture Improved"]:
			if not pPlayer.isCivic(Manager.Civics["Liberty"]):				return True

		if eProcess == Manager.Processes["Culture"]:
			if pPlayer.isCivic(Manager.Civics["Liberty"]):					return True

		# Research rate conversion more effective with Academy
		if eProcess == Manager.Processes["Research"]:
			if pCity.getNumRealBuilding(Manager.Buildings["Academy"]) > 0:	return True

		if eProcess == Manager.Processes["Research Improved"]:
			if pCity.getNumRealBuilding(Manager.Buildings["Academy"]) <= 0:	return True

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotMaintain']:
			if module.cannotMaintain(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def AI_chooseTech(self,argsList):
		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['AI_chooseTech']:
			modularReturn = module.AI_chooseTech(self, argsList)
			if modularReturn != TechTypes.NO_TECH:
				return modularReturn

		## Modular Python End
		## *******************

		return TechTypes.NO_TECH

	def AI_chooseProduction(self,argsList):

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['AI_chooseProduction']:
			if module.AI_chooseProduction(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def AI_unitUpdate(self,argsList):
		pUnit 		= argsList[0]
		iOwner		= pUnit.getOwner()
		gc			= CyGlobalContext()
		pPlot 		= pUnit.plot()
		eUnitType	= pUnit.getUnitType()
		eUnitClass	= pUnit.getUnitClassType()
		iNumUnits	= pPlot.getNumUnits()
		bAnimal		= pUnit.isAnimal()
		Manager		= CvEventInterface.getEventManager()

		if eUnitClass == Manager.UnitClasses["Giant Spider"]:
			iX = pUnit.getX(); iY = pUnit.getY()
			if pPlot.isOwned():	return 0
			getPlot = CyMap().plot
			for iiX,iiY in RANGE1:
				pLoopPlot = getPlot(iX+iiX,iY+iiY)
				for i in xrange(pLoopPlot.getNumUnits()):
					if pLoopPlot.getUnit(i).getOwner() != iOwner: return 0
			return 1

		if eUnitType == Manager.Heroes["Acheron"]:
			if pPlot.isVisibleEnemyUnit(iOwner):
				pUnit.cast(gc.getInfoTypeForString('SPELL_BREATH_FIRE'))

		if not isLimitedUnitClass(eUnitClass):
			iImprovement = pPlot.getImprovementType()
			if iImprovement != -1 and not pUnit.isHurt():
				if   iImprovement in (Manager.Lairs["Barrow"], Manager.Lairs["Ruins"], Manager.Improvements["Hellfire"]):
					if not bAnimal:
						if iNumUnits - pPlot.getNumAnimalUnits() == 1:	return 1
				elif iImprovement in (Manager.Lairs["Bear Den"], Manager.Lairs["Lion Den"]):
					if bAnimal:
						if pPlot.getNumAnimalUnits() == 1:				return 1
				elif iImprovement == Manager.Lairs["Goblin Camp"]:
					if not bAnimal:
						if iNumUnits - pPlot.getNumAnimalUnits() <= 3:	return 1

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['AI_unitUpdate']:
			if module.AI_unitUpdate(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def AI_doWar(self,argsList):
		pTeam = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['AI_doWar']:
			if module.AI_doWar(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def AI_doDiplo(self,argsList):
		ePlayer = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['AI_doDiplo']:
			if module.AI_doDiplo(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def calculateScore(self,argsList):
		ePlayer		= argsList[0]
		bFinal		= argsList[1]
		bVictory	= argsList[2]
		gc			= CyGlobalContext()
		scoreComp	= CvUtil.getScoreComponent
		pPlayer		= gc.getPlayer(ePlayer)
		game		= CyGame()
		getDefINT	= gc.getDefineINT

		iPopulationScore	= scoreComp(pPlayer.getPopScore(), game.getInitPopulation(), game.getMaxPopulation(), getDefINT("SCORE_POPULATION_FACTOR"), True, bFinal, bVictory)
		iLandScore			= scoreComp(pPlayer.getLandScore(), game.getInitLand(), game.getMaxLand(), getDefINT("SCORE_LAND_FACTOR"), True, bFinal, bVictory)
		iTechScore			= scoreComp(pPlayer.getTechScore(), game.getInitTech(), game.getMaxTech(), getDefINT("SCORE_TECH_FACTOR"), True, bFinal, bVictory)
		iWondersScore		= scoreComp(pPlayer.getWondersScore(), game.getInitWonders(), game.getMaxWonders(), getDefINT("SCORE_WONDER_FACTOR"), False, bFinal, bVictory)

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		modularScore = 0
		for module in command['calculateScore']:
			modularScore += module.calculateScore(self, argsList)

		## Modular Python End
		## *******************

		return int(iPopulationScore + iLandScore + iWondersScore + iTechScore + modularScore)

	def doHolyCity(self):

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doHolyCity']:
			if module.doHolyCity(self):
				return True

		## Modular Python End
		## *******************

		return False

	def doHolyCityTech(self,argsList):
		pTeam	= argsList[0]
		ePlayer	= argsList[1]
		eTech	= argsList[2]
		bFirst	= argsList[3]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doHolyCityTech']:
			if module.doHolyCityTech(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doGold(self,argsList):
		ePlayer = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doGold']:
			if module.doGold(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doResearch(self,argsList):
		ePlayer = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doResearch']:
			if module.doResearch(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doGoody(self,argsList):
		ePlayer	= argsList[0]
		pPlot	= argsList[1]
		pUnit	= argsList[2]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doGoody']:
			if module.doGoody(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doGrowth(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doGrowth']:
			if module.doGrowth(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotGrow(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotGrow']:
			if module.cannotGrow(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotStarve(self,argsList):
		pCity = argsList[0]
		## modified: estyles 24-Oct-2010

		## *******************
		## Modular Python: ANW 29-may-2010

		for module in command['cannotStarve']:
			if module.cannotStarve(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotSpreadReligionHere(self,argsList):
		pCity	= argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotSpreadReligionHere']:
			if module.cannotSpreadReligionHere(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doProduction(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doProduction']:
			if module.doProduction(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doCulture(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doCulture']:
			if module.doCulture(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doPlotCulture(self,argsList):
		pCity			= argsList[0]
		bUpdate			= argsList[1]
		ePlayer			= argsList[2]
		iCultureRate	= argsList[3]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doPlotCulture']:
			if module.doPlotCulture(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doReligion(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doReligion']:
			if module.doReligion(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def cannotSpreadReligion(self,argsList):
		iOwner, iUnitID, iReligion, iX, iY = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['cannotSpreadReligion']:
			if module.cannotSpreadReligion(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doGreatPeople(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doGreatPeople']:
			if module.doGreatPeople(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doMeltdown(self,argsList):
		pCity = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doMeltdown']:
			if module.doMeltdown(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doReviveActivePlayer(self,argsList):
		"allows you to perform an action after an AIAutoPlay"
		iPlayer = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doReviveActivePlayer']:
			if module.doReviveActivePlayer(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doPillageGold(self, argsList):
		"controls the gold result of pillaging"
		pPlot			= argsList[0]
		pUnit			= argsList[1]
		gc				= CyGlobalContext()
		eImprovement	= pPlot.getImprovementType()
		iPillage		= gc.getImprovementInfo(eImprovement).getPillageGold()

		iPillageGold  = 0
		iPillageGold  = CyGame().getSorenRandNum(iPillage, "Pillage Gold 1")
		iPillageGold += CyGame().getSorenRandNum(iPillage, "Pillage Gold 2")
		iPillageGold += (pUnit.getPillageChange() * iPillageGold) / 100

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doPillageGold']:
			iPillageGold += module.doPillageGold(self, argsList)

		## Modular Python End
		## *******************

		return iPillageGold

	def doCityCaptureGold(self, argsList):
		"controls the gold result of capturing a city"
		pOldCity		= argsList[0]
		gc				= CyGlobalContext()
		iGameTurn		= CyGame().getGameTurn()

		iCaptureGold  = 0
		iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
		iCaptureGold += pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION")
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1")
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2")

		iGoldMaxTurns = gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")

		if (iGoldMaxTurns > 0):
			iCaptureGold *= cyIntRange((iGameTurn - pOldCity.getGameTurnAcquired()), 0, gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"))
			iCaptureGold /= iGoldMaxTurns

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doCityCaptureGold']:
			iCaptureGold += module.doCityCaptureGold(self, argsList)

		## Modular Python End
		## *******************

		return iCaptureGold

	def citiesDestroyFeatures(self,argsList):
		iX, iY= argsList

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['citiesDestroyFeatures']:
			if not module.citiesDestroyFeatures(self, argsList):
				return False

		## Modular Python End
		## *******************

		return True

	def canFoundCitiesOnWater(self,argsList):
		iX, iY= argsList

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canFoundCitiesOnWater']:
			if module.canFoundCitiesOnWater(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def doCombat(self,argsList):
		pSelectionGroup, pDestPlot = argsList

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['doCombat']:
			if module.doCombat(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False

	def getConscriptUnitType(self, argsList):
		iPlayer = argsList[0]
		iConscriptUnitType = -1 #return this with the value of the UNIT TYPE you want to be conscripted, -1 uses default system

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getConscriptUnitType']:
			modularReturn = module.getConscriptUnitType(self, argsList)
			if modularReturn != -1:
				return modularReturn

		## Modular Python End
		## *******************

		return iConscriptUnitType

	def getCityFoundValue(self, argsList):
		iPlayer, iPlotX, iPlotY = argsList
		iFoundValue = -1 # Any value besides -1 will be used

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getCityFoundValue']:
			modularReturn = module.getCityFoundValue(self, argsList)
			if modularReturn != -1:
				iFoundValue += modularReturn

		## Modular Python End
		## *******************

		return iFoundValue

	def canPickPlot(self, argsList):
		pPlot = argsList[0]

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canPickPlot']:
			if not module.canPickPlot(self, argsList):
				return False

		## Modular Python End
		## *******************

		return True

	def getUnitCostMod(self, argsList):
		iPlayer, iUnit = argsList
		iCostMod = -1 # Any value > 0 will be used

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getUnitCostMod']:
			modularReturn = module.getUnitCostMod(self, argsList)
			if modularReturn > 0:
				iCostMod += modularReturn

		## Modular Python End
		## *******************

		return iCostMod

	def getBuildingCostMod(self, argsList):
		iPlayer, iCityID, iBuilding = argsList
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(iPlayer)
		pCity	= pPlayer.getCity(iCityID)

		iCostMod = -1 # Any value > 0 will be used
		Manager		= CvEventInterface.getEventManager()
		Manager.verifyLoaded()
		Building	= Manager.Buildings

		if iBuilding == Building["Gambling House"]:
			if pPlayer.isGamblingRing():
				iCostMod = 25
		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getBuildingCostMod']:
			modularReturn = module.getBuildingCostMod(self, argsList)
			if modularReturn > 0:
				iCostMod += modularReturn

		## Modular Python End
		## *******************

		return iCostMod

	def canUpgradeAnywhere(self, argsList):
		pUnit = argsList

		#b should mean boolean, so why is this using an int, and why is it different from every other function in this file?
		#I'm going to change it for consistency - estyles
		#bCanUpgradeAnywhere = 0

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['canUpgradeAnywhere']:
			if module.canUpgradeAnywhere(self, argsList):
				return True

		## Modular Python End
		## *******************

		return False
		#below line removed and replaced with above for consistency
		#return bCanUpgradeAnywhere

	def getWidgetHelp(self, argsList):
		eWidgetType, iData1, iData2, bOption = argsList
		gc = CyGlobalContext()
		# DynTraits Start
		if eWidgetType == WidgetTypes.WIDGET_PYTHON:
			if iData1 == 8001:
				return CyTranslator().getText("TXT_KEY_DYN_TRAITS",())
                # DynTraits End
			if iData1 == 1001: return CyTranslator().getText("TXT_KEY_CONCEPT_BUILDINGS",())
			if iData1 == 1002: return CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS",())
			if iData1 == 1003: return CyTranslator().getText("TXT_KEY_PEDIA_EFFECTS",())
			if iData1 == 1004: return CyTranslator().getText("TXT_KEY_HEADING_TRADEROUTE_LIST",())
			if iData1 == 1005: return CyTranslator().getText("TXT_KEY_TRAINING_LABEL",())
			if iData1 == 1006:
				pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
				if pHeadSelectedUnit.isRevealed():
					return CyTranslator().getText("TXT_KEY_UNIT_REVEALED",())
				else:
					return CyTranslator().getText("TXT_KEY_UNIT_HIDDEN",())
			if iData1 == 1007: return CyTranslator().getText("TXT_KEY_PROMOTION_HIDDEN_NATIONALITY",())
			if iData1 == 1008:
				pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
				iUC = pHeadSelectedUnit.getUnitCombatType()
				szUCDecription = gc.getUnitCombatInfo(iUC).getDescription()
				return szUCDecription

## Religion Screen ##
		if eWidgetType == WidgetTypes.WIDGET_HELP_RELIGION:
			if iData1 == -1:
				return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
## Platy WorldBuilder ##
		elif eWidgetType == WidgetTypes.WIDGET_PYTHON:
			if iData1 == 1027:
				return CyTranslator().getText("TXT_KEY_WB_PLOT_DATA",())
			elif iData1 == 1028:
				return gc.getGameOptionInfo(iData2).getHelp()
			elif iData1 == 1029:
				if iData2 == 0:
					sText = CyTranslator().getText("TXT_KEY_WB_PYTHON", ())
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onFirstContact"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onChangeWar"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onVassalState"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityAcquired"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCityBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCultureExpansion"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGoldenAge"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onEndGoldenAge"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onGreatPersonBorn"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlayerChangeStateReligion"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionFounded"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionSpread"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onReligionRemove"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationFounded"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationSpread"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onCorporationRemove"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitCreated"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitLost"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onUnitPromoted"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onBuildingBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onProjectBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onTechAcquired"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onImprovementDestroyed"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onRouteBuilt"
					sText += "\n" + CyTranslator().getText("[ICON_BULLET]", ()) + "onPlotRevealed"
					return sText
				elif iData2 == 1:
					return CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA",())
				elif iData2 == 2:
					return CyTranslator().getText("TXT_KEY_WB_TEAM_DATA",())
				elif iData2 == 3:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH",())
				elif iData2 == 4:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT",())
				elif iData2 == 5:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ())
				elif iData2 == 6:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION",())
				elif iData2 == 7:
					return CyTranslator().getText("TXT_KEY_WB_CITY_DATA2",())
				elif iData2 == 8:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING",())
				elif iData2 == 9:
					return "Platy Builder\nVersion: 4.17b"
				elif iData2 == 10:
					return CyTranslator().getText("TXT_KEY_CONCEPT_EVENTS",())
				elif iData2 == 11:
					return CyTranslator().getText("TXT_KEY_WB_RIVER_PLACEMENT",())
				elif iData2 == 12:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT",())
				elif iData2 == 13:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BONUS",())
				elif iData2 == 14:
					return CyTranslator().getText("TXT_KEY_WB_PLOT_TYPE",())
				elif iData2 == 15:
					return CyTranslator().getText("TXT_KEY_CONCEPT_TERRAIN",())
				elif iData2 == 16:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_ROUTE",())
				elif iData2 == 17:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_FEATURE",())
				elif iData2 == 18:
					return CyTranslator().getText("TXT_KEY_MISSION_BUILD_CITY",())
				elif iData2 == 19:
					return CyTranslator().getText("TXT_KEY_WB_ADD_BUILDINGS",())
				elif iData2 == 20:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_RELIGION",())
				elif iData2 == 21:
					return CyTranslator().getText("TXT_KEY_CONCEPT_CORPORATIONS",())
				elif iData2 == 22:
					return CyTranslator().getText("TXT_KEY_ESPIONAGE_CULTURE",())
				elif iData2 == 23:
					return CyTranslator().getText("TXT_KEY_PITBOSS_GAME_OPTIONS",())
				elif iData2 == 24:
					return CyTranslator().getText("TXT_KEY_WB_SENSIBILITY",())
				elif iData2 == 25:
					return CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PLOT_EFFECT",())
				elif iData2 == 27:
					return CyTranslator().getText("TXT_KEY_WB_ADD_UNITS",())
				elif iData2 == 28:
					return CyTranslator().getText("TXT_KEY_WB_TERRITORY",())
				elif iData2 == 29:
					return CyTranslator().getText("TXT_KEY_WB_ERASE_ALL_PLOTS",())
				elif iData2 == 30:
					return CyTranslator().getText("TXT_KEY_WB_REPEATABLE",())
				elif iData2 == 31:
					return CyTranslator().getText("TXT_KEY_PEDIA_HIDE_INACTIVE", ())
				elif iData2 == 32:
					return CyTranslator().getText("TXT_KEY_WB_STARTING_PLOT", ())
				elif iData2 == 33:
					return CyTranslator().getText("TXT_KEY_INFO_SCREEN", ())
				elif iData2 == 34:
					return CyTranslator().getText("TXT_KEY_CONCEPT_TRADE", ())
			elif iData1 > 1029 and iData1 < 1040:
				if iData1 %2:
					return "-"
				return "+"
			elif iData1 == 1041:
				return CyTranslator().getText("TXT_KEY_WB_KILL",())
			elif iData1 == 1042:
				return CyTranslator().getText("TXT_KEY_MISSION_SKIP",())
			elif iData1 == 1043:
				if iData2 == 0:
					return CyTranslator().getText("TXT_KEY_WB_DONE",())
				elif iData2 == 1:
					return CyTranslator().getText("TXT_KEY_WB_FORTIFY",())
				elif iData2 == 2:
					return CyTranslator().getText("TXT_KEY_WB_WAIT",())
			elif iData1 == 6785:
				return CyGameTextMgr().getProjectHelp(iData2, False, CyCity())
			elif iData1 == 6787:
				return gc.getProcessInfo(iData2).getDescription()
			elif iData1 == 6788:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return gc.getRouteInfo(iData2).getDescription()
			elif iData1 == 6789:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return gc.getPlotEffectInfo(iData2).getDescription()
## City Hover Text ##
			elif iData1 > 7199 and iData1 < 7300:
				iPlayer = iData1 - 7200
				pPlayer = gc.getPlayer(iPlayer)
				pCity = pPlayer.getCity(iData2)
				if CyGame().GetWorldBuilderMode():
					sText = "<font=3>"
					if pCity.isCapital():
						sText += CyTranslator().getText("[ICON_STAR]", ())
					elif pCity.isGovernmentCenter():
						sText += CyTranslator().getText("[ICON_SILVER_STAR]", ())
					sText += u"%s: %d<font=2>" %(pCity.getName(), pCity.getPopulation())
					sTemp = ""
					if pCity.isConnectedToCapital(iPlayer):
						sTemp += CyTranslator().getText("[ICON_TRADE]", ())
					for i in xrange(gc.getNumReligionInfos()):
						if pCity.isHolyCityByType(i):
							sTemp += u"%c" %(gc.getReligionInfo(i).getHolyCityChar())
						elif pCity.isHasReligion(i):
							sTemp += u"%c" %(gc.getReligionInfo(i).getChar())

					for i in xrange(gc.getNumCorporationInfos()):
						if pCity.isHeadquartersByType(i):
							sTemp += u"%c" %(gc.getCorporationInfo(i).getHeadquarterChar())
						elif pCity.isHasCorporation(i):
							sTemp += u"%c" %(gc.getCorporationInfo(i).getChar())
					if len(sTemp) > 0:
						sText += "\n" + sTemp

					iMaxDefense = pCity.getTotalDefense(False)
					if iMaxDefense > 0:
						sText += u"\n%s: " %(CyTranslator().getText("[ICON_DEFENSE]", ()))
						iCurrent = pCity.getDefenseModifier(False)
						if iCurrent != iMaxDefense:
							sText += u"%d/" %(iCurrent)
						sText += u"%d%%" %(iMaxDefense)

					sText += u"\n%s: %d/%d" %(CyTranslator().getText("[ICON_FOOD]", ()), pCity.getFood(), pCity.growthThreshold())
					iFoodGrowth = pCity.foodDifference(True)
					if iFoodGrowth != 0:
						sText += u" %+d" %(iFoodGrowth)

					if pCity.isProduction():
						sText += u"\n%s:" %(CyTranslator().getText("[ICON_PRODUCTION]", ()))
						if not pCity.isProductionProcess():
							sText += u" %d/%d" %(pCity.getProduction(), pCity.getProductionNeeded())
							iProduction = pCity.getCurrentProductionDifference(False, True)
							if iProduction != 0:
								sText += u" %+d" %(iProduction)
						sText += u" (%s)" %(pCity.getProductionName())

					iGPRate = pCity.getGreatPeopleRate()
					iProgress = pCity.getGreatPeopleProgress()
					if iGPRate > 0 or iProgress > 0:
						sText += u"\n%s: %d/%d %+d" %(CyTranslator().getText("[ICON_GREATPEOPLE]", ()), iProgress, pPlayer.greatPeopleThreshold(False), iGPRate)

					sText += u"\n%s: %d/%d (%s)" %(CyTranslator().getText("[ICON_CULTURE]", ()), pCity.getCulture(iPlayer), pCity.getCultureThreshold(), gc.getCultureLevelInfo(pCity.getCultureLevel()).getDescription())

					lTemp = []
					for i in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
						iAmount = pCity.getCommerceRateTimes100(i)
						if iAmount <= 0: continue
						sTemp = u"%d.%02d%c" %(pCity.getCommerceRate(i), pCity.getCommerceRateTimes100(i)%100, gc.getCommerceInfo(i).getChar())
						lTemp.append(sTemp)
					if len(lTemp) > 0:
						sText += "\n"
						for i in xrange(len(lTemp)):
							sText += lTemp[i]
							if i < len(lTemp) - 1:
								sText += ", "

					iMaintenance = pCity.getMaintenanceTimes100()
					if iMaintenance != 0:
						sText += "\n" + CyTranslator().getText("[COLOR_WARNING_TEXT]", ()) + CyTranslator().getText("INTERFACE_CITY_MAINTENANCE", ()) + " </color>"
						sText += u"-%d.%02d%c" %(iMaintenance/100, iMaintenance%100, gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar())

					lBuildings = []
					lWonders = []
					for i in xrange(gc.getNumBuildingInfos()):
						if pCity.isHasBuilding(i):
							Info = gc.getBuildingInfo(i)
							if isLimitedWonderClass(Info.getBuildingClassType()):
								lWonders.append(Info.getDescription())
							else:
								lBuildings.append(Info.getDescription())
					if len(lBuildings) > 0:
						lBuildings.sort()
						sText += "\n" + CyTranslator().getText("[COLOR_BUILDING_TEXT]", ()) + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_BUILDING", ()) + ": </color>"
						for i in xrange(len(lBuildings)):
							sText += lBuildings[i]
							if i < len(lBuildings) - 1:
								sText += ", "
					if len(lWonders) > 0:
						lWonders.sort()
						sText += "\n" + CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + CyTranslator().getText("TXT_KEY_CONCEPT_WONDERS", ()) + ": </color>"
						for i in xrange(len(lWonders)):
							sText += lWonders[i]
							if i < len(lWonders) - 1:
								sText += ", "
					sText += "</font>"
					return sText
## Religion Widget Text##
			elif iData1 == 7869:
				return CyGameTextMgr().parseReligionInfo(iData2, False)
## Building Widget Text##
			elif iData1 == 7870:
				return CyGameTextMgr().getBuildingHelp(iData2, False, False, False, None)
## Tech Widget Text##
			elif iData1 == 7871:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return CyGameTextMgr().getTechHelp(iData2, False, False, False, False, -1)
## Civilization Widget Text##
			elif iData1 == 7872:
				iCiv = iData2 % 10000
				return CyGameTextMgr().parseCivInfos(iCiv, False)
## Promotion Widget Text##
			elif iData1 == 7873:
				return CyGameTextMgr().getPromotionHelp(iData2, False)
## Feature Widget Text##
			elif iData1 == 7874:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				iFeature = iData2 % 10000
				return CyGameTextMgr().getFeatureHelp(iFeature, False)
## Terrain Widget Text##
			elif iData1 == 7875:
				return CyGameTextMgr().getTerrainHelp(iData2, False)
## Leader Widget Text##
			elif iData1 == 7876:
				iLeader = iData2 % 10000
				return CyGameTextMgr().parseLeaderTraits(iLeader, -1, False, False)
## Improvement Widget Text##
			elif iData1 == 7877:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return CyGameTextMgr().getImprovementHelp(iData2, False)
## Bonus Widget Text##
			elif iData1 == 7878:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return CyGameTextMgr().getBonusHelp(iData2, False)
## Specialist Widget Text##
			elif iData1 == 7879:
				return CyGameTextMgr().getSpecialistHelp(iData2, False)
## Yield Text##
			elif iData1 == 7880:
				return gc.getYieldInfo(iData2).getDescription()
## Commerce Text##
			elif iData1 == 7881:
				return gc.getCommerceInfo(iData2).getDescription()
## Build Text##
			elif iData1 == 7882:
				return gc.getBuildInfo(iData2).getDescription()
## Effect Text ##
			elif iData1 == 7883:
				return gc.getPlotEffectInfo(iData2).getDescription()
## Trait Text ##
			elif iData1 == 7884:
				return CyGameTextMgr().parseTraits(iData2, -1, False)
## Flag Text ##
			elif iData1 == 7885:
				return gc.getFlagInfo(iData2).getDescription()
## Corporation Screen ##
			elif iData1 == 8201:
				return CyGameTextMgr().parseCorporationInfo(iData2, False)
## Military Screen ##
			elif iData1 == 8202:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_PEDIA_ALL_UNITS", ())
				return CyGameTextMgr().getUnitHelp(iData2, False, False, False, None)
			elif iData1 > 8299 and iData1 < 8400:
				iPlayer = iData1 - 8300
				pUnit = gc.getPlayer(iPlayer).getUnit(iData2)
				sText = CyGameTextMgr().getSpecificUnitHelp(pUnit, True, False)
				if CyGame().GetWorldBuilderMode():
					sText += "\n" + CyTranslator().getText("TXT_KEY_WB_UNIT", ()) + " ID: " + str(iData2)
					sText += "\n" + CyTranslator().getText("TXT_KEY_WB_GROUP", ()) + " ID: " + str(pUnit.getGroupID())
					sText += "\n" + "X: " + str(pUnit.getX()) + ", Y: " + str(pUnit.getY())
					sText += "\n" + CyTranslator().getText("TXT_KEY_WB_AREA_ID", ()) + ": "  + str(pUnit.plot().getArea())
				return sText
## Civics Screen ##
			elif iData1 == 8205 or iData1 == 8206:
				sText = CyGameTextMgr().parseCivicInfo(iData2, False, True, False)
				if gc.getCivicInfo(iData2).getUpkeep() > -1:
					sText += "\n" + gc.getUpkeepInfo(gc.getCivicInfo(iData2).getUpkeep()).getDescription()
				else:
					sText += "\n" + CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
				return sText
## Ultrapack ##
			elif iData1 == 5001 or iData1 == 5002:
				szCommerce = gc.getCommerceInfo(iData2).getDescription()
				return CyTranslator().getText("TXT_KEY_COMMERCE_CHANGE", (szCommerce,))

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getWidgetHelp']:
			modularReturn = module.getWidgetHelp(self, argsList)
			if len(modularReturn) > 0:
				return modularReturn

		## Modular Python End
		## *******************

		return u""

	def getUpgradePriceOverride(self, argsList):
		iPlayer, iUnitID, iUnitTypeUpgrade = argsList

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getUpgradePriceOverride']:
			modularReturn = module.getUpgradePriceOverride(self, argsList)
			if modularReturn > 0:
				return modularReturn

		## Modular Python End
		## *******************

		return -1	# Any value 0 or above will be used

	def getExperienceNeeded(self, argsList):
		# use this function to set how much experience a unit needs
		iLevel, iOwner = argsList
		gc 		= CyGlobalContext()
		iExperienceNeeded = 0

		# regular epic game experience
		if iLevel < 13:
			iExperienceNeeded = iLevel * iLevel + 1
		else:
			iExperienceNeeded = 13*13+1 + (iLevel-13)*25
		iExperienceNeeded = iExperienceNeeded*100

		iModifier = gc.getPlayer(iOwner).getLevelExperienceModifier()
		if (0 != iModifier):
			iExperienceNeeded += (iExperienceNeeded * iModifier + 99) / 100   # ROUND UP

		## *******************
		## Modular Python: ANW 29-may-2010
		## modified: estyles 24-Oct-2010

		for module in command['getExperienceNeeded']:
			modularReturn = module.getExperienceNeeded(self, argsList)
			if modularReturn > 0:
				return modularReturn

		## Modular Python End
		## *******************

		return iExperienceNeeded
