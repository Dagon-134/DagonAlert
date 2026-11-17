from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

from keyboards import turn_timer

from sql import Repo

rt_handler = Router()

from dotenv import load_dotenv
import os

load_dotenv()

bot_url = os.getenv("BOT_TOKEN")
if bot_url is None:
    raise ValueError("Переменная окружения BOT_TOKEN не задана!")
bot = Bot(token=bot_url)

async def send_alert(user_id, text):
    await bot.send_message(
        chat_id=user_id,
        text=f"{text}"
    )

@rt_handler.message(CommandStart())
async def stast_bot(message: Message, repo: Repo):
    if message.from_user is not None:
        await message.answer(text=f'Привет, {message.from_user.first_name}!\n\nРад видеть вас в DagonAlert!\n\nDagonAlert - это TgBot для мониторинга рынка, здесь вы сможите абсолютно бесплатно узнавать о листингах монет, о резком изменение цены монеты, о наличие повышенной волотильности какой-либо монеты.', )
        tg_id = message.from_user.id
        answer = repo.isUserExist(tg_id)
        if answer == False:
            repo.addUser(tg_id)
            print(tg_id)

@rt_handler.message(Command('instructions'))
async def instructions(message: Message):
    await message.answer(text='Интсрукция')


@rt_handler.message(Command('timer'))
async def timer(message: Message):
    await message.answer(text='Что выберите?',
                         reply_markup=turn_timer())
    
@rt_handler.callback_query(F.data == 'turnOn')
async def turn_on_timer(callback: CallbackQuery):
    await callback.answer(text=f'Таймер успешно подключён.\n\nЕсли хотите отключить зайдите обратно в Таймер и там отключите')
    
@rt_handler.callback_query(F.data == 'turnOff')
async def turn_off_timer(callback: CallbackQuery):
    await callback.answer(text=f'Таймер успешно отключён.\n\nЕсли хотите отключить зайдите обратно в Таймер и там подключить')
    