import asyncio
import logging
from asyncio import StreamReader, StreamWriter


class ServerState:
    def __init__(self):
        self._writers = []

    async def add_client(self, reader: StreamReader, writer: StreamWriter):
        self._writers.append(writer)
        await self._on_connect(writer)
        asyncio.create_task(self._echo(reader, writer))

    async def _on_connect(self, writer: StreamWriter):
        writer.write(f"Welcome! {len(self._writers)} user(s) are online.\n".encode())
        await writer.drain()
        await self._notify_all(f"New user connected!\n")

    async def _echo(self, reader: StreamReader, writer: StreamWriter):
        try:
            while (data := await reader.readline()) != b"":
                writer.write(data)
                await writer.drain()
            self._writers.remove(writer)
            await self._notify_all(f"A user has disconnected.\n")
        except Exception as e:
            logging.error(f"Error in client connection: {e}")
            self._writers.remove(writer)
            await self._notify_all(f"A user has disconnected.\n")

    async def _notify_all(self, message: str):
        for writer in self._writers:
            try:
                writer.write(message.encode())
                await writer.drain()
            except ConnectionError as e:
                logging.error(f"Error notifying client: {e}")
                self._writers.remove(writer)


async def main():
    server_state = ServerState()

    async def client_connected(reader: StreamReader, writer: StreamWriter) -> None:
        await server_state.add_client(reader, writer)

    server = await asyncio.start_server(client_connected, "127.0.0.1", 8000)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
