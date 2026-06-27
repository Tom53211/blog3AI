import { collection, getDocs, Timestamp } from 'firebase/firestore';
import { db } from './firebase';
import type { BlogPost, MonthGroup } from './types';

/**
 * Fetch every post from the `blogs` collection. The dataset is small (three
 * index pages, a few hundred posts), so we read it all once and sort/group/
 * filter in memory rather than maintaining Firestore composite indexes.
 */
export async function fetchBlogs(): Promise<BlogPost[]> {
	const snapshot = await getDocs(collection(db, 'blogs'));
	return snapshot.docs.map((doc) => {
		const d = doc.data();
		const scraped = d.scraped_at;
		return {
			title: d.title,
			url: d.url,
			published_date: d.published_date ?? null,
			source_id: d.source_id,
			source_name: d.source_name,
			scraped_at: scraped instanceof Timestamp ? scraped.toDate() : new Date(scraped ?? 0)
		} satisfies BlogPost;
	});
}

const MONTH_NAMES = [
	'January',
	'February',
	'March',
	'April',
	'May',
	'June',
	'July',
	'August',
	'September',
	'October',
	'November',
	'December'
];

/** "2026-06" -> "June 2026". */
function monthLabel(month: string | null): string {
	if (!month) return 'Undated';
	const [year, m] = month.split('-');
	const name = MONTH_NAMES[Number(m) - 1];
	return name ? `${name} ${year}` : month;
}

/**
 * Sort newest-first by published date (string compare works for "YYYY-MM-DD"),
 * tie-broken by most-recently-scraped. Undated posts sink to the bottom.
 * Returns posts grouped into consecutive month sections.
 */
export function sortAndGroup(posts: BlogPost[]): MonthGroup[] {
	const sorted = [...posts].sort((a, b) => {
		const ad = a.published_date;
		const bd = b.published_date;
		if (ad !== bd) {
			if (ad === null) return 1; // a undated -> after b
			if (bd === null) return -1; // b undated -> after a
			return bd.localeCompare(ad); // newer date first
		}
		return b.scraped_at.getTime() - a.scraped_at.getTime();
	});

	const groups: MonthGroup[] = [];
	for (const post of sorted) {
		const month = post.published_date?.slice(0, 7) ?? null;
		const last = groups[groups.length - 1];
		if (last && last.month === month) {
			last.posts.push(post);
		} else {
			groups.push({ month, label: monthLabel(month), posts: [post] });
		}
	}
	return groups;
}
