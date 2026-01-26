from uuid import uuid4

from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from faker import Faker
from httpx import Response

from application.mediator import Mediator
from application.vacancies.commands import CreateVacancyCommand
from presentation.api.v1.vacancies.schemas import VacancyRequestSchema


@pytest.mark.asyncio
async def test_get_vacancies_list_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения списка вакансий."""
    url = app.url_path_for("get_vacancies_list")

    for _ in range(3):
        data = {
            "title": faker.job(),
            "requirements": [
                faker.sentence(nb_words=5),
                faker.sentence(nb_words=6),
            ],
            "experience": [
                faker.sentence(nb_words=4),
            ],
            "salary": faker.random_int(min=30000, max=200000),
            "category": "Производство",
        }
        request_schema = VacancyRequestSchema(**data)
        await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema.to_entity()))

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
async def test_get_vacancies_list_with_pagination(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка вакансий с пагинацией."""
    url = app.url_path_for("get_vacancies_list")

    for _ in range(5):
        data = {
            "title": faker.job(),
            "requirements": [
                faker.sentence(nb_words=5),
            ],
            "experience": [
                faker.sentence(nb_words=4),
            ],
            "salary": faker.random_int(min=30000, max=200000),
            "category": "Производство",
        }
        request_schema = VacancyRequestSchema(**data)
        await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"limit": 2, "offset": 0})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["limit"] == 2
    assert json_response["data"]["pagination"]["offset"] == 0


@pytest.mark.asyncio
async def test_get_vacancies_list_with_category_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка вакансий с фильтром по категории."""
    url = app.url_path_for("get_vacancies_list")

    for _ in range(3):
        data = {
            "title": faker.job(),
            "requirements": [
                faker.sentence(nb_words=5),
            ],
            "experience": [
                faker.sentence(nb_words=4),
            ],
            "salary": faker.random_int(min=30000, max=200000),
            "category": "Производство",
        }
        request_schema = VacancyRequestSchema(**data)
        await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema.to_entity()))

    for _ in range(2):
        data = {
            "title": faker.job(),
            "requirements": [
                faker.sentence(nb_words=5),
            ],
            "experience": [
                faker.sentence(nb_words=4),
            ],
            "salary": faker.random_int(min=30000, max=200000),
            "category": "Продажи и маркетинг",
        }
        request_schema = VacancyRequestSchema(**data)
        await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"category": "Производство"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 3
    assert all(item["category"] == "Производство" for item in json_response["data"]["items"])


@pytest.mark.asyncio
async def test_get_vacancies_list_with_search(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка вакансий с поиском."""
    url = app.url_path_for("get_vacancies_list")

    data1 = {
        "title": "Python Developer",
        "requirements": [
            faker.sentence(nb_words=5),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }
    request_schema1 = VacancyRequestSchema(**data1)
    await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema1.to_entity()))

    data2 = {
        "title": "JavaScript Developer",
        "requirements": [
            faker.sentence(nb_words=5),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }
    request_schema2 = VacancyRequestSchema(**data2)
    await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema2.to_entity()))

    response: Response = client.get(url=url, params={"search": "Python"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 1
    assert "Python" in json_response["data"]["items"][0]["title"]


@pytest.mark.asyncio
async def test_get_vacancy_by_id_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения вакансии по ID."""
    data = {
        "title": faker.job(),
        "requirements": [
            faker.sentence(nb_words=5),
            faker.sentence(nb_words=6),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }

    request_schema = VacancyRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema.to_entity()))
    vacancy_id = result.oid

    url = app.url_path_for("get_vacancy_by_id", vacancy_id=vacancy_id)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["oid"] == str(vacancy_id)
    assert json_response["data"]["title"] == data["title"]
    assert json_response["data"]["category"] == data["category"]


@pytest.mark.asyncio
async def test_get_vacancy_by_id_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения вакансии по несуществующему ID."""
    non_existent_id = uuid4()
    url = app.url_path_for("get_vacancy_by_id", vacancy_id=non_existent_id)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_vacancy_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест успешного создания вакансии."""
    url = app.url_path_for("create_vacancy")

    data = {
        "title": faker.job(),
        "requirements": [
            faker.sentence(nb_words=5),
            faker.sentence(nb_words=6),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["title"] == data["title"]
    assert json_response["data"]["category"] == data["category"]
    assert json_response["data"]["requirements"] == data["requirements"]
    assert json_response["data"]["experience"] == data["experience"]
    assert json_response["data"]["salary"] == data["salary"]
    assert "oid" in json_response["data"]


@pytest.mark.asyncio
async def test_create_vacancy_unauthorized(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    """Тест создания вакансии без аутентификации."""
    url = app.url_path_for("create_vacancy")

    data = {
        "title": faker.job(),
        "requirements": [
            faker.sentence(nb_words=5),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_vacancy_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления вакансии."""
    data = {
        "title": faker.job(),
        "requirements": [
            faker.sentence(nb_words=5),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }

    request_schema = VacancyRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema.to_entity()))
    vacancy_id = result.oid

    url = app.url_path_for("update_vacancy", vacancy_id=vacancy_id)

    update_data = data.copy()
    update_data["title"] = "Updated Title"
    update_data["salary"] = 150000

    response: Response = authenticated_client.put(url=url, json=update_data)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["title"] == "Updated Title"
    assert json_response["data"]["salary"] == 150000
    assert json_response["data"]["oid"] == str(vacancy_id)


@pytest.mark.asyncio
async def test_update_vacancy_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления вакансии без аутентификации."""
    data = {
        "title": faker.job(),
        "requirements": [
            faker.sentence(nb_words=5),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }

    request_schema = VacancyRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema.to_entity()))
    vacancy_id = result.oid

    url = app.url_path_for("update_vacancy", vacancy_id=vacancy_id)

    response: Response = client.put(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_vacancy_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест обновления несуществующей вакансии."""
    non_existent_id = uuid4()
    url = app.url_path_for("update_vacancy", vacancy_id=non_existent_id)

    data = {
        "title": faker.job(),
        "requirements": [
            faker.sentence(nb_words=5),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }

    response: Response = authenticated_client.put(url=url, json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_vacancy_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного удаления вакансии."""
    data = {
        "title": faker.job(),
        "requirements": [
            faker.sentence(nb_words=5),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }

    request_schema = VacancyRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema.to_entity()))
    vacancy_id = result.oid

    url = app.url_path_for("delete_vacancy", vacancy_id=vacancy_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_url = app.url_path_for("get_vacancy_by_id", vacancy_id=vacancy_id)
    get_response: Response = authenticated_client.get(url=get_url)

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_vacancy_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест удаления вакансии без аутентификации."""
    data = {
        "title": faker.job(),
        "requirements": [
            faker.sentence(nb_words=5),
        ],
        "experience": [
            faker.sentence(nb_words=4),
        ],
        "salary": faker.random_int(min=30000, max=200000),
        "category": "Производство",
    }

    request_schema = VacancyRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateVacancyCommand(vacancy=request_schema.to_entity()))
    vacancy_id = result.oid

    url = app.url_path_for("delete_vacancy", vacancy_id=vacancy_id)

    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_vacancy_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест удаления несуществующей вакансии."""
    non_existent_id = uuid4()
    url = app.url_path_for("delete_vacancy", vacancy_id=non_existent_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0
