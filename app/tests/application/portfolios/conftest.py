import pytest
from faker import Faker


@pytest.fixture
def valid_portfolio_data(faker: Faker) -> dict:
    return {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "year": faker.random_int(min=2000, max=2100),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_right": faker.image_url(),
        "preview_video_path": faker.url(),
        "full_video_path": faker.url(),
        "description": faker.text(max_nb_chars=1000),
        "has_review": False,
    }


@pytest.fixture
def valid_portfolio_data_with_review(faker: Faker) -> dict:
    return {
        "name": faker.sentence(nb_words=3),
        "slug": faker.slug(),
        "poster": faker.image_url(),
        "year": faker.random_int(min=2000, max=2100),
        "task_title": faker.sentence(nb_words=5),
        "task_description": faker.text(max_nb_chars=500),
        "solution_title": faker.sentence(nb_words=5),
        "solution_description": faker.text(max_nb_chars=500),
        "solution_subtitle": faker.sentence(nb_words=3),
        "solution_subdescription": faker.text(max_nb_chars=300),
        "solution_image_left": faker.image_url(),
        "solution_image_right": faker.image_url(),
        "preview_video_path": faker.url(),
        "full_video_path": faker.url(),
        "description": faker.text(max_nb_chars=1000),
        "has_review": True,
        "review_title": faker.sentence(nb_words=3),
        "review_text": faker.text(max_nb_chars=200),
        "review_name": faker.name(),
        "review_image": faker.image_url(),
        "review_role": faker.job(),
    }


@pytest.fixture
def valid_portfolio_data_with_year(faker: Faker):
    def _create(year: int | None = None) -> dict:
        data = {
            "name": faker.sentence(nb_words=3),
            "slug": faker.slug(),
            "poster": faker.image_url(),
            "year": year if year else faker.random_int(min=2000, max=2100),
            "task_title": faker.sentence(nb_words=5),
            "task_description": faker.text(max_nb_chars=500),
            "solution_title": faker.sentence(nb_words=5),
            "solution_description": faker.text(max_nb_chars=500),
            "solution_subtitle": faker.sentence(nb_words=3),
            "solution_subdescription": faker.text(max_nb_chars=300),
            "solution_image_left": faker.image_url(),
            "solution_image_right": faker.image_url(),
            "preview_video_path": faker.url(),
            "full_video_path": faker.url(),
            "description": faker.text(max_nb_chars=1000),
            "has_review": False,
        }
        return data

    return _create
