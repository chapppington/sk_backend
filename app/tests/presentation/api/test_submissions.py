from uuid import uuid4

from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from faker import Faker
from faststream.rabbit import TestRabbitBroker
from httpx import Response

from application.mediator import Mediator
from application.submissions.commands import CreateSubmissionCommand
from presentation.api.v1.submissions import handlers
from presentation.api.v1.submissions.schemas import SubmissionRequestSchema


async def dummy_submission_consumer(message: dict) -> None:
    """Фиктивный консьюмер для тестирования публикации событий."""


# Регистрируем тестовый подписчик для очереди submission_created
# Это необходимо для TestRabbitBroker, который требует подписчика для публикации
handlers.router.broker.subscriber("submission_created")(dummy_submission_consumer)


@pytest.mark.asyncio
async def test_create_submission_success(client: TestClient, faker: Faker):
    """Тест успешного создания заявки."""
    async with TestRabbitBroker(handlers.router.broker):
        url = "/api/v1/submissions"

        data = {
            "form_type": "Опросный лист",
            "name": faker.name(),
            "email": faker.email(),
            "phone": faker.phone_number(),
            "comments": faker.text(max_nb_chars=200),
            "files": [],
            "questionnaire_type": "КТП",
        }

        response: Response = client.post(url=url, json=data)

        assert response.is_success
        assert response.status_code == status.HTTP_201_CREATED

        json_response = response.json()

        assert "data" in json_response
        assert json_response["data"]["form_type"] == data["form_type"]
        assert json_response["data"]["name"] == data["name"]
        assert json_response["data"]["email"] == data["email"]
        assert json_response["data"]["phone"] == data["phone"]
        assert json_response["data"]["questionnaire_type"] == data["questionnaire_type"]
        assert "oid" in json_response["data"]


@pytest.mark.asyncio
async def test_create_submission_minimal(client: TestClient, faker: Faker):
    """Тест создания заявки с минимальными данными."""
    async with TestRabbitBroker(handlers.router.broker):
        url = "/api/v1/submissions"

        data = {
            "form_type": "Обращение",
            "name": faker.name(),
        }

        response: Response = client.post(url=url, json=data)

        assert response.is_success
        assert response.status_code == status.HTTP_201_CREATED

        json_response = response.json()

        assert "data" in json_response
        assert json_response["data"]["form_type"] == data["form_type"]
        assert json_response["data"]["name"] == data["name"]
        assert json_response["data"]["email"] is None
        assert json_response["data"]["phone"] is None


@pytest.mark.asyncio
async def test_create_submission_invalid_form_type(client: TestClient, faker: Faker):
    """Тест создания заявки с невалидным типом формы."""
    url = "/api/v1/submissions"

    data = {
        "form_type": "Невалидный тип",
        "name": faker.name(),
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_submission_invalid_email(client: TestClient, faker: Faker):
    """Тест создания заявки с невалидным email."""
    url = "/api/v1/submissions"

    data = {
        "form_type": "Обращение",
        "name": faker.name(),
        "email": "invalid-email",
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_submission_empty_name(client: TestClient):
    """Тест создания заявки с пустым именем."""
    url = "/api/v1/submissions"

    data = {
        "form_type": "Обращение",
        "name": "",
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_get_submission_by_id_success(
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения заявки по ID."""
    data = {
        "form_type": "Опросный лист",
        "name": faker.name(),
        "email": faker.email(),
        "questionnaire_type": "КТП",
    }

    request_schema = SubmissionRequestSchema(**data)
    submission = request_schema.to_entity()
    result, *_ = await mediator.handle_command(CreateSubmissionCommand(submission=submission))
    submission_id = result.oid

    url = f"/api/v1/submissions/{submission_id}"

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["oid"] == str(submission_id)
    assert json_response["data"]["form_type"] == data["form_type"]
    assert json_response["data"]["name"] == data["name"]


@pytest.mark.asyncio
async def test_get_submission_by_id_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения заявки по несуществующему ID."""
    non_existent_id = uuid4()
    url = f"/api/v1/submissions/{non_existent_id}"

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_get_submissions_list_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения списка заявок."""
    url = "/api/v1/submissions"

    for _ in range(3):
        data = {
            "form_type": "Опросный лист",
            "name": faker.name(),
            "email": faker.email(),
        }
        request_schema = SubmissionRequestSchema(**data)
        submission = request_schema.to_entity()
        await mediator.handle_command(CreateSubmissionCommand(submission=submission))

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert "items" in json_response["data"]
    assert "pagination" in json_response["data"]
    assert len(json_response["data"]["items"]) == 3
    assert json_response["data"]["pagination"]["total"] == 3


@pytest.mark.asyncio
async def test_get_submissions_list_with_pagination(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка заявок с пагинацией."""
    url = "/api/v1/submissions"

    for _ in range(5):
        data = {
            "form_type": "Обращение",
            "name": faker.name(),
            "email": faker.email(),
        }
        request_schema = SubmissionRequestSchema(**data)
        submission = request_schema.to_entity()
        await mediator.handle_command(CreateSubmissionCommand(submission=submission))

    response: Response = client.get(url=url, params={"limit": 2, "offset": 0})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["limit"] == 2
    assert json_response["data"]["pagination"]["offset"] == 0
    assert json_response["data"]["pagination"]["total"] == 5


@pytest.mark.asyncio
async def test_get_submissions_list_with_form_type_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка заявок с фильтром по типу формы."""
    url = "/api/v1/submissions"

    for _ in range(3):
        data = {
            "form_type": "Опросный лист",
            "name": faker.name(),
            "email": faker.email(),
        }
        request_schema = SubmissionRequestSchema(**data)
        submission = request_schema.to_entity()
        await mediator.handle_command(CreateSubmissionCommand(submission=submission))

    for _ in range(2):
        data = {
            "form_type": "Обращение",
            "name": faker.name(),
            "email": faker.email(),
        }
        request_schema = SubmissionRequestSchema(**data)
        submission = request_schema.to_entity()
        await mediator.handle_command(CreateSubmissionCommand(submission=submission))

    response: Response = client.get(url=url, params={"form_type": "Опросный лист"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 3
    assert all(item["form_type"] == "Опросный лист" for item in json_response["data"]["items"])


@pytest.mark.asyncio
async def test_delete_submission_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного удаления заявки."""
    data = {
        "form_type": "Обращение",
        "name": faker.name(),
        "email": faker.email(),
    }

    request_schema = SubmissionRequestSchema(**data)
    submission = request_schema.to_entity()
    result, *_ = await mediator.handle_command(CreateSubmissionCommand(submission=submission))
    submission_id = result.oid

    url = f"/api/v1/submissions/{submission_id}"

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_url = f"/api/v1/submissions/{submission_id}"
    get_response: Response = authenticated_client.get(url=get_url)

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_submission_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест удаления заявки без аутентификации."""
    data = {
        "form_type": "Обращение",
        "name": faker.name(),
        "email": faker.email(),
    }

    request_schema = SubmissionRequestSchema(**data)
    submission = request_schema.to_entity()
    result, *_ = await mediator.handle_command(CreateSubmissionCommand(submission=submission))
    submission_id = result.oid

    url = f"/api/v1/submissions/{submission_id}"

    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_submission_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест удаления несуществующей заявки."""
    non_existent_id = uuid4()
    url = f"/api/v1/submissions/{non_existent_id}"

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0
