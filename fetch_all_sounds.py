import urllib.request
import json

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijk5ODYzMTIiLCJuYW1laWQiOiI5OTg2MzEyIiwianRpIjoiODJiYzljY2YtZWJkYS00ODNlLWJjOTMtMDU4ZWVlNzEzODA2IiwiaWF0IjoxNzkyMzc3NjI0LCJhcHJvbGUiOiJSb2xlVXNlciIsImxvY2FsZSI6InJ1IiwiZ210IjoiMyIsIm5iZiI6MTc5MjM3NzYyNCwiZXhwIjoxNzk3NTYxNjI0LCJhdWQiOiJodHRwczovL21vb25seS5hcHAifQ.t6eo9YbAsV5Hsa1uT9a3s-NHgDu0aYTsQ9v403y_CH8'
url = 'https://api.moonly.app/v2/sounds/page?pageIndex=0&pageSize=100'

req = urllib.request.Request(url, headers={
    'User-Agent': 'okhttp/4.9.2',
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json'
})

with urllib.request.urlopen(req, timeout=10) as res:
    data = json.loads(res.read().decode('utf-8'))
    items = data.get('data', [])
    print(f'Total sounds retrieved: {len(items)}, total in DB: {data.get("total")}')
    with open(r'D:\projects\monly\moonly_sounds_api_response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    if items:
        print('Sample item 0:', json.dumps(items[0], ensure_ascii=False, indent=2))
