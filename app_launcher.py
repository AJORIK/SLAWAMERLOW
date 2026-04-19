import asyncio
from app.main import app, dp, bot
import uvicorn
import os

async def start():
    await dp.start_polling(bot)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    uvicorn.run(app, host="0.0.0.0", port=port)
