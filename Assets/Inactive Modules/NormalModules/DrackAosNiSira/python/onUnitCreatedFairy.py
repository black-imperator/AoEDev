import CvUtil
from CvPythonExtensions import *
import PyHelpers
PyPlayer = PyHelpers.PyPlayer

gc		  = CyGlobalContext()
git			= gc.getInfoTypeForString

import CustomFunctions
cf = CustomFunctions.CustomFunctions()

def onUnitCreated(self, argsList):
	'Unit Completed'
	pUnit = argsList[0]
	getRandNum	= CyGame().getSorenRandNum
 
	# Check if the unit has the Fairy Race promotion
	if pUnit.isHasPromotion(git('PROMOTION_RACE_FAIRY')) or pUnit.isHasPromotion(git('PROMOTION_SIRA')):
		# List of possible Fairy promotions
		fairy_promotions = [
			git('PROMOTION_FAIRY_RED'),
			git('PROMOTION_FAIRY_WHITE'),
			git('PROMOTION_FAIRY_PURPLE'),
			git('PROMOTION_FAIRY_GREEN'),
			git('PROMOTION_FAIRY_CLEAR'),
			git('PROMOTION_FAIRY_BLUE'),
			git('PROMOTION_FAIRY_GOLDEN'),
			git('PROMOTION_FAIRY_DARK')
		]

		 # Check if the unit already has any Fairy Extra Promotion
		has_fairy_extra_promotion = False
		for promotion in fairy_promotions:
			if pUnit.isHasPromotion(promotion):
				has_fairy_extra_promotion = True
				break

		# If the unit doesn't have any Fairy Extra Promotion, grant one
		if not has_fairy_extra_promotion:
			selected_promotion = fairy_promotions[getRandNum(len(fairy_promotions), "Pick Fairy Promotion")]
			pUnit.setHasPromotion(selected_promotion, True)
  
  