# Technical Requirements & Architecture

## Overview
The Root Directory (QuickUtils API Manager) serves as the primary code staging area and orchestrator of core automation scripts used across child repositories (Open Source, Datasets, Tools). It is essential that this repository maintains absolute code health, as modifications here are routinely distributed to downstream components.

## Core Technologies
- **Python 3.11+**: The centralized environment scripting and scraping tool logic.
- **Git / GitHub Actions**: Central orchestrator workflow deployments.

## Strict Operational Mandates
1. **Never Assume 200 OK**: Link checkers must intrinsically account for WAF (Web Application Firewall) bots (e.g., HTTP 403, 405, 429) to prevent false-negative deployment crashes.
2. **Synchronized Test Constraints**: Every time a major branch or function is altered, its corresponding Async Pytest mock must be physically rewritten to account for new logical branches.
3. **No Placeholders**: Never upload `database.json` schemas featuring "Sample Data 1". All data schemas must natively inject verified, real-world data entries exceeding 50+ structures.
4. **Git Discipline**: Virtual Environments `.venv` and logging files `*.txt` must immediately map into `.gitignore`. No temporary build artifacts shall pollute the main branches.
5. **No Blind Global Deletions**: Always verify active directories (`find`, `grep`) prior to executing recursive logic across multiple workspaces.

## Operating Principles
1. **Single Source of Truth Scripts**: The root repo develops generator scripts (`generate_real_data.py`, `generate_docs.py`) meant to be generalized across all domain boundaries.
2. **Modular Zero-Cost Frameworks**: Build assets expecting they run completely isolated across multiple cloud hosting layers (Cloudflare Pages) effortlessly without relying on native backends.
