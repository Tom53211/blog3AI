# AI Blog Aggregator

A lightweight, automated news feed that scrapes the official blogs of OpenAI, Anthropic, Google, and Google DeepMind, aggregates them into a single dashboard, and summarizes them using Gemini.

## 🚀 Tech Stack


- **Frontend:** SvelteKit + TailwindCSS (Deployed on Firebase)
- **Database:** Firebase Firestore
- **Scraper & Cron:** Cloud Run Jobs + Cloud Scheduler (Triggered 2x daily)
- **AI Processing:** Gemini via Vertex AI

---

## 🛠️ How It Works

1. **Trigger:** Cloud Scheduler kicks off the Cloud Run Job twice a day.
2. **Scrape:** The job fetches the latest posts from each source — via its RSS feed when available, otherwise scraping the page to markdown with Firecrawl.
3. **Parse:** Markdown-scraped sources are sent to Gemini, which extracts the exact titles, clean URLs, and generates a quick 1-sentence summary.
4. **Store:** The parsed data is upserted into Firestore (using the URL as the document ID to prevent duplicates).
5. **Display:** The SvelteKit frontend reads directly from Firestore to show the latest updates.

---

## 📂 Project Structure

```text
src/
├── frontend/          # SvelteKit application (Firebase Hosting)
└── backend/           # Python scraper run as a Cloud Run Job
```
