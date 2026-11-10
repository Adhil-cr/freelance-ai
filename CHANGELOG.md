# Changelog

## 1.1.0 (2026-11-10)
- Pricing models: `--options` shows fixed, hourly, milestones, retainer and value-based pricing, plus Lean / Recommended / Premium packages.
- Client type (`client_type`) and client country (`client_region`) change the rate; prices show in the client's currency (approximate rates in `data/regions.json`).
- `--proposal` prints a client-ready proposal draft.
- Country notes: international clients, US/Canada, UK/EU, UAE/Gulf (general knowledge, marked verify).
- Fewer tokens: `SKILL.md` has a routing table so each step opens only the file it needs; the paperwork guide is split into one file per paper; the model is told never to open the data files.
- Unit tests and a GitHub Actions workflow.
- Defaults (small business, India) give the same prices as 1.0.0.

## 1.0.0 (2026-11-08)
First release.
- Intake gate: asks usage type, budget, platform, deadline and scale before any price.
- Usage-based pricing (personal, small business, startup, company system) with a realised-rate check against your band.
- Budget-fit mode, compare mode (what changed), confidence ranges (Draft, Firm, Quote-ready), expert mode.
- Project Card that is updated every reply.
- Plain-language paperwork guide with templates (scope sheet, agreement, change request, acceptance note).
- Client onboarding and communication guide.
- Domain notes: fitness/nutrition, e-commerce/booking, ERP/internal systems. Region notes: India/Kerala.

Repository: added README, MIT license, contributing guide and issue templates.
