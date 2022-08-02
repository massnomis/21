tick=194802
tickA=(int(tick/60))*60
tickB=tickA+60
liquidity=16790429749685430997
USDC=6
WETH=18
decimals=WETH-USDC
sqrtB=(1.0001**(tickB/2)*(2**96))
sqrtA=(1.0001**(tickA/2)*(2**96))
amount0=((liquidity*2**96*(sqrtB-sqrtA)/sqrtB/sqrtA)/10**6)
print(amount0)
amount1=liquidity*(sqrtB-sqrtA)/2**96/10**18
print(amount1)
price=amount1/amount0
price2=amount0/amount1
print(price)
print(price2)

