from abc import ABC
from datetime import datetime

import bson
from dateutil.relativedelta import relativedelta

from src.core.schemas import Payment
from src.project.exceptions import UndefinedGroupTypeException
from src.repositories import PaymentRepository


class PaymentService(ABC):

    @staticmethod
    async def agregate_payments(
            dt_from: datetime,
            dt_upto: datetime,
            group_type: str,
    ) -> dict[str: list]:
        match group_type:
            case 'month':
                dt_from = datetime(dt_from.year, dt_from.month, day=1)
                dt_upto = datetime(dt_upto.year, dt_upto.month, day=1)
                dt_delta = relativedelta(months=1)
            case 'day':
                dt_from = datetime(dt_from.year, dt_from.month, day=dt_from.day)
                dt_upto = datetime(dt_upto.year, dt_upto.month, day=dt_upto.day)
                dt_delta = relativedelta(days=1)
            case 'hour':
                dt_from = datetime(dt_from.year, dt_from.month, day=dt_from.day, hour=dt_from.hour)
                dt_upto = datetime(dt_upto.year, dt_upto.month, day=dt_upto.day, hour=dt_upto.hour)
                dt_delta = relativedelta(hours=1)
            case _:
                raise UndefinedGroupTypeException(f'Trying to use undefined group type: "{group_type}"')

        labels: list = [dt_from]
        dataset: list = []
        payments = await PaymentRepository.get_by_data(
            dt_from=labels[-1],
            dt_upto=labels[-1] + dt_delta,
        )
        dataset.append(sum(payment.value for payment in payments))
        while labels[-1] < dt_upto:
            labels.append(labels[-1] + dt_delta)
            payments = await PaymentRepository.get_by_data(
                dt_from=labels[-1],
                dt_upto=labels[-1] + dt_delta,
            )
            dataset.append(sum(payment.value for payment in payments))
        labels = [label.isoformat() for label in labels]

        return {'dataset': dataset,
                'labels': labels}

    @staticmethod
    async def restore_database_from_file(file_path: str) -> None:

        await PaymentRepository.delete_all()

        with open(file_path, 'rb') as bson_file:
            data = bson.decode_all(bson_file.read())

        data = [Payment(**payment) for payment in data]
        await PaymentRepository.add_many(data=data)
