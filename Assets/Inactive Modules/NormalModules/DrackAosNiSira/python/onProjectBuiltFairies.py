## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Implementaion of miscellaneous game functions

import CvUtil
from CvPythonExtensions import *
from BasicFunctions import *
import CvEventInterface
import ScenarioFunctions

## *******************
## Modular Python: ANW 16-feb-2010
##					 29-may-2010
##					 20-aug-2010
## ArcticNightWolf on CivFanatics
## ArcticNightWolf@gmail.com

# For dynamic plugin loading
import imp	# dynamic importing of libraries
#import glob   # Unix style pathname pattern expansion
import os
import CvPath # path to current assets
import inspect

def getCitiesOfPlayer(pPlayer):
	(pCity, iter) = pPlayer.firstCity(False)
	cities = []
	
	while(pCity):
		cities.append(pCity)
		# Set Next City
		(pCity, iter) = pPlayer.nextCity(iter, False)
  
	return cities

def onMisrakConvertAllSoulsProjectBuilt(self, argsList):
	'Project Completed'
	pCity, iProjectType = argsList
	gc = CyGlobalContext()
	git = gc.getInfoTypeForString
	getPlayer = gc.getPlayer
	iPlayer = pCity.getOwner()
	pPlayer = getPlayer(iPlayer)
 
	# Define the ritual-to-SoulCost mapping
	ritualCostMap = {
		git("PROJECT_FAIRY_CONVERT_SOULS1"): {"soulCost": 10, "minSize": 0, "maxSize": 4},
		git("PROJECT_FAIRY_CONVERT_SOULS2"): {"soulCost": 25, "minSize": 5, "maxSize": 15},
		git("PROJECT_FAIRY_CONVERT_SOULS3"): {"soulCost": 100, "minSize": 16, "maxSize": 100},
	}
 
	cities = getCitiesOfPlayer(pPlayer)
	# Sort cities by population (ascending)
	cities.sort(key=lambda city: city.getPopulation())
 
	# Process each city starting from lowest population
	for city in cities:
		currentPopulation = city.getPopulation()
		currentSoulsOfPlayer = pPlayer.getCivCounter()

		# Find the appropriate ritual info based on population
		ritualInfo = None
		for info in ritualCostMap.values():
			if info["minSize"] <= currentPopulation <= info["maxSize"]:
				ritualInfo = info
				break

		if ritualInfo is None:
			continue

		ritualSoulCost = ritualInfo["soulCost"]
		# Check if Player has enough Souls
		if currentSoulsOfPlayer < ritualSoulCost:
			break

		# Remove Souls from CivCounter
		pPlayer.changeCivCounter(-ritualSoulCost)

		# Increase Population of city by 1
		city.changePopulation(1)
	

def onMisrakConvertSoulsProjectBuilt(self, argsList):
	'Project Completed'
	pCity, iProjectType = argsList
	gc = CyGlobalContext()
	git = gc.getInfoTypeForString
	getPlayer = gc.getPlayer
	iPlayer = pCity.getOwner()
	pPlayer = getPlayer(iPlayer)
	
	# Define the ritual-to-SoulCost mapping
	ritualCostMap = {
		git("PROJECT_FAIRY_CONVERT_SOULS1"): {"soulCost": 10},
		git("PROJECT_FAIRY_CONVERT_SOULS2"): {"soulCost": 25},
		git("PROJECT_FAIRY_CONVERT_SOULS3"): {"soulCost": 100},
	}
	
	# Check if the ritual is in the mapping
	if iProjectType not in ritualCostMap:
		return  # Ritual not recognized, do nothing

	# Get the soul cost associated with the ritual
	ritualInfo = ritualCostMap[iProjectType]
	ritualSoulCost = ritualInfo["soulCost"]

	# Check if Player has enough Souls
	currentSoulsOfPlayer = pPlayer.getCivCounter()
	if currentSoulsOfPlayer < ritualSoulCost:
		# Notify the player that they don't have enough souls
		CyInterface().addMessage(iPlayer, False, 15, CyTranslator().getText("TXT_KEY_PROJECT_FAIRY_CONVERT_SOULS_NOT_ENOUGH_SOULS", (ritualSoulCost, currentSoulsOfPlayer,)), "", 3, "", ColorTypes(7), -1, -1, True, True)
		return  # Exit if not enough souls

	# Remove Souls from CivCounter
	pPlayer.changeCivCounter(-ritualSoulCost)

	# Increase Population of city by 1
	pCity.changePopulation(1)

def onProjectBuilt(self, argsList):
	'Project Completed'
	pCity, iProjectType = argsList

	gc			= CyGlobalContext() 
	git			= gc.getInfoTypeForString
	getPlayer	= gc.getPlayer
	iPlayer		= pCity.getOwner()
	pPlayer		= getPlayer(iPlayer)
	
	projectHouseFane	= git("PROJECT_FAIRY_INVITE_HOUSE_FANE")
	projectHouseDawar	= git("PROJECT_FAIRY_INVITE_HOUSE_DAWAR")
	projectHousePesna	= git("PROJECT_FAIRY_INVITE_HOUSE_PESNA")
	projectHouseRakiri	= git("PROJECT_FAIRY_INVITE_HOUSE_RAKIRI")
	projectHouseWai		= git("PROJECT_FAIRY_INVITE_HOUSE_WAI")
	projectHouseNairu	= git("PROJECT_FAIRY_INVITE_HOUSE_NAIRU")
	projectHouseGodara	= git("PROJECT_FAIRY_INVITE_HOUSE_GODARA")
	projectHouseAstra	= git("PROJECT_FAIRY_INVITE_HOUSE_ASTRA")
	
	projectConvertSouls1 = git("PROJECT_FAIRY_CONVERT_SOULS1")
	projectConvertSouls2 = git("PROJECT_FAIRY_CONVERT_SOULS2")
	projectConvertSouls3 = git("PROJECT_FAIRY_CONVERT_SOULS3")
	projectConvertAllSouls = git("PROJECT_FAIRY_CONVERT_ALL_SOULS")
 
	projectConvertSouls = [projectConvertSouls1, projectConvertSouls2, projectConvertSouls3]
  
	if iProjectType in projectConvertSouls:
		onMisrakConvertSoulsProjectBuilt(self, argsList)
		return

	if iProjectType == projectConvertAllSouls:
		onMisrakConvertAllSoulsProjectBuilt(self, argsList)
		return
  
	if iProjectType == projectHouseFane:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_FANE"), True)
	elif iProjectType == projectHouseDawar:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_DAWAR"), True)
	elif iProjectType == projectHousePesna:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_PESNA"), True)
	elif iProjectType == projectHouseRakiri:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_RAKIRI"), True)
	elif iProjectType == projectHouseWai:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_WAI"), True)
	elif iProjectType == projectHouseNairu:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_NAIRU"), True)
	elif iProjectType == projectHouseGodara:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_GODARA"), True)
	elif iProjectType == projectHouseAstra:
		pPlayer.setHasTrait(git("TRAIT_HOUSE_ASTRA"), True)
	