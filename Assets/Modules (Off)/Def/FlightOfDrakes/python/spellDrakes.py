from CvPythonExtensions import *

gc = CyGlobalContext()
getInfoType = gc.getInfoTypeForString

Drakes = [
	getInfoType("UNIT_RED_DRAKE"),
	getInfoType("UNIT_WHITE_DRAKE"),
	getInfoType("UNIT_BRASS_DRAKE"),
	getInfoType("UNIT_BLACK_DRAKE")
]

BreathAttacks = [
	getInfoType("SPELL_BREATH_FIRE"),
	getInfoType("SPELL_BREATH_LIGHTNING"),
	getInfoType("SPELL_ICY_BREATH"),
	getInfoType("SPELL_SPIT_ACID")
]

def reqFormFlight(caster):
	pPlot = caster.plot()
	iUnitType = caster.getUnitType()
	numSameTypeDrakes = 0 # Will add self
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner() and pUnit.getUnitType() == iUnitType):
			numSameTypeDrakes += 1
	return numSameTypeDrakes >= 3

def spellFormFlight(caster):
	# The actual upgrading of the original unit is done in the XML,
	# so this code just kills the two lowest experienced drakes of the same type
	pPlot = caster.plot()
	iUnitType = caster.getUnitType()
	iID = caster.getID()
	sameTypeDrakes = [] # Will not include self
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner() and pUnit.getUnitType() == iUnitType and pUnit.getID() != iID):
			sameTypeDrakes.append(pUnit)
	sameTypeDrakes.sort(cmp = lambda a, b: a.getExperienceTimes100() - b.getExperienceTimes100())
	for i in range(2):
		if sameTypeDrakes[i].isImmortal():
			sameTypeDrakes[i].changeImmortal(-10)
		sameTypeDrakes[i].kill(True, 0)

def reqFormPrismaticFlight(caster):
	pPlot = caster.plot()
	iCasterUnitType = caster.getUnitType()
	if not iCasterUnitType in Drakes:
		return False
	for iDrakeType in Drakes:
		if iDrakeType == iCasterUnitType:
			continue
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner() and pUnit.getUnitType() == iDrakeType):
				break
		else:
			return False	
	return True

def spellFormPrismaticFlight(caster):
	# The actual upgrading of the original unit is done in the XML,
	# so this code just kills the lowest experienced drake of each different type
	pPlot = caster.plot()
	iCasterUnitType = caster.getUnitType()
	otherTypeDrakes = {}
	joiningDrakes = []
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		iUnitType = pUnit.getUnitType()
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner() and iUnitType in Drakes and iUnitType != iCasterUnitType):
			if not iUnitType in otherTypeDrakes:
				otherTypeDrakes[iUnitType] = []
			otherTypeDrakes[iUnitType].append(pUnit)
	for type in otherTypeDrakes:
		otherTypeDrakes[type].sort(cmp = lambda a, b: a.getExperienceTimes100() - b.getExperienceTimes100())
		joiningDrakes.append(otherTypeDrakes[type][0])
	for pUnit in joiningDrakes:
		if pUnit.isImmortal():
			pUnit.changeImmortal(-10)
		pUnit.kill(True, 0)

def spellPrismaticBreathFlight(pCaster):
	for iBreathAttack in BreathAttacks:
		pCaster.cast(iBreathAttack)