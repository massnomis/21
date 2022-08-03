import asyncio
import websockets

connections = set()
connections.add('wss://stream.binance.com:9443/ws/btcbusd@trade')
connections.add('wss://stream.binance.com:9443/ws/btcusdt@trade')
connections.add('wss://stream.binance.com:9443/ws/btctusd@trade')

async def handle_socket(uri, ):
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            print(message)

async def handler():
    await asyncio.wait([handle_socket(uri) for uri in connections])

asyncio.get_event_loop().run_until_complete(handler())