import streamlit as st
import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

FILENAME = "library_users.json"

# Load data
def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return {}

# Save data
def save_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=4)

# Fake SMS sender (No Twilio needed)
def send_message(contact, message):
    st.info(f"📩 Message to {contact}: {message}")

# Calculate due months
def calculate_due(admission_date, monthly_fee=1200):
    admission_date = datetime.strptime(admission_date, "%Y-%m-%d")
    today = datetime.today()
    months = relativedelta(today, admission_date).months + (relativedelta(today, admission_date).years * 12)
    return months * monthly_fee

# Streamlit UI
st.title("📚 Readerspace Library System")

data = load_data()

menu = st.sidebar.selectbox("Menu", ["New User", "Old User", "All Records"])

# ------------------ New User ------------------
if menu == "New User":
    st.subheader("➕ Register New User")
    name = st.text_input("Full Name")
    father_name = st.text_input("Father's Name")
    address = st.text_area("Address")
    email = st.text_input("Email")
    contact = st.text_input("Contact Number")
    seatno = st.text_input("Seat Number")
    admission_date = st.date_input("Admission Date", datetime.today())
    library_code = "L" + datetime.now().strftime("%Y%m%d%H%M%S")

    if st.button("Create User"):
        data[library_code] = {
            "name": name,
            "father_name": father_name,
            "address": address,
            "email": email,
            "contact": contact,
            "seatno": seatno,
            "admission_date": str(admission_date),
            "monthly_fee": 1200
        }
        save_data(data)
        st.success(f"✅ User created with Library Code: {library_code}")
        send_message(contact, f"Welcome {name}! Your Library ID is {library_code}.")

# ------------------ Old User ------------------
elif menu == "Old User":
    st.subheader("🔑 Existing User Login")
    code = st.text_input("Enter Library Code")
    if st.button("Check User"):
        if code in data:
            user = data[code]
            st.write("### User Details")
            st.json(user)

            due = calculate_due(user["admission_date"], user["monthly_fee"])
            st.warning(f"💰 Total Due: ₹{due}")

            if due > 0:
                send_message(user["contact"], f"Dear {user['name']}, please pay ₹{due} (Library fee pending).")
        else:
            st.error("❌ User not found")

# ------------------ All Records ------------------
elif menu == "All Records":
    st.subheader("📑 All Library Records")
    st.json(data)
