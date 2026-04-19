import asyncio
from fastapi import FastAPI
from bot import dp, bot
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
    uvicorn.run(app, host="0.0.0.0", port=8000)
