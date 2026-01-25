from dataclasses import dataclass

from domain.base.entity import BaseEntity
from domain.vacancies.value_objects import (
    CategoryValueObject,
    ExperienceValueObject,
    RequirementsValueObject,
    SalaryValueObject,
    TitleValueObject,
)


@dataclass(eq=False)
class VacancyEntity(BaseEntity):
    title: TitleValueObject
    requirements: RequirementsValueObject
    experience: ExperienceValueObject
    salary: SalaryValueObject
    category: CategoryValueObject
