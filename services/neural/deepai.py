import aiohttp


async def upscale_photo(photo_url):
    url = "https://api.deepai.org/api/torch-srgan"
    headers = {'api-key': '725ea090-4ba9-494c-8c58-8912b78537a9'}
    data = {'image': photo_url}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            response_data = await response.json()
            return response_data['output_url']
