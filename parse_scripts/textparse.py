from bs4 import BeautifulSoup
#import nltk
import requests

# This will come from a global variable or something
import_text = str("The year kicks off with a bang on 1 Jan and New Year, celebrated in Singapore.")
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
    url_request=str("https://gateway-a.watsonplatform.net/calls/url/%sGetAuthors?apikey=AlchemyAPI-2f")
    #service: AlchemyAPI-2f
    #credentals: Credentials-1
    curl -X POST \
    -d "outputMode=json" \
    -d "url=http://techcrunch.com/2016/01/29/ibm-watson-weather-company-sale/" \
    "https://gateway-a.watsonplatform.net/calls/url/%sGetAuthors?apikey=AlchemyAPI-2f"






get_header(import_text, url, webpage)
word_tokenise(import_text)

'''
#Junk code:
for headers in soup.find_all("span", {"class": "mw-headline"}):
    list_of_headers.append(headers.text)
if list_of_headers == []:
    print "No headers detected. Switching to general header detection."
    for headers in soup.find_all("h"):
        list_of_headers.append(headers.text)

def word_tokenise(text):
    print(text)
    print(nltk.pos_tag(text))
'''
