# Marketplace MVP

Arjuna Badger Press has two marketplace legs:

- ACX-style audiobook production for authors and narrators outside the usual audiobook royalty rails.
- Small-batch print jobs matched with idle printing press capacity.

## Hosting rule

Keep `arjunabadger.press` on GitHub Pages while the public site is static.

Use Webdock for `api.arjunabadger.press` only when private state is required:

- uploaded manuscripts and print PDFs;
- voice samples and auditions;
- quote requests;
- payments and payment webhooks;
- royalty ledgers;
- print order status;
- user accounts and messaging.

## Phase 1: manual matching

Do not build dashboards first.

Collect supply and demand:

- authors with audiobook projects;
- narrators with voice samples, languages, rates, and royalty preferences;
- authors needing small print batches;
- printers with spare capacity, equipment, paper, binding, location, and turnaround.

Match the first projects manually.

Success threshold:

- 10 audiobook projects matched and produced;
- 10 print jobs quoted;
- 3 reliable printers identified;
- repeatable quote fields confirmed.

## Audio rules

Narrator minimum:

- at least 5% of net profit;
- at least 5 years;
- floor is non-negotiable;
- higher tiers are allowed.

Suggested tiers:

- cash upfront plus 5% floor;
- reduced upfront plus 10%;
- royalty-only with higher upside, only by explicit agreement.

Author posture:

- author keeps book rights;
- no exclusivity by default;
- transparent reporting;
- rights and payment terms written plainly.

## Print rules

Author print request fields:

- title;
- interior PDF;
- cover PDF;
- trim size;
- page count;
- colour or black-and-white interior;
- paper preference;
- binding;
- quantity;
- city/country;
- deadline;
- delivery or pickup needs.

Printer profile fields:

- company;
- location;
- equipment;
- colour/BW capability;
- trim sizes;
- paper options;
- binding options;
- minimum viable run;
- idle windows;
- turnaround;
- pickup/delivery radius;
- proofing process.

## Webdock API shape

Initial entities:

- `authors`
- `narrators`
- `audio_projects`
- `printers`
- `print_requests`
- `quotes`
- `orders`
- `payments`
- `royalty_entries`

Initial API endpoints:

- `POST /audio/projects`
- `POST /audio/narrators`
- `POST /print/requests`
- `POST /print/printers`
- `POST /quotes`
- `POST /orders`
- `GET /orders/{id}`

Keep uploads separate from public GitHub Pages. Use Webdock storage first, then object storage if
audio/PDF size or bandwidth becomes expensive.

## Build order

1. Static intake pages on GitHub Pages.
2. Manual spreadsheet/CSV matching.
3. Webdock API for private submissions.
4. Admin dashboard for matching.
5. Payment webhook integration.
6. Royalty ledger.
7. Printer quote automation.
8. Public self-serve dashboards.
