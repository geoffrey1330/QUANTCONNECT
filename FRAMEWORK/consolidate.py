from Execution.ImmediateExecutionModel import ImmediateExecutionModel
from Portfolio.EqualWeightingPortfolioConstructionModel import EqualWeightingPortfolioConstructionModel
from Risk.MaximumDrawdownPercentPerSecurity import MaximumDrawdownPercentPerSecurity
from Selection.QC500UniverseSelectionModel import QC500UniverseSelectionModel

class SimpleRSITestQC500Universe(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1) # Set Start Date
        self.SetEndDate(2020, 6, 5) # Set End Date
        self.SetCash(100000) # Set Strategy Cash
       # self.SetExecution(ImmediateExecutionModel())
       # self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
       # self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.05))
       # symbols = [ Symbol.Create("SPY", SecurityType.Equity, Market.USA), Symbol.Create("GE", SecurityType.Equity, Market.USA), Symbol.Create("BA", SecurityType.Equity, Market.USA) ]
       # self.SetUniverseSelection(ManualUniverseSelectionModel(symbols))
       # self.UniverseSettings.Resolution = Resolution.Minute
       # self.AddAlpha(MacdAlphaModel())
        

class MacdAlphaModel(AlphaModel):
    '''Defines a custom alpha model that uses MACD crossovers. The MACD signal line
    is used to generate up/down insights if it's stronger than the bounce threshold.
    If the MACD signal is within the bounce threshold then a flat price insight is returned.'''

    def __init__(self,
                 fastPeriod = 12,
                 slowPeriod = 26,
                 signalPeriod = 9,
                 movingAverageType = MovingAverageType.Exponential,
                 resolution=Resolution.Minute ):
        ''' Initializes a new instance of the MacdAlphaModel class
        Args:
            fastPeriod: The MACD fast period
            slowPeriod: The MACD slow period</param>
            signalPeriod: The smoothing period for the MACD signal
            movingAverageType: The type of moving average to use in the MACD'''
        self.period=14
        self.fastPeriod = fastPeriod
        self.slowPeriod = slowPeriod
        self.signalPeriod = signalPeriod
        self.movingAverageType = movingAverageType
        self.resolution = resolution
        self.insightPeriod = timedelta(minutes =5)
        self.symbolDataBySymbol = {}
        self.closeWindows = {}
        self.macdWindows = {}
        self.macdWindowsmin = {}
        resolutionString = Extensions.GetEnumString(resolution, Resolution)
        
        self.closeWindowmin = RollingWindow[QuoteBar](20)
        
        self.closeWindowhr = RollingWindow[QuoteBar](20)
        
        #self.Name = '{}({},{})'.format(self.__class__.__name__, period, resolutionString)
   # def FiveMinuteBarHandler(self, consolidated):
   #   pass
   # def On_W1(self,sender,bar):
        '''
        This method will be called every time a new 30 minute bar is ready. 
    
        bar = The incoming Tradebar. This is different to the data object in OnData()
        '''
        
    def Update(self, algorithm, data):
        insights = []
        
        for symbol, symbolData in self.symbolDataBySymbol.items():
            
          #  C1_Con=QuoteBarConsolidator(timedelta(minutes=15))
          #  C1_Con.DataConsolidated += self.On_W1
          #  algorithm.SubscriptionManager.AddConsolidator(symbol,C1_Con)
          #  direction = InsightDirection.Flat
           # D1_Con=QuoteBarConsolidator(timedelta(hours=1))
            #D1_Con.DataConsolidated += self.On_W1
           # algorithm.SubscriptionManager.AddConsolidator(symbol,D1_Con)
            #five_m=algorithm.Consolidate(data[symbol], timedelta(minutes=5), self.FiveMinuteBarHandler)
            
            
            
            #algorithm.Consolidate(security.Symbol,timedelta(hours=4),lambda x:self.window_4hr.Add(x))
            
            if data.ContainsKey(symbol) and data[symbol] is not None:
                self.closeWindows[symbol].Add(data[symbol].Close)
                
                #self.closeWindow.Add(data[symbol].Close)
                algorithm.Consolidate(symbol,timedelta(minutes=5), lambda x:self.closeWindowmin.Add(x))
                
                algorithm.Consolidate(symbol,timedelta(hours=1), lambda x:self.closeWindowhr.Add(x))
               # self.macdWindows[symbol].Add(macd.Current.Value)
           # if self.closeWindows[symbol].Count>2:
            #    algorithm.Debug(self.closeWindows[symbol][2])
            macd = symbolData.MACD
            macdmin=symbolData.macd_min
            #self.fxClosed=self.closeWindows[symbol][0]
            #if self.closeWindowhr.IsReady:
               # self.closeWindow[2].Close
             #  self.fxClosed=self.closeWindowhr[0]
            self.macdWindows[symbol].Add(macd.Current.Value)
            
            fast=symbolData.fast
            slow=symbolData.slow
            
            self.macdWindowsmin[symbol].Add(macdmin.Current.Value)
            ################
            UP_BB_m=symbolData.bool_m.UpperBand.Current.Value #data["EURUSD"].High
           # bb2 = MA - 2*ST
            DW_BB_m=symbolData.bool_m.LowerBand.Current.Value  #

            UP_BB_hr=symbolData.bool_hr.UpperBand.Current.Value #data["EURUSD"].High
           # bb2 = MA - 2*ST
            DW_BB_hr=symbolData.bool_hr.LowerBand.Current.Value  #


            UP_BB_4hr=symbolData.bool_4hr.UpperBand.Current.Value #data["EURUSD"].High
          #  algorithm.Debug(UP_BB_4hr)
           # algorithm.Debug(self.fxClosed)
           # bb2 = MA - 2*ST
            DW_BB_4hr=symbolData.bool_4hr.LowerBand.Current.Value  
            ###############
            if symbolData.bool_4hr.IsReady and self.closeWindowhr.IsReady:
                self.fxClosed=self.closeWindowhr[0].Close
                if ((DW_BB_hr/self.fxClosed)*100>95 and (DW_BB_hr/self.fxClosed)*100<=100):
                    if fast>slow:
                       # signad=self.Macd_min(symbol)
                        #if signad=="BUY":
                        if macdmin.Current.Value>0:
                            insights.append(Insight.Price(symbol, self.insightPeriod, InsightDirection.Up))
                   # if macdmin.Current.Value>0:
                       # algorithm.Debug("BUY")
                    elif fast<slow:
                        #direction=InsightDirection.Flat
                        insights.append(Insight.Price(symbol,self.insightPeriod, InsightDirection.Flat))
                       
                       #direction = InsightDirection.Up
                      #  insights.append(Insight.Price(symbol, self.insightPeriod, InsightDirection.Up))
                    
               # if round(self.fxClose,3)==round(Ch_long,3):
               #     self.Liquidate("EURUSD")
              #  else:
                    #if not self.Portfolio.Invested:
                      #  self.SetHoldings("EURUSD", 0.02)
                elif ((self.fxClosed/UP_BB_hr)*100>95 and (self.fxClosed/UP_BB_hr)*100<=100):
                    if fast<slow:
                        signad=self.Macd_min(symbol)
                        #if signad=="SELL":
                        if macdmin.Current.Value<0:
                            insights.append(Insight.Price(symbol,self.insightPeriod, InsightDirection.Down))
                    #if macdmin.Current.Value<0:
                        #algorithm.Debug("SELL")
                    elif fast>slow:
                      #  direction=InsightDirection.Flat
                         insights.append(Insight.Price(symbol,self.insightPeriod, InsightDirection.Flat))
                        
                  #  direction = InsightDirection.Down
                    # insights.append(Insight.Price(symbol,self.insightPeriod, InsightDirection.Down))

               # if direction == symbolData.PreviousDirection:
                #     continue
            
           
           # insights.append(Insight.Price(symbol, self.insightPeriod,direction))
        
            ################ insights.append(Insight.Price(symbol, self.insightPeriod, InsightDirection.Up))
    
        return insights
        
    
    
    def Macd(self,symbol):
       # if not (self.window.IsReady and self._macdWin.IsReady and self._macdWin2.IsReady): return
       # self.fxOpen =data["EURUSD"].Open  
        #for symbol in self.closeWindows.keys():
        self.fxOpen=self.closeWindows[symbol][0]
        self.fxClose=self.closeWindows[symbol][0]
        self.pxClose2=self.closeWindows[symbol][1]
        self.pxClose3=self.closeWindows[symbol][2]
        self.pxClose4=self.closeWindows[symbol][3]
        self.pxClose5=self.closeWindows[symbol][4]
        self.pxClose6=self.closeWindows[symbol][5]
        self.pxClose7=self.closeWindows[symbol][6]
        self.pxClose8=self.closeWindows[symbol][7]
        self.pxClose9=self.closeWindows[symbol][8]
        self.pxClose10=self.closeWindows[symbol][9]
        self.pxClose11=self.closeWindows[symbol][10]
        self.pxClose12=self.closeWindows[symbol][11]
        self.pxClose13=self.closeWindows[symbol][12]
        self.pxClose14=self.closeWindows[symbol][13]
        self.pxClose15=self.closeWindows[symbol][14]
        self.pxClose16=self.closeWindows[symbol][15]
        self.pxClose17=self.closeWindows[symbol][16]
        self.pxClose18=self.closeWindows[symbol][17]
        self.pxClose19=self.closeWindows[symbol][18]
        self.pxClose20=self.closeWindows[symbol][19]
    #for symbol in self.macdWindows.keys():
        #MACD
        self.currmacd = self.macdWindows[symbol][0]                     # Current SMA had index zero.
        self.pastmacd = self.macdWindows[symbol][1]   # Oldest SMA has index of window count minus 1.
        self.pastmacd2 = self.macdWindows[symbol][2]
        self.pastmacd3 = self.macdWindows[symbol][3]
        self.pastmacd4 = self.macdWindows[symbol][4]
        self.pastmacd5 = self.macdWindows[symbol][5]
        self.pastmacd6 = self.macdWindows[symbol][6]
        self.pastmacd7 = self.macdWindows[symbol][7]
        self.pastmacd8 = self.macdWindows[symbol][8]
        self.pastmacd9 = self.macdWindows[symbol][9]
        self.pastmacd10 = self.macdWindows[symbol][10]
        self.pastmacd11 = self.macdWindows[symbol][11]
        self.pastmacd12 = self.macdWindows[symbol][12]
        self.pastmacd13 = self.macdWindows[symbol][13]
        self.pastmacd14 = self.macdWindows[symbol][14]
        self.pastmacd15 = self.macdWindows[symbol][15]
        self.pastmacd16 = self.macdWindows[symbol][16]
        self.pastmacd17 = self.macdWindows[symbol][17]
        self.pastmacd18 = self.macdWindows[symbol][18]
        self.pastmacd19 = self.macdWindows[symbol][19]
        #self.pastmacd20 = sd._macdWin[sd._macdWin.Count-20]
        #if not sd.__macd.IsReady: return
        data=""
        #data.clear()
        if(self.pastmacd>self.pastmacd2 and self.pastmacd>self.currmacd):
            extremum2=self.currmacd
            extremum1=max([self.pastmacd2,self.pastmacd3,self.pastmacd4,self.pastmacd5,self.pastmacd6,self.pastmacd7,self.pastmacd8,self.pastmacd9,self.pastmacd10,self.pastmacd11,self.pastmacd12,self.pastmacd13,self.pastmacd14,self.pastmacd15,self.pastmacd16,self.pastmacd17,self.pastmacd18,self.pastmacd19])

            preciomax2=self.fxClose
            preciomax=max([self.pxClose2,self.pxClose3,self.pxClose4,self.pxClose5,self.pxClose6,self.pxClose7,self.pxClose8,self.pxClose9,self.pxClose10,self.pxClose11,self.pxClose12,self.pxClose13,self.pxClose14,self.pxClose15,self.pxClose16,self.pxClose17,self.pxClose18,self.pxClose19,self.pxClose20])

            if (extremum2<extremum1 and preciomax2>preciomax):
               # for i in range(1,self.length):
               #     if self.__macd[i]==extremum1:
                #        zz=i
                signal="SELL"
                data=signal
            elif (extremum2>extremum1 and preciomax2<preciomax):
               # print("MACD1")
                #for i in range(wik,wik+N):
               #     if self.__macd[i]==extremum1:

                #        zz=i

                signal="BUY"
                data=signal

        elif (self.pastmacd<self.pastmacd2 and self.pastmacd<self.currmacd):
            extremum22=self.currmacd
            extremum11=min([self.pastmacd2,self.pastmacd3,self.pastmacd4,self.pastmacd5,self.pastmacd6,self.pastmacd7,self.pastmacd8,self.pastmacd9,self.pastmacd10,self.pastmacd11,self.pastmacd12,self.pastmacd13,self.pastmacd14,self.pastmacd15,self.pastmacd16,self.pastmacd17,self.pastmacd18,self.pastmacd19])
            preciomin2=self.fxClose
            preciomin=min([self.pxClose2,self.pxClose3,self.pxClose4,self.pxClose5,self.pxClose6,self.pxClose7,self.pxClose8,self.pxClose9,self.pxClose10,self.pxClose11,self.pxClose12,self.pxClose13,self.pxClose14,self.pxClose15,self.pxClose16,self.pxClose17,self.pxClose18,self.pxClose19,self.pxClose20])

            if (extremum22>extremum11 and preciomin2<preciomin):

               # for i2 in range(1,self.length):

                 #   if self.__macd[j][i2]==extremum11:
                       # zz2=i2
                signal="BUY"
                data=signal
            elif (extremum22<extremum11 and preciomin2>preciomin):
                signal="SELL"
                data=signal
                #for i2 in range(wik,wik+N):
                   # if self.__macd[i2]==extremum11:
                        #zz2=i2
                       # signal="SELL"
        return data 
        
    def Macd_min(self,symbol):
       # if not (self.window.IsReady and self._macdWin.IsReady and self._macdWin2.IsReady): return
       # self.fxOpen =data["EURUSD"].Open  
        #for symbol, symbolData in self.symbolDataBySymbol.items():
        self.fxOpen=self.closeWindows[symbol][0]
        self.fxClose=self.closeWindows[symbol][0]
        self.pxClose2=self.closeWindows[symbol][1]
        self.pxClose3=self.closeWindows[symbol][2]
        self.pxClose4=self.closeWindows[symbol][3]
        self.pxClose5=self.closeWindows[symbol][4]
        self.pxClose6=self.closeWindows[symbol][5]
        self.pxClose7=self.closeWindows[symbol][6]
        self.pxClose8=self.closeWindows[symbol][7]
        self.pxClose9=self.closeWindows[symbol][8]
        self.pxClose10=self.closeWindows[symbol][9]
        self.pxClose11=self.closeWindows[symbol][10]
        self.pxClose12=self.closeWindows[symbol][11]
        self.pxClose13=self.closeWindows[symbol][12]
        self.pxClose14=self.closeWindows[symbol][13]
        self.pxClose15=self.closeWindows[symbol][14]
        self.pxClose16=self.closeWindows[symbol][15]
        self.pxClose17=self.closeWindows[symbol][16]
        self.pxClose18=self.closeWindows[symbol][17]
        self.pxClose19=self.closeWindows[symbol][18]
        self.pxClose20=self.closeWindows[symbol][19]

        #MACD
        self.currmacd = self.macdWindowsmin[symbol][0]                     # Current SMA had index zero.
        self.pastmacd = self.macdWindowsmin[symbol][1]   # Oldest SMA has index of window count minus 1.
        self.pastmacd2 = self.macdWindowsmin[symbol][2]
        self.pastmacd3 = self.macdWindowsmin[symbol][3]
        self.pastmacd4 = self.macdWindowsmin[symbol][4]
        self.pastmacd5 = self.macdWindowsmin[symbol][5]
        self.pastmacd6 = self.macdWindowsmin[symbol][6]
        self.pastmacd7 = self.macdWindowsmin[symbol][7]
        self.pastmacd8 = self.macdWindowsmin[symbol][8]
        self.pastmacd9 = self.macdWindowsmin[symbol][9]
        self.pastmacd10 = self.macdWindowsmin[symbol][10]
        self.pastmacd11 = self.macdWindowsmin[symbol][11]
        self.pastmacd12 = self.macdWindowsmin[symbol][12]
        self.pastmacd13 = self.macdWindowsmin[symbol][13]
        self.pastmacd14 = self.macdWindowsmin[symbol][14]
        self.pastmacd15 = self.macdWindowsmin[symbol][15]
        self.pastmacd16 = self.macdWindowsmin[symbol][16]
        self.pastmacd17 = self.macdWindowsmin[symbol][17]
        self.pastmacd18 = self.macdWindowsmin[symbol][18]
        self.pastmacd19 = self.macdWindowsmin[symbol][19]
        #self.pastmacd20 = sd._macdWin[sd._macdWin.Count-20]
        #if not sd.__macd.IsReady: return
        data=""
        #data.clear()
        if (self.pastmacd>self.pastmacd2 and self.pastmacd>self.currmacd):
            extremum2=self.pastmacd
            extremum1=max([self.pastmacd2,self.pastmacd3,self.pastmacd4,self.pastmacd5,self.pastmacd6,self.pastmacd7,self.pastmacd8,self.pastmacd9,self.pastmacd10,self.pastmacd11,self.pastmacd12,self.pastmacd13,self.pastmacd14,self.pastmacd15,self.pastmacd16,self.pastmacd17,self.pastmacd18,self.pastmacd19])

            preciomax2=self.fxClose
            preciomax=max([self.pxClose2,self.pxClose3,self.pxClose4,self.pxClose5,self.pxClose6,self.pxClose7,self.pxClose8,self.pxClose9,self.pxClose10,self.pxClose11,self.pxClose12,self.pxClose13,self.pxClose14,self.pxClose15,self.pxClose16,self.pxClose17,self.pxClose18,self.pxClose19,self.pxClose20])

            if (extremum2<extremum1 and preciomax2>preciomax):
               # for i in range(1,self.length):
               #     if self.__macd[i]==extremum1:
                #        zz=i
                signal="SELL"
                data=signal
            elif (extremum2>extremum1 and preciomax2<preciomax):
               # print("MACD1")
                #for i in range(wik,wik+N):
               #     if self.__macd[i]==extremum1:

                #        zz=i

                signal="BUY"
                data=signal

        elif (self.pastmacd<self.pastmacd2 and self.pastmacd<self.currmacd):
            extremum22=self.pastmacd
            extremum11=min([self.pastmacd2,self.pastmacd3,self.pastmacd4,self.pastmacd5,self.pastmacd6,self.pastmacd7,self.pastmacd8,self.pastmacd9,self.pastmacd10,self.pastmacd11,self.pastmacd12,self.pastmacd13,self.pastmacd14,self.pastmacd15,self.pastmacd16,self.pastmacd17,self.pastmacd18,self.pastmacd19])
            preciomin2=self.fxClose
            preciomin=min([self.pxClose2,self.pxClose3,self.pxClose4,self.pxClose5,self.pxClose6,self.pxClose7,self.pxClose8,self.pxClose9,self.pxClose10,self.pxClose11,self.pxClose12,self.pxClose13,self.pxClose14,self.pxClose15,self.pxClose16,self.pxClose17,self.pxClose18,self.pxClose19,self.pxClose20])

            if (extremum22>extremum11 and preciomin2<preciomin):

               # for i2 in range(1,self.length):

                 #   if self.__macd[j][i2]==extremum11:
                       # zz2=i2
                signal="BUY"
                data=signal
            elif (extremum22<extremum11 and preciomin2>preciomin):
                signal="SELL"
                data=signal
                #for i2 in range(wik,wik+N):
                   # if self.__macd[i2]==extremum11:
                        #zz2=i2
                       # signal="SELL"
        return data     
            
            #################
    def OnSecuritiesChanged(self, algorithm, changes):
        
        # clean up data for removed securities
        symbols = [ x.Symbol for x in changes.RemovedSecurities ]
        if len(symbols) > 0:
            for subscription in algorithm.SubscriptionManager.Subscriptions:
                if subscription.Symbol in symbols:
                    self.symbolDataBySymbol.pop(subscription.Symbol, None)
                    subscription.Consolidators.Clear()
                
        # initialize data for added securities
        
        addedSymbols = [ x.Symbol for x in changes.AddedSecurities if x.Symbol not in self.symbolDataBySymbol]
        if len(addedSymbols) == 0: return
        
        history = algorithm.History(addedSymbols,self.period+ 20, self.resolution)
        
        for symbol in addedSymbols:
            macd = algorithm.MACD(symbol,self.fastPeriod,self.slowPeriod,self.signalPeriod,self.movingAverageType,Resolution.Hour)
            
            macdmin = algorithm.MACD(symbol,self.fastPeriod,self.slowPeriod,self.signalPeriod,self.movingAverageType,Resolution.Minute)
            #rsi.Updated += self.RsiUpdated(symbol=symbol, sender=sender, updated=updated)
            self.macdWindows[symbol] = RollingWindow[float](20)
            self.closeWindows[symbol] = RollingWindow[float](20)
            
            self.macdWindowsmin[symbol] = RollingWindow[float](20)
            # symbolTradeBarsHistory = history.loc[symbol]
            # symbolClose = symbolTradeBarsHistory["close"]
            # symbolTime = symbolTradeBarsHistory["time"]
            # for historyIndex in range(self.period):
            #     self.closeWindows[symbol].Add(symbolClose[historyIndex])
            #     self.rsiWindows[symbol].Add(symbolTime[historyIndex],symbolClose[historyIndex])
            # if not history.empty:
            #     ticker = SymbolCache.GetTicker(symbol)
            # if ticker not in history.index.levels[0]:
            #     Log.Trace(f'RsiAlphaModel.OnSecuritiesChanged: {ticker} not found in history data frame.')
            #     continue
            for tuple in history.loc[symbol].itertuples():
                self.closeWindows[symbol].Add(tuple.close)
                
               # self.closeWindow.Add(tuple)
                algorithm.Debug(tuple)
                
                macd.Update(tuple.Index, tuple.close)
                macdmin.Update(tuple.Index, tuple.close)
                if macdmin.IsReady:
                    self.macdWindowsmin[symbol].Add(macdmin.Current.Value)
                if macd.IsReady:
                    self.macdWindows[symbol].Add(macd.Current.Value)
        for added in changes.AddedSecurities:
            self.symbolDataBySymbol[symbol] = SymbolData(algorithm,added,self.fastPeriod,self.slowPeriod,self.signalPeriod,self.movingAverageType,self.resolution)
            # symbolTradeBarsHistory = None
            # symbolClose = None
            
        for k in self.closeWindows.keys():
            algorithm.Debug(str(k) + ' ' + str(self.closeWindows[k][0]) + ' ' + str(self.closeWindows[k][1]) + ' ' + str(self.closeWindows[k][2]) + ' ' + str(self.closeWindows[k][3]) + ' ' + str(self.closeWindows[k][4]) + ' ' + str(self.closeWindows[k][5]))
    
    
        #def RsiUpdated(self, symbol, sender, updated):
        # self.rsiWindows[symbol].Add(updated)


class SymbolData:
    def __init__(self, algorithm,security, fastPeriod, slowPeriod, signalPeriod, movingAverageType, resolution):
         self.Security = security
         self.MACD = MovingAverageConvergenceDivergence(fastPeriod, slowPeriod, signalPeriod, movingAverageType)

         self.Consolidator = algorithm.ResolveConsolidator(security.Symbol,Resolution.Hour)
         algorithm.RegisterIndicator(security.Symbol, self.MACD, self.Consolidator)
        # self.State = State.Middle
         self.ATR = AverageTrueRange(5,MovingAverageType.Simple)
         self.Consolidator = algorithm.ResolveConsolidator(security.Symbol,Resolution.Hour)
         algorithm.RegisterIndicator(security.Symbol,self.ATR, self.Consolidator)
         
         self.ADX = AverageDirectionalIndex(14)
         self.Consolidator = algorithm.ResolveConsolidator(security.Symbol,Resolution.Hour)
         algorithm.RegisterIndicator(security.Symbol,self.ADX, self.Consolidator)
         
         self.bool_m =BollingerBands(20,2,MovingAverageType.Simple)
         self.Consolidator = algorithm.ResolveConsolidator(security.Symbol,timedelta(minutes=5))
         algorithm.RegisterIndicator(security.Symbol,self.bool_m , self.Consolidator)
        
         self.bool_hr =BollingerBands(20,2,MovingAverageType.Simple)
         self.Consolidator = algorithm.ResolveConsolidator(security.Symbol,Resolution.Hour)
         algorithm.RegisterIndicator(security.Symbol,self.bool_hr , self.Consolidator)
        
         self.bool_4hr =BollingerBands(20,2,MovingAverageType.Simple)
         #self.Consolidator = algorithm.ResolveConsolidator(security.Symbol,Resolution.Hour)
         #algorithm.RegisterIndicator(security.Symbol,self.bool_hr , self.Consolidator)
         self.consolidator = QuoteBarConsolidator(timedelta(hours=4))
         self.consolidator.DataConsolidated += self.OnDataConsolidated
         algorithm.SubscriptionManager.AddConsolidator(security.Symbol, self.consolidator)
         
         algorithm.RegisterIndicator(security.Symbol,self.bool_4hr, self.consolidator)
        ##############
         self.macd_min = MovingAverageConvergenceDivergence(fastPeriod, slowPeriod, signalPeriod, movingAverageType)

         self.Consolidator = algorithm.ResolveConsolidator(security.Symbol,timedelta(minutes=15))
         algorithm.RegisterIndicator(security.Symbol, self.macd_min, self.Consolidator)
         
         self.fast=LinearWeightedMovingAverage(3)
         self.Consolidator = algorithm.ResolveConsolidator(security.Symbol,timedelta(minutes=15))
         algorithm.RegisterIndicator(security.Symbol,self.fast, self.Consolidator)
         
         self.slow=LinearWeightedMovingAverage(13)
         self.Consolidator = algorithm.ResolveConsolidator(security.Symbol,timedelta(minutes=15))
         algorithm.RegisterIndicator(security.Symbol,self.slow, self.Consolidator)
         
         self.PreviousDirection = None
         #if not (self.bool_4hr.IsReady):return
    def OnDataConsolidated(self, sender, bar):
        self.consolidated = True
        
        # C1_Con=QuoteBarConsolidator(timedelta(hours=4))
        # C1_Con.DataConsolidated += self.On_W1