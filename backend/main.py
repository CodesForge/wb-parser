from fastapi import FastAPI
import random
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI
import aiohttp
from aiogram import F, Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import URL, create_engine, text, insert, select, update, delete
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import BigInteger
import asyncio
import redis.asyncio as redis
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import json
import enum

sys.path.append(os.path.dirname(__file__))
from ParsingTool import products_get

from bs4 import BeautifulSoup
import os
from datetime import datetime
from fake_useragent import UserAgent

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

load_dotenv('backend/.env')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Registration(BaseModel):
    username: str
    email: str
    password: str

class ParsingData(BaseModel):
    request_user: str

class Registr_acc(BaseModel):
    username: str
    email: str

class RegistrEmail(BaseModel):
    email: str

class Base(DeclarativeBase):
    pass

class OpenAIClient:
    def __init__(self):
        self.client = AsyncOpenAI(
        base_url="https://api.polza.ai/api/v1",
        api_key=os.getenv('OPEN_AI_KEY'),
        )

client_AI = OpenAIClient()

async def OpenAIGet(request: str):
    competive = await client_AI.client.chat.completions.create(
        model="mistralai/mistral-tiny",
        messages=[
            {
                "role": "user",
                "content": request,
            }
        ]
    )
    return competive.choices[0].message.content

class DataBaseConfig:
    def __init__(self):
        self.url_db = os.getenv('DB_URL')
        self.async_engine = create_async_engine(self.url_db)
        self.async_session = async_sessionmaker(self.async_engine, expire_on_commit=False)

class Registration_Users(Base):
    __tablename__ = "registration_users"
    username:Mapped[str] = mapped_column()
    email:Mapped[str] = mapped_column()
    password:Mapped[str] = mapped_column()
    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    time_registration:Mapped[str] = mapped_column()

class FastAPIServerAppJSX(Base):
    __tablename__ = "fastapiserverappjsx"
    datatime:Mapped[str] = mapped_column()
    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    request_user:Mapped[str] = mapped_column()
    request_AI:Mapped[str] = mapped_column()

class WildberriesDataBase(Base):
    __tablename__ = "wildberriesdatastats"
    product_brand:Mapped[str] = mapped_column()
    product_id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_name:Mapped[str] = mapped_column()
    product_price:Mapped[int] = mapped_column(BigInteger)
    product_price_basic:Mapped[int] = mapped_column(BigInteger)
    product_rating:Mapped[int] = mapped_column()
    product_url:Mapped[str] = mapped_column()
    timestamp:Mapped[str] = mapped_column()

class UserRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory
    
    async def insert_db(self, product_brand, product_id, product_name, product_price, product_price_basic, product_rating, product_url, timestamp):
        try:
            async with self.session_factory() as session:
                stmt = pg_insert(WildberriesDataBase).values(
                    {
                        "product_brand": product_brand,
                        "product_id": product_id,
                        "product_name": product_name,
                        "product_price": product_price,
                        "product_price_basic": product_price_basic,
                        "product_rating": product_rating,
                        "product_url": product_url,
                        "timestamp": timestamp,
                    }
                ).on_conflict_do_nothing(
                    index_elements=['product_id']
                )
                await session.execute(stmt)
                await session.commit()
                logger.info('Данные успешно получены!')
        except OperationalError as e:
            logger.error(f"Ошибка подключения к БД: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка SQLAlchemy: {e}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")

class ServiceManager:
    def __init__(self):
        self.db = DataBaseConfig()
        self.user_repo = UserRepository(self.db.async_session)
        
service = ServiceManager()

async def init_db():
    try:
        async with service.db.async_engine.begin() as conn:
            await conn.run_sync(WildberriesDataBase.metadata.create_all)
            logger.info('База данных успешно создана!')
    except OperationalError as e:
        logger.error(f"Ошибка подключения к БД: {e}")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка SQLAlchemy: {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        

async def aio_get():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT') as response:
                if response.status == 200:
                    logger.info(f'response status: {response.status}')
                    data = await response.json()
                    logger.info(f"Получена цена крипто-валюты: {data['price']}")
                    return data
                else:
                    logger.error(f'response status: {response.status}')
                    return None
    except aiohttp.ClientError as e:
        logger.error(f'ClientError: {e}')
        return None
    except Exception as e:
        logger.error(f'Error: {e}')
        return None

@app.get("/username-button")
async def get_weather():
    data = await aio_get()
    return{
        "crypto_price": data["price"],
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "status": "success",
    }

@app.post("/registration")
async def registration_account(request: RegistrEmail):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'Успешно получены данные: {request.email} | {time}')
    return {
        "status": "success",
        "message": "user registered successfully",
        "received_data": {
            "timestamp": time,
            "user_email": request.email,
        }
    }

@app.post("/registr_account")
async def registr_account(request: Registr_acc):
    logger.info(f"Получены данные: {request}")
    id = random.randint(666666, 9999999)
    return {
        "status": "success",
        "message": "User registered successfully",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "received_data": {
            "username": request.username,
            "email": request.email,
            "user_id": id,
        }
    }

@app.post('/parsing-data')
async def parsing_data(request: ParsingData):
    logger.info('Данные успешно получены!')
    data = await products_get(request.request_user)
    
    if not data:
        logger.warning(f'Товары не найдены или неполные данные для запроса: {request.request_user}')
        return {
            "status": "error",
            "message": "Товары не найдены или данные неполные. Попробуйте другой запрос.",
            "product_data": None
        }
        
    product = data["products"][0]
    
    product_id = product["id"]
    product_name = product.get("name", "Название не указано")
    product_brand = product.get("brand", "Бренд не указан") 
    product_rating = product.get("rating", 0)
    
    price_data = product["sizes"][0]["price"]
    product_price = price_data.get("product", 0) / 100
    product_price_basic = price_data.get("basic", 0) / 100
    
    url = f"https://www.wildberries.ru/catalog/{product_id}/detail.aspx"
    
    await service.user_repo.insert_db(
        product_brand,
        product_id,
        product_name,
        product_price,
        product_price_basic,
        product_rating,
        url,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    
    return {
        "status": "success",
        "message": "The data has been successfully processed!",
        "product_data": {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "product_name": product_name,
            "product_id": product_id,
            "product_url": url,
            "product_price": product_price,
            "product_brand": product_brand,
            "product_rating": product_rating,
            "product_price_basic": product_price_basic,
        }
    }

@app.get('/info-get/{email}')
async def info_get(email: str):
    data = await OpenAIGet(email)
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id = random.randint(66666, 9999999)
    
    data = await service.user_repo.insert_db(time, id, email, data)
    
    logger.info(f'Ответ ИИ: {data}')
    return {
        "message": data,
        "status": "success",
    }
    
if __name__ == "__main__":
    asyncio.run(init_db())
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )