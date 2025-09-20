from stream import streamer,server
import asyncio

async def main():
    streamer_task = asyncio.create_task(streamer.capture_loop())  # assuming start() updates streamer.frame

    server_task = asyncio.create_task(server.stream_server())

    await asyncio.gather(streamer_task, server_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")