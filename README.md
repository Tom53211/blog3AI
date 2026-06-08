# AI Blog Aggregator

A lightweight, automated news feed that scrapes the official blogs of OpenAI, Anthropic, and Google DeepMind, aggregates them into a single dashboard, and summarizes them using Gemini.

## 🚀 Tech Stac


- **Frontend:** SvelteKit + TailwindCSS (Deployed on Firebase)
- **Database:** Firebase Firestore
- **Scraper & Cron:** Cloud Run Jobs + Cloud Scheduler (Triggered 2x daily)
- **AI Processing:** Gemini via Vertex AI

---

## 🛠️ How It Works

1. **Trigger:** Cloud Scheduler kicks off the Cloud Run Job twice a day.
2. **Scrape:** The job fetches the latest raw HTML/text from the three target blogs.
3. **Parse:** The raw data is sent to Gemini, which extracts the exact titles, clean URLs, and generates a quick 1-sentence summary.
4. **Store:** The parsed data is upserted into Firestore (using the URL as the document ID to prevent duplicates).
5. **Display:** The SvelteKit frontend reads directly from Firestore to show the latest updates.

---

## 📂 Project Structure

```text
├── frontend/          # SvelteKit application
└── scraper/           # Cloud Run Job script (Node.js/Python)
