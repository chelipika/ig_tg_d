from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_LINK

subscribe_channel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Subscribe", url=CHANNEL_LINK)],
    [InlineKeyboardButton(text="Check", callback_data="subchek")]
])

add_to_group = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Add to group", url="https://telegram.me/ReelyFastBot?startgroup=true")]
])

def create_markap_kb(name, url):
    if name == "none" or url== "none":
        return None
    ads_channel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, url=url)]
    ])
    return ads_channel