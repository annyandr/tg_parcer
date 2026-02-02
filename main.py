import json
import os
from telethon import TelegramClient
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Получаем данные из окружения
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')

# Создаем клиент
client = TelegramClient('session_name', API_ID, API_HASH)

async def parse_channel(channel_username, limit=100):
    """
    Парсит посты из канала и сохраняет в JSON
    
    Args:
        channel_username: username канала (без @) или ссылка
        limit: количество постов для парсинга
    """
    await client.start(phone=PHONE)
    
    messages = []
    
    # Получаем сообщения из канала
    async for message in client.iter_messages(channel_username, limit=limit):
        msg_data = {
            'id': message.id,
            'date': message.date.isoformat(),
            'text': message.text,
            'views': message.views,
            'forwards': message.forwards,
            'replies': message.replies.replies if message.replies else 0,
            'has_media': message.media is not None,
            'media_type': type(message.media).__name__ if message.media else None
        }
        messages.append(msg_data)
    
    # Сохраняем в JSON
    with open(f'{channel_username}_posts.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    
    print(f"Сохранено {len(messages)} постов в {channel_username}_posts.json")

# Запуск
with client:
    client.loop.run_until_complete(parse_channel('profgynecologist', limit=50))
