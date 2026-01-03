import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

# ---------- DATABASE ----------
conn = sqlite3.connect("bank.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    acc_no TEXT PRIMARY KEY,
    name TEXT,
    pin TEXT,
    balance REAL,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    acc_no TEXT,
    type TEXT,
    amount REAL,
    timestamp TEXT
)
""")
conn.commit()

# ---------- SECURITY ----------
def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

# ---------- FUNCTIONS ----------
def create_account(acc, name, pin, role="user"):
    try:
        cursor.execute(
            "INSERT INTO accounts VALUES (?, ?, ?, ?, ?)",
            (acc, name, hash_pin(pin), 0, role)
        )
        conn.commit()
        return True
    except:
        return False

def authenticate(acc, pin):
    cursor.execute(
        "SELECT * FROM accounts WHERE acc_no=? AND pin=?",
        (acc, hash_pin(pin))
    )
    return cursor.fetchone()

def get_balance(acc):
    cursor.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc,))
    return cursor.fetchone()[0]

def update_balance(acc, amount, ttype):
    cursor.execute(
        "UPDATE accounts SET balance = balance + ? WHERE acc_no=?",
        (amount, acc)
    )
    cursor.execute(
        "INSERT INTO transactions VALUES (?, ?, ?, ?)",
        (acc, ttype, abs(amount), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()

# ---------- NEW FUNCTIONS ----------
def clear_transactions(acc):
    cursor.execute("DELETE FROM transactions WHERE acc_no=?", (acc,))
    conn.commit()

def reset_account(acc):
    cursor.execute("UPDATE accounts SET balance=0 WHERE acc_no=?", (acc,))
    cursor.execute("DELETE FROM transactions WHERE acc_no=?", (acc,))
    conn.commit()

def delete_account(acc):
    cursor.execute("DELETE FROM transactions WHERE acc_no=?", (acc,))
    cursor.execute("DELETE FROM accounts WHERE acc_no=?", (acc,))
    conn.commit()

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.acc = None
    st.session_state.role = None

# ---------- UI ----------
st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Create Account"]
)

# ---------- CREATE ACCOUNT ----------
if menu == "Create Account":
    st.subheader("Create Account")

    acc = st.text_input("Account Number")
    name = st.text_input("Name")
    pin = st.text_input("PIN", type="password")

    if st.button("Create"):
        if create_account(acc, name, pin):
            st.success("Account created successfully!")
        else:
            st.error("Account already exists!")

# ---------- LOGIN ----------
if menu == "Login":
    st.subheader("Login")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Login"):
        user = authenticate(acc, pin)
        if user:
            st.session_state.logged_in = True
            st.session_state.acc = acc
            st.session_state.role = user[4]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------- USER DASHBOARD ----------
if st.session_state.logged_in and st.session_state.role == "user":
    st.subheader("👤 User Dashboard")

    balance = get_balance(st.session_state.acc)
    st.info(f"💰 Balance: ₹{balance}")

    amount = st.number_input("Amount", min_value=1.0)

    col1, col2 = st.columns(2)

    if col1.button("Deposit"):
        update_balance(st.session_state.acc, amount, "Deposit")
        st.success("Deposited successfully")
        st.rerun()

    if col2.button("Withdraw"):
        if amount > balance:
            st.error("Insufficient balance")
        else:
            update_balance(st.session_state.acc, -amount, "Withdraw")
            st.success("Withdrawn successfully")
            st.rerun()

    st.subheader("📜 Transaction History")
    cursor.execute(
        "SELECT type, amount, timestamp FROM transactions WHERE acc_no=?",
        (st.session_state.acc,)
    )
    st.table(cursor.fetchall())

    st.divider()
    st.subheader("⚠️ Account Management")

    if st.button("🧹 Clear Transaction History"):
        clear_transactions(st.session_state.acc)
        st.success("Transaction history cleared")
        st.rerun()

    if st.button("🔄 Reset Account (Balance = 0)"):
        reset_account(st.session_state.acc)
        st.success("Account reset successfully")
        st.rerun()

    if st.button("❌ Delete Account Completely"):
        delete_account(st.session_state.acc)
        st.session_state.logged_in = False
        st.session_state.acc = None
        st.success("Account deleted successfully")
        st.rerun()

# ---------- ADMIN DASHBOARD ----------
if st.session_state.logged_in and st.session_state.role == "admin":
    st.subheader("👨‍💼 Admin Dashboard")

    cursor.execute("SELECT acc_no, name, balance FROM accounts")
    st.table(cursor.fetchall())

    cursor.execute("SELECT SUM(balance) FROM accounts")
    total = cursor.fetchone()[0]
    st.success(f"🏦 Total Bank Balance: ₹{total}")

# ---------- LOGOUT ----------
if st.session_state.logged_in:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.acc = None
        st.rerun()