# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Blog Aggregator — collects posts from the official blogs of Anthropic, OpenAI, Google, and Google DeepMind and stores them in Firebase Firestore. The SvelteKit frontend (`src/frontend/`) reads from Firestore and displays a unified feed.

## Layout

- `src/backend/` — Python scraper, run as a Cloud Run Job
- `src/frontend/` — SvelteKit SPA, deployed on Firebase Hosting
- `src/backend/config/sources.yaml` — the blog sources and their fetch method

## Architecture

**Pipeline flow:** Cloud Scheduler → Cloud Run Job → `scrape_blogs.py` → Firestore ← SvelteKit frontend

**Key design decisions:**
- Each source is fetched via RSS when a `rss_feed` is set; otherwise Firecrawl converts the page to markdown and Gemini parses it (structured output via `response_schema=BlogFeed`, so the response maps directly to Pydantic models)
- Firestore document ID = post URL, so upserting is idempotent

## Frontend Tasks

For any UI or visual design work on the SvelteKit frontend, invoke the `frontend-design` skill first (`/frontend-design`) before making design decisions or implementing UI changes.

