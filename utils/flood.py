
import asyncio
from pyrogram.errors import FloodWait

class FloodController:
    def __init__(self):
        self.lock = asyncio.Lock()

    async def run(self, func, *args, **kwargs):
        async with self.lock:
            while True:
                try:
                    return await func(*args, **kwargs)
                except FloodWait as e:
                    print(f"[FloodWait] Sleeping {e.value}s")
                    await asyncio.sleep(e.value)

flood = FloodController()
