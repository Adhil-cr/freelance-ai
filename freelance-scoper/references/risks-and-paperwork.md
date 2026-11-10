# Risks and tax points

Last reviewed: 2026-11-10. Laws, thresholds and fees change. Present everything below as "verify before relying on it", and never as legal or tax advice.

## Common project risks and mitigations

| Risk | Early sign | Mitigation |
|---|---|---|
| Scope creep | "Can you just add..." in week 2 | Written scope with an exclusions list; change-request rule; revision cap |
| Underpricing | You cannot explain how you got the number | Use the calculator; keep the buffer; do not drop below the floor |
| Unclear requirements | Client cannot answer discovery questions | Paid discovery or a small paid prototype phase first |
| Late payment | Client delays the advance | No advance, no start; milestone payments; hold final handover until paid |
| Client disappears | Slow replies at sign-off stages | Deadlines for feedback in the agreement; project pauses after N days without reply |
| Feedback by committee | Many people, conflicting changes | One named decision-maker who gives all feedback |
| Third-party dependency | Needs a gateway, SMS, or API approval | Start approvals early; price integration separately; state that approval time is outside your control |
| Data/privacy problems | App stores personal data | Consent, minimal collection, deletion path, secure storage (see region file) |
| Estimation error | New tech, unclear domain | Use the Advanced tier and Medium or High risk multiplier; time-box a spike first |

## Paperwork
See `paperwork-guide.md` for which papers a project needs, a one-entry-per-paper explanation, and fill-in templates in `../templates/`.

## India: execution and tax points to verify

- **Validity.** Electronic contracts and e-signatures are generally valid under the Information Technology Act, 2000. An agreement can be valid yet hard to use as evidence if stamp duty was not paid; stamp duty rules differ by state, so check the state's current rules or ask a lawyer.
- **GST.** Registration is generally required once annual turnover from services crosses a threshold (commonly stated as Rs 20 lakh, lower in some special-category states), or earlier in some situations such as certain inter-state supply. Published guidance still gives Rs 20 lakh for services (Rs 10 lakh in special-category states); verify the current figure. Invoices must follow GST format once registered. Exporting services to foreign clients has its own rules (five conditions, a yearly Letter of Undertaking or IGST with refund, and a FIRC as proof); see `regions/international-clients.md`.
- **TDS.** Business clients may deduct TDS on professional or technical fees. Ask whether they will, and keep the certificates for your income-tax filing.
- **Income tax.** Freelance income is business or professional income. Keep invoices and bank records. A chartered accountant is worth consulting once income grows.
- **Data protection.** India's Digital Personal Data Protection Act, 2023 governs processing of personal data; the Rules were notified on 13 November 2025 and come into force in phases: the Data Protection Board provisions at once, consent-manager rules on 12 November 2026, and the main duties (notice, consent, security, breach notification, children's data, erasure, cross-border transfer) on 12 May 2027. Plan products you build now for those duties. Verify dates with MeitY. Practical baseline for any app that stores personal data: clear consent, collect only what is needed, a privacy notice, a way to access and delete data, secure storage, and a breach response plan.

## When to involve a professional
- Contract value above a few lakh rupees, or any app handling health, financial, or children's data.
- Client asks for unlimited liability or full IP assignment before payment.
- Cross-border clients, foreign tax questions, or a registered company on either side.
