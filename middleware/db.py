from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware


import conf
import asyncio
import asyncpg

class DbMiddleware(BaseMiddleware):
    def __init__(self, pool):
        super(DbMiddleware, self).__init__()
        self.pool = pool

    async def on_process_message(self, message: types.Message, data: dict):
        data['pool'] = self.pool
        data['db'] = await self.pool.acquire()

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        data['pool'] = self.pool
        data['db'] = await self.pool.acquire()

    async def on_post_process_message(self, message: types.Message, data_from_handler: list, data: dict):
        db = data.get('db')
        if db:
            await self.pool.release(db)

    async def on_post_process_callback_query(self, callback_query: types.CallbackQuery, data_from_handler: list, data: dict):
        db = data.get('db')
        if db:
            await self.pool.release(db)

async def create_pool():
    return await asyncpg.create_pool(dsn='postgresql://user:password@host:port/database')

if __name__ == '__main__':
    bot = Bot(token=conf.TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    
    # dp.middleware.setup(LoggingMiddleware())
    
    loop = asyncio.get_event_loop()
    db_pool = loop.run_until_complete(create_pool())
    dp.middleware.setup(DbMiddleware(db_pool))

