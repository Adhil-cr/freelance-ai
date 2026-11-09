# Risks and tax points

Last reviewed: 2026-11-08. Laws, thresholds and fees change. Present everything below as "verify before relying on it", and never as legal or tax advice.

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
- **GST.** Registration is generally required once annual turnover from services crosses a threshold (commonly stated as Rs 20 lakh, lower in some special-category states), or earlier in some situations such as certain inter-state supply. Verify the current threshold. Invoices must follow GST format once registered. Exporting services to foreign clients has its own rules (for example a Letter of Undertaking); verify.
- **TDS.** Business clients may deduct TDS on professional or technical fees. Ask whether they will, and keep the certificates for your income-tax filing.
- **Income tax.** Freelance income is business or professional income. Keep invoices and bank records. A chartered accountant is worth consulting once income grows.
- **Data protection.** India's Digital Personal Data Protection Act, 2023 governs processing of personal data; its rules have been coming into force in phases, so verify the current status. Practical baseline for any app that stores personal data: clear consent, collect only what is needed, a privacy notice, a way to access and delete data, secure storage, and a breach response plan.

## When to involve a professional
- Contract value above a few lakh rupees, or any app handling health, financial, or children's data.
- Client asks for unlimited liability or full IP assignment before payment.
- Cross-border clients, foreign tax questions, or a registered company on either side.
