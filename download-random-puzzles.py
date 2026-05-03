import json
import os
import requests
import sys
import time

API_URL = 'https://api.chess.com/pub/puzzle/random'

OUTPUT_DIR = 'puzzles'
os.makedirs(OUTPUT_DIR, exist_ok=True)

args = sys.argv[1:]

max_requests = 100
request_interval = 1.5

if len(args) >= 1:
	max_requests = int(args[0])

if len(args) >= 2:
	request_interval = float(args[1])

def extract_date(url):
	# https://www.chess.com/daily/YYYY-MM-DD
	try:
		return url.strip('/').split('/')[-1]
	except:
		return None

seen = set()

for filename in os.listdir(OUTPUT_DIR):
	if filename.endswith('.json'):
		seen.add(filename[:-5])

print(f'Loaded {len(seen)} existing puzzles')

saved = 0

for i in range(max_requests):
	try:
		r = requests.get(API_URL, headers={'User-Agent': 'Wget/1.25'}, timeout=10)
		data = r.json()

		url = data.get('url')
		if not url:
			continue

		date_str = extract_date(url)
		if not date_str:
			continue

		if date_str in seen:
			print(f'[{i}] duplicate {date_str}')
			time.sleep(request_interval)
			continue

		seen.add(date_str)

		path = os.path.join(OUTPUT_DIR, f'{date_str}.json')

		with open(path, 'w', encoding='utf-8') as f:
			json.dump(data, f, ensure_ascii=False, indent='\t')

		saved += 1
		print(f'[{i}] saved {date_str} (new total: {len(seen)})')

		time.sleep(request_interval)

	except Exception as e:
		print(f'[{i}] error: {e}')
		time.sleep(request_interval)

print(f'Done. New puzzles saved: {saved}')