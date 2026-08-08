import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(page_title="Smart Dynamic Dashboard", layout="wide")
st.title("📊 Smart Dynamic Dashboard")


# ----------------------------
# Functions
# ----------------------------

def load_data(uploaded_file):
    """Load CSV file safely."""
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None


def show_preview(df):
    """Show first rows of dataset."""
    st.subheader("📄 Data Preview")
    st.dataframe(df)


def show_statistics(df, column):
    """Show statistics."""
    st.subheader("📈 Statistics")
    st.write(df[column].describe())


def draw_chart(df, chart_type, x_col, y_col):
    """Draw selected chart."""

    # Prepare data once (DRY Principle)
    chart_data = df.set_index(x_col)[[y_col]]

    st.subheader("📊 Visualization")

    if chart_type == "Bar Chart":
        st.bar_chart(chart_data)

    elif chart_type == "Line Chart":
        st.line_chart(chart_data)

    elif chart_type == "Scatter Chart":
        st.scatter_chart(df, x=x_col, y=y_col)

    elif chart_type == "Pie Chart":

        pie_data = df.groupby(x_col)[y_col].sum()

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.pie(
            pie_data,
            labels=pie_data.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(y_col)

        st.pyplot(fig)


# ----------------------------
# Upload File
# ----------------------------

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:

    df = load_data(uploaded_file)

    if df is not None:

        show_preview(df)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns found.")
            st.stop()

        # ----------------------------
        # Sidebar
        # ----------------------------

        st.sidebar.header("⚙ Dashboard Controls")

        chart_type = st.sidebar.selectbox(
            "Chart Type",
            [
                "Bar Chart",
                "Line Chart",
                "Scatter Chart",
                "Pie Chart"
            ]
        )

        x_col = st.sidebar.selectbox(
            "Select X-axis",
            df.columns
        )

        y_col = st.sidebar.selectbox(
            "Select Y-axis",
            numeric_cols
        )

        # ----------------------------
        # Output
        # ----------------------------

        show_statistics(df, y_col)

        draw_chart(df, chart_type, x_col, y_col)
