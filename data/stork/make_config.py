import json
import sys

def clean(str: str): 
	return str.replace("Estimate", "").replace("!!", " ").replace(":", "").replace("\"", "")

if len(sys.argv) > 1 and sys.argv[1] == "cols":
	print("creating config file for indexing all columns")

	indexed_files = []
	tables_added = set()

	with open("acs_2019_vars.json") as vars_file: 
		vars = json.load(vars_file)
		for full_col, col_data in vars.items():
			if full_col == "GEO" or full_col == "GEO_ID": 
				continue
			if len(full_col.split("_")) < 2: 
				if full_col in tables_added: 
					continue
				file = {
					"contents": clean(col_data["label"]),
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
					"contents": clean(col_data["concept"]),
					"tableName": clean(col_data["concept"]),
					"table": table,
					"title": table 
				}
				indexed_files.append(file)
				tables_added.add(table)
			
			file = {
				"contents": f"{clean(col_data['label'])}\t{clean(col_data['concept'])}",
				"tableName": clean(col_data["concept"]),
				"table": table,
				"title": full_col,
				"colName": clean(col_data["label"])
			}
			indexed_files.append(file)
	indexed_files.sort(key=lambda f: f['title'])

	toml_txt = "[input]\ntitle_boost = \"Ridiculous\"\n"
	for table in indexed_files:
		file_toml_txt = f"""[[input.files]]
	contents = "{table['contents']}"
	title = "{table['title']}"
	url = "https://data.census.gov/cedsci/"
	table = "{table['table']}"
	tableName = "{table['tableName']}"
	{f'colName = "{table["colName"]}"' if 'colName' in table else ""}
	"""
		toml_txt += file_toml_txt
	with open("stork/stork-col-config.toml", "w") as outfile:
		outfile.write(toml_txt)

else: 
	print("creating config file for indexing tables")	

	tables = {}
	with open("acs_2019_vars.json") as vars_file: 
		vars = json.load(vars_file)
		for full_col, col_data in vars.items():
			if full_col == "GEO" or full_col == "GEO_ID": #these tables cause issues for some reason
				continue
			if len(full_col.split("_")) < 2: 
				tables[full_col] = {
					"contents": clean(col_data["label"]),
					"tableName": clean(col_data["label"]),
					"table": full_col,
					"title": full_col, 
					"url": "https://data.census.gov/cedsci/"
				}
				continue
			table, col = full_col.split("_")
			if table not in tables: 
				tables[table] = {
					"contents": clean(col_data["concept"]),
					"tableName": clean(col_data["concept"]),
					"table": table,
					"title": table,
					"url": f"https://data.census.gov/cedsci/table?q={table}"
				}
			tables[table]["contents"] += f"\t{full_col} {clean(col_data['label'])}"

	toml_txt = "[input]\ntitle_boost = \"Ridiculous\"\n"
	for table in sorted(tables):
		file_toml_txt = f"""[[input.files]]
contents = "{tables[table]['contents']}"
title = "{tables[table]['title']}"
url = "{tables[table]['url']}"
tableName = "{tables[table]['tableName']}"
"""
		toml_txt += file_toml_txt
	with open("stork/stork-table-config.toml", "w") as outfile:
		outfile.write(toml_txt)