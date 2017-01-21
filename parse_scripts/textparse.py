from bs4 import BeautifulSoup
import json
from watson_developer_cloud import AlchemyLanguageV1


def get_country(text, url):
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