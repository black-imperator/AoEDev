
from CvPythonExtensions import *
import PyHelpers
import CvEventInterface
import CvUtil
PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()
localText = CyTranslator()

def getHelpBlackDuke(argsList):
	ePromotion, pUnit = argsList
	git = gc.getInfoTypeForString

	iMelee1 = git('PROMOTION_BD_MELEE1')
	iMelee2 = git('PROMOTION_BD_MELEE2')
	iMelee3 = git('PROMOTION_BD_MELEE3')
	iRecon1 = git('PROMOTION_BD_RECON1')
	iRecon2 = git('PROMOTION_BD_RECON2')
	iRecon3 = git('PROMOTION_BD_RECON3')
	iArcher1 = git('PROMOTION_BD_ARCHER1')
	iMounted1 = git('PROMOTION_BD_MOUNTED1')
	iMounted2 = git('PROMOTION_BD_MOUNTED2')
	iAdept1 = git('PROMOTION_BD_ADEPT1')

	if pUnit == -1 or pUnit.isNone():
		szHelp = ""
	else:
		szHelp = ""
		if pUnit.isHasPromotion(iMelee1):	szHelp += localText.getText("TXT_KEY_PYHELP_BD_MELEE1", ())
		if pUnit.isHasPromotion(iMelee2):	szHelp += localText.getText("TXT_KEY_PYHELP_BD_MELEE2", ())
		if pUnit.isHasPromotion(iMelee3):	szHelp += localText.getText("TXT_KEY_PYHELP_BD_MELEE3", ())
		if pUnit.isHasPromotion(iRecon1):	szHelp += localText.getText("TXT_KEY_PYHELP_BD_RECON1", ())
		if pUnit.isHasPromotion(iRecon2):	szHelp += localText.getText("TXT_KEY_PYHELP_BD_RECON2", ())
		if pUnit.isHasPromotion(iRecon3):	szHelp += localText.getText("TXT_KEY_PYHELP_BD_RECON3", ())
		if pUnit.isHasPromotion(iArcher1):	szHelp += localText.getText("TXT_KEY_PYHELP_BD_ARCHER1", ())
		if pUnit.isHasPromotion(iMounted1):	szHelp += localText.getText("TXT_KEY_PYHELP_BD_MOUNTED1", ())
		if pUnit.isHasPromotion(iMounted2):	szHelp += localText.getText("TXT_KEY_PYHELP_BD_MOUNTED2", ())
		if pUnit.isHasPromotion(iAdept1):	szHelp += localText.getText("TXT_KEY_PYHELP_BD_ADEPT1", ())
	return szHelp