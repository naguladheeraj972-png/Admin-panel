import streamlit as st
import pandas as pd
import requests
import time

# Backend URL (make sure FastAPI is running on this port)
API_URL = ' http://127.0.0.1:8000'

# ---------------- Setup ----------------
st.set_page_config(page_title="Attendance System", layout="wide")

# Sidebar navigation
st.sidebar.title("Admin Panel")
page = st.sidebar.radio("Navigate", ["Dashboard", "Employees", "Attendance", "Reports", "Settings"])

# ---------------- Dashboard ----------------
if page == "Dashboard":
    st.title("Dashboard")

    with st.spinner("Loading data..."):
        time.sleep(1)

    try:
        response = requests.get(f"{API_URL}/attendance")
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            st.success("Data loaded successfully")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Employees", len(df))
            col2.metric("Present Today", (df["status"] == "Present").sum())
            col3.metric("Absent Today", (df["status"] == "Absent").sum())

            st.write("Attendance Overview")
            st.table(df)
        else:
            st.error("Failed to fetch data from backend")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- Employees ----------------
elif page == "Employees":
    st.title("Employee Management")

    name = st.text_input("Employee Name")
    dept = st.text_input("Department")
    email = st.text_input("Email")

    if st.button("Register Employee"):
        payload = {"name": name, "department": dept, "email": email}
        try:
            response = requests.post(f"{API_URL}/employees", json=payload)
            if response.status_code == 200:
                st.success("Employee registered successfully")
            else:
                st.error("Failed to register employee")
        except Exception as e:
            st.error(f"Error: {e}")

    # Show employee list
    try:
        response = requests.get(f"{API_URL}/employees")
        if response.status_code == 200:
            df_emp = pd.DataFrame(response.json())
            st.write("Employee List")
            st.table(df_emp)
        else:
            st.error("Failed to fetch employee list")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- Attendance ----------------
elif page == "Attendance":
    st.title("Attendance Records")

    try:
        response = requests.get(f"{API_URL}/attendance")
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            filter_status = st.selectbox("Filter by Status", ["All", "Present", "Absent", "Late"])
            if filter_status != "All":
                df = df[df["status"] == filter_status]
            st.table(df)
        else:
            st.error("Failed to fetch attendance data")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- Reports ----------------
elif page == "Reports":
    st.title("Reports")
    try:
        response = requests.get(f"{API_URL}/attendance")
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            st.download_button("Download Attendance CSV", df.to_csv(index=False), "attendance.csv")
        else:
            st.error("Failed to fetch report data")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- Settings ----------------
elif page == "Settings":
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.success("Login successful")
        else:
            st.error("Invalid credentials")
