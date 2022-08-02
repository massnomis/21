# CurveSim

CurveSim simulates Curve finance pools with optimal arbitrageurs trading against them. It's primary use is to determine optimal amplitude (A) and fee parameters given historical price and volume feeds. 

## Dependencies:
Python3, scipy, numpy, pandas, matplotlib, itertools, copy

## Basic use:
To simulate a pool with a range of A and/or fee parameters, use the CurveSim.Asim function. Historical data for the coins in 3pool (2 months, 30 min intervals) are provided for testing. Data was acquired from nomics.com and averaged (volume-weighted) across exchanges. Coin pair data (e.g., DAI-USDC) are used to estimate optimal arbitrage trades at each time-point, limiting trade sizes according to historical volume. Coin prices in USD (e.g., DAI-USD) are used to estimate the pool's value over time.

To approximate realistic market conditions, we initiate the pool with the current pool size, and use the "vol_mult" argument to limit trade volume based on the expected proportion of market volume that goes through Curve (e.g., monthly pool volume / monthly price feed volume).

For example, to simulate 3pool with a range of A values, we use:

```python
import CurveSim

coins = ['DAI','USDC','USDT']
D = int(856681803.23*10**18) #10**18 precision
quote = 'USD'
A_list = 'stable' #Default A range for stablecoins, 2**(np.array(range(11,25))/2)
vol_mult = .45

ar, bal, volatility, pool_value, slippage_cost, log_returns, log_returns_hold, err = CurveSim.Asim(D, coins, quote, A_list=A_list, vol_mult=vol_mult, plot=True)
```

To simulate 3pool with a range of A values and fees (caution, may run for a long time), we use:
```python
coins = ['DAI','USDC','USDT']
D = int(856681803.23*10**18)
quote = 'USD'
A_list = 'stable'
fee_list = np.linspace(.0001,.001,10)*10**10 #10**10 precision
vol_mult = .45

ar, bal, volatility, pool_value, slippage_cost, log_returns, log_returns_hold, err = CurveSim.Asim(D, coins, quote, A_list=A_list, fee_list=fee_list, vol_mult=vol_mult, plot=True)
```

## Getting Data:
We provide our code for downloading data from nomics.com in the file "nomics.py". This code requires a paid API key. We will provide comparable code for CoinGecko (free) soon.
