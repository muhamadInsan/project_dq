import streamlit as st
import pandas as pd
from utils.csv_utils import read_csv, check_completeness

DIMENSIONS = [
    "Completeness",
    "Uniqueness",
    "Accuracy",
    "Timeliness",
    "Consistency",
    "Validity"
]

def main():
    st.title("CSV Upload & Data Quality Assessment")
    st.subheader("Upload a CSV file to view its contents and assess data quality dimensions")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        data = read_csv(uploaded_file)
        st.write("Data from the CSV file:")
        st.dataframe(data)

        # Dropdown for data quality dimension
        dimension = st.selectbox(
            "Select Data Quality Dimension to Assess",
            DIMENSIONS
        )

        if dimension == "Completeness":
            completeness_df = check_completeness(data)
            st.subheader("Data Completeness by Column (%)")
            st.dataframe(completeness_df)
            st.bar_chart(
                data=completeness_df.set_index('column')['completeness_percent']
            )
        else:
            st.info(f"Assessment for '{dimension}' is not implemented yet.")

if __name__ == "__main__":
    main()