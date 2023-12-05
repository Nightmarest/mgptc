import random
import aiohttp
import logging as lg

from config_data.config import config


CONFIG = "xg8QGV4vn4yw7B1TBYJdrBHmQNef5y8kMycK5KZuaHAbRMNUTL3vPO79mI0b"


async def stable_pic(prompt: str, ratio: str, model: str, track_id: str, config_dict: dict) -> dict:
    url = "https://stablediffusionapi.com/api/v4/dreambooth"

    wh_data = ratio.split(':')
    width = wh_data[0]
    height = wh_data[1]

    payload = {
        "key": CONFIG,
        "model_id": model,
        "enhance_prompt": "no" if config_dict.get("neg", False) else "yes",
        "self_attention": "no" if config_dict.get("neg", False) else "yes",
        "prompt": f"{prompt}",
        "negative_prompt": config_dict.get("neg", config['NegativeDefault']),
        "width": width,
        "height": height,
        "samples": "1",
        "num_inference_steps": int(config_dict.get("steps", 35)),
        "guidance_scale": int(config_dict.get("scale", 7)),
        "webhook": config["WebHookUrl"] + "/neural/stable",
        "seed": int(config_dict.get("seed", random.randint(1, 999999999999))),
        "track_id": track_id
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                data = await response.json()

                if response.status != 200 or data['status'] == 'error':
                    raise Exception(f"bad response: {data}")

                return data
    except Exception as e:
        lg.error(f"error stable_pic -> {e}")
        return {}
