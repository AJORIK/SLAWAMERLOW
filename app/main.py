import os
import asyncio
import uvicorn
from fastapi import FastAPI
from bot import dp, bot  # импорт вашего бота

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway требует переменную PORT
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    uvicorn.run(app, host="0.0.0.0", port=port)
