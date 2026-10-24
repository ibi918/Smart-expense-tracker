Website Link: https://expense-tracker-by-ibraheem.streamlit.app/
<<<<<<< HEAD
# Smart Expense Tracker & Financial Analytics Dashboard

A beginner-friendly Python portfolio project for tracking income and expenses, storing transactions in SQLite, and exploring financial trends in an interactive Streamlit dashboard.

## Features

- Add income and expense transactions
- Store data locally in SQLite
- Show total income, total expenses, and net balance
- Visualize expenses by category
- Compare income and expenses by month
- Filter transaction history and delete transactions
- Validate transaction amounts and categories
- Run automated tests with pytest
- Run tests automatically on GitHub Actions

## Tech stack

- Python
- Streamlit
- SQLAlchemy
- SQLite
- Pandas
- Plotly
- pytest
- GitHub Actions

## Requirements

- Python 3.10 or newer
- Git (recommended)
- VS Code (recommended)

## Setup on Windows

Open this repository folder in VS Code. In **Terminal → New Terminal**, run:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run this in the same terminal, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the app

```powershell
python -m streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser. To stop the app, focus the terminal and press `Ctrl+C`.

> Use the terminal command above instead of F5/Run and Debug. This is a Streamlit app, not a plain Python script launched directly by the debugger.

## Run tests

```powershell
python -m pytest -q
```

## Project structure

```text
smart-expense-tracker/
├── .github/
│   └── workflows/
│       └── tests.yml
├── src/
│   ├── __init__.py
│   ├── analytics.py
│   ├── database.py
│   ├── models.py
│   └── transactions.py
├── tests/
│   ├── test_analytics.py
│   └── test_transactions.py
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Database and privacy

The app creates `expense_tracker.db` in the project folder on first launch. The database is excluded from Git by `.gitignore`; your personal transactions should not be committed to GitHub.

## Publish to GitHub

If you cloned this repository from GitHub, after adding your project files run:

```powershell
git status
git add .
git commit -m "Build smart expense tracker dashboard"
git push
```

If Git asks you to configure your identity, use the name and email associated with your GitHub commits:

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Possible future improvements

- Edit transactions from the dashboard
- Monthly budgets and budget alerts
- CSV export/import
- Date-range filters
- Login and multiple user support
- Deployment to Streamlit Community Cloud

## Disclaimer

This is an educational portfolio project, not professional financial advice.
=======
# Smart-expense-tracker
A Python-based expense tracker with financial analytics, interactive dashboards, and SQLite storage.
>>>>>>> 90ca5a15ed11ca1374e05e9c92bc3566a2aafd1f
