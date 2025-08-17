import streamlit as st
import pandas as pd
from utils.csv_utils import read_csv

def main():
    st.title("CSV Uploader")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        data = read_csv(uploaded_file)
        st.write("Data from the CSV file:")
        st.dataframe(data)

if __name__ == "__main__":
    main()