from aiogram import types

name = "start"
description = "the command about the bot"
is_fsm = False

async def start(message: types.Message):
    greeting = "Hi! I'm a bot that converts your images according to Telegram's sticker requirements!"
    help = "To find out my capabilities, enter /help"
    
    await message.reply((f"{greeting}\n\n"f"{help}"))