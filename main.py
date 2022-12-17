import bot
import asyncio
import fetch
from datetime import timedelta
import schedule
import threading

def run_loop():
    def fetch_data():
        print('刷新数据')
        fetch.get_last()
    fetch_data()
    schedule.clear()
    schedule.every(30).minutes.do(fetch_data)
    while True:
        schedule.run_pending()

t = threading.Thread(target=run_loop)
t.daemon = True
t.start()

if __name__ == '__main__':
    asyncio.run(bot.main())