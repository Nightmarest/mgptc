import os

config = {
    "APIToken": "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", # OPENAI
    "ZeroscopeToken": "r8_DyAbjQpqxhwxSmj9qKVVpjysDmnSUdT4Bkf2g", #зероскоп токен
    "DeeplToken": "725ea090-4ba9-494c-8c58-8912b78537a9",
    "BotToken": "6219812476:AAHTYOy3svyVM-J3D0IwjXGSvgwB_a428io",  # Токен самого бота 6062729970:AAHxJG2GCp4A4cL5fROgKRnn7OSrkD5wEBQ
    # "BotToken": "6157728996:AAGRBicyQL4ozhTtIBW8m9X-YAuO29csT4s",
    # Токен самого бота 6062729970:AAHxJG2GCp4A4cL5fROgKRnn7OSrkD5wEBQ

    "DBHost": "194.31.173.202",  # DataBase host
    "DBPort": 5432,  # DataBase port
    "DBUser": "gen_user",  # DataBase user
    "DBPswd": "ne+xutQ%tUT6*=",  # DataBase password
    "DBName": "default_db",  # DataBase name

    # Yoomoney
    "YomoneyToken": "4100117825234416.F2B91EDA8EE3DE9FACD59EF611966E0A5AA09546EBDB994BF1E3BFA0EFB1F8CFE517514BAAEFE8515EB3910E0DCB8EC360DF9401041C0D2461756ACBEB8FA546B2F0B0C9B9D0E66D0EBEFDA89404B4E91B20E97168C6CE3087C6CFFE0E2D4EB4CAEDF7767B503185955C10DFF394F18AF30B1CEF9266F28CC6678EC7788B63B5", # токен акка юмани
    "YoomoneyReceiver": "4100117825234416", # индентефикатор кошелька юмани

    "CPID": "pk_5df88d9e7d056f2d1b4c0bbfabd55",
    "CPKEY": "ec642efb31651c6b6f43c3815562627c",
    # CryptoPay
    "CryptoToken": "118034:AA7jQ4RKRM4yiFrFjl7JVLzagVijgk5qqiH",

    "BDTable": "clients",
    "ADSTable": "ads",

    "ContentDir": "content/",  # Директория со всем контентом
    "DialogsDir": "dialogs/",  # Директория для хранения контекста пользователя
    "LangsDir": "langs/",  # Директория с файлами языков
    "MJDownloads": "mj_downloads/",  # Директория с контентом от MJ,
    "BanWords": "utils/ban_words.txt", # бан слова файл
    "Langs": "lexicon/rus.json", # файл с языками
    "LangsAdmin": "lexicon/rus_admin.json", # файл для
    "DiscordLog": "logs/disc_main.log",
    "BotLog": "logs/bot.log",
    "WebHookLog": "logs/webhook.log",

    "Video": "files/start.mp4", # видео
    "StickerGPT": "files/sticker_gpt.tgs",
    "StickerMJ": "files/sticker_mj.tgs",

    "CheckSub": "utils/json/sub_config.json", # json каналы
    "PromptChoose": "utils/json/prompt_config.json", # json с выбором промптов
    "DiscordConfig": "utils/json/discord_config.json", # json с конфигами дискорда
    "PayConfig": "utils/json/pay_config.json", # json с оплатой

    "LogsON": True,  # Логировать?
    "RequestsMonit": True,  # Мониторниг запросов?
    "Debug": True,  # Дебаг?

    "StartFreeTokensGPT": 15, # на старте
    "StartFreeTokensMJ": 10,  # на старте
    "ReferalTokens": 0,  # реферал
    "UserFreeTokens": 0,  # ежедневный апдейт
    "EverydayUpdatesInterval": 3600,  # Интервал для ежедневных обновлений
    "MJLimitRequestsToday": 3000000, # лимит на запросы в день
    "MJTime": 60 * 5,

    "AdminList": {831472057, 1100294105, 1063430005, 1219187097, 5184973436},  # Список админов 1100294105
    "DevList": {831472057, 5184973436},

    "VideoUrl": "https://telegra.ph/file/b41185d890b48ec6deb77.mp4",
    "BotNickName": "midjourneychatgpt_bot",  # Никнейм Бота для реферальных ссылок
    "BotUrl": "https://t.me/midjourneychatgpt_bot",
    "EducationUrl": "https://telegra.ph/Kak-pisat-promty-dlya-Midjourney-50-krutyh-primerov-09-14",
    "ForumUrl": "https://t.me/neonixforum",
    "WebHookUrl": "http://37.220.85.219:8000",
    "ManagerLink": "https://t.me/Lauren_shorts",

    "Models": ["midjourney", "chatgpt", "pikalabs"],
    "ButtonsZoom": ["mj_zoom1", "mj_zoom2"],
    "ButtonsMJ": [["mj_u1", "mj_u2", "mj_u3", "mj_u4"], ["mj_v1", "mj_v2", "mj_v3", "mj_v4"]],
    "GptRole": [('👨‍💻 Программист', 'gpt_programmer'), ('👨‍💼 Психолог', 'gpt_psychologist'), ('💪 Мотиватор', 'gpt_motivator'), ('🤖 По умолчанию', 'gpt_default')],
    "CryptoCurrency": {"USDT", "BTC"},

    # Для MJ, U - upscale, V - создать варианты
    "mj_u_scales": {"mj_u1": 1, "mj_u2": 2, "mj_u3": 3, "mj_u4": 4},
    "mj_v_scales": {"mj_v1": 1, "mj_v2": 2, "mj_v3": 3, "mj_v4": 4},

    # 50 - 2x, 75 - 1.5x
    "mj_zoom": {"mj_zoom1": 50, "mj_zoom2": 75},

    "domain": "https://gpt.apicluster.ru",
    "path": "/bot/",

    "agreement": "http://bit.ly/49WoClh",
    # True agreement: https://telegra.ph/Usloviya-predostavleniya-uslug-k-Telegram-botu-midjourneychatgpt-bot-11-28
}
