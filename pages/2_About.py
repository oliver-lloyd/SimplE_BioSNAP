import streamlit as st


# Header
st.title('SimplE embeddings of BioSNAP drugs')

# Body
st.subheader('About:')
st.write('Online explorer for the data from our recent research. The paper is currently under review but a preprint is available at https://arxiv.org/abs/2404.11374')

st.subheader('Sources:')
st.link_button('- BioSNAP dataset', 'http://snap.stanford.edu/decagon')
#st.link_button('- Decagon paper', 'https://doi.org/10.1093/bioinformatics/bty294')
st.link_button('- LibKGE', 'https://github.com/uma-pi1/kge')
st.link_button('- SimplE paper', 'https://doi.org/10.48550/arXiv.1802.04868')
st.write('')

st.subheader('Contact:')
st.write('- oliver.lloyd@bristol.ac.uk')
st.write('- https://github.com/oliver-lloyd')
