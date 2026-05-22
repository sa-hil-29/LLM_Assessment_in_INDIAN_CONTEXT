## Plan: Sync Column Selection with Leaderboard Table

TL;DR: Update the dashboard template so clicking a chip both toggles its selected state and shows/hides the matching leaderboard column. This is a client-side fix in `assessment/templates/assessment/home.html` plus a small CSS helper.

**Steps**
1. Update `assessment/templates/assessment/home.html`.
   - Add `data-column` attributes to each selectable chip.
   - Ensure the leaderboard table header contains matching `data-column` attributes for each column, including `Type` and `Architecture`.
   - Add a dynamic placeholder row `td` that can update its `colspan` based on visible columns.
   - Add a script that:
     - toggles `.checked` on a chip click,
     - finds all table cells with the matching `data-column`, and toggles a hidden state,
     - recalculates the placeholder row `colspan` based on visible columns.
2. Update `assessment/static/assessment/styles.css`.
   - Add a `.hidden-column` rule for `th` and `td` so hidden table cells are removed from layout cleanly.
3. Initialize column state on DOMContentLoaded so the table reflects whichever chips are initially checked.
4. Verify by toggling chips and observing header column show/hide behavior.

**Relevant files**
- `assessment/templates/assessment/home.html` — main UI, chip selection, leaderboard table, and inline script.
- `assessment/static/assessment/styles.css` — CSS helper for hiding columns.

**Verification**
1. Open the page and confirm clicking a chip changes its checked styling.
2. Confirm the corresponding table header column hides/shows immediately.
3. Confirm the leaderboard placeholder row `colspan` adjusts to visible columns so the row remains centered and formatted.

**Decisions**
- This is a frontend-only change; no Django backend update is needed.
- The leaderboard table will now include all selectable columns present in the chip list so selection mapping is one-to-one.
