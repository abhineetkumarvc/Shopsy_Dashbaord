import streamlit as st
import pandas as pd
import plotly.express as px

# 🛠️ Page setup
st.set_page_config(page_title="Flipkart Shopsy Dashboard", page_icon="📦", layout="wide")

# 🎨 Custom CSS
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        .block-container { padding-top: 2rem; }
        .metric-label { color: #2874F0 !important; font-weight: bold; }
        .stRadio > div { flex-direction: row; }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 🔐 Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🔐 Valid users
valid_users = {
    "abhineetkumar.vc@flipkart.com": "flipkart@0505",
    "bansi.chavada@flipkart.com": "flipkart@8866",
    "navin.nachappa@flipkart.com": "flipkart@9663",
    "ganeshv1.vc@flipkart.com": "flipkart@7019",
    "kambalim.vc@flipkart.com": "flipkart@9591",
    "abdullaha.vc@flipkart.com": "flipkart@8587",
    "aravind.b@flipkart.com": "flipkart@8151",
    "prasanna.br@flipkart.com": "flipkart@9845"
}

# 🔐 Login screen
def login_screen():
    st.title("🔐 Flipkart Dashboard Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if email in valid_users and password == valid_users[email]:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

# 🔓 Logout
def logout():
    st.session_state.logged_in = False
    st.rerun()

# 🧭 Navigation
if not st.session_state.logged_in:
    login_screen()
    st.stop()

st.sidebar.button("Logout", on_click=logout)
st.sidebar.header("🔍 Filters")

# 📂 File Upload
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 🔍 Sidebar Filters
    date_range = st.sidebar.date_input("Date Range", [df["Date"].min(), df["Date"].max()])
    if len(date_range) == 2:
        df = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]

    for col in ["WM Name", "Profile ID", "Vendor ID"]:
        if col in df.columns:
            selected = st.sidebar.multiselect(f"{col}", df[col].unique())
            if selected:
                df = df[df[col].isin(selected)]

    # 🧮 KPI Calculations
    def safe_sum(col): return df[col].sum() if col in df.columns else 0

    total_assigned = safe_sum("Assigned")
    total_delivered = safe_sum("Delivered")
    conversion_rate = round((total_delivered / total_assigned) * 100, 2) if total_assigned else 0
    total_payout = safe_sum("Payout")
    shopsy_delivered = safe_sum("Shopsy Delivered")
    shopsy_payout = safe_sum("Shopsy Payout")
    shopsy_rate_card = round((shopsy_payout / shopsy_delivered), 2) if shopsy_delivered else 0
    document_delivered = safe_sum("number of document delivered")
    document_payout = round(document_delivered * 9, 2)
    document_rate_card = round((document_payout / document_delivered), 2) if document_delivered else 0
    non_shopsy_delivered = total_delivered - shopsy_delivered - document_delivered
    non_shopsy_payout = total_payout - shopsy_payout - document_payout
    non_shopsy_rate_card = round((non_shopsy_payout / non_shopsy_delivered), 2) if non_shopsy_delivered else 0
    total_U2S = safe_sum("total U2S")
    total_non_U2S = non_shopsy_delivered - total_U2S

    # 📄 Page Navigation
    section = st.radio("📂 Select Section", ["KPIs", "Charts", "Table", "Summary"])

    # 📊 KPIs Page
    if section == "KPIs":
        st.subheader("📊 Key Performance Indicators")
        kpi_cols = st.columns(4)
        kpi_cols[0].metric("Total Assigned", total_assigned)
        kpi_cols[1].metric("Total Delivered", total_delivered)
        kpi_cols[2].metric("Conversion Rate (%)", conversion_rate)
        kpi_cols[3].metric("Total Payout", f"₹{total_payout:,.2f}")

        kpi_cols2 = st.columns(3)
        kpi_cols2[0].metric("Shopsy Delivered", shopsy_delivered)
        kpi_cols2[1].metric("Shopsy Payout", f"₹{shopsy_payout:,.2f}")
        kpi_cols2[2].metric("Shopsy Rate Card", f"₹{shopsy_rate_card:,.2f}")

        kpi_cols3 = st.columns(3)
        kpi_cols3[0].metric("Document Delivered", document_delivered)
        kpi_cols3[1].metric("Document Payout", f"₹{document_payout:,.2f}")
        kpi_cols3[2].metric("Document Rate Card", f"₹{document_rate_card:,.2f}")

        kpi_cols4 = st.columns(3)
        kpi_cols4[0].metric("Non-Shopsy Delivered", non_shopsy_delivered)
        kpi_cols4[1].metric("Non-Shopsy Payout", f"₹{non_shopsy_payout:,.2f}")
        kpi_cols4[2].metric("Non-Shopsy Rate Card", f"₹{non_shopsy_rate_card:,.2f}")

        kpi_cols5 = st.columns(2)
        kpi_cols5[0].metric("Total U2S", total_U2S)
        kpi_cols5[1].metric("Total Non-U2S", total_non_U2S)

    # 📈 Charts Page
    elif section == "Charts":
        st.subheader("📈 Performance Charts")
        pie_data = pd.DataFrame({
            "Status": ["Delivered", "Remaining"],
            "Count": [total_delivered, total_assigned - total_delivered]
        })
        st.plotly_chart(px.pie(pie_data, names="Status", values="Count", title="Delivery Breakdown", color_discrete_sequence=["#00cc96", "#636efa"]), use_container_width=True)

        daily_kpi = df.groupby("Date").agg({
            "Assigned": "sum", "Delivered": "sum", "Payout": "sum",
            "Shopsy Delivered": "sum", "Shopsy Payout": "sum",
            "number of document delivered": "sum", "total U2S": "sum"
        }).reset_index()

        daily_kpi["Non-Shopsy Payout"] = daily_kpi["Payout"] - daily_kpi["Shopsy Payout"] - (daily_kpi["number of document delivered"] * 9)
        daily_kpi["Non-U2S"] = daily_kpi["Delivered"] - daily_kpi["Shopsy Delivered"] - daily_kpi["number of document delivered"] - daily_kpi["total U2S"]

        st.plotly_chart(px.line(daily_kpi, x="Date", y=["Assigned", "Delivered"], title="Assigned vs Delivered", color_discrete_map={"Assigned": "#EF553B", "Delivered": "#00cc96"}), use_container_width=True)
        st.plotly_chart(px.area(daily_kpi, x="Date", y="Payout", title="Total Payout Over Time", color_discrete_sequence=["#636efa"]), use_container_width=True)
        st.plotly_chart(px.bar(daily_kpi, x="Date", y=["Shopsy Delivered", "number of document delivered"], barmode="group", title="Shopsy vs Document Deliveries", color_discrete_sequence=["#00cc96", "#EF553B"]), use_container_width=True)
        st.plotly_chart(px.line(daily_kpi, x="Date", y=["Shopsy Payout", "Non-Shopsy Payout"], title="Shopsy vs Non-Shopsy Payout", color_discrete_sequence=["#00cc96", "#EF553B"]), use_container_width=True)
        st.plotly_chart(px.area(daily_kpi, x="Date", y=["total U2S", "Non-U2S"], title="U2S vs Non-U2S Deliveries", color_discrete_sequence=["#00cc96", "#EF553B"]), use_container_width=True)

    # 📄 Table Page
    elif section == "Table":
        st.subheader("📄 Filtered Data Table")
        st.dataframe(df)

    elif section == "Summary":
        st.subheader("📋 Summary")
    st.markdown(f"""
        - **Total Assigned:** {total_assigned}  
        - **Total Delivered:** {total_delivered}  
        - **Conversion Rate:** {conversion_rate}%  
        - **Total Payout:** ₹{total_payout:,.2f}  
        - **Shopsy Delivered:** {shopsy_delivered}  
        - **Document Delivered:** {document_delivered}  
        - **Non-Shopsy Delivered:** {non_shopsy_delivered}  
        - **Total U2S:** {total_U2S}  
        - **Total Non-U2S:** {total_non_U2S}
    """)



# 👥 Footer Credits
st.markdown("""
    <hr style='border: 1px solid #ccc;'>
    <div style='text-align: center; font-size: 16px; color: #555; padding-top: 10px;'>
        <strong>Manager:</strong> Naveen Nachhapa KB &nbsp; | &nbsp;
        <strong>Assistant Manager:</strong> Bansi Chavada &nbsp; | &nbsp;
        <strong>Data Analysis & Creator:</strong> Abhineet Kumar
    </div>
""", unsafe_allow_html=True)

