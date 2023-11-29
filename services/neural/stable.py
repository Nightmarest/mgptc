import asyncio
import aiohttp
import logging as lg

from config_data.config import config

CONFIG = "xg8QGV4vn4yw7B1TBYJdrBHmQNef5y8kMycK5KZuaHAbRMNUTL3vPO79mI0b"


async def stable_pic(prompt: str, ratio: str, model: str, track_id: str) -> dict:
    url = "https://stablediffusionapi.com/api/v4/dreambooth"

    wh_data = ratio.split(':')
    width = wh_data[0]
    height = wh_data[1]

    payload = {
        "key": CONFIG,
        "model_id": model,
        "enhance_prompt": "yes",
        "self_attention": "yes",
        "prompt": f"{prompt}",
        "negative_prompt": "bad quality, bad anatomy, worst quality, low quality, lowres, extra fingers, blur, blurry, ugly, wrong proportions, watermark, image artifacts",
        "width": width,
        "height": height,
        "samples": "1",
        "num_inference_steps": 30,
        "guidance_scale": 4.1,
        "webhook": config["WebHookUrl"] + "/neural/stable",
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


async def get_pic(request_id, count = 0):
    if count > 15:
        return False

    payload = {
        "key": CONFIG,
        "request_id": request_id
    }
    url = "https://stablediffusionapi.com/api/v4/dreambooth/fetch"
    headers = {
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()

            if data['status'] == 'success':
                return data

            elif data['status'] == 'processing':
                await asyncio.sleep(30)
                return await get_pic(request_id, count+1)

            elif data['status'] == 'error':
                lg.error(f'error: {data}')
                return False


async def upscale_pic(pic_code: str, track_id: str) -> bool:
    photo_url = f'https://cdn2.stablediffusionapi.com/generations/{pic_code}.png'

    url = "https://stablediffusionapi.com/api/v3/super_resolution"

    payload = {
        "key": CONFIG,
        "url": photo_url,
        "scale": 2,
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

                if data['status'] == 'processing':
                    data = await get_pic(data['id'])

                return data
    except Exception as e:
        lg.error(f"error upscale_pic -> {e}")
        return {}