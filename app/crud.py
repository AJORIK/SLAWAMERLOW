from models import User, Plan, Payment, async_session
from sqlalchemy.future import select

async def get_user(tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id==tg_id))
        return result.scalars().first()

async def add_user(tg_id: int, username: str, language="RU"):
    async with async_session() as session:
        user = User(tg_id=tg_id, username=username, language=language)
        session.add(user)
        await session.commit()
        return user
