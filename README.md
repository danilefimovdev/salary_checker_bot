<h1>Тестовое задание RLT</h1>
    <p>Стек: Python3, Asyncio, MongoDB, AIOGRAM</p>
    <h2>Описание задачи:</h2>
    <p>Написание алгоритма агрегации статистических данных о зарплатах сотрудников компании по временным промежуткам. Алгоритм принимает на вход:</p>
    <ul>
        <li>Дату и время старта агрегации в ISO формате (далее dt_from)</li>
        <li>Дату и время окончания агрегации в ISO формате (далее dt_upto)</li>
        <li>Тип агрегации (далее group_type). Типы агрегации могут быть следующие: hour, day, month. То есть группировка всех данных за час, день, неделю, месяц.</li>
    </ul>
    <h3>Пример входных данных:</h3>
    <pre>
        {
            "dt_from":"2022-09-01T00:00:00",
            "dt_upto":"2022-12-31T23:59:00",
            "group_type":"month"
        }
    </pre>
    <p>На выходе алгоритм формирует ответ содержащий:</p>
    <ul>
        <li>Агрегированный массив данных (далее dataset)</li>
        <li>Подписи к значениям агрегированного массива данных в ISO формате (далее labels)</li>
    </ul>
    <h3>Пример ответа:</h3>
    <pre>
        {
            "dataset": [5906586, 5515874, 5889803, 6092634],
            "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]
        }
    </pre>
    <p>Помимо разработки алгоритма агрегации, необходимо создать телеграм бота, который будет принимать от пользователей текстовые сообщения содержащие JSON с входными данными и отдавать агрегированные данные в ответ.</p>
