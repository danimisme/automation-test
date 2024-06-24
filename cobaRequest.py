from pprint import pprint

import requests

response = requests.get('https://gorest.co.in/public/v2/users')
print(response.status_code)
pprint(response.json())