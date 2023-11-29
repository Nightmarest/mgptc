from config_data.config import config
from utils.json import read_json
from itertools import cycle


# Создание списка запрещенных промтов для MJ
with open(config["BanWords"], "r") as f:
    ban_list = [line.strip().lower() for line in f if line.strip()]


# Discord accounts list
discord_list = read_json("utils/json/discord_config.json")
discord_relax_cycle = cycle(discord_list["relax"])
discord_fast_cycle = cycle(discord_list["fast"])


# Discord DavinciToken
davinci_token_list = []
for key, value in discord_list.items():
    for account in value:
        davinci_token_list.append(account["DavinciToken"])
davinci_token_list = set(davinci_token_list)


# Discord SalaiToken
salai_token_list = []
for key, value in discord_list.items():
    for account in value:
        salai_token_list.append(account["SalaiToken"])
salai_token_list = set(salai_token_list)

# pay_list
pay_list = read_json("utils/json/pay_config.json")
