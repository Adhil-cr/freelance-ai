# Sample conversation (illustrative numbers; the live skill takes every figure from `scripts/quote.py`)

## Turn 1: freelancer pastes the brief

> I want to build a fitness software for my Malayali client from Edappally. He wants to track daily calorie and nutrition intake from each meal and each food item, and track target body weight, current height, weight. Calculate BMR, maintenance calories, etc.

**Claude (asks first, no single price):**

```
PROJECT CARD v1 · confidence: Draft
Client/project: Edappally client, fitness tracker   Usage type: unknown
Platform: unknown   Deadline: unknown   Budget: unknown
Scope: MUST calorie and macro calculator (BMR, maintenance), food log by meal and item with serving sizes, weight and height log, progress charts, Kerala food list | LATER meal planner, Malayalam UI
Stack: Django + PostgreSQL (your stack), mobile-friendly web app
Price: depends on who uses it (below)
```

Three answers change the price more than anything else:

1. **Who will use it?** A) only him, B) a small business with customers, C) a startup product for many users, D) a company's internal system, E) not sure
2. **Budget:** A) under Rs 50k, B) 50k to 1.5 lakh, C) 1.5 to 5 lakh, D) above 5 lakh, E) not decided
3. **Platform:** A) website that works on phone, B) Android app, C) Android and iPhone, D) not sure

If you don't know yet, pick "I don't know" and I'll draft the message for him.

Indicative only, same core features, Draft range before GST:

| If it is for | Draft range |
|---|---|
| Only him (personal) | Rs 81,663 to 1,52,437 |
| A small business | Rs 1,20,582 to 2,25,087 |
| A startup product | Rs 1,62,835 to 3,03,959 |
| A company system | Rs 1,74,109 to 3,25,003 |

## Turn 2: freelancer answers

> Only for him. He said around 1 to 1.5 lakh. A mobile website is fine.

**Claude:**

**Updated to v2 (Firm). What changed:** usage is personal, so admin panel, roles and analytics are out; budget 1.5 lakh applied, which cut the optional meal planner (24 h); price range narrowed from Rs 81,663 to 1,52,437 to **Rs 1,11,461 to 1,51,992**.

```
PROJECT CARD v2 · Firm
Usage: personal (one user)  Platform: mobile web (PWA)  Budget: ~Rs 1 to 1.5 lakh
Scope: MUST login, profile and goals, BMR/maintenance calculator, food log, progress charts, starter Kerala list (about 150 foods)
       SHOULD data export and deletion | LATER Malayalam UI, meal planner (cut to fit budget) | OUT admin, roles, wearables, payments
Price: Rs 1,11,461 to 1,51,992 before GST (midpoint Rs 1,26,660) · 159 h · realised Rs 796/h (within your band)
Anchor Rs 1,39,326 · walk-away floor Rs 79,600
Open questions: 1) Would he rather use an existing app? What does it lack? 2) Is the food list his own data or should you source it? 3) Offline needed?
```

Do not send a single price yet; send the three questions first (draft below). Say "stages", "paperwork" or "onboarding" when you want those sections.

## Turn 3: the budget changes

> Actually his budget is only 1 lakh.

**Claude:**

**Updated to v3. What changed:** budget Rs 1,00,000. After cutting everything optional (meal planner, Malayalam UI, data export) the price is still **Rs 8,883 over** the budget (Rs 1,08,883 for 137 h). Your floor is about Rs 68,000, so Rs 1,00,000 is workable: it is about 8% under fair, a realised rate of about Rs 730/h, and above your minimum.

Three options to put to him: (a) accept Rs 1,00,000 for the core scope with the exclusions written down, (b) Rs 1,00,000 for a smaller food list (about 100 items) and the rest in phase 2, (c) keep the scope and pay Rs 1.1 lakh. I would offer (b). Do not drop below Rs 1,00,000 without removing scope.

## Turn 4 (expert mode): the freelancer signals experience

> I charge 900 an hour and I know the stack. Skip the basics, give me the phase split.

**Claude** switches to `--rate 900 --mode expert`: no explanations, a phase table (discovery, UI/UX, backend, frontend, integrations, testing, deployment), top three cost drivers, sensitivity (tier and plus or minus 20% hours), and the assumptions list, with the per-feature hour overrides applied.
