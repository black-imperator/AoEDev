
from CvPythonExtensions import *
import PyHelpers
import CvEventInterface
import CvUtil
PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()
localText = CyTranslator()

from BasicFunctions import *
#def wchoice(weighted_choices, log_message='Log message' ):
#	objects, frequences = zip( *weighted_choices )
#	addedFreq = []
#	lastSum = 0
#	for freq in frequences:
#		lastSum += freq
#		addedFreq.append(lastSum)
#	def choosing_function():
#		ballNumber = CyGame().getSorenRandNum(lastSum, log_message)
#		for index, subTotal in enumerate( addedFreq ):
#			if subTotal > ballNumber:
#				return objects[ index ]
#	return choosing_function

def canTriggerBlackDuke(argsList):
	for iPlayer in xrange(gc.getMAX_PLAYERS()):
		pLoopPlayer = gc.getPlayer(iPlayer)
		if pLoopPlayer.getUnitClassCount(gc.getInfoTypeForString("UNITCLASS_BLACK_DUKE"))>0:
			return False
	return True

def doBlackDuke1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	pPlayer = gc.getPlayer(kTriggeredData.ePlayer)
	pCity = pPlayer.getCity(kTriggeredData.iCityId)
	iUnit = gc.getInfoTypeForString('UNIT_BLACK_DUKE')
	newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	potentialClasses=[]
	potentialClasses = [('PROMOTION_BD_MELEE1', 1),('PROMOTION_BD_MELEE2', 1),('PROMOTION_BD_MELEE3', 1),('PROMOTION_BD_RECON1', 1),('PROMOTION_BD_RECON2', 1),('PROMOTION_BD_RECON3', 1),('PROMOTION_BD_ARCHER1', 1),('PROMOTION_BD_MOUNTED1', 1),('PROMOTION_BD_MOUNTED2', 1),('PROMOTION_BD_ADEPT1', 1)]
	getBlackDukeClass = wchoice( potentialClasses, 'Roll Black Duke class' )
	newUnit.setHasPromotion( gc.getInfoTypeForString( getBlackDukeClass() ), True )

	if newUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BD_ADEPT1')):
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING1'), True)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_CHANNELING2'), True)

def getHelpBlackDuke1(argsList):
	iEvent = argsList[0]
	kTriggeredData = argsList[1]
	szHelp = localText.getText("TXT_KEY_EVENT_BLACK_DUKE_HELP", ())
	return szHelp