## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

from CvPythonExtensions import *
from BasicFunctions import *
import CvUtil
import Popup as PyPopup
import CvScreenEnums
import CvEventInterface

class CustomFunctions:
	def __init__(self):
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
		self.Leaders			= {}
		self.LeaderStatus		= {}
		self.Traits				= {}
		self.Civics				= {}
		self.Religions			= {}
		self.Corporations		= {}
		self.Alignments			= {}
		# Buildings, etc
		self.Projects			= {}
		self.Buildings			= {}
		self.Specialists		= {}
		self.BuildingClasses	= {}
		self.Processes			= {}
		# Improvements, etc
		self.Lairs				= {}
		self.ManaNodes			= {}
		self.Improvements		= {}
		self.CivImprovements	= {}
		self.UniqueImprovements	= {}
		# Terrain, etc
		self.Mana				= {}
		self.Terrain			= {}
		self.Feature			= {}
		self.Resources			= {}
		self.WorldSizes			= {}
		# Units, etc
		self.Units				= {}
		self.Heroes				= {}
		self.UnitAI				= {}
		self.Promotions			= {}
		self.UnitClasses		= {}
		self.UnitCombats		= {}
		self.GreatPeople		= {}
		self.DamageTypes		= {}

	def initialize(self):
		Manager					= CvEventInterface.getEventManager()
		self.Defines			= Manager.Defines
		self.Eras				= Manager.Eras
		self.Techs				= Manager.Techs
		self.Victories			= Manager.Victories
		self.GameSpeeds			= Manager.GameSpeeds
		self.GameOptions		= Manager.GameOptions
		self.EventTriggers		= Manager.EventTriggers

		self.Civilizations		= Manager.Civilizations
		self.Leaders 			= Manager.Leaders
		self.LeaderStatus		= Manager.LeaderStatus
		self.Traits 			= Manager.Traits
		self.Civics 			= Manager.Civics
		self.Religions 			= Manager.Religions
		self.Corporations		= Manager.Corporations
		self.Alignments			= Manager.Alignments

		self.Projects			= Manager.Projects
		self.Buildings			= Manager.Buildings
		self.Specialists		= Manager.Specialists
		self.BuildingClasses	= Manager.BuildingClasses
		self.Processes			= Manager.Processes

		self.Lairs				= Manager.Lairs
		self.ManaNodes			= Manager.ManaNodes
		self.Improvements		= Manager.Improvements
		self.CivImprovements	= Manager.CivImprovements
		self.UniqueImprovements	= Manager.UniqueImprovements

		self.Mana				= Manager.Mana
		self.Terrain			= Manager.Terrain
		self.Feature			= Manager.Feature
		self.Resources			= Manager.Resources
		self.WorldSizes			= Manager.WorldSizes
		self.Goodies			= Manager.Goodies

		self.Units				= Manager.Units
		self.Heroes				= Manager.Heroes
		self.UnitAI				= Manager.UnitAI
		self.UnitClasses		= Manager.UnitClasses
		self.UnitCombats		= Manager.UnitCombats
		self.GreatPeople		= Manager.GreatPeople
		self.Promotions			= Manager.Promotions
		self.DamageTypes		= Manager.DamageTypes

	def showAutoPlayPopup(self):
		'Window for when user switches to AI Auto Play'
		popupSizeX	= 400
		popupSizeY	= 200
		screen		= CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		xRes		= screen.getXResolution()
		yRes		= screen.getYResolution()
		popup		= PyPopup.PyPopup(CvUtil.EventSetTurnsAutoPlayPopup, contextType = EventContextTypes.EVENTCONTEXT_ALL)
		popup.setPosition((xRes - popupSizeX) / 2, (yRes - popupSizeY) / 2 - 50)
		popup.setSize(popupSizeX, popupSizeY)
		popup.setHeaderString(CyTranslator().getText("TXT_KEY_AIAUTOPLAY_TURN_ON", ()))
		popup.setBodyString(CyTranslator().getText("TXT_KEY_AIAUTOPLAY_TURNS", ()))
		popup.addSeparator()
		popup.createPythonEditBox('10', 'Number of turns to turn over to AI', 0)
		popup.setEditBoxMaxCharCount(4, 2, 0)
		popup.addSeparator()
		popup.addButton("OK")
		popup.addButton(CyTranslator().getText("TXT_KEY_AIAUTOPLAY_CANCEL", ()))
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def showUnitPerTilePopup(self):
		'Window for when user switches to AI Auto Play'
		popupSizeX	= 400
		popupSizeY	= 250
		screen		= CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		xRes		= screen.getXResolution()
		yRes		= screen.getYResolution()
		popup		= PyPopup.PyPopup(CvUtil.EventSetUnitPerTilePopup, contextType = EventContextTypes.EVENTCONTEXT_ALL)
		popup.setPosition((xRes - popupSizeX) / 2, (yRes - popupSizeY) / 2 - 50)
		popup.setSize(popupSizeX, popupSizeY)
		popup.setHeaderString(CyTranslator().getText("TXT_KEY_UPT", ()))
		popup.setBodyString(CyTranslator().getText("TXT_KEY_UPT_VALUE", ()))
		popup.addSeparator()
		popup.createPythonEditBox('8', 'Number of Units per Tile', 0)
		popup.setEditBoxMaxCharCount(4, 2, 0)
		popup.addSeparator()
		popup.addButton("OK")
		popup.addButton("Lock xUPT Value")
		popup.addButton(CyTranslator().getText("TXT_KEY_AIAUTOPLAY_CANCEL", ()))
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def doCrusade(self, iPlayer):
		gc				= CyGlobalContext()
		iCrusadeChance	= self.Defines["Crusade Spawn"]
		pPlayer 		= gc.getPlayer(iPlayer)
		iSouth			= DirectionTypes.DIRECTION_SOUTH
		iNoAI			= UnitAITypes.NO_UNITAI
		for i in xrange(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getImprovementType() != self.Improvements["Town (IV)"]:	continue
			if pPlot.getOwner() != iPlayer:										continue
			if CyGame().getSorenRandNum(100, "Crusade") >= iCrusadeChance:		continue
			newUnit = pPlayer.initUnit(self.Units["Bannor"]["Demagog"], pPlot.getX(), pPlot.getY(), iNoAI, iSouth)
			pPlot.setImprovementType(self.Improvements["Village (III)"])

	def doForestPush(self, pVictim, pPlot, pCaster, bResistable):
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(pVictim.getOwner())
		if pPlayer.isHasTech(self.Techs["Iron Working"]): return False
		if pPlayer.countNumBuildings(self.Buildings["Mines of Galdur"]) > 0: return False
		iX		= pVictim.getX()
		iY		= pVictim.getY()
		iOwner	= pVictim.getOwner()
		pVPlot	= CyMap().plot(iX,iY)
		if iOwner == gc.getANIMAL_PLAYER(): return False
		if pVPlot.getFeatureType() not in (self.Feature["Forest"], self.Feature["Jungle"], self.Feature["Forest New"]): return False
		pBestPlot	= -1
		iBestPlot	= 0
		for iiX,iiY in SURROUND1:
			pLoopPlot = CyMap().plot(iX+iiX,iY+iiY)
			if pLoopPlot.isNone():												continue
			if pLoopPlot.isVisibleEnemyUnit(iOwner):							continue
			if not pVictim.canMoveOrAttackInto(pLoopPlot, False):				continue
			if pLoopPlot.getImprovementType() == self.Lairs["Blighted Forest"]:	continue
			iRnd		= CyGame().getSorenRandNum(500, "Forest Push Scatter choose Plot")
			if iRnd <= iBestPlot:												continue
			iBestPlot	= iRnd
			pBestPlot	= pLoopPlot
		if pBestPlot != -1:
			pVictim.setXY(pBestPlot.getX(), pBestPlot.getY(), False, True, True, False)
			if pVictim.getOwner() == gc.getORC_PLAYER():
				pVictim.doDamageNoCaster(20, 100, self.DamageTypes["Physical"], False)
			return True
		return False

	def formEmpire(self, iCiv, iLeader, iTeam, pCity, iAlignment, pFromPlayer):
		gc 		= CyGlobalContext()
		iPlayer = getOpenPlayer()
		pPlot 	= pCity.plot()
		pPlot2 	= findClearPlot(-1, pCity.plot())
		if iPlayer == -1 or pPlot2.isNone(): return
		iX = pPlot2.getX(); iY = pPlot2.getY()
		for i in xrange(pPlot.getNumUnits(), -1, -1):
			pUnit = pPlot.getUnit(i)
			pUnit.setXY(iX, iY, True, True, True, False)
		CyGame().addPlayerAdvanced(iPlayer, iTeam, iLeader, iCiv, pFromPlayer.getID())
		pPlayer	= gc.getPlayer(iPlayer)
		iTeam	= pPlayer.getTeam()
		pTeam	= gc.getTeam(iTeam)
		if pFromPlayer != -1:
			iFromTeam	= pFromPlayer.getTeam()
			pFromTeam	= gc.getTeam(iFromTeam)
			for iTech in xrange(gc.getNumTechInfos()):
				if not pFromTeam.isHasTech(iTech): continue
				pTeam.setHasTech(iTech, True, iPlayer, True, False)
			if iFromTeam != iTeam:
				if not pFromTeam.isAtWar(gc.getORC_TEAM()):
					pFromTeam.makePeace(gc.getORC_TEAM())
				if not pFromTeam.isAtWar(gc.getANIMAL_TEAM()):
					pFromTeam.makePeace(gc.getANIMAL_TEAM())
				if not pFromTeam.isAtWar(gc.getDEMON_TEAM()):
					pFromTeam.makePeace(gc.getDEMON_TEAM())
		pPlayer.acquireCity(pCity, False, False)
		pCity = pPlot.getPlotCity()
		pCity.changeCulture(iPlayer, 100, True)
		iX = pPlot.getX(); iY = pPlot.getY();
		iNoAI 	= UnitAITypes.NO_UNITAI
		iSouth 	= DirectionTypes.DIRECTION_SOUTH
		pPlayer.initUnit(self.Units["Generic"]["Archer"], iX, iY, iNoAI, iSouth)
		pPlayer.initUnit(self.Units["Generic"]["Archer"], iX, iY, iNoAI, iSouth)
		pPlayer.initUnit(self.Units["Generic"]["Archer"], iX, iY, iNoAI, iSouth)
		pPlayer.initUnit(self.Units["Generic"]["Archer"], iX, iY, iNoAI, iSouth)
		pPlayer.initUnit(self.Units["Generic"]["Archer"], iX, iY, iNoAI, iSouth)
		if iAlignment != -1:
			pPlayer.setAlignment(iAlignment)

	def doCityFire(self, pCity):
		gc 				= CyGlobalContext()
		iCount 			= 0
		iOwner 			= pCity.getOwner()
		iX = pCity.getX(); iY = pCity.getY()
		iMessage		= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		iGreen			= gc.getInfoTypeForString("COLOR_GREEN")
		iRed			= gc.getInfoTypeForString("COLOR_RED")
		for iBuilding in xrange(gc.getNumBuildingInfos()):
			if iBuilding == self.Buildings["Demonic Citizens"]:								continue
			if pCity.getNumRealBuilding(iBuilding) <= 0:									continue
			if gc.getBuildingInfo(iBuilding).getConquestProbability() == 100:				continue
			if isLimitedWonderClass(gc.getBuildingInfo(iBuilding).getBuildingClassType()):	continue
			if CyGame().getSorenRandNum(100, "City Fire") > 10:								continue
			pCity.setNumRealBuilding(iBuilding, 0)

			szButton	= gc.getBuildingInfo(iBuilding).getButton()
			szText		= CyTranslator().getText("TXT_KEY_MESSAGE_CITY_FIRE",(gc.getBuildingInfo(iBuilding).getDescription(), ))
			CyInterface().addMessage(iOwner, True, 25, szText, '', iMessage, szButton, iRed, iX, iY, True, True)
			iCount += 1
		if iCount == 0:
			szButton	= 'Art/Interface/Buttons/Fire.dds'
			szText		= CyTranslator().getText("TXT_KEY_MESSAGE_CITY_FIRE_NO_DAMAGE",())
			CyInterface().addMessage(iOwner, True, 25, szText, '', iMessage, szButton, iGreen, iX, iY, True, True)

	### TODO: Dictionaries
	def doFFTurn(self, iTurn):
		iNumScions		= CyGame().getNumCivActive(self.Civilizations["Scions"])
		gc				= CyGlobalContext()
		git				= gc.getInfoTypeForString
		iPlotTreshold	= gc.getDefineINT("PLOT_COUNTER_HELL_THRESHOLD")
		iJungleChance	= 10
		iSwampChance	= 25
		iHLSeed			= 0

		if iNumScions:
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer	= gc.getPlayer(iLoopPlayer)
				if not pLoopPlayer.isAlive():					continue
				iLoopCiv	= pLoopPlayer.getCivilizationType()
				if iLoopCiv != self.Civilizations["Scions"]:	continue
				iNatureMana = pLoopPlayer.getNumAvailableBonuses(self.Mana["Nature"])
				iManaMod = 1 + (iNatureMana * 0.1)
				iGhostwalkerFactor	= pLoopPlayer.getUnitClassCount(self.UnitClasses["Ranger"])
				iHauntFactor		= pLoopPlayer.getUnitClassCount(self.UnitClasses["Haunt"]) * 2
				iRedactorFactor		= pLoopPlayer.getUnitClassCount(self.UnitClasses["Druid"]) * 4
				iBlackLadyFactor	= pLoopPlayer.getUnitClassCount(self.UnitClasses["Korrina Black"]) + 1
				iHLSeed = (iGhostwalkerFactor + iHauntFactor + iRedactorFactor) * iBlackLadyFactor * iManaMod
				break

		for i in xrange(CyMap().numPlots()):
			pPlot			 	= CyMap().plotByIndex(i)
			if pPlot == None: continue
			iPlotCounter		= pPlot.getPlotCounter()
			iBonus 				= pPlot.getBonusType(-1)
			iFeature 			= pPlot.getFeatureType()
			iPlotEffect 		= pPlot.getPlotEffectType()
			iImprovement 		= pPlot.getImprovementType()
			iTerrain 			= pPlot.getTerrainType()
			bIsOwned 			= pPlot.isOwned()
			bPeak				= pPlot.isPeak()
			bCity				= pPlot.isCity()
			iConvert			= CyGame().getSorenRandNum(100, "Hell Convert")
			if bIsOwned:
				iPlayer 		= pPlot.getOwner()
				pPlayer 		= gc.getPlayer(iPlayer)
				eCiv 			= pPlayer.getCivilizationType()

				## Lizard Terrain Section
				if eCiv in (self.Civilizations["Mazatl"], self.Civilizations["Cualli"]):
					if pPlot.getRouteType() == self.Improvements["Road"]:
						if CyGame().getSorenRandNum(100, "Trail") < 20:
							pPlot.setRouteType(self.Improvements["Trail"])

					if iTerrain == self.Terrain["Marsh"]:
						if iImprovement == -1 and iBonus == -1 and not bCity and not bPeak:
							if not pPlayer.isHuman(): 	iSwampChance *=2
							if CyGame().getSorenRandNum(1000, "Swamp") < iSwampChance:
								pPlot.setImprovementType(self.Improvements["Swamp"])
						if   iFeature == self.Feature["Forest"] or iFeature == self.Feature["Ancient Forest"]:
							iJungleChance *= 5
						elif iFeature != -1:
							iJungleChance = 0
						if CyGame().getSorenRandNum(1000, "Jungle") < iJungleChance:
							pPlot.setFeatureType(self.Feature["Jungle"], 0)

				#### Haunted Lands Section
				elif eCiv == self.Civilizations["Scions"]:
					if iPlotEffect != self.Feature["Haunted Lands"] and iHLSeed > 0 and not bPeak and not bCity:
						if   iFeature in (self.Feature["Forest"], self.Feature["Ancient Forest"], self.Feature["Jungle"]): 
							iHLSeed *= 1.5
						elif iFeature == self.Feature["Flood Plains"] or iTerrain in (self.Terrain["Grass"], self.Terrain["Plains"], self.Terrain["Marsh"]):
							iHLSeed = iHLSeed
						elif iTerrain == self.Terrain["Desert"]:
							iHLSeed *= 0.5
						else:
							iHLSeed = 0
						if CyGame().getSorenRandNum(1100, "Chance for HL") < iHLSeed:
							pPlot.setPlotEffectType(self.Feature["Haunted Lands"])

			if iImprovement == self.Improvements["Swamp"] and iTerrain != self.Terrain["Marsh"]: pPlot.setImprovementType(-1)

			## Hell Terrain Section
			if not self.GameOptions["No Plot Counter"]:
				if iPlotCounter > iPlotTreshold and not iTerrain in (self.Terrain["Tundra"], self.Terrain["Taiga"]):
					if   iBonus in (self.Resources["Sheep"], self.Resources["Pig"], self.Resources["Fur"], self.Resources["Deer"]):
						pPlot.setBonusType(self.Resources["Toad"])
					elif iBonus in (self.Resources["Horse"], self.Resources["Cow"], self.Resources["Camel"], self.Resources["Ivory"]):
						pPlot.setBonusType(self.Resources["Nightmare"])
					elif iBonus in (self.Resources["Cotton"], self.Resources["Silk"], self.Resources["Wine"]):
						pPlot.setBonusType(self.Resources["Razorweed"])
					elif iBonus in (self.Resources["Fish"], self.Resources["Shrimp"], git('BONUS_WHALE')):
						pPlot.setBonusType(git('BONUS_JETEYE'))
					elif iBonus in (self.Resources["Clam"], self.Resources["Crab"], self.Resources["Pearl"]):
						pPlot.setBonusType(git('BONUS_BLEEDING_GOD_WINE'))
					elif iBonus in (self.Resources["Banana"], self.Resources["Sugar"]):
						pPlot.setBonusType(self.Resources["Gulagarm"])
					elif iBonus == self.Resources["Marble"]:
						pPlot.setBonusType(self.Resources["Sheut"])
					elif iBonus in (self.Resources["Corn"], self.Resources["Rice"], self.Resources["Wheat"]):
						pPlot.setBonusType(-1)
						pPlot.setImprovementType(self.Improvements["Snake Pillar"])
				elif iPlotCounter <= iPlotTreshold:
					if iImprovement == self.Improvements["Snake Pillar"]:
						pPlot.setImprovementType(-1)
						if   iConvert < 33:	pPlot.setBonusType(self.Resources["Corn"])
						elif iConvert < 67:	pPlot.setBonusType(self.Resources["Rice"])
						else:				pPlot.setBonusType(self.Resources["Wheat"])
				if iTerrain == self.Terrain["Burning sands"] and not bCity and not bPeak:
					if CyGame().getSorenRandNum(100, "Flames") <= self.Defines["Flame Spread"]:
						pPlot.setFeatureType(self.Feature["Flames"], 0)
		# Annoying popup
		if iTurn == 3:
			if not CyGame().isNetworkMultiPlayer():
				t = "TROPHY_FEAT_INTRODUCTION"
				if not CyGame().isHasTrophy(t):
					CyGame().changeTrophyValue(t, 1)
					addPopupWB(CyTranslator().getText("TXT_KEY_FFH_INTRO",()),'art/interface/popups/FfHIntro.dds')
		# Global Unit Spawn
		bOrthus			= not CyGame().isOption(self.GameOptions["No Orthus"])
		lSpawnTurns		= [75, 100, 120] # Orthus, Zarcaz, Gyre
		fSpeedMod		= float(gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent()) / 100
		lSpawnTurns		= [int(iSpawnTurn * fSpeedMod) for iSpawnTurn in lSpawnTurns]
		if   iTurn == lSpawnTurns[0]:
			if not CyGame().isUnitClassMaxedOut(self.UnitClasses["Orthus"], 0) and bOrthus:
				iOrthusPlayer = gc.getORC_PLAYER()
				if git("MODULE_EMERGENT_LEADERS") != -1:
					for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if not pLoopPlayer.isAlive(): continue
						if not pLoopPlayer.hasTrait(self.Traits["Matriarch 1"]): continue
						iOrthusPlayer = iLoopPlayer
				addUnit(self.Heroes["Orthus"], iOrthusPlayer)
		elif iTurn == lSpawnTurns[1]:
			if not CyGame().isUnitClassMaxedOut(self.UnitClasses["Zarcaz"], 0) and bOrthus:
				iZarcazPlayer	= gc.getORC_PLAYER()
				pZarcazPlayer	= gc.getPlayer(iZarcazPlayer)
				pZarcaz			= addUnit(self.Heroes["Zarcaz"], iZarcazPlayer)
				iX				= pZarcaz.getX()
				iY				= pZarcaz.getY()
				iAIValue		= UnitAITypes.NO_UNITAI
				iDirection		= DirectionTypes.DIRECTION_SOUTH
				newUnit			= pZarcazPlayer.initUnit(self.Units["Scorpion Clan"]["Archer"], iX, iY, iAIValue, iDirection)
				pZarcaz.addMinion(newUnit)
				newUnit2		= pZarcazPlayer.initUnit(self.Units["Scorpion Clan"]["Goblin"], iX, iY, iAIValue, iDirection)
				pZarcaz.addMinion(newUnit2)
				newUnit3		= pZarcazPlayer.initUnit(self.Units["Scorpion Clan"]["Wolf Rider"], iX, iY, iAIValue, iDirection)
				pZarcaz.addMinion(newUnit3)
		elif iTurn == lSpawnTurns[2]:
			if not CyGame().isUnitClassMaxedOut(git('UNITCLASS_GYRE_CARLIN'), 0) and bOrthus:
				addUnit(git('UNIT_GYRE_CARLIN'), gc.getDEMON_PLAYER())
		# UF Teleport
		if (iTurn + 1) % (40 - 5 * CyGame().getGameSpeedType()) == 0:
			bOrcPlayer			= gc.getPlayer(gc.getORC_PLAYER())
			if not bOrcPlayer.isHasFlag(git('FLAG_CONTROLED_LACUNA')):
				iBL	= self.UniqueImprovements["Bair of Lacuna"]
				lBL	= self.findImprovements(iBL)
				if lBL:
					pPlotBL		= lBL[0]
					iBestValue	= 0
					pBestPlot	= -1
					for iLoopPlot in xrange(CyMap().numPlots()):
						pLoopPlot = CyMap().plotByIndex(iLoopPlot)
						if pLoopPlot.isWater():					continue
						if pLoopPlot.isPeak():					continue
						if pLoopPlot.getBonusType(-1) != -1:	continue
						if pLoopPlot.getRealBonusType() != -1:	continue
						if pLoopPlot.getNumUnits() > 0:			continue
						if pLoopPlot.isCity():					continue
						if pLoopPlot == pPlotBL:				continue
						iValue = 0
						if pLoopPlot.getImprovementType() == -1:	iValue += 1000
						else:
							if gc.getImprovementInfo(pLoopPlot.getImprovementType()).isPermanent(): continue
						if not pLoopPlot.isOwned():					iValue += 500
						if pLoopPlot.getRouteType() == -1:			iValue += 500
						iValue += CyGame().getSorenRandNum(1000, "Bair Move")
						if iValue > iBestValue:
							iBestValue = iValue
							pBestPlot = pLoopPlot
					if pBestPlot != -1:
						pBestPlot.setImprovementType(iBL)
						pBestPlot.setExploreNextTurn(pPlotBL.getExploreNextTurn())
						pBestPlot.setRouteType(pPlotBL.getRouteType())
						pPlotBL.setImprovementType(-1)
						pPlotBL.setBonusType(-1)
						pPlotBL.setRouteType(-1)
						pPlotBL.setExploreNextTurn(0)

	def doTurnKhazad(self, iPlayer):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		iNumCities	= pPlayer.getNumCities()
		if iNumCities <= 0: return
		iGold = pPlayer.getGold() / iNumCities
		if 		iGold <= 49:						iNewVault = self.Buildings["Vault1"]
		elif	(iGold >= 50 and iGold <= 99):		iNewVault = self.Buildings["Vault2"]
		elif	(iGold >= 100 and iGold <= 149):	iNewVault = self.Buildings["Vault3"]
		elif	(iGold >= 150 and iGold <= 199):	iNewVault = self.Buildings["Vault4"]
		elif	(iGold >= 200 and iGold <= 299):	iNewVault = self.Buildings["Vault5"]
		elif	(iGold >= 300 and iGold <= 499):	iNewVault = self.Buildings["Vault6"]
		elif	iGold >= 500:						iNewVault = self.Buildings["Vault7"]

		(pCity, iter) = pPlayer.firstCity(False)
		while(pCity):
			pCity.setNumRealBuilding(self.Buildings["Vault1"], 0)
			pCity.setNumRealBuilding(self.Buildings["Vault2"], 0)
			pCity.setNumRealBuilding(self.Buildings["Vault3"], 0)
			pCity.setNumRealBuilding(self.Buildings["Vault4"], 0)
			pCity.setNumRealBuilding(self.Buildings["Vault5"], 0)
			pCity.setNumRealBuilding(self.Buildings["Vault6"], 0)
			pCity.setNumRealBuilding(self.Buildings["Vault7"], 0)
			pCity.setNumRealBuilding(iNewVault, 1)
			(pCity, iter) = pPlayer.nextCity(iter, False)

	def doTurnLuchuirp(self, iPlayer):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		if pPlayer.getUnitClassCount(self.Heroes["Class-Barnaxus"]) <= 0: return
		pBarnaxus	= -1
		lGolems		= []

		for iUnit in xrange(pPlayer.getNumUnits()):
			pUnit = pPlayer.getUnit(iUnit)
			if   pUnit.getUnitType() == self.Heroes["Barnaxus"]:
				pBarnaxus = pUnit
			elif pUnit.isHasPromotion(self.Promotions["Race"]["Golem"]) and not pUnit.isHasPromotion(self.Promotions["Generic"]["Empower V"]):
				lGolems.append(iUnit)

		if pBarnaxus == -1 or not lGolems: return
		else:
			bEmp1	= pBarnaxus.isHasPromotion(self.Promotions["Generic"]["Combat I"])
			bEmp2	= pBarnaxus.isHasPromotion(self.Promotions["Generic"]["Combat II"])
			bEmp3	= pBarnaxus.isHasPromotion(self.Promotions["Generic"]["Combat III"])
			bEmp4	= pBarnaxus.isHasPromotion(self.Promotions["Generic"]["Combat IV"])
			bEmp5	= pBarnaxus.isHasPromotion(self.Promotions["Generic"]["Combat V"])

		for iUnit in lGolems:
			pUnit = pPlayer.getUnit(iUnit)
			if bEmp1: pUnit.setHasPromotion(self.Promotions["Generic"]["Empower I"], True)
			if bEmp2: pUnit.setHasPromotion(self.Promotions["Generic"]["Empower II"], True)
			if bEmp3: pUnit.setHasPromotion(self.Promotions["Generic"]["Empower III"], True)
			if bEmp4: pUnit.setHasPromotion(self.Promotions["Generic"]["Empower IV"], True)
			if bEmp5: pUnit.setHasPromotion(self.Promotions["Generic"]["Empower V"], True)

	def doTurnArchos(self, iPlayer):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		if pPlayer.getNumCities() <= 0: return
		pNest		= pPlayer.getCapitalCity()
		iNestPop	= pNest.getPopulation()
		if iNestPop < 4: return
		iNoAI		= UnitAITypes.NO_UNITAI
		iSouth		= DirectionTypes.DIRECTION_SOUTH
		iX = pNest.getX(); iY = pNest.getY()
		self.doChanceArchos(iPlayer)
		iSpawnChance			= pPlayer.getCivCounter()
		iScorpionSpawnChance	= pPlayer.getCivCounterMod()

		bSpider		= False
		bScorpion	= False
		if CyGame().getSorenRandNum(10000, "Spawn Archos Spider") < iSpawnChance:
			bSpider		= True
		elif CyGame().getSorenRandNum(10000, "Spawn Archos Scorpion") < iScorpionSpawnChance:
			bScorpion	= True
		if bSpider == False and bScorpion == False: return

		if   iNestPop >= 12:
			iUnit				= self.Units["Archos"]["Giant Spider"]
			if bScorpion: iUnit	= self.Units["Archos"]["Giant Scorpion"]
		elif iNestPop >= 8:
			iUnit				= self.Units["Archos"]["Spider"]
			if bScorpion: iUnit	= self.Units["Archos"]["Scorpion Swarm"]
		else:
			iUnit				= self.Units["Archos"]["Baby Spider"]
			if bScorpion: iUnit	= self.Units["Archos"]["Scorpion"]

		spawnUnit = pPlayer.initUnit(iUnit, iX, iY, iNoAI, iSouth)

		if pPlayer.hasTrait(self.Traits["Spiderkin"]) and iNestPop >= 10:
			spawnUnit.setHasPromotion(self.Promotions["Effects"]["Spiderkin"], True)

		if iNestPop >= 16:
			spawnUnit.setHasPromotion(self.Promotions["Effects"]["Strong"], True)

		szText		= CyTranslator().getText("TXT_KEY_MESSAGE_SPIDER_BORN_IN_NEST",())
		szArt		= gc.getUnitInfo(iUnit).getButton()
		iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
		szSound		= 'AS2D_DISCOVERBONUS'
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, iX, iY, True, True)
		pNest.applyBuildEffects(spawnUnit)

		if   pNest.getNumBuilding(self.Buildings["Nest Addon1"]) > 0:
			iBroodStrength = 1
		elif pNest.getNumBuilding(self.Buildings["Nest Addon2"]) > 0:
			iBroodStrength = 2
		elif pNest.getNumBuilding(self.Buildings["Nest Addon3"]) > 0:
			iBroodStrength = 3
		elif pNest.getNumBuilding(self.Buildings["Nest Addon4"]) > 0:
			iBroodStrength = 4
		else:
			iBroodStrength = 0
		spawnUnit.changeFreePromotionPick(iBroodStrength)

	def doChanceArchos(self, iPlayer):
		gc				= CyGlobalContext()
		pPlayer			= gc.getPlayer(iPlayer)
		if pPlayer.getNumCities() <= 0: return
		pNest			= pPlayer.getCapitalCity()
		iNestPop		= pNest.getPopulation()
		iX				= pNest.getX()
		iY				= pNest.getY()
		iNumNestHills	= 0
		iNumGroves		= pPlayer.countNumBuildings(self.Buildings["Dark Weald"])
		iNumSpiders		= ((pPlayer.getUnitClassCount(self.UnitClasses["Baby Spider"]) * 0.5)	+ pPlayer.getUnitClassCount(self.UnitClasses["Spider"])			+ (pPlayer.getUnitClassCount(self.UnitClasses["Giant Spider"]) * 2))
		iNumScorpions 	= ((pPlayer.getUnitClassCount(self.UnitClasses["Scorpion"]) * 0.5)		+ pPlayer.getUnitClassCount(self.UnitClasses["Scorpion Swarm"])	+ (pPlayer.getUnitClassCount(self.UnitClasses["Giant Scorpion"]) * 2))

		iNumScorpionCities = 0
		iNumSpiderCities = 0

		(pCity, iter) = pPlayer.firstCity(False)
		while(pCity):
			pCityPlot = pCity.plot()
			if pCityPlot.getTerrainType() == self.Terrain["Desert"]:
				iNumScorpionCities += 1
			else:
				iNumSpiderCities += 1
			(pCity, iter) = pPlayer.nextCity(iter, False)

		for iiX,iiY in BFC:
			pLoopPlot = CyMap().plot(iX+iiX,iY+iiY)
			if pLoopPlot.isNone():		continue
			if not pLoopPlot.isHills():	continue
			iNumNestHills += 1

		fSpiderkin = 1
		if pPlayer.hasTrait(self.Traits["Spiderkin"]):
			fSpiderkin = 1.30

		iSpiderSpawnChance = ((iNestPop + (iNumSpiderCities*2) + (iNumGroves*4)) * fSpiderkin) - iNumSpiders
		iSpiderSpawnChance = (iSpiderSpawnChance * 100)
		iSpiderSpawnChance = scaleInverse(iSpiderSpawnChance)

		pPlayer.setCivCounter(iSpiderSpawnChance)

		iScorpionSpawnChance = (iNestPop + (iNumScorpionCities*2) + (iNumNestHills)) - iNumScorpions
		iScorpionSpawnChance = (iScorpionSpawnChance * 100)
		iScorpionSpawnChance = scaleInverse(iScorpionSpawnChance)

		pPlayer.setCivCounterMod(iScorpionSpawnChance)

	### Scions Start
	def doTurnScions(self, iPlayer):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		pTomb		= pPlayer.getCapitalCity()
		if pTomb.isNone(): return
		self.doChanceAwakenedSpawn(iPlayer)
		iSpawnOdds	= pPlayer.getCivCounter()
		iTombPop	= pTomb.getPopulation()
		iTeam		= pPlayer.getTeam()
		pTeam		= gc.getTeam(iTeam)
		iNumCities	= pPlayer.getNumCities()

		iNumOpenBorders = (pTeam.getOpenBordersTradingCount()) - 1
		for iLoopCiv in xrange(gc.getMAX_CIV_PLAYERS()):
			if not (pTeam.isOpenBorders(iLoopCiv)): continue
			iNumOpenBorders += 1
		if pPlayer.isCivic(self.Civics["God King"]):
			iNumOpenBorders += 1
		iNumOpenBorders = min(iNumOpenBorders, 7)
		lOBB = [self.Buildings["Obbuilding1"], self.Buildings["Obbuilding2"], self.Buildings["Obbuilding3"], self.Buildings["Obbuilding4"], self.Buildings["Obbuilding5"], self.Buildings["Obbuilding6"], self.Buildings["Obbuilding7"]]
		iOBB = -1
		if iNumOpenBorders > 0:
			iOBB = lOBB[iNumOpenBorders - 1]
		iNumHealthBonus = 0
		for iBonus in xrange(gc.getNumBonusInfos()):
			if gc.getBonusInfo(iBonus).getHealth() > 0 and pPlayer.hasBonus(iBonus):
				iNumHealthBonus += 1
		## Awakened Spawn
		if CyGame().getSorenRandNum(10000, "Awakened Spawn") < iSpawnOdds:
			pTarget = pTomb
			iNumCities = pPlayer.getNumCities()
			if not pPlayer.isHuman() and iNumCities > 1:
				if CyGame().getSorenRandNum(100, "Awakened Distribution") >= 50:
					lCities	= []
					(pLoopCity, iter) = pPlayer.firstCity(False)
					while(pLoopCity):
						lCities.append(pLoopCity)
						(pLoopCity, iter) = pPlayer.nextCity(iter, False)
					pTarget	= lCities[CyGame().getSorenRandNum(len(lCities), "doTurnScions, City Pick")]
			spawnUnit = pPlayer.initUnit(self.Units["Scions"]["Awakened"], pTarget.getX(), pTarget.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		## Pity Pop
		if iNumCities == 1 and iTombPop == 1:
			pTomb.changePopulation(1)
		### City Start
		(pCity, iter) = pPlayer.firstCity(False)
		while(pCity):
			### Clean Buildings
			for iBuilding in lOBB:
				pCity.setNumRealBuilding(iBuilding, 0)
			pCity.setNumRealBuilding(self.Buildings["Necro Bonus1"], 0)
			pCity.setNumRealBuilding(self.Buildings["Necro Bonus2"], 0)
			pCity.setNumRealBuilding(self.Buildings["Necro Bonus3"], 0)
			pCity.setNumRealBuilding(self.Buildings["Unhealthy Discontent I"], 0)
			pCity.setNumRealBuilding(self.Buildings["Unhealthy Discontent II"], 0)
			## Set Buildings
			if pCity.getProductionUnit() == self.Units["Scions"]["Reborn"] and iNumOpenBorders > 0:
				pCity.setNumRealBuilding(iOBB, 1)
			if pCity.getNumRealBuilding(self.Buildings["Necropolis"]) > 0:
				if   iNumHealthBonus > 8:
					pCity.setNumRealBuilding(self.Buildings["Necro Bonus3"], 1)
				elif iNumHealthBonus > 5:
					pCity.setNumRealBuilding(self.Buildings["Necro Bonus2"], 1)
				elif iNumHealthBonus > 3:
					pCity.setNumRealBuilding(self.Buildings["Necro Bonus1"], 1)
			else:
				iUH = pCity.badHealth(False) - pCity.goodHealth()
				if   iUH > 7:
					pCity.setNumRealBuilding(self.Buildings["Unhealthy Discontent II"], 1)
				elif iUH > 4:
					pCity.setNumRealBuilding(self.Buildings["Unhealthy Discontent I"], 1)
			(pCity, iter) = pPlayer.nextCity(iter, False)
		### Alcinus AI
		for iUnit in xrange(pPlayer.getNumUnits()):
			pUnit		= pPlayer.getUnit(iUnit)
			iUnitType	= pUnit.getUnitType()
			if iUnitType in (self.Heroes["Alcinus"], self.Heroes["Alcinus (Archmage)"], self.Heroes["Alcinus (Upgraded)"]):
				if pUnit.isHasPromotion(self.Promotions["Effects"]["Rampage"]):
					pUnit.setUnitAIType( UnitAITypes.UNITAI_ATTACK )
				else:
					pUnit.setUnitAIType( UnitAITypes.UNITAI_RESERVE )
		### Horned Dread Shenanigans
		pPlayer.setFeatAccomplished(FeatTypes.FEAT_MANIFEST_HORNED_DREAD, True)
		if (pPlayer.getUnitClassCount(self.UnitClasses["Ranger"]) + pPlayer.getUnitClassCount(self.UnitClasses["Haunt"])) < 1:
			pPlayer.setFeatAccomplished(FeatTypes.FEAT_MANIFEST_FIRST_HORNED_DREAD, False)

	### TODO: Dictionaries
	def doChanceAwakenedSpawn(self, iPlayer):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		# Stasis
		if pPlayer.getDisableProduction() > 0:
			pPlayer.setCivCounter(0)
			return
		# Low pop & cap
		tScionCap	= self.calculateScionCap(iPlayer)
		if tScionCap == -1:
			pPlayer.setCivCounter(0)
			return
		iCurPop		= tScionCap[0]
		iMaxPop		= float(tScionCap[1])
		if iCurPop > iMaxPop:
			pPlayer.setCivCounter(0)
			return
		iMultLow	= 1
		if iCurPop < 6: iMultLow = 1.5
		iMultCap	= 1
		if iCurPop * 2 > iMaxPop:
			iMultCap = (iMaxPop - iCurPop) / ( iMaxPop / 2 )
			iMultCap = max(0, iMultCap)
		# Base
		iAddBase	= 3
		# Civics
		iLeader		= pPlayer.getLeaderType()
		iAddCivic	= 0
		iMultCivic	= 1
		if   pPlayer.isCivic(self.Civics["God King"]):
			if gc.getInfoTypeForString("MODULE_MCWHK") != -1:
				if iLeader == gc.getInfoTypeForString("LEADER_KOUNPEROR"):
					iMultCivic = 1.25
			if iLeader == self.Leaders["Risen Emperor"]:
				iMultCivic = 1.25
		elif pPlayer.isCivic(self.Civics["Aristocracy"]):
			iAddCivic = 5
			if iLeader == self.Leaders["Korrina"]:
				iMultCivic = 1.25
		# AI
		iMultAI		= 1
		if not pPlayer.isHuman(): iMultAI = 2.5
		# Speed Multi
		iMultSpeed	= float(gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent()) / 100
		if iMultSpeed == 0: iMultSpeed = 1
		# Bonuses
		iAddBonus	= 0
		for iBonus in xrange(gc.getNumBonusInfos()):
			if not pPlayer.hasBonus(iBonus): continue
			if gc.getBonusInfo(iBonus).getHappiness() > 0:
				iAddBonus += 0.5
			if iBonus == self.Mana["Body"]:
				if not pPlayer.countNumBuildings(self.Buildings["Flesh Studio"]): continue
				iAddBonus += pPlayer.getNumAvailableBonuses(iBonus)
			if iBonus == self.Resources["Patrian"]:
				iAddBonus += pPlayer.getNumAvailableBonuses(iBonus)
		# Buildings
		iAddBuild	= 0
		iAddBuild	+= pPlayer.countNumBuildings(self.Buildings["Hall of the Covenant"])
		iAddBuild	+= pPlayer.countNumBuildings(self.Buildings["Imperial Cenotaph"])
		iAddBuild	+= pPlayer.countNumBuildings(self.Buildings["Temple of the Gift"])		* 0.5
		iAddBuild	+= pPlayer.countNumBuildings(self.Buildings["Shrine to Kylorin"])		* 0.5
		iAddBuild	+= pPlayer.countNumBuildings(self.Buildings["Unhealthy Discontent I"])	* -2
		iAddBuild	+= pPlayer.countNumBuildings(self.Buildings["Unhealthy Discontent II"])	* -4
		# RoP
		iAddRoP		= 0
		if pPlayer.getImprovementCount(self.UniqueImprovements["Remnants of Patria"]) > 0: iAddRoP = 5
		# Calc
		iSpawnChance = round(((iAddBase + iAddCivic + iAddBonus + iAddBuild) * iMultLow * iMultCap * iMultCivic * iMultAI / iMultSpeed ), 2)
		iSpawnChance = int(iSpawnChance * 100)
		pPlayer.setCivCounter(iSpawnChance)

	def calculateScionCap(self, iPlayer):
		if self.UnitCombats == {}: self.initialize()
		pPlayer		= CyGlobalContext().getPlayer(iPlayer)
		pTomb		= pPlayer.getCapitalCity()
		if pTomb.isNone(): return -1
		iMaxPop		= 10;
		iCurPop		= 0
		iOwnedPlots	= pPlayer.getTotalLand()
		iMaxPop		= max(iMaxPop, iOwnedPlots / 2)
		iCurPop		+= pPlayer.getTotalPopulation()
		iCurPop		+= pPlayer.getUnitClassCount(self.UnitClasses["Awakened"])
		iCurPop		+= pPlayer.getUnitClassCount(self.UnitClasses["Reborn"])
		tScionCap = (iCurPop, iMaxPop)
		return tScionCap
	### Scions End

	### Grigori Adventurer Start
#	def doTurnGrigori(self, iPlayer):
#		gc				= CyGlobalContext()
#		pPlayer			= gc.getPlayer(iPlayer)
#		pCapital		= pPlayer.getCapitalCity()
#		if pCapital.isNone(): return
#		iChange			= self.doChanceAdventurerSpawn(iPlayer)
#		pPlayer.changeCivCounter(iChange)
#		iGrigoriSpawn	= pPlayer.getCivCounter()
#		iGrigoriMod		= pPlayer.getCivCounterMod()
#
#		if iGrigoriMod < 10000:
#			pPlayer.setCivCounterMod(10000)
#			iGrigoriMod = 10000
#
#		if iGrigoriSpawn >= iGrigoriMod:
#			spawnUnit = pPlayer.initUnit(self.Units["Grigori"]["Adventurer"], pCapital.getX(), pCapital.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
#			pPlayer.changeCivCounter(-iGrigoriMod)
#			pPlayer.changeCivCounterMod(2000)
#
#	def doChanceAdventurerSpawn(self, iPlayer):
#		gc				= CyGlobalContext()
#		pPlayer			= gc.getPlayer(iPlayer)
#		iPalaceMod		= pPlayer.countNumBuildings(self.Buildings["Grigori Palace"])
#		iDagdaMod		= pPlayer.countNumBuildings(self.Buildings["Grigori Temple"]) * 0.33
#		iMuseumMod		= pPlayer.countNumBuildings(self.Buildings["Museum"]) * 0.33
#		iTavernsMod		= pPlayer.countNumBuildings(self.Buildings["Tavern"])
#		iGuildsMod		= pPlayer.countNumBuildings(self.Buildings["Adventurers Guild"]) * 0.5
#		iRefugeMod		= pPlayer.countNumBuildings(self.Buildings["Dwelling of Refuge"])
#		iNumBountyMinor	= pPlayer.countNumBuildings(self.Buildings["Crime Bounty Minor"])
#		iNumBountyMajor	= pPlayer.countNumBuildings(self.Buildings["Crime Bounty Major"])
#		iNumBountyGrand	= pPlayer.countNumBuildings(self.Buildings["Crime Bounty Grand"])
#		iCivicMod 		= 0.00
#		iCivicMult 		= 1
#		if pPlayer.isCivic(self.Civics["Apprenticeship"]):
#			iCivicMod	= 2
#			iCivicMult	= 1.25
#
#		# Allows Statesmen to take affect after their city has an Assembly
#		iStatesmanMod 	= 0.00
#		iNumStatesmen 	= 0
#		(pCity, iter) = pPlayer.firstCity(False)
#		while(pCity):
#			if pCity.getNumBuilding(self.Buildings["Forum"]) > 0:
#				iNumStatesmen = (pCity.getSpecialistCount(self.Specialists["Statesman"]) + pCity.getFreeSpecialistCount(self.Specialists["Statesman"]))
#				iStatesmanMod += (iNumStatesmen * 0.33)
#			(pCity, iter) = pPlayer.nextCity(iter, False)
#		# AI modifier
#		iAImod = 1
#		if not pPlayer.isHuman():
#			iAImod = 1.5
#
#		iGrigoriSpawn = round(((iPalaceMod + iDagdaMod + iMuseumMod +iTavernsMod + iGuildsMod + iNumBountyMinor + iNumBountyMajor + iNumBountyGrand + iCivicMod + iStatesmanMod + iRefugeMod) * iCivicMult * iAImod), 2)
#		iGrigoriSpawn = int(iGrigoriSpawn * 100)
#		iGrigoriSpawn = scaleInverse(iGrigoriSpawn)
#		return iGrigoriSpawn
	### Grigori Adventurer End

	### Mekara Aspirant Start
#	def doTurnMekara(self, iPlayer):
#		gc				= CyGlobalContext()
#		pPlayer			= gc.getPlayer(iPlayer)
#		pCapital		= pPlayer.getCapitalCity()
#		if pPlayer.getLeaderType() != self.Leaders["Iram Damarr"]:	return
#		if pCapital.isNone():										return
#		iChange			= self.doChanceAspirantSpawn(iPlayer)
#		pPlayer.changeCivCounter(iChange)
#		iMekaraSpawn	= pPlayer.getCivCounter()
#		iMekaraMod		= pPlayer.getCivCounterMod()
#
#		if iMekaraMod < 10000:
#			pPlayer.setCivCounterMod(10000)
#			iMekaraMod = 10000
#
#		if iMekaraSpawn >= iMekaraMod:
#			spawnUnit = pPlayer.initUnit(self.Units["Mekara Order"]["Aspirant"], pCapital.getX(), pCapital.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
#			pPlayer.changeCivCounter(-iMekaraMod)
#			pPlayer.changeCivCounterMod(2000)
#
#	def doChanceAspirantSpawn(self, iPlayer):
#		gc				= CyGlobalContext()
#		pPlayer			= gc.getPlayer(iPlayer)
#		# +2 for each Lab, +1 for each Mage Guild, +2/+25% with Slavery, +3 from Humanist I, +5/+25% from Humanist II, +10/+50% from Humanist III
#		iBaseMod		= 3
#		iLabMod			= pPlayer.countNumBuildings(self.Buildings["Shaper Cabal"]) * 2
#		iCabalMod		= pPlayer.countNumBuildings(self.Buildings["Shaper's Laboratory"])
#		iCivicMod		= 0.00
#		iCivicMult		= 1
#		if pPlayer.isCivic(self.Civics["Slavery"]):
#			iCivicMod	= 2
#			iCivicMult	= 1.25
#		# Allows Healers (+1 for every 2) and Elders (+1 for every 3) to take effect with Labs.
#		iHealer 		= self.Specialists["Healer"]
#		iElder 			= self.Specialists["Scientist"]
#		iGreatHealer 	= self.Specialists["Great Healer"]
#		iGreatElder 	= self.Specialists["Great Scientist"]
#
#		iSpecialistMod		= 0.00
#		iNumHealers			= 0
#		iNumGreatHealers	= 0
#		iNumElders			= 0
#		iNumGreatElders		= 0
#		(pCity, iter) = pPlayer.firstCity(False)
#		while(pCity):
#			if pCity.getNumBuilding(self.Buildings["Shaper's Laboratory"]) > 0:
#				iNumElders			= pCity.getSpecialistCount(iElder)			+ pCity.getFreeSpecialistCount(iElder)
#				iNumHealers			= pCity.getSpecialistCount(iHealer)			+ pCity.getFreeSpecialistCount(iHealer)
#				iNumGreatElders		= pCity.getSpecialistCount(iGreatElder)		+ pCity.getFreeSpecialistCount(iGreatElder)
#				iNumGreatHealers	= pCity.getSpecialistCount(iGreatHealer)	+ pCity.getFreeSpecialistCount(iGreatHealer)
#				iSpecialistMod		+= (iNumHealers * 0.5) + (iNumElders * 0.5) + (iNumGreatElders * 1) + (iNumGreatHealers * 1)
#			(pCity, iter) = pPlayer.nextCity(iter, False)
#		# AI modifier
#		iAImod = 1
#		if not pPlayer.isHuman():
#			iAImod = 1.5
#
#		iMekaraSpawn = round(((iLabMod + iCabalMod + iCivicMod + iBaseMod + iSpecialistMod) * iCivicMult * iAImod), 2)
#		iMekaraSpawn = int(iMekaraSpawn * 100)
#		iMekaraSpawn = scaleInverse(iMekaraSpawn)
#		return iMekaraSpawn
	### Mekara Aspirant Start

	### Doviello Start
	def doCityTurnDoviello(self, iPlayer, pCity):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		pPlot		= pCity.plot()
		iReligion	= pPlayer.getStateReligion()

		self.doChanceAnimalSpawn(iPlayer, pCity)
		iAnimalSpawnChance = pCity.getCityCounter()

		if CyGame().getSorenRandNum(10000, "Animal Spawn") >= iAnimalSpawnChance: return
		lList		= self.doAnimalListDoviello(iPlayer)
		iUnit		= lList[CyGame().getSorenRandNum(len(lList), "Pick Animal")]
		newUnit		= pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(self.Promotions["Effects"]["Loyalty III"], True)

		szText		= CyTranslator().getText("TXT_KEY_MESSAGE_ANIMAL_SPAWN",())
		szSound		= 'AS2D_DISCOVERBONUS'
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		szArt		= gc.getUnitInfo(newUnit.getUnitType()).getButton()
		iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
		CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, pCity.getX(), pCity.getY(), True, True)

		if iReligion != -1:
			newUnit.setReligion(iReligion)
		if pPlayer.isCivic(self.Civics["Wild Council"]):
			newUnit.setHasPromotion(self.Promotions["Effects"]["Heroic Strength I"], True)

	### TODO: Dictionaries
	def doChanceAnimalSpawn(self, iPlayer, pCity):
		gc				= CyGlobalContext()
		pPlayer			= gc.getPlayer(iPlayer)
		iDenPop			= (pCity.getPopulation() - 1) * 0.6
		iSpawnChance	= 8
		iReligion		= pPlayer.getStateReligion()
		if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_BEAR_CAVE"))>0:
			iSpawnChance += 0.5
		if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_GORILLA_FOREST"))>0:
			iSpawnChance += 0.5
		if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_LION_SAVANNA"))>0:
			iSpawnChance += 0.5
		if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_TIGER_MANGROVE"))>0:
			iSpawnChance += 0.5
		if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_WOLF_BURROW"))>0:
			iSpawnChance += 0.5
		if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_CRIME_RAVENOUS_PACK"))>0:
			iSpawnChance += 1
		if pCity.getNumBuilding(gc.getInfoTypeForString("BUILDING_CRIME_RAVENOUS_PACK_ESUS"))>0:
			iSpawnChance += 1
		if pPlayer.isCivic(self.Civics["Wild Council"]):
			iSpawnChance = iSpawnChance * 2
		if iReligion == self.Religions["Fellowship"]:
			iSpawnChance = iSpawnChance * 1.5

		iAnimalSpawnChance = iSpawnChance - iDenPop
		iAnimalSpawnChance = (iAnimalSpawnChance * 100)
		iAnimalSpawnChance = scaleInverse(iAnimalSpawnChance)

		pCity.setCityCounter(iAnimalSpawnChance)

	def doAnimalListDoviello(self, iPlayer):
		gc				= CyGlobalContext()
		pPlayer			= gc.getPlayer(iPlayer)
		lUnits			= []

		if   pPlayer.isHasTech( self.Techs["Feral Bond"]):			lUnits.append(self.Units["Animal"]["Dire Wolf"])
		elif pPlayer.isHasTech( self.Techs["Tracking"]):				lUnits.append(self.Units["Animal"]["Wolf Pack"])
		else:														lUnits.append(self.Units["Animal"]["Wolf"])

		if pPlayer.getBuildingClassCount(self.BuildingClasses["Bear Den"]) >= 1:
			if   pPlayer.isHasTech(self.Techs["Iron Working"]):		lUnits.append(self.Units["Animal"]["Cave Bears"])
			elif pPlayer.isHasTech(self.Techs["Bronze Working"]):		lUnits.append(self.Units["Animal"]["Bear group"])
			else:													lUnits.append(self.Units["Animal"]["Bear"])

		if pPlayer.getBuildingClassCount(self.BuildingClasses["Boar Pen"]) >= 1:
			if   pPlayer.isHasTech(self.Techs["Engineering"]):		lUnits.append(self.Units["Animal"]["Blood Boar"])
			elif pPlayer.isHasTech(self.Techs["Construction"]):		lUnits.append(self.Units["Animal"]["Boar Herd"])
			else:													lUnits.append(self.Units["Animal"]["Boar"])

		if pPlayer.getBuildingClassCount(self.BuildingClasses["Gorilla Hut"]) >= 1:
			if   pPlayer.isHasTech(self.Techs["Bowyers"]):			lUnits.append(self.Units["Animal"]["Silverback"])
			elif pPlayer.isHasTech(self.Techs["Archery"] ):			lUnits.append(self.Units["Animal"]["Gorilla Troop"])
			else:													lUnits.append(self.Units["Animal"]["Gorilla"])

		if pPlayer.getBuildingClassCount(self.BuildingClasses["Griffin Weyr"]) >= 1:
			if   pPlayer.isHasTech(self.Techs["Stirrups"]):			lUnits.append(self.Units["Animal"]["Roc"])
			elif pPlayer.isHasTech(self.Techs["Horseback Riding"]):	lUnits.append(self.Units["Animal"]["Griffon"])
			else:													lUnits.append(self.Units["Animal"]["Hippogriff"])

		if pPlayer.getBuildingClassCount(self.BuildingClasses["Stag Copse"]) >= 1:
			if   pPlayer.isHasTech(self.Techs["Priesthood"]):			lUnits.append(self.Units["Animal"]["Stag"])
			else:													lUnits.append(self.Units["Animal"]["Elk"])

		return lUnits
	### Doviello End

	### Sheaim Start
	def doCityTurnPlanarGate(self, iPlayer, pCity):
		gc 					= CyGlobalContext()
		self.doPlanarGateChance(iPlayer, pCity)
		iPlanarGateChance	= pCity.getCityCounter()
		pPlayer 			= gc.getPlayer(iPlayer)
		if CyGame().getSorenRandNum(10000, "Planar Gate") > iPlanarGateChance: return
		lUnits				= self.doListPlanarGate(iPlayer, pCity)
		if not lUnits: return
		iUnit				= lUnits[CyGame().getSorenRandNum(len(lUnits), "Planar Gate")]
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		szText		= CyTranslator().getText("TXT_KEY_MESSAGE_PLANAR_GATE",())
		szSound		= 'AS2D_DISCOVERBONUS'
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		szArt		= gc.getUnitInfo(newUnit.getUnitType()).getButton()
		iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
		CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, pCity.getX(), pCity.getY(), True, True)

		if iUnit == self.Units["Sheaim"]["Mobius Witch"]:
			fSpheres	= (	self.Promotions["Generic"]["Air I"],	self.Promotions["Generic"]["Earth I"],		self.Promotions["Generic"]["Fire I"],			self.Promotions["Generic"]["Ice I"],		self.Promotions["Generic"]["Water I"],
							self.Promotions["Generic"]["Chaos I"],	self.Promotions["Generic"]["Death I"],		self.Promotions["Generic"]["Dimensional I"],	self.Promotions["Generic"]["Entropy I"],	self.Promotions["Generic"]["Shadow I"],
							self.Promotions["Generic"]["Body I"],	self.Promotions["Generic"]["Creation I"],	self.Promotions["Generic"]["Enchantment I"],	self.Promotions["Generic"]["Force I"],		self.Promotions["Generic"]["Nature I"],
							self.Promotions["Generic"]["Metamagic I"])
			newUnit.setLevel(3)
			newUnit.setExperienceTimes100(1000 + CyGame().getGlobalCounter() * 25, -1)
			for iSphere in fSpheres:
				if CyGame().getSorenRandNum(8, "Mobius Witch Free Promotions") != 0: continue
				newUnit.setHasPromotion(iSphere, True)
		else:
			newUnit.setExperienceTimes100(CyGame().getGlobalCounter() * 25, -1)

	def doPlanarGateChance(self, iPlayer, pCity):
		gc		= CyGlobalContext()
		iX		= pCity.getX()
		iY		= pCity.getY()
		iMult	= 1
		iHell	= 0.00
		iAC		= CyGame().getGlobalCounter()
		iMult += iAC * 0.015

		for iiX,iiY in BFC:
			pLoopPlot = CyMap().plot(iX+iiX,iY+iiY)
			if pLoopPlot.isNone(): continue
			if gc.getTerrainInfo(pLoopPlot.getTerrainType()).isHell(): iHell += 0.05
		iMult += iHell

		iPlanarGateChance = int(self.Defines["Planar Gate"] * iMult)
		iPlanarGateChance = scaleInverse(iPlanarGateChance)

		pCity.setCityCounter(iPlanarGateChance)

	def doListPlanarGate(self, iPlayer, pCity):
		gc = CyGlobalContext()
		pPlayer = gc.getPlayer(iPlayer)

		iMax = 1
		iCounter = CyGame().getGlobalCounter()
		if   iCounter >= 100: iMax = 4
		elif iCounter >= 75:  iMax = 3
		elif iCounter >= 50:  iMax = 2
		iMax = iMax * pPlayer.countNumBuildings( self.Buildings["Planar Gate"])

		lUnits = []

		if pPlayer.getUnitClassCount(self.UnitClasses["Fireball"]) < iMax:				lUnits.append(self.Units["Sheaim"]["Burning Eye"])
		if pCity.getNumBuilding(self.Buildings["Gambling House"]) > 0:
			if pPlayer.getUnitClassCount(self.UnitClasses["Revelers"]) < iMax:			lUnits.append(self.Units["Sheaim"]["Revelers"])
		if pCity.getNumBuilding(self.Buildings["Mage Guild"]) > 0:
			if pPlayer.getUnitClassCount(self.UnitClasses["Mobius Witch"]) < iMax:		lUnits.append(self.Units["Sheaim"]["Mobius Witch"])
		if pCity.getNumBuilding(self.Buildings["Carnival"]) > 0:
			if pPlayer.getUnitClassCount(self.UnitClasses["Chaos Marauder"]) < iMax:	lUnits.append(self.Units["Sheaim"]["Chaos Marauder"])
		if pCity.getNumBuilding(self.Buildings["Grove"]) > 0:
			if pPlayer.getUnitClassCount(self.UnitClasses["Manticore"]) < iMax:			lUnits.append(self.Units["Sheaim"]["Manticore"])
		if pCity.getNumBuilding(self.Buildings["Public Baths"]) > 0:
			if pPlayer.getUnitClassCount(self.UnitClasses["Succubus"]) < iMax:			lUnits.append(self.Units["Sheaim"]["Succubus"])
		if pCity.getNumBuilding(self.Buildings["Obsidian Gate"]) > 0:
			if pPlayer.getUnitClassCount(self.UnitClasses["Minotaur"]) < iMax:			lUnits.append(self.Units["Sheaim"]["Minotaur"])
		if pCity.getNumBuilding(self.Buildings["Barracks"]) > 0:
			if pPlayer.getUnitClassCount(self.UnitClasses["Colubra"]) < iMax:			lUnits.append(self.Units["Sheaim"]["Colubra"])
		if pCity.getNumBuilding(self.Buildings["Temple of the Veil"]) > 0:
			if pPlayer.getUnitClassCount(self.UnitClasses["Tar Demon"]) < iMax:			lUnits.append(self.Units["Sheaim"]["Tar Demon"])
		return lUnits
	### Sheaim End

	### Memorial of the Refugee Start
	def doCityTurnMemorial(self, iPlayer, pCity):
		gc 				= CyGlobalContext()
		pPlot 			= pCity.plot()
		pPlayer 		= gc.getPlayer(iPlayer)

		self.doMemorialChance(iPlayer, pCity)
		iMemorialChance	= pCity.getCityCounter()

		if CyGame().getSorenRandNum(10000, "Refugee") > iMemorialChance: return

		newUnit = pPlayer.initUnit(self.Units["Grigori"]["Refugee"], pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		szText		= CyTranslator().getText("TXT_KEY_MESSAGE_REFUGEE",())
		szSound		= 'AS2D_DISCOVERBONUS'
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		szArt		= gc.getUnitInfo(newUnit.getUnitType()).getButton()
		iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
		CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, pCity.getX(), pCity.getY(), True, True)
		if CyGame().getSorenRandNum(100, "MotR Race") <= 50:
			lRace = [	self.Promotions["Race"]["Angel"],		self.Promotions["Race"]["Dark Elven"],		self.Promotions["Race"]["Elven"],
						self.Promotions["Race"]["Orcish"],		self.Promotions["Race"]["Musteval"],		self.Promotions["Race"]["Lizardman"],
						self.Promotions["Race"]["Goblinoid"],	self.Promotions["Race"]["Fallen Angel"],	self.Promotions["Race"]["Centaur"]]
			iRace = lRace[CyGame().getSorenRandNum(len(lRace), "Pick Race")]
			newUnit.setHasPromotion(iRace, True)
		if CyGame().getSorenRandNum(100, "MotR Hero") <= 10:
			newUnit.setHasPromotion(self.Promotions["Effects"]["Hero"], True)
			newUnit.setName(self.MarnokNameGenerator(newUnit))

	def doMemorialChance(self, iPlayer, pCity):
		iChance		= 0
		if pCity.getNumBuilding(self.Buildings["Memorial Refugee"]) > 0:	iChance += 400
		if pCity.getNumBuilding(self.Buildings["Dwelling of Refuge"]) > 0:	iChance += 200

		iChance = scaleInverse(iChance)

		pCity.setCityCounter(iChance)
	### Memorial of the Refugee End

	def genesis(self, iPlayer):
		for i in xrange(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getOwner() != iPlayer: continue
			iFeature = pPlot.getFeatureType()
			iTerrain = pPlot.getTerrainType()
			if   iTerrain == self.Terrain["Tundra"]:										pPlot.setTerrainType(self.Terrain["Taiga"], False, False)
			elif iTerrain == self.Terrain["Taiga"]:											pPlot.setTerrainType(self.Terrain["Plains"], False, False)
			elif iTerrain == self.Terrain["Desert"] and iFeature != self.Feature["Oasis"]:	pPlot.setTerrainType(self.Terrain["Plains"], False, False)
			elif iTerrain == self.Terrain["Plains"]:										pPlot.setTerrainType(self.Terrain["Grass"], False, False)
			elif iTerrain == self.Terrain["Grass"] and pPlot.getImprovementType() == -1 and not iFeature in (self.Feature["Ancient Forest"], self.Feature["Volcano"]) and not pPlot.isPeak():
				pPlot.setFeatureType(self.Feature["Forest"], 0)

	def getAshenVeilCity(self, iNum):
		gc = CyGlobalContext()
		lValuedCities	= []
		pBestCity1 =	-1
		pBestCity2 =	-1
		pBestCity3 =	-1
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if not pPlayer.isAlive() or pPlayer.getCivilizationType() == self.Civilizations["Infernal"]: continue
			(pCity, iter) = pPlayer.firstCity(False)
			while(pCity):
				if pCity.isHasReligion(self.Religions["Ashen Veil"]) and not pCity.isCapital():
					iValue =  pCity.getPopulation() * 100
					iValue += pCity.getCulture(iPlayer) / 50
					iValue += pCity.getNumBuildings() * 10
					iValue += pCity.getNumWorldWonders() * 200
					iValue += pCity.countNumImprovedPlots() * 20
					lValuedCities.append((pCity,iValue))
				(pCity, iter) = pPlayer.nextCity(iter, False)
		lValuedCities.sort(key=lambda tup: tup[1], reverse=True)
		if len(lValuedCities) > 3:
			pBestCity1 = lValuedCities[0][0]
			pBestCity2 = lValuedCities[1][0]
			pBestCity3 = lValuedCities[2][0]
		if   iNum == 1: return pBestCity1
		elif iNum == 2: return pBestCity2
		elif iNum == 3: return pBestCity3
		return -1

	### TODO: Update
	def getHero(self, pPlayer):
		iCiv 		= pPlayer.getCivilizationType()
		# Grey Fox: changed most if's to elif, cause pointless to check all
		if   iCiv == self.Civilizations["Bannor"]:			return self.Heroes["Class-Donal"]
		elif iCiv == self.Civilizations["Malakim"]:			return self.Heroes["Class-Teutorix"]
		elif iCiv == self.Civilizations["Elohim"]:			return self.Heroes["Class-Corlindale"]
		elif iCiv == self.Civilizations["Mercurians"]:		return self.Heroes["Class-Basium"]
		elif iCiv == self.Civilizations["Lanun"]:			return self.Heroes["Class-Guybrush"]
		elif iCiv == self.Civilizations["Kuriotates"]:		return self.Heroes["Class-Eurabatres"]
		elif iCiv == self.Civilizations["Ljosalfar"]:		return self.Heroes["Class-Gilden"]
		elif iCiv == self.Civilizations["Khazad"]:			return self.Heroes["Class-Maros"]
		elif iCiv == self.Civilizations["Hippus"]:			return self.Heroes["Class-Magnadine"]
		elif iCiv == self.Civilizations["Amurites"]:		return self.Heroes["Class-Govannon"]
		elif iCiv == self.Civilizations["Balseraphs"]:		return self.Heroes["Class-Loki"]
		elif iCiv == self.Civilizations["Clan of Embers"]:	return self.Heroes["Class-Rantine"]
		elif iCiv == self.Civilizations["Svartalfar"]:		return self.Heroes["Class-Alazkan"]
		elif iCiv == self.Civilizations["Calabim"]:			return self.Heroes["Class-Losha"]
		elif iCiv == self.Civilizations["Sheaim"]:			return self.Heroes["Class-Abashi"]
		elif iCiv == self.Civilizations["Sidar"]:			return self.Heroes["Class-Rathus"]
		elif iCiv == self.Civilizations["Illians"]:			return self.Heroes["Class-Wilboman"]
		elif iCiv == self.Civilizations["Infernal"]:		return self.Heroes["Class-Hyborem"]
		elif iCiv == self.Civilizations["Dural"]:			return self.Heroes["Class-Karrlson"]
		elif iCiv == self.Civilizations["Chislev"]:			return self.Heroes["Class-Meshwaki"]
		elif iCiv == self.Civilizations["Archos"]:			return self.Heroes["Class-Mother"]
		elif iCiv == self.Civilizations["Mazatl"]:			return self.Heroes["Class-Coatlann"]
		elif iCiv == self.Civilizations["Cualli"]:			return self.Heroes["Class-Miquiztli"]
		elif iCiv == self.Civilizations["Austrin"]:			return self.Heroes["Class-Harmatt"]
		elif iCiv == self.Civilizations["Scions"]:
			iLeader = pPlayer.getLeaderType()
			if   iLeader == self.Leaders["Risen Emperor"]:	return self.Heroes["Class-Korrina"]
			elif iLeader == self.Leaders["Korrina"]:		return self.Heroes["Class-The Risen Emperor"]
		elif iCiv == self.Civilizations["Frozen"]:			return self.Heroes["Class-Taranis"] # TODO Ronkhar: make modular and move to frozen module
		elif iCiv == self.Civilizations["Mechanos"]:		return self.Heroes["Class-Feris"]

		return -1

	def getUnholyVersion(self, pUnit):
		if( self.UnitCombats=={}): self.initialize()
		gc			= CyGlobalContext()
		iUnitCombat	= pUnit.getUnitCombatType()
		iTier		= gc.getUnitInfo(pUnit.getUnitType()).getTier()
		if   iUnitCombat == self.UnitCombats["Adept"]:
			if   iTier == 2: return self.Units["Infernal"]["Imp"]
			elif iTier == 3: return self.Units["Generic"]["Mage"]
			elif iTier == 4: return self.Units["Summons"]["Lich"]
		elif iUnitCombat in (self.UnitCombats["Animal"], self.UnitCombats["Beast"]):
			if   iTier == 1: return self.Units["Generic"]["Scout"]
			elif iTier == 2: return self.Units["Infernal"]["Hellhound"]
			elif iTier == 3: return self.Units["Generic"]["Assassin"]
			elif iTier == 4: return self.Units["Veil"]["Beast of Agares"]
		elif iUnitCombat == self.UnitCombats["Archer"]:
			if   iTier == 2: return self.Units["Generic"]["Archer"]
			elif iTier == 3: return self.Units["Generic"]["Longbowman"]
			elif iTier == 4: return self.Units["Generic"]["Crossbowman"]
		elif iUnitCombat == self.UnitCombats["Disciple"]:
			if   iTier == 2: return self.Units["Veil"]["Disciple"]
			elif iTier == 3: return self.Units["Veil"]["Ritualist"]
			elif iTier == 4: return self.Units["Generic"]["Eidolon"]
		elif iUnitCombat == self.UnitCombats["Melee"]:
			if   iTier == 1: return self.Units["Summons"]["Skeleton"]
			elif iTier == 2: return self.Units["Veil"]["Diseased Corpse"]
			elif iTier == 3: return self.Units["Generic"]["Champion"]
			elif iTier == 4: return self.Units["Infernal"]["Balor"]
		elif iUnitCombat == self.UnitCombats["Mounted"]:
			if   iTier == 2: return self.Units["Generic"]["Horseman"]
			elif iTier == 3: return self.Units["Generic"]["Chariot"]
			elif iTier == 4: return self.Units["Infernal"]["Death Knight"]
		elif iUnitCombat == self.UnitCombats["Recon"]:
			if   iTier == 1: return self.Units["Generic"]["Scout"]
			elif iTier == 2: return self.Units["Infernal"]["Hellhound"]
			elif iTier == 3: return self.Units["Generic"]["Assassin"]
			elif iTier == 4: return self.Units["Generic"]["Beastmaster"]
		return -1

	def giftUnit(self, iUnit, iCivilization, iXP, pFromPlot, iFromPlayer):
		gc = CyGlobalContext()
		iAngel		= self.Units["Mercurian"]["Angel"]
		iMane		= self.Units["Infernal"]["Manes"]
		iFrozenSoul	= self.Units["Frozen"]["Frozen Souls"]
		if iUnit == -1:
			raise IndexError("giftUnit is called for iUnit = -1. Args: %s, %s, %s, %s, %s" %(str(iUnit), str(iCivilization), str(iXP), str(pFromPlot), str(iFromPlayer)))
			return
		if iUnit in (iAngel, iMane, iFrozenSoul):
			iChance = 100 - (CyGame().countCivPlayersAlive() * 3) + iXP/100
			iChance = min(iChance, 95)
			iChance = max(iChance, 5)
			if CyGame().getSorenRandNum(100, "Gift Unit") > iChance: return
		bValid = False

		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if not pPlayer.isAlive():							continue
			if pPlayer.getCivilizationType() != iCivilization:	continue

#			if iUnit == iFrozenSoul: ### TW: Another chance check is a bit too harsh? Worst case scenario would be 0.25% to get a FS.
#				iChance = 100 * pPlayer.getAveragePopulation() / 15
#				iChance = min(iChance, 95)
#				if CyGame().getSorenRandNum(100, "Gift Frozen Soul") < iChance: break

			iNumCities	= pPlayer.getNumCities()
			if iNumCities <= 0:									continue
			lCities		= []
			(pLoopCity, iter) = pPlayer.firstCity(False)
			while(pLoopCity):
				lCities.append(pLoopCity)
				(pLoopCity, iter) = pPlayer.nextCity(iter, False)
			pCity	= lCities[CyGame().getSorenRandNum(len(lCities), "giftUnit, City Pick")]

			bHuman	= pPlayer.isHuman()
			iX		= pCity.getX()
			iY		= pCity.getY()

			newUnit = pPlayer.initUnit(iUnit, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.changeExperienceTimes100(iXP, -1, False, False, False)
			if bHuman:
				szSound		= 'AS2D_UNIT_FALLS'
				iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
				iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
				if   iUnit == iFrozenSoul:
					szText	= CyTranslator().getText("TXT_KEY_MESSAGE_ADD_FROZEN_SOULS",())
					szArt	= 'Art/Interface/Buttons/Promotions/Races/frostling.dds'
					CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, iX, iY, True, True)
				elif iUnit == iMane:
					szText	= CyTranslator().getText("TXT_KEY_MESSAGE_ADD_MANES",())
					szArt	= 'Art/Interface/Buttons/Promotions/Races/Demon.dds'
					CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, iX, iY, True, True)
				elif iUnit == iAngel:
					szText	= CyTranslator().getText("TXT_KEY_MESSAGE_ADD_ANGEL",())
					szArt	= 'Art/Interface/Buttons/Promotions/Races/Angel.dds'
					CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, iX, iY, True, True)
			elif iUnit in (iMane, iFrozenSoul):
				if CyGame().getSorenRandNum(100, "Manes") >= (100 - (pCity.getPopulation() * 5)): continue
				pCity.changePopulation(1)
				newUnit.kill(True, PlayerTypes.NO_PLAYER)

		if iUnit in (iMane, iFrozenSoul, iAngel) and gc.getPlayer(iFromPlayer).isHuman() and pFromPlot != -1:
			szSound		= 'AS2D_UNIT_FALLS'
			iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_DISPLAY_ONLY
			iRed		= gc.getInfoTypeForString("COLOR_RED")
			if   iUnit == iFrozenSoul:
				szText		= CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_FREEZES",())
				szArt		= 'Art/Interface/Buttons/Promotions/Races/frostling.dds'
			elif iUnit == iMane:
				szText	= CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_FALLS",())
				szArt	= 'Art/Interface/Buttons/Promotions/Races/Demon.dds'
			elif iUnit == iAngel:
				szText	= CyTranslator().getText("TXT_KEY_MESSAGE_UNIT_RISES",())
				szArt	= 'Art/Interface/Buttons/Promotions/Races/Angel.dds'
			CyInterface().addMessage(iFromPlayer, True, 25, szText, szSound, iMessage, szArt, iRed, pFromPlot.getX(), pFromPlot.getY(), True, True)

	def warScript(self, iPlayer):
		gc				= CyGlobalContext()
		pPlayer			= gc.getPlayer(iPlayer)
		iTeam			= pPlayer.getTeam()
		pTeam			= gc.getTeam(iTeam)
		if pTeam.isAVassal(): return
		iCiv			= pPlayer.getCivilizationType()
		iAlignment		= pPlayer.getAlignment()
		iEnemy			= -1
		iCounter		= CyGame().getGlobalCounter()
		WarPlanTotal	= WarPlanTypes.WARPLAN_TOTAL
		iWarCount		= pTeam.getAtWarCount(True)

		for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
			iWarCount	= pTeam.getAtWarCount(True)
			pPlayer2	= gc.getPlayer(iPlayer2)
			if not pPlayer2.isAlive(): continue
			iCiv2		= pPlayer2.getCivilizationType()
			bBetter		= False
			bWorse2		= False

			if CyGame().getPlayerRank(iPlayer2) > CyGame().getPlayerRank(iPlayer):
				bBetter	= True
			if iEnemy == -1 or CyGame().getPlayerRank(iPlayer2) > CyGame().getPlayerRank(iEnemy):
				bWorse2 = True
			iTeam2 = pPlayer2.getTeam()

			if pTeam.isAtWar(iTeam2):
				randName = "War Script, Player %s vs Player %s" % (iPlayer, iPlayer2)
				if CyGame().getSorenRandNum(100, randName) < 5: self.dogpile(iPlayer, iPlayer2)

			if not self.warScriptAllow(iPlayer, iPlayer2): continue

			if iWarCount == 0:
				if   pPlayer2.getBuildingClassMaking(self.BuildingClasses["Tower of Mastery"]) > 0:
					startWar(iPlayer, iPlayer2, WarPlanTotal)
				elif iAlignment == self.Alignments["Evil"]:
					if   pPlayer2.getNumBuilding(self.Buildings["Altar - Divine"]) > 0 or pPlayer2.getNumBuilding(self.Buildings["Altar - Exalted"]) > 0:
						startWar(iPlayer, iPlayer2, WarPlanTotal)
					elif (iCounter > 40 or iCiv in (self.Civilizations["Infernal"], self.Civilizations["Doviello"])) and bBetter and bWorse2:
						iEnemy = iPlayer2
			elif iCiv == self.Civilizations["Mercurians"] and pPlayer2.getStateReligion() == self.Religions["Ashen Veil"]:
				startWar(iPlayer, iPlayer2, WarPlanTotal)
			elif iCounter > 20:
				if iCiv in (self.Civilizations["Svartalfar"], self.Civilizations["Ljosalfar"]) and iCiv2 in (self.Civilizations["Svartalfar"], self.Civilizations["Ljosalfar"]) and bBetter and iCiv != iCiv2:
					startWar(iPlayer, iPlayer2, WarPlanTotal)

		if iEnemy != -1: startWar(iPlayer, iEnemy, WarPlanTotal)

	def warScriptAllow(self, iPlayer, iPlayer2):
		gc 				= CyGlobalContext()
		pPlayer 		= gc.getPlayer(iPlayer)
		pPlayer2 		= gc.getPlayer(iPlayer2)
		iTeam 			= gc.getPlayer(iPlayer).getTeam()
		iTeam2 			= gc.getPlayer(iPlayer2).getTeam()
		pTeam 			= gc.getTeam(iTeam)
		if pPlayer.isBarbarian() or pPlayer2.isBarbarian():	return False
		if pTeam.isHasMet(iTeam2) == False:					return False
		if pTeam.AI_getAtPeaceCounter(iTeam2) < 20:			return False
		if pTeam.isAtWar(iTeam2):							return False
		if pPlayer.getCivilizationType() == self.Civilizations["Infernal"] and pPlayer2.getStateReligion() == self.Religions["Ashen Veil"]: return False
		return True

	def dogpile(self, iPlayer, iVictim):
		gc			= CyGlobalContext()
		iCounter	= CyGame().getGlobalCounter()
		for iPlayer2 in xrange(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			iChance = -1
			if not pPlayer2.isAlive():						continue
			if not self.dogPileAllow(iPlayer, iPlayer2):	continue
			if not self.warScriptAllow(iPlayer2, iVictim):	continue
			iChance = pPlayer2.AI_getAttitude(iPlayer) * 5
			if iChance <= 0:								continue
			iChance -= (pPlayer2.AI_getAttitude(iVictim) * 5) + 10
			if not self.GameOptions["Aggressive AI"]: iChance -= 10
			if iChance <= 0:								continue
			iChance = iChance + (iCounter / 3)
			if pPlayer2.getCivilizationType() == self.Civilizations["Balseraphs"]:
				iChance = CyGame().getSorenRandNum(50, "Dogpile Balseraphs")
			if CyGame().getSorenRandNum(100, "Dogpile") < iChance:
				startWar(iPlayer2, iVictim, WarPlanTypes.WARPLAN_DOGPILE)

	def dogPileAllow(self, iPlayer, iPlayer2):
		gc			= CyGlobalContext()
		getPlayer	= gc.getPlayer
		pPlayer2	= getPlayer(iPlayer2)
		iCiv2		= pPlayer2.getCivilizationType()
		iTeam		= getPlayer(iPlayer).getTeam()
		iTeam2		= getPlayer(iPlayer2).getTeam()
		pTeam2		= gc.getTeam(iTeam2)
		if iPlayer == iPlayer2:						return False
		if iTeam == iTeam2:							return False
		if pPlayer2.isHuman():						return False
		if iCiv2 == self.Civilizations["Elohim"]:	return False
		if pTeam2.isAVassal():						return False
		return True

	def canReceiveReligionUnit(self, pPlayer):
		iCiv = pPlayer.getCivilizationType()
		if   iCiv == self.Civilizations["Cualli"]: return False
	#	elif iCiv == self.Civilizations["Mazatl"]: return False
		return True

	def MarnokNameGenerator(self, pUnit):
		gc 				= CyGlobalContext()
		pPlayer 		= gc.getPlayer(pUnit.getOwner())
		iReligion 		= pPlayer.getStateReligion()
		pAlign 			= pPlayer.getAlignment()
		iUnitType 		= pUnit.getUnitType()

		lPre=["ta","go","da","bar","arc","ken","an","ad","mi","kon","kar","mar","wal","he", "ha", "re", "ar", "bal", "bel", "bo", "bri", "car","dag","dan","ma","ja","co","be","ga","qui","sa"]
		lMid=["ad","z","the","and","tha","ent","ion","tio","for","tis","oft","che","gan","an","en","wen","on","d","n","g","t","ow","dal"]
		lEnd=["ar","sta","na","is","el","es","ie","us","un","th", "er","on","an","re","in","ed","nd","at","en","le","man","ck","ton","nok","git","us","or","a","da","u","cha","ir"]

		lEpithet=["red","blue","black","grey","white","strong","brave","old","young","great","slayer","hunter","seeker"]
		lNoun=["spirit","soul","boon","born","staff","rod","shield","autumn","winter","spring","summer","wit","horn","tusk","glory","claw","tooth","head","heart", "blood","breath", "blade", "hand", "lover","bringer","maker","taker","river","stream","moon","star","face","foot","half","one","hundred","thousand"]
		lSchema=["CPME","CPMESCPME","CPESCPE","CPE","CPMME","CPMDCME","CPMAME","KCPMESCUM","CPMME[ the ]CX", "CPMESCXN", "CPMME[ of ]CPMME", "CNNSCXN"]

		if pAlign == self.Alignments["Evil"]:
			lNoun = lNoun + ["fear","terror","reign","brood","snare","war","strife","pain","hate","evil","hell","misery","murder","anger","fury","rage","spawn","sly","blood","bone","scythe","slave","bound","ooze","scum"]
			lEpithet=["dark","black","white","cruel","foul"]
		if iReligion == self.Religions["Ashen Veil"]:
			lEpithet = lEpithet + ["fallen","diseased","infernal","profane","corrupt"]
			lSchema = lSchema + ["CPME[ the ]CX"]
		if iReligion == self.Religions["Octopus Overlords"]:
			lPre = lPre + ["cth","cht","shu","az","ts","dag","hy","gla","gh","rh","x","ll"]
			lMid = lMid + ["ul","tha","on","ug","st","oi"]
			lEnd = lEnd + ["hu","on", "ha","ua","oa","uth","oth","ath","thua", "thoa","ur","ll","og","hua"]
			lEpithet = lEpithet + ["nameless","webbed","deep","watery"]
			lNoun = lNoun + ["tentacle","wind","wave","sea","ocean","dark","crab","abyss","island"]
			lSchema = lSchema + ["CPMME","CPDMME","CPAMAME","CPMAME","CPAMAMEDCPAMAE"]
		if iReligion == self.Religions["Order"]:
			lPre = lPre + ["ph","v","j"]
			lMid = lMid + ["an","al","un"]
			lEnd = lEnd + ["uel","in","il"]
			lEpithet = lEpithet + ["confessor","crusader", "faithful","obedient","good"]
			lNoun = lNoun + ["order", "faith", "heaven","law"]
			lSchema = lSchema + ["CPESCPME","CPMESCPE","CPMESCPME", "CPESCPE"]
		if iReligion == self.Religions["Fellowship"]:
			lPre = lPre + ["ki","ky","yv"]
			lMid = lMid + ["th","ri"]
			lEnd = lEnd + ["ra","el","ain"]
			lEpithet = lEpithet + ["green"]
			lNoun = lNoun + ["tree","bush","wood","berry","elm","willow","oak","leaf","flower","blossom"]
			lSchema = lSchema + ["CPESCN","CPMESCNN","CPMESCXN"]
		if iReligion == self.Religions["Runes of Kilmorph"]:
			lPre = lPre + ["bam","ar","khel","ki"]
			lMid = lMid + ["th","b","en"]
			lEnd = lEnd + ["ur","dain","ain","don"]
			lEpithet = lEpithet + ["deep","guard","miner"]
			lNoun = lNoun + ["rune","flint","slate","stone","rock","iron","copper","mithril","thane","umber"]
			lSchema = lSchema + ["CPME","CPMME"]
		if iReligion == self.Religions["Empyrean"]:
			lEpithet = lEpithet + ["radiant","holy"]
			lNoun = lNoun + ["honor"]
		if iReligion == self.Religions["Council of Esus"]:
			lEpithet = lEpithet + ["hidden","dark"]
			lNoun = lNoun + ["cloak","shadow","mask"]
			lSchema = lSchema + ["CPME","CPMME"]
		if pUnit.isHasPromotion(self.Promotions["Generic"]["Enraged"]):
			# I have left this as a copy of the Barbarian, see how it goes, this might do the trick. I plan to use it when there is a chance a unit will go Barbarian anyway.
			lPre = lPre + ["gru","bra","no","os","dir","ka","z"]
			lMid = lMid + ["g","ck","gg","sh","b","bh","aa"]
			lEnd = lEnd + ["al","e","ek","esh","ol","olg","alg"]
			lNoun = lNoun + ["death", "hate", "rage", "mad","insane","berserk"]
			lEpithet = lEpithet + ["smasher", "breaker", "mangle","monger"]
		if pUnit.isHasPromotion(self.Promotions["Generic"]["Crazed"]):
			# might want to tone this down, because I plan to use it as possession/driven to madness, less than madcap zaniness.
			lPre = lPre + ["mad","pim","zi","zo","fli","mum","dum","odd","slur"]
			lMid = lMid + ["bl","pl","gg","ug","bl","b","zz","abb","odd"]
			lEnd = lEnd + ["ad","ap","izzle","onk","ing","er","po","eep","oggle","y"]
		if pUnit.isHasPromotion(self.Promotions["Effects"]["Vampire"]):
			lPre = lPre + ["dra","al","nos","vam","vla","tep","bat","bar","cor","lil","ray","zar","stra","le"]
			lMid = lMid + ["cul","u","car","fer","pir","or","na","ov","sta"]
			lEnd = lEnd + ["a","d","u","e","es","y","bas","vin","ith","ne","ak","ich","hd","t"]
		if pUnit.isHasPromotion(self.Promotions["Race"]["Demon"]):
			lPre = lPre + ["aa","ab","adr","ah","al","de","ba","cro","da","be","eu","el","ha","ib","me","she","sth","z"]
			lMid = lMid + ["rax","lia","ri","al","as","b","bh","aa","al","ze","phi","sto","phe","cc","ee"]
			lEnd = lEnd + ["tor","tan","ept","lu","res","ah","mon","gon","bul","gul","lis","les","uz"]
			lSchema = ["CPMMME","CPMACME", "CPKMAUAPUE", "CPMMME[ the ]CNX"]
		if iUnitType == self.Units["Savage"]["Hill Giant"]:
			lPre = lPre + ["gor","gra","gar","gi","gol"]
			lMid = lMid + ["gan","li","ri","go"]
			lEnd = lEnd + ["tus","tan","ath","tha"]
			lSchema = lSchema +["CXNSCNN","CPESCNE", "CPMME[ the ]CX"]
			lEpithet = lEpithet + ["large","huge","collossal","brutal","basher","smasher","crasher","crusher"]
			lNoun = lNoun + ["fist","tor","hill","brute","stomp"]
		if iUnitType == self.Units["Clan of Embers"]["Lizardman"]:
			lPre = lPre + ["ss","s","th","sth","hss"]
			lEnd = lEnd + ["ess","iss","ath","tha"]
			lEpithet = lEpithet + ["cold"]
			lNoun = lNoun + ["hiss","tongue","slither","scale","tail","ruin"]
			lSchema = lSchema + ["CPAECPAE","CPAKECPAU","CPAMMAE"]
		if iUnitType in (self.Units["Summons"]["Fire Elemental"], self.Units["Summons"]["Azer"]):
			lPre = lPre + ["ss","cra","th","sth","hss","roa"]
			lMid = lMid + ["ss","ck","rr","oa","iss","tt"]
			lEnd = lEnd + ["le","iss","st","r","er"]
			lNoun = lNoun + ["hot", "burn","scald","roast","flame","scorch","char","sear","singe","fire","spit"]
			lSchema = ["CNN","CNX","CPME","CPME[ the ]CNX","CPMME","CNNSCPME"]
		if iUnitType == self.Units["Summons"]["Water Elemental"]:
			lPre = lPre + ["who","spl","dr","sl","spr","sw","b"]
			lMid = lMid + ["o","a","i","ub","ib"]
			lEnd = lEnd + ["sh","p","ter","ble"]
			lNoun = lNoun + ["wave","lap","sea","lake","water","tide","surf","spray","wet","damp","soak","gurgle","bubble"]
			lSchema = ["CNN","CNX","CPME","CPME[ the ]CNX","CPMME","CNNSCPME"]
		if iUnitType == self.Units["Summons"]["Air Elemental"]:
			lPre = lPre + ["ff","ph","th","ff","ph","th"]
			lMid = lMid + ["oo","aa","ee","ah","oh"]
			lEnd = lEnd + ["ff","ph","th","ff","ph","th"]
			lNoun = lNoun + ["wind","air","zephyr","breeze","gust","blast","blow"]
			lSchema = ["CNN","CNX","CPME","CPME[ the ]CNX","CPMME","CNNSCPME"]
		if iUnitType == self.Units["Summons"]["Earth Elemental"]:
			lPre = lPre + ["gra","gro","kro","ff","ph","th"]
			lMid = lMid + ["o","a","u"]
			lEnd = lEnd + ["ck","g","k"]
			lNoun = lNoun + ["rock","stone","boulder","slate","granite","rumble","quake"]
			lSchema = ["CNN","CNX","CPME","CPME[ the ]CNX","CPMME","CNNSCPME"]

		# SEA BASED
		# Check for ships - special schemas
		if pUnit.getUnitCombatType() == self.UnitCombats["Naval"]:
			lEnd = lEnd + ["ton","town","port"]
			lNoun = lNoun + ["lady","jolly","keel","bow","stern", "mast","sail","deck","hull","reef","wave"]
			lEpithet = lEpithet + ["sea", "red", "blue","grand","barnacle","gull"]
			lSchema = ["[The ]CNN", "[The ]CXN", "[The ]CNX","[The ]CNSCN", "[The ]CNSCX","CPME['s ]CN","[The ]CPME", "[The ]CNX","CNX","CN['s ]CN"]

		# # #
		# Pick a Schema
		sSchema = lSchema[CyGame().getSorenRandNum(len(lSchema), "Name Gen")]
		sFull = ""
		sKeep = ""
		iUpper = 0
		iKeep = 0
		iSkip = 0

		# Run through each character in schema to generate name
		for iCount in xrange(0,len(sSchema)):
			sAdd=""
			iDone = 0
			sAction = sSchema[iCount]
			if iSkip == 1:
				if sAction == "]":
					iSkip = 0
				else:
					sAdd = sAction
					iDone = 1
			else:					# MAIN SECTION
				if   sAction == "P": 	# Pre 	: beginnings of names
					sAdd = lPre[CyGame().getSorenRandNum(len(lPre), "Name Gen")]
					iDone = 1
				elif sAction == "M":	# Mid 	: middle syllables
					sAdd = lMid[CyGame().getSorenRandNum(len(lMid), "Name Gen")]
					iDone = 1
				elif sAction == "E":	# End	: end of names
					sAdd = lEnd[CyGame().getSorenRandNum(len(lEnd), "Name Gen")]
					iDone = 1
				elif sAction == "X":	# Epithet	: epithet word part
					#epithets ("e" was taken!)
					sAdd = lEpithet[CyGame().getSorenRandNum(len(lEpithet), "Name Gen")]
					iDone = 1
				elif sAction == "N":	# Noun	: noun word part
					#noun
					sAdd = lNoun[CyGame().getSorenRandNum(len(lNoun), "Name Gen")]
					iDone = 1
				elif sAction == "S":	# Space	: a space character. (Introduced before [ ] was possible )
					sAdd =  " "
					iDone = 1
				elif sAction == "D":	# Dash	: a - character. Thought to be common and useful enough to warrant inclusion : Introduced before [-] was possible
					sAdd =  "-"
					iDone = 1
				elif sAction == "A":	# '		: a ' character - as for -, introduced early
					sAdd = "'"
					iDone = 1
				elif sAction == "C":	# Caps	: capitalizes first letter of next phrase generated. No effect on non-letters.
					iUpper = 1
				elif sAction == "K":	# Keep	: stores the next phrase generated for re-use with U
					iKeep = 1
				elif sAction == "U":	# Use	: re-uses a stored phrase.
					sAdd = sKeep
					iDone = 1
				elif sAction == "[":	# Print	: anything between [] is added to the final phrase "as is". Useful for [ the ] and [ of ] among others.
					iSkip = 1
			# capitalizes phrase once.
			if iUpper == 1 and iDone == 1:
				sAdd = sAdd.capitalize()
				iUpper = 0
			# stores the next phrase generated.
			if iKeep == 1 and iDone == 1:
				sKeep = sAdd
				iKeep = 0
			# only adds the phrase if a new bit was actally created.
			if iDone == 1:
				sFull = "%s%s" % (sFull, sAdd)


		# trim name length
		if len(sFull) > 25:
			sFull = sFull[:25]

		return sFull

	### TODO: Dictionaries
	def resetRepublicTraits(self, pPlayer):
		gc = CyGlobalContext()
		for iTrait in xrange(gc.getNumTraitInfos()):
			if gc.getTraitInfo(iTrait).getTraitClass() != gc.getInfoTypeForString("TRAITCLASS_REPUBLIC"): continue
			if not gc.isNoCrash():
				pPlayer.setHasTrait((iTrait),False,-1,True,True)
			else:
				pPlayer.setHasTrait((iTrait),False)

	### TODO: Dictionaries
	def angelorMane(self, pUnit):
		if( self.Religions=={}): self.initialize()
		gc				= CyGlobalContext()
		iUnitCombat		= pUnit.getUnitCombatType()
		iAngel			= self.Units["Mercurian"]["Angel"]
		iMane			= self.Units["Infernal"]["Manes"]
		iFrozenSoul		= self.Units["Frozen"]["Frozen Souls"]
		iFrozen			= self.Civilizations["Frozen"]
		iReligion		= pUnit.getReligion()
		iPlayer			= pUnit.getOwner()
		pPlayer			= gc.getPlayer(iPlayer)
		iLeader			= pPlayer.getLeaderType()
		iAlignment		= pPlayer.getAlignment()
		bPurified		= pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_PURIFIED_WELL'))
		bCanBeFrozen	= False

		if gc.getInfoTypeForString("MODULE_FROZEN") != -1:
			if CyGame().getNumCivActive(iFrozen) > 0:
				bCanBeFrozen = True

		if not pUnit.isAlive():														return -1
		if iUnitCombat in (self.UnitCombats["Animal"], self.UnitCombats["Beast"]):	return -1

		if iReligion == self.Religions["White Hand"]:
			if bCanBeFrozen:	return iFrozenSoul
			else:				return iMane
		if iReligion in (self.Religions["Ashen Veil"],	self.Religions["Octopus Overlords"], self.Religions["Council of Esus"]):
			return iMane
		if iReligion in (self.Religions["Order"],		self.Religions["Empyrean"]):
			return iAngel
		if iReligion in (self.Religions["Fellowship"],	self.Religions["Runes of Kilmorph"]):
			return -1

		lEvilProms = [	gc.getInfoTypeForString('PROMOTION_UNHOLY_TAINT'), gc.getInfoTypeForString('PROMOTION_GULAGARM_POISONED'),
						self.Promotions["Effects"]["Vampire"],
						self.Promotions["Generic"]["Chaos I"],			self.Promotions["Generic"]["Chaos II"],			self.Promotions["Generic"]["Chaos III"],
						self.Promotions["Generic"]["Death I"],			self.Promotions["Generic"]["Death II"],			self.Promotions["Generic"]["Death III"],
						self.Promotions["Generic"]["Dimensional I"],	self.Promotions["Generic"]["Dimensional II"],	self.Promotions["Generic"]["Dimensional III"],
						self.Promotions["Generic"]["Entropy I"],		self.Promotions["Generic"]["Entropy II"],		self.Promotions["Generic"]["Entropy III"],
						self.Promotions["Generic"]["Shadow I"],			self.Promotions["Generic"]["Shadow II"],		self.Promotions["Generic"]["Shadow III"]]
		for iProm in lEvilProms:
			if pUnit.isHasPromotion(iProm):					return iMane

		lGoodProms = []
		for iProm in lGoodProms:
			if pUnit.isHasPromotion(iProm):					return iAngel

		if bCanBeFrozen:
			lFrozenProms = [self.Promotions["Effects"]["Winterborn"],	self.Promotions["Effects"]["Wintered"]]
			for iProm in lFrozenProms:
				if pUnit.isHasPromotion(iProm):				return iFrozenSoul

		if pPlayer.isBarbarian():
			if CyGame().getSorenRandNum(100, "Barb") < 80:	return -1

		if iLeader == self.Leaders["Basium"]:				return iAngel

		iRoll = CyGame().getSorenRandNum(100, "Angel or Mane")
		iGoodThreshold = 5
		iEvilThreshold = 50
		if   iAlignment == self.Alignments["Good"]:
			iGoodThreshold += 15
			iEvilThreshold += 45
		elif iAlignment == self.Alignments["Evil"]:
			iGoodThreshold -= 100
			iEvilThreshold -= 40
		if   bPurified:
			iGoodThreshold += 20
			iEvilThreshold += 40
		if   iRoll < iGoodThreshold:	return iAngel
		elif iRoll > iEvilThreshold:	return iMane
		else:							return -1

	def findImprovements(self, iImprovementType):
		listImprovements = []
		for i in xrange (CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getImprovementType() == iImprovementType:
				listImprovements.append(pPlot)
		return listImprovements

	### TODO: Dictionaries
	# Demon Lord Spawn
	def spawnDemonLord(self,iLeader,iPlayer,bReassign = False):
		if self.UnitCombats == {}: self.initialize()
		iInfernalPlayer	= getOpenPlayer()
		if iInfernalPlayer == -1: return
		gc				= CyGlobalContext()
		git				= gc.getInfoTypeForString
		pBestPlot		= -1
		iBestPlot		= -1
		# Plot Picker
		for i in xrange(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			iPlot = -1
			if pPlot.isWater():				continue
			if pPlot.isCity():				continue
			if pPlot.isImpassable():		continue
			if pPlot.isPeak():				continue
			if pPlot.getNumUnits() != 0:	continue
			iPlot = CyGame().getSorenRandNum(500, "Place Demon Lord")
			iPlot += pPlot.area().getNumTiles() * 2
			iPlot += pPlot.area().getNumUnownedTiles() * 10
			if not pPlot.isOwned():
				iPlot += 500
			if pPlot.getOwner() == iPlayer:
				iPlot += 200
			if iPlot > iBestPlot:
				iBestPlot = iPlot
				pBestPlot = pPlot
		if pBestPlot.isNone(): return
		# Setting Civilization
		# Removing barbs around the plot
		pBestPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
		for iX,iY in RANGE2:
			pClearPlot = CyMap().plot(iX+pBestPlot.getX(),iY+pBestPlot.getY())
			for i in xrange(pClearPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.isBarbarian() and not gc.getUnitClassInfo(pUnit.getUnitClassType()).isUnique():
					pUnit.kill()
		# Spawning Civilization
		CyGame().addPlayerAdvanced(iInfernalPlayer, -1, iLeader, self.Civilizations["Infernal"], iPlayer)
		iFounderTeam	= gc.getPlayer(iPlayer).getTeam()
		eFounderTeam	= gc.getTeam(iFounderTeam)
		iInfernalTeam	= gc.getPlayer(iInfernalPlayer).getTeam()
		eInfernalTeam	= gc.getTeam(iInfernalTeam)
		iDemonTeam		= gc.getPlayer(gc.getDEMON_PLAYER()).getTeam()
		pInfernalPlayer	= gc.getPlayer(iInfernalPlayer)
		iX				= pBestPlot.getX()
		iY				= pBestPlot.getY()
		iAI				= UnitAITypes.NO_UNITAI
		iDirection		= DirectionTypes.DIRECTION_SOUTH
		iArcher			= self.Units["Generic"]["Longbowman"]
		iSect			= self.Units["Infernal"]["Sect of Flies"]
		iWorker			= self.Units["Generic"]["Worker"]
		iImp			= self.Units["Infernal"]["Imp"]
		iMane			= self.Units["Infernal"]["Manes"]
		iSet			= self.Units["Generic"]["Settler"]
		iMobility		= self.Promotions["Generic"]["Mobility I"]
		iStarting		= self.Promotions["Effects"]["Starting Settler"]
		iIron			= self.Promotions["Effects"]["Iron Weapons"]
		# Unique spawn for Demon Leader
		iHero = -1
		if   iLeader == self.Leaders["Hyborem"]:	iHero = self.Heroes["Hyborem"]
		elif iLeader == git("LEADER_JUDECCA"):		iHero = git("UNIT_JUDECCA")
		elif iLeader == git("LEADER_LETHE"):		iHero = git("UNIT_LETHE")
		elif iLeader == git("LEADER_MERESIN"):		iHero = git("UNIT_MERESIN")
		elif iLeader == git("LEADER_OUZZA"):		iHero = git("UNIT_OUZZA")
		elif iLeader == git("LEADER_SALLOS"):		iHero = git("UNIT_SALLOS")
		elif iLeader == git("LEADER_STATIUS"):		iHero = git("UNIT_STATIUS")
		if   iHero != -1:
			NewUnitHero = pInfernalPlayer.initUnit(iHero, iX, iY, iAI, iDirection)
			NewUnitHero.setHasPromotion(self.Promotions["Effects"]["Immortal"], True)
		# Common spawn between demons 
		NewUnitArcher1	= pInfernalPlayer.initUnit(iArcher,	iX, iY, iAI, iDirection)
		NewUnitArcher2	= pInfernalPlayer.initUnit(iArcher,	iX, iY, iAI, iDirection)
		NewUnitChamp1	= pInfernalPlayer.initUnit(iSect,	iX, iY, iAI, iDirection)
		NewUnitChamp2	= pInfernalPlayer.initUnit(iSect,	iX, iY, iAI, iDirection)
		NewUnitWorker	= pInfernalPlayer.initUnit(iWorker,	iX, iY, iAI, iDirection)
		NewUnitImp		= pInfernalPlayer.initUnit(iImp,	iX, iY, iAI, iDirection)
		NewUnitMane1	= pInfernalPlayer.initUnit(iMane,	iX, iY, iAI, iDirection)
		NewUnitMane2	= pInfernalPlayer.initUnit(iMane,	iX, iY, iAI, iDirection)
		NewUnitMane3	= pInfernalPlayer.initUnit(iMane,	iX, iY, iAI, iDirection)
		NewUnitSettler1	= pInfernalPlayer.initUnit(iSet,	iX, iY, iAI, iDirection)
		NewUnitSettler2	= pInfernalPlayer.initUnit(iSet,	iX, iY, iAI, iDirection)

		NewUnitArcher1.setHasPromotion(iMobility,	True)
		NewUnitArcher2.setHasPromotion(iMobility,	True)
		NewUnitChamp1.setHasPromotion(iMobility,	True)
		NewUnitChamp1.setHasPromotion(iIron,		True)
		NewUnitChamp2.setHasPromotion(iMobility,	True)
		NewUnitChamp2.setHasPromotion(iIron,		True)
		NewUnitImp.setHasPromotion(iMobility,		True)
		NewUnitSettler1.setHasPromotion(iStarting,	True)
		NewUnitSettler2.setHasPromotion(iStarting,	True)

		for iTech in xrange(gc.getNumTechInfos()):
			if eFounderTeam.isHasTech(iTech):
				eInfernalTeam.setHasTech(iTech, True, iInfernalPlayer, True, False)
		eFounderTeam.signOpenBorders(iInfernalTeam)
		eInfernalTeam.signOpenBorders(iFounderTeam)
		eInfernalTeam.makePeace(iDemonTeam)
		for iTeam in xrange(gc.getMAX_TEAMS()):
			if iTeam == iDemonTeam:	continue
			pTeam = gc.getTeam(iTeam)
			if not pTeam.isAlive():	continue
			if eFounderTeam.isAtWar(iTeam) or pTeam.isBarbarian():
				eInfernalTeam.declareWar(iTeam, False, WarPlanTypes.WARPLAN_LIMITED)
		pInfernalPlayer.AI_changeAttitudeExtra(iPlayer,4)
		
		if bReassign:
			CyMessageControl().sendModNetMessage(CvUtil.reassignPlayer, iPlayer, iInfernalPlayer, 0, 0)

	### TODO: Dictionaries
	# Check if equipment can`t be removed
	def canRemoveEquipment(self,pHolder,pTaker,iPromotion):
		if self.UnitCombats == {}: self.initialize()
		gc				= CyGlobalContext()
		git				= gc.getInfoTypeForString
		if pHolder != -1:
			if pHolder.getUnitType() == self.Heroes["Barnaxus"]:
				if iPromotion == git('PROMOTION_PIECES_OF_BARNAXUS'):
					return False
			elif pHolder.getUnitType() == git('UNIT_THE_HIVE'):
				if iPromotion == git('PROMOTION_PIECES_OF_THE_HIVE'):
					return False
			elif pHolder.getUnitType() == self.Heroes["Mithril Golem"]:
				if iPromotion == git('PROMOTION_PIECES_OF_MITHRIL_GOLEM'):
					return False
			elif pHolder.getUnitType() == self.Heroes["The War Machine"]:
				if iPromotion == git('PROMOTION_PIECES_OF_WAR_MACHINE'):
					return False
			elif pHolder.getUnitType() == git('UNIT_MECH_DRAGON'):
				if iPromotion == git('PROMOTION_PIECES_OF_MECH_DRAGON'):
					return False
			if pHolder.isHasPromotion(self.Promotions["Race"]["Illusion"]):
				return False
			if pHolder.isHasPromotion(git('PROMOTION_BAIR_GEM_RECHARGING')):
				if iPromotion == git('PROMOTION_BAIR_GEM_RECHARGING'):
					return False
		if pTaker != -1:
			if pTaker.getUnitCombatType() in (self.UnitCombats["Naval"], self.UnitCombats["Siege"]):
				return False
			if pTaker.getSpecialUnitType() in (git('SPECIALUNIT_SPELL'), git('SPECIALUNIT_BIRD')):
				return False
			if pTaker.isHasPromotion(self.Promotions["Race"]["Illusion"]):
				return False
		return True

	def doBarbarianWorld(self):
		gc				= CyGlobalContext()
		lStartingPlots	= []
		lValuedPlots	= []
		iNumCities		= 0
		pBarbPlayer		= gc.getPlayer(gc.getORC_PLAYER())

		# Creating a list of starting points to avoid few checks every plot
		for iPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iPlayer)
			if not pLoopPlayer.isAlive():	continue
			iNumCities += 1
			pStartingPlot = pLoopPlayer.getStartingPlot()
			if pStartingPlot.isNone():		continue
			lStartingPlots.append(pStartingPlot)

		# Early exits everywhere to shave some time
		for iPlot in xrange(CyMap().numPlots()):
			pLoopPlot = CyMap().plotByIndex(iPlot)
			bValid		= True
			iValue		= 0
			iAIValue	= 0
			iDist		= 0
			# Checks that are more likely to filter out a plot are higher
			if pLoopPlot.isWater():						continue
			elif pLoopPlot.isImpassable():				continue
			elif pLoopPlot.isPeak():					continue
			elif pLoopPlot.getBonusType(-1) != -1:		continue
			elif pLoopPlot.getImprovementType() != -1:	continue
			elif pLoopPlot.isCity():					continue
			elif pLoopPlot.isFoundDisabled():			continue

			iAIValue += pBarbPlayer.AI_foundValue(pLoopPlot.getX(), pLoopPlot.getY(), -1, True)
			if iAIValue == 0:							continue

			for StartingPlot in lStartingPlots:
				iDist = plotDistance(pLoopPlot.getX(),pLoopPlot.getY(),StartingPlot.getX(),StartingPlot.getY())
				if iDist == -1:
					iValue += 100
				elif iDist < 7:
					bValid = False
					break
				# Without a cap on distance points, every other point increase becomes irrelevant on larger maps.
				else:
					iValue += min(iDist*5, 100)

			if not bValid: continue

			iValue += iAIValue
			iValue += CyGame().getSorenRandNum(250, "Barb World Plot Eval")
			lValuedPlots.append((iPlot,iValue))

		if not lValuedPlots: return
		# Sorting plots by iValue
		lValuedPlots.sort(key=lambda tup: tup[1], reverse=True)

		# Placing cities
		for i in xrange(iNumCities):

			iDist = 0

			if len(lValuedPlots) == 0: break

			iCityPlot = lValuedPlots[0][0]
			pCityPlot = CyMap().plotByIndex(iCityPlot)
			pBarbPlayer.found(pCityPlot.getX(), pCityPlot.getY())

			del lValuedPlots[0]

			# As plots are already valued, we need to remove plots that are too close to the placed city.
			for tLoopPlot in list(lValuedPlots):
				pLoopPlot = CyMap().plotByIndex(tLoopPlot[0])
				iDist = plotDistance(pLoopPlot.getX(),pLoopPlot.getY(),pCityPlot.getX(),pCityPlot.getY())
				if iDist > -1 and iDist < 7: lValuedPlots.remove(tLoopPlot)

	### TODO: Dictionaries
	def doAoEGameStart(self):
		gc				= CyGlobalContext()
		iAnimalTeam		= gc.getANIMAL_TEAM()
		bOrcPlayer		= gc.getPlayer(gc.getORC_PLAYER())
		bAnimalPlayer	= gc.getPlayer(gc.getANIMAL_PLAYER())
		bDemonPlayer	= gc.getPlayer(gc.getDEMON_PLAYER())
		iElohim			= self.Civilizations["Elohim"]
		iCaln			= self.Civilizations["Clan of Embers"]
		iFeral			= self.Traits["Feral"]
		iCapria			= self.Traits["Aspect Capria"]
		iMahon			= self.Traits["Aspect Mahon"]
		iSauros			= gc.getInfoTypeForString('LEADER_SAUROS')
		iAI				= UnitAITypes.NO_UNITAI
		iDirection		= DirectionTypes.DIRECTION_SOUTH
		# Set Flags
		gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_AKHARIEN_LOST'),True)
		gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_MOKKA_LOST'),True)
		if not self.GameOptions["No Orthus"]: gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_ORTHUS'),True)
		lWell = self.findImprovements(self.UniqueImprovements["Bradeline's Well"])
		if not lWell: gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_PURIFIED_WELL'),True)

		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if not pLoopPlayer.isAlive(): continue
			if pLoopPlayer.hasTrait(iFeral):
				pTeam = gc.getTeam(pLoopPlayer.getTeam())
				pTeam.makePeace(iAnimalTeam)
			if pLoopPlayer.hasTrait(iCapria):
				gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_CAPRIA'),True)
			if pLoopPlayer.hasTrait(iMahon):
				gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_MAHON'),True)
			if pLoopPlayer.isHuman() and pLoopPlayer.getCivilizationType() == iElohim:
				showUniqueImprovements(iLoopPlayer)
			if pLoopPlayer.getLeaderType() == iSauros and pLoopPlayer.getCivilizationType() !=  iCaln:
				pLoopPlayer.setNumMaxTraitPerClass(gc.getInfoTypeForString('TRAITCLASS_SAVAGE'),0)
		## GAME OPTIONS CHECK
		if self.GameOptions["Barbarian World"]:
			self.doBarbarianWorld()

		if self.GameOptions["Wild Mana"]:
			iMana		= self.Mana["Mana"]
			iMGPromo	= self.Promotions["Effects"]["Mana Guardian"]
			iSize		= CyMap().getWorldSize()
			iAdditionalMana = 15
			if   iSize	== self.WorldSizes["Duel"]:		iAdditionalMana += -7
			elif iSize	== self.WorldSizes["Tiny"]:		iAdditionalMana += -5
			elif iSize	== self.WorldSizes["Small"]:	iAdditionalMana += -3
			elif iSize	== self.WorldSizes["Large"]:	iAdditionalMana += 3
			elif iSize	== self.WorldSizes["Huge"]:		iAdditionalMana += 6
			elif iSize	== self.WorldSizes["Huger"]:	iAdditionalMana += 12
			addBonus('BONUS_MANA', iAdditionalMana, -1)

			iConvertRnd = 60
			if self.GameOptions["Feral Mana"]: iConvertRnd = 100

			# Conversion	Mana Type					Mana Guardian									Player
			lWildMana = [	(self.Mana["Air"],			self.Units["Summons"]["Lightning Elemental"],	bDemonPlayer),
							(self.Mana["Body"],			self.Units["Summons"]["Flesh Golem"],			bDemonPlayer),
							(self.Mana["Chaos"],		self.Units["Sheaim"]["Chaos Marauder"],			bDemonPlayer),
							(self.Mana["Death"],		self.Units["Summons"]["Lich"],					bDemonPlayer),
							(self.Mana["Earth"],		self.Units["Summons"]["Earth Elemental"],		bDemonPlayer),
							(self.Mana["Enchantment"],	self.Units["Luchuirp"]["Wood Golem"],			bOrcPlayer),
							(self.Mana["Entropy"],		self.Units["Sheaim"]["Tar Demon"],				bDemonPlayer),
							(self.Mana["Fire"],			self.Units["Summons"]["Fire Elemental"],		bDemonPlayer),
							(self.Mana["Law"],			self.Units["Summons"]["Einherjar"],				bOrcPlayer),
							(self.Mana["Life"],			self.Units["Mercurian"]["Angel"],				bOrcPlayer),
							(self.Mana["Metamagic"],	self.Units["Kahdi"]["Thade"],					bDemonPlayer),
							(self.Mana["Mind"],			self.Units["Kahdi"]["Psion"],					bDemonPlayer),
							(self.Mana["Shadow"],		self.Units["Summons"]["Spectre"],				bDemonPlayer),
							(self.Mana["Spirit"],		self.Units["Elohim"]["Monk"],					bOrcPlayer),
							(self.Mana["Sun"],			self.Units["Summons"]["Aurealis"],				bOrcPlayer),
							(self.Mana["Water"],		self.Units["Summons"]["Water Elemental"],		bDemonPlayer),
							(self.Mana["Creation"],		self.Units["Animal"]["Elk"],					bAnimalPlayer),
							(self.Mana["Force"],		self.Units["Grigori"]["Dragon Slayer"],			bOrcPlayer),
							(self.Mana["Dimensional"],	self.Units["Kahdi"]["Uber Gnosling"],			bDemonPlayer),
							(self.Mana["Ice"],			self.Units["Summons"]["Ice Elemental"],			bDemonPlayer),
							(self.Mana["Nature"],		self.Units["Summons"]["Guardian Vines"],		bAnimalPlayer)]

			for iLoopPlot in xrange(CyMap().numPlots()):
				pLoopPlot = CyMap().plotByIndex(iLoopPlot)
				if pLoopPlot.getBonusType(-1) != iMana:								continue
				if pLoopPlot.isWater():												continue
				if pLoopPlot.getImprovementType() != -1:							continue
				if CyGame().getSorenRandNum(100, "Mana Creation") >= iConvertRnd:	continue
				tBonus = lWildMana[CyGame().getSorenRandNum(len(lWildMana), "Pick Mana")]
				pLoopPlot.setBonusType(tBonus[0])
				if not self.GameOptions["Mana Guardians"]:							continue
				if pLoopPlot.getNumUnits()!= 0:										continue
				iUnit		= tBonus[1]
				pWildPlayer	= tBonus[2]
				newUnit		= pWildPlayer.initUnit(iUnit, pLoopPlot.getX(), pLoopPlot.getY(), iAI, iDirection)
				newUnit.setHasPromotion(iMGPromo, True)

		if self.GameOptions["Thaw"]:
			# FlavourMod: Changed by Jean Elcard 11/06/2008 (Extended End of Winter Option)
			FLAT_WORLDS = ["ErebusWrap", "Erebus"]			# map scripts with wrapping but no equator
			MAX_EOW_PERCENTAGE = 0.35 						# percentage of EoW on total game turns
			THAW_DELAY_PERCENTAGE = 0.05 					# don't start thawing for x percent of EoW
			# forest varieties
			DECIDUOUS_FOREST = 0
			CONIFEROUS_FOREST = 1
			SNOWY_CONIFEROUS_FOREST = 2

			iIce			= self.Feature["Ice"]
			iForest			= self.Feature["Forest"]
			iJungle			= self.Feature["Jungle"]
			iVolcano		= self.Feature["Volcano"]
			iCPlains		= gc.getInfoTypeForString("FEATURE_CRYSTAL_PLAINS")
			iTaiga			= self.Terrain["Taiga"]
			iTundra			= self.Terrain["Tundra"]
			iGrass			= self.Terrain["Grass"]
			iPlains			= self.Terrain["Plains"]
			iDesert			= self.Terrain["Desert"]
			iMarsh			= self.Terrain["Marsh"]

			iTotalGameTurns	= gc.getGameSpeedInfo(CyGame().getGameSpeedType()).getGameTurnInfo(0).iNumGameTurnsPerIncrement
			iMaxEOWTurns	= max(1, int(iTotalGameTurns * MAX_EOW_PERCENTAGE))
			iThawDelayTurns	= max(1, int(iMaxEOWTurns * THAW_DELAY_PERCENTAGE))
			iRandomTurns	= iMaxEOWTurns - iThawDelayTurns
			iMaxLatitude	= max(CyMap().getTopLatitude(), abs(CyMap().getBottomLatitude()))
			bIsFlatWorld	= not (CyMap().isWrapX() or CyMap().isWrapY()) or CyMap().getMapScriptName() in FLAT_WORLDS

			for iLoopPlot in xrange(CyMap().numPlots()):
				pPlot		= CyMap().plotByIndex(iLoopPlot)
				iTerrain	= pPlot.getTerrainType()
				iFeature	= pPlot.getFeatureType()
				iVariety	= pPlot.getFeatureVariety()
				iBonus		= pPlot.getBonusType(-1)
				randTerrain = CyGame().getSorenRandNum(100, "Thaw Terrain Swap")
				randTurns	= CyGame().getSorenRandNum(iRandomTurns, "Thaw Requirement")
				if not bIsFlatWorld:
					iLatitude	= abs(pPlot.getLatitude())
					randTurns	= int(randTurns * ((float(iLatitude) / iMaxLatitude) ** 0.4))
				randTurns	+= iThawDelayTurns
				# cover erebus' oceans and lakes in ice
				if   pPlot.isWater():
					if   bIsFlatWorld:
						if CyGame().getSorenRandNum(100, "Thaw Iceburg Placement") < 90:
							pPlot.setTempFeatureType(iIce, 0, randTurns)
					elif iLatitude + 10 > CyGame().getSorenRandNum(50, "Thaw Glacier Placement"):
						pPlot.setTempFeatureType(iIce, 0, randTurns)
					elif iFeature != -1 and iFeature != iIce:
						pPlot.setTempFeatureType(iIce, 0, randTurns)
				# change terrains to colder climate versions
				elif iTerrain == iTaiga:
					if randTerrain < 90:
						pPlot.setTempTerrainTypeFM(iTundra,	randTurns, False, False)
				elif iTerrain == iGrass and iFeature != iJungle:
					if randTerrain < 60:
						pPlot.setTempTerrainTypeFM(iTundra,	randTurns, False, False)
					else:
						pPlot.setTempTerrainTypeFM(iTaiga,	randTurns, False, False)
				elif iTerrain == iPlains:
					if randTerrain < 30:
						pPlot.setTempTerrainTypeFM(iTundra,	randTurns, False, False)
					else:
						pPlot.setTempTerrainTypeFM(iTaiga,	randTurns, False, False)
				elif iTerrain == iDesert:
					if randTerrain < 50:
						pPlot.setTempTerrainTypeFM(iTaiga,	randTurns, False, False)
					else:
						pPlot.setTempTerrainTypeFM(iPlains,	randTurns, False, False)
				elif iTerrain == iMarsh:
					pPlot.setTempTerrainTypeFM(iGrass,		randTurns, False, False)
				# change all features (except ice) to colder climate versions
				if iFeature == iForest:
					if iVariety == DECIDUOUS_FOREST:
						pPlot.setTempFeatureType(iForest, CONIFEROUS_FOREST, randTurns)
					elif iVariety == CONIFEROUS_FOREST:
						pPlot.setTempFeatureType(iForest, SNOWY_CONIFEROUS_FOREST, randTurns)
				elif (iFeature != FeatureTypes.NO_FEATURE and not pPlot.isWater()):
					if not iFeature in (iIce, iVolcano, iCPlains):
						pPlot.setTempFeatureType(iForest, DECIDUOUS_FOREST, randTurns)
				# remove invalid bonuses or replace them (if food) with a valid surrogate
				if iBonus != -1 and not pPlot.canHaveBonus(iBonus, True):
					if gc.getBonusInfo(iBonus).getYieldChange(YieldTypes.YIELD_FOOD) > 0:
						iPossibleTempFoodBonuses = []
						for iLoopBonus in xrange(gc.getNumBonusInfos()):
							if gc.getBonusInfo(iLoopBonus).getYieldChange(YieldTypes.YIELD_FOOD) > 0:
								if pPlot.canHaveBonus(iLoopBonus, True):
									iPossibleTempFoodBonuses.append(iLoopBonus)
						if len(iPossibleTempFoodBonuses) > 0:
							pPlot.setTempBonusType(iPossibleTempFoodBonuses[CyGame().getSorenRandNum(len(iPossibleTempFoodBonuses), "Thaw Food Replacement")], randTurns)
						else:
							pPlot.setTempBonusType(-1, randTurns)
					else:
						pPlot.setTempBonusType(-1, randTurns)
		## Wilderness
		if self.GameOptions["Dark Forests"]:
			randWild	= CyGame().getSorenRandNum(100, "DF Wilderness chance")
			iBestValue1	= 0
			iBestValue2	= 0
			pBestPlot1	= -1
			pBestPlot2	= -1
			iForest		= self.Feature["Forest"]
			iJungle		= self.Feature["Jungle"]
			iScrub		= self.Feature["Scrub"]
			for iLoopPlot in xrange(CyMap().numPlots()):
				pLoopPlot	= CyMap().plotByIndex(iLoopPlot)
				if pLoopPlot.isWater():													continue
				if pLoopPlot.getNumUnits()!= 0:											continue
				if not pLoopPlot.getFeatureType() in (iForest, iJungle, iScrub):		continue
				if pLoopPlot.getImprovementType() != -1:								continue
				if randWild < 55:
					if pLoopPlot.getFeatureType() == iScrub:							continue
					iValue1	= CyGame().getSorenRandNum(1000, "DF Looking for Blighted Forest spot")
					if not pLoopPlot.isOwned(): iValue1 += 1000
					if iValue1 > iBestValue1:
						iBestValue1	= iValue1
						pBestPlot1	= pLoopPlot
				if randWild >= 45:
					iValue2	= CyGame().getSorenRandNum(1000, "DF Diakonos placement spot")
					if not pLoopPlot.isOwned(): iValue2 += 1000
					if iValue2 > iBestValue2:
						iBestValue2	= iValue2
						pBestPlot2	= pLoopPlot

			if pBestPlot1 != -1:
				newUnit = bAnimalPlayer.initUnit(self.Units["Animal"]["Malignant Flora"], pBestPlot1.getX(), pBestPlot1.getY(), iAI, iDirection)
				pBestPlot1.setImprovementType(self.Lairs["Blighted Forest"])
			if pBestPlot2 != -1:
				iDiakonos = self.Units["Animal"]["Diakonos"]
				iX = pBestPlot2.getX(); iY = pBestPlot2.getY()
				newUnit = bAnimalPlayer.initUnit(iDiakonos, iX, iY, iAI, iDirection)
				newUnit = bAnimalPlayer.initUnit(iDiakonos, iX, iY, iAI, iDirection)
				newUnit = bAnimalPlayer.initUnit(iDiakonos, iX, iY, iAI, iDirection)
				newUnit = bAnimalPlayer.initUnit(iDiakonos, iX, iY, iAI, iDirection)
				newUnit = bAnimalPlayer.initUnit(iDiakonos, iX, iY, iAI, iDirection)

		if not self.GameOptions["No Barbarians"]:
			iGoblinArcher	= self.Units["Scorpion Clan"]["Archer"]
			lGoblinCamp		= self.findImprovements(self.Lairs["Goblin Camp"])
			for pLoopPlot in lGoblinCamp:
				if pLoopPlot.getNumUnits()!= 0: continue
				bOrcPlayer.initUnit(iGoblinArcher, pLoopPlot.getX(), pLoopPlot.getY(), iAI, iDirection)

		# Clearing starting locations of dangerous spots, like Mana Guardians and Lairs
		# Keep unit spawns above
		iLairClearRange	= 5
		iBarbClearRange	= 5
		tSettlers		= (self.UnitClasses["Settler"], gc.getInfoTypeForString("UNITCLASS_VESSEL_DTESH"), self.UnitClasses["Awakened"])

		for iLoopPlot in xrange(CyMap().numPlots()):
			pLoopPlot = CyMap().plotByIndex(iLoopPlot)
			
			for iLoopUnit in xrange(pLoopPlot.getNumUnits()):
				pLoopUnit	= pLoopPlot.getUnit(iLoopUnit)
				iUnitClass	= pLoopUnit.getUnitClassType()
				if not iUnitClass in tSettlers:					continue
				pOwner		= gc.getPlayer(pLoopUnit.getOwner())
				iOwnerTeam	= pOwner.getTeam()
				pOwnerTeam	= gc.getTeam(iOwnerTeam)
				### Lairs
				for x, y in plotsInRange(pLoopUnit.getX(), pLoopUnit.getY(), iLairClearRange):
					pLairPlot = CyMap().plot(x, y)
					if pLairPlot.getImprovementType() == -1:	continue
					pImprovement = gc.getImprovementInfo(pLairPlot.getImprovementType())
					if   pImprovement.isUnique():				continue
					elif pImprovement.getSpawnUnitType() != -1:				pLairPlot.setImprovementType(-1)
					elif pImprovement.getSpawnGroupType() != -1:			pLairPlot.setImprovementType(-1)
					elif pImprovement.getImmediateSpawnUnitType() != -1:	pLairPlot.setImprovementType(-1)
					elif pImprovement.getImmediateSpawnGroupType() != -1:	pLairPlot.setImprovementType(-1)
				### Enemies
				for x, y in plotsInRange(pLoopUnit.getX(), pLoopUnit.getY(), iBarbClearRange):
					pEnemyPlot = CyMap().plot(x, y)
					for iEnemyUnit in xrange(pEnemyPlot.getNumUnits(), -1, -1):
						pEnemyUnit		= pEnemyPlot.getUnit(iEnemyUnit)
						iEnemyPlayer	= pEnemyUnit.getOwner()
						if iEnemyPlayer == -1: continue
						pEnemyPlayer	= gc.getPlayer(iEnemyPlayer)
						iEnemyTeam		= pEnemyPlayer.getTeam()
						if not pOwnerTeam.isAtWar(iEnemyTeam): continue
						pEnemyUnit.kill(False, -1)

	### TODO: Dictionaries
	def doTurnInfernal(self, iPlayer):
		gc = CyGlobalContext()
		if not gc.isNoCrash():
			CyGame().releasefromDeathList(gc.getInfoTypeForString('DEATHLIST_DEMON_CONVERSION'), iPlayer, 6, self.Units["Infernal"]["Manes"])
			CyGame().releasefromDeathList(gc.getInfoTypeForString('DEATHLIST_DEMON_REBIRTH'), iPlayer, 0, -1)

	### TODO: Dictionaries
	def doTurnMercurians(self, iPlayer):
		gc = CyGlobalContext()
		if not gc.isNoCrash():
			CyGame().releasefromDeathList(gc.getInfoTypeForString('DEATHLIST_ANGEL_CONVERSION'), iPlayer, 1, self.Units["Mercurian"]["Angel"])

	### TODO: Dictionaries
	def doInsane(self, iPlayer):
		if CyGame().getSorenRandNum(1, "Insane Trait Roll") != 0: return
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		pCapital	= pPlayer.getCapitalCity()
		iInsane		= self.Traits["Insane"]
		randFlag	= CyGame().getSorenRandNum(100,"Insane Flag")
		lTraits		= []
		for iTrait in xrange(gc.getNumTraitInfos()):
			if not gc.getTraitInfo(iTrait).isSelectable():	continue
			if iTrait == iInsane:							continue
			if not gc.isNoCrash():
				pPlayer.setHasTrait((iTrait),False,-1,True,True)
			else:
				pPlayer.setHasTrait((iTrait),False)
			lTraits.append(iTrait)
		if len(lTraits) >= 3:
			lTraits = sorted(lTraits, key=lambda x: CyGame().getSorenRandNum(67, "Insane Trait"))
			lTraits = lTraits[:3]
		for iTrait in lTraits:
			if not gc.isNoCrash():
				pPlayer.setHasTrait((iTrait),True,-1,True,True)
			else:
				pPlayer.setHasTrait((iTrait),True)
		if randFlag < 10: pPlayer.setHasFlag(gc.getInfoTypeForString("FLAG_PERPENTACH_BODY_SWITCH"),True)
		if pCapital.isNone():return
		iColor		= CyGame().getSorenRandNum(123, "Insane Color Pick")
		szMessage	= CyTranslator().getText("TXT_KEY_INSANE_HELP", (gc.getTraitInfo(lTraits[0]).getDescription(), gc.getTraitInfo(lTraits[1]).getDescription(), gc.getTraitInfo(lTraits[2]).getDescription(),))
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		lIcon		= ["Art/Interface/Buttons/General/happy_person.dds", "Art/Interface/mainscreen/cityscreen/angry_citizen.dds", "Art/Interface/Buttons/General/unhealthy_person.dds", "Art/Interface/Buttons/WorldBuilder/Crab.dds"]
		iIcon		= lIcon[CyGame().getSorenRandNum(len(lIcon), "Insane Icon Pick")]
		CyInterface().addMessage(iPlayer, True, 25, szMessage, '', 3, iIcon, ColorTypes(iColor), pCapital.getX(), pCapital.getY(), True, True)

	def doAdaptive(self, iPlayer, iTurn):
		gc			= CyGlobalContext()
		iCycle		= gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent() - 5
		if iTurn % iCycle != 0: return
		pPlayer		= gc.getPlayer(iPlayer)

		lAdaptiveTrairs	= [	self.Traits["Aggressive"],	self.Traits["Arcane"],		self.Traits["Charismatic"],	self.Traits["Creative"],		self.Traits["Expansive"],
							self.Traits["Financial"],	self.Traits["Industrious"],	self.Traits["Organized"],	self.Traits["Philosophical"],	self.Traits["Raiders"],
							self.Traits["Spiritual"]]
		# Type Name is used in popup to display mouseover help, should match with the list above
		lWidgetTraits	= [	"TRAIT_AGGRESSIVE",			"TRAIT_ARCANE",				"TRAIT_CHARISMATIC",		"TRAIT_CREATIVE",				"TRAIT_EXPANSIVE",
							"TRAIT_FINANCIAL",			"TRAIT_INDUSTRIOUS",		"TRAIT_ORGANIZED",			"TRAIT_PHILOSOPHICAL",			"TRAIT_RAIDERS",
							"TRAIT_SPIRITUAL"]

		if pPlayer.isHuman():
			popupInfo	= CyPopupInfo()
			popupInfo.setOption2(True)
			popupInfo.setFlags(165) # Trait widget on mouseover
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("passToModNetMessage")
			popupInfo.setData1(iPlayer)
			popupInfo.setData3(100) # onModNetMessage id
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENTTRIGGER_TRAIT_ADAPTIVE", ()))
			for iTrait in lAdaptiveTrairs:
				iIndex = lAdaptiveTrairs.index(iTrait)
				if pPlayer.hasTrait(iTrait) and gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:	# Reset iTrait
					if not gc.isNoCrash():
						pPlayer.setHasTrait((iTrait),False,-1,True,True)
					else:
						pPlayer.setHasTrait((iTrait),False)
				if not pPlayer.hasTrait(iTrait):																				# Set iTrait to the pick list
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_ADAPTIVE_HELP", (gc.getTraitInfo(iTrait).getDescription(), )), lWidgetTraits[iIndex])
			popupInfo.addPopup(iPlayer)
		else:
			lAITraits = []
			for iTrait in lAdaptiveTrairs:
				if pPlayer.hasTrait(iTrait) and gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getPermanentTrait() != iTrait:	# Reset iTrait
					if not gc.isNoCrash():
						pPlayer.setHasTrait((iTrait),False,-1,True,True)
					else:
						pPlayer.setHasTrait((iTrait),False)
				if not pPlayer.hasTrait(iTrait):
					lAITraits.append(iTrait)
			if not lAITraits: return
			iAITrait = lAITraits[CyGame().getSorenRandNum(len(lAITraits), "AI Adaptive Trait Roll")]
			if not gc.isNoCrash():
				pPlayer.setHasTrait((iAITrait),True,-1,True,True)
			else:
				pPlayer.setHasTrait((iAITrait),True)

	### TODO: Dictionaries
	def doRepublic(self, iPlayer, iTurn):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		pPlayer.changeFlagValue(gc.getInfoTypeForString("FLAG_REPUBLIC_TIMER"), 1)
		iCycle		= gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent() / 10 * 4
		if pPlayer.getFlagValue(gc.getInfoTypeForString("FLAG_REPUBLIC_TIMER")) == iCycle:
			pPlayer.setFlagValue(gc.getInfoTypeForString("FLAG_REPUBLIC_TIMER"), 0)
		if pPlayer.getFlagValue(gc.getInfoTypeForString("FLAG_REPUBLIC_TIMER")) != 1: return
		self.resetRepublicTraits(pPlayer)
		iElection = CyGame().getSorenRandNum(4, "Republic Election Type")
		if pPlayer.isHuman():
			if   iElection == 0:
				szHeader	=	"TXT_KEY_EVENTTRIGGER_REPUBLIC_ELECTION_HAWK_VS_DOVE"
				lText		=	["TXT_KEY_EVENT_REPUBLIC_ELECTION_SUPPORT_HAWK",		"TXT_KEY_EVENT_REPUBLIC_ELECTION_SUPPORT_DOVE", 	"TXT_KEY_EVENT_REPUBLIC_ELECTION_FAIR_HAWK_VS_DOVE"]
				lWidget		=	['EVENT_REPUBLIC_ELECTION_SUPPORT_HAWK',				'EVENT_REPUBLIC_ELECTION_SUPPORT_DOVE',				'EVENT_REPUBLIC_ELECTION_FAIR_HAWK_VS_DOVE']
			elif iElection == 1:
				szHeader	=	"TXT_KEY_EVENTTRIGGER_REPUBLIC_ELECTION_LANDOWNER_VS_PEASANTS"
				lText		=	["TXT_KEY_EVENT_REPUBLIC_ELECTION_SUPPORT_LANDOWNER",	"TXT_KEY_EVENT_REPUBLIC_ELECTION_SUPPORT_PEASANT",	"TXT_KEY_EVENT_REPUBLIC_ELECTION_FAIR_LANDOWNER_VS_PEASANT"]
				lWidget		=	['EVENT_REPUBLIC_ELECTION_SUPPORT_LANDOWNER',			'EVENT_REPUBLIC_ELECTION_SUPPORT_PEASANT',			'EVENT_REPUBLIC_ELECTION_FAIR_LANDOWNER_VS_PEASANT']
			elif iElection == 2:
				szHeader	=	"TXT_KEY_EVENTTRIGGER_REPUBLIC_ELECTION_CHURCH_VS_STATE"
				lText		=	["TXT_KEY_EVENT_REPUBLIC_ELECTION_SUPPORT_CHURCH",		"TXT_KEY_EVENT_REPUBLIC_ELECTION_SUPPORT_STATE",	"TXT_KEY_EVENT_REPUBLIC_ELECTION_FAIR_CHURCH_VS_STATE"]
				lWidget		=	['EVENT_REPUBLIC_ELECTION_SUPPORT_CHURCH',				'EVENT_REPUBLIC_ELECTION_SUPPORT_STATE',			'EVENT_REPUBLIC_ELECTION_FAIR_CHURCH_VS_STATE']
			else:
				szHeader	=	"TXT_KEY_EVENTTRIGGER_REPUBLIC_ELECTION_LABOR_VS_ACADEMIA"
				lText		=	["TXT_KEY_EVENT_REPUBLIC_ELECTION_SUPPORT_LABOR",		"TXT_KEY_EVENT_REPUBLIC_ELECTION_SUPPORT_ACADEMIA",	"TXT_KEY_EVENT_REPUBLIC_ELECTION_FAIR_LABOR_VS_ACADEMIA"]
				lWidget		=	['EVENT_REPUBLIC_ELECTION_SUPPORT_LABOR',				'EVENT_REPUBLIC_ELECTION_SUPPORT_ACADEMIA',			'EVENT_REPUBLIC_ELECTION_FAIR_LABOR_VS_ACADEMIA']
			popupInfo = CyPopupInfo()
			popupInfo.setOption2(True)
			popupInfo.setFlags(126) # Event widget on mouseover
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("passToModNetMessage")
			popupInfo.setData1(iPlayer)
			popupInfo.setData2(iElection)
			popupInfo.setData3(101) # onModNetMessage id
			popupInfo.setText(CyTranslator().getText(szHeader, ()))
			popupInfo.addPythonButton(CyTranslator().getText(lText[0], ()), lWidget[0])
			popupInfo.addPythonButton(CyTranslator().getText(lText[1], ()), lWidget[1])
			popupInfo.addPythonButton(CyTranslator().getText(lText[2], ()), lWidget[2])
			popupInfo.addPopup(iPlayer)
		else:
			CyMessageControl().sendModNetMessage(101, 2, iPlayer, iElection,-1) # based on iAIValue of events (always fair)

	def doBaneDivine(self, iPlayer):
		gc				= CyGlobalContext()
		iCombatDisciple	= self.UnitCombats["Disciple"]
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if not pLoopPlayer.isAlive(): continue
			for iLoopUnit in xrange(pLoopPlayer.getNumUnits()):
				pLoopUnit = pLoopPlayer.getUnit(iLoopUnit)
				if pLoopUnit.getUnitCombatType() != iCombatDisciple: continue
				pLoopUnit.kill(False, iPlayer)

	def doGlory(self, iPlayer):
		gc				= CyGlobalContext()
		iEvil			= self.Alignments["Evil"]
		iDemon			= self.Promotions["Race"]["Demon"]
		iUndead			= self.Promotions["Race"]["Undead"]
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if not pLoopPlayer.isAlive():														continue
			if not (pLoopPlayer.getAlignment() == iEvil or pLoopPlayer.isBarbarian()):			continue
			for iLoopUnit in xrange(pLoopPlayer.getNumUnits()):
				pLoopUnit = pLoopPlayer.getUnit(iLoopUnit)
				if not (pLoopUnit.isHasPromotion(iDemon) or pLoopUnit.isHasPromotion(iUndead)):	continue
				pLoopUnit.kill(False, iPlayer)

	def doRoO(self):
		iAdditionalMana	= 7
		iSize			= CyMap().getWorldSize()
		if   iSize	== self.WorldSizes["Duel"]:		iAdditionalMana += -3
		elif iSize	== self.WorldSizes["Tiny"]:		iAdditionalMana += -2
		elif iSize	== self.WorldSizes["Small"]:	iAdditionalMana += -1
		elif iSize	== self.WorldSizes["Large"]:	iAdditionalMana += 1
		elif iSize	== self.WorldSizes["Huge"]:		iAdditionalMana += 3
		elif iSize	== self.WorldSizes["Huger"]:	iAdditionalMana += 5
		addBonus('BONUS_MANA', iAdditionalMana, 'Art/Interface/Buttons/WorldBuilder/mana_button.dds')

	def doNatureRevolt(self):
		gc				= CyGlobalContext()
		bAnimalPlayer	= gc.getPlayer(gc.getANIMAL_PLAYER())
		bOrcPlayer		= gc.getPlayer(gc.getORC_PLAYER())
		iAIValue		= UnitAITypes.NO_UNITAI
		iDirection		= DirectionTypes.DIRECTION_SOUTH
		lPromotions		= [	self.Promotions["Effects"]["Heroic Defense I"],		self.Promotions["Effects"]["Heroic Defense II"],
							self.Promotions["Effects"]["Heroic Strength I"],	self.Promotions["Effects"]["Heroic Strength II"]]
		for iLoopUnit in xrange(bOrcPlayer.getNumUnits()):
			pLoopUnit	= bOrcPlayer.getUnit(iLoopUnit)
			bValid		= False
			iUC			= pLoopUnit.getUnitClassType()
			if   iUC == self.UnitClasses["Worker"]:		iNewUnit = self.Units["Animal"]["Elephant"];		bValid = True
			elif iUC == self.UnitClasses["Scout"]:		iNewUnit = self.Units["Animal"]["Sabretooth"];		bValid = True
			elif iUC == self.UnitClasses["Warrior"]:	iNewUnit = self.Units["Animal"]["Dire Wolf"];		bValid = True
			elif iUC == self.UnitClasses["Hunter"]:		iNewUnit = self.Units["Animal"]["Tyrant"];			bValid = True
			elif iUC == self.UnitClasses["Axeman"]:		iNewUnit = self.Units["Animal"]["Cave Bears"];		bValid = True
			elif iUC == self.UnitClasses["Fawn"]:		iNewUnit = self.Units["Animal"]["Roc"];				bValid = True
			elif iUC == self.UnitClasses["Hill Giant"]:	iNewUnit = self.Units["Animal"]["Red Drake"];		bValid = True
			elif iUC == self.UnitClasses["Archer"]:		iNewUnit = self.Units["Animal"]["Silverback"];		bValid = True
			elif iUC == self.UnitClasses["Cyklop"]:		iNewUnit = self.Units["Animal"]["Giant Spider"];	bValid = True
			elif iUC == self.UnitClasses["Minotaur"]:	iNewUnit = self.Units["Animal"]["Blood Boar"];		bValid = True
			elif iUC == self.UnitClasses["Horseman"]:	iNewUnit = self.Units["Animal"]["Giant Scorpion"];	bValid = True
			elif iUC == self.UnitClasses["Frostling"]:	iNewUnit = self.Units["Animal"]["White Drake"];		bValid = True

			if not bValid: continue
			iX		= pLoopUnit.getX()
			iY		= pLoopUnit.getY()
			newUnit	= bAnimalPlayer.initUnit(iNewUnit, iX, iY, iAIValue, iDirection)
			newUnit	= bAnimalPlayer.initUnit(iNewUnit, iX, iY, iAIValue, iDirection)
			newUnit	= bAnimalPlayer.initUnit(iNewUnit, iX, iY, iAIValue, iDirection)
			pLoopUnit.kill(True, -1)

		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if not pLoopPlayer.isAlive(): continue
			for iLoopUnit in xrange(pLoopPlayer.getNumUnits()):
				pLoopUnit = pLoopPlayer.getUnit(iLoopUnit)
				if not pLoopUnit.isAnimal(): continue
				for iPromotion in lPromotions: pLoopUnit.setHasPromotion(iPromotion, True)

	def doBloodOfThePhoenix(self, iPlayer):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		iImmortal	= self.Promotions["Effects"]["Immortal"]
		for iLoopUnit in xrange(pPlayer.getNumUnits()):
			pLoopUnit = pPlayer.getUnit(iLoopUnit)
			if not pLoopUnit.isAlive():				continue
			if pLoopUnit.getUnitCombatType() == -1:	continue
			pLoopUnit.setHasPromotion(iImmortal, True)

	def doPurge(self, iPlayer):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		iStateRel	= pPlayer.getStateReligion()
		if iStateRel == self.Religions["Order"]:	iRevolt = -1
		else:										iRevolt = 0
		(pLoopCity, iter) = pPlayer.firstCity(False)
		while(pLoopCity):
			lBadRel		= []
			iRevolt		+= CyGame().getSorenRandNum(2, "Purge the Unfaithful Revolt")
			for iLoopRel in xrange(gc.getNumReligionInfos()):
				if iStateRel == iLoopRel:					continue
				if not pLoopCity.isHasReligion(iLoopRel):	continue
				if pLoopCity.isHolyCityByType(iLoopRel):	continue
				pLoopCity.setHasReligion(iLoopRel, False, True, True)
				iRevolt	+= 1
				lBadRel.append(iLoopRel)
			if lBadRel:
				for iBuilding in xrange(gc.getNumBuildingInfos()):
					if pLoopCity.getNumBuilding(iBuilding) <= 0:							continue
					if not gc.getBuildingInfo(iBuilding).getPrereqReligion() in lBadRel:	continue
					pLoopCity.setNumRealBuilding(iBuilding, 0)
			if iRevolt > 0: pLoopCity.setOccupationTimer(iRevolt)
			(pLoopCity, iter) = pPlayer.nextCity(iter, False)

	### TODO: Dictionaries
	def doSamhain(self, iPlayer):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iPlayer)
		iOrcPlayer	= gc.getORC_PLAYER()
		iFrostling	= self.Units["Frostling"]["Frostling"]
		iFArcher	= self.Units["Frostling"]["Archer"]
		iWolfRaider	= self.Units["Frostling"]["Wolf Rider"]
		iCount = CyGame().countCivPlayersAlive() + int(CyGame().getHandicapType()) - 5
		for i in xrange(iCount):
			addUnit(iFrostling,		iOrcPlayer)
			addUnit(iFrostling,		iOrcPlayer)
			addUnit(iFArcher,		iOrcPlayer)
			addUnit(iWolfRaider,	iOrcPlayer)
		pMokka = addUnit(self.Heroes["Mokka"], iOrcPlayer)
		if not pPlayer.isHasFlag(gc.getInfoTypeForString('FLAG_MOKKA_LOST')):
			pMokka.safeRemovePromotion(gc.getInfoTypeForString("PROMOTION_MOKKAS_CAULDRON"))
		gc.getGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_MOKKA_LOST'), False)

	def doProjectWH(self, pCity):
		gc			= CyGlobalContext()
		iPlayer		= pCity.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)
		iPriest		= self.Units["White Hand"]["Priest"]
		iX			= pCity.getX()
		iY			= pCity.getY()
		iAI			= UnitAITypes.NO_UNITAI
		iDirection	= DirectionTypes.DIRECTION_SOUTH
		lNames		= ["Dumannios", "Riuros", "Anagantios"]
		pCity.setHasReligion( self.Religions["White Hand"], True, True, True)
		for i in xrange(3):
			newUnit = pPlayer.initUnit(self.Units["White Hand"]["Priest"], iX, iY, iAI, iDirection)
			newUnit.setName(lNames[i])
			newUnit.changeStrBoost(1)

	def doDeepening(self):
		iTimer = 40 + (CyGame().getGameSpeedType() * 20)
		lStartingTerrain	= [self.Terrain["Tundra"],	self.Terrain["Taiga"],	self.Terrain["Grass"],	self.Terrain["Plains"],	self.Terrain["Desert"]]
		lDeepeningTerrain	= [self.Terrain["Glacier"],	self.Terrain["Tundra"],	self.Terrain["Taiga"],	self.Terrain["Taiga"],	self.Terrain["Plains"]]
		iBlizzard			= self.Feature["Blizzard"]
		for iPlot in xrange(CyMap().numPlots()):
			pPlot	= CyMap().plotByIndex(iPlot)
			bValid	= False
			if pPlot.isWater():															continue
			if CyGame().getSorenRandNum(100, "The Deepening") >= 25:					continue
			iTerrain	= pPlot.getTerrainType()
			if not iTerrain in lStartingTerrain:										continue
			iPlotTimer	= CyGame().getSorenRandNum(iTimer, "Deepening Terrain Timer") + 10
			iIndex		= lStartingTerrain.index(iTerrain)
			pPlot.setTempTerrainTypeFM(lDeepeningTerrain[iIndex], iPlotTimer, False, False)
			if CyGame().getSorenRandNum(750, "The Deepening, Blizzard Creation") >= 10:	continue
			pPlot.setFeatureType(iBlizzard, -1)

	def stirFromSlumber(self, pCity):
		gc		= CyGlobalContext()
		iPlayer	= pCity.getOwner()
		pPlayer	= gc.getPlayer(iPlayer)
		pPlayer.initUnit(self.Heroes["Drifa"], pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if pPlayer.getLeaderType() != self.Leaders["Raitlor"]: return
		if not gc.isNoCrash():
			pPlayer.setHasTrait(self.Traits["Ice Touched"], True,-1,True,True)
		else:
			pPlayer.setHasTrait(self.Traits["Ice Touched"], True)

	### TODO: Dictionaries
	def doDraw(self, iPlayer):
		gc				= CyGlobalContext()
		pPlayer			= gc.getPlayer(iPlayer)
		iTeam			= pPlayer.getTeam()
		pTeam			= gc.getTeam(iTeam)
		iOrcTeam		= gc.getORC_TEAM()
		iAnimalTeam		= gc.getANIMAL_TEAM()
		iDemonTeam		= gc.getDEMON_TEAM()
		pPlayer.changeNoDiplomacyWithEnemies(1)
		pPlayer.setHasFlag(gc.getInfoTypeForString("FLAG_DRAW"),True)
		for iLoopTeam in xrange(gc.getMAX_TEAMS()):
			if iLoopTeam == iTeam:			continue
			if iLoopTeam == iOrcTeam:		continue
			if iLoopTeam == iAnimalTeam:	continue
			if iLoopTeam == iDemonTeam:		continue
			pLoopTeam = gc.getTeam(iLoopTeam)
			if not pLoopTeam.isAlive():		continue
			if pLoopTeam.isAVassal():		continue
			pTeam.declareWar(iLoopTeam, False, WarPlanTypes.WARPLAN_LIMITED)
		for iLoopUnit in xrange(pPlayer.getNumUnits()):
			pLoopUnit	= pPlayer.getUnit(iLoopUnit)
			iDamage		= pLoopUnit.getDamage() * 2
			iDamage		= min(99, iDamage)
			iDamage		= max(50, iDamage)
			pLoopUnit.setDamage(iDamage, iPlayer)
		(pLoopCity, iter) = pPlayer.firstCity(False)
		while(pLoopCity):
			iPop		= int(pLoopCity.getPopulation() / 2)
			iPop		= max(1, iPop)
			pLoopCity.setPopulation(iPop)
			(pLoopCity, iter) = pPlayer.nextCity(iter, False)

	def doAscension(self, iPlayer):
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(iPlayer)
		lAurics	= (self.Heroes["Auric"], self.Heroes["Auric Winter"])
		iWHRel	= self.Religions["White Hand"]
		iTeam	= pPlayer.getTeam()
		### Auric Spawn
		for iLoopUnit in xrange(pPlayer.getNumUnits()):
			pLoopUnit	= pPlayer.getUnit(iLoopUnit)
			if not pLoopUnit.getUnitType() in lAurics:		continue
			newUnit = pPlayer.initUnit( self.Heroes["Auric Ascended"], pLoopUnit.getX(), pLoopUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(pLoopUnit)
			break
		### WH Vassals
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if not pLoopPlayer.isAlive():					continue
			if pLoopPlayer.isBarbarian():					continue
			if pLoopPlayer.getStateReligion() != iWHRel:	continue
			iLoopTeam = pLoopPlayer.getTeam()
			pLoopTeam = gc.getTeam(iLoopTeam)
			pLoopTeam.makePeace(iTeam)
			pLoopTeam.setVassal(iTeam, True, False)
		## Trophy
		if pPlayer.isHuman():
			t = "TROPHY_FEAT_ASCENSION"
			if not CyGame().isHasTrophy(t): CyGame().changeTrophyValue(t, 1)
		## Godslayer Spawn
		if CyGame().getWBMapScript(): return
		iBestPlayer	= -1
		iBestValue	= 0
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if not pLoopPlayer.isAlive():					continue
			if pLoopPlayer.isBarbarian():					continue
			if pLoopPlayer.getTeam() == iTeam:				continue
			if pLoopPlayer.getStateReligion() == iWHRel:	continue
			pLoopCapital	= pLoopPlayer.getCapitalCity()
			if pLoopCapital.isNone():						continue
			iValue = CyGame().getSorenRandNum(500, "Ascension")
			iValue += (20 - CyGame().getPlayerRank(iLoopPlayer)) * 50
			if pLoopPlayer.isHuman(): iValue += 2000
			if iValue > iBestValue:
				iBestValue	= iValue
				iBestPlayer	= iLoopPlayer
		if iBestPlayer == -1: return
		pBestPlayer	= gc.getPlayer(iBestPlayer)
		if pBestPlayer.isHuman():
			popupInfo	= CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
			popupInfo.setOnClickedPythonCallback("passToModNetMessage")
			popupInfo.setData1(iBestPlayer)
			popupInfo.setData3(102) # onModNetMessage id
			popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENT_GODSLAYER", ()))
			popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CONTINUE", ()),"")
			popupInfo.addPopup(iBestPlayer)
		else:
			pContainer		= -1
			pBestCity		= pBestPlayer.getCapitalCity()
			pPlot			= pBestCity.plot()
			iContainer		= self.Units["Equipment"]["Container"]
			for iUnit in xrange(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(iUnit)
				if pUnit.getUnitType() != iContainer: continue
				pContainer = pUnit
			if pContainer == -1:
				bPlayer	= gc.getPlayer(gc.getORC_PLAYER())
				pContainer = bPlayer.initUnit(iContainer, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			pContainer.setHasPromotion(self.Promotions["Equipment"]["Godslayer"], True)

	### TODO: Dictionaries
	def unitCreatedTraits(self, pUnit):
		gc		= CyGlobalContext()
		iPlayer	= pUnit.getOwner()
		pPlayer	= gc.getPlayer(iPlayer)

		if pPlayer.hasTrait(self.Traits["Defender"]):
			if pUnit.getUnitCombatType() == self.UnitCombats["Worker"]:
				pUnit.setHasPromotion(self.Promotions["Generic"]["Hardy I"], True)

		if pPlayer.hasTrait(self.Traits["Instructor"]):
			if pUnit.getUnitType() == self.Units["Bannor"]["Demagog"]:
				pUnit.changeFreePromotionPick(1)
				
		if gc.getInfoTypeForString("MODULE_EMERGENT_LEADERS") != - 1 and pPlayer.hasTrait(self.Traits["Incorporeal 1"]):
			if pUnit.getUnitCombatType() == self.UnitCombats["Mounted"] or pUnit.isSecondaryUnitCombat(self.UnitCombats["Mounted"]):
				pUnit.setHasPromotion(self.Promotions["Race"]["Illusion"], True)

		if pPlayer.hasTrait(self.Traits["Spiderkin"]):
			pNest = pPlayer.getCapitalCity()
			iNestPop = pNest.getPopulation()
			spiderUnits = [self.Units["Archos"]["Baby Spider"], self.Units["Archos"]["Spider"], self.Units["Archos"]["Giant Spider"], self.Units["Archos"]["Nesting Spider"], self.Heroes["Mother"]]
			if iNestPop >= 15 and pUnit.getUnitType() not in spiderUnits: pUnit.setHasPromotion(self.Promotions["Effects"]["Spiderkin"], True)

	def unitCreatedWelp(self, pUnit):
		gc		= CyGlobalContext()
		iPlayer	= pUnit.getOwner()
		pPlayer	= gc.getPlayer(iPlayer)
		pPlot	= pUnit.plot()

		GoblinChoice = [(self.Units["Scorpion Clan"]["Goblin"], 10)]

		if   pPlot.getNumUnits() > 5:							GoblinChoice.append((self.Units["Scorpion Clan"]["Lord"], 25))
		if   pPlayer.isHasTech(self.Techs["Bowyers"]):			GoblinChoice.append((self.Units["Scorpion Clan"]["Sapper"], 25));		GoblinChoice.append((self.Units["Scorpion Clan"]["Archer"], 10))
		elif pPlayer.isHasTech(self.Techs["Archery"]): 			GoblinChoice.append((self.Units["Scorpion Clan"]["Archer"], 25))
		if   pPlayer.isHasTech(self.Techs["Stirrups"]):			GoblinChoice.append((self.Units["Scorpion Clan"]["Wolf Archer"], 25));	GoblinChoice.append((self.Units["Scorpion Clan"]["Wolf Rider"], 10))
		elif pPlayer.isHasTech(self.Techs["Horseback Riding"]):	GoblinChoice.append((self.Units["Scorpion Clan"]["Wolf Rider"], 25))
		if   pPlayer.isHasTech(self.Techs["Construction"]):		GoblinChoice.append((self.Units["Scorpion Clan"]["Chariot"], 25))

		getGoblin	= wchoice( GoblinChoice, 'Goblin Whelp Upgrade' )
		newUnit		= pPlayer.initUnit(getGoblin(), pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.convert(pUnit)
		return newUnit

	def unitCreatedAdept(self, pUnit):
		gc				= CyGlobalContext()
		iPlayer			= pUnit.getOwner()
		pPlayer			= gc.getPlayer(iPlayer)

		bChanneling2	= pUnit.isHasPromotion(self.Promotions["Effects"]["Channeling II"])
		bChanneling3	= pUnit.isHasPromotion(self.Promotions["Effects"]["Channeling III"])

		lMana			= [	self.Mana["Air"],			self.Mana["Body"],		self.Mana["Chaos"],		self.Mana["Death"],			self.Mana["Earth"],
							self.Mana["Enchantment"],	self.Mana["Entropy"],	self.Mana["Fire"],		self.Mana["Law"],			self.Mana["Life"],
							self.Mana["Metamagic"],		self.Mana["Mind"],		self.Mana["Shadow"],	self.Mana["Spirit"],		self.Mana["Sun"],
							self.Mana["Water"],			self.Mana["Creation"],	self.Mana["Force"],		self.Mana["Dimensional"],	self.Mana["Ice"],
							self.Mana["Nature"]]

		lSphere			= [	self.Promotions["Generic"]["Air I"],			self.Promotions["Generic"]["Body I"],		self.Promotions["Generic"]["Chaos I"],	self.Promotions["Generic"]["Death I"],			self.Promotions["Generic"]["Earth I"],
							self.Promotions["Generic"]["Enchantment I"],	self.Promotions["Generic"]["Entropy I"],	self.Promotions["Generic"]["Fire I"],	self.Promotions["Generic"]["Law I"],			self.Promotions["Generic"]["Life I"],
							self.Promotions["Generic"]["Metamagic I"],		self.Promotions["Generic"]["Mind I"],		self.Promotions["Generic"]["Shadow I"],	self.Promotions["Generic"]["Spirit I"],			self.Promotions["Generic"]["Sun I"],
							self.Promotions["Generic"]["Water I"],			self.Promotions["Generic"]["Creation I"],	self.Promotions["Generic"]["Force I"],	self.Promotions["Generic"]["Dimensional I"],	self.Promotions["Generic"]["Ice I"],
							self.Promotions["Generic"]["Nature I"]]

		if pPlayer.getCivilizationType() in (self.Civilizations["Scions"], self.Civilizations["D'Tesh"]):
			lSphere[1] = self.Promotions["Generic"]["Corpus I"]

		for iMana in lMana:
			iIndex		= lMana.index(iMana)
			iNumBonuses	= pPlayer.getNumAvailableBonuses(iMana)
			if iNumBonuses <= 1:	continue
			pUnit.setHasPromotion(lSphere[iIndex], True)
			if iNumBonuses <= 2:	continue
			if not bChanneling2:	continue
			iSphere2	= gc.getPromotionInfo(lSphere[iIndex]).getPromotionNextLevel()
			pUnit.setHasPromotion(iSphere2, True)
			if iNumBonuses <= 3:	continue
			if not bChanneling3:	continue
			iSphere3	= gc.getPromotionInfo(iSphere2).getPromotionNextLevel()
			pUnit.setHasPromotion(iSphere3, True)

	### TODO: Dictionaries
	def unitCreatedAspect(self, pUnit):
		if CyGame().getSorenRandNum(100, "Aspect") >= 5:	return
		gc		= CyGlobalContext()
		iPlayer	= pUnit.getOwner()
		pPlayer	= gc.getPlayer(iPlayer)
		iTeam	= pPlayer.getTeam()
		pTeam	= gc.getTeam(iTeam)
		if pTeam.getAtWarCount(True) <= 0:					return

		lFlags	= [	gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_CAPRIA'),	gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_UNKNOWN_2'),	gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_UNKNOWN_1'),
					gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_ORTHUS'),	gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_ARAK'),			gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_MAGNADINE'),
					gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_MAHON'),]
		# Promotion and Flag should share the same index
		lPromos	= [	self.Promotions["Effects"]["Aspect Capria"],			self.Promotions["Effects"]["Aspect Unknown2"],				self.Promotions["Effects"]["Aspect Unknown1"],
					self.Promotions["Effects"]["Aspect Orthus"],			self.Promotions["Effects"]["Aspect Arak"],					self.Promotions["Effects"]["Aspect Magnadine"],
					self.Promotions["Effects"]["Aspect Mahon"]]

		for iFlag in lFlags:
			if pPlayer.isHasFlag(iFlag): continue
			iIndex = lFlags.index(iFlag)
			pUnit.setHasPromotion(lPromos[iIndex], True)
			gc.getGame().setGlobalFlag(iFlag, True)
			break

	### TODO: Dictionaries
	def unitCreatedMounted(self, pUnit):
		gc		= CyGlobalContext()
		if gc.getUnitInfo(pUnit.getUnitType()).getPrereqOrBonuses(0) != self.Resources["Horse"]: return
		iPlayer	= pUnit.getOwner()
		pPlayer	= gc.getPlayer(iPlayer)
		lMounts = [gc.getInfoTypeForString("PROMOTION_HORSE"), gc.getInfoTypeForString("PROMOTION_NIGHTMARE"), gc.getInfoTypeForString("PROMOTION_HYAPON"), gc.getInfoTypeForString("PROMOTION_CAMEL")]
		bHasDefaultMount = False
		for iPromotion in lMounts:
			if not gc.getUnitInfo(pUnit.getUnitType()).getFreePromotions(iPromotion): continue
			bHasDefaultMount = True
			break
		if bHasDefaultMount: return

		if   pPlayer.hasBonus(self.Resources["Camel"]) and pPlayer.getCivilizationType() == self.Civilizations["Malakim"]:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CAMEL"),True)
		elif pPlayer.hasBonus(gc.getInfoTypeForString("BONUS_HYAPON")):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_HYAPON"),True)
		elif pPlayer.hasBonus(self.Resources["Nightmare"]):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_NIGHTMARE"),True)
		elif pPlayer.hasBonus(self.Resources["Horse"]):
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_HORSE"),True)

	### TODO: Dictionaries
	def doHalfMortal(self, pUnit):
		gc			= CyGlobalContext()
		pPlot		= pUnit.plot()
		iCountAngel	= 0
		iCountDemon	= 0
		iCountSylph	= 0
		iNumUnits	= pPlot.getNumUnits()
		if iNumUnits <= 1: return
		for iLoopUnit in xrange(iNumUnits):
			pLoopUnit = pPlot.getUnit(iLoopUnit)
			if pLoopUnit == pUnit: continue
			if pLoopUnit.isHasPromotion(self.Promotions["Race"]["Angel"]):				iCountAngel += 1
			if pLoopUnit.isHasPromotion(self.Promotions["Race"]["Demon"]):				iCountDemon += 1
			if pLoopUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_SLYPH")):	iCountSylph += 1
		if CyGame().getSorenRandNum(100,"doHalfMortal Aasimar") < iCountAngel:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_AASIMAR"),True)
		if CyGame().getSorenRandNum(100,"doHalfMortal Cambion") < iCountDemon:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_CAMBION"),True)
		if CyGame().getSorenRandNum(100,"doHalfMortal Slyph") < iCountSylph:
			pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_SLYPH_BLOOD"),True)

	def doBeastOfAgares(self, pCity):
		if pCity.getCivilizationType() == self.Civilizations["Infernal"]: return
		iPop = max(1, pCity.getPopulation() - 4)
		pCity.setPopulation(iPop)
		pCity.setOccupationTimer(4)

	### TODO: Dictionaries
	def unitBuiltAmurites(self, pUnit, pCity):
		gc			= CyGlobalContext()
		iCombatType	= pUnit.getUnitCombatType()
		iPlayer		= pUnit.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)

		tUC			= (	gc.getInfoTypeForString("UNITCOMBAT_ROGUE"),	gc.getInfoTypeForString("UNITCOMBAT_DEFENSIVE_MELEE"),	self.UnitCombats["Melee"],	self.UnitCombats["Archer"],
						self.UnitCombats["Mounted"],					self.UnitCombats["Recon"],								self.UnitCombats["Adept"],	self.UnitCombats["Disciple"])

		if not iCombatType in tUC: return
		iNumSoG		= pCity.getNumBuilding(self.Buildings["School of Govannon"])
		iNumCoA		= pCity.getNumBuilding(self.Buildings["Cave of Ancestors"])

		if iCombatType == self.UnitCombats["Adept"] and iNumCoA > 0:
			iExtraXP = 0
			for iBonus in xrange(gc.getNumBonusInfos()):
				if gc.getBonusInfo(iBonus).getBonusClassType() != self.Mana["Mana Class"]: continue
				if pCity.hasBonus(iBonus): iExtraXP += 1
			if iExtraXP != 0: pUnit.changeExperience(iExtraXP, -1, False, False, False)

		lMana		= [	self.Mana["Air"],			self.Mana["Body"],		self.Mana["Chaos"],		self.Mana["Death"],			self.Mana["Earth"],
						self.Mana["Enchantment"],	self.Mana["Entropy"],	self.Mana["Fire"],		self.Mana["Law"],			self.Mana["Life"],
						self.Mana["Metamagic"],		self.Mana["Mind"],		self.Mana["Shadow"],	self.Mana["Spirit"],		self.Mana["Sun"],
						self.Mana["Water"],			self.Mana["Creation"],	self.Mana["Force"],		self.Mana["Dimensional"],	self.Mana["Ice"],
						self.Mana["Nature"]]

		fSphere		= (	self.Promotions["Generic"]["Air I"],			self.Promotions["Generic"]["Body I"],		self.Promotions["Generic"]["Chaos I"],	self.Promotions["Generic"]["Death I"],			self.Promotions["Generic"]["Earth I"],
						self.Promotions["Generic"]["Enchantment I"],	self.Promotions["Generic"]["Entropy I"],	self.Promotions["Generic"]["Fire I"],	self.Promotions["Generic"]["Law I"],			self.Promotions["Generic"]["Life I"],
						self.Promotions["Generic"]["Metamagic I"],		self.Promotions["Generic"]["Mind I"],		self.Promotions["Generic"]["Shadow I"],	self.Promotions["Generic"]["Spirit I"],			self.Promotions["Generic"]["Sun I"],
						self.Promotions["Generic"]["Water I"],			self.Promotions["Generic"]["Creation I"],	self.Promotions["Generic"]["Force I"],	self.Promotions["Generic"]["Dimensional I"],	self.Promotions["Generic"]["Ice I"],
						self.Promotions["Generic"]["Nature I"])

		iChance		= 20
		lValidSphere = []
		for iMana in lMana:
			iIndex			= lMana.index(iMana)
			iNumBonuses		= pPlayer.getNumAvailableBonuses(iMana)
			if iNumBonuses == 0: continue
			iChance		   += iNumBonuses * 5
			lValidSphere.append((fSphere[iIndex], iNumBonuses))

		if not lValidSphere:																return
		if CyGame().getSorenRandNum(100, "unitBuiltAmurites Sphere Chance 1") >= iChance:	return
		getSphere1	= wchoice( lValidSphere, "unitBuiltAmurites Sphere Pick" )
		iSphere1	= getSphere1()
		pUnit.setHasPromotion(iSphere1, True)
		if CyGame().getSorenRandNum(100, "unitBuiltAmurites Sphere Chance 2") >= iChance:	return
		if iNumSoG <= 0:																	return
		iSphere2	= gc.getPromotionInfo(iSphere1).getPromotionNextLevel()
		pUnit.setHasPromotion(iSphere2, True)
		if CyGame().getSorenRandNum(100, "unitBuiltAmurites Sphere Chance 3") >= iChance:	return
		if iNumCoA <= 0:																	return
		iSphere3	= gc.getPromotionInfo(iSphere2).getPromotionNextLevel()
		pUnit.setHasPromotion(iSphere3, True)

	def unitBuiltLuchuirp(self, pUnit, pCity):
		if not pUnit.isHasPromotion(self.Promotions["Race"]["Golem"]):		return
		if pCity.getNumBuilding(self.Buildings["Blasting Workshop"]) > 0:	pUnit.setHasPromotion( self.Promotions["Generic"]["Fire II"], True)
		if pCity.getNumBuilding(self.Buildings["Pallens Engine"]) > 0:		pUnit.setHasPromotion( self.Promotions["Generic"]["Perfect Sight"], True)
		if pCity.getNumBuilding(self.Buildings["Adularia Chamber"]) > 0:	pUnit.setHasPromotion( self.Promotions["Effects"]["Hidden"], True)

	def unitBuiltAcheron(self, pUnit, pCity):
		pCity.setNumRealBuilding(self.Buildings["Dragons Hoard"], 1)
		pUnit.setHasPromotion(self.Promotions["Effects"]["Acheron Leashed"], True)
		iX	= pCity.getX()
		iY	= pCity.getY()
		for dX, dY in RANGE1:
			pPlot		= CyMap().plot(iX+dX, iY+dY)
			iFeature	= pPlot.getFeatureType()
			if not iFeature in (self.Feature["Forest"], self.Feature["Jungle"]): continue
			pPlot.setFeatureType(self.Feature["Flames"], 0)

	def unitKilledCity(self, pUnit):
		gc		= CyGlobalContext()
		pPlot	= pUnit.plot()
		iX		= pUnit.getX()
		iY		= pUnit.getY()

		for dX, dY in RANGE1:
			pDeltaPlot = CyMap().plot(iX+dX, iY+dY)
			if not pDeltaPlot.isCity(): continue
			pCity = pDeltaPlot.getPlotCity()
			if pCity.getNumBuilding(self.Buildings["Soul Forge"]) > 0:
				pCity.changeProduction(pUnit.getExperienceTimes100() / 100 + 10)

				szText		= CyTranslator().getText("TXT_KEY_MESSAGE_SOUL_FORGE",())
				szSound		= 'AS2D_DISCOVERBONUS'
				szArt		= 'Art/Interface/Buttons/Buildings/Soulforge.dds'
				iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
				iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
				CyInterface().addMessage(pCity.getOwner(), True, 25, szText, szSound, iMessage, szArt, iGreen, pCity.getX(), pCity.getY(), True, True)
			if gc.getPlayer(pCity.getOwner()).hasTrait(self.Traits["Lycanthropic"]):
				pCity.changeFood(pUnit.getExperienceTimes100()/100 + 10)

				szText		= CyTranslator().getText("TXT_KEY_MESSAGE_CANNIBALIZE",())
				szSound		= 'AS2D_DISCOVERBONUS'
				szArt		= 'Art/Interface/Buttons/Promotions/Cannibalize.dds'
				iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
				iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
				CyInterface().addMessage(pCity.getOwner(), True, 25, szText, szSound, iMessage, szArt, iGreen, pCity.getX(), pCity.getY(), True, True)

		if not pPlot.isCity():												return
		pCity	= pPlot.getPlotCity()
		if pCity.getNumBuilding(self.Buildings["Mokkas Cauldron"]) <= 0:	return
		iLoserPlayer = pUnit.getOwner()
		pLoserPlayer = gc.getPlayer(iLoserPlayer)
		if pCity.getOwner() != iLoserPlayer:								return
		iUnit = self.getUnholyVersion(pUnit)
		if iUnit == -1:														return
		newUnit = pLoserPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(self.Promotions["Race"]["Demon"], True)
		newUnit.setDamage(50, PlayerTypes.NO_PLAYER)
		newUnit.finishMoves()

		szBuffer	= gc.getUnitInfo(newUnit.getUnitType()).getDescription()
		szText		= CyTranslator().getText("TXT_KEY_MESSAGE_MOKKAS_CAULDRON",((szBuffer, )))
		szSound		= 'AS2D_DISCOVERBONUS'
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		szArt		= 'Art/Interface/Buttons/Buildings/MokkasCauldron.dds'
		iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
		CyInterface().addMessage(iLoserPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, pCity.getX(), pCity.getY(), True, True)

	### TODO: Dictionaries
	def unitKilledAoM(self, pUnit):
		gc				= CyGlobalContext()
		bCanBeMane		= False
		bCanBeAngel		= False
		bCanBeFrozen	= False
		iInfernal		= self.Civilizations["Infernal"]
		iMercurians		= self.Civilizations["Mercurians"]
		iFrozen			= self.Civilizations["Frozen"]
		if CyGame().countKnownTechNumTeams(self.Techs["Infernal Pact"]) > 0 and CyGame().getNumCivActive(iInfernal) > 0:
			bCanBeMane	= True
		if CyGame().getBuildingClassCreatedCount(self.Buildings["Mercurian Gate"]) > 0 and CyGame().getNumCivActive(iMercurians) > 0:
			bCanBeAngel	= True
		if gc.getInfoTypeForString("MODULE_FROZEN") != -1:
			if CyGame().getNumCivActive(iFrozen) > 0:
				bCanBeFrozen = True
		if not (bCanBeMane or bCanBeAngel or bCanBeFrozen): return
		iAngel		= self.Units["Mercurian"]["Angel"]
		iMane		= self.Units["Infernal"]["Manes"]
		iFrozenSoul	= self.Units["Frozen"]["Frozen Souls"]
		iUnitType	= self.angelorMane(pUnit)
		pPlot		= pUnit.plot()
		iPlayer		= pUnit.getOwner()

		if   bCanBeMane and iUnitType == iMane:
			if not gc.isNoCrash():
				CyGame().addtoDeathList(gc.getInfoTypeForString('DEATHLIST_DEMON_CONVERSION'), pUnit)
			else:
				self.giftUnit(iMane, iInfernal, 0, pPlot, iPlayer)
		elif bCanBeAngel and iUnitType == iAngel:
			if not gc.isNoCrash():
				CyGame().addtoDeathList(gc.getInfoTypeForString('DEATHLIST_ANGEL_CONVERSION'), pUnit)
			else:
				self.giftUnit(iAngel, iMercurians, pUnit.getExperienceTimes100(), pPlot, iPlayer)
		elif bCanBeFrozen and iUnitType == iFrozenSoul:
			# TODO: Deathlist for Frozen Souls
			# if not gc.isNoCrash():
			# 	CyGame().addtoDeathList(gc.getInfoTypeForString('DEATHLIST_FROZEN_CONVERSION'), pUnit)
			# else:
			self.giftUnit(iFrozenSoul, iFrozen, 0, pPlot, iPlayer)

	def unitKilledGuide(self, pUnit):
		gc		= CyGlobalContext()
		if pUnit.getExperience() <= 0:	return
		lUnits	= []
		iPlayer	= pUnit.getOwner()
		pPlayer	= gc.getPlayer(iPlayer)
		for iLoopUnit in xrange(pPlayer.getNumUnits()):
			pLoopUnit = pPlayer.getUnit(iLoopUnit)
			if not pLoopUnit.isAlive():		continue
			if pLoopUnit.isOnlyDefensive():	continue
			if pLoopUnit.isDelayedDeath():	continue
			lUnits.append(pLoopUnit)
		if len(lUnits) <= 0:			return
		pTargetUnit = lUnits[CyGame().getSorenRandNum(len(lUnits), "Spirit Guide")]
		iXP = pUnit.getExperienceTimes100() / 2
		pTargetUnit.changeExperienceTimes100(iXP, -1, False, False, False)

		szText		= CyTranslator().getText("TXT_KEY_MESSAGE_SPIRIT_GUIDE",())
		szSound		= 'AS2D_DISCOVERBONUS'
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		szArt		= 'Art/Interface/Buttons/Promotions/SpiritGuide.dds'
		iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
		CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, pUnit.getX(), pUnit.getY(), True, True)

	### TODO: Dictionaries
	def resetAspects(self, pUnit):
		gc = CyGlobalContext()
		if pUnit.isHasPromotion(self.Promotions["Effects"]["Aspect Capria"]):
			CyGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_CAPRIA'),False)
			pUnit.setHasPromotion(self.Promotions["Effects"]["Aspect Capria"], False)
		if pUnit.isHasPromotion(self.Promotions["Effects"]["Aspect Mahon"]):
			CyGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_MAHON'),False)
			pUnit.setHasPromotion(self.Promotions["Effects"]["Aspect Mahon"], False)
		if pUnit.isHasPromotion(self.Promotions["Effects"]["Aspect Magnadine"]):
			CyGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_MAGNADINE'),False)
			pUnit.setHasPromotion(self.Promotions["Effects"]["Aspect Magnadine"], False)
		if pUnit.isHasPromotion(self.Promotions["Effects"]["Aspect Arak"]):
			CyGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_ARAK'),False)
			pUnit.setHasPromotion(self.Promotions["Effects"]["Aspect Arak"], False)
		if pUnit.isHasPromotion(self.Promotions["Effects"]["Aspect Orthus"]):
			CyGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_ORTHUS'),False)
			pUnit.setHasPromotion(self.Promotions["Effects"]["Aspect Orthus"], False)
		if pUnit.isHasPromotion(self.Promotions["Effects"]["Aspect Unknown1"]):
			CyGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_UNKNOWN_1'),False)
			pUnit.setHasPromotion(self.Promotions["Effects"]["Aspect Unknown1"], False)
		if pUnit.isHasPromotion(self.Promotions["Effects"]["Aspect Unknown2"]):
			CyGame().setGlobalFlag(gc.getInfoTypeForString('FLAG_ASPECT_OF_WAR_UNKNOWN_2'),False)
			pUnit.setHasPromotion(self.Promotions["Effects"]["Aspect Unknown2"], False)

	### TODO: Dictionaries
	def pillageSlave(self, pUnit, iImprovement):
		gc			= CyGlobalContext()
		iUnittype	= pUnit.getUnitType()
		iChance		= CyGame().getSorenRandNum(100, "Capture Chance")
		if iUnittype == gc.getInfoTypeForString('UNIT_SLAVE_HUNTER'):	iChance -= 10
		if iUnittype == gc.getInfoTypeForString('UNIT_RAIDER'):			iChance -= 20
		if iChance >= 20:						return

		lImprovements	= [	self.Improvements["Pasture"],					self.Improvements["Farm"],					gc.getInfoTypeForString("IMPROVEMENT_HOMESTEAD"),	self.Improvements["Cottage (I)"],					self.Improvements["Hamlet (II)"],
							self.Improvements["Village (III)"],				self.Improvements["Town (IV)"],				self.CivImprovements["Kuriotates"]["Enclave"],		self.Improvements["Plantation"],					self.CivImprovements["Dwarven"]["Mine 2"],
							self.CivImprovements["Dwarven"]["Mine 1"],		self.CivImprovements["Dwarven"]["Mine 3"],	self.CivImprovements["Dwarven"]["Mine 4"],			self.CivImprovements["Malakim"]["Bedouin Camp"],	self.CivImprovements["Malakim"]["Bedouin Gathering"],
							self.CivImprovements["Malakim"]["Bedouin Sit"],	self.CivImprovements["Malakim"]["Bedouin Village"]]

		if not iImprovement in lImprovements:	return
		iUnit		= gc.getInfoTypeForString("UNIT_SLAVE")
		iRace		= -1
		pPlot		= pUnit.plot()
		if pPlot.isOwned():
			iPlayer		= pUnit.getOwner()
			pPlayer		= gc.getPlayer(iPlayer)
			pVictim		= gc.getPlayer(pPlot.getOwner())
			if pPlayer == pVictim: return
			iVictimCiv	= pVictim.getCivilizationType()
			pVictimCiv	= gc.getCivilizationInfo(iVictimCiv)
			if gc.getInfoTypeForString("MODULE_JOTNAR") != -1:
				if iVictimCiv == self.Civilizations["Jotnar"]:
					iUnit = self.Units["Jotnar"]["Jotnar Slave"]
			iRace	= pVictimCiv.getDefaultRace()
		newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iRace > -1: newUnit.setHasPromotion(iRace, True)

	def techRel(self, iTechType, iPlayer):
		gc			= CyGlobalContext()
		lRelTechs	= [	self.Techs["Corruption of Spirit"],		self.Techs["Orders from Heaven"],	self.Techs["Way of the Forests"],	self.Techs["Way of the Earthmother"],
						self.Techs["Message from the Deep"],	self.Techs["Honor"],				self.Techs["Deception"],			self.Techs["White Hand"]]

		if not iTechType in lRelTechs:						return
		pPlayer		= gc.getPlayer(iPlayer)
		if not self.canReceiveReligionUnit(pPlayer):		return
		iIndex		= lRelTechs.index(iTechType)

		tRels		= (	self.Religions["Ashen Veil"],			self.Religions["Order"],			self.Religions["Fellowship"],		self.Religions["Runes of Kilmorph"],
						self.Religions["Octopus Overlords"],	self.Religions["Empyrean"],			self.Religions["Council of Esus"],	self.Religions["White Hand"])

		if not CyGame().isReligionFounded(tRels[iIndex]):	return

		tUnits		= (	self.Units["Veil"]["Disciple"],			self.Units["Order"]["Disciple"],	self.Units["Leaves"]["Disciple"],	self.Units["Runes"]["Disciple"],
						self.Units["Overlords"]["Disciple"],	self.Units["Empyrean"]["Disciple"],	self.Units["Esus"]["Nightwatch"],	self.Units["White Hand"]["Disciple"])

		self.giftUnit(tUnits[iIndex], pPlayer.getCivilizationType(), 0, -1, -1)

	### TODO: Dictionaries
	def infernalPact(self, iTechType, iPlayer):
		gc			= CyGlobalContext()
		if gc.getGame().isOption(self.GameOptions["No Hyborem or Basium"]):	return
		pPlayer		= gc.getPlayer(iPlayer)
		iLeader		= pPlayer.getLeaderType()

		lDemonLordsList					= [	self.Leaders["Hyborem"]]

		if gc.getInfoTypeForString("MODULE_IMPORTANT_LEADERS") != -1:

			lDemonLordsList			   += [	gc.getInfoTypeForString("LEADER_MERESIN"),	gc.getInfoTypeForString("LEADER_OUZZA"),	gc.getInfoTypeForString("LEADER_STATIUS"),
											gc.getInfoTypeForString("LEADER_SALLOS"),	gc.getInfoTypeForString("LEADER_LETHE"),	gc.getInfoTypeForString("LEADER_JUDECCA")]

		if iLeader in lDemonLordsList:										return

		lDemonLordsTraitList			= [	"TRAIT_PACT_HYBOREM"]
		lDemonLordsHelpTraitList		= [	"EVENT_PYHELP_TRAIT_HYBOREM"]
		lDemonLordsHelpPactList			= [	"EVENT_PYHELP_PACT_HYBOREM"]

		if gc.getInfoTypeForString("MODULE_IMPORTANT_LEADERS") != -1:

			lDemonLordsTraitList	   += [	"TRAIT_PACT_MERESIN",						"TRAIT_PACT_OUZZA",							"TRAIT_PACT_STATIUS",
											"TRAIT_PACT_SALLOS",						"TRAIT_PACT_LETHE",							"TRAIT_PACT_JUDECCA"]
			lDemonLordsHelpTraitList   += [	"EVENT_PYHELP_TRAIT_MERESIN",				"EVENT_PYHELP_TRAIT_OUZZA",					"EVENT_PYHELP_TRAIT_STATIUS",
											"EVENT_PYHELP_TRAIT_SALLOS",				"EVENT_PYHELP_TRAIT_LETHE",					"EVENT_PYHELP_TRAIT_JUDECCA"]
			lDemonLordsHelpPactList	   += [	"EVENT_PYHELP_PACT_MERESIN",				"EVENT_PYHELP_PACT_OUZZA",					"EVENT_PYHELP_PACT_STATIUS",
											"EVENT_PYHELP_PACT_SALLOS",					"EVENT_PYHELP_PACT_LETHE",					"EVENT_PYHELP_PACT_JUDECCA"]

		lDemonLordsToSpawn				= []
		lDemonLordsTraitToSpawn			= []
		lDemonLordsHelpTraitClean		= []
		lDemonLordsHelpPactClean		= []
		for iLeader in xrange(len(lDemonLordsList)):
			if CyGame().isLeaderEverActive(lDemonLordsList[iLeader]): continue
			lDemonLordsToSpawn.append(lDemonLordsList[iLeader])
			lDemonLordsTraitToSpawn.append(lDemonLordsTraitList[iLeader])
			lDemonLordsHelpTraitClean.append(lDemonLordsHelpTraitList[iLeader])
			lDemonLordsHelpPactClean.append(lDemonLordsHelpPactList[iLeader])
		if lDemonLordsToSpawn:
			if pPlayer.isHuman() and not CyGame().GetWorldBuilderMode():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_PICK_DEMON_LORD",()))
				popupInfo.setData1(iPlayer)
				popupInfo.setData3(103) # onModNetMessage id
				popupInfo.setOnClickedPythonCallback("passToModNetMessage")
				popupInfo.setOption2(True); #Activate WIDGET HELP in buttons
				popupInfo.setFlags(126); #165 is WIDGET_HELP_EVENT
				for i in range(len(lDemonLordsToSpawn)):
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_SPAWN_DEMON_LORD", (gc.getLeaderHeadInfo(lDemonLordsToSpawn[i]).getDescription(),)), lDemonLordsHelpTraitClean[i])
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_START_AS_DEMON_LORD", (gc.getLeaderHeadInfo(lDemonLordsToSpawn[i]).getDescription(),)), lDemonLordsHelpPactClean[i])
				popupInfo.addPopup(iPlayer)
			else:
				iRnd	= CyGame().getSorenRandNum(len(lDemonLordsToSpawn), "Random Infernal Lord")
				iLeader	= lDemonLordsToSpawn[iRnd]
				iTrait	= gc.getInfoTypeForString(lDemonLordsTraitToSpawn[iRnd])
				self.spawnDemonLord(iLeader,iPlayer)
				if not gc.isNoCrash():
					pPlayer.setHasTrait((iTrait),False,-1,True,True)
				else:
					pPlayer.setHasTrait((iTrait),False)
		elif CyGame().isLeaderEverActive(self.Leaders["Hyborem"]) and not CyGame().isUnitClassMaxedOut(self.Heroes["Class-Hyborem"], 0):
			pInfernalPlayer	= gc.getPlayer(CyGame().getCivActivePlayer(self.Civilizations["Infernal"], 0))
			pCapital		= pInfernalPlayer.getCapitalCity()
			if pCapital.isNone(): return
			NewUnit = pInfernalPlayer.initUnit(self.Heroes["Hyborem"], pCapital.getX(), pCapital.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			NewUnit.setHasPromotion(self.Promotions["Effects"]["Immortal"], True)
			NewUnit.setHasCasted(True)
			NewUnit.setExperienceTimes100(2500, -1)

	def spreadOrder(self, iOwner, pSpreadCity):
		gc			= CyGlobalContext()
		pPlayer		= gc.getPlayer(iOwner)
		if pPlayer.getStateReligion() != self.Religions["Order"]:	return
		if pSpreadCity.getOccupationTimer() > 0:					return
		if pPlayer.isHasTech(self.Techs["Fanaticism"]):
			iUnit	= self.Units["Order"]["Crusader"]
			szText	= CyTranslator().getText("TXT_KEY_MESSAGE_ORDER_SPAWN_CRUSADER",())
			szArt	= 'Art/Interface/Buttons/Units/Crusader.dds'
		else:
			iUnit	= self.Units["Order"]["Disciple"]
			szText	= CyTranslator().getText("TXT_KEY_MESSAGE_ORDER_SPAWN_ACOLYTE",())
			szArt	= 'Art/Interface/Buttons/Units/Disciple Order.dds'
		newUnit = pPlayer.initUnit(iUnit, pSpreadCity.getX(), pSpreadCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		szSound		= 'AS2D_UNIT_BUILD_UNIT'
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
		CyInterface().addMessage(iOwner, True, 25, szText, szSound, iMessage, szArt, iGreen, pSpreadCity.getX(), pSpreadCity.getY(), True, True)

	### TODO: Dictionaries
	def resetPactTraits(self, iTeamA, iTeamB):
		gc							= CyGlobalContext()
		lDemonLordsList				= [	self.Leaders["Hyborem"]]
		lDemonLordsTraitList		= [	"TRAIT_PACT_HYBOREM"]

		if gc.getInfoTypeForString("MODULE_IMPORTANT_LEADERS") != -1:
			lDemonLordsList		   += [	gc.getInfoTypeForString("LEADER_MERESIN"),	gc.getInfoTypeForString("LEADER_OUZZA"),	gc.getInfoTypeForString("LEADER_STATIUS"),
										gc.getInfoTypeForString("LEADER_SALLOS"),	gc.getInfoTypeForString("LEADER_LETHE"),	gc.getInfoTypeForString("LEADER_JUDECCA")]

			lDemonLordsTraitList   += [	"TRAIT_PACT_MERESIN",						"TRAIT_PACT_OUZZA",							"TRAIT_PACT_STATIUS",
										"TRAIT_PACT_SALLOS",						"TRAIT_PACT_LETHE",							"TRAIT_PACT_JUDECCA"]

		lEverActive					= [ iLeader for iLeader in lDemonLordsList if CyGame().isLeaderEverActive(iLeader) ]
		if not lEverActive: return
		lTraitsToRemoveA			= []
		lTraitsToRemoveB			= []
		### If a member of TeamA or TeamB is a DemonLord put their trait in the list
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer				= gc.getPlayer(iLoopPlayer)
			if not pLoopPlayer.isAlive():	continue
			iLeader					= pLoopPlayer.getLeaderType()
			if not iLeader in lEverActive:	continue
			iLoopTeam				= pLoopPlayer.getTeam()
			if   iLoopTeam == iTeamA:
				iIndex				= lDemonLordsList.index(iLeader)
				lTraitsToRemoveA.append(lDemonLordsTraitList[iIndex])
			elif iLoopTeam == iTeamB:
				iIndex				= lDemonLordsList.index(iLeader)
				lTraitsToRemoveB.append(lDemonLordsTraitList[iIndex])
		### Remove Traits granted by TeamA from TeamB if any
		for szTrait in lTraitsToRemoveA:
			iTrait					= gc.getInfoTypeForString(szTrait)
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer			= gc.getPlayer(iLoopPlayer)
				if not pLoopPlayer.isAlive():	continue
				iLoopTeam			= pLoopPlayer.getTeam()
				if iLoopTeam != iTeamB:			continue
				if not gc.isNoCrash():
					pLoopPlayer.setHasTrait((iTrait),False,-1,True,True)
				else:
					pLoopPlayer.setHasTrait((iTrait),False)
		### Remove Traits granted by TeamB from TeamA if any
		for szTrait in lTraitsToRemoveB:
			iTrait					= gc.getInfoTypeForString(szTrait)
			for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
				pLoopPlayer			= gc.getPlayer(iLoopPlayer)
				if not pLoopPlayer.isAlive():	continue
				iLoopTeam			= pLoopPlayer.getTeam()
				if iLoopTeam != iTeamA:			continue
				if not gc.isNoCrash():
					pLoopPlayer.setHasTrait((iTrait),False,-1,True,True)
				else:
					pLoopPlayer.setHasTrait((iTrait),False)

	### TODO: Dictionaries
	def cityTraitCheck(self, pCity):
		gc			= CyGlobalContext()
		iPlayer		= pCity.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)

		if pPlayer.hasTrait(self.Traits["Imperialist"]):
			eSpeed		= CyGame().getGameSpeedType()
			iCulture	= 10
			if   eSpeed == self.GameSpeeds["Marathon"]:	iCulture = iCulture * 3
			elif eSpeed == self.GameSpeeds["Epic"]:		iCulture = iCulture * 3 / 2
			elif eSpeed == self.GameSpeeds["Quick"]:	iCulture = iCulture / 3 * 2
			pCity.changeCulture(iPlayer, iCulture, True)

		if gc.getInfoTypeForString("MODULE_IMPORTANT_LEADERS") != -1:
			if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_TYRANT")):
				pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_TYRANT"), 1)

		if pCity.isCapital():
			if pPlayer.hasTrait(self.Traits["Hydromancer 1"]):
				pCity.setNumRealBuilding(self.Buildings["Water Mana"], 1)
			if pPlayer.hasTrait(self.Traits["Necromancer 1"]):
				pCity.setNumRealBuilding(self.Buildings["Death Mana"], 1)
			if pPlayer.hasTrait(self.Traits["Ambitious"]):
				pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MANA_MIND"), 1)
			if gc.getInfoTypeForString("MODULE_CHUREL") !=- 1:
				if pPlayer.hasTrait(self.Traits["Graveleech 1"]):
					pCity.setNumRealBuilding(self.Buildings["Death Mana"], 1)
			if gc.getInfoTypeForString("MODULE_EMERGENT_LEADERS") !=- 1:
				if pPlayer.hasTrait(self.Traits["Incorporeal 1"]):
					pCity.setNumRealBuilding(self.Buildings["Nightmare"], 1)

	### TODO: Dictionaries
	def cityLeaderCheck(self, pCity):
		gc			= CyGlobalContext()
		iPlayer		= pCity.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)
		iLeader		= pPlayer.getLeaderType()

		if iLeader == gc.getInfoTypeForString("LEADER_SAUROS"):
			iCiv	= pPlayer.getCivilizationType()
			if   iCiv == self.Civilizations["Clan of Embers"]:
				pCity.setCityClass(gc.getInfoTypeForString("CITYCLASS_SAUROS_CLAN"))
			elif iCiv == self.Civilizations["Cualli"]:
				pCity.setCityClass(gc.getInfoTypeForString("CITYCLASS_SAUROS_CUALLI"))

		if iLeader == self.Leaders["Risen Emperor"]:
			pCity.setNumRealBuilding(self.Buildings["Emperors Mark"], 1)

	### TODO: Dictionaries
	def cityCivCheck(self, pCity):
		gc			= CyGlobalContext()
		iPlayer		= pCity.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)
		iCiv		= pPlayer.getCivilizationType()

		if   iCiv == self.Civilizations["Infernal"]:
			pCity.setNumRealBuilding(self.Buildings["Demonic Citizens"], 1)
			pCity.setPopulation(3)
			if CyGame().countKnownTechNumTeams(self.Techs["Infernal Pact"]) > 0:
				pCity.setHasReligion(self.Religions["Ashen Veil"], True, True, True)
				pCity.setNumRealBuilding(self.Buildings["Elder Council"], 1)
				pCity.setNumRealBuilding(self.Buildings["Barracks"], 1)
				pCity.setNumRealBuilding(self.Buildings["Obsidian Gate"], 1)
				pCity.setNumRealBuilding(self.Buildings["Forge"], 1)
				pCity.setNumRealBuilding(self.Buildings["Mage Guild"], 1)

		elif iCiv == self.Civilizations["Austrin"]:
			pCity.setNumRealBuilding(self.Buildings["Austrin Settlement"], 1)

		elif iCiv == self.Civilizations["Balseraphs"]:
			pCity.setHasCorporation( self.Corporations["Masquerade"], True, False, False)

		elif iCiv == self.Civilizations["Barbarian (Orc)"]:
			eEra		= CyGame().getStartEra()
			iUnit1		= self.Units["Generic"]["Warrior"]
			iX			= pCity.getX()
			iY			= pCity.getY()
			iAI			= UnitAITypes.NO_UNITAI
			iDirection	= DirectionTypes.DIRECTION_SOUTH
			if   pPlayer.isHasTech(self.Techs["Iron Working"]) or eEra > self.Eras["Classical"]:
				iUnit1	= self.Units["Generic"]["Champion"]
			elif pPlayer.isHasTech(self.Techs["Bronze Working"]) or eEra > self.Eras["Ancient"]:
				iUnit1	= self.Units["Generic"]["Axeman"]
			newUnit1	= pPlayer.initUnit(iUnit1, iX, iY, iAI, iDirection)
			newUnit1.setHasPromotion( self.Promotions["Race"]["Orcish"], True)
			iUnit2	= self.Units["Generic"]["Archer"]
			if pPlayer.isHasTech( self.Techs["Bowyers"]) or eEra > self.Eras["Classical"]:
				iUnit2	= self.Units["Generic"]["Longbowman"]
			newUnit2	= pPlayer.initUnit(iUnit2, iX, iY, iAI, iDirection)
			newUnit3	= pPlayer.initUnit(iUnit2, iX, iY, iAI, iDirection)
			newUnit2.setHasPromotion(self.Promotions["Race"]["Orcish"], True)
			newUnit3.setHasPromotion(self.Promotions["Race"]["Orcish"], True)
			if not pPlayer.isHasTech( self.Techs["Archery"]) or eEra == self.Eras["Ancient"]:
				newUnit2.setHasPromotion(self.Promotions["Effects"]["Weak"], True)
				newUnit3.setHasPromotion(self.Promotions["Effects"]["Weak"], True)

		elif iCiv == self.Civilizations["D'Tesh"]:
			pPlot	= pCity.plot()
			iBonus	= pPlot.getBonusType(-1)
			if iBonus != -1:
				tBonusAlive		= (	self.Resources["Arctic Deer"],	self.Resources["Banana"],	self.Resources["Corn"],			self.Resources["Cotton"],	self.Resources["Deer"],
									self.Resources["Dye"],			self.Resources["Fur"],		self.Resources["Gulagarm"],		self.Resources["Ivory"],	self.Resources["Incense"],
									self.Resources["Mushrooms"],	self.Resources["Pig"],		self.Resources["Razorweed"],	self.Resources["Reagents"],	self.Resources["Rice"],
									self.Resources["Silk"],			self.Resources["Sheep"],	self.Resources["Sugar"],		self.Resources["Toad"],		self.Resources["Wine"],
									self.Resources["Wheat"])

				tBonusNightmare	= (	self.Resources["Bison"], self.Resources["Camel"], self.Resources["Cow"], self.Resources["Horse"])

				bWantsNightmare		= False
				bMessage			= False
				if not pPlayer.hasBonus(self.Resources["Nightmare"]):
					bWantsNightmare	= True

				if   iBonus in tBonusAlive:
					pPlot.setBonusType(gc.getInfoTypeForString('BONUS_ASH'))
					bMessage		= True
				elif iBonus in tBonusNightmare:
					if not pPlayer.isHasTech(self.Techs["Animal Husbandry"]):
						pPlot.setBonusType(gc.getInfoTypeForString('BONUS_ASH'))
						bMessage	= True
					else:
						if pPlayer.isHuman():
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_DTESH_FIND_HORSE",()))
							popupInfo.setData1(pCity.getID())
							popupInfo.setData2(iPlayer)
							popupInfo.setData3(121) # onModNetMessage id
							popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_DTESH_FIND_HORSE_NIGHTMARE",()),"")
							popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_DTESH_FIND_HORSE_BURN",()),"")
							popupInfo.setOnClickedPythonCallback("passToModNetMessage")
							popupInfo.addPopup(iPlayer)
						elif bWantsNightmare:
							pPlot.setBonusType(self.Resources["Nightmare"])
						else:
							pPlot.setBonusType(gc.getInfoTypeForString('BONUS_ASH'))
				elif iBonus == self.Resources["Nightmare"]:
					if pPlayer.isHuman():
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
						popupInfo.setText(CyTranslator().getText("TXT_KEY_DTESH_FIND_NIGHTMARE",()))
						popupInfo.setData1(pCity.getID())
						popupInfo.setData2(iPlayer)
						popupInfo.setData3(122) # onModNetMessage id
						popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_DTESH_FIND_NIGHTMARE_KEEP",()),"")
						popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_DTESH_FIND_NIGHTMARE_BURN",()),"")
						popupInfo.setOnClickedPythonCallback("passToModNetMessage")
						popupInfo.addPopup(iPlayer)
					elif bWantsNightmare:
						pPlot.setBonusType(self.Resources["Nightmare"])
					else:
						pPlot.setBonusType(gc.getInfoTypeForString('BONUS_ASH'))

				if bMessage:
					szText		= CyTranslator().getText("TXT_KEY_BONUS_CONVERTED_TO_ASH",())
					szSound		= 'AS2D_DISCOVERBONUS'
					iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
					szArt		= 'Art/Civs/Dtesh/Ashes.dds'
					iGrey		= gc.getInfoTypeForString("COLOR_LIGHT_GREY")
					CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGrey, pPlot.getX(), pPlot.getY(), True, True)

	def razeScorcedEarth(self, pCity):
		gc			= CyGlobalContext()
		pPlot		= pCity.plot()
		iPlayer		= pCity.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)
		iPopulation	= pCity.getPopulation()
		for iUnit in xrange(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(iUnit)
			if pUnit.getOwner() != iPlayer: continue
			pUnit.changeExperience(iPopulation, -1, False, False, False)

	### TODO: rewrite with religion weights
	def razeAoM(self, pCity):
		iInfernal		= self.Civilizations["Infernal"]
		iMercurians		= self.Civilizations["Mercurians"]
		iFrozen			= self.Civilizations["Frozen"]
		if CyGame().getNumCivActive(iInfernal) + CyGame().getNumCivActive(iMercurians) + CyGame().getNumCivActive(iFrozen) <= 0: return
		gc				= CyGlobalContext()
		pPlot			= pCity.plot()
		iPlayer			= pCity.getOwner()
		iNewOwnerCiv	= gc.getPlayer(iPlayer).getCivilizationType()
		iPopulation		= pCity.getPopulation()
		iOriginalPlayer	= pCity.getOriginalOwner()
		pOriginalPlayer	= gc.getPlayer(iOriginalPlayer)
		iOriginalCiv	= pOriginalPlayer.getCivilizationType()
		iAlignment		= pOriginalPlayer.getAlignment()
		iDefaultRace	= gc.getCivilizationInfo(iOriginalCiv).getDefaultRace()
		bCanBeFrozen	= False
		bCanBeMane		= False

		if gc.getInfoTypeForString("MODULE_FROZEN") != -1:
			if CyGame().getNumCivActive(iFrozen) > 0:
				if iDefaultRace == self.Promotions["Effects"]["Winterborn"] or iNewOwnerCiv == self.Civilizations["Frozen"]:
					bCanBeFrozen = True

		if CyGame().countKnownTechNumTeams(self.Techs["Infernal Pact"]) > 0 and CyGame().getNumCivActive(iInfernal) > 0:
			bCanBeMane = True

		if not iOriginalCiv in (iInfernal, iFrozen) and (bCanBeMane or bCanBeFrozen):
			iNumSouls		= iPopulation
			if   iAlignment == self.Alignments["Neutral"]:
				iNumSouls	= (iPopulation / 2) + 1
			elif iAlignment == self.Alignments["Good"]:
				iNumSouls	= 0
			if bCanBeFrozen:	iUnit = self.Units["Frozen"]["Frozen Souls"];	iCiv = iFrozen
			else:				iUnit = self.Units["Infernal"]["Manes"];		iCiv = iInfernal
			for i in xrange(iNumSouls):
				self.giftUnit(iUnit, iCiv, 0, pPlot, iPlayer)

		if CyGame().getBuildingClassCreatedCount(self.Buildings["Mercurian Gate"]) > 0 and CyGame().getNumCivActive(iMercurians) > 0:
			if not iOriginalCiv == iMercurians:
				iNumAngels		= 0
				if   iAlignment == self.Alignments["Neutral"]:
					iNumAngels	= (iPopulation / 4) + 1
				elif iAlignment == self.Alignments["Good"]:
					iNumAngels	= (iPopulation / 2) + 1
				iAngel			= self.Units["Mercurian"]["Angel"]
				for i in xrange(iNumAngels):
					self.giftUnit(iAngel, iMercurians, 0, pPlot, iPlayer)

	def razeScions(self, pCity):
		gc			= CyGlobalContext()
		iPlayer		= pCity.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)
		if not pPlayer.isHasTech(self.Techs["Sorcery"]):	return
		if not pPlayer.isHasTech(self.Techs["Priesthood"]):	return
		iReborn		= self.Units["Scions"]["Reborn"]
		iPopulation	= pCity.getPopulation()
		iNumReborn	= max((iPopulation - 1), 1)
		iX			= pCity.getX()
		iY			= pCity.getY()
		iAI			= UnitAITypes.NO_UNITAI
		iDirection	= DirectionTypes.DIRECTION_SOUTH
		bGodKing	= pPlayer.isCivic(self.Civics["God King"])
		for i in xrange(iNumReborn):
			newUnit	= pPlayer.initUnit(iReborn, iX, iY, iAI, iDirection)
			if bGodKing: 
				szName = CyTranslator().getText("TXT_KEY_UNIT_REBORN_GOD_KING", ())
				newUnit.setName(szName)

		szText		= CyTranslator().getText("TXT_KEY_MESSAGE_REBORN_SPAWNED_RAZED", ())
		szSound		= ''
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		szArt		= 'Art/Interface/Buttons/Units/Scions/reborn.dds'
		iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
		CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, iX, iY, True, True)

	def razeDtesh(self, pCity):
		gc			= CyGlobalContext()
		iPlayer		= pCity.getOwner()
		pPlayer		= gc.getPlayer(iPlayer)
		iX			= pCity.getX()
		iY			= pCity.getY()
		iAI			= UnitAITypes.NO_UNITAI
		iDirection	= DirectionTypes.DIRECTION_SOUTH
		iSlave		= self.Units["D'Tesh"]["Slave"]
		iPopulation	= pCity.getPopulation()
		iNumSlave	= max((iPopulation * 3 / 4), 1)
		pPlayer.initUnit(self.Units["D'Tesh"]["Vessel of D'tesh"], iX, iY, iAI, iDirection)
		for i in xrange(iNumSlave):
			pPlayer.initUnit(iSlave, iX, iY, iAI, iDirection)

	### TODO: Dictionaries
	def doCityTurnPixieGarden(self, pCity, iPlayer):
		if CyGame().getSorenRandNum(1000, "City Turn Pixie") > 2:	return
		gc		= CyGlobalContext()
		pPlot	= pCity.plot()
		if pPlot.getNumUnits() <= 0:					return
		pUnit	= pPlot.getUnit(0)
		if not pUnit.isAlive():							return
		if pUnit.isHasPromotion(gc.getInfoTypeForString("PROMOTION_PIXIE_COMPANION")): return
		pUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_PIXIE_COMPANION"), True)

		szText		= CyTranslator().getText("TXT_KEY_MESSAGE_PIXIE_JOIN", ())
		szSound		= 'AS2D_TECH_DING'
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		szArt		= 'Art/units/spawns/fairy/fairy.dds'
		iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
		CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, pPlot.getX(), pPlot.getY(), True, True)

	def doCityTurnEAE(self, pCity, iPlayer):
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(iPlayer)
		iTeam	= pPlayer.getTeam()
		pTeam	= gc.getTeam(iTeam)
		lTeams	= []
		for iLoopPlayer in xrange(gc.getMAX_PLAYERS()):
			pLoopPlayer = gc.getPlayer(iLoopPlayer)
			if not pLoopPlayer.isAlive():			continue
			if iLoopPlayer == iPlayer:				continue
			iLoopTeam = pLoopPlayer.getTeam()
			if not pTeam.isOpenBorders(iLoopTeam):	continue
			lTeams.append(iLoopTeam)
		if len(lTeams) < 3: return
		for iTech in xrange(gc.getNumTechInfos()):
			if not pPlayer.canEverResearch(iTech):	continue
			if pTeam.isHasTech(iTech):				continue
			iCount = 0
			for iLoopTeam in lTeams:
				pLoopTeam = gc.getTeam(iLoopTeam)
				if not pLoopTeam.isHasTech(iTech):	continue
				iCount += 1
			if iCount < 3:							continue
			pTeam.setHasTech(iTech, True, iPlayer, False, True)

			szText		= CyTranslator().getText("TXT_KEY_MESSAGE_EYES_AND_EARS_NETWORK_FREE_TECH", ())
			szSound		= 'AS2D_TECH_DING'
			iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
			szArt		= 'Art/Interface/Buttons/Buildings/Eyesandearsnetwork.dds'
			iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
			CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, pCity.getX(), pCity.getY(), True, True)

	def doCityTurnHallOfMirrors(self, pCity, iPlayer):
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(iPlayer)
		iTeam	= pPlayer.getTeam()
		pTeam	= gc.getTeam(iTeam)
		pUnit	= -1
		iX		= pCity.getX()
		iY		= pCity.getY()
		for dX, dY in RANGE1:
			if not pUnit == -1: break
			pDeltaPlot = CyMap().plot(iX+dX, iY+dY)
			if not pDeltaPlot.isVisibleEnemyUnit(iPlayer): continue
			for iUnit in xrange(pDeltaPlot.getNumUnits()):
				pLoopUnit	= pDeltaPlot.getUnit(iUnit)
				if not pTeam.isAtWar(pLoopUnit.getTeam()): continue
				pUnit		= pLoopUnit
				break
		if pUnit == -1: return
		newUnit = pPlayer.initUnit(pUnit.getUnitType(), iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(self.Promotions["Race"]["Illusion"], True)
		if pPlayer.hasTrait(self.Traits["Summoner"]):	newUnit.setDuration(5)
		else:											newUnit.setDuration(3)
		for iPromotion in xrange(gc.getNumPromotionInfos()):
			if not newUnit.isHasPromotion(iPromotion):				continue
			if not gc.getPromotionInfo(iPromotion).isEquipment():	continue
			newUnit.setHasPromotion(iPromotion, False)

	### TODO: Dictionaries
	def doCityTurnKahdiVault(self, pCity, iPlayer):
		gc		= CyGlobalContext()
		pPlayer	= gc.getPlayer(iPlayer)
		iMax	= 1
		iMult	= 1
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_KAHD_OGHMA")):
			iMult	= 3
			iMax	= 1.5
		if pCity.getNumBuilding(self.Buildings["Library"]) > 0:	iMult += 0.5
		if CyGame().getSorenRandNum(10000, "Planar Gate") > (self.Defines["Planar Gate"] * iMult): return
		lAvailableUnits	= []
		iGates			= pPlayer.countNumBuildings(self.Buildings["Kahdi Vault Gate"])
		iLibraries		= pPlayer.countNumBuildings(self.Buildings["Library"])
		iMedHalls		= pPlayer.countNumBuildings(self.Buildings["School of Govannon"])
		iGreatLibrary	= pPlayer.countNumBuildings(self.Buildings["The Great Library"]) * 4
		iMageGuild		= pPlayer.countNumBuildings(self.Buildings["Wizards Hall"])
		iMax = iMax * (iGates + iLibraries + iMedHalls + iGreatLibrary + iMageGuild)
		bMageGuild		= False
		bMedHalls		= False
		bMammon			= False
		if pCity.getNumBuilding(self.Buildings["Wizards Hall"]) > 0:		bMageGuild	= True
		if pCity.getNumBuilding(self.Buildings["School of Govannon"]) > 0:	bMedHalls	= True
		if pPlayer.hasTrait(gc.getInfoTypeForString("TRAIT_KAHD_MAMMON")):	bMammon		= True

		lUnitTypes		= [	self.Units["Kahdi"]["Gnosling"],			self.Units["Kahdi"]["Thade"],		self.Units["Summons"]["Djinn"],			self.Units["Summons"]["Fire Elemental"],
							self.Units["Summons"]["Air Elemental"],		self.Units["Summons"]["Spectre"],	self.Units["Summons"]["Flesh Golem"],	self.Units["Summons"]["Pit Beast"],
							self.Units["Summons"]["Ice Elemental"],		self.Units["Summons"]["Einherjar"],	self.Units["Summons"]["Mistform"],		self.Units["Summons"]["Aurealis"],
							self.Units["Summons"]["Water Elemental"],	self.Units["Kahdi"]["Psion"]]

		fUnitUC			= (	self.UnitClasses["Gnossling"],				self.UnitClasses["Thade"],			self.UnitClasses["Djinn"],				self.UnitClasses["Fire Elemental"],
							self.UnitClasses["Air Elemental"],			self.UnitClasses["Spectre"],		self.UnitClasses["Flesh Golem"],		self.UnitClasses["Pit Beast"],
							self.UnitClasses["Ice Elemental"],			self.UnitClasses["Einherjar"],		self.UnitClasses["Mistform"],			self.UnitClasses["Aurealis"],
							self.UnitClasses["Water Elemental"],		self.UnitClasses["Psion"])

		fCapDivider		= (	2,											3,									8,										6,
							6,											4,									6,										4,
							4,											4,									8,										6,
							6,											10)

		fManaType		= (	-1,											-1,									self.Mana["Metamagic"],					self.Mana["Fire"],
							self.Mana["Air"],							self.Mana["Death"],					self.Mana["Body"],						self.Mana["Entropy"],
							self.Mana["Ice"],							self.Mana["Law"],					self.Mana["Shadow"],					self.Mana["Sun"],
							self.Mana["Water"],							-1)

		fPrereqs		= (	True,										bMageGuild,							bMedHalls,								bMedHalls,
							bMedHalls,									bMedHalls,							bMedHalls,								bMedHalls,
							bMedHalls,									bMedHalls,							bMedHalls,								bMedHalls,
							bMedHalls,									bMammon)

		for iUnit in lUnitTypes:
			iIndex	= lUnitTypes.index(iUnit)
			if not fPrereqs[iIndex]:	continue
			iCountMana	= 1
			if fManaType[iIndex] != -1:
				iCountMana = pPlayer.getNumAvailableBonuses(fManaType[iIndex])
			if iCountMana == 0:			continue
			iCountUC	= pPlayer.getUnitClassCount(fUnitUC[iIndex])
			iUnitMax	= iMax / (fCapDivider[iIndex]) * iCountMana
			if iCountUC >= iUnitMax:	continue
			lAvailableUnits.append(iUnit)

		if not lAvailableUnits:	return
		iTarget			= lAvailableUnits[CyGame().getSorenRandNum(len(lAvailableUnits), "Kahdi Gate")]
		newUnit			= pPlayer.initUnit(iTarget, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if iTarget == self.Units["Kahdi"]["Thade"]:

			fSpheres	= (	self.Promotions["Generic"]["Air I"],	self.Promotions["Generic"]["Earth I"],		self.Promotions["Generic"]["Fire I"],			self.Promotions["Generic"]["Ice I"],		self.Promotions["Generic"]["Water I"],
							self.Promotions["Generic"]["Chaos I"],	self.Promotions["Generic"]["Death I"],		self.Promotions["Generic"]["Dimensional I"],	self.Promotions["Generic"]["Entropy I"],	self.Promotions["Generic"]["Shadow I"],
							self.Promotions["Generic"]["Body I"],	self.Promotions["Generic"]["Creation I"],	self.Promotions["Generic"]["Enchantment I"],	self.Promotions["Generic"]["Force I"],		self.Promotions["Generic"]["Nature I"],
							self.Promotions["Generic"]["Metamagic I"])

			newUnit.setLevel(3)
			newUnit.setExperienceTimes100(1000 + CyGame().getGlobalCounter() * 25, -1)
			for iSphere in fSpheres:
				if CyGame().getSorenRandNum(8, "Mobius Witch Free Promotions") != 0: continue
				newUnit.setHasPromotion(iSphere, True)

		szText		= CyTranslator().getText("TXT_KEY_MESSAGE_KAHDI_GATE", ())
		szSound		= 'AS2D_DISCOVERBONUS'
		iMessage	= InterfaceMessageTypes.MESSAGE_TYPE_MINOR_EVENT
		szArt		= gc.getUnitInfo(newUnit.getUnitType()).getButton()
		iGreen		= gc.getInfoTypeForString("COLOR_GREEN")
		CyInterface().addMessage(iPlayer, True, 25, szText, szSound, iMessage, szArt, iGreen, pCity.getX(), pCity.getY(), True, True)
