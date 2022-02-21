<script lang="ts">
	import type { Stork } from "src/stork";
	import { onMount } from "svelte";
	let storkInitialized = false;
	let stork: Stork = null;
	async function initializeStork() {
		if (storkInitialized) return;
		stork = (<any>window).stork;
		await stork?.initialize();
		await stork?.register("acs-tables", "http://localhost:3000/static/acs-tables.st", {
			forceOverwrite: true
		});
		storkInitialized = true;
	}

	onMount(async () => {
		if (!storkInitialized) await initializeStork();
	});

	let search = "";
	let debounceTimer: NodeJS.Timeout;

	$: results = search && storkInitialized ? stork?.search("acs-tables", search).results : [];
	$: console.log(results);

	function debounce(event: Event) {
		const newSearchValue = (<HTMLInputElement>event.target).value;
		const debounceTime = 300;
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(() => {
			search = newSearchValue;
		}, debounceTime);
	}
</script>

<svelte:head>
	<script
		lang="js"
		src="https://files.stork-search.net/releases/v1.4.0/stork.js"
		on:load={initializeStork}></script>
</svelte:head>

<h1 class="text-4xl text-center font-bold">American Community Survey</h1>

<div class="container flex max-w-xl m-auto mt-6">
	<div class="border-2 border-r-0 px-2 grid place-items-center rounded-l">
		<svg
			class="w-6 h-6 text-teal-600"
			fill="currentColor"
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 24 24"
		>
			<path
				d="M16.32 14.9l5.39 5.4a1 1 0 0 1-1.42 1.4l-5.38-5.38a8 8 0 1 1 1.41-1.41zM10 16a6 6 0 1 0 0-12 6 6 0 0 0 0 12z"
			/>
		</svg>
	</div>
	<input
		class="px-2 py-2 w-100 grow border-2 focus:border-black outline-none rounded-r"
		type="text"
		on:keyup={debounce}
		placeholder={storkInitialized ? "Search" : "Initializing Search Engine..."}
		disabled={!storkInitialized}
	/>
</div>
<div class="container m-auto max-w-xl max-h-96 overflow-auto">
	{#if results && storkInitialized}
		{#each results as result}
			<div class="border-2 px-3 py-3 border-gray-100 rounded box-border mt-1 mb-1">
				<div class="flex justify-between">
					<h3 class="text-teal-600 font-bold hover:underline">{result.entry.title}</h3>
					<button class="bg-teal-400 py-1 px-3 rounded hover:bg-teal-500 transition">Select</button>
				</div>
				<p class="capitalize">{result.entry.fields.tableName.toLowerCase()}</p>
			</div>
		{/each}
	{/if}
</div>

<input data-stork="acs-tables" class="hidden" />
<div data-stork="acs-tables-output" class="hidden" />
