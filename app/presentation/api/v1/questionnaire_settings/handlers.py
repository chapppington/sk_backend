from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from application.container import get_container
from application.mediator import Mediator
from application.questionnaire_settings.commands import (
    CreateQuestionnaireSettingsCommand,
    DeleteQuestionnaireSettingsCommand,
    UpdateQuestionnaireSettingsCommand,
)
from application.questionnaire_settings.queries import (
    GetQuestionnaireSettingsBySlugQuery,
    GetQuestionnaireSettingsListQuery,
)
from presentation.api.dependencies import get_current_user_id
from presentation.api.schemas import (
    ApiResponse,
    ErrorResponseSchema,
)
from presentation.api.v1.questionnaire_settings.schemas import (
    QuestionnaireSettingsRequestSchema,
    QuestionnaireSettingsResponseSchema,
)


router = APIRouter(prefix="/questionnaire-settings", tags=["questionnaire-settings"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[list[QuestionnaireSettingsResponseSchema]],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[list[QuestionnaireSettingsResponseSchema]]},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_questionnaire_settings_list(
    container=Depends(get_container),
) -> ApiResponse[list[QuestionnaireSettingsResponseSchema]]:
    mediator: Mediator = container.resolve(Mediator)
    settings_list = await mediator.handle_query(GetQuestionnaireSettingsListQuery())
    return ApiResponse[list[QuestionnaireSettingsResponseSchema]](
        data=[QuestionnaireSettingsResponseSchema.from_entity(item) for item in settings_list],
    )


@router.get(
    "/slug/{slug}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[QuestionnaireSettingsResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[QuestionnaireSettingsResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def get_questionnaire_settings_by_slug(
    slug: str,
    container=Depends(get_container),
) -> ApiResponse[QuestionnaireSettingsResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)
    settings = await mediator.handle_query(GetQuestionnaireSettingsBySlugQuery(slug=slug))
    return ApiResponse[QuestionnaireSettingsResponseSchema](
        data=QuestionnaireSettingsResponseSchema.from_entity(settings),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[QuestionnaireSettingsResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[QuestionnaireSettingsResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def create_questionnaire_settings(
    request: QuestionnaireSettingsRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[QuestionnaireSettingsResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)
    command = CreateQuestionnaireSettingsCommand(settings=request.to_entity())
    created, *_ = await mediator.handle_command(command)
    return ApiResponse[QuestionnaireSettingsResponseSchema](
        data=QuestionnaireSettingsResponseSchema.from_entity(created),
    )


@router.put(
    "/{settings_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[QuestionnaireSettingsResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[QuestionnaireSettingsResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def update_questionnaire_settings(
    settings_id: UUID,
    request: QuestionnaireSettingsRequestSchema,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> ApiResponse[QuestionnaireSettingsResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)
    command = UpdateQuestionnaireSettingsCommand(
        settings_id=settings_id,
        settings=request.to_entity(),
    )
    updated, *_ = await mediator.handle_command(command)
    return ApiResponse[QuestionnaireSettingsResponseSchema](
        data=QuestionnaireSettingsResponseSchema.from_entity(updated),
    )


@router.delete(
    "/{settings_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponseSchema},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"model": ErrorResponseSchema},
    },
)
async def delete_questionnaire_settings(
    settings_id: UUID,
    _=Depends(get_current_user_id),
    container=Depends(get_container),
) -> None:
    mediator: Mediator = container.resolve(Mediator)
    command = DeleteQuestionnaireSettingsCommand(settings_id=settings_id)
    await mediator.handle_command(command)
