import streamlit as st


# Initialize
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
se = st.selectbox('Side effect', emb.rel_index['description'])

for _ in range(gap):
    st.write('')
if drug1 != drug2:
    score = emb.SimplE_scorer(drug1, se, drug2)
    st.divider()
    st.markdown(f'Scoring the side effect "{se}" between drugs "{drug1}" and "{drug2}":')
    st.latex(f'SimplE({drug1}, {se}, {drug2}) =  {score:.3f}')
    st.divider()
else:
    st.subheader('Choose two different drugs to get a score.')