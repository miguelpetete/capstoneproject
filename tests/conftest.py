# pylint: skip-file
import pytest
from clapstone import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True, "DEBUG": True})
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
