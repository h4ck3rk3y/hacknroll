from bs4 import BeautifulSoup
import json
from watson_developer_cloud import AlchemyLanguageV1

# This will come from a global variable or something
import_text = str(
    "The year kicks off with a bang on 1 Jan and New Year, celebrated in Singapore.")
url = "http://wikitravel.org/en/Singapore"
webpage = 'example_webpage.htm'

# A function that parses the information passed from the extension.


def get_header(text, url, full_webpage):
    f = open('example_webpage.htm', 'r')
    soup = BeautifulSoup(f, 'html.parser')

    # Find specific header
    plain_soup = []
    list_of_headers = []
    for line in soup.find_all():
        print(line.text)
        plain_soup.append(line.text)
        if import_text in str(line.text):
            print("HUZZAH")
    for headers in soup.find_all("span", {"class": "mw-headline"}):
        list_of_headers.append(headers.text)


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
    for location_type in list_of_locations:
        for n, i in enumerate(response['entities']):
            if i["type"]==location_type and float(i['relevance']) > 0.5:
                return(i["text"])
            else:
                return('No reliable location keywords found.')


print(get_country(url))
