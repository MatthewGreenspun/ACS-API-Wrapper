import json

formatted_vars = {}

with open("acs_2019_vars.json") as vars_file: 
	vars = json.load(vars_file)
	for (full_col, col_data) in vars.items():
		if len(full_col.split("_")) < 2: 
			formatted_vars[full_col] = {
				full_col: col_data["label"]
			}
			continue
		table, col = full_col.split("_")
		if table not in formatted_vars:
			formatted_vars[table] = {}

		formatted_vars[table][col] = col_data["label"] \
		.replace("Estimate!!", "") \
		.replace("!!", ">") \
		.replace(":", "") \
		.replace("--", "")

sorted_vars = {}
num_tables = 0
num_cols = 0

for table in sorted(formatted_vars):
	num_tables += 1
	sorted_vars[table] = {}
	for col in sorted(formatted_vars[table]):
		num_cols += 1
		sorted_vars[table][col] = formatted_vars[table][col]

print(f"total number of tables: {num_tables}")
print(f"total number of columns: {num_cols}")

with open("acs_2019_vars_by_tableid.json", "w") as outfile:
	json.dump(sorted_vars, outfile, indent=2)	