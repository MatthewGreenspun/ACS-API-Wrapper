<script lang="ts">
	import type { DataSet } from "../types";
	export let dataSet: DataSet;
	export let shouldShowResults: boolean;

	$: numRows = Math.max(
		...Object.keys(dataSet).map((table) => Object.keys(dataSet[table].cols).length)
	);

	let fullView = false;

	function createDownloadLink() {
		let configFile = `
url: "https://api.census.gov/data/2019/acs/acs5"
geo: "zip code tabulation area"
api_key: "INSERT YOUR API KEY HERE"

census_tables:\n`;
		Object.keys(dataSet).forEach((table, idx) => {
			configFile += `  table${idx}:\n`;
			configFile += `    source_table: ${table}\n`;
			configFile += "    columns:\n";

			let colNames = "    column_names:\n";
			Object.keys(dataSet[table].cols).forEach((col) => {
				configFile += `      - ${col.includes("_") ? col.split("_")[1] : col}\n`;
				colNames += `      - ${dataSet[table].cols[col].replace(/\s>|>|\s/g, "_")}\n`;
			});
			configFile += colNames;
		});

		return "data:text/yaml;charset=utf-8," + encodeURIComponent(configFile);
	}
</script>

{#if fullView}
	<div
		class="absolute top-0 bottom-0 left-0 right-0 bg-black opacity-70"
		on:click={() => (fullView = false)}
	/>
{/if}

<div
	class={fullView
		? "absolute top-12 bottom-12 left-12 right-12 bg-white rounded-lg"
		: "overflow-hidden border-2 rounded shadow-sm m-5 p-2"}
	on:click={() => (shouldShowResults = false)}
>
	{#if fullView}
		<div class="flex justify-between bg-teal-700 items-center mb-3">
			<h2 class="ml-3 text-2xl font-bold text-white text-center">Data Set</h2>
			<div class="flex">
				<button
					class="my-1 mr-2 flex items-center bg-teal-400 px-3 rounded hover:bg-teal-500 transition h-7"
				>
					<a href={createDownloadLink()} download="config.yaml">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-6 w-6"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
							/>
						</svg>
					</a>
				</button>
				<button class="bg-red-400 hover:bg-red-500 px-3 py-2" on:click={() => (fullView = false)}>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						/>
					</svg>
				</button>
			</div>
		</div>
	{:else}
		<div class="flex justify-between border-b-2 mb-2 items-center pb-2">
			<h2 class="text-2xl font-bold">Data Set</h2>
			<div class="flex">
				<button
					class="mr-2 flex items-center bg-teal-400 px-3 rounded hover:bg-teal-500 transition h-9"
				>
					<a href={createDownloadLink()} download="config.yaml">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-6 w-6"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
							/>
						</svg>
					</a>
				</button>
				<button
					class="flex items-center bg-teal-400 px-3 rounded hover:bg-teal-500 transition h-9"
					on:click={() => (fullView = !fullView)}
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5 mr-2"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
						/>
					</svg>
					Full View
				</button>
			</div>
		</div>
	{/if}
	<div class={fullView ? "overflow-auto absolute top-12 bottom-3 left-3 right-3" : ""}>
		<table class="mb-2 table-auto border-collapse border border-slate-500">
			<thead>
				<tr>
					{#each Object.keys(dataSet) as table}
						<th class="border border-slate-600 min-w-fit">{table}</th>
					{/each}
				</tr>
			</thead>
			<tbody class="">
				{#each Array(numRows > 0 ? numRows : 0) as _, idx}
					<tr>
						{#each Object.keys(dataSet) as table}
							<td class="p-1 border border-slate-700 min-w-fit"
								>{(() => {
									const col = Object.keys(dataSet[table].cols)[idx];
									return col ? col : "";
								})()}</td
							>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
