<script lang="ts">
	import type { Entry, Stork } from "src/stork";
	import type { DataSet } from "src/types";
	import { onMount } from "svelte";
	import Search from "../components/Search.svelte";
	import SearchResults from "../components/SearchResults.svelte";
	import SideBar from "../components/SideBar.svelte";
	import DataSetTable from "../components/DataSetTable.svelte";

	import tableStore from "../stores/tableStore";

	let storkInitialized = false;
	let stork: Stork = null;
	async function initializeStork() {
		if (storkInitialized) return;
		stork = (<any>window).stork;
		await stork?.initialize();
		await stork?.register("acs-tables", "/acs-tables.st", {
			forceOverwrite: true
		});
		storkInitialized = true;
	}

	let colSearchInitialized = false;
	let cols: { [tableName: string]: { [colName: string]: string } };
	async function loadCols() {
		if (colSearchInitialized) return;
		const res = await fetch("/acs_2019_vars_by_tableid.json");
		cols = await res.json();
		colSearchInitialized = true;
	}

	onMount(async () => {
		initializeStork();
		loadCols();
	});

	let search = "";

	$: results = search && storkInitialized ? stork?.search("acs-tables", search).results : [];
	let shouldShowResults = false;
	function handleHideResults(
		e: MouseEvent & {
			currentTarget: EventTarget & HTMLDivElement;
		}
	) {
		if (e.target === e.currentTarget) shouldShowResults = false;
	}

	let shouldShowSideBar = false;
	let tableEntry: Entry;
	tableStore.subscribe(([newTableEntry, newShouldShowSideBar]) => {
		tableEntry = newTableEntry;
		shouldShowSideBar = newShouldShowSideBar;
	});

	let dataSet: DataSet = {};
</script>

<svelte:head>
	<script
		lang="js"
		src="https://files.stork-search.net/releases/v1.4.0/stork.js"
		on:load={initializeStork}></script>
</svelte:head>

<div class="flex w-screen h-screen max-h-screen max-w-screen flex-col sm:flex-row">
	<div class="flex flex-col shrink grow-2 h-screen items-center" on:click={handleHideResults}>
		<div class="relative">
			<h1 class="text-3xl text-center font-bold mt-4">
				American Community Survey Data Set Builder
			</h1>
			<Search bind:search bind:shouldShowResults {storkInitialized} />
			{#if shouldShowResults}
				<SearchResults {results} {dataSet} />
			{/if}
		</div>

		{#if Object.keys(dataSet).length > 0}
			<DataSetTable bind:dataSet {shouldShowSideBar} bind:shouldShowResults />
		{/if}
	</div>
	{#if shouldShowSideBar}
		<SideBar
			{tableEntry}
			cols={cols[tableEntry.title]}
			{colSearchInitialized}
			bind:showSideBar={shouldShowSideBar}
			bind:dataSet
		/>
	{/if}
</div>

<input data-stork="acs-tables" class="hidden" />
<div data-stork="acs-tables-output" class="hidden" />
