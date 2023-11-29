# # from aiogram import Bot, types, Dispatcher, F

# # TOKEN = "6381626647:AAHslG-YIAVYEZjbIB_wTt70-QyrqtVvF2M"
# # bot = Bot(TOKEN)
# # dp = Dispatcher()

# # @dp.message(F.sticker)
# # async def msg(message: types.Message):
# #     await message.answer_sticker(types.URLInputFile("https://api.telegram.org/file/bot6381626647:AAHslG-YIAVYEZjbIB_wTt70-QyrqtVvF2M/stickers/file_0.tgs", filename="file_0.tgs"))
# #     file = await bot.get_file(message.sticker.file_id)
# #     document_url = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"
# #     await message.answer(document_url)


# # @dp.message(F.video)
# # async def msg(message: types.Message):
# #     await message.answer_video(types.URLInputFile("https://api.telegram.org/file/bot6381626647:AAHslG-YIAVYEZjbIB_wTt70-QyrqtVvF2M/videos/file_1.mp4", filename="file_1.mp4"))
# #     # file = await bot.get_file(message.video.file_id)
# #     # document_url = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"
# #     # await message.answer(document_url)


# # if __name__ == "__main__":
# #     dp.run_polling(bot)

# # # import aiocron
# # # import asyncio

# # # # Ваша функция, которую вы хотите выполнить с аргументами
# # # async def my_task(arg1, arg2):
# # #     print(f"My task executed with arguments: {arg1}, {arg2}")

# # # aiocron.crontab("15 13 * * *", func=my_task, args=("1", "2"))

# # # # Запускаем асинхронное приложение
# # # loop = asyncio.get_event_loop()
# # # loop.run_forever()


# # # import re

# # # # Ваш текст, включая "Prompt:" и "Author:"
# # # text = "<@1123133752399364146> Prompt: 333 333 33 Author: <@1123133752399364146>"

# # # # Используем регулярное выражение для извлечения текста после "Prompt:", исключая "Author:"
# # # match = re.search(r'Prompt:(.*?)\s*Author:', text)

# # # if match:
# # #     extracted_text = match.group(1).strip()
# # #     print("Извлеченное предложение:", extracted_text)
# # # else:
# # #     print("Предложение после 'Prompt:' не найдено.")


# # import re

# # def remove_content_inside_brackets(input_string: str) -> str:
# #     pattern = r'<[^>]*>'
# #     result = re.sub(pattern, '', input_string)
# #     return result

# # result = remove_content_inside_brackets(input_string)
# # print(result.strip() + "1")


# # from database.PostgreSQL import PostgreSQL
# # import datetime


# # db = PostgreSQL()

# # result = db.admin_request(f"SELECT join_date, buyer, where_from FROM clients")

# # # for element in result:
# # #     print(f"{element[0]} {element[1]} {element[2]}")


# # today = datetime.date.today()

# # count_ads_today = 0
# # count_ads_week = 0
# # count_ads_month = 0

# # count_samorost_today = 0
# # count_samorost_week = 0
# # count_samorost_month = 0

# # count_buyer_today = 0
# # count_buyer_week = 0
# # count_buyer_month = 0


# # for user_element in result:
# #     date: datetime.date = user_element[0]
# #     buyer: bool = user_element[1]
# #     where_from: str = user_element[2]

# #     if date is None:
# #         break

# #     if date == today:
# #         if buyer:
# #             count_buyer_today += 1
# #         if where_from:
# #             count_ads_today += 1
# #         else:
# #             count_samorost_today += 1

# #     if (today - date).days <= 7:
# #         if buyer:
# #             count_buyer_week += 1
# #         if where_from:
# #             count_ads_week += 1
# #         else:
# #             count_samorost_week += 1

# #     if (today - date).days <= 30:
# #         if buyer:
# #             count_buyer_month += 1
# #         if where_from:
# #             count_ads_month += 1
# #         else:
# #             count_samorost_month += 1


# # print(f"Сумма за сегодня: {count_ads_today + count_samorost_today}")
# # print(f"Сумма за неделю: {count_ads_week + count_samorost_week}")
# # print(f"Сумма за месяц: {count_ads_month + count_samorost_month}\n")

# # print(f"Cаморост за сегодня: {count_samorost_today}")
# # print(f"Саморост за неделю: {count_samorost_week}")
# # print(f"Саморост за месяц: {count_samorost_month}\n")

# # print(f"Реклама за сегодня: {count_ads_today}")
# # print(f"Реклама за неделю: {count_ads_week}")
# # print(f"Реклама за месяц: {count_ads_month}\n")

# # print(f"Купили за сегодня: {count_buyer_today}")
# # print(f"Купили за неделю: {count_buyer_week}")
# # print(f"Купили за месяц: {count_buyer_month}")

# # import matplotlib.pyplot as plt
# # from collections import Counter
# # from datetime import timedelta, date
# # from database.PostgreSQL import PostgreSQL

# # def get_graph_stats():
# #     db = PostgreSQL()
# #     result = db.admin_request("SELECT join_date FROM clients")
# #     date_list = [date_element[0] for date_element in result]

# #     end_date = max(date_list)
# #     start_date = end_date - timedelta(days=14)

# #     date_range = [start_date + timedelta(days=i) for i in range(15)]

# #     date_counter = Counter(date_list)
# #     section_counts = [date_counter[d] for d in date_range]

# #     date_labels = [d.strftime("%d.%m.%Y") for d in date_range]

# #     plt.figure(figsize=(12, 6))
# #     bar_width = 0.8
# #     bars = plt.bar(date_labels, section_counts, color='b', width=bar_width)

# #     plt.title('Сумма прибывших за последний месяц')
# #     plt.xlabel('Дата за последние две недели')
# #     plt.ylabel('Количество людей')
# #     plt.xticks(rotation=45, fontsize=8)
# #     plt.ylim(0, max(section_counts) * 1.05)

# #     for bar, count in zip(bars, section_counts):
# #         plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, count, ha='center', va='bottom')

# #     plt.tight_layout()
# #     plt.show()

# # get_graph_stats()


# from database.PostgreSQL import PostgreSQL
# import datetime

# today = datetime.date.today()
# db = PostgreSQL()
# result = db.admin_request(f"SELECT join_date, buyer FROM clients WHERE where_from='XGytvHfPYL'")

# count_ads_today = 0
# count_ads_week = 0
# count_ads_month = 0

# count_buyer_today = 0
# count_buyer_week = 0
# count_buyer_month = 0


# for user_element in result:
#     date: datetime.date = user_element[0]
#     buyer: bool = user_element[1]

#     if date is None:
#         break

#     if date == today:
#         if buyer:
#             count_buyer_today += 1
#         count_ads_today += 1

#     if (today - date).days <= 7:
#         if buyer:
#             count_buyer_week += 1
#         count_ads_week += 1

#     if (today - date).days <= 30:
#         if buyer:
#             count_buyer_month += 1
#         count_ads_month += 1


# print(f"Реклама за сегодня: {count_ads_today}")
# print(f"Реклама за неделю: {count_ads_week}")
# print(f"Реклама за месяц: {count_ads_month}\n")

# print(f"Купили за сегодня: {count_buyer_today}")
# print(f"Купили за неделю: {count_buyer_week}")
# print(f"Купили за месяц: {count_buyer_month}")


from aiogram import Bot, Dispatcher
from aiogram.types import Message, InputMediaPhoto


dp = Dispatcher()
bot = Bot("6219812476:AAHV6E9f7NJZ9LcHNeVU90r4P-cGZKYkDHc")


@dp.message()
async def message(message: Message):
    url_list = [
        "https://pub-3626123a908346a7a8be8d9295f44e26.r2.dev/generations/0-ac6ab0c4-31a4-47fc-b50f-8d5dc8a121a6.png",
        "https://pub-3626123a908346a7a8be8d9295f44e26.r2.dev/generations/1-ac6ab0c4-31a4-47fc-b50f-8d5dc8a121a6.png",
        "https://pub-3626123a908346a7a8be8d9295f44e26.r2.dev/generations/2-ac6ab0c4-31a4-47fc-b50f-8d5dc8a121a6.png",
        "https://pub-3626123a908346a7a8be8d9295f44e26.r2.dev/generations/3-ac6ab0c4-31a4-47fc-b50f-8d5dc8a121a6.png"
    ]

    photo_list = []
    photo_list.append(
        InputMediaPhoto(
            media=url_list[0],
            caption="123"
        )
    )

    for url in url_list[1:]:
        photo_list.append(
            InputMediaPhoto(
                media=url
            )
        )

    await bot.send_media_group(
        chat_id=message.from_user.id,
        media=photo_list
    )


if __name__ == "__main__":
    dp.run_polling(bot)