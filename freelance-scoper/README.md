# freelance-scoper (v2)

An interactive skill for freelancers. It asks the right questions first, then turns a client's requirement into a living Project Card and a playbook: scope (must/should/later), stack, price range with budget fit, anchor and walk-away floor, stages and payments, client onboarding and communication, plain-language paperwork with templates, risks, and recurring costs. Default focus: India and Kerala.

## What changed in v2
- **Asks before pricing:** usage type (personal / small business / startup / company system), budget, platform, deadline, scale. Unknown answers become questions to send to the client.
- **Price follows project type.** No more stacked category and risk multipliers; the realised hourly rate is checked against your band.
- **Budget fit:** cuts "later" then "should" scope to meet a budget, or tells you plainly that the core scope does not fit.
- **Dynamic replies:** a Project Card is updated each turn, and the reply opens with what changed (price, hours, scope).
- **Expert mode:** phase breakdown, cost drivers, sensitivity, your own rate and hour overrides.
- **Paperwork made simple:** "which papers does this project need", one short entry per paper, plus fill-in templates (scope sheet, plain-language agreement, change request, acceptance note).
- **Onboarding and communication:** first 48 hours, kickoff agenda, communication rules, weekly update format, client-type tips, difficult-situation scripts, handover.

## Use in Claude
Add the `.skill` file in skills settings, then paste a client brief. Claude asks its questions first.

## Use in other AI tools
It is plain markdown and JSON.
1. Paste `SKILL.md` as the instructions or system prompt.
2. Upload `references/`, `templates/`, and `data/pricing.json` as knowledge files.
3. If the tool cannot run code, tell it to calculate by hand using `references/pricing-model.md` and show each step. Models make arithmetic mistakes, so check the numbers.

## Make it yours
- Edit `data/pricing.json`: base hourly rate (default Rs 650), rate band, minimum rate (default Rs 500), feature hours, hosting, usage profiles.
- Add domains in `references/domains/`, regions in `references/regions/`, and list them in `SKILL.md`.
- Keep "last reviewed" dates honest; rates, fees and tax rules change.

## Run the calculator directly
```
python scripts/quote.py examples/fitness-personal.spec.json --mode brief
python scripts/quote.py examples/fitness-personal.spec.json --budget 100000
python scripts/quote.py examples/erp-company.spec.json --mode expert --rate 900
python scripts/quote.py spec.json --json > state/result-v2.json
python scripts/quote.py spec.json --compare state/result-v1.json
```

## Limits
- The price model is a heuristic for a junior-to-mid freelancer. Check it against the client's budget and your market, and calibrate after your first few real quotes.
- Paperwork and tax content is a draft to verify, not legal or tax advice. I did not re-check current rules.
- Domain depth: fitness/nutrition, e-commerce/booking, ERP/internal systems. Other domains get general guidance.
- The script and examples are tested; the skill has not been through a full evaluation on many real briefs. Collect real briefs and refine.
