import asyncio
import sys
import json
import random
from pathlib import Path

from aiohttp import web


app = web.Application()


async def index(request):
    path = Path(__file__).parent / 'static/index.html'
    return web.Response(content_type='text/html', body=path.read_bytes())


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    app.sockets.add(ws)

    name = chr(random.randint(0x4e00, 0x9fff))
    ws.send_str(json.dumps(dict(type='name', value=name)))

    async for msg in ws:
        data = json.loads(msg.data)
        if data['command'] == 'start':
            asyncio.ensure_future(count(app.sockets, name, data['stop']))

    app.sockets.remove(ws)
    return ws


async def count(sockets, name, stop):
    """
    Send 1 to n numbers to all websockets with a 1 second delay.
    """
    for i in range(1, stop+1):
        data = json.dumps(dict(type='message', value='%s: %s'  % (name, i)))
        for ws in sockets:
            ws.send_str(data)
        await asyncio.sleep(1.0)


def main():
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    else:
        port = 8080

    app.sockets = set()
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/websocket/', websocket_handler)
    app.router.add_static('/static/', Path(__file__).parent / 'static')

    async def shutdown_callback(_):
        for ws in app.sockets:
            await ws.close()

    app.on_shutdown.append(shutdown_callback)
    web.run_app(app, port=port)


if __name__ == '__main__':
    main()
