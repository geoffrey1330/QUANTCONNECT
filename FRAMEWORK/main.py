from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Algorithm.Framework")
AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Orders import *
from QuantConnect.Algorithm import *
from QuantConnect.Algorithm.Framework import *
#from QuantConnect.Algorithm.Framework.Alphas import *
from QuantConnect.Algorithm.Framework.Execution import *
#from QuantConnect.Algorithm.Framework.Portfolio import *
from QuantConnect.Algorithm.Framework.Risk import *
from QuantConnect.Algorithm.Framework.Selection import *
from datetime import timedelta
import numpy as np
from MacdAlphaModel import MacdAlphaModel
from EqualWeightingPortfolioConstructionModel import EqualWeightingPortfolioConstructionModel
### <summary>
### Basic template framework algorithm uses framework components to define the algorithm.
### </summary>
### <meta name="tag" content="using data" />
### <meta name="tag" content="using quantconnect" />
### <meta name="tag" content="trading and orders" />
class BasicTemplateFrameworkAlgorithm(QCAlgorithm):
    '''Basic template framework algorithm uses framework components to define the algorithm.'''

    def Initialize(self):
        ''' Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        # Set requested data resolution
       # self._macdWin2 = RollingWindow[IndicatorDataPoint](20)
      #  if not (self._macdWin2.IsReady):return
        self.UniverseSettings.Resolution = Resolution.Minute

        self.SetStartDate(2018,10,7)   #Set Start Date
        self.SetEndDate(2019,10,11)    #Set End Date
        self.SetCash(100000)           #Set Strategy Cash
       # self.SetWarmup(100)
        # Find more symbols here: http://quantconnect.com/data
        # Forex, CFD, Equities Resolutions: Tick, Second, Minute, Hour, Daily.
        # Futures Resolution: Tick, Second, Minute
        # Options Resolution: Minute Only.
        symbols = [ Symbol.Create("EURUSD", SecurityType.Forex, Market.Oanda)]

        # set algorithm framework models
        self.AddUniverseSelection(ManualUniverseSelectionModel(symbols))
        self.AddAlpha(MacdAlphaModel())

        # We can define who often the EWPCM will rebalance if no new insight is submitted using:
        # Resolution Enum:
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel(Resolution.Minute))
        # timedelta
        # self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel(timedelta(2)))
        # A lamdda datetime -> datetime. In this case, we can use the pre-defined func at Expiry helper class
        # self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel(Expiry.EndOfWeek))

        self.SetExecution(ImmediateExecutionModel())
        self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.01))

        self.Debug("numpy test >>> print numpy.pi: " + str(np.pi))

    def OnOrderEvent(self, orderEvent):
        if orderEvent.Status == OrderStatus.Filled:
            self.Debug("Purchased Stock: {0}".format(orderEvent.Symbol))