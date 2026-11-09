# Domain: fitness and nutrition apps

Use for calorie trackers, diet planners, workout trackers, and coaching apps. Pair with `regions/india-kerala.md` for Kerala clients.

## What the product usually needs

**Core (MVP):** profile and goals, calorie and macro calculator, food logging, progress tracking, simple reminders.
**Advanced (phase 2):** meal planner, workout builder, wearable sync, coach dashboard, recipe import, barcode scanning, community or challenges, subscription payments.

## Calculators
- Daily energy estimates usually start from a resting-energy equation (Mifflin-St Jeor is widely used) multiplied by an activity factor, then adjusted for the goal. Treat results as estimates, not prescriptions.
- Show the formula and assumptions to the user, allow manual override, and keep units clear (kg or lb, cm or ft, kcal).
- Add guardrails: minimum age, sensible bounds on calorie targets and rate of weight change, no extreme targets, and a prompt to consult a professional for medical conditions, pregnancy, or very low targets.

## The hard part: regional food data
Global apps are weak on regional dishes. For Kerala this means items like puttu, appam, idiyappam, kappa (tapioca), fish curry (meen curry), beef fry, sadya items, parotta, and varied coconut-oil usage.
- A food database is the largest hidden cost. Budget real time to curate it (see the "Regional food database (curated)" feature).
- Possible sources: India's national food composition tables (the Indian Food Composition Tables from ICMR-NIN) and open datasets. **Check licensing, terms of use, and accuracy before promising anything to the client.** Recipes vary by household, so label values as estimates.
- Serving sizes drive accuracy: use household measures (a cup of rice, a ladle of curry, one piece of parotta) and let users adjust portions.
- Cooking method matters (fried vs steamed, amount of coconut oil). Offer simple variants per dish.
- Decide who maintains the database after launch, and whether users can add custom foods.

## Risks specific to this domain
| Risk | Mitigation |
|---|---|
| Medical-claim liability | Clear disclaimer that the app gives general information and is not medical advice; no diagnosis or treatment claims; referral prompt |
| Harmful targets / disordered-eating triggers | Sensible limits, no shaming language, no extreme-deficit goals, easy path to support resources |
| Inaccurate food data | Cite source, label estimates, versioned database, report-error button |
| Personal and health data | Consent, minimal collection, secure storage, deletion and export (see `risks-and-paperwork.md`) |
| Wearable integrations | Each platform has its own approval and policy process; price and schedule separately |
| App-store review for health apps | Expect stricter review; keep disclaimers and privacy policy ready |

## Discovery questions to ask this client
1. Which goals matter most: weight loss, muscle gain, maintenance, health conditions?
2. Who is the end user: the client alone, many customers, or members of a gym or clinic?
3. Does a nutritionist or dietitian review the content? Who owns the food data?
4. Must it work in Malayalam, English, or both? Voice or text logging?
5. Android only, iOS too, or mobile web first?
6. Which advanced tools are essential at launch (meal plans, workouts, wearables)?
7. Will it be free, subscription, or paid per coaching client?
8. Is offline use important?

## Suggested MVP vs phase 2 for a single-user Kerala fitness app
- MVP: sign-up and profile, calorie and macro calculator, Kerala food database with serving sizes, daily food log, progress charts, privacy controls.
- Phase 2: meal planner, workout library and builder, wearable sync, reminders, reports, coach dashboard.
- Out of scope initially: medical advice, barcode scanning, social features, payments (unless the business model requires it).
