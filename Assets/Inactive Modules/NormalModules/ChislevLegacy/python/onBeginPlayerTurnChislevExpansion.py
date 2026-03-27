from CvPythonExtensions import *
from BasicFunctions import *
import CvScreensInterface

def onBeginPlayerTurn(self, argsList):
	'Called at the beginning of a players turn'
	iGameTurn, iPlayer	= argsList
	gc					= CyGlobalContext()
	pPlayer				= gc.getPlayer(iPlayer)
	git					= gc.getInfoTypeForString
	if pPlayer.getCivilizationType() == git("CIVILIZATION_CHISLEV"):
		if pPlayer.getCivics(git("CIVICOPTION_GOVERNMENT")) == git("CIVIC_TRIBAL_LAW") and pPlayer.getLeaderType() != git("LEADER_THE_COUNCIL"):
			pPlayer.changeCivCounterMod(1)
		iCycle = gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGrowthPercent() / 10 * 6
		if pPlayer.getCivCounterMod() % iCycle == 1: # After either 1 turn into Tribal Law, or after "iCycle"+1 turns, trigger an election
			if pPlayer.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setOption2(True)
				popupInfo.setFlags(126)
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
				popupInfo.setOnClickedPythonCallback("passToModNetMessage")
				popupInfo.setData1(iPlayer)
				popupInfo.setData3(114) # onModNetMessage id
				popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENTTRIGGER_TRIBAL_LAW_ELECTION", ()))
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_EAGLE_TRIBE", ()),"EVENT_TRIBAL_LAW_ELECTION_EAGLE_TRIBE")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_COYOTE_TRIBE", ()),"EVENT_TRIBAL_LAW_ELECTION_COYOTE_TRIBE")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_BEAR_TRIBE", ()),"EVENT_TRIBAL_LAW_ELECTION_BEAR_TRIBE")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SERPENT_TRIBE", ()),"EVENT_TRIBAL_LAW_ELECTION_SERPENT_TRIBE")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_TORTOISE_TRIBE", ()),"EVENT_TRIBAL_LAW_ELECTION_TORTOISE_TRIBE")
				if pPlayer.getCivCounter() != 2:
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_FAIR", ()),"EVENT_TRIBAL_LAW_ELECTION_FAIR")
				else:
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_FAIR3", ()),"EVENT_TRIBAL_LAW_ELECTION_FAIR3")
				popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_NO_PARTICIPATION", ()),"EVENT_TRIBAL_LAW_ELECTION_NO_PARTICIPATION")
				popupInfo.addPopup(iPlayer)
			else:
				argsList = [5,iPlayer]
				effectTribalLawElection(argsList) # based on iAIValue of events (always fair)
		if pPlayer.getCivics(git("CIVICOPTION_GOVERNMENT")) != git("CIVIC_TRIBAL_LAW"):
			pPlayer.setCivCounterMod(0)
			if pPlayer.getLeaderType() == git("LEADER_SHIMASANI") or pPlayer.getLeaderType() == git("LEADER_SOYALA") or pPlayer.getLeaderType() == git("LEADER_MOTSQUEH") or pPlayer.getLeaderType() == git("LEADER_OSYKA") or pPlayer.getLeaderType() == git("LEADER_ALOSAKA"):
				if pPlayer.isHuman():
					popupInfo = CyPopupInfo()
					popupInfo.setOption2(True)
					popupInfo.setFlags(126)
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
					popupInfo.setOnClickedPythonCallback("passToModNetMessage")
					popupInfo.setData1(iPlayer)
					popupInfo.setData3(115) # onModNetMessage id
					popupInfo.setText(CyTranslator().getText("TXT_KEY_EVENTTRIGGER_CIVIC_NOT_TRIBAL_LAW", ()))
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CIVIC_NOT_TRIBAL_LAW_ABSAROKE", ()),"EVENT_CIVIC_NOT_TRIBAL_LAW_ABSAROKE")
					popupInfo.addPythonButton(CyTranslator().getText("TXT_KEY_EVENT_CIVIC_NOT_TRIBAL_LAW_NATANE", ()),"EVENT_CIVIC_NOT_TRIBAL_LAW_NATANE")
					popupInfo.addPopup(iPlayer)
				else:
					AIPick = CyGame().getSorenRandNum(2, "NotTribalLaw, AI Pick")
					argsList = [AIPick,iPlayer]
					effectCivicNotTribalLaw(argsList)

def effectTribalLawElection(argsList):
	iButtonId		= argsList[0]
	iPlayer			= argsList[1]
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
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(lLeaderText[iLeader], ()),'',3,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',git("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
	elif iRnd < 50:											# Same Leader, Failed 50/50, no Bonus
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(lAltFailText[iLeader], ()),'',3,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',git("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
	elif iRnd >= 50:										# Same Leader, Passed 50/50, do Bonus
		CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText(lAltPassText[iLeader], ()),'',3,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',git("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
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

def effectCivicNotTribalLaw(argsList):
	iButtonId		= argsList[0]
	iPlayer			= argsList[1]
	pPlayer			= CyGlobalContext().getPlayer(iPlayer)
	lLeaders		= [CyGlobalContext().getInfoTypeForString("LEADER_CHISLEV"),CyGlobalContext().getInfoTypeForString("LEADER_NATANE")]
	pPlayer.changeLeader(lLeaders[iButtonId])