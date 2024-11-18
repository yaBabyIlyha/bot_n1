from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

from app.bot import bot

from dotenv import load_dotenv
import os
load_dotenv()

router = Router()

class Registration(StatesGroup):
    name = State()
    how_many = State()
    tg_link = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    kurs = await rq.get_kurs()
    await message.answer(f'Привет!\nАктульальный курс: {kurs}', reply_markup=kb.main)

@router.message(Command('id'))
async def send_user_id(message: Message):
    user_id = message.chat.id
    await message.answer(str(user_id))

@router.callback_query(F.data == 'order')
async def reg_first(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Вы выбрали заполнить заявку')
    await state.set_state(Registration.name)
    await callback.message.answer('Ввведите ваше имя:')

@router.message(Registration.name)
async def reg_second(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registration.how_many)
    await message.answer('Введите кол-во: ')

@router.message(Registration.how_many)
async def second_third(message: Message, state: FSMContext):
    await state.update_data(how_many=message.text)
    await state.update_data(tg_link=message.from_user.username)
    data = await state.get_data()
    await message.answer(f'Заявка сформирована:\n\nВаше имя: {data["name"]}\nКол-во: {data["how_many"]}', reply_markup=kb.second)

@router.callback_query(F.data == 'send')
async def send_order_data(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await rq.set_order(data["name"], data["how_many"], data["tg_link"])
    await callback.message.answer('Заявка отправлена!')
    await callback.answer('')
    notification_status = await rq.get_notification_data()
    if notification_status == 1:
        await bot.send_message(chat_id=os.getenv("SADMIN_ID"), text=(f'Новая заявка!\nИмя: {data["name"]}\nКол-во: {data["how_many"]}\nTG: @{data["tg_link"]}'))
    await state.clear()
