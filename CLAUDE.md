# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Blog Aggregator — scrapes the official blogs of Anthropic, OpenAI, and Google DeepMind, parses posts with Gemini (structured JSON output), and stores them in Firebase Firestore. The SvelteKit frontend (not yet in this repo) reads from Firestore and displays a unified feed.

## Architecture

**Pipeline flow:** Cloud Scheduler → Cloud Run Job → `scrape_blogs.py` → Firestore ← SvelteKit frontend

**Key design decisions:**
- Firecrawl converts each blog page to markdown before it reaches Gemini — keeps prompts simple and avoids HTML parsing
- Gemini structured output (`response_schema=BlogFeed`) guarantees the response parses directly into Pydantic models
- Firestore document ID = post URL, so upserting is idempotent

## Frontend Tasks

For any UI or visual design work on the SvelteKit frontend, invoke the `frontend-design` skill first (`/frontend-design`) before making design decisions or implementing UI changes.

