import logging
import aiohttp
from fake_useragent import UserAgent
from pathlib import Path
import asyncio
import json

class SmartParser:
    def __init__(self):
        self.ua = UserAgent()
    
    def random_agent(self):
        return self.ua.random

logs_dir = Path(__file__).parent / "logs"
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s][%(message)s]',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(str(logs_dir / 'wb_parser.log')),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

async def products_get(request_user: str):
    params = {
    'ab_testing': [
        'false',
        'false',
    ],
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'hide_dtype': '11',
    'inheritFilters': 'false',
    'lang': 'ru',
    'page': '1',
    'query': request_user,
    'resultset': 'catalog',
    'sort': 'popular',
    'spp': '30',
    'suppressSpellcheck': 'false',
}
    try:
        parser = SmartParser()
        user_agent = parser.random_agent()
        async with aiohttp.ClientSession(headers={"User-Agent": user_agent}) as session:
            async with session.get('https://u-search.wb.ru/exactmatch/ru/common/v18/search', params=params) as response:
                if response.status == 200:
                    logger.info(f'Response status: {response.status}')
                    html = await response.text()
                    try:
                        data = json.loads(html)
                        logger.info("JSON успешно распарсен")
                        return data
                    except json.JSONDecodeError as e:
                        logger.error(f"Ошибка парсинга JSON: {e}")
                        return {"error": "Invalid JSON", "raw_text": html[:500]}
                else:
                    logger.error(f'Response status: {response.status}')
                    return None
    except aiohttp.ClientError as e:
        logger.error(f'ClientError: {e}')
    except Exception as e:
        logger.error(f'Error: {e}')
        