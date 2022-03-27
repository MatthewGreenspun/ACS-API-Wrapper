<script lang="ts">
	import type { Entry, Result } from "src/stork";
	import tableStore from "../stores/tableStore";
	import type { DataSet } from "src/types";

	export let results: Result[];
	export let dataSet: DataSet;

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
				<div class="flex items-center">
					<h3
						class="text-teal-600 font-bold hover:underline"
						on:click={() => selectTable(result.entry)}
					>
						{result.entry.title}
					</h3>
					{#if result.entry.title in dataSet}
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-5 w-5 ml-1 text-green-500"
							viewBox="0 0 20 20"
							fill="currentColor"
						>
							<path
								fill-rule="evenodd"
								d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
								clip-rule="evenodd"
							/>
						</svg>
					{/if}
				</div>
				<button
					class="bg-teal-400 py-1 px-3 rounded hover:bg-teal-500 transition"
					on:click={() => selectTable(result.entry)}>Select</button
				>
			</div>
			<p class="capitalize">{result.entry.fields.tableName.toLowerCase()}</p>
		</div>
	{/each}
</div>
