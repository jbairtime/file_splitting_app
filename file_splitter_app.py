import streamlit as st
import pandas as pd

# This app takes a csv file and splits it randomly into two files based on the percentage of rows for file A.
# Can get rid of duplicates and missing values.

st.title("File Splitter")
st.markdown("This app splits a csv file into two files based. Give the percentage of rows for file A, and the rest will go to file B.")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

    percentage = st.slider("Percentage of rows for file A", 0, 100, 50)
    percentage = percentage / 100
    percentage_b = 1 - percentage
    st.write(f"File A will have {percentage:.0%} of the rows, and File B will have {percentage_b:.0%} of the rows.")
    if st.checkbox("Use only unique rows"):
        df = df.drop_duplicates()
    if st.checkbox("Get rid of rows with missing values"):
        df = df.dropna()

    if st.button("Split Files"):
        df_a = df.sample(frac=percentage)
        df_b = df.drop(df_a.index)  

        st.markdown("### Download Files")
        st.markdown("Click below to download the files.")
        
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False)
        
        csv_a = convert_df(df_a)
        csv_b = convert_df(df_b)

        st.download_button("Download File A", csv_a, f"{uploaded_file.name.split('.')[0]}_A.csv", "text/csv")
        st.download_button("Download File B", csv_b, f"{uploaded_file.name.split('.')[0]}_B.csv", "text/csv")