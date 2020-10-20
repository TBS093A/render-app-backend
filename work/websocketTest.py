import asyncio
from websockets import connect

# sudo docker run -p 6379:6379 -d redis:5

class EchoWebsocket:
    async def __aenter__(self):
        self._conn = connect("wss://localhost:6379/")
        self.websocket = await self._conn.__aenter__()        
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def send(self, message):
        await self.websocket.send(message)

    async def receive(self):
        return await self.websocket.recv()


async def main():
    async with EchoWebsocket() as echo:
        while True:
            await echo.send("Hello!")
            print(await echo.receive())  # "Hello!"
        # while True:
        #     print(await echo.receive())
        #     await asyncio.sleep(.1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())