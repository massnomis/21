from itertools import combinations, product
from scipy.optimize import root_scalar, least_squares
from scipy.stats import siegelslopes
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.lines import Line2D

class pool:

    """
    Python model of Curve pool math.
    """

    def __init__(self, A, D, n, p=None, tokens=None, fee=4*10**6):
        """
        A: Amplification coefficient
        D: Total deposit size
        n: number of currencies
        p: target prices
        fee: fee with 10**10 precision (default = .004%)
        """
        self.A = A  # actually A * n ** (n - 1) because it's an invariant
        self.n = n
        self.fee = fee
        if p:
            self.p = p
        else:
            self.p = [10 ** 18] * n
        if isinstance(D, list):
            self.x = D
        else:
            self.x = [D // n * 10 ** 18 // _p for _p in self.p]
        self.tokens = tokens

    def xp(self):
        return [x * p // 10 ** 18 for x, p in zip(self.x, self.p)]

    def D(self):
        """
        D invariant calculation in non-overflowing integer operations
        iteratively

        A * sum(x_i) * n**n + D = A * D * n**n + D**(n+1) / (n**n * prod(x_i))

        Converging solution:
        D[j+1] = (A * n**n * sum(x_i) - D[j]**(n+1) / (n**n prod(x_i))) / (A * n**n - 1)
        """
        Dprev = 0
        xp = self.xp()
        S = sum(xp)
        D = S
        Ann = self.A * self.n
        while abs(D - Dprev) > 1:
            D_P = D
            for x in xp:
                D_P = D_P * D // (self.n * x)
            Dprev = D
            D = (Ann * S + D_P * self.n) * D // ((Ann - 1) * D + (self.n + 1) * D_P)

        return D

    def y(self, i, j, x):
        """
        Calculate x[j] if one makes x[i] = x

        Done by solving quadratic equation iteratively.
        x_1**2 + x1 * (sum' - (A*n**n - 1) * D / (A * n**n)) = D ** (n+1)/(n ** (2 * n) * prod' * A)
        x_1**2 + b*x_1 = c

        x_1 = (x_1**2 + c) / (2*x_1 + b)
        """
        D = self.D()
        xx = self.xp()
        xx[i] = x  # x is quantity of underlying asset brought to 1e18 precision
        xx = [xx[k] for k in range(self.n) if k != j]
        Ann = self.A * self.n
        c = D
        for y in xx:
            c = c * D // (y * self.n)
        c = c * D // (self.n * Ann)
        b = sum(xx) + D // Ann - D
        y_prev = 0
        y = D
        while abs(y - y_prev) > 1:
            y_prev = y
            y = (y ** 2 + c) // (2 * y + b)
        return y  # the result is in underlying units too

    def y_D(self, i, _D):
        """
        Calculate x[j] if one makes x[i] = x

        Done by solving quadratic equation iteratively.
        x_1**2 + x1 * (sum' - (A*n**n - 1) * D / (A * n**n)) = D ** (n+1)/(n ** (2 * n) * prod' * A)
        x_1**2 + b*x_1 = c

        x_1 = (x_1**2 + c) / (2*x_1 + b)
        """
        xx = self.xp()
        xx = [xx[k] for k in range(self.n) if k != i]
        S = sum(xx)
        Ann = self.A * self.n
        c = _D
        for y in xx:
            c = c * _D // (y * self.n)
        c = c * _D // (self.n * Ann)
        b = S + _D // Ann
        y_prev = 0
        y = _D
        while abs(y - y_prev) > 1:
            y_prev = y
            y = (y ** 2 + c) // (2 * y + b - _D)
        return y  # the result is in underlying units too

    def dy(self, i, j, dx):
        # dx and dy are in underlying units
        xp = self.xp()
        return xp[j] - self.y(i, j, xp[i] + dx)

    def exchange(self, i, j, dx):
        xp = self.xp()
        x = xp[i] + dx
        y = self.y(i, j, x)
        dy = xp[j] - y
        fee = dy * self.fee // 10 ** 10
        assert dy > 0
        self.x[i] = x * 10 ** 18 // self.p[i]
        self.x[j] = (y + fee) * 10 ** 18 // self.p[j]
        return dy - fee


    def remove_liquidity_imbalance(self, amounts):
        _fee = self.fee * self.n // (4 * (self.n - 1))

        old_balances = self.x
        new_balances = self.x[:]
        D0 = self.D()
        for i in range(self.n):
            new_balances[i] -= amounts[i]
        self.x = new_balances
        D1 = self.D()
        self.x = old_balances
        fees = [0] * self.n
        for i in range(self.n):
            ideal_balance = D1 * old_balances[i] // D0
            difference = abs(ideal_balance - new_balances[i])
            fees[i] = _fee * difference // 10 ** 10
            new_balances[i] -= fees[i]
        self.x = new_balances
        D2 = self.D()
        self.x = old_balances

        token_amount = (D0 - D2) * self.tokens // D0

        return token_amount


    def calc_withdraw_one_coin(self, token_amount, i):
        xp = self.xp()
        if self.fee:
            fee = self.fee - self.fee * xp[i] // sum(xp) + 5 * 10 ** 5
        else:
            fee = 0

        D0 = self.D()
        D1 = D0 - token_amount * D0 // self.tokens
        dy = xp[i] - self.y_D(i, D1)

        return dy - dy * fee // 10 ** 10


    def dydx(self, i, j, dx):
        """
        Returns price, dy[j]/dx[i], given some dx[i]
        """
        dy = self.dy(i,j,dx)
        return dy/dx


    def dydxfee(self, i, j, dx):
        """
        Returns price with fee, (dy[j]-fee)/dx[i]. given some dx[i]
        """
        dy = self.dy(i,j,dx)*(1-self.fee/10**10)
        return dy/dx


    def optarb(self,i,j, p):
        """
        Estimates trade to optimally arbitrage coin[i] for coin[j] given external price p (base: i, quote: j)
        p must be less than dy[j]/dx[i], including fees
        
        Returns:
        trade: format (i,j,dx)
        errors: price errors, (dy-fee)/dx - p, for each pair of coins after the trades
        res: output from numerical estimator
        
        """
        bounds = (10**12, self.y(j, i, int(self.xp()[j]*.01))-self.xp()[i]) #Lo: 1, Hi: enough coin[i] to leave 1% of coin[j]
        
        res = root_scalar(arberror, args=(self, i, j, p), bracket=bounds, method="brentq")
    
        trade = (i, j, int(res.root))
    
        error = arberror(res.root, self, i, j, p)
    
        return trade, error, res


    def slippage(self, size=.0005):
        """
        Estimates proportion of pool holdings needed to move price by "size"; default = .05%
        
        """
        combos = list(combinations(range(self.n),2))       
        sumxp = sum(self.xp())
        
        slippage_cost = []
        for i,j in combos:
            trade, error, res = self.optarb(i,j, self.dydxfee(i, j, 10**12)*(1-size))
            slippage_cost.append(trade[2]/sumxp)
            
            trade, error, res = self.optarb(j,i, self.dydxfee(j, i, 10**12)*(1-size))
            slippage_cost.append(trade[2]/sumxp)
            
        return slippage_cost
            
    
    
    def optarbs(self,prices,limits):
        """
        Estimates trades to optimally arbitrage all coins in a pool, given prices and volume limits
        
        Returns:
        trades: list of trades with format (i,j,dx)
        error: (dy-fee)/dx - p
        res: output from numerical estimator
        
        """
        combos = list(combinations(range(self.n),2))
    
        #Initial guesses for dx, limits, and trades
        #uses optarb (i.e., only considering price of coin[i] and coin[j])
        #guess will be too high but in range
        k = 0
        x0 = []
        lo = []
        hi = []
        coins = []
        price_targs = []
        for pair in combos:
            i = pair[0]
            j = pair[1]
            if prices[k] < arberror(10**12,self,i,j, prices[k]) + prices[k]:
                trade, error, res = self.optarb(i,j, prices[k])
                x0.append(min(trade[2], limits[k]*10**18))
                lo.append(0)
                hi.append(limits[k]*10**18+1)
                coins.append((i,j))
                price_targs.append(prices[k])
                
            elif 1/prices[k] < arberror(10**12,self,j,i, 1/prices[k]) + 1/prices[k]:
                trade, error, res = self.optarb(j,i, 1/prices[k])
                x0.append(min(trade[2], limits[k]*10**18))
                lo.append(0)
                hi.append(limits[k]*10**18+1)
                coins.append((j,i))
                price_targs.append(1/prices[k])
                
            else:
                x0.append(0.0)
                lo.append(0)
                hi.append(limits[k]*10**18+1)
                coins.append((i,j))
                price_targs.append(prices[k])
            k += 1

        #Order trades in terms of expected size
        order = sorted(range(len(x0)), reverse= True, key=x0.__getitem__)
        x0 =  [x0[i] for i in order]
        lo =  [lo[i] for i in order]
        hi =  [hi[i] for i in order]
        coins =  [coins[i] for i in order]
        price_targs =  [price_targs[i] for i in order]
    
        #Find trades that minimize difference between pool price and external market price
        res = least_squares(arberrors, x0=x0, args=(self, price_targs, coins), bounds = (lo, hi), gtol = 10**-15, xtol=10**-15)
    
        #Format trades into tuples, ignore if dx=0
        dxs = res.x
        trades = []
        for k in range(len(dxs)):
            if np.isnan(dxs[k]):
                dx = 0
            else:
                dx = int(dxs[k])
        
            if dx > 0:
                i = coins[k][0]
                j = coins[k][1]
                trades.append((i,j,dx))
        
        errors = res.fun
        return trades, errors, res
        
    def dotrades(self, trades, limits=None):
        """
        Does trades formatted as the output of optarbs
        
        Returns list of trades done in format (i,j,dx[i],dy[j])
        
        """
    
        trades_done = []
        for trade in trades:
            i = trade[0]
            j = trade[1]
            dx = trade[2]
            
            dy = self.exchange(i,j,dx)
            trades_done.append((i, j, dx, dy))
    
        return trades_done
        
        
##Simulation functions        
def sim(A, D, n, prices, volumes, fee=4*10**6, vol_mult=1, quotes=None):
    """
    Simulates a pool with parameters A, D, n, and (optionally) fee, given time series of prices and volumes
    Optarbs is called for each timepoint
    
    fee: fee with precision 10**10. Default fee is .0004 (.04%)
    vol_mult: scalar multiplied by volume at each timepoint
    quotes: time series of the values of each coin in units of some quote currency (e.g., USD); used to estimate pool value over time.

    Returns:
    pl: pool object at end of simulation
    err: time series of absolute price errors, (dy-fee)/dx - p, summed accros coin pairs
    bal: balance parameter over time; bal=1 when in perfect balance, and bal=0 when all holdings are in 1 coin
    pool_value: time series of pool's value in supplied quote currency
        
    """  
    
    #Initiate pool
    pl = pool(A,D,n, fee=fee)
    
    #Loop through timepoints and do optimal arb trades
    err = []
    bal = []
    pool_value = []
    slippage_cost = []
    for t in range(len(prices)):
        curr_prices = prices.iloc[t]
        curr_volume = volumes.iloc[t]*vol_mult
        trades, errors, res = pl.optarbs(curr_prices, curr_volume)
        trades_done = pl.dotrades(trades)
        err.append(sum(abs(errors)))
        
        xp = np.array(pl.xp())
        bal.append(1 - sum(abs(xp/sum(xp) - 1/n))/(2*(n-1)/n))
        slippage_cost.append(np.average(pl.slippage()))
        
        if quotes is not None:
            curr_quote = quotes.iloc[t]
            pool_value.append(sum(xp*curr_quote/10**18))
        
    
    return pl, err, bal, pool_value, slippage_cost
    
def Asim(D, coins, quote, arbroute=None, A_list=None, fee_list=[4*10**6], vol_mult=1, t_start=None, t_end=None, resample=None, plot=False):
    """
    Wrapper to load data and call sim repeatedly with a variety of A parameters (A_list) and/or fees (fee_list)
    
    coins: list of coins to load (e.g., ['DAI', 'USDC', 'USDT'])
    quote: if string, name of quote currency to load (e.g., 'USD'); if int, pool value quoted in coins[int] 
    arbroute: determine pairwise coin prices using a third currency (e.g., ETH-SUSD/SETH-SUSD, instead of ETH-SETH)
    A_list: list of A_values; input 'crypto' or 'stable' for default values
    fee_list: list of fees with precision 10**10. Default fee is .0004 (.04%)
    vol_mult: scalar multiplied by volume at each timepoint
    t_start/t_end: used to truncate input time series
    resample: used to downsample input time series
    plot: if true, plots outputs
    
        
    Returns:
    ar: annualized returns 
    bal: pool balance over time
    volatility: relative volatility (compared to holding)
    pool_value: pool value (in quote currency) over time
    log_returns: log returns over time
    log_returns_hold: log returns of holding the original pool balance over time
    err: time series of absolute price errors, (dy-fee)/dx - p, summed accros coin pairs

    """  
    
    n = len(coins)
   
    #Default range of A values
    if A_list is None:
        A_list = (2**(np.array(range(8,25))/2)).round().astype(int)
    elif isinstance(A_list, str):
        if A_list == 'crypto':
            A_list = (2**(np.array(range(8,19))/2)).round().astype(int)
        elif A_list == 'stable':
            A_list = (2**(np.array(range(11,25))/2)).round().astype(int)

    #Multiplier for computing annualized returns (ar)
    if resample is None:
        yearmult = 2*24*365 #default is 30m intervals
    else:
        yearmult = resample/60*24*365
        resample = str(resample)+'T'
        
    #Load price data
    if arbroute is not None:
        prices, volumes = pooldata(coins, quote=arbroute, quotediv=True, t_start=t_start, t_end=t_end, resample=resample)
    else:
        prices, volumes = pooldata(coins, t_start=t_start, t_end=t_end, resample=resample)
    
    #Load quote data (for valuing the pool)
    #If string, load quote data
    if isinstance(quote, str):
        quotes, qvolumes = pooldata(coins, quote=quote, t_start=t_start, t_end=t_end, resample=resample)
    
    #If quote is integer, compute quotes using the provided coin index
    elif isinstance(quote, int):
        quotes = []
        combos = list(combinations(range(len(coins)),2))
        
        for i in range(len(coins)):
            if i < quote:        
                curr_pair = (i, quote)
                curr_idx = combos.index(curr_pair)
                quotes.append(prices.iloc[:,curr_idx])
                
            elif i > quote:        
                curr_pair = (quote, i)
                curr_idx = combos.index(curr_pair)
                quotes.append(prices.iloc[:,curr_idx]**-1)
                
        quotes = pd.concat(quotes,axis=1)
        quotes.insert(quote,'price',np.ones(len(quotes)), allow_duplicates = True)
            
            
    
    #Value over time of holding
    value_hold = np.sum(quotes*([D/n] * n)/10**18,1)
    log_returns_hold = np.diff(np.log(value_hold))
    
    #Loop through sims
    p_list = list(product(A_list,fee_list))
    err_all = []; bal_all = []; value_all = []; slippage_cost_all = []; log_returns_all = []; ar_all = []; volatility_all = []
    for i in range(len(p_list)):
        A = int(round(p_list[i][0]))
        fee = int(round(p_list[i][1]))
        print('Simulating A='+str(A)+', Fee='+str(fee/int(10**8))+'%')
        pl, err, bal, pool_value, slippage_cost = sim(A, D, n, prices, volumes, fee=fee, vol_mult=vol_mult, quotes=quotes)
        
        err_all.append(err)
        bal_all.append(bal)
        value_all.append(pool_value)
        slippage_cost_all.append(slippage_cost)
        
        log_returns = np.diff(np.log(pool_value))
        ar = np.exp(np.average(log_returns)*yearmult)
        slope, intercept = siegelslopes(log_returns, log_returns_hold)
        
        log_returns_all.append(log_returns)
        ar_all.append(ar-1)
        volatility_all.append(slope)

    #Output as DataFrames
    p_list = pd.MultiIndex.from_tuples(p_list, names=["A", "fee"])
    
    err = pd.DataFrame(err_all, index=p_list, columns=quotes.index)
    bal = pd.DataFrame(bal_all, index=p_list, columns=quotes.index)
    pool_value = pd.DataFrame(value_all, index=p_list, columns=quotes.index)
    slippage_cost = pd.DataFrame(slippage_cost_all, index=p_list, columns=quotes.index)
    log_returns = pd.DataFrame(log_returns_all, index=p_list, columns=quotes.index[1:])
    ar = pd.DataFrame(ar_all, index=p_list)
    volatility = pd.DataFrame(volatility_all, index=p_list)
    
    #Plotting
    if plot:
        if len(fee_list) > 1:
            plotsimsfee(A_list, fee_list, ar, bal, slippage_cost, volatility, err)
        else:
            plotsims(A_list, ar, bal, volatility, pool_value, slippage_cost, log_returns, log_returns_hold, err)
    
    return ar, bal, volatility, pool_value, slippage_cost, log_returns, log_returns_hold, err


def pooldata(coins, quote=None, quotediv=False, t_start=None, t_end=None, resample=None):
    """
    Loads and formats price/volume data from CSVs. 
    
    coins: list of coins to load (e.g., ['DAI', 'USDC', 'USDT'])
    quote: if string, name of quote currency to load (e.g., 'USD') 
    quotediv: determine pairwise coin prices using a third currency (e.g., ETH-SUSD/SETH-SUSD, instead of ETH-SETH)
    t_start/t_end: used to truncate input time series
    resample: used to downsample input time series
    
    Returns exchange rates/volumes for each coin pair in order of itertools.list(combinations(coins,2))
    
    """  

    prices = []
    volumes = []
    
    #If no quote, get prices for each pair of coins
    if quote is None:
        combos = list(combinations(coins,2))
    
        for pair in combos:
            curr_file = pair[0]+'-'+pair[1]+'.csv'
            curr_file = pd.read_csv(curr_file, index_col=0)
            prices.append(curr_file['price'])
            volumes.append(curr_file['volume'])
    
    #If quote given, get prices for each coin in quote currency
    else:
        for coin in coins:
            curr_file = coin+'-'+quote+'.csv'
            curr_file = pd.read_csv(curr_file, index_col=0)
            prices.append(curr_file['price'])
            volumes.append(curr_file['volume'])
           
    prices = pd.concat(prices,axis=1)
    volumes = pd.concat(volumes,axis=1)
    
    prices = prices.replace(to_replace=0, method='ffill') #replace price=0 with previous price
    prices = prices.replace(to_replace=0, method='bfill') #replace any price=0 at beginning with subsequent price
    
    #If quotediv, calc prices for each coin pair from prices in quote currency
    if quotediv:
        combos = list(combinations(range(len(coins)),2))
        prices_tmp = []
        volumes_tmp = []
        
        for pair in combos:
            prices_tmp.append(prices.iloc[:,pair[0]]/prices.iloc[:,pair[1]]) #divide prices
            volumes_tmp.append(volumes.iloc[:,pair[0]]+volumes.iloc[:,pair[1]]) #sum volumes
        
        prices = pd.concat(prices_tmp,axis=1)
        volumes = pd.concat(volumes_tmp,axis=1)
    
    #Index as date-time type
    prices.index = pd.to_datetime(prices.index)
    volumes.index = pd.to_datetime(volumes.index)
    
    #Trim to t_start and/or t_end
    if t_start is not None:
        prices = prices.loc[t_start:]
        volumes = volumes.loc[t_start:]
        
    if t_end is not None:
        prices = prices.loc[:t_end]
        volumes = prices.loc[:t_end]
         
    #Resample times
    if resample is not None:
        prices = prices.resample(resample).first()
        volumes = volumes.resample(resample).sum()
        
    return prices, volumes
    
def plotsims(A_list, ar, bal, volatility, pool_value, slippage_cost, log_returns, log_returns_hold, err):
    """
    Plots output of Asims when only 1 fee is used
        
    """
    
    colors = plt.cm.viridis(np.linspace(0,1,len(A_list)))

    #Summary stats
    fig, axs = plt.subplots(2, 3, constrained_layout=True, figsize = (8,5))

    axs[0, 0].plot(ar.unstack(level=1)*100, 'k', zorder=1)
    axs[0, 0].scatter(A_list, ar*100, c=colors, zorder=2)
    axs[0, 0].yaxis.set_major_formatter(mtick.PercentFormatter())
    axs[0, 0].set_xlabel('Amplitude (A)')
    axs[0, 0].set_ylabel('Annualized Returns')
    
    axs[0, 1].plot(A_list, np.median(slippage_cost, axis=1)*100, 'k', zorder=1, label='Med')
    axs[0, 1].plot(A_list, np.min(slippage_cost, axis=1)*100, 'k--', zorder=1, label='Min')
    axs[0, 1].scatter(A_list, np.median(slippage_cost, axis=1)*100, c=colors, zorder=2)
    axs[0, 1].scatter(A_list, np.min(slippage_cost, axis=1)*100, c=colors, zorder=2)
    axs[0, 1].yaxis.set_major_formatter(mtick.PercentFormatter())
    axs[0, 1].set_xlabel('Amplitude (A)')
    axs[0, 1].set_ylabel('Cost of .05% Slippage')
    axs[0, 1].legend(loc='lower right')

    axs[0, 2].plot(A_list, bal.median(axis=1), 'k', zorder=1, label='Med')
    axs[0, 2].plot(A_list, bal.min(axis=1), 'k--', zorder=1, label='Min')
    axs[0, 2].scatter(A_list, bal.median(axis=1), c=colors, zorder=2)
    axs[0, 2].scatter(A_list, bal.min(axis=1), c=colors, zorder=2)
    axs[0, 2].set_ylim([0, 1])
    axs[0, 2].set_xlabel('Amplitude (A)')
    axs[0, 2].set_ylabel('Pool Balance')
    axs[0, 2].legend(loc='lower right')
    


    axs[1, 0].plot(volatility.unstack(level=1), 'k', zorder=1)
    axs[1, 0].scatter(A_list, volatility, c=colors, zorder=2)
    axs[1, 0].set_xlabel('Amplitude (A)')
    axs[1, 0].set_ylabel('Relative Volatility')

    axs[1, 1].plot(A_list, err.median(axis=1), 'k', zorder=1)
    scatter = axs[1, 1].scatter(A_list, err.median(axis=1), c=colors, zorder=2)
    axs[1, 1].set_xlabel('Amplitude (A)')
    axs[1, 1].set_ylabel('Median Price Error')
    
    #Legend
    handles = []
    for i in range(len(colors)):
        handles.append(Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[i], markersize=10))

    axs[1,2].legend(handles, A_list, title='Amplitude', ncol=2) #loc='lower right', bbox_to_anchor=(.95, .9),
    axs[1,2].axis("off")

    #Time-series Data
    fig, axs = plt.subplots(3, 2, constrained_layout=True, figsize = (8,5))

    for i in range(len(colors)):
        axs[0, 0].plot(pool_value.iloc[i], '.', color=colors[i], alpha=.25)

    axs[0, 0].set_ylabel('Pool Value')
    plt.setp(axs[0, 0].xaxis.get_majorticklabels(), rotation=40, ha='right')
   


    for i in range(len(colors)):
        axs[0, 1].plot(bal.iloc[i], color=colors[i])

    axs[0, 1].set_ylabel('Pool Balance')
    plt.setp(axs[0, 1].xaxis.get_majorticklabels(), rotation=40, ha='right')


    for i in range(len(colors)):
        axs[1, 0].plot(log_returns.iloc[i], '.', color=colors[i], alpha=.25)

    axs[1, 0].set_ylabel('Log Returns')  
    plt.setp(axs[1, 0].xaxis.get_majorticklabels(), rotation=40, ha='right')


    for i in range(len(colors)):
        axs[1, 1].plot(slippage_cost.iloc[i], color=colors[i])

    axs[1, 1].set_ylabel('Slippage Cost')  
    plt.setp(axs[1, 1].xaxis.get_majorticklabels(), rotation=40, ha='right')


    for i in range(len(colors)):
        axs[2, 0].plot(log_returns_hold, log_returns.iloc[i], '.', color=colors[i])

    axs[2, 0].set_xlabel('Log Returns (Hold)') 
    axs[2, 0].set_ylabel('Log Returns')  
    plt.setp(axs[2, 0].xaxis.get_majorticklabels(), rotation=40, ha='right')
    
    
    axs[2,1].hist(err.T,30,histtype='step', color=colors)
    axs[2, 1].set_xlabel('Price Error') 
    axs[2, 1].set_ylabel('Frequency')  
    
    plt.show()
    
def plotsimsfee(A_list, fee_list, ar, bal, slippage_cost, volatility, err):
    """
    Plots 2D summary output of Asims when multiple fees are used
        
    """
    fig, axs = plt.subplots(2, 4, constrained_layout=True, figsize = (11,5))
    fee_list_pct = fee_list.round().astype(int)/10**8
    
    #Annualized Returns
    im = axs[0,0].imshow(ar.unstack('fee')*100, cmap='plasma')
    axs[0,0].set_title('Annualized Returns (%)')
    axs[0,0].set_xlabel('Fee (%)')
    axs[0,0].set_ylabel('Amplitude (A)')
    axs[0,0].set_xticks(np.arange(len(fee_list)))
    axs[0,0].set_yticks(np.arange(len(A_list)))
    axs[0,0].set_xticklabels(fee_list_pct)
    axs[0,0].set_yticklabels(A_list)
    plt.setp(axs[0, 0].xaxis.get_majorticklabels(), rotation=90)
    cbar = fig.colorbar(im, ax=axs[0,0])
    
    axs[1,0].axis("off")
    
    
    #Median Slippage
    im = axs[0,1].imshow(slippage_cost.median(axis=1).unstack('fee'), cmap='plasma')
    axs[0,1].set_title('Med. Slippage Cost')
    axs[0,1].set_xlabel('Fee (%)')
    axs[0,1].set_ylabel('Amplitude (A)')
    axs[0,1].set_xticks(np.arange(len(fee_list)))
    axs[0,1].set_yticks(np.arange(len(A_list)))
    axs[0,1].set_xticklabels(fee_list_pct)
    axs[0,1].set_yticklabels(A_list)
    plt.setp(axs[0,1].xaxis.get_majorticklabels(), rotation=90)
    cbar = fig.colorbar(im, ax=axs[0,1])
    
    #Minimum Slippage
    im = axs[1,1].imshow(slippage_cost.min(axis=1).unstack('fee'), cmap='plasma')
    axs[1,1].set_title('Min. Slippage Cost')
    axs[1,1].set_xlabel('Fee (%)')
    axs[1,1].set_ylabel('Amplitude (A)')
    axs[1,1].set_xticks(np.arange(len(fee_list)))
    axs[1,1].set_yticks(np.arange(len(A_list)))
    axs[1,1].set_xticklabels(fee_list_pct)
    axs[1,1].set_yticklabels(A_list)
    plt.setp(axs[1,1].xaxis.get_majorticklabels(), rotation=90)
    cbar = fig.colorbar(im, ax=axs[1,1])
    
    #Median Balance
    im = axs[0,2].imshow(bal.median(axis=1).unstack('fee'), cmap='plasma')
    axs[0,2].set_title('Median Balance')
    axs[0,2].set_xlabel('Fee (%)')
    axs[0,2].set_ylabel('Amplitude (A)')
    axs[0,2].set_xticks(np.arange(len(fee_list)))
    axs[0,2].set_yticks(np.arange(len(A_list)))
    axs[0,2].set_xticklabels(fee_list_pct)
    axs[0,2].set_yticklabels(A_list)
    plt.setp(axs[0,2].xaxis.get_majorticklabels(), rotation=90)
    cbar = fig.colorbar(im, ax=axs[0,2])
    
    #Minimum Balance
    im = axs[1,2].imshow(bal.min(axis=1).unstack('fee'), cmap='plasma')
    axs[1,2].set_title('Minimum Balance')
    axs[1,2].set_xlabel('Fee (%)')
    axs[1,2].set_ylabel('Amplitude (A)')
    axs[1,2].set_xticks(np.arange(len(fee_list)))
    axs[1,2].set_yticks(np.arange(len(A_list)))
    axs[1,2].set_xticklabels(fee_list_pct)
    axs[1,2].set_yticklabels(A_list)
    plt.setp(axs[1,2].xaxis.get_majorticklabels(), rotation=90)
    cbar = fig.colorbar(im, ax=axs[1,2])
    
    #Relative Volatility
    im = axs[0,3].imshow(volatility.unstack('fee'), cmap='plasma')
    axs[0,3].set_title('Relative Volatility')
    axs[0,3].set_xlabel('Fee (%)')
    axs[0,3].set_ylabel('Amplitude (A)')
    axs[0,3].set_xticks(np.arange(len(fee_list)))
    axs[0,3].set_yticks(np.arange(len(A_list)))
    axs[0,3].set_xticklabels(fee_list_pct)
    axs[0,3].set_yticklabels(A_list)
    plt.setp(axs[0,3].xaxis.get_majorticklabels(), rotation=90)
    cbar = fig.colorbar(im, ax=axs[0,3])
    
    #Median Price Error
    im = axs[1,3].imshow(err.median(axis=1).unstack('fee'), cmap='plasma')
    axs[1,3].set_title('Median Price Error')
    axs[1,3].set_xlabel('Fee (%)')
    axs[1,3].set_ylabel('Amplitude (A)')
    axs[1,3].set_xticks(np.arange(len(fee_list)))
    axs[1,3].set_yticks(np.arange(len(A_list)))
    axs[1,3].set_xticklabels(fee_list_pct)
    axs[1,3].set_yticklabels(A_list)
    plt.setp(axs[1,3].xaxis.get_majorticklabels(), rotation=90)
    cbar = fig.colorbar(im, ax=axs[1,3])
    
    plt.show()
    
        

##Error functions for optarb and optarbs     
def arberror(dx,pool,i,j, p):
    dx = int(dx)
    pool_temp = copy.deepcopy(pool)
    
    pool_temp.exchange(i,j,dx) #do trade
    
    #Check price error after trade
    #Error = pool price (dy/dx) - external price (p); 
    error = pool_temp.dydxfee(i,j,10**12) - p 
    return error
    
def arberrors(dxs,pool,price_targs, coins):  
    pool_temp = copy.deepcopy(pool)
    
    #Do each trade
    k = 0
    for pair in coins:
        i = pair[0]
        j = pair[1]
        
        if np.isnan(dxs[k]):
            dx = 0
        else:
            dx = int(dxs[k])
            
        if dx > 0:
            pool_temp.exchange(i,j,dx)

        k += 1
    
    #Check price errors after all trades
    errors = []
    k = 0
    for pair in coins:
        i = pair[0]
        j = pair[1]
        p = price_targs[k]
        errors.append(pool_temp.dydxfee(i,j,10**12) - p)
        k += 1

    return errors
        

