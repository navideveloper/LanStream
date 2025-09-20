import asyncio
import cv2,sys
from aiohttp import web
from stream import streamer,config
from stream.helpers import get_local_ip

async def mjpeg_handler(request):
    response = web.StreamResponse(
        status=200,
        reason="OK",
        headers={"Content-Type": "multipart/x-mixed-replace; boundary=frame"},
    )
    await response.prepare(request)

    try:
        while config.RUN:
            if streamer.frame is None:
                await asyncio.sleep(0.01)
                continue

            # Encode latest streamer.frame
            _, jpg = cv2.imencode(".jpg", streamer.frame, [int(cv2.IMWRITE_JPEG_QUALITY), config.JPEG_QUALITY])

            await response.write(b"--frame\r\n")
            await response.write(b"Content-Type: image/jpeg\r\n\r\n")
            await response.write(jpg.tobytes())
            await response.write(b"\r\n")

            await asyncio.sleep(1 / config.TARGET_FPS)
    except (asyncio.CancelledError):
        print('exiting...')
        for i in asyncio.all_tasks():
            i.cancel()
    finally:
        return response


async def stream_server():
    app = web.Application()
    app.router.add_get("/", mjpeg_handler)

    runner = web.AppRunner(app)
    ip = get_local_ip()
    await runner.setup()
    site = web.TCPSite(runner, ip, config.PORT)
    await site.start()
    
    print(f"🚀 Server running at http://{ip}:{config.PORT}/")

    while config.RUN:
        await asyncio.sleep(3600)