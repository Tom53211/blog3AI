export type SourceId = 'anthropic' | 'openai' | 'deepmind';

/** A single scraped blog post, as stored in the Firestore `blogs` collection. */
export interface BlogPost {
	title: string;
	url: string;
	/** "YYYY-MM-DD", or null when the source showed no date. */
	published_date: string | null;
	source_id: SourceId;
	source_name: string;
	/** When the scraper last saw this post. */
	scraped_at: Date;
}

/** A run of posts sharing the same published month (or the undated group). */
export interface MonthGroup {
	/** "YYYY-MM", or null for the undated group. */
	month: string | null;
	/** Display label, e.g. "June 2026" or "Undated". */
	label: string;
	posts: BlogPost[];
}
