from aiohttp import ClientSession
import asyncio
from telebot.async_telebot import AsyncTeleBot, asyncio_filters
from telebot.types import *
from telebot import asyncio_helper
from datetime import datetime
from config import bot_config

asyncio_helper.proxy = bot_config.proxy
bot = AsyncTeleBot(bot_config.token)
chat_id = bot_config.chat_id

async def send_text_message(text: str):
    await bot.send_message(
        chat_id=chat_id,
        text=text,
    )

def current_time_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@bot.message_handler(commands=['now'])
async def send_current_time(message: Message):
    await bot.reply_to(
        message=message, 
        text=current_time_text(),
    )

async def set_bot_commands():
    await bot.delete_my_commands()
    await bot.set_my_commands(
        commands=[
            BotCommand('now', '获取当前时间'),
            BotCommand('bind', '绑定电表账户'), 
            BotCommand('banance', '获取当前余额'),
            BotCommand('curve24hours', '获取近24小时用电曲线'),
            BotCommand('curve7days', '获取近14天用电曲线'),
        ]
    )



async def main():
    await set_bot_commands()
    await send_text_message(f'KiteBot started at {current_time_text()}!!!')
    bot.add_custom_filter(asyncio_filters.ChatFilter())
    await bot.polling(
        non_stop=True,
        interval=1,
    )
    async with ClientSession(
        base_url='https://bzp.iyunmu.com'
    ) as session:
        response = await session.get(
            url='/prepaid/device/meter',
            params = {'sn': 'YM002272EDA2', 'userid': ''},
        )
        data = await response.json()
        print(data)
        

if __name__ == '__main__':
    asyncio.run(main())