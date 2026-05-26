// plotGroup.cpp

#include "CvGameCoreDLL.h"
#include "CvPlotGroup.h"
#include "CvPlot.h"
#include "CvGlobals.h"
#include "CvPlayerAI.h"
#include "CvMap.h"
#include "CvCity.h"
#include "CvDLLFAStarIFaceBase.h"
#include "FProfiler.h"

// Public Functions...

CvPlotGroup::CvPlotGroup()
{
	m_paiNumBonuses = NULL;

	reset(0, NO_PLAYER, true);
}


CvPlotGroup::~CvPlotGroup()
{
	uninit();
}


void CvPlotGroup::init(int iID, PlayerTypes eOwner, CvPlot* pPlot)
{
	//--------------------------------
	// Init saved data
	reset(iID, eOwner);

	//--------------------------------
	// Init non-saved data

	//--------------------------------
	// Init other game data
	addPlot(pPlot);
}


void CvPlotGroup::uninit()
{
	SAFE_DELETE_ARRAY(m_paiNumBonuses);

	m_plots.clear();
}

// FUNCTION: reset()
// Initializes data members that are serialized.
void CvPlotGroup::reset(int iID, PlayerTypes eOwner, bool bConstructorCall)
{
	int iI;

	//--------------------------------
	// Uninit class
	uninit();

	m_iID = iID;
	m_eOwner = eOwner;

	if (!bConstructorCall)
	{
		FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::reset");
		m_paiNumBonuses = new int [GC.getNumBonusInfos()];
		for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
		{
			m_paiNumBonuses[iI] = 0;
		}
	}
}


void CvPlotGroup::addPlot(CvPlot* pPlot)
{
	XYCoords xy;

	xy.iX = pPlot->getX_INLINE();
	xy.iY = pPlot->getY_INLINE();

	insertAtEndPlots(xy);

	pPlot->setPlotGroup(getOwnerINLINE(), this);
}


void CvPlotGroup::removePlot(CvPlot* pPlot)
{
	CLLNode<XYCoords>* pPlotNode;

	pPlotNode = headPlotsNode();

	while (pPlotNode != NULL)
	{
		if (GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY) == pPlot)
		{
			pPlot->setPlotGroup(getOwnerINLINE(), NULL);

			pPlotNode = deletePlotsNode(pPlotNode); // can delete this PlotGroup...
			break;
		}
		else
		{
			pPlotNode = nextPlotsNode(pPlotNode);
		}
	}
}


void CvPlotGroup::recalculatePlots(bool bForce)
{
	PROFILE_FUNC();

	CLLNode<XYCoords>* pPlotNode;
	CvPlot* pPlot;
	CLinkList<XYCoords> oldPlotGroup;
	CLinkList<XYCoords> oldCityGroup;
	XYCoords xy;
	PlayerTypes eOwner;
	int iCount;

	eOwner = getOwnerINLINE();

	pPlotNode = headPlotsNode();

	if (pPlotNode != NULL)
	{
		pPlot = GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY);

		iCount = 0;

		gDLL->getFAStarIFace()->SetData(&GC.getPlotGroupFinder(), &iCount);
		gDLL->getFAStarIFace()->GeneratePath(&GC.getPlotGroupFinder(), pPlot->getX_INLINE(), pPlot->getY_INLINE(), -1, -1, false, eOwner);

		if (iCount == getLengthPlots() && !bForce)
		{
			return;
		}
	}

	{
		PROFILE("CvPlotGroup::recalculatePlots update");

		oldPlotGroup.clear();
		oldCityGroup.clear();

		pPlotNode = headPlotsNode();

		while (pPlotNode != NULL)
		{
			PROFILE("CvPlotGroup::recalculatePlots update 1");

			pPlot = GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY);

			FAssertMsg(pPlot != NULL, "Plot is not assigned a valid value");

			xy.iX = pPlot->getX_INLINE();
			xy.iY = pPlot->getY_INLINE();

			oldPlotGroup.insertAtEnd(xy);
			if (pPlot->isCity())
			{
				oldCityGroup.insertAtEnd(xy);
				pPlot->getPlotCity()->setDelayBonusUpdate(true);
			}

			pPlot->setPlotGroup(eOwner, NULL);

			pPlotNode = deletePlotsNode(pPlotNode); // will delete this PlotGroup...
		}

		pPlotNode = oldPlotGroup.head();

		while (pPlotNode != NULL)
		{
				PROFILE("CvPlotGroup::recalculatePlots update 2");

			pPlot = GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY);

			FAssertMsg(pPlot != NULL, "Plot is not assigned a valid value");

			pPlot->updatePlotGroup(eOwner, true);

			pPlotNode = oldPlotGroup.deleteNode(pPlotNode);
		}

		pPlotNode = oldCityGroup.head();

		while (pPlotNode != NULL)
		{
			PROFILE("CvPlotGroup::recalculatePlots update 2");

			pPlot = GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY);

			FAssertMsg(pPlot != NULL, "Plot is not assigned a valid value");
			pPlot->getPlotCity()->setDelayBonusUpdate(false);
			if (pPlot->getPlotCity()->plotGroup(eOwner) != NULL)
			{
				pPlot->getPlotCity()->plotGroup(eOwner)->updatePlotGroupBonusCity(pPlot->getPlotCity());
			}
			else
			{
				GET_PLAYER(eOwner).initPlotGroup(pPlot)->updatePlotGroupBonusCity(pPlot->getPlotCity());
			}
			pPlotNode = oldCityGroup.deleteNode(pPlotNode);
		}


	}
}


int CvPlotGroup::getID() const
{
	return m_iID;
}


void CvPlotGroup::setID(int iID)
{
	m_iID = iID;
}


PlayerTypes CvPlotGroup::getOwner() const
{
	return getOwnerINLINE();
}


int CvPlotGroup::getNumBonuses(BonusTypes eBonus) const
{
	FAssertMsg(eBonus >= 0, "eBonus is expected to be non-negative (invalid Index)");
	FAssertMsg(eBonus < GC.getNumBonusInfos(), "eBonus is expected to be within maximum bounds (invalid Index)");
	return m_paiNumBonuses[eBonus];
}


bool CvPlotGroup::hasBonus(BonusTypes eBonus)
{
	return(getNumBonuses(eBonus) > 0);
}


void CvPlotGroup::changeNumBonuses(BonusTypes eBonus, int iChange)
{
	CLLNode<XYCoords>* pPlotNode;
	CvCity* pCity;
	int iOldNumBonuses;

	FAssertMsg(eBonus >= 0, "eBonus is expected to be non-negative (invalid Index)");
	FAssertMsg(eBonus < GC.getNumBonusInfos(), "eBonus is expected to be within maximum bounds (invalid Index)");

	if (iChange != 0)
	{
		iOldNumBonuses = getNumBonuses(eBonus);

		m_paiNumBonuses[eBonus] = (m_paiNumBonuses[eBonus] + iChange);

		//FAssertMsg(m_paiNumBonuses[eBonus] >= 0, "m_paiNumBonuses[eBonus] is expected to be non-negative (invalid Index)"); XXX
		
		
		pPlotNode = headPlotsNode();

		while (pPlotNode != NULL)
		{
			pCity = GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY)->getPlotCity();

			if (pCity != NULL && ! pCity->isDelayBonusUpdate())
			{
				if (pCity->getOwnerINLINE() == getOwnerINLINE())
				{
//					pCity->changeNumBonuses(eBonus, iChange);
					if (((iOldNumBonuses *getNumBonuses(eBonus) <= 0)) && !GC.getBonusInfo(eBonus).isModifierPerBonus())
					{
						if (getNumBonuses(eBonus) > 0 && pCity->getOldNumBonuses(eBonus) <=0)
						{
							pCity->processBonus(eBonus, 1);
							pCity->setNumBonuses(eBonus, getNumBonuses(eBonus));
						}
						else if (getNumBonuses(eBonus)<=0 && pCity->getOldNumBonuses(eBonus) >0)
						{
							pCity->processBonus(eBonus, -1);
							pCity->setNumBonuses(eBonus, getNumBonuses(eBonus));
						}
					}

					if (GC.getBonusInfo(eBonus).isModifierPerBonus() && pCity->getOldNumBonuses(eBonus) != getNumBonuses(eBonus))
					{
						pCity->processBonus(eBonus, getNumBonuses(eBonus) - pCity->getOldNumBonuses(eBonus));
						pCity->setNumBonuses(eBonus, getNumBonuses(eBonus));
					}
					if (pCity->getOldNumBonuses(eBonus) != getNumBonuses(eBonus))
					{
						pCity->setNumBonuses(eBonus, getNumBonuses(eBonus));
					}
				}
			}

			pPlotNode = nextPlotsNode(pPlotNode);
		}
	}

//FfH Damage Types: Added by Kael 08/23/2007
	if (getOwnerINLINE() != NO_PLAYER)
	{
		int iLoop;
		CvUnit* pLoopUnit;
		for (pLoopUnit = GET_PLAYER(getOwnerINLINE()).firstUnit(&iLoop); pLoopUnit != NULL; pLoopUnit = GET_PLAYER(getOwnerINLINE()).nextUnit(&iLoop))
		{
			pLoopUnit->updateBonusAffinity(eBonus);
		}
	}
//FfH: End Add

}


void CvPlotGroup::insertAtEndPlots(XYCoords xy)
{
	m_plots.insertAtEnd(xy);
}


CLLNode<XYCoords>* CvPlotGroup::deletePlotsNode(CLLNode<XYCoords>* pNode)
{
	CLLNode<XYCoords>* pPlotNode;

	pPlotNode = m_plots.deleteNode(pNode);

	if (getLengthPlots() == 0)
	{
		GET_PLAYER(getOwnerINLINE()).deletePlotGroup(getID());
	}

  return pPlotNode;
}


CLLNode<XYCoords>* CvPlotGroup::nextPlotsNode(CLLNode<XYCoords>* pNode)
{
	return m_plots.next(pNode);
}


int CvPlotGroup::getLengthPlots()
{
	return m_plots.getLength();
}


CLLNode<XYCoords>* CvPlotGroup::headPlotsNode()
{
	return m_plots.head();
}


void CvPlotGroup::read(FDataStreamBase* pStream)
{
	// Init saved data
	reset();

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iID);

	pStream->Read((int*)&m_eOwner);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::read");
	pStream->Read(GC.getNumBonusInfos(), m_paiNumBonuses);

	m_plots.Read(pStream);
}


void CvPlotGroup::write(FDataStreamBase* pStream)
{
	uint uiFlag=0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iID);

	pStream->Write(m_eOwner);

	FAssertMsg((0 < GC.getNumBonusInfos()), "GC.getNumBonusInfos() is not greater than zero but an array is being allocated in CvPlotGroup::write");
	pStream->Write(GC.getNumBonusInfos(), m_paiNumBonuses);

	m_plots.Write(pStream);
}

void CvPlotGroup::updatePlotGroupBonusCities()
{
	CLLNode<XYCoords>* pPlotNode;
	CvPlot* pPlot;
	
	pPlotNode = headPlotsNode();

	while (pPlotNode != NULL)
	{
		PROFILE("CvPlotGroup::recalculatePlots update 1");

		pPlot = GC.getMapINLINE().plotSorenINLINE(pPlotNode->m_data.iX, pPlotNode->m_data.iY);

		FAssertMsg(pPlot != NULL, "Plot is not assigned a valid value");

		
		if (pPlot->isCity())
		{
			updatePlotGroupBonusCity(pPlot->getPlotCity());
		}

		
		pPlotNode = nextPlotsNode(pPlotNode); // will delete this PlotGroup...
	}
}

void CvPlotGroup::updatePlotGroupBonusCity(CvCity* pCity)
{
	BonusTypes eBonus;
	if (pCity != NULL)
	{
		if (pCity->getOwnerINLINE() == getOwnerINLINE())
		{
			
			for (int iI = 0; iI < GC.getNumBonusInfos(); iI++)
			{
				eBonus = (BonusTypes)iI;
				if (!GC.getBonusInfo(eBonus).isModifierPerBonus())
				{
					if (getNumBonuses(eBonus) > 0 &&pCity->getOldNumBonuses(eBonus) <=0)
					{
						pCity->processBonus(eBonus, 1);
						pCity->setNumBonuses(eBonus, getNumBonuses(eBonus));
					}
					else if (getNumBonuses(eBonus) <= 0 && pCity->getOldNumBonuses(eBonus) > 0)
					{
						pCity->processBonus(eBonus, -1);
						pCity->setNumBonuses(eBonus, getNumBonuses(eBonus));
					}
				}

				if (GC.getBonusInfo(eBonus).isModifierPerBonus() && pCity->getOldNumBonuses(eBonus) != getNumBonuses(eBonus))
				{
					pCity->processBonus(eBonus, getNumBonuses(eBonus)- pCity->getOldNumBonuses(eBonus));
					pCity->setNumBonuses(eBonus, getNumBonuses(eBonus));
				}
				if (pCity->getOldNumBonuses(eBonus) != getNumBonuses(eBonus))
				{
					pCity->setNumBonuses(eBonus, getNumBonuses(eBonus));
				}

			}
		}
	}

}