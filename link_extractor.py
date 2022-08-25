from pprint import pprint
from json import dumps
import requests
end_path = '/'
url = 'http://localhost:3000' + end_path
import re

response = requests.get(url)

response_text = response.text


matches = re.finditer(r'href="(?P<item>.*?)".*?>(?P<name>.*?)<', response_text)
output = []
track_path = set()
counter = 0
for _ in matches:
    data = _.groupdict()
    link = data.get('item')
    if not data.get('name'):
        print('#' * 80)
        pprint(data)
        print('#' * 80)
        continue
    if link.startswith('/') and link.endswith('/') and link not in track_path and end_path in link:
        track_path.add(link)
        counter += 1
        data['position'] = counter
        output.append(data)

pprint(output)
