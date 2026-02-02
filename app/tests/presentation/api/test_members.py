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
from application.members.commands import CreateMemberCommand
from presentation.api.v1.members.schemas import MemberRequestSchema


@pytest.mark.asyncio
async def test_get_members_list_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения списка членов команды."""
    url = app.url_path_for("get_members_list")

    for i in range(3):
        data = {
            "name": faker.name(),
            "position": faker.job(),
            "image": f"member-{i}.jpg",
            "order": i + 1,
            "email": faker.email(),
        }
        request_schema = MemberRequestSchema(**data)
        await mediator.handle_command(CreateMemberCommand(member=request_schema.to_entity()))

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
async def test_get_members_list_with_pagination(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка членов с пагинацией."""
    url = app.url_path_for("get_members_list")

    for i in range(5):
        data = {
            "name": faker.name(),
            "position": faker.job(),
            "image": f"member-{i}.jpg",
            "order": i + 1,
        }
        request_schema = MemberRequestSchema(**data)
        await mediator.handle_command(CreateMemberCommand(member=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"limit": 2, "offset": 0})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["limit"] == 2
    assert json_response["data"]["pagination"]["offset"] == 0
    assert json_response["data"]["pagination"]["total"] == 5


@pytest.mark.asyncio
async def test_get_member_by_id_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения члена команды по ID."""
    data = {
        "name": "Иван Иванов",
        "position": "Генеральный директор",
        "image": "team-member-1.jpg",
        "order": 1,
        "email": "ivan@example.com",
    }
    request_schema = MemberRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateMemberCommand(member=request_schema.to_entity()))
    member_id = result.oid

    url = app.url_path_for("get_member_by_id", member_id=member_id)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert "data" in json_response
    assert json_response["data"]["oid"] == str(member_id)
    assert json_response["data"]["name"] == data["name"]
    assert json_response["data"]["position"] == data["position"]
    assert json_response["data"]["email"] == data["email"]


@pytest.mark.asyncio
async def test_get_member_by_id_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения члена команды по несуществующему ID."""
    non_existent_id = uuid4()
    url = app.url_path_for("get_member_by_id", member_id=non_existent_id)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_member_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест успешного создания члена команды."""
    url = app.url_path_for("create_member")

    data = {
        "name": faker.name(),
        "position": faker.job(),
        "image": "member.jpg",
        "order": 1,
        "email": faker.email(),
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()
    assert "data" in json_response
    assert json_response["data"]["name"] == data["name"]
    assert json_response["data"]["position"] == data["position"]
    assert json_response["data"]["image"] == data["image"]
    assert json_response["data"]["order"] == data["order"]
    assert json_response["data"]["email"] == data["email"]
    assert "oid" in json_response["data"]


@pytest.mark.asyncio
async def test_create_member_without_email_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест создания члена команды без email."""
    url = app.url_path_for("create_member")

    data = {
        "name": faker.name(),
        "position": faker.job(),
        "image": "member.jpg",
        "order": 1,
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()
    assert json_response["data"]["email"] is None


@pytest.mark.asyncio
async def test_create_member_unauthorized(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    """Тест создания члена команды без аутентификации."""
    url = app.url_path_for("create_member")

    data = {
        "name": faker.name(),
        "position": faker.job(),
        "image": "member.jpg",
        "order": 1,
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_member_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления члена команды."""
    data = {
        "name": faker.name(),
        "position": faker.job(),
        "image": "member.jpg",
        "order": 1,
        "email": faker.email(),
    }
    request_schema = MemberRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateMemberCommand(member=request_schema.to_entity()))
    member_id = result.oid

    url = app.url_path_for("update_member", member_id=member_id)

    update_data = {
        "name": "Обновленное Имя",
        "position": "Директор",
        "image": "updated.jpg",
        "order": 5,
        "email": "updated@example.com",
    }

    response: Response = authenticated_client.put(url=url, json=update_data)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert json_response["data"]["name"] == "Обновленное Имя"
    assert json_response["data"]["position"] == "Директор"
    assert json_response["data"]["order"] == 5
    assert json_response["data"]["oid"] == str(member_id)


@pytest.mark.asyncio
async def test_update_member_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления члена команды без аутентификации."""
    data = {
        "name": faker.name(),
        "position": faker.job(),
        "image": "member.jpg",
        "order": 1,
    }
    request_schema = MemberRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateMemberCommand(member=request_schema.to_entity()))
    member_id = result.oid

    url = app.url_path_for("update_member", member_id=member_id)

    response: Response = client.put(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_member_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест обновления несуществующего члена команды."""
    non_existent_id = uuid4()
    url = app.url_path_for("update_member", member_id=non_existent_id)

    data = {
        "name": faker.name(),
        "position": faker.job(),
        "image": "member.jpg",
        "order": 1,
    }

    response: Response = authenticated_client.put(url=url, json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_patch_member_order_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления порядка члена команды."""
    data = {
        "name": faker.name(),
        "position": faker.job(),
        "image": "member.jpg",
        "order": 1,
    }
    request_schema = MemberRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateMemberCommand(member=request_schema.to_entity()))
    member_id = result.oid

    url = app.url_path_for("patch_member_order", member_id=member_id)

    response: Response = authenticated_client.patch(url=url, json={"order": 10})

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert json_response["data"]["oid"] == str(member_id)
    assert json_response["data"]["order"] == 10


@pytest.mark.asyncio
async def test_patch_member_order_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления порядка члена команды без аутентификации."""
    data = {
        "name": faker.name(),
        "position": faker.job(),
        "image": "member.jpg",
        "order": 1,
    }
    request_schema = MemberRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateMemberCommand(member=request_schema.to_entity()))
    member_id = result.oid

    url = app.url_path_for("patch_member_order", member_id=member_id)

    response: Response = client.patch(url=url, json={"order": 5})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_patch_member_order_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест обновления порядка несуществующего члена команды."""
    non_existent_id = uuid4()
    url = app.url_path_for("patch_member_order", member_id=non_existent_id)

    response: Response = authenticated_client.patch(url=url, json={"order": 1})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_member_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного удаления члена команды."""
    data = {
        "name": faker.name(),
        "position": faker.job(),
        "image": "member.jpg",
        "order": 1,
    }
    request_schema = MemberRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateMemberCommand(member=request_schema.to_entity()))
    member_id = result.oid

    url = app.url_path_for("delete_member", member_id=member_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_url = app.url_path_for("get_member_by_id", member_id=member_id)
    get_response: Response = authenticated_client.get(url=get_url)

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_member_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест удаления члена команды без аутентификации."""
    data = {
        "name": faker.name(),
        "position": faker.job(),
        "image": "member.jpg",
        "order": 1,
    }
    request_schema = MemberRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateMemberCommand(member=request_schema.to_entity()))
    member_id = result.oid

    url = app.url_path_for("delete_member", member_id=member_id)

    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_member_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест удаления несуществующего члена команды."""
    non_existent_id = uuid4()
    url = app.url_path_for("delete_member", member_id=non_existent_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0
