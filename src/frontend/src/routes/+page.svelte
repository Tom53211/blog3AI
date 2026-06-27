<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchBlogs, sortAndGroup } from '$lib/blogs';
	import { LABS, labForSource } from '$lib/labs';
	import type { BlogPost, LabId } from '$lib/types';
	import Masthead from '$lib/components/Masthead.svelte';
	import LabFilter from '$lib/components/LabFilter.svelte';
	import MonthDivider from '$lib/components/MonthDivider.svelte';
	import EntryRow from '$lib/components/EntryRow.svelte';

	let posts = $state<BlogPost[]>([]);
	let loading = $state(true);
	let failed = $state(false);

	let filters = $state<Record<LabId, boolean>>(
		Object.fromEntries(LABS.map((lab) => [lab.id, true])) as Record<LabId, boolean>
	);

	onMount(async () => {
		try {
			posts = await fetchBlogs();
		} catch (e) {
			console.error('[AI Record] failed to load blogs', e);
			failed = true;
		} finally {
			loading = false;
		}
	});

	let lastUpdated = $derived(
		posts.length ? new Date(Math.max(...posts.map((p) => p.scraped_at.getTime()))) : null
	);

	let visible = $derived(
		posts.filter((p) => {
			const lab = labForSource(p.source_id);
			return lab ? filters[lab] : false;
		})
	);
	let noneSelected = $derived(!Object.values(filters).some(Boolean));

	let groups = $derived(sortAndGroup(visible));
</script>

<svelte:head>
	<title>Blog3AI</title>
	<meta
		name="description"
		content="A running index of posts from Anthropic, OpenAI, Google DeepMind, and Google."
	/>
</svelte:head>

<main class="page">
	<Masthead total={visible.length} {lastUpdated} />

	<div class="controls">
		<LabFilter bind:active={filters} />
	</div>

	{#if loading}
		<p class="state mono">Reading the record…</p>
	{:else if failed}
		<p class="state mono">Couldn't reach the record. Refresh to retry.</p>
	{:else if noneSelected}
		<p class="state mono">No labs selected — pick one above to read the record.</p>
	{:else if visible.length === 0}
		<p class="state mono">Nothing here yet.</p>
	{:else}
		<section class="record">
			{#each groups as group (group.label)}
				<MonthDivider label={group.label} count={group.posts.length} />
				{#each group.posts as post, i (post.url)}
					<EntryRow {post} />
				{/each}
			{/each}
		</section>
	{/if}

	<footer class="foot">
		<span class="eyebrow">{LABS.map((lab) => lab.name).join(' · ')}</span>
	</footer>
</main>

<style>
	.page {
		max-width: var(--measure);
		margin: 0 auto;
		padding: clamp(2.5rem, 8vh, 5rem) 1.25rem 4rem;
	}

	.controls {
		padding-bottom: 0.5rem;
	}

	.state {
		padding: 3rem 0.6rem;
		font-size: 0.8rem;
		color: var(--muted);
	}

	.record {
		margin-top: 0.5rem;
		/* Closing hairline under the last row. */
		border-bottom: 1px solid var(--hairline);
	}

	.foot {
		margin-top: 2.5rem;
		padding-top: 1.25rem;
	}
</style>
