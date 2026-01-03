#Bank Management System
**A simple Bank Management System built using Python, Streamlit, and SQLite.
This project demonstrates basic banking operations such as account creation, login, deposits, withdrawals, transaction history, and admin management with secure PIN hashing.**

**👤User Features:**

Create a bank account

Secure login using hashed PIN (SHA-256)

Deposit money

Withdraw money (with balance check)

View transaction history

Clear transaction history

Reset account balance to zero

Delete account permanently

Logout securely

Admin Features

View all user accounts

View individual balances

View total bank balance


🔐 Security:

PINs are hashed using SHA-256
Raw PINs are never stored in the database
Session-based authentication using Streamlit session state


