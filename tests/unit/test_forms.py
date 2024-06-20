from app.forms.forms import JobBoardScraperEmailForm, SendMeEmailForm

def test_job_board_scraper_accepts_valid_email(client):
    form_data = {'email': 'tester123@gmail.com'}
    response = client.post('/job_board_scraper', data=form_data)

    assert response.status_code == 200
