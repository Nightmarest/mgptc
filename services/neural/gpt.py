import openai.error
from typing import Tuple
import logging as lg
import io
from aiogtts import aiogTTS

from config_data.config import config
from utils.func import report, get_text


async def text_to_voice(text: str) -> io.BytesIO:
    aiogtts = aiogTTS()
    voice_bytes = io.BytesIO()
    await aiogtts.write_to_fp(
        text=text,
        fp=voice_bytes,
        lang='ru'
    )
    return voice_bytes


async def voice_to_text(voice: io.BytesIO, attempt = 0) -> str:
    if attempt > 3:
        raise Exception("ERROR IN get_response_gpt. CHECK LOGS")
    openai.api_key = config["APIToken"]

    try:
        result = await openai.Audio.atranscribe(
            model="whisper-1",
            file=voice
        )
        print(result["text"])
        return result["text"]
    except (
        openai.error.Timeout,
        openai.error.ServiceUnavailableError,
        openai.error.APIConnectionError,
        openai.error.InvalidRequestError,
    ) as e:
        lg.error(f"ERROR IN get_response_gpt: {e} ||| Try again...")
        return await voice_to_text(voice, attempt + 1)




# Получить ответ на вопрос от GPT
async def get_response_gpt(dialog_list: list, request: str, attempt=0) -> Tuple[list, str]:
    if attempt > 3:
        raise Exception("ERROR IN get_response_gpt. CHECK LOGS")
    openai.api_key = config["APIToken"]

    try:
        dialog_list.append({"role": "user", "content": request})
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=dialog_list
        )
        response = completion.choices[0].message.content
        dialog_list.append({"role": "assistant", "content": response})
    except (
        openai.error.Timeout,
        openai.error.ServiceUnavailableError,
        openai.error.APIConnectionError,
        openai.error.InvalidRequestError,
    ) as e:
        lg.error(f"ERROR IN get_response_gpt: {e} ||| Try again...")
        return await get_response_gpt(
            [{"role": "system", "content": ""}], request[:2048], attempt + 1
        )
    except Exception as e:
        await report(f"⚠️ <b>ERROR IN ChatGPT:</b> <code>{e}</code>",
                     config["DevList"])
        return [{"role": "system", "content": ""}], get_text("text.error_gpt")

    return dialog_list, response