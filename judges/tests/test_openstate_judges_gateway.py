import pytest
from judges.openstate_judges_gateway import OpenStateJudgesGateway


@pytest.fixture
def officials_list():
    gateway = OpenStateJudgesGateway()
    return gateway._request_list_officials()


@pytest.fixture
def official_details():
    gateway = OpenStateJudgesGateway()
    uri = gateway._request_list_officials()[0]['uri']
    return gateway._request_official_details(uri)


def test_request_lists_provides_non_empyty_list(officials_list):
    assert isinstance(officials_list, list)
    assert len(officials_list) > 0


def test_request_officials_list_entry_keys(officials_list):
    assert {'uri', 'set', 'name'} <= set(officials_list[0])


def test_request_official_details_keys(official_details):
    assert {'name', 'set', 'data'} <= set(official_details)
    assert {'Beroepsgegevens'} <= set(official_details['data'])
    assert isinstance(official_details['data']['Beroepsgegevens'], list)
    assert {'Functie', 'Instantie', 'Datum+ingang'} <= set(official_details['data']['Beroepsgegevens'][0])

