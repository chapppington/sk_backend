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

## Интеграция с Битрикс

- **События заявок** — из RabbitMQ очередь `submission_created` прилетают события по схемам `SubmissionCreatedEventSchema`
- **Конвертация в лиды** — `convert_event_to_lead_data` превращает событие заявки в `BitrixLeadData` (лид по типу формы, разбор ФИО на части, сбор комментариев, ответов опросного листа и списков файлов в единый `COMMENTS`)
- **Создание лида** — `BitrixClient.create_lead` дергает Bitrix24 webhook `crm.lead.add` c заполнением полей `TITLE`, `ASSIGNED_BY_ID`, `NAME`, `LAST_NAME`, `SECOND_NAME`, `EMAIL`, `PHONE`, `COMMENTS` и др.
- **Конфигурации** — URL вебхука и ID ответственного берутся из настроек `BitrixConfig` (`BITRIX_WEBHOOK_URL`, `BITRIX_ASSIGNED_BY_ID`)

## Интеграция с email

- **Формирование шаблонов** — `EmailTemplatesService` рендерит Jinja2-шаблон `email_submission.html` на основе `SubmissionCreatedEventSchema`
- **Отправка писем** — `EmailClient.send_email` собирает `MIMEMultipart` с HTML-телом и отправляет его через `aiosmtplib` по SMTP
- **Конфигурации** — SMTP-хост, порт, логин/пароль, имя и адрес отправителя берутся из `EmailConfig` (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_USE_TLS`, `SMTP_FROM_EMAIL`, `SMTP_FROM_NAME`)

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

## Деплой на VPS

Проект настроен для автоматического деплоя на VPS через GitHub Actions.

### Настройка GitHub Secrets

Для работы автоматического деплоя необходимо настроить следующие секреты в GitHub:

**Необходимые секреты:**
- `VPS_SSH_PRIVATE_KEY` - приватный SSH ключ для доступа к VPS
- `VPS_HOST` - IP адрес или домен VPS сервера
- `VPS_USER` - имя пользователя для SSH подключения (обычно `root` или `ubuntu`)
- `VPS_APP_DIR` - путь к директории проекта на сервере (например, `/opt/sk_backend`)
- `VPS_APP_URL` - (опционально) URL приложения для health check (например, `http://your-domain.com`)

**Подробные инструкции по настройке SSH ключа и добавлению секретов см. ниже в разделе "Подготовка VPS сервера" (шаги 2 и 5).**

### Подготовка VPS сервера

1. **Установите необходимые зависимости:**
   ```bash
   # Обновление системы
   sudo apt update && sudo apt upgrade -y
   
   # Установка Docker и Docker Compose
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo apt install docker-compose-plugin -y
   
   # Установка Git
     ```

2. **Настройте SSH ключ для GitHub Actions:**
   
   **Шаг 1: Создайте SSH ключ (на вашей локальной машине)**
   ```bash
   # Сгенерируйте новый SSH ключ специально для GitHub Actions
   ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_deploy
   
   # Или используйте существующий ключ (если у вас уже есть SSH ключ для VPS)
   # В этом случае пропустите этот шаг
   ```
   
   **Шаг 2: Скопируйте публичный ключ на VPS сервер**
   ```bash
   # Если создали новый ключ
   ssh-copy-id -i ~/.ssh/github_actions_deploy.pub user@your-vps-ip
   
   # Или если используете существующий ключ
   ssh-copy-id user@your-vps-ip
   
   # Проверьте подключение
   ssh -i ~/.ssh/github_actions_deploy user@your-vps-ip
   # или
   ssh user@your-vps-ip
   ```

3. **Клонируйте репозиторий на сервер:**
   ```bash
   cd /opt
   sudo git clone https://github.com/your-username/sk_backend.git
   cd sk_backend
   ```

4. **Создайте файл `.env` на сервере:**
   ```bash
   # Скопируйте пример .env и отредактируйте под продакшн
   cp .env.prod .env
   nano .env
   ```

5. **Добавьте SSH ключ в GitHub Secrets:**
   
   **Шаг 1: Откройте настройки репозитория в GitHub**
   - Перейдите в ваш репозиторий на GitHub
   - Нажмите на **Settings** (в верхней панели)
   - В левом меню выберите **Secrets and variables** → **Actions**
   
   **Шаг 2: Добавьте секреты**
   
   Нажмите **New repository secret** и добавьте каждый секрет:
   
   - **Name:** `VPS_SSH_PRIVATE_KEY`

     **Скопируйте приватный ключ для GitHub Secrets**
     ```bash
     # Если создали новый ключ
     cat ~/.ssh/github_actions_deploy
    
     # Или если используете существующий ключ (обычно ~/.ssh/id_ed25519 или ~/.ssh/id_rsa)
     cat ~/.ssh/id_ed25519
     # или
     cat ~/.ssh/id_rsa
     ```
    
    **Важно:** Скопируйте весь вывод команды (включая строки `-----BEGIN OPENSSH PRIVATE KEY-----` и `-----END OPENSSH PRIVATE KEY-----`)

     **Value:** Вставьте весь приватный ключ 
     - Должен начинаться с `-----BEGIN OPENSSH PRIVATE KEY-----`
     - И заканчиваться на `-----END OPENSSH PRIVATE KEY-----`
     - Включая все строки между ними
   
   - **Name:** `VPS_HOST`
     **Value:** IP адрес или домен вашего VPS (например, `123.45.67.89` или `example.com`)
   
   - **Name:** `VPS_USER`
     **Value:** Имя пользователя для SSH (обычно `root`, `ubuntu`, или `debian`)
   
   - **Name:** `VPS_APP_DIR`
     **Value:** Путь к директории проекта на сервере (например, `/opt/sk_backend`)
   
   **Важно:** После добавления секретов они будут зашифрованы и их нельзя будет просмотреть. Убедитесь, что сохранили значения где-то безопасно.

### Автоматический деплой

После настройки, деплой будет автоматически запускаться при:
- Push в ветку `main`
- Ручном запуске через GitHub Actions (Actions → Deploy to VPS → Run workflow)

**Важно:** Перед деплоем автоматически выполняются проверки:
1. **Линтинг кода** - проверка стиля кода с помощью `ruff` и `isort`
2. **Тесты** - запуск всех тестов через `pytest`

Деплой на VPS произойдет **только если** все проверки пройдут успешно. Это гарантирует, что на продакшн попадает только проверенный код.