import CurveSim

coins = ['DAI','USDC','USDT']
D = int(856681803.23*10**18) #10**18 precision
quote = 'USD'
A_list = 'stable' #Default A range for stablecoins, 2**(np.array(range(11,25))/2)
vol_mult = .45

ar, bal, volatility, pool_value, slippage_cost, log_returns, log_returns_hold, err = CurveSim.Asim(D, coins, quote, A_list=A_list, vol_mult=vol_mult, plot=True)