# Backend для корпоративного сайта

Backend-сервис для корпоративного сайта на FastAPI. Архитектура построена на принципах Domain-Driven Design с четким разделением слоев.

## Технологии

- Python 3.13, FastAPI (async)
- MongoDB, Motor (async драйвер)
- MinIO/S3 для хранения файлов
- JWT аутентификация (access/refresh токены)
- Docker, docker-compose
- Makefile для управления командами
- Pydantic Settings для конфигурации


## Архитектура

Проект разделен на четыре слоя:

- **Domain** (`app/domain/`) — бизнес-логика, сущности, доменные сервисы
- **Application** (`app/application/`) — use cases через CQRS (Commands/Queries) и Mediator
- **Infrastructure** (`app/infrastructure/`) — MongoDB репозитории, конвертеры, S3 клиент
- **Presentation** (`app/presentation/`) — FastAPI роуты, схемы запросов/ответов

**Dependency Injection** реализован через контейнер `punq`. Все зависимости регистрируются в контейнере и автоматически инжектируются в handlers через конструкторы.

## Модули

- **Auth** — регистрация и аутентификация пользователей
- **Users** — управление пользователями
- **News** — новости компании
- **Vacancies** — вакансии
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

# Запуск всех сервисов (приложение + MongoDB + MinIO)
make all
```

API документация: http://localhost:8000/api/docs

## Основные команды Makefile

### Управление приложением

| Команда | Описание |
|---------|----------|
| `make all` | Запуск приложения + MongoDB + MinIO |
| `make all-down` | Остановка всех сервисов |
| `make app-up` | Запуск только приложения |
| `make app-down` | Остановка приложения |
| `make storages` | Запуск только MongoDB и MinIO |
| `make storages-down` | Остановка MongoDB и MinIO |

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
