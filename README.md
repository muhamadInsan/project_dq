# Streamlit Project Data Quality

This project is a simple Streamlit application that allows users to upload a CSV file and display its contents in a tabular format. 

## Project Structure

```
app
├── src
│   ├── app.py
│   └── utils
│       └── csv_utils.py
├── requirements.txt
└── README.md
```

## Requirements

To run this project, you need to have Python installed on your machine. You can install the required packages using the following command:

```
pip install -r requirements.txt
```

## Running the Application

To start the Streamlit application, navigate to the `src` directory and run the following command:

```
streamlit run app/src/app.py
```

Once the application is running, you can upload a CSV file using the provided interface, and the data will be displayed in a table format.

## Features

- Upload and preview CSV files in a tabular format.
- Select a data quality dimension to assess via a dropdown:
  - **Completeness** (officially ready)
  - **Uniqueness** (officially ready)
  - Accuracy
  - Timeliness
  - Consistency
  - Validity
- Visualize column completeness as a table and bar chart.

## How to Run

rom the project root, run:

```
streamlit run app/src/app.py
```