from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_LINK

subscribe_channel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Subscribe", url=CHANNEL_LINK)],
    [InlineKeyboardButton(text="Check", callback_data="subchek")]
])

add_to_group = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Add to group", url="https://telegram.me/ReelyFastBot?startgroup=true")]
])