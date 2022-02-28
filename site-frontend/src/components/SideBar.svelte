<script lang="ts">
	import type { Entry } from "../stork";
	import type { DataSet, ColList } from "../types";
	import { onMount } from "svelte";

	export let showSideBar: boolean;
	export let tableEntry: Entry;
	export let cols: { [colName: string]: string };
	export let colSearchInitialized: boolean;
	export let dataSet: DataSet;

	$: isTable = !Object.keys(cols).includes(tableEntry.title);

	let allChecked = false;
	let colArr: ColList = [];
	function makeColArr(checked = false) {
		colArr = [...Array(Object.keys(cols).length)].map((_, idx) => ({
			checked,
			col: isTable ? `${tableEntry.title}_${Object.keys(cols)[idx]}` : tableEntry.title,
			colName: Object.values(cols)[idx]
		}));
	}
	onMount(() => makeColArr());

	$: cols, makeColArr();
	$: cols, (() => (allChecked = false))();

	function handleSelectAllChecked() {
		makeColArr(!allChecked);
		allChecked = !allChecked;
	}

	function addColsToDataSet() {
		const colsToAdd = {};
		colArr.forEach((col) => {
			if (col.checked) colsToAdd[col.col] = col.colName;
		});
		dataSet = {
			...dataSet,
			[tableEntry.title]: {
				tableName: tableEntry.fields.tableName,
				cols: colsToAdd
			}
		};
	}
</script>

<div class="w-64 border-l-2 border-b-2 overflow-auto grow min-w-min">
	<div class="flex justify-end bg-teal-700">
		<button class="bg-red-400 hover:bg-red-500 px-3 py-1" on:click={() => (showSideBar = false)}>
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
	<div class="border-b-2 p-3">
		<div class="flex justify-between flex-wrap">
			<h2 class="text-2xl font-bold text-teal-600 flex-1 mr-5">{tableEntry.title}</h2>
			{#if isTable}
				<a href={tableEntry.url} target="_blank" class="underline text-teal-500 text-lg"
					>View on census.gov</a
				>
			{/if}
		</div>
		<p class="capitalize mt-2">{tableEntry.fields.tableName.toLowerCase()}</p>

		<div class="mt-2 flex justify-between items-center flex-wrap">
			<div class="flex items-center mr-5 mb-3">
				<input
					type="checkbox"
					id="select-all"
					on:change={handleSelectAllChecked}
					checked={allChecked}
					class="mr-2"
				/>
				<label for="select-all">Select All</label>
			</div>
			<button
				class="bg-teal-400 py-1 px-3 rounded hover:bg-teal-500 transition"
				on:click={addColsToDataSet}
			>
				Add to Data Set</button
			>
		</div>
	</div>
	<div class="h-4 bg-teal-700" />

	<div class:animate-pulse={!colSearchInitialized} class="border-collapse border-t-2">
		{#if !colSearchInitialized}
			<h2 class="text-lg text-center mt-5">Loading Columns ...</h2>
		{/if}
		{#each colArr as col}
			<div class="p-2 border-b-2 hover:bg-yellow-50">
				<div class="flex items-center">
					<input type="checkbox" bind:checked={col.checked} class="mr-2 w-4" />
					<h2 class="text-teal-600 font-bold">{col.col}</h2>
				</div>
				<p>{col.colName}</p>
			</div>
		{/each}
	</div>
</div>
