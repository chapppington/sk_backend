from punq import Container
from pytest import fixture

from application.mediator import Mediator
from tests.fixtures import get_dummy_container


@fixture(scope="function")
def container() -> Container:
    return get_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)
