<script lang="ts">
	import type { Entry, Result } from "src/stork";
	import tableStore from "../stores/tableStore";

	export let results: Result[];

	function selectTable(entry: Entry) {
		tableStore.update(() => [entry, true]);
	}
</script>

<div
	class="container m-auto max-w-xl max-h-96 overflow-auto -translate-x-2/4 absolute left-1/2 bg-white shadow-lg rounded-lg"
>
	{#each results as result}
		<div class="border-2 px-3 py-3 border-gray-100 rounded box-border mt-1 mb-1 ">
			<div class="flex justify-between">
				<h3
					class="text-teal-600 font-bold hover:underline"
					on:click={() => selectTable(result.entry)}
				>
					{result.entry.title}
				</h3>
				<button
					class="bg-teal-400 py-1 px-3 rounded hover:bg-teal-500 transition"
					on:click={() => selectTable(result.entry)}>Select</button
				>
			</div>
			<p class="capitalize">{result.entry.fields.tableName.toLowerCase()}</p>
		</div>
	{/each}
</div>
