# Domain: clinics, hospitals and healthcare apps

Use for appointment and patient-record systems, clinic management, diagnostic-lab portals and health apps that store patient information. Fitness and nutrition trackers are covered in `fitness-nutrition.md`.

## Why price and caution go up
Health data is sensitive personal data. Mistakes can harm patients and expose the client and you to claims. Quote discovery first, state clearly what the software does and does not decide, and never present the app as medical advice.

## What is easy to underprice
- Patient records with roles (doctor, reception, admin) and an audit trail of who saw or changed what.
- Appointments, reminders (SMS or WhatsApp) and queue handling.
- Prescription and report uploads, with secure storage and access rules.
- Billing and GST invoices for consultations or tests.
- Backups and a tested restore, because losing records is serious.
- Staff training and a support period.

## Questions to ask
1. Who uses it (doctors, staff, patients) and how many sites?
2. What patient data will be stored, and is it already on paper or in another tool?
3. Who is responsible for medical content and decisions? (it must be the clinic, not the software)
4. Do patients log in, and are minors included?
5. Which integrations: lab systems, payment, SMS or WhatsApp?
6. Where must data be hosted, and who can see it?

## Risks
| Risk | Mitigation |
|---|---|
| Data breach | Access control, encryption, audit log, least-privilege roles, secure hosting |
| Wrong medical output | The software records and calculates only; a clinician decides; written disclaimer |
| Data loss | Backups and a restore test before go-live |
| Legal exposure | Data-processing terms, consent screens, liability cap in the agreement; ask a lawyer to review |

## Paperwork
Agreement with a liability cap and a data-processing clause, NDA, privacy notice and consent wording, acceptance notes per module. Health data is sensitive under India's data protection law; the main duties start in May 2027 (verify), so build consent, erasure and breach handling in now. Involve a lawyer for contracts above a few lakh rupees.

## Calculator
Use category "Clinic / healthcare app" and the features "Patient records (health data)" and "Prescription / report upload", with Medium or High risk.
