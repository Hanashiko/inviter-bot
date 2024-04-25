from aiogram import executor, Dispatcher, Bot, types
from config import *
from datetime  import datetime, timedelta

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)

async def on_startup(_):
    print("Бот запущений!")
    
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.reply("Привіт, я бот для генерації посилань.")
    
@dp.message_handler(commands=['get_id'])
async def command_get_id(message:types.Message):
    await message.reply(f"Chat ID - {message.chat.id}\nUser ID - {message.from_user.id}")   

@dp.message_handler(commands=['link'])
async def command_link(message:types.Message):
    if message.from_user.id == ADMIN_ID:
        link = await bot.create_chat_invite_link(chat_id=CHAT_ID, creates_join_request=True)
        expire_date = datetime.now() + timedelta(days=1,hours=12)
        link = await bot.create_chat_invite_link(chat_id=CHAT_ID, name=message.get_args(), member_limit=1, expire_date=expire_date)
        await message.reply(link.invite_link)

@dp.message_handler(commands=['delete_link'])
async def comamnd_delete_link(message:types.Message):
    if message.from_user.id == ADMIN_ID:
        invite_link = message.get_args()
        await bot.revoke_chat_invite_link(chat_id=CHAT_ID, invite_link=invite_link)
        await message.reply(f"Deleted link - {invite_link}")

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=False, on_startup=on_startup)
