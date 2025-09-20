import streamlit as st
import pandas as pd

# 🏷️ Dashboard Title
st.set_page_config(page_title="Shopsy Dashboard", layout="wide")
st.title("🛍️ Shopsy Dashboard")

# 📂 File Upload
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # 📊 Load Data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # 🧮 Sidebar Filters
    st.sidebar.header("🔍 Filters")
    date_filter = st.sidebar.date_input("Select Date Range", [])
    wm_filter = st.sidebar.multiselect("WM Name", options=df["WM Name"].unique())
    profile_filter = st.sidebar.multiselect("Profile ID", options=df["Profile ID"].unique())
    vendor_filter = st.sidebar.multiselect("Vendor ID", options=df["Vendor ID"].unique())

    # 🧼 Apply Filters
    filtered_df = df.copy()
    if date_filter:
        if len(date_filter) == 2:
            filtered_df = filtered_df[
                (pd.to_datetime(filtered_df["Date"]) >= pd.to_datetime(date_filter[0])) &
                (pd.to_datetime(filtered_df["Date"]) <= pd.to_datetime(date_filter[1]))
            ]
    if wm_filter:
        filtered_df = filtered_df[filtered_df["WM Name"].isin(wm_filter)]
    if profile_filter:
        filtered_df = filtered_df[filtered_df["Profile ID"].isin(profile_filter)]
    if vendor_filter:
        filtered_df = filtered_df[filtered_df["Vendor ID"].isin(vendor_filter)]

    # 📈 KPIs
    st.subheader("📊 Key Performance Indicators")

    total_assigned = filtered_df["Assigned"].sum()
    total_delivered = filtered_df["Delivered"].sum()
    conversion_rate = round((total_delivered / total_assigned) * 100, 2) if total_assigned else 0
    total_payout = filtered_df["Payout"].sum()
    shopsy_delivered = filtered_df["Shopsy Delivered"].sum()
    shopsy_payout = filtered_df["Shopsy Payout"].sum()
    shopsy_rate_card = round((shopsy_payout / shopsy_delivered), 2) if shopsy_delivered else 0

    # 📌 Display KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Assigned", total_assigned)
    col2.metric("Total Delivered", total_delivered)
    col3.metric("Conversion Rate (%)", conversion_rate)
    col4.metric("Total Payout", f"₹{total_payout:,.2f}")

    col5, col6, col7 = st.columns(3)
    col5.metric("Shopsy Delivered", shopsy_delivered)
    col6.metric("Shopsy Payout", f"₹{shopsy_payout:,.2f}")
    col7.metric("Shopsy Rate Card", f"₹{shopsy_rate_card:,.2f}")

    # 📋 Data Table
    st.subheader("📄 Filtered Data Table")
    st.dataframe(filtered_df)

else:
    st.info("Please upload a file to begin.")