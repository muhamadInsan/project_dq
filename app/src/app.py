import streamlit as st
import pandas as pd
from utils.csv_utils import read_csv, check_completeness, check_uniqueness

DIMENSIONS = [
    "Completeness",
    "Uniqueness",
    "Accuracy",
    "Timeliness",
    "Consistency",
    "Validity"
]

def main():
    st.title("Data Quality Assessment")
    st.subheader("Upload a CSV file to view its contents and assess data quality dimensions")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        data = read_csv(uploaded_file)
        st.write("Data from the CSV file:")
        st.dataframe(data)

        # Calculate summary for available dimensions
        completeness_df = check_completeness(data)
        uniqueness_df = check_uniqueness(data)

        # Calculate mean percentage for each dimension
        summary = {
            "Completeness": completeness_df['completeness_percent'].mean(),
            "Uniqueness": uniqueness_df['uniqueness_percent'].mean(),
            "Accuracy": 0,
            "Timeliness": 0,
            "Consistency": 0,
            "Validity": 0
        }
        summary_df = pd.DataFrame(list(summary.items()), columns=["Dimension", "Mean %"])

        st.subheader("Summary of Data Quality Dimensions (%)")
        st.bar_chart(data=summary_df.set_index("Dimension")["Mean %"])

        # Dropdown for data quality dimension
        dimension = st.selectbox(
            "Select Data Quality Dimension to Assess",
            DIMENSIONS
        )

        # Dropdown for column selection (allow multiple columns)
        if dimension in ["Completeness", "Uniqueness"]:
            columns = st.multiselect(
                f"Select column(s) to assess {dimension.lower()}",
                list(data.columns)
            )
            if columns:
                if dimension == "Completeness":
                    selected_df = completeness_df[completeness_df['column'].isin(columns)]
                    st.subheader(f"Completeness for selected columns")
                    st.dataframe(selected_df)
                    st.bar_chart(selected_df.set_index('column')['completeness_percent'])
                elif dimension == "Uniqueness":
                    selected_df = uniqueness_df[uniqueness_df['column'].isin(columns)]
                    st.subheader(f"Uniqueness for selected columns")
                    st.dataframe(selected_df)
                    st.bar_chart(selected_df.set_index('column')['uniqueness_percent'])
            else:
                st.info("Please select at least one column to assess.")
        else:
            st.info(f"Assessment for '{dimension}' is not implemented yet.")

if __name__ == "__main__":
    main()