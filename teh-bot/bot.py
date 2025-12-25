import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import CommandStart
from aiogram.enums import ParseMode
from database import db

load_dotenv('.env')
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8044141716:AAFwbbi6o6hnHkXGpik7lwEuzZtTjBxC4N4") 
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    db.register_user(str(message.from_user.id), 'student')
    await message.answer(
        "*Добро пожаловать в университетского бота!*\n"
        "/homework — посмотреть домашние задания.\n"
        "/lectures — просмотреть доступные лекции.",
        parse_mode=ParseMode.MARKDOWN_V2
    )

@dp.message(F.text.startswith('/homework'))
async def show_homework(message: types.Message):
    homeworks = db.get_homeworks()
    text = '*Домашние задания:*\n'
    for hw in homeworks:
        text += f'\n_{hw[1]}_\nСрок сдачи: `{hw[3]}`\nОписание: {hw[2]}\n'
    await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2)

@dp.message(F.text.startswith('/lectures'))
async def show_lectures(message: types.Message):
    lectures = db.get_lectures()
    text = '*Доступные лекции:*\n'
    for lec in lectures:
        text += f'\n_{lec[1]}_, Дата: `{lec[3]}`\nКонтент: {lec[2]}\n'
    await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2)

@dp.message(F.text.startswith('/add_hw'))
async def add_homework(message: types.Message):
    args = message.get_args().split('|')
    if len(args) != 3:
        await message.answer('*Формат добавления домашнего задания:* `/add_hw Название|Описание|Срок сдачи`', parse_mode=ParseMode.MARKDOWN_V2)
        return
    title, desc, deadline = args
    db.add_homework(title.strip(), desc.strip(), deadline.strip())
    await message.answer(f'*Задание "{title}" успешно добавлено!*', parse_mode=ParseMode.MARKDOWN_V2)

@dp.message(F.text.startswith('/delete_hw'))
async def delete_homework(message: types.Message):
    hw_id = int(message.get_args())
    db.delete_homework(hw_id)
    await message.answer(f'*Задание с ID={hw_id} удалено!*', parse_mode=ParseMode.MARKDOWN_V2)

@dp.message(F.text.startswith('/update_hw'))
async def update_homework(message: types.Message):
    args = message.get_args().split('|')
    if len(args) != 4:
        await message.answer('*Формат обновления задания:* `/update_hw ID|Название|Описание|Срок сдачи`', parse_mode=ParseMode.MARKDOWN_V2)
        return
    hw_id, title, desc, deadline = args
    db.update_homework(int(hw_id), title.strip(), desc.strip(), deadline.strip())
    await message.answer(f'*Задание с ID={hw_id} обновлено!*', parse_mode=ParseMode.MARKDOWN_V2)

@dp.message(F.text.startswith('/add_lec'))
async def add_lecture(message: types.Message):
    args = message.get_args().split('|')
    if len(args) != 3:
        await message.answer('*Формат добавления лекции:* `/add_lec Название|Содержание|Дата`', parse_mode=ParseMode.MARKDOWN_V2)
        return
    title, content, date = args
    db.add_lecture(title.strip(), content.strip(), date.strip())
    await message.answer(f'*Лекция "{title}" успешно добавлена!*', parse_mode=ParseMode.MARKDOWN_V2)

@dp.message(F.text.startswith('/delete_lec'))
async def delete_lecture(message: types.Message):
    lec_id = int(message.get_args())
    db.delete_lecture(lec_id)
    await message.answer(f'*Лекция с ID={lec_id} удалена!*', parse_mode=ParseMode.MARKDOWN_V2)

if __name__ == '__main__':
    dp.run_polling(bot)