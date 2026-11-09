# India and Kerala notes

Last reviewed: 2026-11-08. Verify fees and rules before quoting.

## Language and users
- Malayalam is the main language in Kerala. Many users read English but prefer Malayalam for everyday apps. Ask whether the UI needs Malayalam, English, or both, and whether voice or text input matters.
- Use Unicode Malayalam fonts, test rendering on low-end Android phones, and plan for longer text in translated labels.
- Android dominates in India; iOS share is smaller but not zero. Ask the client's real audience before paying for two platforms. A cross-platform framework or a good mobile web app may be enough for an MVP.
- Many users have patchy connectivity and mid-range phones. Keep the app light and consider offline-tolerant behavior.

## Payments
- UPI is the default for consumers. Common gateways include Razorpay, Cashfree, PayU, and Stripe (for international). Typical gateway fees are around 2 percent plus GST per transaction for cards and some methods, with UPI pricing varying. Verify current fees and onboarding requirements; gateways need business verification (KYC), which can take days.
- Advance payments from clients usually arrive by bank transfer or UPI. Issue a proper invoice for each payment.

## Communication habits
- WhatsApp is the main channel. Keep a written trail: after any call, send a summary message and ask for a "yes".
- Expect clients to be relationship-driven and to negotiate. Anchor high, and trade price for scope.

## Hosting and data
- Choose a server region close to the users (for example Mumbai) for speed, and note that some clients care about data staying in India.
- Cheap shared hosting is fine for brochure sites; apps with login and user data need a VPS or managed cloud with backups.

## Market rates (rough bands, verify locally)
- Junior with one strong project: about Rs 500 to 950 per hour realised; mid-level: about Rs 900 to 1,800; senior or specialist: Rs 1,800 and above. Local clients usually pay less than clients abroad for the same work; do not assume a client's first price is the market price.

## Paperwork
See `paperwork-guide.md` for which papers to use, and `risks-and-paperwork.md` for GST, TDS, stamp duty and data protection. Register the domain and cloud accounts in the client's name.
