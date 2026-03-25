#Set aside for scenario specific functions, the epic game should never use this file
# does anyone actually read these comments?

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvScreenEnums
import CustomFunctions
import CvEspionageAdvisor
from BasicFunctions import *

# globals
cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

class ScenarioFunctions:

	def addPopupWB(self, szText, sDDS):
		szTitle = CyGameTextMgr().getTimeStr(CyGame().getGameTurn(), false)
		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xRes = screen.getXResolution()
		yRes = screen.getYResolution()
		popup = PyPopup.PyPopup(-1)
		popup.addDDS(sDDS, 0, 0, 500, 800)
		popup.addSeparator()
		popup.setHeaderString(szTitle)
		popup.setBodyString(szText)
		popup.setPosition((xRes - 840) / 2,(yRes - 640) / 2)
		popup.setSize(840, 640)
		popup.launch(true, PopupStates.POPUPSTATE_IMMEDIATE)

	def addPopup(self, szText, sDDS):
		szTitle = CyGameTextMgr().getTimeStr(CyGame().getGameTurn(), False)
		popup = PyPopup.PyPopup(-1)
		popup.addDDS(sDDS, 0, 0, 128, 384)
		popup.addSeparator()
		popup.setHeaderString(szTitle)
		popup.setBodyString(szText)
		popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

	def cannotResearch(self, ePlayer, eTech, bTrade):
		pPlayer = gc.getPlayer(ePlayer)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			return True

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):
			if gc.getTechInfo(eTech).getEra() == gc.getInfoTypeForString('ERA_MEDIEVAL'):
				return True

		return False

	def cannotTrain(self, pCity, eUnit, bContinue, bTestVisible, bIgnoreCost, bIgnoreUpgrades):
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			if pPlayer.isHuman():
				return True

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			if pPlayer.isHuman():
				if eUnit != gc.getInfoTypeForString('UNIT_HUNTER'):
					return True
			else:
				return True

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			if not pPlayer.isHuman():
				if gc.getUnitInfo(eUnit).getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
					if eUnit != gc.getInfoTypeForString('UNIT_WORKBOAT'):
						return True

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			if eUnit == gc.getInfoTypeForString('UNIT_SETTLER'):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_PERPENTACH'):
					return True

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			if not pPlayer.isHuman():
				if gc.getTeam(pPlayer.getTeam()).isHuman():
					if eUnit == gc.getInfoTypeForString('UNIT_GILDEN'):
						return True
					if eUnit == gc.getInfoTypeForString('UNIT_ALAZKAN'):
						return True

		return False

	def doTurn(self):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_WALL):
			self.doTurnAgainstTheWall()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
			self.doTurnBarbarianAssault()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			self.doTurnBeneathTheHeel()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			self.doTurnFallOfCuantine()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			self.doTurnGrandMenagerie()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			if gc.getPlayer(0).isHuman():
				self.doTurnIntoTheDesertMalakim()
			else:
				self.doTurnIntoTheDesertCalabim()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			self.doTurnLordOfTheBalors()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			self.doTurnMulcarnReborn()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			self.doTurnTheBlackTower()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			self.doTurnTheMomus()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			self.doTurnSplinteredCourt()
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			self.doTurnTheRadiantGuard()

	def doTurnAgainstTheWall(self):
		iPlayer = 0
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.getNumCities() < 5:
			if gc.getGame().getScenarioCounter() != 0:
				gc.getGame().changeScenarioCounter(-1 * gc.getGame().getScenarioCounter())
		else:
			gc.getGame().changeScenarioCounter(1)
			if gc.getGame().getScenarioCounter() == 100:
				gc.getGame().setWinner(pPlayer.getTeam(), 2)

	def doTurnBarbarianAssault(self):
		if gc.getGame().countCivPlayersAlive() > 5:
			gc.getGame().changeCutLosersCounter(-1)
			if gc.getGame().getCutLosersCounter() == 0:
				iClanOfEmbers = gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS')
				iWorstPlayerRank = -1
				iWorstPlayer = -1
				for iPlayer in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.isAlive():
						if pPlayer.getCivilizationType() != iClanOfEmbers:
							if gc.getGame().getPlayerRank(iPlayer) > iWorstPlayerRank:
								iWorstPlayerRank = gc.getGame().getPlayerRank(iPlayer)
								iWorstPlayer = iPlayer
				gc.getPlayer(iWorstPlayer).setAlive(false)
				gc.getGame().changeCutLosersCounter(50)

	def doTurnBeneathTheHeel(self):
		iPlayer = 0
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.getGold() >= 40:
			pCity = pPlayer.getCapitalCity()
			iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_MAGNADINE_HIRE_UNITS')
			triggerData = pPlayer.initTriggeredData(iEvent, true, -1, pCity.getX(), pCity.getY(), iPlayer, pCity.getID(), -1, -1, -1, -1)
		pTeam = gc.getTeam(3) #Calabim
		iTeam2 = 0 #Hippus
		if pTeam.isAlive():
			if pTeam.AI_getAtPeaceCounter(iTeam2) > 50:
				if pTeam.isHasMet(iTeam2):
					if pTeam.getAtWarCount(True) == 0:
						pTeam.declareWar(iTeam2, false, WarPlanTypes.WARPLAN_TOTAL)
		pCity = gc.getPlayer(1).getCapitalCity() #Illians
		pPlot = pCity.plot()
		bWin = False
		iBarnaxus = gc.getInfoTypeForString('EQUIPMENT_PIECES_OF_BARNAXUS')
		iPromBarnaxus = gc.getInfoTypeForString('PROMOTION_PIECES_OF_BARNAXUS')
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getUnitType() == iBarnaxus:
				bWin = True
			if pUnit.isHasPromotion(iPromBarnaxus):
				bWin = True
		if bWin:
			gc.getGame().setWinner(pPlayer.getTeam(), 2)

	def doTurnFallOfCuantine(self):
		iPlayer = 0 #Decius
		pPlayer = gc.getPlayer(iPlayer)
		if gc.getGame().getScenarioCounter() == 7:
			gc.getGame().setWinner(pPlayer.getTeam(), 2)
		if gc.getGame().getScenarioCounter() == 6:
			gc.getGame().changeScenarioCounter(1)
			iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_FALL_OF_CUANTINE_FLEE')
			triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, 0, -1, -1, -1, -1, -1)
		if gc.getGame().getScenarioCounter() == 3:
			gc.getGame().changeScenarioCounter(1)
			addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_LANUN",()), iPlayer)
			pTeam = gc.getTeam(pPlayer.getTeam())
			if not pTeam.isAtWar(1):
				pTeam.declareWar(1, true, WarPlanTypes.WARPLAN_TOTAL)
			pTeam.setPermanentWarPeace(1, True)
			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
		if gc.getGame().getScenarioCounter() == 0:
			pPlot = CyMap().plot(24,12)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getOwner() == iPlayer:
					if gc.getGame().getScenarioCounter() == 0:
						gc.getGame().changeScenarioCounter(1)
						pCity = pPlot.getPlotCity()
						pPlayer.acquireCity(pCity,false,false)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_CONFESSOR",()), iPlayer)
						CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_CONFESSOR_BALLOON",()),'',1,'Art/Interface/Buttons/Units/Priest Order.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
						CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)

		pPlot = CyMap().plot(16,2)
		if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVMENT_JUNGLE_ALTAR'):
			# DemonPerTurnKnownTechPercent is a decent standin for the old lairSpawnRate
			iChance = gc.getHandicapInfo(gc.getGame().getHandicapType()).getDemonPerTurnKnownTechsPercent()
			if gc.getGame().getSorenRandNum(100, "Fall of Cuantine") < iChance:
				iRnd = gc.getGame().getSorenRandNum(100, "Fall of Cuantine")
				if iRnd < 50:
					iUnit = gc.getInfoTypeForString('UNIT_FREAK')
				else:
					iUnit = gc.getInfoTypeForString('UNIT_DROWN')
				bPlayer = gc.getPlayer(gc.getORC_PLAYER())
				bPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

	def doTurnGrandMenagerie(self):
		bPlayer = gc.getPlayer(gc.getANIMAL_PLAYER())
		bBear = False
		bElephant = False
		bGorilla = False
		bGriffon = False
		bLion = False
		bTiger = False
		bWolf = False
		iBear = gc.getInfoTypeForString('UNITCLASS_BEAR')
		iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
		iElephant = gc.getInfoTypeForString('UNITCLASS_ELEPHANT')
		iForest = gc.getInfoTypeForString('FEATURE_FOREST')
		iGorilla = gc.getInfoTypeForString('UNITCLASS_GORILLA')
		iGriffon = gc.getInfoTypeForString('UNITCLASS_GRIFFON')
		iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
		iLion = gc.getInfoTypeForString('UNITCLASS_LION')
		iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
		iTiger = gc.getInfoTypeForString('UNITCLASS_TIGER')
		iTaiga = gc.getInfoTypeForString('TERRAIN_TUNDRA')
		iWolf = gc.getInfoTypeForString('UNITCLASS_WOLF')
		if bPlayer.getUnitClassCount(iBear) < 2:
			bBear = True
			lBear = []
		if bPlayer.getUnitClassCount(iGorilla) < 1:
			bGorilla = True
			lGorilla = []
		if bPlayer.getUnitClassCount(iLion) < 2:
			bLion = True
			lLion = []
		if bPlayer.getUnitClassCount(iTiger) < 1:
			bTiger = True
			lTiger = []
		if bPlayer.getUnitClassCount(iWolf) < 2:
			bWolf = True
			lWolf = []
		if gc.getGame().getScenarioCounter() > 0:
			if bPlayer.getUnitClassCount(iElephant) == 0:
				bElephant = True
				lElephant = []
		if gc.getGame().getScenarioCounter() > 1:
			if bPlayer.getUnitClassCount(iGriffon) == 0:
				bGriffon = True
				lGriffon = []
		if (bBear or bElephant or bGorilla or bGriffon or bLion or bTiger or bWolf):
			for i in range (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if not pPlot.isVisibleToCivTeam():
					if bBear:
						if pPlot.getTerrainType() == iTaiga:
							lBear.append(pPlot)
					if bElephant:
						if pPlot.getTerrainType() == iPlains:
							lElephant.append(pPlot)
					if bGorilla:
						if pPlot.getFeatureType() == iJungle:
							lGorilla.append(pPlot)
					if bGriffon:
						if pPlot.isPeak():
							lGriffon.append(pPlot)
					if bLion:
						if pPlot.getTerrainType() == iDesert:
							lLion.append(pPlot)
					if bTiger:
						if pPlot.getFeatureType() == iJungle:
							lTiger.append(pPlot)
					if bWolf:
						if pPlot.getFeatureType() == iForest:
							lWolf.append(pPlot)
		if bBear:
			if len(lBear) > 0:
				pPlot = lBear[CyGame().getSorenRandNum(len(lBear), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_POLAR_BEAR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bElephant:
			if len(lElephant) > 0:
				pPlot = lElephant[CyGame().getSorenRandNum(len(lElephant), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_ELEPHANT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bGorilla:
			if len(lGorilla) > 0:
				pPlot = lGorilla[CyGame().getSorenRandNum(len(lGorilla), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GORILLA'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bGriffon:
			if len(lGriffon) > 0:
				pPlot = lGriffon[CyGame().getSorenRandNum(len(lGriffon), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_GRIFFON'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bLion:
			if len(lLion) > 0:
				pPlot = lLion[CyGame().getSorenRandNum(len(lLion), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_LION'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bTiger:
			if len(lTiger) > 0:
				pPlot = lTiger[CyGame().getSorenRandNum(len(lTiger), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_TIGER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if bWolf:
			if len(lWolf) > 0:
				pPlot = lWolf[CyGame().getSorenRandNum(len(lWolf), "Grand Menagerie")-1]
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_WOLF'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		iPlayer = 0 #Falamar
		if gc.getGame().getScenarioCounter() == 0:
			if gc.getPlayer(iPlayer).getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_GRAND_MENAGERIE')) > 0:
				gc.getGame().changeScenarioCounter(1)
				szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_KEELYN_ELEPHANT",())
				addPlayerPopup(szText, iPlayer)
		if gc.getGame().getScenarioCounter() == 1:
			if gc.getPlayer(iPlayer).getUnitClassCount(iElephant) > 0:
				gc.getGame().changeScenarioCounter(1)
				szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_KEELYN_GRIFFON",())
				addPlayerPopup(szText, iPlayer)
		if gc.getGame().getScenarioCounter() == 2:
			if gc.getPlayer(iPlayer).getUnitClassCount(iGriffon) > 0:
				gc.getGame().changeScenarioCounter(1)
				gc.getGame().setWinner(gc.getPlayer(iPlayer).getTeam(), 2)

	def doTurnIntoTheDesertCalabim(self):
		iPlayer = 1 #Decius
		if gc.getGame().getGameTurn() == 3:
			addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_GOVERNOR",()), iPlayer)
		if gc.getGame().getScenarioCounter() > 0:
			if CyGame().getSorenRandNum(100, "Disciple Spawn") < 10:
				iVarn = 0
				pVarnPlayer = gc.getPlayer(iVarn)
				if pVarnPlayer.isAlive():
					pPlot = CyMap().plot(30,23)
					if not pPlot.isVisibleEnemyUnit(iVarn):
						pVarnPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_EMPYREAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		if gc.getGame().getScenarioCounter() > 1:
			gc.getGame().changeScenarioCounter(-1)
			if gc.getGame().getScenarioCounter() == 1:
				addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_ATTACK",()), iPlayer)
		if gc.getGame().getScenarioCounter() == 1:
			bValid = True
			for iLoopPlayer in range(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if not pLoopPlayer.isHuman():
					for pyCity in PyPlayer(iLoopPlayer).getCityList():
						pCity = pyCity.GetCy()
						if pCity.isHasReligion(gc.getInfoTypeForString('RELIGION_THE_EMPYREAN')):
							bValid = False
			if bValid:
				gc.getGame().setWinner(gc.getPlayer(iPlayer).getTeam(), 2)

	def doTurnIntoTheDesertMalakim(self):
		if gc.getGame().getScenarioCounter() > 100:
			gc.getGame().changeScenarioCounter(-1)
			if gc.getGame().getScenarioCounter() == 100:
				iPlayer = 0 #Decius
				addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_COUNCIL",()), iPlayer)
				gc.getGame().changeScenarioCounter(-1)

	def doTurnLordOfTheBalors(self):
		iManeChance = 4 + int(gc.getGame().getHandicapType())
		iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
		iMercurians = gc.getInfoTypeForString('CIVILIZATION_MERCURIANS')
		pJudecca = gc.getPlayer(6)
		pSallos = gc.getPlayer(7)
		pOuzza = gc.getPlayer(8)
		pMeresin = gc.getPlayer(9)
		pStatius = gc.getPlayer(10)
		pLethe = gc.getPlayer(11)
		for iPlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive():
				if pPlayer.getCivilizationType() == iInfernal:
					if gc.getGame().getSorenRandNum(100, "Mane Spawns") < iManeChance:
						py = PyPlayer(iPlayer)
						if pPlayer.getNumCities() > 0:
							iRnd = CyGame().getSorenRandNum(py.getNumCities(), "Gift Unit")
							pCity = py.getCityList()[iRnd]
							if CyGame().getSorenRandNum(100, "Manes") < (100 - (pCity.getPopulation() * 5)):
								pCity.changePopulation(1)
							else:
								pPlayer.initUnit(gc.getInfoTypeForString('UNIT_MANES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if pPlayer.isHuman():
					if pPlayer.getCivilizationType() != iMercurians:
						pTeam = gc.getTeam(pPlayer.getTeam())
						if not pTeam.isAtWar(pJudecca.getTeam()):
							if pTeam.AI_getAtPeaceCounter(6) >= 100:
								pTeam.setPermanentWarPeace(6, False)
								gc.getTeam(pJudecca.getTeam()).declareWar(pPlayer.getTeam(), true, WarPlanTypes.WARPLAN_TOTAL)
								pTeam.setPermanentWarPeace(6, True)
						if not pTeam.isAtWar(pSallos.getTeam()):
							if pTeam.AI_getAtPeaceCounter(7) >= 50:
								pTeam.setPermanentWarPeace(7, False)
								gc.getTeam(pSallos.getTeam()).declareWar(pPlayer.getTeam(), true, WarPlanTypes.WARPLAN_TOTAL)
								pTeam.setPermanentWarPeace(7, True)
						if not pTeam.isAtWar(pOuzza.getTeam()):
							if pTeam.AI_getAtPeaceCounter(8) >= 25:
								pTeam.setPermanentWarPeace(8, False)
								gc.getTeam(pOuzza.getTeam()).declareWar(pPlayer.getTeam(), true, WarPlanTypes.WARPLAN_TOTAL)
								pTeam.setPermanentWarPeace(8, True)
						if not pTeam.isAtWar(pMeresin.getTeam()):
							if pTeam.AI_getAtPeaceCounter(9) >= 25:
								pTeam.setPermanentWarPeace(9, False)
								gc.getTeam(pMeresin.getTeam()).declareWar(pPlayer.getTeam(), true, WarPlanTypes.WARPLAN_TOTAL)
								pTeam.setPermanentWarPeace(9, True)
						if not pTeam.isAtWar(pStatius.getTeam()):
							if pTeam.AI_getAtPeaceCounter(10) >= 100:
								pTeam.setPermanentWarPeace(10, False)
								gc.getTeam(pStatius.getTeam()).declareWar(pPlayer.getTeam(), true, WarPlanTypes.WARPLAN_TOTAL)
								pTeam.setPermanentWarPeace(10, True)
						if not pTeam.isAtWar(pLethe.getTeam()):
							if pTeam.AI_getAtPeaceCounter(11) >= 50:
								pTeam.setPermanentWarPeace(11, False)
								gc.getTeam(pLethe.getTeam()).declareWar(pPlayer.getTeam(), true, WarPlanTypes.WARPLAN_TOTAL)
								pTeam.setPermanentWarPeace(11, True)
						if gc.getGame().getSorenRandNum(10000, "Tempt") < 200:
							lList = []
							if pJudecca.isAlive():
								if pTeam.isAtWar(pJudecca.getTeam()):
									bValid = False
									if not gc.getPlayer(2).isHuman():
										if not pTeam.isAtWar(2):
											iJudeccaData = 2
											bValid = True
									if not gc.getPlayer(0).isHuman():
										if not pTeam.isAtWar(0):
											iJudeccaData = 0
											bValid = True
									if not gc.getPlayer(1).isHuman():
										if not pTeam.isAtWar(1):
											iJudeccaData = 1
											bValid = True
									if not gc.getPlayer(4).isHuman():
										if not pTeam.isAtWar(4):
											iJudeccaData = 4
											bValid = True
									if bValid:
										lList = lList + ['Judecca']
							if pSallos.isAlive():
								if pTeam.isAtWar(pSallos.getTeam()):
									lList = lList + ['Sallos']
							if pOuzza.isAlive():
								if pTeam.isAtWar(pOuzza.getTeam()):
									lList = lList + ['Ouzza']
							if pMeresin.isAlive():
								if pTeam.isAtWar(pMeresin.getTeam()):
									lList = lList + ['Meresin']
							if pStatius.isAlive():
								if pTeam.isAtWar(pStatius.getTeam()):
									bValid = False
									for pyCity in PyPlayer(iPlayer).getCityList():
										pCity = pyCity.GetCy()
										if gc.getPlayer(pCity.getOriginalOwner()).getCivilizationType() == iInfernal:
											iStatiusData = pCity.getID()
											bValid = True
									if bValid:
										lList = lList + ['Statius']
							if pLethe.isAlive():
								if pTeam.isAtWar(pLethe.getTeam()):
									bValid = False
									py = PyPlayer(iPlayer)
									for pUnit in py.getUnitList():
										if pUnit.isAlive():
											iLetheData = pUnit.getID()
											bValid = True
									lList = lList + ['Lethe']
							if len(lList) >= 3:
								sLeader = lList[CyGame().getSorenRandNum(len(lList), "Pick Leader")-1]
								if sLeader == 'Judecca':
									iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_JUDECCA')
									triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, iJudeccaData, -1, -1, -1, -1, -1)
								if sLeader == 'Sallos':
									if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VARN'):
										iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_SALLOS_MALE')
									else:
										iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_SALLOS_FEMALE')
									triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, -1, -1, -1, -1, -1, -1)
								if sLeader == 'Ouzza':
									iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_OUZZA')
									triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, -1, -1, -1, -1, -1, -1)
								if sLeader == 'Meresin':
									iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_MERESIN')
									triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, -1, -1, -1, -1, -1, -1)
								if sLeader == 'Statius':
									pCity = pPlayer.getCity(iStatiusData)
									iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_STATIUS')
									triggerData = pPlayer.initTriggeredData(iEvent, true, iStatiusData, pCity.getX(), pCity.getY(), -1, -1, -1, -1, -1, -1)
								if sLeader == 'Lethe':
									pUnit = pPlayer.getUnit(iLetheData)
									iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_LORD_OF_THE_BALORS_TEMPT_LETHE')
									triggerData = pPlayer.initTriggeredData(iEvent, true, -1, pUnit.getX(), pUnit.getY(), -1, -1, -1, -1, iLetheData, -1)

	def doTurnMulcarnReborn(self):
		if gc.getGame().getGameTurn() == 5:
			iPlayer = cf.getOpenPlayer()
			iTeam = 1
			bSpawned = False
			pPlot = CyMap().plot(68,18)
			pPlot.setMoveDisabledAI(False)
			pPlot.setMoveDisabledHuman(False)
			pPlot = CyMap().plot(58,38)
			pPlot.setMoveDisabledAI(False)
			pPlot.setMoveDisabledHuman(False)
			if CyGame().getTrophyValue("TROPHY_WB_CIV_DECIUS") == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DECIUS_MALAKIM_INTRO",())
				CyGame().addPlayerAdvanced(iPlayer, iTeam, gc.getInfoTypeForString('LEADER_DECIUS'), gc.getInfoTypeForString('CIVILIZATION_MALAKIM'),-1)
				gc.getPlayer(iPlayer).setAlignment(gc.getInfoTypeForString('ALIGNMENT_GOOD'))
				pPlot = CyMap().plot(68,18)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_SWORDSMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_SWORDSMAN'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				bSpawned = True
			if CyGame().getTrophyValue("TROPHY_WB_CIV_DECIUS") == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DECIUS_CALABIM_INTRO",())
				CyGame().addPlayerAdvanced(iPlayer, iTeam, gc.getInfoTypeForString('LEADER_DECIUS'), gc.getInfoTypeForString('CIVILIZATION_CALABIM'),-1)
				gc.getPlayer(iPlayer).setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_MOROI'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_MOROI'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				bSpawned = True
			if bSpawned:
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_HUNTER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_WORKER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString('UNIT_DECIUS'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit = gc.getPlayer(gc.getORC_PLAYER()).initUnit(gc.getInfoTypeForString('EQUIPMENT_CONTAINER'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_NETHER_BLADE'), True)
				self.addPopup(szText,'art/interface/popups/Decius.dds')
		gc.getGame().changeScenarioCounter(1)
		if gc.getGame().getScenarioCounter() == 40:
			gc.getGame().changeScenarioCounter(-40)
			if not gc.getGame().isNetworkMultiPlayer():
				for iPlayer in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.isAlive():
						if pPlayer.isHuman():
							iHumanPlayer = iPlayer
							pHumanPlayer = pPlayer
				iBestPlayer = -1
				for iLoopPlayer in range(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if pLoopPlayer.isAlive():
						if pHumanPlayer.getTeam() == pLoopPlayer.getTeam():
							if not pLoopPlayer.isHuman():
								if iBestPlayer == -1:
									iBestPlayer = iLoopPlayer
								else:
									if gc.getGame().getPlayerRank(iLoopPlayer) > gc.getGame().getPlayerRank(iBestPlayer):
										iBestPlayer = iLoopPlayer
				if iBestPlayer != -1:
					CyGame().reassignPlayerAdvanced(iHumanPlayer, iBestPlayer, -1)
					pPlayer = gc.getPlayer(iBestPlayer)
					szText = CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_SWITCH_CIV", ((gc.getCivilizationInfo(pPlayer.getCivilizationType()).getDescription(), )))
					addPlayerPopup(szText, iBestPlayer)

	def doTurnSplinteredCourt(self):
		if gc.getGame().getScenarioCounter() == 7:
			gc.getGame().changeScenarioCounter(-7)
		else:
			gc.getGame().changeScenarioCounter(1)

		iParith = gc.getGame().getTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH")
		if iParith > 1:
			for iPlayer in range(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iPlayer)
				if pLoopPlayer.isHuman():
					if gc.getTeam(pLoopPlayer.getTeam()).isHasTech(gc.getInfoTypeForString('TECH_SMELTING')):
						szText = CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_PARITH", ((gc.getUnitInfo(iParith).getDescription(), )))
						addPlayerPopup(szText, iPlayer)
						pCity = pLoopPlayer.getCapitalCity()
						newUnit = pLoopPlayer.initUnit(iParith, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						gc.getGame().setTrophyValue("TROPHY_WB_SPLINTERED_COURT_PARITH", 0)

		iCalabim = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
		iDoviello = gc.getInfoTypeForString('CIVILIZATION_DOVIELLO')
		iDuin = gc.getInfoTypeForString('UNIT_DUIN')
		iImmigrants = gc.getInfoTypeForString('EVENTTRIGGER_IMMIGRANTS')
		iLjosalfar = gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR')
		iStrong = gc.getInfoTypeForString('PROMOTION_STRONG')
		iSvartalfar = gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')
		iVampire = gc.getInfoTypeForString('PROMOTION_VAMPIRE')
		for iPlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isAlive():
				if pPlayer.getCivilizationType() == iCalabim:
					if gc.getGame().getScenarioCounter() == 0 or gc.getGame().getScenarioCounter() == 4:
						bState = False
						if gc.getGame().getScenarioCounter() == 4:
							bState = True
						py = PyPlayer(iPlayer)
						for pLoopUnit in py.getUnitList():
							if pLoopUnit.isHasPromotion(iVampire):
								pLoopUnit.setHasPromotion(iStrong, bState)
				if pPlayer.getCivilizationType() == iDoviello:
					if gc.getGame().getScenarioCounter() == 0:
						py = PyPlayer(iPlayer)
						lList = []
						for pLoopUnit in py.getUnitList():
							if pLoopUnit.getScenarioCounter() != -1:
								lList.append(pLoopUnit)
						for pLoopUnit in lList:
							newUnit = pPlayer.initUnit(pLoopUnit.getScenarioCounter(), pLoopUnit.getX(), pLoopUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							newUnit.convert(pLoopUnit)
							newUnit.setScenarioCounter(-1)
					if gc.getGame().getScenarioCounter() == 4:
						py = PyPlayer(iPlayer)
						lList = []
						for pLoopUnit in py.getUnitList():
							if not pLoopUnit.isOnlyDefensive():
								if pLoopUnit.getUnitType() != iDuin:
									if pLoopUnit.isAlive():
										lList.append(pLoopUnit)
				if pPlayer.getCivilizationType() == iLjosalfar or pPlayer.getCivilizationType() == iSvartalfar:
					if gc.getGame().getScenarioCounter() == 0:
						if CyGame().getSorenRandNum(100, "Immigrants") < 10:
							lList = []
							for pyCity in PyPlayer(iPlayer).getCityList():
								pCity = pyCity.GetCy()
								lList.append(pCity)
							if len(lList) > 0:
								pCity = lList[CyGame().getSorenRandNum(len(lList), "Pick City")-1]
								triggerData = pPlayer.initTriggeredData(iImmigrants, true, -1, pCity.getX(), pCity.getY(), iPlayer, pCity.getID(), -1, -1, -1, -1)

	def doTurnTheBlackTower(self):
		bSanctuary = False
		if gc.getPlayer(2).isAlive():
			bSanctuary = True
		if gc.getPlayer(3).isAlive():
			bSanctuary = True
		if gc.getPlayer(4).isAlive():
			bSanctuary = True
		if bSanctuary:
			gc.getPlayer(1).changeSanctuaryTimer(1)
		iPlayer = 0 #Falamar
		pPlayer = gc.getPlayer(iPlayer)
		lTechs = ['TECH_FANATICISM', 'TECH_WARHORSES', 'TECH_IRON_WORKING', 'TECH_CONSTRUCTION', 'TECH_ARCHERY', 'TECH_POISONS']
		lUnits = ['UNIT_DONAL', 'UNIT_MAGNADINE', 'UNIT_GUYBRUSH', 'UNIT_BARNAXUS', 'UNIT_GILDEN', 'UNIT_ALAZKAN']
		lCivs = ['CIVILIZATION_BANNOR', 'CIVILIZATION_HIPPUS', 'CIVILIZATION_LANUN', 'CIVILIZATION_LUCHUIRP', 'CIVILIZATION_LJOSALFAR', 'CIVILIZATION_SVARTALFAR']
		for i in range(len(lUnits)):
			iUnit = gc.getInfoTypeForString(lUnits[i])
			if CyGame().getUnitCreatedCount(iUnit) == 0:
				if gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString(lTechs[i])):
					bValid = True
					for pyCity in PyPlayer(iPlayer).getCityList():
						pCity = pyCity.GetCy()
						if (bValid and pCity.getCivilizationType() == gc.getInfoTypeForString(lCivs[i])):
							pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
							CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_WB_THE_BLACK_TOWER_HERO",()),'',1,gc.getUnitInfo(iUnit).getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
							bValid = False
		cf.doTurnLuchuirp(iPlayer)

	def doTurnTheMomus(self):
		if not gc.getTeam(0).isAtWar(1): #if Falamar isnt at war with Perpentach
			gc.getGame().changeScenarioCounter(1)
			if gc.getGame().getScenarioCounter() == 20:
				gc.getGame().changeScenarioCounter(-20)
				iBestPlayer = -1
				iPerpentach = gc.getInfoTypeForString('LEADER_PERPENTACH')
				iRnd = CyGame().getSorenRandNum(100, "The Momus")
				if iRnd < 30:
					for iLoopTeam in range(gc.getMAX_TEAMS()):
						pTeam = gc.getTeam(iLoopTeam)
						if pTeam.isAlive():
							if iLoopTeam != 1: #Perpentach
								for iLoopTeam2 in range(gc.getMAX_TEAMS()):
									eTeam2 = gc.getTeam(iLoopTeam2)
									if eTeam2.isAlive():
										if iLoopTeam2 != 1: # Perpentach
											if iLoopTeam != iLoopTeam2:
												pTeam.setPermanentWarPeace(iLoopTeam2, False)
												pTeam.declareWar(iLoopTeam2, false, WarPlanTypes.WARPLAN_TOTAL)
												pTeam.setPermanentWarPeace(iLoopTeam2, True)
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_ALL_WAR",()),'art/interface/popups/Perpentach.dds')
				if iRnd >= 30 and iRnd < 70:
					iBestRank = 100
					for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if not pLoopPlayer.isBarbarian():
								if pLoopPlayer.getLeaderType() != iPerpentach:
									if gc.getGame().getPlayerRank(iLoopPlayer) < iBestRank:
										iBestPlayer = iLoopPlayer
										iBestRank = gc.getGame().getPlayerRank(iLoopPlayer)
				if iRnd >= 70:
					lList = []
					for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if not pLoopPlayer.isBarbarian():
								if pLoopPlayer.getLeaderType() != iPerpentach:
									lList.append(iLoopPlayer)
					if len(lList) >= 1:
						iBestPlayer = lList[CyGame().getSorenRandNum(len(lList), "The Momus")-1]
				if iBestPlayer != -1:
					iBestTeam = gc.getPlayer(iBestPlayer).getTeam()
					for iLoopTeam in range(gc.getMAX_TEAMS()):
						pTeam = gc.getTeam(iLoopTeam)
						if pTeam.isAlive():
							if iLoopTeam != iBestTeam:
								if not pTeam.isBarbarian():
									if iLoopTeam != 1: #Perpentach
										for iLoopTeam2 in range(gc.getMAX_TEAMS()):
											eTeam2 = gc.getTeam(iLoopTeam2)
											if eTeam2.isAlive():
												if not eTeam2.isBarbarian():
													if iLoopTeam2 != 1: # Perpentach
														if iLoopTeam != iLoopTeam2:
															pTeam.setPermanentWarPeace(iLoopTeam2, False)
															if iLoopTeam2 == iBestTeam:
																pTeam.declareWar(iLoopTeam2, false, WarPlanTypes.WARPLAN_TOTAL)
															else:
																pTeam.makePeace(iLoopTeam2)
															pTeam.setPermanentWarPeace(iLoopTeam2, True)
					pPlayer = gc.getPlayer(iBestPlayer)
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FALAMAR'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_FALAMAR",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MAHON'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_MAHON",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SALLOS'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_SALLOS",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BEERI'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_BEERI",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_ULDANOR'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_ULDANOR",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TYA'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_TYA",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_WEEVIL'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_WEEVIL",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FURIA'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_FURIA",()),'art/interface/popups/Perpentach.dds')
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MELISANDRE'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DOGPILE_MELISANDRE",()),'art/interface/popups/Perpentach.dds')

	def doTurnTheRadiantGuard(self):
		if CyGame().getGameTurn() == 10:
			self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_CAPRIA",()),'art/interface/popups/Capria.dds')
		if CyGame().getGameTurn() == 40:
			pPlot = CyMap().plot(29,3)
			if pPlot.isCity():
				if pPlot.getOwner() == 2: #Hyborem
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_CAPRIA_2",()),'art/interface/popups/Capria.dds')
		if CyGame().getGameTurn() == 50:
			pPlot = CyMap().plot(29,3)
			if pPlot.isCity():
				if pPlot.getOwner() == 2: #Hyborem
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_CAPRIA_3",()),'art/interface/popups/Capria.dds')
		if CyGame().getGameTurn() == 60:
			pPlot = CyMap().plot(29,3)
			if pPlot.isCity():
				if pPlot.getOwner() == 2: #Hyborem
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_CAPRIA_LOST",()),'art/interface/popups/Capria.dds')
					gc.getPlayer(3).setAlive(false) #Capria
		iPlayer = 2 #Hyborem
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			for pyCity in PyPlayer(iPlayer).getCityList():
				pCity = pyCity.GetCy()
				iCounter = 160 - gc.getGame().getScenarioCounter()
				if iCounter == 160:
					iCounter = 125
				iRnd = CyGame().getSorenRandNum(iCounter, "doTurnTheRadiantGuard")
				iProm = -1
				iUnit = -1
				iNum = 1
				if iRnd > 20 and iRnd <= 25:
					iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
					iProm = gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
					iNum = 2
				if iRnd > 25 and iRnd <= 30:
					iUnit = gc.getInfoTypeForString('UNIT_SPECTRE')
				if iRnd > 30 and iRnd <= 35:
					iUnit = gc.getInfoTypeForString('UNIT_HORSEMAN')
				if iRnd > 35 and iRnd <= 40:
					iUnit = gc.getInfoTypeForString('UNIT_HORSEMAN')
					iNum = 2
				if iRnd > 40 and iRnd <= 45:
					iUnit = gc.getInfoTypeForString('UNIT_HELLHOUND')
				if iRnd > 45 and iRnd <= 50:
					iUnit = gc.getInfoTypeForString('UNIT_HELLHOUND')
					iNum = 2
				if iRnd > 50 and iRnd <= 55:
					iUnit = gc.getInfoTypeForString('UNIT_PIT_BEAST')
				if iRnd > 55 and iRnd <= 60:
					iUnit = gc.getInfoTypeForString('UNIT_PIT_BEAST')
					iNum = 2
				if iRnd > 60 and iRnd <= 65:
					iUnit = gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_VEIL')
				if iRnd > 65 and iRnd <= 70:
					iUnit = gc.getInfoTypeForString('UNIT_IRA')
				if iRnd > 70 and iRnd <= 75:
					iUnit = gc.getInfoTypeForString('UNIT_IRA')
					iNum = 2
				if iRnd > 75 and iRnd <= 80:
					iUnit = gc.getInfoTypeForString('UNIT_CHAMPION')
				if iRnd > 80 and iRnd <= 85:
					iUnit = gc.getInfoTypeForString('UNIT_BEAST_OF_AGARES')
				if iRnd > 85 and iRnd <= 90:
					iUnit = gc.getInfoTypeForString('UNIT_RANGER')
				if iRnd > 90 and iRnd <= 95:
					iUnit = gc.getInfoTypeForString('UNIT_HORSE_ARCHER')
				if iRnd > 95 and iRnd <= 100:
					iUnit = gc.getInfoTypeForString('UNIT_MANTICORE')
				if iRnd > 100 and iRnd <= 105:
					iUnit = gc.getInfoTypeForString('UNIT_HIGH_PRIEST_OF_THE_VEIL')
				if iRnd > 105 and iRnd <= 110:
					iUnit = gc.getInfoTypeForString('UNIT_IMMORTAL')
					iProm = gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
				if iRnd > 110 and iRnd <= 115:
					iUnit = gc.getInfoTypeForString('UNIT_EIDOLON')
					iProm = gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
				if iRnd > 115 and iRnd <= 120:
					iUnit = gc.getInfoTypeForString('UNIT_LICH')
					iProm = gc.getInfoTypeForString('PROMOTION_DEATH1')
				if iRnd > 120:
					iUnit = gc.getInfoTypeForString('UNIT_BALOR')
					iProm = gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
				if iRnd > 140:
					iNum = 2
				if iUnit != -1:
					for i in range (iNum):
						newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK_CITY_LEMMING, DirectionTypes.DIRECTION_SOUTH)
						newUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, 5, 13, 0, False, False, MissionAITypes.NO_MISSIONAI, newUnit.plot(), newUnit)
						if iProm != -1:
							newUnit.setHasPromotion(iProm, True)
							if iProm == gc.getInfoTypeForString('PROMOTION_DEATH1'):
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH2'), True)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH3'), True)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EXTENSION1'), True)
								newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_EXTENSION2'), True)

	def gameStart(self):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LOAD_SCREEN):
			CvEspionageAdvisor.CvEspionageAdvisor().interfaceScreen()

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_GREY):
			CvUtil.pyPrint("Starting the scenario")
			pPlayer = gc.getPlayer(0)
			if pPlayer.isHuman():
				gc.getPlayer(0).setAlignment(gc.getInfoTypeForString('ALIGNMENT_GOOD'))
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_GREY_INTRO_MALAKIM",()), 'art/interface/popups/Against the Grey.dds')
			else:
				gc.getPlayer(1).setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_GREY_INTRO_CALABIM",()), 'art/interface/popups/Against the Grey.dds')

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_WALL):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_WALL_INTRO",()), 'art/interface/popups/Against the Wall.dds')
			if CyGame().isHasTrophy("TROPHY_WB_BARBARIAN_ASSAULT"):
				gc.getPlayer(4).setAlive(false)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_INTRO",()), 'art/interface/popups/Barbarian Assault.dds')
			gc.getTeam(0).setPermanentWarPeace(3, True)
			gc.getTeam(1).setPermanentWarPeace(3, True)
			gc.getTeam(2).setPermanentWarPeace(3, True)
			gc.getTeam(5).setPermanentWarPeace(3, True)
			gc.getTeam(6).setPermanentWarPeace(3, True)
			gc.getTeam(7).setPermanentWarPeace(3, True)
			gc.getTeam(3).setPermanentWarPeace(0, True)
			gc.getTeam(3).setPermanentWarPeace(1, True)
			gc.getTeam(3).setPermanentWarPeace(2, True)
			gc.getTeam(3).setPermanentWarPeace(5, True)
			gc.getTeam(3).setPermanentWarPeace(6, True)
			gc.getTeam(3).setPermanentWarPeace(7, True)
			iForest = gc.getInfoTypeForString('FEATURE_FOREST')
			iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
			for iPlayer in range(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
						pPlot = pPlayer.getStartingPlot()
						iX = pPlot.getX()
						iY = pPlot.getY()
						for iiX in range(iX-1, iX+2, 1):
							for iiY in range(iY-1, iY+2, 1):
								pLoopPlot = CyMap().plot(iiX,iiY)
								if not pLoopPlot.isNone():
									iFeature = pLoopPlot.getFeatureType()
									if (iFeature == iForest or iFeature == iJungle):
										pLoopPlot.setFeatureType(-1, -1)
						iUnit = -1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_AMURITES'):
							iUnit = gc.getInfoTypeForString('UNIT_ADEPT')
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_BANNOR'):
							iUnit = gc.getInfoTypeForString('UNIT_AXEMAN')
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_HIPPUS'):
							iUnit = gc.getInfoTypeForString('UNIT_HORSEMAN')
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
							iUnit = gc.getInfoTypeForString('UNIT_ARCHER')
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
							iUnit = gc.getInfoTypeForString('UNIT_WOOD_GOLEM')
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
							iUnit = gc.getInfoTypeForString('UNIT_ARCHER')
						if iUnit != -1:
							pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_INTRO",()), 'art/interface/popups/Beneath the Heel.dds')
			gc.getPlayer(1).changeDisableProduction(1000)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_INTRO",()), 'art/interface/popups/Blood of Angels.dds')
			iXP = gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP")
			if iXP > 0:
				if iXP > 10:
					iXP = 10
				iPlayer = 0 #Mahala
				self.giftHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'), iXP)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_INTRO",()), 'art/interface/popups/Fall of Cuantine.dds')
			gc.getGame().incrementUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_VALIN'))
			gc.getGame().setReligionSlotTaken(gc.getInfoTypeForString('RELIGION_THE_ORDER'), True)
			gc.getGame().setReligionSlotTaken(gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'), True)
			pPlot = CyMap().plot(16,1)
			pPlot.setMoveDisabledHuman(True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_INTRO",()), 'art/interface/popups/Gift of Kylorin.dds')
			pPlot = CyMap().plot(21,16)
			pPlot.setMoveDisabledAI(True)
			pPlot = CyMap().plot(29,18)
			pPlot.setMoveDisabledAI(True)
			pPlot = CyMap().plot(37,16)
			pPlot.setMoveDisabledAI(True)
			pPlot = CyMap().plot(28,1)
			pPlot.setMoveDisabledAI(True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_INTRO",()), 'art/interface/popups/Grand Menagerie.dds')
			pPlot = CyMap().plot(21,16)
			pPlot.setMoveDisabledAI(True)
			pPlot = CyMap().plot(27,15)
			pPlot.setMoveDisabledAI(True)
			pPlot = CyMap().plot(27,16)
			pPlot.setMoveDisabledAI(True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			pPlayer = gc.getPlayer(0)
			if pPlayer.isHuman():
				pPlayer.setAlignment(gc.getInfoTypeForString('ALIGNMENT_GOOD'))
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_INTRO",()), 'art/interface/popups/Into the Desert.dds')
			else:
				gc.getPlayer(1).setAlignment(gc.getInfoTypeForString('ALIGNMENT_EVIL'))
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_INTRO",()), 'art/interface/popups/Into the Desert Calabim.dds')
				gc.getPlayer(3).setFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL, True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			gc.getGame().incrementUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_DONAL'))
			gc.getTeam(0).setPermanentWarPeace(5, True)
			gc.getTeam(0).setPermanentWarPeace(6, True)
			gc.getTeam(0).setPermanentWarPeace(7, True)
			gc.getTeam(0).setPermanentWarPeace(8, True)
			gc.getTeam(0).setPermanentWarPeace(9, True)
			gc.getTeam(0).setPermanentWarPeace(10, True)
			gc.getTeam(0).setPermanentWarPeace(11, True)
			gc.getTeam(1).setPermanentWarPeace(5, True)
			gc.getTeam(1).setPermanentWarPeace(6, True)
			gc.getTeam(1).setPermanentWarPeace(7, True)
			gc.getTeam(1).setPermanentWarPeace(8, True)
			gc.getTeam(1).setPermanentWarPeace(9, True)
			gc.getTeam(1).setPermanentWarPeace(10, True)
			gc.getTeam(1).setPermanentWarPeace(11, True)
			gc.getTeam(2).setPermanentWarPeace(5, True)
			gc.getTeam(4).setPermanentWarPeace(5, True)
			gc.getTeam(4).setPermanentWarPeace(6, True)
			gc.getTeam(4).setPermanentWarPeace(7, True)
			gc.getTeam(4).setPermanentWarPeace(8, True)
			gc.getTeam(4).setPermanentWarPeace(9, True)
			gc.getTeam(4).setPermanentWarPeace(10, True)
			gc.getTeam(4).setPermanentWarPeace(11, True)
			iCount = 0
			for iPlayer in range(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					if pPlayer.isHuman():
						iCount += 1
						pHumanPlayer = pPlayer
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
						pPlot = pPlayer.getStartingPlot()
						if pPlot.getX() <= 51 and pPlot.getY() <= 14:
							pNewPlot = CyMap().plot(29,28)
							pPlayer.setStartingPlot(pNewPlot, True)
							for i in range(pPlot.getNumUnits(), -1, -1):
								pUnit = pPlot.getUnit(i)
								pUnit.setXY(pNewPlot.getX(), pNewPlot.getY(), True, True, True,False)
			if iCount == 1:
				if pHumanPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BASIUM'):
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_INTRO_BASIUM",()), 'art/interface/popups/Lord of the Balors.dds')
				if pHumanPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CAPRIA'):
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_INTRO_CAPRIA",()), 'art/interface/popups/Lord of the Balors.dds')
				if pHumanPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_INTRO_KEELYN",()), 'art/interface/popups/Lord of the Balors.dds')
				if pHumanPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VARN'):
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_INTRO_VARN",()), 'art/interface/popups/Lord of the Balors.dds')
			iBarrow = gc.getInfoTypeForString('IMPROVEMENT_BARROW')
			iBrokenLands = gc.getInfoTypeForString('TERRAIN_BROKEN_LANDS')
			iDemon = gc.getInfoTypeForString('PROMOTION_DEMON')
			iDungeon = gc.getInfoTypeForString('IMPROVEMENT_DUNGEON')
			iFieldsOfPerdition = gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION')
			iNecrototem = gc.getInfoTypeForString('IMPROVEMENT_NECROTOTEM')
			iScout = gc.getInfoTypeForString('UNIT_SCOUT')
			iShallows = gc.getInfoTypeForString('TERRAIN_SHALLOWS')
			iSkeleton = gc.getInfoTypeForString('UNIT_SKELETON')
			iTower = gc.getInfoTypeForString('IMPROVEMENT_TOWER')
			iWarrior = gc.getInfoTypeForString('UNIT_WARRIOR')
			bPlayer = gc.getPlayer(gc.getORC_PLAYER())
			for i in range (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				iTerrain = pPlot.getTerrainType()
				if (iTerrain == iBrokenLands or iTerrain == iFieldsOfPerdition or iTerrain == iShallows):
					if not pPlot.isPeak():
						iImprovement = pPlot.getImprovementType()
						if iImprovement == -1:
							if gc.getGame().getSorenRandNum(10000, "Necrototem") < 90:
								pPlot.setImprovementType(iNecrototem)
						else:
							if iImprovement == iBarrow:
								newUnit = bPlayer.initUnit(iSkeleton, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							if iImprovement == iDungeon:
								newUnit = bPlayer.initUnit(iWarrior, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.setHasPromotion(iDemon, True)
							if iImprovement == iTower:
								newUnit = bPlayer.initUnit(iScout, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.setHasPromotion(iDemon, True)
			if CyGame().isHasTrophy("TROPHY_WB_BARBARIAN_ASSAULT"):
				gc.getGame().setOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS, True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_INTRO",()), 'art/interface/popups/Mulcarn Reborn.dds')
			if CyGame().getTrophyValue("TROPHY_WB_CIV_AMELANCHIER") != gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				gc.getPlayer(5).setAlive(false)
			if CyGame().getTrophyValue("TROPHY_WB_CIV_VOLANNA") != gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				gc.getPlayer(6).setAlive(false)
			pPlot = CyMap().plot(68,18)
			pPlot.setMoveDisabledAI(True)
			pPlot.setMoveDisabledHuman(True)
			pPlot = CyMap().plot(58,38)
			pPlot.setMoveDisabledAI(True)
			pPlot.setMoveDisabledHuman(True)
			gc.getGame().incrementProjectCreatedCount(gc.getInfoTypeForString('PROJECT_STIR_FROM_SLUMBER'))
			gc.getGame().incrementProjectCreatedCount(gc.getInfoTypeForString('PROJECT_THE_WHITE_HAND'))
			gc.getTeam(0).setPermanentWarPeace(1, True)
			gc.getTeam(1).setPermanentWarPeace(0, True)
			gc.getPlayer(1).setFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL, True) #Dumannious
			gc.getPlayer(2).setFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL, True) #Riuros
			gc.getPlayer(3).setFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL, True) #Anagantios
			iXP = gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP")
			if iXP > 0:
				iPlayer = 4 #Mahala
				self.giftHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'), iXP)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_INTRO",()), 'art/interface/popups/Return of Winter.dds')

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_BLACK_TOWER_INTRO",()), 'art/interface/popups/The Black Tower.dds')
			gc.getPlayer(0).setHasTrait(gc.getInfoTypeForString('TRAIT_TOLERANT'), True,-1,True,True)
			if CyGame().isHasTrophy("TROPHY_WB_BARBARIAN_ASSAULT"):
				gc.getPlayer(6).setAlive(false)
			if CyGame().isHasTrophy("TROPHY_WB_LORD_OF_THE_BALORS"):
				gc.getPlayer(5).setAlive(false)
			if gc.getGame().getHandicapType() > 3:
				for iLoopPlayer in range(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if pLoopPlayer.isAlive():
						if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
							pCity = pLoopPlayer.getCapitalCity()
							pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
							if gc.getGame().getHandicapType() > 4:
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_WORKER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_WORKER, DirectionTypes.DIRECTION_SOUTH)
							if gc.getGame().getHandicapType() > 5:
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_PYRE_ZOMBIE'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
							if gc.getGame().getHandicapType() > 6:
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_CITY_DEFENSE, DirectionTypes.DIRECTION_SOUTH)
							if gc.getGame().getHandicapType() > 7:
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_SETTLE, DirectionTypes.DIRECTION_SOUTH)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_CULT):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_CULT_INTRO",()), 'art/interface/popups/The Cult.dds')
			pPlot = CyMap().plot(21,15)
			pPlot.setPortalExitX(45)
			pPlot.setPortalExitY(1)
			pPlot = CyMap().plot(45,1)
			pPlot.setPortalExitX(21)
			pPlot.setPortalExitY(15)
			pPlot = CyMap().plot(21,18)
			pPlot.setPortalExitX(42)
			pPlot.setPortalExitY(30)
			pPlot = CyMap().plot(42,30)
			pPlot.setPortalExitX(21)
			pPlot.setPortalExitY(18)
			iGoodyHut = gc.getInfoTypeForString('IMPROVEMENT_GOODY_HUT')
			for i in range (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.getX() >= 37:
					pPlot.setBuildDisabled(True)
					pPlot.setFoundDisabled(True)
					pPlot.setBonusType(-1)
					if pPlot.getImprovementType() == iGoodyHut:
						pPlot.setImprovementType(-1)
			for iY in range(18, 31, 1):
				pPlot = CyMap().plot(21,iY)
				pPlot.setMoveDisabledAI(True)
			bPlayer = gc.getPlayer(gc.getORC_PLAYER())
			if not CyGame().isHasTrophy("TROPHY_WB_BARBARIAN_ASSAULT"):
				newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), 40, 8, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS'), True)
				newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), 40, 8, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ORC'), True)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS'), True)
			if not CyGame().isHasTrophy("TROPHY_WB_LORD_OF_THE_BALORS"):
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_BALOR'), 43, 28, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				bPlayer.initUnit(gc.getInfoTypeForString('UNIT_BALOR'), 43, 28, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			iXP = gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP")
			if iXP > 0:
				if iXP > 25:
					iXP = 25
				iPlayer = 1 #Mahala
				self.giftHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'), iXP)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_INTRO",()), 'art/interface/popups/The Momus.dds')
			gc.getGame().incrementUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_BARNAXUS'))
			gc.getGame().incrementUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_HYBOREM'))
			gc.getGame().incrementUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_LOKI'))
			for iLoopTeam in range(gc.getMAX_TEAMS()):
				pTeam = gc.getTeam(iLoopTeam)
				if pTeam.isAlive():
					for iLoopTeam2 in range(gc.getMAX_TEAMS()):
						eTeam2 = gc.getTeam(iLoopTeam2)
						if eTeam2.isAlive():
							if iLoopTeam != iLoopTeam2:
								pTeam.setPermanentWarPeace(iLoopTeam2, True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_INTRO",()), 'art/interface/popups/The Radiant Guard.dds')
			gc.getGame().changeScenarioCounter(100)
			for i in range (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if pPlot.getX() <= 9:
					if not pPlot.isWater():
						pPlot.setMoveDisabledHuman(True)
			for iLoopTeam in range(gc.getMAX_TEAMS()):
				pTeam = gc.getTeam(iLoopTeam)
				if pTeam.isAlive():
					for iLoopTeam2 in range(gc.getMAX_TEAMS()):
						eTeam2 = gc.getTeam(iLoopTeam2)
						if eTeam2.isAlive():
							if iLoopTeam != iLoopTeam2:
								pTeam.setPermanentWarPeace(iLoopTeam2, True)
			pPlot = CyMap().plot(75,47)
			pPlot.setMoveDisabledHuman(True)
			iPlayer = 0 #Falamar
			pPlayer = gc.getPlayer(iPlayer)
			if gc.getGame().getHandicapType() < 5:
				pPlot = CyMap().plot(16,7)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RADIANT_GUARD'), pPlot.getX(),  pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			if gc.getGame().getHandicapType() < 4:
				pPlot = CyMap().plot(16,23)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RADIANT_GUARD'), pPlot.getX(),  pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			if gc.getGame().getHandicapType() < 3:
				pPlot = CyMap().plot(18,16)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RADIANT_GUARD'), pPlot.getX(),  pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			if gc.getGame().getHandicapType() < 2:
				pPlot = CyMap().plot(16,9)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RATHA'), pPlot.getX(),  pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			if gc.getGame().getHandicapType() < 1:
				pPlot = CyMap().plot(16,29)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RATHA'), pPlot.getX(),  pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			gc.getGame().incrementUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_LUCIAN'))
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_INTRO",()), 'art/interface/popups/The Splintered Court.dds')
			gc.getTeam(0).setPermanentWarPeace(1, True)
			gc.getTeam(1).setPermanentWarPeace(0, True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
			iCount = 0
			for iPlayer in range(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isAlive():
					if pPlayer.isHuman():
						iCount += 1
						pHumanPlayer = pPlayer
			if iCount == 1:
				if pHumanPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_MALAKIM",())
				if pHumanPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_ELOHIM",())
				if pHumanPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_SHEAIM",())
				if pHumanPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
					szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_INTRO_CALABIM",())
				self.addPopupWB(szText, 'art/interface/popups/Wages of Sin.dds')

	def getGoalTag(self, pPlayer):
		szBuffer = u"<font=2>"
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_WALL):
			if gc.getGame().getScenarioCounter() == 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_AGAINST_THE_WALL_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			else:
				iCount = 100 - gc.getGame().getScenarioCounter()
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_AGAINST_THE_WALL_GOAL_2", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_BARBARIAN_ASSAULT_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_BENEATH_THE_HEEL_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
			if gc.getGame().getScenarioCounter() == 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_BLOOD_OF_ANGELS_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			else:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_BLOOD_OF_ANGELS_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if gc.getGame().getScenarioCounter() == 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_0", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 1:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 2:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 3:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_3", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 4:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_4", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 5:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_FALL_OF_CUANTINE_GOAL_5", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GIFT_OF_KYLORIN_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			if gc.getGame().getScenarioCounter() == 2:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_GRIFFON", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 1:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_ELEPHANT", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 0:
				iPlayer = 0 #Falamar
				iSubdueAnimal = gc.getInfoTypeForString('PROMOTION_SUBDUE_ANIMAL')
				bHunter = False
				py = PyPlayer(iPlayer)
				for pLoopUnit in py.getUnitList():
					if pLoopUnit.isHasPromotion(iSubdueAnimal):
						bHunter = True
				if not bHunter:
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_HUNTER", (), gc.getInfoTypeForString("COLOR_RED"))
				else:
					pCity = gc.getPlayer(iPlayer).getCapitalCity()
					iCount = 5
					bBear = True
					bLion = True
					bGorilla = True
					bTiger = True
					bWolf = True
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_DANCING_BEAR')) > 0:
						iCount -= 1
						bBear = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_LION_CAGE')) > 0:
						iCount -= 1
						bLion = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_GORILLA_CAGE')) > 0:
						iCount -= 1
						bGorilla = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_TIGER_CAGE')) > 0:
						iCount -= 1
						bTiger = False
					if pCity.getNumRealBuilding(gc.getInfoTypeForString('BUILDING_WOLF_CAGE')) > 0:
						iCount -= 1
						bWolf = False
					if iCount > 1:
						szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))
					if iCount == 1:
						if bBear:
							szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_BEAR", (), gc.getInfoTypeForString("COLOR_RED"))
						if bLion:
							szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_LION", (), gc.getInfoTypeForString("COLOR_RED"))
						if bGorilla:
							szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_GORILLA", (), gc.getInfoTypeForString("COLOR_RED"))
						if bTiger:
							szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_TIGER", (), gc.getInfoTypeForString("COLOR_RED"))
						if bWolf:
							szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_GRAND_MENAGERIE_GOAL_WOLF", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			pPlayer = gc.getPlayer(0)
			if pPlayer.isHuman():
				if gc.getGame().getScenarioCounter() == 0:
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_GOAL_0", (), gc.getInfoTypeForString("COLOR_RED"))
				if gc.getGame().getScenarioCounter() > 100:
					iCount = gc.getGame().getScenarioCounter() - 100
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_GOAL_1", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))
				if gc.getGame().getScenarioCounter() == 99:
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))
			else:
				if gc.getGame().getScenarioCounter() == 0:
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_GOAL_0", (), gc.getInfoTypeForString("COLOR_RED"))
				if gc.getGame().getScenarioCounter() > 1:
					iCount = gc.getGame().getScenarioCounter()
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_GOAL_1", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))
				if gc.getGame().getScenarioCounter() == 1:
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			iCount = 0
			iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
			for iLoopPlayer in range(gc.getMAX_PLAYERS()):
				pLoopPlayer = gc.getPlayer(iLoopPlayer)
				if pLoopPlayer.isAlive():
					if pLoopPlayer.getCivilizationType() == iInfernal:
						iCount += 1
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_LORD_OF_THE_BALORS_GOAL", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			iCount = 40 - gc.getGame().getScenarioCounter()
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_MULCARN_REBORN_GOAL", ((iCount, )), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_RETURN_OF_WINTER_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			bSanctuary = False
			if gc.getPlayer(2).isAlive():
				bSanctuary = True
			if gc.getPlayer(3).isAlive():
				bSanctuary = True
			if gc.getPlayer(4).isAlive():
				bSanctuary = True
			if bSanctuary:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_BLACK_TOWER_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			else:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_BLACK_TOWER_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_CULT):
			if gc.getGame().getScenarioCounter() == 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_CULT_GOAL_1", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 1:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_CULT_GOAL_2", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 2:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_CULT_GOAL_3", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_MOMUS_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_SPLINTERED_COURT_LJOSALFAR_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_SPLINTERED_COURT_SVARTALFAR_GOAL", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_DAWN", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 1:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_MORNING", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 2:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_NOON", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 3:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_AFTERNOON", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 4:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_DUSK", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 5:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_EARLY_NIGHT", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 6:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_MIDNIGHT", (), gc.getInfoTypeForString("COLOR_RED"))
			if gc.getGame().getScenarioCounter() == 7:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_MESSAGE_DAY_CYCLE_LATE_NIGHT", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			if gc.getGame().getScenarioCounter() > 0:
				szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_RADIANT_GUARD_GOAL", ((gc.getGame().getScenarioCounter(), )), gc.getInfoTypeForString("COLOR_RED"))
			else:
				if gc.getTeam(0).isAtWar(1):
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_RADIANT_GUARD_GOAL_DEFEAT_BASIUM", (), gc.getInfoTypeForString("COLOR_RED"))
				if gc.getTeam(0).isAtWar(2):
					szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_THE_RADIANT_GUARD_GOAL_DEFEAT_HYBOREM", (), gc.getInfoTypeForString("COLOR_RED"))

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
			iCount = 0
			if (pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM') or pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM')):
				for iPlayer in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.isAlive():
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
							iCount += 1
			if (pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM') or pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM')):
				for iPlayer in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.isAlive():
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MERCURIANS'):
							iCount += 1
						if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
							iCount += 1
			szBuffer = szBuffer + CyTranslator().getColorText("TXT_KEY_WB_WAGES_OF_SIN_GOAL", ((iCount - 1, )), gc.getInfoTypeForString("COLOR_RED"))

		szBuffer = szBuffer + "</font>"
		return szBuffer

	def getHeroXP(self, iPlayer, iUnit):
		apUnitList = PyPlayer(iPlayer).getUnitList()
		iXP = -1
		for pLoopUnit in apUnitList:
			if pLoopUnit.getUnitType() == iUnit:
				if pLoopUnit.getExperienceTimes100() > iXP:
					iXP = pLoopUnit.getExperienceTimes100()
		return iXP

	def giftHeroXP(self, iPlayer, iUnit, iXP):
		apUnitList = PyPlayer(iPlayer).getUnitList()
		for pLoopUnit in apUnitList:
			if pLoopUnit.getUnitType() == iUnit:
				pLoopUnit.changeExperienceTimes100(iXP, -1, False, False, False)

	def onCityAcquired(self, iPreviousOwner, iNewOwner, pCity, bConquest, bTrade):
		pPlayer = gc.getPlayer(iNewOwner)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
			if pPlayer.isHuman():
				if gc.getPlayer(iPreviousOwner).getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
					iUnit = gc.getInfoTypeForString('UNIT_GURID')
					if CyGame().getUnitCreatedCount(iUnit) == 0:
						cf.addUnit(iUnit)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
			if pPlayer.getTeam() == 0:
				if pCity.getName() == "Torrolerial":
					self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_TORROLERIAL",()), 'art/interface/popups/Blood of Angels Torrolerial.dds')
					gc.getGame().changeScenarioCounter(1)
					gc.getTeam(0).setPermanentWarPeace(2, False)
					gc.getTeam(0).setPermanentWarPeace(3, False)
					pTeam = gc.getTeam(0) #Doviello & Illians
					pTeam.meet(2, False)
					pTeam.meet(3, False)
					pTeam.declareWar(2, false, WarPlanTypes.WARPLAN_TOTAL)
					pTeam.declareWar(3, false, WarPlanTypes.WARPLAN_TOTAL)
					gc.getTeam(0).setPermanentWarPeace(2, True)
					gc.getTeam(0).setPermanentWarPeace(3, True)
				if pCity.getName() == "Midgar":
					gc.getGame().setWinner(0, 2)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			if pPlayer.isHuman():
				iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_THE_BLACK_TOWER_PICK_CIV')
				triggerData = pPlayer.initTriggeredData(iEvent, true, -1, pCity.getX(), pCity.getY(), iNewOwner, pCity.getID(), -1, -1, -1, -1)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			if pPlayer.isHuman():
				if pCity.getName() == "Bastradam":
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_CAPRIA_WON",()),'art/interface/popups/Capria.dds')
					gc.getGame().changeTrophyValue("TROPHY_WB_THE_RADIANT_GUARD_CAPRIA_ALLY", 1)
					pPlayer = gc.getPlayer(0) #Falamar
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(),  pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(),  pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(),  pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER'), pCity.getX(),  pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					gc.getPlayer(3).setAlive(False) #Capria

	def onCityBuilt(self, pCity):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			if pPlayer.isHuman():
				iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_THE_BLACK_TOWER_PICK_CIV')
				triggerData = pPlayer.initTriggeredData(iEvent, true, -1, pCity.getX(), pCity.getY(), iPlayer, pCity.getID(), -1, -1, -1, -1)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			if pPlayer.getNumCities() == 1:
				pCity.setPopulation(3)

	def onCityRazed(self, city, iPlayer):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if city.isHolyCityByType(gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS')):
				if gc.getGame().getScenarioCounter() == 4:
					gc.getGame().changeScenarioCounter(1)
				addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_MASK",()), iPlayer)
				bPlayer = gc.getPlayer(gc.getORC_PLAYER())
				newUnit = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_DROWN'), 15, 17, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)
				newUnit2 = bPlayer.initUnit(gc.getInfoTypeForString('UNIT_DROWN'), 15, 19, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)
				py = PyPlayer(0) #Decius
				for pLoopUnit in py.getUnitList():
					if pLoopUnit.getUnitType() == gc.getInfoTypeForString('UNIT_ROSIER_OATHTAKER'):
						pLoopUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER_WALKING'), True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			iPlayer = 1 #Decius (in the Calabim version)
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isHuman():
				if city.getName() == "Dirage":
					if gc.getGame().getScenarioCounter() == 0:
						gc.getGame().changeScenarioCounter(75)
						addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_DIRGE_RAZED",()), iPlayer)
						pCity = pPlayer.getCapitalCity()
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_NIGHTWATCH'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer = gc.getPlayer(0) #Varn
						pCity = pPlayer.getCapitalCity()
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_EMPYREAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						pTeam = gc.getTeam(pPlayer.getTeam())
						pTeam.setHasTech(gc.getInfoTypeForString('TECH_HONOR'), true, 0, true, false)
						pTeam.setDefensivePact(gc.getPlayer(2).getTeam(), true)
						pTeam.setDefensivePact(gc.getPlayer(3).getTeam(), true)
						pTeam.setDefensivePact(gc.getPlayer(5).getTeam(), true)
						CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)

	def onImprovementDestroyed(self, iImprovement, iOwner, iX, iY):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			iPlayer = 0 #Decius
			if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BARROW'):
				if (iX == 19 and iY == 23):
					pPlayer = gc.getPlayer(iPlayer)
					pPlot = CyMap().plot(29,21)
					bValid = False
					for i in range(pPlot.getNumUnits(), -1, -1):
						pLoopUnit = pPlot.getUnit(i)
						if pLoopUnit.getUnitType() == gc.getInfoTypeForString('UNIT_CATAPULT'):
							bValid = True
							newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CATAPULT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							newUnit.convert(pLoopUnit)
							newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), False)
					if bValid:
						addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_CATAPULTS",()), iPlayer)

			if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_JUNGLE_ALTAR'):
				if (iX == 16 and iY == 1):
					addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_TWISTED_MEN",()), iOwner)
					if gc.getGame().getScenarioCounter() == 2:
						gc.getGame().changeScenarioCounter(1)

	def atRangeJungleAltar(self, pCaster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if pCaster.isHuman():
				if gc.getGame().getScenarioCounter() == 1:
					if (pPlot.getX() == 16 and pPlot.getY() == 1):
						pPlot.setPythonActive(False)
						iPlayer = 0 #Decius
						addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_MUIRIN",()), iPlayer)
						if gc.getGame().getScenarioCounter() == 1:
							gc.getGame().changeScenarioCounter(1)

	def onMoveJungleAltar(self, pCaster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			iPlayer = pCaster.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isHuman():
				if (pPlot.getX() == 34 and pPlot.getY() == 12):
					addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_ALTAR",()), iPlayer)
					pPlot.setPythonActive(False)
				if (pPlot.getX() == 70 and pPlot.getY() == 37):
					szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_ALTAR_TO_DIS",())
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
						szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_ALTAR_TO_DIS_KEELYN",())
					addPlayerPopup(szText, iPlayer)
					pPlot.setPythonActive(False)

	def onMoveMirrorOfHeaven(self, pCaster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			if gc.getGame().getScenarioCounter() == 0:
				iPlayer = pCaster.getOwner()
				pPlayer = gc.getPlayer(iPlayer)
				if pPlayer.isHuman():
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
						gc.getGame().changeScenarioCounter(175)
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_MIRROR_OF_HEAVEN",()),'art/interface/popups/Varn.dds')
						pPlot = CyMap().plot(30,23)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pPlot.getX(),  pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SETTLER'), pPlot.getX(),  pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_EMPYREAN'), pPlot.getX(),  pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pTeam = gc.getTeam(1) #Flauros
						pTeam.declareWar(0, false, WarPlanTypes.WARPLAN_TOTAL)

	def onMovePortal(self, pCaster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			if pCaster.getUnitType() == gc.getInfoTypeForString('UNIT_ARCHMAGE'):
				gc.getPlayer(0).initCity(20,3)
				gc.getGame().setOption(GameOptionTypes.GAMEOPTION_COMPLETE_KILLS, False)
				for iPlayer in range(gc.getMAX_PLAYERS()):
					if iPlayer != 0:
						pPlayer = gc.getPlayer(iPlayer)
						if pPlayer.isAlive():
							pPlayer.setAlive(False)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_CULT):
			iPlayer = pCaster.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isHuman():
				if (pPlot.getX() == 45 and pPlot.getY() == 1):
					if gc.getGame().getScenarioCounter() == 0:
						gc.getGame().changeScenarioCounter(1)
						CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
						pPlot.setPythonActive(False)
				if (pPlot.getX() == 21 and pPlot.getY() == 18):
					if gc.getGame().getScenarioCounter() == 1:
						for iY in range(18, 31, 1):
							pPlot = CyMap().plot(21,iY)
							pPlot.setMoveDisabledAI(False)
						pPlayer = gc.getPlayer(3) #Cardith
						pCity = pPlayer.getCapitalCity()
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_EURABATRES'), pCity.getX(),  pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer = gc.getPlayer(4) #Os-Gabella
						pCity = pPlayer.getCapitalCity()
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ABASHI'), pCity.getX(),  pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						bPlayer = gc.getPlayer(gc.getORC_PLAYER())
						bPlayer.initUnit(gc.getInfoTypeForString('UNIT_ACHERON'), 21, 20, UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						gc.getGame().changeScenarioCounter(1)
						CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
						pPlot.setPythonActive(False)
						pPlot.setImprovementType(-1)
						pPlot = CyMap().plot(21,17)
						pPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
						pPlot = CyMap().plot(21,16)
						pPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)
						pPlot = CyMap().plot(21,15)
						pPlot.setImprovementType(-1)

	def onMoveWarningPost(self, pCaster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			iPlayer = pCaster.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isHuman():
				iHeld = gc.getInfoTypeForString('PROMOTION_HELD')
				if (pPlot.getX() == 4 and pPlot.getY() == 14):
					if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR2')):
						pCaster.setXY(4, 13, False, True, True,False)
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_WARD_AIR",()),'art/interface/popups/Dain.dds')
					else:
						apUnitList = PyPlayer(gc.getORC_PLAYER()).getUnitList()
						iManes = gc.getInfoTypeForString('UNIT_MANES')
						for pUnit in apUnitList:
							if pUnit.getUnitType() == iManes:
								pUnit.setHasPromotion(iHeld, False)
				if (pPlot.getX() == 16 and pPlot.getY() == 11):
					if not pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE2')):
						pCaster.setXY(17, 11, False, True, True,False)
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_WARD_FIRE",()),'art/interface/popups/Dain.dds')
					else:
						apUnitList = PyPlayer(gc.getORC_PLAYER()).getUnitList()
						iPyreZombie = gc.getInfoTypeForString('UNIT_PYRE_ZOMBIE')
						iSpectre = gc.getInfoTypeForString('UNIT_SPECTRE')
						for pUnit in apUnitList:
							if pUnit.getUnitType() == iPyreZombie:
								pUnit.setHasPromotion(iHeld, False)
							if pUnit.getUnitType() == iSpectre:
								pUnit.setHasPromotion(iHeld, False)
				if (pPlot.getX() == 23 and pPlot.getY() == 6):
					iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_GIFT_OF_KYLORIN_SECRET_DOOR')
					triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, 0, -1, -1, -1, -1, -1)
				if (pPlot.getX() == 8 and pPlot.getY() == 4):
					apUnitList = PyPlayer(gc.getORC_PLAYER()).getUnitList()
					iWoodGolem = gc.getInfoTypeForString('UNIT_WOOD_GOLEM')
					for pUnit in apUnitList:
						if pUnit.getUnitType() == iWoodGolem:
							pUnit.setHasPromotion(iHeld, False)
					pPlot.setPythonActive(False)
				if (pPlot.getX() == 19 and pPlot.getY() == 16):
					if pPlayer.isHuman():
						if pCaster.getUnitType() != gc.getInfoTypeForString('UNIT_ARCHMAGE'):
							pCaster.kill(True, 0)
						else:
							iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_GIFT_OF_KYLORIN_MESHABBER')
							triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, 0, -1, -1, -1, -1, -1)
				if (pPlot.getX() == 28 and pPlot.getY() == 1):
					if pPlayer.isHuman():
						if pCaster.getUnitType() == gc.getInfoTypeForString('UNIT_ARCHMAGE'):
							self.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_POTION_OF_INVISIBILITY",()),'art/interface/popups/Dain.dds')
							pPlot = CyMap().plot(27,1)
							pUnit = pPlot.getUnit(0)
							pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_INVISIBLE'), True)
							pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POTION_OF_INVISIBILITY'), True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			iPlayer = pCaster.getOwner()
			pPlayer = gc.getPlayer(iPlayer)
			if pPlayer.isHuman():
				if (pPlot.getX() == 33 and pPlot.getY() == 14):
					szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONQUERERS_PASS",())
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
						szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONQUERERS_PASS_KEELYN",())
					addPlayerPopup(szText, iPlayer)
					pPlot.setPythonActive(False)
				if (pPlot.getX() == 50 and pPlot.getY() == 12):
					szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_SORROWS_PASS",())
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
						szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_SORROWS_PASS_KEELYN",())
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VARN'):
						szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_SORROWS_PASS_VARN",())
					addPlayerPopup(szText, iPlayer)
					pPlot.setPythonActive(False)
				if (pPlot.getX() == 2 and pPlot.getY() == 16):
					addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_FORGOTTEN_PASS",()), iPlayer)
					pPlot.setPythonActive(False)
			if (pPlot.getX() == 29 and pPlot.getY() == 36):
				addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_FREE_CHAMPION",()), iPlayer)
				newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), 29, 38, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.setDamage(90, PlayerTypes.NO_PLAYER)
				CyMap().plot(29,37).setFeatureType(-1, -1)
				CyMap().plot(29,38).setImprovementType(-1)
				pPlot.setPythonActive(False)

	def onReligionFounded(self, iReligion, iFounder):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			pPlayer = gc.getPlayer(iFounder)
			pCity = gc.getGame().getHolyCity(iReligion)
			if iReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_RADIANT_GUARD'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_EMPYREAN'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_EMPYREAN'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_RELIGION_EMPYREAN", ())
				addPlayerPopup(szText, iFounder)
			if iReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_OCTOPUS_OVERLORDS'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DROWN'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DROWN'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_RELIGION_OVERLORDS", ())
				addPlayerPopup(szText, iFounder)
			if iReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CRUSADER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ORDER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				pPlayer.initUnit(gc.getInfoTypeForString('UNIT_DISCIPLE_THE_ORDER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_RELIGION_ORDER", ())
				addPlayerPopup(szText, iFounder)

	def onTechAcquired(self, iTechType, iTeam, iPlayer, bAnnounce):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if iTechType == gc.getInfoTypeForString('TECH_ORDERS_FROM_HEAVEN'):
				if iTeam == 0: #Decius's Team
					pPlayer = gc.getPlayer(0) #Decius
					pCity = pPlayer.getCapitalCity()
					newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ROSIER_OATHTAKER'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COURAGE'), True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			if gc.getTeam(iTeam).isHuman():
				if iTechType == gc.getInfoTypeForString('TECH_SMELTING'):
					if not gc.getGame().isHasTrophy("TROPHY_WB_SPLINTER_COURT_PARITH"):
						for iPlayer in range(gc.getMAX_PLAYERS()):
							pLoopPlayer = gc.getPlayer(iPlayer)
							if pLoopPlayer.getTeam() == iTeam:
								if pLoopPlayer.isHuman():
									iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_WB_SPLINTERED_COURT_PARITH')
									triggerData = pLoopPlayer.initTriggeredData(iEvent, true, -1, -1, -1, -1, -1, -1, -1, -1, -1)

	def onUnitCreated(self, pUnit):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			pPlayer = gc.getPlayer(pUnit.getOwner())
			if pPlayer.isHuman():
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BOUNTY_HUNTER'), True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_ROSIER_OATHTAKER'):
				pPlot = CyMap().plot(16,1)
				pPlot.setMoveDisabledHuman(False)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			pPlayer = gc.getPlayer(pUnit.getOwner())
			if pPlayer.isHuman():
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMBAT1'), True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			if pUnit.getUnitType() == gc.getInfoTypeForString('EQUIPMENT_TREASURE'):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_INVISIBLE'), False)
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_ARCHMAGE'):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING2'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING3'), False)
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POTENCY'), False)
				pUnit.changeFreePromotionPick(-1)
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FLYING'), False)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_AURIC_ASCENDED'):
				for iPlayer in range(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iPlayer)
					if pLoopPlayer.isAlive():
						if pLoopPlayer.getTeam() != 0:
							gc.getPlayer(iPlayer).changeDisableProduction(1000)
				iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
				iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
				iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
				iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
				iTaiga = gc.getInfoTypeForString('TERRAIN_TAIGA')
				for i in range (CyMap().numPlots()):
					pPlot = CyMap().plotByIndex(i)
					if pPlot.getFeatureType() == -1:
						if pPlot.getImprovementType() == -1:
							if pPlot.isWater() == False:
								iTerrain = pPlot.getTerrainType()
								if iTerrain == iTaiga:
									pPlot.setTerrainType(iTundra)
								if iTerrain == iGrass:
									pPlot.setTerrainType(iTaiga)
								if iTerrain == iPlains:
									pPlot.setTerrainType(iTaiga)
								if iTerrain == iDesert:
									pPlot.setTerrainType(iPlains)
				self.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_AURIC_ASCENDED",()),'art/interface/popups/Auric Ascended.dds')

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_CULT):
			pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FLYING'), False)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			if pUnit.isAlive():
				if not pUnit.isOnlyDefensive():
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MUTATED'), True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			pPlayer = gc.getPlayer(pUnit.getOwner())
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				if pUnit.getUnitCombatType() != gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
					pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, 5, 13, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_VALIN'):
				if gc.getGame().getUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_VALIN')) == 1:
					bGood = True
					for iPlayer in range(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_CALABIM",())
								if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_ELOHIM",())
								if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_MALAKIM",())
								if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_VALIN_SHEAIM",())
								self.addPopup(szText,'art/interface/popups/Valin Phanuel.dds')

			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_ROSIER'):
				if gc.getGame().getUnitClassCreatedCount(gc.getInfoTypeForString('UNITCLASS_ROSIER')) == 1:
					bGood = True
					for iPlayer in range(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_CALABIM",())
								if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_ELOHIM",())
								if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_MALAKIM",())
								if pLoopPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
									szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_HERO_ROSIER_SHEAIM",())
								self.addPopup(szText,'art/interface/popups/Rosier the Fallen.dds')

	def onUnitKilled(self, pUnit, iAttacker):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GREAT_COMMANDER')):
				iDecius = gc.getInfoTypeForString('UNIT_DECIUS')
				if pUnit.getScenarioCounter() == iDecius:
					pPlayer = gc.getPlayer(pUnit.getOwner())
					pCity = pPlayer.getCapitalCity()
					if not pCity.isNone():
						pPlayer.initUnit(iDecius, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_ROSIER_OATHTAKER'):
				if gc.getGame().getScenarioCounter() < 6:
					iPlayer = 0 #Decius
					addPlayerPopup(CyTranslator().getText("TXT_KEY_WB_FALL_OF_CUANTINE_ROSIER_KILLED",()), iPlayer)
					gc.getPlayer(iPlayer).setAlive(False)
			if gc.getGame().getScenarioCounter() == 5:
				if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_DROWN'):
					bValid = True
					iX = 16
					iY = 18
					for iiX in range(iX-1, iX+2, 1):
						for iiY in range(iY-1, iY+2, 1):
							pPlot = CyMap().plot(iiX,iiY)
							for i in range(pPlot.getNumUnits()):
								pLoopUnit = pPlot.getUnit(i)
								if pLoopUnit.getUnitType() == gc.getInfoTypeForString('UNIT_DROWN'):
									if pLoopUnit.getID() != pUnit.getID():
										bValid = False
					if bValid:
						gc.getGame().changeScenarioCounter(1)
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_FALL_OF_CUANTINE_ROSIER')
						iPlayer = 0 #Decius
						pPlayer = gc.getPlayer(iPlayer)
						triggerData = pPlayer.initTriggeredData(iEvent, true, -1, -1, -1, 0, -1, -1, -1, -1, -1)
						for iUnit in range(pPlayer.getNumUnits()):
							pLoopUnit = pPlayer.getUnit(iUnit)
							if pLoopUnit.getUnitType() == gc.getInfoTypeForString('UNIT_ROSIER_OATHTAKER'):
								pLoopUnit.kill(True,0)
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GREAT_COMMANDER')):
				iDecius = gc.getInfoTypeForString('UNIT_DECIUS')
				if pUnit.getScenarioCounter() == iDecius:
					pPlayer = gc.getPlayer(pUnit.getOwner())
					pCity = pPlayer.getCapitalCity()
					if not pCity.isNone():
						pPlayer.initUnit(iDecius, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_ARCHMAGE'):
				pPlayer = gc.getPlayer(pUnit.getOwner())
				if pPlayer.isHuman():
					pPlayer.setAlive(False)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			if pUnit.getOwner() == gc.getORC_PLAYER():
				iUnitClass = pUnit.getUnitClassType()
				iPlayer = 0 #Falamar
				szText = -1
				if gc.getGame().getUnitClassCreatedCount(iUnitClass) == 2:
					if iUnitClass == gc.getInfoTypeForString('UNITCLASS_BEAR'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_BEAR",())
					if iUnitClass == gc.getInfoTypeForString('UNITCLASS_LION'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_LION",())
					if iUnitClass == gc.getInfoTypeForString('UNITCLASS_WOLF'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_WOLF",())
				if gc.getGame().getUnitClassCreatedCount(iUnitClass) == 1:
					if iUnitClass == gc.getInfoTypeForString('UNITCLASS_ELEPHANT'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_ELEPHANT",())
					if iUnitClass == gc.getInfoTypeForString('UNITCLASS_GORILLA'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_GORILLA",())
					if iUnitClass == gc.getInfoTypeForString('UNITCLASS_GRIFFON'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_GRIFFON",())
					if iUnitClass == gc.getInfoTypeForString('UNITCLASS_GIANT_SPIDER'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_SPIDER",())
					if iUnitClass == gc.getInfoTypeForString('UNITCLASS_TIGER'):
						szText = CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_ANIMAL_TIGER",())
				if szText != -1:
					addPlayerPopup(szText, iPlayer)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_AURIC_ASCENDED'):
				gc.getGame().setWinner(0, 2) #Falamar wins
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GREAT_COMMANDER')):
				iDecius = gc.getInfoTypeForString('UNIT_DECIUS')
				if pUnit.getScenarioCounter() == iDecius:
					pPlayer = gc.getPlayer(pUnit.getOwner())
					pCity = pPlayer.getCapitalCity()
					if not pCity.isNone():
						pPlayer.initUnit(iDecius, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			if pUnit.isAlive():
				iUnit = cf.getUnholyVersion(pUnit)
				if iUnit != -1:
					pPlayer = gc.getPlayer(1)
					pCity = pPlayer.getCapitalCity()
					newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
					newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON'), True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			pPlayer = gc.getPlayer(pUnit.getOwner())
			if gc.getGame().getScenarioCounter() == 0:
				if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_BASIUM'):
					if gc.getTeam(0).isAtWar(pPlayer.getTeam()):
						gc.getGame().setOption(GameOptionTypes.GAMEOPTION_COMPLETE_KILLS, False)
						if not (CyMap().plot(0,2).isCity()):
							gc.getPlayer(0).initCity(0,2)
					##	for iPlayer in range(gc.getMAX_PLAYERS()):
					#		if iPlayer != 0:
					 #			pPlayer = gc.getPlayer(iPlayer)
					#			if pPlayer.isAlive():
					#				pPlayer.setAlive(False)
						gc.getGame().setWinner(0, 2) #Falamar wins
					else:
						gc.getGame().setWinner(2, 2) #Hyborem wins
				if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_HYBOREM'):
					if gc.getTeam(0).isAtWar(pPlayer.getTeam()):
						gc.getGame().setOption(GameOptionTypes.GAMEOPTION_COMPLETE_KILLS, False)
						if not (CyMap().plot(0,2).isCity()):
							gc.getPlayer(0).initCity(0,2)
					#	for iPlayer in range(gc.getMAX_PLAYERS()):
					#		if iPlayer != 0:
					#			pPlayer = gc.getPlayer(iPlayer)
					#			if pPlayer.isAlive():
					#				pPlayer.setAlive(False)
						gc.getGame().setWinner(0, 2) #Falamar wins
					else:
						gc.getGame().setWinner(1, 2) #Basium wins
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				if gc.getGame().getScenarioCounter() > 0:
					gc.getGame().changeScenarioCounter(-1)
					if gc.getGame().getScenarioCounter() == 0:
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_THE_RADIANT_GUARD_CHOOSE_SIDES')
						iPlayer = 0 #Falamar
						triggerData = gc.getPlayer(iPlayer).initTriggeredData(iEvent, true, -1, -1, -1, 0, -1, -1, -1, -1, -1)
						for i in range (CyMap().numPlots()):
							pPlot = CyMap().plotByIndex(i)
							if pPlot.getX() <= 9:
								pPlot.setMoveDisabledHuman(False)
						pPlayer = gc.getPlayer(1) #Basium
						pCity = pPlayer.getCapitalCity()
						newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_BASIUM'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_HELD'), True)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ANGEL'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SERAPH'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SERAPH'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SERAPH'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_OPHANIM'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_OPHANIM'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_OPHANIM'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_VALKYRIE'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_VALKYRIE'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_VALKYRIE'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHAMPION'), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
						pPlot = CyMap().plot(75,47)
						pPlot.setMoveDisabledHuman(False)
					CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GREAT_COMMANDER')):
				iDecius = gc.getInfoTypeForString('UNIT_DECIUS')
				if pUnit.getScenarioCounter() == iDecius:
					pPlayer = gc.getPlayer(pUnit.getOwner())
					pCity = pPlayer.getCapitalCity()
					if not pCity.isNone():
						pPlayer.initUnit(iDecius, pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

	def onVictory(self, iPlayer, iVictory):
		pPlayer = gc.getPlayer(iPlayer)
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_GREY):
			gc.getGame().changeTrophyValue("TROPHY_WB_AGAINST_THE_GREY", 1)
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_GREY_VICTORY_CALABIM",())
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_GREY_VICTORY_MALAKIM",())
			self.addPopupWB(szText, 'art/interface/popups/Against the Grey.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_AGAINST_THE_WALL):
			gc.getGame().changeTrophyValue("TROPHY_WB_AGAINST_THE_WALL", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_AGAINST_THE_WALL_VICTORY",()), 'art/interface/popups/Against the Wall Victory.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
			gc.getGame().changeTrophyValue("TROPHY_WB_BARBARIAN_ASSAULT", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_VICTORY",()), 'art/interface/popups/Barbarian Assault.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
			gc.getGame().changeTrophyValue("TROPHY_WB_BENEATH_THE_HEEL", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_VICTORY",()), 'art/interface/popups/Beneath the Heel.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
			gc.getGame().changeTrophyValue("TROPHY_WB_BLOOD_OF_ANGELS", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_VICTORY",()), 'art/interface/popups/Blood of Angels Victory.dds')
			iXP = self.getHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'))
			if iXP > gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP")*100:
				gc.getGame().setTrophyValue("TROPHY_WB_LUCIAN_XP", iXP)
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_FALL_OF_CUANTINE):
			gc.getGame().changeTrophyValue("TROPHY_WB_FALL_OF_CUANTINE", 1)
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			gc.getGame().changeTrophyValue("TROPHY_WB_GIFT_OF_KYLORIN", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_VICTORY",()), 'art/interface/popups/Gift of Kylorin.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GRAND_MENAGERIE):
			gc.getGame().changeTrophyValue("TROPHY_WB_GRAND_MENAGERIE", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_GRAND_MENAGERIE_VICTORY",()), 'art/interface/popups/Grand Menagerie Victory.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_INTO_THE_DESERT):
			gc.getGame().changeTrophyValue("TROPHY_WB_INTO_THE_DESERT", 1)
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_MALAKIM_VICTORY",()), 'art/interface/popups/Into the Desert.dds')
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_INTO_THE_DESERT_CALABIM_VICTORY",()), 'art/interface/popups/Into the Desert Calabim.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
			gc.getGame().changeTrophyValue("TROPHY_WB_LORD_OF_THE_BALORS", 1)
			if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BASIUM'):
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONCLUSION_BASIUM",())
			if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CAPRIA'):
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONCLUSION_CAPRIA",())
			if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONCLUSION_KEELYN",())
			if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
				szText = CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_CONCLUSION_VARN",())
			self.addPopupWB(szText, 'art/interface/popups/Lord of the Balors Victory.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
			gc.getGame().changeTrophyValue("TROPHY_WB_MULCARN_REBORN", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_VICTORY",()), 'art/interface/popups/Mulcarn Reborn Victory.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):
			gc.getGame().changeTrophyValue("TROPHY_WB_RETURN_OF_WINTER", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_VICTORY",()), 'art/interface/popups/Return of Winter Victory.dds')
			iXP = self.getHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'))
			if iXP > gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP"):
				gc.getGame().setTrophyValue("TROPHY_WB_LUCIAN_XP", iXP)
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
			gc.getGame().changeTrophyValue("TROPHY_WB_THE_BLACK_TOWER", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_BLACK_TOWER_VICTORY",()), 'art/interface/popups/The Black Tower Victory.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_CULT):
			gc.getGame().changeTrophyValue("TROPHY_WB_THE_CULT", 1)
			self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_CULT_VICTORY",()), 'art/interface/popups/The Cult.dds')
			iXP = self.getHeroXP(iPlayer, gc.getInfoTypeForString('UNIT_LUCIAN'))
			if iXP > gc.getGame().getTrophyValue("TROPHY_WB_LUCIAN_XP"):
				gc.getGame().setTrophyValue("TROPHY_WB_LUCIAN_XP", iXP)
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
			gc.getGame().changeTrophyValue("TROPHY_WB_THE_MOMUS", 1)
			szText = CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_VICTORY_PERPENTACH",())
			if CyGame().isHasTrophy("TROPHY_WB_THE_MOMUS_BEERI_ALLY"):
				szText = CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_VICTORY_BEERI",())
			self.addPopupWB(szText, 'art/interface/popups/The Momus Victory.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
			gc.getGame().changeTrophyValue("TROPHY_WB_THE_SPLINTERED_COURT", 1)
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				gc.getGame().setTrophyValue("TROPHY_WB_THE_SPLINTERED_COURT_LJOSALFAR", 1)
				gc.getGame().setTrophyValue("TROPHY_WB_THE_SPLINTERED_COURT_SVARTALFAR", 0)
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_VICTORY_LJOSALFAR",()), 'art/interface/popups/The Splintered Court Ljosalfar Victory.dds')
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				gc.getGame().setTrophyValue("TROPHY_WB_THE_SPLINTERED_COURT_LJOSALFAR", 0)
				gc.getGame().setTrophyValue("TROPHY_WB_THE_SPLINTERED_COURT_SVARTALFAR", 1)
				self.addPopupWB(CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_VICTORY_SVARTALFAR",()), 'art/interface/popups/The Splintered Court Svartalfar Victory.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_RADIANT_GUARD):
			gc.getGame().changeTrophyValue("TROPHY_WB_THE_RADIANT_GUARD", 1)
			szText = CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_VICTORY_BASIUM",())
			if CyGame().isHasTrophy("TROPHY_WB_THE_RADIANT_GUARD_HYBOREM_ALLY"):
				szText = CyTranslator().getText("TXT_KEY_WB_THE_RADIANT_GUARD_VICTORY_HYBOREM",())
			self.addPopupWB(szText, 'art/interface/popups/The Radiant Guard.dds')
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
			gc.getGame().changeTrophyValue("TROPHY_WB_WAGES_OF_SIN", 1)
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_ELOHIM",())
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_MALAKIM",())
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_CALABIM",())
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
				szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_CONCLUSION_SHEAIM",())
			self.addPopupWB(szText, 'art/interface/popups/Wages of Sin Victory.dds')

	def openChest(self, caster, pPlot):
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_GIFT_OF_KYLORIN):
			if caster.getUnitType() != gc.getInfoTypeForString('UNIT_ARCHMAGE'):
				self.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORON_TREASURE_LOCKED",()),'art/interface/popups/Dain.dds')
				return False
			if (pPlot.getX() == 20 and pPlot.getY() == 11):
				self.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_SPRING",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1'), True)
				gc.getGame().changeScenarioCounter(1)
			if (pPlot.getX() == 25 and pPlot.getY() == 4):
				self.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_RAISE_SKELETON",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1'), True)
			if (pPlot.getX() == 27 and pPlot.getY() == 11):
				self.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_FIREBALL",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE2'), True)
				gc.getGame().changeScenarioCounter(1)
			if (pPlot.getX() == 8 and pPlot.getY() == 14):
				self.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_COURAGE",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT1'), True)
			if (pPlot.getX() == 17 and pPlot.getY() == 4):
				self.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_MAELSTROM",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR2'), True)
				gc.getGame().changeScenarioCounter(1)
			if (pPlot.getX() == 27 and pPlot.getY() == 20):
				self.addPopup(CyTranslator().getText("TXT_KEY_WB_GIFT_OF_KYLORIN_TREASURE_FLOATING_EYE",()),'art/interface/popups/Dain.dds')
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC1'), True)
				gc.getGame().changeScenarioCounter(1)
			iTreasure = gc.getInfoTypeForString('EQUIPMENT_TREASURE')
			pTreasure = -1
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getUnitType() == iTreasure:
					if pUnit.getOwner() == caster.getOwner():
						pTreasure = pUnit
			if pTreasure != -1:
				pTreasure.kill(True, 0)
			return False
		return True

	def playerDefeated(self, pPlayer):
		if gc.getGame().getGameTurn() > 5:
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BARBARIAN_ASSAULT):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AMELANCHIER'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_AMELANCHIER",()),'art/interface/popups/Amelanchier.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BEERI'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_BEERI",()),'art/interface/popups/Beeri.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CAPRIA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_CAPRIA",()),'art/interface/popups/Capria.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CHARADON'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_CHARADON",()),'art/interface/popups/Charadon.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_DAIN'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_DAIN",()),'art/interface/popups/Dain.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_EINION'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_EINION",()),'art/interface/popups/Einion.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HALFGAN'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_HALFGAN",()),'art/interface/popups/Halfgan.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SHEELBA'):
					for iTeam in range(gc.getMAX_TEAMS()):
						pTeam = gc.getTeam(iTeam)
						if pTeam.isAlive():
							if pTeam.isHuman():
								gc.getGame().setWinner(iTeam, 2)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TASUNKE'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BARBARIAN_ASSAULT_DEFEATED_TASUNKE",()),'art/interface/popups/Tasunke.dds')

			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BENEATH_THE_HEEL):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AURIC'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_AURIC",()),'art/interface/popups/Auric.dds')
					for iTeam in range(gc.getMAX_TEAMS()):
						pTeam = gc.getTeam(iTeam)
						if pTeam.isAlive():
							if not pTeam.isHuman():
								gc.getGame().setWinner(iTeam, 2)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BEERI'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_BEERI",()),'art/interface/popups/Beeri.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_EINION'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_EINION",()),'art/interface/popups/Einion.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_GARRIM'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_GARRIM",()),'art/interface/popups/Garrim.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SANDALPHON'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_SANDALPHON",()),'art/interface/popups/Sandalphon.dds')

			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_BLOOD_OF_ANGELS):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AURIC'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_DEFEATED_AURIC",()),'art/interface/popups/Auric.dds')
					for iTeam in range(gc.getMAX_TEAMS()):
						pTeam = gc.getTeam(iTeam)
						if pTeam.isAlive():
							if not pTeam.isHuman():
								gc.getGame().setWinner(iTeam, 2)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HANNAH'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_DEFEATED_HANNAH",()),'art/interface/popups/Hannah.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MAHALA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_DEFEATED_MAHALA",()),'art/interface/popups/Lucian.dds')
					for iTeam in range(gc.getMAX_TEAMS()):
						pTeam = gc.getTeam(iTeam)
						if pTeam.isAlive():
							if not pTeam.isHuman():
								gc.getGame().setWinner(iTeam, 2)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_SABATHIEL'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BLOOD_OF_ANGELS_DEFEATED_SABATHIEL",()),'art/interface/popups/Sabathiel.dds')

			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_LORD_OF_THE_BALORS):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_HYBOREM'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_HYBOREM",()),'art/interface/popups/Hyborem.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BASIUM'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_BASIUM",()),'art/interface/popups/Basium.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CAPRIA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_CAPRIA",()),'art/interface/popups/Capria.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KEELYN'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_KEELYN",()),'art/interface/popups/Keelyn.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VARN'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_LORD_OF_THE_BALORS_DEFEATED_VARN",()),'art/interface/popups/Varn.dds')
				iCount = 0
				iInfernal = gc.getInfoTypeForString('CIVILIZATION_INFERNAL')
				for iPlayer in range(gc.getMAX_PLAYERS()):
					pPlayer = gc.getPlayer(iPlayer)
					if pPlayer.isAlive():
						if pPlayer.getCivilizationType() == iInfernal:
							iCount += 1
				if iCount == 0:
					for iPlayer in range(gc.getMAX_PLAYERS()):
						pPlayer = gc.getPlayer(iPlayer)
						if pPlayer.isAlive():
							if pPlayer.isHuman():
								gc.getGame().setWinner(pPlayer.getTeam(), 2)

			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_MULCARN_REBORN):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_MAHALA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_MAHALA",()),'art/interface/popups/Mahala.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AMELANCHIER'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_AMELANCHIER",()),'art/interface/popups/Amelanchier.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VOLANNA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_VOLANNA",()),'art/interface/popups/Volanna.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RHOANNA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_RHOANNA",()),'art/interface/popups/Rhoanna.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FALAMAR'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_FALAMAR",()),'art/interface/popups/Falamar.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CAPRIA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_CAPRIA",()),'art/interface/popups/Capria.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_DECIUS'):
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_DECIUS_CALABIM",()),'art/interface/popups/Decius.dds')
					if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_MULCARN_REBORN_DEFEATED_DECIUS_MALAKIM",()),'art/interface/popups/Decius.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AURIC'):
					gc.getGame().setWinner(1, 2) #Falamar Wins

			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_RETURN_OF_WINTER):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AURIC'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_BENEATH_THE_HEEL_DEFEATED_AURIC",()),'art/interface/popups/Auric.dds')
					iPlayer = 0 #Mahala
					gc.getPlayer(iPlayer).setAlive(false)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_CARDITH'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_CARDITH_DEFEATED",()),'art/interface/popups/Cardith.dds')
					for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								pLoopPlayer.changeGold(250)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_KOUN'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_KOUN_DEFEATED",()),'art/interface/popups/Koun.dds')
					for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								pCity = pLoopPlayer.getCapitalCity()
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_LEAVES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								pLoopPlayer.initUnit(gc.getInfoTypeForString('UNIT_PRIEST_OF_LEAVES'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TETHIRA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_TETHIRA_DEFEATED",()),'art/interface/popups/Tethira.dds')
					for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								for iUnit in range(pLoopPlayer.getNumUnits()):
									pUnit = pLoopPlayer.getUnit(iUnit)
									pUnit.changeExperience(2, -1, False, False, False)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_THESSALONICA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_RETURN_OF_WINTER_THESSALONICA_DEFEATED",()),'art/interface/popups/Thessalonica.dds')
					for iLoopPlayer in range(gc.getMAX_PLAYERS()):
						pLoopPlayer = gc.getPlayer(iLoopPlayer)
						if pLoopPlayer.isAlive():
							if pLoopPlayer.isHuman():
								for pyCity in PyPlayer(iLoopPlayer).getCityList() :
									pCity = pyCity.GetCy()
									pCity.changeCulture(iLoopPlayer, 300, True)

			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_BLACK_TOWER):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TEBRYN'):
					gc.getGame().setWinner(0, 2) #Falamar Wins

			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_MOMUS):
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FURIA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_FURIA",()),'art/interface/popups/Furia.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_WEEVIL'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_WEEVIL",()),'art/interface/popups/Weevil.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_TYA'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_TYA",()),'art/interface/popups/Tya.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_BEERI'):
					self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_MOMUS_DEFEATED_BEERI",()),'art/interface/popups/Beeri.dds')
				bValid = True
				if not gc.getPlayer(1).isAlive(): #Perpentach
					gc.getGame().setWinner(0, 2)
					bValid = False
				if gc.getPlayer(2).isAlive(): #Melisandre
					bValid = False
				if gc.getPlayer(3).isAlive(): #Furia
					bValid = False
				if gc.getPlayer(4).isAlive(): #Weevil
					bValid = False
				if gc.getPlayer(5).isAlive(): #Tya
					bValid = False
				if gc.getPlayer(6).isAlive(): #Uldanor
					bValid = False
				if gc.getPlayer(8).isAlive(): #Sallos
					bValid = False
				if gc.getPlayer(9).isAlive(): #Mahon
					bValid = False
				if bValid:
					if gc.getPlayer(7).isAlive(): #Beeri
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_THE_MOMUS_BEERIS_OFFER')
						triggerData = gc.getPlayer(0).initTriggeredData(iEvent, true, -1, -1, -1, 0, -1, -1, -1, -1, -1)
					else:
						gc.getGame().setWinner(0, 2)

			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_THE_SPLINTERED_COURT):
				bWin = False
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
					bWin = True
					iWinningTeam = 1
					if gc.getPlayer(0).isAlive():
						bWin = False
					if gc.getPlayer(1).isAlive():
						bWin = False
					if gc.getPlayer(2).isAlive():
						bWin = False
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
					bWin = True
					iWinningTeam = 0
					if gc.getPlayer(3).isAlive():
						bWin = False
					if gc.getPlayer(4).isAlive():
						bWin = False
					if gc.getPlayer(5).isAlive():
						bWin = False
				iHumanPlayer = -1
				for iLoopPlayer in range(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if pLoopPlayer.isAlive():
						if pLoopPlayer.isHuman():
							if pLoopPlayer.getCivilizationType() != pPlayer.getCivilizationType():
								iHumanPlayer = iLoopPlayer
				if iHumanPlayer != -1:
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_AMELANCHIER'):
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_SPLINTERED_COURT_DEFEATED_AMELANCHIER')
						triggerData = gc.getPlayer(iHumanPlayer).initTriggeredData(iEvent, true, -1, -1, -1, iHumanPlayer, -1, -1, -1, -1, -1)
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_THESSA'):
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_SPLINTERED_COURT_DEFEATED_THESSA')
						triggerData = gc.getPlayer(iHumanPlayer).initTriggeredData(iEvent, true, -1, -1, -1, iHumanPlayer, -1, -1, -1, -1, -1)
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_RIVANNA'):
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_SPLINTERED_COURT_DEFEATED_RIVANNA')
						triggerData = gc.getPlayer(iHumanPlayer).initTriggeredData(iEvent, true, -1, -1, -1, iHumanPlayer, -1, -1, -1, -1, -1)
					if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_VOLANNA'):
						iEvent = gc.getInfoTypeForString('EVENTTRIGGER_WB_SPLINTERED_COURT_DEFEATED_VOLANNA')
						triggerData = gc.getPlayer(iHumanPlayer).initTriggeredData(iEvent, true, -1, -1, -1, iHumanPlayer, -1, -1, -1, -1, -1)
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_ARENDEL'):
					if not bWin:
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_DEFEATED_ARENDEL",()),'art/interface/popups/Arendel.dds')
				if pPlayer.getLeaderType() == gc.getInfoTypeForString('LEADER_FAERYL'):
					if not bWin:
						self.addPopup(CyTranslator().getText("TXT_KEY_WB_THE_SPLINTERED_COURT_DEFEATED_FAERYL",()),'art/interface/popups/Faeryl.dds')
				if bWin:
					gc.getGame().setWinner(iWinningTeam, 2)

			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_WB_WAGES_OF_SIN):
				iCalabim = gc.getInfoTypeForString('CIVILIZATION_CALABIM')
				iElohim = gc.getInfoTypeForString('CIVILIZATION_ELOHIM')
				iMalakim = gc.getInfoTypeForString('CIVILIZATION_MALAKIM')
				iSheaim = gc.getInfoTypeForString('CIVILIZATION_SHEAIM')
				for iLoopPlayer in range(gc.getMAX_PLAYERS()):
					pLoopPlayer = gc.getPlayer(iLoopPlayer)
					if pLoopPlayer.isAlive():
						if pLoopPlayer.isHuman():
							pHumanPlayer = pLoopPlayer
				iCount = 0
				if (pHumanPlayer.getCivilizationType() == iElohim or pHumanPlayer.getCivilizationType() == iMalakim):
					if gc.getPlayer(1).isAlive(): #Flauros
						iCount += 1
					if gc.getPlayer(3).isAlive(): #Faeryl
						iCount += 1
					if gc.getPlayer(5).isAlive(): #Os-Gabella
						iCount += 1
					if gc.getPlayer(6).isAlive(): #Hyborem
						iCount += 1
				if (pHumanPlayer.getCivilizationType() == iSheaim or pHumanPlayer.getCivilizationType() == iCalabim):
					if gc.getPlayer(0).isAlive(): #Varn
						iCount += 1
					if gc.getPlayer(2).isAlive(): #Arendel
						iCount += 1
					if gc.getPlayer(4).isAlive(): #Ethne
						iCount += 1
					if gc.getPlayer(7).isAlive(): #Basium
						iCount += 1
				if iCount < 2:
					gc.getGame().setWinner(pHumanPlayer.getTeam(), 2)
				szText = -1
				bGood = True
				if pPlayer.getCivilizationType() == iCalabim:
					bGood = False
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
					bGood = False
				if pPlayer.getCivilizationType() == iSheaim:
					bGood = False
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
					bGood = False
				if iCount == 2:
					if bGood:
						if pHumanPlayer.getCivilizationType() == iCalabim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_CALABIM",())
						if pHumanPlayer.getCivilizationType() == iSheaim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_SHEAIM",())
					if not bGood:
						if pHumanPlayer.getCivilizationType() == iElohim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_ELOHIM",())
						if pHumanPlayer.getCivilizationType() == iMalakim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_2_MALAKIM",())
				if iCount == 3:
					if bGood:
						if pHumanPlayer.getCivilizationType() == iCalabim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_CALABIM",())
						if pHumanPlayer.getCivilizationType() == iSheaim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_SHEAIM",())
					if not bGood:
						if pHumanPlayer.getCivilizationType() == iElohim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_ELOHIM",())
						if pHumanPlayer.getCivilizationType() == iMalakim:
							szText = CyTranslator().getText("TXT_KEY_WB_WAGES_OF_SIN_TALIA_1_MALAKIM",())
				if szText != -1:
					szTitle = CyGameTextMgr().getTimeStr(CyGame().getGameTurn(), false)
					popup = PyPopup.PyPopup(-1)
					popup.addDDS('art/interface/popups/Talia.dds', 0, 0, 384, 384)
					popup.addSeparator()
					popup.setHeaderString(szTitle)
					popup.setBodyString(szText)
					popup.launch(true, PopupStates.POPUPSTATE_IMMEDIATE)
