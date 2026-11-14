# Sid Meier's Civilization 4
# Frozen originally created by TC01
# Updated by Derf for Ashes of Erebus compatibility
# python amended to line up with modular format by LPlate

from CvPythonExtensions import *


def onCityDoTurn(self, argsList):
    'City Production'
    pCity = argsList[0]
    iPlayer = argsList[1]
    map = CyMap()

    gc = CyGlobalContext()
    cf = self.cf
    getInfoType = gc.getInfoTypeForString
    pPlot = pCity.plot()
    iPlayer = pCity.getOwner()
    getPlayer = gc.getPlayer
    pPlayer = getPlayer(iPlayer)
    numB = pCity.getNumBuilding
    git = gc.getInfoTypeForString
    iNoAI = UnitAITypes.NO_UNITAI
    iSouth = DirectionTypes.DIRECTION_SOUTH

    map = CyMap()
    iX = pCity.getX()
    iY = pCity.getY()

    if pCity.getNumBuilding(getInfoType("BUILDING_GIANT_FLYTRAPS")) > 0:
        iHeroPromo = getInfoType("PROMOTION_HERO")

        iOwner = pCity.getOwner()
        pTeam = gc.getTeam(pCity.getTeam())

        pPlot = pCity.plot()

        potential_victims = []

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue

                pLoopPlot = map.plot(pPlot.getX() + dx, pPlot.getY() + dy)

                if not pLoopPlot.isNone():
                    for i in range(pLoopPlot.getNumUnits()):
                        pUnit = pLoopPlot.getUnit(i)

                        if pTeam.isAtWar(pUnit.getTeam()):
                            if not pUnit.isHasPromotion(iHeroPromo):
                                potential_victims.append(pUnit)

        if not potential_victims:
            return

        best_score = 9999999

        for unit in potential_victims:

            iScore = (unit.getLevel() * 1000) + unit.currHitPoints()

            if iScore < best_score:
                best_score = iScore
                best_candidate = unit

        if best_score < 9999999:
            sUnitName = best_candidate.getName()
            sCityName = pCity.getName()
            iVictimOwner = best_candidate.getOwner()

            best_candidate.kill(True, iOwner)
            pCity.changeFood(10)
            CyInterface().addMessage(
                iOwner, True, 20,
                "Hostile %s killed by Giant Flytraps in %s!" % (sUnitName, sCityName),
                "AS2D_COMBAT", 0, best_candidate.getButton(),
                ColorTypes(gc.getInfoTypeForString("COLOR_GREEN")),
                pCity.getX(), pCity.getY(), True, True
            )

            if iVictimOwner != -1:
                CyInterface().addMessage(
                    iVictimOwner, True, 20,
                    "Your %s was killed by Giant Flytraps in %s!" % (sUnitName, sCityName),
                    "AS2D_UNIT_DEATH", 0, best_candidate.getButton(),
                    ColorTypes(gc.getInfoTypeForString("COLOR_RED")),
                    pCity.getX(), pCity.getY(), True, True
                )

    if pCity.getNumBuilding(getInfoType("BUILDING_ROOT_WALLS")) > 0:
        iMaxDefense = pCity.getTotalDefense(False)
        walldamareregen = 3
        if pCity.getNumBuilding(getInfoType("BUILDING_THORNROOT_WALLS")) > 0:
            walldamareregen = walldamareregen + 5
        damage = pCity.getDefenseDamage()
        if damage > 0 and iMaxDefense > 0:
            walldamareregen = walldamareregen * 100 // iMaxDefense
            if damage > walldamareregen:
                pCity.changeDefenseDamage(-walldamareregen)
            else:
                pCity.changeDefenseDamage(-damage)

    if numB(getInfoType("BUILDING_CRIME_FOREST_FIRES")) > 0:
        setForestOnFire = CyGame().getSorenRandNum(100, "")
        if setForestOnFire >= 95:
            iForest = git("FEATURE_FOREST")
            iAForest = git("FEATURE_FOREST_ANCIENT")
            plotList = []
            iCultureRange = pCity.getCultureLevel()
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if iX + dx < 0 or iX + dx >= map.getGridWidth() or iY + dy < 0 or iY + dy >= map.getGridHeight() or dx + dy > iCultureRange + 1:
                        continue
                    plot = map.plot(iX + dx, iY + dy)
                    if plot.getOwner() == iPlayer:
                        feature = plot.getFeatureType()
                        if feature == iForest or feature == iAForest:
                            plotList.append(plot)
            if len(plotList) > 0:
                r = CyGame().getSorenRandNum(len(plotList), "")
                plotList[r].setFeatureType(git("FEATURE_FOREST_BURNT"), 0)
                CyInterface().addMessage(iPlayer, True, 25, 'forest burned due to Forest Fires', '', 2,
                                         'Art/interface/buttons/terrainfeatures/flames.dds', ColorTypes(8),
                                         plotList[r].getX(), plotList[r].getY(), True, True)

        if numB(getInfoType("BUILDING_CRIME_UNCONTROLLED_VEGETATION")) > 0:
            vegetationRandValue = CyGame().getSorenRandNum(100, "")
            iForest = git("FEATURE_FOREST")
            iAForest = git("FEATURE_FOREST_ANCIENT")
            iJungle = git("FEATURE_JUNGLE")
            iCultureRange = pCity.getCultureLevel()
            plotList = []
            if vegetationRandValue >= 95:
                iCultureRange = pCity.getCultureLevel()
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        if iX + dx < 0 or iX + dx >= map.getGridWidth() or iY + dy < 0 or iY + dy >= map.getGridHeight() or dx + dy > iCultureRange + 1:
                            continue
                        plot = map.plot(iX + dx, iY + dy)
                        if plot.getOwner() == iPlayer:
                            feature = plot.getFeatureType()
                            if feature == iForest or feature == iJungle:
                                plotList.append(plot)
                if len(plotList) > 0:
                    r = CyGame().getSorenRandNum(len(plotList), "")
                    plotList[r].setFeatureType(git("FEATURE_FOREST_ANCIENT"), 0)
            elif vegetationRandValue <= 2:
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        if iX + dx < 0 or iX + dx >= map.getGridWidth() or iY + dy < 0 or iY + dy >= map.getGridHeight() or dx + dy > iCultureRange + 1:
                            continue
                        plot = map.plot(iX + dx, iY + dy)
                        if plot.getOwner() == iPlayer:
                            feature = plot.getFeatureType()
                            if feature == iForest or feature == iJungle or feature == iAForest:
                                plotList.append(plot)

                if len(plotList) > 0:
                    r = CyGame().getSorenRandNum(len(plotList), "")
                    CyInterface().addMessage(iPlayer, True, 25, str(r), '', 2,
                                             '', ColorTypes(8),
                                             iX, iY, True, True)
                    iDemonPlayer = gc.getDEMON_PLAYER()
                    pDemonPlayer = gc.getPlayer(iDemonPlayer)
                    newUnit = pDemonPlayer.initUnit(git('UNIT_GUARDIAN_VINES'), plotList[r].getX(),
                                                    plotList[r].getY(), UnitAITypes.NO_UNITAI,
                                                    DirectionTypes.DIRECTION_SOUTH)
                    newUnit.setHasPromotion(git('PROMOTION_IMMOBILE_PLANT'), True)
                    CyInterface().addMessage(iPlayer, True, 25, 'Hostile plants grow in the area', '', 2,
                                             'Art/interface/buttons/units/guardian vines.dds', ColorTypes(8),
                                             plotList[r].getX(), plotList[r].getY(), True, True)
