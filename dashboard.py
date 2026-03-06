import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Data Analytics Dashboard", layout="wide")

st.title("📊 Data Analytics Dashboard")
st.write("Upload a CSV file and visualize your data")

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------
file = st.file_uploader("Upload CSV File", type=["csv"])

# ---------------------------------------------------
# MAIN LOGIC
# ---------------------------------------------------
if file is not None:

    # Read dataset
    data = pd.read_csv(file)

    # Dataset Preview
    st.subheader("Dataset Preview")
    st.dataframe(data.head())

    # ---------------------------------------------------
    # DATASET INFORMATION
    # ---------------------------------------------------
    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    col1.metric("Rows", data.shape[0])
    col1.metric("Columns", data.shape[1])

    col2.write("Column Names")
    col2.write(list(data.columns))

    # ---------------------------------------------------
    # STATISTICS
    # ---------------------------------------------------
    st.subheader("Statistical Summary")
    st.write(data.describe())

    # ---------------------------------------------------
    # VISUALIZATION SECTION
    # ---------------------------------------------------
    st.subheader("📊 Data Visualization")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Line Chart", "Pie Chart", "Histogram", "Scatter Plot", "Box Plot"]
    )

    column1 = st.selectbox("Select First Column", data.columns)

    if chart_type == "Scatter Plot":
        column2 = st.selectbox("Select Second Column", data.columns)

    if st.button("Generate Chart"):

        fig, ax = plt.subplots()

        if chart_type == "Bar Chart":
            data[column1].value_counts().plot(kind="bar", ax=ax)
            ax.set_title("Bar Chart")

        elif chart_type == "Line Chart":
            data[column1].plot(kind="line", ax=ax)
            ax.set_title("Line Chart")

        elif chart_type == "Pie Chart":
            data[column1].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax)
            ax.set_title("Pie Chart")

        elif chart_type == "Histogram":
            data[column1].plot(kind="hist", bins=20, ax=ax)
            ax.set_title("Histogram")

        elif chart_type == "Scatter Plot":
            ax.scatter(data[column1], data[column2])
            ax.set_xlabel(column1)
            ax.set_ylabel(column2)
            ax.set_title("Scatter Plot")

        elif chart_type == "Box Plot":
            data.boxplot(column=column1, ax=ax)
            ax.set_title("Box Plot")

        st.pyplot(fig)

else:
    st.info("Please upload a CSV dataset to begin.")