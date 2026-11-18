from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def menu() -> ReplyKeyboardMarkup:
    
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Таймер')],
            [KeyboardButton(text='Настройка бирж')], 
            [KeyboardButton(text='Настройка алертов')]
        ],
        one_time_keyboard=True, resize_keyboard=True
    )
    
    return menu

def turn_timer() -> InlineKeyboardMarkup:
    
    turn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Вкл', callback_data='turnOn')],
            [InlineKeyboardButton(text='Выкл', callback_data='turnOff')]
        ],
        one_time_keyboard=True
    )
    
    return turn