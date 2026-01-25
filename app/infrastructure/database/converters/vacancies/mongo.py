from datetime import datetime
from uuid import UUID

from domain.vacancies.entities.vacancies import VacancyEntity
from domain.vacancies.value_objects.vacancies import (
    CategoryValueObject,
    ExperienceValueObject,
    RequirementsValueObject,
    SalaryValueObject,
    TitleValueObject,
)


def vacancy_entity_to_document(entity: VacancyEntity) -> dict:
    return {
        "oid": str(entity.oid),
        "title": entity.title.as_generic_type(),
        "requirements": entity.requirements.as_generic_type(),
        "experience": entity.experience.as_generic_type(),
        "salary": entity.salary.as_generic_type(),
        "category": entity.category.as_generic_type(),
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
    }


def vacancy_document_to_entity(document: dict) -> VacancyEntity:
    return VacancyEntity(
        oid=UUID(document["oid"]),
        title=TitleValueObject(value=document["title"]),
        requirements=RequirementsValueObject(value=document["requirements"]),
        experience=ExperienceValueObject(value=document["experience"]),
        salary=SalaryValueObject(value=document["salary"]),
        category=CategoryValueObject(value=document["category"]),
        created_at=datetime.fromisoformat(document["created_at"]),
        updated_at=datetime.fromisoformat(document["updated_at"]),
    )
