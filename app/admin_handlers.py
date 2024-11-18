from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

from dotenv import load_dotenv
import os
load_dotenv()

admin_router = Router()

class Val(StatesGroup):
    kurs_val = State()

@admin_router.message(Command('admin'))
async def admin_panel(message: Message):
    
    if await rq.is_admin(message.chat.id):
        await message.answer('admin panel', reply_markup=kb.admin)
    else:
        await message.answer('У вас нет прав доступа!')

@admin_router.message(Command('add_admin'))
async def add_admin(message: Message):
    args = message.text.split()
    new_admin = int(args[1])
    if message.chat.id == os.getenv("SADMIN_ID"):
        await rq.new_admin(new_admin)
        await message.answer('Новый админ успешно добавлен!')
    
@admin_router.callback_query(F.data == 'change_kurs')
async def change_first(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали - сменить курс')
    await state.set_state(Val.kurs_val)
    await callback.message.answer('Введите желаемый курс: ')

@admin_router.message(Val.kurs_val)
async def change_second(message: Message, state: FSMContext):
    await state.update_data(kurs_val=message.text)
    data = await state.get_data()
    await rq.set_kurs(data["kurs_val"])
    new_kurs = await rq.get_kurs()
    await message.answer(f'Курс обновлен в бд\nНовое значение: {new_kurs}')
    await state.clear()

@admin_router.callback_query(F.data == 'notifications')
async def notifications_first(callback: CallbackQuery):
    await callback.message.edit_reply_markup('', kb.k_notifications)

@admin_router.callback_query(F.data == 'menu_admin')
async def main_admin_menu(Callback: CallbackQuery):
    await Callback.message.edit_text('admin panel')
    await Callback.message.edit_reply_markup('', kb.admin)

@admin_router.callback_query(F.data == 'kurs')
async def change_second(callback: CallbackQuery):
    kurs = await rq.get_kurs()
    await callback.message.edit_text(f'Сейчас курс: {kurs}')
    await callback.message.edit_reply_markup('', kb.k_kurs)

@admin_router.callback_query(F.data == 'admin_orders')
async def orders_first(callback: CallbackQuery):
    await callback.message.edit_text('admin panel')
    await callback.message.edit_reply_markup('', kb.k_orders)

@admin_router.callback_query(F.data == 'help')
async def help_first(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('@yababyilyha', reply_markup=kb.admin)

@admin_router.callback_query(F.data == 'notifications_on')
async def notifications_on(callback: CallbackQuery):
    await callback.answer('')
    await rq.set_notification_data(1)
    await callback.message.edit_text('Уведомления включенны', reply_markup=kb.k_notifications)

@admin_router.callback_query(F.data == 'notifications_off')
async def notifications_off(callback: CallbackQuery):
    await callback.answer('')
    await rq.set_notification_data(0)
    await callback.message.edit_text('Уведомления выключенны', reply_markup=kb.k_notifications)

@admin_router.callback_query(F.data == 'show_all_orders')
async def send_all_orders(callback: CallbackQuery):
    await callback.answer('')
    id = callback.message.chat.id
    await rq.send_all_orders(id)

class f_by_id(StatesGroup):
    id = State()

@admin_router.callback_query(F.data == 'find_by_id')
async def find_by_id(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.clear()
    await callback.message.edit_text('Напишите ID для поиска', reply_markup=kb.k_orders)
    await state.set_state(f_by_id.id)

@admin_router.message(f_by_id.id)
async def second_find_by_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()
    a_id = message.chat.id
    o_id = data["id"]
    await rq.find_order_by_id(int(o_id), a_id)
    await state.clear()

class d_by_id(StatesGroup):
    id = State()


@admin_router.callback_query(F.data == 'delete_by_id')
async def delete_order_by_id(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(d_by_id.id)
    await callback.message.edit_text('Напишите ID для удаления', reply_markup=kb.k_orders)

@admin_router.message(d_by_id.id)
async def second_delete_order_by_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    data = await state.get_data()
    a_id = message.chat.id
    o_id = int(data["id"])
    await rq.delete_order_by_id(o_id, a_id)
    await state.clear()

