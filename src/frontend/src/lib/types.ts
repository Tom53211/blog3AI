/**
 * A lab the UI groups posts under. Distinct from a Firestore `source_id`: a
 * single lab can span several feeds (Google publishes from more than one blog),
 * so {@link labForSource} maps raw source ids onto these.
 */
export type LabId = 'anthropic' | 'openai' | 'deepmind' | 'google';

/** A single scraped blog post, as stored in the Firestore `blogs` collection. */
export interface BlogPost {
	title: string;
	url: string;
	/** "YYYY-MM-DD", or null when the source showed no date. */
	published_date: string | null;
	/** Raw Firestore feed id, e.g. "google_research". Group via {@link labForSource}. */
	source_id: string;
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
