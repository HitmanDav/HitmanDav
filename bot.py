import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards import get_reply_keyboard, get_inline_keyboard
from states import Form

TOKEN = "6869395577:AAGJP86Zqa-B7T2uxBCbdua_xuTjJEzKtNE"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Выбери кнопку:", reply_markup=get_reply_keyboard())

@dp.message(Command("button"))
async def send_inline_button(message: Message):
    await message.answer("Вот твоя кнопка:", reply_markup=get_inline_keyboard())

@dp.callback_query(F.data == "button_pressed")
async def button_pressed(callback: CallbackQuery):
    await callback.answer("Кнопка нажата")
    await callback.message.answer("Ты большой молодец!")

# Начало анкеты по команде /form
@dp.message(Command("form"))
async def start_form(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Как тебя зовут?")

# Принимаем имя и запрашиваем возраст
@dp.message(StateFilter(Form.name))
async def form_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет?")

# Принимаем возраст и запрашиваем город
@dp.message(StateFilter(Form.age))
async def form_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуй еще раз:")
        return

    await state.update_data(age=int(message.text))
    await state.set_state(Form.city)
    await message.answer("Из какого ты города?")

# Принимаем город и завершаем анкету
@dp.message(StateFilter(Form.city))
async def form_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()

    await message.answer(f"Спасибо за ответы! Вот твоя анкета:\n\n"
                         f"👤 Имя: {data['name']}\n"
                         f"🎂 Возраст: {data['age']}\n"
                         f"🏙️ Город: {data['city']}")
    await state.clear()  # Очищаем состояние после завершения

async def main():
    print("Бот запущен и ждет вашей команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())