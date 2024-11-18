from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оставить заявку', callback_data='order')]
])

second = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить', callback_data='send')],
    [InlineKeyboardButton(text='Изменить', callback_data='order')]
])

admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Обработка заявок', callback_data='admin_orders'),  InlineKeyboardButton(text='Уведомления', callback_data='notifications')],
    [InlineKeyboardButton(text='Курс', callback_data='kurs'), InlineKeyboardButton(text='Поддержка', callback_data='help')]
])

k_notifications = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Включить', callback_data='notifications_on'), InlineKeyboardButton(text='Выключить', callback_data='notifications_off')],
    [InlineKeyboardButton(text='На главную', callback_data='menu_admin')]
])

k_kurs = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сменить курс', callback_data='change_kurs'), InlineKeyboardButton(text='На главную', callback_data='menu_admin')]
])

k_orders = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Все заявки', callback_data='show_all_orders'), InlineKeyboardButton(text='Найти по ID', callback_data='find_by_id')],
    [InlineKeyboardButton(text='Удалить по ID', callback_data='delete_by_id'), InlineKeyboardButton(text='На главную', callback_data='menu_admin')]
])