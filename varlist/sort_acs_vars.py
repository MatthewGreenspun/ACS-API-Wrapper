import json

formatted_vars = {}

with open("varlist/acs_2019_vars.json") as vars_file: 
	vars = json.load(vars_file)
	for (full_col, col_data) in vars.items():
		if len(full_col.split("_")) < 2: 
			formatted_vars[full_col] = {
				"table_name": f"{full_col} - {col_data['label']}",
				"cols": {}
			}
			continue
		table, col = full_col.split("_")
		if table in formatted_vars:
			formatted_vars[table]["cols"][col] = col_data["label"].replace("!!", ">").replace(":", "")
		else: 
			formatted_vars[table] = {
				"table_name": col_data["concept"],
				"cols": {}
			}

sorted_vars = {}
num_tables = 0
num_cols = 0

for table in sorted(formatted_vars):
	num_tables += 1
	sorted_vars[table] = {
		"table_name": "", 
		"cols": {}
	}
	sorted_vars[table]["table_name"] = formatted_vars[table]["table_name"]
	for col in sorted(formatted_vars[table]["cols"]):
		num_cols += 1
		sorted_vars[table]["cols"][col] = formatted_vars[table]["cols"][col]

print(f"total number of tables: {num_tables}")
print(f"total number of columns: {num_cols}")

with open("varlist/sorted_acs_2019_vars.json", "w") as outfile:
	json.dump(sorted_vars, outfile, indent=2)	
