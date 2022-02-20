import json

indexed_files = []
tables_added = set()

def clean(str: str): 
	return str.replace("Estimate", "").replace("!!", " ").replace(":", "").replace("\"", "")

with open("acs_2019_vars.json") as vars_file: 
	vars = json.load(vars_file)
	for full_col, col_data in vars.items():
		if full_col == "GEO" or full_col == "GEO_ID": 
			continue
		if len(full_col.split("_")) < 2: 
			if full_col in tables_added: 
				continue
			file = {
				"content": clean(col_data["label"]),
				"tableName": clean(col_data["label"]),
				"table": full_col,
				"title": full_col
			}
			indexed_files.append(file)
			tables_added.add(full_col)
			continue
		table, col = full_col.split("_")
		if table not in tables_added: 
			file = {
				"content": clean(col_data["concept"]),
				"tableName": clean(col_data["concept"]),
				"table": table,
				"title": table 
			}
			indexed_files.append(file)
			tables_added.add(table)
		
		file = {
			"content": f"{clean(col_data['label'])}\t{clean(col_data['concept'])}",
			"tableName": clean(col_data["concept"]),
			"table": table,
			"title": full_col,
			"colName": clean(col_data["label"])
		}
		indexed_files.append(file)
indexed_files.sort(key=lambda f: f['title'])

toml_txt = "[input]\ntitle_boost = \"Ridiculous\"\n"
for idx_file in indexed_files:
	file_toml_txt = f"""[[input.files]]
contents = "{idx_file['content']}"
title = "{idx_file['title']}"
url = "https://data.census.gov/cedsci/"
table = "{idx_file['table']}"
tableName = "{idx_file['tableName']}"
{f'colName = "{idx_file["colName"]}"' if 'colName' in idx_file else ""}
"""
	toml_txt += file_toml_txt
with open("stork/stork-config.toml", "w") as outfile:
	outfile.write(toml_txt)
