import streamlit as st
import pandas as pd
import re
from analyzer import analyze_logs

st.set_page_config(
    page_title="AI Incident Root Cause Detector",
    layout="wide"
)

st.title("AI Incident Root Cause Detector")

st.write("Upload system logs and let AI analyze the incident root cause.")

uploaded_file = st.file_uploader(
    "Upload Log File", type=["txt", "log"]
)

if uploaded_file:

    logs = uploaded_file.read().decode("utf-8")

    # -----------------------
    # Log Preview
    # -----------------------

    st.subheader("Log Preview")
    st.text(logs[:1000])

    # -----------------------
    # Log Statistics
    # -----------------------

    error_count = logs.count("ERROR")
    warning_count = logs.count("WARNING")
    info_count = logs.count("INFO")

    data = pd.DataFrame({
        "Type": ["ERROR", "WARNING", "INFO"],
        "Count": [error_count, warning_count, info_count]
    })

    st.subheader("Log Statistics")
    st.bar_chart(data.set_index("Type"))

    # -----------------------
    # Incident Timeline
    # -----------------------

    timestamps = re.findall(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", logs)

    if timestamps:

        df = pd.DataFrame({"Timestamp": timestamps})
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        timeline = df["Timestamp"].value_counts().sort_index()

        st.subheader("Incident Timeline")
        st.line_chart(timeline)

    # -----------------------
    # AI Analysis Button
    # -----------------------

    if st.button("Run AI Root Cause Analysis"):

        with st.spinner("Analyzing logs with AI..."):

            result = analyze_logs(logs)

        if result:

            st.subheader("AI Incident Analysis")
            st.write(result)

            # Download report

            st.download_button(
                label="Download Incident Report",
                data=result,
                file_name="incident_report.txt",
                mime="text/plain"
            )

        else:
            st.error("AI analysis failed.")