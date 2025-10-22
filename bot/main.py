import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from decouple import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
WEBHOOK_URL = config('TELEGRAM_WEBHOOK_URL', default='')
WEBHOOK_PATH = '/webhook'
WEBAPP_URL = config('WEBAPP_URL', default='http://localhost:3000')

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    """Handle /start command."""
    user = message.from_user
    
    # Welcome message
    welcome_text = f"""
🎓 Добро пожаловать в GOdrive!

Приложение для подготовки к теоретическому экзамену на водительские права в Армении.

👋 Привет, {user.first_name}!

Вы можете:
• 📚 Изучать билеты в режиме обучения
• 🧪 Проходить тестирование
• 📊 Просматривать свою статистику
• ⚙️ Настраивать профиль

Нажмите кнопку ниже, чтобы открыть приложение:
    """
    
    # Create keyboard with WebApp button
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Открыть приложение",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )
    
    await message.answer(welcome_text, reply_markup=keyboard)


@dp.message(Command('help'))
async def help_command(message: types.Message):
    """Handle /help command."""
    help_text = """
🆘 Справка по использованию бота:

/start - Начать работу с ботом
/help - Показать эту справку
/app - Открыть веб-приложение

📱 Веб-приложение включает:
• Режим обучения - изучение билетов с объяснениями
• Режим тестирования - проверка знаний
• Статистика - ваш прогресс и результаты
• Настройки - персональные предпочтения

❓ Если у вас есть вопросы, обратитесь к администратору.
    """
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Открыть приложение",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )
    
    await message.answer(help_text, reply_markup=keyboard)


@dp.message(Command('app'))
async def app_command(message: types.Message):
    """Handle /app command."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Открыть приложение",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )
    
    await message.answer("Нажмите кнопку ниже, чтобы открыть веб-приложение:", reply_markup=keyboard)


@dp.message()
async def handle_message(message: types.Message):
    """Handle other messages."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Открыть приложение",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )
    
    await message.answer(
        "Используйте команды или нажмите кнопку для открытия приложения:",
        reply_markup=keyboard
    )


async def on_startup():
    """Bot startup actions."""
    logger.info("Bot is starting up...")
    
    if WEBHOOK_URL:
        # Set webhook
        webhook_url = f"{WEBHOOK_URL}{WEBHOOK_PATH}"
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    else:
        logger.info("Running in polling mode")


async def on_shutdown():
    """Bot shutdown actions."""
    logger.info("Bot is shutting down...")
    
    if WEBHOOK_URL:
        # Remove webhook
        await bot.delete_webhook()
        logger.info("Webhook removed")


def create_app():
    """Create aiohttp application for webhook."""
    app = web.Application()
    
    # Setup webhook handler
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    # Setup application
    setup_application(app, dp, bot=bot)
    
    return app


async def main():
    """Main function."""
    if WEBHOOK_URL:
        # Run with webhook
        app = create_app()
        
        # Start web server
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 8080)
        await site.start()
        
        logger.info("Bot is running with webhook on port 8080")
        
        # Keep running
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            await runner.cleanup()
    else:
        # Run in polling mode
        await on_startup()
        
        try:
            await dp.start_polling(bot)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            await on_shutdown()


if __name__ == '__main__':
    asyncio.run(main())

