import sys
import re as regex
import yaml
import requests
import time 
import numpy as np
import pandas as pd 
import threading

if len(sys.argv) < 2:
	print("No path to config file provided")
	print("usage: <config.yaml> <outfile path>")
	quit()

config_path = sys.argv[1]
if regex.search('.+\.yaml', config_path) is None:
	print('Config file must end in .yaml')
	quit()

if '.yaml' in config_path:
	try: 
		with open(config_path) as config_file:
			config = yaml.full_load(config_file)
	except FileNotFoundError:
		print(f'file "{config_path}" not found')
		quit()
	except:
		print("error reading yaml file")
		quit()

vars = []
var_labels = []
for table in config['census_tables'].values():
	table_code = table['source_table']
	table_vars = [] #used to correct for different number of columns and column names
	for column in table['columns']:
		table_vars.append(f"{table_code}_{column}")

	for idx, column_name in enumerate(table['column_names']):
		if idx >= len(table['columns']):
			break
		var_labels.append(column_name)
	if idx < len(table['columns']) - 1:
		var_labels.extend(table_vars[idx+1:len(table_vars)])
	vars.extend(table_vars)

batch_size = 10 # number of variables per request, census api allows fetching a maximum of 50 variables per request

df_fragments = []
threads = []
lock = threading.Lock()

def req_with_vars(col_vars, col_names):
	url_params = {
		'get': ','.join(col_vars),
		'for': f'{config["geo"]}:*',
		'key': f'{config["api_key"]}',
	}
	url_base = 'https://api.census.gov/data/2019/acs/acs5'
	res = requests.get(url_base, params=url_params)
	
	if res.status_code != 200:
		print("error fetching data")
		print("response:")
		print(res.__dict__)
		quit()

	data = res.json()
	res_col_names = data[0]
	col_names.extend(res_col_names[len(col_names):])
	res_data = np.array(data[1:], dtype=np.int64)
	df = pd.DataFrame(res_data, columns=col_names)
	with lock:
		df_fragments.append(df)

for i in range(0, len(vars), batch_size):
	thread = threading.Thread(target=req_with_vars, args=(vars[i:i+batch_size], var_labels[i:i+batch_size]), daemon=True)
	threads.append(thread)

start_time = time.time()
print("Fetching data ...")
for t in threads:
	t.start()

for t in threads:
	t.join()
end_time = time.time()
print(f"Fetched data in {end_time - start_time} seconds")

state_codes_to_abbr = {1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE', 11: 'DC', 12: 'FL', 13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA', 20: 'KS', 21: 'KY', 22: 'LA', 23: 'ME', 24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN', 28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE', 32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM', 36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK', 41: 'OR', 42: 'PA', 44: 'RI', 45: 'SC', 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT', 51: 'VA', 53: 'WA', 54: 'WV', 55: 'WI', 56: 'WY', 60: 'AS', 64: 'FM', 66: 'GU', 68: 'MH', 69: 'MP', 70: 'PW', 72: 'PR', 74: 'UM', 78: 'VI'}

print("Creating csv file ... ")
start_time = time.time()

final_cols = []
df = pd.concat(df_fragments, axis=1)
df = df.loc[:, ~df.columns.duplicated()]
if 'state' in df.columns:
	df['state'] = df['state'].apply(lambda code: state_codes_to_abbr[code])
	final_cols.append("state")
if 'zip code tabulation area' in df.columns:
	final_cols.append("zip code tabulation area")
final_cols.extend(var_labels)
df = df[final_cols]

outfile_path = sys.argv[2] if len(sys.argv) >= 3 and regex.search('.+\.csv', sys.argv[2]) is not None else "data/data.csv"
df.to_csv(outfile_path)

end_time = time.time()
print(f"Created {outfile_path} in {end_time - start_time} seconds")