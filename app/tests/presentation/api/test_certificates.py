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
async def test_get_certificates_list_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения списка сертификатов."""
    url = app.url_path_for("get_certificates_list")

    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    for _ in range(3):
        data = {
            "title": faker.sentence(nb_words=3),
            "link": faker.url(),
            "order": faker.random_int(min=0, max=100),
        }
        request_schema = CertificateRequestSchema(**data)
        await mediator.handle_command(
            CreateCertificateCommand(
                certificate=request_schema.to_entity(),
                certificate_group_id=group_id,
            ),
        )

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
async def test_get_certificates_list_with_pagination(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка сертификатов с пагинацией."""
    url = app.url_path_for("get_certificates_list")

    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    for _ in range(5):
        data = {
            "title": faker.sentence(nb_words=3),
            "link": faker.url(),
            "order": faker.random_int(min=0, max=100),
        }
        request_schema = CertificateRequestSchema(**data)
        await mediator.handle_command(
            CreateCertificateCommand(
                certificate=request_schema.to_entity(),
                certificate_group_id=group_id,
            ),
        )

    response: Response = client.get(url=url, params={"limit": 2, "offset": 0})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["limit"] == 2
    assert json_response["data"]["pagination"]["offset"] == 0


@pytest.mark.asyncio
async def test_get_certificates_list_with_certificate_group_id_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка сертификатов с фильтром по группе."""
    url = app.url_path_for("get_certificates_list")

    group_data1 = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema1 = CertificateGroupRequestSchema(**group_data1)
    group_result1, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema1.to_entity()),
    )
    group_id1 = group_result1.oid

    group_data2 = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema2 = CertificateGroupRequestSchema(**group_data2)
    group_result2, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema2.to_entity()),
    )
    group_id2 = group_result2.oid

    for _ in range(3):
        data = {
            "title": faker.sentence(nb_words=3),
            "link": faker.url(),
            "order": faker.random_int(min=0, max=100),
        }
        request_schema = CertificateRequestSchema(**data)
        await mediator.handle_command(
            CreateCertificateCommand(
                certificate=request_schema.to_entity(),
                certificate_group_id=group_id1,
            ),
        )

    for _ in range(2):
        data = {
            "title": faker.sentence(nb_words=3),
            "link": faker.url(),
            "order": faker.random_int(min=0, max=100),
        }
        request_schema = CertificateRequestSchema(**data)
        await mediator.handle_command(
            CreateCertificateCommand(
                certificate=request_schema.to_entity(),
                certificate_group_id=group_id2,
            ),
        )

    response: Response = client.get(url=url, params={"certificate_group_id": str(group_id1)})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 3


@pytest.mark.asyncio
async def test_get_certificates_list_with_search(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка сертификатов с поиском."""
    url = app.url_path_for("get_certificates_list")

    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    data1 = {
        "title": "Python Certificate",
        "link": faker.url(),
        "order": 1,
    }
    request_schema1 = CertificateRequestSchema(**data1)
    await mediator.handle_command(
        CreateCertificateCommand(
            certificate=request_schema1.to_entity(),
            certificate_group_id=group_id,
        ),
    )

    data2 = {
        "title": "JavaScript Certificate",
        "link": faker.url(),
        "order": 2,
    }
    request_schema2 = CertificateRequestSchema(**data2)
    await mediator.handle_command(
        CreateCertificateCommand(
            certificate=request_schema2.to_entity(),
            certificate_group_id=group_id,
        ),
    )

    response: Response = client.get(url=url, params={"search": "Python"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 1
    assert "Python" in json_response["data"]["items"][0]["title"]


@pytest.mark.asyncio
async def test_get_certificate_by_id_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения сертификата по ID."""
    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    data = {
        "title": faker.sentence(nb_words=3),
        "link": faker.url(),
        "order": faker.random_int(min=0, max=100),
    }

    request_schema = CertificateRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=request_schema.to_entity(),
            certificate_group_id=group_id,
        ),
    )
    certificate_id = result.oid

    url = app.url_path_for("get_certificate_by_id", certificate_id=certificate_id)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["oid"] == str(certificate_id)
    assert json_response["data"]["title"] == data["title"]
    assert json_response["data"]["link"] == data["link"]


@pytest.mark.asyncio
async def test_get_certificate_by_id_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения сертификата по несуществующему ID."""
    non_existent_id = uuid4()
    url = app.url_path_for("get_certificate_by_id", certificate_id=non_existent_id)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_certificate_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного создания сертификата."""
    url = app.url_path_for("create_certificate")

    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    data = {
        "title": faker.sentence(nb_words=3),
        "link": faker.url(),
        "order": faker.random_int(min=0, max=100),
    }

    response: Response = authenticated_client.post(url=url, json=data, params={"certificate_group_id": str(group_id)})

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["title"] == data["title"]
    assert json_response["data"]["link"] == data["link"]
    assert "oid" in json_response["data"]


@pytest.mark.asyncio
async def test_create_certificate_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест создания сертификата без аутентификации."""
    url = app.url_path_for("create_certificate")

    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    data = {
        "title": faker.sentence(nb_words=3),
        "link": faker.url(),
        "order": faker.random_int(min=0, max=100),
    }

    response: Response = client.post(url=url, json=data, params={"certificate_group_id": str(group_id)})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_certificate_duplicate_title(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест создания сертификата с дублирующимся названием."""
    url = app.url_path_for("create_certificate")

    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    title = faker.sentence(nb_words=3)
    data = {
        "title": title,
        "link": faker.url(),
        "order": faker.random_int(min=0, max=100),
    }

    request_schema = CertificateRequestSchema(**data)
    await mediator.handle_command(
        CreateCertificateCommand(
            certificate=request_schema.to_entity(),
            certificate_group_id=group_id,
        ),
    )

    response: Response = authenticated_client.post(url=url, json=data, params={"certificate_group_id": str(group_id)})

    assert response.status_code == status.HTTP_409_CONFLICT
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_certificate_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления сертификата."""
    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    data = {
        "title": faker.sentence(nb_words=3),
        "link": faker.url(),
        "order": faker.random_int(min=0, max=100),
    }

    request_schema = CertificateRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=request_schema.to_entity(),
            certificate_group_id=group_id,
        ),
    )
    certificate_id = result.oid

    url = app.url_path_for("update_certificate", certificate_id=certificate_id)

    update_data = {
        "title": "Updated Title",
        "link": data["link"],
        "order": data["order"],
    }

    response: Response = authenticated_client.put(url=url, json=update_data)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["title"] == "Updated Title"
    assert json_response["data"]["oid"] == str(certificate_id)


@pytest.mark.asyncio
async def test_update_certificate_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления сертификата без аутентификации."""
    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    data = {
        "title": faker.sentence(nb_words=3),
        "link": faker.url(),
        "order": faker.random_int(min=0, max=100),
    }

    request_schema = CertificateRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=request_schema.to_entity(),
            certificate_group_id=group_id,
        ),
    )
    certificate_id = result.oid

    url = app.url_path_for("update_certificate", certificate_id=certificate_id)

    response: Response = client.put(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_certificate_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест обновления несуществующего сертификата."""
    non_existent_id = uuid4()
    url = app.url_path_for("update_certificate", certificate_id=non_existent_id)

    data = {
        "title": faker.sentence(nb_words=3),
        "link": faker.url(),
        "order": faker.random_int(min=0, max=100),
    }

    response: Response = authenticated_client.put(url=url, json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_patch_certificate_order_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления порядка сертификата."""
    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    data = {
        "title": faker.sentence(nb_words=3),
        "link": faker.url(),
        "order": 1,
    }

    request_schema = CertificateRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=request_schema.to_entity(),
            certificate_group_id=group_id,
        ),
    )
    certificate_id = result.oid

    url = app.url_path_for("patch_certificate_order", certificate_id=certificate_id)

    response: Response = authenticated_client.patch(url=url, json={"order": 10})

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert "data" in json_response
    assert json_response["data"]["oid"] == str(certificate_id)
    assert json_response["data"]["order"] == 10


@pytest.mark.asyncio
async def test_patch_certificate_order_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления порядка сертификата без аутентификации."""
    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    data = {
        "title": faker.sentence(nb_words=3),
        "link": faker.url(),
        "order": 1,
    }

    request_schema = CertificateRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=request_schema.to_entity(),
            certificate_group_id=group_id,
        ),
    )
    certificate_id = result.oid

    url = app.url_path_for("patch_certificate_order", certificate_id=certificate_id)

    response: Response = client.patch(url=url, json={"order": 5})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_patch_certificate_order_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест обновления порядка несуществующего сертификата."""
    non_existent_id = uuid4()
    url = app.url_path_for("patch_certificate_order", certificate_id=non_existent_id)

    response: Response = authenticated_client.patch(url=url, json={"order": 1})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_certificate_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного удаления сертификата."""
    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    data = {
        "title": faker.sentence(nb_words=3),
        "link": faker.url(),
        "order": faker.random_int(min=0, max=100),
    }

    request_schema = CertificateRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=request_schema.to_entity(),
            certificate_group_id=group_id,
        ),
    )
    certificate_id = result.oid

    url = app.url_path_for("delete_certificate", certificate_id=certificate_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_url = app.url_path_for("get_certificate_by_id", certificate_id=certificate_id)
    get_response: Response = authenticated_client.get(url=get_url)

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_certificate_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест удаления сертификата без аутентификации."""
    group_data = {
        "section": "Сертификаты",
        "title": faker.sentence(nb_words=5),
        "content": faker.text(max_nb_chars=500),
    }
    group_schema = CertificateGroupRequestSchema(**group_data)
    group_result, *_ = await mediator.handle_command(
        CreateCertificateGroupCommand(certificate_group=group_schema.to_entity()),
    )
    group_id = group_result.oid

    data = {
        "title": faker.sentence(nb_words=3),
        "link": faker.url(),
        "order": faker.random_int(min=0, max=100),
    }

    request_schema = CertificateRequestSchema(**data)
    result, *_ = await mediator.handle_command(
        CreateCertificateCommand(
            certificate=request_schema.to_entity(),
            certificate_group_id=group_id,
        ),
    )
    certificate_id = result.oid

    url = app.url_path_for("delete_certificate", certificate_id=certificate_id)

    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_certificate_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест удаления несуществующего сертификата."""
    non_existent_id = uuid4()
    url = app.url_path_for("delete_certificate", certificate_id=non_existent_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0
