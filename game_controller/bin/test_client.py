import asyncio
import websockets


async def hello():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        befehl = input("What's your name? ")

        await websocket.send(befehl)

asyncio.get_event_loop().run_until_complete(hello())