import anthropic from './assets/logos/anthropic.svg?raw';
import openai from './assets/logos/openai.svg?raw';
import deepmind from './assets/logos/deepmind.svg?raw';
import google from './assets/logos/google.svg?raw';
import type { LabId } from './types';

export interface Lab {
	id: LabId;
	/** Short label shown on filter chips. */
	name: string;
	/** Inline monochrome SVG, rendered via {@html} so it inherits `currentColor`. */
	logo: string;
	/** Firestore `source_id`s that roll up into this lab. */
	sources: string[];
}

/**
 * The labs the record covers, in display order. A lab can gather several feeds:
 * Google ships from more than one blog, but reads as one name on the page.
 */
export const LABS: Lab[] = [
	{ id: 'anthropic', name: 'Anthropic', logo: anthropic, sources: ['anthropic', 'anthropic_news'] },
	{ id: 'openai', name: 'OpenAI', logo: openai, sources: ['openai'] },
	{ id: 'deepmind', name: 'DeepMind', logo: deepmind, sources: ['deepmind'] },
	{ id: 'google', name: 'Google', logo: google, sources: ['google_dev_tools', 'google_research'] }
];

const SOURCE_TO_LAB = new Map<string, LabId>(
	LABS.flatMap((lab) => lab.sources.map((source) => [source, lab.id] as const))
);

/** Which lab a raw Firestore `source_id` belongs to, or undefined if unknown. */
export function labForSource(source_id: string): LabId | undefined {
	return SOURCE_TO_LAB.get(source_id);
}

export const LAB_LOGOS = Object.fromEntries(LABS.map((lab) => [lab.id, lab.logo])) as Record<
	LabId,
	string
>;
