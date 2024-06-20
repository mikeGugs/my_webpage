import pytest
import os
from app import create_app
from flask import template_rendered
from app.extensions import db
import tempfile
from app.models.jbs_subscriptions import JobBoardScraperEmails
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import TestingConfig

@pytest.fixture()
def app():
    app = create_app(TestingConfig)
    app.config.update({
        "TESTING": True,
        "CSRF_ENABLED": False,
        })

    with app.app_context():
        db.create_all()
    
        yield app

@pytest.fixture
def app_mock():
    app_mock = Flask(__name__)
    mock_db = SQLAlchemy(app_mock)
    mock_db.init_app(app_mock)
    yield app_mock
    mock_db.drop_all()

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

@pytest.fixture()
def mock_jbs_subscriptions_model():
    jbs_subs = JobBoardScraperEmails(
        email="testing123@example.com",
        )
    return jbs_subs

@pytest.fixture()
def mock_get_sqlalchemy(mocker):
    mock = mocker.patch("flask_sqlalchemy.model._QueryProperty.__get__").return_value = mocker.Mock()
    return mock
