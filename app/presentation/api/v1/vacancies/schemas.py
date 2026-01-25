from uuid import UUID

from pydantic import BaseModel

from domain.vacancies.entities.vacancies import VacancyEntity


class VacancyResponseSchema(BaseModel):
    oid: UUID
    title: str
    requirements: list[str]
    experience: list[str]
    salary: int
    category: str
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, entity: VacancyEntity) -> "VacancyResponseSchema":
        return cls(
            oid=entity.oid,
            title=entity.title.as_generic_type(),
            requirements=entity.requirements.as_generic_type(),
            experience=entity.experience.as_generic_type(),
            salary=entity.salary.as_generic_type(),
            category=entity.category.as_generic_type(),
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat(),
        )


class CreateVacancyRequestSchema(BaseModel):
    title: str
    requirements: list[str]
    experience: list[str]
    salary: int
    category: str


class UpdateVacancyRequestSchema(BaseModel):
    title: str
    requirements: list[str]
    experience: list[str]
    salary: int
    category: str
