import CvUtil
from CvPythonExtensions import *
import PyHelpers
PyPlayer = PyHelpers.PyPlayer

gc		  = CyGlobalContext()
git			= gc.getInfoTypeForString

import CustomFunctions
cf = CustomFunctions.CustomFunctions()

# Auto Clan Promotions for Vampire Units based on Clan Trait
def onUnitCreated(self, argsList):
	'Unit Completed'
	pUnit = argsList[0]
	iPlayer = pUnit.getOwner()
	cyPlayer = gc.getPlayer(iPlayer)  # Get the CyPlayer object

	# Define the traits and promotions you want to check
	pClanFlauros 		= git("PROMOTION_VAMP_CLAN_FLAUROS")
	pClanRavana			= git("PROMOTION_VAMP_CLAN_RAVANA")
	
	tClanFlauros		= git("TRAIT_VAMP_CLAN_FLAUROS")
	tClanRavana			= git("TRAIT_VAMP_CLAN_RAVANA")
	
	vamp_clan_traits = [tClanFlauros, tClanRavana]
	vamp_clan_promotions = {
		tClanFlauros: pClanFlauros,
		tClanRavana: pClanRavana
	}
 
	# Check if the leader has any of the vamp clan traits
	leader_trait = None
	for trait in vamp_clan_traits:
		if cyPlayer.hasTrait(trait):
			leader_trait = trait
			break
		
	if not leader_trait:
		return  # No relevant trait found
	
	# Check if the unit already has a clan promotion
	for promo in vamp_clan_promotions.values():
		if pUnit.isHasPromotion(promo):
			return  # Unit already has a clan promotion
	
	# Check if the unit is a vampire
	if not pUnit.isHasPromotion(git("PROMOTION_VAMPIRE")):
		return  # Unit is not a vampire

	# Assign the correct clan promotion based on the leader's trait
	correct_promo = vamp_clan_promotions[leader_trait]
	pUnit.setHasPromotion(correct_promo, True)