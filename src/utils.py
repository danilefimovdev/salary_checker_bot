import datetime
import json


def get_next_date_of_next_month(current_date: datetime.datetime) -> datetime.datetime:
    """
    :param current_date: текущая используемая дата (левая граница)
    :return: возвращает правую границу при использовании group_type = month
    """
    next_month = current_date.replace(day=1).month + 1
    next_year = current_date.year if next_month <= 12 else current_date.year + 1
    next_month = next_month if next_month <= 12 else 1
    first_day_of_next_month = datetime.datetime(next_year, next_month, 1)
    return first_day_of_next_month


# словарь функций
get_next_date = {
    'hour': lambda current_date: current_date + datetime.timedelta(hours=1),
    'day': lambda current_date: current_date + datetime.timedelta(days=1),
    'month': get_next_date_of_next_month,
}


def get_pipeline(current_date: datetime.datetime, next_date: datetime.datetime) -> list:
    """
    :param current_date: дата, которая будет левой границей
    :param next_date: дата, которая будет правой границей
    :return: возвращает pipeline (фильтр запроса) для использования в запросе к бд
    """
    pipeline = [
        {
            "$match": {
                "dt": {
                    "$gte": current_date,
                    "$lt": next_date
                }
            }
        },
        {
            "$group": {
                "_id": str(current_date),
                "total_value": {"$sum": "$value"}
            }
        }
    ]
    return pipeline


def convert_date_from_str_to_datime(input_data: dict) -> tuple[datetime.datetime, datetime.datetime]:
    """
    :param input_data: строковые данные в iso формате для перевода в объекты datetime
    :return: два объекта datetime (лквая и правая границы считывания записей в бд)
    """
    start_date = datetime.datetime.fromisoformat(input_data["dt_from"])
    end_date = datetime.datetime.fromisoformat(input_data["dt_upto"])
    return start_date, end_date


def data_to_json(results: tuple) -> str:
    """
    Возвращает данные в json формате для отправки пользователю
    """
    jsoned = json.dumps(
        {"dataset": [result[0] for result in results], "labels": [result[1] for result in results]})
    return jsoned
