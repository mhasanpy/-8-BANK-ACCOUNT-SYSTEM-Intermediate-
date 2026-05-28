# -8-BANK-ACCOUNT-SYSTEM-Intermediate-
Concepts: OOP, inheritance, exceptions, datetime
# 🏦 Bank Account System (Intermediate)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![OOP](https://img.shields.io/badge/OOP-Inheritance-purple.svg)](https://docs.python.org/3/tutorial/classes.html)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A **professional banking system** that simulates real-world financial operations including account management, transactions, interest calculation, and exception handling. This is **Project 9** in my Python exercises series, demonstrating advanced OOP concepts.

## 🎯 Purpose

Simulate a complete banking system with different account types, transaction history, interest calculations, and robust error handling. Perfect for learning object-oriented programming, inheritance, and real-world financial logic.

## ✨ Features

### 🏧 Account Management
- **Create Accounts** – Savings, Checking, and Business accounts
- **Deposit Funds** – Add money with transaction recording
- **Withdraw Funds** – Remove money with balance validation
- **Transfer Money** – Send funds between accounts
- **View Balance** – Check current account balance
- **Account Statements** – View transaction history

### 🏦 Account Types with Inheritance

| Account Type | Features | Interest | Overdraft |
|--------------|----------|----------|-----------|
| **Savings Account** | High interest, limited withdrawals | 2.5% APY | ❌ No |
| **Checking Account** | Low interest, unlimited transactions | 0.5% APY | ✅ Yes ($500) |
| **Business Account** | High transaction limits, special fees | 1.5% APY | ✅ Yes ($2000) |

### 📊 Transaction System
- **Deposit Records** – Amount, date, time, type
- **Withdrawal Records** – Amount, date, time, type  
- **Transfer History** – Source, destination, amount
- **Interest Accrual** – Monthly interest calculation
- **Statement Generation** – Filter by date range

### 🔒 Security & Validation
- **Minimum Balance** – Prevent overdrawing (except overdraft accounts)
- **Daily Limits** – Maximum withdrawal per day
- **Transaction Limits** – Savings account withdrawal limits
- **Input Validation** – Amount, account number, PIN verification
- **Exception Handling** – Custom exceptions for banking errors

## 🧠 Advanced Concepts Covered

| Concept | Implementation |
|---------|----------------|
| **OOP & Inheritance** | `BankAccount` parent class with `SavingsAccount`, `CheckingAccount`, `BusinessAccount` children |
| **Method Overriding** | Custom `withdraw()` and `calculate_interest()` per account type |
| **Exception Handling** | `InsufficientFundsError`, `LimitExceededError`, `InvalidTransactionError` |
| **Datetime Module** | Timestamp every transaction for history |
| **Encapsulation** | Private attributes (`__balance`, `__pin`) with getters/setters |
| **Composition** | Transaction list within each account |
| **Polymorphism** | Same methods behave differently per account type |

## 🚀 How to Run

### Prerequisites
- Python 3.7 or higher
- No external libraries required!

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mhasanpy/-8-BANK-ACCOUNT-SYSTEM-Intermediate-.git
   cd -8-BANK-ACCOUNT-SYSTEM-Intermediate-
