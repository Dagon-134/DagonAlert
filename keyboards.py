from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def turn_timer() -> InlineKeyboardMarkup:
    
    turn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Вкл', callback_data='turnOn')],
            [InlineKeyboardButton(text='Выкл', callback_data='turnOff')]
        ],
        one_time_keyboard=True
    )
    
    return turn