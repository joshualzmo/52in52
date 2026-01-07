# Week 1 – Personal Finance CLI Ledger (Python)

This is Week 1 of my 52in52 challenge, where I build one project per week to steadily improve my software development skills.

## What I Built
- A CLI menu interface that continuously runs until the user exits
- An “Add transaction” flow that validates user input before saving anything
- Transactions stored as dictionaries inside a list (simple and easy to expand)
- Weekly and monthly summary reports:
  - total income, total expenses, and net balance
  - category totals with top categories highlighted
- Save/load persistence using a JSON file so data is not lost between runs

## What I Learned
- How to structure a CLI program so each feature is its own function
- Why input validation matters (and how to re-prompt safely without crashing)
- How to work with dates for filtering transactions by time period
- How saving/loading changes the program from “temporary” to “usable”

## Next Improvements
- Add a cleaner “Save/Load” submenu (more user-friendly options)
- Improve date validation to reject impossible dates (e.g., Feb 30)
- Better formatting when listing transactions (table-like output)
- Optional export to CSV for spreadsheet analysis
