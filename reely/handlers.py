import asyncio
import os
from pathlib import Path
from aiogram import F, Bot, Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery, FSInputFile, ChatJoinRequest
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from reely.classes import InstagramDownloader
import reely.keyboards as kb
from config import USERNAME, PASSWORD, CHANNEL_ID, CHANNEL_LINK, TOKEN

bot = Bot(token=TOKEN)
router = Router()
downloader = InstagramDownloader(USERNAME, PASSWORD)
INSTAGRAM_URL_REGEX = r"(https?:\/\/)?(www\.)?instagram\.com\/(reel|p)\/[\w-]+\/?"
download_dir = Path("downloads")
pending_requests = set()

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

async def subscription_check(user, msg: Message) -> bool:
    if await is_subscribed(user):
        return True
    elif user in pending_requests:
        return True
    else:
        await msg.answer(f"Subscribe first: {CHANNEL_LINK}", reply_markup=kb.subscribe_channel)
        return False

@router.chat_join_request()
async def handle_join_request(update: ChatJoinRequest):
    pending_requests.add(update.from_user.id)

@router.message(CommandStart())
async def start(message: Message):
    if not await subscription_check(message.from_user.id, message):
        return
    await message.answer("Hello the bot is working")

@router.callback_query(F.data == "subchek")
async def subchek(callback: CallbackQuery, message: Message):
    if not await subscription_check(message.from_user.id, message):
        await callback.answer("Your not subscribed yet")
        return
    await callback.answer("Your are okay to go")

@router.message(F.text.regexp(INSTAGRAM_URL_REGEX))
async def handle_instagram_reel(message: Message):
    if not await subscription_check(message.from_user.id, message):
        return
    await message.reply("✅ Instagram post detected! Processing...")
    file_path = downloader.download_single_post(url=message.text, id=message.from_user.id)
    
    for file in download_dir.iterdir():
        if file.suffix == ".mp4":
            reel = FSInputFile(str(file), filename=file.name)
            await message.answer_video(video=reel, caption="📥 Downloaded via @ReelyFastBot")
            file.unlink()
        elif file.suffix == ".txt":
            file.unlink()
        elif file.suffix == ".jpg":
            img = FSInputFile(str(file), filename=file.name)
            await message.answer_photo(img, caption="here is your image")
            file.unlink()

@router.message()
async def catch_all(message: Message):
    if not await subscription_check(message.from_user.id, message):
        return
    await message.answer("Pls send instagram url/link")
