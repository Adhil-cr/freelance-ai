# Contributing

Thanks for helping. The most useful contributions are:

- **Real quote data:** what you quoted versus what the project actually took, so the hours model can be calibrated.
- **New domains** in `freelance-scoper/references/domains/` (follow an existing file's structure: why projects go wrong, commercial approach, hidden costs, questions, risks, paperwork).
- **New regions** in `freelance-scoper/references/regions/`, with a "last reviewed" date and a "verify before relying on it" note.
- **Corrections** to tax, legal or fee information, with a source link.

## Guidelines
- Keep prices and hours in `data/pricing.json`, not in prose.
- Run `python freelance-scoper/scripts/quote.py freelance-scoper/examples/fitness-personal.spec.json` before opening a pull request.
- Use plain language. The audience may be a beginner freelancer.
- Do not present legal or tax content as advice.
