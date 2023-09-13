from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from django.contrib.auth import authenticate
import os
import django
from asgiref.sync import sync_to_async  # Импортируем sync_to_async

# Устанавливаем настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyCafe.settings")
django.setup()

# Ваш токен бота
BOT_TOKEN = '6517353437:AAHcX0XYuv1Iph96lxjwWslrHoxkwECtLRY'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()  # Подключение MemoryStorage
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


class UserLogin(StatesGroup):
    login = State()
    password = State()
    waiting_for_start = State()  # Новое состояние для ожидания начала


# Оборачиваем функцию аутентификации с помощью sync_to_async
async_authenticate = sync_to_async(authenticate)


# Асинхронная функция для отправки уведомления
async def send_telegram_message(chat_id, message_text):
    await bot.send_message(chat_id, message_text)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    # Переводим пользователя в состояние ожидания начала
    await UserLogin.waiting_for_start.set()

    keyboard = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Начать", callback_data="start")
    keyboard.add(start_button)
    await message.answer("Привет! Я бот для вашего кафе. Чтобы начать, нажмите кнопку 'Начать'.", reply_markup=keyboard)


# Обработчик кнопки "Начать"
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'start', state=UserLogin.waiting_for_start)
async def start_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()

    # Переводим пользователя в состояние ввода логина
    await UserLogin.login.set()
    await bot.send_message(callback_query.message.chat.id, "Для входа введите свой логин:")


# Обработчик логина
@dp.message_handler(state=UserLogin.login)
async def process_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text

    await message.answer("Теперь введите свой пароль:")
    await UserLogin.next()


# Обработчик пароля
@dp.message_handler(state=UserLogin.password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text

    # Проверяем логин и пароль в соответствии с базой данных Django
    user = await async_authenticate(username=data['login'], password=data['password'])

    if user:
        user.telegram_chat_id = message.chat.id

        # Выполняем сохранение пользователя в синхронном режиме
        await sync_to_async(user.save)()

        await message.answer("Вы успешно вошли. Ваш чат ID был сохранен.")
    else:
        await message.answer("Неверный логин или пароль. Попробуйте снова.")

    # Сброс состояния
    await state.finish()

    # Обработчик текстовых сообщений
    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def on_text(message: types.Message):
        chat_id = message.chat.id
        user_message = message.text

        # Здесь можно добавить логику обработки заказа и отправки уведомления
        await send_telegram_message(chat_id, user_message)

        # Добавьте логирование для отслеживания chat_id
        print(f"Received message from chat_id {chat_id}: {user_message}")


class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **options):
        from aiogram import executor
        executor.start_polling(dp, skip_updates=True)
