<script lang="ts">
	import { LAB_LOGOS, labForSource } from '$lib/labs';
	import type { BlogPost } from '$lib/types';

	let { post }: { post: BlogPost } = $props();

	let logo = $derived(labForSource(post.source_id));

	let shortDate = $derived(
		post.published_date
			? `${post.published_date.slice(8, 10)}/${post.published_date.slice(5, 7)}/${post.published_date.slice(2, 4)}`
			: '—'
	);
</script>

<a
	class="row"
	href={post.url}
	target="_blank"
	rel="noopener noreferrer"
	aria-label={`${post.title} — ${post.source_name}`}
>
	<span class="logo" aria-hidden="true">{#if logo}{@html LAB_LOGOS[logo]}{/if}</span>
	<span class="title">{post.title}</span>
	<span class="month mono" aria-hidden="true">{shortDate}</span>
</a>

<style>
	.row {
		display: grid;
		grid-template-columns: 1.25rem 1fr auto;
		align-items: baseline;
		column-gap: 0.9rem;
		padding: 0.7rem 0.6rem;
		margin: 0 -0.6rem;
		border-radius: 4px;
		border-top: 1px solid var(--hairline);
		transition: background 0.15s ease;
	}

	.row:hover,
	.row:focus-visible {
		background: var(--accent-wash);
	}

	.logo {
		display: inline-flex;
		width: 15px;
		height: 15px;
		align-self: center;
		color: var(--ink);
	}

	.logo :global(svg) {
		width: 100%;
		height: 100%;
		fill: currentColor;
	}

	.title {
		font-size: 1.0625rem;
		line-height: 1.35;
		/* Underline that draws in on hover. */
		background-image: linear-gradient(var(--accent), var(--accent));
		background-position: 0 100%;
		background-repeat: no-repeat;
		background-size: 0% 1px;
		transition: background-size 0.25s ease;
		padding-bottom: 1px;
	}

	.row:hover .title,
	.row:focus-visible .title {
		background-size: 100% 1px;
	}

	.month {
		font-size: 0.7rem;
		color: var(--muted);
		letter-spacing: 0.02em;
	}

	@media (max-width: 32rem) {
		.row {
			grid-template-columns: 1.25rem 1fr;
			row-gap: 0.15rem;
		}
		.month {
			grid-column: 3;
			justify-self: start;
		}
	}
</style>
