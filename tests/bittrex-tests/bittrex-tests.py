import sys
sys.path.append('../../python-bittrex/bittrex')

from bittrex import Bittrex

#Define Bittrex Key and Sectret
#from https://bittrex.com/Account/ManageApiKey
bittrexKey = ''
bittrexSecret = ''

#Connect to bittrex with api key
print 'Connecting to bittrex'
bitcon = Bittrex(bittrexKey,bittrexSecret)

#Define Market Dictionaries
trustMarket = {}

print 'Getting all bittrex markets and looking for TRUST.'
for result in  bitcon.get_markets()['result']:
	if 'TRUST' in result['MarketCurrency']:
		foundTrust = True
		trustMarket['MarketInfo'] =  result

print 'Getting current TRUST orderbook'
trustMarket['OrderBook'] = bitcon.get_orderbook('BTC-TRUST','both')['result']

print '\n\nCurrent TRUST Market and Orderbook information.'
if foundTrust:
	print trustMarket['MarketInfo'],'\n\n'
	print 'Sell','Buy'
	for sell,buy in zip(trustMarket['OrderBook']['sell'],trustMarket['OrderBook']['buy']):
		print sell,buy
	
