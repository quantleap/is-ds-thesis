# -*- coding: utf-8 -*-
import scrapy

""" 
    on the form: 
    1. only 'successful controls', input fields with a name property and checked checkboxes 
       are sent in the post request the fields 
    2. the profession (functie) list is updated as an authority is checked/unchecked
    3. hidden input fields are created for RechtbankenChecked, GerechtshovenChecked and FieldSelectedFunction 
    4. search results are displayed up to max 500 entries - so each search should return less. The number of results is 
       displayed, e.g. Aantal gevonden personen: 278 in p:nth-child(5)
"""


class Official(scrapy.Item):
    name = scrapy.Field()
    function_title = scrapy.Field()
    authority = scrapy.Field()


class RechtspraakSpider(scrapy.Spider):
    name = 'rechtspraak'
    allowed_domains = ['namenlijst.rechtspraak.nl']
    start_urls = ['https://namenlijst.rechtspraak.nl//']

    def parse(self, response):
        # for Hoge Raad der Nederlanden
        # for Centrale Raad van Beroep
        # for College van Beroep voor het bedrijfsleven
        # for Gerechtshoven

        # for Rechtbanken
        # query one by one to keep under the max 500 results
        selector_list = response.selector.css('input[id^="ctl00_ContentPlaceHolder1_chklCourts_"]')

        for court_checkbox_selector in [selector_list[0]]:  # remove [0] for all courts
            control_name = court_checkbox_selector.css('::attr(name)').extract_first()
            current_value = court_checkbox_selector.css('::attr(value)').extract_first()

            override_form_data = {'rechtbanken': 'rechtbanken',
                                  'ctl00$ContentPlaceHolder1$hiddenFieldRechtbankenChecked': 'true',
                                  control_name: current_value,
                                  'ctl00$ContentPlaceHolder1$ddlFunctions': 'alle functies',
                                  'ctl00$ContentPlaceHolder1$hiddenFieldSelectedFunction': 'alle functies',
                                  }

            request = scrapy.FormRequest.from_response(response,
                                                       formid="aspnetForm",
                                                       formdata=override_form_data,
                                                       clickdata={'value': 'Zoeken'},  # this  defines the submit button
                                                       callback=self.parse_officials)
            yield request

    # noinspection PyMethodMayBeStatic
    def parse_officials(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        no_results = int(response.selector.css("div.resultheader p:nth-child(5)").
                         re_first(r'Aantal gevonden personen:\s*(\d+).'))
        assert(no_results < 500, "too many search results")
        selector_list = response.css('tbody tr')

        for row_selector in selector_list:
            name = row_selector.css('td input::attr(value)').extract_first()

            # officials may have more than one function title and for subsequent professions the name is not given
            if name:
                name = name.strip()
                previous_name = name
            else:
                name = previous_name

            function_title = row_selector.css('td:nth-child(2)::text').extract_first().strip()  # functie
            authority = row_selector.css('td:nth-child(3)::text').extract_first().strip()  # instantie
            yield Official({'name': name,
                            'function_title': function_title,
                            'authority': authority})
