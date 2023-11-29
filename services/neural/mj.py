import aiohttp
import logging as lg
from fake_useragent import UserAgent
ua = UserAgent(browsers=['edge', 'chrome'], os="linux")


class midjourney:
    # Отправить запрос в MJ
    async def prompt(prompt: str, discord_config: dict):
        payload = {
            "type": 2,
            "application_id": "936929561302675456",
            "guild_id": discord_config["ServerID"],
            "channel_id": discord_config["ChannelID"],
            "session_id": "1b3afa47e449362f01aaf2256f5682e2",
            "data": {
                "version": "1166847114203123795",
                "id": "938956540159881230",
                "name": "imagine",
                "type": 1,
                "options": [
                {
                    "type": 3,
                    "name": "prompt",
                    "value": prompt
                }
                ],
                "application_command": {
                "id": "938956540159881230",
                "application_id": "936929561302675456",
                "version": "1166847114203123795",
                "default_member_permissions": None,
                "type": 1,
                "nsfw": False,
                "name": "imagine",
                "description": "Create images with Midjourney",
                "dm_permission": True,
                "contexts": None,
                "integration_types": [
                    0
                ],
                "options": [
                    {
                    "type": 3,
                    "name": "prompt",
                    "description": "The prompt to imagine",
                    "required": True
                    }
                ]
                },
                "attachments": []
            }
        }

        headers = {
            'authorization': discord_config["SalaiToken"],
            #'user-agent': ua.random
        }

        async with aiohttp.ClientSession() as session:
            async with session.post("https://discord.com/api/v9/interactions", json=payload, headers=headers) as response:
                print(response.text)
                return response.status


    # Отправить запрос на Upscale в MJ
    async def upscale(index, messageId, messageHash, discord_config):
        payload = {
            "type": 3,
            "guild_id": discord_config["ServerID"],
            "channel_id": discord_config["ChannelID"],
            "message_flags": 0,
            "message_id": messageId,
            "application_id": "936929561302675456",
            "session_id": "45bc04dd4da37141a5f73dfbfaf5bdcf",
            "data": {
                "component_type": 2,
                "custom_id": "MJ::JOB::upsample::{}::{}".format(index, messageHash)
            }
        }

        headers = {
            'authorization': discord_config["SalaiToken"],
            #'user-agent': ua.random
        }

        async with aiohttp.ClientSession() as session:
            async with session.post("https://discord.com/api/v9/interactions", json=payload, headers=headers) as response:
                print(response.status)
                text = await response.text()
                if response.status != 204:
                    raise Exception(f"ERROR RESPONSE <code>{response.status}</code>\n\n"
                                    f"<code>{text}</code>"
                                    f"CHECK DISCORD ACCOUNT <code>{discord_config['name']}</code>")
                return response.status


    # Отправить запрос на Variation в MJ
    async def variation(index, messageId, messageHash, discord_config):
        payload = {
            "type": 3,
            "guild_id": discord_config["ServerID"],
            "channel_id": discord_config["ChannelID"],
            "message_flags": 0,
            "message_id": messageId,
            "application_id": "936929561302675456",
            "session_id": "1f3dbdf09efdf93d81a3a6420882c92c",
            "data": {
                "component_type": 2,
                "custom_id": "MJ::JOB::variation::{}::{}".format(index, messageHash)
            }
        }

        headers = {
            'authorization': discord_config["SalaiToken"],
            #'user-agent': ua.random
        }

        async with aiohttp.ClientSession() as session:
            async with session.post("https://discord.com/api/v9/interactions", json=payload, headers=headers) as response:
                print(response.status)
                text = await response.text()
                if response.status != 204:
                    raise Exception(f"ERROR RESPONSE <code>{response.status}</code>\n\n"
                                    f"<code>{text}</code>"
                                    f"CHECK DISCORD ACCOUNT <code>{discord_config['name']}</code>")
                return response.status



    async def zoom(index, messageId, messageHash, discord_config):
        payload = {
            "type": 3,
            "guild_id": discord_config["ServerID"],
            "channel_id": discord_config["ChannelID"],
            "message_flags": 0,
            "message_id": messageId,
            "application_id": "936929561302675456",
            "session_id": "1f3dbdf09efdf93d81a3a6420882c92c",
            "data": {
                "component_type": 2,
                "custom_id": "MJ::Outpaint::{}::1::{}::SOLO".format(index, messageHash)
            }
        }

        headers = {
            'authorization': discord_config["SalaiToken"],
            #'user-agent': ua.random
        }

        async with aiohttp.ClientSession() as session:
            async with session.post("https://discord.com/api/v9/interactions", json=payload, headers=headers) as response:
                print(response.status)
                text = await response.text()
                if response.status != 204:
                    raise Exception(f"ERROR RESPONSE <code>{response.status}</code>\n\n"
                                    f"<code>{text}</code>"
                                    f"CHECK DISCORD ACCOUNT <code>{discord_config['name']}</code>")
                return response.status
