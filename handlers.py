from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

from keyboards import turn_timer, menu

from sql import Repo

rt_handler = Router()

from dotenv import load_dotenv
import os

load_dotenv()

bot_url = os.getenv("BOT_TOKEN")
if bot_url is None:
    raise ValueError("Переменная окружения BOT_TOKEN не задана!")
bot = Bot(token=bot_url)

#Функция для отправки каких либо сообщений всем пользователям
async def send_alert(user_id, text):
    await bot.send_message(
        chat_id=user_id,
        text=f"{text}"
    )

#Старт
@rt_handler.message(CommandStart())
async def stast_bot(message: Message, repo: Repo):
    if message.from_user is not None:
        await message.answer(text=f'👋Привет, {message.from_user.first_name}!\n\nРад видеть вас в DagonAlert!\n\n🔵DagonAlert - это TgBot для мониторинга рынка, здесь вы сможите абсолютно бесплатно узнавать о листингах монет, о резком изменение цены монеты, о наличие повышенной волотильности какой-либо монеты.', )
        tg_id = message.from_user.id
        answer = repo.isUserExist(tg_id)
        if answer == False:
            repo.addUser(tg_id)
            
#Меню
@rt_handler.message(Command('menu'))
async def main_menu(message: Message):
    await message.answer(text='⚙️Вы находитесь в основном меню бота, здесь можете настройть то, что вам хочется⚙️',
                         reply_markup=menu())
    
    
#Инструкция
@rt_handler.message(Command('instructions'))
async def instructions(message: Message):
    await message.answer(text='Интсрукция')
    

#Таймер
@rt_handler.message(F.text == 'Таймер')
async def timer(message: Message):
    await message.answer(text='Что выберите?',
                         reply_markup=turn_timer())
    
@rt_handler.callback_query(F.data == 'turnOn')
async def turn_on_timer(callback: CallbackQuery, repo: Repo):
    await callback.answer(text=f'Таймер успешно подключён.\n\nЕсли хотите отключить зайдите обратно в Таймер и там отключите')
    tg_id = callback.from_user.id
    print(tg_id)
    new_cust = True
    repo.changeTimerImformation(new_cust, tg_id)
    
@rt_handler.callback_query(F.data == 'turnOff')
async def turn_off_timer(callback: CallbackQuery, repo: Repo):
    await callback.answer(text=f'Таймер успешно отключён.\n\nЕсли хотите отключить зайдите обратно в Таймер и там подключить')
    tg_id = callback.from_user.id
    print(tg_id)
    new_cust = False
    repo.changeTimerImformation(new_cust, tg_id)
    
    
@rt_handler.message(Command('get_volatility'))
async def get_volatility(message: Message):
    print('начал')
    m = await message.answer(text='Подождите пару секунд...')