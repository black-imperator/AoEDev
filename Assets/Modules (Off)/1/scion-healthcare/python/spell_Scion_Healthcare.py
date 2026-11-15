import CvPythonExtensions

gc = CvPythonExtensions.CyGlobalContext()

def patriaAffinity(pCaster):
    pPlayer = gc.getPlayer( pCaster.getOwner() )
    if pPlayer.getNumCities():
        pCapital = pPlayer.getCapitalCity()
        numPatrianArtifacts = pPlayer.getNumAvailableBonuses( gc.getInfoTypeForString('BONUS_PATRIAN_ARTIFACTS') )

        strengthAffinity = 0.
        strengthAffinity += .1  * pCapital.getPopulation()
        strengthAffinity += .75 * numPatrianArtifacts
        strengthAffinity += pPlayer.countHolyCities()
##        strengthAffinity += pPlayer.countTotalCulture()
##        strengthAffinity += pPlayer.getCitiesLost()
##        strengthAffinity += pPlayer.getGreatPeopleCreated()
##        strengthAffinity += pPlayer.getHighestUnitLevel()

        idAffinity = gc.getInfoTypeForString( 'PROMOTION_STRENGTH_OF_PATRIA_EFFECT' )

        changeAffinity = int( strengthAffinity ) - pCaster.countHasPromotion( idAffinity )
        if changeAffinity < 0:
            for _ in xrange( -changeAffinity ):
                pCaster.setHasPromotion(idAffinity, False)
        else:
            for _ in xrange( changeAffinity ):
                pCaster.setHasPromotion(idAffinity, True)