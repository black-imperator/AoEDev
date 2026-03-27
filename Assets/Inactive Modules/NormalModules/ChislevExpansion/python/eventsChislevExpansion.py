## tribalLawElection.py
## This file applies the effects of each election choice.
## Created by Alsark, 2/3/2018
from CvPythonExtensions import *
import FoxDebug
import FoxTools
import time
from BasicFunctions import *
import CustomFunctions

import pickle
import CvUtil
import CvScreensInterface
import CvMainInterface
import sys
import ScenarioFunctions
import imp    # dynamic importing of libraries
#import glob   # Unix style pathname pattern expansion
import os     # Windows style pathname
import CvPath # path to current assets
import inspect


#Global
gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString
localText = CyTranslator()

sf = ScenarioFunctions.ScenarioFunctions()

##Begin Tribal Law Election
# def doTribalLawElectionEagle(argsList):
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# game 		= CyGame()
	# randNum 		= game.getSorenRandNum
	# setFeat 	= pPlayer.setFeatAccomplished
	
	# setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION1'), False)
        # setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION2'), False)
        # if pPlayer.getLeaderType() == getInfoType('LEADER_SHIMASANI'):
            # iShimasaniChance = randNum(2, "Shimasani Chance")
            # if iShimasaniChance == 0:
                # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SHIMASANI_WINS_ALREADY_SHIMASANI_SUCCESS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
                # for iLoopPlayer in range(gc.getMAX_CIV_PLAYERS()):
                    # loopPlayer = gc.getPlayer(iLoopPlayer)
                    # if loopPlayer.isAlive():
                        # if loopPlayer.getTeam() != pPlayer.getTeam():
                            # loopPlayer.AI_changeAttitudeExtra(iPlayer, 3)
                            # pPlayer.AI_changeAttitudeExtra(iLoopPlayer, 3)
            # elif iShimasaniChance == 1:
                # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SHIMASANI_WINS_ALREADY_SHIMASANI_FAIL", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
        # else:
            # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SHIMASANI_WINS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
            # pPlayer.changeLeader(getInfoType('LEADER_SHIMASANI'))
# ##            pPlayer.setAlignment(getInfoType('ALIGNMENT_GOOD'))
# ##            pPlayer.setBroadAlignment(440)
# ##            pPlayer.setEthicalAlignment(getInfoType('ETHICAL_ALIGNMENT_NEUTRAL'))
# ##            pPlayer.setBroadEthicalAlignment(-50)
# ##            CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
# ##            CvMainInterface.CvMainInterface().updateScreen()
	# return

def getHelpTribalLawElectionEagle(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)
	
	if pPlayer.getLeaderType() == getInfoType('LEADER_SHIMASANI'):
            szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_EAGLE_TRIBE_ALREADY_SHIMASANI", ())
        else:
            szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_EAGLE_TRIBE", ())
	return szHelp

# def doTribalLawElectionCoyote(argsList):
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# game 		= CyGame()
	# randNum 		= game.getSorenRandNum
	# setFeat 	= pPlayer.setFeatAccomplished
	
	# setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION1'), False)
        # setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION2'), False)
        # if pPlayer.getLeaderType() == getInfoType('LEADER_SOYALA'):
            # iSoyalaChance = randNum(2, "Soyala Chance")
            # if iSoyalaChance == 0:
		# CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SOYALA_WINS_ALREADY_SOYALA_SUCCESS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		# pPlayer.initUnit(getInfoType('UNIT_ARTIST'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	    # elif iSoyalaChance == 1:
                # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SOYALA_WINS_ALREADY_SOYALA_FAIL", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
	    # pPlayer.changeAnarchyTurns(1)
        # else:
            # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SOYALA_WINS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
            # pPlayer.changeLeader(getInfoType('LEADER_SOYALA'))
# ##            pPlayer.setAlignment(getInfoType('ALIGNMENT_NEUTRAL'))
# ##            pPlayer.setBroadAlignment(-130)
# ##            pPlayer.setEthicalAlignment(getInfoType('ETHICAL_ALIGNMENT_CHAOTIC'))
# ##            pPlayer.setBroadEthicalAlignment(-750)
# ##            CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
# ##            CvMainInterface.CvMainInterface().updateScreen()
	# return

def getHelpTribalLawElectionCoyote(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)
	
	if pPlayer.getLeaderType() == getInfoType('LEADER_SOYALA'):
            szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_COYOTE_TRIBE_ALREADY_SOYALA", ())
        else:
            szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_COYOTE_TRIBE", ())
	return szHelp

# def doTribalLawElectionBear(argsList):
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
        # game 		= CyGame()
	# randNum 		= game.getSorenRandNum
	# setFeat 	= pPlayer.setFeatAccomplished

	# setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION1'), False)
        # setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION2'), False)
        # if pPlayer.getLeaderType() == getInfoType('LEADER_MOTSQUEH'):
            # iMotsquehChance = randNum(2, "Motsqueh Chance")
            # if iMotsquehChance == 0:
		# CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_MOTSQUEH_WINS_ALREADY_MOTSQUEH_SUCCESS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		# pPlayer.initUnit(getInfoType('UNIT_ENGINEER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	    # elif iMotsquehChance == 1:
                # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_MOTSQUEH_WINS_ALREADY_MOTSQUEH_FAIL", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
	    # pPlayer.changeAnarchyTurns(1)
        # else:
            # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_MOTSQUEH_WINS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
            # pPlayer.changeLeader(getInfoType('LEADER_MOTSQUEH'))
# ##            pPlayer.setAlignment(getInfoType('ALIGNMENT_NEUTRAL'))
# ##            pPlayer.setBroadAlignment(55)
# ##            pPlayer.setEthicalAlignment(getInfoType('ETHICAL_ALIGNMENT_LAWFUL'))
# ##            pPlayer.setBroadEthicalAlignment(370)
# ##            CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
# ##            CvMainInterface.CvMainInterface().updateScreen()
	# return

def getHelpTribalLawElectionBear(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)
	
	if pPlayer.getLeaderType() == getInfoType('LEADER_MOTSQUEH'):
            szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_BEAR_TRIBE_ALREADY_MOTSQUEH", ())
        else:
            szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_BEAR_TRIBE", ())
	return szHelp

# def doTribalLawElectionSerpent(argsList):
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# game 		= CyGame()
	# randNum 		= game.getSorenRandNum
	# setFeat 	= pPlayer.setFeatAccomplished

	# setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION1'), False)
        # setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION2'), False)
        # if pPlayer.getLeaderType() == getInfoType('LEADER_OSYKA'):
            # iOsykaChance = randNum(2, "Osyka Chance")
            # if iOsykaChance == 0:
		# CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_OSYKA_WINS_ALREADY_OSYKA_SUCCESS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		# pPlayer.initUnit(getInfoType('UNIT_COMMANDER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	    # elif iOsykaChance == 1:
                # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_OSYKA_WINS_ALREADY_OSYKA_FAIL", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
	    # pPlayer.changeAnarchyTurns(1)
        # else:
            # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_OSYKA_WINS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
            # pPlayer.changeLeader(getInfoType('LEADER_OSYKA'))
# ##            pPlayer.setAlignment(getInfoType('ALIGNMENT_EVIL'))
# ##            pPlayer.setBroadAlignment(-350)
# ##            pPlayer.setEthicalAlignment(getInfoType('ETHICAL_ALIGNMENT_NEUTRAL'))
# ##            pPlayer.setBroadEthicalAlignment(-120)
# ##            CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
# ##            CvMainInterface.CvMainInterface().updateScreen()
	# return

def getHelpTribalLawElectionSerpent(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)
	
	if pPlayer.getLeaderType() == getInfoType('LEADER_OSYKA'):
            szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_SERPENT_TRIBE_ALREADY_OSYKA", ())
        else:
            szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_SERPENT_TRIBE", ())
	return szHelp

# def doTribalLawElectionTortoise(argsList):
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# game 		= CyGame()
	# randNum 		= game.getSorenRandNum
	# setFeat 	= pPlayer.setFeatAccomplished

	# setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION1'), False)
        # setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION2'), False)
        # if pPlayer.getLeaderType() == getInfoType('LEADER_ALOSAKA'):
            # iAlosakaChance = randNum(2, "Alosaka Chance")
            # if iAlosakaChance == 0:
		# CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_ALOSAKA_WINS_ALREADY_ALOSAKA_SUCCESS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
		# pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())
	    # elif iAlosakaChance == 1:
                # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_ALOSAKA_WINS_ALREADY_ALOSAKA_FAIL", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
	    # pPlayer.changeAnarchyTurns(1)
        # else:
            # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_ALOSAKA_WINS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
            # pPlayer.changeLeader(getInfoType('LEADER_ALOSAKA'))
# ##            pPlayer.setAlignment(getInfoType('ALIGNMENT_GOOD'))
# ##            pPlayer.setBroadAlignment(315)
# ##            pPlayer.setEthicalAlignment(getInfoType('ETHICAL_ALIGNMENT_LAWFUL'))
# ##            pPlayer.setBroadEthicalAlignment(750)
# ##            CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
# ##            CvMainInterface.CvMainInterface().updateScreen()
	# return

def getHelpTribalLawElectionTortoise(argsList):
	kTriggeredData = argsList[1]
	iPlayer = gc.getGame().getActivePlayer()
	pPlayer = gc.getPlayer(iPlayer)
	
	if pPlayer.getLeaderType() == getInfoType('LEADER_ALOSAKA'):
            szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_TORTOISE_TRIBE_ALREADY_ALOSAKA", ())
        else:
            szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_TORTOISE_TRIBE", ())
	return szHelp
        
# def doTribalLawElectionFair(argsList):
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# game 		= CyGame()
	# randNum 		= game.getSorenRandNum
	# setFeat 	= pPlayer.setFeatAccomplished

	# (loopCity, iter) = pPlayer.firstCity(False)
	# while(loopCity):
		# loopCity.changeHappinessTimer(1)
		# (loopCity, iter) = pPlayer.nextCity(iter, False)
        # if pPlayer.isFeatAccomplished((getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION1'))):
            # setFeat((getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION2')), True)
        # else:
            # setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION1'), True)
	# iElectionResult = randNum(5, "Election Result") # The actual code is put here because we don't want fair elections to trigger anarchy
	# if   iElectionResult == 0: doTribalLawElectionEagle(argsList) # Shimasani can call her function because she does not have anarchy in her event
	# elif iElectionResult == 1:
            # if pPlayer.getLeaderType() == getInfoType('LEADER_SOYALA'):
                # iSoyalaChance = randNum(2, "Soyala Chance")
                # if iSoyalaChance == 0:
                    # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SOYALA_WINS_ALREADY_SOYALA_SUCCESS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
                    # pPlayer.initUnit(getInfoType('UNIT_ARTIST'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
                # elif iSoyalaChance == 1:
                    # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SOYALA_WINS_ALREADY_SOYALA_FAIL", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
            # else:
                # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_SOYALA_WINS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
                # pPlayer.changeLeader(getInfoType('LEADER_SOYALA'))
# ##                pPlayer.setAlignment(getInfoType('ALIGNMENT_NEUTRAL'))
# ##                pPlayer.setBroadAlignment(-130)
# ##                pPlayer.setEthicalAlignment(getInfoType('ETHICAL_ALIGNMENT_CHAOTIC'))
# ##                pPlayer.setBroadEthicalAlignment(-750)
# ##                CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
# ##                CvMainInterface.CvMainInterface().updateScreen()
        # elif iElectionResult == 2:
            # if pPlayer.getLeaderType() == getInfoType('LEADER_MOTSQUEH'):
                # iMotsquehChance = randNum(2, "Motsqueh Chance")
                # if iMotsquehChance == 0:
                    # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_MOTSQUEH_WINS_ALREADY_MOTSQUEH_SUCCESS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
                    # pPlayer.initUnit(getInfoType('UNIT_ENGINEER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
                # elif iMotsquehChance == 1:
                    # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_MOTSQUEH_WINS_ALREADY_MOTSQUEH_FAIL", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
            # else:
                # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_MOTSQUEH_WINS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
                # pPlayer.changeLeader(getInfoType('LEADER_MOTSQUEH'))
# ##                pPlayer.setAlignment(getInfoType('ALIGNMENT_NEUTRAL'))
# ##                pPlayer.setBroadAlignment(55)
# ##                pPlayer.setEthicalAlignment(getInfoType('ETHICAL_ALIGNMENT_LAWFUL'))
# ##                pPlayer.setBroadEthicalAlignment(370)
# ##                CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
# ##                CvMainInterface.CvMainInterface().updateScreen()
	# elif iElectionResult == 3:
            # if pPlayer.getLeaderType() == getInfoType('LEADER_OSYKA'):
                # iOsykaChance = randNum(2, "Osyka Chance")
                # if iOsykaChance == 0:
                    # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_OSYKA_WINS_ALREADY_OSYKA_SUCCESS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
                    # pPlayer.initUnit(getInfoType('UNIT_COMMANDER'), pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
                # elif iOsykaChance == 1:
                    # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_OSYKA_WINS_ALREADY_OSYKA_FAIL", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
            # else:
                # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_OSYKA_WINS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
                # pPlayer.changeLeader(getInfoType('LEADER_OSYKA'))
# ##                pPlayer.setAlignment(getInfoType('ALIGNMENT_EVIL'))
# ##                pPlayer.setBroadAlignment(-350)
# ##                pPlayer.setEthicalAlignment(getInfoType('ETHICAL_ALIGNMENT_NEUTRAL'))
# ##                pPlayer.setBroadEthicalAlignment(-120)
# ##                CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
# ##                CvMainInterface.CvMainInterface().updateScreen()
	# elif iElectionResult == 4:
            # if pPlayer.getLeaderType() == getInfoType('LEADER_ALOSAKA'):
                # iAlosakaChance = randNum(2, "Alosaka Chance")
                # if iAlosakaChance == 0:
                    # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_ALOSAKA_WINS_ALREADY_ALOSAKA_SUCCESS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
                    # pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength())
                # elif iAlosakaChance == 1:
                    # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_ALOSAKA_WINS_ALREADY_ALOSAKA_FAIL", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_RED"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
            # else:
                # CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_ALOSAKA_WINS", ()),'',1,'Modules/NormalModules/ChislevExpansion/Art/Buttons/Tribal_Law_Button.dds',getInfoType("COLOR_GREEN"),pPlayer.getCapitalCity().getX(),pPlayer.getCapitalCity().getY(),True,True)
                # pPlayer.changeLeader(getInfoType('LEADER_ALOSAKA'))
# ##                pPlayer.setAlignment(getInfoType('ALIGNMENT_GOOD'))
# ##                pPlayer.setBroadAlignment(315)
# ##                pPlayer.setEthicalAlignment(getInfoType('ETHICAL_ALIGNMENT_LAWFUL'))
# ##                pPlayer.setBroadEthicalAlignment(750)
# ##                CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, True)
# ##                CvMainInterface.CvMainInterface().updateScreen()
	# return

def getHelpTribalLawElectionFair(argsList):
    
         szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_FAIR", ())
         return szHelp        

# def doTribalLawElectionFair3(argsList):
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# setFeat 	= pPlayer.setFeatAccomplished

	# (loopCity, iter) = pPlayer.firstCity(False)
	# while(loopCity):
		# loopCity.changeHappinessTimer(5)
		# (loopCity, iter) = pPlayer.nextCity(iter, False)
        # setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION1'), False)
        # setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION2'), False)
        # doTribalLawElectionFair(argsList)
	# return

def getHelpTribalLawElectionFair3(argsList): ## Not programmed; switch to The Council
    
         szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_FAIR3", ())
         return szHelp
        
# def doTribalLawElectionNoParticipation(argsList): 
	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	# setFeat 	= pPlayer.setFeatAccomplished

	# setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION1'), False)
        # setFeat(getInfoType('FEAT_TRIBAL_LAW_FAIR_ELECTION2'), False)
	# pPlayer.changeAnarchyTurns(1)
	# return

def getHelpTribalLawElectionNoParticipation(argsList): ## 
    
         szHelp = localText.getText("TXT_KEY_EVENT_TRIBAL_LAW_ELECTION_HELP_NO_PARTICIPATION", ())
         return szHelp  

## Begin Menawa tribe selection
# def doMenawaTribeSelectionEagle(argsList):
    	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# setPromo           = pUnit.setHasPromotion
	
        # setPromo(getInfoType('PROMOTION_MENAWA_EAGLE_TRIBE'), True)

        # if pUnit.isHasPromotion(getInfoType('PROMOTION_MOBILITY1')):
            # setPromo(getInfoType('PROMOTION_MOBILITY2'), True)
        # else:
            # setPromo(getInfoType('PROMOTION_MOBILITY1'), True)
            
def getHelpMenawaTribeSelectionEagle(argsList):

        szHelp = localText.getText("TXT_KEY_EVENT_MENAWA_TRIBE_SELECTION_HELP_EAGLE_TRIBE", ())
        return szHelp
        
# def doMenawaTribeSelectionCoyote(argsList):
    	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# setPromo           = pUnit.setHasPromotion
	
	# setPromo(getInfoType('PROMOTION_MENAWA_COYOTE_TRIBE'), True)

        # if pUnit.isHasPromotion(getInfoType('PROMOTION_DRILL1')):
            # setPromo(getInfoType('PROMOTION_DRILL2'), True)
        # else:
            # setPromo(getInfoType('PROMOTION_DRILL1'), True)

def getHelpMenawaTribeSelectionCoyote(argsList):

        szHelp = localText.getText("TXT_KEY_EVENT_MENAWA_TRIBE_SELECTION_HELP_COYOTE_TRIBE", ())
        return szHelp

# def doMenawaTribeSelectionBear(argsList):
    	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# setPromo           = pUnit.setHasPromotion
	
	# setPromo(getInfoType('PROMOTION_MENAWA_BEAR_TRIBE'), True)

        # if pUnit.isHasPromotion(getInfoType('PROMOTION_COMBAT1')):
            # setPromo(getInfoType('PROMOTION_COMBAT2'), True)
        # else:
            # setPromo(getInfoType('PROMOTION_COMBAT1'), True)

def getHelpMenawaTribeSelectionBear(argsList):

        szHelp = localText.getText("TXT_KEY_EVENT_MENAWA_TRIBE_SELECTION_HELP_BEAR_TRIBE", ())
        return szHelp

# def doMenawaTribeSelectionSerpent(argsList):
    	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# setPromo           = pUnit.setHasPromotion
	
	# setPromo(getInfoType('PROMOTION_MENAWA_SERPENT_TRIBE'), True)

        # if pUnit.isHasPromotion(getInfoType('PROMOTION_CITY_RAIDER1')):
            # setPromo(getInfoType('PROMOTION_CITY_RAIDER2'), True)
        # else:
            # setPromo(getInfoType('PROMOTION_CITY_RAIDER1'), True)

def getHelpMenawaTribeSelectionSerpent(argsList):

        szHelp = localText.getText("TXT_KEY_EVENT_MENAWA_TRIBE_SELECTION_HELP_SERPENT_TRIBE", ())
        return szHelp
    
# def doMenawaTribeSelectionTortoise(argsList):
    	# kTriggeredData = argsList[1]
	# pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	# pUnit = pPlayer.getUnit(kTriggeredData.iUnitId)
	# setPromo           = pUnit.setHasPromotion
	
	# setPromo(getInfoType('PROMOTION_MENAWA_TORTOISE_TRIBE'), True)

        # if pUnit.isHasPromotion(getInfoType('PROMOTION_CITY_GARRISON1')):
            # setPromo(getInfoType('PROMOTION_CITY_GARRISON2'), True)
        # else:
            # setPromo(getInfoType('PROMOTION_CITY_GARRISON1'), True)

def getHelpMenawaTribeSelectionTortoise(argsList):

        szHelp = localText.getText("TXT_KEY_EVENT_MENAWA_TRIBE_SELECTION_HELP_TORTOISE_TRIBE", ())
        return szHelp
                    
# def doCivicNotTribalLawAbsaroke(argsList):
    	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	
        # pPlayer.changeLeader(getInfoType('LEADER_CHISLEV'))

def getHelpCivicNotTribalLawAbsaroke(argsList):

         szHelp = localText.getText("TXT_KEY_EVENT_CIVIC_NOT_TRIBAL_LAW_HELP_ABSAROKE", ())
         return szHelp
    
# def doCivicNotTribalLawNatane(argsList):
    	# kTriggeredData = argsList[1]
	# iPlayer = kTriggeredData.ePlayer
	# pPlayer = gc.getPlayer(iPlayer)
	
        # pPlayer.changeLeader(getInfoType('LEADER_NATANE'))

def getHelpCivicNotTribalLawNatane(argsList):

         szHelp = localText.getText("TXT_KEY_EVENT_CIVIC_NOT_TRIBAL_LAW_HELP_NATANE", ())
         return szHelp
        
##def doTraitTribalCohesion(argsList): ##For an old version of Tribal Cohesion that had an Insane-like system
##	iEvent = argsList[0]
##	kTriggeredData = argsList[1]
##	iPlayer = kTriggeredData.ePlayer
##	pPlayer = gc.getPlayer(iPlayer)
##	
##	for i in range(gc.getNumTraitInfos()):
##	    if pPlayer.hasTrait(i) and i != getInfoType('TRAIT_TRIBAL_COHESION') and i != getInfoType('TRAIT_TRIBAL_COHESION2') and i != getInfoType('TRAIT_TRIBAL_COHESION3'):
##		pPlayer.setHasTrait(i,False,-1,True,True)
##	cohesionTraits = [ 'TRAIT_AGGRESSIVE','TRAIT_CHARISMATIC','TRAIT_TRADER','TRAIT_CREATIVE','TRAIT_IMPERIALIST','TRAIT_EXPANSIVE','TRAIT_INDUSTRIOUS','TRAIT_PHILOSOPHICAL','TRAIT_RAIDERS','TRAIT_DEFENDER' ]
##	iRnd1 = CyGame().getSorenRandNum(len(cohesionTraits), "Tribal Cohesion")
##	iRnd2 = CyGame().getSorenRandNum(len(cohesionTraits), "Tribal Cohesion")
##	while iRnd2 == iRnd1:
##	    iRnd2 = CyGame().getSorenRandNum(len(cohesionTraits), "Tribal Cohesion")
##	iRnd3 = CyGame().getSorenRandNum(len(cohesionTraits), "Tribal Cohesion")
##	while iRnd3 == iRnd1 or iRnd3 == iRnd2:
##	    iRnd3 = CyGame().getSorenRandNum(len(cohesionTraits), "Tribal Cohesion")
##	pPlayer.setHasTrait(getInfoType(cohesionTraits[iRnd1]),True,-1,True,True)
##        pPlayer.setHasTrait(getInfoType(cohesionTraits[iRnd2]),True,-1,True,True)
##	pPlayer.setHasTrait(getInfoType(cohesionTraits[iRnd3]),True,-1,True,True)
##	
##	if pPlayer.hasTrait(getInfoType('TRAIT_TRIBAL_COHESION2')) or pPlayer.hasTrait(getInfoType('TRAIT_TRIBAL_COHESION3')):
##            iRnd4 = CyGame().getSorenRandNum(len(cohesionTraits), "Tribal Cohesion")    
##	    while iRnd4 == iRnd1 or iRnd4 == iRnd2 or iRnd4 == iRnd3:
##		iRnd4 = CyGame().getSorenRandNum(len(cohesionTraits), "Tribal Cohesion")
##	    pPlayer.setHasTrait(getInfoType(cohesionTraits[iRnd4]),True,-1,True,True)
##            if pPlayer.hasTrait(getInfoType('TRAIT_TRIBAL_COHESION3')):
##                iRnd5 = CyGame().getSorenRandNum(len(cohesionTraits), "Tribal Cohesion")
##                while iRnd5 == iRnd1 or iRnd5 == iRnd2 or iRnd5 == iRnd3 or iRnd5 == iRnd4:
##                    iRnd5 = CyGame().getSorenRandNum(len(cohesionTraits), "Tribal Cohesion")
##                pPlayer.setHasTrait(getInfoType(cohesionTraits[iRnd5]),True,-1,True,True)