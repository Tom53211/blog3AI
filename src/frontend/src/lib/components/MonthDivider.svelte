<script lang="ts">
	let { label, count }: { label: string; count: number } = $props();
</script>

<div class="divider">
	<span class="eyebrow">{label}</span>
	<span class="eyebrow rule-count">{count}</span>
</div>

<style>
	.divider {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: 1rem;
		padding: 1.75rem 0 0.5rem;
	}

	.rule-count {
		color: var(--hairline);
	}
</style>
