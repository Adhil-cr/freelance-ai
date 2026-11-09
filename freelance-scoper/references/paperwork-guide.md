# Paperwork guide, in plain language

Last reviewed: 2026-11-08. This is a practical guide, not legal or tax advice. Laws, thresholds and stamp-duty rules change and differ by state, so verify before relying on anything marked "verify". For larger contracts, ask a lawyer to review your template once and reuse it.

## Step 1: Which papers does this project need?

| Project | Minimum set | Add when |
|---|---|---|
| Personal use, small budget | Scope sheet + short agreement (or a proposal the client accepts in writing) + invoices | Client wants an NDA |
| Small business | Above + change request form + acceptance note | Client stores customer data (privacy terms) |
| Scalable startup | Above + IP clause + NDA | Investors will review ownership; user data (privacy terms) |
| Company / ERP | Full agreement, NDA, privacy and data terms, vendor documents, purchase order | Long projects: milestone schedule and a support agreement |

If you only do one thing: **a written scope with an exclusions list that the client has approved in writing.** It prevents most disputes.

## Step 2: The papers, one by one

### 1. Scope sheet (1 page)
- **In one line:** what exactly will and will not be built.
- **When:** after the discovery call, before the price is final.
- **Must include:** goal; features in the first version; features explicitly not included; platforms and languages; what you need from the client; acceptance criteria per feature; assumptions.
- **Watch out:** vague words ("modern", "simple", "like app X"). Replace with a list.
- Template: `templates/scope-sheet.md`.

### 2. Proposal or quotation
- **In one line:** the offer: scope summary, price, timeline, payment schedule, validity.
- **Must include:** price before GST, what GST will be if you charge it, how long the offer is valid (for example 14 days), revision rounds included, what is not included.
- **Watch out:** a single price while scope is still unclear. Give a range until it is.

### 3. Agreement (the contract)
- **In one line:** who agreed to do what, for how much, by when, and what happens if things go wrong.
- **Must include:** the 14 clauses in `templates/simple-agreement.md`, in plain words.
- **Watch out:** unlimited liability, "full IP on signing" (should be on full payment), no payment dates, no way to end the contract.
- **Signing:** electronic signatures are generally valid in India (verify the method you use, for example Aadhaar e-sign). An agreement can be valid but hard to use as evidence if stamp duty was not paid; stamp duty rules differ by state (verify for your state).

### 4. NDA (confidentiality agreement)
- **In one line:** both sides promise not to share the other's secrets.
- **When:** the client asks, or you will see business data, customer data or unreleased ideas.
- **Must include:** what is confidential, how long, exceptions (public information), return or deletion of data.
- **Watch out:** NDAs that stop you from showing the work in your portfolio without a carve-out. Ask for permission to show non-confidential screenshots.

### 5. Invoice
- **In one line:** your formal request for payment.
- **Must include:** invoice number, date, your and the client's names and addresses, description of the work or milestone, amount, due date, bank or UPI details. If you are GST-registered: GSTIN, tax breakdown and the required format (verify).
- **Watch out:** unregistered freelancers cannot charge GST; verify whether you must register (threshold and special cases apply). Issue an invoice for each payment including the advance.

### 6. Change request form
- **In one line:** a short written quote for anything outside the scope.
- **Must include:** what changes, extra hours, extra price, effect on the date, client approval line.
- Template: `templates/change-request.md`.

### 7. Acceptance note
- **In one line:** the client confirms the work meets the agreed criteria.
- **When:** at each milestone and at the end. Final payment is due on this.
- **Must include:** what was delivered, the acceptance checklist result, remaining small fixes with dates, date and name.
- Template: `templates/acceptance-note.md`.

### 8. Handover note
- **In one line:** everything the client needs to run the product without you.
- **Must include:** where it is hosted, logins transferred, how to back up, how to add a user or change content, third-party services and renewal dates, how to contact you for support within the warranty period.

### 9. Privacy and data terms (when the product stores personal data)
- **In one line:** who is responsible for people's data and how it is protected.
- **Must include:** the client decides what data is collected (usually the "data fiduciary" in India's data-protection law, verify), you process it on their instructions, security measures, deletion and export, breach notification, no use of data for your own purposes.
- **For apps:** a privacy notice for end users, consent where required, and a way to delete data. Verify the current status of India's Digital Personal Data Protection Act rules before launch.
- **Extra care:** health data, children's data, financial data.

### 10. Vendor and tax documents (companies)
- Your PAN, bank details, GST registration if you have it, a work order or purchase order from the company, and your invoice.
- Companies often deduct TDS on professional or technical fees and should give you a TDS certificate; keep it for your tax filing (verify rates and forms).

## Step 3: Which paper at which stage

| Stage | Paper |
|---|---|
| After discovery call | Scope sheet, proposal |
| Client says yes | Agreement, NDA (if any), advance invoice |
| Design done | Design approval message (written "approved") |
| During build | Change request forms, weekly updates |
| Milestones | Acceptance note, milestone invoice |
| Launch | Handover note, final acceptance note, final invoice |
| After launch | Maintenance agreement (monthly) |

## Plain-language glossary
- **Scope:** the list of what you will build.
- **Change request:** a priced addition outside the scope.
- **Acceptance criteria:** how both sides will know a feature is done.
- **IP (intellectual property):** who owns the code and designs. Common rule: client owns the final deliverables once fully paid; you keep your reusable tools and the right to mention the project.
- **Warranty:** a free-fix period for defects in what you delivered.
- **Liability cap:** a limit on how much you could owe if something goes wrong. Common: the amount the client paid you.
- **TDS:** tax a client may deduct from your fee and pay to the government on your behalf.
- **GST:** a tax added to invoices if you are registered.
- **Stamp duty:** a state fee that makes some agreements stronger as evidence.
