<script lang="ts">
	export let search: string;
	export let shouldShowResults: boolean;
	export let storkInitialized: boolean;

	let debounceTimer: NodeJS.Timeout;
	function debounce(event: Event) {
		const newSearchValue = (<HTMLInputElement>event.target).value;
		const debounceTime = 300;
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(() => {
			search = newSearchValue;
		}, debounceTime);
	}
</script>

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
		on:focus={() => (shouldShowResults = true)}
	/>
</div>
