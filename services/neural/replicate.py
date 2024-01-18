from typing import Optional

import openai
import aiohttp

from config_data.config import config


async def replicate(request_dict: dict) -> Optional[dict]:

    url = 'https://api.replicate.com/v1/predictions'

    headers = {
        "Authorization": f"Token {config['ReplicateToken']}",
        "Content-Type": "application/json"
    }

    data = request_dict

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            data: dict = await response.json()

            if data.get('status') != "starting":
                raise Exception(f"Replicate says Bad Response: {data}")

    return data