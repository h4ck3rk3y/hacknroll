import requests

from bs4 import BeautifulSoup
import json
from watson_developer_cloud import AlchemyLanguageV1


def get_country(url):
    list_of_locations = ["Country", "City"]
    alchemy_language = AlchemyLanguageV1(
        api_key='9a8353fc5871e9ae43c990d25ed6bf281f091ca2')
    response = (json.dumps(
        alchemy_language.combined(
            url=url,
            extract='entities,keywords',
            sentiment=1,
            max_items=1),
        indent=2))
    response = json.loads(response)
    data = {}

    for location_type in list_of_locations:
        for n, i in enumerate(response['entities']):
            if i["type"]==location_type and float(i['relevance']) > 0.5:
                data[location_type] = (i["text"])

    return data

def parse_money(money):

	# handle 5000 USD
	smoney = money.split(' ')
	parsed_money = None
	errors = []

	# something other than SGD
	if len(smoney) == 2 and smoney[1]!='USD':
		url = 'http://api.fixer.io/latest?symbols=%s&base=USD'%smoney[1].upper()
		response = requests.get(url)

		if response.status_code == 200:
			response = response.json()

			if not 'error' in response:
				parsed_money = float(smoney[0]) / float(response['rates'][smoney[1].upper()])
			else:
				errors.append('Couldnt convert the currency')
				parsed_money = float(smoney[0])
	else:
		parsed_money = float(smoney[0])

	return parsed_money, errors

countries = {0: u'Argentina',
 1: u'Australia',
 2: u'Austria',
 3: u'Bahrain',
 4: u'Belgium',
 5: u'Brazil',
 6: u'Canada',
 7: u'China',
 8: u'Croatia',
 9: u'Czech Republic',
 10: u'Czechia',
 11: u'Denmark',
 12: u'Egypt',
 13: u'Estonia',
 14: u'Finland',
 15: u'France',
 16: u'Germany',
 17: u'Hong Kong',
 18: u'Hungary',
 19: u'Iceland',
 20: u'India',
 21: u'Ireland',
 22: u'Israel',
 23: u'Italy',
 24: u'Japan',
 25: u'Luxembourg',
 26: u'Malaysia',
 27: u'Mexico',
 28: u'Morocco',
 29: u'Netherlands',
 30: u'Norway',
 31: u'Poland',
 32: u'Portugal',
 33: u'Russia',
 34: u'Saudi Arabia',
 35: u'Singapore',
 36: u'Slovakia',
 37: u'South Africa',
 38: u'South Korea',
 39: u'Spain',
 40: u'Sweden',
 41: u'Switzerland',
 42: u'Taiwan',
 43: u'Thailand',
 44: u'Turkey',
 45: u'United Arab Emirates',
 46: u'United Kingdom',
 47: u'United States'}
