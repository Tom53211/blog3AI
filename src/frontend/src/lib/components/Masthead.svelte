<script lang="ts">
	let { total, lastUpdated }: { total: number; lastUpdated: Date | null } = $props();

	const fmt = new Intl.DateTimeFormat('en-GB', {
		day: '2-digit',
		month: 'short',
		year: 'numeric',
		hour: '2-digit',
		minute: '2-digit'
	});

	let updated = $derived(lastUpdated ? fmt.format(lastUpdated) : null);
</script>

<header class="masthead">
	<h1>The AI Record</h1>
	<p class="mono sub">
		<span>{total} {total === 1 ? 'entry' : 'entries'}</span>
		{#if updated}
			<span class="dot" aria-hidden="true">·</span>
			<span>updated {updated}</span>
		{/if}
	</p>
</header>

<style>
	.masthead {
		margin-bottom: 1.75rem;
	}

	h1 {
		margin: 0;
		font-style: italic;
		font-weight: 400;
		font-size: clamp(2.4rem, 7vw, 3.5rem);
		letter-spacing: -0.01em;
		line-height: 1;
	}


	.sub {
		margin: 0.9rem 0 0;
		font-size: 0.75rem;
		letter-spacing: 0.04em;
		color: var(--muted);
	}

	.dot {
		margin: 0 0.4em;
	}
</style>
