## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums
import CvSomniumInterface
import traceback
import Popup as PyPopup

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()
cs = CvSomniumInterface.CvSomnium()

class CvCorporationScreen:

	def __init__(self):

		self.SCREEN_NAME = "CorporationScreen"
		self.BACKGROUND_ID = "SomniumBackground"
		self.LEFT_PLAYER_ID = "SomniumLeftPlayer"
		self.RIGHT_PLAYER_ID = "SomniumRightPlayer"
		self.DRAW_BUTTON_ID = "SomniumDrawButton"
		self.END_TURN_ID = "SomniumEndTurnButton"
		self.CONCEDE_ID = "SomniumConcedeButton"
		self.RULES_BUTTON_ID = "SomniumRulesButton"
		self.SCORE_LEFT_ID = "SomniumScoreLeft"
		self.SCORE_RIGHT_ID = "SomniumScoreRight"
		self.CARDS_LEFT_ID = "SomniumCardsLeft"
		self.CARDS_LEFT_PANEL = "Panel" + self.CARDS_LEFT_ID
		self.R_ID = "abcdefghij" # inputClass.getFunctionName() doesn't return a number in the string ...
		self.TEXT_INFO_IDS = [ "SomniumTextInfo" + self.R_ID[i] for i in range(5) ]
		self.TEXT_INFO_PANEL = "PanelSomniumTextInfo"
		self.LEFT_CARDS_IDS = [ "SomniumLeftCards" + self.R_ID[i] for i in range(10) ]
		self.RIGHT_CARDS_IDS = [ "SomniumRightCards" + self.R_ID[i] for i in range(10) ]
		self.CENTER_CARDS_IDS = [ "SomniumCenterCards" + self.R_ID[i] for i in range(10) ]

		self.W_SCREEN = 1024
		self.H_SCREEN = 768

		self.iZ = -0.1

		self.X_MARGIN = 3
		self.Y_MARGIN = 2

		self.W_SMALL_CARD = 100
		self.H_SMALL_CARD = 150
		self.W_BIG_CARD = 160
		self.H_BIG_CARD = 240

		self.X_SMALL_CARD_SPACE = 2 + self.W_SMALL_CARD

		self.X_PLAYER_MARGIN = 3
		self.Y_PLAYER_MARGIN = self.X_PLAYER_MARGIN

		self.Y_CENTER_MARGIN = 5
		self.X_CENTER_MARGIN = self.Y_CENTER_MARGIN
		self.Y_BIG_CARD_MARGIN = 8

		self.H_PLAYER_SIZE = (self.H_SCREEN - 2 * (self.Y_MARGIN + self.H_SMALL_CARD + self.Y_CENTER_MARGIN)) / 3 - 2 * self.Y_PLAYER_MARGIN
		self.W_PLAYER_SIZE = self.H_PLAYER_SIZE

		self.X_PLAYER_LEFT = self.W_SCREEN - self.X_MARGIN - 2 * self.X_PLAYER_MARGIN - self.W_PLAYER_SIZE -1
		self.Y_PLAYER_LEFT = self.H_SCREEN - self.Y_MARGIN - self.H_SMALL_CARD - self.Y_CENTER_MARGIN - 2 * self.Y_PLAYER_MARGIN - self.H_PLAYER_SIZE -1

		self.X_PLAYER_RIGHT = self.X_PLAYER_LEFT
		self.Y_PLAYER_RIGHT = self.Y_MARGIN + self.H_SMALL_CARD + self.Y_CENTER_MARGIN

		self.H_INFO_TEXT = self.H_SMALL_CARD

		self.X_DECAIL_BIG_CARD = self.W_BIG_CARD / 4
		self.Y_DECAIL_BIG_CARD = self.H_SCREEN - 2 * (self.Y_MARGIN + self.H_SMALL_CARD) - 3 * self.Y_CENTER_MARGIN - self.H_INFO_TEXT - self.H_BIG_CARD - self.Y_BIG_CARD_MARGIN
		self.Y_DECAIL_BIG_CARD = min(self.Y_DECAIL_BIG_CARD, self.H_BIG_CARD / 4) - 10

		self.W_CENTER_BCARD_PANEL = self.W_SCREEN - 2 * (self.X_MARGIN + self.X_PLAYER_MARGIN) - self.X_CENTER_MARGIN - self.W_PLAYER_SIZE
		self.H_CENTER_BCARD_PANEL = self.H_SCREEN - 2 * (self.Y_MARGIN + self.H_SMALL_CARD + self.Y_CENTER_MARGIN) - self.H_INFO_TEXT - self.Y_CENTER_MARGIN

		self.X_B_BIG_CARDS = (self.W_SCREEN - 2 * (self.X_MARGIN + self.X_CENTER_MARGIN + self.X_PLAYER_MARGIN) - self.W_PLAYER_SIZE - self.X_DECAIL_BIG_CARD - 5 * self.W_BIG_CARD) / 5
		self.X_BIG_CARD_SPACE = self.W_BIG_CARD + self.X_B_BIG_CARDS

		self.X_DECAIL_BIG_CARD -= 5

		self.X_BIG_CARD_FIRST = self.X_MARGIN
		self.Y_BIG_CARD_FIRST = self.Y_MARGIN + self.H_SMALL_CARD + self.Y_CENTER_MARGIN

		self.X_INFO_PANEL = self.X_MARGIN
		self.Y_INFO_PANEL = self.H_SCREEN - self.Y_MARGIN - self.Y_CENTER_MARGIN - 2 * self.H_SMALL_CARD - 1

		self.W_C_BUTTONS = self.W_SMALL_CARD + self.W_SMALL_CARD / 2
		self.X_C_BUTTONS = self.W_SCREEN - self.X_MARGIN - self.X_CENTER_MARGIN - 2 * self.X_PLAYER_MARGIN - self.W_PLAYER_SIZE - self.W_C_BUTTONS - 1
		self.X_CARDS_LEFT = self.X_C_BUTTONS - self.X_CENTER_MARGIN - self.W_SMALL_CARD
		self.Y_CARDS_LEFT = self.Y_INFO_PANEL

		self.Y_C_BUTTONS_MARGIN = 3
		self.H_C_BUTTONS = (self.H_SMALL_CARD - 2 * self.Y_C_BUTTONS_MARGIN) / 3

		self.Y_C_BUTTON_DRAW = self.Y_INFO_PANEL
		self.Y_C_BUTTON_END = self.Y_INFO_PANEL + self.H_C_BUTTONS + self.Y_C_BUTTONS_MARGIN
		self.Y_C_BUTTON_CONCEDE = self.Y_INFO_PANEL + 2 * (self.H_C_BUTTONS + self.Y_C_BUTTONS_MARGIN)

		self.W_INFO_PANEL = self.X_CARDS_LEFT - self.X_INFO_PANEL - self.X_CENTER_MARGIN
		self.H_INFO_PANEL = self.H_SMALL_CARD

		self.Y_SCORES_MARGIN = 3
		self.H_SCORES = 30
		self.W_SCORES = self.W_PLAYER_SIZE + 2 * self.X_PLAYER_MARGIN

		self.X_SCORES = self.X_PLAYER_LEFT
		self.Y_LEFT_SCORE = self.Y_PLAYER_LEFT - self.Y_SCORES_MARGIN - self.H_SCORES - 1
		self.Y_RIGHT_SCORE = self.Y_PLAYER_RIGHT + self.H_PLAYER_SIZE + 2 * self.Y_PLAYER_MARGIN + self.Y_SCORES_MARGIN

		self.X_RULES = self.X_PLAYER_LEFT
		self.H_RULES = self.H_C_BUTTONS
		self.W_RULES = self.W_SCORES
		self.Y_RULES = self.H_SCREEN / 2 - self.H_RULES / 2 - 1

		self.iActivePlayer = -1
		self.iLeftPlayer = -1
		self.iRightPlayer = -1
		self.iLeftLeader = -1
		self.iRightLeader = -1
		self.sLeftName = ""
		self.sRightName = ""
		self.gameMP = False
		self.contextMP = False

		# used to be sure a previous action has been finished to allow the player to handle another action.
		# in SG, to prevent 10 click on draw while the implementation is done.
		# in MP, to prevent a stack of event also
		self.nbActionCalled = 0
		self.nbActionReceived = 0
		self.nbMovieActionCalled = 0
		self.nbMovieActionReceived = 0
		self.nbMPMovieActionCalled = 0
		self.nbMPMovieActionReceived = 0

		self.bScreen = False

		# defined to play the AI turn movie
		self.turnMovie = []
		self.iTime = -1

		self.cardArtPath = {}

		self.colorLight = u""
		self.colorHigh = u""

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.CORPORATION_SCREEN)

	def interfaceScreen(self):

		self.bScreen = True

		screen = self.getScreen()
		if screen.isActive():
			return

		cCL = gc.getColorInfo(gc.getInfoTypeForString("COLOR_SOMNIUM_LIGHT")).getColor()
		cCH = gc.getColorInfo(gc.getInfoTypeForString("COLOR_SOMNIUM_HIGH")).getColor()

		self.colorLight = u"<color=%d,%d,%d>" %(int(cCL.r * 255), int(cCL.g * 255), int(cCL.b * 255))
		self.colorHigh = u"<color=%d,%d,%d>" %(int(cCH.r * 255), int(cCH.g * 255), int(cCH.b * 255))

		self.cardArtPath = {
						-1 : ArtFileMgr.getInterfaceArtInfo("SOMNIUM_NO_CARD").getPath() ,
						(10, 0) : ArtFileMgr.getInterfaceArtInfo("SOMNIUM_JOKER").getPath() ,
						(10, 1) : ArtFileMgr.getInterfaceArtInfo("SOMNIUM_JOKER").getPath() ,
						(10, 2) : ArtFileMgr.getInterfaceArtInfo("SOMNIUM_JOKER").getPath() ,
						(11, 0) : ArtFileMgr.getInterfaceArtInfo("SOMNIUM_DEATH").getPath()
						}
		for i in range(10) :
			for j in range(5) :
				self.cardArtPath[(i, j + 3)] = ArtFileMgr.getInterfaceArtInfo("SOMNIUM_%d_%d" %(i, j + 3)).getPath()

		self.iActivePlayer = gc.getGame().getActivePlayer()

		self.iLeftPlayer = cs.getLeftPlayer(self.iActivePlayer)
		self.iRightPlayer = cs.getRightPlayer(self.iActivePlayer)
		self.iLeftLeader = gc.getPlayer(self.iLeftPlayer).getLeaderType()
		self.iRightLeader = gc.getPlayer(self.iRightPlayer).getLeaderType()
		self.sLeftName = gc.getPlayer(self.iLeftPlayer).getName()
		self.sRightName = gc.getPlayer(self.iRightPlayer).getName()
		self.gameMP = cs.getMPGame(self.iLeftPlayer)
		self.contextMP = bool(gc.getGame().isNetworkMultiPlayer())

		self.nbActionCalled = 0
		self.nbActionReceived = 0
		self.nbMovieActionCalled = 0
		self.nbMovieActionReceived = 0
		self.nbMPMovieActionCalled = 0
		self.nbMPMovieActionReceived = 0

		self.turnMovie = []
		self.iTime = -1

		screen.setRenderInterfaceOnly(True)
		screen.setCloseOnEscape(False)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		# Set the background
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo(cs.getBackGround(self.iLeftPlayer)).getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.showWindowBackground(False)

		self.drawLeftCards()
		self.drawRightCards()
		self.drawPlayers()
		self.drawCenterCards()
		self.drawLeftScore()
		self.drawRightScore()
		self.drawCardsLeft()
		self.drawInfoPanel()
		self.drawDrawButton()
		self.drawEndTurnButton()
		self.drawRulesButton()
		self.drawConcedeButton()

	def drawLeftCards(self):
		screen = self.getScreen()
		for i in range(10) :
			szPanelID = "Panel" + self.LEFT_CARDS_IDS[i]
			screen.addPanel(szPanelID, u"", u"", False, False, self.X_MARGIN + i * self.X_SMALL_CARD_SPACE, self.H_SCREEN - self.Y_MARGIN - self.H_SMALL_CARD -1, self.W_SMALL_CARD, self.H_SMALL_CARD, PanelStyles.PANEL_STYLE_OUT)

			screen.setImageButtonAt(self.LEFT_CARDS_IDS[i], szPanelID, self.cardArtPath[-1], 0, 0, self.W_SMALL_CARD, self.H_SMALL_CARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.enable(self.LEFT_CARDS_IDS[i], False)

	def drawRightCards(self):
		screen = self.getScreen()
		for i in range(10) :
			szPanelID = "Panel" + self.RIGHT_CARDS_IDS[i]
			screen.addPanel(szPanelID, u"", u"", False, False, self.X_MARGIN + i * self.X_SMALL_CARD_SPACE, self.Y_MARGIN, self.W_SMALL_CARD, self.H_SMALL_CARD, PanelStyles.PANEL_STYLE_OUT)

			screen.setImageButtonAt(self.RIGHT_CARDS_IDS[i], szPanelID, self.cardArtPath[-1], 0, 0, self.W_SMALL_CARD, self.H_SMALL_CARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.enable(self.RIGHT_CARDS_IDS[i], False)

	def drawPlayers(self):
		screen = self.getScreen()

		szPanelID = "Panel" + self.LEFT_PLAYER_ID
		screen.addPanel(szPanelID, u"", u"", False, False, self.X_PLAYER_LEFT, self.Y_PLAYER_LEFT, self.W_PLAYER_SIZE + 2 * self.X_PLAYER_MARGIN, self.H_PLAYER_SIZE + 2 * self.Y_PLAYER_MARGIN, PanelStyles.PANEL_STYLE_OUT)
		screen.addLeaderheadGFC(self.LEFT_PLAYER_ID, self.iLeftLeader, AttitudeTypes.ATTITUDE_PLEASED, self.X_PLAYER_LEFT + self.X_PLAYER_MARGIN, self.Y_PLAYER_LEFT + self.Y_PLAYER_MARGIN, self.W_PLAYER_SIZE, self.H_PLAYER_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

		szPanelID = "Panel" + self.RIGHT_PLAYER_ID
		screen.addPanel(szPanelID, u"", u"", False, False, self.X_PLAYER_RIGHT, self.Y_PLAYER_RIGHT, self.W_PLAYER_SIZE + 2 * self.X_PLAYER_MARGIN, self.H_PLAYER_SIZE + 2 * self.Y_PLAYER_MARGIN, PanelStyles.PANEL_STYLE_OUT)
		screen.addLeaderheadGFC(self.RIGHT_PLAYER_ID, self.iRightLeader, AttitudeTypes.ATTITUDE_PLEASED, self.X_PLAYER_RIGHT + self.X_PLAYER_MARGIN, self.Y_PLAYER_RIGHT + self.Y_PLAYER_MARGIN, self.W_PLAYER_SIZE, self.H_PLAYER_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def drawCenterCards(self):
		screen = self.getScreen()

		szPanelID = "PanelCenterCards"
		screen.addPanel(szPanelID, u"", u"", False, False, self.X_BIG_CARD_FIRST, self.Y_BIG_CARD_FIRST, self.W_CENTER_BCARD_PANEL, self.H_CENTER_BCARD_PANEL, PanelStyles.PANEL_STYLE_IN)

		for i in range(10) :
			screen.addDDSGFCAt(self.CENTER_CARDS_IDS[i], szPanelID, self.cardArtPath[-1], self.X_BIG_CARD_SPACE * (i%5) + self.X_DECAIL_BIG_CARD * (i/5), self.Y_BIG_CARD_MARGIN / 2 + self.Y_DECAIL_BIG_CARD * (i/5), self.W_BIG_CARD, self.H_BIG_CARD, WidgetTypes.WIDGET_GENERAL, -1, -1, False )
			screen.hide(self.CENTER_CARDS_IDS[i])

	def drawCardsLeft(self):
		screen = self.getScreen()

		nbCards = len(cs.getCardsLeft(self.iLeftPlayer))

		szPanelID = self.CARDS_LEFT_PANEL
		screen.addPanel(szPanelID, u"", u"", True, False, self.X_CARDS_LEFT, self.Y_CARDS_LEFT, self.W_SMALL_CARD, self.H_SMALL_CARD, PanelStyles.PANEL_STYLE_OUT)

		szImageID = "Image" + self.CARDS_LEFT_ID
		screen.addDDSGFCAt(szImageID, szPanelID, self.cardArtPath[-1], 0, 0, self.W_SMALL_CARD, self.H_SMALL_CARD, WidgetTypes.WIDGET_GENERAL, -1, -1, False )

		szTextID = "Card" + self.CARDS_LEFT_ID
		szText = u"<font=3>" + localText.getText("TXT_KEY_SOMNIUM_CARDS", ()) + u"</font>"
		screen.setLabelAt( szTextID, szPanelID, szText, CvUtil.FONT_CENTER_JUSTIFY, self.W_SMALL_CARD / 2, 0.15 * self.H_SMALL_CARD, self.iZ, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		szTextID = "Left" + self.CARDS_LEFT_ID
		szText = u"<font=3>" + localText.getText("TXT_KEY_SOMNIUM_LEFT", ()) + u"</font>"
		screen.setLabelAt( szTextID, szPanelID, szText, CvUtil.FONT_CENTER_JUSTIFY, self.W_SMALL_CARD / 2, 0.30 * self.H_SMALL_CARD, self.iZ, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		szTextID = self.CARDS_LEFT_ID
		szText = self.colorHigh + u"<font=4b>" + CvUtil.convertToUnicode(str(nbCards)) + u"</font></color>"
		screen.setLabelAt( szTextID, szPanelID, szText, CvUtil.FONT_CENTER_JUSTIFY, self.W_SMALL_CARD / 2, 0.60 * self.H_SMALL_CARD, self.iZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def drawInfoPanel(self):
		screen = self.getScreen()

		szPanelID = self.TEXT_INFO_PANEL
		screen.addPanel(szPanelID, u"", u"", True, False, self.X_INFO_PANEL, self.Y_INFO_PANEL, self.W_INFO_PANEL, self.H_INFO_PANEL, PanelStyles.PANEL_STYLE_IN)

		for i in range(5) :
			szTextID = self.TEXT_INFO_IDS[4 - i]
			szText = u""
			screen.setLabelAt( szTextID, szPanelID, szText, CvUtil.FONT_LEFT_JUSTIFY, 4, self.H_SMALL_CARD * ( i / 6.0 ) + 2, self.iZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def drawDrawButton(self):
		screen = self.getScreen()

		szPanelID = "Panel" + self.DRAW_BUTTON_ID
		screen.addPanel(szPanelID, u"", u"", False, False, self.X_C_BUTTONS, self.Y_C_BUTTON_DRAW, self.W_C_BUTTONS, self.H_C_BUTTONS, PanelStyles.PANEL_STYLE_DAWNTOP)

		szTextID = self.DRAW_BUTTON_ID
		szText = self.colorHigh + localText.getText("TXT_KEY_SOMNIUM_DRAW", ()) + u"</color>"
		screen.setButtonGFC(szTextID, szText, "", self.X_C_BUTTONS, self.Y_C_BUTTON_DRAW, self.W_C_BUTTONS, self.H_C_BUTTONS, WidgetTypes.WIDGET_GENERAL, -1, -1,  ButtonStyles.BUTTON_STYLE_IMAGE )

	def drawEndTurnButton(self):
		screen = self.getScreen()

		szPanelID = "Panel" + self.END_TURN_ID
		screen.addPanel(szPanelID, u"", u"", False, False, self.X_C_BUTTONS, self.Y_C_BUTTON_END, self.W_C_BUTTONS, self.H_C_BUTTONS, PanelStyles.PANEL_STYLE_DAWNTOP)

		szTextID = self.END_TURN_ID
		szText = self.colorHigh + localText.getText("TXT_KEY_SOMNIUM_END_TURN", ()) + u"</color>"
		screen.setButtonGFC(szTextID, szText, "", self.X_C_BUTTONS, self.Y_C_BUTTON_END, self.W_C_BUTTONS, self.H_C_BUTTONS, WidgetTypes.WIDGET_GENERAL, -1, -1,  ButtonStyles.BUTTON_STYLE_IMAGE )

	def drawConcedeButton(self):
		screen = self.getScreen()

		szPanelID = "Panel" + self.CONCEDE_ID
		screen.addPanel(szPanelID, u"", u"", False, False, self.X_C_BUTTONS, self.Y_C_BUTTON_CONCEDE, self.W_C_BUTTONS, self.H_C_BUTTONS, PanelStyles.PANEL_STYLE_DAWNTOP)

		szTextID = self.CONCEDE_ID
		szText = localText.getText("TXT_KEY_SOMNIUM_CONCEDE", ())
		screen.setButtonGFC(szTextID, szText, "", self.X_C_BUTTONS, self.Y_C_BUTTON_CONCEDE, self.W_C_BUTTONS, self.H_C_BUTTONS, WidgetTypes.WIDGET_GENERAL, -1, -1,  ButtonStyles.BUTTON_STYLE_IMAGE )

	def drawRulesButton(self):
		screen = self.getScreen()

		szPanelID = "Panel" + self.RULES_BUTTON_ID
		screen.addPanel(szPanelID, u"", u"", False, False, self.X_RULES, self.Y_RULES, self.W_RULES, self.H_RULES, PanelStyles.PANEL_STYLE_DAWNTOP)

		szTextID = self.RULES_BUTTON_ID
		szText = localText.getText("TXT_KEY_SOMNIUM_RULES", ())
		screen.setButtonGFC(szTextID, szText, "", self.X_RULES, self.Y_RULES, self.W_RULES, self.H_RULES, WidgetTypes.WIDGET_GENERAL, -1, -1,  ButtonStyles.BUTTON_STYLE_IMAGE )

	def drawLeftScore(self):
		screen = self.getScreen()

		szPanelID = "Panel" + self.SCORE_LEFT_ID
		screen.addPanel(szPanelID, u"", u"", True, False, self.X_SCORES, self.Y_LEFT_SCORE, self.W_SCORES, self.H_SCORES, PanelStyles.PANEL_STYLE_IN)

		szTextID = self.SCORE_LEFT_ID
		szPlayerName = self.sLeftName
		szTxtKey = "TXT_KEY_SOMNIUM_SCORE"
		if len(szPlayerName) > 11 : szTxtKey = "TXT_KEY_SOMNIUM_SCORE2"
		if len(szPlayerName) > 18 : szPlayerName = szPlayerName[0:17] +"."
		szText = u"<font=2>" + localText.getText(szTxtKey, (szPlayerName, cs.getLeftScore(self.iLeftPlayer))) + u"</font>"
		screen.setLabelAt( szTextID, szPanelID, szText, CvUtil.FONT_LEFT_JUSTIFY, 0, 0, self.iZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def drawRightScore(self):
		screen = self.getScreen()

		szPanelID = "Panel" + self.SCORE_RIGHT_ID
		screen.addPanel(szPanelID, u"", u"", True, False, self.X_SCORES, self.Y_RIGHT_SCORE, self.W_SCORES, self.H_SCORES, PanelStyles.PANEL_STYLE_IN)

		szTextID = self.SCORE_RIGHT_ID
		szPlayerName = self.sRightName
		szTxtKey = "TXT_KEY_SOMNIUM_SCORE"
		if len(szPlayerName) > 11 : szTxtKey = "TXT_KEY_SOMNIUM_SCORE2"
		if len(szPlayerName) > 18 : szPlayerName = szPlayerName[0:17] +"."
		szText = u"<font=2>" + localText.getText(szTxtKey, (szPlayerName, cs.getRightScore(self.iLeftPlayer))) + u"</font>"
		screen.setLabelAt( szTextID, szPanelID, szText, CvUtil.FONT_LEFT_JUSTIFY, 0, 0, self.iZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	def updateElement(self, part, argsList = None):
		if not self.bScreen : return

		updateDict = {
			"updateLeftCards" : self.updateLeftCards ,
			"updateRightCards" : self.updateRightCards ,
			"updateCenterCards" : self.updateCenterCards ,
			"updateCardsLeft" : self.updateCardsLeft ,
			"updateInfoPanel" : self.updateInfoPanel ,
			"updateLeftScore" : self.updateLeftScore ,
			"updateRightScore" : self.updateRightScore ,
			"closeScreen" : self.closeScreen ,
			"actionsCalled" : self.incActionsCalled ,
			"actionsReceived" : self.incActionsReceived ,
			"actionsMovieCalled" : self.incMovieActionsCalled ,
			"actionsMovieReceived" : self.incMovieActionsReceived ,
			"actionsMovieMPCalled" : self.incMovieMPActionsCalled ,
			"actionsMovieMPReceived" : self.incMovieMPActionsReceived ,
			"launchTurnMovie" : self.launchTurnMovie ,
			"playSound" : self.playSound
			}

		if part in updateDict.keys() :
			# use try except to prevent an unexpected bug in the refresh to kill the game
			try :
				if argsList :
					updateDict[part](argsList)
				else :
					updateDict[part]()
			except :
				print traceback.format_exc()
				print " SomniumScreen, updateElement : ERROR %r " %part
		else :
			print " SomniumScreen, updateElement : %r not recognized" %part

	def playSound(self, argsList):
		CyInterface().playGeneralSound(argsList[0])

	def launchTurnMovie(self, argsList):
		self.turnMovie = argsList

	def incMovieActionsCalled(self):
		self.nbMovieActionCalled += 1

	def incMovieActionsReceived(self):
		self.nbMovieActionReceived += 1

	def incMovieMPActionsCalled(self):
		self.nbMPMovieActionCalled += 2

	def incMovieMPActionsReceived(self):
		self.nbMPMovieActionReceived += 1

	def incActionsCalled(self):
		self.nbActionCalled += 1

	def incActionsReceived(self, argsList = None):
		if self.iActivePlayer == argsList[0] : self.nbActionReceived += 1

	def updateInfoPanel(self, argsList = None):
		screen = self.getScreen()

		if argsList :
			actions = argsList
		else :
			actions = cs.getActions(self.iLeftPlayer)

		if self.iActivePlayer == self.iLeftPlayer :
			sPlayerName = self.sRightName
		else :
			sPlayerName = self.sLeftName

		nbActions = len(actions)
		if nbActions > 1 : actions.reverse()

		i = 0
		for act in actions :
			szTextID = self.TEXT_INFO_IDS[i]
			szText = u""
			sActTag = act[0]

			if sActTag == "gameStart" :
				iPlayerAction = act[1]
				if self.iActivePlayer == iPlayerAction :
					sDrawCard = CvUtil.convertToStr(localText.getText("TXT_KEY_SOMNIUM_DRAW", ()))
					szText = localText.getText("TXT_KEY_SOMNIUM_WIN_TOSS", ()) + self.colorLight + u". " + u"</color>" + localText.getText("TXT_KEY_SOMNIUM_PRESS_BUTTON", (sDrawCard, ))
				else :
					szText = localText.getText("TXT_KEY_SOMNIUM_WIN_TOSS_PLAYER", (sPlayerName, ))
					if self.gameMP :
						szText += self.colorLight + u"." + u"</color>"
					else :
						szText += self.colorLight + u". " + u"</color>"
						sEndTurn = CvUtil.convertToStr(localText.getText("TXT_KEY_SOMNIUM_END_TURN", ()))
						szText += localText.getText("TXT_KEY_SOMNIUM_PRESS_BUTTON", (sEndTurn, ))
			elif sActTag == "drawCard" :
				iPlayerAction = act[1]
				iCardType = act[2]
				iCardNumber = act[3]

				lArgs = []
				if iCardType > 9 :
					lArgs.append(CvUtil.convertToStr(localText.getText("TXT_KEY_SOMNIUM_TYPE_%d" %iCardType, ())))
					if self.iActivePlayer == iPlayerAction :
						sTxtKey = "TXT_KEY_SOMNIUM_DRAW_SPECIAL_CARD_INFO"
					else :
						sTxtKey = "TXT_KEY_SOMNIUM_DRAW_SPECIAL_CARD_INFO_PLAYER"
						lArgs.append(sPlayerName)
				else :
					lArgs.append(iCardNumber)
					lArgs.append(CvUtil.convertToStr(localText.getText("TXT_KEY_SOMNIUM_TYPE_%d" %iCardType, ())))
					if self.iActivePlayer == iPlayerAction :
						sTxtKey = "TXT_KEY_SOMNIUM_DRAW_CARD_INFO"
					else :
						sTxtKey = "TXT_KEY_SOMNIUM_DRAW_CARD_INFO_PLAYER"
						lArgs.append(sPlayerName)
					szText = localText.getText(sTxtKey, tuple(lArgs))

			elif sActTag == "DiscardDeath" :
				iPlayerAction = act[1]
				sDeath = CvUtil.convertToStr(localText.getText("TXT_KEY_SOMNIUM_TYPE_11", ()))
				if self.iActivePlayer == iPlayerAction :
					szText = localText.getText("TXT_KEY_SOMNIUM_DEATH_DISCARD", (sDeath, ))
				else :
					szText = localText.getText("TXT_KEY_SOMNIUM_DEATH_DISCARD_PLAYER", (sDeath, sPlayerName))

			elif sActTag == "EndGame" :
				iLooser = act[1]
				if iLooser == -1 :
					szText = localText.getText("TXT_KEY_SOMNIUM_DRAW_GAME_INFO", (sPlayerName, ))
				elif self.iActivePlayer == iLooser :
					szText = localText.getText("TXT_KEY_SOMNIUM_LOOSE_GAME_INFO", ())
				else :
					szText = localText.getText("TXT_KEY_SOMNIUM_WIN_GAME_INFO", ())

			elif sActTag == "BeginTurn" :
				iPlayerBegin = act[1]
				if self.iActivePlayer == iPlayerBegin :
					sDrawCard = CvUtil.convertToStr(localText.getText("TXT_KEY_SOMNIUM_DRAW", ()))
					szText = localText.getText("TXT_KEY_SOMNIUM_BEGIN_TURN", ())
					szText += self.colorLight + u" " + u"</color>"
					szText += localText.getText("TXT_KEY_SOMNIUM_PRESS_BUTTON", (sDrawCard, ))
				else :
					szText = localText.getText("TXT_KEY_SOMNIUM_BEGIN_TURN_PLAYER", (sPlayerName, ))

			elif sActTag == "JokerSteal" :
				iStealPlayer, iStolenPlayer, iCardType, iCardValue = act[1:]
				sJoker = CvUtil.convertToStr(localText.getText("TXT_KEY_SOMNIUM_TYPE_10", ()))
				sCardType = CvUtil.convertToStr(localText.getText("TXT_KEY_SOMNIUM_TYPE_%d" %iCardType, ()))
				if self.iActivePlayer == iStolenPlayer :
					szText = localText.getText("TXT_KEY_SOMNIUM_JOKER_STEAL_PLAYER", (sCardType, iCardValue, sJoker, sPlayerName))
				else :
					szText = localText.getText("TXT_KEY_SOMNIUM_JOKER_STEAL", (sCardType, iCardValue, sJoker, sPlayerName))

			elif sActTag == "JokerNoUse" :
				iJokPlayer = act[1]
				sJoker = CvUtil.convertToStr(localText.getText("TXT_KEY_SOMNIUM_TYPE_10", ()))
				if self.iActivePlayer == iJokPlayer :
					szText = localText.getText("TXT_KEY_SOMNIUM_JOKER_NO_USE", (sJoker, sPlayerName))
				else :
					szText = localText.getText("TXT_KEY_SOMNIUM_JOKER_NO_USE_PLAYER", (sJoker, sPlayerName))

			elif sActTag == "DiscardSameType" :
				iDiscardPlayer, iCardType = act[1:]
				sCardType = CvUtil.convertToStr(localText.getText("TXT_KEY_SOMNIUM_TYPE_%d" %iCardType, ()))
				if self.iActivePlayer == iDiscardPlayer :
					szText = localText.getText("TXT_KEY_SOMNIUM_SAME_TYPE_DISCARD", (sCardType, ))
				else :
					szText = localText.getText("TXT_KEY_SOMNIUM_SAME_TYPE_DISCARD_PLAYER", (sCardType, sPlayerName))

			elif sActTag == "BankCard" :
				iBankPlayer, iPoints = act[1:]
				if self.iActivePlayer == iBankPlayer :
					szText = localText.getText("TXT_KEY_SOMNIUM_BANK_CARDS", (iPoints, ))
				else :
					szText = localText.getText("TXT_KEY_SOMNIUM_BANK_CARDS_PLAYER", (iPoints, sPlayerName))

			elif sActTag == "HUJokerPickCard" :
				iPickPlayer = act[1]
				if self.iActivePlayer == iPickPlayer :
					szText = localText.getText("TXT_KEY_SOMNIUM_JOKER_PICK_CARD", (sPlayerName, ))
				else :
					szText = localText.getText("TXT_KEY_SOMNIUM_JOKER_PICK_CARD_PLAYER", (sPlayerName, ))

			else :
				continue

			szText = u"<font=3>" + szText + u"</font>"
			screen.modifyLabel( szTextID, u"", CvUtil.FONT_LEFT_JUSTIFY )
			screen.modifyLabel( szTextID, szText, CvUtil.FONT_LEFT_JUSTIFY )
			i += 1
			if i == 5 : break

			if i < 5 :
				for j in range(i, 5) :
					szTextID = self.TEXT_INFO_IDS[j]
					szText = u""
					screen.modifyLabel( szTextID, szText, CvUtil.FONT_LEFT_JUSTIFY )

	def updateRightScore(self, argsList = None):
		screen = self.getScreen()

		szTextID = self.SCORE_RIGHT_ID
		szPlayerName = gc.getPlayer(self.iRightPlayer).getName()
		szTxtKey = "TXT_KEY_SOMNIUM_SCORE"
		if len(szPlayerName) > 11 : szTxtKey = "TXT_KEY_SOMNIUM_SCORE2"
		if len(szPlayerName) > 18 : szPlayerName = szPlayerName[0:17] +"."

		if argsList :
			szText = u"<font=2>" + localText.getText(szTxtKey, (szPlayerName, argsList[0])) + u"</font>"
		else :
			szText = u"<font=2>" + localText.getText(szTxtKey, (szPlayerName, cs.getRightScore(self.iLeftPlayer))) + u"</font>"

		screen.modifyLabel( szTextID, u"", CvUtil.FONT_LEFT_JUSTIFY)
		screen.modifyLabel( szTextID, szText, CvUtil.FONT_LEFT_JUSTIFY)

	def updateLeftScore(self, argsList = None):
		screen = self.getScreen()

		szTextID = self.SCORE_LEFT_ID
		szPlayerName = gc.getPlayer(self.iLeftPlayer).getName()
		szTxtKey = "TXT_KEY_SOMNIUM_SCORE"
		if len(szPlayerName) > 11 : szTxtKey = "TXT_KEY_SOMNIUM_SCORE2"
		if len(szPlayerName) > 18 : szPlayerName = szPlayerName[0:17] +"."

		if argsList :
			szText = u"<font=2>" + localText.getText(szTxtKey, (szPlayerName, argsList[0])) + u"</font>"
		else :
			szText = u"<font=2>" + localText.getText(szTxtKey, (szPlayerName, cs.getLeftScore(self.iLeftPlayer))) + u"</font>"

		screen.modifyLabel( szTextID, u"", CvUtil.FONT_LEFT_JUSTIFY)
		screen.modifyLabel( szTextID, szText, CvUtil.FONT_LEFT_JUSTIFY)

	def updateCardsLeft(self, argsList = None):
		screen = self.getScreen()

		if argsList :
			nbCards = argsList[0]
		else :
			nbCards = len(cs.getCardsLeft(self.iLeftPlayer))

		szTextID = self.CARDS_LEFT_ID
		szText = self.colorHigh + u"<font=4b>" + CvUtil.convertToUnicode(str(nbCards)) + u"</font></color>"
		screen.modifyLabel( szTextID, u"", CvUtil.FONT_CENTER_JUSTIFY ) #A bug, the text string doesn't update numbers, so reset before apply when there is a number
		screen.modifyLabel( szTextID, szText, CvUtil.FONT_CENTER_JUSTIFY )

	def updateCenterCards(self, argsList = None):
		screen = self.getScreen()

		if argsList :
			centerCards = argsList
		else :
			centerCards = cs.getCenterCards(self.iLeftPlayer)

		nbCards = len(centerCards)

		for i in range(10) :
			if i < nbCards :
				screen.changeDDSGFC(self.CENTER_CARDS_IDS[i], self.cardArtPath[centerCards[i]])
				screen.show(self.CENTER_CARDS_IDS[i])
			else :
				screen.hide(self.CENTER_CARDS_IDS[i])

	def updateRightCards(self, argsList = None):
		screen = self.getScreen()
		for i in range(10) :
			if argsList :
				bestCard = argsList[i]
			else :
				bestCard = cs.getBestCardRight(self.iLeftPlayer, i)

			screen.changeImageButton(self.RIGHT_CARDS_IDS[i], self.cardArtPath[bestCard])
			if bestCard == -1:
				screen.enable(self.RIGHT_CARDS_IDS[i], False)
			else :
				screen.enable(self.RIGHT_CARDS_IDS[i], True)

	def updateLeftCards(self, argsList = None):
		screen = self.getScreen()
		for i in range(10) :
			if argsList :
				bestCard = argsList[i]
			else :
				bestCard = cs.getBestCardLeft(self.iLeftPlayer, i)

			screen.changeImageButton(self.LEFT_CARDS_IDS[i], self.cardArtPath[bestCard])
			if bestCard == -1:
				screen.enable(self.LEFT_CARDS_IDS[i], False)
			else :
				screen.enable(self.LEFT_CARDS_IDS[i], True)

	def closeScreen(self, argsList = None):
		screen = self.getScreen()
		self.bScreen = False
		screen.hideScreen()

	# Will handle the input for this screen...
	def handleInput(self, inputClass):
		if not self.bScreen : return 0
		screen = self.getScreen()

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER) :
			if (inputClass.getData() == int(InputTypes.KB_ESCAPE)) :
				cs.handleAction(1, self.iLeftPlayer, self.iActivePlayer)
				return 1

		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED) :
			sFunctionName = inputClass.getFunctionName()
			if sFunctionName == self.CONCEDE_ID :
				cs.handleAction(1, self.iLeftPlayer, self.iActivePlayer)
				return 1

			if self.nbActionCalled != self.nbActionReceived : return 0
			if self.nbMovieActionCalled != self.nbMovieActionReceived : return 0
			if self.nbMPMovieActionCalled != self.nbMPMovieActionReceived : return 0

			if sFunctionName == self.RULES_BUTTON_ID :
				self.showRulesPopUP()

			elif sFunctionName == self.DRAW_BUTTON_ID :
				cs.handleAction(2, self.iLeftPlayer, self.iActivePlayer)

			elif sFunctionName == self.END_TURN_ID :
				cs.handleAction(3, self.iLeftPlayer, self.iActivePlayer)

			elif "SomniumLeftCards" in sFunctionName :
				cs.handleAction(4, self.iLeftPlayer, self.iActivePlayer, self.R_ID.index(sFunctionName[-1]))

			elif "SomniumRightCards" in sFunctionName :
				cs.handleAction(5, self.iLeftPlayer, self.iActivePlayer, self.R_ID.index(sFunctionName[-1]))
			else :
				print " Somnium, screen.handleInput : function name %r not recognized" %sFunctionName
				return 0

			return 1
		return 0

	# play movie turn
	def update(self, fDelta):
		if not self.bScreen : return
		if self.nbMovieActionCalled != self.nbMovieActionReceived : return
		if len(self.turnMovie) == 0 : return
		if not cs.canHandleAction() : return

		sTag, lArgs = self.turnMovie[0]

		if sTag == "wait" :
			self.iTime = lArgs[0]
			self.turnMovie[0][0] = "waiting"
		elif sTag == "waiting" :
			self.iTime -= fDelta
			if self.iTime < 0 :
				del self.turnMovie[0]
				self.iTime = -1
		elif sTag == "endGame" :
			del self.turnMovie[0]
			if self.iActivePlayer == self.iLeftPlayer :
				cs.handleAction(6, self.iLeftPlayer)

		elif sTag == "canDrawCard" :
			del self.turnMovie[0]
			if self.iActivePlayer == self.iLeftPlayer :
				cs.handleAction(7, self.iLeftPlayer)

		elif sTag == "canEndTurn" :
			del self.turnMovie[0]
			if self.iActivePlayer == self.iLeftPlayer :
				cs.handleAction(8, self.iLeftPlayer)

		elif sTag == "canPickCard" :
			del self.turnMovie[0]
			if self.iActivePlayer == self.iLeftPlayer :
				cs.handleAction(9, self.iLeftPlayer)

		elif sTag == "currentPlayer" :
			del self.turnMovie[0]
			if self.iActivePlayer == self.iLeftPlayer :
				cs.handleAction(10, self.iLeftPlayer, lArgs[0])

		elif sTag == "endMovieMP" :
			del self.turnMovie[0]
			cs.handleAction(11, self.iLeftPlayer, self.iActivePlayer)

		else :
			self.updateElement(sTag, lArgs)
			del self.turnMovie[0]

	def showRulesPopUP(self):
		popup = PyPopup.PyPopup()

		sResText = CyUserProfile().getResolutionString(CyUserProfile().getResolution())
		sX, sY = sResText.split("x")
		iXRes = int(sX)
		iYRes = int(sY)

		iW = 620
		iH = 650

		popup.setSize(iW, iH)
		popup.setPosition((iXRes - iW) / 2, 30)

		popup.addDDS(CyArtFileMgr().getInterfaceArtInfo("SOMNIUM_POPUP_INTRO").getPath(), 0, 0, 512, 128)
		popup.addSeparator()
		popup.setBodyString(localText.getText("TXT_KEY_CONCEPT_SOMNIUM_PEDIA", ()))
		popup.launch()
