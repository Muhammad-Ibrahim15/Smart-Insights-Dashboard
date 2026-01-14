import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# PAGE CONFIG
st.set_page_config(
    page_title="Smart Insights Dashboard",
    layout="wide"
)


# CUSTOM CSS (COLORFUL & UNIQUE)

st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}
.big-title {
    font-size: 38px;
    font-weight: 700;
    color: #2c3e50;
}
.section {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 25px;
}
.sub-title {
    color: #6c5ce7;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# TITLE

st.markdown('<div class="big-title"> Smart Insights Dashboard</div>', unsafe_allow_html=True)
st.write("A clean, interactive and student-built data analysis dashboard")

# FILE UPLOAD

uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

 
    # DATA PREVIEW

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">🔍 Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head())
    st.markdown('</div>', unsafe_allow_html=True)

    # DATA SUMMARY
   
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">🧠 Dataset Summary</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", df.isnull().sum().sum())

    st.markdown('</div>', unsafe_allow_html=True)

    # DATA CLEANING
   
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">🧹 Data Cleaning</div>', unsafe_allow_html=True)

    clean_df = df.copy()

    option = st.selectbox(
        "Choose missing value handling method",
        ["Do Nothing", "Drop Rows", "Fill with Mean", "Fill with Median", "Fill with Mode"]
    )

    if option == "Drop Rows":
        clean_df.dropna(inplace=True)

    elif option == "Fill with Mean":
        for col in numeric_cols:
            clean_df[col] = clean_df[col].fillna(clean_df[col].mean())

    elif option == "Fill with Median":
        for col in numeric_cols:
            clean_df[col] = clean_df[col].fillna(clean_df[col].median())

    elif option == "Fill with Mode":
        for col in clean_df.columns:
            clean_df[col] = clean_df[col].fillna(clean_df[col].mode()[0])

    if st.checkbox("Remove duplicate rows"):
        clean_df.drop_duplicates(inplace=True)

    st.dataframe(clean_df.head())
    st.markdown('</div>', unsafe_allow_html=True)

   
    # EDA
  
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">📈 Exploratory Data Analysis</div>', unsafe_allow_html=True)

    st.dataframe(clean_df.describe())

    if numeric_cols:
        col = st.selectbox("Select numeric column for histogram", numeric_cols)
        fig, ax = plt.subplots()
        ax.hist(clean_df[col].dropna(), bins=20)
        st.pyplot(fig)

        col2 = st.selectbox("Select numeric column for box plot", numeric_cols)
        fig2, ax2 = plt.subplots()
        ax2.boxplot(clean_df[col2].dropna())
        st.pyplot(fig2)

    if categorical_cols:
        cat = st.selectbox("Select categorical column", categorical_cols)
        vc = clean_df[cat].value_counts()
        fig3, ax3 = plt.subplots()
        ax3.bar(vc.index, vc.values)
        plt.xticks(rotation=45)
        st.pyplot(fig3)

    st.markdown('</div>', unsafe_allow_html=True)

    # FILTERING
    # 
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">🎛️ Data Filtering</div>', unsafe_allow_html=True)

    filtered_df = clean_df.copy()

    if numeric_cols:
        fcol = st.selectbox("Numeric filter column", numeric_cols)
        min_v, max_v = float(filtered_df[fcol].min()), float(filtered_df[fcol].max())
        rng = st.slider("Select range", min_v, max_v, (min_v, max_v))
        filtered_df = filtered_df[(filtered_df[fcol] >= rng[0]) & (filtered_df[fcol] <= rng[1])]

    if categorical_cols:
        fcat = st.selectbox("Categorical filter column", categorical_cols)
        vals = st.multiselect("Select values", filtered_df[fcat].unique())
        if vals:
            filtered_df = filtered_df[filtered_df[fcat].isin(vals)]

    st.dataframe(filtered_df.head())
    st.markdown('</div>', unsafe_allow_html=True)

    # DOWNLOAD

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">⬇️ Download Results</div>', unsafe_allow_html=True)

    st.download_button(
        "Download Cleaned Data",
        clean_df.to_csv(index=False),
        "cleaned_data.csv"
    )

    st.download_button(
        "Download Filtered Data",
        filtered_df.to_csv(index=False),
        "filtered_data.csv"
    )

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 Upload a CSV file to begin analysis")
