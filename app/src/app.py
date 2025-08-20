import streamlit as st
import pandas as pd
from utils.csv_utils import read_csv, check_completeness, check_uniqueness, check_timeliness

st.set_page_config(layout="wide")  # Set layout to wide

DIMENSIONS = [
    "Completeness",
    "Uniqueness",
    "Accuracy",
    "Timeliness",
    "Consistency",
    "Validity"
]

def landing_page():
    st.title("Welcome to Data Quality Assessment App")
    st.markdown("""
    ## What is Data Quality?
    Data quality refers to the condition of a set of values of qualitative or quantitative variables. High data quality means the data is fit for its intended uses in operations, decision making, and planning.

    ## Data Quality Dimensions (Based on DMBOK)
    The Data Management Body of Knowledge (DMBOK) defines several key dimensions for assessing data quality:
    - **Completeness**: The degree to which all required data is present.
    - **Uniqueness**: The extent to which all records are unique and free from duplication.
    - **Accuracy**: The degree to which data correctly describes the real-world object or event.
    - **Timeliness**: The degree to which data is up-to-date and available when needed.
    - **Consistency**: The degree to which data is presented in the same format and matches across datasets.
    - **Validity**: The degree to which data conforms to the syntax (format, type, range) of its definition.

    ---
    Click "Data Quality" in the sidebar to begin uploading your CSV and assessing its data quality!
    """)
    if st.button("Go to Data Quality"):
        st.session_state.page = "data_quality"

def data_quality_page():
    st.title("Data Quality Assessment")
    st.subheader("Upload a CSV file to view its contents and assess data quality dimensions")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        data = read_csv(uploaded_file)
        st.write("Data from the CSV file:")
        st.dataframe(data)

        # Show shape info and top 5 rows
        st.info(f"Table shape: {data.shape[0]} rows × {data.shape[1]} columns")

        # Calculate summary for available dimensions
        completeness_df = check_completeness(data)
        uniqueness_df = check_uniqueness(data)
        # Timeliness summary: auto-select date columns and get mean timeliness
        date_columns = [
            col for col in data.columns
            if pd.api.types.is_datetime64_any_dtype(data[col]) or
               pd.to_datetime(data[col], errors='coerce').notna().sum() > 0
        ]
        if date_columns:
            timeliness_df = check_timeliness(data, date_columns)
            timeliness_mean = timeliness_df['timeliness_percent'].mean()
        else:
            timeliness_mean = 0

        summary = {
            "Completeness": completeness_df['completeness_percent'].mean(),
            "Uniqueness": uniqueness_df['uniqueness_percent'].mean(),
            "Accuracy": 0,
            "Timeliness": timeliness_mean,
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

        # Dropdown for column selection (allow multiple columns, add "Select All" option)
        if dimension in ["Completeness", "Uniqueness", "Timeliness"]:
            all_columns = list(data.columns)
            # For timeliness, auto-select columns with date dtype or date-like values
            if dimension == "Timeliness":
                date_columns = [
                    col for col in all_columns
                    if pd.api.types.is_datetime64_any_dtype(data[col]) or
                       pd.to_datetime(data[col], errors='coerce').notna().sum() > 0
                ]
                columns = st.multiselect(
                    f"Select column(s) to assess {dimension.lower()}",
                    ["[Select All]"] + date_columns,
                    default=date_columns if date_columns else []
                )
                if "[Select All]" in columns:
                    selected_columns = date_columns
                else:
                    selected_columns = columns
            else:
                columns = st.multiselect(
                    f"Select column(s) to assess {dimension.lower()}",
                    ["[Select All]"] + all_columns,
                    default=["[Select All]"]
                )
                if "[Select All]" in columns:
                    selected_columns = all_columns
                else:
                    selected_columns = columns

            if selected_columns:
                if dimension == "Completeness":
                    selected_df = completeness_df[completeness_df['column'].isin(selected_columns)]
                    st.subheader(f"Completeness for selected columns")
                    st.dataframe(selected_df)
                    st.bar_chart(selected_df.set_index('column')['completeness_percent'])
                elif dimension == "Uniqueness":
                    selected_df = uniqueness_df[uniqueness_df['column'].isin(selected_columns)]
                    st.subheader(f"Uniqueness for selected columns")
                    st.dataframe(selected_df)
                    st.bar_chart(selected_df.set_index('column')['uniqueness_percent'])
                elif dimension == "Timeliness":
                    st.info("Timeliness assesses how recent the dates are in selected columns (default threshold: 30 days).")
                    timeliness_df = check_timeliness(data, selected_columns)
                    st.subheader(f"Timeliness for selected columns")
                    st.dataframe(timeliness_df)
                    st.bar_chart(timeliness_df.set_index('column')['timeliness_percent'])
            else:
                st.info("Please select at least one column to assess.")
        else:
            st.info(f"Assessment for '{dimension}' is not implemented yet.")

def main():
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "data_quality":
        data_quality_page()

if __name__ == "__main__":
    main()