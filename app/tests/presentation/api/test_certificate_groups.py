from uuid import uuid4

from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from faker import Faker
from httpx import Response

from application.certificates.commands import (
    CreateCertificateCommand,
    CreateCertificateGroupCommand,
)
from application.mediator import Mediator
from presentation.api.v1.certificates.schemas import (
    CertificateGroupRequestSchema,
    CertificateRequestSchema,
)


@pytest.mark.asyncio
async def test_get_certificate_groups_list_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения списка групп сертификатов."""
    url = app.url_path_for("get_certificate_groups_list")

    for _ in range(3):
        data = {
            "section": "Сертификаты",
            "title": faker.sentence(nb_words=5),
            "content": faker.text(max_nb_chars=500),
        }
        request_schema = CertificateGroupRequestSchema(**data)
        await mediator.handle_command(CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()))

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
async def test_get_certificate_groups_list_with_pagination(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка групп сертификатов с пагинацией."""
    url = app.url_path_for("get_certificate_groups_list")

    for _ in range(5):
        data = {
            "section": "Сертификаты",
            "title": faker.sentence(nb_words=5),
            "content": faker.text(max_nb_chars=500),
        }
        request_schema = CertificateGroupRequestSchema(**data)
        await mediator.handle_command(CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"limit": 2, "offset": 0})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["limit"] == 2
    assert json_response["data"]["pagination"]["offset"] == 0


@pytest.mark.asyncio
async def test_get_certificate_groups_list_with_section_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка групп сертификатов с фильтром по секции."""
    url = app.url_path_for("get_certificate_groups_list")

    for _ in range(3):
        data = {
            "section": "Сертификаты",
            "title": faker.sentence(nb_words=5),
            "content": faker.text(max_nb_chars=500),
        }
        request_schema = CertificateGroupRequestSchema(**data)
        await mediator.handle_command(CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()))

    for _ in range(2):
        data = {
            "section": "Декларации",
            "title": faker.sentence(nb_words=5),
            "content": faker.text(max_nb_chars=500),
        }
        request_schema = CertificateGroupRequestSchema(**data)
        await mediator.handle_command(CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"section": "Сертификаты"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 3
    assert all(item["section"] == "Сертификаты" for item in json_response["data"]["items"])


@pytest.mark.asyncio
async def test_get_certificate_groups_list_with_is_active_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка групп сертификатов с фильтром по активности."""
    url = app.url_path_for("get_certificate_groups_list")

    for _ in range(3):
        data = {
            "section": "Сертификаты",
            "title": faker.sentence(nb_words=5),
            "content": faker.text(max_nb_chars=500),
            "is_active": True,
        }
        request_schema = CertificateGroupRequestSchema(**data)
        await mediator.handle_command(CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()))

    for _ in range(2):
        data = {
            "section": "Сертификаты",
            "title": faker.sentence(nb_words=5),
            "content": faker.text(max_nb_chars=500),
            "is_active": False,
        }
        request_schema = CertificateGroupRequestSchema(**data)
        await mediator.handle_command(CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"is_active": True})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 3
    assert all(item["is_active"] is True for item in json_response["data"]["items"])


@pytest.mark.asyncio
async def test_get_certificate_groups_list_with_search(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка групп сертификатов с поиском."""
    url = app.url_path_for("get_certificate_groups_list")

    data1 = {
        "section": "Сертификаты",
        "title": "Python Certificate Group",
        "content": faker.text(max_nb_chars=500),
    }
    request_schema1 = CertificateGroupRequestSchema(**data1)
    await mediator.handle_command(CreateCertificateGroupCommand(certificate_group=request_schema1.to_entity()))

    data2 = {
        "section": "Сертификаты",
        "title": "JavaScript Certificate Group",
        "content": faker.text(max_nb_chars=500),
    }
    request_schema2 = CertificateGroupRequestSchema(**data2)
    await mediator.handle_command(CreateCertificateGroupCommand(certificate_group=request_schema2.to_entity()))

    response: Response = client.get(url=url, params={"search": "Python"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 1
    assert "Python" in json_response["data"]["items"][0]["title"]


@pytest.mark.asyncio
async def test_get_certificate_group_by_id_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения группы сертификатов по ID."""
    data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }

    request_schema = CertificateGroupRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()),
    )
    certificate_group_id = result.oid

    url = app.url_path_for("get_certificate_group_by_id", certificate_group_id=certificate_group_id)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["oid"] == str(certificate_group_id)
    assert json_response["data"]["title"] == data["title"]
    assert json_response["data"]["section"] == data["section"]


@pytest.mark.asyncio
async def test_get_certificate_group_by_id_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения группы сертификатов по несуществующему ID."""
    non_existent_id = uuid4()
    url = app.url_path_for("get_certificate_group_by_id", certificate_group_id=non_existent_id)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_certificate_group_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест успешного создания группы сертификатов."""
    url = app.url_path_for("create_certificate_group")

    data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["title"] == data["title"]
    assert json_response["data"]["section"] == data["section"]
    assert "oid" in json_response["data"]


@pytest.mark.asyncio
async def test_create_certificate_group_unauthorized(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    """Тест создания группы сертификатов без аутентификации."""
    url = app.url_path_for("create_certificate_group")

    data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_certificate_group_duplicate_title(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест создания группы сертификатов с дублирующимся названием."""
    url = app.url_path_for("create_certificate_group")
    title = faker.sentence(nb_words=5)

    data = {
        "section": "Сертификаты",
        "title": title,
        "content": faker.text(max_nb_chars=500),
    }

    request_schema = CertificateGroupRequestSchema(**data)
    await mediator.handle_command(CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()))

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.status_code == status.HTTP_409_CONFLICT
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_certificate_group_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления группы сертификатов."""
    data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }

    request_schema = CertificateGroupRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()),
    )
    certificate_group_id = result.oid

    url = app.url_path_for("update_certificate_group", certificate_group_id=certificate_group_id)

    update_data = {
        "section": data["section"],
        "title": "Updated Title",
        "content": data["content"],
    }

    response: Response = authenticated_client.put(url=url, json=update_data)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["title"] == "Updated Title"
    assert json_response["data"]["oid"] == str(certificate_group_id)


@pytest.mark.asyncio
async def test_update_certificate_group_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления группы сертификатов без аутентификации."""
    data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }

    request_schema = CertificateGroupRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()),
    )
    certificate_group_id = result.oid

    url = app.url_path_for("update_certificate_group", certificate_group_id=certificate_group_id)

    response: Response = client.put(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_certificate_group_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест обновления несуществующей группы сертификатов."""
    non_existent_id = uuid4()
    url = app.url_path_for("update_certificate_group", certificate_group_id=non_existent_id)

    data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }

    response: Response = authenticated_client.put(url=url, json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_patch_certificate_group_order_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления порядка группы сертификатов."""
    data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }

    request_schema = CertificateGroupRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()),
    )
    certificate_group_id = result.oid

    url = app.url_path_for("patch_certificate_group_order", certificate_group_id=certificate_group_id)

    response: Response = authenticated_client.patch(url=url, json={"order": 10})

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert "data" in json_response
    assert json_response["data"]["oid"] == str(certificate_group_id)
    assert json_response["data"]["order"] == 10


@pytest.mark.asyncio
async def test_patch_certificate_group_order_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления порядка группы сертификатов без аутентификации."""
    data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }

    request_schema = CertificateGroupRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()),
    )
    certificate_group_id = result.oid

    url = app.url_path_for("patch_certificate_group_order", certificate_group_id=certificate_group_id)

    response: Response = client.patch(url=url, json={"order": 5})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_patch_certificate_group_order_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест обновления порядка несуществующей группы сертификатов."""
    non_existent_id = uuid4()
    url = app.url_path_for("patch_certificate_group_order", certificate_group_id=non_existent_id)

    response: Response = authenticated_client.patch(url=url, json={"order": 1})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_certificate_group_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного удаления группы сертификатов."""
    data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }

    request_schema = CertificateGroupRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()),
    )
    certificate_group_id = result.oid

    url = app.url_path_for("delete_certificate_group", certificate_group_id=certificate_group_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_url = app.url_path_for("get_certificate_group_by_id", certificate_group_id=certificate_group_id)
    get_response: Response = authenticated_client.get(url=get_url)

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_certificate_group_deletes_its_certificates(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест: при удалении группы сертификатов удаляются и все её
    сертификаты."""
    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    certificate_group_id = group_result.oid

    cert_ids = []
    for _ in range(2):
        cert_data = {
            "title": faker.sentence(nb_words=3),
            "link": faker.url(),
            "order": 0,
        }
        cert_schema = CertificateRequestSchema(**cert_data)
        cert_result, *_ = await mediator.handle_command(
            CreateCertificateCommand(
                certificate=cert_schema.to_entity(),
                certificate_group_id=certificate_group_id,
            ),
        )
        cert_ids.append(cert_result.oid)

    url = app.url_path_for("delete_certificate_group", certificate_group_id=certificate_group_id)
    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    for certificate_id in cert_ids:
        get_cert_url = app.url_path_for("get_certificate_by_id", certificate_id=certificate_id)
        get_response: Response = authenticated_client.get(url=get_cert_url)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_certificate_group_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест удаления группы сертификатов без аутентификации."""
    data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }

    request_schema = CertificateGroupRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=request_schema.to_entity()),
    )
    certificate_group_id = result.oid

    url = app.url_path_for("delete_certificate_group", certificate_group_id=certificate_group_id)

    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_certificate_group_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест удаления несуществующей группы сертификатов."""
    non_existent_id = uuid4()
    url = app.url_path_for("delete_certificate_group", certificate_group_id=non_existent_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0
