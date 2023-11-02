import json
from enum import Enum


class ValidInputData(Enum):
    """
    Класс, который содержит валидные запросы и используется для проверок входных данных
    """
    hour = {"dt_from": "2022-02-01T00:00:00", "dt_upto": "2022-02-02T00:00:00", "group_type": "hour"}
    day = {"dt_from": "2022-10-01T00:00:00", "dt_upto": "2022-11-30T23:59:00", "group_type": "day"}
    month = {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}

    @classmethod
    def get_name_list(cls) -> list[str]:
        return cls.__dict__["_member_names_"]


def validate_input_data(data: str) -> dict | None:
    """
    :param data: текст запроса для проверки
    :return: либо dict, с данными для проверки с валидными запросами, либо None (означает невалидность данных)
    """

    try:
        input_data = json.loads(data)
        if input_data.get("group_type", None) and input_data.get("group_type", None) in ValidInputData.get_name_list():
            valid_data = ValidInputData.__getitem__(name=input_data["group_type"]).value
            if input_data == valid_data:
                return input_data
    except Exception:
        pass
    return None


