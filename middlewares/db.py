from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject, Message

from utilities import Utilities

import conf
import asyncio
import asyncpg

class DbMiddleware(BaseMiddleware):
    def __init__(self, pool):
        super(DbMiddleware, self).__init__()
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:  # pragma: no cover
        """
        Execute middleware

        :param handler: Wrapped handler in middlewares chain
        :param event: Incoming event (Subclass of :class:`aiogram.types.base.TelegramObject`)
        :param data: Contextual data. Will be mapped to handler arguments
        :return: :class:`Any`
        """
        await self.on_process_message(event, data)
        #todo разобраться с аргументами
        await self.on_post_process_callback_query(event, [], data)
        result = await handler(event, data)
        await self.on_post_process_message(event, [], data)
        await self.on_post_process_callback_query(event, [], data)

    async def on_process_message(self, message: types.Message, data: dict):
        data['pool'] = self.pool
        # data['db'] = await self.pool.acquire()
        
        query = "SELECT * FROM city WHERE countrycode = 'USA';"
        execute = await data['pool'].fetch(query)
        # response_pql = await data['db'].execute(query)
        
        # valid_response = await data['db'].fetchall()
        # print(valid_response)
        data['response'] = Utilities.escape_markdown_v2(str(execute[0]['id']))
        # data['response'] = await data['db'].execute(query)
        # data['response'] = await data['response'].fetchrow()#.fetchone()[0]

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
    return await asyncpg.create_pool(dsn=conf.POSTGRES)


if __name__ == '__main__':
    bot = Bot(token=conf.TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    
    # dp.middleware.setup(LoggingMiddleware())
    
    loop = asyncio.get_event_loop()
    db_pool = loop.run_until_complete(create_pool())
    dp.middleware.setup(DbMiddleware(db_pool))

