import aiohttp


async def prompt_to_video(prompt: str, discord_config: dict) -> int:
    payload = {
        "type": 2,
        "application_id": "1123673306256650240",
        "channel_id": discord_config["PikaLabsID"],
        "session_id": "9f98b485e50adfc0ec2d9422c0d0f3cd",
        "data": {
            "version": "1133491895239184455",
            "id": "1123674537049981100",
            "name": "create",
            "type": 1,
            "options": [
            {
                "type": 3,
                "name": "prompt",
                "value": prompt
            }
            ],
            "application_command": {
                "id": "1123674537049981100",
                "application_id": "1123673306256650240",
                "version": "1133491895239184455",
                "default_member_permissions": None,
                "type": 1,
                "nsfw": False,
                "name": "create",
                "description": "No description provided",
                "dm_permission": True,
                "contexts": None,
                "integration_types": [
                    0
                ],
                "options": [
                    {
                        "type": 3,
                        "name": "prompt",
                        "description": "prompt",
                        "required": True,
                        "max_length": 1500
                    },
                    {
                        "type": 11,
                        "name": "image",
                        "description": "image prompt"
                    }
                ]
            },
            "attachments": []
        }
    }
    headers = {
        'authorization': discord_config["SalaiToken"]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://discord.com/api/v9/interactions", json=payload, headers=headers) as response:
            return response.status
