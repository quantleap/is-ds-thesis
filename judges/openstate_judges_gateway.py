import requests


class OpenStateJudgesGateway:
    """ encapsulates access to the open state API for secondary functions
        of various officials in the case law (nevenfuncties) """

    _OFFICIALS_LIST_URL = r'http://ors.openstate.eu/index.php/relations/json'
    _OFFICIAL_DETAILS_URL = r' http://ors.openstate.eu/relations/instantie/RECHTBANK/NAAM/json'

    def _request_list_officials(self):
        """ requests the list of officials """
        response = requests.get(self._OFFICIALS_LIST_URL)
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.RequestException("Expected status code 200, but got {}".format(page.status_code))

    @staticmethod
    def _request_official_details(uri):
        """ request the officials details """
        response = requests.get(uri)
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.RequestException("Expected status code 200, but got {}".format(page.status_code))

    def get_judges_name_list(self):
        pass