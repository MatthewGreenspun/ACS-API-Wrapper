<script lang="ts">
	import type { DataSet } from "src/types";
	import type { Entry } from "src/stork";
	import tableStore from "../stores/tableStore";

	export let dataSet: DataSet;
	export let table: string;
	export let tableDesc: string;
	export let col = "";
	export let colDesc = "";
	export let isTable = true;

	let isHover = false;

	function handleDelete() {
		if (isTable) {
			delete dataSet[table];
			dataSet = { ...dataSet };
		} else {
			delete dataSet[table].cols[col];
			dataSet = { ...dataSet };
		}
	}

	function handleClick() {
		const entry: Entry = {
			title: table,
			url: "https://data.census.gov/cedsci/table?q=" + table,
			fields: {
				tableName: tableDesc,
				colName: colDesc
			}
		};
		tableStore.update(() => [entry, true]);
	}
</script>

<div
	on:mouseenter={() => (isHover = true)}
	on:mouseleave={() => (isHover = false)}
	class="flex items-center cursor-pointer relative"
>
	<h3 class="mr-2" on:click={handleClick}>
		{isTable ? table : col}
	</h3>
	{#if isHover}
		<button
			class="bg-red-400 hover:bg-red-500 rounded w-full flex justify-center"
			on:click={handleDelete}
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="h-5 w-5 "
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
		{#if isTable || col.length > 0}
			<div
				class="absolute rounded-lg p-5 shadow-md top-7 left-3 bg-white w-max max-w-xs transition-transform capitalize z-20"
			>
				{(isTable ? tableDesc : colDesc).toLowerCase()}
			</div>
		{/if}
	{/if}
</div>
