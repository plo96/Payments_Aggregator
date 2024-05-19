import os
from datetime import datetime
from io import BytesIO
import json

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from src.services import PaymentService

router = Router()


@router.message(Command("start"))
async def start(
        message: Message,
):
    await message.answer(
        text=f'Hi {message.from_user.full_name}!'
    )


@router.message()
async def handle_json(
        message: Message,
        bot: Bot,
):
    document = message.document
    if not document:
        await message.reply(
            text="Извините, я вас не понимаю.",
        )
        return
    if document.mime_type != 'application/json':
        await message.reply(
            text="Извините, я могу обрабатывать только JSON-файлы!",
        )
    else:
        file_info = await bot.get_file(document.file_id)
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)

        with BytesIO() as buf:
            buf.write(downloaded_file.read())
            buf.seek(0)
            input_data = json.load(buf)

        dt_from = datetime.fromisoformat(input_data.__getitem__('dt_from'))
        dt_upto = datetime.fromisoformat(input_data.__getitem__('dt_upto'))
        group_type = input_data.__getitem__('group_type')

        answer = await PaymentService.aggregate_payments(
            dt_from=dt_from,
            dt_upto=dt_upto,
            group_type=group_type,
        )

        await message.answer(
            f"```{json.dumps(answer, indent=4)}```",
            parse_mode="MARKDOWN"
        )

        # json_file_name = 'answer.json'
        # try:
        #     json_file_name = 'answer.json'
        #     with open(json_file_name, 'w') as json_file:
        #         json_file.write(json.dumps(answer))
        #
        #     await bot.send_document(
        #         chat_id=message.chat.id,
        #         document=FSInputFile(json_file_name),
        #         caption='Вот ваш ответ в виде JSON-файла.',
        #     )
        #
        # finally:
        #     if json_file_name in os.listdir():
        #         os.remove(json_file_name)
