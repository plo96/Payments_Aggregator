from abc import ABC
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from src.core.schemas import Payment
from src.project.config import settings


class PaymentRepository(ABC):
    _client = AsyncIOMotorClient(settings.db_url_mongodb)
    _collection = _client['database']['payment_collection']

    @classmethod
    async def get_all(cls) -> list[Payment]:
        """Получение списка всех хранящихся в БД платежей."""
        return [Payment(**entity) async for entity in cls._collection.find({})]

    @classmethod
    async def delete_all(cls) -> None:
        """Удаление всех хранящихся в БД платежей."""
        await cls._collection.delete_many({})

    @classmethod
    async def add_many(cls, data: list[Payment]) -> None:
        """
        Добавление в БД нескольких платежей сразу.
        :param data: Список платежей (в виде схемы Payment).
        :return: None.
        """
        await cls._collection.insert_many([payment.__dict__ for payment in data])

    @classmethod
    async def get_by_data(
            cls,
            dt_from: datetime,
            dt_upto: datetime,
    ) -> list[Payment]:
        """
        Получение данных из БД по платежам в пределах заданных дат.
        :param dt_from: Начальная дата (включается в поиск).
        :param dt_upto: Конечная дата (не включается в поиск).
        :return: Список подходящих под условие платежей (схема Payments).
        """
        query = {
            'dt': {
                '$gte': dt_from,
                '$lt': dt_upto,
            }
        }
        data = cls._collection.find(query)
        return [Payment(**entity) async for entity in data]

    @classmethod
    def close_client(cls):
        """Закрытие клиента соединения с БД."""
        cls._client.close()
