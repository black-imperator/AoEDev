## Copyright (c) 2005-2006, Gillmer J. Derge.

## This file is part of Civilization IV Alerts mod.
##
## Civilization IV Alerts mod is free software; you can redistribute
## it and/or modify it under the terms of the GNU General Public
## License as published by the Free Software Foundation; either
## version 2 of the License, or (at your option) any later version.
##
## Civilization IV Alerts mod is distributed in the hope that it will
## be useful, but WITHOUT ANY WARRANTY; without even the implied
## warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Civilization IV Alerts mod; if not, write to the Free
## Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
## 02110-1301 USA

__version__ = "$Revision: 1.2 $"
# $Source: /usr/local/cvsroot/Civ4lerts/src/main/python/Civ4lerts.py,v $

## Civ4lerts
## This class extends the built in event manager and overrides various
## event handlers to display alerts about important game situations.
##
## [*] = Already implemented in the Civ4lerts mod
## [o] = Partially implemented in the Civ4lerts mod
## [x] = Already implemented in CivIV
## [?] = Not sure if this applies in CivIV
## 
## Golden Age turns left
## At Year 1000 B.C. (QSC Save Submission)
## Within 10 tiles of domination limit
## There is new technology for sale
## There is a new luxury resource for sale
## There is a new strategic resource for sale
## There is a new bonus resource for sale
## We can sell a technology
## We can sell a luxury resource
## We can sell a strategic resource
## We can sell a bonus resource
## [*] Rival has lots of cash
## [*] Rival has lots of cash per turn
## [x] Rival has changed civics
## Rival has entered a new Era
## Trade deal expires next turn
## [o] Enemy at war is willing to negotiate
## [x] There are foreign units in our territory
## City is about to riot or rioting
## [*] City has grown or shrunk
## City has shrunk
## [*] City is unhealthy
## [*] City is angry
## City specialists reassigned
## [*] City is about to grow
## City is about to starve
## [*] City is about to grow into unhealthyness
## [*] City is about to grow into anger
## City is in resistance
## [?] City is wasting food
## City is working unimproved tiles
## Disconnected resources in our territory
## City is about to produce a great person
## 
## Other:
## City is under cultural pressure

# < Revolution Mod Start >

# Replaced all uses of Bug Options etc with calls to config file

import CvConfigParser
config = CvConfigParser.CvConfigParser("Civ4lerts.ini")

bEnabled = config.getboolean("CIV4LERTS", "Enabled", True)
bCityPendingGrowth = config.getboolean("CIV4LERTS", "City Pending Growth", True)
bCityPendingHealth = config.getboolean("CIV4LERTS", "City Pending Healthiness", True)
bCityPendingHappy = config.getboolean("CIV4LERTS", "City Pending Happiness", True)
bCityGrowth = config.getboolean("CIV4LERTS", "City Growth", True)
bCityCrime = config.getboolean("CIV4LERTS", "City Crime", True)
bCityHealth = config.getboolean("CIV4LERTS", "City Healthiness", True)
bCityHappy = config.getboolean("CIV4LERTS", "City Happiness", True)
bHurryPop = config.getboolean("CIV4LERTS", "City Can Hurry Pop", True)
bHurryGold = config.getboolean("CIV4LERTS", "City Can Hurry Gold", True)
bGoldTrade = config.getboolean("CIV4LERTS", "Gold Trade", True)
iGoldTrade = config.getint("CIV4LERTS", "Gold Trade Threshold", 50)
bGoldPerTrade = config.getboolean("CIV4LERTS", "Gold Per Turn Trade", True)
iGoldPerTrade = config.getint("CIV4LERTS", "Gold Per Turn Threshold", 3)

# < Revolution Mod End >

class Civ4lerts:

	def __init__(self, eventManager):
		cityEvent = EndGameTurnCityAlertManager(eventManager)
		cityEvent.add(CityPendingGrowth(eventManager))
		cityEvent.add(CityGrowth(eventManager))
		cityEvent.add(CityCrime(eventManager))
		cityEvent.add(CityHealthiness(eventManager))
		cityEvent.add(CityHappiness(eventManager))
		cityEvent.add(CanHurryPopulation(eventManager))
		cityEvent.add(CanHurryGold(eventManager))
		
		GoldTrade(eventManager)
		GoldPerTurnTrade(eventManager)

from CvPythonExtensions import *

### Globals

gc = CyGlobalContext()
localText = CyTranslator()
game = CyGame()

# Must set alerts to "not immediate" to have icons show up
HEALTHY_ICON = "Art/Interface/Buttons/General/unhealthy_person.dds"
UNHEALTHY_ICON = "Art/Interface/Buttons/General/unhealthy_person.dds"

HAPPY_ICON = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"
UNHAPPY_ICON = "Art/Interface/mainscreen/cityscreen/angry_citizen.dds"


### Displaying alerts on-screen

def addMessageNoIcon(iPlayer, message):
	"Displays an on-screen message with no popup icon."
	addMessage(iPlayer, message, None, 0, 0)

def addMessageAtCity(iPlayer, message, icon, city):
	"Displays an on-screen message with a popup icon that zooms to the given city."
	addMessage(iPlayer, message, icon, city.getX(), city.getY())

def addMessageAtPlot(iPlayer, message, icon, plot):
	"Displays an on-screen message with a popup icon that zooms to the given plot."
	addMessage(iPlayer, message, icon, plot.getX(), plot.getY())

def addMessage(iPlayer, szString, szIcon, iFlashX, iFlashY):
	"Displays an on-screen message."
	eventMessageTimeLong = gc.getDefineINT("EVENT_MESSAGE_TIME_LONG")
	CyInterface().addMessage(iPlayer, True, eventMessageTimeLong,
							 szString, None, 0, szIcon, ColorTypes(-1),
							 iFlashX, iFlashY, True, True)


### Abstract and Core Classes

class AbstractStatefulAlert:
	"""
	Provides a base class and several convenience functions for 
	implementing an alert that retains state information between turns.
	"""
	def __init__(self, eventManager):
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)

	def onGameStart(self, argsList):
		self._init()
		self._reset()

	def onLoadGame(self, argsList):
		self._init()
		self._reset()
		return 0

	def _init(self):
		"Initializes globals that could not be done in __init__."
		pass

	def _reset(self):
		"Resets the state for this alert."
		pass

class EndGameTurnCityAlertManager(AbstractStatefulAlert):
	"""
	Triggered at the end of each game turn, this event loops over all of the
	active player's cities, passing each off to a set of alert checkers.
	
	This is like a mini event manager that triggers an EndGameTurn event
	for each city of the active player.
	
	All of the alerts are reset when the game is loaded or started.
	"""
	def __init__(self, eventManager):
		AbstractStatefulAlert.__init__(self, eventManager)
		eventManager.addEventHandler("cityAcquiredAndKept", self.onCityAcquiredAndKept)
		eventManager.addEventHandler("cityLost", self.onCityLost)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)
		self.alerts = []

	def add(self, alert):
		self.alerts.append(alert)
		if( game.isFinalInitialized() ) :
			alert.init()
			alert.reset()
	
	def onCityAcquiredAndKept(self, argsList):
		iPlayer, city = argsList
		if (iPlayer == gc.getGame().getActivePlayer()):
			self._resetCity(city)
	
	def onCityLost(self, argsList):
		'City Lost'
		city = argsList[0]
		iPlayer = gc.getGame().getActivePlayer()
		if (iPlayer == gc.getGame().getActivePlayer()):
			self._discardCity(city)
	
	def onEndGameTurn(self, argsList):
		"Loops over active player's cities, telling each to perform its check."
		iTurn = argsList[0]
		iPlayer = gc.getGame().getActivePlayer()
		player = gc.getActivePlayer()
		(pLoopCity, iter) = player.firstCity(False)
		while(pLoopCity):
			for alert in self.alerts:
				iCityID = pLoopCity.getID()
				alert.checkCity(iTurn, iCityID, pLoopCity, iPlayer, player)
			(pLoopCity, iter) = player.nextCity(iter, False)

	def _init(self):
		"Initializes each alert."
		for alert in self.alerts:
			alert.init()

	def _reset(self):
		"Resets each alert."
		for alert in self.alerts:
			alert.reset()

	def _resetCity(self, city):
		"tells each alert to check the state of the given city -- no alerts are displayed."
		for alert in self.alerts:
			alert.resetCity(city)

	def _discardCity(self, city):
		"tells each alert to discard the state of the given city."
		for alert in self.alerts:
			alert.discardCity(city)

class AbstractCityAlert:
	"""
	Tracks cities from turn-to-turn and checks each at the end of every game turn
	to see if the alert should be displayed.
	"""
	def __init__(self, eventManager):
		"Performs static initialization that doesn't require game data."
		pass
	
	def checkCity(self, iTurn, iCityID, city, iPlayer, player):
		"Checks the city, updates its tracked state and possibly displays an alert."
		pass
	
	def init(self):
		"Initializes globals that could not be done in __init__."
		pass
	
	def reset(self):
		"Clears state kept for each city."
		self._beforeReset()
		player	= gc.getActivePlayer()
		(pLoopCity, iter) = player.firstCity(False)
		while(pLoopCity):
			self.resetCity(pLoopCity)
			(pLoopCity, iter) = player.nextCity(iter, False)
	
	def _beforeReset(self):
		"Performs clearing of state before looping over cities."
		pass
	
	def resetCity(self, city):
		"Checks the city and updates its tracked state."
		pass
	
	def discardCity(self, city):
		"Discards the tracked state of the city."
		pass

class AbstractCityTestAlert(AbstractCityAlert):
	"""
	Extends the basic city alert by applying a boolean test to each city, tracking the results,
	and displaying an alert whenever a city switches or will switch state on the following turn.
	
	State: set of city IDs that pass the test.
	"""
	def __init__(self, eventManager):
		AbstractCityAlert.__init__(self, eventManager)
		
	def checkCity(self, iTurn, iCityID, city, iPlayer, player):
		message = None
		passes = self._passesTest(city)
		passed = iCityID in self.cities
		if (passes != passed):
			# City switched this turn, save new state and display an alert
			if (passes):
				self.cities.add(iCityID)
				if (self._isShowAlert(passes)):
					message, icon = self._getAlertMessageIcon(city, passes)
			else:
				self.cities.discard(iCityID)
				if (self._isShowAlert(passes)):
					message, icon = self._getAlertMessageIcon(city, passes)
		elif (self._isShowPendingAlert(passes)):
			# See if city will switch next turn
			willPass = self._willPassTest(city)
			if (passed != willPass):
				message, icon = self._getPendingAlertMessageIcon(city, willPass)
		if (message):
			addMessageAtCity(iPlayer, message, icon, city)
	
	def _passedTest(self, iCityID):
		"Returns true if the city passed the test last turn."
		return iCityID in self.cities

	def _passesTest(self, city):
		"Returns true if the city passes the test."
		return False

	def _willPassTest(self, city):
		"Returns true if the city will pass the test next turn based on current conditions."
		return False

	def _beforeReset(self):
		self.cities = set()
	
	def resetCity(self, city):
		if (self._passesTest(city)):
			self.cities.add(city.getID())
	
	def discardCity(self, city):
		self.cities.discard(city.getID())
	
	def _isShowAlert(self, passes):
		"Returns true if the alert is enabled."
		return False
	
	def _getAlertMessageIcon(self, city, passes):
		"Returns a tuple of the message and icon to use for the alert."
		return (None, None)
	
	def _isShowPendingAlert(self, passes):
		"Returns true if the alert is enabled."
		return False

	def _getPendingAlertMessageIcon(self, city, passes):
		"Returns a tuple of the message and icon to use for the pending alert."
		return (None, None)


### Population

class CityPendingGrowth(AbstractCityAlert):
	"""
	Displays an alert when a city's population will change next turn.
	State: None.
	"""
	def __init__(self, eventManager):
		AbstractCityAlert.__init__(self, eventManager)
	
	def init(self):
		#CyInterface().addImmediateMessage("5 / 4 = %d" % (5//-4), "")
		#CyInterface().addImmediateMessage("4 / 4 = %d" % (4//-4), "")
		#CyInterface().addImmediateMessage("3 / 4 = %d" % (3//-4), "")
		#CyInterface().addImmediateMessage("2 / 4 = %d" % (2//-4), "")
		#CyInterface().addImmediateMessage("1 / 4 = %d" % (1//-4), "")
		#CyInterface().addImmediateMessage("0 / 4 = %d" % (0//-4), "")
		pass
	
	def checkCity(self, iTurn, iCityID, city, iPlayer, player):
		if (bCityPendingGrowth):
			iFoodRate = city.foodDifference(True)
			# FF: Change by Jean Elcard 11/16/2008
			'''
			if (iFoodRate > 0 and city.getFoodTurnsLeft() == 1
			and not city.isFoodProduction() and not city.AI_isEmphasize(5)):
			'''
			if (iFoodRate > 0 and city.getFoodTurnsLeft() == 1 and not gc.getPlayer(iPlayer).isIgnoreFood()
			and not city.isFoodProduction() and not city.AI_stopGrowth()):
			# FF: End Change
				message = localText.getText(
						"TXT_KEY_CIV4LERTS_ON_CITY_PENDING_GROWTH",
						(city.getName(), city.getPopulation() + 1))
				icon = "Art/Interface/Symbols/Food/food05.dds"
				addMessageAtCity(iPlayer, message, icon, city)
			elif (iFoodRate < 0 and city.getFood() // -iFoodRate == 0 and not gc.getPlayer(iPlayer).isIgnoreFood()):
				message = localText.getText(
						"TXT_KEY_CIV4LERTS_ON_CITY_PENDING_SHRINKAGE",
						(city.getName(), city.getPopulation() - 1))
				icon = "Art/Interface/Symbols/Food/food05.dds"
				addMessageAtCity(iPlayer, message, icon, city)

class CityGrowth(AbstractCityAlert):
	"""
	Displays an alert when a city's population changes.
	State: map of populations by city ID.
	"""
	def __init__(self, eventManager):
		AbstractCityAlert.__init__(self, eventManager)
		
	def checkCity(self, iTurn, iCityID, city, iPlayer, player):
		if (iCityID not in self.populations):
			self.resetCity(city)
		else:
			iPop = city.getPopulation()
			iOldPop = self.populations[iCityID]
			if (iPop > iOldPop):
				self.populations[iCityID] = iPop
				if (bCityGrowth):
					message = localText.getText(
							"TXT_KEY_CIV4LERTS_ON_CITY_GROWTH",
							(city.getName(), iPop))
					icon = "Art/Interface/Symbols/Food/food05.dds"
					addMessageAtCity(iPlayer, message, icon, city)
			elif (iPop < iOldPop):
				self.populations[iCityID] = iPop
				if (bCityGrowth):
					message = localText.getText(
							"TXT_KEY_CIV4LERTS_ON_CITY_SHRINKAGE",
							(city.getName(), iPop))
					icon = "Art/Interface/Symbols/Food/food05.dds"
					addMessageAtCity(iPlayer, message, icon, city)

	def _beforeReset(self):
		self.populations = dict()
	
	def resetCity(self, city):
		self.populations[city.getID()] = city.getPopulation()
	
	def discardCity(self, city):
		try :
			self.populations.pop(city.getID())
		except KeyError :
			pass

###
class CityCrime(AbstractCityAlert):
	"""
	Displays an alert when a city's population changes.
	State: map of populations by city ID.
	"""
	def __init__(self, eventManager):
		AbstractCityAlert.__init__(self, eventManager)
		
	def checkCity(self, iTurn, iCityID, city, iPlayer, player):
		if (iCityID not in self.populations):
			self.resetCity(city)
		else:
			iPop = city.getCrimePerTurn()
			iOldPop = self.populations[iCityID]
			if (iPop >0 and  iOldPop<=0):
				self.populations[iCityID] = iPop
				if (bCityCrime):
					message = localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_CRIME_INCREASE",(city.getName(),0))
					icon = "Art/Interface/Symbols/Food/food05.dds"
					addMessageAtCity(iPlayer, message, icon, city)
			elif (iPop<=0 and iOldPop>0):
				self.populations[iCityID] = iPop
				if (bCityCrime):
					message = localText.getText(
							"TXT_KEY_CIV4LERTS_ON_CITY_CRIME_DECREASE",
							(city.getName(),0))
					icon = "Art/Interface/Symbols/Food/food05.dds"
					addMessageAtCity(iPlayer, message, icon, city)

	def _beforeReset(self):
		self.populations = dict()
	
	def resetCity(self, city):
		self.populations[city.getID()] = city.getCrimePerTurn()
	
	def discardCity(self, city):
		try :
			self.populations.pop(city.getID())
		except KeyError :
			pass

### Happiness and Healthiness

class CityHappiness(AbstractCityTestAlert):
	"""
	Displays an event when a city goes from happy to angry or vice versa.
	
	Test: True if the city is unhappy.
	"""
	def __init__(self, eventManager):
		AbstractCityTestAlert.__init__(self, eventManager)
	
	def init(self):
		AbstractCityTestAlert.init(self)
		self.kiTempHappy = gc.getDefineINT("TEMP_HAPPY")
	
	def _passesTest(self, city):
		return city.angryPopulation(0) > 0

	def _willPassTest(self, city):
		# FF: Change by Jean Elcard 11/16/2008
		'''
		if (city.getFoodTurnsLeft() == 1 and not city.isFoodProduction() and not city.AI_isEmphasize(5)):
		'''
		if (city.getFoodTurnsLeft() == 1 and not city.isFoodProduction() and not city.AI_stopGrowth()):
		# FF: End Change
			iExtra = 1
		elif (city.getFoodTurnsLeft() == -1):
			iExtra = -1
		else:
			iExtra = 0
		iHappy = city.happyLevel()
		iUnhappy = city.unhappyLevel(iExtra)
		if (iUnhappy > 0 and city.getHurryAngerTimer() > 0 
		and city.getHurryAngerTimer() % city.flatHurryAngerLength() == 0):
			iUnhappy -= 1
		if (iUnhappy > 0 and city.getConscriptAngerTimer()
		and city.getConscriptAngerTimer() % city.flatConscriptAngerLength() == 0):
			iUnhappy -= 1
		if (iUnhappy > 0 and city.getDefyResolutionAngerTimer() > 0
		and city.getDefyResolutionAngerTimer() % city.flatDefyResolutionAngerLength() == 0):
			iUnhappy -= 1
		if (iUnhappy > 0 and city.getEspionageHappinessCounter() > 0):
			iUnhappy -= 1
		if (iHappy > 0 and city.getHappinessTimer() == 1):
			iHappy -= self.kiTempHappy
		if (iHappy < 0):
			iHappy = 0
		if (iUnhappy < 0):
			iUnhappy = 0
		return iHappy < iUnhappy
	
	def _isShowAlert(self, passes):
		return bCityHappy
	
	def _getAlertMessageIcon(self, city, passes):
		if (passes):
			return (localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_UNHAPPY", (city.getName(), )),
					UNHAPPY_ICON)
		else:
			return (localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_HAPPY", (city.getName(), )),
					HAPPY_ICON)
	
	def _isShowPendingAlert(self, passes):
		return bCityPendingHappy

	def _getPendingAlertMessageIcon(self, city, passes):
		if (passes):
			return (localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_PENDING_UNHAPPY", (city.getName(), )),
					UNHAPPY_ICON)
		else:
			return (localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_PENDING_HAPPY", (city.getName(), )),
					HAPPY_ICON)

class CityHealthiness(AbstractCityTestAlert):
	"""
	Displays an event when a city goes from healthy to sick or vice versa.
	
	Test: True if the city is unhealthy.
	"""
	def __init__(self, eventManager):
		AbstractCityTestAlert.__init__(self, eventManager)
	
	def _passesTest(self, city):
		return city.healthRate(False, 0) < 0

	def _willPassTest(self, city):
		# FF: Change by Jean Elcard 11/16/2008
		'''
		if (city.getFoodTurnsLeft() == 1 and not city.isFoodProduction() and not city.AI_isEmphasize(5)):
		'''
		if (city.getFoodTurnsLeft() == 1 and not city.isFoodProduction() and not city.AI_stopGrowth()):
		# FF: End Change
			iExtra = 1
		elif (city.getFoodTurnsLeft() == -1):
			iExtra = -1
		else:
			iExtra = 0
		# badHealth() doesn't take iExtra!
		iHealthRate = city.healthRate(False, iExtra)
		if (city.getEspionageHealthCounter() > 0):
			iHealthRate -= 1
		return iHealthRate < 0
	
	def _isShowAlert(self, passes):
		return bCityHealth
	
	def _getAlertMessageIcon(self, city, passes):
		if (passes):
			return (localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_UNHEALTHY", (city.getName(), )),
					UNHEALTHY_ICON)
		else:
			return (localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_HEALTHY", (city.getName(), )),
					HEALTHY_ICON)
	
	def _isShowPendingAlert(self, passes):
		return bCityPendingHealth

	def _getPendingAlertMessageIcon(self, city, passes):
		if (passes):
			return (localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_PENDING_UNHEALTHY", (city.getName(), )),
					UNHEALTHY_ICON)
		else:
			return (localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_PENDING_HEALTHY", (city.getName(), )),
					HEALTHY_ICON)


### Hurrying Production

class AbstractCanHurry(AbstractCityTestAlert):
	"""
	Displays an alert when a city can hurry the current production item.
	
	Test: True if the city can hurry.
	"""
	def __init__(self, eventManager):
		AbstractCityTestAlert.__init__(self, eventManager)
		eventManager.addEventHandler("cityBuildingUnit", self.onCityBuildingUnit)
		eventManager.addEventHandler("cityBuildingBuilding", self.onCityBuildingBuilding)
	
	def init(self, szHurryType):
		AbstractCityTestAlert.init(self)
		self.keHurryType = gc.getInfoTypeForString(szHurryType)

	def onCityBuildingUnit(self, argsList):
		city, iUnit = argsList
		self._onItemStarted(city)

	def onCityBuildingBuilding(self, argsList):
		city, iBuilding = argsList
		self._onItemStarted(city)

	def _onItemStarted(self, city):
		if (city.getOwner() == gc.getGame().getActivePlayer()):
			self.discardCity(city)
	
	def _passesTest(self, city):
		return city.canHurry(self.keHurryType, False)
	
	def _getAlertMessageIcon(self, city, passes):
		if (passes):
			info = None
			if (city.isProductionBuilding()):
				iType = city.getProductionBuilding()
				if (iType >= 0):
					info = gc.getBuildingInfo(iType)
			elif (city.isProductionUnit()):
				iType = city.getProductionUnit()
				if (iType >= 0):
					info = gc.getUnitInfo(iType)
			elif (city.isProductionProject()):
				# Can't hurry projects, but just in case
				iType = city.getProductionProject()
				if (iType >= 0):
					info = gc.getProjectInfo(iType)
			if (info):
				return (self._getAlertMessage(city, info), info.getButton())
		return (None, None)

class CanHurryPopulation(AbstractCanHurry):
#   Displays an alert when a city can hurry using population.

	def __init__(self, eventManager): 
		AbstractCanHurry.__init__(self, eventManager)
	
	def init(self):
		AbstractCanHurry.init(self, "HURRY_POPULATION")
		self.kszPopIcon = u"%c" % gc.getGame().getSymbolID(FontSymbols.ANGRY_POP_CHAR)
		self.kszHammerIcon = u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar()

	def _isShowAlert(self, passes):
		return passes and bHurryPop
	
	def _getAlertMessage(self, city, info):
		iPop = city.hurryPopulation(self.keHurryType)
		iOverflow = city.hurryProduction(self.keHurryType) - (city.getProductionNeeded() - city.getProduction())
		return localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_CAN_HURRY_POP", 
								 (city.getName(), info.getDescription(), 
								  iPop, self.kszPopIcon, iOverflow, self.kszHammerIcon))

class CanHurryGold(AbstractCanHurry):
#   Displays an alert when a city can hurry using gold.

	def __init__(self, eventManager): 
		AbstractCanHurry.__init__(self, eventManager)

	def init(self):
		AbstractCanHurry.init(self, "HURRY_GOLD")
		self.kszGoldIcon = u"%c" % gc.getCommerceInfo(CommerceTypes.COMMERCE_GOLD).getChar()

	def _isShowAlert(self, passes):
		return passes and bHurryGold
	
	def _getAlertMessage(self, city, info):
		iGold = city.hurryGold(self.keHurryType)
		return localText.getText("TXT_KEY_CIV4LERTS_ON_CITY_CAN_HURRY_GOLD", 
								 (city.getName(), info.getDescription(), 
								  iGold, self.kszGoldIcon))


### Trading Gold

class GoldTrade(AbstractStatefulAlert):
#   Displays an alert when a civilization has a significant increase
#	in gold available for trade since the last alert.

	def __init__(self, eventManager):
		AbstractStatefulAlert.__init__(self, eventManager)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)
		self._reset()

	def onEndGameTurn(self, argsList):
		if (not bGoldTrade):
			return

		turn = argsList[0]
		iPlayer = gc.getGame().getActivePlayer()
		pTeam = gc.getTeam(gc.getPlayer(iPlayer).getTeam())
		for iLoopPlayer in range(gc.getMAX_PLAYERS()):
			if (iLoopPlayer == iPlayer): continue #ignore ourselves and go to next player
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			iLoopTeam = pLoopPlayer.getTeam()
			pLoopTeam = gc.getTeam(iLoopTeam)
			# TODO: does this need to check for war or trade denial?
			if (pTeam.isHasMet(iLoopTeam) and (pTeam.isGoldTrading() or pLoopTeam.isGoldTrading())):
				oldMaxGoldTrade = self._getMaxGoldTrade(iPlayer, iLoopPlayer)
				newMaxGoldTrade = pLoopPlayer.AI_maxGoldTrade(iPlayer)
				deltaMaxGoldTrade = newMaxGoldTrade - oldMaxGoldTrade
				if (deltaMaxGoldTrade >= iGoldTrade): # iGoldTrade is defined at the beginning of this file (50)
					message = localText.getText("TXT_KEY_CIV4LERTS_ON_GOLD_TRADE",(pLoopPlayer.getName(), newMaxGoldTrade)) # test Ronkhar
					addMessageNoIcon(iPlayer, message)
					self._setMaxGoldTrade(iPlayer, iLoopPlayer, newMaxGoldTrade)
				else:
					maxGoldTrade = min(oldMaxGoldTrade, newMaxGoldTrade)
					self._setMaxGoldTrade(iPlayer, iLoopPlayer, maxGoldTrade)

	def _reset(self):
		self.maxGoldTrade = {}
		for player in range(gc.getMAX_PLAYERS()):
			self.maxGoldTrade[player] = {}
			for iLoopPlayer in range(gc.getMAX_PLAYERS()):
				self._setMaxGoldTrade(player, iLoopPlayer, 0)

	def _getMaxGoldTrade(self, player, rival):
		return self.maxGoldTrade[player][rival]
	
	def _setMaxGoldTrade(self, player, rival, value):
		self.maxGoldTrade[player][rival] = value

class GoldPerTurnTrade(AbstractStatefulAlert):
#   Displays an alert when a civilization has a significant increase
#   in gold per turn available for trade since the last alert.

	def __init__(self, eventManager):
		AbstractStatefulAlert.__init__(self, eventManager)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)
		self._reset()

	def onEndGameTurn(self, argsList):
		if (not bGoldPerTrade):
			return

		turn = argsList[0]
		player = gc.getGame().getActivePlayer()
		team = gc.getTeam(gc.getPlayer(player).getTeam())
		for rival in range(gc.getMAX_PLAYERS()):
			if (rival == player): continue
			rivalPlayer = gc.getPlayer(rival)
			rivalTeam = gc.getTeam(rivalPlayer.getTeam())
			# TODO: does this need to check for war or trade denial?
			if (team.isHasMet(rivalPlayer.getTeam())
				and (team.isGoldTrading() or rivalTeam.isGoldTrading())):
				oldMaxGoldPerTurnTrade = self._getMaxGoldPerTurnTrade(player, rival)
				newMaxGoldPerTurnTrade = rivalPlayer.AI_maxGoldPerTurnTrade(player)
				deltaMaxGoldPerTurnTrade = newMaxGoldPerTurnTrade - oldMaxGoldPerTurnTrade
				if (deltaMaxGoldPerTurnTrade >= iGoldPerTrade):
					message = localText.getText(
							"TXT_KEY_CIV4LERTS_ON_GOLD_PER_TURN_TRADE",
							(gc.getTeam(rival).getName(),
							 newMaxGoldPerTurnTrade))
					addMessageNoIcon(player, message)
					self._setMaxGoldPerTurnTrade(player, rival, newMaxGoldPerTurnTrade)
				else:
					maxGoldPerTurnTrade = min(oldMaxGoldPerTurnTrade, newMaxGoldPerTurnTrade)
					self._setMaxGoldPerTurnTrade(player, rival, maxGoldPerTurnTrade)

	def _reset(self):
		self.maxGoldPerTurnTrade = {}
		for player in range(gc.getMAX_PLAYERS()):
			self.maxGoldPerTurnTrade[player] = {}
			for rival in range(gc.getMAX_PLAYERS()):
				self._setMaxGoldPerTurnTrade(player, rival, 0)

	def _getMaxGoldPerTurnTrade(self, player, rival):
		return self.maxGoldPerTurnTrade[player][rival]
	
	def _setMaxGoldPerTurnTrade(self, player, rival, value):
		self.maxGoldPerTurnTrade[player][rival] = value
