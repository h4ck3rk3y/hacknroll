import json
import urllib.parse
import requests

#replace this with global variable
text =("Bali is a famous skateboarding location. You can rent a board for $4.")

# A function that parses the information passed from the extension.
def get_context(text):
    url = 'https://api.wit.ai/message'
    params = {'q':text, 'v': '20170122'}
    r = requests.get(url, params=params, headers={'Authorization': 'Bearer 7WXLSZVVS35BHYSORSJQASAEH7GNLKFI'})
    response = r.json()
    return response

get_context(text)
