import asyncio
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from src.config import DB_COLLECTION, DB_NAME, mongodb_uri
from utils import get_next_date, get_pipeline, convert_date_from_str_to_datime, data_to_json


async def aggregate_data_by_time_period(input_data: dict) -> str:
    """
    :param input_data: входной словарь с данными из сообщения пользователя
    :return: полученные результаты из бд
    """

    values = []
    client = None

    try:
        # сначала подключаемся к бд
        client = AsyncIOMotorClient(mongodb_uri)
        db = client[DB_NAME]
        collection = db[DB_COLLECTION]

        async def aggregate_data_(current_date_: datetime, next_date_: datetime) -> tuple[int, str]:
            """
            Функция берет две даты и получает отрезок времени, в котором считает сумму зарплат
            :param current_date_: начала периода записей для проверки
            :param next_date_: конец периода записей для проверки
            :return: возвращает кортеж из значения суммы за период времени и timestamp (будущий label)
            """
            try:
                pipeline = get_pipeline(current_date=current_date_, next_date=next_date_)
                aggregation_result = await collection.aggregate(pipeline).to_list(1)
                total_value = aggregation_result[0]["total_value"] if aggregation_result else 0
                return total_value, current_date_.isoformat()
            except Exception:
                return 0, current_date_.isoformat()

        start_date, end_date = convert_date_from_str_to_datime(input_data=input_data)
        current_date = start_date

        # мы будем создавать корутины получения записей за промежутки времени (с переданной дельтой в месяц, день или
        # час) пока наша левая граница отрезка проверки не станет больше правой границы, переданной в запросе
        while current_date <= end_date:
            # получаем правую границу в зависимости от переданного group_type
            next_date = get_next_date[input_data["group_type"]](current_date)
            # добавляем корутину в спикок
            values.append(aggregate_data_(current_date, next_date))
            # значение правой границы становится значением левой для следующего запроса
            current_date = next_date

        # выполняем все корутины (как по мне, самый быстрый способ выполнения задачи)
        results = await asyncio.gather(*values)

    except Exception as ex:
        return str(ex)
    finally:
        client.close()

    data_to_send = data_to_json(results=results)

    return data_to_send
