# 🚀 WB Parser - FullStack Application

**15 лет • FastAPI + React • Production Ready**

Полнофункциональное full-stack приложение для парсинга Wildberries с интеграцией AI-ассистента.

## 📸 Скриншоты
![Главная страница](screenshots/main-page.png)
![Результаты поиска](screenshots/results-page.png)

## 🎯 Возможности
- 🛒 **Парсинг Wildberries** в реальном времени
- 🤖 **AI-ассистент** на базе Mistral AI
- 💾 **Асинхронная БД** с SQLAlchemy + PostgreSQL
- 🎨 **Modern UI** на React + Tailwind CSS
- ⚡ **Production-ready** архитектура
- 🔍 **Умный парсинг** с ротацией User-Agent
- 📊 **Логирование** операций
- 🔐 **CORS** защита
- 🤖 **Telegram Bot** интеграция (в разработке)

## 🏗️ Архитектура

### Backend (FastAPI)
- **Фреймворк**: FastAPI с асинхронной обработкой
- **База данных**: PostgreSQL с SQLAlchemy ORM
- **Парсинг**: aiohttp с ротацией User-Agent
- **AI-интеграция**: Mistral AI через Polza AI API
- **Кэширование**: Redis (подготовлено)
- **Логирование**: Structured logging в файлы

### Frontend (React)
- **Фреймворк**: React 18 с React Router
- **Стили**: Tailwind CSS
- **Формы**: React Hook Form
- **Состояние**: React useState

## 📦 Установка и запуск

### Предварительные требования
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis (опционально)

### Backend установка

```bash
# Клонирование репозитория
git clone <your-repo>
cd wb-parser

# Установка Python зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp backend/.env.example backend/.env
# редактирование backend/.env с вашими настройками

# Инициализация БД
python main.py

**Backend установка**
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установка Python зависимостей
pip install fastapi uvicorn sqlalchemy asyncpg aiohttp python-dotenv openai redis aiogram beautifulsoup4 fake-useragent

# Настройка переменных окружения
cp backend/.env.example backend/.env

**Frontend установка**

# В новом терминале
cd frontend

# Установка зависимостей
npm install react react-dom react-router-dom react-hook-form
npm install -D vite @vitejs/plugin-react tailwindcss autoprefixer postcss

# Инициализация Tailwind
npx tailwindcss init -p

# Запуск в режиме разработки
npm run dev

Frontend будет доступен по адресу: http://localhost:5173

**⚙️ Конфигурация**

Обязательные переменные окружения:
DB_URL=postgresql+asyncpg://user:pass@localhost:5432/wb_parser
OPEN_AI_KEY=your_polza_ai_api_key_from_polza.ai

🚀 Использование
Основной workflow:

1. Запустите backend и frontend

2. Откройте http://localhost:5173

3. Введите название товара в поиск

4. Получите данные о товаре с Wildberries

5. Используйте кнопки для навигации и открытия товара

**🔧 Технические особенности**

Парсинг Wildberries
• Асинхронные запросы через aiohttp
• Ротация User-Agent для обхода защиты
• Обработка ошибок и повторные попытки
• Валидация данных перед сохранением

Безопасность
• CORS middleware для frontend
• Валидация данных через Pydantic
• Защита от SQL-инъекций через SQLAlchemy
• Логирование подозрительной активности

Производительность
• Асинхронная архитектура
• Connection pooling для БД
• Оптимизированные SQL запросы
• Кэширование (подготовлено для Redis)

**🔮 Планы развития**
• Аутентификация пользователей
• История запросов в личном кабинете
• Уведомления о изменении цен
• Расширенная аналитика товаров
• Telegram бот для уведомлений
• Dashboard с метриками
• API документация Swagger/OpenAPI

**Вклад в проект**
1. Форкните репозиторий
2. Создайте feature branch
3. Commit ваши изменения
4. Push в branch
5. Создайте Pull Request

**📄 Лицензия**
MIT License - смотрите файл LICENSE для деталей.

**👨‍💻 Автор**
Разработано с ❤️ для эффективного парсинга Wildberries

📞 Поддержка: Для вопросов и предложений пишите в телеграм: @CodesForge