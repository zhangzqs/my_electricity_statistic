from aiohttp import ClientSession
import asyncio
from telebot.async_telebot import AsyncTeleBot, asyncio_filters
from telebot.types import *
from telebot import asyncio_helper
from datetime import datetime
from config import config
import fetch


asyncio_helper.proxy = config.proxy
bot = AsyncTeleBot(config.token)
chat_id = config.chat_id

async def send_text_message(text: str):
    await bot.send_message(
        chat_id=chat_id,
        text=text,
    )

def current_time_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@bot.message_handler(commands=['now'])
async def now(message: Message):
    await bot.reply_to(
        message=message, 
        text=current_time_text(),
    )

@bot.message_handler(commands=['balance'])
async def balance(message: Message):
    b = fetch.get_last()
    await bot.reply_to(
        message=message, 
        text=f'刷新时间: {str(b.ts)}\n当前余额: {b.balance}',
    )

@bot.message_handler(commands=['curve24hours'])
async def curve24hours(message: Message):
    with fetch.draw_recently_by_cnt(24) as f:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=f,
        )

@bot.message_handler(commands=['curve7days'])
async def curve7days(message: Message):
    with fetch.draw_recently_by_cnt(7*24) as f:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=f,
        )

async def set_bot_commands():
    await bot.delete_my_commands()
    await bot.set_my_commands(
        commands=[
            BotCommand('now', '获取当前时间'),
            BotCommand('balance', '获取当前余额'),
            BotCommand('curve24hours', '获取近24小时用电曲线'),
            BotCommand('curve7days', '获取近14天用电曲线'),
        ]
    )

async def main():
    await set_bot_commands()
    await send_text_message(f'KiteBot started at {current_time_text()}!!!')
    bot.add_custom_filter(asyncio_filters.ChatFilter())
    await bot.polling(non_stop=True)
