import streamlit as st
import pandas as pd
import plotly.express as px

# 🏷️ Branding Header
st.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Flipkart_logo.svg/2560px-Flipkart_logo.svg.png' width='120'>
        <h1 style='color: #2874F0;'>Flipkart Shopsy Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# 📂 File Upload
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.write("📄 Preview of your data:")
    st.dataframe(df.head())

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

    # 📊 KPI Display
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

    # 📈 Charts Section
    st.subheader("📈 Performance Charts")

    if total_assigned and total_delivered:
        pie_data = pd.DataFrame({
            "Status": ["Delivered", "Remaining"],
            "Count": [total_delivered, total_assigned - total_delivered]
        })
        fig_pie = px.pie(pie_data, names="Status", values="Count", title="Delivery Breakdown")
        st.plotly_chart(fig_pie, use_container_width=True)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        agg_dict = {}
        for col in ["Assigned", "Delivered", "Payout", "Shopsy Delivered", "Shopsy Payout", "number of document delivered", "total U2S"]:
            if col in df.columns:
                agg_dict[col] = "sum"
        daily_kpi = df.groupby("Date").agg(agg_dict).reset_index()

        if "Payout" in daily_kpi.columns and "Shopsy Payout" in daily_kpi.columns and "number of document delivered" in daily_kpi.columns:
            daily_kpi["Non-Shopsy Payout"] = daily_kpi["Payout"] - daily_kpi["Shopsy Payout"] - (daily_kpi["number of document delivered"] * 9)
        if "Delivered" in daily_kpi.columns and "Shopsy Delivered" in daily_kpi.columns and "number of document delivered" in daily_kpi.columns and "total U2S" in daily_kpi.columns:
            daily_kpi["Non-U2S"] = daily_kpi["Delivered"] - daily_kpi["Shopsy Delivered"] - daily_kpi["number of document delivered"] - daily_kpi["total U2S"]

        if "Assigned" in daily_kpi.columns and "Delivered" in daily_kpi.columns:
            st.plotly_chart(px.line(daily_kpi, x="Date", y=["Assigned", "Delivered"], title="Assigned vs Delivered Over Time"), use_container_width=True)
        if "Payout" in daily_kpi.columns:
            st.plotly_chart(px.area(daily_kpi, x="Date", y="Payout", title="Total Payout Over Time"), use_container_width=True)
        if "Shopsy Delivered" in daily_kpi.columns and "number of document delivered" in daily_kpi.columns:
            st.plotly_chart(px.bar(daily_kpi, x="Date", y=["Shopsy Delivered", "number of document delivered"], barmode="group", title="Shopsy vs Document Deliveries"), use_container_width=True)
        if "Shopsy Payout" in daily_kpi.columns and "Non-Shopsy Payout" in daily_kpi.columns:
            st.plotly_chart(px.line(daily_kpi, x="Date", y=["Shopsy Payout", "Non-Shopsy Payout"], title="Shopsy vs Non-Shopsy Payout"), use_container_width=True)
        if "total U2S" in daily_kpi.columns and "Non-U2S" in daily_kpi.columns:
            st.plotly_chart(px.area(daily_kpi, x="Date", y=["total U2S", "Non-U2S"], title="U2S vs Non-U2S Deliveries"), use_container_width=True)

    # 👥 Footer Credits
    st.markdown("""
        <hr>
        <div style='text-align: center; font-size: 16px; color: #555;'>
            <strong>Manager:</strong> Nachhappa KB &nbsp; | &nbsp;
            <strong>Assistant Manager:</strong> Bansi Chavada &nbsp; | &nbsp;
            <strong>Dashboard Creator:</strong> Abhineet Kumar
        </div>
    """, unsafe_allow_html=True)

else:
    st.info("📁 Please upload a CSV or Excel file to begin.")
    