import asyncio
import os
import shutil
from random import randint
from aiogram import F, Bot, Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery, FSInputFile, ChatJoinRequest
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import reely.keyboards as kb
import database.requests as rq
import instaloader
import re
import uuid
from datetime import datetime
from config import CHANNEL_ID, CHANNEL_LINK, TOKEN
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

bot = Bot(token=TOKEN)
executor = ThreadPoolExecutor(max_workers=5)

fact_list = [
    "🔥 Instagram boasts over 2 billion monthly active users.",
    "📸 High-quality visuals drive engagement.",
    "🗓️ Consistent posting keeps you visible.",
    "⚙️ Engagement fuels the algorithm.",
    "📖 Stories offer direct audience connection.",
    "🎥 Video content often outperforms images.",
    "🎬 Reels can dramatically increase reach.",
    "🙌 User-generated content builds credibility.",
    "🔍 Smart hashtag use boosts discoverability.",
    "🎯 Instagram ads allow precise targeting.",
    "👤 A clear bio converts visitors into followers.",
    "📚 Carousel posts capture more attention.",
    "📊 Analytics reveal what truly works.",
    "🛒 Instagram Shopping simplifies product sales.",
    "🤝 Influencer collaborations extend your audience.",
    "📝 Captions matter—be clear and compelling.",
    "⏰ Posting at peak times maximizes views.",
    "💡 Leverage various formats to keep content fresh.",
    "📍 Location tags attract local audiences.",
    "🔄 Regular testing refines your strategy.",
    "Instagram has over 2 billion monthly active users! 🌍",
    "The first Instagram post was a photo of a dog and a taco stand! 🐶🌮",
    "The most-liked post on Instagram is the photo of an egg! 🥚",
    "Instagram Stories are used by 500 million people daily! 📸",
    "The most popular hashtag on Instagram is #Love! ❤️",
    "Instagram was launched on October 6, 2010! 🎉",
    "The average user spends 30 minutes per day on Instagram! ⏳",
    "70% of Instagram users are under the age of 35! 👶",
    "Instagram is the second most downloaded free app on the App Store! 📱",
    "The most-followed account on Instagram is Instagram itself! 📈",
    "Over 95 million photos and videos are shared on Instagram daily! 🖼️",
    "Instagram Reels are watched by 45% of users weekly! 🎥",
    "The most-used filter on Instagram is Clarendon! 🌟",
    "Instagram's algorithm prioritizes content based on user engagement! 💬",
    "Businesses share 80% of their Instagram posts as photos! 📷",
    "The most popular emoji on Instagram is the heart emoji! ❤️",
    "Instagram influencers can earn up to $1 million per post! 💰",
    "The average Instagram post gets 10.7 hashtags! #️⃣",
    "Instagram ads reach over 1.2 billion people monthly! 📣",
    "The most popular time to post on Instagram is Wednesday at 11 AM! ⏰",
]

greeting_message = '''
Need to save an Instagram post? Just send the link, and I'll get it for you in seconds!

📌 What can I download?
✔️ Reels
✔️ Videos
✔️ Photos
✔️ Carousels

🚀 How to use:
1️⃣ Copy the Instagram post link 📋
2️⃣ Paste it here and send it 📩
3️⃣ Get your media instantly! 🎉

Let’s go—send me a link! 🎬🔥'''

router = Router()
INSTAGRAM_URL_REGEX = r"(https?:\/\/)?(www\.)?instagram\.com\/(reel|p)\/[\w-]+\/?"
pending_requests = set()

async def extract_shortcode(url):
    """
    Extract shortcode from various Instagram URL formats.
    """
    patterns = [
        r'/(?:p|reel)/([A-Za-z0-9_-]+)',  # Matches both /p/ and /reel/
        r'shortcode=([A-Za-z0-9_-]+)',     # Matches shortcode parameter
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Could not extract shortcode from URL")

def sync_download_single_post(url, id):
    """Synchronously download an Instagram post."""
    try:
        # Create a new Instaloader instance for each download (public posts assumed)
        L = instaloader.Instaloader(
            download_comments=False,
            save_metadata=False,
            download_video_thumbnails=False,
            filename_pattern="{shortcode}"
        )
        shortcode_match = re.search(r'/(?:p|reel)/([A-Za-z0-9_-]+)', url)
        if not shortcode_match:
            raise ValueError("Could not extract shortcode from URL")
        shortcode = shortcode_match.group(1)
        # Create a unique download directory using pathlib (Linux-friendly)
        download_dir = Path("downloads") / f"{id}_{shortcode}_{uuid.uuid4()}"
        download_dir.mkdir(parents=True, exist_ok=True)
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=str(download_dir))
        return str(download_dir)
    except Exception as e:
        print(f"Error downloading single post: {e}")
        return None

async def download_single_post(url, id):
    """Async wrapper to run synchronous download in a thread."""
    loop = asyncio.get_running_loop()
    download_dir = await loop.run_in_executor(executor, sync_download_single_post, url, id)
    return download_dir

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

async def process_download(message: Message, x: Message):
    try:
        download_dir = await download_single_post(message.text, message.from_user.id)
        if download_dir is None:
            await message.answer("Error occurred: Could not download the post.")
            return

        download_path = Path(download_dir)
        # Iterate over files using pathlib to ensure Linux compatibility
        for file in download_path.iterdir():
            if file.suffix == ".mp4":
                reel = FSInputFile(str(file), filename=file.name)
                await message.answer_video(video=reel, caption="📥 Downloaded via @ReelyFastBot", reply_markup=kb.add_to_group)
                file.unlink()
            elif file.suffix == ".txt":
                file.unlink()
            elif file.suffix == ".jpg":
                img = FSInputFile(str(file), filename=file.name)
                await message.answer_photo(img, caption="📥 Downloaded via @ReelyFastBot")
                file.unlink()

        await x.delete()
        if download_path.is_dir():
            shutil.rmtree(download_dir)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")

@router.chat_join_request()
async def handle_join_request(update: ChatJoinRequest):
    pending_requests.add(update.from_user.id)

@router.message(CommandStart())
async def start(message: Message):
    await rq.set_user(tg_id=message.from_user.id)
    if not await subscription_check(message.from_user.id, message):
        return
    await message.answer(f"⚡ Welcome to {(await message.bot.get_me()).username}! ⚡" + greeting_message, reply_markup=kb.add_to_group)

@router.callback_query(F.data == "subchek")
async def subchek(callback: CallbackQuery, message: Message):
    if not await subscription_check(message.from_user.id, message):
        await callback.answer("Your not subscribed yet")
        return
    await callback.answer("Your are okay to go")

@router.message(Command("narrator"))
async def narrator(message: Message, command: CommandObject):
    for user in await rq.get_all_user_ids():
        await bot.send_message(chat_id=user, text=command.args)

@router.message(F.text.regexp(INSTAGRAM_URL_REGEX))
async def handle_instagram_reel(message: Message):
    if not await subscription_check(message.from_user.id, message):
        return
    x = await message.answer(f"✅ Instagram post detected! Did you know: {fact_list[randint(0, len(fact_list)-1)]}")
    # Start download as a background task
    asyncio.create_task(process_download(message, x))

@router.message()
async def catch_all(message: Message):
    if not await subscription_check(message.from_user.id, message):
        return
    await message.answer("Pls send instagram url/link")
