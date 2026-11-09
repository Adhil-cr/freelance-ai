# Pricing model (v2), for hand calculation or porting

Mirrors `scripts/quote.py`. Values live in `data/pricing.json`.

## What changed from v1
v1 multiplied the price by a category factor, a client-size factor and a risk factor. They stacked, so a simple personal tool was priced like a product and the realised hourly rate jumped to about Rs 1,500. In v2: category only sets **foundation hours**, risk adds **buffer hours**, the usage type scales foundation and sets a modest client factor, and the realised rate is checked against the freelancer's band.

## Hours
```
foundation   = category.base_hours x usage.base_scale
raw          = foundation + sum(feature hours at the chosen tier)    # features may carry your own hours
tech_scaled  = raw x tech.hours_mult
pre          = tech_scaled + extra_revision_rounds x 4
buffer       = pre x (0.15 + risk.extra_buffer)      # Low 0, Medium 0.10, High 0.25
meetings     = pre x 0.08
total_hours  = pre + buffer + meetings
calendar_days = total_hours / urgency.hours_per_day
```
Category base hours cover setup, design system, navigation, deploy pipeline and basic QA only. Login, admin and real features are separate lines so nothing is counted twice.

## Price
```
effective_rate = base_hourly x experience_mult x tech.rate_mult x urgency.rate_mult
dev_cost       = total_hours x effective_rate x usage.client_mult
fair_price     = dev_cost x (1 + margin 0.20)            # before GST
realised_rate  = fair_price / total_hours                # check against the rate band
anchor         = fair_price x (1 + usage.anchor_uplift)  # personal 10%, business 15%, startup 20%, company 25%
floor          = min(total_hours x min_hourly, 0.90 x fair_price)
gst            = fair_price x 0.18                       # only if the freelancer is registered
```
Usage types: Personal 0.5 foundation / 0.85 client; Small business 0.8 / 1.0; Startup 1.2 / 1.1; Company system 1.3 / 1.2; Not sure 1.0 / 1.0.

## Confidence ranges (never send a single price at Draft)
Draft x0.75 to x1.40, Firm x0.88 to x1.20, Quote-ready x0.95 to x1.08, applied to the fair price. The range is asymmetric because estimates overrun more often than they underrun.

## Budget fit
Given a budget (before GST), drop "later" features then "should" features, largest hours first, until the fair price is within budget. "must" features are never dropped. If still over, say how much, and offer: phase it, simplify the stack, or explain that the budget buys less.

## Rate band check
Band default Rs 500 to 950 realised (after tech premium and margin; base hourly Rs 650), scaled by experience, with the high end scaled up by the client factor when it is above 1. If realised is above, show the price at the band top as the capped alternative. If below the band, warn of underpricing.

## Phase split (expert view)
Of the work hours before buffer and meetings: discovery 7%, UI/UX and prototype 15%, backend and database 28%, frontend 22%, integrations and data 8%, testing 12%, deployment and handover 8%.

## Technology has two effects
`hours_mult`: does it genuinely take longer to build well? `rate_mult`: does the market pay more per hour for this skill? Urgency changes only the rate and the working pace, never the hour count.

## Payments
Under about Rs 60,000: 50% advance, 50% on acceptance. Above: 40% advance, then half of the rest at the midpoint (core features on staging) and half on acceptance. Advance before any design work.

## Change requests
Within included rounds (default 2): free. Extra round: about 4 hours at the effective rate. New feature: quote with the same method in writing before work. Client-caused urgent fix 1.5x; weekend 1.3x; defect in delivered work within warranty: free.

## Honest limits
It is a heuristic for a junior-to-mid freelancer. Treat output as a starting point, check it against the client's budget, the local market, and a bottom-up sense of whether the hours are deliverable. Calibrate after your first few real quotes by adjusting the base rate or experience multiplier, not by editing every number.
