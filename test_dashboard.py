
import streamlit as st
import pandas as pd

st.title("✅ Streamlit Dashboard Test")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
    st.write("📄 Preview of your data:")
    st.dataframe(df.head())
else:
    st.info("📁 Please upload a CSV file to begin.")