## Bootleg Strategy Overlay
## By TiberiusW
## v 0.1

from CvPythonExtensions import *
import CvScreenEnums
import CvScreensInterface
import SdToolKitAdvanced as sd
#import CustomFunctions

gc = CyGlobalContext()
#cf = CustomFunctions.CustomFunctions()
Range1 = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
Range2 = ((-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(0,-2),(0,-1),(0,1),(0,2),(1,-2),(1,-1),(1,0),(1,1),(1,2),(2,-1),(2,0),(2,1))
Range3 = ((-3,-1),(-3,0),(-3,1),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-1,-3),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(-1,3),(0,-3),(0,-2),(0,-1),(0,1),(0,2),(0,3),(1,-3),(1,-2),(1,-1),(1,0),(1,1),(1,2),(1,3),(2,-2),(2,-1),(2,0),(2,1),(2,2),(3,-1),(3,0),(3,1))
lRange = [Range1,Range2,Range3]

class CvBootlegSOScreen:

	def __init__(self):
		self.bDrawPlots			= False
		self.bLeftMouseDown		= False
		self.iRadiusBSO			= 2
		self.m_pCurrentPlot		= 0
		self.m_iCurrentX		= -1
		self.m_iCurrentY		= -1
		self.alpha				= 50.0
		self.plotData			= []

	def interfaceScreen(self):
		screen = CyGInterfaceScreen("BootlegSOScreen", CvScreenEnums.BOOTLEG_SO_SCREEN)
		screen.setAlwaysShown(True)
		screen.setCloseOnEscape(False)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
		screen.setForcedRedraw(True)
		self.bDrawPlots = True
		self.updateBSO()
		CyInterface().addImmediateMessage("Bootleg Strategy Overlay: Alt-X Highlighter on/off, Shift-X to change radius, Ctrl-X Planned points on/off","")

	def hideScreen(self):
		screen = CyGInterfaceScreen("BootlegSOScreen", CvScreenEnums.BOOTLEG_SO_SCREEN)
		screen.hideScreen()
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		CyEngine().clearColoredPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)

	def update(self, fDelta):
		if CyInterface().isLeftMouseDown():
			if not self.bLeftMouseDown:
				self.writePlot()
				self.bLeftMouseDown = True
		else:
			self.bLeftMouseDown = False
		self.highlightPlot()
		return

	def mouseOverPlot(self, argsList):
		self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
		self.m_iCurrentX = self.m_pCurrentPlot.getX()
		self.m_iCurrentY = self.m_pCurrentPlot.getY()

	def highlightPlot(self):
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		CyEngine().clearColoredPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		if self.m_pCurrentPlot in (0, -1): return
		if self.m_pCurrentPlot.isNone(): return
		iPlayer		= gc.getGame().getActivePlayer()
		iTeam		= gc.getPlayer(iPlayer).getTeam()
		if iTeam == -1: return
		if not self.m_pCurrentPlot.isRevealed(iTeam, False): return
		CyEngine().addColoredPlotAlt( self.m_iCurrentX, self.m_iCurrentY, PlotStyles.PLOT_STYLE_DOT_TARGET, AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", self.alpha )
		if self.iRadiusBSO > 0:
			tRadius = lRange[self.iRadiusBSO - 1]
			for dX,dY in tRadius:
				iX = dX + self.m_iCurrentX
				iY = dY + self.m_iCurrentY
				pPlot = CyMap().plot(iX,iY)
				if pPlot.isNone(): continue
				if not pPlot.isRevealed(iTeam, False): continue
				CyEngine().fillAreaBorderPlotAlt( iX, iY, AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_GREEN", self.alpha )

	def changeRadius(self):
		self.iRadiusBSO += 1
		if self.iRadiusBSO > 3:
			self.iRadiusBSO = 0

	def changeDraw(self):
		if CyGInterfaceScreen("BootlegSOScreen", CvScreenEnums.BOOTLEG_SO_SCREEN).isActive():
			self.bDrawPlots = True
			CyInterface().addImmediateMessage("Planned points are always drawn if Highliter is on. Prees Alt+X to disable the Highliter","")
		else:
			self.bDrawPlots = not self.bDrawPlots
		self.updateBSO()

	def writePlot(self):
		iPlayer		= gc.getGame().getActivePlayer()
		iTeam		= gc.getPlayer(iPlayer).getTeam()
		if self.m_pCurrentPlot == 0: return
		if self.m_pCurrentPlot.isNone(): return
		if not self.m_pCurrentPlot.isRevealed(iTeam, False): return
		data		= sd.sdGetGlobal("BootlegSO", "PlotData"+str(iPlayer))
		bNewPlot	= True
		if data:
			self.plotData = data
		if self.plotData:
			for item in self.plotData:
				if item[0] == self.m_iCurrentX and item[1] == self.m_iCurrentY:
					bNewPlot = False
					self.plotData.remove(item)
					break
			if bNewPlot:
				newItem = [self.m_iCurrentX, self.m_iCurrentY, self.iRadiusBSO]
				self.plotData.append(newItem)
		else:
			newItem = [self.m_iCurrentX, self.m_iCurrentY, self.iRadiusBSO]
			self.plotData.append(newItem)
		sd.sdSetGlobal("BootlegSO", "PlotData"+str(iPlayer), self.plotData)
		self.updateBSO()

	def updateBSO(self):
		iPlayer	= gc.getGame().getActivePlayer()
		iTeam	= gc.getPlayer(iPlayer).getTeam()
		iLayer	= PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_NUMPAD_HELP
		CyEngine().clearAreaBorderPlots(iLayer)
		CyEngine().clearColoredPlots(iLayer)
		data	= sd.sdGetGlobal("BootlegSO", "PlotData"+str(iPlayer))
		if not data or not self.bDrawPlots: return
		for item in data:
			iX = item[0]
			iY = item[1]
			iRadius = item[2]
			CyEngine().addColoredPlotAlt( iX, iY, PlotStyles.PLOT_STYLE_DOT_TARGET, iLayer, "COLOR_CYAN", self.alpha )
			if iRadius > 0:
				tRadius = lRange[iRadius - 1]
				for dX,dY in tRadius:
					jX = dX + iX
					jY = dY + iY
					pPlot = CyMap().plot(jX,jY)
					if pPlot.isNone(): continue
					if not pPlot.isRevealed(iTeam, False): continue
					CyEngine().fillAreaBorderPlotAlt( jX, jY, iLayer, "COLOR_CYAN", self.alpha )

	def handleInput (self, inputClass):
		return 0