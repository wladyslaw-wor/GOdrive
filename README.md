# GOdrive - Подготовка к экзамену ПДД Армении

Telegram-бот и веб-приложение для подготовки к теоретическому экзамену на водительские права в Армении.

## Описание

GOdrive - это комплексное решение для изучения правил дорожного движения Армении, включающее:

- **Telegram-бот** с интеграцией WebApp
- **Веб-приложение** для пользователей (обучение и тестирование)
- **Админ-панель** для управления контентом
- **Система статистики** и отслеживания прогресса

## Функциональность

### Для пользователей:
- 📚 **Режим обучения** - изучение билетов с подробными объяснениями
- 🧪 **Режим тестирования** - проверка знаний и получение сертификата
- 📊 **Статистика** - отслеживание прогресса и результатов
- ⚙️ **Настройки** - персональные предпочтения и язык интерфейса

### Для администраторов:
- 👥 **Управление пользователями** - просмотр, фильтрация, деактивация
- 📝 **Управление контентом** - создание и редактирование билетов, вопросов, ответов
- 📈 **Аналитика** - статистика использования и производительности
- 🔄 **Импорт/экспорт** - массовые операции с контентом

## Технологический стек

### Backend:
- **Django 4.2** + Django REST Framework
- **PostgreSQL** - основная база данных
- **Redis** - кэширование и сессии
- **Docker** - контейнеризация

### Frontend:
- **Next.js 14** + React 18
- **TypeScript** - типизация
- **Tailwind CSS** - стилизация
- **Telegram WebApp API** - интеграция с Telegram

### Bot:
- **aiogram 3.2** - Telegram Bot API
- **aiohttp** - веб-сервер для webhook

## Установка и запуск

### Предварительные требования:
- Docker и Docker Compose
- Node.js 18+ (для локальной разработки)
- Python 3.11+ (для локальной разработки)

### 1. Клонирование репозитория:
```bash
git clone <repository-url>
cd GOdrive
```

### 2. Настройка переменных окружения:
```bash
cp env.example .env
# Отредактируйте .env файл с вашими настройками
```

### 3. Запуск с Docker Compose:
```bash
docker-compose up -d
```

### 4. Выполнение миграций:
```bash
docker-compose exec backend python manage.py migrate
```

### 5. Создание суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```

### 6. Загрузка тестовых данных (опционально):
```bash
docker-compose exec backend python manage.py loaddata fixtures/initial_data.json
```

## Структура проекта

```
GOdrive/
├── backend/                 # Django backend
│   ├── config/             # Настройки Django
│   ├── apps/               # Django приложения
│   │   ├── users/          # Пользователи и аутентификация
│   │   ├── tickets/        # Билеты и вопросы
│   │   ├── attempts/       # Попытки тестирования
│   │   └── admin_panel/    # Админ-панель
│   └── requirements.txt    # Python зависимости
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/     # React компоненты
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API сервисы
│   │   └── types/          # TypeScript типы
│   └── package.json        # Node.js зависимости
├── bot/                    # Telegram bot
│   ├── main.py            # Основной файл бота
│   └── requirements.txt   # Python зависимости
├── docker-compose.yml     # Docker Compose конфигурация
└── README.md             # Документация
```

## API Endpoints

### Аутентификация:
- `POST /api/auth/profile/` - Получить профиль пользователя
- `PATCH /api/auth/profile/` - Обновить профиль
- `POST /api/auth/activity/` - Обновить активность

### Билеты:
- `GET /api/tickets/` - Список билетов
- `GET /api/tickets/{number}/` - Детали билета
- `GET /api/tickets/random/` - Случайный билет
- `GET /api/tickets/progress/` - Прогресс пользователя

### Попытки:
- `POST /api/attempts/create/` - Создать попытку
- `POST /api/attempts/{id}/submit-answer/` - Отправить ответ
- `POST /api/attempts/{id}/complete/` - Завершить попытку
- `GET /api/attempts/statistics/` - Статистика пользователя

## Разработка

### Локальная разработка:

1. **Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py runserver
```

2. **Frontend:**
```bash
cd frontend
npm install
npm run dev
```

3. **Bot:**
```bash
cd bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Тестирование:
```bash
# Backend тесты
docker-compose exec backend python manage.py test

# Frontend тесты
cd frontend
npm test
```

## Развертывание

### Production настройки:
1. Обновите переменные окружения для production
2. Настройте SSL сертификаты
3. Настройте webhook для Telegram bot
4. Настройте мониторинг и логирование

### Docker Production:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Лицензия

MIT License

## Поддержка

Для вопросов и поддержки обращайтесь к администратору проекта.

