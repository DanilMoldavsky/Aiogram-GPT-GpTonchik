import logging
import sys
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

# from config_reader import config
import conf
from handlers import \
    common, gpt_assist
# from middlewares import \
#     UserInternalIdMiddleware, WeekendCallbackMiddleware, ChatActionMiddleware

# Запуск бота
async def main():
    logging.basicConfig(
        level=logging.INFO,
        
    )

    default = DefaultBotProperties(parse_mode="MarkdownV2")
    bot = Bot(token=conf.TOKEN, default=default)
    dp = Dispatcher(storage=MemoryStorage())
    
    # checkin.router.message.middleware(WeekendCallbackMiddleware())
    
    
    # dp.update.outer_middleware(UserInternalIdMiddleware())
    # dp.callback_query.outer_middleware(WeekendCallbackMiddleware())
    # write_mail.router.message.outer_middleware(ChatActionMiddleware())
    
    # dp.include_router(common.router)
    dp.include_routers(
        common.router, gpt_assist.router
        )
    
    
    # admins = await bot.get_chat_administrators(config.main_chat_id.get_secret_value())
    # admin_ids = {admin.user.id for admin in admins}
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot) # allowed_updates=["message", "inline_query", "chat_member"] , admins=admin_ids


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, 
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S"
    )
    asyncio.run(main())