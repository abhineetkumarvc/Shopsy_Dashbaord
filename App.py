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

    # 🔍 Show column names for debugging
    st.write("🧾 Columns in your file:", df.columns.tolist())

    # 🧮 Sidebar Filters
    st.sidebar.header("🔍 Filters")

    # Date filter (only if 'Date' column exists)
    if "Date" in df.columns:
        date_filter = st.sidebar.date_input("Select Date Range", [])
    else:
        st.sidebar.warning("Column 'Date' not found.")
        date_filter = []

    # WM Name filter
    if "WM Name" in df.columns:
        wm_filter = st.sidebar.multiselect("WM Name", options=df["WM Name"].unique())
    else:
        st.sidebar.warning("Column 'WM Name' not found.")
        wm_filter = []

    # Profile ID filter
    if "Profile ID" in df.columns:
        profile_filter = st.sidebar.multiselect("Profile ID", options=df["Profile ID"].unique())
    else:
        st.sidebar.warning("Column 'Profile ID' not found.")
        profile_filter = []

    # Vendor ID filter
    if "Vendor ID" in df.columns:
        vendor_filter = st.sidebar.multiselect("Vendor ID", options=df["Vendor ID"].unique())
    else:
        st.sidebar.warning("Column 'Vendor ID' not found.")
        vendor_filter = []

    # 🧼 Apply Filters
    filtered_df = df.copy()

    if "Date" in df.columns and date_filter and len(date_filter) == 2:
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df["Date"]) >= pd.to_datetime(date_filter[0])) &
            (pd.to_datetime(filtered_df["Date"]) <= pd.to_datetime(date_filter[1]))
        ]
    if "WM Name" in df.columns and wm_filter:
        filtered_df = filtered_df[filtered_df["WM Name"].isin(wm_filter)]
    if "Profile ID" in df.columns and profile_filter:
        filtered_df = filtered_df[filtered_df["Profile ID"].isin(profile_filter)]
    if "Vendor ID" in df.columns and vendor_filter:
        filtered_df = filtered_df[filtered_df["Vendor ID"].isin(vendor_filter)]

    # 📈 KPIs
    st.subheader("📊 Key Performance Indicators")

    def safe_sum(col):
        return filtered_df[col].sum() if col in filtered_df.columns else 0

    total_assigned = safe_sum("Assigned")
    total_delivered = safe_sum("Delivered")
    conversion_rate = round((total_delivered / total_assigned) * 100, 2) if total_assigned else 0
    total_payout = safe_sum("Payout")
    shopsy_delivered = safe_sum("Shopsy Delivered")
    shopsy_payout = safe_sum("Shopsy Payout")
    shopsy_rate_card = round((shopsy_payout / shopsy_delivered), 2) if shopsy_delivered else 0
    document_delivered = safe_sum("number of document delivered") 
    document_Payout = round((document_delivered*9),2)
    documennt_rate_card = round((document_Payout / document_delivered),2) if document_delivered else 0
    non_shopsy_delivered = total_delivered - shopsy_delivered - document_delivered
    non_shopsy_payout = total_payout - shopsy_payout - document_Payout
    non_shopsy_rate_card = round((non_shopsy_payout /non_shopsy_delivered),2) if non_shopsy_delivered else 0
    total_U2S = safe_sum("total U2S")
    total_non_U2S = non_shopsy_delivered - total_U2S
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
