import requests
import json

class OpenStateJudgesGateway:
    """ encapsulates access to the open state API for secondary functions
        of various officials in the case law (nevenfuncties) """

    _OFFICIALS_LIST_URL = r'http://ors.openstate.eu/index.php/relations/json'
    _OFFICIAL_DETAILS_URL = r' http://ors.openstate.eu/relations/instantie/RECHTBANK/NAAM/json'

    def _request_list_officials(self):
        """ requests the list of officials """
        response = requests.get(self._OFFICIALS_LIST_URL)
        assert 'application/json' in response.headers['content-type']
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.RequestException("Expected status code 200, but got {}".format(page.status_code))

    @staticmethod
    def _request_official_details(uri):
        """ request the officials details """
        response = requests.get(uri)
        assert 'application/json' in response.headers['content-type']
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.RequestException("Expected status code 200, but got {}".format(page.status_code))

    def _subset_official_details(self, official_details):
        """ subset the official details - keep only relevant information """

        # only report profession when it is performed at the appropiate authority (set/instantie)
        # there is always a trailing space in the name
        subset_official_details = {'name': official_details['name'].strip(),
                                   'set': official_details['set'],
                                   'Beroepsgegevens':
                                       [x for x in official_details['data']['Beroepsgegevens']
                                        if x['Instantie'] == official_details['set']]
                                   }
        return subset_official_details

    def _get_details_all_officials(self):
        details_all_officials = []

        list_officials = self._request_list_officials()

        # append details per official
        for official in list_officials[:10]:
            uri = official['uri']

            try:
                official_details = self._request_official_details(uri)
                subset_details = self._subset_official_details(official_details)
                details_all_officials.append(subset_details)
            except AssertionError:
                pass

        return details_all_officials


if __name__ == '__main__':
    import pprint
    gw = OpenStateJudgesGateway()
    all_details = gw._get_details_all_officials()
    print(all_details)
