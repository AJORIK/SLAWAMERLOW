import datetime
from models import Payment, async_session

async def create_payment(user_id: int, plan_name: str, amount_stars: float, currency="USDT"):
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    wallet_address = "0xFAKEWALLET123"  # заменить на реальный кошелек
    async with async_session() as session:
        payment = Payment(
            user_id=user_id,
            amount_stars=amount_stars,
            currency=currency,
            amount_crypto=amount_stars,  # тестовая конвертация
            wallet_address=wallet_address,
            status="pending",
            expires_at=expires_at
        )
        session.add(payment)
        await session.commit()
        return payment

async def check_payment(tx_hash: str):
    # Здесь нужно интегрировать блокчейн API
    return True
