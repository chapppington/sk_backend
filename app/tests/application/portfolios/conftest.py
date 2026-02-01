import pytest
from faker import Faker

from domain.portfolios.entities.portfolios import PortfolioEntity
from domain.portfolios.value_objects.portfolios import (
    DescriptionValueObject,
    ImageAltValueObject,
    NameValueObject,
    PosterUrlValueObject,
    ReviewImageUrlValueObject,
    ReviewNameValueObject,
    ReviewRoleValueObject,
    ReviewTextValueObject,
    ReviewTitleValueObject,
    SlugValueObject,
    SolutionDescriptionValueObject,
    SolutionImageUrlValueObject,
    SolutionSubdescriptionValueObject,
    SolutionSubtitleValueObject,
    SolutionTitleValueObject,
    TaskDescriptionValueObject,
    TaskTitleValueObject,
    YearValueObject,
)


@pytest.fixture
def valid_portfolio_entity(faker: Faker) -> PortfolioEntity:
    return PortfolioEntity(
        name=NameValueObject(value=faker.sentence(nb_words=3)),
        slug=SlugValueObject(value=faker.slug()),
        poster=PosterUrlValueObject(value=faker.image_url()),
        poster_alt=ImageAltValueObject(value=faker.sentence(nb_words=3)),
        year=YearValueObject(value=faker.random_int(min=2000, max=2100)),
        description=DescriptionValueObject(value=faker.text(max_nb_chars=1000)),
        task_title=TaskTitleValueObject(value=faker.sentence(nb_words=5)),
        task_description=TaskDescriptionValueObject(value=faker.text(max_nb_chars=500)),
        solution_title=SolutionTitleValueObject(value=faker.sentence(nb_words=5)),
        solution_description=SolutionDescriptionValueObject(value=faker.text(max_nb_chars=500)),
        solution_subtitle=SolutionSubtitleValueObject(value=faker.sentence(nb_words=3)),
        solution_subdescription=SolutionSubdescriptionValueObject(value=faker.text(max_nb_chars=300)),
        solution_image_left=SolutionImageUrlValueObject(value=faker.image_url()),
        solution_image_left_alt=ImageAltValueObject(value=faker.sentence(nb_words=3)),
        solution_image_right=SolutionImageUrlValueObject(value=faker.image_url()),
        solution_image_right_alt=ImageAltValueObject(value=faker.sentence(nb_words=3)),
        has_review=False,
    )


@pytest.fixture
def valid_portfolio_entity_with_review(faker: Faker) -> PortfolioEntity:
    return PortfolioEntity(
        name=NameValueObject(value=faker.sentence(nb_words=3)),
        slug=SlugValueObject(value=faker.slug()),
        poster=PosterUrlValueObject(value=faker.image_url()),
        poster_alt=ImageAltValueObject(value=faker.sentence(nb_words=3)),
        year=YearValueObject(value=faker.random_int(min=2000, max=2100)),
        description=DescriptionValueObject(value=faker.text(max_nb_chars=1000)),
        task_title=TaskTitleValueObject(value=faker.sentence(nb_words=5)),
        task_description=TaskDescriptionValueObject(value=faker.text(max_nb_chars=500)),
        solution_title=SolutionTitleValueObject(value=faker.sentence(nb_words=5)),
        solution_description=SolutionDescriptionValueObject(value=faker.text(max_nb_chars=500)),
        solution_subtitle=SolutionSubtitleValueObject(value=faker.sentence(nb_words=3)),
        solution_subdescription=SolutionSubdescriptionValueObject(value=faker.text(max_nb_chars=300)),
        solution_image_left=SolutionImageUrlValueObject(value=faker.image_url()),
        solution_image_left_alt=ImageAltValueObject(value=faker.sentence(nb_words=3)),
        solution_image_right=SolutionImageUrlValueObject(value=faker.image_url()),
        solution_image_right_alt=ImageAltValueObject(value=faker.sentence(nb_words=3)),
        has_review=True,
        review_title=ReviewTitleValueObject(value=faker.sentence(nb_words=3)),
        review_text=ReviewTextValueObject(value=faker.text(max_nb_chars=200)),
        review_name=ReviewNameValueObject(value=faker.name()),
        review_image=ReviewImageUrlValueObject(value=faker.image_url()),
        review_role=ReviewRoleValueObject(value=faker.job()),
    )


@pytest.fixture
def valid_portfolio_entity_with_year(faker: Faker):
    def _create(year: int | None = None) -> PortfolioEntity:
        return PortfolioEntity(
            name=NameValueObject(value=faker.sentence(nb_words=3)),
            slug=SlugValueObject(value=faker.slug()),
            poster=PosterUrlValueObject(value=faker.image_url()),
            poster_alt=ImageAltValueObject(value=faker.sentence(nb_words=3)),
            year=YearValueObject(value=year if year else faker.random_int(min=2000, max=2100)),
            description=DescriptionValueObject(value=faker.text(max_nb_chars=1000)),
            task_title=TaskTitleValueObject(value=faker.sentence(nb_words=5)),
            task_description=TaskDescriptionValueObject(value=faker.text(max_nb_chars=500)),
            solution_title=SolutionTitleValueObject(value=faker.sentence(nb_words=5)),
            solution_description=SolutionDescriptionValueObject(value=faker.text(max_nb_chars=500)),
            solution_subtitle=SolutionSubtitleValueObject(value=faker.sentence(nb_words=3)),
            solution_subdescription=SolutionSubdescriptionValueObject(value=faker.text(max_nb_chars=300)),
            solution_image_left=SolutionImageUrlValueObject(value=faker.image_url()),
            solution_image_left_alt=ImageAltValueObject(value=faker.sentence(nb_words=3)),
            solution_image_right=SolutionImageUrlValueObject(value=faker.image_url()),
            solution_image_right_alt=ImageAltValueObject(value=faker.sentence(nb_words=3)),
            has_review=False,
        )

    return _create
