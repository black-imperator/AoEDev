# FoxTools.py
# 2010 Fredrik 'Grey Fox' Henriksson

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import PyHelpers
import CvEventInterface

# GLOBALS
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer

# Grey Fox Tools (RifE)
class FoxTools:

	def __init__(self):
		self.Defines            = {}
		self.Eras               = {}
		self.Techs              = {}
		self.Victories          = {}
		self.GameSpeeds         = {}
		self.GameOptions        = {}
		self.EventTriggers      = {}

		self.Civilizations      = {}
		self.Leaders            = {}
		self.LeaderStatus       = {}
		self.Traits             = {}
		self.Civics             = {}
		self.Religions          = {}
		self.Corporations       = {}
		self.Alignments         = {}

		# Buildings, etc
		self.Projects           = {}
		self.Buildings          = {}
		self.Specialists        = {}
		self.BuildingClasses    = {}
		self.Processes          = {}

		# Terrain, etc
		self.Terrain            = {}
		self.Feature            = {}
		self.Mana               = {}
		self.Resources          = {}
		self.WorldSizes         = {}
		self.Goodies            = {}

		# Improvements, etc
		self.Builds             = {}
		self.Lairs              = {}
		self.ManaNodes          = {}
		self.Improvements       = {}
		self.CivImprovements    = {}
		self.UniqueImprovements = {}

		# Units, etc
		self.Units              = {}
		self.Heroes             = {}
		self.UnitAI             = {}
		self.Promotions         = {}
		self.UnitClasses        = {}
		self.UnitCombats        = {}
		self.GreatPeople        = {}
		self.DamageTypes        = {}

		# Dynamic Traits Popup
		self.popupMsg           = {}

	def initialize(self):
		'Initialize the Dictionaries'
		self.initDefineDict()
		self.initEraDict()
		self.initTechDict()
		self.initVictoryDict()
		self.initGameSpeedDict()
		self.initGameOptionDict()
		self.initEventTriggerDict()
		self.initCivilizationDict()
		self.initLeaderDict()
		self.initLeaderStatusDict()
		self.initCivicDict()
		self.initTraitDict()
		self.initReligionDict()
		self.initCorporationDict()
		self.initAlignmentDict()
		self.initTerrainDict()
		self.initFeatureDict()
		self.initManaDict()
		self.initResourcesDict()
		self.initWorldSizesDict()
		self.initProjectDict()
		self.initBuildingDict()
		self.initBuildingClassDict()
		self.initLairDict()
		self.initManaNodeDict()
		self.initImprovementDict()
		self.initCivImprovementDict()
		self.initUniqueImprovementDict()
		self.initUnitDict()
		self.initHeroesDict()
		self.initUnitAIDict()
		self.initPromotionDict()
		self.initUnitClassDict()
		self.initUnitCombatDict()
		self.initGreatPeopleDict()
		self.initBuildDict()
		self.initSpecialistDict()
		self.initProcessesDict()
		self.initGoodyDict()
		self.initDamageTypesDict()

	def getPopupMsg(self, index):
		List = []
		if self.popupMsg.has_key(index):
			List = self.popupMsg[index]
		return List

	def addPopupMsg(self, index, szText, szArt ):
		List = []
		if self.popupMsg.has_key(index):
			List = self.popupMsg[index]
		List.append( [ szText, szArt ] )
		self.popupMsg[index] = List

	def showTraitPopup(self):
		Lost    = self.getPopupMsg("Lost")
		Gained  = self.getPopupMsg("Gained")
		iLen    = 0
		iLen    += len(Lost)
		iLen    += len(Gained)

		if iLen == 0: return

		szTitle = CyGameTextMgr().getTimeStr(CyGame().getGameTurn(), false)
		popup = PyPopup.PyPopup(-1)

		popup.setHeaderString(szTitle)

		iCount = 0
		if len(Gained) > 0:
			szArt = 'art/interface/popups/TraitsGained.dds'
			popup.addDDS(szArt, 0, 0, 48, 344)
			for msg, art in Gained:
				# popup.addSeparator()
				popup.setBodyString(msg)
				iCount += 1
			popup.addSeparator()

		iCount = 0
		if len(Lost) > 0:
			szArt = 'art/interface/popups/TraitsLost.dds'
			popup.addDDS(szArt, 0, 0, 48, 344)
			for msg, art in Lost:
				# popup.addSeparator()
				popup.setBodyString(msg)
				iCount += 1

		self.popupMsg = {}
		popup.launch(true, PopupStates.POPUPSTATE_IMMEDIATE)

	def getDefineDict(self): return self.Defines
	def initDefineDict(self):
		gc = CyGlobalContext()
		getDefineINT = gc.getDefineINT
		Define = {}
		Define["Flame Spread"]      = getDefineINT('FLAMES_SPREAD_CHANCE')
		Define["Planar Gate"]       = getDefineINT('PLANAR_GATE_CHANCE')
		Define["Start Year"]        = getDefineINT("START_YEAR")
		Define["Gone to Hell"]      = getDefineINT("GONE_TO_HELL_THRESHOLD_PERCENTAGE")
		Define["Order Spawn"]       = getDefineINT("ORDER_SPAWN_CHANCE")
		Define["Crusade Spawn"]     = getDefineINT("CRUSADE_SPAWN_CHANCE")
		Define["Apocalypse Kill"]   = getDefineINT('APOCALYPSE_KILL_CHANCE')
		Define["Hellfire Chance"]   = getDefineINT('HELLFIRE_CHANCE')
		Define["Wrath Convert"]     = getDefineINT('WRATH_CONVERT_CHANCE')
		self.Defines = Define

	def getEventTriggerDict(self): return self.EventTriggers
	def initEventTriggerDict(self):
		gc       = CyGlobalContext()
		eTrigger = gc.getEventTriggerInfo
		iNum     = gc.getNumEventTriggerInfos()
		findInfo = CvUtil.findInfoTypeNum

		Event = {}
#		Event["Adaptive"]               = findInfo(eTrigger, iNum,'EVENTTRIGGER_TRAIT_ADAPTIVE')
#		Event["Insane"]                 = findInfo(eTrigger, iNum,'EVENTTRIGGER_TRAIT_INSANE')

#		Event["Aggressive"]             = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_AGGRESSIVE_TRAIT')
#		Event["Arcane"]                 = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_ARCANE_TRAIT')
#		Event["Creative"]               = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_CREATIVE_TRAIT')
#		Event["Expansive"]              = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_EXPANSIVE_TRAIT')
#		Event["Financial"]              = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_FINANCIAL_TRAIT')
#		Event["Industrious"]            = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_INDUSTRIOUS_TRAIT')
#		Event["Ingenuity"]              = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_INGENUITY_TRAIT')
#		Event["Magic Resistant"]        = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_MAGIC_RESISTANT_TRAIT')
#		Event["Organized"]              = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_ORGANIZED_TRAIT')
#		Event["Philosophical"]          = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_PHILOSOPHICAL_TRAIT')
#		Event["Raiders"]                = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_RAIDERS_TRAIT')
#		Event["Spiritual"]              = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_SPIRITUAL_TRAIT')
#		Event["Summoner"]               = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_SUMMONER_TRAIT')
#		Event["Swashbuckler"]           = findInfo(eTrigger, iNum,'EVENTTRIGGER_ADD_SWASHBUCKLER_TRAIT')

#		Event["Godslayer"]              = findInfo(eTrigger, iNum,'EVENTTRIGGER_GODSLAYER')
#		Event["GodslayerFrozen"]              = findInfo(eTrigger, iNum,'EVENTTRIGGER_GODSLAYER_FROZEN')

		# Republic Elections
#		Event["Hawk vs Dove"]           = findInfo(eTrigger, iNum,'EVENTTRIGGER_REPUBLIC_ELECTION_HAWK_VS_DOVE')
#		Event["Landowner vs Peasant"]   = findInfo(eTrigger, iNum,'EVENTTRIGGER_REPUBLIC_ELECTION_LANDOWNER_VS_PEASANTS')
#		Event["Church vs State"]        = findInfo(eTrigger, iNum,'EVENTTRIGGER_REPUBLIC_ELECTION_CHURCH_VS_STATE')
#		Event["Labor vs Academia"]      = findInfo(eTrigger, iNum,'EVENTTRIGGER_REPUBLIC_ELECTION_LABOR_VS_ACADEMIA')

		# Exploration
#		Event["Lair Portal"]            = findInfo(eTrigger, iNum,'EVENTTRIGGER_EXPLORE_LAIR_PORTAL')
#		Event["Dwarf vs Lizardmen"]     = findInfo(eTrigger, iNum,'EVENTTRIGGER_EXPLORE_LAIR_DWARF_VS_LIZARDMEN')
#		Event["Goblin Red Yellow"]     = findInfo(eTrigger, iNum,'EVENTTRIGGER_EXPLORE_LAIR_RED_VS_YELLOW')
#		Event["Lair Depths"]            = findInfo(eTrigger, iNum,'EVENTTRIGGER_EXPLORE_LAIR_DEPTHS')

		self.EventTriggers 	= Event

	def getEraDict(self): return self.Eras
	def initEraDict(self):
		gc  = CyGlobalContext()
		git = gc.getInfoTypeForString
		Era = {}

		Era["Ancient"]  = git('ERA_ANCIENT')
		Era["Classical"]= git('ERA_CLASSICAL')
		Era["Medieval"] = git('ERA_MEDIEVAL')

		self.Eras = Era

	def getGameOptionDict(self): return self.GameOptions
	def initGameOptionDict(self):

		isOption = CyGame().isOption

		Option                          = {}
		Option["Advanced Start"]        = isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START)
		Option["Thaw"]                  = isOption(GameOptionTypes.GAMEOPTION_THAW)
		Option["Wild Mana"]             = isOption(GameOptionTypes.GAMEOPTION_WILD_MANA)
		Option["Dark Forests"]          = isOption(GameOptionTypes.GAMEOPTION_DARK_FORESTS)
		Option["Mana Guardians"]        = isOption(GameOptionTypes.GAMEOPTION_MANA_GUARDIANS)
		Option["Feral Mana"]            = isOption(GameOptionTypes.GAMEOPTION_FERAL_MANA)
		Option["No Plot Counter"]       = isOption(GameOptionTypes.GAMEOPTION_NO_PLOT_COUNTER)
		Option["No Leaves"]             = isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_0)
		Option["No Order"]              = isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_1)
		Option["No OO"]                 = isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_2)
		Option["No RoK"]                = isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_3)
		Option["No Veil"]               = isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_4)
		Option["No Empy"]               = isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_5)
		Option["No Esus"]               = isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_6)
		Option["No Liberation"]         = isOption(GameOptionTypes.GAMEOPTION_NO_LIBERATION)
		Option["One City Challenge"]    = isOption(GameOptionTypes.GAMEOPTION_ONE_CITY_CHALLENGE)
		Option["No Settlers"]           = isOption(GameOptionTypes.GAMEOPTION_NO_SETTLERS)
		Option["No Orthus"]             = isOption(GameOptionTypes.GAMEOPTION_NO_ORTHUS)
		Option["No Acheron"]            = isOption(GameOptionTypes.GAMEOPTION_NO_ACHERON)
		Option["No Duin"]               = isOption(GameOptionTypes.GAMEOPTION_NO_DUIN)
		Option["Aggressive AI"]         = isOption(GameOptionTypes.GAMEOPTION_AGGRESSIVE_AI)
		Option["No Barbarians"]         = isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS)
		Option["No Hyborem or Basium"]  = isOption(GameOptionTypes.GAMEOPTION_NO_HYBOREM_OR_BASIUM)
		Option["Barbarian World"]       = isOption(GameOptionTypes.GAMEOPTION_BARBARIAN_WORLD)
		Option["Cut Losers"]            = isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_CUT_LOSERS)
		Option["High to Low"]           = isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_HIGH_TO_LOW)
		Option["Increasing Difficulty"] = isOption(GameOptionTypes.GAMEOPTION_CHALLENGE_INCREASING_DIFFICULTY)
#		Option["No Freed Civilizations"] = isOption(GameOptionTypes.GAMEOPTION_LAIR_CIVILIZATIONS)
		self.GameOptions                = Option

	def getGameSpeedDict(self):	return self.GameSpeeds
	def initGameSpeedDict(self):
		gc                      = CyGlobalContext()
		git                     = gc.getInfoTypeForString
		Gamespeed               = {}
		Gamespeed["Quick"]      = git('GAMESPEED_QUICK')
		Gamespeed["Normal"]     = git('GAMESPEED_NORMAL')
		Gamespeed["Epic"]       = git('GAMESPEED_EPIC')
		Gamespeed["Marathon"]   = git('GAMESPEED_MARATHON')
		self.GameSpeeds         = Gamespeed

	def getLeaderStatusDict(self): return self.LeaderStatus
	def initLeaderStatusDict(self):
		gc                   = CyGlobalContext()
		git                  = gc.getInfoTypeForString
		Status               = {}
		Status["Emergent"]   = git('EMERGENT_STATUS')
		Status["Historical"] = git('HISTORICAL_STATUS')
		Status["Important"]  = git('IMPORTANT_STATUS')
		self.LeaderStatus    = Status


	def getAlignmentDict(self): return self.Alignments
	def initAlignmentDict(self):
		gc                      = CyGlobalContext()
		git                     = gc.getInfoTypeForString
		Alignment = {}
		Alignment["Good"]       = git('ALIGNMENT_GOOD')
		Alignment["Neutral"]    = git('ALIGNMENT_NEUTRAL')
		Alignment["Evil"]       = git('ALIGNMENT_EVIL')
		self.Alignments         = Alignment

	def getVictoryDict(self): return self.Victories
	def initVictoryDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Victory                 = {}
		Victory["Altar"]        = git('VICTORY_ALTAR_OF_THE_LUONNOTAR')
		Victory["Conquest"]     = git('VICTORY_CONQUEST')
		Victory["Cultural"]     = git('VICTORY_CULTURAL')
		Victory["Domination"]   = git('VICTORY_DOMINATION')
		Victory["Religious"]    = git('VICTORY_RELIGIOUS')
		Victory["Score"]        = git('VICTORY_SCORE')
		Victory["Time"]         = git('VICTORY_TIME')
		Victory["Tower"]        = git('VICTORY_TOWER_OF_MASTERY')
		Victory["Gone to Hell"] = git('VICTORY_GONE_TO_HELL')
		self.Victories          = Victory

	def getCivilizationDict(self): return self.Civilizations
	def initCivilizationDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Civ = {}
		Civ["Amurites"]             = git('CIVILIZATION_AMURITES')
		Civ["Archos"]               = git('CIVILIZATION_ARCHOS')
		Civ["Austrin"]              = git('CIVILIZATION_AUSTRIN')
		Civ["Balseraphs"]           = git('CIVILIZATION_BALSERAPHS')
		Civ["Bannor"]               = git('CIVILIZATION_BANNOR')
		Civ["Calabim"]              = git('CIVILIZATION_CALABIM')
		Civ["Chislev"]              = git('CIVILIZATION_CHISLEV')
		Civ["Clan of Embers"]       = git('CIVILIZATION_CLAN_OF_EMBERS')
		Civ["Cualli"]               = git('CIVILIZATION_CUALLI')
		Civ["Doviello"]             = git('CIVILIZATION_DOVIELLO')
		Civ["D'Tesh"]               = git('CIVILIZATION_DTESH')
		Civ["Dural"]                = git('CIVILIZATION_DURAL')         # Module Dural
		Civ["Elohim"]               = git('CIVILIZATION_ELOHIM')
		Civ["Frozen"]               = git('CIVILIZATION_FROZEN')        # Module Frozen
		Civ["Grigori"]              = git('CIVILIZATION_GRIGORI')
		Civ["Hippus"]               = git('CIVILIZATION_HIPPUS')
		Civ["Illians"]              = git('CIVILIZATION_ILLIANS')
		Civ["Infernal"]             = git('CIVILIZATION_INFERNAL')
		Civ["Jotnar"]               = git('CIVILIZATION_JOTNAR')
		Civ["Khazad"]               = git('CIVILIZATION_KHAZAD')
		Civ["Kuriotates"]           = git('CIVILIZATION_KURIOTATES')
		Civ["Lanun"]                = git('CIVILIZATION_LANUN')
		Civ["Ljosalfar"]            = git('CIVILIZATION_LJOSALFAR')
		Civ["Luchuirp"]             = git('CIVILIZATION_LUCHUIRP')
		Civ["Malakim"]              = git('CIVILIZATION_MALAKIM')
		Civ["Mazatl"]               = git('CIVILIZATION_MAZATL')
		Civ["Mechanos"]             = git('CIVILIZATION_MECHANOS')
		Civ["Mekara Order"]         = git('CIVILIZATION_MEKARA_V2')
		Civ["Mercurians"]           = git('CIVILIZATION_MERCURIANS')
		Civ["Scions"]               = git('CIVILIZATION_SCIONS')
		Civ["Sheaim"]               = git('CIVILIZATION_SHEAIM')
		Civ["Sidar"]                = git('CIVILIZATION_SIDAR')
		Civ["Svartalfar"]           = git('CIVILIZATION_SVARTALFAR')
		Civ["Barbarian (Orc)"]      = git('CIVILIZATION_ORC')
		Civ["Barbarian (Animal)"]   = git('CIVILIZATION_ANIMAL')
		Civ["Barbarian (Demon)"]    = git('CIVILIZATION_DEMON')
		self.Civilizations = Civ

	def getLeaderDict(self): return self.Leaders
	def initLeaderDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Leader = {}
		# Barbarian Civilizations
		Leader["Cernnunos"]     = git('LEADER_ANIMAL')
		Leader["Agares"]        = git('LEADER_DEMON')
		Leader["Bhall"]         = git('LEADER_ORC')
		# Standard Civilizations
		Leader["Aeriel"]		= git('LEADER_AERIEL')			# Module EmergentLeaders
		Leader["Alexis"]        = git('LEADER_ALEXIS')
		Leader["Amelanchier"]   = git('LEADER_AMELANCHIER')
		Leader["Angaad"]        = git('LEADER_ANGAAD')
		Leader["Arendel"]       = git('LEADER_ARENDEL')
		Leader["Arturus"]       = git('LEADER_ARTURUS')
		Leader["Athel"]         = git('LEADER_ATHEL')
		Leader["Auric"]         = git('LEADER_AURIC')
		Leader["Basium"]        = git('LEADER_BASIUM')
		Leader["Blackheart"]    = git('LEADER_BLACKHEART')
		Leader["Beeri"]         = git('LEADER_BEERI')
		Leader["Capria"]        = git('LEADER_CAPRIA')
		Leader["Cardith"]       = git('LEADER_CARDITH')
		Leader["Casin"]         = git('LEADER_CASIN')
		Leader["Cassiel"]       = git('LEADER_CASSIEL')
		Leader["Charadon"]      = git('LEADER_CHARADON')
		Leader["Chislev"]       = git('LEADER_CHISLEV')
		Leader["Corane"]        = git('LEADER_CORANE')
		Leader["Cuai-Ixl"]      = git('LEADER_CUAI_IXL')
		Leader["Dain"]          = git('LEADER_DAIN')
		Leader["Dannmos"]       = git('LEADER_DANNMOS')         # Module Dural
		Leader["Daracaat"]      = git('LEADER_DARACAAT')
		Leader["Decius"]        = git('LEADER_DECIUS')
		Leader["Deirdra"]       = git('LEADER_DEIRDRA')
		Leader["Detlesias"]		= git('LEADER_DETLESIAS')		# Module EmergentLeaders
		Leader["Dtesh"]         = git('LEADER_DTESH')
		Leader["Duin"]          = git('LEADER_DUIN')
		Leader["Einion"]        = git('LEADER_EINION')
		Leader["Elijah"]        = git('LEADER_ELIJAH')
		Leader["Esirce"]        = git('LEADER_ESIRCE')
		Leader["Ethne"]         = git('LEADER_ETHNE')
		Leader["Faeryl"]        = git('LEADER_FAERYL')
		Leader["Falamar"]       = git('LEADER_FALAMAR')
		Leader["Flauros"]       = git('LEADER_FLAUROS')
		Leader["Furia"]         = git('LEADER_FURIA')
		Leader["Gaius"]         = git('LEADER_GAIUS')
		Leader["Garrim"]        = git('LEADER_GARRIM')
		Leader["Gimil"]         = git('LEADER_GIMIL')
		Leader["Goodreau"]      = git('LEADER_GOODREAU')
		Leader["Hafgan"]        = git('LEADER_HAFGAN')
		Leader["Hannah"]        = git('LEADER_HANNAH')
		Leader["Herne"]         = git('LEADER_HERNE')
		Leader["Hyborem"]       = git('LEADER_HYBOREM')
		Leader["Iram Damarr"]   = git('LEADER_IRAM')
		Leader["Jonas"]         = git('LEADER_JONAS')
		Leader["Kahd"]          = git('LEADER_KAHD')
		Leader["Kane"]          = git('LEADER_KANE')
		Leader["Kandros"]       = git('LEADER_KANDROS')
		Leader["Keelyn"]        = git('LEADER_KEELYN')
		Leader["Kolsehvahn"]    = git('LEADER_KOLSEHVAHN')
		Leader["Korrina"]       = git('LEADER_KORINNA')
		Leader["Koun"]          = git('LEADER_KOUN')
		Leader["Lorelei"]       = git('LEADER_LORELEI')
		Leader["Maer"]          = git('LEADER_MAER')
		Leader["Mahala"]        = git('LEADER_MAHALA')
		Leader["Mazatl"]        = git('LEADER_MAZATL')
		Leader["Mihuatl"]       = git('LEADER_MIHUATL')
		Leader["Mordmorgan"]    = git('LEADER_MORDMORGAN')
		Leader["Natane"]        = git('LEADER_NATANE')
		Leader["Naxus"]         = git('LEADER_NAXUS')
		Leader["Nojah"]         = git('LEADER_NOJAH')
		Leader["Ophelia"]       = git('LEADER_OPHELIA')
		Leader["Os-Gabella"]    = git('LEADER_OS-GABELLA')
		Leader["Perpentach"]    = git('LEADER_PERPENTACH')
		Leader["Raitlor"]       = git('LEADER_RAITLOR')
		Leader["Reorx"]         = git('LEADER_REORX')
		Leader["Rhoanna"]       = git('LEADER_RHOANNA')
		Leader["Risen Emperor"] = git('LEADER_RISEN_EMPEROR')
		Leader["Rigmora"]       = git('LEADER_RIGMORA')				# Module EmergentLeaders
		Leader["Rivanna"]       = git('LEADER_RIVANNA')
		Leader["Rizuruk"]       = git('LEADER_RIZURUK')				# Module EmergentLeaders
		Leader["Sabathiel"]     = git('LEADER_SABATHIEL')
		Leader["Sandalphon"]    = git('LEADER_SANDALPHON')
		Leader["Shealnis"]		= git('LEADER_SHEALNIS')			# Module EmergentLeaders
		Leader["Sheelba"]       = git('LEADER_SHEELBA')
		Leader["Shekinah"]      = git('LEADER_SHEKINAH')
		Leader["Taranis"]       = git('LEADER_TARANIS')             # Module Frozen
		Leader["Tarquelne"]     = git('LEADER_TARQ')                # Module Hamstalfar
		Leader["Tasunke"]       = git('LEADER_TASUNKE')
		Leader["Tebryn"]        = git('LEADER_TEBRYN')
		Leader["Tethira"]       = git('LEADER_TETHIRA')
		Leader["Thanatos"]      = git('LEADER_THANATOS')
		Leader["Thessa"]        = git('LEADER_THESSA')
		Leader["Thessalonica"]  = git('LEADER_THESSALONICA')
		Leader["Tya"]           = git('LEADER_TYA')
		Leader["Valkrionn"]     = git('LEADER_VALK')                # Module Hamstalfar
		Leader["Valledia"]      = git('LEADER_VALLEDIA')
		Leader["Varn"]          = git('LEADER_VARN')
		Leader["Verocchio"]     = git('LEADER_VEROCCHIO')
		Leader["Volanna"]       = git('LEADER_VOLANNA')
		Leader["Weevil"]        = git('LEADER_WEEVIL')
		Leader["Yakut"]         = git('LEADER_YAKUT')
		self.Leaders = Leader

	def getTraitDict(self): return self.Traits
	def initTraitDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Trait = {}
		Trait["Adaptive"]           = git('TRAIT_ADAPTIVE')
		Trait["Aggressive"]         = git('TRAIT_AGGRESSIVE')
		Trait["Agnostic"]           = git('TRAIT_AGNOSTIC')
		Trait["Ambitious"]          = git('TRAIT_AMBITIOUS')
		Trait["Arcane"]             = git('TRAIT_ARCANE')
		Trait["Canoness 1"]    	= git('TRAIT_CANONESS')				# Module EmergentLeaders
		Trait["Canoness 2"]    	= git('TRAIT_CANONESS2')			# Module EmergentLeaders
		Trait["Canoness 3"]    	= git('TRAIT_CANONESS3')			# Module EmergentLeaders
		Trait["Charismatic"]        = git('TRAIT_CHARISMATIC')
		Trait["Cold Blooded"]       = git('TRAIT_COLD_BLOODED')
		Trait["Conqueror"]          = git('TRAIT_CONQUEROR')
		Trait["Craftmaster"]        = git('TRAIT_CRAFTMASTER')
		Trait["Creative"]           = git('TRAIT_CREATIVE')
		Trait["Deathtouched"]       = git('TRAIT_DEATHTOUCHED')
		Trait["Defender"]           = git('TRAIT_DEFENDER')
		Trait["Dominant"]           = git('TRAIT_DOMINANT')
		Trait["Egalitarian"]        = git('TRAIT_EGALITARIAN') # Emergent Leader Yakut Trait lvl1
		Trait["Egalitarian2"]       = git('TRAIT_EGALITARIAN2') # Emergent Leader Yakut Trait lvl2
		Trait["Egalitarian3"]       = git('TRAIT_EGALITARIAN3') # Emergent Leader Yakut Trait lvl3
		Trait["Personality Cult"]   = git('TRAIT_PERSONALITY_CULT')
		Trait["Expansive"]          = git('TRAIT_EXPANSIVE')
		Trait["Fallow"]             = git('TRAIT_FALLOW')
		Trait["Feral"]              = git('TRAIT_FERAL')
		Trait["Financial"]          = git('TRAIT_FINANCIAL')
		Trait["Graveleech 1"]				= git('TRAIT_GRAVELEECH')
		Trait["Horselord"]          = git('TRAIT_HORSELORD')
		Trait["Hydromancer 1"]      = git('TRAIT_HYDROMANCER')
		Trait["Hydromancer 2"]      = git('TRAIT_HYDROMANCER2')
		Trait["Hydromancer 3"]      = git('TRAIT_HYDROMANCER3')
		Trait["Ice Touched"]        = git('TRAIT_ICE_TOUCHED')
		Trait["Illusionist"]        = git('TRAIT_ILLUSIONIST')
		Trait["Imperialist"]        = git('TRAIT_IMPERIALIST')
		Trait["Incorporeal 1"]    	= git('TRAIT_INCORPOREAL')			# Module EmergentLeaders
		Trait["Incorporeal 2"]    	= git('TRAIT_INCORPOREAL2')			# Module EmergentLeaders
		Trait["Incorporeal 3"]    	= git('TRAIT_INCORPOREAL3')			# Module EmergentLeaders
		Trait["Industrious"]        = git('TRAIT_INDUSTRIOUS')
		Trait["Ingenuity"]          = git('TRAIT_INGENUITY')
		Trait["Insane"]             = git('TRAIT_INSANE')
		Trait["Instructor"]         = git('TRAIT_INSTRUCTOR')
		Trait["Instructor2"]        = git('TRAIT_INSTRUCTOR2')
		Trait["Instructor3"]        = git('TRAIT_INSTRUCTOR3')
		Trait["Intolerant"]         = git('TRAIT_INTOLERANT')
		Trait["Lycanthropic"]       = git('TRAIT_LYCANTHROPIC')
		Trait["Lycanthropic2"]       = git('TRAIT_LYCANTHROPIC2')
		Trait["Lycanthropic3"]       = git('TRAIT_LYCANTHROPIC3')
		Trait["Magic Resistant"]    = git('TRAIT_MAGIC_RESISTANT')
		Trait["Matriarch 1"]     	= git('TRAIT_PATRIARCH')			# Module EmergentLeaders
		Trait["Matriarch 2"]     	= git('TRAIT_PATRIARCH2')			# Module EmergentLeaders
		Trait["Matriarch 3"]     	= git('TRAIT_PATRIARCH3')			# Module EmergentLeaders
		Trait["Pyromancer 1"]     	= git('TRAIT_PYROMANCER')			# Module EmergentLeaders
		Trait["Pyromancer 2"]     	= git('TRAIT_PYROMANCER2')			# Module EmergentLeaders
		Trait["Pyromancer 3"]     	= git('TRAIT_PYROMANCER3')			# Module EmergentLeaders
		Trait["Mechanic"]           = git('TRAIT_MECHANIC')
		Trait["Merchant"]           = git('TRAIT_MERCHANT')
		Trait["Necromancer 1"]      = git('TRAIT_NECROMANCER')
		Trait["Necromancer 2"]      = git('TRAIT_NECROMANCER2')
		Trait["Necromancer 3"]      = git('TRAIT_NECROMANCER3')
		Trait["Opportunistic"]      = git('TRAIT_OPPORTUNISTIC')
		Trait["Organized"]          = git('TRAIT_ORGANIZED')
		Trait["Philosophical"]      = git('TRAIT_PHILOSOPHICAL')
		Trait["Raiders"]            = git('TRAIT_RAIDERS')
		Trait["Reckless"]           = git('TRAIT_RECKLESS')
		Trait["Horde"]              = git('TRAIT_HORDE')
		Trait["Civilized"]              = git('TRAIT_CIVILIZED')
		Trait["Regimented"]         = git('TRAIT_REGIMENTED')
		Trait["Sinister"]           = git('TRAIT_SINISTER')
		Trait["Slaver"]             = git('TRAIT_SLAVER')
		Trait["Spiderkin"]          = git('TRAIT_SPIDERKIN')
		Trait["Spiritual"]          = git('TRAIT_SPIRITUAL')
		Trait["Sprawling"]          = git('TRAIT_SPRAWLING')
		Trait["Strategist"]         = git('TRAIT_STRATEGIST')
		Trait["Summoner"]           = git('TRAIT_SUMMONER')
		Trait["Sundered"]           = git('TRAIT_SUNDERED')
		Trait["Swashbuckler"]       = git('TRAIT_SWASHBUCKLER')
		Trait["Sylvan Shade 1"]    	= git('TRAIT_SYLVAN_SHADE')			# Module EmergentLeaders
		Trait["Sylvan Shade 2"]    	= git('TRAIT_SYLVAN_SHADE2')		# Module EmergentLeaders
		Trait["Sylvan Shade 3"]    	= git('TRAIT_SYLVAN_SHADE3')		# Module EmergentLeaders
		Trait["Theocratic"]         = git('TRAIT_THEOCRATIC')
		Trait["Tolerant"]           = git('TRAIT_TOLERANT')
		Trait["Trader"]             = git('TRAIT_TRADER')
		Trait["Treacherous"]        = git('TRAIT_TREACHEROUS')
		Trait["Veinhunter"]         = git('TRAIT_VEINHUNTER')
		Trait["Virtuous Pirate"]    = git('TRAIT_VIRTUOUS_PIRATE')
		Trait["Wanderer"]           = git('TRAIT_WANDERER')
		Trait["Warlord"]            = git('TRAIT_WARLORD')
		Trait["Humanist I"]         = git('TRAIT_HUMANIST1')
	#	Trait["Humanist II"]        = git('TRAIT_HUMANIST2')
	#	Trait["Humanist III"]       = git('TRAIT_HUMANIST3')
		Trait["Scorched Earth"]		= git('TRAIT_SCORCHED_EARTH')
		Trait["Winterborn"]         = git('TRAIT_WINTERBORN')       # Module Frozen
		Trait["Aspect Capria"]         = git('TRAIT_ASPECT_OF_WAR_CAPRIA')       # Module Frozen
		Trait["Aspect Mahon"]         = git('TRAIT_ASPECT_OF_WAR_MAHON')       # Module Frozen
		self.Traits = Trait

	def getManaDict(self): return self.Mana
	def initManaDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Mana = {}
		Mana["Mana Class"]	= git('BONUSCLASS_MANA')
		Mana["Mana"] 		= git('BONUS_MANA')
		Mana["Air"] 		= git('BONUS_MANA_AIR')
		Mana["Body"] 		= git('BONUS_MANA_BODY')
		Mana["Chaos"]		= git('BONUS_MANA_CHAOS')
		Mana["Creation"]	= git('BONUS_MANA_CREATION')
		Mana["Death"] 		= git('BONUS_MANA_DEATH')
		Mana["Dimensional"] = git('BONUS_MANA_DIMENSIONAL')
		Mana["Earth"] 		= git('BONUS_MANA_EARTH')
		Mana["Enchantment"]	= git('BONUS_MANA_ENCHANTMENT')
		Mana["Entropy"] 	= git('BONUS_MANA_ENTROPY')
		Mana["Fire"] 		= git('BONUS_MANA_FIRE')
		Mana["Force"] 		= git('BONUS_MANA_FORCE')
		Mana["Ice"] 		= git('BONUS_MANA_ICE')
		Mana["Law"] 		= git('BONUS_MANA_LAW')
		Mana["Life"] 		= git('BONUS_MANA_LIFE')
		Mana["Metamagic"] 	= git('BONUS_MANA_METAMAGIC')
		Mana["Mind"] 		= git('BONUS_MANA_MIND')
		Mana["Nature"] 		= git('BONUS_MANA_NATURE')
		Mana["Shadow"] 		= git('BONUS_MANA_SHADOW')
		Mana["Spirit"] 		= git('BONUS_MANA_SPIRIT')
		Mana["Sun"] 		= git('BONUS_MANA_SUN')
		Mana["Water"] 		= git('BONUS_MANA_WATER')
		self.Mana = Mana

	def getResourcesDict(self): return self.Resources
	def initResourcesDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Bonus = {}

		Bonus["Mana"] 		= git('BONUS_MANA')
		Bonus["Arctic Deer"]= git('BONUS_DEER_ARCTIC')
		Bonus["Banana"] 	= git('BONUS_BANANA')
		Bonus["Bison"] 		= git('BONUS_BISON')
		Bonus["Camel"] 		= git('BONUS_CAMEL')
		Bonus["Corn"] 		= git('BONUS_CORN')
		Bonus["Cow"] 		= git('BONUS_COW')
		Bonus["Clam"] 		= git('BONUS_CLAM')
		Bonus["Crab"] 		= git('BONUS_CRAB')
		Bonus["Copper"] 	= git('BONUS_COPPER')
		Bonus["Cotton"] 	= git('BONUS_COTTON')
		Bonus["Deer"] 		= git('BONUS_DEER')
		Bonus["Dye"] 		= git('BONUS_DYE')
		Bonus["Fish"] 		= git('BONUS_FISH')
		Bonus["Fur"] 		= git('BONUS_FUR')
		Bonus["Gold"] 		= git('BONUS_GOLD')
		Bonus["Gems"] 		= git('BONUS_GEMS')
		Bonus["Gulagarm"]	= git('BONUS_GULAGARM')
		Bonus["Horse"]		= git('BONUS_HORSE')
		Bonus["Iron"] 		= git('BONUS_IRON')
		Bonus["Ivory"] 		= git('BONUS_IVORY')
		Bonus["Incense"] 	= git('BONUS_INCENSE')
		Bonus["Marble"] 	= git('BONUS_MARBLE')
		Bonus["Mushrooms"] 	= git('BONUS_MUSHROOMS')
		Bonus["Mithril"] 	= git('BONUS_MITHRIL')
		Bonus["Nightmare"]	= git('BONUS_NIGHTMARE')
		Bonus["Obsidian"] 	= git('BONUS_OBSIDIAN')
		Bonus["Patrian"] 	= git('BONUS_PATRIAN_ARTIFACTS')
		Bonus["Pearl"] 		= git('BONUS_PEARL')
		Bonus["Pig"]		= git('BONUS_PIG')
		Bonus["Razorweed"]	= git('BONUS_RAZORWEED')
		Bonus["Reagents"]	= git('BONUS_REAGENTS')
		Bonus["Rice"]		= git('BONUS_RICE')
		Bonus["Silk"] 		= git('BONUS_SILK')
		Bonus["Sheep"]		= git('BONUS_SHEEP')
		Bonus["Sheut"]		= git('BONUS_SHEUT_STONE')
		Bonus["Shrimp"] 	= git('BONUS_SHRIMP')
		Bonus["Sugar"]		= git('BONUS_SUGAR')
		Bonus["Toad"]		= git('BONUS_TOAD')
		Bonus["Wine"]		= git('BONUS_WINE')
		Bonus["Wheat"]		= git('BONUS_WHEAT')
		self.Resources = Bonus

	def getWorldSizesDict(self): return self.WorldSizes
	def initWorldSizesDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		WorldSize = {}
		WorldSize["Duel"] 	= git('WORLDSIZE_DUEL')
		WorldSize["Tiny"] 	= git('WORLDSIZE_TINY')
		WorldSize["Small"] 	= git('WORLDSIZE_SMALL')
		WorldSize["Standard"]= git('WORLDSIZE_STANDARD')
		WorldSize["Large"] 	= git('WORLDSIZE_LARGE')
		WorldSize["Huge"] 	= git('WORLDSIZE_HUGE')
		WorldSize["Huger"] 	= git('WORLDSIZE_HUGER')
		self.WorldSizes = WorldSize

	def getTechDict(self): return self.Techs
	def initTechDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		Tech = {}
		Tech["Ancient Chants"]			= git('TECH_ANCIENT_CHANTS')
		Tech["Agriculture"]				= git('TECH_AGRICULTURE')
		Tech["Alteration"]				= git('TECH_ALTERATION')
		Tech["Arete"]					= git('TECH_ARETE')
		Tech["Arcane Lore"]				= git('TECH_ARCANE_LORE')
		Tech["Archery"]					= git('TECH_ARCHERY')
		Tech["Armored Cavalry"]			= git('TECH_ARMORED_CAVALRY')
		Tech["Animal Handling"]			= git('TECH_ANIMAL_HANDLING')
		Tech["Animal Husbandry"]		= git('TECH_ANIMAL_HUSBANDRY')
		Tech["Animal Mastery"]	 		= git('TECH_ANIMAL_MASTERY')
		Tech["Astronomy"]				= git('TECH_ASTRONOMY')

		Tech["Blasting Powder"]			= git('TECH_BLASTING_POWDER')
		Tech["Bowyers"]					= git('TECH_BOWYERS')
		Tech["Bronze Working"]			= git('TECH_BRONZE_WORKING')

		Tech["Calendar"]			 	= git('TECH_CALENDAR')
		Tech["Cartography"]			 	= git('TECH_CARTOGRAPHY')
		Tech["Code of Laws"]		 	= git('TECH_CODE_OF_LAWS')
		Tech["Construction"] 			= git('TECH_CONSTRUCTION')
		Tech["Commune with Nature"]		= git('TECH_COMMUNE_WITH_NATURE')
		Tech["Corruption of Spirit"]	= git('TECH_CORRUPTION_OF_SPIRIT')
		Tech["Currency"]	 			= git('TECH_CURRENCY')
		Tech["Crafting"]	 			= git('TECH_CRAFTING')

		Tech["Deception"]	 			= git('TECH_DECEPTION')
		Tech["Divination"]	 			= git('TECH_DIVINATION')
		Tech["Divine Essence"] 			= git('TECH_DIVINE_ESSENCE')
		Tech["Drama"]					= git('TECH_DRAMA')

		Tech["Education"] 				= git('TECH_EDUCATION')
		Tech["Elementalism"] 			= git('TECH_ELEMENTALISM')
		Tech["Engineering"]	 			= git('TECH_ENGINEERING')
		Tech["Exploration"]	 			= git('TECH_EXPLORATION')

		Tech["Fanaticism"]				= git('TECH_FANATICISM')
		Tech["Feral Bond"]				= git('TECH_FERAL_BOND')
		Tech["Festivals"]				= git('TECH_FESTIVALS')
		Tech["Feudalism"]				= git('TECH_FEUDALISM')
		Tech["Fishing"]					= git('TECH_FISHING')

		Tech["Guilds"]					= git('TECH_GUILDS')

		Tech["Hidden Paths"]			= git('TECH_HIDDEN_PATHS')

		Tech["Infernal Pact"]			= git('TECH_INFERNAL_PACT')
		Tech["Iron Working"]			= git('TECH_IRON_WORKING')

		Tech["Dark Secrets"]			= git('TECH_DARK_SECRETS')

		Tech["Knowledge of the Ether"]	= git('TECH_KNOWLEDGE_OF_THE_ETHER')

		Tech["Honor"] 					= git('TECH_HONOR')
		Tech["Hunting"]					= git('TECH_HUNTING')
		Tech["Horseback Riding"]		= git('TECH_HORSEBACK_RIDING')

		Tech["Machinery"]				= git('TECH_MACHINERY')
		Tech["Malevolent Designs"]		= git('TECH_MALEVOLENT_DESIGNS')

		Tech["Math"]		 			= git('TECH_MATHEMATICS')
		Tech["Masonry"]		 			= git('TECH_MASONRY')
		Tech["Mercentalism"]		 	= git('TECH_MERCANTILISM')
		Tech["Mining"]		 			= git('TECH_MINING')
		Tech["Mind Stapling"]			= git('TECH_MIND_STAPLING')
		Tech["Military Strategy"]		= git('TECH_MILITARY_STRATEGY')
		Tech["Medicine"]				= git('TECH_MEDICINE')
		Tech["Message from the Deep"]	= git('TECH_MESSAGE_FROM_THE_DEEP')
		Tech["Mithril Working"]			= git('TECH_MITHRIL_WORKING')
		Tech["Mysticism"]				= git('TECH_MYSTICISM')

		Tech["Necromancy"]				= git('TECH_NECROMANCY')


		Tech["Omniscience"]				= git('TECH_OMNISCIENCE')
		Tech["Optics"]					= git('TECH_OPTICS')
		Tech["Orders from Heaven"]		= git('TECH_ORDERS_FROM_HEAVEN')


		Tech["Philosophy"]				= git('TECH_PHILOSOPHY')
		Tech["Poisons"]					= git('TECH_POISONS')
		Tech["Precision"]				= git('TECH_PRECISION')
		Tech["Priesthood"]				= git('TECH_PRIESTHOOD')

		Tech["Rage"]					= git('TECH_RAGE')
		Tech["Religious Law"]			= git('TECH_RELIGIOUS_LAW')
		Tech["Righteousness"]			= git('TECH_RIGHTEOUSNESS')

		Tech["Sailing"]	 				= git('TECH_SAILING')
		Tech["Sanitation"]	 			= git('TECH_SANITATION')
		Tech["Seafaring"]	 			= git('TECH_SEAFARING')
		Tech["Smelting"]	 			= git('TECH_SMELTING')
		Tech["Sorcery"]					= git('TECH_SORCERY')
		Tech["Steam Power"]				= git('TECH_STEAM_POWER')
		Tech["Strength of Will"]		= git('TECH_STRENGTH_OF_WILL')
		Tech["Stirrups"]				= git('TECH_STIRRUPS')
		Tech["Swampdwelling"]			= git('TECH_SWAMPDWELLING')

		Tech["Taxation"]	 			= git('TECH_TAXATION')
		Tech["Theology"]		 		= git('TECH_THEOLOGY')
		Tech["Tracking"]		 		= git('TECH_TRACKING')
		Tech["Trade"]		 			= git('TECH_TRADE')
		Tech["The Gift"]	 			= git('TECH_THE_GIFT')

		Tech["Warhorses"]				= git('TECH_WARHORSES')
		Tech["Warfare"]					= git('TECH_WARFARE')
		Tech["Way of the Forests"]		= git('TECH_WAY_OF_THE_FORESTS')
		Tech["Way of the Earthmother"]	= git('TECH_WAY_OF_THE_EARTHMOTHER')
		Tech["Way of the Wicked"]		= git('TECH_WAY_OF_THE_WICKED')
		Tech["Way of the Wise"]			= git('TECH_WAY_OF_THE_WISE')
		Tech["Writing"]					= git('TECH_WRITING')
		Tech["White Hand"]				= git('TECH_WHITE_HAND')
		
		Tech["Traditions"]				= git('TECH_JO1')
		Tech["Dunespeakers"]			= git('TECH_DESERTPEOPLE')
		Tech["Alchemy"]					= git('TECH_ALCHEMY')
		self.Techs 						= Tech

	def getTerrainDict(self): return self.Terrain
	def initTerrainDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		Terrain = {}
		# Terrain
		Terrain["Wasteland"]            = git('TERRAIN_WASTELAND')
		Terrain["Desert"]               = git('TERRAIN_DESERT')
		Terrain["Plains"]               = git('TERRAIN_PLAINS')
		Terrain["Grass"]                = git('TERRAIN_GRASS')
		Terrain["Marsh"]                = git('TERRAIN_MARSH')

		Terrain["Taiga"]                = git('TERRAIN_TAIGA')
		Terrain["Tundra"]               = git('TERRAIN_TUNDRA')
		Terrain["Glacier"]              = git('TERRAIN_GLACIER')
		
		Terrain["Coast"]                = git('TERRAIN_COAST')
		Terrain["Ocean"]                = git('TERRAIN_OCEAN')
		Terrain["Deep ocean"]           = git('TERRAIN_OCEAN_DEEP')
		
		# Hell terrain
		Terrain["Burning sands"]        = git('TERRAIN_BURNING_SANDS')          # desert
		Terrain["Fields of perdition"]  = git('TERRAIN_FIELDS_OF_PERDITION')    # plains
		Terrain["Broken lands"]         = git('TERRAIN_BROKEN_LANDS')           # grass
		Terrain["Shallows"]             = git('TERRAIN_SHALLOWS')               # marsh
		Terrain["Blighted coast"]       = git('TERRAIN_BLIGHTED_COAST')         # coast
		Terrain["Blackwater"]           = git('TERRAIN_BLACKWATER')             # ocean
		
		self.Terrain 	= Terrain

	def getFeatureDict(self): return self.Feature
	def initFeatureDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		Feature = {}

		# Features
		Feature["Volcano"]          = git('FEATURE_VOLCANO')
		Feature["Haunted Lands"]    = git('PLOT_EFFECT_HAUNTED_LANDS')
		Feature["Flood Plains"]     = git('FEATURE_FLOOD_PLAINS')
		Feature["Oasis"]            = git('FEATURE_OASIS')
		Feature["Ice"]              = git('FEATURE_ICE')
		Feature["Forest"]           = git('FEATURE_FOREST')
		Feature["Forest New"]       = git('FEATURE_FOREST_NEW')
		Feature["Ancient Forest"]   = git('FEATURE_FOREST_ANCIENT')
		Feature["Burnt Forest"]     = git('FEATURE_FOREST_BURNT')
		Feature["Jungle"]           = git('FEATURE_JUNGLE')
		Feature["Scrub"]            = git('FEATURE_SCRUB')
		Feature["Blizzard"]         = git('FEATURE_BLIZZARD')
		Feature["Winter"]           = git('FEATURE_WINTER') #�Module Frozen
		Feature["Flames"]           = git('FEATURE_FLAMES')
		Feature["Kelp"]             = git('FEATURE_KELP')
		Feature["Kelp Forest"]      = git('FEATURE_KELP_FOREST')
		self.Feature                = Feature

	def getUnitCombatDict(self): return self.UnitCombats
	def initUnitCombatDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		UnitCombat = {}
		UnitCombat["Recon"] 	= git('UNITCOMBAT_RECON')
		UnitCombat["Archer"] 	= git('UNITCOMBAT_ARCHER')
		UnitCombat["Mounted"] 	= git('UNITCOMBAT_MOUNTED')
		UnitCombat["Melee"] 	= git('UNITCOMBAT_MELEE')
		UnitCombat["Siege"] 	= git('UNITCOMBAT_SIEGE')
		UnitCombat["Adept"] 	= git('UNITCOMBAT_ADEPT')
		UnitCombat["Disciple"]	= git('UNITCOMBAT_DISCIPLE')
		UnitCombat["Animal"]	= git('UNITCOMBAT_ANIMAL')
		UnitCombat["Naval"] 	= git('UNITCOMBAT_NAVAL')
		UnitCombat["Beast"] 	= git('UNITCOMBAT_BEAST')
		UnitCombat["Worker"] 	= git('UNITCOMBAT_WORKER')
		UnitCombat["Commander"] = git('UNITCOMBAT_COMMANDER')
		self.UnitCombats 	= UnitCombat

	def getHeroesDict(self): return self.Heroes
	def initHeroesDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Hero = {}
		Hero["Abashi"] 				= git('UNIT_ABASHI')
		Hero["Acheron"] 			= git('UNIT_ACHERON')
		Hero["Alazkan"] 			= git('UNIT_ALAZKAN')
		Hero["Alcinus"] 			= git('UNIT_ALCINUS')
		Hero["Alcinus (Archmage)"] 	= git('UNIT_ALCINUS_ARCHMAGE')
		Hero["Alcinus (Upgraded)"] 	= git('UNIT_ALCINUS_UPGRADED')
		Hero["Ars Moriendi"] 		= git('UNIT_ARS')
		Hero["Arthendain"] 			= git('UNIT_ARTHENDAIN')
		Hero["Auric Ascended"] 		= git('UNIT_AURIC_ASCENDED')
		Hero["Auric"] 				= git('UNIT_AURIC')
		Hero["Auric Winter"] 		= git('UNIT_AURIC_WINTER')
		Hero["Avatar of Wrath"] 	= git('UNIT_WRATH')
		Hero["Bambur"] 				= git('UNIT_BAMBUR')
		Hero["Barnaxus"] 			= git('UNIT_BARNAXUS')
		Hero["Duin"] 				= git('UNIT_DUIN')
		Hero["Basium"] 				= git('UNIT_BASIUM')
		Hero["Boris"] 				= git('UNIT_BORIS')
		Hero["Brigit"] 				= git('UNIT_BRIGIT')
		Hero["Buboes"] 				= git('UNIT_BUBOES')
		Hero["Chalid"] 				= git('UNIT_CHALID')
		Hero["Coatlann"] 			= git('UNIT_COATLANN')
		Hero["Corlindale"] 			= git('UNIT_CORLINDALE')
		Hero["Donal Lugh"] 			= git('UNIT_DONAL')
		Hero["Drifa"] 				= git('UNIT_DRIFA')
		Hero["Egrass"] 				= git('UNIT_EGRASS')
		Hero["Eurabatres"] 			= git('UNIT_EURABATRES')
		Hero["Feris"] 				= git('UNIT_FERIS')
		Hero["Fiacra"] 				= git('UNIT_FIACRA')
		Hero["Gaelan"] 				= git('UNIT_GAELAN')
		Hero["Gibbon"] 				= git('UNIT_GIBBON')
		Hero["Gilden"] 				= git('UNIT_GILDEN')
		Hero["Goliath"] 			= git('UNIT_GOLIATH')
		Hero["Govannon"] 			= git('UNIT_GOVANNON')
		Hero["Gurid"] 				= git('UNIT_GURID')
		Hero["Guybrush"] 			= git('UNIT_GUYBRUSH')
		Hero["Harmatt"] 			= git('UNIT_HARMATT')
		Hero["Hemah"] 				= git('UNIT_HEMAH')
		Hero["Hyborem"] 			= git('UNIT_HYBOREM')
		Hero["Kahd"] 				= git('UNIT_KAHD')
		Hero["Karrlson"] 			= git('UNIT_KARRLSON')
		Hero["Kithra"] 				= git('UNIT_KITHRA')
		Hero["Korrina (Black Lady)"]= git('UNIT_KORRINA_BLACK_LADY')
		Hero["Korrina (Haunt)"] 	= git('UNIT_HAUNT_KORRINA')
		Hero["Korrina (Red Lady)"] 	= git('UNIT_KORRINA_RED_LADY')
		Hero["Korrina (Unshackled)"]= git('UNIT_KORRINA_PROTECTOR')
		Hero["Lenora"] 				= git('UNIT_LENORA')
		Hero["Leviathan"] 			= git('UNIT_LEVIATHAN')
		Hero["Loki"] 				= git('UNIT_LOKI')
		Hero["Lord D'Tesh"] 		= git('UNIT_DTESH')
		Hero["Losha"] 				= git('UNIT_LOSHA')
		Hero["Lucian"] 				= git('UNIT_LUCIAN')
		Hero["Magnadine"] 			= git('UNIT_MAGNADINE')
		Hero["Mardero"] 			= git('UNIT_MARDERO')
		Hero["Margalard"] 			= git('UNIT_MARGALARD')
		Hero["Maros"] 				= git('UNIT_MAROS')
		Hero["Mary"] 				= git('UNIT_MARY')
		Hero["Melante"] 			= git('UNIT_MELANTE')
		Hero["Meshabber"] 			= git('UNIT_MESHABBER')
		Hero["Meshwaki"] 			= git('UNIT_MESKWAKI')
		Hero["Miquiztli"] 			= git('UNIT_MIQUIZTLI')
		Hero["Mithril Golem"] 		= git('UNIT_MITHRIL_GOLEM')
		Hero["Mokka"] 				= git('UNIT_MOKKA')
		Hero["Mother"] 				= git('UNIT_MOTHER_SPIDER')
		Hero["Muirin"] 				= git('UNIT_MUIRIN')
		Hero["Orthus"] 				= git('UNIT_ORTHUS')
		Hero["Pelemoc"] 			= git('UNIT_PELEMOC')
		Hero["Rantine"] 			= git('UNIT_RANTINE')
		Hero["Rathus"] 				= git('UNIT_RATHUS')
		Hero["Rosier the Fallen"] 	= git('UNIT_ROSIER')
		Hero["Rosier Oathtaker"] 	= git('UNIT_ROSIER_OATHTAKER')
		Hero["Sailor's Dirge"] 		= git('UNIT_SAILORS_DIRGE')
		Hero["Saverous"] 			= git('UNIT_SAVEROUS')
		Hero["Sphener"] 			= git('UNIT_SPHENER')
		Hero["Stephanos"] 			= git('UNIT_STEPHANOS')
		Hero["Taranis"] 			= git('UNIT_TARANIS')
		Hero["Taranis Ascended"] 	= git('UNIT_TARANIS_ASCENDED')
		Hero["Teutorix"] 			= git('UNIT_TEUTORIX')
		Hero["Thanatos"] 			= git('UNIT_THANATOS')
		Hero["The Black Wind"] 		= git('UNIT_BLACK_WIND')
		Hero["The Risen Emperor"] 	= git('UNIT_RISEN_EMPEROR')
		Hero["The War Machine"] 	= git('UNIT_WAR_MACHINE')
		Hero["Themoch"] 			= git('UNIT_THEMOCH')
		Hero["Tumtum"] 				= git('UNIT_TUMTUM')
		Hero["Valin"] 				= git('UNIT_VALIN')
		Hero["Varulv"] 				= git('UNIT_DOVIELLO_WEREWOLF')
		Hero["Wilboman"] 			= git('UNIT_WILBOMAN')
		Hero["Yersinia"] 			= git('UNIT_YERSINIA')
		Hero["Yvain"] 				= git('UNIT_YVAIN')
		Hero["Zarcaz"] 				= git('UNIT_ZARCAZ')

		Hero["Class-Abashi"] 				= git('UNITCLASS_ABASHI')
		Hero["Class-Acheron"] 				= git('UNITCLASS_ACHERON')
		Hero["Class-Alazkan"] 				= git('UNITCLASS_ALAZKAN')
		Hero["Class-Alcinus"] 				= git('UNITCLASS_ALCINUS')
		Hero["Class-Alcinus (Archmage)"]	= git('UNITCLASS_ALCINUS_ARCHMAGE')
		Hero["Class-Alcinus (Upgraded)"]	= git('UNITCLASS_ALCINUS_UPGRADED')
		Hero["Class-Ars Moriendi"] 			= git('UNITCLASS_ARS')
		Hero["Class-Arthendain"] 			= git('UNITCLASS_ARTHENDAIN')
		Hero["Class-Auric Ascended"] 		= git('UNITCLASS_AURIC_ASCENDED')
		Hero["Class-Auric"] 				= git('UNITCLASS_AURIC')
		Hero["Class-Auric Winter"] 			= git('UNITCLASS_AURIC_WINTER')
		Hero["Class-Avatar of Wrath"] 		= git('UNITCLASS_WRATH')
		Hero["Class-Bambur"] 				= git('UNITCLASS_BAMBUR')
		Hero["Class-Barnaxus"] 				= git('UNITCLASS_BARNAXUS')
		Hero["Class-Basium"] 				= git('UNITCLASS_BASIUM')
		Hero["Class-Boris"] 				= git('UNITCLASS_BORIS')
		Hero["Class-Brigit"] 				= git('UNITCLASS_BRIGIT')
		Hero["Class-Buboes"] 				= git('UNITCLASS_BUBOES')
		Hero["Class-Chalid"] 				= git('UNITCLASS_CHALID')
		Hero["Class-Coatlann"] 				= git('UNITCLASS_COATLANN')
		Hero["Class-Corlindale"] 			= git('UNITCLASS_CORLINDALE')
		Hero["Class-Donal"]		 			= git('UNITCLASS_DONAL')
		Hero["Class-Duin"] 					= git('UNITCLASS_DUIN')
		Hero["Class-Drifa"] 				= git('UNITCLASS_DRIFA')
		Hero["Class-Egrass"] 				= git('UNITCLASS_EGRASS')
		Hero["Class-Eurabatres"] 			= git('UNITCLASS_EURABATRES')
		Hero["Class-Feris"] 				= git('UNITCLASS_FERIS')
		Hero["Class-Fiacra"] 				= git('UNITCLASS_FIACRA')
		Hero["Class-Gaelan"] 				= git('UNITCLASS_GAELAN')
		Hero["Class-Gibbon"] 				= git('UNITCLASS_GIBBON')
		Hero["Class-Gilden"] 				= git('UNITCLASS_GILDEN')
		Hero["Class-Goliath"] 				= git('UNITCLASS_GOLIATH')
		Hero["Class-Govannon"] 				= git('UNITCLASS_GOVANNON')
		Hero["Class-Gurid"] 				= git('UNITCLASS_GURID')
		Hero["Class-Guybrush"] 				= git('UNITCLASS_GUYBRUSH')
		Hero["Class-Harmatt"] 				= git('UNITCLASS_HARMATT')
		Hero["Class-Hemah"] 				= git('UNITCLASS_HEMAH')
		Hero["Class-Hyborem"] 				= git('UNITCLASS_HYBOREM')
		Hero["Class-Kahd"] 					= git('UNITCLASS_KAHD')
		Hero["Class-Karrlson"] 				= git('UNITCLASS_KARRLSON')
		Hero["Class-Kithra"] 				= git('UNITCLASS_KITHRA')
		Hero["Class-Korrina (Black Lady)"]	= git('UNITCLASS_KORRINA_BLACK_LADY')
		Hero["Class-Korrina (Haunt)"] 		= git('UNITCLASS_HAUNT_KORRINA')
		Hero["Class-Korrina (Red Lady)"] 	= git('UNITCLASS_KORRINA_RED_LADY')
		Hero["Class-Korrina"]				= git('UNITCLASS_KORRINA')
		Hero["Class-Lenora"] 				= git('UNITCLASS_LENORA')
		Hero["Class-Leviathan"] 			= git('UNITCLASS_LEVIATHAN')
		Hero["Class-Loki"] 					= git('UNITCLASS_LOKI')
		Hero["Class-Lord D'Tesh"] 			= git('UNITCLASS_DTESH')
		Hero["Class-Losha"] 				= git('UNITCLASS_LOSHA')
		Hero["Class-Lucian"] 				= git('UNITCLASS_LUCIAN')
		Hero["Class-Magnadine"] 			= git('UNITCLASS_MAGNADINE')
		Hero["Class-Mardero"] 				= git('UNITCLASS_MARDERO')
		Hero["Class-Margalard"] 			= git('UNITCLASS_MARGALARD')
		Hero["Class-Maros"] 				= git('UNITCLASS_MAROS')
		Hero["Class-Mary"] 					= git('UNITCLASS_MARY')
		Hero["Class-Melante"] 				= git('UNITCLASS_MELANTE')
		Hero["Class-Meshabber"] 			= git('UNITCLASS_MESHABBER')
		Hero["Class-Meshwaki"] 				= git('UNITCLASS_MESKWAKI')
		Hero["Class-Miquiztli"] 			= git('UNITCLASS_MIQUIZTLI')
		Hero["Class-Mithril Golem"] 		= git('UNITCLASS_MITHRIL_GOLEM')
		Hero["Class-Mokka"] 				= git('UNITCLASS_MOKKA')
		Hero["Class-Mother"] 				= git('UNITCLASS_MOTHER_SPIDER')
		Hero["Class-Muirin"] 				= git('UNITCLASS_MUIRIN')
		Hero["Class-Orthus"] 				= git('UNITCLASS_ORTHUS')
		Hero["Class-Pelemoc"] 				= git('UNITCLASS_PELEMOC')
		Hero["Class-Rantine"] 				= git('UNITCLASS_RANTINE')
		Hero["Class-Rathus"] 				= git('UNITCLASS_RATHUS')
		Hero["Class-Rosier the Fallen"] 	= git('UNITCLASS_ROSIER')
		Hero["Class-Rosier Oathtaker"] 		= git('UNITCLASS_ROSIER_OATHTAKER')
		Hero["Class-Sailor's Dirge"] 		= git('UNITCLASS_SAILORS_DIRGE')
		Hero["Class-Saverous"] 				= git('UNITCLASS_SAVEROUS')
		Hero["Class-Sphener"] 				= git('UNITCLASS_SPHENER')
		Hero["Class-Stephanos"] 			= git('UNITCLASS_STEPHANOS')
		Hero["Class-Taranis"] 				= git('UNITCLASS_TARANIS')
		Hero["Class-Teutorix"] 				= git('UNITCLASS_TEUTORIX')
		Hero["Class-Thanatos"] 				= git('UNITCLASS_THANATOS')
		Hero["Class-The Black Wind"] 		= git('UNITCLASS_BLACK_WIND')
		Hero["Class-The Risen Emperor"] 	= git('UNITCLASS_RISEN_EMPEROR')
		Hero["Class-The War Machine"] 		= git('UNITCLASS_WAR_MACHINE')
		Hero["Class-Themoch"] 				= git('UNITCLASS_THEMOCH')
		Hero["Class-Tumtum"] 				= git('UNITCLASS_TUMTUM')
		Hero["Class-Valin"] 				= git('UNITCLASS_VALIN')
		Hero["Class-Varulv"] 				= git('UNITCLASS_DOVIELLO_WEREWOLF')
		Hero["Class-Wilboman"] 				= git('UNITCLASS_WILBOMAN')
		Hero["Class-Yersinia"] 				= git('UNITCLASS_YERSINIA')
		Hero["Class-Yvain"] 				= git('UNITCLASS_YVAIN')
		Hero["Class-Zarcaz"] 				= git('UNITCLASS_ZARCAZ')
		self.Heroes = Hero

	def getBuildDict(self): return self.Builds
	def initBuildDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		Build = {}
		Build["Farm"]			= git('BUILD_FARM')
		Build["Cottage"]			= git('BUILD_COTTAGE')
		Build["Windmill"]		= git('BUILD_WINDMILL')
		Build["Workshop"]		= git('BUILD_WORKSHOP')
		Build["Lumbermill"]		= git('BUILD_LUMBERMILL')

		Build["Mana Air"]		= git('BUILD_MANA_AIR')
		Build["Mana Body"]		= git('BUILD_MANA_BODY')
		Build["Mana Chaos"]		= git('BUILD_MANA_CHAOS')
		Build["Mana Creation"]	= git('BUILD_MANA_CREATION')
		Build["Mana Death"]		= git('BUILD_MANA_DEATH')
		Build["Mana Dimensional"]= git('BUILD_MANA_DIMENSIONAL')
		Build["Mana Earth"]		= git('BUILD_MANA_EARTH')
		Build["Mana Enchantment"]= git('BUILD_MANA_ENCHANTMENT')
		Build["Mana Entropy"]	= git('BUILD_MANA_ENTROPY')
		Build["Mana Fire"]		= git('BUILD_MANA_FIRE')
		Build["Mana Force"]		= git('BUILD_MANA_FORCE')
		Build["Mana Ice"]		= git('BUILD_MANA_ICE')
		Build["Mana Law"]		= git('BUILD_MANA_LAW')
		Build["Mana Life"]		= git('BUILD_MANA_LIFE')
		Build["Mana Metamagic"]	= git('BUILD_MANA_METAMAGIC')
		Build["Mana Mind"]		= git('BUILD_MANA_MIND')
		Build["Mana Nature"]		= git('BUILD_MANA_NATURE')
		Build["Mana Spirit"]		= git('BUILD_MANA_SPIRIT')
		Build["Mana Water"]		= git('BUILD_MANA_WATER')
		Build["Mana Shadow"]		= git('BUILD_MANA_SHADOW')
		Build["Mana Sun"]		= git('BUILD_MANA_SUN')

		Build["Bedouin Sit"]		= git('BUILD_BEDOUIN_SIT')
		Build["Wyrmfisher Fishing Boats"]= git('BUILD_FISHING_BOATS_WYRMFISHER')
		Build["Pyre"]				= git('BUILD_PYRE')
		Build["Graveyard"]			= git('BUILD_GRAVEYARD')
		Build["Refinery"]			= git('BUILD_REFINERY')
		Build["Pasture Corrupted"]	= git('BUILD_PASTURE_CORRUPTED')
		Build["Dwarven Mine"]		= git('BUILD_DWARVEN_MINE')
		Build["Lanun Fishing Boats"]	= git('BUILD_FISHING_BOATS_LANUN')
		Build["Pirate Cove"]			= git('BUILD_PIRATE_COVE')
		self.Builds	= Build

	def getUnitDict(self): return self.Units
	def initUnitDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		""" Generic Units """
		Unit = {}
		Unit["Adept"] 			= git('UNIT_ADEPT')
		Unit["Archer"] 			= git('UNIT_ARCHER')
		Unit["Assassin"]		= git('UNIT_ASSASSIN')
		Unit["Axeman"] 			= git('UNIT_AXEMAN')
		Unit["Beastmaster"]		= git('UNIT_BEASTMASTER')

		Unit["Catapult"] 		= git('UNIT_CATAPULT')
		Unit["Champion"] 		= git('UNIT_CHAMPION')
		Unit["Chariot"] 		= git('UNIT_CHARIOT')
		Unit["Crossbowman"]		= git('UNIT_CROSSBOWMAN')
		Unit["Eidolon"]			= git('UNIT_EIDOLON')
		Unit["Horseman"] 		= git('UNIT_HORSEMAN')
		Unit["Javelin Thrower"]	= git('UNIT_JAVELIN_THROWER')
		Unit["Longbowman"] 		= git('UNIT_LONGBOWMAN')
		Unit["Mage"]	 		= git('UNIT_MAGE')
		Unit["Mercenary"] 		= git('UNIT_MERCENARY')

		Unit["Privateer"]		= git('UNIT_PRIVATEER')
		Unit["Ranger"]			= git('UNIT_RANGER')
		Unit["Scout"]	 		= git('UNIT_SCOUT')
		Unit["Settler"] 		= git('UNIT_SETTLER')
		Unit["Slave"]	 		= git('UNIT_SLAVE')
		Unit["Warrior"]			= git('UNIT_WARRIOR')
		Unit["Worker"] 			= git('UNIT_WORKER')
		Unit["Workboat"] 		= git('UNIT_WORKBOAT')
		Unit["Wandering Sage"]  = git('UNIT_WANDERING_SAGE')

		self.Units["Generic"] 	= Unit

		""" Equipment """
		Unit = {}
		Unit["Container"] 			= git('EQUIPMENT_CONTAINER')
		Unit["Golden Hammer"] 		= git('EQUIPMENT_GOLDEN_HAMMER')
		Unit["Pieces of Barnaxus"] 	= git('EQUIPMENT_PIECES_OF_BARNAXUS')
		Unit["Treasure"] 			= git('EQUIPMENT_TREASURE')
		self.Units["Equipment"] 	= Unit

		""" Amurites """
		Unit = {}
		Unit["Apprentice"] 		= git('UNIT_APPRENTICE')
		Unit["Battlemage"] 		= git('UNIT_BATTLEMAGE')
		Unit["Bladedancer"] 	= git('UNIT_BLADEDANCER')
		Unit["Chanter"] 		= git('UNIT_CHANTER')
		Unit["Firebow"] 		= git('UNIT_FIREBOW')
		Unit["Spellsword"] 		= git('UNIT_SPELLSWORD')
		Unit["Tower Mage"] 		= git('UNIT_TOWER_MAGE')
		Unit["Wizard"] 			= git('UNIT_WIZARD')
		self.Units["Amurites"] 	= Unit

		""" Archos """
		Unit = {}
		Unit["Baby Spider"] 	= git('UNIT_BABY_SPIDER')
		Unit["Brute"] 			= git('UNIT_BRUTE')
		Unit["Chosen"] 			= git('UNIT_CHOSEN')
		Unit["Eternal"] 		= git('UNIT_ETERNAL')
		Unit["Giant Spider"] 	= git('UNIT_GIANT_SPIDER')
		Unit["Huntsman"] 		= git('UNIT_HUNTSMAN')
		Unit["Nesting Spider"] 	= git('UNIT_NESTING_SPIDER')
		Unit["Recluse"] 		= git('UNIT_RECLUSE')
		Unit["Scorpion"]		= git('UNIT_SCORPION')
		Unit["Scorpion Swarm"]	= git('UNIT_SCORPION_SWARM')
		Unit["Giant Scorpion"]	= git('UNIT_SCORPION_GIANT')
		Unit["Spider"] 			= git('UNIT_SPIDER')
		Unit["Spiderkin"] 		= git('UNIT_SPIDERKIN')
		Unit["Tribesman"] 		= git('UNIT_TRIBESMAN')
		self.Units["Archos"] 	= Unit

		""" Austrin """
		Unit = {}
		Unit["Explorer"] 		= git('UNIT_EXPLORER')
		Unit["Falconer"] 		= git('UNIT_FALCONER')
		Unit["Highlander"] 		= git('UNIT_HIGHLANDER')
		Unit["Recurve Archer"] 	= git('UNIT_RECURVE_ARCHER')
		Unit["Rogue"] 			= git('UNIT_ROGUE')
		Unit["Shore Party"] 	= git('UNIT_SHOREPARTY')
		Unit["Tracker"] 		= git('UNIT_TRACKER')
		Unit["Windsword"] 		= git('UNIT_WINDSWORD')
		self.Units["Austrin"] 	= Unit

		""" Balseraph """
		Unit = {}
		Unit["Courtesan"] 		= git('UNIT_COURTESAN')
		Unit["Freak"] 			= git('UNIT_FREAK')
		Unit["Harlequin"] 		= git('UNIT_HARLEQUIN')
		Unit["Mimic"] 			= git('UNIT_MIMIC')
		Unit["Puppet"] 			= git('UNIT_PUPPET')
		Unit["Puppet (Loki)"] 	= git('UNIT_PUPPET_LOKI')
		Unit["Taskmaster"] 		= git('UNIT_TASKMASTER')
		self.Units["Balseraph"] = Unit

		""" Bannor """
		Unit = {}
		Unit["Cleric"] 			= git('UNIT_CLERIC')
		Unit["Demagog"] 		= git('UNIT_DEMAGOG')
		Unit["Flagbearer"] 		= git('UNIT_FLAGBEARER')
		Unit["Garrison Captain"]= git('UNIT_GARRISON_CAPTAIN')
		self.Units["Bannor"] 	= Unit

		""" Calabim """
		Unit = {}
		Unit["Bloodpet"] 		= git('UNIT_BLOODPET')
		Unit["Brujah"] 			= git('UNIT_BRUJAH')
		Unit["Moroi"] 			= git('UNIT_MOROI')
		Unit["Vampire"]			= git('UNIT_VAMPIRE')
		Unit["Vampire Lord"]	= git('UNIT_VAMPIRE_LORD')
		self.Units["Calabim"] 	= Unit

		""" Chislev """
		Unit = {}
		Unit["Rock Raven"] 		= git('UNIT_ROCK_RAVEN')
		Unit["Windtalker"] 		= git('UNIT_WINDTALKER')
		Unit["Spirit Healer"] 	= git('UNIT_SPIRIT_HEALER')
		self.Units["Chislev"] 	= Unit

		""" Clan of Embers """
		Unit = {}
		Unit["Big Boss"] 			= git('UNIT_BIG_BOSS')
		Unit["Boss"] 				= git('UNIT_BOSS')
		Unit["Lizardman"] 			= git('UNIT_LIZARDMAN')
		Unit["Lizardman Assassin"] 	= git('UNIT_LIZARDMAN_ASSASSIN')
		Unit["Lizardman Beastmaster"] 	= git('UNIT_LIZARDMAN_BEASTMASTER')
		Unit["Lizardman Druid "] 	= git('UNIT_LIZARDMAN_DRUID')
		Unit["Lizardman Ranger"] 	= git('UNIT_LIZARDMAN_RANGER')
		Unit["Ogre"] 				= git('UNIT_OGRE')
		Unit["Ogre Warchief"] 		= git('UNIT_OGRE_WARCHIEF')
		Unit["Overlord"] 			= git('UNIT_ORC_FORT_COMMANDER')
		Unit["Priest of Bhall"] 	= git('UNIT_PRIEST_OF_BHALL')
		Unit["Stoneskin Ogre"] 		= git('UNIT_STONESKIN_OGRE')
		Unit["War Boss"] 			= git('UNIT_WAR_BOSS')
		self.Units["Clan of Embers"]= Unit

		""" Cualli """
		Unit = {}
		Unit["Lizard Worker"] 			= git('UNIT_WORKER_LIZARD')
		Unit["Blowpipe"] 				= git('UNIT_LIZARD_BLOWPIPE')
		Unit["Priest of Agruonn"] 		= git('UNIT_LIZARD_PRIEST_OF_AGRUONN')
		Unit["Shadow Priest of Agruonn"]= git('UNIT_SHADOW_PRIEST_OF_AGRUONN')
		self.Units["Cualli"] 	= Unit

		""" Doviello """
		Unit = {}
		Unit["Battlemaster"] 	= git('UNIT_BATTLEMASTER')
		Unit["Bear Rider"] 		= git('UNIT_BEAR_RIDER')
		Unit["Beastman"]		= git('UNIT_BEASTMAN')
		Unit["Bison Rider"] 	= git('UNIT_BISON_RIDER')
		Unit["Circle of Urd"] 	= git('UNIT_CIRCLE_OF_URD')
		Unit["Skuld"]			= git('UNIT_SKULD')
		Unit["Sons of Asena"] 	= git('UNIT_SONS_OF_ASENA')
		Unit["Verdandi"] 		= git('UNIT_VERDANDI')
		self.Units["Doviello"] 	= Unit

		""" Dural """
		Unit = {}
		Unit["Battle Architect"] 			= git('UNIT_BATTLE_ARCHITECT')
		Unit["Professor"] 					= git('UNIT_PROFESSOR')
		Unit["Student of the Emyprean"]		= git('UNIT_STUDENT_EMPYREAN')
		Unit["Student of the Kilmorph"] 	= git('UNIT_STUDENT_RUNES_OF_KILMORPH')
		Unit["Student of the Leaves"] 		= git('UNIT_STUDENT_FELLOWSHIP_OF_LEAVES')
		Unit["Student of the Order"]		= git('UNIT_STUDENT_THE_ORDER')
		Unit["Student of the Overlords"] 	= git('UNIT_STUDENT_OCTOPUS_OVERLORDS')
		Unit["Student of the Veil"] 		= git('UNIT_STUDENT_THE_ASHEN_VEIL')
		self.Units["Dural"] 	= Unit

		""" Elohim """
		Unit = {}
		Unit["Devout"] 			= git('UNIT_DEVOUT')
		Unit["Monk"] 			= git('UNIT_MONK')
		self.Units["Elohim"] 	= Unit

		""" Frozen """
		Unit = {}
		Unit["Aquilan"] 			= git('UNIT_AQUILAN')
		Unit["Frozen Frost Giant"] 	= git('UNIT_FROST_GIANT')
		Unit["Frozen Souls"] 		= git('UNIT_FROZEN_SOUL')
		Unit["Ice Golem"] 			= git('UNIT_ICE_GOLEM')
		Unit["Kocrachon"] 			= git('UNIT_KOCRACHON')
		Unit["Mulyalfar Elf"] 		= git('UNIT_ICE_DRUID')
		Unit["Nive"] 				= git('UNIT_NIVE')
		Unit["Winter Wolf"] 		= git('UNIT_WOLVERINE')
		Unit["Young Kocrachon"] 	= git('UNIT_YOUNG_KOCRACHON')
		self.Units["Frozen"] 		= Unit

		""" Grigori """
		Unit = {}
		Unit["Adventurer"]			= git('UNIT_ADVENTURER')
		Unit["Dragon Slayer"] 		= git('UNIT_DRAGON_SLAYER')
		Unit["Grigori Medic"] 		= git('UNIT_GRIGORI_MEDIC')
		Unit["Luonnotar"] 			= git('UNIT_LUONNOTAR')
		Unit["Refugee"] 			= git('UNIT_REFUGEE')
		self.Units["Grigori"] 		= Unit

		""" Mekara """
		Unit = {}
		Unit["Aspirant"]			= git('UNIT_ASPIRANT')
		self.Units["Mekara Order"] 		= Unit

		""" Hippus """
		Unit = {}
		Unit["Mounted Mercenary"] 	= git('UNIT_MERCENARY_MOUNTED')
		self.Units["Hippus"] 		= Unit

		""" Infernal """
		Unit = {}
		Unit["Balor"] 				= git('UNIT_BALOR')
		Unit["Death Knight"] 		= git('UNIT_DEATH_KNIGHT')
		Unit["Hellhound"] 			= git('UNIT_HELLHOUND')
		Unit["Imp"] 				= git('UNIT_IMP')
		Unit["Manes"] 				= git('UNIT_MANES')
		Unit["Sect of Flies"] 		= git('UNIT_SECT_OF_FLIES')
		self.Units["Infernal"] 		= Unit

		""" Jotnar """
		Unit = {}
		Unit["Deadeye"] 			= git('UNIT_DEADEYE')
		Unit["Fyrd"] 				= git('UNIT_FYRD')
		Unit["Gothi"] 				= git('UNIT_GOTHI')
		Unit["Herredcarl"] 			= git('UNIT_JOT_FORT_COMMANDER')
		Unit["Hurler"] 				= git('UNIT_HURLER')
		Unit["Huscarl"] 			= git('UNIT_HUSCARL')
		Unit["Jarl"] 				= git('UNIT_JOT_GIANT_CHAMPION')
		Unit["Jotnar Berserker"] 	= git('UNIT_JOT_BERSERKER')
		Unit["Jotnar Citizens"] 	= git('UNIT_JOT_ADULT')
		Unit["Jotnar Freebooters"] 	= git('UNIT_FREEBOOTER')
		Unit["Jotnar Reavers"] 		= git('UNIT_REAVER')
		Unit["Jotnar Settler"] 		= git('UNIT_JOT_SETTLER')
		Unit["Jotnar Slave"] 		= git('UNIT_JOT_SLAVE')
		Unit["Jotun"] 				= git('UNIT_JOTUN')
		Unit["Mouth of the Divine"] = git('UNIT_JOT_MOUTH_OF_THE_DIVINE')
		Unit["Skald"] 				= git('UNIT_JOT_SPEAKER')
		Unit["Sloegrrekkr"] 		= git('UNIT_JOT_ADEPT')
		Unit["Thrall Militia"] 		= git('UNIT_THRALL_MILITIA')
		Unit["Troll Elder"] 		= git('UNIT_JOT_BEASTMASTER')
		Unit["Troll Goblincatcher"] = git('UNIT_TROLL_HUNTER')
		Unit["Troll Trailblazer"] 	= git('UNIT_TROLL_RANGER')
		Unit["Tryggvi"] 			= git('UNIT_TRYGGVI')
		Unit["Vala"] 				= git('UNIT_JOT_HIGH_SPEAKER')
		Unit["Vanir"] 				= git('UNIT_TITAN')
		Unit["Voice of the Divine"] = git('UNIT_VOICE_OF_THE_DIVINE')
		Unit["Wild Troll"] 			= git('UNIT_JOT_TROLL')
		self.Units["Jotnar"] 		= Unit

		""" Kahdi """
		Unit = {}
		Unit["Gnosling"] 		= git('UNIT_GNOSLING')
		Unit["Psion"] 			= git('UNIT_PSION')
		Unit["Thade"] 			= git('UNIT_THADE')
		Unit["Uber Gnosling"] 	= git('UNIT_UBER_GNOSLING')
		self.Units["Kahdi"] 	= Unit

		""" Khazad """
		Unit = {}
		Unit["Auditor"] 			= git('UNIT_AUDITOR')
		Unit["Battering Ram"] 		= git('UNIT_BATTERING_RAM')
		Unit["Boar Rider"] 			= git('UNIT_BOAR_RIDER')
		Unit["ClanHold Chieftain"] 	= git('UNIT_DWARVEN_COMMANDER')
		Unit["Dwarven Cannon"] 		= git('UNIT_DWARVEN_CANNON')
		Unit["Dwarven Defender"] 	= git('UNIT_DWARVEN_DEFENDER')
		Unit["Dwarven Druid"] 		= git('UNIT_DWARVEN_DRUID')
		Unit["Dwarven Shadow"] 		= git('UNIT_DWARVEN_SHADOW')
		Unit["Dwarven Slinger"] 	= git('UNIT_DWARVEN_SLINGER')
		Unit["Hornguard"] 			= git('UNIT_HORNGUARD')
		Unit["Ironclad"] 			= git('UNIT_IRONCLAD')
		Unit["Myconid"] 			= git('UNIT_MYCONID')
		Unit["Trebuchet"] 			= git('UNIT_TREBUCHET')
		self.Units["Khazad"] 		= Unit

		""" Kuriotates """
		Unit = {}
		Unit["Airship"] 			= git('UNIT_AIRSHIP')
		Unit["Centaur"] 			= git('UNIT_CENTAUR')
		Unit["Centaur Archer"] 		= git('UNIT_CENTAUR_ARCHER')
		Unit["Centaur Charger"] 	= git('UNIT_CENTAUR_CHARGER')
		Unit["Centaur Guard"] 		= git('UNIT_CENTAUR_GUARD')
		Unit["Centaur Lancer"] 		= git('UNIT_CENTAUR_LANCER')
		Unit["Pioneer"] 			= git('UNIT_PIONEER')
		Unit["WyrmFisher"] 			= git('UNIT_WYRMFISHER')
		self.Units["Kuriotates"] 	= Unit

		""" Lanun """
		Unit = {}
		Unit["Boarding Party"] 		= git('UNIT_BOARDING_PARTY')
		Unit["Buccaneer"] 			= git('UNIT_BUCCANEER')
		Unit["Pirate"] 				= git('UNIT_PIRATE')
		Unit["War Tortoise"] 		= git('UNIT_WAR_TORTOISE')
		Unit["Workboat"] 			= git('UNIT_WORKBOAT_LANUN')
		self.Units["Lanun"] 		= Unit

		""" Ljosalfar """
		Unit = {}
		Unit["Flurry"] 				= git('UNIT_FLURRY')
		Unit["Fyrdwell"] 			= git('UNIT_FYRDWELL')
		Unit["Sagittar"] 			= git('UNIT_SAGITTAR')
		self.Units["Ljosalfar"] 	= Unit

		""" Luchuirp """
		Unit = {}
		Unit["Bone Golem"] 			= git('UNIT_BONE_GOLEM')
		Unit["Clockwork Golem"] 	= git('UNIT_CLOCKWORK_GOLEM')
		Unit["Gargoyle"] 			= git('UNIT_GARGOYLE')
		Unit["Iron Golem"] 			= git('UNIT_IRON_GOLEM')
		Unit["Mud Golem"] 			= git('UNIT_MUD_GOLEM')
		Unit["Nullstone Golem"] 	= git('UNIT_NULLSTONE_GOLEM')
		Unit["Wood Golem"] 			= git('UNIT_WOOD_GOLEM')
		self.Units["Luchuirp"] 		= Unit

		""" Malakim """
		Unit = {}
		Unit["Anubis"] 				= git('UNIT_ANUBIS')
		Unit["Camel Archer"] 		= git('UNIT_CAMEL_ARCHER')
		Unit["Champion"] 			= git('UNIT_CHAMPION_MALAKIM')
		Unit["Dervish"] 			= git('UNIT_SHADOW_MALAKIM')
		Unit["Lightbringer"] 		= git('UNIT_LIGHTBRINGER')
		Unit["Horseman"] 			= git('UNIT_HORSEMAN_MALAKIM')
		Unit["Knight"] 				= git('UNIT_KNIGHT_MALAKIM')
		Unit["Worker"]		 		= git('UNIT_WORKER_MALAKIM')
		self.Units["Malakim"] 		= Unit

		""" Mazatl """
		Unit = {}
		Unit["Lizard Worker"]       = git('UNIT_WORKER_LIZARD')
		Unit["Priest of Kalshekk"]  = git('UNIT_LIZARD_PRIEST_OF_KALSHEKK')
		Unit["Priest of Omorr"]     = git('UNIT_LIZARD_PRIEST_OF_OMORR')
		Unit["Wyvern Guardian"]     = git('UNIT_DRAGON_GUARDIAN')
		self.Units["Mazatl"]        = Unit

		""" Mechanos """
		Unit = {}
		Unit["Adeptus"] 			= git('UNIT_ADEPTUS')
		Unit["Thopter"] 			= git('UNIT_THOPTER')
		Unit["Dirigible Fleet"] 	= git('UNIT_DIRIGIBLE')
		Unit["Dragoon"] 			= git('UNIT_DRAGOON')
		Unit["Flamethrower"] 		= git('UNIT_FLAMETHROWER')
		Unit["Grenadier"] 			= git('UNIT_GRENADIER')
		Unit["Handgunner"] 			= git('UNIT_HANDGUNNER')
		Unit["Howitzer"] 			= git('UNIT_MECHANOS_CANNON')
		Unit["Mobile Fortress"] 	= git('UNIT_MOBILE_FORTRESS')
		Unit["Musketman"] 			= git('UNIT_MUSKETMAN')
		Unit["Organ Gun"] 			= git('UNIT_ORGAN_GUN')
		Unit["Techpriest"] 			= git('UNIT_TECHPRIEST')
		Unit["Vulture"] 			= git('UNIT_VULTURE')
		Unit["Witchhunter"] 		= git('UNIT_WITCHHUNTER')
		Unit["Operator"] 	        = git('UNIT_OPERATOR')
		Unit["Aquilan Thopter"] 	= git('UNIT_AQUILAN_THOPTER')
		Unit["Mortar"] 				= git('UNIT_MORTAR_MACHINARUM')
		Unit["Steamtank"] 			= git('UNIT_STEAMTANK')
		self.Units["Mechanos"] 		= Unit

		""" Mercurian """
		Unit = {}
		Unit["Angel"] 				= git('UNIT_ANGEL')
		Unit["Angel of Death"] 		= git('UNIT_ANGEL_OF_DEATH')
		Unit["Herald"] 				= git('UNIT_HERALD')
		Unit["Ophanim"] 			= git('UNIT_OPHANIM')
		Unit["Repentant Angel"] 	= git('UNIT_REPENTANT_ANGEL')
		Unit["Seraph"] 				= git('UNIT_SERAPH')
		Unit["Valkyrie"] 			= git('UNIT_VALKYRIE')
		self.Units["Mercurian"] 	= Unit

		""" Scions """
		Unit = {}
		Unit["Abomination"] 		= git('UNIT_ABOMINATION')
		Unit["Awakened"] 			= git('UNIT_AWAKENED')
		Unit["Bone Horde"] 			= git('UNIT_BONE_HORDE')
		Unit["Centeni"] 			= git('UNIT_CENTENI')
		Unit["Cetratus"] 			= git('UNIT_CETRATUS')
		Unit["Doomgiver"] 			= git('UNIT_DOOMGIVER')
		Unit["Doomsayer"] 			= git('UNIT_DOOMSAYER')
		Unit["Emperors Dagger"] 	= git('UNIT_EMPERORS_DAGGER')
		Unit["Ghostwalker"] 		= git('UNIT_GHOSTWALKER')
		Unit["Haunt"] 				= git('UNIT_HAUNT')
		Unit["Honored Band"] 		= git('UNIT_HONORED_BAND')
		Unit["Horned Dread"] 		= git('UNIT_BEASTMASTER_SCION')
		Unit["Legate"] 				= git('UNIT_LEGATE')
		Unit["Martyrs of Patria"] 	= git('UNIT_MARTYR_OF_PATRIA')
		Unit["Necromancer"] 		= git('UNIT_NECROMANCER')
		Unit["Praetorian"] 			= git('UNIT_PRAETORIAN')
		Unit["Principes"] 			= git('UNIT_PRINCIPES')
		Unit["Reaching Creeper"] 	= git('UNIT_CREEPER')
		Unit["Reborn"] 				= git('UNIT_REBORN')
		Unit["Redactor"] 			= git('UNIT_REDACTOR')
		Unit["Revenant"] 			= git('UNIT_REVENANT')
		Unit["Settler"] 			= git('UNIT_SETTLER_SCIONS')
		Unit["Velite"] 				= git('UNIT_VELITES')
		Unit["Wraith Lord"] 		= git('UNIT_WRAITH_LORD')
		self.Units["Scions"] 		= Unit

		""" Sheaim """
		Unit = {}
		Unit["Chaos Marauder"] 		= git('UNIT_CHAOS_MARAUDER')
		Unit["Eater of Dreams"] 	= git('UNIT_EATER_OF_DREAMS')
		Unit["Manticore"] 			= git('UNIT_MANTICORE')
		Unit["Minotaur"] 			= git('UNIT_MINOTAUR')
		Unit["Mobius Witch"] 		= git('UNIT_MOBIUS_WITCH')
		Unit["Pyrelord"] 			= git('UNIT_PYRELORD')
		Unit["Pyre Zombie"] 		= git('UNIT_PYRE_ZOMBIE')
		Unit["Revelers"] 			= git('UNIT_REVELERS')
		Unit["Succubus"] 			= git('UNIT_SUCCUBUS')
		Unit["Tar Demon"] 			= git('UNIT_TAR_DEMON')
		Unit["Burning Eye"] 		= git('UNIT_BURNING_EYE')
		Unit["Colubra"] 		= git('UNIT_COLUBRA')
		self.Units["Sheaim"] 		= Unit

		""" Sidar """
		Unit = {}
		Unit["Divided Soul"] 		= git('UNIT_DIVIDED_SOUL')
		Unit["Ghost"] 				= git('UNIT_GHOST')
		Unit["Severed Soul"] 		= git('UNIT_SEVERED_SOUL')
		Unit["Shade"] 				= git('UNIT_SHADE')
		Unit["Trackless"] 			= git('UNIT_TRACKLESS')
		self.Units["Sidar"] 		= Unit

		""" Svartalfar """
		Unit = {}
		Unit["Illusionist"] 		= git('UNIT_ILLUSIONIST')
		Unit["Nyxkin"] 				= git('UNIT_NYXKIN')
		self.Units["Svartalfar"] 	= Unit

		""" D'Tesh """
		Unit = {}
		Unit["Binder"] 				= git('UNIT_BINDER')
		Unit["Chosen of D'Tesh"] 	= git('UNIT_CHOSEN_DTESH')
		Unit["Council of Four"] 	= git('UNIT_COUNCIL_EIGHT')
		Unit["D'teshi Commander"] 	= git('UNIT_DTESHI_COMMANDER')
		Unit["Dullahan"]			= git('UNIT_COMMANDER_FALLEN')
		Unit["Vessel of D'tesh"]	= git('UNIT_VESSEL_DTESH')
		Unit["Slave"]               = git('UNIT_SLAVE_UNDEAD')
		Unit["Funeral Barge"]		= git('UNIT_FUNERAL_BARGE')
		self.Units["D'Tesh"] 		= Unit

		""" Order """
		Unit = {}
		Unit["Disciple"] 		= git('UNIT_DISCIPLE_THE_ORDER')
		Unit["Confessor"] 		= git('UNIT_PRIEST_OF_THE_ORDER')
		Unit["Prior"] 			= git('UNIT_HIGH_PRIEST_OF_THE_ORDER')
		Unit["Crusader"] 		= git('UNIT_CRUSADER')
		Unit["Mendacite"] 		= git('UNIT_MENDACITE_ORDER')
		self.Units["Order"] 	= Unit

		""" Veil """
		Unit = {}
		Unit["Disciple"] 		= git('UNIT_DISCIPLE_THE_ASHEN_VEIL')
		Unit["Ritualist"] 		= git('UNIT_PRIEST_OF_THE_VEIL')
		Unit["Profane"] 		= git('UNIT_HIGH_PRIEST_OF_THE_VEIL')
		Unit["Diseased Corpse"] = git('UNIT_DISEASED_CORPSE')
		Unit["Beast of Agares"] = git('UNIT_BEAST_OF_AGARES')
		Unit["Mendacite"] 		= git('UNIT_MENDACITE_AV')
		self.Units["Veil"] 		= Unit

		""" Esus """
		Unit = {}
		Unit["Nightwatch"] 		= git('UNIT_NIGHTWATCH')
		Unit["Shadow"] 			= git('UNIT_SHADOW')
		Unit["Shadowrider"] 	= git('UNIT_SHADOWRIDER')
		self.Units["Esus"] 		= Unit

		""" Empyrean """
		Unit = {}
		Unit["Disciple"] 		= git('UNIT_DISCIPLE_EMPYREAN')
		Unit["Vicar"] 			= git('UNIT_PRIEST_OF_THE_EMPYREAN')
		Unit["Luridus"] 		= git('UNIT_HIGH_PRIEST_OF_THE_EMPYREAN')
		Unit["Radiant Guard"] 	= git('UNIT_RADIANT_GUARD')
		Unit["Ratha"] 			= git('UNIT_RATHA')
		Unit["Mendacite"] 		= git('UNIT_MENDACITE_EMPY')
		self.Units["Empyrean"] 	= Unit

		""" Leaves """
		Unit = {}
		Unit["Disciple"] 				= git('UNIT_DISCIPLE_FELLOWSHIP_OF_LEAVES')
		Unit["Priest of Leaves"] 		= git('UNIT_PRIEST_OF_LEAVES')
		Unit["High Priest of Leaves"] 	= git('UNIT_HIGH_PRIEST_OF_LEAVES')
		Unit["Fawn"] 					= git('UNIT_FAWN')
		Unit["Satyr"] 					= git('UNIT_SATYR')
		Unit["Mendacite"] 				= git('UNIT_MENDACITE_LEAVES')
		self.Units["Leaves"] 			= Unit

		""" Overlords """
		Unit = {}
		Unit["Disciple"] 				= git('UNIT_DISCIPLE_OCTOPUS_OVERLORDS')
		Unit["Cultist"] 				= git('UNIT_PRIEST_OF_THE_OVERLORDS')
		Unit["Speaker"] 				= git('UNIT_HIGH_PRIEST_OF_THE_OVERLORDS')
		Unit["Drown"] 					= git('UNIT_DROWN')
		Unit["Lunatic"] 				= git('UNIT_LUNATIC')
		Unit["Stygian Guard"] 			= git('UNIT_STYGIAN_GUARD')
		Unit["Mendacite"] 				= git('UNIT_MENDACITE_OO')
		self.Units["Overlords"] 		= Unit

		""" Runes """
		Unit = {}
		Unit["Disciple"] 				= git('UNIT_DISCIPLE_RUNES_OF_KILMORPH')
		Unit["Stonewarden"] 			= git('UNIT_PRIEST_OF_KILMORPH')
		Unit["Runekeeper"] 				= git('UNIT_HIGH_PRIEST_OF_KILMORPH')
		Unit["Soldier of Kilmorph"] 	= git('UNIT_DWARVEN_SOLDIER_RUNES')
		Unit["Paramander"] 				= git('UNIT_PARAMANDER')
		Unit["Mendacite"] 				= git('UNIT_MENDACITE_RUNES')
		self.Units["Runes"] 			= Unit

		""" White Hand """
		Unit = {}
		Unit["Disciple"] 			= git('UNIT_DISCIPLE_OF_WINTER')
		Unit["Priest"] 				= git('UNIT_PRIEST_OF_WINTER')
		Unit["High Priest"] 		= git('UNIT_HIGH_PRIEST_OF_WINTER')
		Unit["Frostling Archer"] 	= git('UNIT_FROSTLING_ARCHER_WH')
		Unit["Frost Giant"] 		= git('UNIT_FROST_GIANT')
		self.Units["White Hand"] 	= Unit

		""" Animal """
		Unit = {}
		Unit["Bear"]				= git('UNIT_BEAR')
		Unit["Bear group"]				= git('UNIT_BEAR_GROUP')
		Unit["Cave Bears"]			= git('UNIT_CAVE_BEARS')
		Unit["Boar"]				= git('UNIT_BOAR')
		Unit["Boar Herd"]			= git('UNIT_BOAR_HERD')
		Unit["Blood Boar"]			= git('UNIT_BLOOD_BOAR')
		Unit["Shardik"]				= git('UNIT_SHARDIK')
		Unit["Lion"]				= git('UNIT_LION')
		Unit["Lion Pride"]			= git('UNIT_LION_PRIDE')
		Unit["Tiger"]				= git('UNIT_TIGER')
		Unit["Sabretooth"]			= git('UNIT_SABRETOOTH')
		Unit["Black Drake"]			= git('UNIT_BLACK_DRAKE')
		Unit["Brass Drake"]			= git('UNIT_BRASS_DRAKE')
		Unit["Red Drake"]			= git('UNIT_RED_DRAKE')
		Unit["White Drake"]			= git('UNIT_WHITE_DRAKE')
		Unit["Gorilla"]				= git('UNIT_GORILLA')
		Unit["Gorilla Troop"]		= git('UNIT_GORILLA_TROOP')
		Unit["Silverback"]			= git('UNIT_SILVERBACK')
		Unit["Hippogriff"]			= git('UNIT_HIPPOGRIFF')
		Unit["Griffon"]				= git('UNIT_GRIFFON')
		Unit["Roc"]					= git('UNIT_ROC')
		Unit["Raptor"]				= git('UNIT_RAPTOR')
		Unit["Allosaur"]			= git('UNIT_ALLOSAUR')
		Unit["Tyrant"]				= git('UNIT_TYRANT')
		Unit["Scorpion"]			= git('UNIT_SCORPION')
		Unit["Scorpion Swarm"]		= git('UNIT_SCORPION_SWARM')
		Unit["Giant Scorpion"]		= git('UNIT_SCORPION_GIANT')
		Unit["Baby Spider"]			= git('UNIT_BABY_SPIDER')
		Unit["Spider"]				= git('UNIT_SPIDER')
		Unit["Giant Spider"]		= git('UNIT_GIANT_SPIDER')
		Unit["Stag"]				= git('UNIT_STAG')
		Unit["Elk"]					= git('UNIT_ELK')
		Unit["Wolf"]				= git('UNIT_WOLF')
		Unit["Wolf Pack"]			= git('UNIT_WOLF_PACK')
		Unit["Dire Wolf"]			= git('UNIT_DIRE_WOLF')
		Unit["Elephant"]			= git('UNIT_ELEPHANT')
		Unit["Mammoth"]				= git('UNIT_MAMMOTH')
		Unit["Sand Wyrm"]			= git('UNIT_SAND_WORM')
		Unit["Ice Wyrm"]			= git('UNIT_ICE_WORM')
		Unit["Marsh Wyrm"]			= git('UNIT_MARSH_WORM')
		Unit["Sea Serpent"]			= git('UNIT_SEA_SERPENT')
		Unit["Giant Tortoise"]		= git('UNIT_GIANT_TORTOISE')
		Unit["Kraken"]				= git('UNIT_KRAKEN')
		Unit["Diakonos"]			= git('UNIT_DIAKONOS')
		Unit["Forest Creeper"]		= git('UNIT_FOREST_CREEPER')
		Unit["Malignant Flora"]		= git('UNIT_MALIGNANT_COMMANDER')
		self.Units["Animal"] 		= Unit

		""" Summons """
		Unit = {}
		Unit["Air Elemental"] 			= git('UNIT_AIR_ELEMENTAL')
		Unit["Aurealis"] 				= git('UNIT_AUREALIS')
		Unit["Azer"] 					= git('UNIT_AZER')
		Unit["Djinn"] 					= git('UNIT_DJINN')
		Unit["Earth Elemental"] 		= git('UNIT_EARTH_ELEMENTAL')
		Unit["Fire Elemental"] 			= git('UNIT_FIRE_ELEMENTAL')
		Unit["Fireball"] 				= git('UNIT_FIREBALL')
		Unit["Flesh Golem"] 			= git('UNIT_FLESH_GOLEM')
		Unit["Floating Eye"] 			= git('UNIT_EYE')
		Unit["Guardian Vines"]			= git('UNIT_GUARDIAN_VINES')
		Unit["Holy Avenger"] 			= git('UNIT_HOLY_AVENGER')
		Unit["Einherjar"] 				= git('UNIT_EINHERJAR')
		Unit["Ice Elemental"] 			= git('UNIT_ICE_ELEMENTAL')
		Unit["Ira"] 					= git('UNIT_IRA')
		Unit["Lich"]	 				= git('UNIT_LICH')
		Unit["Lightning Elemental"] 	= git('UNIT_LIGHTNING_ELEMENTAL')
		Unit["Meteor"] 					= git('UNIT_METEOR')
		Unit["Mistform"] 				= git('UNIT_MISTFORM')
		Unit["Pegasus"] 				= git('UNIT_PEGASUS')
		Unit["Pit Beast"] 				= git('UNIT_PIT_BEAST')
		Unit["Sand Lion"] 				= git('UNIT_SAND_LION')
		Unit["Shooting Star"] 			= git('UNIT_SHOOTING_STAR')
		Unit["Skeleton"] 				= git('UNIT_SKELETON')
		Unit["Spectre"] 				= git('UNIT_SPECTRE')
		Unit["Treant"] 					= git('UNIT_TREANT')
		Unit["Tree of Life"] 			= git('UNIT_TREE_OF_LIFE')
		Unit["Vyrkul"] 					= git('UNIT_VYRKUL')
		Unit["Water Elemental"] 		= git('UNIT_WATER_ELEMENTAL')
		Unit["Wraith"] 					= git('UNIT_WRAITH')
		self.Units["Summons"] 	= Unit

		""" Savage """
		Unit = {}
		Unit["Cyklop"] 				= git('UNIT_CYKLOP')
		Unit["Goblin"] 				= git('UNIT_GOBLIN')
		Unit["Hill Giant"] 			= git('UNIT_HILL_GIANT')
		Unit["Minotaur"] 			= git('UNIT_MINOTAUR_LESSER')
		Unit["Wolf Rider"] 			= git('UNIT_WOLF_RIDER')
		self.Units["Savage"] 		= Unit

		""" Frostlings """
		Unit = {}
		Unit["Frostling"] 			= git('UNIT_FROSTLING')
		Unit["Archer"] 				= git('UNIT_FROSTLING_ARCHER')
		Unit["Wolf Rider"] 			= git('UNIT_FROSTLING_WOLF_RIDER')
		self.Units["Frostling"] 	= Unit

		""" Scorpion Clan """
		Unit = {}
		Unit["Archer"] 				= git('UNIT_ARCHER_SCORPION_CLAN')
		Unit["Chariot"] 			= git('UNIT_CHARIOT_SCORPION_CLAN')
		Unit["Goblin"] 				= git('UNIT_GOBLIN_SCORPION_CLAN')
		Unit["Whelp"] 				= git('UNIT_SCORPION_CLAN_WHELP')
		Unit["Wolf Rider"] 			= git('UNIT_WOLF_RIDER_SCORPION_CLAN')
		Unit["Sapper"]				= git('UNIT_GOBLIN_SAPPER')
		Unit["Wolf Archer"]			= git('UNIT_GOBLIN_WOLF_ARCHER')
		Unit["Lord"]				= git('UNIT_GOBLIN_LORD')
		self.Units["Scorpion Clan"] = Unit

		""" Goblins """
		Unit = {}
		Unit["Gretchin"] 			= git('UNIT_GRETCHIN')
		self.Units["Goblins"] = Unit

	def getUnitClassDict(self): return self.UnitClasses
	def initUnitClassDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		UnitClass = {}

		UnitClass["Fort Commander"]		= git('UNITCLASS_FORT_COMMANDER')
		
		UnitClass["Adventurer"]		= git('UNITCLASS_ADVENTURER')
		UnitClass["Awakened"]		= git('UNITCLASS_AWAKENED')
		UnitClass["Archer"] 			= git('UNITCLASS_ARCHER')
		UnitClass["Axeman"] 			= git('UNITCLASS_AXEMAN')
		UnitClass["Assassin"]		= git('UNITCLASS_ASSASSIN')
		UnitClass["Settler"]			= git('UNITCLASS_SETTLER')
		UnitClass["Fireball"]		= git('UNITCLASS_FIREBALL')

		UnitClass["Catapult"]		= git('UNITCLASS_CATAPULT')
		UnitClass["Champion"]		= git('UNITCLASS_CHAMPION')
		UnitClass["Chariot"]			= git('UNITCLASS_CHARIOT')
		UnitClass["War Chariot"]		= git('UNITCLASS_WAR_CHARIOT')
		UnitClass["Horse Archer"]	= git('UNITCLASS_HORSE_ARCHER')
		UnitClass["Longbowman"]		= git('UNITCLASS_LONGBOWMAN')
		UnitClass["Demagog"]			= git('UNITCLASS_DEMAGOG')
		UnitClass["Creeper"]			= git('UNITCLASS_CREEPER')
		UnitClass["Reborn"]			= git('UNITCLASS_REBORN')

		UnitClass["Ranger"]			= git('UNITCLASS_RANGER')
		UnitClass["Haunt"]			= git('UNITCLASS_HAUNT')
		UnitClass["Druid"]			= git('UNITCLASS_DRUID')
		UnitClass["Cyklop"] 			= git('UNITCLASS_CYKLOP')
		UnitClass["Fawn"] 			= git('UNITCLASS_FAWN')
		UnitClass["Frostling"] 		= git('UNITCLASS_FROSTLING')
		UnitClass["Hill Giant"] 		= git('UNITCLASS_HILL_GIANT')
		UnitClass["Horseman"] 		= git('UNITCLASS_HORSEMAN')
		UnitClass["Hunter"] 			= git('UNITCLASS_HUNTER')
		UnitClass["Scout"] 			= git('UNITCLASS_SCOUT')
		UnitClass["Supplies"] 		= git('UNITCLASS_SUPPLIES')
		UnitClass["Warrior"] 		= git('UNITCLASS_WARRIOR')
		UnitClass["Worker"] 			= git('UNITCLASS_WORKER')

		UnitClass["Revelers"] 		= git('UNITCLASS_REVELERS')
		UnitClass["Mobius Witch"]	= git('UNITCLASS_MOBIUS_WITCH')
		UnitClass["Chaos Marauder"]	= git('UNITCLASS_CHAOS_MARAUDER')
		UnitClass["Manticore"]		= git('UNITCLASS_MANTICORE')
		UnitClass["Succubus"]		= git('UNITCLASS_SUCCUBUS')
		UnitClass["Minotaur"] 		= git('UNITCLASS_MINOTAUR')
		UnitClass["Tar Demon"]		= git('UNITCLASS_TAR_DEMON')
		UnitClass["Colubra"]		= git('UNITCLASS_COLUBRA')

		UnitClass["Djinn"]	 		= git('UNITCLASS_DJINN')
		UnitClass["Fire Elemental"]	= git('UNITCLASS_FIRE_ELEMENTAL')
		UnitClass["Air Elemental"]	= git('UNITCLASS_AIR_ELEMENTAL')
		UnitClass["Spectre"]	 		= git('UNITCLASS_SPECTRE')
		UnitClass["Flesh Golem"]		= git('UNITCLASS_FLESH_GOLEM')
		UnitClass["Pit Beast"]		= git('UNITCLASS_PIT_BEAST')
		UnitClass["Ice Elemental"]	= git('UNITCLASS_ICE_ELEMENTAL')
		UnitClass["Einherjar"]		= git('UNITCLASS_EINHERJAR')
		UnitClass["Mistform"]	 	= git('UNITCLASS_MISTFORM')
		UnitClass["Aurealis"]		= git('UNITCLASS_AUREALIS')
		UnitClass["Water Elemental"]	= git('UNITCLASS_WATER_ELEMENTAL')
		UnitClass["Psion"]			= git('UNITCLASS_PSION')
		UnitClass["Gnossling"] 		= git('UNITCLASS_GNOSLING')
		UnitClass["Thade"]	 		= git('UNITCLASS_THADE')

		UnitClass["Baby Spider"]	= git('UNITCLASS_BABY_SPIDER')
		UnitClass["Spider"]			= git('UNITCLASS_SPIDER')
		UnitClass["Giant Spider"]	= git('UNITCLASS_GIANT_SPIDER')

		UnitClass["Scorpion"]		= git('UNITCLASS_SCORPION')
		UnitClass["Scorpion Swarm"] = git('UNITCLASS_SCORPION_SWARM')
		UnitClass["Giant Scorpion"] = git('UNITCLASS_SCORPION_GIANT')

		UnitClass["Disciple Empyrean"]	= git('UNITCLASS_DISCIPLE_EMPYREAN')
		UnitClass["Disciple Leaves"]		= git('UNITCLASS_DISCIPLE_FELLOWSHIP_OF_LEAVES')
		UnitClass["Disciple Overlords"]	= git('UNITCLASS_DISCIPLE_OCTOPUS_OVERLORDS')
		UnitClass["Disciple Kilmorph"]	= git('UNITCLASS_DISCIPLE_RUNES_OF_KILMORPH')
		UnitClass["Disciple Veil"]		= git('UNITCLASS_DISCIPLE_THE_ASHEN_VEIL')
		UnitClass["Disciple Order"]		= git('UNITCLASS_DISCIPLE_THE_ORDER')

		UnitClass["Priest of Leaves"]	= git('UNITCLASS_PRIEST_OF_LEAVES')
		UnitClass["Priest of Kilmorph"]	= git('UNITCLASS_PRIEST_OF_KILMORPH')
		UnitClass["Priest of Order"]		= git('UNITCLASS_PRIEST_OF_THE_ORDER')
		UnitClass["Priest of Empyrean"]	= git('UNITCLASS_PRIEST_OF_THE_EMPYREAN')
		UnitClass["Priest of Overlords"]	= git('UNITCLASS_PRIEST_OF_THE_OVERLORDS')
		UnitClass["Priest of Veil"]		= git('UNITCLASS_PRIEST_OF_THE_VEIL')

		# These are already in Heroes
		UnitClass["Basium"] 				= git('UNITCLASS_BASIUM')
		UnitClass["Hyborem"] 			= git('UNITCLASS_HYBOREM')
		UnitClass["Kahd"] 				= git('UNITCLASS_KAHD')
		UnitClass["Orthus"] 				= git('UNITCLASS_ORTHUS')
		UnitClass["Zarcaz"] 				= git('UNITCLASS_ZARCAZ')
		UnitClass["Korrina Black"]		= git('UNITCLASS_KORRINA_BLACK_LADY')
		self.UnitClasses = UnitClass

	def getPromotionDict(self): return self.Promotions
	def initPromotionDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		""" Generic """
		Promo = {}
		Promo["Amphibious"]			= git('PROMOTION_AMPHIBIOUS')
		Promo["Air I"] 				= git('PROMOTION_AIR1')
		Promo["Air II"] 			= git('PROMOTION_AIR2')
		Promo["Air III"] 			= git('PROMOTION_AIR3')
		Promo["Body I"] 			= git('PROMOTION_BODY1')
		Promo["Body II"] 			= git('PROMOTION_BODY2')
		Promo["Body III"] 			= git('PROMOTION_BODY3')
		Promo["Chaos I"] 			= git('PROMOTION_CHAOS1')
		Promo["Chaos II"] 			= git('PROMOTION_CHAOS2')
		Promo["Chaos III"] 			= git('PROMOTION_CHAOS3')
		Promo["Commando"]			= git('PROMOTION_COMMANDO')

		Promo["Combat I"]			= git('PROMOTION_COMBAT1')
		Promo["Combat II"]			= git('PROMOTION_COMBAT2')
		Promo["Combat III"]			= git('PROMOTION_COMBAT3')
		Promo["Combat IV"]			= git('PROMOTION_COMBAT4')
		Promo["Combat V"]			= git('PROMOTION_COMBAT5')

		Promo["Corpus I"] 			= git('PROMOTION_CORPUS1')
		Promo["Corpus II"] 			= git('PROMOTION_CORPUS2')
		Promo["Corpus III"] 		= git('PROMOTION_CORPUS3')
		Promo["Crazed"]				= git('PROMOTION_CRAZED')
		Promo["Creation I"] 		= git('PROMOTION_CREATION1')
		Promo["Creation II"] 		= git('PROMOTION_CREATION2')
		Promo["Creation III"] 		= git('PROMOTION_CREATION3')
		Promo["Death I"] 			= git('PROMOTION_DEATH1')
		Promo["Death II"] 			= git('PROMOTION_DEATH2')
		Promo["Death III"] 			= git('PROMOTION_DEATH3')
		Promo["Defensive"]			= git('PROMOTION_DEFENSIVE')
		Promo["Dimensional I"] 		= git('PROMOTION_DIMENSIONAL1')
		Promo["Dimensional II"] 	= git('PROMOTION_DIMENSIONAL2')
		Promo["Dimensional III"] 	= git('PROMOTION_DIMENSIONAL3')
		Promo["Earth I"] 			= git('PROMOTION_EARTH1')
		Promo["Earth II"] 			= git('PROMOTION_EARTH2')
		Promo["Earth III"] 			= git('PROMOTION_EARTH3')
		Promo["Eastwinds"]			= git('PROMOTION_EASTWINDS')
		Promo["Enraged"]			= git('PROMOTION_ENRAGED')

		Promo["Empower I"]			= git('PROMOTION_EMPOWER1')
		Promo["Empower II"]			= git('PROMOTION_EMPOWER2')
		Promo["Empower III"]		= git('PROMOTION_EMPOWER3')
		Promo["Empower IV"]			= git('PROMOTION_EMPOWER4')
		Promo["Empower V"]			= git('PROMOTION_EMPOWER5')

		Promo["Enchantment I"] 		= git('PROMOTION_ENCHANTMENT1')
		Promo["Enchantment II"] 	= git('PROMOTION_ENCHANTMENT2')
		Promo["Enchantment III"] 	= git('PROMOTION_ENCHANTMENT3')
		Promo["Entropy I"] 			= git('PROMOTION_ENTROPY1')
		Promo["Entropy II"] 		= git('PROMOTION_ENTROPY2')
		Promo["Entropy III"] 		= git('PROMOTION_ENTROPY3')
		Promo["Fire I"] 			= git('PROMOTION_FIRE1')
		Promo["Fire II"] 			= git('PROMOTION_FIRE2')
		Promo["Fire III"] 			= git('PROMOTION_FIRE3')
		Promo["Force I"] 			= git('PROMOTION_FORCE1')
		Promo["Force II"] 			= git('PROMOTION_FORCE2')
		Promo["Force III"] 			= git('PROMOTION_FORCE3')
		Promo["Hardy I"] 			= git('PROMOTION_HARDY1')
		Promo["Hardy II"] 			= git('PROMOTION_HARDY2')
		Promo["Hardy III"] 			= git('PROMOTION_HARDY3')
		Promo["Headless"]			= git('PROMOTION_HEADLESS')
		Promo["Ice I"] 				= git('PROMOTION_ICE1')
		Promo["Ice II"] 			= git('PROMOTION_ICE2')
		Promo["Ice III"] 			= git('PROMOTION_ICE3')
		Promo["Law I"] 				= git('PROMOTION_LAW1')
		Promo["Law II"] 			= git('PROMOTION_LAW2')
		Promo["Law III"] 			= git('PROMOTION_LAW3')
		Promo["Life I"] 			= git('PROMOTION_LIFE1')
		Promo["Life II"] 			= git('PROMOTION_LIFE2')
		Promo["Life III"] 			= git('PROMOTION_LIFE3')
		Promo["Magic Resistance"]	= git('PROMOTION_MAGIC_RESISTANCE')
		Promo["Metamagic I"] 		= git('PROMOTION_METAMAGIC1')
		Promo["Metamagic II"] 		= git('PROMOTION_METAMAGIC2')
		Promo["Metamagic III"] 		= git('PROMOTION_METAMAGIC3')
		Promo["Mind I"] 			= git('PROMOTION_MIND1')
		Promo["Mind II"] 			= git('PROMOTION_MIND2')
		Promo["Mind III"] 			= git('PROMOTION_MIND3')
		Promo["Mobility I"] 		= git('PROMOTION_MOBILITY1')
		Promo["Mobility II"] 		= git('PROMOTION_MOBILITY2')
		Promo["Nature I"] 			= git('PROMOTION_NATURE1')
		Promo["Nature II"] 			= git('PROMOTION_NATURE2')
		Promo["Nature III"] 		= git('PROMOTION_NATURE3')
		Promo["Perfect Sight"]		= git('PROMOTION_PERFECT_SIGHT')
		Promo["Shadow I"] 			= git('PROMOTION_SHADOW1')
		Promo["Shadow II"] 			= git('PROMOTION_SHADOW2')
		Promo["Shadow III"] 		= git('PROMOTION_SHADOW3')
		Promo["Spirit I"] 			= git('PROMOTION_SPIRIT1')
		Promo["Spirit II"] 			= git('PROMOTION_SPIRIT2')
		Promo["Spirit III"] 		= git('PROMOTION_SPIRIT3')
		Promo["Sun I"] 				= git('PROMOTION_SUN1')
		Promo["Sun II"] 			= git('PROMOTION_SUN2')
		Promo["Sun III"] 			= git('PROMOTION_SUN3')
		Promo["Water I"] 			= git('PROMOTION_WATER1')
		Promo["Water II"] 			= git('PROMOTION_WATER2')
		Promo["Water III"] 			= git('PROMOTION_WATER3')
		Promo["Woodsman I"]			= git('PROMOTION_WOODSMAN1')
		self.Promotions["Generic"] 	= Promo

		""" Effects """
		Promo = {}
		Promo["Alive"] 				= git('PROMOTION_ALIVE')
		Promo["Ambition"] 			= git('PROMOTION_AMBITION')
		Promo["Acheron Leashed"] 	= git('PROMOTION_ACHERON_LEASHED')
		Promo["Held"] 				= git('PROMOTION_HELD')
		Promo["Channeling I"] 		= git('PROMOTION_CHANNELING1')
		Promo["Channeling II"]		= git('PROMOTION_CHANNELING2')
		Promo["Channeling III"]		= git('PROMOTION_CHANNELING3')
		Promo["Chosen"]             = git('PROMOTION_CHOSEN')
		Promo["Deathmarked"]        = git('PROMOTION_DEATHMARKED')
		Promo["Hero"] 				= git('PROMOTION_HERO')
		Promo["Heroic Defense I"] 	= git('PROMOTION_HEROIC_DEFENSE')
		Promo["Heroic Defense II"] 	= git('PROMOTION_HEROIC_DEFENSE2')
		Promo["Heroic Strength I"] 	= git('PROMOTION_HEROIC_STRENGTH')
		Promo["Heroic Strength II"] = git('PROMOTION_HEROIC_STRENGTH2')
		Promo["Hidden"]			 	= git('PROMOTION_HIDDEN')
		Promo["Hidden Nationality"] = git('PROMOTION_HIDDEN_NATIONALITY')
		Promo["Immortal"] 			= git('PROMOTION_IMMORTAL')
		Promo["Immune Disease"]		= git('PROMOTION_IMMUNE_DISEASE')
		Promo["Loyalty III"]		= git('PROMOTION_LOYALTY3')
		Promo["Mana Guardian"] 		= git('PROMOTION_MANA_GUARDIAN')
		Promo["Spiderkin"] 			= git('PROMOTION_SPIDERKIN')
		Promo["Strong"] 			= git('PROMOTION_STRONG')
		Promo["Starting Settler"]	= git('PROMOTION_STARTING_SETTLER')
		Promo["Bronze Weapons"]		= git('PROMOTION_BRONZE_WEAPONS')
		Promo["Iron Weapons"]		= git('PROMOTION_IRON_WEAPONS')
		Promo["Mithril Weapons"]	= git('PROMOTION_MITHRIL_WEAPONS')
		Promo["Rusted"]				= git('PROMOTION_RUSTED')
		Promo["Shackled"]			= git('PROMOTION_SHACKLED')
		Promo["Spirit Guide"]		= git('PROMOTION_SPIRIT_GUIDE')
		Promo["Weak"] 				= git('PROMOTION_WEAK')
		Promo["Winterborn"]			= git('PROMOTION_WINTERBORN')
		Promo["Wintered"]			= git('PROMOTION_WINTERED')
		Promo["Unreliable"]			= git('PROMOTION_UNRELIABLE')
		Promo["Vampire"]			= git('PROMOTION_VAMPIRE')
		Promo["Rampage"]			= git('PROMOTION_RAMPAGE')
		Promo["Poisoned Blade"]		= git('PROMOTION_POISONED_BLADE')
		Promo["Dexterous"]			= git('PROMOTION_DEXTEROUS')
		Promo["Sinister"]			= git('PROMOTION_SINISTER')
		Promo["Mutated"]			= git('PROMOTION_MUTATED')
		Promo["Diseased"]			= git('PROMOTION_DISEASED')
		Promo["Aspect Capria"]			= git('PROMOTION_ASPECT_OF_WAR_CAPRIA')
		Promo["Aspect Mahon"]			= git('PROMOTION_ASPECT_OF_WAR_MAHON')
		Promo["Aspect Magnadine"]			= git('PROMOTION_ASPECT_OF_WAR_MAGNADINE')
		Promo["Aspect Orthus"]			= git('PROMOTION_ASPECT_OF_WAR_ORTHUS')
		Promo["Aspect Arak"]			= git('PROMOTION_ASPECT_OF_WAR_ARAK')
		Promo["Aspect Unknown1"]			= git('PROMOTION_ASPECT_OF_WAR_UNKNOWN_1')
		Promo["Aspect Unknown2"]			= git('PROMOTION_ASPECT_OF_WAR_UNKNOWN_2')
		self.Promotions["Effects"] 	= Promo

		""" Race """
		Race = {}
		Race["Angel"]               = git('PROMOTION_ANGEL')
		Race["Avatar"]              = git('PROMOTION_AVATAR')
		Race["Centaur"]             = git('PROMOTION_CENTAUR')
		Race["Demon"]               = git('PROMOTION_DEMON')
		Race["Dragon"]              = git('PROMOTION_DRAGON')
		Race["Dwarven"]             = git('PROMOTION_DWARF')
		Race["Elemental"]           = git('PROMOTION_ELEMENTAL')
		Race["Dark Elven"]          = git('PROMOTION_DARK_ELF')
		Race["Elven"]               = git('PROMOTION_ELF')
		Race["Fallen Angel"]        = git('PROMOTION_FALLEN_ANGEL')
		Race["Frostling"]           = git('PROMOTION_FROSTLING')
		Race["Giantkin"]            = git('PROMOTION_GIANTKIN')
		Race["Goblinoid"]           = git('PROMOTION_GOBLIN')
		Race["Golem"]               = git('PROMOTION_GOLEM')
		Race["Ice Demon"]           = git('PROMOTION_ICE_DEMON') #�Module Frozen
		Race["Illusion"]            = git('PROMOTION_ILLUSION')
		Race["Lizardman"]           = git('PROMOTION_LIZARDMAN')
		Race["Minotaur"]            = git('PROMOTION_MINOTAUR')
		Race["Musteval"]            = git('PROMOTION_MUSTEVAL')
		Race["Orcish"]              = git('PROMOTION_ORC')
		Race["Puppet"]              = git('PROMOTION_PUPPET')
		Race["Trollkin"]            = git('PROMOTION_TROLLKIN')
		Race["Undead"]              = git('PROMOTION_UNDEAD')
		self.Promotions["Race"]     = Race

		""" Equipment """
		Promo = {}
		Promo["Compelling Jewel"]	= git('PROMOTION_COMPELLING_JEWEL')
		Promo["Godslayer"]			= git('PROMOTION_GODSLAYER')
		Promo["Zarcazs Bow"]		= git('PROMOTION_ZARCAZS_BOW')
		self.Promotions["Equipment"]= Promo

	def getUnitAIDict(self): return self.UnitAI
	def initUnitAIDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		UnitAI = {}
		UnitAI["Counter"] 		= git('UNITAI_COUNTER')
		UnitAI["City Defense"]	= git('UNITAI_CITY_DEFENSE')
		UnitAI["Collateral"]	= git('UNITAI_COLLATERAL')
		self.UnitAI 			= UnitAI

	def getCorporationDict(self): return self.Corporations
	def initCorporationDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		Guild = {}
		Guild["Fishermans"] 	= git('CORPORATION_FISHERMANS_GUILD')
		Guild["Masquerade"] 	= git('CORPORATION_MASQUERADE')
		Guild["Fabricaforma"]	= git('CORPORATION_FABRICAFORMA')
		Guild["Farmers"]		= git('CORPORATION_FARMERS_GUILD')
		Guild["Stonefire"] 		= git('CORPORATION_STONEFIRE')
		self.Corporations 		= Guild

	def getBuildingClassDict(self): return self.BuildingClasses
	def initBuildingClassDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		BuildingClass = {}
		BuildingClass["Bear Den"] 			= git('BUILDINGCLASS_BEAR_DEN')
		BuildingClass["Boar Pen"] 			= git('BUILDINGCLASS_BOAR_PEN')
		BuildingClass["Gorilla Hut"]		= git('BUILDINGCLASS_GORILLA_HUT')
		BuildingClass["Griffin Weyr"]		= git('BUILDINGCLASS_GRIFFIN_WEYR')
		BuildingClass["Stag Copse"] 		= git('BUILDINGCLASS_STAG_COPSE')

		BuildingClass["Alchemy Lab"]		= git('BUILDINGCLASS_ALCHEMY_LAB')
		BuildingClass["Archery Range"]		= git('BUILDINGCLASS_ARCHERY_RANGE')
		BuildingClass["Barracks"]			= git('BUILDINGCLASS_BARRACKS')
		BuildingClass["Courthouse"]			= git('BUILDINGCLASS_COURTHOUSE')
		BuildingClass["Forge"]				= git('BUILDINGCLASS_FORGE')
		BuildingClass["Fletcher"]			= git('BUILDINGCLASS_FLETCHER')
		BuildingClass["Hunting Lodge"]		= git('BUILDINGCLASS_HUNTING_LODGE')
		BuildingClass["Library"]			= git('BUILDINGCLASS_LIBRARY')
		BuildingClass["Mage Guild"]			= git('BUILDINGCLASS_MAGE_GUILD')
		BuildingClass["Market"]				= git('BUILDINGCLASS_MARKET')
		BuildingClass["Training Yard"]		= git('BUILDINGCLASS_TRAINING_YARD')
		BuildingClass["Siege Workshop"]		= git('BUILDINGCLASS_SIEGE_WORKSHOP')
		BuildingClass["Stable"]				= git('BUILDINGCLASS_STABLE')
		BuildingClass["Elder Council"] 		= git('BUILDINGCLASS_ELDER_COUNCIL')
		BuildingClass["National Epic"]			= git('BUILDINGCLASS_NATIONAL_EPIC')
		BuildingClass["Heroic Epic"]			= git('BUILDINGCLASS_HEROIC_EPIC')
		BuildingClass["Shrine of Champion"] 	= git('BUILDINGCLASS_SHRINE_OF_THE_CHAMPION')

		BuildingClass["Tower of Alteration"]	= git('BUILDINGCLASS_TOWER_OF_ALTERATION')
		BuildingClass["Tower of Divination"]	= git('BUILDINGCLASS_TOWER_OF_DIVINATION')
		BuildingClass["Tower of Elements"]		= git('BUILDINGCLASS_TOWER_OF_THE_ELEMENTS')
		BuildingClass["Tower of Necromancy"]	= git('BUILDINGCLASS_TOWER_OF_NECROMANCY')
		BuildingClass["Tower of Mastery"]		= git('BUILDINGCLASS_TOWER_OF_MASTERY')

		self.BuildingClasses	= BuildingClass

	def getBuildingDict(self): return self.Buildings
	def initBuildingDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		Building = {}
		# Civilization Amurites
		Building["Water Mana"]             = git('BUILDING_MANA_WATER')
		Building["Death Mana"]             = git('BUILDING_MANA_DEATH')
		# Civilization Archos
		Building["Nest Addon1"]             = git('BUILDING_ARCHOS_NEST_ADDON1')
		Building["Nest Addon2"]             = git('BUILDING_ARCHOS_NEST_ADDON2')
		Building["Nest Addon3"]             = git('BUILDING_ARCHOS_NEST_ADDON3')
		Building["Nest Addon4"]             = git('BUILDING_ARCHOS_NEST_ADDON4')
		# Civilization Hippus
		Building["Nightmare"]           	= git('BUILDING_NIGHTMARE')
		# Civilization Khazad
		Building["Dwarven Smithy"]          = git('BUILDING_DWARVEN_SMITHY')
		# Civilization Luchuirp
		Building["Sculptors Studio"]        = git('BUILDING_SCULPTORS_STUDIO')
		Building["Blasting Workshop"]       = git('BUILDING_BLASTING_WORKSHOP')
		Building["Pallens Engine"]          = git('BUILDING_PALLENS_ENGINE')
		Building["Adularia Chamber"]        = git('BUILDING_ADULARIA_CHAMBER')
		Building["Machinists Shop"]         = git('BUILDING_MACHINISTS_SHOP')
		# Civilization Malakim
		Building["Temple Mirror"]           = git('BUILDING_MALAKIM_TEMPLE_MIRROR')
		# Civilization Mekara
		Building["Shaper's Laboratory"]     = git('BUILDING_SHAPER_LAB')
		Building["Shaper Cabal"]            = git('BUILDING_SHAPER_CABAL')
		# Temples
		Building["Temple of the Veil"]      = git('BUILDING_TEMPLE_OF_THE_VEIL')
		Building["Temple of the Order"]     = git('BUILDING_TEMPLE_OF_THE_ORDER')
		Building["Temple of the Empyrean"]  = git('BUILDING_TEMPLE_OF_THE_EMPYREAN')
		Building["Temple of the Leaves"]    = git('BUILDING_TEMPLE_OF_LEAVES')
		Building["Temple of the Kilmorph"]  = git('BUILDING_TEMPLE_OF_KILMORPH')
		Building["Temple of the Hand"]      = git('BUILDING_TEMPLE_OF_THE_HAND')
		Building["Temple of the Overlords"] = git('BUILDING_TEMPLE_OF_THE_OVERLORDS')
		# Tower of Mastery
		Building["Tower of Alteration"]     = git('BUILDING_TOWER_OF_ALTERATION')
		Building["Tower of Necromancy"]     = git('BUILDING_TOWER_OF_NECROMANCY')
		Building["Tower of Elements"]       = git('BUILDING_TOWER_OF_THE_ELEMENTS')
		Building["Tower of Divination"]     = git('BUILDING_TOWER_OF_DIVINATION')
		# Guilds
		Building["Fisher Guild"]            = git('BUILDING_GUILD_FISHER')
		Building["Masquerade Troupe Camp"]   = git('BUILDING_GUILD_MASQUERADE_TROUPE_CAMP')
		Building["Fabricaforma"]            = git('BUILDING_GUILD_FABRICAFORMA')
		Building["Farmers Guild"]           = git('BUILDING_GUILD_FARMERS_GUILD')
		Building["Stonefire Guild"]         = git('BUILDING_GUILD_STONEFIRE')
		# Altars
		Building["Altar of Luonnotar"]      = git('BUILDING_ALTAR_OF_THE_LUONNOTAR')
		Building["Altar - Anointed"]        = git('BUILDING_ALTAR_OF_THE_LUONNOTAR_ANOINTED')
		Building["Altar - Blessed"]         = git('BUILDING_ALTAR_OF_THE_LUONNOTAR_BLESSED')
		Building["Altar - Consecrated"]     = git('BUILDING_ALTAR_OF_THE_LUONNOTAR_CONSECRATED')
		Building["Altar - Divine"]          = git('BUILDING_ALTAR_OF_THE_LUONNOTAR_DIVINE')
		Building["Altar - Exalted"]         = git('BUILDING_ALTAR_OF_THE_LUONNOTAR_EXALTED')
		Building["Altar - Final"]           = git('BUILDING_ALTAR_OF_THE_LUONNOTAR_FINAL')
		# World Wonders
		Building["Mines of Galdur"]         = git('BUILDING_MINES_OF_GALDUR')
		Building["Tablets of Bambur"]       = git('BUILDING_TABLETS_OF_BAMBUR')
		Building["Caminus Aureus"]          = git('BUILDING_CAMINUS_AUREUS')
		Building["Guild of Hammers"]        = git('BUILDING_GUILD_OF_HAMMERS')
		Building["Soul Forge"]              = git('BUILDING_SOUL_FORGE')
		Building["Mokkas Cauldron"]         = git('BUILDING_MOKKAS_CAULDRON')
		Building["Eyes and Ears"]           = git('BUILDING_EYES_AND_EARS_NETWORK')
		Building["Thousand Slums"]          = git('BUILDING_CITY_OF_A_THOUSAND_SLUMS')
		Building["Prophechy of Ragnarok"]   = git('BUILDING_PROPHECY_OF_RAGNAROK')
		# Palaces
		Building["Amurite Palace"]          = git('BUILDING_PALACE_AMURITES')
		Building["Doviello Palace"]         = git('BUILDING_PALACE_DOVIELLO')
		Building["Grigori Palace"]          = git('BUILDING_PALACE_GRIGORI')
		Building["Mechanos Palace"]         = git('BUILDING_PALACE_MECHANOS')
		Building["Mekaran Palace"]          = git('BUILDING_PALACE_MEKARA')
		Building["Scions Palace"]           = git('BUILDING_PALACE_SCIONS')
		
		# TODO sort
		Building["Dark Weald"]		= git('BUILDING_DARK_WEALD')
		Building["Dungeon"]			= git('BUILDING_DUNGEON')

		Building["Obbuilding1"]		= git('BUILDING_OBBUILDING1')
		Building["Obbuilding2"]		= git('BUILDING_OBBUILDING2')
		Building["Obbuilding3"]		= git('BUILDING_OBBUILDING3')
		Building["Obbuilding4"]		= git('BUILDING_OBBUILDING4')
		Building["Obbuilding5"]		= git('BUILDING_OBBUILDING5')
		Building["Obbuilding6"]		= git('BUILDING_OBBUILDING6')
		Building["Obbuilding7"]		= git('BUILDING_OBBUILDING7')

		Building["Heroic Epic"]		= git('BUILDING_HEROIC_EPIC')
		Building["National Epic"]		= git('BUILDING_NATIONAL_EPIC')
		Building["Academy"]				= git('BUILDING_ACADEMY')
		Building["Camel Stable"]		= git('BUILDING_STABLE_CAMEL')
		Building["Stable"]				= git('BUILDING_STABLE')
		Building["Hunting Lodge"]		= git('BUILDING_HUNTING_LODGE')
		Building["Training Yard"]		= git('BUILDING_TRAINING_YARD')
		Building["Siege Workshop"]		= git('BUILDING_SIEGE_WORKSHOP')

		Building["Vacant Mausoleum"]	= git('BUILDING_VACANT_MAUSOLEUM')
		Building["Monument to Avarice"]	= git('BUILDING_MONUMENT_TO_AVARICE')
		Building["Smugglers Port"]		= git('BUILDING_SMUGGLERS_PORT')
		Building["Command Post"]		= git('BUILDING_COMMAND_POST')
		Building["Form of the Titan"]	= git('BUILDING_FORM_OF_THE_TITAN')

		Building["Vault1"] 				= git('BUILDING_DWARVEN_VAULT_EMPTY')
		Building["Vault2"] 				= git('BUILDING_DWARVEN_VAULT_LOW')
		Building["Vault3"] 				= git('BUILDING_DWARVEN_VAULT')
		Building["Vault4"] 				= git('BUILDING_DWARVEN_VAULT_STOCKED')
		Building["Vault5"] 				= git('BUILDING_DWARVEN_VAULT_ABUNDANT')
		Building["Vault6"] 				= git('BUILDING_DWARVEN_VAULT_FULL')
		Building["Vault7"] 				= git('BUILDING_DWARVEN_VAULT_OVERFLOWING')

		Building["Shrine of Sirona"]	= git('BUILDING_SHRINE_OF_SIRONA')

		Building["Unhealthy Discontent I"]= git('BUILDING_UNHEALTHY_DISCONTENT1')
		Building["Unhealthy Discontent II"]= git('BUILDING_UNHEALTHY_DISCONTENT2')

		Building["Necropolis"]			= git('BUILDING_NECROPOLIS')
		Building["Necro Bonus1"]		= git('BUILDING_NECRO_BONUS_BUILDING1')
		Building["Necro Bonus2"]		= git('BUILDING_NECRO_BONUS_BUILDING2')
		Building["Necro Bonus3"]		= git('BUILDING_NECRO_BONUS_BUILDING3')
		Building["Water Keep"]              = git('BUILDING_KEEP_WATER')
		Building["Death Keep"]              = git('BUILDING_KEEP_DEATH')


		Building["Flesh Studio"]		= git('BUILDING_FLESH_STUDIO')
		Building["Cathedral of Rebirth"]= git('BUILDING_CATHEDRAL_OF_REBIRTH')

		Building["Bear Den"]			= git('BUILDING_BEAR_DEN')
		Building["Mammoth Den"]			= git('BUILDING_MAMMOTH_DEN')
		Building["Lion Den"]			= git('BUILDING_LION_DEN')
		Building["Stag Corpse"]			= git('BUILDING_STAG_COPSE')
		Building["Griffin Weyr"]		= git('BUILDING_GRIFFIN_WEYR')
		Building["Bear Den"]			= git('BUILDING_BEAR_DEN')
		Building["Jotnar Staedding"]	= git('BUILDING_JOT_STAEDDING')
		Building["House of Ancestors"]	= git('BUILDING_JOT_HOUSE_OF_THE_ANCESTORS')
		Building["Planar Gate"] 		= git('BUILDING_PLANAR_GATE')
		Building["Gambling House"] 		= git('BUILDING_GAMBLING_HOUSE')
		Building["Mage Guild"]			= git('BUILDING_MAGE_GUILD')
		Building["Carnival"]			= git('BUILDING_CARNIVAL')
		Building["Grove"] 				= git('BUILDING_GROVE')
		Building["Public Baths"]		= git('BUILDING_PUBLIC_BATHS')
		Building["Obsidian Gate"]		= git('BUILDING_OBSIDIAN_GATE')



		Building["Meditation Hall"] 	= git('BUILDING_MEDITATION_HALL')
		Building["Infernal Grimoire"] 	= git('BUILDING_INFERNAL_GRIMOIRE')
		Building["Pact of the Nilhorn"]	= git('BUILDING_PACT_OF_THE_NILHORN')
		Building["Mercurian Gate"]		= git('BUILDING_MERCURIAN_GATE')
		Building["Pax Diabolis"] 		= git('BUILDING_PAX_DIABOLIS')
		Building["Demonic Citizens"]	= git('BUILDING_DEMONIC_CITIZENS')
		Building["Elder Council"]		= git('BUILDING_ELDER_COUNCIL')
		Building["Barracks"]			= git('BUILDING_BARRACKS')
		Building["Forge"]				= git('BUILDING_FORGE')
		Building["Austrin Settlement"]	= git('BUILDING_AUSTRIN_SETTLEMENT')
		Building["The Great Library"]	= git('BUILDING_GREAT_LIBRARY')

		Building["Courthouse"]			= git('BUILDING_COURTHOUSE')
		Building["Market"]				= git('BUILDING_MARKET')
		Building["Monument"]			= git('BUILDING_MONUMENT')
		Building["Moneychanger"]		= git('BUILDING_MONEYCHANGER')
		Building["Theatre"]				= git('BUILDING_THEATRE')
		Building["Tax Office"]			= git('BUILDING_TAX_OFFICE')
		Building["Breeding Pit"]		= git('BUILDING_BREEDING_PIT')
		Building["Reliquary"]			= git('BUILDING_RELIQUARY')
		Building["Inn"]					= git('BUILDING_INN')
		Building["Shrouded Woods"]		= git('BUILDING_SHROUDED_WOODS')


		Building["Kahdi Vault Gate"]    = git('BUILDING_KAHDI_VAULT_GATE')

		Building["Jotnar Monument"]		= git('BUILDING_JOT_MONUMENT')
		Building["Catacomb Libralus"]	= git('BUILDING_CATACOMB_LIBRALUS')
		Building["Forbidden Palace"]	= git('BUILDING_FORBIDDEN_PALACE')

		Building["Temple of the Gift"]	= git('BUILDING_TEMPLE_OF_THE_GIFT')
		Building["Emperors Mark"] 		= git('BUILDING_EMPERORS_MARK')
		Building["Grand Menagerie"]		= git('BUILDING_GRAND_MENAGERIE')
		Building["Swamp of Souls"]		= git('BUILDING_SWAMP_OF_SOULS')
		Building["Asylum"]				= git('BUILDING_ASYLUM')
		Building["Brewery"]				= git('BUILDING_BREWERY')
		Building["Demons Altar"]		= git('BUILDING_DEMONS_ALTAR')
		Building["Asylum"]				= git('BUILDING_ASYLUM')
		Building["School of Govannon"]	= git('BUILDING_SCHOOL_OF_GOVANNON')
		Building["Wizards Hall"]		= git('BUILDING_WIZARDS_HALL')
		Building["Cave of Ancestors"]	= git('BUILDING_CAVE_OF_ANCESTORS')
		Building["Chancel of Guardians"]= git('BUILDING_CHANCEL_OF_GUARDIANS')
		Building["Frozen Souls"]		= git('BUILDING_FROZEN_SOULS')

		Building["Hall of the Covenant"]= git('BUILDING_HALL_OF_THE_COVENANT')
		Building["Imperial Cenotaph"]	= git('BUILDING_IMPERIAL_CENOTAPH')
		Building["Shrine to Kylorin"]	= git('BUILDING_SHRINE_TO_KYLORIN')

		Building["Lighthouse"]			= git('BUILDING_LIGHTHOUSE')
		Building["Harbor Lanun"]		= git('BUILDING_HARBOR_LANUN')
		Building["Harbor"]				= git('BUILDING_HARBOR')
		Building["Library"]				= git('BUILDING_LIBRARY')
		Building["Alchemy Lab"]			= git('BUILDING_ALCHEMY_LAB')
		Building["Granary"]				= git('BUILDING_GRANARY')
		Building["Smokehouse"]			= git('BUILDING_SMOKEHOUSE')

		Building["Herbalist"]			= git('BUILDING_HERBALIST')
		Building["Aqueduct"]			= git('BUILDING_AQUEDUCT')
		Building["Infirmary"]			= git('BUILDING_INFIRMARY')
		Building["Well"]				= git('BUILDING_WELL')
		Building["Sewer"]				= git('BUILDING_SEWERS')

		Building["Archery Range"]		= git('BUILDING_ARCHERY_RANGE')

		Building["Riot and Sedition"]	= git('BUILDING_RIOT_AND_SEDITION')
		Building["Poison Words"]		= git('BUILDING_POISON_WORDS')
		Building["Hall of Mirrors"]		= git('BUILDING_HALL_OF_MIRRORS')

		Building["Museum"]				= git('BUILDING_MUSEUM')
		Building["Tavern"]				= git('BUILDING_TAVERN_GRIGORI')
		Building["Adventurers Guild"]	= git('BUILDING_ADVENTURERS_GUILD')
		Building["Grigori Temple"]		= git('BUILDING_GRIGORI_TEMPLE')
		Building["Memorial Refugee"]	= git('BUILDING_MEMORIAL_REFUGEE')
		Building["Dwelling of Refuge"]	= git('BUILDING_DWELLING_OF_REFUGE')
		Building["Forum"]				= git('BUILDING_FORUM')
		Building["Crime Bounty Minor"]			= git('BUILDING_CRIME_BOUNTY_MINOR')
		Building["Crime Bounty Major"]		        = git('BUILDING_CRIME_BOUNTY_MAJOR')
		Building["Crime Bounty Grand"]			= git('BUILDING_CRIME_BOUNTY_GRAND')

		Building["Warrens"]				= git('BUILDING_WARRENS')
		Building["Manor"]				= git('BUILDING_GOVERNORS_MANOR')
		Building["Fletcher"]			= git('BUILDING_FLETCHER')

		Building["Dragons Hoard"]		= git('BUILDING_THE_DRAGONS_HOARD')


		Building["Tower of Complacency"]	= git('BUILDING_TOWER_OF_COMPLACENCY')

		Building["Shrine of the Champion"]	= git('BUILDING_SHRINE_OF_THE_CHAMPION')
		self.Buildings = Building

	def getProcessesDict(self):
		return self.Processes

	def initProcessesDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		Process = {}
		Process["Caste System"]			= git('PROCESS_CASTE_SYSTEM')
		Process["Wealth"]				= git('PROCESS_WEALTH')
		Process["Culture"]				= git('PROCESS_CULTURE')
		Process["Culture Improved"]		= git('PROCESS_CULTURE_IMPROVED')
		Process["Research"]				= git('PROCESS_RESEARCH')
		Process["Research Improved"]	= git('PROCESS_RESEARCH_IMPROVED')

		self.Processes = Process

	def getProjectDict(self):
		return self.Projects

	def initProjectDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		Project = {}
		Project["Liberation"]               = git('PROJECT_LIBERATION')
		Project["Appease Divinity"]         = git('PROJECT_APPEASE_DIVINITY')
		Project["Bane Divine"]              = git('PROJECT_BANE_DIVINE')
		Project["Birthright Regained"]      = git('PROJECT_BIRTHRIGHT_REGAINED')
		Project["Blood of the Phoenix"]     = git('PROJECT_BLOOD_OF_THE_PHOENIX')
		Project["Chosen of Esus"]           = git('PROJECT_CHOSEN_OF_ESUS')
		Project["Curse the Lands"]          = git('PROJECT_BLIGHT_THE_CROPS')
		Project["Dowsing"]                  = git('PROJECT_DOWSING')
		Project["Elegy of the Sheaim"]      = git('PROJECT_ELEGY_OF_THE_SHEAIM')
		Project["Genesis"]                  = git('PROJECT_GENESIS')
		Project["Glory Everlasting"]        = git('PROJECT_GLORY_EVERLASTING')
		Project["Hallowing of the Elohim"]  = git('PROJECT_HALLOWING_OF_THE_ELOHIM')
		Project["Light of Lugus"]           = git('PROJECT_LIGHT_OF_LUGUS')
		Project["Mana Surge"]               = git('PROJECT_MANA_SURGE')
		Project["Nature's Revolt"]          = git('PROJECT_NATURES_REVOLT')
		Project["Purge the Unfaithful"]     = git('PROJECT_PURGE_THE_UNFAITHFUL')
		Project["Rites of Oghma"]           = git('PROJECT_RITES_OF_OGHMA')
		Project["Samhain"]                  = git('PROJECT_SAMHAIN')
		Project["The White Hand"]           = git('PROJECT_THE_WHITE_HAND')
		Project["The Deepening"]            = git('PROJECT_THE_DEEPENING')
		Project["Stir From Slumber"]        = git('PROJECT_STIR_FROM_SLUMBER')
		Project["The Draw"]                 = git('PROJECT_THE_DRAW')
		Project["Ascension"]                = git('PROJECT_ASCENSION')
		Project["Pax Diabolis"]             = git('PROJECT_PAX_DIABOLIS')
		Project["Prepare Expedition"]       = git('PROJECT_PREPARE_EXPEDITION')

		self.Projects = Project

	def getGoodyDict(self):	return self.Goodies

	def initGoodyDict(self):
		gc 	= CyGlobalContext()
		git = gc.getInfoTypeForString
		Goody = {}
		Goody["Experience"] 	= git('GOODY_EXPLORE_LAIR_EXPERIENCE')
		Goody["Supplies"] 		= git('GOODY_EXPLORE_LAIR_SUPPLIES')

		Goody["Jade Torc"] 		= git('GOODY_EXPLORE_LAIR_ITEM_JADE_TORC')
		Goody["Rod of Winds"]	= git('GOODY_EXPLORE_LAIR_ITEM_ROD_OF_WINDS')
		Goody["Timor Mask"]		= git('GOODY_EXPLORE_LAIR_ITEM_TIMOR_MASK')

		Goody["Sea Serpent"]	= git('GOODY_EXPLORE_LAIR_SPAWN_SEA_SERPENT')
		Goody["Drown"] 			= git('GOODY_EXPLORE_LAIR_SPAWN_DROWN')
		Goody["Spider"]			= git('GOODY_EXPLORE_LAIR_SPAWN_SPIDER')
		Goody["Skeleton"] 		= git('GOODY_EXPLORE_LAIR_SPAWN_SKELETON')
		Goody["Lizardman"] 		= git('GOODY_EXPLORE_LAIR_SPAWN_LIZARDMAN')

		Goody["Crazed"] 		= git('GOODY_MARNOK_CRAZED')
		Goody["Diseased"] 		= git('GOODY_MARNOK_DISEASED')
		Goody["Enraged"] 		= git('GOODY_MARNOK_ENRAGED')
		Goody["Mutated"] 		= git('GOODY_MARNOK_MUTATED')
		Goody["Plagued"] 		= git('GOODY_MARNOK_PLAGUED')
		Goody["Poisoned"] 		= git('GOODY_MARNOK_POISONED')
		Goody["Possessed"] 		= git('GOODY_MARNOK_POSSESSED')
		Goody["Rusted"] 		= git('GOODY_MARNOK_RUSTED')
		Goody["Withered"] 		= git('GOODY_MARNOK_WITHERED')
		Goody["Hill Giant"] 	= git('GOODY_MARNOK_HILLGIANT')
		Goody["Lich"] 			= git('GOODY_MARNOK_LICH')
		Goody["Ogre"] 			= git('GOODY_MARNOK_OGRE')
		Goody["Treant"]			= git('GOODY_MARNOK_TREANT')
		Goody["Zombie"]			= git('GOODY_MARNOK_ZOMBIE')

		Goody["Cyklop"]			= git('GOODY_CYKLOP')
		Goody["Minotaur"] 		= git('GOODY_MINOTAUR')
		Goody["Troll"] 			= git('GOODY_TROLL')

		Goody["Prisoner Adventurer"]= git('GOODY_EXPLORE_LAIR_PRISONER_ADVENTURER')
		Goody["Prisoner Angel"]		= git('GOODY_EXPLORE_LAIR_PRISONER_ANGEL')
		Goody["Prisoner Artist"]	= git('GOODY_EXPLORE_LAIR_PRISONER_ARTIST')
		Goody["Prisoner Assassin"]	= git('GOODY_EXPLORE_LAIR_PRISONER_ASSASSIN')
		Goody["Prisoner Champion"]	= git('GOODY_EXPLORE_LAIR_PRISONER_CHAMPION')
		Goody["Prisoner Commander"]	= git('GOODY_EXPLORE_LAIR_PRISONER_COMMANDER')
		Goody["Prisoner Engineer"]	= git('GOODY_EXPLORE_LAIR_PRISONER_ENGINEER')
		Goody["Prisoner Mage"]		= git('GOODY_EXPLORE_LAIR_PRISONER_MAGE')
		Goody["Prisoner Merchant"]	= git('GOODY_EXPLORE_LAIR_PRISONER_MERCHANT')
		Goody["Prisoner Monk"]		= git('GOODY_EXPLORE_LAIR_PRISONER_MONK')
		Goody["Prisoner Prophet"]	= git('GOODY_EXPLORE_LAIR_PRISONER_PROPHET')
		Goody["Prisoner Serpent"]	= git('GOODY_EXPLORE_LAIR_PRISONER_SEA_SERPENT')
		Goody["Prisoner Scientist"]	= git('GOODY_EXPLORE_LAIR_PRISONER_SCIENTIST')

		Goody["Grave - Spectre"]	= git('GOODY_GRAVE_SPECTRE')
		Goody["Grave - Tech"]		= git('GOODY_GRAVE_TECH')

		Goody["Healing Salve"]		= git('GOODY_EXPLORE_LAIR_ITEM_HEALING_SALVE')
		Goody["Spirit Guide"] 		= git('GOODY_MARNOK_SPIRIT_GUIDE')
		Goody["Shield of Faith"]	= git('GOODY_MARNOK_SHIELD_OF_FAITH')
		Goody["Enchanted Blade"]	= git('GOODY_MARNOK_ENCHANTED_BLADE')
		Goody["Spellstaff"] 		= git('GOODY_MARNOK_SPELLSTAFF')
		Goody["Poisoned Blade"]		= git('GOODY_MARNOK_POISONED_BLADE')
		Goody["Flaming Arrows"]		= git('GOODY_MARNOK_FLAMING_ARROWS')

		Goody["Climbing Kit - Recon"] 	= git('GOODY_MARNOK_CLIMBING_KIT_RECON')
		Goody["Desert Gear - Recon"] 	= git('GOODY_MARNOK_DESERT_GEAR_RECON')
		Goody["Snow Gear - Recon"] 		= git('GOODY_MARNOK_SNOW_GEAR_RECON')
		Goody["Woods Gear - Recon"] 	= git('GOODY_MARNOK_WOODS_GEAR_RECON')
		Goody["Fine Kit - Recon"] 		= git('GOODY_MARNOK_FINE_KIT_RECON')
		Goody["Mantraps - Recon"] 		= git('GOODY_MARNOK_MANTRAPS_RECON')

		Goody["Potion of Restoration"]	= git('GOODY_EXPLORE_LAIR_ITEM_POTION_OF_RESTORATION')
		Goody["Potion of Invisibility"] = git('GOODY_EXPLORE_LAIR_ITEM_POTION_OF_INVISIBILITY')

		self.Goodies = Goody

	def getDamageTypesDict(self):
		return self.DamageTypes

	def initDamageTypesDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Damage = {}
		Damage["Physical"]	= git('DAMAGE_PHYSICAL')
		Damage["Poison"] 	= git('DAMAGE_POISON')
		self.DamageTypes = Damage

	def getImprovementDict(self):
		return self.Improvements

	def initImprovementDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Improvement = {}
		Improvement["Cottage (I)"]      = git('IMPROVEMENT_COTTAGE')
		Improvement["Hamlet (II)"]      = git('IMPROVEMENT_HAMLET')
		Improvement["Village (III)"]    = git('IMPROVEMENT_VILLAGE')
		Improvement["Town (IV)"]        = git('IMPROVEMENT_TOWN')
		
		Improvement["Ash Field"] 		= git('IMPROVEMENT_ASH_FIELD')
		Improvement["Cage"] 			= git('IMPROVEMENT_CAGE')
		Improvement["Camp"] 			= git('IMPROVEMENT_CAMP')
		Improvement["Castle"] 			= git('IMPROVEMENT_CASTLE')
		Improvement["Citadel"] 			= git('IMPROVEMENT_CITADEL')
		Improvement["City Ruins"]		= git('IMPROVEMENT_CITY_RUINS')
		Improvement["Farm"] 			= git('IMPROVEMENT_FARM')
		Improvement["Fishing Boats"] 	= git('IMPROVEMENT_FISHING_BOATS')
		Improvement["Fort"] 			= git('IMPROVEMENT_FORT')
		Improvement["Hellfire"] 		= git('IMPROVEMENT_HELLFIRE')
		Improvement["Jungle Altar"] 	= git('IMPROVEMENT_JUNGLE_ALTAR')
		Improvement["Lumbermill"]		= git('IMPROVEMENT_LUMBERMILL')
		Improvement["Mine"] 			= git('IMPROVEMENT_MINE')
		Improvement["Necrototem"] 		= git('IMPROVEMENT_NECROTOTEM')
		Improvement["HellGate"] 		= git('IMPROVEMENT_AERON_VAULTGATE')
		Improvement["Pasture"]			= git('IMPROVEMENT_PASTURE')
		Improvement["Penguins"]			= git('IMPROVEMENT_PENGUINS')
		Improvement["Plantation"]		= git('IMPROVEMENT_PLANTATION')
		Improvement["Portal"]			= git('IMPROVEMENT_PORTAL')
		Improvement["Quarry"] 			= git('IMPROVEMENT_QUARRY')
		Improvement["Smoke"] 			= git('IMPROVEMENT_SMOKE')
		Improvement["Snake Pillar"] 	= git('IMPROVEMENT_SNAKE_PILLAR')
		Improvement["Swamp"] 			= git('IMPROVEMENT_SWAMP')
		Improvement["Tower"] 			= git('IMPROVEMENT_TOWER')
		Improvement["Warning Post"] 	= git('IMPROVEMENT_WARNING_POST')
		Improvement["Watermill"] 		= git('IMPROVEMENT_WATERMILL')
		Improvement["Windmill"] 		= git('IMPROVEMENT_WINDMILL')
		Improvement["Winery"] 			= git('IMPROVEMENT_WINERY')
		Improvement["Workshop"] 		= git('IMPROVEMENT_WORKSHOP')
		
		Improvement["Road"]	 			= git('ROUTE_ROAD')
		Improvement["Trail"]	 		= git('ROUTE_TRAIL')

		self.Improvements = Improvement

	def getLairDict(self):
		return self.Lairs

	def initLairDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Lair = {}
		Lair["Barrow"] 				= git('IMPROVEMENT_BARROW')
		Lair["Bear Den"] 			= git('IMPROVEMENT_BEAR_DEN')
		Lair["Blighted Forest"]		= git('IMPROVEMENT_BLIGHTED_FOREST')
		Lair["Cave Bear Den"] 		= git('IMPROVEMENT_CAVE_BEAR_DEN')
		Lair["Dungeon"] 			= git('IMPROVEMENT_DUNGEON')
		Lair["Goblin Camp"] 		= git('IMPROVEMENT_GOBLIN_CAMP')
		Lair["Goblin Fort (Cleared Out)"] = git('IMPROVEMENT_GOBLIN_FORT_CLEARED')
		Lair["Goody Hut"] 			= git('IMPROVEMENT_GOODY_HUT')
		Lair["Graveyard"] 			= git('IMPROVEMENT_GRAVEYARD')
		Lair["Lion Den"] 			= git('IMPROVEMENT_LION_DEN')
		Lair["Sabretooth Den"] 		= git('IMPROVEMENT_SABRETOOTH_DEN')
		Lair["Shipwreck"] 			= git('IMPROVEMENT_SHIP_WRECK')
		Lair["Steading"] 			= git('IMPROVEMENT_MARNOK_HILLGIANT_STEADING')
		Lair["Griffin Weyr"] 		= git('IMPROVEMENT_GRIFFIN_WEYR')
		Lair["Hippogriffin Weyr"] 	= git('IMPROVEMENT_HIPPOGRIFF_WEYR')
		Lair["Ruins"] 				= git('IMPROVEMENT_RUINS')
		Lair["Spider Den"] 			= git('IMPROVEMENT_DEN_SPIDER')
		Lair["Wolf Den"] 			= git('IMPROVEMENT_DEN_WOLF')
		self.Lairs = Lair

	def getCivImprovementDict(self):
		return self.CivImprovements

	def initCivImprovementDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		CivImprovement = {}
		CivImprovement["Bedouin Camp"] 			= git('IMPROVEMENT_BEDOUIN_CAMP')
		CivImprovement["Bedouin Gathering"] 	= git('IMPROVEMENT_BEDOUIN_GATHERING')
		CivImprovement["Bedouin Sit"] 			= git('IMPROVEMENT_BEDOUIN_SIT')
		CivImprovement["Bedouin Village"] 		= git('IMPROVEMENT_BEDOUIN_VILLAGE')
		CivImprovement["Citadel of Light"] 		= git('IMPROVEMENT_CITADEL_OF_LIGHT')
		self.CivImprovements["Malakim"] = CivImprovement

		CivImprovement = {}
		CivImprovement["Crypt"] 				= git('IMPROVEMENT_DTESH_CRYPT')
		CivImprovement["Corrupted Pasture"] 	= git('IMPROVEMENT_PASTURE_CORRUPTED')
		CivImprovement["Pyre"] 					= git('IMPROVEMENT_DTESH_PYRE')
		CivImprovement["Aquatic Pyre"]			= git('IMPROVEMENT_DTESH_PYRE_AQUATIC')
		CivImprovement["Catacombs"] 			= git('IMPROVEMENT_DTESH_CATACOMBS')
		CivImprovement["Mausoleum - Lesser"] 	= git('IMPROVEMENT_DTESH_MAUSOLEUM_LESSER')
		CivImprovement["Mausoleum"] 			= git('IMPROVEMENT_DTESH_MAUSOLEUM')
		CivImprovement["Mausoleum - Greater"]	= git('IMPROVEMENT_DTESH_MAUSOLEUM_GREATER')
		self.CivImprovements["D'Tesh"] 			= CivImprovement

		CivImprovement = {}
		CivImprovement["Mine 1"]                = git('IMPROVEMENT_DWARVEN_MINE')
		CivImprovement["Mine 2"]                = git('IMPROVEMENT_DWARVEN_SETTLEMENT')
		CivImprovement["Mine 3"]                = git('IMPROVEMENT_DWARVEN_HALL')
		CivImprovement["Mine 4"]                = git('IMPROVEMENT_DWARVEN_FORTRESS')
		self.CivImprovements["Dwarven"] = CivImprovement

		CivImprovement = {}
		CivImprovement["Enclave"] 			= git('IMPROVEMENT_ENCLAVE')
		self.CivImprovements["Kuriotates"] 	= CivImprovement

		CivImprovement = {}
		CivImprovement["Cove"] 				= git('IMPROVEMENT_PIRATE_COVE')
		CivImprovement["Harbor"] 			= git('IMPROVEMENT_PIRATE_HARBOR')
		CivImprovement["Port"] 				= git('IMPROVEMENT_PIRATE_PORT')
		self.CivImprovements["Lanun"] 		= CivImprovement

		CivImprovement = {}
		CivImprovement["Yaranga"] 			= git('IMPROVEMENT_YARANGA')
		self.CivImprovements["Doviello"] 	= CivImprovement

	def getUniqueImprovementDict(self):
		return self.UniqueImprovements

	def initUniqueImprovementDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		UniqueImprovement = {}
		UniqueImprovement["Aifon Isle"] 					= git('IMPROVEMENT_AIFON_ISLE')
		UniqueImprovement["Bair of Lacuna"]			    	= git('IMPROVEMENT_BAIR_OF_LACUNA')
		UniqueImprovement["Bradeline's Well"] 				= git('IMPROVEMENT_BRADELINES_WELL')
		UniqueImprovement["Bradeline's Well (Purified)"] 	= git('IMPROVEMENT_BRADELINES_WELL_PURIFIED')
		UniqueImprovement["Broken Sepulcher"] 				= git('IMPROVEMENT_BROKEN_SEPULCHER')
		UniqueImprovement["Dragon Bones"] 					= git('IMPROVEMENT_DRAGON_BONES')
		UniqueImprovement["Foxford"] 						= git('IMPROVEMENT_FOXFORD')
		UniqueImprovement["Guardian"] 						= git('IMPROVEMENT_GUARDIAN')
		UniqueImprovement["Letum Frigus"] 					= git('IMPROVEMENT_LETUM_FRIGUS')
		UniqueImprovement["Maelstrom"] 						= git('IMPROVEMENT_MAELSTROM')
		UniqueImprovement["Mirror of Heaven"] 				= git('IMPROVEMENT_MIRROR_OF_HEAVEN')
		UniqueImprovement["Monster Skeleton"] 				= git('IMPROVEMENT_MONSTER_SKELETON')
		UniqueImprovement["Mount Kalshekk"] 				= git('IMPROVEMENT_MOUNT_KALSHEKK')
		UniqueImprovement["Odio's Prison"] 					= git('IMPROVEMENT_ODIOS_PRISON')
		UniqueImprovement["Pool of Tears"] 					= git('IMPROVEMENT_POOL_OF_TEARS')
		UniqueImprovement["Pyre of the Seraphic"] 			= git('IMPROVEMENT_PYRE_OF_THE_SERAPHIC')
		UniqueImprovement["Remnants of Patria"]				= git('IMPROVEMENT_REMNANTS_OF_PATRIA')
		UniqueImprovement["Ring of Carcer"] 				= git('IMPROVEMENT_RING_OF_CARCER')
		UniqueImprovement["Rinwell"] 						= git('IMPROVEMENT_RINWELL')
		UniqueImprovement["Rinwell 2"] 						= git('IMPROVEMENT_RINWELL2')
		UniqueImprovement["Rinwell 3"] 						= git('IMPROVEMENT_RINWELL3')
		UniqueImprovement["Seven Pines"] 					= git('IMPROVEMENT_SEVEN_PINES')
		UniqueImprovement["Sirona's Beacon"] 				= git('IMPROVEMENT_SIRONAS_BEACON')
		UniqueImprovement["Standing Stones"] 				= git('IMPROVEMENT_STANDING_STONES')
		UniqueImprovement["Tower of Eyes"] 					= git('IMPROVEMENT_TOWER_OF_EYES')
		UniqueImprovement["Tomb of Sucellus"] 				= git('IMPROVEMENT_TOMB_OF_SUCELLUS')
		UniqueImprovement["Well of Souls"]					= git('IMPROVEMENT_WELL_OF_SOULS')
		UniqueImprovement["Well of Souls (Open)"]			= git('IMPROVEMENT_WELL_OF_SOULS_OPEN')
		UniqueImprovement["Yggdrasil"] 						= git('IMPROVEMENT_YGGDRASIL')
		self.UniqueImprovements 				= UniqueImprovement

	def getManaNodeDict(self):
		return self.ManaNodes

	def initManaNodeDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString

		Mana = {}
		Mana["Air"] 		= git('IMPROVEMENT_MANA_AIR')
		Mana["Body"] 		= git('IMPROVEMENT_MANA_BODY')
		Mana["Chaos"]		= git('IMPROVEMENT_MANA_CHAOS')
		Mana["Creation"]	= git('IMPROVEMENT_MANA_CREATION')
		Mana["Death"] 		= git('IMPROVEMENT_MANA_DEATH')
		Mana["Dimensional"] = git('IMPROVEMENT_MANA_DIMENSIONAL')
		Mana["Earth"] 		= git('IMPROVEMENT_MANA_EARTH')
		Mana["Enchantment"]	= git('IMPROVEMENT_MANA_ENCHANTMENT')
		Mana["Entropy"] 	= git('IMPROVEMENT_MANA_ENTROPY')
		Mana["Fire"] 		= git('IMPROVEMENT_MANA_FIRE')
		Mana["Force"] 		= git('IMPROVEMENT_MANA_FORCE')
		Mana["Ice"] 		= git('IMPROVEMENT_MANA_ICE')
		Mana["Law"] 		= git('IMPROVEMENT_MANA_LAW')
		Mana["Life"] 		= git('IMPROVEMENT_MANA_LIFE')
		Mana["Metamagic"] 	= git('IMPROVEMENT_MANA_METAMAGIC')
		Mana["Mind"] 		= git('IMPROVEMENT_MANA_MIND')
		Mana["Nature"] 		= git('IMPROVEMENT_MANA_NATURE')
		Mana["Refined"]		= git('IMPROVEMENT_REFINERY')
		Mana["Shadow"] 		= git('IMPROVEMENT_MANA_SHADOW')
		Mana["Spirit"] 		= git('IMPROVEMENT_MANA_SPIRIT')
		Mana["Sun"] 		= git('IMPROVEMENT_MANA_SUN')
		Mana["Water"] 		= git('IMPROVEMENT_MANA_WATER')
		self.ManaNodes 		= Mana

	def getSpecialistDict(self):
		return self.Specialists

	def initSpecialistDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Specialist = {}
		Specialist["Statesman"]         = git('SPECIALIST_STATESMAN')
		Specialist["Great Merchant"]    = git('SPECIALIST_GREAT_MERCHANT')
		Specialist["Great Scientist"]   = git('SPECIALIST_GREAT_SCIENTIST')
		Specialist["Scientist"]         = git('SPECIALIST_SCIENTIST')
		Specialist["Healer"]            = git('SPECIALIST_HEALER')
		Specialist["Great Healer"]      = git('SPECIALIST_GREAT_HEALER')

		self.Specialists = Specialist

	def getGreatPeopleDict(self):
		return self.GreatPeople

	def initGreatPeopleDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		GreatPerson = {}
		GreatPerson["Adventurer"] 		= git('UNITCLASS_ADVENTURER')
		GreatPerson["Great Bard"] 		= git('UNITCLASS_ARTIST')
		GreatPerson["Great Commander"] = git('UNITCLASS_COMMANDER')
		GreatPerson["Great Engineer"] 	= git('UNITCLASS_ENGINEER')
		GreatPerson["Great Merchant"] 	= git('UNITCLASS_MERCHANT')
		GreatPerson["Great Prophet"] 	= git('UNITCLASS_PROPHET')
		GreatPerson["Great Sage"] 		= git('UNITCLASS_SCIENTIST')
		GreatPerson["Healer"] 			= git('UNITCLASS_HEALER')

		self.GreatPeople = GreatPerson

	def getReligionDict(self):
		return self.Religions

	def initReligionDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Religion = {}
		Religion["Ashen Veil"] 			= git('RELIGION_THE_ASHEN_VEIL')
		Religion["Fellowship"]			= git('RELIGION_FELLOWSHIP_OF_LEAVES')
		Religion["Order"] 				= git('RELIGION_THE_ORDER')
		Religion["Runes of Kilmorph"] 	= git('RELIGION_RUNES_OF_KILMORPH')
		Religion["Octopus Overlords"] 	= git('RELIGION_OCTOPUS_OVERLORDS')
		Religion["Empyrean"] 			= git('RELIGION_THE_EMPYREAN')
		Religion["Council of Esus"] 	= git('RELIGION_COUNCIL_OF_ESUS')
		Religion["White Hand"] 			= git('RELIGION_WHITE_HAND')
		self.Religions = Religion

	def getCivicDict(self):
		return self.Civics

	def initCivicDict(self):
		gc = CyGlobalContext()
		git = gc.getInfoTypeForString
		Civic = {}
		Civic["Government"] 			= git('CIVICOPTION_GOVERNMENT')
		Civic["Despotism"] 				= git('CIVIC_DESPOTISM')
		Civic["City States"]			= git('CIVIC_CITY_STATES')
		Civic["Tribal Law"]				= git('CIVIC_TRIBAL_LAW')
		Civic["God King"] 				= git('CIVIC_GOD_KING')
		Civic["Aristocracy"]			= git('CIVIC_ARISTOCRACY')
		Civic["Theocracy"] 				= git('CIVIC_THEOCRACY')
		Civic["Republic"] 				= git('CIVIC_REPUBLIC')
		Civic["Traditions"]				= git('CIVIC_TRADITIONS')

		Civic["Cultural Values"] 		= git('CIVICOPTION_CULTURAL_VALUES')
		Civic["Religion"] 				= git('CIVIC_RELIGION')
		Civic["Pacifism"] 				= git('CIVIC_PACIFISM')
		Civic["Nationhood"] 			= git('CIVIC_NATIONHOOD')
		Civic["Sacrifice The Weak"] 	= git('CIVIC_SACRIFICE_THE_WEAK')
		Civic["Social Order"] 			= git('CIVIC_SOCIAL_ORDER')
		Civic["Consumption"] 			= git('CIVIC_CONSUMPTION')
		Civic["Scholarship"] 			= git('CIVIC_SCHOLARSHIP')
		Civic["Liberty"]				= git('CIVIC_LIBERTY')
		Civic["Glory"]					= git('CIVIC_GLORY')

		Civic["Labor"] 					= git('CIVICOPTION_LABOR')
		Civic["Tribalism"]				= git('CIVIC_TRIBALISM')
		Civic["Apprenticeship"]			= git('CIVIC_APPRENTICESHIP')
		Civic["Slavery"]				= git('CIVIC_SLAVERY')
		Civic["Blood And Sacrifice"] 	= git('CIVIC_BLOOD_AND_SACRIFICE')
		Civic["Arete"] 					= git('CIVIC_ARETE')
		Civic["Military State"]			= git('CIVIC_MILITARY_STATE')
		Civic["Caste System"] 			= git('CIVIC_CASTE_SYSTEM')
		Civic["Guilds"]					= git('CIVIC_GUILDS')
		Civic["Industry"]				= git('CIVIC_INDUSTRY')

		Civic["Economy"] 				= git('CIVICOPTION_ECONOMY')
		Civic["Decentralization"] 		= git('CIVIC_DECENTRALIZATION')
		Civic["Agrarianism"] 			= git('CIVIC_AGRARIANISM')
		Civic["Conquest"] 				= git('CIVIC_CONQUEST')
		Civic["Mercentalism"] 			= git('CIVIC_MERCANTILISM')
		Civic["Foreign Trade"] 			= git('CIVIC_FOREIGN_TRADE')
		Civic["Lost Lands"]	 			= git('CIVIC_LOST_LANDS')
		Civic["Guardian of Nature"] 	= git('CIVIC_GUARDIAN_OF_NATURE')

		Civic["Membership"] 			= git('CIVICOPTION_MEMBERSHIP')
		Civic["No Membership"] 			= git('CIVIC_NO_MEMBERSHIP')
		Civic["Overcouncil"]  			= git('CIVIC_OVERCOUNCIL')
		Civic["Undercouncil"] 			= git('CIVIC_UNDERCOUNCIL')
		Civic["Wild Council"]			= git('CIVIC_WILDCOUNCIL')
		Civic["Crusade"] 				= git('CIVIC_CRUSADE')
		self.Civics = Civic

	def showAutoPlayPopup(self):
		'Window for when user switches to AI Auto Play'
		popupSizeX = 400
		popupSizeY = 200
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		xRes = screen.getXResolution()
		yRes = screen.getYResolution()
		popup = PyPopup.PyPopup(CvUtil.EventSetTurnsAutoPlayPopup, contextType = EventContextTypes.EVENTCONTEXT_ALL)
		popup.setPosition((xRes - popupSizeX) / 2, (yRes - popupSizeY) / 2 - 50)
		popup.setSize(popupSizeX, popupSizeY)
		popup.setHeaderString(CyTranslator().getText("TXT_KEY_AIAUTOPLAY_TURN_ON", ()))
		popup.setBodyString(CyTranslator().getText("TXT_KEY_AIAUTOPLAY_TURNS", ()))
		popup.addSeparator()
		popup.createPythonEditBox('10', 'Number of turns to turn over to AI', 0)
		popup.setEditBoxMaxCharCount(4, 2, 0)
		popup.addSeparator()
		popup.addButton("OK")
		popup.addButton(CyTranslator().getText("TXT_KEY_AIAUTOPLAY_CANCEL", ()))
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def printScreen(self, szText):
		CyInterface().addImmediateMessage(szText,"")

	def getEffectInfo(self, name):
		gc = CyGlobalContext()
		for i in range(gc.getNumEffectInfos()):
			item=gc.getEffectInfo(i)
			if(item.getType()==name):
				return i

	def isAI(self, iPlayer):
		if not CyGlobalContext().getPlayer(iPlayer).isHuman():
			return True
		return False

	def isBarbarian(self, iPlayer):
		if iPlayer == CyGlobalContext().getORC_PLAYER():
			return True
		return False

	def getNumPlayers(self): # Ronkhar : this function is never used in RifE or AoE as of 2014_10
	##########################################
	#' Counts the number of active players  '#
	##########################################
		gc = CyGlobalContext()
		iNum = 0
		for iPlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(iPlayer)
			if (pPlayer.isAlive() and iPlayer != gc.getORC_PLAYER()):
				iNum+=1
		return iNum

	def getDistance(self, pPlot, pTarget): # Ronkhar : this function is never used in RifE or AoE as of 2014_10
		return plotDistance(pTarget.getX(), pTarget.getY(), pPlot.getX(), pPlot.getY())

	def getMovesLeft(self, pUnit): return (pUnit.movesLeft() / gc.getMOVE_DENOMINATOR())
