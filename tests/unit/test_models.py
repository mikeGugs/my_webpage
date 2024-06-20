from app.models.jbs_subscriptions import JobBoardScraperEmails
from app.extensions import db


def test_new_email(mock_jbs_subscriptions_model):
    """
    GIVEN a mock JobBoardScraperEmails model
    WHEN an email already exists in the database
    THEN check the email field we expect exists
    """

    my_model = mock_jbs_subscriptions_model

    assert my_model.email == "testing123@example.com"


def test_sqlalchemy_query_property_get_mock(app, mock_jbs_subscriptions_model, mock_get_sqlalchemy):
    mock_get_sqlalchemy.first.return_value = mock_jbs_subscriptions_model
    with app.app_context():
        response = JobBoardScraperEmails.query.first()

    assert response == mock_jbs_subscriptions_model
