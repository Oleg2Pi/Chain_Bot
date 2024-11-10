import asyncio
import logging
import sys
from os import getenv

from aiogram import Dispatcher, Bot, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from dao import PersonDao, ImagePersonDao, ExecutorDao
from db import Person, ImagePerson, Executor

bot = Bot(token=getenv('BOT_TOKEN'))
dp = Dispatcher()


async def get_profile_photo_bytes(user_id: int) -> bytes | None:
    profile_photo = await bot.get_user_profile_photos(user_id)
    photo_bytes = None

    if profile_photo.total_count > 0:
        large_photo = profile_photo.photos[-1][-1]
        file_id = large_photo.file_id

        file = await bot.get_file(file_id)

        photo = await bot.download_file(file.file_path)
        photo_bytes = photo.read()

    return photo_bytes


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = message.from_user
    profile_photo = await get_profile_photo_bytes(user.id)

    person = await PersonDao.find_by_chat_id(message.chat.id)

    if person is None:
        new_person = Person(
            first_name=user.first_name,
            last_name=user.last_name,
            username_tg=user.username,
            chat_id=message.chat.id,
        )

        try:
            saved_person = await PersonDao.save(new_person)
            image_person = ImagePerson(
                person_id=saved_person.id,
                file=profile_photo,
            )
            await ImagePersonDao.save(image_person)
        except Exception as e:
            logging.error(f"Error saving person or image: {str(e)}")
            await message.answer("Произошла ошибка при сохранении вашего профиля.")
            return

    await message.answer(
        "Нажмите кнопку ниже, чтобы поделиться своим номером телефона:",
        reply_markup=await phone_request_keyboard()
    )


async def phone_request_keyboard():
    contact_button = types.KeyboardButton(text="Поделиться номером", request_contact=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[contact_button]])  # Задаем список кнопок
    return keyboard


@dp.message(F.contact)
async def handle_contact(message: types.Message):
    person = await PersonDao.find_by_chat_id(message.chat.id)
    if person:
        person.phone = message.contact.phone_number
        await PersonDao.update(person.id, person)

    await send_role_selection_message(message.chat.id)


async def send_role_selection_message(chat_id):
    executor_button = types.KeyboardButton(text="Исполнитель")
    customer_button = types.KeyboardButton(text="Заказчик")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[executor_button], [customer_button]])

    await bot.send_message(chat_id, "Выберите вашу роль:", reply_markup=keyboard)


@dp.message(lambda message: message.text in ["Исполнитель", "Заказчик"])
async def handle_role_selection(message: types.Message):
    chat_id = message.chat.id
    if message.text == 'Заказчик':
        await bot.send_message(chat_id, "На данный момент заказчик находится в разработке, доступен исполнитель")
    elif message.text == "Исполнитель":

        person = await PersonDao.find_by_chat_id(chat_id)
        if person:
            try:
                executor = Executor(
                    person_id=person.id,
                )
                await ExecutorDao.save(executor)
            except Exception as e:
                logging.error(f"Error saving person or image: {str(e)}")
                await message.answer("Произошла ошибка при сохранении вашего профиля.")
                return

        await bot.send_message(chat_id, "Ваш профиль создан. Нажмите на кнопку, чтобы перейти в него.")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
