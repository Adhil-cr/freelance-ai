# Working with clients outside India (freelancer based in India)

Last reviewed: 2026-11-10. Tax points checked against published guidance from payment and accounting firms (not government pages); rates and exchange rates are estimates. **Verify with the official source or a chartered accountant before relying on it. Not legal or tax advice.**

## Pricing
- Set the client region in the spec (`client_region`). The calculator applies a conservative rate multiplier and shows the price in the client's currency. Raise the multiplier as you gain international reviews.
- Exchange rates in `data/regions.json` are approximate. Update them before quoting, and quote in the client's currency to avoid disputes.

## Getting paid
- Common routes: bank wire (SWIFT), Wise, Payoneer, PayPal, Stripe-based invoices. Compare the fee and the exchange margin, not just the headline fee.
- Take the advance before starting, exactly as with Indian clients. Time-zone gaps make late payment harder to chase.
- Ask your bank for the foreign inward remittance certificate (FIRC/FIRA) for each payment. You need it as proof of export income.

## Tax points to verify
- **GST, what counts as an export of services:** all five must hold: you are in India; the client is outside India when the service is delivered; the place of supply is outside India; payment arrives in convertible foreign exchange (or INR where the RBI permits); and you and the client are separate legal entities.
- **GST, how to export:** two routes. File a Letter of Undertaking (LUT) each financial year and export without paying IGST, or pay IGST on the invoice and claim a refund later. Most freelancers choose the LUT. Keep the export invoice and the FIRC/BRC as proof; report exports in your GST returns.
- **GST, registration:** the usual threshold for service providers is Rs 20 lakh turnover a year (Rs 10 lakh in special-category states), and export turnover counts toward it. Ask a CA whether you must register at your turnover, since rules for inter-state services have exceptions.
- **Income:** foreign income is taxable in India. Keep invoices and remittance certificates; consult a chartered accountant once income grows.
- **Client side:** ask whether they will withhold tax. Many clients need a form from you (see the country file).

Sources: Razorpay guide to export of services under GST (updated March 2026); ClearTax GST registration limits.

## Contract points
- Name the governing law and where disputes are settled. Many freelancers choose their own country's law or a neutral arbitration clause; ask a lawyer to review the template once.
- State the currency, who bears bank and transfer fees, the late-payment fee, and that work stays yours until paid.
- Keep the same safeguards: written scope, design sign-off, advance, change requests, IP on full payment.

## Communication
- Agree on overlap hours and a response time. Write for non-native readers: short sentences, no idioms.
- Use calendar invites with the time zone written out. Send written summaries after every call.
- Do not assume WhatsApp. Ask the client's preferred channel (email, Slack, Teams).

## Risks
| Risk | Mitigation |
|---|---|
| Client does not pay | Advance, milestones, hold source code until final payment |
| Platform or payment hold | Do not depend on one channel; keep two ways to get paid |
| Misread requirements across cultures | Written scope with examples and screenshots |
| Overpromising on price to win the job | Use the walk-away floor from the calculator |
