import sys
from data_grabber import get_config_path, get_vars_from_config, make_csv_from_fragments, request_data

if len(sys.argv) < 2:
	print("No path to config file provided")
	print("usage: <config.yaml> <outfile path>")
	quit()

config_path, config = get_config_path()

vars, var_labels = get_vars_from_config(config)

geo = config["geo"]
api_key = config["api_key"]
df_fragments = request_data(vars, var_labels, geo=geo, api_key=api_key)

make_csv_from_fragments(df_fragments, var_labels)
