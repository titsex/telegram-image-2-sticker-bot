import settings, requests

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram import types
from io import BytesIO
from PIL import Image
from main import bot

name = "convert"
description = (f"the command that accepts the image "
               f"and returns the converted image "
               f"in accordance with the requirements "
               f"of the telegram for stickers")
is_fsm = True

class Form(StatesGroup):
    photo = State()

async def convert(message: types.Message, state: FSMContext):
    await state.set_state(Form.photo)
    return await message.reply("Send me an image!")

async def photo(message: types.Message, state: FSMContext):
    if not message.photo and not message.document:
        return await message.reply("Send me an image!")

    photo = types.PhotoSize
    photo_url = str()
    
    if message.photo:
        photo = message.photo[-1]
    elif message.document:
        if message.document.mime_type and message.document.mime_type.startswith("image"):
            photo = message.document
            
    if not photo:
        return await message.reply("Send me an image!")
    
    waiting_message = await message.reply("Please wait, we are processing...")

    try:
        file = await bot.get_file(photo.file_id)
        photo_url = f"https://api.telegram.org/file/bot{settings.TOKEN}/{file.file_path}"
    except Exception:
        await waiting_message.delete()
        return await message.reply("Telegram has eaten your image :(\nSend me an image again!")
    
    image = Image.open(requests.get(photo_url, stream=True).raw)
    image = image.resize((512, 512))
    
    image_byte_array = BytesIO()
    image.save(image_byte_array, format="png")
    
    document = types.BufferedInputFile(file=image_byte_array.getvalue(), filename=f"{str(datetime.now().timestamp())}.png")
    
    await state.clear()
    await waiting_message.delete()
    return await message.reply_document(document)