import matplotlib.pyplot as plt
from collections import Counter
import datetime
import io
import aiohttp

from config_data.create_bot import db
from config_data.config import config
from openpyxl import Workbook
from utils.json import read_json


class func:
    def get_stats_graph(db_info: list) -> io.BytesIO:
        date_list = [date_element[0] for date_element in db_info]

        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=14)
        date_range = [start_date + datetime.timedelta(days=i) for i in range(15)]

        date_counter = Counter(date_list)
        section_counts = [date_counter[d] for d in date_range]

        date_labels = [d.strftime("%d.%m.%Y") for d in date_range]

        plt.figure(figsize=(12, 6))
        bar_width = 0.8
        bars = plt.bar(date_labels, section_counts, color='b', width=bar_width)

        plt.title('Сумма прибывших за последние 14 дней')
        plt.xlabel('Дата за последние 14 дней')
        plt.ylabel('Количество людей')
        plt.xticks(rotation=45, fontsize=8)
        plt.ylim(0, max(section_counts) * 1.1)

        for bar, count in zip(bars, section_counts):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, count, ha='center', va='bottom')

        buff = io.BytesIO()
        plt.savefig(buff, format="png")

        return buff


    def get_stats_str(db_info: list) -> str:
        today = datetime.date.today()

        count_dead = 0
        count_buyer = 0

        count_ads_today = 0
        count_ads_week = 0
        count_ads_month = 0

        count_samorost_today = 0
        count_samorost_week = 0
        count_samorost_month = 0

        # count_buyer_today = 0
        # count_buyer_week = 0
        # count_buyer_month = 0

        for user_element in db_info:
            date: datetime.date = user_element[0]
            buyer: bool = user_element[1]
            where_from: str = user_element[2]
            dead: bool = user_element[3]

            if date is None:
                break

            if buyer:
                count_buyer += 1

            if date == today:
                # if buyer:
                #     count_buyer_today += 1
                if where_from:
                    count_ads_today += 1
                else:
                    count_samorost_today += 1

            if (today - date).days <= 7:
                # if buyer:
                #     count_buyer_week += 1
                if where_from:
                    count_ads_week += 1
                else:
                    count_samorost_week += 1

            if (today - date).days <= 30:
                # if buyer:
                #     count_buyer_month += 1
                if where_from:
                    count_ads_month += 1
                else:
                    count_samorost_month += 1

            if dead:
                count_dead += 1


        summary_text = f"<b>📊 Статистика:</b>\n\n"

        summary_text += f"<b>Пользователей всего:</b> {len(db_info)}\n\n"

        summary_text += f"<b>Живые пользователи:</b> {len(db_info) - count_dead}\n"
        summary_text += f"<b>Мёртвых пользователей:</b> {count_dead}\n"
        summary_text += f"<b>Cовершили покупок:</b> {count_buyer}\n\n"

        summary_text += f"<b>Сумма за сегодня:</b> {count_ads_today + count_samorost_today}\n"
        summary_text += f"<b>Сумма за неделю:</b> {count_ads_week + count_samorost_week}\n"
        summary_text += f"<b>Сумма за месяц:</b> {count_ads_month + count_samorost_month}\n\n"

        summary_text += f"<b>Cаморост за сегодня:</b> {count_samorost_today}\n"
        summary_text += f"<b>Cаморост за неделю:</b> {count_samorost_week}\n"
        summary_text += f"<b>Cаморост за месяц:</b> {count_samorost_month}\n\n"

        summary_text += f"<b>Реклама за сегодня:</b> {count_ads_today}\n"
        summary_text += f"<b>Реклама за неделю:</b> {count_ads_week}\n"
        summary_text += f"<b>Реклама за месяц:</b> {count_ads_month}\n\n"

        # summary_text += f"<b>Купили за сегодня:</b> {count_buyer_today}\n"
        # summary_text += f"<b>Купили за неделю:</b> {count_buyer_week}\n"
        # summary_text += f"<b>Купили за месяц:</b> {count_buyer_month}"

        return summary_text


    def get_statslink_str(db_info: list, ref_name: str, ref_code: str) -> str:
        today = datetime.date.today()

        count_dead = 0
        count_buyer = 0

        count_ads_today = 0
        count_ads_week = 0
        count_ads_month = 0

        count_buyer_today = 0
        count_buyer_week = 0
        count_buyer_month = 0


        for user_element in db_info:
            date: datetime.date = user_element[0]
            buyer: bool = user_element[1]
            dead: bool = user_element[2]

            if date is None:
                break

            if buyer:
                count_buyer += 1

            if dead:
                count_dead += 1

            if date == today:
                # if buyer:
                #     count_buyer_today += 1
                count_ads_today += 1

            if (today - date).days <= 7:
                # if buyer:
                #     count_buyer_week += 1
                count_ads_week += 1

            if (today - date).days <= 30:
                # if buyer:
                #     count_buyer_month += 1
                count_ads_month += 1

        summary_text = f"<b>📊 Статистика ссылки {ref_name}:</b>\n\n"

        summary_text += f"<b>Всего пользователей:</b> {len(db_info)}\n"
        summary_text += f"<b>Мёртвых пользователей:</b> {count_dead}\n"
        summary_text += f"<b>Совершили покупок:</b> {count_buyer}\n\n"

        summary_text += f"<b>Пришло за сегодня:</b> {count_ads_today}\n"
        summary_text += f"<b>Пришло за неделю:</b> {count_ads_week}\n"
        summary_text += f"<b>Пришло за месяц:</b> {count_ads_month}\n\n"

        # summary_text += f"<b>Купили за сегодня:</b> {count_buyer_today}\n"
        # summary_text += f"<b>Купили за неделю:</b> {count_buyer_week}\n"
        # summary_text += f"<b>Купили за месяц:</b> {count_buyer_month}\n\n"

        summary_text += f"<b>🔗 Ссылка:</b> <code>https://t.me/midjourneychatgpt_bot?start=ads{ref_code}</code>"

        return summary_text


    def get_bd():
        headers = db.admin_request(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{config['BDTable']}' ORDER BY ordinal_position;")
        data = db.admin_request(f"SELECT * FROM {config['BDTable']}")
        wb = Workbook()
        ws = wb.active

        for index, value in enumerate(headers, 1):
            ws.cell(row=1, column=index, value=value[0])
        for row_data in data:
            ws.append(row_data)
        wb.save('admins/output.xlsx')


    def divide_list(lst, parts):
        avg = len(lst) // parts
        remainder = len(lst) % parts
        result = []

        i = 0
        for _ in range(parts):
            size = avg + (1 if remainder > 0 else 0)
            result.append(lst[i:i + size])
            i += size
            remainder -= 1

        return result


    def get_op():
        channels = read_json(config["CheckSub"])
        text = ''
        i = 0

        for element in channels:
            channel_id = element["id"]
            first_name = element["first_name"]
            url = element["url"]
            skip = ' (БП) ' if element["skip"] else ' '
            i += 1

            text += f'{i}) <a href="{url}">{first_name}</a>{skip}| [<code>{channel_id}</code>]\n'
        return text


    async def get_bot_info(token):
        url = f"https://api.telegram.org/bot{token}/getMe"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if response.status == 200 and data.get('ok'):
                    bot_info = data['result']
                    return bot_info
                else:
                    return None