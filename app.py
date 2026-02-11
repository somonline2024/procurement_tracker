import streamlit as st
import pandas as pd

st.set_page_config(page_title="Request Tracker", layout="wide")

st.title("📊 Customer Request Tracker Dashboard")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip()

    # -----------------------------
    # Ensure Status column exists
    # -----------------------------
    if "Status" not in df.columns:
        st.error("Excel must contain a 'Status' column")
        st.stop()

    # -----------------------------
    # Status Counts
    # -----------------------------
    delivered = (df["Status"] == "Delivered").sum()
    inprogress = (df["Status"] == "Inprogress").sum()
    hold = (df["Status"] == "Hold").sum()
    pending = (df["Status"] == "Pending").sum()
    total = len(df)

    # -----------------------------
    # KPI CARDS
    # -----------------------------
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Delivered", delivered)
    col2.metric("Inprogress", inprogress)
    col3.metric("Hold", hold)
    col4.metric("Pending", pending)
    col5.metric("Total", total)

    st.divider()

    # -----------------------------
    # Filters
    # -----------------------------
    st.subheader("🔎 Filters")

    status_filter = st.multiselect(
        "Filter by Status",
        options=df["Status"].unique(),
        default=df["Status"].unique()
    )

    filtered_df = df[df["Status"].isin(status_filter)]

    # -----------------------------
    # Editable Table
    # -----------------------------
    st.subheader("📋 Request Table")

    edited_df = st.data_editor(
        filtered_df,
        use_container_width=True,
        num_rows="dynamic"
    )

    # -----------------------------
    # Download option
    # -----------------------------
    st.download_button(
        "⬇ Download Updated Excel",
        edited_df.to_excel(index=False, engine="openpyxl"),
        file_name="updated_tracker.xlsx"
    )

else:
    st.info("Please upload your Excel tracker file to continue.")
