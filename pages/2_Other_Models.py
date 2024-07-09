import streamlit as st
import pandas as pd


st.title('Other models and their performance on this dataset')
st.write('')
st.write('Please get in touch to report any inaccuracies on this page, or suggest papers I\'ve missed.')

df = pd.read_excel('data/lit/biosnap_papers.xlsx')
st.dataframe(
    df.drop(columns=['Paper']), 
    hide_index=True,
    use_container_width=True
)