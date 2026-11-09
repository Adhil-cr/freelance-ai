# Domain: e-commerce and booking platforms

Use for online stores, marketplaces, appointment or table booking, and rental systems.

## E-commerce: what is easy to underprice
- Checkout is where complexity hides: taxes (GST), shipping rules, coupons, returns and refunds, order status emails, abandoned carts.
- Payment gateway onboarding needs the client's business KYC and can take days; start early and price integration separately.
- Inventory: manual stock updates vs sync with another system changes the price sharply.
- Product data: who uploads products, and in what format? Bulk import is a separate task.
- Security: never store card data yourself; use the gateway's hosted checkout.

## Booking systems: what is easy to underprice
- Availability logic (slots, durations, buffers, holidays, time zones), double-booking prevention, cancellations and rescheduling, reminders (SMS, WhatsApp, email), and staff or resource calendars.
- Payments for deposits vs full payment, and refund rules for cancellations.

## Marketplace extras
Multi-vendor onboarding, commission rules, payouts, dispute handling, moderation. Treat as a much larger project; quote discovery first.

## Questions to ask
1. How many products or services, and who maintains them?
2. How will customers pay and how will money reach the client (gateway, UPI, cash on delivery)?
3. Shipping or service areas, delivery partners, and return policy?
4. Do you need invoices with GST, and are you registered?
5. Is there an existing website, catalog, or customer list to migrate?
6. Peak traffic expectations (sales, festivals)?

## Risks
Payment failures and reconciliation, overselling stock, fake bookings, refund disputes, GST invoice mistakes, and dependence on gateway or SMS providers. Mitigate with webhook handling, stock checks at order time, OTP or deposit for bookings, and clear refund policies written into the terms.
