# Mycelium
Built an early-stage agentic system where Slack and Email agents interpret user intent, query a structured knowledge graph, and return contextual responses.
Key contributions:

Designed a standard agent flow: input → intent classification → knowledge graph query → response/hand-off

Implemented Slack and Email agents, routing messages through a shared backend pipeline

Built a Python-based Google Drive metadata crawler to automate asset ingestion (name, type, owner, timestamps) into a structured catalogue

Identified and documented a critical permission bottleneck with Google Drive APIs (metadata access constrained by org-level permissions)

Designed initial knowledge graph schema (assets, tags, relations) to support agent queries like “find latest policy doc”

Hardest challenge:
The crawler failed on live data due to restricted Drive permissions. I validated that both Sheets and Drive APIs respect access controls, documented the limitation, and proposed permission-aware ingestion workflows instead of brittle scraping.

Tech stack:
Python, HuggingFace transformers, Google APIs, JSON-LD / graph schemas, Slack bot integration
