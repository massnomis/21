import asyncio
import websockets

connections = set()
connections.add('wss://api.foo.com:8765')
connections.add('wss://api.bar.com:8765')
connections.add('wss://api.foobar.com:8765')

async def handle_socket(uri, ):
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            print(message)

async def handler():
    await asyncio.wait([handle_socket(uri) for uri in connections])

asyncio.get_event_loop().run_until_complete(handler())