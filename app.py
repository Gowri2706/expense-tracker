import streamlit as st
import sqlite3
import pandas as pd

# ---------------- DATABASE ----------------
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    category TEXT,
    amount REAL,
    date TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def add_data(type, category, amount, date):
    cursor.execute(
        "INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
        (type, category, amount, date)
    )
    conn.commit()

def get_data():
    return pd.read_sql("SELECT * FROM transactions", conn)

# ---------------- UI ----------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

# 🎨 CSS DESIGN
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.metric-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}
.metric-title {
    font-size: 18px;
    color: #cbd5e1;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Expense Tracker Dashboard")

# Sidebar
menu = st.sidebar.radio("Menu", ["Dashboard", "Add Transaction"])

# ---------------- ADD TRANSACTION ----------------
if menu == "Add Transaction":
    st.subheader("➕ Add Transaction")

    type = st.selectbox("Type", ["Income", "Expense"])
    category = st.text_input("Category")
    amount = st.number_input("Amount")
    date = st.date_input("Date")

    if st.button("Save"):
        add_data(type, category, amount, str(date))
        st.success("✅ Added Successfully!")

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    df = get_data()

    income = df[df['type']=="Income"]['amount'].sum()
    expense = df[df['type']=="Expense"]['amount'].sum()
    balance = income - expense

    # 🔥 METRIC CARDS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">💵 Income</div>
            <div class="metric-value">{income:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">💸 Expenses</div>
            <div class="metric-value">{expense:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">💰 Balance</div>
            <div class="metric-value">{balance:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col4, col5 = st.columns(2)

    # Income Table
    with col4:
        st.subheader("📥 Income Details")
        st.dataframe(df[df['type']=="Income"], use_container_width=True)

    # Expense Table
    with col5:
        st.subheader("📤 Expense Details")
        st.dataframe(df[df['type']=="Expense"], use_container_width=True)

    st.divider()

    # 📊 Chart
    st.subheader("📊 Expense by Category")

    exp_df = df[df['type']=="Expense"]

    if not exp_df.empty:
        chart = exp_df.groupby("category")["amount"].sum()
        st.bar_chart(chart)
    else:
        st.info("No expense data available")