import anthropic from './assets/logos/anthropic.svg?raw';
import openai from './assets/logos/openai.svg?raw';
import deepmind from './assets/logos/deepmind.svg?raw';
import type { SourceId } from './types';

/**
 * Inline monochrome SVG markup per lab. Imported `?raw` so the marks render via
 * {@html} and inherit `currentColor` — keeping the palette to ink + one accent.
 */
export const LOGOS: Record<SourceId, string> = {
	anthropic,
	openai,
	deepmind
};
