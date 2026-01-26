from uuid import UUID

from pydantic import BaseModel

from domain.vacancies.entities.vacancies import VacancyEntity
from domain.vacancies.value_objects.vacancies import (
    CategoryValueObject,
    ExperienceValueObject,
    RequirementsValueObject,
    SalaryValueObject,
    TitleValueObject,
)


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


class VacancyRequestSchema(BaseModel):
    title: str
    requirements: list[str]
    experience: list[str]
    salary: int
    category: str

    def to_entity(self) -> VacancyEntity:
        return VacancyEntity(
            title=TitleValueObject(value=self.title),
            requirements=RequirementsValueObject(value=self.requirements),
            experience=ExperienceValueObject(value=self.experience),
            salary=SalaryValueObject(value=self.salary),
            category=CategoryValueObject(value=self.category),
        )
