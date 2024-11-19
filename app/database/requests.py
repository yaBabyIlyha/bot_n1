from app.database.models import async_session
from app.database.models import User, Order, Kurs, Notifications, Admin
from sqlalchemy import select
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.bot import bot

class Order_info(StatesGroup):
    id = State()
    name = State()
    how_many = State()
    tg_link = State()

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_order(name, how_many, tg_link):
    async with async_session() as session:
        session.add(Order(name=name, how_many=how_many, tg_link=tg_link))
        await session.commit()

async def set_kurs(number):
    async with async_session() as session:
        result = await session.execute(select(Kurs).filter(Kurs.id == 1))
        kurs = result.scalar_one_or_none()

        if kurs:
            kurs.number = number
            await session.commit()

async def get_kurs():
    async with async_session() as session:
        result = await session.execute(select(Kurs).filter(Kurs.id == 1))
        kurs = result.scalar_one_or_none()

        if kurs:
            return kurs.number       
        

async def set_notification_data(number):
    async with async_session() as session:
        result = await session.execute(select(Notifications).filter(Notifications.id == 1))
        data = result.scalar_one_or_none()

        if data:
            data.on_off = number
            await session.commit()

async def get_notification_data():
    async with async_session() as session:
        result = await session.execute(select(Notifications).filter(Notifications.id == 1))
        data = result.scalar_one_or_none()

        if data:
            return data.on_off
        
async def send_all_orders(admin_id):
    async with async_session() as session:
        result = await session.execute(select(Order))
        data = result.scalars().all()

        if not data:
            await bot.send_message(chat_id=admin_id, text='Нет заявок!')
            return
        
        for order in data:
            await bot.send_message(
                chat_id=admin_id,
                text=(
                    f'ID: {order.id}\n'
                    f'Имя: {order.name}\n'
                    f'Кол-во {order.how_many}\n'
                    f'TG: @{order.tg_link}'
                )
            )

        await bot.send_message(chat_id=admin_id, text='Все заявки успешно отправленны!')

async def find_order_by_id(id, admin_id):
    async with async_session() as session:
        result = await session.execute(select(Order).filter(Order.id == id))
        data = result.scalar_one_or_none()

        if data:
            await bot.send_message(
                chat_id=admin_id,
                text=(
                    f'ID: {data.id}\n'
                    f'Имя: {data.name}\n'
                    f'Кол-во {data.how_many}\n'
                    f'TG: @{data.tg_link}'
                )
            )
        else: 
            await bot.send_message(chat_id=admin_id, text='Нет такого ID!')
            

async def delete_order_by_id(id, admin_id):
    async with async_session() as session:
        result = await session.execute(select(Order).filter(Order.id == id))
        data = result.scalar_one_or_none()
        if data:
            await session.delete(data)
            await session.commit()

            await bot.send_message(chat_id=admin_id, text=f'Заявка с ID: {id} успешно удалена!')
        
        else:
            await bot.send_message(chat_id=admin_id, text=f'Заявка с ID: {id} не найдена!')

async def is_admin(chat_id):
    async with async_session() as session:
        result = await session.execute(select(Admin).filter(Admin.admin_id == chat_id))
        data = result.scalar_one_or_none()

        if data:
            return True
        return False
    
async def new_admin(chat_id):
    async with async_session() as session:
        result = await session.execute(select(Admin).filter(Admin.admin_id == chat_id))
        
        n_admin  = Admin(admin_id=chat_id)
        session.add(n_admin)
        await session.commit()