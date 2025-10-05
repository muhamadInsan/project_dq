import streamlit as st
import pandas as pd
from utils.csv_utils import read_csv, check_completeness, check_uniqueness, check_timeliness, check_validity

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
        st.info(f"Table shape: {data.shape[0]} rows × {data.shape[1]} columns")

        tabs = st.tabs(DIMENSIONS)

        # Completeness Tab
        with tabs[0]:
            st.header("Completeness")
            completeness_df = check_completeness(data)
            columns = st.multiselect(
                "Select column(s) to assess completeness",
                ["[Select All]"] + list(data.columns),
                default=["[Select All]"]
            )
            selected_columns = list(data.columns) if "[Select All]" in columns else columns
            if selected_columns:
                selected_df = completeness_df[completeness_df['column'].isin(selected_columns)]
                st.dataframe(selected_df)
                st.bar_chart(selected_df.set_index('column')['completeness_percent'])
                summary_data = []
                total_rows = len(data)
                for idx, row in selected_df.iterrows():
                    col = row['column']
                    percent = row['completeness_percent']
                    failed_percent = 100 - percent
                    passed_rows = int(total_rows * percent / 100)
                    failed_rows = total_rows - passed_rows
                    summary_data.append({
                        "Column": col,
                        "Passed (%)": f"{percent:.2f}",
                        "Failed (%)": f"{failed_percent:.2f}",
                        "Rows Passed": passed_rows,
                        "Rows Failed": failed_rows
                    })
                st.markdown("##### Completeness Detail: Data Presence Breakdown")
                st.table(pd.DataFrame(summary_data))
            else:
                st.info("Please select at least one column to assess.")

        # Uniqueness Tab
        with tabs[1]:
            st.header("Uniqueness")
            uniqueness_df = check_uniqueness(data)
            columns = st.multiselect(
                "Select column(s) to assess uniqueness",
                ["[Select All]"] + list(data.columns),
                default=["[Select All]"]
            )
            selected_columns = list(data.columns) if "[Select All]" in columns else columns
            if selected_columns:
                selected_df = uniqueness_df[uniqueness_df['column'].isin(selected_columns)]
                st.dataframe(selected_df)
                st.bar_chart(selected_df.set_index('column')['uniqueness_percent'])
                summary_data = []
                total_rows = len(data)
                for idx, row in selected_df.iterrows():
                    col = row['column']
                    percent = row['uniqueness_percent']
                    failed_percent = 100 - percent
                    passed_rows = int(total_rows * percent / 100)
                    failed_rows = total_rows - passed_rows
                    summary_data.append({
                        "Column": col,
                        "Passed (%)": f"{percent:.2f}",
                        "Failed (%)": f"{failed_percent:.2f}",
                        "Rows Passed": passed_rows,
                        "Rows Failed": failed_rows
                    })
                st.markdown("##### Uniqueness Detail: Duplicate Data Breakdown")
                st.table(pd.DataFrame(summary_data))
            else:
                st.info("Please select at least one column to assess.")

        # Accuracy Tab
        with tabs[2]:
            st.header("Accuracy")
            st.info("Accuracy assessment is not implemented yet.")

        # Timeliness Tab
        with tabs[3]:
            st.header("Timeliness")
            st.info("Timeliness assessment is not implemented yet.")

        # Consistency Tab
        with tabs[4]:
            st.header("Consistency")
            st.info("Consistency assessment is not implemented yet.")

        # Validity Tab
        with tabs[5]:
            st.header("Validity")
            columns = st.multiselect(
                "Select column(s) to assess validity",
                ["[Select All]"] + list(data.columns),
                default=["[Select All]"]
            )
            selected_columns = list(data.columns) if "[Select All]" in columns else columns
            validity_column = st.selectbox("Select column to check validity", selected_columns)
            validity_condition = st.selectbox(
                "Select validity condition",
                ["equal", "min", "max", "in", "between", "regex"]
            )
            if validity_condition == "between":
                val1 = st.text_input("Minimum value")
                val2 = st.text_input("Maximum value")
                try:
                    val1 = float(val1)
                    val2 = float(val2)
                    validity_value = [val1, val2]
                except:
                    validity_value = [val1, val2]
            elif validity_condition == "in":
                validity_value = st.text_input("List of valid values (comma separated)").split(",")
                validity_value = [v.strip() for v in validity_value]
            elif validity_condition == "regex":
                validity_value = st.text_input(
                    "Regex pattern (e.g. ^[A-Za-z0-9]+$ for alphanumeric, ^\\d+$ for digits, ^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$ for email)"
                )
            else:
                validity_value = st.text_input("Value for validity check")
                try:
                    validity_value = float(validity_value)
                except:
                    pass
            if st.button("Check Validity", key="validity_btn"):
                percent = check_validity(data, validity_column, validity_condition, validity_value)
                total_rows = len(data)
                passed_rows = int(total_rows * percent / 100)
                failed_rows = total_rows - passed_rows
                summary_data = [{
                    "Column": validity_column,
                    "Passed (%)": f"{percent:.2f}",
                    "Failed (%)": f"{100 - percent:.2f}",
                    "Rows Passed": passed_rows,
                    "Rows Failed": failed_rows
                }]
                st.success(f"Validity for column '{validity_column}' with condition '{validity_condition}': {percent:.2f}%")
                st.markdown("##### Validity Detail: Data Format & Rule Breakdown")
                st.table(pd.DataFrame(summary_data))
    else:
        st.info("Please upload a CSV file to get started.")

def main():
    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if st.session_state.page == "landing":
        landing_page()
    elif st.session_state.page == "data_quality":
        data_quality_page()

if __name__ == "__main__":
    main()