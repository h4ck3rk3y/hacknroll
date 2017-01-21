import requests

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