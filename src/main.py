import asyncio
import sys

from src.repositories import PaymentRepository
from src.services import PaymentService
from src.project.config import settings
from src.telegram_bot import init_bot


async def main():
    try:

        await PaymentService.restore_database_from_file(file_path=settings.path_to_db_file)

        await init_bot()

    except Exception as _ex:
        print(_ex, file=sys.stderr)
    finally:
        PaymentRepository.close_client()


if __name__ == "__main__":
    asyncio.run(main())
