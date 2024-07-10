import streamlit as st
import altair as alt
from pandas import DataFrame


# Initialize
try:
    emb = st.session_state.emb
except AttributeError:
    from simple_biosnap import Embeds
    st.session_state.emb = Embeds()
    emb = st.session_state.emb

# Header
st.title('SimplE polypharmacy side effect scores')

# Body
st.write('\
    This page allows users to calculate edge scores, \
    i.e. model confidence scores of polyparmacy side \
    effects, between any pair of drugs in the dataset. \
')
st.write('\
    Please note that this tool is intended for research \
    purposes only. Consult with a pharmacist if you have \
    any real queries about drug side effects. \
')

gap = 2
for _ in range(gap):
    st.write('')
st.write('Choose two drugs:')
drug1 = st.selectbox('Drug 1', emb.ent_index['Drug'])
drug2 = st.selectbox('Drug 2', emb.ent_index['Drug'])

for _ in range(gap):
    st.write('')
st.write('Choose a side effect')
se_options = ['All'] + emb.rel_index['description'].to_list()
se = st.selectbox('Side effect', se_options)

for _ in range(gap):
    st.write('')
if drug1 != drug2:
    if se != 'All':
        score = emb.SimplE_scorer(drug1, se, drug2)
        st.subheader(f'Scoring the side effect "{se}" between drugs "{drug1}" and "{drug2}":')
        st.divider()
        st.latex(f'SimplE({drug1}, {se}, {drug2})')
        st.latex(f'= {score:.3f}')
        st.divider()
    else:
        scores = [emb.SimplE_scorer(drug1, se_, drug2) for se_ in emb.rel_index.description]
        scores_df = DataFrame()
        scores_df['Model score'] = scores
        scores_df['Side effect'] = emb.rel_index.description

        st.subheader(f'Scoring all side effects between drugs "{drug1}" and "{drug2}":')
        st.divider()
        st.latex(f'SimplE({drug1}, * , {drug2})')
        st.divider()
        st.markdown(
            '<div style="text-align: center;">Scores for all side effects between the chosen drugs. Higher score = more likely.</div>',
            unsafe_allow_html=True
        )
        st.write()

        chart = alt.Chart(scores_df).mark_circle(size=60).encode(
            x='Model score',
            tooltip=['Side effect', 'Model score']
        )
        st.altair_chart(
            chart.interactive(),
            use_container_width=True
        )
        st.divider()
        
else:
    st.subheader('Choose two different drugs to get a score.')