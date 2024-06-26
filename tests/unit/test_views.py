
def test_home_page_returns_basic_info(client, captured_templates):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to My Personal Website!" in response.data

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == "home.html"

def test_job_board_scraper_returns_basic_info(client, captured_templates):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/job_board_scraper' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/job_board_scraper')
    assert response.status_code == 200
    assert b"Job Board Scraper" in response.data

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == 'job_board_scraper.html'

def test_about_me_returns_basic_info(client, captured_templates):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/about_me' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/about_me')
    assert response.status_code == 200
    assert b'Thanks for visiting my personal website!' in response.data

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == 'about_me.html'

def test_contact_returns_basic_info(client, captured_templates):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/contact.html' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'My Linkedin' in response.data

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == 'contact.html'

def test_unsubscribe_returns_basic_info(client, captured_templates):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/unsubscribe.html' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('unsubscribe')
    assert response.status_code == 200
    assert b'Sorry to see you go!' in response.data

    assert len(captured_templates) == 1

    template, context = captured_templates[0]

    assert template.name == 'unsubscribe.html'
