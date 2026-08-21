# ModernBank - Bank Management System

A Python Flask Bank Management System created as an Object-Oriented Programming and SOLID principles demonstration project.

## Features

- Create customers and bank accounts
- Savings, Current and Business accounts
- Deposit money
- Withdraw money
- Transfer funds
- Check balances
- Transaction history
- Notifications
- Responsive web interface
- OOP four pillars
- SOLID principles

## OOP Demonstration

### Encapsulation
`BankAccount` protects its balance using `_balance` and exposes controlled operations such as `deposit()` and `withdraw()`.

### Abstraction
`BankAccount` is an abstract base class with abstract methods:
- `account_type`
- `calculate_interest`

### Inheritance
These classes inherit from `BankAccount`:
- `SavingsAccount`
- `CurrentAccount`
- `BusinessAccount`

### Polymorphism
Each account type implements `calculate_interest()` differently while the application works with the common `BankAccount` abstraction.

## SOLID Demonstration

### Single Responsibility Principle
Responsibilities are separated into:
- Models
- Bank service
- Notification service
- Repository

### Open/Closed Principle
A new account type can be added by creating a new subclass without rewriting the existing account classes.

### Liskov Substitution Principle
All account subclasses can be used through the `BankAccount` abstraction.

### Interface Segregation Principle
The repository abstraction exposes focused persistence operations. The design can be extended with more focused interfaces as the application grows.

### Dependency Inversion Principle
`BankService` depends on the abstract `AccountRepository`, not directly on a database implementation.

## Run Locally

Python 3.10+ is recommended.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000

## Important limitation

This demonstration currently uses an in-memory repository. Data is lost when the application restarts.

For a production version, replace `InMemoryAccountRepository` with a persistent database repository such as PostgreSQL.

## Netlify

Netlify is best used for the web frontend/static assets. A traditional always-running Flask server should be deployed on a Python-capable backend host.

For a Netlify-hosted production architecture:

```text
Netlify frontend
       |
       v
Python API
       |
       v
PostgreSQL
```

Do not put real banking credentials or sensitive customer data into this educational project.
