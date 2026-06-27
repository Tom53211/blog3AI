<script lang="ts">
	import { LOGOS } from '$lib/logos';
	import type { SourceId } from '$lib/types';

	let { active = $bindable() }: { active: Record<SourceId, boolean> } = $props();

	const labs: { id: SourceId; name: string }[] = [
		{ id: 'anthropic', name: 'Anthropic' },
		{ id: 'openai', name: 'OpenAI' },
		{ id: 'deepmind', name: 'DeepMind' }
	];

	function toggle(id: SourceId) {
		active = { ...active, [id]: !active[id] };
	}
</script>

<div class="filter" role="group" aria-label="Filter by lab">
	{#each labs as lab (lab.id)}
		<button
			type="button"
			class="chip"
			class:on={active[lab.id]}
			aria-pressed={active[lab.id]}
			onclick={() => toggle(lab.id)}
		>
			<span class="logo" aria-hidden="true">{@html LOGOS[lab.id]}</span>
			<span class="name mono">{lab.name}</span>
		</button>
	{/each}
</div>

<style>
	.filter {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}

	.chip {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.4rem 0.7rem;
		border: 1px solid var(--hairline);
		border-radius: 999px;
		background: transparent;
		color: var(--muted);
		cursor: pointer;
		transition:
			color 0.15s ease,
			border-color 0.15s ease,
			background 0.15s ease;
	}

	.chip:hover {
		border-color: var(--muted);
	}

	.chip.on {
		color: var(--ink);
		border-color: var(--ink);
	}

	.name {
		font-size: 0.75rem;
		letter-spacing: 0.02em;
	}

	.logo {
		display: inline-flex;
		width: 14px;
		height: 14px;
		opacity: 0.45;
		transition: opacity 0.15s ease;
	}

	.chip.on .logo {
		opacity: 1;
	}

	.logo :global(svg) {
		width: 100%;
		height: 100%;
		fill: currentColor;
	}
</style>
