# Bank Management System

**A simple Bank Management System built using Python, Streamlit, and SQLite.
This project demonstrates basic banking operations such as account creation, login, deposits, withdrawals, transaction history, and admin management with secure PIN hashing.**

# 👤User Features:

Create a bank account

Secure login using hashed PIN (SHA-256)

Deposit money

Withdraw money (with balance check)

View transaction history

Clear transaction history

Reset account balance to zero

Delete account permanently

View total bank balance

# 🔐 Security:

PINs are hashed using SHA-256
Raw PINs are never stored in the database
Session-based authentication using Streamlit session state

# ScreenShots
### Account Creation Page:

You can create new account by using this page

![Alt text](https://github.com/satwikakancherla/Bank_Management_System/blob/main/create_acc.png)

### Login page:

If you have an existing account then only possible to login here. If you are trying to login without having an account it raises an error i.e Invalid credentials.

![Alt text](https://github.com/satwikakancherla/Bank_Management_System/blob/main/login_page.png)

### User DashBoard and Transaction History:

The user can perform Operations like withdraw and deposit.
It shows how much amount in their account.
whereas Transaction History shows your complete transaction from the scratch.

![Alt text](https://github.com/satwikakancherla/Bank_Management_System/blob/main/user_dashboard.png)

Here you can see the example transactions to get clarify.

![Alt text](https://github.com/satwikakancherla/Bank_Management_System/blob/main/Ex_Transaction.png)

### Account Management

Here you can clear your all trasactions, Reset account balance and delete your account

![Alt text](https://github.com/satwikakancherla/Bank_Management_System/blob/main/account_mgmt.png)

Finally you can logout your account by using Logout button.



