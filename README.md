# freelance-ai

**An AI skill that plans, prices and manages freelance projects, built for freelancers in India.**

Paste a client's requirement. The skill asks the questions that change the price, then builds a living **Project Card** and a freelancer's playbook: scope, stack, price range, negotiation anchor and walk-away floor, stages and payments, client onboarding, plain-language paperwork and risks.

![version](https://img.shields.io/badge/version-1.1.0-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![python](https://img.shields.io/badge/python-3.8%2B-informational) ![deps](https://img.shields.io/badge/dependencies-none-lightgrey) ![CI](https://github.com/Adhil-cr/freelance-ai/actions/workflows/ci.yml/badge.svg)

## Why it exists

Most freelancers price by gut feeling and lose money to scope creep, late payments and unclear requirements. A scripted FAQ bot cannot fix that, because the right answer depends on **who will use the product**, the budget, the platform and the client's location. This skill asks first, calculates with a transparent model, and updates its answer every time you give new information.

## What it does

| Area | What you get |
|---|---|
| **Intake** | Asks usage type (personal, small business, startup, company system), budget, platform, deadline and scale before quoting. Unknown answers become questions to send the client. |
| **Pricing** | Hours-based model with a realised hourly-rate check, Draft / Firm / Quote-ready ranges, anchor price and walk-away floor. |
| **Pricing models** | The same project priced six ways: fixed, hourly, milestones, retainer, value-based, plus Lean / Recommended / Premium packages for the client to choose from. |
| **Client and country** | Client type (individual, small business, startup, agency, enterprise) and client country change the rate; quotes show the client's currency. |
| **Proposal** | `--proposal` prints a client-ready proposal draft. |
| **Budget fit** | Cuts "later" then "should" scope to meet a budget, or says plainly that the core scope does not fit. |
| **Living Project Card** | Updated every reply, opening with **what changed** (price, hours, scope). |
| **Modes** | Beginner (explains) and expert (phase split, cost drivers, sensitivity, your own rate). |
| **Paperwork** | Which papers a project needs, one short entry each, plus templates: scope sheet, agreement, change request, acceptance note. |
| **Onboarding** | First 48 hours, kickoff agenda, communication rules, weekly update format, difficult-situation scripts. |
| **Context** | Domain notes (fitness and nutrition, e-commerce and booking, ERP and internal systems). Country notes: India/Kerala (GST, TDS, DPDP Act, UPI), plus clients in the UAE/Gulf, UK, EU and US/Canada. |
| **Low token use** | The skill loads only the file a step needs; the calculator reads the data files so the model never has to. |

## Quick start

**In Claude:** download the `.skill` file from the [latest release](../../releases/latest), add it under skills settings, then paste a client brief.

**In any other AI tool:** the skill is plain markdown and JSON.
1. Paste `freelance-scoper/SKILL.md` as the instructions.
2. Upload `references/`, `templates/` and `data/pricing.json` as knowledge files.
3. If the tool cannot run code, ask it to calculate by hand using `references/pricing-model.md`, and check its arithmetic.

**Run the calculator directly** (Python 3.8+, no dependencies):

```bash
cd freelance-scoper
python scripts/quote.py examples/fitness-personal.spec.json --mode brief
python scripts/quote.py examples/fitness-personal.spec.json --budget 100000
python scripts/quote.py examples/erp-company.spec.json --mode expert --rate 900
python scripts/quote.py examples/fitness-uk-client.spec.json --options     # pricing models and packages
python scripts/quote.py examples/fitness-uk-client.spec.json --proposal    # client-ready proposal draft
```

Run the tests: `python -m unittest discover -s tests -v`

## Example

A client in Edappally wants a fitness and nutrition tracker (`examples/fitness-personal.spec.json`, Draft confidence). The same core features price very differently depending on who uses it:

| If it is for | Draft range (before GST) |
|---|---|
| Only him (personal) | Rs 1,14,994 to 2,14,656 |
| A small business | Rs 1,44,110 to 2,69,006 |
| A startup product | Rs 1,71,462 to 3,20,062 |
| A company system | Rs 1,90,579 to 3,55,747 |

And it changes again with the client's country (small-business client, fair price): India Rs 1,92,147; UAE AED 11,764; UK GBP 3,008; US USD 4,367. Exchange rates are approximate and the regional multipliers are conservative estimates; check both before quoting.

The conversation example (`sample-conversation.md`) uses illustrative numbers. See the flow in [`freelance-scoper/examples/sample-conversation.md`](freelance-scoper/examples/sample-conversation.md).

## Repository layout

```
freelance-scoper/
  SKILL.md              skill instructions
  data/pricing.json     rates, multipliers, feature hours (edit this to make it yours)
  data/regions.json     client countries: currency, approximate exchange rate, rate multiplier
  scripts/quote.py      price calculator
  references/           onboarding, communication, paperwork (one file per paper), domains, regions
  templates/            scope sheet, agreement, change request, acceptance note
  examples/             sample specs and a sample conversation
tests/                  unit tests (no dependencies)
.github/workflows/      CI
ROADMAP.md              what is next
```

## Make it yours

- Edit `data/pricing.json`: base hourly rate (default Rs 650), rate band, minimum rate (Rs 500), feature hours, hosting costs.
- Add domains in `references/domains/` and regions in `references/regions/`, then list them in `SKILL.md`.
- Keep "last reviewed" dates honest. Rates, fees and tax rules change.

## Limits

- The price model is a heuristic for a junior-to-mid freelancer. Calibrate it against your first real quotes.
- Paperwork and tax content is a draft to verify. **It is not legal or tax advice.**
- Domain depth covers three areas so far; others get general guidance.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and pull requests are welcome.

## License

[MIT](LICENSE) © 2026 Muhammed Adhil C R
