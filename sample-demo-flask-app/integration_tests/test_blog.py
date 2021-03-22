from random import randint
from requests import get, post, Session


class TestIndex:
    def test_200(self):
        assert_200(get(get_blog_url()))


class TestCreate:
    def test_200_get(self):
        assert_200(get(get_blog_url_create()))

    def test_correct_auth(self):
        auth_response = auth_request_login()
        assert_200(auth_response)
        assert "Incorrect" not in str(auth_response.content)
        assert "required" not in str(auth_response.content)

    def test_no_auth(self):
        no_auth_response = get(get_blog_url_auth())
        assert_200(no_auth_response)
        assert "required" in str(no_auth_response.content)

    def test_incorrect_auth(self):
        auth_response = auth_request('wrong')
        assert_200(auth_response)
        assert "Incorrect" in str(auth_response.content)
        assert "required" in str(auth_response.content)

    def test_create_post(self):
        ses = Session()
        ses.post(get_blog_url_auth(), data={'username': 'test', 'password': 'test'})
        suffix = str(randint(1, 2021))
        post_response = ses.post(get_blog_url_create(),
                                 data={'title': 'The Title of My Blog ' + suffix, 'body': 'Here'})
        assert_200(post_response)
        get_index_page = ses.get(get_blog_url())
        assert_200(get_index_page)
        assert "The Title of My Blog " + suffix in str(get_index_page.content)


def get_blog_url():
    return 'http://localhost:8000'


def get_blog_url_create():
    return get_blog_url() + '/create'


def get_blog_url_auth():
    return get_blog_url() + '/auth/login'


def assert_200(response):
    assert_status_code(response, 200)


def assert_status_code(response, expected_status_code):
    assert response.status_code == expected_status_code


def auth_request_login():
    return auth_request('test')


def auth_request(password):
    return post(get_blog_url_auth(), data={'username': 'test', 'password': password})
