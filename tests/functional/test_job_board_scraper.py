import datetime
import pytest
import os


@pytest.mark.skipif(os.environ.get('ENVIRONMENT') == 'LOCAL',
                    reason="job_board_scraper only runs every day on production server")
def test_jobs_data_is_up_to_date(client):
    """GIVEN the most recent weekday
    WHEN the '/job_board_scraper' page is requested (GET)
    THEN check that the job_board_scraper.py program ran successfully,
    and the Flask application is publishing the data
    """
    if datetime.datetime.today().weekday() == 5:
        relevant_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    elif datetime.datetime.today().weekday() == 6:
        relevant_date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    else:
        relevant_date = datetime.datetime.today().strftime('%Y%m%d')
    relevant_date = str.encode(relevant_date)
    response = client.get('/job_board_scraper')
    assert relevant_date in response.data
