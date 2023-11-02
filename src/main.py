import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from src.algorithm import aggregate_data_by_time_period
from src.config import TOKEN
from constants import ERROR_TEXT
from validators import validate_input_data


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    """
    Приветствует пользователя как бот из тз
    """
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    user_profile_link = f'<a href="tg://user?id={user_id}">{user_name}</a>'

    await message.answer(f'Hi {user_profile_link}!', parse_mode=ParseMode.HTML)


@dp.message()
async def handle_message(message: types.Message):
    """
    Валидирует данные из переданного сообщения пользователя и если они валидны (это один из json запросов),
    то генерирует данные и возвращает их пользователю. В ином случае, возвращает текст ошибки.
    """
    if message.text:
        validated_data = validate_input_data(message.text)
        if validated_data:
            result = await aggregate_data_by_time_period(input_data=validated_data)
        else:
            result = ERROR_TEXT
    else:
        result = ERROR_TEXT
    await bot.send_message(
        text=result,
        chat_id=message.chat.id)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
