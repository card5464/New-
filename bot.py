import logging
import requests
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from fastapi import FastAPI
import uvicorn

API_TOKEN = os.getenv("8026718612:AAGuYHadarUY9bO-cFwri_eBhPYxaWAj37o")  # Fetch token from environment variable

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

app = FastAPI()  # Create a FastAPI app

@app.get("/")
def home():
    return {"message": "Bot is running"}

def get_bin_info(bin_number):
    url = f"https://lookup.binlist.net/{bin_number}"
    headers = {"Accept-Version": "3"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return f"BIN: {bin_number}\n" \
                   f"Brand: {data.get('scheme', 'Unknown')}\n" \
                   f"Type: {data.get('type', 'Unknown')}\n" \
                   f"Bank: {data.get('bank', {}).get('name', 'Unknown')}\n" \
                   f"Country: {data.get('country', {}).get('name', 'Unknown')}"
        else:
            return "Invalid BIN or API limit reached."
    except:
        return "Error fetching BIN data."

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Hello! Send me a BIN (first 6 digits of a card) to check.")

@dp.message_handler()
async def bin_lookup(message: types.Message):
    bin_number = message.text.strip()
    if bin_number.isdigit() and len(bin_number) == 6:
        result = get_bin_info(bin_number)
        await message.reply(result)
    else:
        await message.reply("Please enter a valid 6-digit BIN.")

if __name__ == '__main__':
    from threading import Thread
    Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=10000)).start()
    executor.start_polling(dp, skip_updates=True)
