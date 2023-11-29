import subprocess

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message


bot = Bot("6744833121:AAG-ABdIBRzoKEEKFgD5qxSZA2rc5m6pHe8")
dp = Dispatcher()


@dp.message(F.text == "/start", F.chat.id.in_({1100294105, 831472057}))
async def start(message: Message):
    await message.answer('чтобы ребутнуть основного бота - /reboot')


@dp.message(F.text == "/reboot", F.chat.id.in_({1100294105, 831472057}))
async def reboot(message: Message):
    kill_command = "sudo docker compose kill"
    subprocess.run(kill_command, shell=True)

    up_command = "sudo docker compose up -d"
    subprocess.run(up_command, shell=True)

    await message.answer('успешный перезапуск.')


if __name__ == "__main__":
    dp.run_polling(bot)