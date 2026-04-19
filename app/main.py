import asyncio
import os
from fastapi import FastAPI
from bot import dp, bot
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway передает PORT
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    uvicorn.run(app, host="0.0.0.0", port=port)
