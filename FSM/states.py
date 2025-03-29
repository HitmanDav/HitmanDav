from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    name = State()       # Состояние ожидания имени
    age = State()        # Состояние ожидания возраста
    city = State()       # Состояние ожидания города