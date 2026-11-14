from CvPythonExtensions import *

gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString


def spellNaturesCall(pCaster):
    map = CyMap()
    player = pCaster.getOwner()

    iNumPlots = map.numPlots()
    iForest = getInfoType("FEATURE_FOREST")
    iJungle = getInfoType("FEATURE_JUNGLE")
    iAForest = getInfoType("FEATURE_FOREST_ANCIENT")
    for i in range(0, iNumPlots):
        plot = map.plotByIndex(i)
        feature = plot.getFeatureType()
        if feature == iForest or feature == iJungle:
            r = CyGame().getSorenRandNum(100, "")
            if plot.getOwner() == player:
                if r >= 20:
                    plot.setFeatureType(iAForest, 0)
            elif r >= 80:
                plot.setFeatureType(iAForest, 0)

def reqSpreadForest(pCaster):
    map = CyMap()
    pPlot = pCaster.plot()
    iX = pPlot.getX()
    iY = pPlot.getY()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if iX + dx < 0 or iX + dx >= map.getGridWidth() or iY + dy < 0 or iY + dy >= map.getGridHeight():
                continue
            feature = pPlot.getFeatureType()
            if feature == -1:
                if pPlot.getImprovementType() == -1:
                    if pPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") or pPlot.getTerrainType() != getInfoType(
                            "TERRAIN_COAST"):
                        return True
    return False


def spellSpreadForest(pCaster):
    map = CyMap()
    pPlot = pCaster.plot()
    iX = pPlot.getX()
    iY = pPlot.getY()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if iX + dx < 0 or iX + dx >= map.getGridWidth() or iY + dy < 0 or iY + dy >= map.getGridHeight() or (dx==dy and dy==0):
                continue
            feature = pPlot.getFeatureType()
            if feature == -1:
                if pPlot.getImprovementType() == -1:
                    if pPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") or pPlot.getTerrainType() != getInfoType(
                            "TERRAIN_COAST"):
                        pPlot.setFeatureType(getInfoType("FEATURE_FOREST_NEW"), 1)

def reqSpreadForestGreater(pCaster):
    map = CyMap()
    pPlot = pCaster.plot()
    iX = pPlot.getX()
    iY = pPlot.getY()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if iX + dx < 0 or iX + dx >= map.getGridWidth() or iY + dy < 0 or iY + dy >= map.getGridHeight():
                continue
            feature = pPlot.getFeatureType()
            if feature == -1:
                if pPlot.getImprovementType() == getInfoType("FOREST_ANCIENT"):
                    if pPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") or pPlot.getTerrainType() != getInfoType(
                            "TERRAIN_COAST"):
                        return True
    return False
def spellSpreadForestGreater(pCaster):
    map = CyMap()
    pPlot = pCaster.plot()
    iX = pPlot.getX()
    iY = pPlot.getY()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if iX + dx < 0 or iX + dx >= map.getGridWidth() or iY + dy < 0 or iY + dy >= map.getGridHeight():
               continue
            feature = pPlot.getFeatureType()

            if feature == -1:
                if pPlot.getImprovementType() != getInfoType("FEATURE_FOREST_ANCIENT"):
                    if pPlot.getTerrainType() != getInfoType("TERRAIN_OCEAN") or pPlot.getTerrainType() != getInfoType(
                            "TERRAIN_COAST"):
                        pPlot.setFeatureType(getInfoType("FEATURE_FOREST_ANCIENT"), 1)

def spellFuryOfNature(pCaster):
    lAnimalList = ["UNIT_WOLF", "UNIT_BOAR", "UNIT_PEGASUS", "UNIT_GORILLA", "UNIT_LION", "UNIT_BEES", "UNIT_BEAR",
                   "UNIT_SPIDER", "UNIT_BRASS_DRAKE"]
    iLevel = pCaster.getLevel()
    pPlayer = gc.getPlayer(pCaster.getOwner())
    spawnedType = CyGame().getSorenRandNum(min(len(lAnimalList), iLevel//2 + 1), "")
    newUnit = pPlayer.initUnit(getInfoType(lAnimalList[spawnedType]), pCaster.getX(), pCaster.getY(),
                               UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
    newUnit.setDuration(3)
    newUnit.setHasPromotion(getInfoType("PROMOTION_MARKSMAN"), True)
    newUnit.setHasPromotion(getInfoType("PROMOTION_FREE_UNIT"), True)
    newUnit.setHasPromotion(getInfoType("PROMOTION_SUMMONED_ANIMAL"), True)