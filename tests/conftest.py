import pytest
from app import create_app
from flask import template_rendered

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        })

    yield app

@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
    
@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

