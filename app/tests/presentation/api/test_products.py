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
from application.products.commands import CreateProductCommand
from presentation.api.v1.products.schemas import ProductRequestSchema


@pytest.mark.asyncio
async def test_get_products_list_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения списка продуктов."""
    url = app.url_path_for("get_products_list")

    for _ in range(3):
        data = {
            "category": "Трансформаторные подстанции",
            "name": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "description": faker.text(max_nb_chars=500),
            "preview_image_url": faker.image_url(),
            "preview_image_alt": faker.sentence(nb_words=3),
        }
        request_schema = ProductRequestSchema(**data)
        await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))

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
async def test_get_products_list_with_pagination(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка продуктов с пагинацией."""
    url = app.url_path_for("get_products_list")

    for _ in range(5):
        data = {
            "category": "Трансформаторные подстанции",
            "name": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "description": faker.text(max_nb_chars=500),
            "preview_image_url": faker.image_url(),
            "preview_image_alt": faker.sentence(nb_words=3),
        }
        request_schema = ProductRequestSchema(**data)
        await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"limit": 2, "offset": 0})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 2
    assert json_response["data"]["pagination"]["limit"] == 2
    assert json_response["data"]["pagination"]["offset"] == 0


@pytest.mark.asyncio
async def test_get_products_list_with_category_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка продуктов с фильтром по категории."""
    url = app.url_path_for("get_products_list")

    for _ in range(3):
        data = {
            "category": "Трансформаторные подстанции",
            "name": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "description": faker.text(max_nb_chars=500),
            "preview_image_url": faker.image_url(),
            "preview_image_alt": faker.sentence(nb_words=3),
        }
        request_schema = ProductRequestSchema(**data)
        await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))

    for _ in range(2):
        data = {
            "category": "Распределительные устройства среднего напряжения 6(10) кВ",
            "name": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "description": faker.text(max_nb_chars=500),
            "preview_image_url": faker.image_url(),
            "preview_image_alt": faker.sentence(nb_words=3),
        }
        request_schema = ProductRequestSchema(**data)
        await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"category": "Трансформаторные подстанции"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 3
    assert all(item["category"] == "Трансформаторные подстанции" for item in json_response["data"]["items"])


@pytest.mark.asyncio
async def test_get_products_list_with_search(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка продуктов с поиском."""
    url = app.url_path_for("get_products_list")

    data1 = {
        "category": "Трансформаторные подстанции",
        "name": "Python трансформатор",
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }
    request_schema1 = ProductRequestSchema(**data1)
    await mediator.handle_command(CreateProductCommand(product=request_schema1.to_entity()))

    data2 = {
        "category": "Трансформаторные подстанции",
        "name": "JavaScript устройство",
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }
    request_schema2 = ProductRequestSchema(**data2)
    await mediator.handle_command(CreateProductCommand(product=request_schema2.to_entity()))

    response: Response = client.get(url=url, params={"search": "Python"})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 1
    assert "Python" in json_response["data"]["items"][0]["name"]


@pytest.mark.asyncio
async def test_get_products_list_with_is_shown_filter(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка продуктов с фильтром по видимости."""
    url = app.url_path_for("get_products_list")

    for _ in range(3):
        data = {
            "category": "Трансформаторные подстанции",
            "name": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "description": faker.text(max_nb_chars=500),
            "preview_image_url": faker.image_url(),
            "preview_image_alt": faker.sentence(nb_words=3),
            "is_shown": True,
        }
        request_schema = ProductRequestSchema(**data)
        await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))

    for _ in range(2):
        data = {
            "category": "Трансформаторные подстанции",
            "name": faker.sentence(nb_words=5),
            "slug": faker.slug(),
            "description": faker.text(max_nb_chars=500),
            "preview_image_url": faker.image_url(),
            "preview_image_alt": faker.sentence(nb_words=3),
            "is_shown": False,
        }
        request_schema = ProductRequestSchema(**data)
        await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))

    response: Response = client.get(url=url, params={"is_shown": True})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) == 3
    assert all(item["is_shown"] is True for item in json_response["data"]["items"])


@pytest.mark.asyncio
async def test_get_products_list_with_sorting(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест получения списка продуктов с сортировкой."""
    url = app.url_path_for("get_products_list")

    data1 = {
        "category": "Трансформаторные подстанции",
        "name": "A Product",
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }
    request_schema1 = ProductRequestSchema(**data1)
    await mediator.handle_command(CreateProductCommand(product=request_schema1.to_entity()))

    data2 = {
        "category": "Трансформаторные подстанции",
        "name": "B Product",
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }
    request_schema2 = ProductRequestSchema(**data2)
    await mediator.handle_command(CreateProductCommand(product=request_schema2.to_entity()))

    response: Response = client.get(url=url, params={"sort_field": "name", "sort_order": 1})

    assert response.is_success
    json_response = response.json()
    assert len(json_response["data"]["items"]) >= 2
    items = json_response["data"]["items"]
    product_names = [item["name"] for item in items if item["name"] in ["A Product", "B Product"]]
    if len(product_names) == 2:
        assert product_names[0] < product_names[1]


@pytest.mark.asyncio
async def test_get_product_by_id_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения продукта по ID."""
    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    request_schema = ProductRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))
    product_id = result.oid

    url = app.url_path_for("get_product_by_id", product_id=product_id)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["oid"] == str(product_id)
    assert json_response["data"]["name"] == data["name"]
    assert json_response["data"]["slug"] == data["slug"]


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(
    app: FastAPI,
    client: TestClient,
):
    """Тест получения продукта по несуществующему ID."""
    non_existent_id = uuid4()
    url = app.url_path_for("get_product_by_id", product_id=non_existent_id)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_get_product_by_slug_success(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного получения продукта по slug."""
    slug = faker.slug()
    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": slug,
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    request_schema = ProductRequestSchema(**data)
    await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))

    url = app.url_path_for("get_product_by_slug", slug=slug)

    response: Response = client.get(url=url)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["slug"] == slug
    assert json_response["data"]["name"] == data["name"]


@pytest.mark.asyncio
async def test_get_product_by_slug_not_found(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    """Тест получения продукта по несуществующему slug."""
    non_existent_slug = faker.slug()
    url = app.url_path_for("get_product_by_slug", slug=non_existent_slug)

    response: Response = client.get(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_product_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест успешного создания продукта."""
    url = app.url_path_for("create_product")

    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["name"] == data["name"]
    assert json_response["data"]["slug"] == data["slug"]
    assert json_response["data"]["category"] == data["category"]
    assert "oid" in json_response["data"]


@pytest.mark.asyncio
async def test_create_product_with_all_fields_success(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест успешного создания продукта со всеми полями."""
    url = app.url_path_for("create_product")

    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
        "important_characteristics": [
            {
                "value": "10 кВ",
                "unit": {"text": "кВ"},
                "description": "Напряжение",
            },
        ],
        "advantages": [
            {
                "label": "Надежность",
                "icon": "reliability",
                "image": faker.image_url(),
                "alt": "Надежность",
                "description": "Высокая надежность",
            },
        ],
        "simple_description": [
            {"text": "Простое описание"},
        ],
        "detailed_description": [
            {
                "title": "Детальное описание",
                "description": "Полное описание продукта",
            },
        ],
        "documentation": [
            {
                "title": "Документация",
                "url": faker.url(),
                "type": "pdf",
            },
        ],
        "order": 5,
        "is_shown": True,
        "show_advantages": True,
        "portfolio_ids": [],
    }

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.is_success
    assert response.status_code == status.HTTP_201_CREATED

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["name"] == data["name"]
    assert len(json_response["data"]["important_characteristics"]) == 1
    assert len(json_response["data"]["advantages"]) == 1
    assert len(json_response["data"]["simple_description"]) == 1
    assert len(json_response["data"]["detailed_description"]) == 1
    assert len(json_response["data"]["documentation"]) == 1
    assert json_response["data"]["order"] == 5


@pytest.mark.asyncio
async def test_create_product_unauthorized(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    """Тест создания продукта без аутентификации."""
    url = app.url_path_for("create_product")

    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    response: Response = client.post(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_product_duplicate_slug(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест создания продукта с дублирующимся slug."""
    url = app.url_path_for("create_product")
    slug = faker.slug()

    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": slug,
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    request_schema = ProductRequestSchema(**data)
    await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))

    response: Response = authenticated_client.post(url=url, json=data)

    assert response.status_code == status.HTTP_409_CONFLICT
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_product_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления продукта."""
    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    request_schema = ProductRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))
    product_id = result.oid

    url = app.url_path_for("update_product", product_id=product_id)

    update_data = {
        "category": data["category"],
        "name": "Updated Product Name",
        "slug": faker.slug(),
        "description": data["description"],
        "preview_image_url": data["preview_image_url"],
        "preview_image_alt": data["preview_image_alt"],
    }

    response: Response = authenticated_client.put(url=url, json=update_data)

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()

    assert "data" in json_response
    assert json_response["data"]["name"] == "Updated Product Name"
    assert json_response["data"]["oid"] == str(product_id)


@pytest.mark.asyncio
async def test_update_product_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления продукта без аутентификации."""
    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    request_schema = ProductRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))
    product_id = result.oid

    url = app.url_path_for("update_product", product_id=product_id)

    response: Response = client.put(url=url, json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_update_product_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
    faker: Faker,
):
    """Тест обновления несуществующего продукта."""
    non_existent_id = uuid4()
    url = app.url_path_for("update_product", product_id=non_existent_id)

    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    response: Response = authenticated_client.put(url=url, json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_patch_product_order_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного обновления порядка продукта."""
    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    request_schema = ProductRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))
    product_id = result.oid

    url = app.url_path_for("patch_product_order", product_id=product_id)

    response: Response = authenticated_client.patch(url=url, json={"order": 10})

    assert response.is_success
    assert response.status_code == status.HTTP_200_OK

    json_response = response.json()
    assert "data" in json_response
    assert json_response["data"]["oid"] == str(product_id)
    assert json_response["data"]["order"] == 10


@pytest.mark.asyncio
async def test_patch_product_order_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест обновления порядка продукта без аутентификации."""
    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    request_schema = ProductRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))
    product_id = result.oid

    url = app.url_path_for("patch_product_order", product_id=product_id)

    response: Response = client.patch(url=url, json={"order": 5})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_patch_product_order_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест обновления порядка несуществующего продукта."""
    non_existent_id = uuid4()
    url = app.url_path_for("patch_product_order", product_id=non_existent_id)

    response: Response = authenticated_client.patch(url=url, json={"order": 1})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_product_success(
    app: FastAPI,
    authenticated_client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест успешного удаления продукта."""
    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    request_schema = ProductRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))
    product_id = result.oid

    url = app.url_path_for("delete_product", product_id=product_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_url = app.url_path_for("get_product_by_id", product_id=product_id)
    get_response: Response = authenticated_client.get(url=get_url)

    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_product_unauthorized(
    app: FastAPI,
    client: TestClient,
    mediator: Mediator,
    faker: Faker,
):
    """Тест удаления продукта без аутентификации."""
    data = {
        "category": "Трансформаторные подстанции",
        "name": faker.sentence(nb_words=5),
        "slug": faker.slug(),
        "description": faker.text(max_nb_chars=500),
        "preview_image_url": faker.image_url(),
        "preview_image_alt": faker.sentence(nb_words=3),
    }

    request_schema = ProductRequestSchema(**data)
    result, *_ = await mediator.handle_command(CreateProductCommand(product=request_schema.to_entity()))
    product_id = result.oid

    url = app.url_path_for("delete_product", product_id=product_id)

    response: Response = client.delete(url=url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_delete_product_not_found(
    app: FastAPI,
    authenticated_client: TestClient,
):
    """Тест удаления несуществующего продукта."""
    non_existent_id = uuid4()
    url = app.url_path_for("delete_product", product_id=non_existent_id)

    response: Response = authenticated_client.delete(url=url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    json_response = response.json()
    assert "errors" in json_response
    assert len(json_response["errors"]) > 0
