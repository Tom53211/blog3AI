<script lang="ts">
	import '@fontsource/newsreader/400.css';
	import '@fontsource/newsreader/500.css';
	import '@fontsource/newsreader/400-italic.css';
	import '@fontsource/ibm-plex-mono/400.css';
	import '@fontsource/ibm-plex-mono/500.css';
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{@render children()}
