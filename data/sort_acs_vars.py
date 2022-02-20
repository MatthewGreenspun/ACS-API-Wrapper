import json

formatted_vars = {}

with open("varlist/acs_2019_vars.json") as vars_file: 
	vars = json.load(vars_file)
	for (full_col, col_data) in vars.items():
		if len(full_col.split("_")) < 2: 
			print(f"fullcol: {full_col} col_data: {col_data}")
			formatted_vars[full_col] = {
				"tableName": col_data['label'],
				"cols": {}
			}
			continue
		table, col = full_col.split("_")
		if table in formatted_vars:
			formatted_vars[table]["cols"][col] = col_data["label"].replace("!!", ">").replace(":", "")
		else: 
			formatted_vars[table] = {
				"tableName": col_data["concept"],
				"cols": {}
			}

sorted_vars = {}
num_tables = 0
num_cols = 0

for table in sorted(formatted_vars):
	num_tables += 1
	sorted_vars[table] = {
		"tableName": "", 
		"cols": {}
	}
	sorted_vars[table]["tableName"] = formatted_vars[table]["tableName"]
	for col in sorted(formatted_vars[table]["cols"]):
		num_cols += 1
		sorted_vars[table]["cols"][col] = formatted_vars[table]["cols"][col]

print(f"total number of tables: {num_tables}")
print(f"total number of columns: {num_cols}")

with open("varlist/acs_2019_vars_by_tableid.json", "w") as outfile:
	json.dump(sorted_vars, outfile, indent=2)	

varlist = []
for table_id in sorted_vars:
	table = {
		"tableId": table_id,
		**sorted_vars[table_id]
	}
	varlist.append(table)

with open("varlist/acs_2019_vars_list.json", "w") as outfile:
	json.dump(varlist, outfile, indent=2)	

# index file for tinysearch
tinysearch_varlist = []
title = "{var_id}-{var_name}"
for table in varlist:
	if table["tableId"] == "GEO":
		continue
	index = {
		"title": title.format(var_id=table["tableId"], var_name=table["tableName"]),
		"url": "",
	}
	tinysearch_varlist.append(index)
	for col, col_name in table["cols"].items():
		var_id = table["tableId"] + "_" + col
		var_name=col_name.replace("Estimate>Total>", "").replace("Estimate>", "").replace("\"", "")
		index = {
			"title": title.format(var_id=var_id, var_name=var_name),
			"url": "",
		}
		tinysearch_varlist.append(index)


with open("varlist/tinysearch.json", "w") as outfile:
	json.dump(tinysearch_varlist, outfile, indent=2)
