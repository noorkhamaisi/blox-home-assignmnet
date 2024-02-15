import requests

resp = requests.get('http://localhost:5005/state?fileName=blocks.json&blockNumber=2')
if resp.status_code == 200:
    print(resp.json())  
else:
    print('Error:', resp.status_code, resp.text)