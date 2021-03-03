import requests


class TestIndex:
    def test_200(self):
        assert_200_request_to(get_polls_url_index())


class TestQuestionDetail:
    def test_get_question(self):
        for question_id in {2020, 2021}:
            assert_200_request_to(get_polls_url_detail(question_id))
            assert_200_request_to(get_polls_url_results(question_id))
            assert_200_request_to(get_polls_url_vote(question_id))

    def test_404_question(self):
        assert_404(requests.get(get_polls_url_detail(2019)))


def get_polls_url():
    return 'http://localhost:8000/polls/'


def get_polls_url_index():
    return get_polls_url()


def get_polls_url_detail(question_id):
    return get_polls_url() + str(question_id) + '/'


def get_polls_url_results(question_id):
    return get_polls_url() + str(question_id) + '/results'


def get_polls_url_vote(question_id):
    return get_polls_url() + str(question_id) + '/vote'


def assert_200_request_to(url):
    assert_200(requests.get(url))


def assert_200(response):
    assert_status_code(response, 200)


def assert_404(response):
    assert_status_code(response, 404)


def assert_status_code(response, expected_status_code):
    assert response.status_code == expected_status_code
