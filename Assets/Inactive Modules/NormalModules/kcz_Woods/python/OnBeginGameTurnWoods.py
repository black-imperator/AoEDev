from CvPythonExtensions import *


def spawn_eert_forests():
    gc = CyGlobalContext()
    eert = gc.getInfoTypeForString("CIVILIZATION_EERT")
    # 1. Get Feature ID
    iFeatureNewForest = gc.getInfoTypeForString("FEATURE_FOREST_NEW")
    if iFeatureNewForest == -1:
        return  # Feature doesn't exist in XML

    # 2. Identify EERT Player ID(s)
    # We create a list in case multiple players are using the same Civ
    eert_player_ids = []
    for i in range(gc.getMAX_CIV_PLAYERS()):
        pPlayer = gc.getPlayer(i)
        if pPlayer.isAlive():
            civ_info = gc.getCivilizationInfo(pPlayer.getCivilizationType())
            if civ_info.getType() == "CIVILIZATION_EERT":
                eert_player_ids.append(i)

    if not eert_player_ids:
        return

    map = CyMap()
    game = CyGame()

    for iX in range(map.getGridWidth()):
        for iY in range(map.getGridHeight()):
            pPlot = map.plot(iX, iY)

            if pPlot.isCity() or pPlot.isPeak() or pPlot.isWater():
                continue

            iTotalCulture = pPlot.countTotalCulture()
            if iTotalCulture <= 0:
                continue

            iEertCulture = 0
            for iPlayer in eert_player_ids:
                iEertCulture += pPlot.getCulture(iPlayer)

            if iEertCulture <= 0:
                continue

            if pPlot.getFeatureType() != -1:
                iFeatureForest = gc.getInfoTypeForString("FEATURE_FOREST")
                iFeatureJungle = gc.getInfoTypeForString("FEATURE_JUNGLE")
                iFeatureAncientForest = gc.getInfoTypeForString("FEATURE_FOREST_ANCIENT")
                if pPlot.getFeatureType() in [iFeatureForest, iFeatureAncientForest, iFeatureJungle]:
                    iImprovement = pPlot.getImprovementType()
                    if iImprovement == -1 or gc.getImprovementInfo(iImprovement).isUnique():
                        continue
                    iImprovementClass = gc.getImprovementInfo(iImprovement).getImprovementClass()
                    if iImprovementClass in [gc.getInfoTypeForString("IMPROVEMENTCLASS_FORT"),
                                             gc.getInfoTypeForString("IMPROVEMENTCLASS_CASTLE"),
                                             gc.getInfoTypeForString("IMPROVEMENTCLASS_CITADEL")]:
                        continue
                    if (iImprovement != -1 and iImprovement !=
                            gc.getCivilizationInfo(eert).getCivilizationImprovements(iImprovementClass)):
                        if gc.getPlayer(pPlot.getOwner()).getCivilizationType() == eert:
                            if game.getSorenRandNum(100, "") < 20:
                                pPlot.setImprovementType(-1)
                continue

            if not pPlot.canHaveFeature(iFeatureNewForest):
                continue

            iInfluencePercent = (iEertCulture * 100) // iTotalCulture

            if iInfluencePercent <= 10:
                iChanceBP = 0
            elif iInfluencePercent >= 50:
                iChanceBP = 300  # 3% cap
            else:
                iChanceBP = ((iInfluencePercent - 10) * 300) // 40

            if iChanceBP > 0:
                if game.getSorenRandNum(10000, "Eert Forest Spawn") < iChanceBP:
                    pPlot.setFeatureType(iFeatureNewForest, 0)


def onBeginGameTurn(self, argsList):
    iGameTurn = argsList[0]

    spawn_eert_forests()
