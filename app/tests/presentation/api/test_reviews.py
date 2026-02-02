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
from application.reviews.commands import CreateReviewCommand
from presentation.api.v1.reviews.schemas import ReviewRequestSchema


@pytest.mark.asyncio
async def test_get_reviews_list_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    url = app.url_path_for("get_reviews_list")

    for i in range(3):
        data = {
            "name": faker.name(),
            "category": "Сотрудники",
            "position": faker.job(),
            "image": f"review-{i}.jpg",
            "text": "Полный отзыв",
            "short_text": "Короткий отзыв",
        }
        request_schema = ReviewRequestSchema(**data)
        await mediator.handle_command(CreateReviewCommand(review=request_schema.to_entity()))

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
async def test_get_reviews_list_with_pagination(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    url = app.url_path_for("get_reviews_list")

    for i in range(5):
        data = {
            "name": faker.name(),
            "category": "Сотрудники",
            "position": faker.job(),
            "text": "Текст",
            "short_text": "Короткий",
        }
        request_schema = ReviewRequestSchema(**data)
        await mediator.handle_command(CreateReviewCommand(review=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"limit": 2, "offset": 0})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["limit"] == 2
    assert json_response["data"]["pagination"]["offset"] == 0
    assert json_response["data"]["pagination"]["total"] == 5


@pytest.mark.asyncio
async def test_get_reviews_list_with_category_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    url = app.url_path_for("get_reviews_list")

    for _ in range(2):
        data = {
            "name": faker.name(),
            "category": "Сотрудники",
            "text": "Текст",
            "short_text": "Короткий",
        }
        request_schema = ReviewRequestSchema(**data)
        await mediator.handle_command(CreateReviewCommand(review=request_schema.to_entity()))

    data_client = {
        "name": faker.company(),
        "category": "Клиенты",
        "content_url": "https://example.com/review",
    }
    request_schema = ReviewRequestSchema(**data_client)
    await mediator.handle_command(CreateReviewCommand(review=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"category": "Сотрудники"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["total"] == 2
    assert all(item["category"] == "Сотрудники" for item in json_response["data"]["items"])


@pytest.mark.asyncio
async def test_get_review_by_id_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    data = {
        "name": "Иван Иванов",
        "category": "Сотрудники",
        "position": "Инженер",
        "image": "review-1.jpg",
        "text": "Полный отзыв...",
        "short_text": "Короткий отзыв",
    }
    request_schema = ReviewRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateReviewCommand(review=request_schema.to_entity()))
    review_id = result.oid

    url = app.url_path_for("get_review_by_id", review_id=review_id)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert "data" in json_response
    assert json_response["data"]["oid"] == str(review_id)
    assert json_response["data"]["name"] == data["name"]
    assert json_response["data"]["category"] == data["category"]
    assert json_response["data"]["position"] == data["position"]
    assert json_response["data"]["text"] == data["text"]
    assert json_response["data"]["short_text"] == data["short_text"]


@pytest.mark.asyncio
async def test_get_review_by_id_not_found(
    app: FastAPI,
    client: TestClient,
):
    non_existent_id = uuid4()
    url = app.url_path_for("get_review_by_id", review_id=non_existent_id)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_review_employee_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    url = app.url_path_for("create_review")

    data = {
        "name": faker.name(),
        "category": "Сотрудники",
        "position": faker.job(),
        "image": "review.jpg",
        "text": "Полный отзыв сотрудника",
        "short_text": "Короткий отзыв",
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()
    assert "data" in json_response
    assert json_response["data"]["name"] == data["name"]
    assert json_response["data"]["category"] == data["category"]
    assert json_response["data"]["position"] == data["position"]
    assert json_response["data"]["text"] == data["text"]
    assert json_response["data"]["short_text"] == data["short_text"]
    assert "oid" in json_response["data"]


@pytest.mark.asyncio
async def test_create_review_client_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    url = app.url_path_for("create_review")

    data = {
        "name": faker.company(),
        "category": "Клиенты",
        "content_url": "https://example.com/review",
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()
    assert json_response["data"]["category"] == "Клиенты"
    assert json_response["data"]["content_url"] == data["content_url"]
    assert json_response["data"]["text"] is None
    assert json_response["data"]["short_text"] is None


@pytest.mark.asyncio
async def test_create_review_unauthorized(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for("create_review")

    data = {
        "name": faker.name(),
        "category": "Сотрудники",
        "text": "Текст",
        "short_text": "Короткий",
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_review_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    data = {
        "name": faker.name(),
        "category": "Сотрудники",
        "position": faker.job(),
        "text": "Текст",
        "short_text": "Короткий",
    }
    request_schema = ReviewRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateReviewCommand(review=request_schema.to_entity()))
    review_id = result.oid

    url = app.url_path_for("update_review", review_id=review_id)

    update_data = {
        "name": "Обновленное Имя",
        "category": "Сотрудники",
        "position": "Директор",
        "text": "Новый текст",
        "short_text": "Новый короткий",
    }

    response: Response = authenticated_client.put(url=url, json=update_data)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert json_response["data"]["name"] == "Обновленное Имя"
    assert json_response["data"]["position"] == "Директор"
    assert json_response["data"]["oid"] == str(review_id)


@pytest.mark.asyncio
async def test_update_review_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    data = {
        "name": faker.name(),
        "category": "Сотрудники",
        "text": "Текст",
        "short_text": "Короткий",
    }
    request_schema = ReviewRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateReviewCommand(review=request_schema.to_entity()))
    review_id = result.oid

    url = app.url_path_for("update_review", review_id=review_id)

    response: Response = client.put(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_review_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    non_existent_id = uuid4()
    url = app.url_path_for("update_review", review_id=non_existent_id)

    data = {
        "name": faker.name(),
        "category": "Сотрудники",
        "text": "Текст",
        "short_text": "Короткий",
    }

    response: Response = authenticated_client.put(url=url, json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_review_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    data = {
        "name": faker.name(),
        "category": "Сотрудники",
        "text": "Текст",
        "short_text": "Короткий",
    }
    request_schema = ReviewRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateReviewCommand(review=request_schema.to_entity()))
    review_id = result.oid

    url = app.url_path_for("delete_review", review_id=review_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_url = app.url_path_for("get_review_by_id", review_id=review_id)
    get_response: Response = authenticated_client.get(url=get_url)

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_review_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    data = {
        "name": faker.name(),
        "category": "Сотрудники",
        "text": "Текст",
        "short_text": "Короткий",
    }
    request_schema = ReviewRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateReviewCommand(review=request_schema.to_entity()))
    review_id = result.oid

    url = app.url_path_for("delete_review", review_id=review_id)

    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_review_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    non_existent_id = uuid4()
    url = app.url_path_for("delete_review", review_id=non_existent_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0
