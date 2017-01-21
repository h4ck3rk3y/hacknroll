from bs4 import BeautifulSoup

#This will come from a global variable or something
example_import_text = "The year kicks off with a bang on 1 Jan and New Year, celebrated in Singapore."
example_url = "http://wikitravel.org/en/Singapore"
example_webpage = 'example_webpage.htm'

# A function that parses the information passed from the extension using wit.
def get_headers(text, full_webpage):
    list_of_stuff_thats_important =["warning", "WARNING", "Warning"]
    # instantiate the parser and feed it some HTML
    f=open('example_webpage.htm', 'r')
    soup = BeautifulSoup(f, 'html.parser')
    list_of_headers = []
    for headers in soup.find_all("span", {"class":"mw-headline"}):
        list_of_headers.append(headers.text)
    if list_of_headers == []:
        print "No headers detected. Switching to general header detection."
        for headers in soup.find_all("h"):
            list_of_headers.append(headers.text)

get_headers(example_import_text, example_webpage)
