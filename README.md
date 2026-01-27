# Backend для корпоративного сайта

Backend-сервис для корпоративного сайта на FastAPI. Архитектура построена на принципах Domain-Driven Design с четким разделением слоев.

## Технологии

- Python 3.13, FastAPI (async)
- MongoDB, Motor (async драйвер)
- MinIO/S3 для хранения файлов
- RabbitMQ для асинхронных событий
- MailDev для разработки и тестирования email
- JWT аутентификация (access/refresh токены)
- Docker, docker-compose
- Makefile для управления командами
- Pydantic Settings для конфигурации
- Jinja2 для шаблонов email


## Архитектура

Проект разделен на четыре слоя:

- **Domain** (`app/domain/`) — бизнес-логика, сущности, доменные сервисы
- **Application** (`app/application/`) — use cases через CQRS (Commands/Queries) и Mediator
- **Infrastructure** (`app/infrastructure/`) — MongoDB репозитории, конвертеры, S3 клиент, email клиент, интеграции
- **Presentation** (`app/presentation/`) — FastAPI роуты, схемы запросов/ответов, consumer для обработки событий

**Dependency Injection** реализован через контейнер `punq`. (`app/presentation/container.py`) Все зависимости регистрируются в контейнере и автоматически инжектируются в handlers через конструкторы.

## Модули

- **Auth** — регистрация и аутентификация пользователей
- **Users** — управление пользователями
- **News** — новости компании
- **Vacancies** — вакансии
- **Submissions** — заявки и опросные листы
- **Portfolios** — портфолио проектов
- **Products** — продукция
- **Certificates** — сертификаты и группы сертификатов
- **SEO Settings** — настройки SEO
- **Media** — загрузка и управление файлами

## Добавление нового модуля

Последовательность разработки нового модуля:

1. **Доменная модель** — создание сущностей в `app/domain/`
2. **Регистрация доменных сервисов** — регистрация в контейнере `app/application/container.py`
3. **Тесты доменной модели** — тесты в `app/tests/domain/`
4. **Репозитории** — дамми-репозиторий и MongoDB репозиторий в `app/infrastructure/`
5. **Регистрация репозиториев** — регистрация в контейнере `app/application/container.py`
6. **Команды и запросы** — создание команд и запросов в `app/application/`
7. **Регистрация команд и запросов** — регистрация handlers в контейнере `app/application/container.py`
8. **Тесты команд и запросов** — тесты в `app/tests/application/`
9. **API ручки** — создание эндпоинтов в `app/presentation/api/v1/`
10. **Мапперы исключений** — создание мапперов на статус коды в `app/presentation/api/exceptions/mappers/`
11. **Тесты API** — интеграционные тесты в `app/tests/presentation/api/`

## Запуск

```bash
# Копирование файла с переменными окружения
cp .env.example .env

# Запуск всех сервисов (приложение + MongoDB + MinIO + RabbitMQ + MailDev)
make all
```

API документация: http://localhost:8000/api/docs

MailDev веб-интерфейс: http://localhost:1080

RabbitMQ Management: http://localhost:15672

## Основные команды Makefile

### Управление приложением

| Команда | Описание |
|---------|----------|
| `make all` | Запуск приложения + MongoDB + MinIO + RabbitMQ + MailDev |
| `make all-down` | Остановка всех сервисов |
| `make app-up` | Запуск только приложения |
| `make app-down` | Остановка приложения |
| `make storages` | Запуск только MongoDB и MinIO |
| `make storages-down` | Остановка MongoDB и MinIO |
| `make messaging` | Запуск только RabbitMQ |
| `make messaging-down` | Остановка RabbitMQ |
| `make messaging-logs` | Просмотр логов RabbitMQ |
| `make mail` | Запуск только MailDev |
| `make mail-down` | Остановка MailDev |
| `make mail-logs` | Просмотр логов MailDev |

### Разработка

| Команда | Описание |
|---------|----------|
| `make precommit` | Запуск pre-commit проверок для всех файлов |
| `make app-shell` | Подключение напрямую в контейнер приложения |

### Логи

| Команда | Описание |
|---------|----------|
| `make app-logs` | Просмотр логов приложения |
| `make storages-logs` | Просмотр логов MongoDB и MinIO |

### Тестирование

| Команда | Описание |
|---------|----------|
| `make test` | Запуск всех тестов |
| `make test-domain` | Запуск тестов доменного слоя |
| `make test-logic` | Запуск тестов application слоя (команды и запросы) |
| `make test-e2e` | Запуск интеграционных тестов API |
